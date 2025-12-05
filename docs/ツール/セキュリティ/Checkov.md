# Checkov

## 概要

Checkovは、Bridgecrewが開発したInfrastructure as Code（IaC）のためのオープンソース静的解析ツールです。Terraform、CloudFormation、Kubernetes、Dockerfileなど、幅広いIaCフレームワークに対応し、デプロイ前にセキュリティとコンプライアンスの問題を検出します。2,000以上のポリシーを組み込みで持ち、CIS Benchmarks、PCI-DSS、HIPAA等の業界標準に対応しています。開発フローの早い段階でインフラの設定ミスを発見できるため、「Shift Left Security」の実践に最適です。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Checkov (OSS)** | 🟢 完全無料 | オープンソース、無制限スキャン、Apache License 2.0 |
| **Bridgecrew Platform Free** | 🟢 無料 | クラウド統合、無制限スキャン、基本レポート |
| **Bridgecrew Platform Team** | 💰 見積もり必要 | 高度な分析、カスタムポリシー、チーム機能 |
| **Bridgecrew Platform Enterprise** | 💰 見積もり必要 | SSO、監査ログ、専用サポート、SLA |

**注意**: Checkov本体は完全無料。Bridgecrew Platformは追加のクラウド機能を提供（任意）。

## メリット・デメリット

### メリット
- ✅ **完全無料**: オープンソース、商用利用も無料
- ✅ **多様なIaC対応**: Terraform、CloudFormation、K8s、Docker、ARM、Bicep等
- ✅ **豊富なポリシー**: 2,000以上の組み込みポリシー
- ✅ **コンプライアンス**: CIS、PCI-DSS、HIPAA、GDPR対応
- ✅ **カスタムポリシー**: Pythonで独自ポリシーを作成可能
- ✅ **CI/CD統合**: GitHub Actions、GitLab CI、Jenkins等と簡単に統合
- ✅ **自動修正**: 一部の問題を自動修正可能
- ✅ **詳細なレポート**: SARIF、JSON、JUnit XML等の形式で出力

### デメリット
- ❌ **実行時間**: 大規模プロジェクトではスキャンに時間がかかる
- ❌ **誤検知**: 環境によってはfalse positiveが発生
- ❌ **Python依存**: Python環境が必要
- ❌ **ドキュメント**: 一部のポリシーのドキュメントが不足
- ❌ **学習曲線**: カスタムポリシー作成には Python知識が必要

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **6. 詳細設計（インフラ）** | IaCコードのセキュリティ設計検証 | セキュリティ設計レビュー |
| **8. インフラ構築** | IaCコードのセキュリティチェック | セキュリティスキャン結果 |
| **8-1. CI/CD** | パイプラインでの自動セキュリティゲート | CI/CDセキュリティレポート |
| **10. テスト（インフラ）** | インフラ設定の脆弱性テスト | 脆弱性診断結果 |
| **11. 導入** | 本番デプロイ前の最終セキュリティチェック | セキュリティ監査レポート |

## 基本的な利用方法

### 1. インストール

```bash
# pip経由でインストール（推奨）
pip install checkov

# Homebrew (macOS)
brew install checkov

# Docker
docker pull bridgecrew/checkov

# バージョン確認
checkov --version

# ヘルプ表示
checkov --help
```

### 2. 基本的なスキャン

```bash
# ディレクトリ全体をスキャン
checkov -d /path/to/terraform

# 特定のファイルをスキャン
checkov -f main.tf

# Terraformプロジェクトのスキャン
checkov --framework terraform -d terraform/

# CloudFormationのスキャン
checkov --framework cloudformation -f template.yaml

# Kubernetesマニフェストのスキャン
checkov --framework kubernetes -d k8s/

# Dockerfileのスキャン
checkov --framework dockerfile -f Dockerfile

# 複数フレームワークを同時スキャン
checkov -d . --framework terraform,dockerfile,kubernetes
```

