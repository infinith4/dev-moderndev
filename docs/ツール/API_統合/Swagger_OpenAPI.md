# Swagger / OpenAPI

## 概要

Swagger（現在はOpenAPI）は、RESTful APIを設計・文書化・テストするためのオープンソースツールセットです。OpenAPI Specification (OAS)という標準仕様に基づき、APIをYAML/JSON形式で定義し、インタラクティブなAPIドキュメント、コード生成、モックサーバーなどを自動生成できます。API開発の標準として広く採用されています。

## 主な特徴

| 項目 | 内容 |
|------|------|
| 業界標準 | RESTful APIのデファクトスタンダード仕様 |
| 自動ドキュメント | コード/定義から最新ドキュメントを生成 |
| コード生成 | 50以上の言語/フレームワークのSDK・サーバースタブ生成 |
| インタラクティブ | Swagger UIでブラウザからAPIテスト可能 |
| エコシステム | 豊富なツール・ライブラリとの連携 |
| オープンソース | Swagger UI、Editor、OpenAPI Generatorは無料 |

## 主な機能

### API仕様定義（OpenAPI Specification）

| 機能 | 説明 |
|------|------|
| YAML/JSON形式 | 人間にも機械にも読みやすいAPI定義 |
| エンドポイント定義 | パス、パラメータ、レスポンスの記述 |
| データモデル | スキーマ定義とコンポーネント再利用 |
| セキュリティ | 認証・セキュリティスキーム設定 |

### Swagger UI

| 機能 | 説明 |
|------|------|
| ドキュメント自動生成 | OpenAPI定義からインタラクティブなドキュメント |
| Try it out | ブラウザ上でAPIリクエストを送信 |
| レスポンス表示 | リアルタイムでレスポンスを確認 |
| 認証対応 | OAuth、API Key等の認証フロー |

### コード生成

| 機能 | 説明 |
|------|------|
| クライアントSDK | TypeScript、Python、Java等のクライアント自動生成 |
| サーバースタブ | Express、Spring Boot等のサーバースケルトン生成 |
| カスタムテンプレート | 生成コードのテンプレートカスタマイズ |
| 50以上の言語 | 多数の言語/フレームワーク対応 |

## インストールとセットアップ

