# Postman

## 概要

Postmanは、API開発・テストプラットフォームです。HTTPリクエスト送信、レスポンス検証、環境変数、コレクション、自動テスト（Newman）、モック、ドキュメント生成により、REST/GraphQL API開発を効率化します。GUI、チームコラボレーション、CI/CD統合で、API開発のデファクトスタンダードです。

## 主な機能

### 1. API リクエスト
- **HTTP メソッド**: GET、POST、PUT、DELETE等
- **認証**: Bearer、OAuth、API Key
- **ヘッダー**: カスタムヘッダー
- **ボディ**: JSON、FormData、XML

### 2. テスト
- **アサーション**: レスポンス検証
- **スクリプト**: Pre-request、Test scripts
- **環境変数**: 環境切り替え
- **コレクション**: リクエストグループ

### 3. 自動化
- **Newman**: CLI実行
- **CI/CD**: Jenkins、GitLab CI統合
- **スケジュール**: 定期実行

### 4. コラボレーション
- **ワークスペース**: チーム共有
- **バージョン管理**: コレクション履歴
- **コメント**: レビュー

## 利用方法

### インストール

```bash
# Postman Desktop
# https://www.postman.com/downloads/

# Newman（CLI）
npm install -g newman
```

### 基本リクエスト

```
1. 新規リクエスト作成
2. メソッド選択（GET、POST等）
3. URL入力: https://api.example.com/users
4. Headers設定:
   Content-Type: application/json
   Authorization: Bearer <token>
5. Body設定（POST）:
   {
     "name": "Alice",
     "email": "alice@example.com"
   }
6. Send
```

### テストスクリプト

```javascript
// Tests タブ
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

pm.test("Response has user data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property("name");
    pm.expect(jsonData.name).to.eql("Alice");
});

// 環境変数設定
pm.environment.set("userId", pm.response.json().id);
```

### Pre-request スクリプト

```javascript
// Pre-request Script タブ
// タイムスタンプ生成
pm.environment.set("timestamp", new Date().toISOString());

// ランダムID生成
pm.environment.set("randomId", Math.floor(Math.random() * 10000));

// 認証トークン取得
pm.sendRequest({
    url: 'https://api.example.com/auth/token',
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            username: 'admin',
            password: 'secret'
        })
    }
}, function (err, res) {
    pm.environment.set("token", res.json().token);
});
```

### 環境変数

```json
// Environment
{
  "name": "Production",
  "values": [
    {
      "key": "baseUrl",
      "value": "https://api.example.com",
      "enabled": true
    },
    {
      "key": "apiKey",
      "value": "secret-key",
      "enabled": true
    }
  ]
}
```

```
# リクエストで使用
GET {{baseUrl}}/users
Headers:
  X-API-Key: {{apiKey}}
```

### Newman（CLI実行）

```bash
# コレクションエクスポート（Postmanから）
# Export Collection as JSON

# Newman実行
newman run my-collection.json \
  --environment production.json \
  --reporters cli,json \
  --reporter-json-export results.json

# 特定フォルダー実行
newman run my-collection.json --folder "User Tests"

# CI/CD統合
newman run my-collection.json --bail
```

### CI/CD統合（GitHub Actions）

```yaml
name: API Tests

on: [push]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Newman
        run: npm install -g newman

      - name: Run API Tests
        run: newman run postman-collection.json \
          --environment production.json \
          --reporters cli,junit \
          --reporter-junit-export results.xml
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Postman Free** | 🟢 無料 | 個人利用、3人チーム |
| **Postman Basic** | 💰 $12/月 | チームコラボ、無制限API |
| **Postman Professional** | 💰 $29/月 | モック、モニタリング |
| **Postman Enterprise** | 💰 要問い合わせ | SSO、専用サポート |

## メリット

1. **無料枠**: 個人利用無料
2. **GUI**: 使いやすいUI
3. **Newman**: CLI自動化
4. **コラボレーション**: チーム共有
5. **ドキュメント**: 自動生成

## デメリット

1. **オフライン**: ネット接続必要（一部機能）
2. **有料機能**: モック、モニタ有料
3. **学習曲線**: 高度機能複雑
4. **パフォーマンス**: 大量リクエストで遅延

## 公式リンク

- **公式サイト**: [https://www.postman.com/](https://www.postman.com/)
- **ドキュメント**: [https://learning.postman.com/docs/](https://learning.postman.com/docs/)

## 関連ドキュメント

- [APIテストツール一覧](../APIテストツール/)
- [Insomnia](./Insomnia.md)
- [Newman](./Newman.md)

---

**カテゴリ**: APIテストツール
**対象工程**: API開発・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
