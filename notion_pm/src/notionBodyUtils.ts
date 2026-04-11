import * as fs from "fs";
import * as path from "path";
import { Client } from "@notionhq/client";
import { markdownToBlocks } from "@tryfabric/martian";

// ---------------------------------------------------------------------------
// テンプレート型定義
// ---------------------------------------------------------------------------

export interface TemplateSection {
  _section: string;
  _upsert_mode: "overwrite" | "append" | "skip";
  blocks: unknown[];
}

export function loadTemplate(filePath: string): TemplateSection[] {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf-8")) as TemplateSection[];
  } catch {
    console.warn(`Template not found or invalid: ${filePath}. Using empty body.`);
    return [];
  }
}

// ---------------------------------------------------------------------------
// Markdown ファイル読み込み・セクション分解
// ---------------------------------------------------------------------------

/**
 * Markdown テキストを ## 見出しでセクションに分解し、
 * セクション名 → コンテンツブロック配列 のマップを返す。
 * 見出しブロック自体はマップに含めない（テンプレートの見出しを使うため）。
 */
export function parseMarkdownSections(markdown: string): Map<string, unknown[]> {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const allBlocks = markdownToBlocks(markdown) as any[];
  const sections = new Map<string, unknown[]>();
  let currentSection = "_preamble";
  let currentBlocks: unknown[] = [];

  for (const block of allBlocks) {
    if (block.type === "heading_2") {
      sections.set(currentSection, currentBlocks);
      currentSection = (block.heading_2?.rich_text ?? [])
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .map((r: any) => r.text?.content ?? "")
        .join("");
      currentBlocks = [];
    } else {
      currentBlocks.push(block);
    }
  }
  sections.set(currentSection, currentBlocks);
  return sections;
}

/**
 * 親タスクの Markdown を読み込み、セクションマップを返す。
 * パス: {taskBodiesDir}/{parentName}.md
 */
export function loadParentMarkdownSections(
  taskBodiesDir: string,
  parentName: string
): Map<string, unknown[]> | null {
  const filePath = path.join(taskBodiesDir, `${parentName}.md`);
  if (!fs.existsSync(filePath)) return null;
  console.log(`  [body] Loaded: ${parentName}.md`);
  return parseMarkdownSections(fs.readFileSync(filePath, "utf-8"));
}

/**
 * 子タスクの Markdown を読み込み、セクションマップを返す。
 * パス: {taskBodiesDir}/{parentName}/{originalTaskName}.md
 */
export function loadChildMarkdownSections(
  taskBodiesDir: string,
  parentName: string,
  originalTaskName: string
): Map<string, unknown[]> | null {
  const filePath = path.join(taskBodiesDir, parentName, `${originalTaskName}.md`);
  if (!fs.existsSync(filePath)) return null;
  console.log(`  [body] Loaded: ${parentName}/${originalTaskName}.md`);
  return parseMarkdownSections(fs.readFileSync(filePath, "utf-8"));
}

/**
 * テンプレートセクションと Markdown セクションマップからページ作成用ブロック配列を生成する。
 */
export function buildBodyBlocks(
  template: TemplateSection[],
  mdSections: Map<string, unknown[]> | null
): unknown[] {
  return template.flatMap((s) => {
    const heading = s.blocks[0];
    const content = mdSections?.get(s._section) ?? s.blocks.slice(1);
    return heading ? [heading, ...content] : content;
  });
}

// ---------------------------------------------------------------------------
// Notion ブロック操作ヘルパー
// ---------------------------------------------------------------------------

export type BlockObject = { id: string; type: string; [key: string]: unknown };

/** 既存ページのブロックを全件取得（ページネーション対応） */
export async function fetchAllBlocks(client: Client, pageId: string): Promise<BlockObject[]> {
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
export function matchesHeading(block: BlockObject, text: string): boolean {
  if (block.type !== "heading_2") return false;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const richText: any[] = (block["heading_2"] as any)?.rich_text ?? [];
  return richText.map((r) => r.text?.content ?? "").join("") === text;
}

/** 見出しブロック（heading_1/2/3）か判定 */
export function isHeadingBlock(block: BlockObject): boolean {
  return block.type === "heading_1" || block.type === "heading_2" || block.type === "heading_3";
}

export function extractTemplateSectionsFromBlocks(
  blocks: BlockObject[],
  template: TemplateSection[],
): Map<string, BlockObject[]> {
  const sectionNames = new Set(template.map((section) => section._section));
  const sections = new Map<string, BlockObject[]>();
  let currentSection: string | null = null;

  for (const block of blocks) {
    if (isHeadingBlock(block)) {
      const headingText = getHeadingText(block);
      if (block.type === "heading_2" && headingText && sectionNames.has(headingText)) {
        currentSection = headingText;
        sections.set(currentSection, []);
      } else {
        currentSection = null;
      }
      continue;
    }

    if (currentSection) {
      sections.get(currentSection)?.push(block);
    }
  }

  return sections;
}

function getHeadingText(block: BlockObject): string {
  if (!isHeadingBlock(block)) return "";
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const richText: any[] = (block[block.type] as any)?.rich_text ?? [];
  return richText.map((item) => item.plain_text ?? item.text?.content ?? "").join("");
}

function renderRichText(richText: unknown[]): string {
  return richText
    .map((item) => renderRichTextItem(item))
    .join("");
}

function renderRichTextItem(item: unknown): string {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const textItem = item as any;
  let text = String(textItem?.plain_text ?? textItem?.text?.content ?? "");
  if (!text) return "";

  const href = textItem?.href ?? textItem?.text?.link?.url ?? null;
  if (href) {
    text = `[${text}](${href})`;
  }

  const annotations = textItem?.annotations ?? {};
  if (annotations.code) text = `\`${text}\``;
  if (annotations.bold) text = `**${text}**`;
  if (annotations.italic) text = `*${text}*`;
  if (annotations.strikethrough) text = `~~${text}~~`;
  if (annotations.underline) text = `<u>${text}</u>`;

  return text;
}

function escapeTableCell(text: string): string {
  return text.replace(/\|/g, "\\|").replace(/\n/g, "<br>");
}

async function renderTableBlock(client: Client, block: BlockObject): Promise<string> {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const inlineChildren = (block.table as any)?.children;
  const rowBlocks = Array.isArray(inlineChildren)
    ? (inlineChildren as BlockObject[])
    : await fetchAllBlocks(client, block.id);
  const rows = rowBlocks
    .filter((row) => row.type === "table_row")
    .map((row) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const cells = (row.table_row as any)?.cells ?? [];
      return cells.map((cell: unknown[]) => escapeTableCell(renderRichText(cell)));
    });

  if (rows.length === 0) return "";

  const width = Math.max(...rows.map((row) => row.length));
  const normalizedRows = rows.map((row) => {
    const cloned = row.slice();
    while (cloned.length < width) cloned.push("");
    return cloned;
  });
  const [header, ...bodyRows] = normalizedRows;
  const separator = new Array(width).fill("---");
  const lines = [
    `| ${header.join(" | ")} |`,
    `| ${separator.join(" | ")} |`,
    ...bodyRows.map((row) => `| ${row.join(" | ")} |`),
  ];

  return lines.join("\n");
}

