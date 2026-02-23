# TFLint

## 概要

TFLintは、Terraformコードの静的解析ツールです。Terraform言語の構文チェックに加え、AWS・Azure・GCPなどのプロバイダー固有のルールにより、存在しないインスタンスタイプの指定やリージョン名のタイプミスなど、`terraform plan` では検出できない誤設定を早期に発見します。プラグインアーキテクチャにより拡張可能で、カスタムルールの作成やCI/CDパイプラインへの統合を通じて、インフラコードの品質を継続的に保証します。

## 主な機能

### 1. Terraform構文チェック
- **構文エラー**: HCL構文の問題検出
- **非推奨構文**: 古い記法の警告
- **変数検証**: 変数の型チェックとデフォルト値検証
- **モジュール検証**: モジュール参照の検証

### 2. プロバイダー固有ルール
- **AWS**: インスタンスタイプ、AMI、リージョン等の検証
- **Azure**: VMサイズ、リージョン、リソース名等の検証
- **GCP**: マシンタイプ、ゾーン等の検証
- **カスタムプロバイダー**: プラグインによる拡張

### 3. ベストプラクティス
- **命名規則**: リソース名の規約チェック
- **タグ付け**: 必須タグの存在確認
- **セキュリティ**: セキュリティグループ等の設定検証
- **コスト**: 高コストリソースの警告

### 4. プラグインシステム
- **公式プラグイン**: AWS、Azure、GCP対応
- **コミュニティプラグイン**: 追加ルール
- **カスタムプラグイン**: Go言語で独自プラグイン作成

### 5. CI/CD統合
- **GitHub Actions**: ワークフロー統合
- **GitLab CI**: パイプライン統合
- **Pre-commit**: コミット前チェック
- **自動修正**: 一部ルールの自動修正対応

## 利用方法

### インストール

```bash
# Homebrewでインストール（macOS/Linux）
brew install tflint

# Chocolateyでインストール（Windows）
choco install tflint

# バイナリダウンロード（Linux）
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Dockerで実行
docker run --rm -v $(pwd):/data -t ghcr.io/terraform-linters/tflint

# バージョン確認
tflint --version
```

### 設定ファイル（.tflint.hcl）

```hcl
# .tflint.hcl

# TFLintの基本設定
config {
  # Terraformモジュールの検査を有効化
  module = true

  # 強制終了するルールレベル
  force = false
}

# AWSプロバイダープラグイン
plugin "aws" {
  enabled = true
  version = "0.30.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"

  # リージョン指定
  deep_check = true
}

# Azureプロバイダープラグイン
plugin "azurerm" {
  enabled = true
  version = "0.25.0"
  source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
}

# GCPプロバイダープラグイン
plugin "google" {
  enabled = true
  version = "0.27.0"
  source  = "github.com/terraform-linters/tflint-ruleset-google"
}

# 個別ルールの設定
rule "terraform_naming_convention" {
  enabled = true

  custom_formats = {
    resource = {
      format = "^[a-z][a-z0-9_]*$"
      description = "リソース名は小文字英数字とアンダースコアのみ"
    }
  }
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

rule "terraform_standard_module_structure" {
  enabled = true
}

# 特定ルールの無効化
rule "terraform_unused_declarations" {
  enabled = false
}
```

### 実行

```bash
# プラグインのインストール
tflint --init

# 現在のディレクトリを検査
tflint

# 特定ディレクトリを検査
tflint ./modules/vpc/

# 再帰的に全ディレクトリを検査
tflint --recursive

# 出力フォーマットを指定
tflint --format json
tflint --format compact
tflint --format sarif

# 設定ファイルを指定
tflint --config .tflint.custom.hcl

# 特定ルールのみ実行
tflint --only terraform_naming_convention

# 変数ファイルを指定
tflint --var-file=terraform.tfvars
```

### 検査対象のTerraformコード例

```hcl
# main.tf
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"  # TFLintがインスタンスタイプを検証

  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # TFLintが警告を出す
  }
}

resource "aws_db_instance" "main" {
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.medium"
  allocated_storage    = 20
  storage_encrypted    = false  # TFLintが警告を出す

  tags = {
    Name = "main-db"
  }
}
```

