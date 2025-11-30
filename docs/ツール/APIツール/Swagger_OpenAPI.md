# Swagger / OpenAPI

## 概要

OpenAPIは、REST APIの仕様を記述するための標準フォーマットで、Swaggerはそのツールセットです。YAML/JSON形式でAPI仕様を記述し、Swagger UIで視覚的なドキュメントを自動生成できます。外部システム連携要件定義フェーズではAPI仕様の標準化に、基本設計フェーズでは詳細なAPI仕様書作成、コード自動生成、バリデーションに活用します。

### 主な特徴

- **完全無料**: オープンソースで無料
- **業界標準**: REST APIの事実上の標準仕様
- **コード自動生成**: サーバースタブ・クライアントSDKを自動生成
- **UIドキュメント自動生成**: Swagger UIで対話的なドキュメントを生成
- **バリデーション**: API仕様の妥当性を自動チェック
- **言語非依存**: 実装言語に依存しない仕様記述

### OpenAPI/Swaggerツールセット

- **OpenAPI Specification**: YAML/JSONでAPI仕様を記述
- **Swagger Editor**: OpenAPI仕様を編集するエディタ
- **Swagger UI**: API仕様からUIドキュメントを自動生成
- **Swagger Codegen**: サーバー・クライアントコードを自動生成

### 料金プラン

- **完全無料**: オープンソース

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- REST APIの業界標準仕様
- コード自動生成により、実装の手間を削減
- Swagger UIで対話的なドキュメントを自動生成
- バリデーション機能でAPI仕様の一貫性を保証
- 言語非依存で、実装チームと仕様を共有しやすい
- CI/CDパイプラインに組み込み可能

**デメリット**
- YAML/JSONの記述が必要（GUIではない）
- 学習曲線がやや急
- REST API専用（SOAP、GraphQL等には非対応）
- 複雑なAPIの表現が困難な場合がある

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| 要件定義/外部システム連携要件定義 | API仕様の標準化、APIドキュメント作成 | OpenAPI仕様書、Swagger UIドキュメント |
| 基本設計/外部システムI/F設計 | 詳細API仕様書、リクエスト/レスポンス定義、コード生成、バリデーション | OpenAPI仕様書、自動生成コード、APIドキュメント |

## 基本的な利用方法

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
          content:
            application/json:
              schema:
                type: object
```

### 3. 主要セクション

| セクション | 説明 | 必須 |
|-----------|------|------|
| openapi | OpenAPIバージョン（3.0.0、3.0.3等） | ○ |
| info | APIのメタ情報（タイトル、バージョン、説明） | ○ |
| servers | APIサーバーのURL | - |
| paths | APIエンドポイントの定義 | ○ |
| components | 再利用可能なコンポーネント（スキーマ、パラメータ等） | - |
| security | セキュリティスキーム | - |
| tags | APIのグループ分け | - |

### 4. Swagger UIでのプレビュー

Swagger Editorの右側パネルに、自動生成されたSwagger UIが表示されます。

## 工程別の活用方法

### 要件定義/外部システム連携要件定義での活用

要件定義フェーズでは、OpenAPIを使って外部システムとのAPI連携要件を標準化します。

#### API連携要件の定義

**例: ECサイトと外部決済システムの連携**

```yaml
openapi: 3.0.0
info:
  title: 決済システムAPI要件定義
  version: 1.0.0
  description: ECサイトと外部決済システムの連携API仕様（要件定義レベル）
  contact:
    name: ECサイト開発チーム
    email: dev@example.com

servers:
  - url: https://api.payment-provider.com/v1
    description: 決済プロバイダーAPI

paths:
  /payments:
    post:
      summary: 決済処理
      description: クレジットカード決済を実行する
      tags:
        - 決済
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                amount:
                  type: integer
                  description: 決済金額（円）
                  example: 3000
                currency:
                  type: string
                  description: 通貨コード
                  example: "JPY"
                payment_method:
                  type: object
                  properties:
                    type:
                      type: string
                      enum: [credit_card, bank_transfer]
                      example: "credit_card"
                customer:
                  type: object
                  properties:
                    email:
                      type: string
                      format: email
                      example: "customer@example.com"
                    name:
                      type: string
                      example: "山田太郎"
                order_id:
                  type: string
                  description: 注文ID
                  example: "ORD-12345"
      responses:
        '200':
          description: 決済成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  payment_id:
                    type: string
                    example: "PAY-789"
                  status:
                    type: string
                    enum: [completed, pending, failed]
                    example: "completed"
                  amount:
                    type: integer
                    example: 3000
                  created_at:
                    type: string
                    format: date-time
                    example: "2024-01-15T10:30:00Z"
        '400':
          description: リクエストエラー
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: object
                    properties:
                      code:
                        type: string
                        example: "INVALID_AMOUNT"
                      message:
                        type: string
                        example: "金額が不正です"
        '402':
          description: 決済エラー
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: object
                    properties:
                      code:
                        type: string
                        example: "CARD_DECLINED"
                      message:
                        type: string
                        example: "カードが拒否されました"

  /payments/{payment_id}:
    get:
      summary: 決済状態確認
      description: 決済の現在の状態を取得する
      tags:
        - 決済
      parameters:
        - name: payment_id
          in: path
          required: true
          schema:
            type: string
          description: 決済ID
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  payment_id:
                    type: string
                  status:
                    type: string
                    enum: [completed, pending, failed, cancelled]
                  amount:
                    type: integer
