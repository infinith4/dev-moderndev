# Plan: WBS インポート時のページボディテンプレート適用

## Context

`npm run import-xlsx-wbs` で Notion にページを作成する際、現在はボディが空になっている。
親タスク・子タスクそれぞれに JSON ファイルで定義したテンプレートブロックをページボディとして設定する。

**方針:**
- テンプレートは JSON ファイルで外部定義（コード変更なしで内容を編集可能）
- 親タスク・子タスクで別々のテンプレートファイル
- **新規作成時のみ**適用（upsert/更新時は既存ボディを変更しない）

---

## 変更対象ファイル

| ファイル | 変更種別 |
|---|---|
| `docs/parent-template.json` | **新規作成** |
| `docs/child-template.json` | **新規作成** |
| `src/importXlsxWbs.ts` | **変更** |
| `.env.example` | **変更**（テンプレートパス変数を追加） |

---

## 実装内容

### 1. テンプレート JSON ファイルの作成

**`docs/parent-template.json`**（工程レベル・親タスク用）

Markdown イメージ:
```markdown
## 目的

**(このフェーズで達成すること)**

## スコープ

**対象**
- 

**対象外**
- 

## 完了条件

**(フェーズ全体の完了基準)**

- 

## 成果物

**(フェーズの主要な成果物)**

- 

## リスク・課題

| # | 内容 | 対応方針 |
|---|---|---|
| 1 | | |
```

Notion ブロック定義:
```json
[
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "目的" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": { "content": "(このフェーズで達成すること)" },
          "annotations": { "bold": true }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "スコープ" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "対応" }, "annotations": { "bold": true } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{ "text": { "content": "対象外" }, "annotations": { "bold": true } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "完了条件" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": { "content": "(フェーズ全体の完了基準)" },
          "annotations": { "bold": true }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "成果物" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": { "content": "(フェーズの主要な成果物)" },
          "annotations": { "bold": true }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "リスク・課題" } }]
    }
  },
  {
    "object": "block",
    "type": "table",
    "table": {
      "table_width": 3,
      "has_column_header": true,
      "has_row_header": false,
      "children": [
        {
          "object": "block",
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "text": { "content": "#" } }],
              [{ "text": { "content": "内容" } }],
              [{ "text": { "content": "対応方針" } }]
            ]
          }
        },
        {
          "object": "block",
          "type": "table_row",
          "table_row": {
            "cells": [
              [{ "text": { "content": "1" } }],
              [{ "text": { "content": "" } }],
              [{ "text": { "content": "" } }]
            ]
          }
        }
      ]
    }
  }
]
```

**`docs/child-template.json`**（タスクレベル・子タスク用）
```json
[
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "タスク着手時" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "期間に対応を期間を入力してください。(5日を超えるタスクは分割してください)" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "見積(人日)に記載がなければ入力してください。" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "ステータスを対応中に変更してください。" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "完了条件を満たしたら、ステータスをレビューに変更してください。" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "成果物を記載してください。(例: PR, SpreadsheetのURLなど)" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "対応内容" } }]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "完了条件" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": { "content": "(タスクの完了条件を記載してください)" },
          "annotations": { "bold": true }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  },
  {
    "object": "block",
    "type": "heading_2",
    "heading_2": {
      "rich_text": [{ "text": { "content": "成果物" } }]
    }
  },
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        {
          "text": { "content": "(成果物へのリンクを記載すること、成果物のファイルは添付しない)" },
          "annotations": { "bold": true }
        }
      ]
    }
  },
  {
    "object": "block",
    "type": "bulleted_list_item",
    "bulleted_list_item": {
      "rich_text": [{ "text": { "content": "" } }]
    }
  }
]
```

### 2. `src/importXlsxWbs.ts` の変更

#### 追加するインポート
```typescript
import * as fs from "fs";
```

#### 定数に追加
```typescript
const PARENT_TEMPLATE_PATH = process.env.PARENT_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/parent-template.json");
const CHILD_TEMPLATE_PATH = process.env.CHILD_TEMPLATE_PATH
  ?? path.resolve(__dirname, "../docs/child-template.json");
```

#### テンプレート読み込み関数の追加
```typescript
function loadTemplate(filePath: string): unknown[] {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf-8")) as unknown[];
  } catch {
    console.warn(`Template not found or invalid: ${filePath}. Using empty body.`);
    return [];
  }
}
```

#### `upsertXlsxTasks` のシグネチャ変更
```typescript
async function upsertXlsxTasks(
  client: Client,
  databaseId: string,
  tasks: WBSTask[],
  termMap: Map<string, TermEntry>,
  existingTitles: Map<string, string>,
  parentTemplate: unknown[],  // 追加
  childTemplate: unknown[],   // 追加
): Promise<{ created: number; updated: number }>
```

#### `pages.create` にテンプレートを渡す（新規作成時のみ）

`upsertRecursive` 内の新規作成分岐に追加:
```typescript
const templateBlocks = isParent ? parentTemplate : childTemplate;

page = await client.pages.create({
  parent: { database_id: databaseId },
  properties: properties as any,
  ...(isParent && { icon: PARENT_ICON }),
  ...(templateBlocks.length > 0 && { children: templateBlocks as any }),
});
```

> `pages.update` には `children` を渡さない（更新時はボディを変更しない）

#### `main()` でテンプレートを読み込んで渡す
```typescript
const parentTemplate = loadTemplate(PARENT_TEMPLATE_PATH);
const childTemplate  = loadTemplate(CHILD_TEMPLATE_PATH);
// ...
const { created, updated } = await upsertXlsxTasks(
  client, DATABASE_ID, tasks, termMap, existingTitles,
  parentTemplate, childTemplate,
);
```

### 3. `.env.example` への追記
```env
PARENT_TEMPLATE_PATH=docs/parent-template.json
CHILD_TEMPLATE_PATH=docs/child-template.json
```

---

## 動作確認

```bash
cd /src/notion_pm

# 1. Dry run（テンプレート読み込みエラーがないか確認）
npm run import-xlsx-wbs -- --dry-run

# 2. 実登録（新規作成時にボディが設定されることを Notion で確認）
npm run import-xlsx-wbs

# 3. 再実行（upsert 時にボディが上書きされないことを確認）
npm run import-xlsx-wbs
```

Notion で確認するポイント:
- 親タスクページに「目的」「スコープ」「完了条件」「成果物」「リスク・課題」の見出しとテーブルが存在する
- 子タスクページに「タスク着手時」「対応内容」「完了条件」「成果物」の見出しと各リストが存在する
- 2回目実行後に手動編集したボディが消えていない