### 3. 結果のフィルタリングと出力

```bash
# 重要度High以上のみ表示
checkov -d . --check CKV_AWS_*

# 特定のチェックをスキップ
checkov -d . --skip-check CKV_AWS_79

# JSON形式で出力
checkov -d . -o json

# SARIF形式で出力（GitHub連携用）
checkov -d . -o sarif --output-file-path results.sarif

# JUnit XML形式で出力
checkov -d . -o junitxml

# 複数形式で同時出力
checkov -d . -o cli -o json -o sarif

# コンパクト出力（合格したチェックを非表示）
checkov -d . --compact

# 詳細出力
checkov -d . -v
```

## 工程別の活用方法

### 6. 詳細設計（インフラ）での活用

**目的**: IaCコードの設計段階でセキュリティベストプラクティスを適用

**活用方法**:
- Terraformコードのセキュリティレビュー
- CIS Benchmarksへの準拠確認
- リソース設定のベストプラクティスチェック

**実装例（Terraformスキャン）**:
```bash
# Terraformプロジェクトの包括的スキャン
checkov -d terraform/ --framework terraform

# 出力例:
# Check: CKV_AWS_79: "Ensure Instance Metadata Service Version 1 is not enabled"
#   FAILED for resource: aws_instance.web
#   File: /terraform/ec2.tf:10-25
#   Guide: https://docs.bridgecrew.io/docs/bc_aws_general_31
#
# Check: CKV_AWS_23: "Ensure every security groups rule has a description"
#   FAILED for resource: aws_security_group.web
#   File: /terraform/security_group.tf:5-15

# CIS Benchmarksに準拠しているか確認
checkov -d terraform/ --framework terraform --check CKV_AWS_*

# 特定のコンプライアンス基準でフィルタ
checkov -d terraform/ --compact --framework terraform \
  --external-checks-dir ./custom_policies
```

**カスタムポリシーの作成**:
```python
# custom_policies/require_tags.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class RequireSpecificTags(BaseResourceCheck):
    def __init__(self):
        name = "Ensure all resources have required tags"
        id = "CKV_CUSTOM_1"
        supported_resources = ['aws_instance', 'aws_s3_bucket']
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        required_tags = ['Environment', 'Owner', 'CostCenter']
        tags = conf.get('tags', [{}])[0]

        for required_tag in required_tags:
            if required_tag not in tags:
                return CheckResult.FAILED

        return CheckResult.PASSED

check = RequireSpecificTags()
```

---

### 8. インフラ構築での活用

**目的**: インフラ構築前のセキュリティ検証

**活用方法**:
- デプロイ前のセキュリティゲート
- 複数環境（dev/staging/prod）の一貫したチェック
- インフラコードのセキュリティ標準化

**実装例（環境別スキャン）**:
```bash
# 開発環境
checkov -d terraform/environments/dev \
  --framework terraform \
  --soft-fail

# ステージング環境
checkov -d terraform/environments/staging \
  --framework terraform \
  --soft-fail

# 本番環境（厳格チェック）
checkov -d terraform/environments/prod \
  --framework terraform \
  --hard-fail-on high \
  -o json -o sarif

# CloudFormationスタックのスキャン
checkov -f cloudformation/stack.yaml \
  --framework cloudformation \
  -o junitxml --output-file-path cfn-results.xml
```

**設定ファイル（.checkov.yaml）**:
```yaml
# .checkov.yaml
framework:
  - terraform
  - dockerfile
  - kubernetes

directory:
  - terraform/
  - k8s/

skip-check:
  - CKV_AWS_79  # IMDSv2（特定の環境で無効化）

external-checks-dir:
  - ./custom_policies

output:
  - cli
  - json
  - sarif

compact: true

quiet: false
```

---

### 8-1. CI/CDでの活用

**目的**: パイプラインでの自動セキュリティチェック

