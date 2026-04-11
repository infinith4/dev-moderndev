/**
 * syncTaskBodies.ts
 *
 * Notion データベース上のページボディを docs/task-bodies/ 配下の Markdown に同期する。
 * Excel には依存せず、Notion → Markdown の一方向同期を行う独立スクリプト。
 *
 * ディレクトリ規則:
 *   task-bodies/{parentName}.md          → 親タスク
 *   task-bodies/{parentName}/{name}.md   → 子タスク
 *
 * 状態ファイル: docs/task-bodies/.sync-state.json
 *   task key → Notion page ID のキャッシュ
 *
 * Usage:
 *   npm run import-notion-markdown
 *   npm run import-notion-markdown -- --dry-run
 */

import * as fs from "fs";
import * as path from "path";
import dotenv from "dotenv";
import {
  createNotionClient,
  DatabasePageEntry,
  getDatabasePagesByDatabaseId,
} from "./notionClient";
import {
  extractTemplateSectionsFromBlocks,
  fetchAllBlocks,
  loadTemplate,
  serializeBlocksToMarkdown,
  TemplateSection,
} from "./notionBodyUtils";

dotenv.config();

const DATABASE_ID = process.env.NOTION_DATABASE_ID ?? "";
const PARENT_RELATION_PROP = process.env.PARENT_RELATION_PROP ?? "親タスク";
const TASK_BODIES_DIR = process.env.TASK_BODIES_DIR
  ?? path.resolve(__dirname, "../docs/task-bodies");
const PARENT_TEMPLATE_PATH = process.env.PARENT_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/parent-template.json");
const CHILD_TEMPLATE_PATH = process.env.CHILD_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/child-template.json");
const SYNC_STATE_PATH = path.join(TASK_BODIES_DIR, ".sync-state.json");
const DRY_RUN = process.argv.includes("--dry-run");

type SyncState = Record<string, string>;

interface ResolvedTaskPath {
  key: string;
  filePath: string;
  isParent: boolean;
}

function loadSyncState(): SyncState {
  if (!fs.existsSync(SYNC_STATE_PATH)) return {};
  try {
    return JSON.parse(fs.readFileSync(SYNC_STATE_PATH, "utf-8")) as SyncState;
  } catch {
    return {};
  }
}

function saveSyncState(state: SyncState): void {
  fs.mkdirSync(TASK_BODIES_DIR, { recursive: true });
  fs.writeFileSync(SYNC_STATE_PATH, JSON.stringify(state, null, 2), "utf-8");
}

function buildPageIdToKeyMap(state: SyncState): Map<string, string> {
  const map = new Map<string, string>();

  for (const [key, pageId] of Object.entries(state)) {
    if (!pageId || map.has(pageId)) continue;
    map.set(pageId, key);
  }

  return map;
}

function getRelationPageIds(prop: unknown): string[] {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const relation = (prop as any)?.relation;
  if (!Array.isArray(relation)) return [];
  return relation
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    .map((item: any) => String(item?.id ?? ""))
    .filter((id) => !!id);
}

function resolveTaskPathFromKey(key: string): ResolvedTaskPath {
  const parts = key.split("/");
  if (parts.length === 1) {
    return {
      key,
      filePath: path.join(TASK_BODIES_DIR, `${parts[0]}.md`),
      isParent: true,
    };
  }

  const [parentName, ...rest] = parts;
  const childName = rest.join("/");

  return {
    key,
    filePath: path.join(TASK_BODIES_DIR, parentName, `${childName}.md`),
    isParent: false,
  };
}

function resolveTaskPath(
  page: DatabasePageEntry,
  pageById: Map<string, DatabasePageEntry>,
  keyByPageId: Map<string, string>,
): ResolvedTaskPath | null {
  const cachedKey = keyByPageId.get(page.pageId);
  if (cachedKey) {
    return resolveTaskPathFromKey(cachedKey);
  }

  if (!page.title) {
    console.warn(`  [sync] WARN: Untitled page skipped (page=${page.pageId})`);
    return null;
  }

  const parentIds = getRelationPageIds(page.properties[PARENT_RELATION_PROP]);
  if (parentIds.length === 0) {
    return resolveTaskPathFromKey(page.title);
  }

  if (parentIds.length > 1) {
    console.warn(
      `  [sync] WARN: Multiple parent relations found for "${page.title}" (page=${page.pageId}). Skipping.`
    );
    return null;
  }

  const parentPage = pageById.get(parentIds[0]);
  if (!parentPage?.title) {
    console.warn(
      `  [sync] WARN: Parent page not found for "${page.title}" (page=${page.pageId}). Skipping.`
    );
    return null;
  }

  return resolveTaskPathFromKey(`${parentPage.title}/${page.title}`);
}

async function buildMarkdownDocument(
  client: ReturnType<typeof createNotionClient>,
  template: TemplateSection[],
  pageId: string,
): Promise<string> {
  const blocks = await fetchAllBlocks(client, pageId);
  const sections = extractTemplateSectionsFromBlocks(blocks, template);
  const markdownSections: string[] = [];

  for (const section of template) {
    const content = await serializeBlocksToMarkdown(client, sections.get(section._section) ?? []);
    markdownSections.push(
      content
        ? `## ${section._section}\n\n${content}`
        : `## ${section._section}`
    );
  }

  return `${markdownSections.join("\n\n").trim()}\n`;
}

async function main(): Promise<void> {
  const apiKey = process.env.NOTION_API_KEY;
  if (!apiKey) {
    console.error("ERROR: NOTION_API_KEY is not set");
    process.exit(1);
  }
  if (!DATABASE_ID) {
    console.error("ERROR: NOTION_DATABASE_ID is not set");
    process.exit(1);
  }

  const client = createNotionClient(apiKey);
  const parentTemplate = loadTemplate(PARENT_TEMPLATE_PATH);
  const childTemplate = loadTemplate(CHILD_TEMPLATE_PATH);
  const state = loadSyncState();
  const keyByPageId = buildPageIdToKeyMap(state);

  console.log(`Fetching pages from Notion database: ${DATABASE_ID}`);
  const pages = await getDatabasePagesByDatabaseId(client, DATABASE_ID);
  console.log(`Found ${pages.length} page(s)`);

  const pageById = new Map(pages.map((page) => [page.pageId, page]));
  const nextState: SyncState = { ...state };
  let synced = 0;
  let skipped = 0;

  for (const page of pages) {
    const resolved = resolveTaskPath(page, pageById, keyByPageId);
    if (!resolved) {
      skipped++;
      continue;
    }

    const template = resolved.isParent ? parentTemplate : childTemplate;
    nextState[resolved.key] = page.pageId;

    if (DRY_RUN) {
      console.log(`  ${resolved.isParent ? "[親]" : "[子]"} ${resolved.key} -> ${resolved.filePath}`);
      synced++;
      continue;
    }

    console.log(`\n[sync] Exporting "${resolved.key}" from page=${page.pageId}`);
    const markdown = await buildMarkdownDocument(client, template, page.pageId);

    fs.mkdirSync(path.dirname(resolved.filePath), { recursive: true });
    fs.writeFileSync(resolved.filePath, markdown, "utf-8");
    synced++;
  }

  if (!DRY_RUN) {
    saveSyncState(nextState);
  }

  console.log(`\nDone. Synced ${synced}, skipped ${skipped}.`);
  if (DRY_RUN) {
    console.log("Dry run complete. Remove --dry-run to write Markdown files.");
  }
}

main().catch((err) => {
  console.error("Fatal error:", err instanceof Error ? err.message : err);
  process.exit(1);
});
