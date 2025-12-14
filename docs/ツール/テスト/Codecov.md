# Codecov

## 概要

**Codecov**は、コードカバレッジ可視化・分析プラットフォームです。CI/CD統合、プルリクエストへのカバレッジコメント、トレンド分析により、チーム全体でテストカバレッジを継続的に監視・改善できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Codecov（Sentry社傘下） |
| **種別** | コードカバレッジ可視化プラットフォーム（SaaS） |
| **ライセンス** | プロプライエタリ（一部オープンソース） |
| **料金** | 🟡 Free（オープンソース）/ 有料プラン |
| **公式サイト** | https://about.codecov.io/ |
| **ドキュメント** | https://docs.codecov.com/ |

## 主な特徴

### 1. CI/CD統合
- **GitHub Actions**: 公式アクション
- **GitLab CI/CD**: パイプライン統合
- **CircleCI**: Orbsサポート
- **Jenkins**: プラグイン対応

### 2. プルリクエスト連携
- **カバレッジコメント**: PR画面に自動投稿
- **差分表示**: 変更箇所のカバレッジ
- **ステータスチェック**: マージ判定基準
- **カバレッジバッジ**: README.md表示

### 3. 多言語対応
- **主要言語**: Python、JavaScript、Java、Go、Ruby等
- **フォーマット**: JaCoCo、lcov、Cobertura、gcov等
- **複数レポート**: モノレポ対応
- **マージ機能**: 複数CI結果統合

### 4. 分析・可視化
- **トレンドグラフ**: 時系列カバレッジ推移
- **ファイル単位**: 詳細なカバレッジ表示
- **サンバースト図**: パッケージ階層可視化
- **フラグ機能**: テストタイプ別分析

## 使い方

### アカウント登録

1. **Codecovサインアップ**: https://about.codecov.io/
2. **GitHub連携**: GitHub OAuth認証
3. **リポジトリ追加**: Organization → リポジトリ選択
4. **トークン取得**: Settings → Upload Token

### GitHub Actions統合

```yaml
# .github/workflows/test.yml
name: Test Coverage

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests with coverage
        run: npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: true
```

### Node.js プロジェクト

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "collectCoverage": true,
    "coverageDirectory": "coverage",
    "coverageReporters": ["lcov", "text", "html"]
  }
}
```

```bash
# カバレッジ計測
npm run test:coverage

