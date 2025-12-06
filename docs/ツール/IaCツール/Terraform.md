# Terraform

## 概要

Terraformは、HashiCorp製のInfrastructure as Code（IaC）ツールです。HCL（HashiCorp Configuration Language）、宣言的記述、マルチクラウド対応（AWS、Azure、GCP等）、ステート管理により、インフラ構築・管理を自動化します。オープンソース、クラウドネイティブで広く使用されています。

## 主な機能

### 1. 宣言的記述
- **HCL**: 独自設定言語
- **リソース定義**: インフラリソース
- **モジュール**: 再利用可能コンポーネント
- **変数**: パラメータ化

### 2. ステート管理
- **terraform.tfstate**: 現状管理
- **リモートステート**: S3、Terraform Cloud
- **ロック**: 同時実行防止
- **バージョン管理**: ステート履歴

### 3. プロバイダー
- **AWS**: EC2、S3、RDS等
- **Azure**: VM、Storage等
- **GCP**: Compute Engine等
- **100+プロバイダー**: Kubernetes、GitHub等

### 4. ライフサイクル
- **plan**: 変更プレビュー
- **apply**: 適用
- **destroy**: 削除
- **import**: 既存リソース取り込み

## 利用方法

### インストール

```bash
# macOS (Homebrew)
brew install terraform

# Linux (Ubuntu)
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# バージョン確認
terraform version
```

### 基本構成

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

# EC2インスタンス
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }
}

# S3バケット
resource "aws_s3_bucket" "bucket" {
  bucket = "my-terraform-bucket"
}
```

### 変数・出力

```hcl
# variables.tf
variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

# outputs.tf
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}

output "instance_public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.web.public_ip
}
```

```hcl
# main.tf（変数使用）
provider "aws" {
  region = var.region
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_type
}
```

### 基本コマンド

```bash
# 初期化
terraform init

# フォーマット
terraform fmt

# 検証
terraform validate

# プラン（変更プレビュー）
terraform plan

# 適用
terraform apply

# 自動承認
terraform apply -auto-approve

# 削除
terraform destroy

# ステート確認
terraform show
terraform state list
```

### モジュール

```hcl
# modules/vpc/main.tf
variable "cidr_block" {
  type = string
}

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block

  tags = {
    Name = "main-vpc"
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}
```

```hcl
# main.tf（モジュール使用）
module "vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id     = module.vpc.vpc_id
  cidr_block = "10.0.1.0/24"
}
```

### リモートステート

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-northeast-1"

    # ステートロック
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
```

### ワークスペース

```bash
# ワークスペース一覧
terraform workspace list

# ワークスペース作成
terraform workspace new dev
terraform workspace new prod

# ワークスペース切り替え
terraform workspace select dev

# 現在のワークスペース
terraform workspace show
```

```hcl
# main.tf（ワークスペース使用）
locals {
  env = terraform.workspace
}

resource "aws_instance" "web" {
  instance_type = local.env == "prod" ? "t2.medium" : "t2.micro"

  tags = {
    Environment = local.env
  }
}
```

### データソース

```hcl
# 既存VPC取得
data "aws_vpc" "existing" {
  id = "vpc-123456"
}

# 最新AMI取得
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}
```

### プロビジョナー

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  # リモート実行
  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }

  # ローカル実行
  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> instances.txt"
  }
}
```

### 条件・ループ

```hcl
# count
resource "aws_instance" "web" {
  count = 3

  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "web-${count.index}"
  }
}

# for_each
variable "users" {
  type = set(string)
  default = ["alice", "bob", "charlie"]
}

resource "aws_iam_user" "users" {
  for_each = var.users
  name     = each.value
}

# 条件
variable "environment" {
  default = "dev"
}

resource "aws_instance" "web" {
  count = var.environment == "prod" ? 3 : 1

  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.environment == "prod" ? "t2.medium" : "t2.micro"
}
```

### インポート

```bash
# 既存リソースをTerraformに取り込み
terraform import aws_instance.web i-1234567890abcdef0
terraform import aws_s3_bucket.bucket my-existing-bucket
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Terraform OSS** | 🟢 完全無料 | オープンソース |
| **Terraform Cloud** | 🟢/💰 | Free/Team ($20/user/月)/Business |
| **Terraform Enterprise** | 💰 要問い合わせ | オンプレミス、エンタープライズ機能 |

## メリット

1. **マルチクラウド**: AWS、Azure、GCP対応
2. **宣言的**: 望ましい状態を記述
3. **ステート管理**: 現状把握・差分適用
4. **モジュール**: コード再利用
5. **エコシステム**: 豊富なプロバイダー

## デメリット

1. **ステート管理**: ステートファイル管理必要
2. **学習曲線**: HCL習得必要
3. **ドリフト**: 手動変更で不整合
4. **複雑性**: 大規模で複雑化

## 公式リンク

- **公式サイト**: [https://www.terraform.io/](https://www.terraform.io/)
- **ドキュメント**: [https://developer.hashicorp.com/terraform/docs](https://developer.hashicorp.com/terraform/docs)

## 関連ドキュメント

- [IaCツール一覧](../IaCツール/)
- [AWS](../クラウドプラットフォームツール/AWS.md)
- [Ansible](../構成管理ツール/Ansible.md)

---

**カテゴリ**: IaCツール
**対象工程**: インフラ自動化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