```

#### Swagger UIドキュメントの生成

1. Swagger Editorで仕様を記述
2. 右側のSwagger UIプレビューを確認
3. 外部システム担当者に共有

### 基本設計/外部システムI/F設計での活用

基本設計フェーズでは、OpenAPIを使って詳細なAPI仕様書を作成します。

#### 詳細API仕様書の作成

**例: ECサイト外部API仕様（基本設計レベル）**

```yaml
openapi: 3.0.3
info:
  title: ECサイト外部API
  version: 1.0.0
  description: |
    ECサイトの商品情報、注文情報を外部システムに提供するREST API

    ## 認証
    - API Keyによる認証（Authorizationヘッダー）

    ## レート制限
    - 1分間に60リクエストまで

    ## エラーハンドリング
    - HTTPステータスコードに準拠
    - エラー詳細はJSONボディで返却
  contact:
    name: ECサイトAPI サポート
    email: api-support@example.com
    url: https://example.com/api-support
  license:
    name: Proprietary
  termsOfService: https://example.com/terms

servers:
  - url: https://api.example.com/v1
    description: 本番環境
  - url: https://api-staging.example.com/v1
    description: ステージング環境
  - url: http://localhost:3000/v1
    description: ローカル開発環境

tags:
  - name: 商品管理
    description: 商品の取得・検索
  - name: 注文管理
    description: 注文の作成・取得・更新

paths:
  /products:
    get:
      summary: 商品一覧取得
      description: 商品の一覧をページネーション付きで取得する
      operationId: listProducts
      tags:
        - 商品管理
      security:
        - ApiKeyAuth: []
      parameters:
        - name: page
          in: query
          description: ページ番号（1から開始）
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
            example: 1
        - name: limit
          in: query
          description: 1ページあたりの件数
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
            example: 20
        - name: category
          in: query
          description: カテゴリID（フィルタリング用）
          required: false
          schema:
            type: string
            example: "electronics"
        - name: sort
          in: query
          description: ソート順
          required: false
          schema:
            type: string
            enum: [price_asc, price_desc, name_asc, name_desc, created_desc]
            default: created_desc
            example: "price_asc"
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/TooManyRequests'

  /products/{id}:
    get:
      summary: 商品詳細取得
      description: 指定したIDの商品詳細を取得する
      operationId: getProduct
      tags:
        - 商品管理
      security:
        - ApiKeyAuth: []
      parameters:
        - name: id
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
                $ref: '#/components/schemas/Product'
        '404':
          $ref: '#/components/responses/NotFound'

  /orders:
    post:
      summary: 注文作成
      description: 新規注文を作成する
      operationId: createOrder
      tags:
        - 注文管理
      security:
        - ApiKeyAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: 注文作成成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
      description: |
        API Key認証

        例: Authorization: Bearer YOUR_API_KEY

  schemas:
    Product:
      type: object
      properties:
        product_id:
          type: integer
          description: 商品ID
          example: 101
        name:
          type: string
          description: 商品名
          maxLength: 200
          example: "ノートPC"
        price:
          type: integer
          description: 価格（円）
          minimum: 0
          example: 89800
        stock_quantity:
          type: integer
          description: 在庫数
          minimum: 0
          example: 50
        category_id:
          type: string
          description: カテゴリID
          example: "electronics"
        image_url:
          type: string
          format: uri
          description: 商品画像URL
          example: "https://example.com/images/101.jpg"
        created_at:
          type: string
          format: date-time
          description: 作成日時
          example: "2024-01-01T00:00:00Z"
        updated_at:
          type: string
          format: date-time
          description: 更新日時
          example: "2024-01-15T10:30:00Z"
      required:
        - product_id
        - name
        - price
        - stock_quantity

    CreateOrderRequest:
      type: object
      properties:
        customer_id:
          type: integer
          description: 顧客ID
          example: 12345
        items:
          type: array
          description: 注文商品リスト
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
                description: 数量
                minimum: 1
                example: 2
              unit_price:
                type: integer
                description: 単価（円）
                minimum: 0
                example: 89800
            required:
              - product_id
              - quantity
              - unit_price
        shipping_address:
          $ref: '#/components/schemas/Address'
        payment_method:
          type: string
          enum: [credit_card, bank_transfer, cash_on_delivery]
          description: 支払方法
          example: "credit_card"
      required:
        - customer_id
        - items
        - shipping_address
        - payment_method

    Address:
      type: object
      properties:
        postal_code:
          type: string
          pattern: '^\d{3}-\d{4}$'
          description: 郵便番号
          example: "100-0001"
        prefecture:
          type: string
          description: 都道府県
          example: "東京都"
        city:
          type: string
          description: 市区町村
          example: "千代田区"
        address_line:
          type: string
          description: 番地
          example: "千代田1-1"
        name:
          type: string
          description: 宛名
          example: "山田太郎"
        phone:
          type: string
          pattern: '^\d{2,4}-\d{2,4}-\d{4}$'
          description: 電話番号
          example: "03-1234-5678"
      required:
        - postal_code
        - prefecture
        - city
        - address_line
        - name
        - phone

    Order:
      type: object
      properties:
        order_id:
          type: string
          description: 注文ID
          example: "ORD-789"
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered, cancelled]
          description: 注文ステータス
          example: "pending"
        total_amount:
          type: integer
          description: 合計金額（円）
          example: 179600
        created_at:
          type: string
          format: date-time
          description: 作成日時
          example: "2024-01-15T10:30:00Z"
        estimated_delivery:
          type: string
          format: date
          description: 配送予定日
          example: "2024-01-18"

    Pagination:
      type: object
      properties:
        current_page:
          type: integer
          description: 現在のページ番号
          example: 1
        total_pages:
          type: integer
          description: 総ページ数
          example: 10
        total_items:
          type: integer
          description: 総件数
          example: 200
        items_per_page:
          type: integer
          description: 1ページあたりの件数
          example: 20

    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              description: エラーコード
              example: "INVALID_PARAMETER"
            message:
              type: string
              description: エラーメッセージ
              example: "パラメータが不正です"
            details:
              type: array
              description: エラー詳細
              items:
                type: object
                properties:
                  field:
                    type: string
                    example: "limit"
                  issue:
                    type: string
                    example: "1〜100の範囲で指定してください"

  responses:
    BadRequest:
      description: リクエストエラー
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: 認証エラー
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                    example: "UNAUTHORIZED"
                  message:
                    type: string
                    example: "APIキーが無効です"
    NotFound:
      description: リソースが見つかりません
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                    example: "NOT_FOUND"
                  message:
                    type: string
                    example: "指定されたリソースが見つかりません"
    TooManyRequests:
      description: レート制限超過
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                    example: "RATE_LIMIT_EXCEEDED"
                  message:
                    type: string
                    example: "リクエスト制限を超えました。しばらくしてから再度お試しください"
