# Terraform

## 概要

Terraformは、HashiCorp社が開発したオープンソースのInfrastructure as Code（IaC）ツールです。HCL（HashiCorp Configuration Language）という宣言型の設定言語を使用して、クラウドインフラストラクチャをコードとして定義・管理できます。AWS、Azure、GCP、その他多数のプロバイダーに対応したマルチクラウド対応が特徴です。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Terraform CLI** | 🟢 完全無料 | オープンソース版、ローカル実行 |
| **Terraform Cloud Free** | 🟢 無料 | 最大5ユーザー、リモートステート管理 |
| **Terraform Cloud Team** | 💰 $20/user/月 | チーム協業機能、ポリシー管理 |
| **Terraform Cloud Business** | 💰 見積もり必要 | SAML SSO、監査ログ、SLA |
| **Terraform Enterprise** | 💰 見積もり必要 | オンプレミス版、エンタープライズ機能 |

## メリット・デメリット

### メリット
- ✅ **マルチクラウド対応**: AWS、Azure、GCP、その他300以上のプロバイダー対応
- ✅ **宣言型構文**: HCL言語でインフラを簡潔に記述
- ✅ **状態管理**: tfstateファイルで現在のインフラ状態を追跡
- ✅ **実行計画**: `terraform plan`で変更内容を事前確認
- ✅ **モジュール化**: 再利用可能なモジュールで管理を効率化
- ✅ **大規模コミュニティ**: Terraform Registryで多数のモジュール利用可能
- ✅ **GitOps対応**: コードとしてバージョン管理、CI/CD統合可能

### デメリット
- ❌ **学習曲線**: HCL言語、モジュール、状態管理の概念の習得が必要
- ❌ **状態管理の複雑さ**: tfstateファイルの競合、ロック機構の設定が必要
- ❌ **プロバイダー依存**: プロバイダーのバージョン互換性に注意が必要
- ❌ **デバッグ困難**: エラーメッセージが分かりにくい場合がある
- ❌ **クラウド固有機能**: 各クラウドの最新機能への対応に遅延がある場合も

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **6. 詳細設計（インフラ）** | インフラ構成のコード化設計、リソース定義 | Terraformコード設計書、モジュール設計 |
| **8. インフラ構築** | 実際のインフラリソースのプロビジョニング | Terraformコード、tfstateファイル |
| **10. テスト（インフラ）** | インフラのテスト、変更の検証 | テスト結果、検証レポート |
| **11. 導入** | 本番環境へのインフラデプロイ | デプロイ手順書、本番環境構成 |

## 基本的な利用方法

### 1. インストール

```bash
# macOS (Homebrew)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Windows (Chocolatey)
choco install terraform

# Linux
wget https://releases.hashicorp.com/terraform/<VERSION>/terraform_<VERSION>_linux_amd64.zip
unzip terraform_<VERSION>_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# バージョン確認
terraform version
```

### 2. 基本的なワークフロー

```bash
# 1. Terraformの初期化
terraform init

# 2. 実行計画の確認
terraform plan

# 3. リソースの適用
terraform apply

# 4. リソースの削除
terraform destroy
```

### 3. 基本的なTerraformコード例

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

# VPCの作成
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}

# サブネットの作成
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "ap-northeast-1a"

  tags = {
    Name = "public-subnet"
  }
}
```

## 工程別の活用方法

### 6. 詳細設計（インフラ）での活用

**目的**: インフラ構成をTerraformコードとして設計

**活用方法**:
- リソースの依存関係を明確化
- モジュール構造の設計
- 変数とoutputの定義
- リモートステート管理の設計

**成果物**:
- Terraformコード設計書
- ディレクトリ構造設計
- モジュール設計書
- 環境別変数定義（dev/staging/prod）

**ベストプラクティス**:
```hcl
# variables.tf - 変数定義
variable "environment" {
  description = "環境名（dev/staging/prod）"
  type        = string
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  type        = string
  default     = "10.0.0.0/16"
}

# outputs.tf - 出力定義
output "vpc_id" {
  description = "作成されたVPCのID"
  value       = aws_vpc.main.id
}

