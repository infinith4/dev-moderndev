import * as path from "path";
import * as XLSX from "xlsx";
import { Client } from "@notionhq/client";
import dotenv from "dotenv";
import { createNotionClient, getPagesByDatabaseId } from "./notionClient";
import type { WBSTask } from "./wbsImporter";

dotenv.config();

const XLSX_PATH   = path.resolve(__dirname, "../docs/template-development-wbs.xlsx");
const DATABASE_ID = process.env.NOTION_DATABASE_ID  ?? "332f76ee7f8680e5b459ea9e58da4e7f";
const PARENT_PROP   = process.env.PARENT_RELATION_PROP   ?? "親タスク";
const CHILDREN_PROP = process.env.CHILDREN_RELATION_PROP ?? "子タスク";
const PERIOD_PROP   = process.env.PERIOD_PROP             ?? "期間";
const EFFORT_PROP   = process.env.EFFORT_PROP             ?? "工数";
const DRY_RUN     = process.argv.includes("--dry-run");

const PARENT_ICON = {
  type: "external" as const,
  external: { url: "https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f48e.svg" },
};

interface TermEntry {
  startDate: string; // "YYYY-MM-DD"
  endDate:   string;
  effort:    number;
}

/** term シートを読み込み、タスク名 → TermEntry のマップを返す */
function readTermSheet(filePath: string): Map<string, TermEntry> {
  const wb = XLSX.readFile(filePath, { cellDates: true });
  const ws = wb.Sheets["term"];
  if (!ws) return new Map();

  const rows = XLSX.utils.sheet_to_json<unknown[]>(ws, { header: 1 });
  const map = new Map<string, TermEntry>();

  for (const row of rows.slice(1) as unknown[][]) {
    const taskName  = (row[1] ?? "").toString().trim(); // B列: 工程
    const startRaw  = row[2];                           // C列: 開始日
    const endRaw    = row[3];                           // D列: 終了日
    const effortRaw = row[4];                           // E列: 対応工数(D)

    if (!taskName) continue;

    map.set(taskName, {
      startDate: toIsoDate(startRaw),
      endDate:   toIsoDate(endRaw),
      effort:    typeof effortRaw === "number" ? effortRaw : parseFloat(String(effortRaw)) || 0,
    });
  }
  return map;
}

function toIsoDate(value: unknown): string {
  if (value instanceof Date) return value.toISOString().split("T")[0];
  if (typeof value === "string") return value;
  return "";
}

/**
 * wbs シートを読み込み、E列(工程)を親タスク・F列(タスク)を子タスクとする
 * WBSTask[] ツリーを返す。
 * 子タスクの details["_originalTaskName"] に F列の元の値を保存（term マッチング用）。
 */
function parseXlsxWbs(filePath: string): WBSTask[] {
  const wb = XLSX.readFile(filePath);
  const ws = wb.Sheets["wbs"];
  if (!ws) throw new Error('Sheet "wbs" not found');

  const rows = XLSX.utils.sheet_to_json<unknown[]>(ws, { header: 1 });
  const parentTasks: WBSTask[] = [];
  const parentMap = new Map<string, WBSTask>();

  for (const row of rows.slice(1) as unknown[][]) {
    const parentName = (row[4] ?? "").toString().trim(); // E列
    const childRaw   = (row[5] ?? "").toString().trim(); // F列
    if (!parentName && !childRaw) continue;

    if (parentName && !parentMap.has(parentName)) {
      const t: WBSTask = { level: "大項目", name: parentName, details: {}, children: [] };
      parentTasks.push(t);
      parentMap.set(parentName, t);
    }

    if (childRaw && parentName) {
      const prefix    = `${parentName}-`;
      const childName = childRaw.startsWith(prefix) ? childRaw.slice(prefix.length) : childRaw;
      parentMap.get(parentName)!.children.push({
        level: "中項目",
        name: childName,
        details: { _originalTaskName: childRaw },
        children: [],
      });
    }
  }
  return parentTasks;
}

/**
 * Notion データベースの全ページを取得し、タイトル → pageId のマップを返す。
 * タイトルが完全一致する既存ページの upsert 判定に使用する。
 */
async function fetchExistingTitles(
  client: Client,
  databaseId: string
): Promise<Map<string, string>> {
  const pages = await getPagesByDatabaseId(client, databaseId);
  return new Map(pages.map((p) => [p.title, p.pageId]));
}

/**
 * WBSTask ツリーを Notion データベースに upsert する。
 * - タイトルが既存ページと完全一致する場合は更新（pages.update）
 * - 一致しない場合は新規作成（pages.create）
 * - 子タスクには term マップから期間・工数プロパティを設定する。
 * - 親タスク（工程）にはアイコンを設定する。
 */
