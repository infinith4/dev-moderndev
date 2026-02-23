# GitHub Actions

## 概要

GitHub Actionsは、GitHubが提供する公式のCI/CD（継続的インテグレーション/継続的デリバリー）プラットフォームです。GitHubリポジトリに統合されたワークフロー自動化ツールとして、ビルド、テスト、デプロイを含むソフトウェア開発ライフサイクル全体を自動化できます。YAMLファイルでワークフローを定義し、プッシュ、プルリクエスト、スケジュール、手動トリガーなど様々なイベントで実行できます。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Public repositories** |  無料 | パブリックリポジトリは無制限利用可能 |
| **Free (Private)** |  無料 | プライベート: 2,000分/月、500MBストレージ |
| **Pro** |  $4/user/月 | 3,000分/月、1GBストレージ |
| **Team** |  $4/user/月 | 3,000分/月、2GBストレージ |
| **Enterprise** |  $21/user/月 | 50,000分/月、50GBストレージ |
| **追加料金** |  従量課金 | Ubuntu: $0.008/分、Windows: $0.016/分、macOS: $0.08/分 |

**注意**: パブリックリポジトリは無料ですが、プライベートリポジトリは月間実行時間の上限があります。

## メリット・デメリット

### メリット
-  **GitHub統合**: リポジトリと完全統合、追加設定不要
-  **豊富なマーケットプレイス**: 数千のアクションが利用可能
-  **マルチプラットフォーム**: Linux、Windows、macOSをサポート
-  **マトリックスビルド**: 複数の環境で並列テスト可能
-  **シークレット管理**: 環境変数の安全な管理
-  **再利用可能なワークフロー**: 共通ワークフローの再利用
-  **セルフホストランナー**: 独自の実行環境をホスト可能
-  **依存関係キャッシュ**: ビルド時間を短縮

### デメリット
-  **GitHub依存**: GitHub以外のプラットフォームでは使えない
-  **実行時間制限**: プライベートリポジトリには月間制限あり
-  **デバッグ困難**: ローカルでのワークフローテストが難しい
-  **ログ保持期間**: 90日間のみ（Enterpriseは最大400日）
-  **ワークフロー制限**: ジョブあたり最大6時間の実行時間

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | コミット時の自動ビルド、コードフォーマット | ワークフローファイル、ビルド結果 |
| **8-1. CI/CD** | 自動ビルド、テスト、デプロイパイプライン構築 | CI/CDパイプライン、デプロイ履歴 |
| **9. テスト（アプリケーション）** | 自動テストの実行、カバレッジ計測 | テスト結果、カバレッジレポート |
| **10. テスト（インフラ）** | インフラコードのテスト、検証 | インフラテスト結果 |
| **11. 導入** | 本番環境への自動デプロイ | デプロイログ、リリースノート |

## 基本的な利用方法

### 1. ワークフローファイルの作成

GitHub Actionsはリポジトリの `.github/workflows/` ディレクトリにYAMLファイルを配置することで動作します。

```bash
# リポジトリのルートディレクトリで
mkdir -p .github/workflows
cd .github/workflows

# ワークフローファイルを作成
touch ci.yml
```

### 2. 基本的なワークフロー例

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

# トリガー: mainブランチへのプッシュとプルリクエスト
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

# ジョブ定義
jobs:
  build:
    # 実行環境
    runs-on: ubuntu-latest

    # ステップ定義
    steps:
      # 1. リポジトリのチェックアウト
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. Node.jsのセットアップ
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # 3. 依存関係のインストール
      - name: Install dependencies
        run: npm ci

      # 4. リンティング
      - name: Run linter
        run: npm run lint

      # 5. テスト実行
      - name: Run tests
        run: npm test

      # 6. ビルド
      - name: Build
        run: npm run build
```

### 3. 基本的なコマンド

```bash
# ローカルでYAML構文チェック（VS Code拡張機能使用）
# 拡張機能: GitHub Actions (GitHub公式)

