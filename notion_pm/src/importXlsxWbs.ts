import * as fs from "fs";
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

const PARENT_TEMPLATE_PATH = process.env.PARENT_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/parent-template.json");
const CHILD_TEMPLATE_PATH = process.env.CHILD_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/child-template.json");

const PARENT_ICON = {
  type: "external" as const,
  external: { url: "https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f48e.svg" },
};

// ---------------------------------------------------------------------------
// テンプレート型定義
// ---------------------------------------------------------------------------

interface TemplateSection {
  _section: string;
  _upsert_mode: "overwrite" | "append" | "skip";
  blocks: unknown[];
}

function loadTemplate(filePath: string): TemplateSection[] {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf-8")) as TemplateSection[];
  } catch {
    console.warn(`Template not found or invalid: ${filePath}. Using empty body.`);
    return [];
  }
}

// ---------------------------------------------------------------------------
// Notion ブロック操作ヘルパー
// ---------------------------------------------------------------------------

type BlockObject = { id: string; type: string; [key: string]: unknown };

/** 既存ページのブロックを全件取得（ページネーション対応） */
async function fetchAllBlocks(client: Client, pageId: string): Promise<BlockObject[]> {
  const blocks: BlockObject[] = [];
  let cursor: string | undefined;

  do {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const res: any = await client.blocks.children.list({
      block_id: pageId,
      ...(cursor ? { start_cursor: cursor } : {}),
    });
    blocks.push(...(res.results as BlockObject[]));
    cursor = res.has_more ? res.next_cursor : undefined;
  } while (cursor);

  return blocks;
}

/** ブロックが heading_2 かつ指定テキストに一致するか */
function matchesHeading(block: BlockObject, text: string): boolean {
  if (block.type !== "heading_2") return false;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const richText: any[] = (block["heading_2"] as any)?.rich_text ?? [];
  return richText.map((r) => r.text?.content ?? "").join("") === text;
}

/** 見出しブロック（heading_1/2/3）か判定 */
function isHeadingBlock(block: BlockObject): boolean {
  return block.type === "heading_1" || block.type === "heading_2" || block.type === "heading_3";
}

/**
 * upsert 時にテンプレートセクションをページに適用する。
 *
 * - overwrite: 既存の見出し配下のコンテンツブロックを削除し、テンプレートのコンテンツを挿入
 * - append:    既存セクション末尾にテンプレートのコンテンツを追記
 * - skip:      何もしない（手動編集を保護）
 * - 見出しが存在しない場合: セクション全体（見出し＋コンテンツ）をページ末尾に追加
 */
