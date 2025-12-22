# json-server

## 概要

json-serverは、JSONファイルから即座にREST APIを作成できる超軽量なモックサーバツールです。npm一発インストールで、CRUD操作を自動生成し、フロントエンド開発やプロトタイピングに最適です。設定不要でシンプルに使え、フィルタ、ソート、ページネーション、リレーションなど基本的なREST API機能を提供します。

## 主な機能

### 1. 自動REST API生成
- **CRUD操作**: GET、POST、PUT、PATCH、DELETE
- **リソース自動認識**: JSONキーがエンドポイントに
- **ID自動割り当て**: POST時に自動ID生成
- **データ永続化**: JSON自動更新

### 2. クエリ機能
- **フィルタリング**: ?key=value
- **ソート**: ?_sort=field&_order=asc
- **ページネーション**: ?_page=1&_limit=10
- **全文検索**: ?q=keyword

### 3. リレーション
- **子リソース展開**: ?_embed=comments
- **親リソース展開**: ?_expand=author
- **カスタムルート**: routes.json定義

### 4. ミドルウェア
- **カスタムロジック**: server.js拡張
- **遅延シミュレーション**: --delay オプション
- **静的ファイル**: public/配下提供
- **CORS**: 自動有効化

## 利用方法

### インストール

```bash
# グローバルインストール
npm install -g json-server

# プロジェクト内インストール
npm install --save-dev json-server
```

### 基本使用

```bash
# db.json作成
cat > db.json <<EOF
{
  "users": [
    { "id": 1, "name": "John Doe", "email": "john@example.com" },
    { "id": 2, "name": "Jane Smith", "email": "jane@example.com" }
  ],
  "posts": [
    { "id": 1, "title": "Hello World", "userId": 1 },
    { "id": 2, "title": "json-server", "userId": 2 }
  ]
}
EOF

# サーバ起動（デフォルト: ポート3000）
json-server --watch db.json

# カスタムポート
json-server --watch db.json --port 8080

# ホスト指定
json-server --watch db.json --host 0.0.0.0
```

### API エンドポイント自動生成

```bash
# GET /users - 全ユーザー取得
curl http://localhost:3000/users

# GET /users/1 - IDで取得
curl http://localhost:3000/users/1

# POST /users - 新規作成
curl -X POST http://localhost:3000/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alice","email":"alice@example.com"}'

# PUT /users/1 - 更新（全体）
curl -X PUT http://localhost:3000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"id":1,"name":"John Updated","email":"john@example.com"}'

# PATCH /users/1 - 部分更新
curl -X PATCH http://localhost:3000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"John Patched"}'

# DELETE /users/1 - 削除
curl -X DELETE http://localhost:3000/users/1
```

### クエリパラメータ

```bash
# フィルタリング
curl 'http://localhost:3000/users?name=John Doe'
curl 'http://localhost:3000/posts?userId=1'

# ソート（昇順）
curl 'http://localhost:3000/users?_sort=name&_order=asc'

# ソート（降順）
curl 'http://localhost:3000/users?_sort=id&_order=desc'

# ページネーション
curl 'http://localhost:3000/users?_page=1&_limit=10'

# 全文検索
curl 'http://localhost:3000/users?q=john'

# 範囲指定
curl 'http://localhost:3000/users?id_gte=2&id_lte=5'

# 複数値
curl 'http://localhost:3000/users?id=1&id=2'
```

### リレーション

```bash
# 子リソース展開（usersにpostsを含める）
curl 'http://localhost:3000/users/1?_embed=posts'

# 親リソース展開（postsにuserを含める）
curl 'http://localhost:3000/posts/1?_expand=user'
```

### カスタムルート

```json
// routes.json
{
  "/api/*": "/$1",
  "/blog/:resource/:id/show": "/:resource/:id",
  "/posts/:category": "/posts?category=:category"
}
```

```bash
# カスタムルート適用
json-server --watch db.json --routes routes.json

# /api/users -> /users
curl http://localhost:3000/api/users
```

### ミドルウェア拡張

```javascript
// server.js
const jsonServer = require('json-server');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();

// カスタムミドルウェア
server.use((req, res, next) => {
  // 認証チェック（例）
  if (req.headers.authorization === 'Bearer token123') {
    next();
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
});

// デフォルトミドルウェア
server.use(middlewares);

// ルーター
server.use(router);

// サーバ起動
server.listen(3000, () => {
  console.log('JSON Server is running');
});
```

```bash
# カスタムサーバ起動
node server.js
```

### 遅延シミュレーション

```bash
# 2秒遅延
json-server --watch db.json --delay 2000
```

### package.json統合

```json
{
  "scripts": {
    "mock-api": "json-server --watch db.json --port 3000",
    "mock-api:delay": "json-server --watch db.json --port 3000 --delay 1000"
  },
  "devDependencies": {
    "json-server": "^0.17.4"
  }
}
```

```bash
npm run mock-api
```

### Docker使用

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

RUN npm install -g json-server

COPY db.json /app/db.json

EXPOSE 3000

CMD ["json-server", "--watch", "db.json", "--host", "0.0.0.0"]
```

```bash
# Dockerビルド・起動
docker build -t json-server-mock .
docker run -p 3000:3000 json-server-mock
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **json-server** | 🟢 完全無料 | オープンソース、npm無料 |

## メリット

1. **完全無料**: npm無料
2. **超シンプル**: JSONファイルのみで即API
3. **npm一発インストール**: セットアップ簡単
4. **CRUD自動生成**: コード不要
5. **フロントエンド開発最適**: バックエンド不要

## デメリット

1. **機能限定的**: 基本CRUD のみ
2. **複雑なロジック不可**: ビジネスロジック実装困難
3. **プロダクション非推奨**: 開発専用
4. **認証機能なし**: カスタムミドルウェア必要

## 公式リンク

- **公式サイト**: [https://github.com/typicode/json-server](https://github.com/typicode/json-server)
- **npm**: [https://www.npmjs.com/package/json-server](https://www.npmjs.com/package/json-server)

## 関連ドキュメント

- [モックサーバツール一覧](../../dev_process_開発工程_9_テスト_アプリケーション.md#922-apiテスト用モックサーバツールtop-6)
- [Mockoon](./Mockoon.md)
- [Prism](./Prism.md)

---

**カテゴリ**: モックサーバ・APIテスト
**対象工程**: フロントエンド開発・プロトタイピング
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
