# AWS CloudFormation

## 概要

AWS CloudFormation は AWS リソースをテンプレートで定義し、スタックとして一括管理する IaC サービスである。AWS ネイティブに統合されており、インフラ変更の一貫性と監査性を確保しやすい。

## 料金

| プラン | 内容 |
|------|------|
| CloudFormation 本体 | 無料 |
| 補足 | 作成した AWS リソース利用料は別途発生 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| AWS ネイティブ | IAM、CloudTrail などと統合しやすい |
| スタック管理 | まとめて作成・更新・削除が可能 |
| 変更セット | 適用前に差分を確認できる |
| ドリフト検出 | 実環境とテンプレート差分を検知 |
| 再利用性 | ネストスタックで部品化可能 |

## 主な機能

### テンプレート機能

| 機能 | 説明 |
|------|------|
| YAML/JSON 定義 | リソースを宣言的に記述 |
| Parameters | 環境差分を入力値で吸収 |
| Outputs | 他スタック参照情報を出力 |
| Conditions | 条件付きリソース作成 |

### スタック運用機能

| 機能 | 説明 |
|------|------|
| 作成/更新/削除 | ライフサイクルを一元管理 |
| Change Sets | 変更内容を事前確認 |
| Stack Policy | 重要リソースの更新制御 |
| Rollback | 失敗時の自動復旧 |

### ガバナンス機能

| 機能 | 説明 |
|------|------|
| Drift Detection | 手動変更の検出 |
| IAM 制御 | 操作権限を厳密に管理 |
| CloudTrail 監査 | 変更履歴を追跡 |
| Guard 連携 | 事前ポリシーチェック |

## インストールとセットアップ

公式URL:
- [CloudFormation 公式](https://aws.amazon.com/cloudformation/)
- [CloudFormation Docs](https://docs.aws.amazon.com/cloudformation/)
- [AWS CLI](https://docs.aws.amazon.com/cli/)

セットアップの要点:
1. AWS CLI と認証情報を設定する。
2. テンプレート、パラメータ、環境別設定の管理方針を決める。
3. スタック命名規則とタグ戦略を統一する。

## 基本的な使い方

1. まず最小テンプレートで VPC や S3 など基盤リソースを定義する。
2. `validate-template` で構文を確認する。
3. 変更時は Change Set で差分を確認してから適用する。
4. 定期的に Drift Detection を実行し、手動変更を検知する。

最小コマンド:
- 検証: `aws cloudformation validate-template --template-body file://template.yaml`
- デプロイ: `aws cloudformation deploy --template-file template.yaml --stack-name sample`

## メリット

- AWS サービスとの統合が強く運用しやすい
- スタック単位で変更を追跡しやすい
- 監査・権限管理を組み込みやすい
- 失敗時ロールバックで安全性を確保しやすい

## デメリット

- AWS 専用でマルチクラウドには向かない
- テンプレートが大規模化すると可読性が下がりやすい
- 依存関係設計が不十分だと更新が複雑になる

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| AWS CloudFormation | AWS IaC | AWS ネイティブ統合が強い |
| Terraform | マルチクラウド IaC | プロバイダ横断で管理可能 |
| AWS CDK | AWS IaC | プログラミング言語で定義可能 |
| Azure Bicep | Azure IaC | Azure ネイティブ管理に強い |

## ベストプラクティス

### 1. テンプレートを分割

- ネストスタックで責務ごとに分割する
- 共通部品を再利用して重複を減らす

### 2. 変更前レビューを徹底

- Change Set を必須化する
- 重要スタックは承認フローを入れる

### 3. 手動変更を抑制

- Drift Detection を定期実行する
- 手動修正時はテンプレートへ即時反映する

## 公式ドキュメント

- 公式サイト: https://aws.amazon.com/cloudformation/
- ドキュメント: https://docs.aws.amazon.com/cloudformation/
- AWS CLI: https://docs.aws.amazon.com/cli/

## まとめ

1. ** 統合管理 ** : AWS 環境の構成をネイティブに管理する IaC サービスである。
2. ** 監査性 ** : スタック単位で変更を追跡し、監査性を高めやすい。
3. ** 安全性 ** : 変更セットとロールバックにより安全な運用を実現しやすい。
