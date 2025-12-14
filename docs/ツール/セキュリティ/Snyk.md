# Snyk

## 概要

Snykは、開発者向けのセキュリティプラットフォームで、オープンソース依存関係、コンテナイメージ、Infrastructure as Code（IaC）、アプリケーションコードの脆弱性を検出・修正します。「開発者ファーストのセキュリティ」を掲げ、IDEやCI/CDパイプラインに統合して、開発ワークフローの中でセキュリティ問題を早期発見できます。自動修正機能により、脆弱性の修正プルリクエストを自動生成することも可能です。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Free** | 🟢 無料 | 個人・小規模プロジェクト、月200テスト、1プロジェクト |
| **Team** | 💰 $52/developer/月 | 月1,000テスト、無制限プロジェクト、Slackサポート |
| **Business** | 💰 $152/developer/月 | 無制限テスト、SSO、カスタムルール、優先サポート |
| **Enterprise** | 💰 見積もり必要 | オンプレミス、専用サポート、SLA、高度な統合 |

**注意**: オープンソースプロジェクトは無料プランで無制限に利用可能。個人開発者向けにも無料枠が提供されています。

## メリット・デメリット

### メリット
- ✅ **開発者フレンドリー**: IDE、Git、CI/CDに統合、開発フローを妨げない
- ✅ **包括的スキャン**: 依存関係、コンテナ、IaC、コードの4領域をカバー
- ✅ **自動修正**: 脆弱性の修正PRを自動生成
- ✅ **詳細な脆弱性情報**: CVE、CWE、修正方法を提供
- ✅ **リアルタイム監視**: 新しい脆弱性を継続的に監視
- ✅ **多言語対応**: JavaScript、Java、Python、Go、Ruby、PHP、.NET等
- ✅ **無料枠**: オープンソース・個人開発者向けに無料提供
- ✅ **ライセンスチェック**: オープンソースライセンスのコンプライアンス確認

### デメリット
- ❌ **料金**: 商用利用では比較的高額
- ❌ **誤検知**: 特に古いライブラリで誤検知が発生する場合も
- ❌ **ネットワーク依存**: クラウドサービスのため常時接続が必要
- ❌ **プライバシー**: コードをSnykクラウドに送信（オンプレミス版で解決可能）
- ❌ **学習コスト**: 高度な機能を使いこなすには時間が必要

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | 依存関係の脆弱性チェック、ライセンス確認 | 脆弱性レポート、修正PR |
| **8. インフラ構築** | IaCコードのセキュリティチェック | IaCセキュリティレポート |
| **8-1. CI/CD** | パイプラインでの自動セキュリティチェック | CI/CDセキュリティゲート |
| **10. テスト（インフラ）** | コンテナイメージの脆弱性スキャン | コンテナセキュリティレポート |
| **11. 導入** | 本番環境デプロイ前のセキュリティ検証 | セキュリティ監査結果 |

## 基本的な利用方法

### 1. インストール

```bash
# npm（グローバルインストール）
npm install -g snyk

# Homebrew (macOS)
brew tap snyk/tap
brew install snyk

# Scoop (Windows)
scoop bucket add snyk https://github.com/snyk/scoop-snyk
scoop install snyk

# Docker
docker pull snyk/snyk

# 認証
snyk auth

# バージョン確認
snyk --version
```

### 2. 基本的なスキャン

```bash
# プロジェクトの依存関係をスキャン
snyk test

# 詳細情報付きスキャン
snyk test --severity-threshold=high

# JSON形式で出力
snyk test --json

# HTMLレポート生成
snyk test --json | snyk-to-html -o snyk-report.html

# 継続的監視（Snykクラウドに登録）
snyk monitor

# 自動修正可能な脆弱性を確認
snyk wizard

# Dockerイメージのスキャン
snyk container test docker-image:tag

# IaCコードのスキャン（Terraform、CloudFormation等）
snyk iac test terraform.tf

# コードの脆弱性スキャン
snyk code test
```

### 3. IDE統合

```bash
# VS Code拡張機能
# Marketplace から "Snyk Security" をインストール

# IntelliJ IDEA / PyCharm等
# Plugins → "Snyk Vulnerability Scanner" をインストール

# 設定
# Settings → Snyk → Authenticate → トークンを入力
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: 依存関係の脆弱性を早期発見、ライセンスコンプライアンス確認

**活用方法**:
- package.json、requirements.txt等の依存関係スキャン
- 脆弱性の自動修正
- ライセンスポリシー違反の検出
- IDEでのリアルタイムフィードバック

**実装例（Node.jsプロジェクト）**:
```bash
# 依存関係のスキャン
cd /path/to/your/project
snyk test

# 出力例:
# Testing /path/to/your/project...
#
# ✗ High severity vulnerability found in lodash
#   Description: Prototype Pollution
#   Info: https://snyk.io/vuln/SNYK-JS-LODASH-590103
#   Introduced through: lodash@4.17.15
#   From: lodash@4.17.15
#   Fixed in: 4.17.19
#
# Organization: my-org
# Tested 245 dependencies for known issues, found 3 issues, 3 vulnerable paths.

