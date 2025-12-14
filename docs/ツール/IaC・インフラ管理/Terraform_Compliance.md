# Terraform Compliance

## 概要

Terraform Complianceは、BDD（振る舞い駆動開発）スタイルでTerraformコードのコンプライアンステストを実行するオープンソースツールです。Gherkin構文（Given-When-Then）でポリシーを記述し、セキュリティ、コスト、組織のベストプラクティスに準拠しているかを検証します。CI/CDパイプラインに統合し、インフラコードの品質とコンプライアンスを自動的に保証します。

## 主な機能

### 1. BDDスタイルポリシー
- **Gherkin構文**: 自然言語風のポリシー記述
- **Given-When-Then**: 可読性の高いテストシナリオ
- **非技術者でも理解可能**: ビジネスルールを明確化

### 2. Terraform統合
- **terraform plan解析**: planファイルをJSON解析
- **リソース検証**: 全リソースタイプ対応
- **属性チェック**: タグ、暗号化、ネットワーク設定等

### 3. カスタムポリシー
- **独自ルール**: 組織固有のポリシー作成
- **再利用可能**: ポリシーファイルの共有
- **階層化**: 複数ポリシーファイルの組み合わせ

### 4. CI/CD統合
- **GitHub Actions**: アクションとして実行
- **GitLab CI**: パイプライン統合
- **Jenkins**: プラグイン統合
- **終了コード**: 失敗時に非ゼロ返却

### 5. レポート
- **詳細レポート**: テスト結果の詳細表示
- **JUnit XML**: CI/CD統合フォーマット
- **色付き出力**: ターミナルでの視認性向上

## 利用方法

### インストール

```bash
# pip
pip install terraform-compliance

# Docker
docker pull eerkunt/terraform-compliance

# バージョン確認
terraform-compliance --version
```

### 基本的な使い方

```bash
# 1. Terraform planをJSON形式で出力
terraform init
terraform plan -out=plan.out
terraform show -json plan.out > plan.json

# 2. ポリシーディレクトリ作成
mkdir compliance-policies

# 3. terraform-compliance実行
terraform-compliance -f compliance-policies -p plan.json
```

### ポリシー作成例

```gherkin
# compliance-policies/s3.feature
Feature: S3 Bucket Encryption
  
  Scenario: S3 buckets must have encryption enabled
    Given I have aws_s3_bucket defined
    Then it must contain server_side_encryption_configuration
```

### CI/CD統合

#### GitHub Actions

```yaml
name: Terraform Compliance

on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Plan
        run: |
          terraform plan -out=plan.out
          terraform show -json plan.out > plan.json
      
      - name: Install terraform-compliance
        run: pip install terraform-compliance
      
      - name: Run Compliance Tests
        run: terraform-compliance -f compliance-policies -p plan.json
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Terraform Compliance** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **完全無料**: オープンソース、MIT License
2. **BDD形式**: 自然言語風で可読性高い
3. **カスタムポリシー**: 組織独自のルール作成
4. **CI/CD統合**: GitHub Actions、GitLab CI対応
5. **再利用可能**: ポリシーファイルの共有
6. **非技術者でも理解**: Gherkin構文で明確
7. **柔軟な検証**: 正規表現、論理演算子サポート
8. **詳細レポート**: 失敗理由を明確に表示
9. **軽量**: Pythonパッケージ
10. **アクティブ開発**: 継続的な改善

## デメリット

### ❌ 制約・課題

1. **学習曲線**: Gherkin構文の習得必要
2. **terraform plan必須**: planファイル生成が前提
3. **静的解析のみ**: 実行時の問題は検出不可
4. **ドキュメント**: 公式ドキュメントが限定的
5. **IDE統合**: サポート限定的
6. **GUI不在**: コマンドラインのみ
7. **大規模ポリシー**: 管理が煩雑になる可能性
8. **エラーメッセージ**: 一部わかりにくい場合あり

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **tfsec** | セキュリティスキャン | Complianceより高速だがBDD非対応 |
| **Checkov** | マルチIaCセキュリティ | Complianceより包括的 |
| **Terraform Sentinel** | HashiCorp公式ポリシーエンジン | Complianceよりエンタープライズ向け |
| **OPA (Open Policy Agent)** | 汎用ポリシーエンジン | ComplianceよりRegoベース |
| **Regula** | OPAベースTerraformポリシー | Complianceと類似、Rego使用 |

## 公式リンク

- **GitHub**: [https://github.com/terraform-compliance/cli](https://github.com/terraform-compliance/cli)
- **ドキュメント**: [https://terraform-compliance.com/](https://terraform-compliance.com/)
- **PyPI**: [https://pypi.org/project/terraform-compliance/](https://pypi.org/project/terraform-compliance/)

## 関連ドキュメント

- [IaCセキュリティツール一覧](../IaCセキュリティツール/)
- [Terraform](../IaCツール/Terraform.md)
- [tfsec](./tfsec.md)
- [Terraform Validate](./Terraform_Validate.md)
- [Checkov](../セキュリティツール/Checkov.md)
- [Terraformベストプラクティス](../../best-practices/terraform.md)

---

**カテゴリ**: IaCセキュリティツール  
**対象工程**: インフラ構築、セキュリティ  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
