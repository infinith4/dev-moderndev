# GitHub

## 概要

GitHubは、Gitベースのソースコード管理・コラボレーションプラットフォームです。リポジトリホスティング、プルリクエスト、Issue管理、GitHub Actions（CI/CD）、GitHub Pages、GitHub Copilot（AI）により、ソフトウェア開発のワークフロー全体を支援します。Microsoft買収、世界最大のコード共有プラットフォーム、オープンソースコミュニティで広く採用されています。

## 主な機能

### 1. リポジトリ管理
- **Git リポジトリ**: プライベート・パブリック
- **ブランチ管理**: ブランチ保護ルール
- **コードレビュー**: プルリクエスト
- **マージ**: Merge、Squash、Rebase

### 2. コラボレーション
- **Issue**: バグ・機能要望管理
- **Projects**: カンバンボード
- **Discussions**: ディスカッション
- **Wiki**: ドキュメント

### 3. GitHub Actions
- **CI/CD**: ワークフロー自動化
- **マーケットプレイス**: 再利用可能アクション
- **セルフホストランナー**: 自前ランナー

### 4. セキュリティ
- **Dependabot**: 依存関係更新
- **Code scanning**: セキュリティスキャン
- **Secret scanning**: シークレット検出
- **Security advisories**: セキュリティアドバイザリ

## 利用方法

### リポジトリ作成

```bash
# GitHubでリポジトリ作成後
git clone https://github.com/username/repo.git
cd repo

# または既存プロジェクト
git init
git remote add origin https://github.com/username/repo.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

### ブランチ・プルリクエスト

```bash
# 新規ブランチ作成
git checkout -b feature/new-feature

# 変更・コミット
git add .
git commit -m "Add new feature"

# プッシュ
git push origin feature/new-feature

# GitHub上でPull Request作成
# Compare & pull request ボタンをクリック
```

### GitHub Actions（基本）

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Build
      run: npm run build
```

### GitHub Actions（マルチジョブ）

```yaml
# .github/workflows/build.yml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-files
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: build-files
      - name: Deploy
        run: ./deploy.sh
```

### Issue テンプレート

```markdown
<!-- .github/ISSUE_TEMPLATE/bug_report.md -->
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.
```

### Pull Request テンプレート

```markdown
<!-- .github/pull_request_template.md -->
## Description
Please include a summary of the change and which issue is fixed.

Fixes # (issue)

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective
- [ ] New and existing unit tests pass locally
```

### ブランチ保護ルール

```
Settings > Branches > Add branch protection rule

Branch name pattern: main

☑ Require a pull request before merging
  ☑ Require approvals (1)
  ☑ Dismiss stale pull request approvals when new commits are pushed

☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  Status checks: CI, tests

☑ Require conversation resolution before merging

☑ Include administrators
```

### GitHub Pages

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install and Build
        run: |
          npm ci
          npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### GitHub CLI

```bash
# インストール
brew install gh  # macOS
# または https://cli.github.com/

# 認証
gh auth login

# リポジトリ作成
gh repo create my-repo --public

# Issue作成
gh issue create --title "Bug: ..." --body "Description"

# Pull Request作成
gh pr create --title "Add feature" --body "Description"

# Pull Request一覧
gh pr list

# Pull Request マージ
gh pr merge 123 --squash
```

### Dependabot設定

```yaml
# .dependabot/config.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Code Owners

```
# .github/CODEOWNERS
# デフォルトオーナー
* @default-owner

# 特定ディレクトリ
/docs/ @docs-team
/src/api/ @api-team
*.js @frontend-team
```

### Secrets管理

```yaml
# GitHub Secrets使用
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          echo "Deploying with API_KEY"
          ./deploy.sh
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** |  無料 | パブリック無制限、プライベート500MB |
| **Pro** |  $4/月 | プライベート2GB、高度ツール |
| **Team** |  $4/ユーザー/月 | チームアクセス管理 |
| **Enterprise** |  $21/ユーザー/月 | SSO、監査ログ、サポート |

## メリット

1. **無料枠**: 個人開発無料
2. **コミュニティ**: 世界最大
3. **GitHub Actions**: CI/CD統合
4. **エコシステム**: 豊富な統合
5. **GitHub Copilot**: AIコード補完

## デメリット

1. **プライベート制限**: 無料枠制限
2. **ベンダーロックイン**: GitHub依存
3. **ダウンタイム**: 稀にダウン
4. **料金**: 大規模で高額

## 公式リンク

- **公式サイト**: [https://github.com/](https://github.com/)
- **ドキュメント**: [https://docs.github.com/](https://docs.github.com/)

## 関連ドキュメント

- [バージョン管理ツール一覧](../バージョン管理ツール/)
- [GitLab](./GitLab.md)
- [Git](./Git.md)

---

**カテゴリ**: バージョン管理ツール
**対象工程**: ソースコード管理・コラボレーション
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0