公式URL:
- [OpenAPI Specification](https://spec.openapis.org/)
- [Swagger.io](https://swagger.io/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Swagger Editor](https://editor.swagger.io/)
- [OpenAPI Generator](https://openapi-generator.tech/)

## 基本的な使い方

### 1. OpenAPI定義作成

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: ユーザー管理API

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: ユーザー一覧取得
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

    post:
      summary: ユーザー作成
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserInput'
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

  /users/{userId}:
    get:
      summary: ユーザー詳細取得
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: ユーザーが見つかりません

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "山田太郎"
        email:
          type: string
          format: email
          example: "yamada@example.com"

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

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### 2. Swagger UIの起動

```bash
# Dockerで起動
docker run -p 80:8080 -e SWAGGER_JSON=/openapi.yaml \
  -v $(pwd)/openapi.yaml:/openapi.yaml \
  swaggerapi/swagger-ui

# ブラウザで http://localhost にアクセス
```

### 3. Swagger Editorの起動

```bash
# Dockerで起動
docker run -p 8080:8080 swaggerapi/swagger-editor
# ブラウザで http://localhost:8080 にアクセス
```

### 4. クライアントSDK生成

```bash
# OpenAPI Generatorインストール
npm install @openapitools/openapi-generator-cli -g

# TypeScript Axiosクライアント生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./generated-client

# Pythonクライアント生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./generated-client-python
```

### 5. サーバースタブ生成

```bash
# Node.js Express サーバースタブ生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g nodejs-express-server \
  -o ./generated-server

# Spring Boot サーバースタブ生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g spring \
  -o ./generated-server-spring
```

## CI/CD 統合

### GitHub Actions

```yaml
name: API Docs & Validation

on:
  push:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate OpenAPI
        uses: char0n/swagger-editor-validate@v1
        with:
          definition-file: openapi.yaml
```

### GitLab CI

```yaml
validate_api:
  stage: test
  image: node:24
  before_script:
    - npm install -g @openapitools/openapi-generator-cli
  script:
    - openapi-generator-cli validate -i openapi.yaml
```

## Docker での使用

### Dockerfile 例（Swagger UI）

```dockerfile
FROM swaggerapi/swagger-ui
COPY openapi.yaml /usr/share/nginx/html/openapi.yaml
ENV SWAGGER_JSON=/usr/share/nginx/html/openapi.yaml
```

### docker-compose.yml 例

```yaml
version: '3.8'
services:
  swagger-ui:
    image: swaggerapi/swagger-ui
    ports:
      - "8080:8080"
    volumes:
      - ./openapi.yaml:/openapi.yaml
    environment:
      SWAGGER_JSON: /openapi.yaml

  swagger-editor:
    image: swaggerapi/swagger-editor
    ports:
      - "8081:8080"
```

## 他ツールとの比較

### Swagger/OpenAPI vs Postman

| 機能 | Swagger/OpenAPI | Postman |
|------|----------------|---------|
| API定義 | YAML/JSON仕様 | コレクション形式 |
| コード生成 | 50以上の言語 | 限定的 |
| テスト機能 | Try it out | 強力なテスト機能 |
| チーム協業 | SwaggerHub（有料） | ワークスペース |
| 価格 | ツール無料 | 有料プランあり |

### Swagger/OpenAPI vs GraphQL

| 機能 | Swagger/OpenAPI | GraphQL |
|------|----------------|---------|
| API形式 | REST API | GraphQL |
| スキーマ | OpenAPI Spec | GraphQL Schema |
| ツール | Swagger UI等 | GraphiQL等 |
| データ取得 | 固定レスポンス | クライアント指定 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| APIファースト開発 | 実装前にAPI仕様を定義 | OpenAPI定義→モック→実装の順序で開発 |
| SDKクライアント生成 | マルチ言語クライアント配布 | OpenAPI Generatorで各言語のSDKを自動生成 |
| APIドキュメント公開 | 外部開発者向けリファレンス | Swagger UIで公開、ReDocで美しいドキュメント |
| 契約テスト | API仕様の遵守確認 | スキーマバリデーションで仕様との一致を検証 |

## ベストプラクティス

### 1. OpenAPI定義の管理

- YAMLファイルをGitでバージョン管理する
- コンポーネント（$ref）を活用してスキーマを再利用する
- examplesを充実させてドキュメントの品質を上げる

### 2. API設計ガイドライン

- 一貫した命名規則（camelCase / snake_case）を適用する
- 適切なHTTPステータスコードを使用する
- エラーレスポンスの形式を統一する

### 3. バリデーション

- CIパイプラインにOpenAPI定義のバリデーションを組み込む
- スキーマの変更はPull Requestでレビューする
- 破壊的変更を検出するツールを導入する

## トラブルシューティング

### よくある問題と解決策

#### 1. YAML構文エラー

```
原因: インデントの不整合やコロンの後のスペース不足
解決策:
- YAMLバリデータでチェックする
- Swagger Editorのリアルタイム検証を活用する
```

#### 2. $refの参照エラー

```
原因: 参照先のコンポーネントが存在しない
解決策:
- components/schemas に定義が存在するか確認する
- パスの大文字小文字を確認する
```

#### 3. 生成コードの品質問題

```
原因: OpenAPI Generatorのテンプレートが要件に合わない
解決策:
- カスタムテンプレートを作成する
- 生成後の手動調整をスクリプト化する
- configオプションで生成設定を調整する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://swagger.io/
- OpenAPI Specification: https://spec.openapis.org/

### コミュニティ
- GitHub (Swagger UI): https://github.com/swagger-api/swagger-ui
- GitHub (OpenAPI Generator): https://github.com/OpenAPITools/openapi-generator

### チュートリアル
- Getting Started: https://swagger.io/docs/
- Swagger Editor Online: https://editor.swagger.io/

## まとめ

Swagger/OpenAPIは、以下の場面で特に有用です:

1. **APIファースト開発** - 実装前にAPI仕様を定義し、チーム全体で合意形成
2. **マルチ言語SDK生成** - OpenAPI Generatorで50以上の言語のクライアントを自動生成
3. **インタラクティブドキュメント** - Swagger UIで開発者がブラウザからAPIを試験

RESTful API開発の業界標準として、設計から実装、テスト、ドキュメントまでAPI開発ライフサイクル全体を支援する。
