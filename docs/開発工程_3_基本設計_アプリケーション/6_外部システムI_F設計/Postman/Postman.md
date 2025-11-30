# Postman（外部システムI/F設計）

## 概要

Postmanは、API開発・テストプラットフォームで、基本設計フェーズではREST API仕様の詳細設計、リクエスト/レスポンス仕様の定義、エラーハンドリング設計、認証方式の設計に活用します。APIのモックサーバー機能により、実装前にI/F仕様を検証できます。

### 基本設計フェーズでの活用

- **APIエンドポイント設計**: URL、HTTPメソッド、パスパラメータ、クエリパラメータ
- **リクエスト仕様**: Headers、Body（JSON/XML）、認証情報
- **レスポンス仕様**: ステータスコード、レスポンスボディ、エラーレスポンス
- **認証設計**: API Key、Bearer Token、OAuth 2.0、Basic Auth
- **モックサーバー**: 実装前のI/F検証用モックAPI
- **テストケース定義**: 正常系・異常系のテストシナリオ

### 料金プラン

- **無料プラン**: 基本機能、個人利用
- **Basic**: $12/月（チームコラボレーション）
- **Professional**: $29/月（モックサーバー、モニタリング）
- **Enterprise**: カスタム価格（SSO、高度なガバナンス）

### メリット・デメリット

**メリット**
- 無料プランで基本機能が利用可能
- APIリクエスト/レスポンスを直感的に定義
- モックサーバーで実装前にI/F検証が可能
- コレクション機能でAPI仕様を体系的に管理
- 自動テスト機能でAPIの動作確認が容易
- OpenAPI仕様のインポート/エクスポート対応

**デメリット**
- 無料プランはモックサーバーに制限あり
- 大規模なAPI仕様書には向いていない（OpenAPIと併用推奨）

## 利用方法

### 1. Postmanのインストール

