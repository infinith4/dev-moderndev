# Postman

## 概要

Postmanは、API開発・テストプラットフォームで、REST APIやSOAP APIの仕様書作成、テスト、モックサーバー機能を提供します。外部システム連携要件定義フェーズではAPI仕様の定義とドキュメント化に、基本設計フェーズではREST API仕様の詳細設計、リクエスト/レスポンス仕様の定義、認証方式の設計に活用します。

### 主な特徴

- **API開発標準ツール**: 業界標準のAPIツール
- **OpenAPI対応**: OpenAPI 3.0仕様のインポート・エクスポート
- **ドキュメント自動生成**: APIリクエストから自動的にドキュメント生成
- **コレクション管理**: APIをグループ化して管理
- **モックサーバー**: 実際のAPIがなくてもモックで動作確認可能
- **テスト機能**: 自動テストケースの定義と実行

### 料金プラン

- **Free版**: 基本機能（個人利用、制限あり）
- **Basic**: $12-14/月/ユーザー（チーム協業機能）
- **Professional**: $29/月/ユーザー（モックサーバー、モニタリング、高度な機能）
- **Enterprise**: カスタム価格（SSO、高度なガバナンス、大企業向け）

### メリット・デメリット

**メリット**
- API開発のデファクトスタンダード
- 無料プランで基本機能が利用可能
- OpenAPI 3.0に対応し、業界標準の仕様書を作成可能
- APIリクエスト・レスポンスの例を簡単に記録し、ドキュメント化できる
- コレクション管理により、APIを体系的に整理できる
- モックサーバー機能により、実装前にAPIの動作確認が可能
- 自動テスト機能でAPIの動作確認が容易
- APIリクエスト/レスポンスを直感的に定義

**デメリット**
- 無料版は機能制限あり（チーム機能、モックサーバーは有料）
- 複雑なワークフローの定義は困難
- 大規模なAPI仕様書には向いていない（OpenAPIと併用推奨）
- 学習曲線がやや急

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| 要件定義/外部システム連携要件定義 | API仕様の定義、APIドキュメント作成、モックサーバーによる検証 | API要件定義書、APIコレクション |
| 基本設計/外部システムI/F設計 | APIエンドポイント設計、リクエスト/レスポンス仕様、認証設計、エラーハンドリング設計 | API仕様書、モックサーバー、テストケース |

## 基本的な利用方法

### 1. アカウント作成とインストール

#### Webアプリケーション

