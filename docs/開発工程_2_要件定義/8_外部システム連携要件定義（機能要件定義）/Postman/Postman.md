# Postman

## 概要

Postmanは、API開発・テストプラットフォームで、REST APIやSOAP APIの仕様書作成、テスト、モックサーバー機能を提供します。外部システム連携要件定義では、API仕様の定義とドキュメント化に活用できます。

### 主な特徴

- **API開発標準ツール**: 業界標準のAPIツール
- **OpenAPI対応**: OpenAPI 3.0仕様のインポート・エクスポート
- **ドキュメント自動生成**: APIリクエストから自動的にドキュメント生成
- **コレクション管理**: APIをグループ化して管理
- **モックサーバー**: 実際のAPIがなくてもモックで動作確認可能

### 料金プラン

- **Free版**: 基本機能（個人利用、制限あり）
- **Basic**: $14/月/ユーザー（チーム協業機能）
- **Professional**: $29/月/ユーザー（高度な機能）
- **Enterprise**: カスタム価格（大企業向け）

### メリット・デメリット

**メリット**
- API開発のデファクトスタンダード
- OpenAPI 3.0に対応し、業界標準の仕様書を作成可能
- APIリクエスト・レスポンスの例を簡単に記録し、ドキュメント化できる
- コレクション管理により、APIを体系的に整理できる
- モックサーバー機能により、実装前にAPIの動作確認が可能

**デメリット**
- 無料版は機能制限あり（チーム機能は有料）
- 複雑なワークフローの定義は困難
- チーム機能は有料プランが必要
- 学習曲線がやや急

## 利用方法

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

1. 「Add Request」をクリック
2. リクエスト名: "注文作成"
3. HTTPメソッド: **POST**
4. URL: `https://api.example.com/v1/orders`
5. 「Headers」タブ:
   - `Authorization`: Bearer {token}
   - `Content-Type`: application/json
6. 「Body」タブ:
   - 「raw」を選択
   - 形式を「JSON」に変更
   - リクエストボディを入力:

```json
{
  "customer_id": 12345,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 1000
    },
    {
      "product_id": 5,
      "quantity": 1,
      "price": 5000
    }
  ],
  "shipping_address": {
    "postal_code": "123-4567",
    "address": "東京都渋谷区..."
  },
  "payment_method": "credit_card"
}
```

7. 「Save」をクリック

### 4. レスポンス例の追加

APIの仕様書には、レスポンス例が必要です。

1. リクエストを選択
2. 「Save Response」→「Save as Example」をクリック
3. 例の名前を入力（例: "成功レスポンス（200 OK）"）
4. レスポンスボディを編集:

```json
{
  "status": "success",
  "data": {
    "order_id": 98765,
    "customer_id": 12345,
    "total_amount": 7000,
    "status": "pending",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

5. 「Save Example」をクリック

#### エラーレスポンス例の追加

同様に、エラーレスポンスの例も追加します。

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_CUSTOMER",
    "message": "指定された顧客IDは存在しません"
  }
}
```

### 5. APIドキュメントの自動生成

Postmanは、コレクションから自動的にAPIドキュメントを生成できます。

1. コレクションを選択
2. 「View Documentation」アイコンをクリック
3. 自動生成されたドキュメントを確認
4. 各リクエストの説明を編集（オプション）
5. 「Publish」ボタンでドキュメントを公開

#### 公開ドキュメントの共有

1. 「Publish」をクリック
2. 公開設定を選択:
   - **Public**: 誰でもアクセス可能
   - **Private**: チームメンバーのみ
3. 「Publish Collection」をクリック
4. 生成されたURLを共有

### 6. 外部システムIF一覧の作成

外部システム連携要件定義では、インターフェース一覧が必要です。Postmanのコレクション構造を活用して整理します。

#### コレクション構造の例

```
ECサイトAPI
├── 認証
│   ├── ログイン (POST /v1/auth/login)
│   └── ログアウト (POST /v1/auth/logout)
├── 商品管理
│   ├── 商品一覧取得 (GET /v1/products)
│   ├── 商品詳細取得 (GET /v1/products/{id})
│   └── 商品登録 (POST /v1/products)
├── 注文管理
│   ├── 注文作成 (POST /v1/orders)
│   ├── 注文一覧取得 (GET /v1/orders)
│   └── 注文詳細取得 (GET /v1/orders/{id})
└── 顧客管理
    ├── 顧客情報取得 (GET /v1/customers/{id})
    └── 顧客情報更新 (PUT /v1/customers/{id})
```

### 7. OpenAPI仕様のエクスポート

Postmanは、OpenAPI 3.0形式でAPI仕様をエクスポートできます。

1. コレクションを選択
2. 「...」メニュー→「Export」をクリック
3. フォーマットを選択: **OpenAPI 3.0 with Postman extensions**
4. 「Export」ボタンをクリック
5. ファイルを保存（例: "ec-site-api-v1.0.json"）

### 8. 環境変数の設定

APIのベースURLやトークンを環境変数として管理できます。

1. 左上の「Environments」を選択
2. 「+ Create Environment」をクリック
3. 環境名を入力（例: "本番環境"、"開発環境"）
4. 変数を追加:
   - `base_url`: https://api.example.com
   - `api_key`: your_api_key_here
5. 「Save」をクリック

#### 環境変数の利用

リクエストURL: `{{base_url}}/v1/products`
ヘッダー: `Authorization: Bearer {{api_key}}`

### 9. モックサーバー

実際のAPIが実装される前に、モックサーバーでテストできます。

1. コレクションを選択
2. 「...」メニュー→「Mock Collection」をクリック
3. モックサーバー名を入力
4. 「Create Mock Server」をクリック
5. モックURLが生成される（例: https://xxxxxxxx.mock.pstmn.io）

モックサーバーは、保存されたレスポンス例を返します。

### 10. API仕様書テンプレート

#### リクエスト仕様の記載項目

各APIリクエストに以下の情報を記載します：

- **エンドポイント**: `/v1/orders`
- **HTTPメソッド**: POST
- **概要**: 新規注文を作成する
- **認証**: Bearer Token必須
- **リクエストヘッダー**:
  - `Authorization`: Bearer {token}
  - `Content-Type`: application/json
- **リクエストボディ**: JSON（例あり）
- **レスポンス**:
  - **200 OK**: 成功時のレスポンス例
  - **400 Bad Request**: バリデーションエラー
  - **401 Unauthorized**: 認証エラー
  - **500 Internal Server Error**: サーバーエラー
- **備考**: その他の注意事項

## 公式ドキュメント

- **公式サイト**: [Postman](https://www.postman.com/)
- **Postman Learning Center**: [Learning Resources](https://learning.postman.com/)
- **APIドキュメント作成**: [Documenting your API](https://learning.postman.com/docs/publishing-your-api/documenting-your-api/)
- **コレクション管理**: [Grouping requests in collections](https://learning.postman.com/docs/sending-requests/intro-to-collections/)
- **モックサーバー**: [Setting up mock servers](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)

## 学習リソース

- **Postman YouTube チャンネル**: [Postman Videos](https://www.youtube.com/c/Postman)
- **Postman Academy**: [Free Courses](https://academy.postman.com/)

## 関連リンク

- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API設計ベストプラクティス](https://restfulapi.net/)
- [HTTP ステータスコード](https://developer.mozilla.org/ja/docs/Web/HTTP/Status)
