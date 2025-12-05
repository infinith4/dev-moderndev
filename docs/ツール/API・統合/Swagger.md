# Swagger / OpenAPI

## 概要

Swagger（OpenAPI）は、RESTful APIドキュメント・設計ツールです。OpenAPI Specification（YAML/JSON）、Swagger UI（インタラクティブドキュメント）、Swagger Editor、コード生成により、API設計、ドキュメント、クライアント生成を自動化します。API-First開発、契約駆動開発、多言語コード生成で広く採用されています。

## 主な機能

### 1. API仕様
- **OpenAPI Spec**: YAML/JSON定義
- **エンドポイント**: パス、メソッド
- **スキーマ**: リクエスト、レスポンス
- **認証**: OAuth、API Key

### 2. ドキュメント
- **Swagger UI**: インタラクティブUI
- **Try it out**: ブラウザテスト
- **リクエスト例**: サンプルリクエスト
- **レスポンス例**: サンプルレスポンス

### 3. コード生成
- **サーバースタブ**: Node.js、Java、Go等
- **クライアント**: JavaScript、Python、Java等
- **モデル**: データモデル

### 4. バリデーション
- **スキーマ検証**: 仕様検証
- **Linter**: API設計ルール

## 利用方法

### OpenAPI Specification（基本）

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: Sample API

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

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
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
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

### Swagger UI（Docker）

```bash
docker run -d --name swagger-ui \
  -p 8080:8080 \
  -e SWAGGER_JSON=/foo/openapi.yaml \
  -v $(pwd)/openapi.yaml:/foo/openapi.yaml \
  swaggerapi/swagger-ui

# http://localhost:8080
```

### Node.js統合（Express）

```javascript
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');

const app = express();
const swaggerDocument = YAML.load('./openapi.yaml');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.listen(3000, () => {
  console.log('Swagger UI: http://localhost:3000/api-docs');
});
```

### Spring Boot統合（Springdoc）

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-ui</artifactId>
    <version>1.7.0</version>
</dependency>
```

```java
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping
    @Operation(summary = "Get all users")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successful response")
    })
    public List<User> getAllUsers() {
        return userService.findAll();
    }

    @PostMapping
    @Operation(summary = "Create user")
    public User createUser(@RequestBody UserInput input) {
        return userService.create(input);
    }
}

// Swagger UI: http://localhost:8080/swagger-ui.html
```

### 認証設定

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - BearerAuth: []
  - ApiKeyAuth: []
```

### コード生成（Swagger Codegen）

```bash
# クライアント生成（JavaScript）
swagger-codegen generate \
  -i openapi.yaml \
  -l javascript \
  -o ./client

# サーバースタブ生成（Node.js）
swagger-codegen generate \
  -i openapi.yaml \
  -l nodejs-server \
  -o ./server
```

### Docker Compose（Swagger Editor + UI）

```yaml
version: '3.8'
services:
  swagger-editor:
    image: swaggerapi/swagger-editor
    ports:
      - "8081:8080"

  swagger-ui:
    image: swaggerapi/swagger-ui
    ports:
      - "8080:8080"
    environment:
      SWAGGER_JSON: /foo/openapi.yaml
    volumes:
      - ./openapi.yaml:/foo/openapi.yaml
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Swagger OSS** | 🟢 完全無料 | オープンソース、Apache License |
| **SwaggerHub Free** | 🟢 無料 | 1 API、3ユーザー |
| **SwaggerHub Team** | 💰 $75/月 | 複数API、チームコラボ |

## メリット

1. **完全無料**: オープンソース
2. **標準**: OpenAPI標準
3. **インタラクティブ**: Swagger UI
4. **コード生成**: 多言語対応
5. **API-First**: 設計駆動開発

## デメリット

1. **学習曲線**: OpenAPI学習必要
2. **同期**: コードとドキュメント同期
3. **コード生成品質**: 生成コード品質
4. **複雑なAPI**: 複雑なAPI記述困難

## 低頻度ツール

Swagger/OpenAPIエコシステムには、特定のユースケースで有用な低頻度ツールがあります。

### ReDoc

**概要**: OpenAPI仕様書から美しく読みやすいAPIドキュメントを自動生成するオープンソースツール

**主な特徴**:
- **3カラムレイアウト**: ナビゲーション、説明、サンプルコードの見やすい構成
- **レスポンシブデザイン**: モバイル・デスクトップ両対応
- **軽量高速**: SwaggerUIより高速なレンダリング
- **完全無料**: オープンソース、MIT License

**使用時期**:
- APIドキュメントの外部公開（美しいUIが必要な場合）
- Swagger UIの代替として読みやすいドキュメントが欲しい場合
- 静的HTMLファイル1つで公開したい場合

**Swagger UIとの比較**:
| 項目 | ReDoc | Swagger UI |
|------|-------|------------|
| **UI/UX** | 洗練された3カラムレイアウト | シンプルな2カラム |
| **Try It Out** | ❌ なし（表示のみ） | ✅ あり（APIテスト可能） |
| **パフォーマンス** | ✅ 高速 | 標準 |
| **カスタマイズ** | テーマ、色設定 | 高度なカスタマイズ可能 |
| **ユースケース** | ドキュメント公開特化 | ドキュメント+テスト |

**詳細**: [ReDoc.md](./ReDoc.md)

### Stoplight Studio

**概要**: API設計とドキュメント作成に特化したビジュアルエディタ

**主な特徴**:
- **ビジュアル編集**: GUIでOpenAPI仕様書作成（コード不要）
- **リアルタイムプレビュー**: ドキュメントを即座に確認
- **モックサーバー**: API実装前にモックAPIを起動
- **デスクトップ版無料**: ローカル利用は完全無料

**使用時期**:
- OpenAPI仕様書を初めて作成する場合（学習コスト低減）
- API設計をビジュアルに行いたい場合
- API実装前にフロントエンド開発を並行したい場合（モック活用）
- Git統合でバージョン管理したい場合

**Swagger Editorとの比較**:
| 項目 | Stoplight Studio | Swagger Editor |
|------|------------------|----------------|
| **編集方法** | ビジュアル + コード | コードのみ |
| **モックサーバー** | ✅ 高度なモック機能 | ❌ なし |
| **リアルタイムプレビュー** | ✅ あり | ✅ あり |
| **Git統合** | ✅ あり | ❌ なし |
| **価格** | デスクトップ版無料 | 完全無料 |
| **ユースケース** | API設計+モック+ドキュメント | シンプルなAPI仕様編集 |

**詳細**: [Stoplight_Studio.md](./Stoplight_Studio.md)

---

## 公式リンク

- **公式サイト**: [https://swagger.io/](https://swagger.io/)
- **OpenAPI Spec**: [https://spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)

## 関連ドキュメント

- [APIドキュメントツール一覧](../APIドキュメントツール/)
- [Stoplight Studio](./Stoplight_Studio.md)
- [ReDoc](./ReDoc.md)

---

**カテゴリ**: APIドキュメントツール
**対象工程**: API設計・ドキュメント
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
