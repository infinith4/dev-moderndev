# Swagger / OpenAPI

## 概要

OpenAPIは、REST APIの仕様を記述するための標準フォーマットで、Swaggerはそのツールセットです。YAML/JSON形式でAPI仕様を記述し、Swagger UIで視覚的なドキュメントを自動生成できます。業界標準として広く採用されています。

### 主な特徴

- **完全無料**: オープンソースで無料
- **業界標準**: REST APIの事実上の標準仕様
- **コード自動生成**: サーバースタブ・クライアントSDKを自動生成
- **UIドキュメント自動生成**: Swagger UIで対話的なドキュメントを生成
- **バリデーション**: API仕様の妥当性を自動チェック

### OpenAPI/Swaggerツールセット

- **OpenAPI Specification**: YAML/JSONでAPI仕様を記述
- **Swagger Editor**: OpenAPI仕様を編集するエディタ
- **Swagger UI**: API仕様からUIドキュメントを自動生成
- **Swagger Codegen**: サーバー・クライアントコードを自動生成

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- REST APIの業界標準仕様
- コード自動生成により、実装の手間を削減
- Swagger UIで対話的なドキュメントを自動生成
- バリデーション機能でAPI仕様の一貫性を保証

**デメリット**
- YAML/JSONの記述が必要（GUIではない）
- 学習曲線がやや急
- REST API専用（SOAP、GraphQL等には非対応）
- 複雑なAPIの表現が困難な場合がある

## 利用方法

### 1. Swagger Editorへのアクセス

#### オンライン版

