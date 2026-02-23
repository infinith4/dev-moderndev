# Apidog

## 概要

Apidog は、API 設計、ドキュメント生成、テスト、モックを統合したオールインワンの API 開発プラットフォームです。Postman、Swagger、Mock.io の機能を一つのツールに統合し、API ライフサイクル全体をカバーします。

## 主な特徴

### 1. 統合 API 開発環境
- API 設計からテスト、ドキュメント化まで一元管理
- OpenAPI 3.0/3.1 および Swagger 2.0 完全サポート
- ビジュアルエディタとコードエディタの切り替え可能

### 2. API 設計
- 直感的な UI での API 設計
- スキーマファーストアプローチ
- データモデルとエンドポイントの視覚的管理
- リアルタイムバリデーション

### 3. ドキュメント自動生成
- API 設計から自動的に美しいドキュメント生成
- カスタマイズ可能なテーマとレイアウト
- インタラクティブな API リファレンス
- マルチ言語サポート

### 4. モックサーバー
- API 設計に基づいた自動モックサーバー生成
- カスタムモックデータ設定
- レスポンスシナリオの管理
- クラウドまたはローカルモック

### 5. API テスト
- 機能テスト、統合テスト、パフォーマンステスト
- テストケースの自動生成
- テストスクリプト (JavaScript/Python)
- CI/CD パイプライン統合

### 6. コラボレーション
- チームワークスペース
- バージョン管理とブランチ機能
- コメントとレビュー機能
- 役割ベースのアクセス制御

## 主な機能

### API 設計機能

| 機能 | 説明 |
|------|------|
| ビジュアルエディタ | GUI で API 設計が可能 |
| OpenAPI サポート | OpenAPI 仕様の完全サポート |
| データモデル管理 | 再利用可能なスキーマ定義 |
| リクエスト/レスポンス設計 | 詳細なリクエストとレスポンスの定義 |
| バリデーション | リアルタイムでの設計検証 |

### テスト機能

| 機能 | 説明 |
|------|------|
| 手動テスト | インタラクティブな API テスト実行 |
| 自動テスト | テストケースの自動実行 |
| テストスクリプト | Pre-request と Test スクリプト |
| アサーション | 豊富なアサーションライブラリ |
| テストスイート | テストの整理と管理 |
| データ駆動テスト | CSV/JSON データによるテスト |
| 環境変数 | 複数環境の管理 |

### モック機能

| 機能 | 説明 |
|------|------|
| 自動モック生成 | API 設計からの自動生成 |
| カスタムモック | モックデータのカスタマイズ |
| スマートモック | リアルなデータ生成 |
| シナリオ管理 | 複数のレスポンスシナリオ |
| クラウドモック | クラウドホスティング |

## アーキテクチャ

### デスクトップアプリケーション
```
Apidog Desktop
├── API 設計ワークスペース
│   ├── ビジュアルエディタ
│   ├── コードエディタ (OpenAPI)
│   └── データモデル管理
├── テストワークスペース
│   ├── リクエストビルダー
│   ├── テストスクリプト
│   └── テスト結果
├── モックサーバー
│   ├── モック設定
│   └── モックログ
└── ドキュメント
    ├── API リファレンス
    └── カスタマイズ設定
```

### クラウドサービス
- チーム同期
- クラウドモックサーバー
- CI/CD 統合
- API モニタリング

## インストールとセットアップ

### デスクトップアプリケーション

#### Windows
```powershell
# 公式サイトからインストーラーをダウンロード
# https://apidog.com/download/

# または Chocolatey を使用
choco install apidog
```

#### macOS
```bash
# 公式サイトからインストーラーをダウンロード
# https://apidog.com/download/

# または Homebrew を使用
brew install --cask apidog
```

#### Linux
```bash
# Debian/Ubuntu
wget https://assets.apidog.com/download/latest/linux/deb/x64/Apidog-latest.deb
sudo dpkg -i Apidog-latest.deb

# Fedora/RHEL
wget https://assets.apidog.com/download/latest/linux/rpm/x64/Apidog-latest.rpm
sudo rpm -i Apidog-latest.rpm
```

### CLI ツール

```bash
# npm でインストール
npm install -g @apidog/cli

# 使用例
apidog run <project-id> --environment <env-id>
```

## 基本的な使い方

### 1. プロジェクトの作成

```
1. Apidog を起動
2. 「New Project」をクリック
3. プロジェクト名と説明を入力
4. テンプレートを選択 (空白 / OpenAPI インポート / Postman インポート)
5. 「Create」をクリック
```