# ワークフローの手動実行（workflow_dispatchトリガーが必要）
# GitHubのUI: Actions タブ → ワークフロー選択 → Run workflow

# セルフホストランナーの追加
# Settings → Actions → Runners → New self-hosted runner

# シークレットの追加
# Settings → Secrets and variables → Actions → New repository secret
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: コード品質の維持、自動フォーマット、早期バグ検出

**活用方法**:
- コミット時の自動リンティング
- コードフォーマットチェック
- 単体テストの自動実行
- 依存関係の脆弱性スキャン

**実装例（Pull Requestチェック）**:
```yaml
# .github/workflows/pr-check.yml
name: Pull Request Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  code-quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install flake8 black pytest

      - name: Code formatting check
        run: black --check .

      - name: Linting
        run: flake8 . --max-line-length=88

      - name: Run unit tests
        run: pytest tests/unit/

      - name: Security scan
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

### 8-1. CI/CDでの活用

**目的**: 完全自動化されたビルド・テスト・デプロイパイプライン構築

**活用方法**:
- マルチステージビルド
- 環境別デプロイ（dev/staging/prod）
- 承認フローの実装
- ロールバック機能

**実装例（マルチステージデプロイ）**:
```yaml
# .github/workflows/deploy.yml
name: Deploy Pipeline

on:
  push:
    branches:
      - develop  # 開発環境へ自動デプロイ
      - main     # 本番環境へ承認後デプロイ

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker tag myapp:${{ github.sha }} myapp:latest

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Push image
        run: |
          docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
          docker push ghcr.io/${{ github.repository }}:latest

  deploy-dev:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: development

    steps:
      - name: Deploy to Dev
        run: |
          echo "Deploying to development environment"
          # kubectl apply -f k8s/dev/ など

  deploy-prod:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.example.com

    steps:
      - name: Deploy to Production
        run: |
          echo "Deploying to production environment"
          # kubectl apply -f k8s/prod/ など
```

---

### 9. テスト（アプリケーション）での活用

**目的**: 包括的な自動テストの実行、品質メトリクスの取得

**活用方法**:
- マトリックステスト（複数バージョン/OS）
- E2Eテストの実行
- コードカバレッジ計測
- テスト結果の可視化

**実装例（マトリックステスト）**:
```yaml
# .github/workflows/test-matrix.yml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 21]
        exclude:
          # macOSではNode 18をスキップ
          - os: macos-latest
            node-version: 18

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/coverage-final.json
          flags: ${{ matrix.os }}-node${{ matrix.node-version }}
```

---

### 10. テスト（インフラ）での活用

**目的**: Infrastructure as Codeの検証、インフラ変更の安全性確保

**活用方法**:
- Terraformのplanとvalidate
- Ansible Playbookの構文チェック
- インフラセキュリティスキャン
- コスト見積もり

**実装例（Terraformテスト）**:
```yaml
# .github/workflows/terraform.yml
name: Terraform CI

on:
  push:
    paths:
      - 'terraform/**'
  pull_request:
    paths:
      - 'terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Terraform Format Check
        run: terraform fmt -check -recursive
        working-directory: ./terraform

      - name: Terraform Init
        run: terraform init
        working-directory: ./terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Terraform Validate
        run: terraform validate
        working-directory: ./terraform

      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: ./terraform

      - name: Security Scan with Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform

      - name: Cost Estimation
        uses: infracost/actions/setup@v2
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate cost estimate
        run: infracost breakdown --path=terraform/
```

---

### 11. 導入での活用

**目的**: 本番環境への安全で確実なデプロイ、リリース管理

**活用方法**:
- ブルー/グリーンデプロイメント
- カナリアリリース
- 承認ゲート
- ロールバック機能
- リリースノート自動生成

**実装例（承認ゲート付きデプロイ）**:
```yaml
# .github/workflows/production-deploy.yml
name: Production Deployment

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: |
          npm ci
          npm test

      - name: Build artifacts
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: dist/

  deploy-production:
    needs: build-and-test
    runs-on: ubuntu-latest

    # 承認が必要な本番環境
    environment:
      name: production
      url: https://app.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-artifacts
          path: dist/

      - name: Deploy to Production
        run: |
          echo "Deploying version ${{ github.ref_name }}"
          # デプロイスクリプト実行

      - name: Health Check
        run: |
          sleep 30
          curl -f https://app.example.com/health || exit 1

      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref_name }}
          body: |
            Changes in this release:
            - Auto-generated from tag ${{ github.ref_name }}
          draft: false
          prerelease: false
