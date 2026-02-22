# tfsec

## 概要

tfsecは、Terraformコードの静的セキュリティ解析ツールです。Terraformファイルをスキャンし、AWS、Azure、GCP等のクラウドリソース設定における潜在的なセキュリティリスクを検出します。CIS Benchmark、PCI-DSS、SOC2等のコンプライアンス基準に準拠したチェックを実施し、CI/CDパイプラインに統合することで、インフラコードのセキュリティを事前に確保します。

## 主な機能

### 1. セキュリティスキャン
- **500+のチェック**: AWS、Azure、GCP、Kubernetes等
- **CIS Benchmark**: 業界標準コンプライアンス
- **ベストプラクティス**: クラウドセキュリティのベストプラクティス
- **カスタムチェック**: 独自ルール追加

### 2. マルチクラウド対応
- **AWS**: S3、EC2、RDS、IAM等
- **Azure**: Storage、VM、Database等
- **GCP**: GCS、Compute、Cloud SQL等
- **Kubernetes**: Pod Security、RBAC等
- **Docker**: Dockerfileセキュリティ

### 3. 検出可能な脆弱性
- **パブリック公開**: S3バケット、ストレージの公開設定
- **暗号化なし**: データ暗号化の欠落
- **過度な権限**: IAMポリシーの過剰権限
- **デフォルト設定**: セキュアでないデフォルト値
- **ログ無効**: 監査ログの未設定
- **ネットワーク**: 0.0.0.0/0からのアクセス許可

### 4. CI/CD統合
- **GitHub Actions**: アクションとして実行
- **GitLab CI**: パイプライン統合
- **Jenkins**: プラグイン統合
- **Terraform Cloud**: 自動スキャン
- **Pre-commit Hook**: コミット前チェック

### 5. レポート
- **JSON**: 機械可読形式
- **JUnit**: CI/CD統合
- **SARIF**: GitHub Code Scanningフォーマット
- **HTML**: 人間可読レポート
- **CSV**: スプレッドシート形式

### 6. IDE統合
- **VS Code**: tfsec拡張
- **IntelliJ IDEA**: プラグイン
- **Vim/Emacs**: コマンドライン統合

## 利用方法

### インストール

```bash
# Homebrew (macOS/Linux)
brew install tfsec

# Linux (wget)
wget https://github.com/aquasecurity/tfsec/releases/latest/download/tfsec-linux-amd64
chmod +x tfsec-linux-amd64
sudo mv tfsec-linux-amd64 /usr/local/bin/tfsec

# Windows (Chocolatey)
choco install tfsec

# Docker
docker pull aquasec/tfsec

# バージョン確認
tfsec --version
```

### 基本的な使い方

```bash
# カレントディレクトリのTerraformコードをスキャン
tfsec .

# 特定ディレクトリをスキャン
tfsec /path/to/terraform

# 詳細出力
tfsec . --verbose

# 重大度でフィルタ（HIGH以上のみ表示）
tfsec . --minimum-severity HIGH
```

### 出力例

```
Result #1 HIGH S3 bucket does not have logging enabled.
─────────────────────────────────────────────────────────────
  main.tf:5-10
─────────────────────────────────────────────────────────────
   5    resource "aws_s3_bucket" "example" {
   6      bucket = "my-bucket"
   7      acl    = "private"
   8    
   9      # No logging configuration
  10    }
─────────────────────────────────────────────────────────────
  ID:          AWS017
  Impact:      There is no way to determine access to this bucket
  Resolution:  Add a logging block to the resource

  More Info:
  - https://aquasecurity.github.io/tfsec/latest/checks/aws/s3/enable-bucket-logging/

Results:
  1 problems detected.
```

### 特定のチェックを無視

```hcl
# Terraformコード内でコメントで無視
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
  #tfsec:ignore:aws-s3-enable-bucket-logging
  acl    = "private"
}

# 理由を記載
resource "aws_security_group" "example" {
  #tfsec:ignore:aws-vpc-no-public-ingress-sgr:This is intentionally public
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 設定ファイル（.tfsec.yml）

```yaml
# .tfsec/config.yml
severity_overrides:
  aws-s3-enable-bucket-encryption: ERROR
  aws-s3-enable-versioning: WARNING

exclude:
  - aws-vpc-no-public-ingress-sgr
  - azure-storage-use-secure-tls-policy

minimum_severity: MEDIUM
```

### JSON出力（CI/CD統合）

```bash
# JSON形式で出力
tfsec . --format json > tfsec-results.json

