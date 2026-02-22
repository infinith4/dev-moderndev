# Mockoon

## 概要

Mockoonは、デスクトップGUIを備えたモックAPIサーバツールです。ノーコードで直感的にREST APIやGraphQLのモックを作成でき、テンプレート機能、CLI対応、クロスプラットフォーム対応により、開発・テスト環境で簡単にモックサーバを構築できます。無料版でもフル機能が利用可能で、Cloud版でチーム共有も可能です。

## 主な機能

### 1. ノーコードGUI
- **ビジュアルエディタ**: ドラッグ&ドロップ操作
- **リアルタイムプレビュー**: 即座に確認
- **環境管理**: 複数環境切り替え
- **エクスポート/インポート**: JSON形式

### 2. モックAPI作成
- **REST API**: HTTPメソッド全対応
- **GraphQL**: GraphQLスキーマ対応
- **レスポンステンプレート**: Handlebars
- **動的レスポンス**: ヘルパー関数

### 3. 高度な機能
- **ルーティング**: パスパラメータ、クエリ
- **遅延シミュレーション**: レスポンス遅延
- **プロキシモード**: 実サーバへの転送
- **CORS設定**: カスタマイズ可能

### 4. CLI対応
- **mockoon-cli**: CI/CD統合
- **Docker対応**: コンテナ実行
- **自動起動**: スクリプト統合
- **ログ出力**: 詳細ログ

## 利用方法

### デスクトップアプリインストール

```bash
# macOS (Homebrew)
brew install --cask mockoon

# Windows (Chocolatey)
choco install mockoon

# Linux (Snap)
snap install mockoon

# または公式サイトからダウンロード
# https://mockoon.com/download/
```

### GUIでモック作成

```
1. Mockoon起動
2. "New environment" クリック
3. Environment名入力（例: "User API"）
4. "Add route" クリック
5. Route設定:
   - Method: GET
   - Path: /api/users
   - Status: 200
   - Body:
     [
       {"id": 1, "name": "John Doe"},
       {"id": 2, "name": "Jane Smith"}
     ]
6. "Start server" クリック
7. http://localhost:3000/api/users にアクセス
```

### レスポンステンプレート（Handlebars）

```json
{
  "id": "{{faker 'datatype.uuid'}}",
  "name": "{{faker 'name.findName'}}",
  "email": "{{faker 'internet.email'}}",
  "timestamp": "{{now 'yyyy-MM-dd HH:mm:ss'}}",
  "requestId": "{{queryParam 'requestId'}}"
}
```

### パスパラメータ

```
# Route: /api/users/:id
# URL: /api/users/123

# Response template:
{
  "id": "{{urlParam 'id'}}",
  "name": "User {{urlParam 'id'}}"
}
```

### CLI使用

```bash
# CLI インストール
npm install -g @mockoon/cli

# Mockoon環境ファイルエクスポート（GUI から）
# File > Export environment > user-api.json

# CLI でモックサーバ起動
mockoon-cli start --data user-api.json --port 3000

# 複数環境起動
mockoon-cli start --data env1.json --data env2.json

# ログレベル指定
mockoon-cli start --data user-api.json --log-level info
```

### Docker使用

```bash
# Mockoon環境ファイル準備
# user-api.json

# Docker起動
docker run -d \
  -p 3000:3000 \
  -v $(pwd)/user-api.json:/data/user-api.json \
  mockoon/cli:latest \
  --data /data/user-api.json \
  --port 3000
```

### package.json統合

```json
{
  "scripts": {
    "mock-api": "mockoon-cli start --data ./mocks/user-api.json --port 3000",
    "mock-api:all": "mockoon-cli start --data ./mocks/*.json"
  },
  "devDependencies": {
    "@mockoon/cli": "^7.0.0"
  }
}
```

```bash
npm run mock-api
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

      - name: Install Mockoon CLI
        run: npm install -g @mockoon/cli

      - name: Start Mock Server
        run: |
          mockoon-cli start --data ./mocks/user-api.json --port 3000 &
          sleep 5

      - name: Run API Tests
        run: npm test

      - name: Stop Mock Server
        run: killall mockoon-cli
```

### プロキシモード

```
# GUI設定:
1. Route設定画面
2. "Proxy" タブ選択
3. "Enable proxy mode" チェック
4. Proxy host: https://api.example.com
5. Proxy headers: 追加ヘッダー設定
```

### GraphQL対応

```graphql
# GraphQL エンドポイント: /graphql
# Body (GraphQL):

query {
  user(id: 1) {
    id
    name
    email
  }
}

# Response template:
{
  "data": {
    "user": {
      "id": "{{queryParam 'id'}}",
      "name": "{{faker 'name.findName'}}",
      "email": "{{faker 'internet.email'}}"
    }
  }
}
```

### 環境変数

```json
// Environment variables (GUI設定)
{
  "API_KEY": "secret-key-123",
  "BASE_URL": "https://api.example.com"
}

// Response template:
{
  "apiKey": "{{getEnvVar 'API_KEY'}}",
  "baseUrl": "{{getEnvVar 'BASE_URL'}}"
}
```

### 条件分岐レスポンス

```
# GUI設定:
1. Route に複数の Response 追加
2. Response 1: Status 200（デフォルト）
3. Response 2: Status 404
   - Rules > Add rule
   - Query param: id
   - Operator: equals
   - Value: 999
   - Response body: {"error": "User not found"}
```

### 遅延シミュレーション

```
# GUI設定（Route settings）:
1. "Response" タブ
2. "Latency" フィールド: 2000 (ms)
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Mockoon Desktop** | 🟢 無料 | オープンソース、フル機能 |
| **Mockoon Cloud** | 💰 $8/月〜 | チーム共有、クラウド同期 |
| **Mockoon Pro** | 💰 $15/月 | 優先サポート、高度機能 |

## メリット

1. **美しいGUI**: 直感的なビジュアルエディタ
2. **ノーコード**: コード不要で即作成
3. **テンプレート機能**: 動的レスポンス簡単
4. **CLI対応**: CI/CD統合可能
5. **クロスプラットフォーム**: Windows/Mac/Linux

## デメリット

1. **GUI必要**: 自動化にやや手間（CLI あるが）
2. **大規模データには不向き**: パフォーマンス制限
3. **Cloud版は有料**: チーム共有有料
4. **カスタムロジック限定的**: 複雑なビジネスロジック困難

## 公式リンク

- **公式サイト**: [https://mockoon.com/](https://mockoon.com/)
- **ドキュメント**: [https://mockoon.com/docs/latest/about/](https://mockoon.com/docs/latest/about/)
- **GitHub**: [https://github.com/mockoon/mockoon](https://github.com/mockoon/mockoon)
- **CLI**: [https://github.com/mockoon/mockoon/tree/main/packages/cli](https://github.com/mockoon/mockoon/tree/main/packages/cli)

## 関連ドキュメント

- [モックサーバツール一覧](../../dev_process_開発工程_9_テスト_アプリケーション.md#922-apiテスト用モックサーバツールtop-6)
- [json-server](./json-server.md)
- [Prism](./Prism.md)

---

**カテゴリ**: モックサーバ・APIテスト
**対象工程**: API開発・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
