# Terraform Validate

## 概要

Terraform Validateは、Terraformコアに組み込まれた構文検証コマンドです。`terraform validate`コマンドにより、Terraformコードの構文エラー、型エラー、必須属性の欠落等を検出します。プロバイダーAPIを呼び出さずにローカルで実行されるため、高速かつ安全に検証でき、CI/CDパイプラインの初期段階でコード品質を確保します。

## 主な機能

### 1. 構文検証
- **HCL構文チェック**: HashiCorp Configuration Language（HCL）の構文検証
- **リソースブロック検証**: resource、data、module等の構文確認
- **変数型チェック**: 変数型の整合性確認

### 2. 設定検証
- **必須属性**: リソースの必須属性の欠落検出
- **型整合性**: 変数・出力の型チェック
- **参照エラー**: 存在しないリソース参照の検出
- **モジュール検証**: モジュール呼び出しの妥当性

### 3. エラーレポート
- **詳細なエラーメッセージ**: 行番号付きエラー表示
- **JSON出力**: 機械可読フォーマット
- **終了コード**: 0（成功）、1（失敗）

### 4. 特徴
- **オフライン実行**: インターネット接続不要
- **高速**: 数秒で完了
- **プロバイダー不要**: クラウドAPIアクセス不要
- **無料**: Terraform標準機能

## 利用方法

### 基本的な使い方

```bash
# Terraform初期化（必須）
terraform init

# 検証実行
terraform validate

# 成功時の出力
Success! The configuration is valid.

# エラー時の出力例
Error: Missing required argument
  on main.tf line 5, in resource "aws_instance" "example":
   5: resource "aws_instance" "example" {

The argument "ami" is required, but no definition was found.
```

### JSON出力

```bash
# JSON形式で出力
terraform validate -json

# 成功時
{
  "valid": true,
  "error_count": 0,
  "warning_count": 0,
  "diagnostics": []
}

# エラー時
{
  "valid": false,
  "error_count": 1,
  "warning_count": 0,
  "diagnostics": [
    {
      "severity": "error",
      "summary": "Missing required argument",
      "detail": "The argument \"ami\" is required, but no definition was found.",
      "range": {
        "filename": "main.tf",
        "start": { "line": 5, "column": 1 },
        "end": { "line": 5, "column": 38 }
      }
    }
  ]
}
```

### 検出可能なエラー例

#### 1. 必須属性の欠落

```hcl
# エラー: ami属性が必須
resource "aws_instance" "example" {
  instance_type = "t2.micro"
  # ami が欠落
}
```

```
Error: Missing required argument
  on main.tf line 1, in resource "aws_instance" "example":
   1: resource "aws_instance" "example" {

The argument "ami" is required, but no definition was found.
```

#### 2. 型エラー

```hcl
variable "instance_count" {
  type    = number
  default = "not_a_number"  # 型不一致
}
```

```
Error: Invalid default value for variable
  on variables.tf line 3, in variable "instance_count":
   3:   default = "not_a_number"

This default value is not compatible with the variable's type constraint: a number is required.
```

#### 3. 未定義リソース参照

```hcl
resource "aws_security_group_rule" "example" {
  security_group_id = aws_security_group.nonexistent.id  # 存在しないSG
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}
```

```
Error: Reference to undeclared resource
  on main.tf line 2, in resource "aws_security_group_rule" "example":
   2:   security_group_id = aws_security_group.nonexistent.id

A managed resource "aws_security_group" "nonexistent" has not been declared in the root module.
```

#### 4. モジュール引数エラー

```hcl
module "vpc" {
  source = "./modules/vpc"
  # 必須変数 cidr_block が欠落
}
```

```
Error: Missing required argument
  on main.tf line 1, in module "vpc":
   1: module "vpc" {

The argument "cidr_block" is required, but no definition was found.
```

### CI/CD統合

#### GitHub Actions

```yaml
name: Terraform Validate

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0
      
      - name: Terraform Init
        run: terraform init -backend=false
      
      - name: Terraform Validate
        run: terraform validate
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
validate:
  image: hashicorp/terraform:1.6
  stage: test
  script:
    - terraform init -backend=false
    - terraform validate
  only:
    - merge_requests
    - main
```

#### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Terraform Validate') {
            steps {
                sh 'terraform init -backend=false'
                sh 'terraform validate'
            }
        }
    }
}
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.5
    hooks:
      - id: terraform_validate
```

```bash
# インストール
pip install pre-commit
pre-commit install

# 実行
pre-commit run terraform_validate
```

### スクリプトでの使用

```bash
#!/bin/bash
set -e

# Terraform検証スクリプト
echo "Running Terraform validate..."

terraform init -backend=false
terraform validate

if [ $? -eq 0 ]; then
    echo "✅ Validation successful"
    exit 0
else
    echo "❌ Validation failed"
    exit 1
fi
```

### 複数ディレクトリの検証

```bash
#!/bin/bash

# 複数のTerraformディレクトリを検証
for dir in environments/*/; do
    echo "Validating $dir"
    cd "$dir"
    terraform init -backend=false
    terraform validate
    if [ $? -ne 0 ]; then
        echo "Validation failed in $dir"
        exit 1
    fi
    cd - > /dev/null
done

echo "All directories validated successfully"
```

## ベストプラクティス

### 1. CI/CDパイプラインに組み込む

```
terraform init → terraform validate → terraform fmt → terraform plan → terraform apply
```

### 2. `terraform fmt` と併用

```bash
# フォーマット確認
terraform fmt -check

# 検証
terraform validate
```

### 3. `terraform plan` の前に実行

```bash
# 検証してからプラン
terraform validate && terraform plan
```

### 4. JSON出力でCI/CD統合

```bash
# JSON出力をパースして処理
terraform validate -json | jq '.valid'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Terraform Validate** | 🟢 完全無料 | Terraform標準機能、MPL 2.0 License |

## メリット

### ✅ 主な利点

1. **完全無料**: Terraform標準機能
2. **高速**: 数秒で検証完了
3. **オフライン**: インターネット接続不要
4. **プロバイダー不要**: クラウドAPI呼び出し不要
5. **構文エラー早期検出**: コミット前に検出
6. **CI/CD統合容易**: 簡単にパイプライン組み込み
7. **JSON出力**: 機械可読フォーマット
8. **軽量**: 追加インストール不要
9. **エラーメッセージ詳細**: 行番号付きエラー表示
10. **学習容易**: シンプルなコマンド

## デメリット

### ❌ 制約・課題

1. **構文のみ**: セキュリティチェックは非対応
2. **ロジックエラー未検出**: 意図しない設定は検出不可
3. **ベストプラクティス**: コーディング規約は非対応
4. **リソース検証なし**: クラウド側の制約は未確認
5. **ランタイムエラー**: 実行時エラーは検出不可
6. **コンプライアンス**: CIS Benchmark等は非対応
7. **カスタムルール**: 独自ルール追加不可
8. **統合機能なし**: 単一機能のみ

## 代替・補完ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **tfsec** | セキュリティスキャン | Validateより高度なセキュリティチェック |
| **Checkov** | マルチIaCセキュリティ | Validateより包括的 |
| **Terraform Compliance** | BDD形式ポリシーテスト | Validateより柔軟なルール |
| **terraform fmt** | フォーマットチェック | Validateと併用 |
| **Sentinel** | HashiCorp公式ポリシーエンジン | Validateよりエンタープライズ向け |

## 公式リンク

- **Terraform公式**: [https://www.terraform.io/](https://www.terraform.io/)
- **Validateドキュメント**: [https://developer.hashicorp.com/terraform/cli/commands/validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
- **Terraform CLI**: [https://developer.hashicorp.com/terraform/cli](https://developer.hashicorp.com/terraform/cli)

## 関連ドキュメント

- [IaCセキュリティツール一覧](../IaCセキュリティツール/)
- [Terraform](../IaCツール/Terraform.md)
- [tfsec](./tfsec.md)
- [Terraform Compliance](./Terraform_Compliance.md)
- [Checkov](../セキュリティツール/Checkov.md)
- [Terraformベストプラクティス](../../best-practices/terraform.md)

---

**カテゴリ**: IaCセキュリティツール  
**対象工程**: インフラ構築  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