# 自動修正を試行
snyk wizard

# 修正可能な脆弱性を自動でアップデート
snyk fix

# 特定の脆弱性を無視（誤検知の場合）
snyk ignore --id=SNYK-JS-LODASH-590103 --reason="Not applicable to our use case"
```

**CI/CD統合（GitHub Actions）**:
```yaml
# .github/workflows/snyk-security.yml
name: Snyk Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Upload Snyk report
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: snyk.sarif
```

**package.jsonにスクリプト追加**:
```json
{
  "scripts": {
    "security:check": "snyk test",
    "security:monitor": "snyk monitor",
    "security:fix": "snyk wizard"
  },
  "snyk": true
}
```

**Python プロジェクトでの使用**:
```bash
# Pythonプロジェクトのスキャン
cd /path/to/python/project
pip install -r requirements.txt

snyk test --file=requirements.txt

# Pipfileのスキャン
snyk test --file=Pipfile

# 特定の重要度以上のみ報告
snyk test --severity-threshold=critical

# 修正可能な脆弱性を自動アップデート
snyk fix
```

---

### 8. インフラ構築での活用

**目的**: Infrastructure as Codeのセキュリティ問題検出

**活用方法**:
- Terraform、CloudFormation、Kubernetes YAMLのスキャン
- セキュリティベストプラクティス違反の検出
- リソース設定の誤りを早期発見

**実装例（Terraformスキャン）**:
```bash
# Terraformファイルのスキャン
snyk iac test terraform/

# 出力例:
# Testing main.tf...
#
# Infrastructure as code issues:
#   ✗ S3 bucket is not encrypted [High Severity]
#     Path: resource > aws_s3_bucket > my_bucket > encryption
#     File: main.tf:10-15
#
#   ✗ Security group allows ingress from 0.0.0.0/0 [Medium Severity]
#     Path: resource > aws_security_group > my_sg > ingress
#     File: main.tf:30-35

# JSON形式で出力
snyk iac test terraform/ --json > iac-report.json

# SARIFフォーマットで出力（GitHub連携用）
snyk iac test terraform/ --sarif > snyk-iac.sarif

# 特定のルールのみチェック
snyk iac test --rules=SNYK-CC-TF-1,SNYK-CC-TF-2
```

**Kubernetes YAMLのスキャン**:
```bash
# Kubernetesマニフェストのスキャン
snyk iac test k8s/deployment.yaml

# 出力例:
# ✗ Container is running without root user control [High Severity]
#   Path: spec > containers[0] > securityContext > runAsNonRoot
#
# ✗ Container is running without AppArmor profile [Low Severity]
#   Path: metadata > annotations > container.apparmor.security.beta.kubernetes.io
```

**CI/CD統合（GitLab CI/CD）**:
```yaml
# .gitlab-ci.yml
stages:
  - security

snyk-iac-scan:
  stage: security
  image: snyk/snyk:node
  script:
    - snyk auth $SNYK_TOKEN
    - snyk iac test terraform/ --sarif-file-output=snyk-iac.sarif
  artifacts:
    reports:
      sast: snyk-iac.sarif
  only:
    - main
    - develop
```

---

### 10. テスト（インフラ）での活用

**目的**: コンテナイメージの脆弱性検出

**活用方法**:
- Dockerイメージのスキャン
- ベースイメージの脆弱性チェック
- レイヤー別の脆弱性分析

**実装例（Dockerイメージスキャン）**:
```bash
# Dockerイメージのスキャン
snyk container test node:18-alpine

# 出力例:
# Testing node:18-alpine...
#
# ✗ High severity vulnerability found in openssl
#   Package manager: apk
#   Vulnerable module: openssl
#   Introduced through: openssl@3.0.7-r0
#   Fixed in: 3.0.7-r2
#
# Organization: my-org
# Tested node:18-alpine for known issues, found 5 vulnerabilities

# ローカルイメージのスキャン
docker build -t myapp:latest .
snyk container test myapp:latest

# Dockerfileもスキャン
snyk container test myapp:latest --file=Dockerfile

# JSONレポート生成
snyk container test myapp:latest --json > container-report.json