### 2. API の設計

```
1. 左サイドバーで「APIs」を選択
2. 「+ New API」をクリック
3. メソッドとパスを設定
4. リクエストパラメータを定義
   - Path Parameters
   - Query Parameters
   - Headers
   - Body (JSON Schema)
5. レスポンスを定義
   - ステータスコード
   - Headers
   - Body (JSON Schema)
6. 「Save」をクリック
```

### 3. モックサーバーの起動

```
1. 「Mock」タブを選択
2. 「Start Mock Server」をクリック
3. モック URL が生成される
4. 各 API のモックデータをカスタマイズ (オプション)
5. クライアントからモック URL にリクエスト
```

### 4. API テスト

```
1. 「Test」タブを選択
2. API エンドポイントを選択
3. リクエストパラメータを設定
4. 「Send」をクリック
5. レスポンスを確認
6. テストスクリプトを追加 (オプション)
7. テストケースとして保存
```

### 5. ドキュメント生成

```
1. 「Docs」タブを選択
2. 自動生成されたドキュメントを確認
3. カスタマイズ設定
   - テーマ選択
   - カスタム CSS
   - 追加ページ
4. 公開設定
   - 公開 URL 生成
   - アクセス制御
```

## OpenAPI インポート/エクスポート

### インポート

```
1. 「Import」ボタンをクリック
2. インポート形式を選択
   - OpenAPI 3.0/3.1
   - Swagger 2.0
   - Postman Collection
   - HAR
3. ファイルを選択または URL を入力
4. インポートオプションを設定
5. 「Import」をクリック
```

### エクスポート

```
1. プロジェクト設定を開く
2. 「Export」を選択
3. エクスポート形式を選択
   - OpenAPI 3.0
   - OpenAPI 3.1
   - Swagger 2.0
   - Postman Collection
4. エクスポート範囲を選択
5. 「Export」をクリック
```

## テストスクリプト

### Pre-request Script

```javascript
// 環境変数の設定
pm.environment.set("timestamp", Date.now());

// 動的データ生成
const randomId = Math.floor(Math.random() * 1000);
pm.variables.set("userId", randomId);

// リクエスト前の処理
console.log("Sending request to:", pm.request.url);
```

### Test Script

```javascript
// ステータスコードの検証
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// レスポンスボディの検証
pm.test("Response has user data", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData.name).to.be.a('string');
});

// レスポンス時間の検証
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// 環境変数への保存
const responseData = pm.response.json();
pm.environment.set("authToken", responseData.token);
```

## CI/CD 統合

### GitHub Actions

```yaml
name: API Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  api-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install Apidog CLI
      run: npm install -g @apidog/cli

    - name: Run API Tests
      run: |
        apidog run ${{ secrets.APIDOG_PROJECT_ID }} \
          --environment ${{ secrets.APIDOG_ENV_ID }} \
          --token ${{ secrets.APIDOG_TOKEN }} \
          --reporter cli,json

    - name: Upload Test Results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: apidog-results
        path: apidog-report.json
```

### GitLab CI

```yaml
api_test:
  stage: test
  image: node:18
  before_script:
    - npm install -g @apidog/cli
  script:
    - |
      apidog run $APIDOG_PROJECT_ID \
        --environment $APIDOG_ENV_ID \
        --token $APIDOG_TOKEN \
        --reporter cli,junit
  artifacts:
    reports:
      junit: apidog-report.xml
    when: always
```

## Docker での使用

### Dockerfile 例

```dockerfile
FROM node:18-alpine

# Apidog CLI のインストール
RUN npm install -g @apidog/cli

# プロジェクトファイルのコピー
WORKDIR /app
COPY . .

# テスト実行スクリプト
COPY run-tests.sh /app/
RUN chmod +x /app/run-tests.sh

CMD ["/app/run-tests.sh"]
```

### docker-compose.yml 例

```yaml
version: '3.8'

services:
  api-tests:
    build: .
    environment:
      - APIDOG_PROJECT_ID=${APIDOG_PROJECT_ID}
      - APIDOG_ENV_ID=${APIDOG_ENV_ID}
      - APIDOG_TOKEN=${APIDOG_TOKEN}
      - API_BASE_URL=${API_BASE_URL}
    volumes:
      - ./reports:/app/reports
```

## 他ツールとの比較

### Apidog vs Postman