async function upsertXlsxTasks(
  client: Client,
  databaseId: string,
  tasks: WBSTask[],
  termMap: Map<string, TermEntry>,
  existingTitles: Map<string, string>
): Promise<{ created: number; updated: number }> {
  let created = 0;
  let updated = 0;

  const upsertRecursive = async (task: WBSTask, parentPageId: string | null): Promise<void> => {
    const properties: Record<string, unknown> = {
      title: { title: [{ text: { content: task.name } }] },
    };

    // 親タスク Relation: 子タスクは親ページを設定、親タスクは明示的にクリア
    // （pages.update は PATCH のため、明示的にセットしないと既存値が残る）
    if (PARENT_PROP) {
      properties[PARENT_PROP] = parentPageId
        ? { relation: [{ id: parentPageId }] }
        : { relation: [] };
    }

    // term データから期間・工数を設定（子タスクのみ）
    const originalName = task.details["_originalTaskName"];
    if (originalName) {
      const term = termMap.get(originalName);
      if (term) {
        if (term.startDate) {
          properties[PERIOD_PROP] = {
            date: { start: term.startDate, end: term.endDate || null },
          };
        }
        if (term.effort > 0) {
          properties[EFFORT_PROP] = { number: term.effort };
        }
      }
    }

    const isParent = parentPageId === null;
    const existingPageId = existingTitles.get(task.name);
    let page;

    if (existingPageId) {
      // タイトル完全一致 → 更新
      page = await client.pages.update({
        page_id: existingPageId,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        properties: properties as any,
        ...(isParent && { icon: PARENT_ICON }),
      });
      updated++;
    } else {
      // 未一致 → 新規作成
      page = await client.pages.create({
        parent: { database_id: databaseId },
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        properties: properties as any,
        ...(isParent && { icon: PARENT_ICON }),
      });
      created++;
    }

    task.notionPageId = page.id;

    // 子タスクを再帰処理
    for (const child of task.children) {
      await upsertRecursive(child, page.id);
    }

    // 子タスクが存在する場合、親タスクに子タスク Relation を明示セット
    if (CHILDREN_PROP && task.children.length > 0) {
      const childIds = task.children
        .map((c) => c.notionPageId)
        .filter((id): id is string => !!id);
      if (childIds.length > 0) {
        await client.pages.update({
          page_id: page.id,
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          properties: {
            [CHILDREN_PROP]: { relation: childIds.map((id) => ({ id })) },
          } as any,
        });
      }
    }
  };

  for (const task of tasks) {
    await upsertRecursive(task, null);
  }
  return { created, updated };
}

async function main(): Promise<void> {
  const apiKey = process.env.NOTION_API_KEY;
  if (!apiKey) {
    console.error("ERROR: NOTION_API_KEY is not set");
    process.exit(1);
  }

  console.log(`Reading: ${XLSX_PATH}`);
  const tasks   = parseXlsxWbs(XLSX_PATH);
  const termMap = readTermSheet(XLSX_PATH);

  const totalChildren = tasks.reduce((s, t) => s + t.children.length, 0);
  const matched = tasks
    .flatMap((t) => t.children)
    .filter((c) => termMap.has(c.details["_originalTaskName"] ?? "")).length;

  console.log(`Parsed ${tasks.length} parent tasks, ${totalChildren} child tasks`);
  console.log(`Term matched: ${matched} / ${totalChildren} child tasks`);

  if (DRY_RUN) {
    console.log("\n[DRY RUN] Task tree:");
    for (const p of tasks) {
      console.log(`  [親] ${p.name}`);
      for (const c of p.children) {
        const orig = c.details["_originalTaskName"] ?? "";
        const term = termMap.get(orig);
        const termInfo = term
          ? ` [期間: ${term.startDate}〜${term.endDate}, 工数: ${term.effort}d]`
          : " [term: 未一致]";
        console.log(`    [子] ${c.name}${termInfo}`);
      }
    }
    console.log("\nDry run complete. Remove --dry-run to upsert tasks in Notion.");
    return;
  }

  const client = createNotionClient(apiKey);

  console.log(`\nFetching existing pages from Notion database: ${DATABASE_ID}`);
  const existingTitles = await fetchExistingTitles(client, DATABASE_ID);
  console.log(`Found ${existingTitles.size} existing pages`);

  console.log("Upserting tasks...");
  const { created, updated } = await upsertXlsxTasks(client, DATABASE_ID, tasks, termMap, existingTitles);
  console.log(`Done. Created ${created}, updated ${updated} tasks.`);
}

main().catch((err) => {
  console.error("Fatal error:", err instanceof Error ? err.message : err);
  process.exit(1);
});
