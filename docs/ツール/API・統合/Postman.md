# Postman

## 概要

Postmanは、API開発・テストのための包括的プラットフォームです。REST API、GraphQL、SOAP、WebSocketなどのAPIリクエストを簡単に作成・送信し、レスポンスを検証できます。開発者がAPIを設計、テスト、ドキュメント化、モニタリングするための統合環境を提供し、世界中で2,500万人以上の開発者に利用されています。

## 主な機能

### 1. APIリクエスト作成・送信
- **HTTPメソッド対応**: GET、POST、PUT、DELETE、PATCH等
- **リクエストビルダー**: ヘッダー、パラメータ、ボディを簡単設定
- **認証**: Basic、Bearer Token、OAuth 2.0、API Key等
- **環境変数**: 開発/ステージング/本番環境の切り替え

### 2. API自動テスト
- **テストスクリプト**: JavaScriptでアサーション記述
- **チェーン実行**: 複数リクエストの連続実行
- **データ駆動テスト**: CSVからテストデータ読み込み
- **CI/CD統合**: Newman (CLI) でパイプライン統合

### 3. APIドキュメント自動生成
- **自動ドキュメント**: コレクションから自動生成
- **公開API**: 外部公開用ドキュメント作成
- **サンプルコード**: 各言語のサンプルコード自動生成

### 4. モックサーバー
- 実装前にモックAPIサーバーを起動
- フロントエンド開発を並行実施可能

### 5. APIモニタリング
- 定期的なAPIヘルスチェック
- アラート通知
- パフォーマンス計測

### 6. チームコラボレーション
- コレクション共有
- チームワークスペース
- コメント・レビュー機能

## 利用方法

### 基本的な使い方

1. **新規リクエスト作成**
   ```
   New → HTTP Request
   → メソッド選択（GET/POST等）
   → URLを入力
   → Send
   ```

2. **リクエストヘッダー設定**
   ```
   Headersタブ
   → Key: Content-Type, Value: application/json
   → Key: Authorization, Value: Bearer <token>
   ```

3. **リクエストボディ設定（POST/PUT）**
   ```
   Bodyタブ → raw → JSON選択
   {
     "name": "テストユーザー",
     "email": "test@example.com"
   }
   ```

4. **環境変数設定**
   ```
   Environments → New Environment
   → 変数定義: base_url = https://api.example.com
   → リクエストで使用: {{base_url}}/users
   ```

5. **テストスクリプト作成**
   ```javascript
   pm.test("ステータスコードは200", function () {
       pm.response.to.have.status(200);
   });
   
   pm.test("レスポンスにnameフィールドが存在", function () {
       var jsonData = pm.response.json();
       pm.expect(jsonData).to.have.property('name');
   });
   ```

### コレクション作成例

```
1. New Collection → 名前入力（例: "User API Tests"）
2. コレクションにリクエスト追加
   - GET /users （ユーザー一覧取得）
   - POST /users （ユーザー作成）
   - GET /users/{id} （ユーザー詳細取得）
   - PUT /users/{id} （ユーザー更新）
   - DELETE /users/{id} （ユーザー削除）
3. 各リクエストにテストスクリプト追加
4. Collection Runner で一括実行
```

### CI/CD統合（Newman使用）

```bash
# Newmanインストール
npm install -g newman

# コレクション実行
newman run collection.json -e environment.json

# レポート出力
newman run collection.json --reporters cli,json,html
```

## 料金プラン

| プラン | 価格 | 主な機能 |
|--------|------|----------|
| **Free** | 無料 | 個人利用、基本機能 |
| **Basic** | $12/月/ユーザー | チーム協業、25,000リクエスト/月 |
| **Professional** | $29/月/ユーザー | 高度な協業、100,000リクエスト/月 |
| **Enterprise** | 要問い合わせ | SSO、監査ログ、専用サポート |

※価格は2025年時点、年間契約の場合の月額換算

## メリット

### ✅ 主な利点

1. **使いやすいUI**: 直感的なインターフェース
2. **無料プラン充実**: 個人開発に十分な機能
3. **環境変数**: 開発/本番環境の簡単切り替え
4. **テスト自動化**: JavaScriptでアサーション記述
5. **CI/CD統合**: Newman CLIでパイプライン統合
6. **ドキュメント自動生成**: APIドキュメントを自動作成
7. **モックサーバー**: フロントエンド開発を並行可能
8. **チーム協業**: コレクション共有・レビュー機能
9. **多様な認証**: OAuth、JWT、Basic等に対応
10. **クロスプラットフォーム**: Windows/Mac/Linux/Web対応

## デメリット

### ❌ 制約・課題

1. **無料版リクエスト制限**: 月1,000リクエストまで（モニタリング）
2. **オフライン機能限定**: Web版はオフライン不可
3. **大規模チーム高額**: Enterpriseプランは高価
4. **パフォーマンステスト弱い**: JMeterやGatlingに劣る
5. **複雑なシナリオ困難**: 高度なテストケースは記述が煩雑
6. **バージョン管理弱い**: Gitとの統合はやや手間
7. **セキュリティ懸念**: クラウド版は機密情報の管理に注意

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Insomnia** | シンプルUI、無料、GraphQL対応 | Postmanよりシンプル |
| **cURL** | コマンドライン、軽量 | GUI不要、スクリプト化容易 |
| **HTTPie** | コマンドライン、使いやすい | cURLより見やすい出力 |
| **SoapUI** | SOAP API特化 | RESTよりSOAPに強い |
| **Paw** | Mac専用、美しいUI | Postmanより軽量 |
| **REST Client (VS Code)** | VS Code拡張、無料 | エディタ内で完結 |

## 公式リンク

- **公式サイト**: [https://www.postman.com/](https://www.postman.com/)
- **ドキュメント**: [https://learning.postman.com/docs/](https://learning.postman.com/docs/)
- **Learning Center**: [https://learning.postman.com/](https://learning.postman.com/)
- **Newman CLI**: [https://www.npmjs.com/package/newman](https://www.npmjs.com/package/newman)
- **Public API Network**: [https://www.postman.com/explore](https://www.postman.com/explore)

## 関連ドキュメント

- [APIツール一覧](../APIツール/)
- [Insomnia](./Insomnia.md)
- [Swagger/OpenAPI](./Swagger_OpenAPI.md)
- [API設計ベストプラクティス](../../best-practices/api-design.md)
- [REST APIテスト手法](../../best-practices/rest-api-testing.md)

---

**カテゴリ**: APIツール  
**対象工程**: 基本設計、詳細設計、実装、テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