| 機能 | Apidog | Postman |
|------|--------|---------|
| API 設計 | ビジュアル設計、OpenAPI ネイティブ | 限定的 |
| モックサーバー | 自動生成、高度なカスタマイズ | 基本的なモック |
| ドキュメント | 自動生成、カスタマイズ可能 | 手動作成 |
| 価格 | 無料プランあり、低価格 | 無料プランあり、高価格 |
| チーム機能 | 組み込み | Pro プラン以上 |

### Apidog vs Swagger/OpenAPI

| 機能 | Apidog | Swagger Editor |
|------|--------|----------------|
| エディタ | GUI + コード | コードのみ |
| テスト | 統合テスト機能 | 基本的なテスト |
| モック | 高度なモック | 限定的 |
| コラボレーション | チーム機能あり | なし |

## ユースケース

### 1. API ファースト開発

```
フェーズ1: API 設計
- Apidog で API 仕様を設計
- データモデルとエンドポイントを定義
- チームレビュー

フェーズ2: モックサーバー
- 自動モックサーバー起動
- フロントエンド開発開始

フェーズ3: バックエンド開発
- API 仕様に基づいた実装
- Apidog でテスト

フェーズ4: 統合
- 実 API に切り替え
- 統合テスト実行
```

### 2. マイクロサービステスト

```
- 各サービスの API を Apidog で定義
- サービス間の依存関係をモック
- 統合テストスイートの作成
- CI/CD パイプラインに統合
```

### 3. API ドキュメンテーション

```
- OpenAPI 仕様から自動生成
- カスタムドキュメントページ追加
- 公開 URL で共有
- バージョン管理
```

## ベストプラクティス

### 1. プロジェクト構成

```
my-api-project/
├── common/              # 共通定義
│   ├── schemas/         # データモデル
│   ├── examples/        # サンプルデータ
│   └── responses/       # 共通レスポンス
├── endpoints/           # API エンドポイント
│   ├── users/
│   ├── products/
│   └── orders/
├── tests/               # テストケース
│   ├── integration/
│   └── e2e/
└── environments/        # 環境設定
    ├── dev
    ├── staging
    └── production
```

### 2. データモデル管理

- 再利用可能なスキーマを定義
- 共通モデルは `common/schemas` に配置
- ネーミング規則を統一
- バージョン管理を行う

### 3. テスト戦略

```javascript
// テストの階層化
// 1. 基本的なレスポンス検証
pm.test("Status code is 200", () => {
    pm.response.to.have.status(200);
});

// 2. スキーマバリデーション
pm.test("Response matches schema", () => {
    const schema = pm.variables.get("userSchema");
    pm.response.to.have.jsonSchema(schema);
});

// 3. ビジネスロジック検証
pm.test("User email is valid", () => {
    const user = pm.response.json();
    pm.expect(user.email).to.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
});
```

### 4. 環境管理

- 環境ごとに変数を分離
- 機密情報は環境変数として管理
- ベース URL は環境変数で定義
- 環境固有の設定をドキュメント化

## トラブルシューティング

### よくある問題と解決策

#### 1. モックサーバーが起動しない

```
原因: ポートが既に使用されている
解決策:
- 設定でポート番号を変更
- または既存のプロセスを終了
```

#### 2. OpenAPI インポートエラー

```
原因: 仕様のバージョン不一致
解決策:
- OpenAPI 仕様を最新バージョンに更新
- バリデーションエラーを修正
```

#### 3. テストスクリプトエラー

```
原因: 環境変数が未定義
解決策:
- 環境変数を設定
- Pre-request スクリプトで初期化
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://apidog.com/
- ドキュメント: https://apidog.com/help/
- API リファレンス: https://api.apidog.com/

### コミュニティ
- GitHub: https://github.com/apidog
- Discord: https://discord.gg/apidog
- フォーラム: https://forum.apidog.com/

### チュートリアル
- Getting Started: https://apidog.com/docs/getting-started/
- Best Practices: https://apidog.com/docs/best-practices/
- Video Tutorials: https://www.youtube.com/@apidog

## まとめ

Apidog は、API 開発ライフサイクル全体をカバーする統合プラットフォームとして、以下の場面で特に有用です:

1. **API ファースト開発** - 設計からモック、テスト、ドキュメントまで一貫した環境
2. **チーム開発** - コラボレーション機能とバージョン管理
3. **マイクロサービス** - 複数 API の管理とテスト
4. **CI/CD 統合** - 自動テストとデプロイメントパイプライン

Postman の代替として、より統合的で設計重視のアプローチを提供します。
