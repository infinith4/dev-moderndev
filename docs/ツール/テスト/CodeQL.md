# CodeQL

## 概要

**CodeQL**は、GitHubが開発したコード解析エンジンです。セマンティック解析により、セキュリティ脆弱性・バグをコードから検出し、GitHub Advanced Securityの一部として、プルリクエスト段階での自動セキュリティチェックを実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | GitHub（Semmle買収） |
| **種別** | セマンティックコード解析エンジン |
| **ライセンス** | プロプライエタリ（オープンソースは無料） |
| **料金** | 🟡 Free（パブリックリポジトリ）/ 有料（GitHub Advanced Security） |
| **公式サイト** | https://codeql.github.com/ |
| **ドキュメント** | https://codeql.github.com/docs/ |

## 主な特徴

### 1. セマンティック解析
- **データフロー分析**: 変数の追跡
- **制御フロー分析**: プログラムの実行パス
- **コールグラフ**: 関数呼び出し関係
- **クエリ言語**: SQLライクなクエリでコード検索

### 2. 脆弱性検出
- **OWASP Top 10**: SQLインジェクション、XSS等
- **CWE**: Common Weakness Enumeration
- **カスタムクエリ**: 独自ルール定義
- **誤検知低減**: セマンティック解析による精度向上

### 3. GitHub統合
- **GitHub Actions**: 自動スキャン
- **Code Scanning**: PR画面にアラート表示
- **Security Advisory**: 脆弱性データベース
- **Dependabot連携**: 依存関係脆弱性

### 4. 多言語対応
- **Java**: Spring、Struts等フレームワーク
- **JavaScript/TypeScript**: Node.js、React等
- **Python**: Django、Flask等
- **C/C++、C#、Go、Ruby**: 幅広い対応

## 使い方

### GitHub Actions セットアップ

```yaml
# .github/workflows/codeql-analysis.yml
name: "CodeQL"

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # 毎週月曜日0時

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript', 'python' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: ${{ matrix.language }}
        queries: security-and-quality

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        category: "/language:${{matrix.language}}"
```

### Java プロジェクト

```yaml
# .github/workflows/codeql-analysis.yml
jobs:
  analyze:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: java

    - name: Build with Maven
      run: mvn clean install -DskipTests

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
```

### C/C++ プロジェクト

```yaml
# .github/workflows/codeql-analysis.yml
jobs:
  analyze:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: cpp

    - name: Build
      run: |
        mkdir build
        cd build
        cmake ..
        make

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
```

### カスタムクエリ

```yaml
# .github/workflows/codeql-analysis.yml
steps:
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: javascript
    queries: security-and-quality, ./.github/codeql/custom-queries.qls
```

```yaml
# .github/codeql/custom-queries.qls
- queries: .
  from: codeql/javascript-queries
- queries: .
  from: ./.github/codeql/custom
```

```ql
# .github/codeql/custom/sql-injection.ql
/**
 * @name SQL injection
 * @description User input flows to SQL query without sanitization
 * @kind path-problem
 * @problem.severity error
 * @id js/sql-injection-custom
 */

import javascript
import DataFlow::PathGraph

class SqlInjectionConfig extends TaintTracking::Configuration {
  SqlInjectionConfig() { this = "SqlInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source instanceof RemoteFlowSource
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(SQL::SqlString s |
      s.getAnArgument() = sink.asExpr()
    )
  }
}

from SqlInjectionConfig cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink, "SQL injection from $@.", source.getNode(), "user input"
```

### CLI使用（ローカル解析）

```bash
# CodeQL CLI ダウンロード
wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip
unzip codeql-linux64.zip
export PATH=$PATH:$(pwd)/codeql

# CodeQLクエリライブラリクローン
git clone https://github.com/github/codeql.git codeql-repo

# データベース作成（JavaScript）
codeql database create myapp-db --language=javascript --source-root=./myapp

# データベース作成（Java - Maven）
codeql database create myapp-db --language=java --command="mvn clean install -DskipTests"

# クエリ実行
codeql query run codeql-repo/javascript/ql/src/Security/CWE-079/XSS.ql --database=myapp-db

# 解析実行
codeql database analyze myapp-db \
  codeql-repo/javascript/ql/src/codeql-suites/javascript-security-and-quality.qls \
  --format=sarif-latest \
  --output=results.sarif

# SARIF結果表示
codeql github upload-results \
  --repository=owner/repo \
  --ref=refs/heads/main \
  --commit=$(git rev-parse HEAD) \
  --sarif=results.sarif
```

### VS Code統合

```bash
# VS Code拡張機能インストール
code --install-extension GitHub.vscode-codeql

# ワークスペース設定
# .vscode/settings.json
{
  "codeQL.cli.executablePath": "/path/to/codeql/codeql",
  "codeQL.runningQueries.numberOfThreads": 4
}
```