### カスタムルールの例（.tflint.hcl内）

```hcl
# 必須タグルール
rule "aws_resource_missing_tags" {
  enabled = true

  tags = ["Environment", "Project", "Owner"]
}

# インスタンスタイプの制限
rule "aws_instance_invalid_type" {
  enabled = true
}

# デフォルトVPCの使用禁止
rule "aws_instance_default_vpc" {
  enabled = true
}
```

### CI/CD統合

```yaml
# .github/workflows/tflint.yml
name: TFLint

on:
  push:
    paths:
      - '**.tf'
      - '.tflint.hcl'
  pull_request:
    paths:
      - '**.tf'
      - '.tflint.hcl'

jobs:
  tflint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/cache@v4
        with:
          path: ~/.tflint.d/plugins
          key: tflint-${{ hashFiles('.tflint.hcl') }}

      - uses: terraform-linters/setup-tflint@v4
        with:
          tflint_version: v0.50.0

      - name: Init TFLint
        run: tflint --init

      - name: Run TFLint
        run: tflint --recursive --format compact
```

### Pre-commit設定

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/terraform-linters/tflint
    rev: v0.50.0
    hooks:
      - id: tflint
        args: ['--recursive']
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **TFLint** | 無料 | オープンソース、MPL-2.0 License |

## メリット

### 主な利点

1. **早期検出**: `terraform plan` 前に問題を発見
2. **プロバイダー固有ルール**: AWS/Azure/GCP固有の誤設定を検出
3. **軽量・高速**: 単一バイナリで高速実行
4. **プラグイン拡張**: プラグインによる柔軟な機能拡張
5. **CI/CD統合**: GitHub Actions等との簡単な統合
6. **カスタムルール**: プロジェクト固有のルール定義
7. **再帰的検査**: モジュール構造の一括検査
8. **複数出力形式**: JSON、SARIF、コンパクト形式対応
9. **アクティブ開発**: 頻繁なアップデートとルール追加
10. **pre-commit対応**: コミット前の自動チェック

## デメリット

### 制約・課題

1. **プラグイン管理**: プロバイダープラグインの個別管理が必要
2. **ルールカバレッジ**: 全てのリソースタイプをカバーしていない
3. **動的値**: 変数やデータソースの動的な値は検証不可
4. **学習曲線**: ルール設定とプラグイン設定の理解が必要
5. **偽陽性**: 一部ルールで誤検知が発生する場合がある
6. **Go依存**: カスタムプラグイン開発にはGo言語の知識が必要
7. **ドキュメント**: プラグイン固有ルールのドキュメントが分散

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Checkov** | IaCセキュリティスキャナー | セキュリティに特化、マルチIaC対応 |
| **tfsec** | Terraformセキュリティスキャナー | セキュリティルールに特化 |
| **Sentinel** | HashiCorp製ポリシー言語 | Terraform Cloud/Enterprise統合 |
| **OPA/Conftest** | 汎用ポリシーエンジン | Rego言語でのポリシー記述 |
| **terraform validate** | 公式バリデーション | 構文チェックのみ（プロバイダー検証なし） |

## 公式リンク

- **GitHub**: [https://github.com/terraform-linters/tflint](https://github.com/terraform-linters/tflint)
- **ドキュメント**: [https://github.com/terraform-linters/tflint/tree/master/docs](https://github.com/terraform-linters/tflint/tree/master/docs)
- **AWSプラグイン**: [https://github.com/terraform-linters/tflint-ruleset-aws](https://github.com/terraform-linters/tflint-ruleset-aws)
- **Azureプラグイン**: [https://github.com/terraform-linters/tflint-ruleset-azurerm](https://github.com/terraform-linters/tflint-ruleset-azurerm)
- **GCPプラグイン**: [https://github.com/terraform-linters/tflint-ruleset-google](https://github.com/terraform-linters/tflint-ruleset-google)

## 関連ドキュメント

- [IaCインフラ管理一覧](../IaCインフラ管理/)
- [CloudFormation Guard](./CloudFormation_Guard.md)
- [Velero](./Velero.md)

---

**カテゴリ**: IaCインフラ管理
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