**活用方法**:
- プルリクエスト時の自動スキャン
- マージ前のセキュリティゲート
- 脆弱性の早期検出

**GitHub Actions統合**:
```yaml
# .github/workflows/checkov.yml
name: Checkov Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  checkov-scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Checkov scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          output_format: sarif
          output_file_path: checkov-results.sarif
          soft_fail: false  # FAILで終了

      - name: Upload Checkov results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: checkov-results.sarif

      - name: Archive scan results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: checkov-report
          path: checkov-results.sarif
```

**GitLab CI/CD統合**:
```yaml
# .gitlab-ci.yml
stages:
  - security

checkov-scan:
  stage: security
  image: bridgecrew/checkov:latest
  script:
    - checkov -d terraform/ -o json -o junitxml --output-file-path results
  artifacts:
    reports:
      junit: results.xml
    paths:
      - results.json
  allow_failure: false
```

**Jenkins統合**:
```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Checkov Scan') {
            steps {
                script {
                    docker.image('bridgecrew/checkov:latest').inside {
                        sh '''
                            checkov -d terraform/ \
                              -o cli -o json -o junitxml \
                              --output-file-path scan-results
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            junit 'scan-results.xml'
            archiveArtifacts artifacts: 'scan-results.json'
        }
    }
}
```

---

### 10. テスト（インフラ）での活用

**目的**: インフラ設定の包括的セキュリティテスト

**活用方法**:
- Kubernetesマニフェストの検証
- Dockerイメージのセキュリティチェック
- Helmチャートのスキャン

**実装例（Kubernetesスキャン）**:
```bash
# Kubernetesマニフェストのスキャン
checkov -d k8s/ --framework kubernetes

# 出力例:
# Check: CKV_K8S_8: "Liveness Probe Should be Configured"
#   FAILED for resource: Deployment.default.nginx
#   File: /k8s/deployment.yaml:1-20
#
# Check: CKV_K8S_22: "Use read-only filesystem for containers"
#   FAILED for resource: Deployment.default.nginx
#   File: /k8s/deployment.yaml:15-18

# Helmチャートのスキャン
helm template myapp ./mychart > rendered.yaml
checkov -f rendered.yaml --framework kubernetes

# Docker Composeのスキャン
checkov -f docker-compose.yml --framework docker_composition
```

**複数フレームワークの統合スキャン**:
```bash
#!/bin/bash
# comprehensive-scan.sh

set -e

echo "Running comprehensive infrastructure security scan..."

# Terraform
echo "1. Scanning Terraform..."
checkov -d terraform/ --framework terraform -o json > terraform-results.json

# Kubernetes
echo "2. Scanning Kubernetes..."
checkov -d k8s/ --framework kubernetes -o json > k8s-results.json

# Dockerfile
echo "3. Scanning Dockerfiles..."
checkov -d . --framework dockerfile -o json > dockerfile-results.json

# ARM Templates
echo "4. Scanning ARM templates..."
checkov -d arm/ --framework arm -o json > arm-results.json

# 結果の集約
echo "All scans completed. Generating consolidated report..."
python generate_report.py \
  terraform-results.json \
  k8s-results.json \
  dockerfile-results.json \
  arm-results.json
```

---

### 11. 導入での活用

**目的**: 本番デプロイ前の最終セキュリティ検証

**活用方法**:
- 本番環境への厳格なセキュリティゲート
- コンプライアンス監査への対応
- セキュリティレポート生成