### SARIF レポート

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "CodeQL",
          "version": "2.10.0",
          "rules": [
            {
              "id": "js/sql-injection",
              "name": "SQL injection",
              "shortDescription": {
                "text": "SQL injection vulnerability"
              }
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "js/sql-injection",
          "level": "error",
          "message": {
            "text": "User input flows to SQL query"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "src/controllers/user.js"
                },
                "region": {
                  "startLine": 42,
                  "startColumn": 10
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### カスタムクエリ例（XSS検出）

```ql
/**
 * @name Cross-site scripting
 * @description User input rendered without escaping
 * @kind path-problem
 * @problem.severity error
 * @id js/xss-custom
 */

import javascript
import semmle.javascript.security.dataflow.DomBasedXssQuery
import DataFlow::PathGraph

from Configuration cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink,
  "Cross-site scripting vulnerability from $@.", source.getNode(), "user input"
```

### GitLab統合

```yaml
# .gitlab-ci.yml
codeql:
  image: ghcr.io/github/codeql-action/codeql-runner:latest
  script:
    - codeql database create codeql-db --language=javascript
    - codeql database analyze codeql-db \
        --format=sarif-latest \
        --output=results.sarif \
        javascript-security-and-quality.qls
  artifacts:
    reports:
      sast: results.sarif
```

### Jenkins統合

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('CodeQL Analysis') {
            steps {
                sh '''
                    codeql database create codeql-db --language=java --command="mvn clean install -DskipTests"
                    codeql database analyze codeql-db \
                        --format=sarif-latest \
                        --output=results.sarif \
                        java-security-and-quality.qls
                '''

                recordIssues(
                    enabledForFailure: true,
                    tool: sarif(pattern: 'results.sarif')
                )
            }
        }
    }
}
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | PR レビュー | コミット時の自動セキュリティチェック |
| **テスト** | 静的解析 | 脆弱性検出 |
| **テスト** | コード品質 | バグ・アンチパターン検出 |
| **CI/CD** | セキュリティゲート | ビルドパイプラインでの自動スキャン |

## メリット

- **セマンティック解析**: 誤検知低減、高精度
- **多言語対応**: 主要言語サポート
- **GitHub統合**: PR画面にアラート表示
- **カスタムクエリ**: 独自ルール定義可能
- **OWASP/CWE対応**: セキュリティ標準準拠
- **無料**: パブリックリポジトリ無料
- **データフロー追跡**: 複雑な脆弱性検出

## デメリット

- **料金**: プライベートリポジトリはGitHub Advanced Security必要（有料）
- **学習曲線**: クエリ言語の習得
- **実行時間**: 大規模プロジェクトで時間がかかる
- **GitHub依存**: GitHub Actions推奨
- **セットアップ**: 初期設定が複雑
- **ビルド必要**: コンパイル言語はビルドステップ必須

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **CodeQL** | セマンティック解析、GitHub統合 | 無料/有料 | GitHub中心開発 |
| **SonarQube** | 品質・セキュリティ総合 | 無料/有料 | 総合品質管理 |
| **Snyk Code** | リアルタイム、IDE統合 | 無料/有料 | 開発中の脆弱性検出 |
| **Checkmarx** | エンタープライズSAST | 有料 | 大規模組織 |

## ベストプラクティス

### 1. PRでの自動スキャン

```yaml
on:
  pull_request:
    branches: [ main ]
```

### 2. カスタムクエリで組織固有ルール

```yaml
queries: security-and-quality, ./.github/codeql/custom-queries.qls
```

### 3. スケジュール実行で定期スキャン

```yaml
on:
  schedule:
    - cron: '0 0 * * 1'  # 毎週月曜日
```

### 4. マトリックスビルドで複数言語

```yaml
strategy:
  matrix:
    language: [ 'javascript', 'python', 'java' ]
```

## 公式リソース

- **公式サイト**: https://codeql.github.com/
- **ドキュメント**: https://codeql.github.com/docs/
- **クエリリポジトリ**: https://github.com/github/codeql
- **CLI**: https://github.com/github/codeql-cli-binaries
- **VS Code拡張**: https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-codeql

## まとめ

CodeQLは、GitHubが開発したセマンティックコード解析エンジンです。データフロー・制御フロー分析により、SQLインジェクション・XSS等のセキュリティ脆弱性を高精度で検出します。GitHub Advanced Securityの一部として、プルリクエスト段階での自動セキュリティチェックを実現し、シフトレフトなセキュリティ対策を支援します。

---

**最終更新**: 2025-12-10
**対象バージョン**: CodeQL CLI 2.15+
