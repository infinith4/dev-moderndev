# Prism

## 概要

Prismは、OpenAPI仕様（旧Swagger）からモックサーバを自動生成するツールです。Stoplight社が開発したオープンソースツールで、OpenAPI 3.0仕様に基づいて動的レスポンス生成、バリデーション、エラーシミュレーションを行います。CLI・Docker対応で、API設計とテストの自動化に最適です。

## 主な機能

### 1. OpenAPI自動モック
- **仕様ベース**: OpenAPI 3.0対応
- **自動レスポンス生成**: スキーマから動的生成
- **サンプル優先**: examplesフィールド優先使用
- **バリデーション**: リクエスト検証

### 2. 動的レスポンス
- **スキーマベース**: type定義から生成
- **リアルなデータ**: Faker統合
- **複数例**: examples から選択
- **エラーレスポンス**: 4xx/5xx シミュレーション

### 3. リクエストバリデーション
- **スキーマ検証**: リクエストボディ検証
- **パラメータ検証**: クエリ・パス検証
- **ヘッダー検証**: 必須ヘッダー確認
- **エラー返却**: バリデーションエラー詳細

### 4. CLI・Docker対応
- **コマンドライン**: CLI実行
- **Docker**: コンテナ実行
- **CI/CD統合**: パイプライン対応
- **ログ出力**: 詳細ログ

## 利用方法

### インストール

```bash
# npm インストール
npm install -g @stoplight/prism-cli

# または yarn
yarn global add @stoplight/prism-cli
```

### 基本使用（OpenAPI仕様から起動）

```bash
# OpenAPI仕様ファイル準備（YAML or JSON）
# openapi.yaml

# モックサーバ起動
prism mock openapi.yaml

# カスタムポート指定
prism mock openapi.yaml --port 4010

# 動的レスポンス生成モード
prism mock openapi.yaml --dynamic
```

### OpenAPI仕様例

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

servers:
  - url: http://localhost:4010

paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
              examples:
                users:
                  value:
                    - id: 1
                      name: "John Doe"
                      email: "john@example.com"
                    - id: 2
                      name: "Jane Smith"
                      email: "jane@example.com"

  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found

    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserInput'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email

    UserInput:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email
```

### 動的レスポンス生成

```bash
# --dynamic オプション: スキーマから動的生成
prism mock openapi.yaml --dynamic

# レスポンス例（スキーマベース自動生成）:
# {
#   "id": 12345,
#   "name": "string",
#   "email": "user@example.com"
# }
```

### バリデーションモード

```bash
# リクエストバリデーション有効化（デフォルトで有効）
prism mock openapi.yaml

# バリデーションエラー例:
# POST /users with invalid body:
# {
#   "validation": [
#     {
#       "location": ["body", "email"],
#       "severity": "Error",
#       "code": "format",
#       "message": "must match format \"email\""
#     }
#   ]
# }
```

### エラーレスポンスシミュレーション

```bash
# OpenAPI仕様で複数レスポンス定義

# Prefer ヘッダーで指定
curl http://localhost:4010/users/999 \
  -H 'Prefer: code=404'

# レスポンス: 404 Not Found
```

### リモートOpenAPI仕様使用

```bash
# URL指定
prism mock https://api.example.com/openapi.yaml

# GitHub Raw
prism mock https://raw.githubusercontent.com/user/repo/main/openapi.yaml
```

### Docker使用

```bash
# Docker起動
docker run --init --rm \
  -p 4010:4010 \
  -v $(pwd)/openapi.yaml:/tmp/openapi.yaml \
  stoplight/prism:4 \
  mock -h 0.0.0.0 /tmp/openapi.yaml

# Docker Compose
version: '3'
services:
  prism:
    image: stoplight/prism:4
    command: mock -h 0.0.0.0 /tmp/openapi.yaml
    ports:
      - "4010:4010"
    volumes:
      - ./openapi.yaml:/tmp/openapi.yaml
```

### package.json統合

```json
{
  "scripts": {
    "mock-api": "prism mock openapi.yaml --port 4010",
    "mock-api:dynamic": "prism mock openapi.yaml --dynamic"
  },
  "devDependencies": {
    "@stoplight/prism-cli": "^5.5.0"
  }
}
```

```bash
npm run mock-api
```

### CI/CD統合（GitHub Actions）

```yaml
name: API Tests

on: [push]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Prism
        run: npm install -g @stoplight/prism-cli

      - name: Start Mock Server
        run: |
          prism mock openapi.yaml --port 4010 &
          sleep 5

      - name: Run API Tests
        run: npm test

      - name: Stop Mock Server
        run: killall prism
```

### プロキシモード

```bash
# プロキシとして動作（実サーバと併用）
prism proxy openapi.yaml https://api.example.com --port 4010

# リクエスト検証しつつ実サーバに転送
```

### ログレベル設定

```bash
# ログレベル指定
prism mock openapi.yaml --log-level debug

# ログレベル: fatal, error, warn, info, debug, trace
```

### 複数例の切り替え

```yaml
# OpenAPI仕様で複数examples定義
responses:
  '200':
    content:
      application/json:
        examples:
          success:
            value: { "status": "ok" }
          error:
            value: { "status": "error" }
```

```bash
# Prefer ヘッダーで例指定
curl http://localhost:4010/api/endpoint \
  -H 'Prefer: example=error'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Prism CLI** | 🟢 完全無料 | オープンソース、フル機能 |
| **Stoplight Platform** | 💰 $99/月〜 | GUI統合、チームコラボ |

## メリット

1. **OpenAPI仕様から自動生成**: 仕様書がそのままモックに
2. **バリデーション機能**: リクエスト自動検証
3. **動的レスポンス生成**: リアルなデータ生成
4. **CLI・Docker対応**: CI/CD統合容易
5. **サンプル生成優秀**: Faker統合

## デメリット

1. **OpenAPI仕様必須**: 仕様書作成必要
2. **GraphQL非対応**: REST APIのみ
3. **複雑なビジネスロジック不可**: シンプルなモックのみ
4. **UI なし**: CLI only（Stoplight Platformは有料）

## 公式リンク

- **公式サイト**: [https://stoplight.io/open-source/prism](https://stoplight.io/open-source/prism)
- **ドキュメント**: [https://docs.stoplight.io/docs/prism/](https://docs.stoplight.io/docs/prism/)
- **GitHub**: [https://github.com/stoplightio/prism](https://github.com/stoplightio/prism)
- **npm**: [https://www.npmjs.com/package/@stoplight/prism-cli](https://www.npmjs.com/package/@stoplight/prism-cli)

## 関連ドキュメント

- [モックサーバツール一覧](../../dev_process_開発工程_9_テスト_アプリケーション.md#922-apiテスト用モックサーバツールtop-6)
- [Mockoon](./Mockoon.md)
- [WireMock](./WireMock.md)

---

**カテゴリ**: モックサーバ・APIテスト
**対象工程**: API設計・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
