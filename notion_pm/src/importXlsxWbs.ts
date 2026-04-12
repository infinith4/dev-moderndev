import * as fs from "fs";
import * as path from "path";
import ExcelJS from "exceljs";
import { Client } from "@notionhq/client";
import dotenv from "dotenv";
import { createNotionClient, getPagesByDatabaseId } from "./notionClient";
import type { WBSTask } from "./wbsImporter";
import {
  TemplateSection,
  loadTemplate,
  loadParentMarkdownSections as _loadParentMd,
  loadChildMarkdownSections as _loadChildMd,
  buildBodyBlocks,
  applyTemplateSections as _applyTemplateSections,
} from "./notionBodyUtils";

dotenv.config();

const XLSX_PATH   = path.resolve(__dirname, "../docs/template-development-wbs.xlsx");
const DATABASE_ID = process.env.NOTION_DATABASE_ID  ?? "332f76ee7f8680e5b459ea9e58da4e7f";
const PARENT_PROP   = process.env.PARENT_RELATION_PROP   ?? "親タスク";
const CHILDREN_PROP = process.env.CHILDREN_RELATION_PROP ?? "子タスク";
const PERIOD_PROP   = process.env.PERIOD_PROP             ?? "期間";
const EFFORT_PROP   = process.env.EFFORT_PROP             ?? "工数";
const DRY_RUN     = process.argv.includes("--dry-run");

const OVERWRITE_PERIOD            = process.env.OVERWRITE_PERIOD            !== "false";
const OVERWRITE_EFFORT            = process.env.OVERWRITE_EFFORT            !== "false";
const OVERWRITE_PARENT_RELATION   = process.env.OVERWRITE_PARENT_RELATION   !== "false";
const OVERWRITE_CHILDREN_RELATION = process.env.OVERWRITE_CHILDREN_RELATION !== "false";

const PARENT_TEMPLATE_PATH = process.env.PARENT_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/parent-template.json");
const CHILD_TEMPLATE_PATH = process.env.CHILD_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/child-template.json");
const TASK_BODIES_DIR = process.env.TASK_BODIES_DIR
  ?? path.resolve(__dirname, "../docs/task-bodies");

const PARENT_ICON = {
  type: "external" as const,
  external: { url: "https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f48e.svg" },
};

// notionBodyUtils.ts から全共通ヘルパーを import 済み。
// ローカルラッパー: TASK_BODIES_DIR を束縛して引数を省略できるようにする。

function loadParentMarkdownSections(parentName: string): Map<string, unknown[]> | null {
  return _loadParentMd(TASK_BODIES_DIR, parentName);
}

function loadChildMarkdownSections(
  parentName: string,
  originalTaskName: string
): Map<string, unknown[]> | null {
  return _loadChildMd(TASK_BODIES_DIR, parentName, originalTaskName);
}

