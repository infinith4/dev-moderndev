# Terraform

## 概要

Terraform は HashiCorp が提供する IaC ツールであり、クラウドや SaaS を宣言的に定義してプロビジョニングできる。プロバイダを通じて複数環境を統一管理しやすく、インフラ構築の再現性を高められる。

## 料金

| プラン | 内容 |
|------|------|
| Terraform CLI | 無料（BUSL 対象バージョンあり） |
| HCP Terraform / Terraform Enterprise | リモート実行・ガバナンス向け有料機能あり |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 宣言的 IaC | 望ましい状態を HCL で定義 |
| マルチクラウド | AWS/Azure/GCP など横断管理 |
| 状態管理 | state により差分を把握 |
| 実行計画 | 適用前に変更内容を確認 |
| モジュール化 | 再利用しやすい構成を作れる |

## 主な機能

### 定義機能

| 機能 | 説明 |
|------|------|
| Resource | 各種インフラを宣言的に定義 |
| Variable | 環境差分を入力化 |
| Output | 他工程への値受け渡し |
| Module | 共通構成を部品化 |

### 実行機能

| 機能 | 説明 |
|------|------|
| plan | 差分の可視化 |
| apply | 変更の反映 |
| destroy | リソース削除 |
| import | 既存リソース取り込み |

### 運用機能

| 機能 | 説明 |
|------|------|
| Backend | リモート state 管理 |
| Workspace | 環境分離 |
| Policy 連携 | Sentinel/OPA 等で統制 |
| Lint/Sec 連携 | tflint、tfsec、Checkov など |

## インストールとセットアップ

公式URL:
- [Terraform 公式](https://www.terraform.io/)
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/)

セットアップの要点:
1. Terraform CLI を導入する。
2. Backend（state 保管先）を最初に決める。
3. ディレクトリ構成を `modules` と `envs` で分離する。

## 基本的な使い方

1. プロバイダ設定と最小リソースを定義する。
2. `init` で初期化し、`validate` で構文確認する。
3. `plan` で差分を確認してから `apply` する。
4. 変更は Pull Request ベースでレビューし、state の整合性を維持する。

最小コマンド:
- 初期化: `terraform init`
- 差分確認: `terraform plan`
- 反映: `terraform apply`

## メリット

- マルチクラウドを共通方式で管理できる
- 差分ベースで安全に変更しやすい
- モジュールで再利用性を高めやすい
- 既存インフラも段階的に IaC 化しやすい

## デメリット

- state 管理設計が不十分だと事故につながりやすい
- 大規模化すると plan のレビュー負荷が増える
- プロバイダ更新による差分影響に注意が必要

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Terraform | マルチクラウド IaC | プロバイダ横断で統一管理 |
| AWS CloudFormation | AWS IaC | AWS ネイティブ統合に強い |
| Azure Bicep | Azure IaC | Azure に最適化 |
| Pulumi | IaC 全般 | 汎用言語で記述可能 |

## ベストプラクティス

### 1. state を厳格管理

- リモート Backend とロックを利用する
- state ファイルを直接編集しない

### 2. モジュール設計を標準化

- 入出力を最小化し責務を明確化する
- バージョン固定で破壊的変更を抑える

### 3. 反映前チェックを固定

- `fmt`、`validate`、`plan` を必須化する
- 重要変更は複数人レビューにする

## 公式ドキュメント

- 公式サイト: https://www.terraform.io/
- ドキュメント: https://developer.hashicorp.com/terraform/docs
- Registry: https://registry.terraform.io/

## まとめ

1. **統一管理** : 複数環境を統一的に管理しやすい IaC の中心ツールである。
2. **安全変更** : plan による差分確認とモジュール化で安全に変更を反映しやすい。
3. **汎用性** : マルチクラウドや標準化されたインフラ運用を進めたいチームに適している。
