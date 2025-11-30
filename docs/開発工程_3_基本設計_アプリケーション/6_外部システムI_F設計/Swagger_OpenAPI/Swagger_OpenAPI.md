# Swagger/OpenAPI（外部システムI/F設計）

## 概要

Swagger/OpenAPIは、REST API仕様の標準フォーマットで、基本設計フェーズではAPI仕様書の詳細作成、エンドポイント定義、スキーマ定義、インタラクティブなAPIドキュメント生成に活用します。YAML/JSON形式で記述し、Swagger UIで可視化することで、外部システム開発者への仕様伝達が容易になります。

### 基本設計フェーズでの活用

- **OpenAPI仕様書作成**: エンドポイント、パラメータ、レスポンススキーマの定義
- **スキーマ定義**: リクエスト/レスポンスのJSONスキーマ設計
- **エラーレスポンス設計**: エラーコード、エラーメッセージの詳細設計
- **認証・認可設計**: API Key、Bearer Token、OAuth 2.0の仕様定義
- **インタラクティブドキュメント**: Swagger UIで試せるAPIドキュメント
- **コード生成**: サーバースタブ、クライアントSDKの自動生成

### OpenAPIバージョン

- **OpenAPI 3.1**: 最新版（JSON Schema完全準拠）
- **OpenAPI 3.0**: 現在の主流（2017年リリース）
- **Swagger 2.0**: 旧バージョン（2014年リリース、非推奨）

### メリット・デメリット

**メリット**
- 完全無料でオープンスタンダード
- YAML/JSON形式でバージョン管理（Git）が容易
- Swagger UIでインタラクティブなドキュメントを自動生成
- 各種言語のサーバースタブ、クライアントSDKを自動生成
- 業界標準のため、外部システム開発者との連携が容易
- バリデーション、テストツールが豊富

**デメリット**
- YAML記述の学習コストが必要
- 大規模なAPI仕様書は管理が複雑
- スキーマ定義が冗長になりがち

## 利用方法

### 1. Swagger Editorのセットアップ

#### オンライン版（推奨）