# 継続監視
snyk container monitor myapp:latest
```

**マルチステージビルドの推奨**:
```dockerfile
# Dockerfile (Snyk推奨パターン)
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine
WORKDIR /app
# 脆弱性のあるパッケージを含まない本番用イメージ
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "server.js"]
```

**CI/CDでのコンテナスキャン（Jenkins）**:
```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }

        stage('Snyk Container Scan') {
            steps {
                script {
                    sh """
                        snyk container test myapp:${BUILD_NUMBER} \
                        --severity-threshold=high \
                        --json > snyk-container-report.json
                    """
                }
            }
        }

        stage('Push to Registry') {
            when {
                expression {
                    // Snykスキャン通過時のみプッシュ
                    return currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh 'docker push myapp:${BUILD_NUMBER}'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'snyk-container-report.json'
        }
    }
}
```

---

### 11. 導入での活用

**目的**: 本番環境デプロイ前の最終セキュリティチェック

**活用方法**:
- デプロイゲートとしてのセキュリティチェック
- 本番環境の継続的監視
- セキュリティポリシーの強制

**実装例（デプロイゲート）**:
```bash
# デプロイ前チェックスクリプト
#!/bin/bash
# deploy-gate.sh

set -e

echo "Running security checks before deployment..."

# 依存関係スキャン
echo "1. Checking dependencies..."
snyk test --severity-threshold=critical || {
    echo "Critical vulnerabilities found in dependencies!"
    exit 1
}

# コンテナイメージスキャン
echo "2. Checking container image..."
snyk container test myapp:latest --severity-threshold=high || {
    echo "High severity vulnerabilities found in container!"
    exit 1
}

# IaCスキャン
echo "3. Checking infrastructure code..."
snyk iac test terraform/ --severity-threshold=high || {
    echo "Infrastructure security issues found!"
    exit 1
}

echo "All security checks passed! Proceeding with deployment..."
exit 0
```

**Snykポリシーファイル（.snyk）**:
```yaml
# .snyk
# Snyk (https://snyk.io) policy file

version: v1.25.0

# 無視する脆弱性
ignore:
  'SNYK-JS-LODASH-590103':
    - '*':
        reason: Not applicable to our use case
        expires: 2025-12-31T00:00:00.000Z

# パッチ適用
patch:
  'SNYK-JS-MINIMIST-559764':
    - '*':
        patched: '2024-01-15T10:30:00.000Z'

# ライセンスポリシー
license:
  allowed:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
  disallowed:
    - GPL-3.0
    - AGPL-3.0
```

**継続的監視（Snyk Monitor）**:
```bash
# 本番環境の継続的監視を有効化
snyk monitor --project-name=production-app

# 特定のタグで監視
snyk monitor --project-tags=env=production,team=backend

# 定期実行（cron）
# 毎日午前2時にスキャン実行
0 2 * * * cd /path/to/project && snyk monitor
```

## 公式ドキュメント

- [Snyk 公式サイト](https://snyk.io/)
- [Snyk Documentation](https://docs.snyk.io/)
- [Snyk CLI Reference](https://docs.snyk.io/snyk-cli)
- [Snyk API Documentation](https://snyk.docs.apiary.io/)
- [Snyk GitHub Repository](https://github.com/snyk)
- [Snyk Vulnerability Database](https://security.snyk.io/)

## 学習リソース

### チュートリアル
- [Getting Started with Snyk](https://docs.snyk.io/getting-started)
- [Snyk Learn](https://learn.snyk.io/) - 無料セキュリティ学習プラットフォーム
- [Snyk CLI Tutorial](https://docs.snyk.io/snyk-cli/getting-started-with-the-cli)

### 書籍・コース
- "Securing DevOps" by Julien Vehent (O'Reilly)
- Snyk Academy - 公式トレーニングコース

### 動画
- [Snyk YouTube Channel](https://www.youtube.com/c/Snyksec)
- [Snyk Tutorial for Beginners](https://www.youtube.com/results?search_query=snyk+tutorial)
- [DevSecOps with Snyk](https://www.youtube.com/results?search_query=devsecops+snyk)

### コミュニティ
- [Snyk Community](https://community.snyk.io/)
- [Snyk GitHub Discussions](https://github.com/snyk/cli/discussions)
- [Stack Overflow - Snyk](https://stackoverflow.com/questions/tagged/snyk)

## 関連リンク

### 統合ツール
- [Snyk for VS Code](https://marketplace.visualstudio.com/items?itemName=snyk-security.snyk-vulnerability-scanner)
- [Snyk for IntelliJ](https://plugins.jetbrains.com/plugin/10972-snyk-vulnerability-scanner)
- [Snyk GitHub Action](https://github.com/snyk/actions)
- [Snyk Jenkins Plugin](https://plugins.jenkins.io/snyk-security-scanner/)

### 関連セキュリティツール
- [Dependabot](https://github.com/dependabot) - GitHub依存関係アップデート
- [Trivy](https://github.com/aquasecurity/trivy) - コンテナスキャナー
- [Checkov](https://www.checkov.io/) - IaCセキュリティスキャナー
- [SonarQube](https://www.sonarqube.org/) - コード品質・セキュリティ

### ベストプラクティス
- [DevSecOps Best Practices](https://snyk.io/learn/devsecops/)
- [Container Security Best Practices](https://snyk.io/learn/container-security/)
- [Shift Left Security](https://snyk.io/learn/shift-left-security/)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
