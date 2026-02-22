# API Blueprint

## 概要

**API Blueprint**は、Markdown形式でAPI仕様を記述するドキュメントフォーマットです。人間が読みやすい記法で、RESTful APIの設計・ドキュメント化・テストを支援します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Apiary（Oracle傘下） |
| **種別** | API設計・ドキュメントフォーマット |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料（仕様自体、ツールは製品により異なる） |
| **公式サイト** | https://apiblueprint.org/ |
| **ドキュメント** | https://apiblueprint.org/documentation/ |

## 主な特徴

### 1. Markdown形式
- シンプルで読みやすい
- バージョン管理システムでの差分管理が容易
- プログラマ向けのわかりやすい記法

### 2. リクエスト/レスポンス定義
- HTTPメソッド、ヘッダー、ボディを明確に定義
- 複数のレスポンス例（成功/エラー）
- JSON Schema統合

### 3. ツールエコシステム
- **Dredd**: APIテスト自動化
- **Aglio**: HTML生成
- **API Elements**: パーサー・コンバータ

### 4. モックサーバー生成
- 仕様からモックサーバー自動生成
- フロントエンド開発との並行作業を実現

## 使い方

### 基本的なAPI Blueprint記法

#### シンプルなGET API

```markdown
FORMAT: 1A

# Users API

Simple API for user management.

# Group Users

## User Collection [/users]

### List All Users [GET]

Retrieve a list of all users.

+ Response 200 (application/json)

    + Attributes (array[User])

    + Body

            [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john@example.com"
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane@example.com"
                }
            ]

## User [/users/{id}]

+ Parameters
    + id: 1 (number, required) - The user ID

### Get User Details [GET]

Retrieve details of a specific user.

+ Response 200 (application/json)

    + Attributes (User)

    + Body

            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "created_at": "2025-01-01T00:00:00Z"
            }

+ Response 404 (application/json)

    + Body

            {
                "error": "User not found"
            }

## Data Structures

### User (object)

+ id: 1 (number, required) - Unique identifier
+ name: `John Doe` (string, required) - Full name
+ email: `john@example.com` (string, required) - Email address
+ created_at: `2025-01-01T00:00:00Z` (string) - ISO 8601 timestamp
```

#### POST APIの定義

```markdown
### Create User [POST]

Create a new user.

+ Request (application/json)

    + Headers

            Authorization: Bearer YOUR_TOKEN

    + Attributes (UserCreate)

    + Body

            {
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "password": "securePassword123"
            }

+ Response 201 (application/json)

    + Headers

            Location: /users/3

    + Attributes (User)

    + Body

            {
                "id": 3,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "created_at": "2025-12-06T10:00:00Z"
            }

+ Response 400 (application/json)

    + Body

            {
                "error": "Invalid email format"
            }

## Data Structures

### UserCreate (object)

+ name: `Alice Johnson` (string, required) - Full name
+ email: `alice@example.com` (string, required) - Email address
+ password: `securePassword123` (string, required) - Password (min 8 chars)
```

### 認証の定義

```markdown
# Group Authentication

## Login [/auth/login]

### User Login [POST]

Authenticate a user and receive an access token.

+ Request (application/json)

    + Body

            {
                "email": "john@example.com",
                "password": "password123"
            }

+ Response 200 (application/json)

    + Body

            {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 3600
            }

+ Response 401 (application/json)

    + Body

            {
                "error": "Invalid credentials"
            }
```

### ツール使用

#### Aglio（HTML生成）

```bash
# Aglioインストール
npm install -g aglio

# HTMLドキュメント生成
aglio -i api.apib -o api.html

# ライブプレビュー
aglio -i api.apib -s
# ブラウザで http://localhost:3000 にアクセス

# カスタムテーマ
aglio -i api.apib -o api.html --theme-template triple
```

#### Dredd（APIテスト）

```bash
# Dreddインストール
npm install -g dredd

# APIテスト実行
dredd api.apib http://localhost:3000

# 設定ファイル作成
dredd init

# dredd.yml
dry-run: null
hookfiles: null
language: nodejs
sandbox: false
server: npm start
server-wait: 3
init: false
custom: {}
names: false
only: []
reporter: []
output: []
header: []
sorted: false
user: null
inline-errors: false
details: false
method: []
color: true
level: info
timestamp: false
silent: false
path: []
blueprint: api.apib
endpoint: 'http://localhost:3000'

# テスト実行
dredd
```

#### drafter（パーサー）