1. [Swagger Editor](https://editor.swagger.io/)にアクセス
2. ブラウザでYAMLを編集
3. リアルタイムでSwagger UIがプレビュー表示

#### ローカル版（Docker）

```bash
docker pull swaggerapi/swagger-editor
docker run -d -p 8080:8080 swaggerapi/swagger-editor
# http://localhost:8080 にアクセス
```

### 2. OpenAPI 3.0仕様書の作成

#### 例: ECサイト外部API仕様

**基本構造:**

```yaml
openapi: 3.0.3
info:
  title: ECサイト外部API
  description: |
    ECサイトの商品情報、注文情報を外部システムに提供するREST API。

    ## 認証方式
    Bearer Token認証を使用。HTTPヘッダーに`Authorization: Bearer {token}`を含めてください。

    ## レート制限
    - 1時間あたり1000リクエスト
    - 超過時は429 Too Many Requestsを返却

  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
    url: https://support.example.com
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html

servers:
  - url: https://api.example.com/v1
    description: 本番環境
  - url: https://api-staging.example.com/v1
    description: ステージング環境
  - url: http://localhost:8080/v1
    description: ローカル開発環境

tags:
  - name: Products
    description: 商品管理API
  - name: Orders
    description: 注文管理API
  - name: Customers
    description: 顧客管理API
```

### 3. エンドポイントの詳細設計

#### GET /products（商品一覧取得）

```yaml
paths:
  /products:
    get:
      tags:
        - Products
      summary: 商品一覧取得
      description: |
        商品の一覧を取得します。ページネーション、フィルタリング、ソート機能をサポートします。

        ## 使用例
        - 全商品取得: `/products`
        - カテゴリ絞り込み: `/products?category_id=5`
        - 価格順ソート: `/products?sort=price_asc`

      operationId: listProducts
      parameters:
        - name: page
          in: query
          description: ページ番号（1始まり）
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
            example: 1

        - name: limit
          in: query
          description: 1ページあたりの取得件数
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
            example: 20

        - name: category_id
          in: query
          description: カテゴリID（フィルタリング用）
          required: false
          schema:
            type: integer
            example: 5

        - name: sort
          in: query
          description: ソート順
          required: false
          schema:
            type: string
            enum:
              - price_asc
              - price_desc
              - name_asc
              - name_desc
              - created_at_desc
            default: created_at_desc
            example: price_asc

        - name: keyword
          in: query
          description: 商品名・説明文での検索キーワード
          required: false
          schema:
            type: string
            maxLength: 100
            example: "マウス"

      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductListResponse'
              examples:
                success:
                  summary: 正常系レスポンス
                  value:
                    status: success
                    data:
                      products:
                        - product_id: 101
                          product_name: ワイヤレスマウス
                          category_id: 5
                          category_name: PC周辺機器
                          price: 2980
                          stock_quantity: 150
                          image_url: https://example.com/images/product_101.jpg
                          created_at: "2025-01-10T10:30:00Z"
                      pagination:
                        current_page: 1
                        total_pages: 10
                        total_items: 200
                        items_per_page: 20

        '400':
          $ref: '#/components/responses/BadRequest'

        '401':
          $ref: '#/components/responses/Unauthorized'

        '500':
          $ref: '#/components/responses/InternalServerError'

      security:
        - BearerAuth: []
```

#### GET /products/{product_id}（商品詳細取得）

```yaml
  /products/{product_id}:
    get:
      tags:
        - Products
      summary: 商品詳細取得
      description: 指定された商品IDの詳細情報を取得します
      operationId: getProductById
      parameters:
        - name: product_id
          in: path
          description: 商品ID
          required: true
          schema:
            type: integer
            example: 101

      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductDetailResponse'

        '404':
          description: 商品が見つかりません
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                status: error
                error:
                  code: PRODUCT_NOT_FOUND
                  message: 指定された商品が見つかりません
                  product_id: 9999

      security:
        - BearerAuth: []
```

#### POST /orders（注文作成）

```yaml
  /orders:
    post:
      tags:
        - Orders
      summary: 注文作成
      description: 新規注文を作成します
      operationId: createOrder
      requestBody:
        description: 注文情報
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              example1:
                summary: 通常注文
                value:
                  customer_id: 1001
                  items:
                    - product_id: 101
                      quantity: 2
                    - product_id: 102
                      quantity: 1
                  shipping_address:
                    postal_code: "100-0001"
                    prefecture: 東京都
                    city: 千代田区
                    street: 千代田1-1-1
                    building: サンプルビル101
                  payment_method: credit_card
                  memo: 午前中配送希望

      responses:
        '201':
          description: 注文作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderDetailResponse'

        '400':
          $ref: '#/components/responses/BadRequest'

        '422':
          description: 在庫不足等の処理不可能なエラー
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                status: error
                error:
                  code: OUT_OF_STOCK
                  message: 在庫不足のため注文できません
                  details:
                    - product_id: 101
                      requested_quantity: 2
                      available_quantity: 1

      security:
        - BearerAuth: []
```

### 4. スキーマ定義（components/schemas）

#### Productスキーマ

```yaml
components:
  schemas:
    Product:
      type: object
      properties:
        product_id:
          type: integer
          description: 商品ID
          example: 101
        product_name:
          type: string
          maxLength: 200
          description: 商品名
          example: ワイヤレスマウス
        category_id:
          type: integer
          description: カテゴリID
          example: 5
        category_name:
          type: string
          description: カテゴリ名
          example: PC周辺機器
        price:
          type: number
          format: decimal
          minimum: 0
          description: 価格（税込）
          example: 2980
        stock_quantity:
          type: integer
          minimum: 0
          description: 在庫数
          example: 150
        image_url:
          type: string
          format: uri
          description: 商品画像URL
          example: https://example.com/images/product_101.jpg
        created_at:
          type: string
          format: date-time
          description: 作成日時（ISO 8601形式）
          example: "2025-01-10T10:30:00Z"
      required:
        - product_id
        - product_name
        - price
        - stock_quantity
```

#### ProductDetailスキーマ

```yaml
    ProductDetail:
      allOf:
        - $ref: '#/components/schemas/Product'
        - type: object
          properties:
            description:
              type: string
              description: 商品説明
              example: 静音設計の高性能ワイヤレスマウス。Bluetooth 5.0対応。
            images:
              type: array
              description: 商品画像一覧
              items:
                type: string
                format: uri
              example:
                - https://example.com/images/product_101_main.jpg
                - https://example.com/images/product_101_sub1.jpg
            specifications:
              type: object
              description: 商品スペック
              additionalProperties:
                type: string
              example:
                weight: "75g"
                dimensions: "10.5 x 6.8 x 3.8 cm"
                battery_life: 最大18ヶ月
            updated_at:
              type: string
              format: date-time
              description: 更新日時
              example: "2025-01-10T10:30:00Z"
```

#### CreateOrderRequestスキーマ

```yaml
    CreateOrderRequest:
      type: object
      properties:
        customer_id:
          type: integer
          description: 顧客ID
          example: 1001
        items:
          type: array
          description: 注文商品一覧
          minItems: 1
          items:
            type: object
            properties:
              product_id:
                type: integer
                description: 商品ID
                example: 101
              quantity:
                type: integer
                minimum: 1
                description: 数量
                example: 2
            required:
              - product_id
              - quantity
        shipping_address:
          $ref: '#/components/schemas/Address'
        payment_method:
          type: string
          enum:
            - credit_card
            - bank_transfer
            - cash_on_delivery
          description: 支払方法
          example: credit_card
        memo:
          type: string
          maxLength: 500
          description: 備考（配送時間指定等）
          example: 午前中配送希望
      required:
        - customer_id
        - items
        - shipping_address
        - payment_method
```

#### Addressスキーマ

```yaml
    Address:
      type: object
      properties:
        postal_code:
          type: string
          pattern: '^\d{3}-\d{4}$'
          description: 郵便番号（ハイフン付き）
          example: "100-0001"
        prefecture:
          type: string
          description: 都道府県
          example: 東京都
        city:
          type: string
          description: 市区町村
          example: 千代田区
        street:
          type: string
          description: 番地
          example: 千代田1-1-1
        building:
          type: string
          description: 建物名・部屋番号
          example: サンプルビル101
      required:
        - postal_code
        - prefecture
        - city
        - street
```

#### ErrorResponseスキーマ

```yaml
    ErrorResponse:
      type: object
      properties:
        status:
          type: string
          enum:
            - error
          example: error
        error:
          type: object
          properties:
            code:
              type: string
              description: エラーコード
              example: INVALID_PARAMETER
            message:
              type: string
              description: エラーメッセージ
              example: パラメータが不正です
            field:
              type: string
              description: エラーが発生したフィールド名
              example: email
            details:
              type: array
              description: 詳細エラー情報
              items:
                type: object
          required:
            - code
            - message
      required:
        - status
        - error
```

### 5. 認証・認可の設計

#### Bearer Token認証

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        Bearer Token認証。
        HTTPヘッダーに`Authorization: Bearer {token}`を含めてください。

        トークンの取得方法については、API管理者にお問い合わせください。

# 全エンドポイントにデフォルトで適用
security:
  - BearerAuth: []
```

#### OAuth 2.0認証

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read:products: 商品情報の読み取り
            write:orders: 注文の作成・更新
            admin: 管理者権限
```

### 6. レスポンスの再利用定義

```yaml
components:
  responses:
    BadRequest:
      description: リクエストパラメータが不正
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            status: error
            error:
              code: INVALID_PARAMETER
              message: パラメータが不正です
              field: limit

    Unauthorized:
      description: 認証エラー
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            status: error
            error:
              code: UNAUTHORIZED
              message: 認証に失敗しました。有効なAPIキーを指定してください

    InternalServerError:
      description: サーバー内部エラー
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            status: error
            error:
              code: INTERNAL_SERVER_ERROR
              message: サーバー内部エラーが発生しました
```

### 7. Swagger UIでのドキュメント生成

#### Swagger UIのセットアップ（Docker）

```bash
docker pull swaggerapi/swagger-ui
docker run -p 8081:8080 \
  -e SWAGGER_JSON=/app/openapi.yaml \
  -v $(pwd)/openapi.yaml:/app/openapi.yaml \
  swaggerapi/swagger-ui
# http://localhost:8081 にアクセス
```

### 8. コード生成

#### サーバースタブの生成（Spring Boot）

```bash
# Swagger Codegenのインストール
brew install swagger-codegen  # macOS
# または
npm install -g @openapitools/openapi-generator-cli

# Spring Bootサーバースタブ生成
openapi-generator-cli generate \
  -i openapi.yaml \
  -g spring \
  -o ./server-stub \
  --additional-properties=basePackage=com.example.api
```

#### クライアントSDKの生成（TypeScript）

```bash
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./client-sdk-typescript
```

### 9. バリデーション

#### OpenAPI仕様の検証

```bash
# Spectralのインストール
npm install -g @stoplight/spectral-cli

# バリデーション実行
spectral lint openapi.yaml
```

### 10. I/F設計書への統合

#### 設計書の構成

**1. API概要**

OpenAPIのinfoセクションから自動生成:
- API名称
- バージョン
- 説明
- 連絡先情報

**2. サーバー環境**

serversセクションから自動生成:
- 本番環境URL
- ステージング環境URL
- ローカル開発環境URL

**3. エンドポイント一覧**

| No. | Path | Method | 概要 | 認証 |
|-----|------|--------|------|------|
| 1 | /products | GET | 商品一覧取得 | Required |
| 2 | /products/{id} | GET | 商品詳細取得 | Required |
| 3 | /orders | POST | 注文作成 | Required |

**4. 詳細仕様（各エンドポイント）**

Swagger UIで生成されたHTMLを添付

**5. スキーマ定義一覧**

componentsセクションのスキーマを表形式で記載

**6. エラーコード一覧**

| コード | HTTP Status | メッセージ | 説明 |
|--------|-------------|-----------|------|
| INVALID_PARAMETER | 400 | パラメータが不正です | リクエストパラメータのバリデーションエラー |
| UNAUTHORIZED | 401 | 認証に失敗しました | APIキーが無効または期限切れ |

### 11. バージョン管理

#### Git管理

```bash
git add openapi.yaml
git commit -m "Add POST /orders endpoint with validation schema"
git push
```

#### 変更履歴の記録

```yaml
info:
  version: 1.1.0
  x-changelog:
    1.1.0:
      - date: 2025-01-20
        changes:
          - "POST /orders エンドポイントを追加"
          - "Addressスキーマにbuilding項目を追加"
    1.0.0:
      - date: 2025-01-15
        changes:
          - "初版リリース"
```

## 公式ドキュメント

- **OpenAPI Specification**: [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.3)
- **Swagger Editor**: [Swagger Editor](https://editor.swagger.io/)
- **Swagger UI**: [Swagger UI](https://swagger.io/tools/swagger-ui/)
- **OpenAPI Generator**: [OpenAPI Generator](https://openapi-generator.tech/)

## 学習リソース

- **OpenAPI Tutorial**: [Getting Started with OpenAPI](https://swagger.io/docs/specification/about/)
- **Best Practices**: [OpenAPI Best Practices](https://swagger.io/blog/api-design/openapi-best-practices/)
- **YouTube**: [OpenAPI/Swagger Tutorial](https://www.youtube.com/results?search_query=openapi+swagger+tutorial)

## 関連リンク

- [Postman](https://www.postman.com/)（APIテストツール）
- [Stoplight Studio](https://stoplight.io/)（OpenAPIエディタ）
- [ReDoc](https://redoc.ly/)（代替APIドキュメントジェネレーター）
- [API Blueprint](https://apiblueprint.org/)（代替API仕様フォーマット）
