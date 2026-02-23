# Newman

## 概要

Newmanは、PostmanコレクションをコマンドラインからCI/CDパイプラインで自動実行するためのCLIツールです。Postmanで作成したAPIテスト（リクエスト、テストスクリプト、環境変数）をそのまま`newman run`コマンドで実行し、HTML/JUnit/JSON形式のレポートを生成します。Node.jsベースで動作し、npm経由でインストールでき、GitHub Actions、Jenkins、GitLab CI等のCI/CDツールとシームレスに統合できます。

## 主な機能

### 1. コレクション実行

- **コレクション実行**: Postman Collection v2.1形式のJSON実行
- **環境変数**: 環境ファイル（`-e`）、グローバル変数（`-g`）の適用
- **データ駆動テスト**: CSVやJSONファイルによる反復実行（`-d`）
- **フォルダ指定**: コレクション内の特定フォルダのみ実行（`--folder`）
- **反復実行**: 同一コレクションの複数回実行（`-n`）

### 2. レポート

- **CLI出力**: ターミナル上のテスト結果サマリ
- **HTML**: `newman-reporter-htmlextra`によるリッチなHTMLレポート
- **JUnit XML**: CI/CDツールのテスト結果連携用
- **JSON**: 機械処理用の詳細結果

### 3. テストスクリプト

- **Pre-request Script**: リクエスト送信前の前処理
- **Test Script**: レスポンス検証（ステータスコード、JSON Schema、値チェック）
- **変数設定**: テスト間での変数受け渡し
- **Chai.js**: アサーションライブラリによる柔軟な検証

### 4. 認証・セキュリティ

- **Bearer Token**: OAuth2トークン認証
- **Basic Auth**: 基本認証
- **API Key**: ヘッダー/クエリパラメータによるAPIキー
- **SSL証明書**: クライアント証明書の指定

## 利用方法

### インストール

```bash
# npm でグローバルインストール
npm install -g newman

# HTMLレポーター追加
npm install -g newman-reporter-htmlextra

# バージョン確認
newman --version
```

### 基本実行

```bash
# ローカルコレクションファイルの実行
newman run collection.json

# 環境変数ファイル指定
newman run collection.json -e environment.json

# グローバル変数指定
newman run collection.json -e env.json -g globals.json

# データファイルによる反復実行
newman run collection.json -d testdata.csv -n 5

# 特定フォルダのみ実行
newman run collection.json --folder "User API"

# タイムアウト設定
newman run collection.json --timeout-request 10000
```

### レポート生成

```bash
# HTMLレポート生成
newman run collection.json \
  -r htmlextra \
  --reporter-htmlextra-export ./reports/report.html

# 複数レポーター同時出力
newman run collection.json \
  -r cli,htmlextra,junit \
  --reporter-htmlextra-export ./reports/report.html \
  --reporter-junit-export ./reports/junit.xml

# JSON結果出力
newman run collection.json \
  -r json \
  --reporter-json-export ./reports/results.json
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/api-test.yml
name: API Tests

on: [push, pull_request]

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install Newman
        run: npm install -g newman newman-reporter-htmlextra
      - name: Run API Tests
        run: |
          newman run postman/collection.json \
            -e postman/environment.json \
            -r cli,htmlextra,junit \
            --reporter-htmlextra-export reports/report.html \
            --reporter-junit-export reports/junit.xml
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-test-report
          path: reports/
```

### Node.js APIとしての利用

```javascript
const newman = require('newman');

newman.run({
    collection: require('./collection.json'),
    environment: require('./environment.json'),
    reporters: ['cli', 'htmlextra'],
    reporter: {
        htmlextra: {
            export: './reports/report.html'
        }
    }
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Total requests:', summary.run.stats.requests.total);
    console.log('Failed:', summary.run.stats.assertions.failed);
});
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Newman** | 無料 | オープンソース、Apache License 2.0 |
| **Postman（Free）** | 無料 | コレクション作成、基本的なコラボレーション |
| **Postman（Pro/Enterprise）** | 有料 | 高度なモニタリング、チーム管理、Postman Cloud |

## メリット

1. **Postman互換**: Postmanで作成したコレクションをそのまま実行可能
2. **CI/CD統合**: コマンドラインベースで各CIツールと容易に統合
3. **データ駆動**: CSV/JSONによるパラメータ化テストで網羅性向上
4. **豊富なレポーター**: HTML、JUnit、JSON等の出力形式に対応
5. **環境分離**: 環境変数ファイルで開発/ステージング/本番を切り替え
6. **Node.js API**: プログラマティックな実行でカスタムワークフロー構築可能

## デメリット

1. **Postman依存**: テストコレクションの作成にPostmanが必要
2. **GUIなし**: テスト結果の確認はレポートファイルまたはターミナル出力
3. **パフォーマンステスト不可**: 負荷テストには対応していない（k6やJMeterが代替）
4. **認証フロー**: OAuth2のインタラクティブ認証フローは手動トークン取得が必要
5. **デバッグ**: テスト失敗時のデバッグはPostman GUIの方が効率的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Postman CLI** | Postman公式CLI（新版） | Newmanの後継、Postman Cloud連携が充実 |
| **REST Assured** | Java APIテスト | Java/Groovyで記述、Newmanよりプログラマブル |
| **Karate** | APIテスト/BDD | Gherkin風記法、Newmanより機能豊富 |
| **Hurl** | CLI APIテスト | シンプルなテキスト形式、軽量 |

## 公式リンク

- **GitHub**: [https://github.com/postmanlabs/newman](https://github.com/postmanlabs/newman)
- **npm**: [https://www.npmjs.com/package/newman](https://www.npmjs.com/package/newman)
- **Postman Docs**: [https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/](https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/)
- **htmlextra Reporter**: [https://github.com/DannyDainton/newman-reporter-htmlextra](https://github.com/DannyDainton/newman-reporter-htmlextra)

## 関連ドキュメント

- [Allure Report](./Allure_Report.md)

---

**カテゴリ**: テスト
**対象工程**: テスト・CI/CD
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