# terraform.tfvars - 環境別変数値
environment = "dev"
vpc_cidr    = "10.0.0.0/16"
```

---

### 8. インフラ構築での活用

**目的**: 設計したインフラを実際にプロビジョニング

**活用方法**:
- 開発環境での動作検証
- ステージング環境でのテスト
- 本番環境へのデプロイ
- リモートバックエンドの設定

**実行コマンド**:
```bash
# 環境別の適用
terraform workspace new dev
terraform workspace select dev
terraform apply -var-file="env/dev.tfvars"

# リモートバックエンドの設定
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "dev/terraform.tfstate"
    region = "ap-northeast-1"
    dynamodb_table = "terraform-lock"
  }
}
```

**ディレクトリ構造例**:
```
terraform/
├── modules/
│   ├── vpc/
│   ├── ec2/
│   └── rds/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
└── backend.tf
```

---

### 10. テスト（インフラ）での活用

**目的**: Terraformコードの品質保証とインフラの検証

**活用方法**:
- `terraform validate`: 構文チェック
- `terraform plan`: 変更内容の確認
- Terraform Test（実験的機能）
- Terratest等のテストフレームワーク

**テストコマンド例**:
```bash
# 構文チェック
terraform fmt -check -recursive
terraform validate

# 変更計画の確認
terraform plan -out=tfplan

# tflintでリンティング
tflint

# Terratestによるテスト（Go言語）
go test -v -timeout 30m
```

---

### 11. 導入での活用

**目的**: 本番環境への安全なデプロイ

**活用方法**:
- CI/CDパイプラインとの統合
- 承認フローの実装
- ロールバック手順の準備
- 監視・アラート設定

**CI/CD統合例（GitHub Actions）**:
```yaml
name: Terraform Apply

on:
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply tfplan
```

## 公式ドキュメント

- [Terraform 公式サイト](https://www.terraform.io/)
- [Terraform ドキュメント](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [HashiCorp Learn - Terraform Tutorials](https://developer.hashicorp.com/terraform/tutorials)
- [Terraform AWS Provider ドキュメント](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Azure Provider ドキュメント](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform GCP Provider ドキュメント](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

## 学習リソース

### チュートリアル
- [Getting Started with Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Gruntwork Terraform Training](https://gruntwork.io/training/)

### 書籍
- "Terraform: Up & Running" by Yevgeniy Brikman
- "Terraform in Action" by Scott Winkler
- "Infrastructure as Code, 2nd Edition" by Kief Morris

### 動画・コース
- [HashiCorp Terraform Certification](https://www.hashicorp.com/certification/terraform-associate)
- [Udemy - Terraform Beginner to Advanced](https://www.udemy.com/topic/terraform/)
- [YouTube - Terraform Tutorial for Beginners](https://www.youtube.com/results?search_query=terraform+tutorial)

### コミュニティ
- [HashiCorp Discuss - Terraform](https://discuss.hashicorp.com/c/terraform-core/)
- [Terraform GitHub Repository](https://github.com/hashicorp/terraform)
- [r/Terraform (Reddit)](https://www.reddit.com/r/Terraform/)

## 関連リンク

### 関連ツール
- [Terragrunt](https://terragrunt.gruntwork.io/) - Terraformのラッパーツール、DRYな設定を実現
- [Terratest](https://terratest.gruntwork.io/) - Terraformコードのテストフレームワーク
- [tflint](https://github.com/terraform-linters/tflint) - Terraformのリンター
- [tfsec](https://aquasecurity.github.io/tfsec/) - Terraformのセキュリティスキャナー
- [Checkov](https://www.checkov.io/) - IaCセキュリティスキャナー
- [Infracost](https://www.infracost.io/) - Terraformのコスト見積もりツール

### ベストプラクティス
- [Terraform Style Guide](https://www.terraform-best-practices.com/code-styling)
- [Google Cloud Terraform Best Practices](https://cloud.google.com/docs/terraform/best-practices-for-terraform)
- [AWS Terraform Best Practices](https://aws.amazon.com/blogs/apn/terraform-best-practices-for-aws-users/)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