```

#### コード自動生成

**サーバースタブの生成:**

```bash
# Swagger Codegenを使用
swagger-codegen generate -i openapi.yaml -l spring -o ./server

# OpenAPI Generatorを使用（推奨）
openapi-generator generate -i openapi.yaml -g spring -o ./server
```

**クライアントSDKの生成:**

```bash
# JavaScriptクライアント
openapi-generator generate -i openapi.yaml -g javascript -o ./client-js

# Pythonクライアント
openapi-generator generate -i openapi.yaml -g python -o ./client-python

# Javaクライアント
openapi-generator generate -i openapi.yaml -g java -o ./client-java
```

#### Swagger UIのホスティング

```bash
# Dockerで起動
docker run -p 8080:8080 -e SWAGGER_JSON=/openapi.yaml -v $(pwd):/openapi.yaml swaggerapi/swagger-ui
```

ブラウザで `http://localhost:8080` にアクセス

#### バリデーション

OpenAPI仕様の妥当性をチェック:

```bash
# Swagger CLIでバリデーション
swagger-cli validate openapi.yaml

# OpenAPI CLIでバリデーション
openapi-generator validate -i openapi.yaml
```

## 公式ドキュメント

- **OpenAPI Specification**: [OpenAPI 3.0 Spec](https://swagger.io/specification/)
- **Swagger Editor**: [Swagger Editor](https://editor.swagger.io/)
- **Swagger UI**: [Swagger UI](https://swagger.io/tools/swagger-ui/)
- **Swagger Codegen**: [Swagger Codegen](https://swagger.io/tools/swagger-codegen/)
- **OpenAPI Generator**: [OpenAPI Generator](https://openapi-generator.tech/)

## 学習リソース

- **OpenAPI公式ガイド**: [OpenAPI Guide](https://swagger.io/docs/specification/about/)
- **OpenAPI Tutorial**: [Getting Started with OpenAPI](https://swagger.io/docs/specification/basic-structure/)
- **Swagger Blog**: [Swagger Blog](https://swagger.io/blog/)

## 関連リンク

- [Postman](https://www.postman.com/)（APIテストツール）
- [ReDoc](https://redocly.github.io/redoc/)（OpenAPIドキュメントジェネレーター）
- [Stoplight](https://stoplight.io/)（API設計ツール）
- [Insomnia](https://insomnia.rest/)（APIクライアント）