1. [Postman公式サイト](https://www.postman.com/)にアクセス
2. 「Download the App」をクリック
3. OS別のインストーラーをダウンロード
4. インストーラーを実行
5. Postmanアカウントを作成（無料）

### 2. ワークスペースの作成

1. Postmanを起動
2. 左上の「Workspaces」→「Create Workspace」
3. ワークスペース名: "ECサイトAPI設計"
4. Visibility: "Team"または"Personal"
5. 「Create Workspace」をクリック

### 3. コレクションの作成

#### 例: ECサイト外部API仕様

**1. 新規コレクションの作成**

1. 左サイドバーの「Collections」タブ
2. 「+」ボタンをクリック
3. コレクション名: "ECサイト外部API v1.0"
4. Description: "ECサイトの商品情報、注文情報を外部システムに提供するAPI"

**2. コレクションの変数設定**

1. コレクションを選択 → 「Variables」タブ
2. 変数を追加:

| Variable | Type | Initial Value | Current Value |
|----------|------|---------------|---------------|
| base_url | default | https://api.example.com/v1 | https://api.example.com/v1 |
| api_key | secret | your_api_key_here | ******** |

### 4. APIエンドポイントの設計

#### エンドポイント一覧

| No. | エンドポイント | メソッド | 説明 |
|-----|--------------|---------|------|
| 1 | `/products` | GET | 商品一覧取得 |
| 2 | `/products/{id}` | GET | 商品詳細取得 |
| 3 | `/orders` | POST | 注文作成 |
| 4 | `/orders/{id}` | GET | 注文詳細取得 |
| 5 | `/orders/{id}` | PUT | 注文更新 |
| 6 | `/orders/{id}` | DELETE | 注文キャンセル |

#### エンドポイント1: GET /products（商品一覧取得）

**1. リクエストの作成**

1. コレクション内で「Add request」をクリック
2. Request name: "商品一覧取得"
3. HTTPメソッド: GET
4. URL: `{{base_url}}/products`

**2. クエリパラメータの定義**

「Params」タブで以下を追加:

| Key | Value | Description |
|-----|-------|-------------|
| page | 1 | ページ番号（デフォルト: 1） |
| limit | 20 | 1ページあたりの件数（デフォルト: 20、最大: 100） |
| category_id | 5 | カテゴリID（オプション） |
| sort | price_asc | ソート順（price_asc, price_desc, name_asc, created_at_desc） |

**3. ヘッダーの設定**

「Headers」タブで以下を追加:

| Key | Value | Description |
|-----|-------|-------------|
| Authorization | Bearer {{api_key}} | API認証トークン |
| Content-Type | application/json | リクエストボディの形式 |
| Accept | application/json | レスポンスの形式 |

**4. レスポンス仕様の定義**

「Tests」タブでレスポンス例を記載:

**正常系（200 OK）:**

```json
{
  "status": "success",
  "data": {
    "products": [
      {
        "product_id": 101,
        "product_name": "ワイヤレスマウス",
        "category_id": 5,
        "category_name": "PC周辺機器",
        "price": 2980,
        "stock_quantity": 150,
        "image_url": "https://example.com/images/product_101.jpg",
        "created_at": "2025-01-10T10:30:00Z"
      },
      {
        "product_id": 102,
        "product_name": "USB-Cハブ",
        "category_id": 5,
        "category_name": "PC周辺機器",
        "price": 3480,
        "stock_quantity": 80,
        "image_url": "https://example.com/images/product_102.jpg",
        "created_at": "2025-01-12T15:20:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 10,
      "total_items": 200,
      "items_per_page": 20
    }
  }
}
```

**異常系（400 Bad Request）:**

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "limitパラメータは1〜100の範囲で指定してください",
    "field": "limit",
    "value": 150
  }
}
```

**異常系（401 Unauthorized）:**

```json
{
  "status": "error",
  "error": {
    "code": "UNAUTHORIZED",
    "message": "認証に失敗しました。有効なAPIキーを指定してください"
  }
}
```

#### エンドポイント2: GET /products/{id}（商品詳細取得）

**1. リクエストの作成**

1. Request name: "商品詳細取得"
2. HTTPメソッド: GET
3. URL: `{{base_url}}/products/:product_id`

**2. パスパラメータの定義**

「Params」タブのPath Variables:

| Key | Value | Description |
|-----|-------|-------------|
| product_id | 101 | 商品ID（必須） |

**3. レスポンス仕様**

**正常系（200 OK）:**

```json
{
  "status": "success",
  "data": {
    "product_id": 101,
    "product_name": "ワイヤレスマウス",
    "description": "静音設計の高性能ワイヤレスマウス。Bluetooth 5.0対応。",
    "category_id": 5,
    "category_name": "PC周辺機器",
    "price": 2980,
    "stock_quantity": 150,
    "images": [
      "https://example.com/images/product_101_main.jpg",
      "https://example.com/images/product_101_sub1.jpg"
    ],
    "specifications": {
      "weight": "75g",
      "dimensions": "10.5 x 6.8 x 3.8 cm",
      "battery_life": "最大18ヶ月"
    },
    "created_at": "2025-01-10T10:30:00Z",
    "updated_at": "2025-01-10T10:30:00Z"
  }
}
```

**異常系（404 Not Found）:**

```json
{
  "status": "error",
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "指定された商品が見つかりません",
    "product_id": 9999
  }
}
```

#### エンドポイント3: POST /orders（注文作成）

**1. リクエストの作成**

1. Request name: "注文作成"
2. HTTPメソッド: POST
3. URL: `{{base_url}}/orders`

**2. リクエストボディの定義**

「Body」タブで「raw」→「JSON」を選択:

```json
{
  "customer_id": 1001,
  "items": [
    {
      "product_id": 101,
      "quantity": 2
    },
    {
      "product_id": 102,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "postal_code": "100-0001",
    "prefecture": "東京都",
    "city": "千代田区",
    "street": "千代田1-1-1",
    "building": "サンプルビル101"
  },
  "payment_method": "credit_card",
  "memo": "午前中配送希望"
}
```

**3. レスポンス仕様**

**正常系（201 Created）:**

```json
{
  "status": "success",
  "data": {
    "order_id": 50001,
    "customer_id": 1001,
    "order_date": "2025-01-15T14:30:00Z",
    "status": "pending",
    "items": [
      {
        "product_id": 101,
        "product_name": "ワイヤレスマウス",
        "quantity": 2,
        "unit_price": 2980,
        "subtotal": 5960
      },
      {
        "product_id": 102,
        "product_name": "USB-Cハブ",
        "quantity": 1,
        "unit_price": 3480,
        "subtotal": 3480
      }
    ],
    "total_amount": 9440,
    "tax_amount": 944,
    "grand_total": 10384,
    "shipping_address": {
      "postal_code": "100-0001",
      "prefecture": "東京都",
      "city": "千代田区",
      "street": "千代田1-1-1",
      "building": "サンプルビル101"
    },
    "payment_method": "credit_card"
  }
}
```

**異常系（422 Unprocessable Entity）:**

```json
{
  "status": "error",
  "error": {
    "code": "OUT_OF_STOCK",
    "message": "在庫不足のため注文できません",
    "details": [
      {
        "product_id": 101,
        "requested_quantity": 2,
        "available_quantity": 1
      }
    ]
  }
}
```

### 5. 認証方式の設計

#### Bearer Token認証

**1. Authorizationタブの設定**

1. リクエストを選択 → 「Authorization」タブ
2. Type: "Bearer Token"
3. Token: `{{api_key}}`

#### OAuth 2.0認証

**1. OAuth 2.0設定**

1. Type: "OAuth 2.0"
2. Grant Type: "Authorization Code"
3. Callback URL: `https://example.com/oauth/callback`
4. Auth URL: `https://auth.example.com/oauth/authorize`
5. Access Token URL: `https://auth.example.com/oauth/token`
6. Client ID: `{{client_id}}`
7. Client Secret: `{{client_secret}}`
8. Scope: `read:products write:orders`

### 6. テストケースの定義

#### Testsタブでの自動テスト

**正常系テスト:**

```javascript
// ステータスコード200の確認
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// レスポンスボディがJSONであることを確認
pm.test("Response is JSON", function () {
    pm.response.to.be.json;
});

// data.productsが配列であることを確認
pm.test("products is an array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.data.products).to.be.an('array');
});

// 商品数が20件以下であることを確認
pm.test("products count is <= 20", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.data.products.length).to.be.at.most(20);
});

// 各商品にproduct_idが存在することを確認
pm.test("Each product has product_id", function () {
    var jsonData = pm.response.json();
    jsonData.data.products.forEach(function(product) {
        pm.expect(product).to.have.property('product_id');
        pm.expect(product).to.have.property('product_name');
        pm.expect(product).to.have.property('price');
    });
});
```

### 7. モックサーバーの作成

#### 実装前のI/F検証用モック

**1. モックサーバーの作成**

1. コレクションを選択 → 「...」メニュー → 「Mock Collection」
2. Mock Server Name: "ECサイトAPI Mock"
3. 「Create Mock Server」をクリック
4. Mock URLが生成される: `https://xxxxxx.mock.pstmn.io`

**2. モックレスポンスの設定**

1. リクエストを選択 → 「Save Response」→「Save as example」
2. Example name: "商品一覧取得 - 正常系"
3. レスポンスボディを入力（上記のJSON）
4. Status Code: 200

**3. モックサーバーのテスト**

```bash
curl -X GET "https://xxxxxx.mock.pstmn.io/v1/products?page=1&limit=20" \
  -H "Authorization: Bearer test_api_key"
```

### 8. I/F設計書の自動生成

#### Postman Documentationの活用

**1. ドキュメント生成**

1. コレクションを選択 → 「View Documentation」
2. 「Publish」をクリック
3. 公開URLが生成される
4. 外部システム開発者に共有

**2. ドキュメントの構成**

- **エンドポイント一覧**: 全APIエンドポイントのリスト
- **リクエスト例**: 各エンドポイントのリクエスト例
- **レスポンス例**: 正常系・異常系のレスポンス
- **認証方法**: 認証方式の説明

### 9. OpenAPI仕様のエクスポート

#### OpenAPI 3.0形式での出力

1. コレクションを選択 → 「...」メニュー → 「Export」
2. Format: "OpenAPI 3.0"
3. 「Export」をクリック
4. .yamlファイルをダウンロード

**生成されるOpenAPI仕様例:**

```yaml
openapi: 3.0.0
info:
  title: ECサイト外部API
  version: 1.0.0
  description: ECサイトの商品情報、注文情報を外部システムに提供するAPI

servers:
  - url: https://api.example.com/v1
    description: Production server

paths:
  /products:
    get:
      summary: 商品一覧取得
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductListResponse'
```

### 10. 環境変数の管理

#### 開発・本番環境の切り替え

**1. 環境の作成**

1. 左サイドバー「Environments」→「+」ボタン
2. Environment name: "開発環境"
3. 変数を追加:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| base_url | https://api-dev.example.com/v1 | https://api-dev.example.com/v1 |
| api_key | dev_api_key | ******** |

**2. 本番環境の作成**

同様に "本番環境" を作成:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| base_url | https://api.example.com/v1 | https://api.example.com/v1 |
| api_key | prod_api_key | ******** |

**3. 環境の切り替え**

右上の環境セレクターで「開発環境」または「本番環境」を選択

### 11. I/F設計書への統合

#### 基本設計書の構成

**1. I/F概要**

- システム間I/F一覧
- 通信方式（REST API）
- 認証方式（Bearer Token）
- データ形式（JSON）

**2. エンドポイント仕様**

各エンドポイントごとに以下を記載:

- **URL**: `/products`
- **HTTPメソッド**: GET
- **概要**: 商品一覧を取得する
- **パラメータ**: クエリパラメータ一覧
- **リクエスト例**: Postmanのリクエスト例
- **レスポンス例**: 正常系・異常系のJSON
- **ステータスコード一覧**: 200, 400, 401, 404, 500

**3. エラーコード一覧**

| コード | メッセージ | HTTP Status | 説明 |
|--------|-----------|-------------|------|
| INVALID_PARAMETER | パラメータが不正です | 400 | リクエストパラメータのバリデーションエラー |
| UNAUTHORIZED | 認証に失敗しました | 401 | APIキーが無効または期限切れ |
| PRODUCT_NOT_FOUND | 商品が見つかりません | 404 | 指定された商品IDが存在しない |
| OUT_OF_STOCK | 在庫不足です | 422 | 商品の在庫が不足 |
| INTERNAL_SERVER_ERROR | サーバーエラー | 500 | サーバー内部エラー |

## 公式ドキュメント

- **公式サイト**: [Postman](https://www.postman.com/)
- **Learning Center**: [Postman Learning Center](https://learning.postman.com/)
- **API Documentation**: [Documenting your API](https://learning.postman.com/docs/publishing-your-api/documenting-your-api/)
- **Mock Servers**: [Setting up mock servers](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)

## 学習リソース

- **Postman Tutorial**: [Postman Beginner's Course](https://www.youtube.com/watch?v=VywxIQ2ZXw4)
- **API Testing**: [API Testing with Postman](https://www.guru99.com/postman-tutorial.html)

## 関連リンク

- [OpenAPI Specification](https://swagger.io/specification/)（API仕様標準）
- [Insomnia](https://insomnia.rest/)（代替APIクライアント）
- [HTTPie](https://httpie.io/)（コマンドラインHTTPクライアント）