# Codecovにアップロード（ローカル）
bash <(curl -s https://codecov.io/bash) -t <CODECOV_TOKEN>
```

### Python プロジェクト

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=myproject --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          flags: unittests
```

```bash
# ローカルでカバレッジ計測
pytest --cov=myproject --cov-report=xml

# Codecovにアップロード
codecov -t <CODECOV_TOKEN>
```

### Java プロジェクト（JaCoCo）

```xml
<!-- pom.xml -->
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.10</version>
      <executions>
        <execution>
          <goals>
            <goal>prepare-agent</goal>
          </goals>
        </execution>
        <execution>
          <id>report</id>
          <phase>test</phase>
          <goals>
            <goal>report</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run tests with coverage
        run: mvn clean test

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./target/site/jacoco/jacoco.xml
          flags: unittests
```

### Go プロジェクト

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'

      - name: Run tests with coverage
        run: go test -v -coverprofile=coverage.txt -covermode=atomic ./...

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.txt
          flags: unittests
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
test:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm run test:coverage
    - bash <(curl -s https://codecov.io/bash) -t $CODECOV_TOKEN
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

### CircleCI

```yaml
# .circleci/config.yml
version: 2.1

orbs:
  codecov: codecov/codecov@3.2

jobs:
  test:
    docker:
      - image: cimg/node:18.17
    steps:
      - checkout
      - run: npm ci
      - run: npm run test:coverage
      - codecov/upload:
          file: ./coverage/lcov.info
          flags: unittests

workflows:
  test_and_coverage:
    jobs:
      - test
```

### codecov.yml 設定

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: auto
        threshold: 1%  # 1%以上の低下でNG
        base: auto
    patch:
      default:
        target: 80%  # 新規コード80%以上必須

comment:
  layout: "reach, diff, flags, files"
  behavior: default
  require_changes: false

ignore:
  - "tests/**"
  - "**/__tests__/**"
  - "**/node_modules/**"
  - "**/*.test.js"
  - "**/*.spec.js"
```

### カバレッジバッジ

```markdown
<!-- README.md -->
# My Project

[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)

![Coverage](https://img.shields.io/codecov/c/github/username/repo)
```

### フラグ機能

```yaml
# .github/workflows/test.yml
- name: Upload coverage - Unit Tests
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/unit.lcov
    flags: unittests
    name: unit-tests

- name: Upload coverage - Integration Tests
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/integration.lcov
    flags: integration
    name: integration-tests
```

```yaml
# codecov.yml
flags:
  unittests:
    paths:
      - src/
  integration:
    paths:
      - src/
```

### モノレポ対応

```yaml
# codecov.yml
coverage:
  status:
    project:
      frontend:
        target: 80%
        paths:
          - "packages/frontend/**"
      backend:
        target: 85%
        paths:
          - "packages/backend/**"
```

```yaml
# .github/workflows/test.yml
- name: Upload coverage - Frontend
  uses: codecov/codecov-action@v3
  with:
    files: ./packages/frontend/coverage/lcov.info
    flags: frontend
    name: frontend-coverage

- name: Upload coverage - Backend
  uses: codecov/codecov-action@v3
  with:
    files: ./packages/backend/coverage/lcov.info
    flags: backend
    name: backend-coverage
```

### CLI使用

```bash
# Codecov CLI インストール
pip install codecov

# または npm
npm install -g codecov

# カバレッジアップロード
codecov -t <CODECOV_TOKEN>

# 特定ファイル指定
codecov -t <CODECOV_TOKEN> -f ./coverage/lcov.info

# フラグ付き
codecov -t <CODECOV_TOKEN> -f ./coverage/lcov.info --flags unittests
```

### セルフホスト（Codecov Enterprise）

```yaml
# .github/workflows/test.yml
- name: Upload to Codecov Enterprise
  uses: codecov/codecov-action@v3
  with:
    url: https://codecov.company.com
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage/lcov.info
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | PR レビュー | カバレッジコメント確認 |
| **テスト** | カバレッジ監視 | トレンド分析 |
| **テスト** | 品質ゲート | マージ基準設定 |
| **CI/CD** | 継続的品質監視 | 自動カバレッジ計測 |

## メリット

- **PR統合**: 変更箇所のカバレッジ自動表示
- **多言語対応**: 主要言語・フォーマットサポート
- **CI/CD統合**: 主要CI/CDプラットフォーム対応
- **トレンド分析**: 時系列カバレッジ推移
- **無料プラン**: オープンソースプロジェクト
- **視覚化**: サンバースト図、ファイル単位表示
- **フラグ機能**: テストタイプ別分析

## デメリット

- **料金**: プライベートリポジトリは有料
- **外部依存**: SaaS依存、ダウン時影響
- **セットアップ**: トークン管理必要
- **レポート形式**: 各言語でカバレッジツール必須
- **プライバシー**: ソースコード一部アップロード
- **制限**: 無料プランは5ユーザーまで

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Codecov** | PR統合、多言語、トレンド | 無料/有料 | CI/CD統合 |
| **Coveralls** | GitHub統合、シンプル | 無料/有料 | オープンソース |
| **SonarCloud** | 品質分析、セキュリティ | 無料/有料 | 総合品質管理 |
| **JaCoCo（単体）** | Java専用、ローカル | 無料 | Java開発 |

## ベストプラクティス

### 1. codecov.yml で閾値設定

```yaml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 1%
```

### 2. フラグで詳細分析

```yaml
flags:
  unittests:
    paths:
      - src/
  integration:
    paths:
      - src/
```

### 3. PR ブロック設定

```yaml
comment:
  require_changes: true

coverage:
  status:
    patch:
      default:
        target: 80%
```

### 4. バッジ表示

```markdown
[![codecov](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/user/repo)
```

## 公式リソース

- **公式サイト**: https://about.codecov.io/
- **ドキュメント**: https://docs.codecov.com/
- **GitHub Action**: https://github.com/codecov/codecov-action
- **CLI**: https://github.com/codecov/codecov-cli
- **サポート**: https://codecov.io/support

## まとめ

Codecovは、コードカバレッジ可視化・分析プラットフォームです。CI/CD統合、プルリクエストへのカバレッジコメント、トレンド分析により、チーム全体でテストカバレッジを継続的に監視・改善できます。多言語対応、豊富な統合オプションにより、モダンな開発ワークフローを支援します。

---

**最終更新**: 2025-12-10
**対象バージョン**: Codecov Action v3
