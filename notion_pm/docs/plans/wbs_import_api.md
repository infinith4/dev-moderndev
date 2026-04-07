# WBS スプレッドシート → Notion タスク一括作成 API

## Context

Google Spreadsheet (ID: `1Pb2WoREUfUwp17j9UySfpx0O37Bhu-nq-GuBgjms9Bw`) の `wbs` シートを読み込み、大項目ごとに親タスク、中項目・小項目を子タスクとして Notion データベースに作成する REST API を `notion_pm` (TypeScript/Express) プロジェクトに追加する。

- スプレッドシートのカラム名: `大項目` / `中項目` / `小項目`
- タスク登録先: Notion データベース

---

## 実装ファイル

| ファイル | 変更内容 |
|---------|---------|
| `src/googleSheetsClient.ts` | 新規: Google Sheets API でシートを読み込む |
| `src/wbsImporter.ts` | 新規: 大項目→中項目→小項目 のツリー解析 + Notion ページ作成 |
| `src/index.ts` | 修正: `express.json()` 追加 + `POST /api/tasks/import-wbs` エンドポイント追加 |
| `restclient/import_wbs.http` | 新規: REST Client テスト用リクエスト |
| `package.json` | `googleapis` を dependencies に追加 |

---

## API 仕様

```
POST /api/tasks/import-wbs
Content-Type: application/json
```

### Request Body

| フィールド | 型 | 必須 | デフォルト | 説明 |
|-----------|-----|------|-----------|------|
| `spreadsheetId` | string | △ | env `SPREADSHEET_ID` | Google Spreadsheet ID |
| `sheetName` | string | × | `"wbs"` | 読み込むシート名 |
| `databaseId` | string | △ | env `NOTION_DATABASE_ID` | Notion データベース ID |
| `parentRelationProp` | string | × | `"親タスク"` | 親タスクを紐付ける Relation プロパティ名 |
| `dryRun` | boolean | × | `false` | `true` の場合タスクを作成せず解析結果のみ返す |

### Response (dryRun: false)

```json
{
  "spreadsheetId": "...",
  "sheetName": "wbs",
  "databaseId": "...",
  "created": 42,
  "tasks": [
    {
      "level": "大項目",
      "name": "要件定義",
      "notionPageId": "xxx-xxx",
      "children": [
        {
          "level": "中項目",
          "name": "ヒアリング",
          "notionPageId": "yyy-yyy",
          "children": [
            {
              "level": "小項目",
              "name": "ステークホルダーインタビュー",
              "notionPageId": "zzz-zzz",
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```

---

## タスク階層ロジック

```
大項目（同一値はまとめる）
  └─ 中項目（同一 大項目+中項目 はまとめる）
       └─ 小項目（各行ごとに作成）
  └─ 小項目（中項目が空の行は大項目直下に作成）
```

### スプレッドシート行の解釈ルール

| 大項目 | 中項目 | 小項目 | 動作 |
|-------|-------|-------|------|
| あり | なし | なし | 大項目タスクの詳細カラムを補完 |
| あり | あり | なし | 中項目タスクを大項目の子として作成 |
| あり | あり | あり | 小項目タスクを中項目の子として作成 |
| あり | なし | あり | 小項目タスクを大項目の直下に作成 |

---

## 環境変数

`.env` に以下を追加:

```env
# Google Spreadsheet
SPREADSHEET_ID=1Pb2WoREUfUwp17j9UySfpx0O37Bhu-nq-GuBgjms9Bw

# Notion
NOTION_DATABASE_ID=<NotionデータベースID>

# Google 認証（どちらか一方を設定）
GOOGLE_SERVICE_ACCOUNT_KEY_FILE=/path/to/service-account.json
GOOGLE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}
```

### Google Service Account の準備手順

1. Google Cloud Console でサービスアカウントを作成
2. 「Sheets API」を有効化
3. サービスアカウントの JSON キーをダウンロード
4. スプレッドシートをサービスアカウントのメールアドレスに共有（閲覧者権限）

---

## Notion データベース要件

| プロパティ名 | 型 | 必須 | 説明 |
|------------|-----|------|------|
| `title` (任意の名前) | Title | ✓ | タスク名 |
| `親タスク` | Relation (自己参照) | × | 親タスクへのリンク（省略可） |

`parentRelationProp` を空文字列 `""` にするとフラット作成（Relation なし）。

---

## 検証手順

```bash
# 1. ビルド
cd notion_pm
npm run build

# 2. サーバー起動
npm start

# 3. ドライランで解析結果を確認
curl -X POST http://localhost:3500/api/tasks/import-wbs \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheetId": "1Pb2WoREUfUwp17j9UySfpx0O37Bhu-nq-GuBgjms9Bw",
    "sheetName": "wbs",
    "databaseId": "YOUR_DATABASE_ID",
    "dryRun": true
  }'

# 4. 実際にタスクを作成
curl -X POST http://localhost:3500/api/tasks/import-wbs \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheetId": "1Pb2WoREUfUwp17j9UySfpx0O37Bhu-nq-GuBgjms9Bw",
    "sheetName": "wbs",
    "databaseId": "YOUR_DATABASE_ID",
    "parentRelationProp": "親タスク",
    "dryRun": false
  }'
```

REST Client ファイル: [restclient/import_wbs.http](../restclient/import_wbs.http)