async function applyTemplateSections(
  client: Client,
  pageId: string,
  sections: TemplateSection[],
  taskName: string,
  mdSections: Map<string, unknown[]> | null,
): Promise<void> {
  return _applyTemplateSections(client, pageId, sections, taskName, mdSections);
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
async function readTermSheet(filePath: string): Promise<Map<string, TermEntry>> {
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(filePath);
  const ws = workbook.getWorksheet("term");
  if (!ws) return new Map();

  const map = new Map<string, TermEntry>();
  ws.eachRow((row, rowNumber) => {
    if (rowNumber === 1) return; // ヘッダー行をスキップ
    // .text はリッチテキスト・数式セルも文字列として返す
    // .value は Date/number をネイティブ型で返す
    const taskName  = row.getCell(2).text.trim(); // B列: 工程
    const startRaw  = row.getCell(3).value;       // C列: 開始日
    const endRaw    = row.getCell(4).value;       // D列: 終了日
    const effortRaw = row.getCell(5).value;       // E列: 対応工数(D)

    if (!taskName) return;

    const effortResolved = resolveCell(effortRaw);
    const effortNum = typeof effortResolved === "number" ? effortResolved : parseFloat(String(effortResolved ?? "")) || 0;
    map.set(taskName, {
      startDate: toIsoDate(startRaw),
      endDate:   toIsoDate(endRaw),
      effort:    effortNum,
    });
  });
  return map;
}

/** ExcelJS の数式セル ({ formula, result }) から実値を取り出す */
function resolveCell(value: unknown): unknown {
  if (value !== null && typeof value === "object" && "result" in (value as object)) {
    return (value as { result: unknown }).result;
  }
  return value;
}

function toIsoDate(value: unknown): string {
  const v = resolveCell(value);
  if (v instanceof Date) return v.toISOString().split("T")[0];
  if (typeof v === "string") return v;
  return "";
}

/**
 * wbs シートを読み込み、E列(工程)を親タスク・F列(タスク)を子タスクとする
 * WBSTask[] ツリーを返す。
 * 子タスクの details["_originalTaskName"] に F列の元の値を保存（term マッチング用）。
 */
async function parseXlsxWbs(filePath: string): Promise<WBSTask[]> {
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(filePath);
  const ws = workbook.getWorksheet("wbs");
  if (!ws) throw new Error('Sheet "wbs" not found');

  const parentTasks: WBSTask[] = [];
  const parentMap = new Map<string, WBSTask>();

  ws.eachRow((row, rowNumber) => {
    if (rowNumber === 1) return; // ヘッダー行をスキップ
    const parentName = row.getCell(5).text.trim(); // E列
    const childRaw   = row.getCell(6).text.trim(); // F列
    if (!parentName && !childRaw) return;

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
  });
  return parentTasks;
}

// ---------------------------------------------------------------------------
// Notion upsert
// ---------------------------------------------------------------------------

async function fetchExistingTitles(
  client: Client,
  databaseId: string
): Promise<Map<string, string>> {
  const pages = await getPagesByDatabaseId(client, databaseId);
  return new Map(pages.map((p) => [p.title, p.pageId]));
}

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

  const upsertRecursive = async (
    task: WBSTask,
    parentPageId: string | null,
    parentName: string | null,
  ): Promise<void> => {
    const isParent = parentPageId === null;
    const existingPageId = existingTitles.get(task.name);
    const isUpsert = !!existingPageId;

    const properties: Record<string, unknown> = {
      title: { title: [{ text: { content: task.name } }] },
    };

    if (PARENT_PROP) {
      if (!isUpsert || OVERWRITE_PARENT_RELATION) {
        properties[PARENT_PROP] = parentPageId
          ? { relation: [{ id: parentPageId }] }
          : { relation: [] };
      }
    }

    const originalName = task.details["_originalTaskName"];
    if (originalName) {
      const term = termMap.get(originalName);
      if (term) {
        if (term.startDate && (!isUpsert || OVERWRITE_PERIOD)) {
          properties[PERIOD_PROP] = {
            date: { start: term.startDate, end: term.endDate || null },
          };
        }
        if (term.effort > 0 && (!isUpsert || OVERWRITE_EFFORT)) {
          properties[EFFORT_PROP] = { number: term.effort };
        }
      }
    }
    const template = isParent ? parentTemplate : childTemplate;

    // Markdown セクションを読み込む
    let mdSections: Map<string, unknown[]> | null = null;
    if (isParent) {
      mdSections = loadParentMarkdownSections(task.name);
    } else if (parentName) {
      const originalTaskName = task.details["_originalTaskName"] ?? task.name;
      mdSections = loadChildMarkdownSections(parentName, originalTaskName);
    }

    let page;

    if (existingPageId) {
      // 更新: プロパティを更新し、テンプレートセクションを適用
      page = await client.pages.update({
        page_id: existingPageId,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        properties: properties as any,
        ...(isParent && { icon: PARENT_ICON }),
      });
      updated++;
      await applyTemplateSections(client, page.id, template, task.name, mdSections);
    } else {
      // 新規作成: Markdown セクション優先でコンテンツを結合して children に渡す
      const bodyBlocks = buildBodyBlocks(template, mdSections);
      page = await client.pages.create({
        parent: { database_id: databaseId },
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        properties: properties as any,
        ...(isParent && { icon: PARENT_ICON }),
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ...(bodyBlocks.length > 0 && { children: bodyBlocks as any }),
      });
      created++;
    }

    task.notionPageId = page.id;

    // 子タスクを再帰処理（parentName を渡す）
    for (const child of task.children) {
      await upsertRecursive(child, page.id, isParent ? task.name : parentName);
    }

    // 子タスクが存在する場合、親タスクに子タスク Relation を明示セット
    if (CHILDREN_PROP && task.children.length > 0) {
      if (!isUpsert || OVERWRITE_CHILDREN_RELATION) {
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
    }
  };

  for (const task of tasks) {
    try {
      await upsertRecursive(task, null, null);
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
  const tasks   = await parseXlsxWbs(XLSX_PATH);
  const termMap = await readTermSheet(XLSX_PATH);

  const totalChildren = tasks.reduce((s, t) => s + t.children.length, 0);
  const matched = tasks
    .flatMap((t) => t.children)
    .filter((c) => termMap.has(c.details["_originalTaskName"] ?? "")).length;

  console.log(`Parsed ${tasks.length} parent tasks, ${totalChildren} child tasks`);
  console.log(`Term matched: ${matched} / ${totalChildren} child tasks`);

  if (DRY_RUN) {
    console.log(`\nOVERWRITE flags: PERIOD=${OVERWRITE_PERIOD} EFFORT=${OVERWRITE_EFFORT} PARENT_RELATION=${OVERWRITE_PARENT_RELATION} CHILDREN_RELATION=${OVERWRITE_CHILDREN_RELATION}`);
    console.log("\n[DRY RUN] Task tree:");
    for (const p of tasks) {
      const parentMd = fs.existsSync(path.join(TASK_BODIES_DIR, `${p.name}.md`));
      console.log(`  [親] ${p.name}${parentMd ? " [body: md]" : " [body: template]"}`);
      for (const c of p.children) {
        const orig = c.details["_originalTaskName"] ?? "";
        const term = termMap.get(orig);
        const termInfo = term
          ? ` [期間: ${term.startDate}〜${term.endDate}, 工数: ${term.effort}d]`
          : " [term: 未一致]";
        const childMd = fs.existsSync(path.join(TASK_BODIES_DIR, p.name, `${orig}.md`));
        console.log(`    [子] ${c.name}${termInfo}${childMd ? " [body: md]" : " [body: template]"}`);
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
  console.log(`Task bodies dir: ${TASK_BODIES_DIR}`);

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