# JUnit形式（Jenkins統合）
tfsec . --format junit > tfsec-junit.xml

# SARIF形式（GitHub Code Scanning）
tfsec . --format sarif > tfsec.sarif
```

### CI/CD統合

#### GitHub Actions

```yaml
name: tfsec

on:
  push:
    branches: [main]
  pull_request:

jobs:
  tfsec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run tfsec
        uses: aquasecurity/tfsec-action@v1.0.0
        with:
          soft_fail: false
          format: sarif
          
      - name: Upload SARIF file
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: tfsec.sarif
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
tfsec:
  image: aquasec/tfsec:latest
  script:
    - tfsec . --format json > tfsec-report.json
  artifacts:
    reports:
      sast: tfsec-report.json
  only:
    - merge_requests
    - main
```

#### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/aquasecurity/tfsec
    rev: v1.28.1
    hooks:
      - id: tfsec
        args:
          - --minimum-severity=HIGH
```

```bash
# インストール
pip install pre-commit
pre-commit install

# 実行
pre-commit run tfsec
```

### Docker実行

```bash
# Dockerコンテナで実行
docker run --rm -v $(pwd):/src aquasec/tfsec /src

# カスタム設定ファイル使用
docker run --rm \
  -v $(pwd):/src \
  -v $(pwd)/.tfsec:/config \
  aquasec/tfsec /src --config-file /config/config.yml
```

### カスタムチェック作成

```rego
# custom_checks/s3_custom.rego
package custom.s3

deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    not resource.tags.Owner
    msg := sprintf("S3 bucket '%s' must have an Owner tag", [name])
}
```

```bash
# カスタムチェック実行
tfsec . --custom-check-dir ./custom_checks
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **tfsec (OSS)** | 🟢 無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **無料**: オープンソース、MIT License
2. **高速**: 数秒でスキャン完了
3. **500+チェック**: 包括的なセキュリティチェック
4. **マルチクラウド**: AWS、Azure、GCP対応
5. **CI/CD統合**: GitHub Actions、GitLab CI等
6. **カスタムルール**: Regoで独自チェック追加
7. **無視機能**: 特定チェックの除外可能
8. **IDE統合**: VS Code、IntelliJ対応
9. **軽量**: 単一バイナリ、依存なし
10. **アクティブ開発**: 継続的な更新

## デメリット

### ❌ 制約・課題

1. **静的解析のみ**: 実行時の問題は検出不可
2. **誤検知**: 一部で誤検知の可能性
3. **Terraform専用**: CloudFormation、Bicep等は非対応
4. **ランタイム設定**: 環境変数等の動的設定は未考慮
5. **学習コスト**: ルールの理解が必要
6. **カスタムルール**: Rego言語の習得必要
7. **統合設定**: CI/CD統合に初期設定必要
8. **GUI不在**: コマンドラインのみ

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Checkov** | Python製、マルチIaC対応 | tfsecよりCloudFormation、Bicep対応 |
| **Terrascan** | マルチクラウド、500+ポリシー | tfsecと類似、追加機能あり |
| **Snyk IaC** | 商用、UIあり | tfsecより高機能だが有料 |
| **Terraform Sentinel** | HashiCorp公式、ポリシーエンジン | tfsecよりエンタープライズ向け |
| **Trivy** | コンテナ+IaCスキャン | tfsecよりオールインワン |

## 公式リンク

- **公式サイト**: [https://aquasecurity.github.io/tfsec/](https://aquasecurity.github.io/tfsec/)
- **GitHub**: [https://github.com/aquasecurity/tfsec](https://github.com/aquasecurity/tfsec)
- **チェックリスト**: [https://aquasecurity.github.io/tfsec/latest/checks/](https://aquasecurity.github.io/tfsec/latest/checks/)
- **GitHub Actions**: [https://github.com/aquasecurity/tfsec-action](https://github.com/aquasecurity/tfsec-action)

## 関連ドキュメント

- [IaCセキュリティツール一覧](../IaCセキュリティツール/)
- [Terraform](../IaCツール/Terraform.md)
- [Checkov](../セキュリティツール/Checkov.md)
- [Snyk](../セキュリティツール/Snyk.md)
- [Terraformセキュリティベストプラクティス](../../best-practices/terraform-security.md)

---

**カテゴリ**: IaCセキュリティツール  
**対象工程**: インフラ構築、セキュリティ  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
