# Azure Bicep

## 概要

Azure Bicep は Azure Resource Manager（ARM）の宣言的 IaC 言語である。ARM JSON より読みやすく書きやすい構文で Azure リソースを定義でき、Azure 環境の標準化と自動構築を進めやすい。

## 料金

| プラン | 内容 |
|------|------|
| Bicep 本体 | 無料 |
| 補足 | デプロイされる Azure リソース利用料は別途発生 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Azure ネイティブ | ARM と完全互換で運用可能 |
| シンプル構文 | ARM JSON より可読性が高い |
| モジュール化 | 再利用しやすい構成を作れる |
| 型サポート | VS Code 補完で記述ミスを減らしやすい |
| 宣言的管理 | 望ましい状態をコードで定義 |

## 主な機能

### テンプレート機能

| 機能 | 説明 |
|------|------|
| resource 定義 | Azure リソースを宣言的に記述 |
| parameters | 環境差分を外部入力化 |
| outputs | 生成値を他工程へ受け渡し |
| conditions | 条件付き展開を制御 |

### 再利用機能

| 機能 | 説明 |
|------|------|
| module | テンプレート部品化 |
| registry | モジュール配布と共有 |
| scopes | サブスク/RG/管理グループ単位で適用 |
| template specs | 共有テンプレートの版管理 |

### 運用機能

| 機能 | 説明 |
|------|------|
| what-if | 適用前差分を確認 |
| linter | 記述品質をチェック |
| ARM 変換 | JSON 変換で互換性維持 |
| Policy 連携 | 組織ルールと整合を取りやすい |

## インストールとセットアップ

公式URL:
- [Bicep 公式ドキュメント](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Bicep GitHub](https://github.com/Azure/bicep)
- [Azure CLI](https://learn.microsoft.com/cli/azure/)

セットアップの要点:
1. Azure CLI と Bicep ツールを準備する。
2. `modules` と `environments` の分割方針を決める。
3. パラメータファイルとシークレット管理方法を統一する。

## 基本的な使い方

1. まず最小構成の Bicep ファイルを作成する。
2. `build` や lint で構文品質を確認する。
3. `what-if` で差分確認してからデプロイする。
4. 共通部品は module 化して再利用する。

最小コマンド:
- 差分確認: `az deployment group what-if --resource-group rg-sample --template-file main.bicep`
- デプロイ: `az deployment group create --resource-group rg-sample --template-file main.bicep`

## メリット

- Azure との親和性が高く導入しやすい
- ARM JSON より保守しやすい
- モジュール化で大規模管理に対応しやすい
- 差分確認で安全に反映しやすい

## デメリット

- Azure 専用で他クラウドには直接使えない
- 大規模化するとモジュール設計が重要になる
- 組織ルール未整備だとテンプレートが乱立しやすい

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Azure Bicep | Azure IaC | ARM 互換で可読性が高い |
| Terraform | マルチクラウド IaC | 複数クラウドを統一管理しやすい |
| ARM Template | Azure IaC | 低レベル制御が可能だが冗長になりやすい |
| Pulumi | IaC 全般 | 汎用言語で記述可能 |

## ベストプラクティス

### 1. モジュール標準化

- ネットワーク、監視、セキュリティを部品化する
- バージョン管理で互換性を維持する

### 2. パラメータ管理を分離

- 環境差分は `*.bicepparam` へ切り出す
- シークレットは Key Vault 連携で管理する

### 3. 反映前チェックを固定

- `what-if` と lint を必須化する
- 変更レビュー手順を明文化する

## 公式ドキュメント

- 公式ドキュメント: https://learn.microsoft.com/azure/azure-resource-manager/bicep/
- GitHub: https://github.com/Azure/bicep
- Azure CLI: https://learn.microsoft.com/cli/azure/

## まとめ

Azure Bicep は Azure 環境の IaC を読みやすく安全に運用するための実践的な選択肢である。Azure 中心の開発・運用で標準化を進めたいチームに適している。