async function renderBlockToMarkdown(client: Client, block: BlockObject): Promise<string> {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const data = (block[block.type] as any) ?? {};
  const richText = Array.isArray(data.rich_text) ? data.rich_text : [];

  switch (block.type) {
    case "paragraph":
      return renderRichText(richText);
    case "bulleted_list_item":
      return `- ${renderRichText(richText)}`.trimEnd();
    case "numbered_list_item":
      return renderRichText(richText);
    case "to_do":
      return `- [${data.checked ? "x" : " "}] ${renderRichText(richText)}`.trimEnd();
    case "quote":
      return renderRichText(richText)
        .split("\n")
        .map((line) => `> ${line}`)
        .join("\n");
    case "code": {
      const content = renderRichText(richText);
      const language = data.language && data.language !== "plain text" ? data.language : "";
      return `\`\`\`${language}\n${content}\n\`\`\``;
    }
    case "divider":
      return "---";
    case "heading_1":
      return `# ${renderRichText(richText)}`;
    case "heading_2":
      return `## ${renderRichText(richText)}`;
    case "heading_3":
      return `### ${renderRichText(richText)}`;
    case "table":
      return renderTableBlock(client, block);
    default:
      console.warn(`  [body] WARN: Unsupported Notion block type skipped: ${block.type}`);
      return "";
  }
}

export async function serializeBlocksToMarkdown(
  client: Client,
  blocks: BlockObject[],
): Promise<string> {
  const chunks: string[] = [];
  const listLines: string[] = [];
  let numberedIndex = 1;

  const flushListLines = (): void => {
    if (listLines.length === 0) return;
    chunks.push(listLines.join("\n"));
    listLines.length = 0;
  };

  for (const block of blocks) {
    if (block.type === "bulleted_list_item") {
      listLines.push(await renderBlockToMarkdown(client, block));
      numberedIndex = 1;
      continue;
    }

    if (block.type === "to_do") {
      listLines.push(await renderBlockToMarkdown(client, block));
      numberedIndex = 1;
      continue;
    }

    if (block.type === "numbered_list_item") {
      const content = await renderBlockToMarkdown(client, block);
      listLines.push(`${numberedIndex}. ${content}`);
      numberedIndex++;
      continue;
    }

    flushListLines();
    numberedIndex = 1;

    const markdown = await renderBlockToMarkdown(client, block);
    if (markdown) {
      chunks.push(markdown);
    }
  }

  flushListLines();

  return chunks.join("\n\n").trim();
}

/**
 * upsert 時にテンプレートセクションをページに適用する。
 *
 * - overwrite: 既存コンテンツを blocks.update で in-place 更新
 * - append（テーブル）: 既存テーブルの block_id に行を追記
 * - append（通常）: 既存セクション末尾の直後（after 指定）にコンテンツを追記
 * - skip: 何もしない（手動編集を保護）
 * - 見出しが存在しない場合: セクション全体をページ末尾に追加
 * - mdSections が指定された場合、コンテンツブロックを Markdown から優先使用する
 */
export async function applyTemplateSections(
  client: Client,
  pageId: string,
  sections: TemplateSection[],
  taskName: string,
  mdSections: Map<string, unknown[]> | null,
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

    const contentBlocks: unknown[] = mdSections?.get(section._section) ?? section.blocks.slice(1);

    if (headingIndex === -1) {
      const heading = section.blocks[0];
      const blocksToAppend = heading ? [heading, ...contentBlocks] : contentBlocks;
      if (blocksToAppend.length > 0) {
        try {
          console.log(`  [template]   heading not found → append section to page end`);
          await client.blocks.children.append({
            block_id: pageId,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            children: blocksToAppend as any,
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
    console.log(`  [template]   heading found at idx=${headingIndex}, existing=${existingContentBlocks.length}, new=${contentBlocks.length}`);

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
        const afterId =
          updateCount > 0
            ? existingContentBlocks[updateCount - 1].id
            : allBlocks[headingIndex].id;
        try {
          console.log(`  [template]   append ${extras.length} extra blocks after blockId=${afterId}`);
          await client.blocks.children.append({
            block_id: pageId,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            children: extras as any,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            after: afterId as any,
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