1. [Swagger Editor](https://editor.swagger.io/)にアクセス
2. ブラウザで直接利用可能（インストール不要）

#### ローカル版（Docker）

```bash
docker pull swaggerapi/swagger-editor
docker run -d -p 80:8080 swaggerapi/swagger-editor
```

ブラウザで `http://localhost` にアクセス

### 2. OpenAPI仕様の基本構造

OpenAPI 3.0仕様は、YAMLまたはJSON形式で記述します。

#### 最小限の例

```yaml
openapi: 3.0.0
info:
  title: ECサイトAPI
  version: 1.0.0
  description: ECサイトのREST API仕様書

servers:
  - url: https://api.example.com/v1
    description: 本番環境
  - url: https://api-dev.example.com/v1
    description: 開発環境

paths:
  /products:
    get:
      summary: 商品一覧取得
      description: 商品の一覧を取得する
      responses:
        '200':
          description: 成功
```

### 3. APIエンドポイントの定義

#### GETリクエストの例

**エンドポイント**: 商品一覧取得

```yaml
paths:
  /products:
    get:
      summary: 商品一覧取得
      description: 商品の一覧をページネーション付きで取得する
      tags:
        - 商品管理
      parameters:
        - name: page
          in: query
          description: ページ番号（1から開始）
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: 1ページあたりの件数
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: category
          in: query
          description: カテゴリでフィルタ
          required: false
          schema:
            type: string
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          description: リクエストエラー
        '500':
          description: サーバーエラー
```

#### POSTリクエストの例

**エンドポイント**: 注文作成

```yaml
paths:
  /orders:
    post:
      summary: 注文作成
      description: 新規注文を作成する
      tags:
        - 注文管理
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - customer_id
                - items
              properties:
                customer_id:
                  type: integer
                  description: 顧客ID
                  example: 12345
                items:
                  type: array
                  description: 注文商品リスト
                  items:
                    type: object
                    required:
                      - product_id
                      - quantity
                    properties:
                      product_id:
                        type: integer
                        example: 1
                      quantity:
                        type: integer
                        minimum: 1
                        example: 2
                shipping_address:
                  type: object
                  properties:
                    postal_code:
                      type: string
                      example: "123-4567"
                    address:
                      type: string
                      example: "東京都渋谷区..."
                payment_method:
                  type: string
                  enum: [credit_card, bank_transfer, cash_on_delivery]
                  example: credit_card
      responses:
        '201':
          description: 作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: バリデーションエラー
        '401':
          description: 認証エラー
        '500':
          description: サーバーエラー
```

### 4. スキーマ定義（components/schemas）

共通で使用するデータモデルを `components/schemas` に定義します。

```yaml
components:
  schemas:
    Product:
      type: object
      properties:
        product_id:
          type: integer
          example: 1
        product_name:
          type: string
          example: "ノートパソコン"
        price:
          type: number
          format: double
          example: 120000
        stock:
          type: integer
          example: 50
        category:
          type: string
          example: "electronics"
      required:
        - product_id
        - product_name
        - price

    Order:
      type: object
      properties:
        order_id:
          type: integer
          example: 98765
        customer_id:
          type: integer
          example: 12345
        total_amount:
          type: number
          format: double
          example: 240000
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered, cancelled]
          example: pending
        created_at:
          type: string
          format: date-time
          example: "2025-01-15T10:30:00Z"
      required:
        - order_id
        - customer_id
        - total_amount
        - status

    Pagination:
      type: object
      properties:
        current_page:
          type: integer
          example: 1
        total_pages:
          type: integer
          example: 10
        total_items:
          type: integer
          example: 200
        items_per_page:
          type: integer
          example: 20

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### 5. 認証の定義

API認証方式を定義します。

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT Bearer Token認証

    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-KEY
      description: APIキー認証

    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://api.example.com/oauth/authorize
          tokenUrl: https://api.example.com/oauth/token
          scopes:
            read: 読み取り権限
            write: 書き込み権限
```

エンドポイントに認証を適用：

```yaml
paths:
  /orders:
    post:
      security:
        - BearerAuth: []
```

### 6. エラーレスポンスの定義

標準的なエラーレスポンスを定義します。

```yaml
components:
  schemas:
    Error:
      type: object
      properties:
        status:
          type: string
          example: error
        error:
          type: object
          properties:
            code:
              type: string
              example: "INVALID_PARAMETER"
            message:
              type: string
              example: "指定されたパラメータが不正です"
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
```

エンドポイントでの利用：

```yaml
responses:
  '400':
    description: バリデーションエラー
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
```

### 7. Swagger UIでのドキュメント表示

Swagger Editorで作成した仕様は、Swagger UIで対話的なドキュメントとして表示できます。

1. Swagger Editorで仕様を作成
2. 右側のプレビューパネルにSwagger UIが表示される
3. 各エンドポイントをクリックして詳細を確認
4. 「Try it out」ボタンでAPIをテスト実行可能

#### Swagger UIの配置（独自サーバー）

```bash
# Docker で Swagger UI を起動
docker run -p 8080:8080 -e SWAGGER_JSON=/api/openapi.yaml -v $(pwd):/api swaggerapi/swagger-ui
```

ブラウザで `http://localhost:8080` にアクセス

### 8. コード生成（Swagger Codegen）

OpenAPI仕様からサーバー・クライアントコードを自動生成できます。

#### サーバースタブの生成（Java Spring Boot）

```bash
swagger-codegen generate \
  -i openapi.yaml \
  -l spring \
  -o ./server
```

#### クライアントSDKの生成（JavaScript）

```bash
swagger-codegen generate \
  -i openapi.yaml \
  -l javascript \
  -o ./client
```

### 9. バリデーション

OpenAPI仕様の妥当性をチェックできます。

#### オンラインバリデーター

[Swagger Validator](https://validator.swagger.io/)にアクセスしてYAMLをペースト

#### CLI ツール

```bash
npm install -g @apidevtools/swagger-cli
swagger-cli validate openapi.yaml
```

### 10. API仕様書のバージョン管理

OpenAPI仕様はYAML/JSONのテキストファイルなので、Gitでバージョン管理できます。

```bash
git add openapi.yaml
git commit -m "Add order creation endpoint"
git push
```

## 公式ドキュメント

- **OpenAPI公式サイト**: [OpenAPI Initiative](https://www.openapis.org/)
- **OpenAPI Specification**: [OpenAPI 3.0 Spec](https://spec.openapis.org/oas/latest.html)
- **Swagger Editor**: [Swagger Editor](https://editor.swagger.io/)
- **Swagger UI**: [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- **Swagger Codegen**: [Swagger Codegen](https://swagger.io/tools/swagger-codegen/)

## 学習リソース

- **OpenAPI Tutorial**: [Getting Started Guide](https://swagger.io/docs/specification/about/)
- **OpenAPI Examples**: [Example Specifications](https://github.com/OAI/OpenAPI-Specification/tree/main/examples)

## 関連リンク

- [Swagger Hub](https://swagger.io/tools/swaggerhub/)（クラウドベースのSwaggerツール）
- [Postman](https://www.postman.com/)（OpenAPIインポート/エクスポート対応）
- [REST API設計ベストプラクティス](https://restfulapi.net/)
