# Swagger / OpenAPI

## 概要

Swagger（現在はOpenAPI）は、RESTful APIを設計・文書化・テストするためのオープンソースツールセットです。OpenAPI Specification (OAS)という標準仕様に基づき、APIをYAML/JSON形式で定義し、インタラクティブなAPIドキュメント、コード生成、モックサーバーなどを自動生成できます。API開発の標準として広く採用されています。

## 主な機能

### 1. API仕様定義（OpenAPI Specification）
- YAML/JSON形式でAPI定義
- エンドポイント、パラメータ、レスポンスの記述
- データモデル（スキーマ）定義
- 認証・セキュリティ設定

### 2. Swagger UI
- インタラクティブなAPIドキュメント自動生成
- ブラウザ上でAPIテスト実行
- "Try it out" 機能でリクエスト送信
- レスポンスのリアルタイム表示

### 3. Swagger Editor
- OpenAPI定義のリアルタイムエディタ
- シンタックスハイライト、自動補完
- バリデーション（文法チェック）
- プレビュー機能

### 4. Swagger Codegen / OpenAPI Generator
- API定義からクライアントSDK自動生成
- サーバースタブ生成
- 50以上の言語/フレームワーク対応
- カスタムテンプレート

### 5. SwaggerHub（商用サービス）
- クラウドベースAPI設計プラットフォーム
- チーム協業、バージョン管理
- API自動テスト、モックサーバー

## 利用方法

### OpenAPI定義作成

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

### Swagger UI の使用

```bash
# Dockerで起動
docker run -p 80:8080 -e SWAGGER_JSON=/openapi.yaml \
  -v $(pwd)/openapi.yaml:/openapi.yaml \
  swaggerapi/swagger-ui

# ブラウザで http://localhost にアクセス
# "Try it out" ボタンでAPIテスト実行可能
```

### Swagger Editor の使用

```bash
# Dockerで起動
docker run -p 8080:8080 swaggerapi/swagger-editor

# ブラウザで http://localhost:8080 にアクセス
# 左ペインでYAML編集、右ペインでプレビュー
```

### OpenAPI Generator でクライアントSDK生成

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

### サーバースタブ生成

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

## ツール・料金

| ツール | 価格 | 特徴 |
|--------|------|------|
| **OpenAPI Specification** | 🟢 無料 | オープンスタンダード |
| **Swagger UI** | 🟢 無料 | オープンソース |
| **Swagger Editor** | 🟢 無料 | オープンソース |
| **OpenAPI Generator** | 🟢 無料 | オープンソース |
| **SwaggerHub Free** | 🟢 無料 | 1ユーザー、3API |
| **SwaggerHub Team** | $75/月～ | チーム協業、API管理 |
| **SwaggerHub Enterprise** | 要問い合わせ | SSO、高度な管理機能 |

## メリット

### ✅ 主な利点

1. **業界標準**: RESTful APIのデファクトスタンダード
2. **自動ドキュメント**: コードから最新ドキュメント生成
3. **インタラクティブ**: ブラウザでAPIテスト可能
4. **コード生成**: クライアントSDK、サーバースタブ自動生成
5. **言語非依存**: 50以上の言語/フレームワーク対応
6. **オープンソース**: 無料で利用可能
7. **エコシステム**: 豊富なツール・ライブラリ
8. **バリデーション**: API定義の妥当性チェック
9. **チーム協業**: SwaggerHubでAPI設計協業
10. **API-First開発**: 設計→実装のワークフロー

## デメリット

### ❌ 制約・課題

1. **学習曲線**: OpenAPI仕様の習得に時間がかかる
2. **YAML記述**: 大規模APIでは記述が煩雑
3. **バージョン管理**: 定義ファイルのGit管理が必要
4. **完全性**: 複雑なビジネスロジックは表現困難
5. **ツール品質**: 生成コードの品質はツール依存
6. **カスタマイズ**: 生成コードのカスタマイズが必要な場合あり
7. **REST API専用**: GraphQL、gRPCには非対応
8. **SwaggerHub有料**: チーム利用は有料プラン必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Postman** | APIテスト・ドキュメント化 | Swagger/OpenAPIより手動作業多い |
| **API Blueprint** | Markdown形式のAPI記述 | OpenAPIより簡潔だが機能少ない |
| **RAML** | RESTful API Modeling Language | OpenAPIと類似、採用率低い |
| **ReDoc** | OpenAPIからドキュメント生成 | Swagger UIの代替、美しいUI |
| **GraphQL Schema** | GraphQL専用 | REST API非対応 |
| **Protobuf (gRPC)** | gRPC専用 | REST API非対応 |

## 公式リンク

- **OpenAPI Specification**: [https://spec.openapis.org/](https://spec.openapis.org/)
- **Swagger.io**: [https://swagger.io/](https://swagger.io/)
- **Swagger UI**: [https://swagger.io/tools/swagger-ui/](https://swagger.io/tools/swagger-ui/)
- **Swagger Editor**: [https://editor.swagger.io/](https://editor.swagger.io/)
- **OpenAPI Generator**: [https://openapi-generator.tech/](https://openapi-generator.tech/)
- **SwaggerHub**: [https://swagger.io/tools/swaggerhub/](https://swagger.io/tools/swaggerhub/)

## 関連ドキュメント

- [APIツール一覧](../APIツール/)
- [Postman](./Postman.md)
- [Insomnia](./Insomnia.md)
- [API設計ベストプラクティス](../../best-practices/api-design.md)
- [OpenAPI仕様書作成ガイド](../../best-practices/openapi-spec.md)

---

**カテゴリ**: APIツール  
**対象工程**: 基本設計、詳細設計、実装  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