1. [Postman公式サイト](https://www.postman.com/)にアクセス
2. 「Sign Up for Free」をクリック
3. メールアドレスまたはGoogle/GitHubアカウントで登録
4. Webブラウザで直接利用可能

#### デスクトップアプリ

1. Postman公式サイトから「Download the App」をクリック
2. OSに応じたインストーラーをダウンロード
3. インストールしてログイン

### 2. コレクションの作成

コレクションは、関連するAPIリクエストをグループ化するためのコンテナです。

1. 左側サイドバーで「Collections」を選択
2. 「+ New Collection」ボタンをクリック
3. コレクション名を入力（例: "ECサイトAPI"）
4. 説明を追加（オプション）

### 3. APIリクエストの定義

#### GETリクエストの例

**エンドポイント**: 商品一覧取得

1. コレクション内で「Add Request」をクリック
2. リクエスト名を入力: "商品一覧取得"
3. HTTPメソッドを選択: **GET**
4. URLを入力: `https://api.example.com/v1/products`
5. 「Params」タブでクエリパラメータを追加:
   - `page`: 1
   - `limit`: 20
   - `category`: electronics
6. 「Headers」タブでヘッダーを追加:
   - `Authorization`: Bearer {token}
   - `Content-Type`: application/json
7. 「Save」ボタンをクリック

#### POSTリクエストの例

**エンドポイント**: 注文作成

1. 「Add Request」→ リクエスト名: "注文作成"
2. HTTPメソッド: **POST**
3. URL: `https://api.example.com/v1/orders`
4. 「Body」タブ→「raw」→「JSON」を選択
5. JSONボディを入力:

```json
{
  "customer_id": 12345,
  "items": [
    {
      "product_id": 101,
      "quantity": 2,
      "price": 1500
    }
  ],
  "total_amount": 3000,
  "shipping_address": {
    "postal_code": "100-0001",
    "address": "東京都千代田区千代田1-1"
  }
}
```

6. 「Save」ボタンをクリック

### 4. レスポンスの定義

1. リクエストを保存後、「Examples」タブを選択
2. 「Add Example」をクリック
3. Example名: "成功レスポンス (200 OK)"
4. ステータスコード: 200
5. レスポンスボディを入力:

```json
{
  "status": "success",
  "data": {
    "order_id": 789,
    "status": "pending",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

6. 「Save Example」をクリック

### 5. モックサーバーの作成

1. コレクションを選択
2. 「...」メニュー→「Mock Collection」を選択
3. Mock名を入力: "ECサイトAPI Mock"
4. 「Create Mock Server」をクリック
5. モックサーバーURLが生成される（例: `https://xxxxxxxx.mock.pstmn.io`）

## 工程別の活用方法

### 要件定義/外部システム連携要件定義での活用

要件定義フェーズでは、Postmanを使って外部システムとのAPI連携要件を定義します。

#### API連携要件の定義

**例: ECサイトと外部決済システムの連携**

**1. コレクションの作成**

コレクション名: "決済システムAPI要件"

**APIエンドポイント一覧:**

| API名 | メソッド | エンドポイント | 説明 |
|------|---------|--------------|------|
| 決済処理 | POST | /api/v1/payments | クレジットカード決済を実行 |
| 決済状態確認 | GET | /api/v1/payments/{payment_id} | 決済状態を取得 |
| 決済キャンセル | POST | /api/v1/payments/{payment_id}/cancel | 決済をキャンセル |
| 返金処理 | POST | /api/v1/refunds | 返金を実行 |

**2. API仕様の定義**

**決済処理API (POST /api/v1/payments)**

**リクエスト:**
```json
{
  "amount": 3000,
  "currency": "JPY",
  "payment_method": {
    "type": "credit_card",
    "card_number": "4111111111111111",
    "expiry_month": "12",
    "expiry_year": "2025",
    "cvv": "123"
  },
  "customer": {
    "email": "customer@example.com",
    "name": "山田太郎"
  },
  "order_id": "ORD-12345"
}
```

**レスポンス (成功):**
```json
{
  "payment_id": "PAY-789",
  "status": "completed",
  "amount": 3000,
  "currency": "JPY",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**エラーレスポンス:**
```json
{
  "error": {
    "code": "CARD_DECLINED",
    "message": "カードが拒否されました"
  }
}
```

**3. モックサーバーによる検証**

1. コレクションからモックサーバーを作成
2. モックサーバーURLを外部システム担当者に共有
3. 実装前にAPI仕様を検証

#### API要件定義書の作成

1. コレクションを選択
2. 「View Documentation」をクリック
3. 「Publish」→公開URLが生成される
4. 外部システム担当者と要件を共有

### 基本設計/外部システムI/F設計での活用

基本設計フェーズでは、Postmanを使って詳細なAPI仕様を設計します。

#### ワークスペースの作成

1. Postmanを起動
2. 左上の「Workspaces」→「Create Workspace」
3. ワークスペース名: "ECサイトAPI設計"
4. Visibility: "Team"または"Personal"
5. 「Create Workspace」をクリック

#### コレクションの詳細設計

**例: ECサイト外部API仕様**

**1. コレクション作成**

コレクション名: "ECサイト外部API v1.0"
Description: "ECサイトの商品情報、注文情報を外部システムに提供するAPI"

**2. コレクションの変数設定**

コレクションを選択 → 「Variables」タブ

| Variable | Type | Initial Value | Current Value |
|----------|------|---------------|---------------|
| base_url | default | https://api.example.com/v1 | https://api.example.com/v1 |
| api_key | secret | your_api_key_here | ******** |

#### APIエンドポイントの設計

**エンドポイント一覧:**

| No. | エンドポイント | メソッド | 説明 |
|-----|--------------|---------|------|
| 1 | /products | GET | 商品一覧取得 |
| 2 | /products/{id} | GET | 商品詳細取得 |
| 3 | /orders | POST | 注文作成 |
| 4 | /orders/{id} | GET | 注文詳細取得 |
| 5 | /orders/{id}/status | PUT | 注文ステータス更新 |

**1. 商品一覧取得API (GET /products)**

**リクエスト仕様:**

クエリパラメータ:
- `page` (integer, optional): ページ番号（デフォルト: 1）
- `limit` (integer, optional): 1ページあたりの件数（デフォルト: 20、最大: 100）
- `category` (string, optional): カテゴリID
- `sort` (string, optional): ソート順（price_asc, price_desc, name_asc）

Headers:
- `Authorization`: Bearer {api_key}
- `Content-Type`: application/json

**レスポンス仕様:**

ステータスコード: 200 OK

```json
{
  "data": [
    {
      "product_id": 101,
      "name": "ノートPC",
      "price": 89800,
      "stock_quantity": 50,
      "category_id": "electronics",
      "image_url": "https://example.com/images/101.jpg"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 200,
    "items_per_page": 20
  }
}
```

**エラーレスポンス:**

ステータスコード: 401 Unauthorized
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "APIキーが無効です"
  }
}
```

ステータスコード: 400 Bad Request
```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "limitパラメータは1〜100の範囲で指定してください"
  }
}
```

**2. 注文作成API (POST /orders)**

**リクエスト仕様:**

Headers:
- `Authorization`: Bearer {api_key}
- `Content-Type`: application/json

Body:
```json
{
  "customer_id": 12345,
  "items": [
    {
      "product_id": 101,
      "quantity": 2,
      "unit_price": 89800
    }
  ],
  "shipping_address": {
    "postal_code": "100-0001",
    "prefecture": "東京都",
    "city": "千代田区",
    "address_line": "千代田1-1",
    "name": "山田太郎",
    "phone": "03-1234-5678"
  },
  "payment_method": "credit_card"
}
```

**レスポンス仕様:**

ステータスコード: 201 Created

```json
{
  "order_id": "ORD-789",
  "status": "pending",
  "total_amount": 179600,
  "created_at": "2024-01-15T10:30:00Z",
  "estimated_delivery": "2024-01-18"
}
```

#### 認証設計

**1. API Key認証**

コレクションレベルで認証を設定:

1. コレクションを選択 → 「Authorization」タブ
2. Type: **API Key**
3. Key: `Authorization`
4. Value: `Bearer {{api_key}}`
5. Add to: **Header**

**2. OAuth 2.0認証**

1. Type: **OAuth 2.0**
2. Grant Type: **Authorization Code**
3. Callback URL: `https://example.com/callback`
4. Auth URL: `https://auth.example.com/oauth/authorize`
5. Access Token URL: `https://auth.example.com/oauth/token`
6. Client ID: `your_client_id`
7. Client Secret: `your_client_secret`
8. Scope: `read:products write:orders`

#### テストケースの定義

「Tests」タブでテストケースを定義:

```javascript
// ステータスコードのテスト
pm.test("ステータスコードは200", function () {
    pm.response.to.have.status(200);
});

// レスポンスボディの検証
pm.test("商品データが存在する", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.data).to.be.an('array');
    pm.expect(jsonData.data.length).to.be.greaterThan(0);
});

// レスポンスタイムの検証
pm.test("レスポンスタイムは500ms以下", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

#### モックサーバーの構築

1. コレクションを選択 → 「...」→「Mock Collection」
2. Mock名: "ECサイトAPI Mock v1.0"
3. 「Create Mock Server」をクリック
4. モックURL取得: `https://xxxxxxxx.mock.pstmn.io`
5. Examplesを追加していれば、モックサーバーが自動応答

#### ドキュメント生成

1. コレクションを選択 → 「View Documentation」
2. 「Publish」ボタンをクリック
3. 公開URLが生成される
4. 外部システム開発者に共有

#### OpenAPI仕様のエクスポート

1. コレクションを選択 → 「Export」
2. Format: **OpenAPI 3.0**
3. Export → JSONまたはYAML形式で保存
4. Swagger Editorで編集可能

## 公式ドキュメント

- **公式サイト**: [Postman](https://www.postman.com/)
- **ドキュメント**: [Postman Learning Center](https://learning.postman.com/)
- **API Documentation**: [Documenting APIs](https://learning.postman.com/docs/publishing-your-api/documenting-your-api/)
- **Mock Servers**: [Mock Servers Guide](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)
- **Testing APIs**: [Writing Tests](https://learning.postman.com/docs/writing-scripts/test-scripts/)

## 学習リソース

- **Postman公式チュートリアル**: [Get Started with Postman](https://learning.postman.com/docs/getting-started/introduction/)
- **Postman YouTube**: [Official Channel](https://www.youtube.com/c/Postman)
- **Postman Blog**: [Postman Blog](https://blog.postman.com/)

## 関連リンク

- [Swagger/OpenAPI](https://swagger.io/)（API仕様書作成）
- [Insomnia](https://insomnia.rest/)（代替ツール）
- [HTTPie](https://httpie.io/)（CLI APIツール）
- [cURL](https://curl.se/)（コマンドラインHTTPクライアント）
