# notion-pm

Notion データベースのページ一覧を取得する REST API サーバー兼Excel インポート機能。

[WBS のテンプレート](https://docs.google.com/spreadsheets/u/0/d/1Pb2WoREUfUwp17j9UySfpx0O37Bhu-nq-GuBgjms9Bw/copy?pli=1)

[Notion のテンプレート](https://chocolate-weather-214.notion.site/Template-Project-33ff76ee7f86800c8033cef10890465e?source=copy_link)

## 前提条件

- Node.js
- Notion Integration（API キー）が作成済みであること
- 対象の Notion データベースに Integration が接続されていること

## セットアップ

```bash
cd notion_pm
npm i
```

## 環境変数

プロジェクトルートに `.env` ファイルを作成する。

```bash
cp .env.example .env
```

```env
NOTION_API_KEY=ntn_xxxxxxxxxxxxxxxxxxxx
PORT=3500
NOTION_DATABASE_ID=your_notion_database_id
PARENT_RELATION_PROP=親タスク
CHILDREN_RELATION_PROP=サブタスク
PERIOD_PROP=期間
EFFORT_PROP=見積(人日)
PARENT_TEMPLATE_PATH=docs/parent-template.json
CHILD_TEMPLATE_PATH=docs/child-template.json
```

| 変数名 | 必須 | 説明 |
|---|---|---|
| `NOTION_API_KEY` | Yes | Notion Integration の API キー |
| `PORT` | No | サーバーのポート番号（デフォルト: `3500`） |
| `NOTION_DATABASE_ID` | WBS インポート時 | インポート先の Notion データベース ID。Notion URL の `notion.so/<workspace>/<DATABASE_ID>?v=...` から取得 |
| `PARENT_RELATION_PROP` | No | 親タスク Relation プロパティ名（デフォルト: `親タスク`） |
| `CHILDREN_RELATION_PROP` | No | 子タスク Relation プロパティ名（デフォルト: `子タスク`） |
| `PERIOD_PROP` | No | 期間プロパティ名（デフォルト: `期間`） |
| `EFFORT_PROP` | No | 工数プロパティ名（デフォルト: `工数`） |
| `PARENT_TEMPLATE_PATH` | No | 親タスクのページボディテンプレート JSON パス（デフォルト: `docs/parent-template.json`） |
| `CHILD_TEMPLATE_PATH` | No | 子タスクのページボディテンプレート JSON パス（デフォルト: `docs/child-template.json`） |

## 実行方法

### 開発モード（ts-node）

```bash
npm ci
npm run dev
```

### ビルド & 実行

```bash
npm run build
npm start
```

## WBS インポート（Excel → Notion）

`docs/template-development-wbs.xlsx` の WBS データを Notion データベースにインポートする。

### 前提

Notion データベースに以下のプロパティが存在すること:

| プロパティ名 | 種別 |
|---|---|
| `親タスク` | Relation（同一DB） |
| `子タスク` | Relation（同一DB） |
| `期間` | Date |
| `工数` | Number |

### 前提: Notion データベースのプロパティ

[Notion のテンプレート](https://chocolate-weather-214.notion.site/Template-Project-33ff76ee7f86800c8033cef10890465e?source=copy_link) を使用するか、以下のプロパティを手動で作成する。

| プロパティ名 | 種別 |
|---|---|
| `親タスク` | Relation（同一DB） |
| `サブタスク` | Relation（同一DB） |
| `期間` | Date |
| `見積(人日)` | Number |

### 手順

**1. セットアップ**

```bash
cd notion_pm
cp .env.example .env
npm ci
```

`.env` を編集して `NOTION_API_KEY` と `NOTION_DATABASE_ID` を設定する。

**2. Dry run で確認（Notion への書き込みなし）**

```bash
npm run import-xlsx-wbs -- --dry-run
```

期待出力例:

```
Reading: /src/notion_pm/docs/template-development-wbs.xlsx
Parsed 8 parent tasks, 31 child tasks
Term matched: 31 / 31 child tasks

[DRY RUN] Task tree:
  [親] 要件定義
    [子] ヒアリング・現状分析-現状ヒアリングMTG設定 [期間: 2026-02-01〜2026-02-05, 工数: 4d]
    [子] 業務フロー作成-業務フロー作成 [期間: 2026-02-05〜2026-02-11, 工数: 2d]
    ...

Dry run complete. Remove --dry-run to upsert tasks in Notion.
```

> `term: 未一致` が表示される場合は、`wbs` シートの F 列と `term` シートの B 列の値が一致していないため Excel を確認する。

**3. 実登録**

```bash
npm run import-xlsx-wbs
```

出力例（初回）:

```
Reading: /src/notion_pm/docs/template-development-wbs.xlsx
Parsed 8 parent tasks, 31 child tasks
Term matched: 31 / 31 child tasks
Parent template sections: 5
Child template sections: 4

Fetching existing pages from Notion database: 332f76ee...
Found 0 existing pages
Upserting tasks...
Done. Created 39, updated 0 tasks.
```

出力例（2回目以降・upsert）:

```
Found 39 existing pages
Upserting tasks...
Done. Created 0, updated 39 tasks.
```

### ページボディテンプレート

インポート時にページボディへ自動挿入するテンプレートを JSON で定義する。

| ファイル | 対象 |
|---|---|
| `docs/parent-template.json` | 親タスク（工程）のページ |
| `docs/child-template.json` | 子タスクのページ |

各セクションに `_upsert_mode` を指定することで、upsert（更新）時の挙動を制御できる。

| `_upsert_mode` | 新規作成時 | 更新時 |
|---|---|---|
| `overwrite` | 挿入 | 既存コンテンツを削除して再挿入 |
| `append` | 挿入 | 既存コンテンツの末尾に追記 |
| `skip` | 挿入 | 何もしない（手動編集を保護） |

**child-template.json のセクション設定:**

| セクション | `_upsert_mode` |
|---|---|
| タスク着手時 | `overwrite` |
| 対応内容 | `skip` |
| 完了条件 | `skip` |
| 成果物 | `skip` |

**parent-template.json のセクション設定:**

| セクション | `_upsert_mode` |
|---|---|
| 目的 | `skip` |
| スコープ | `skip` |
| 完了条件 | `skip` |
| 成果物 | `skip` |
| リスク・課題 | `append` |

### 動作仕様

| 処理 | 内容 |
|---|---|
| Excel 読み込み | `wbs` シートの E 列（工程）→ 親タスク、F 列（タスク）→ 子タスク |
| 期間・工数 | `term` シートの B 列をキーに開始日・終了日・工数を子タスクに設定 |
| 重複対策 | タイトル完全一致の既存ページは更新（upsert）、新規は作成 |
| Relation | 子 → 親（`親タスク`）、親 → 子（`サブタスク`）の双方向 Relation を設定 |
| ページボディ | 新規作成時は全セクションを挿入、更新時は `_upsert_mode` に従って制御 |

## API

### `GET /api/databases/:databaseId/pages`

指定した Notion データベースのページ一覧を取得する。

**リクエスト例:**

```bash
curl http://localhost:3500/api/databases/<DATABASE_ID>/pages
```

**レスポンス例:**

```json
{
  "databaseId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "count": 2,
  "pages": [
    {
      "pageId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "title": "[TASK-001] サンプルタスク",
      "prefix": "[TASK-001]"
    },
    {
      "pageId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "title": "タスク名のみ",
      "prefix": ""
    }
  ]
}
```