**実装例（本番デプロイゲート）**:
```bash
#!/bin/bash
# production-deployment-gate.sh

set -e

THRESHOLD_HIGH=0
THRESHOLD_CRITICAL=0

echo "=== Production Deployment Security Gate ==="

# Checkov実行（JSON出力）
checkov -d terraform/environments/prod \
  --framework terraform \
  -o json > prod-scan-results.json

# 重大度Critical/Highの脆弱性数を取得
CRITICAL_COUNT=$(jq '[.results.failed_checks[] | select(.check_class contains "CKV_AWS")] | length' prod-scan-results.json)
HIGH_COUNT=$(jq '[.results.failed_checks[] | select(.severity == "HIGH")] | length' prod-scan-results.json)

echo "Critical issues: $CRITICAL_COUNT (threshold: $THRESHOLD_CRITICAL)"
echo "High issues: $HIGH_COUNT (threshold: $THRESHOLD_HIGH)"

# しきい値チェック
if [ "$CRITICAL_COUNT" -gt "$THRESHOLD_CRITICAL" ]; then
    echo "❌ FAILED: Critical vulnerabilities found!"
    exit 1
fi

if [ "$HIGH_COUNT" -gt "$THRESHOLD_HIGH" ]; then
    echo "❌ FAILED: Too many high severity issues!"
    exit 1
fi

echo "✅ PASSED: Security gate checks passed!"
exit 0
```

**コンプライアンスレポート生成**:
```bash
# PCI-DSS準拠レポート
checkov -d terraform/ \
  --framework terraform \
  --check CKV_AWS_* \
  -o json | \
  jq '.results.failed_checks[] | select(.guideline contains "PCI-DSS")' \
  > pci-dss-violations.json

# CIS Benchmarksレポート
checkov -d terraform/ \
  --framework terraform \
  --compact \
  -o cli > cis-benchmark-report.txt
```

## 公式ドキュメント

- [Checkov 公式サイト](https://www.checkov.io/)
- [Checkov Documentation](https://www.checkov.io/1.Welcome/Quick%20Start.html)
- [Checkov GitHub Repository](https://github.com/bridgecrewio/checkov)
- [Checkov Policy Index](https://www.checkov.io/5.Policy%20Index/all.html)
- [Bridgecrew Platform](https://www.bridgecrew.cloud/)
- [Checkov CLI Reference](https://www.checkov.io/2.Basics/CLI%20Command%20Reference.html)

## 学習リソース

### チュートリアル
- [Getting Started with Checkov](https://www.checkov.io/1.Welcome/Quick%20Start.html)
- [Checkov Custom Policies](https://www.checkov.io/3.Custom%20Policies/Custom%20Policies%20Overview.html)
- [Integrating Checkov into CI/CD](https://www.checkov.io/4.Integrations/CI%20Integrations.html)

### 動画・コース
- [Checkov Tutorial](https://www.youtube.com/results?search_query=checkov+tutorial)
- [IaC Security with Checkov](https://www.youtube.com/results?search_query=iac+security+checkov)

### コミュニティ
- [Checkov Slack Community](https://slack.bridgecrew.io/)
- [Checkov GitHub Discussions](https://github.com/bridgecrewio/checkov/discussions)
- [Stack Overflow - Checkov](https://stackoverflow.com/questions/tagged/checkov)

## 関連リンク

### 統合ツール
- [Checkov VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Bridgecrew.checkov)
- [Checkov GitHub Action](https://github.com/bridgecrewio/checkov-action)
- [Checkov Pre-commit Hook](https://github.com/bridgecrewio/checkov#pre-commit)
- [Terraform Checkov Module](https://registry.terraform.io/modules/bridgecrewio/checkov/null/latest)

### 関連セキュリティツール
- [tfsec](https://github.com/aquasecurity/tfsec) - Terraform専用セキュリティスキャナー
- [Terrascan](https://runterrascan.io/) - IaCセキュリティスキャナー
- [KICS](https://kics.io/) - IaCセキュリティスキャナー
- [Snyk IaC](https://snyk.io/product/infrastructure-as-code-security/) - Snyk IaCスキャン

### ベストプラクティス
- [IaC Security Best Practices](https://www.checkov.io/7.Scan%20Examples/Terraform.html)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [Shift Left Security](https://www.bridgecrew.io/blog/shift-left-security/)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
