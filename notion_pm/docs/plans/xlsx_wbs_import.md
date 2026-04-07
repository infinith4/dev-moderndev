# Plan: ExcelファイルからNotionへのWBSインポート

## Context
Excelファイル `docs/template-development-wbs.xlsx` から以下2シートを読み取り、
Notion データベースに2階層のタスク（親タスク → 子タスク）として登録する。

| シート | 使用列 | 用途 |
|---|---|---|
| wbs | E列: 工程 / F列: タスク | 親子タスクの構造 |
| term | B列: タスク名（マッチキー）/ C列: 開始日 / D列: 終了日 / E列: 対応工数(D) | 子タスクの期間・工数 |

**マッチング:** wbs F列の値 == term B列の値（完全一致）

`wbsImporter.ts` の `createNotionTasks` は親 Relation の設定に対応していないため、
期間・工数プロパティを含む独自の `createXlsxTasks` 関数を `importXlsxWbs.ts` 内に実装する。

---

## 実装内容

### 1. `xlsx` パッケージのインストール
```bash
cd /src/notion_pm && npm install xlsx
```

### 2. 新規ファイル: `src/importXlsxWbs.ts`

#### 定数・型定義
```typescript
import * as path from "path";
import * as XLSX from "xlsx";
import { Client } from "@notionhq/client";
import dotenv from "dotenv";
import { createNotionClient, type WBSTask } from "./notionClient";  // createNotionClient のみ流用
// ※ WBSTask は wbsImporter.ts からインポート
import type { WBSTask } from "./wbsImporter";

dotenv.config();

const XLSX_PATH    = path.resolve(__dirname, "../docs/template-development-wbs.xlsx");
const DATABASE_ID  = process.env.NOTION_DATABASE_ID  ?? "332f76ee7f8680e5b459ea9e58da4e7f";
const PARENT_PROP  = process.env.PARENT_RELATION_PROP ?? "親タスク";
const PERIOD_PROP  = process.env.PERIOD_PROP          ?? "期間";
const EFFORT_PROP  = process.env.EFFORT_PROP          ?? "工数";
const DRY_RUN      = process.argv.includes("--dry-run");

interface TermEntry {
  startDate: string; // "YYYY-MM-DD"
  endDate:   string;
  effort:    number;
}
```

#### term シート読み込み
```typescript
function readTermSheet(filePath: string): Map<string, TermEntry> {
  const wb = XLSX.readFile(filePath, { cellDates: true });
  const ws = wb.Sheets["term"];
  if (!ws) return new Map();

  const rows = XLSX.utils.sheet_to_json<unknown[]>(ws, { header: 1 });
  const map = new Map<string, TermEntry>();

  for (const row of rows.slice(1) as unknown[][]) {
    const taskName  = (row[1] ?? "").toString().trim(); // B列
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
```

#### wbs シート読み込み（F列の元値を details に保存）
```typescript
// COL_PARENT = 4 (E列), COL_CHILD = 5 (F列)
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
        details: { _originalTaskName: childRaw }, // term とのマッチングに使用
        children: [],
      });
    }
  }
  return parentTasks;
}
```

#### Notion タスク作成（期間・工数プロパティを含む）
```typescript
// wbsImporter.ts の createNotionTasks は期間/工数プロパティに未対応のため独自実装
async function createXlsxTasks(
  client: Client,
  databaseId: string,
  tasks: WBSTask[],
  termMap: Map<string, TermEntry>
): Promise<number> {
  let created = 0;

  const createRecursive = async (task: WBSTask, parentPageId: string | null) => {
    const properties: Record<string, unknown> = {
      title: { title: [{ text: { content: task.name } }] },
    };

    // 親タスク Relation
    if (PARENT_PROP && parentPageId) {
      properties[PARENT_PROP] = { relation: [{ id: parentPageId }] };
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

    const page = await client.pages.create({
      parent: { database_id: databaseId },
      properties,
    });

    task.notionPageId = page.id;
    created++;

    for (const child of task.children) {
      await createRecursive(child, page.id);
    }
  };

  for (const task of tasks) {
    await createRecursive(task, null);
  }
  return created;
}
```

#### main 関数
```typescript
async function main() {
  const apiKey = process.env.NOTION_API_KEY;
  if (!apiKey) { console.error("NOTION_API_KEY not set"); process.exit(1); }

  const tasks   = parseXlsxWbs(XLSX_PATH);
  const termMap = readTermSheet(XLSX_PATH);

  const totalChildren = tasks.reduce((s, t) => s + t.children.length, 0);
  const matched = tasks.flatMap(t => t.children)
    .filter(c => termMap.has(c.details["_originalTaskName"] ?? "")).length;
  console.log(`Parsed ${tasks.length} parent tasks, ${totalChildren} child tasks`);
  console.log(`Term matched: ${matched} / ${totalChildren} child tasks`);

  if (DRY_RUN) {
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
    return;
  }

  const client  = createNotionClient(apiKey);
  const created = await createXlsxTasks(client, DATABASE_ID, tasks, termMap);
  console.log(`Done. Created ${created} tasks.`);
}

main().catch(err => { console.error(err); process.exit(1); });
```

---

### 3. `package.json` の変更

**`dependencies`** に追加:
```json
"xlsx": "^0.18.5"
```

**`scripts`** に追加:
```json
"import-xlsx-wbs": "ts-node src/importXlsxWbs.ts"
```

### 4. `.env` に追加
```
NOTION_DATABASE_ID=332f76ee7f8680e5b459ea9e58da4e7f
```

### 5. `.env.example` に追加
```
NOTION_DATABASE_ID=your_notion_database_id
PARENT_RELATION_PROP=親タスク
PERIOD_PROP=期間
EFFORT_PROP=工数
```

---

## 変更対象ファイル

| ファイル | 変更種別 |
|---|---|
| `src/importXlsxWbs.ts` | **新規作成** |
| `package.json` | xlsx 追加、スクリプト追加 |
| `.env` | DATABASE_ID 追加 |
| `.env.example` | 変数ドキュメント追加 |
| `src/wbsImporter.ts` | **変更なし** |

---

## 動作確認

### 1. Dry run（Notion への書き込みなし）
```bash
cd /src/notion_pm
npm run import-xlsx-wbs -- --dry-run
```

期待出力例:
```
Parsed 8 parent tasks, 31 child tasks
Term matched: 31 / 31 child tasks
  [親] 要件定義
    [子] ヒアリング・現状分析-現状ヒアリングMTG設定 [期間: 2026-02-02〜2026-02-06, 工数: 4d]
    [子] 業務フロー作成-業務フロー作成 [期間: 2026-02-06〜2026-02-12, 工数: 2d]
    ...
  [親] 基本設計
    ...
```

確認ポイント:
- 親タスクが重複なく出力される
- 子タスクのタイトルに `{親タスク名}-` 接頭辞が含まれない
- term 一致件数が正しい（全 31 件一致が期待値）

### 2. 実登録
```bash
cd /src/notion_pm
npm run import-xlsx-wbs
```

Notion データベースで確認:
- 親タスク 8 件が作成されている
- 子タスクに `親タスク` Relation が設定されている
- 子タスクに `期間`（開始日〜終了日）が設定されている
- 子タスクに `工数`（数値）が設定されている