async function applyTemplateSections(
  client: Client,
  pageId: string,
  sections: TemplateSection[],
  taskName: string,
): Promise<void> {
  for (const section of sections) {
    if (section._upsert_mode === "skip") continue;

    console.log(`  [template] page="${taskName}" section="${section._section}" mode=${section._upsert_mode}`);

    let allBlocks: BlockObject[];
    try {
      allBlocks = await fetchAllBlocks(client, pageId);
    } catch (e: unknown) {
      console.error(`  [template] ERROR fetchAllBlocks page="${taskName}" section="${section._section}":`, (e as Error).message);
      continue;
    }

    const headingIndex = allBlocks.findIndex((b) => matchesHeading(b, section._section));
    const contentBlocks = section.blocks.slice(1);

    if (headingIndex === -1) {
      // 見出しが存在しない → セクション全体をページ末尾に追加
      if (section.blocks.length > 0) {
        try {
          console.log(`  [template]   heading not found → append section to page end`);
          await client.blocks.children.append({
            block_id: pageId,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            children: section.blocks as any,
          });
        } catch (e: unknown) {
          console.error(`  [template] ERROR append(missing heading) page="${taskName}" section="${section._section}":`, (e as Error).message);
        }
      }
      continue;
    }

    const contentStart = headingIndex + 1;
    let contentEnd = allBlocks.length;
    for (let i = contentStart; i < allBlocks.length; i++) {
      if (isHeadingBlock(allBlocks[i])) {
        contentEnd = i;
        break;
      }
    }
    const existingContentBlocks = allBlocks.slice(contentStart, contentEnd);
    console.log(`  [template]   heading found at idx=${headingIndex}, existing content blocks=${existingContentBlocks.length}, template content blocks=${contentBlocks.length}`);

    if (section._upsert_mode === "overwrite") {
      const updateCount = Math.min(existingContentBlocks.length, contentBlocks.length);

      for (let i = 0; i < updateCount; i++) {
        const tmpl = contentBlocks[i] as any;
        try {
          console.log(`  [template]   blocks.update blockId=${existingContentBlocks[i].id} type=${tmpl.type}`);
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          await (client.blocks.update as any)({
            block_id: existingContentBlocks[i].id,
            [tmpl.type]: tmpl[tmpl.type],
          });
        } catch (e: unknown) {
          console.error(`  [template] ERROR blocks.update page="${taskName}" section="${section._section}" i=${i}:`, (e as Error).message);
        }
      }

      for (let i = updateCount; i < existingContentBlocks.length; i++) {
        try {
          console.log(`  [template]   blocks.delete blockId=${existingContentBlocks[i].id}`);
          await client.blocks.delete({ block_id: existingContentBlocks[i].id });
        } catch (e: unknown) {
          console.error(`  [template] ERROR blocks.delete page="${taskName}" section="${section._section}" i=${i}:`, (e as Error).message);
        }
      }

      if (contentBlocks.length > existingContentBlocks.length) {
        const extras = contentBlocks.slice(existingContentBlocks.length);
        try {
          console.log(`  [template]   append ${extras.length} extra blocks to page end`);
          await client.blocks.children.append({
            block_id: pageId,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            children: extras as any,
          });
        } catch (e: unknown) {
          console.error(`  [template] ERROR append(extras) page="${taskName}" section="${section._section}":`, (e as Error).message);
        }
      }
    } else if (section._upsert_mode === "append") {
      const templateTable = (contentBlocks as any[]).find((b) => b.type === "table");
      const existingTable = existingContentBlocks.find((b) => b.type === "table");

      if (templateTable && existingTable) {
        const rows = templateTable.table?.children ?? [];
        if (rows.length > 0) {
          try {
            console.log(`  [template]   append ${rows.length} rows to table blockId=${existingTable.id}`);
            await client.blocks.children.append({
              block_id: existingTable.id,
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              children: rows as any,
            });
          } catch (e: unknown) {
            console.error(`  [template] ERROR append(table rows) page="${taskName}" section="${section._section}":`, (e as Error).message);
          }
        }
      } else if (contentBlocks.length > 0) {
        // セクション末尾（最後の既存ブロック or 見出しブロック）の後に挿入
        const afterId =
          existingContentBlocks.length > 0
            ? existingContentBlocks[existingContentBlocks.length - 1].id
            : allBlocks[headingIndex].id;
        try {
          console.log(`  [template]   append ${contentBlocks.length} blocks after blockId=${afterId}`);
          await client.blocks.children.append({
            block_id: pageId,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            children: contentBlocks as any,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            after: afterId as any,
          });
        } catch (e: unknown) {
          console.error(`  [template] ERROR append(content) page="${taskName}" section="${section._section}":`, (e as Error).message);
        }
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Excel 読み込み
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// Notion upsert
// ---------------------------------------------------------------------------

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
 * - タイトルが既存ページと完全一致する場合は更新（pages.update）し、テンプレートセクションを適用
 * - 一致しない場合は新規作成（pages.create）し、全セクションを children として渡す
 * - 子タスクには term マップから期間・工数プロパティを設定する。
 * - 親タスク（工程）にはアイコンを設定する。
 */
async function upsertXlsxTasks(
  client: Client,
  databaseId: string,
  tasks: WBSTask[],
  termMap: Map<string, TermEntry>,
  existingTitles: Map<string, string>,
  parentTemplate: TemplateSection[],
  childTemplate: TemplateSection[],
): Promise<{ created: number; updated: number }> {
  let created = 0;
  let updated = 0;

  const upsertRecursive = async (task: WBSTask, parentPageId: string | null): Promise<void> => {
    const properties: Record<string, unknown> = {
      title: { title: [{ text: { content: task.name } }] },
    };

    // 親タスク Relation: 子タスクは親ページを設定、親タスクは明示的にクリア
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
    const template = isParent ? parentTemplate : childTemplate;
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
      // テンプレートセクションを適用（skip 以外）
      await applyTemplateSections(client, page.id, template, task.name);
    } else {
      // 未一致 → 新規作成（全セクションの blocks を結合して children に渡す）
      const allBlocks = template.flatMap((s) => s.blocks);
      page = await client.pages.create({
        parent: { database_id: databaseId },
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        properties: properties as any,
        ...(isParent && { icon: PARENT_ICON }),
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ...(allBlocks.length > 0 && { children: allBlocks as any }),
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
    try {
      await upsertRecursive(task, null);
    } catch (e: unknown) {
      console.error(`[upsert] ERROR task="${task.name}":`, (e as Error).message);
    }
  }
  return { created, updated };
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

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

  const parentTemplate = loadTemplate(PARENT_TEMPLATE_PATH);
  const childTemplate  = loadTemplate(CHILD_TEMPLATE_PATH);
  console.log(`Parent template sections: ${parentTemplate.length}`);
  console.log(`Child template sections: ${childTemplate.length}`);

  console.log(`\nFetching existing pages from Notion database: ${DATABASE_ID}`);
  const existingTitles = await fetchExistingTitles(client, DATABASE_ID);
  console.log(`Found ${existingTitles.size} existing pages`);

  console.log("Upserting tasks...");
  const { created, updated } = await upsertXlsxTasks(client, DATABASE_ID, tasks, termMap, existingTitles, parentTemplate, childTemplate);
  console.log(`Done. Created ${created}, updated ${updated} tasks.`);
}

main().catch((err) => {
  console.error("Fatal error:", err instanceof Error ? err.message : err);
  process.exit(1);
});