```bash
# drafterインストール
npm install -g drafter

# API Blueprintパース（JSON形式）
drafter api.apib -o api.json

# AST（Abstract Syntax Tree）生成
drafter api.apib -t ast -o api-ast.json
```

### モックサーバー生成

```bash
# api-mock（モックサーバー）
npm install -g api-mock

# モックサーバー起動
api-mock api.apib --port 8080

# リクエストテスト
curl http://localhost:8080/users
```

### CI/CD統合

```yaml
# .github/workflows/api-docs.yml
name: API Documentation
on: [push]
jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Aglio
        run: npm install -g aglio

      - name: Generate HTML
        run: aglio -i api.apib -o docs/api.html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs

  test-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Dredd
        run: npm install -g dredd

      - name: Start API Server
        run: npm start &

      - name: Run API Tests
        run: dredd api.apib http://localhost:3000
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | API仕様策定 | RESTful API要件定義 |
| **基本設計** | API設計 | エンドポイント・リクエスト/レスポンス設計 |
| **テスト** | APIテスト | Dreddで自動テスト |
| **導入** | APIドキュメント公開 | 開発者向けドキュメント生成 |

## メリット

- **Markdown形式**: プログラマに馴染みやすい記法
- **バージョン管理容易**: Git差分管理が簡単
- **ツールエコシステム**: HTML生成、テスト自動化、モック生成
- **人間可読**: 仕様を読みやすい形式で記述
- **無料**: 仕様自体は無料、オープンソース
- **シンプル**: OpenAPIより学習コストが低い

## デメリット

- **OpenAPIほど普及していない**: 業界標準はOpenAPI（Swagger）
- **ツールサポート**: OpenAPIに比べてツールが少ない
- **複雑なAPI表現の限界**: 非常に複雑なAPIにはOpenAPI推奨
- **Apiary依存**: 主要ツールがApiary（Oracle）エコシステム
- **仕様の制約**: OpenAPIほど柔軟性がない

## 類似ツールとの比較

| ツール | 形式 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **API Blueprint** | Markdown | シンプル、読みやすい | 中小規模API、ドキュメント重視 |
| **OpenAPI (Swagger)** | YAML/JSON | 業界標準、ツール豊富 | エンタープライズ、複雑なAPI |
| **RAML** | YAML | 再利用性高い | モジュラーAPI設計 |
| **GraphQL Schema** | GraphQL SDL | GraphQL専用 | GraphQL API |

## ベストプラクティス

### 1. データ構造の再利用

```markdown
## Data Structures

### User (object)
+ id: 1 (number, required)
+ name: `John Doe` (string, required)
+ email: `john@example.com` (string, required)

### UserList (object)
+ users (array[User], required)
+ total: 100 (number, required)
+ page: 1 (number, required)

### Response 200 (application/json)
+ Attributes (UserList)
```

### 2. 認証の明記

```markdown
# Group Authentication

All endpoints require Bearer token authentication unless otherwise noted.

## Headers

    Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 3. エラーレスポンスの標準化

```markdown
## Data Structures

### Error (object)
+ error: `Error message` (string, required) - Error description
+ code: `VALIDATION_ERROR` (string, required) - Error code
+ details (array[ErrorDetail], optional) - Detailed error info

### ErrorDetail (object)
+ field: `email` (string, required) - Field name
+ message: `Invalid email format` (string, required) - Field error
```

### 4. バージョニング

```markdown
FORMAT: 1A

# API v1

Base URL: https://api.example.com/v1

# API v2 Migration Guide

Version 2 introduces breaking changes. See migration guide at:
https://docs.example.com/api/v2-migration
```

## 公式リソース

- **公式サイト**: https://apiblueprint.org/
- **チュートリアル**: https://apiblueprint.org/documentation/tutorial.html
- **仕様**: https://github.com/apiaryio/api-blueprint/blob/master/API%20Blueprint%20Specification.md
- **Aglio**: https://github.com/danielgtaylor/aglio
- **Dredd**: https://dredd.org/

## まとめ

API Blueprintは、Markdown形式でAPI仕様を記述する、シンプルで読みやすいフォーマットです。OpenAPIほど普及していませんが、Markdown記法に慣れた開発者には直感的で、バージョン管理やドキュメント生成が容易です。中小規模のRESTful API設計や、ドキュメント重視のプロジェクトに最適です。

---

**最終更新**: 2025-12-06
**対象バージョン**: API Blueprint Format 1A