```

**ロールバック用ワークフロー**:
```yaml
# .github/workflows/rollback.yml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to (e.g., v1.2.3)'
        required: true
        type: string

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.version }}

      - name: Rollback to ${{ inputs.version }}
        run: |
          echo "Rolling back to version ${{ inputs.version }}"
          # ロールバックスクリプト実行

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🔄 Rollback to ${{ inputs.version }} completed"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## 公式ドキュメント

- [GitHub Actions 公式サイト](https://github.com/features/actions)
- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
- [ワークフロー構文リファレンス](https://docs.github.com/ja/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Marketplace](https://github.com/marketplace?type=actions) - 公式アクション集
- [GitHub Actions Changelog](https://github.blog/changelog/label/actions/)
- [セルフホストランナー](https://docs.github.com/ja/actions/hosting-your-own-runners)

## 学習リソース

### チュートリアル
- [GitHub Actions Quickstart](https://docs.github.com/ja/actions/quickstart)
- [Learning GitHub Actions](https://docs.github.com/ja/actions/learn-github-actions)
- [GitHub Actions Workshops](https://github.com/githubpartners/github-actions-workshop)

### 書籍・コース
- "Learning GitHub Actions" by Brent Laster (O'Reilly)
- GitHub Learning Lab - GitHub Actions コース
- LinkedIn Learning - GitHub Actions
- Udemy - GitHub Actions: The Complete Guide

### 動画
- [GitHub Actions Tutorial for Beginners](https://www.youtube.com/results?search_query=github+actions+tutorial)
- [GitHub Universe - Actions Sessions](https://githubuniverse.com/)
- [freeCodeCamp - GitHub Actions](https://www.youtube.com/watch?v=R8_veQiYBjI)

### コミュニティ
- [GitHub Community Discussions - Actions](https://github.com/orgs/community/discussions/categories/actions)
- [GitHub Actions GitHub Repository](https://github.com/actions)
- [r/github (Reddit)](https://www.reddit.com/r/github/)
- [Stack Overflow - GitHub Actions](https://stackoverflow.com/questions/tagged/github-actions)

## 関連リンク

### 関連ツール・アクション
- [actions/checkout](https://github.com/actions/checkout) - リポジトリチェックアウト
- [actions/setup-node](https://github.com/actions/setup-node) - Node.js環境セットアップ
- [actions/setup-python](https://github.com/actions/setup-python) - Python環境セットアップ
- [docker/build-push-action](https://github.com/docker/build-push-action) - Dockerイメージビルド&プッシュ
- [codecov/codecov-action](https://github.com/codecov/codecov-action) - コードカバレッジアップロード
- [act](https://github.com/nektos/act) - ローカルでGitHub Actionsを実行

### 便利なアクション集
- [super-linter](https://github.com/github/super-linter) - 複数言語対応リンター
- [release-drafter](https://github.com/release-drafter/release-drafter) - リリースノート自動生成
- [stale](https://github.com/actions/stale) - 古いIssue/PRの自動クローズ
- [labeler](https://github.com/actions/labeler) - PRへの自動ラベル付け
- [dependency-review-action](https://github.com/actions/dependency-review-action) - 依存関係レビュー

### ベストプラクティス
- [GitHub Actions Best Practices](https://docs.github.com/ja/actions/security-guides/security-hardening-for-github-actions)
- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions) - アクション集
- [Security Hardening Guide](https://docs.github.com/ja/actions/security-guides/security-hardening-for-github-actions)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

