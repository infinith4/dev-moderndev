# notion-pm

Notion データベースのページ一覧を取得する REST API サーバー。

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

```env
NOTION_API_KEY=ntn_xxxxxxxxxxxxxxxxxxxx
PORT=3500
```

| 変数名 | 必須 | 説明 |
|---|---|---|
| `NOTION_API_KEY` | Yes | Notion Integration の API キー |
| `PORT` | No | サーバーのポート番号（デフォルト: `3500`） |

## 実行方法

### 開発モード（ts-node）

```bash
npm run dev
```

### ビルド & 実行

```bash
npm run build
npm start
```

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
