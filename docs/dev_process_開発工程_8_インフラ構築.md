# 開発工程_8_インフラ構築

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**インフラ構築プロセス**における開発タスクと推奨ツールをまとめたものです。

インフラ構築では、[開発工程_6_詳細設計_インフラ](docs/dev_process_開発工程_6_詳細設計_インフラ.md) によって設計されたインフラストラクチャを Infrastructure as Code (IaC) を活用して実際に構築・プロビジョニングします。

## 5. インフラ構築

実装フェーズでは、[開発工程_6_詳細設計_インフラ](docs/dev_process_開発工程_6_詳細設計_インフラ.md) で設計されたインフラストラクチャを実際に構築・プロビジョニングします。Infrastructure as Code (IaC) を活用した自動化、再現性、バージョン管理可能なインフラ構築が推奨されます。

### 主要タスク
- IaCコードの実装（Terraform、CloudFormation等）
- インフラのプロビジョニング・構築
- 環境構築の自動化
- 構成管理コードの実装（Ansible等）
- インフラCI/CDパイプラインの構築
- マシンイメージのビルド（AMI、コンテナイメージ等）
- ネットワーク・セキュリティグループの設定
- **IaCコードの検証・テスト**(構文チェック、ポリシー検証、セキュリティスキャン)

### 推奨ツール（マルチクラウド対応 Infrastructure as Code - Top 10）

**注**: Azure専用ツールは「Azure専用インフラ構築ツール」、AWS専用ツールは「AWS専用インフラ構築ツール」セクションを参照してください。

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Terraform**](https://www.terraform.io/) | HashiCorp製マルチクラウドIaC。HCL言語、状態管理、モジュール化 | マルチクラウドインフラ構築、状態管理、モジュール再利用 | ✅ マルチクラウド対応<br>✅ 業界標準・実績豊富<br>✅ モジュール化・再利用容易<br>✅ 状態管理優秀<br>✅ プラン機能で事前確認 | ❌ 状態ファイル管理必要<br>❌ 学習曲線やや急<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料(Cloud) |
| 2 | [**Ansible**](https://www.ansible.com/) | Red Hat製構成管理・自動化ツール。エージェントレス、YAML | サーバー構成管理、OS設定、ミドルウェア設定、デプロイ | ✅ エージェントレス<br>✅ YAML記述シンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ 無料オープンソース | ❌ 状態管理なし(べき等性は自己実装)<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 3 | [**Pulumi**](https://www.pulumi.com/) | プログラマブルIaC。TypeScript/Python/Go/C#、既存言語活用 | プログラマブルインフラ構築、既存言語でIaC、テスト容易 | ✅ 既存言語使用(TS/Python等)<br>✅ IDEサポート・補完<br>✅ テスト容易<br>✅ マルチクラウド対応<br>✅ 状態管理自動 | ❌ 比較的新しい(2018〜)<br>❌ Terraformより情報少ない<br>❌ 一部機能有料<br>❌ 言語依存性高い |
| 4 | [**Packer**](https://www.packer.io/) | HashiCorp製マシンイメージビルドツール。AMI、Docker、VM等 | マシンイメージ作成、AMI/コンテナビルド、イミュータブルインフラ | ✅ マルチプラットフォーム<br>✅ イミュータブルインフラ<br>✅ 並列ビルド<br>✅ プロビジョナー豊富<br>✅ 無料オープンソース | ❌ イメージビルド専用<br>❌ 状態管理なし<br>❌ 学習コストあり<br>❌ ビルド時間長い |
| 5 | [**Terragrunt**](https://terragrunt.gruntwork.io/) | Terraformラッパー。DRY原則、複数環境管理、リモートステート管理 | Terraform複数環境管理、コードDRY化、モジュール再利用 | ✅ Terraform DRY化<br>✅ 複数環境管理容易<br>✅ リモートステート自動設定<br>✅ 依存関係管理<br>✅ 無料オープンソース | ❌ Terraform知識前提<br>❌ 追加の学習コスト<br>❌ 複雑性増加<br>❌ デバッグやや困難 |
| 6 | [**Crossplane**](https://www.crossplane.io/) | CNCF製KubernetesベースIaC。マルチクラウドリソース管理 | Kubernetes経由でクラウドリソース管理、GitOps、宣言的管理 | ✅ Kubernetesネイティブ<br>✅ マルチクラウド対応<br>✅ GitOps統合<br>✅ CRDベース宣言的管理<br>✅ 無料オープンソース | ❌ Kubernetes必須<br>❌ 学習曲線非常に急<br>❌ 比較的新しい<br>❌ Terraformより情報少ない |
| 7 | [**Chef**](https://www.chef.io/) | 構成管理ツール。Ruby DSL、インフラをコードで管理 | サーバー構成管理、コンプライアンス、自動化 | ✅ 大規模環境実績<br>✅ エンタープライズ機能<br>✅ コンプライアンス管理<br>✅ クラウド統合<br>✅ コミュニティ大きい | ❌ 学習曲線非常に急<br>❌ Ruby知識必要<br>❌ エージェント必要<br>❌ Ansibleより複雑 |
| 8 | [**Puppet**](https://puppet.com/) | 構成管理ツール。宣言的DSL、エージェントベース、大規模環境向け | サーバー構成管理、コンプライアンス、エンタープライズ自動化 | ✅ 大規模環境実績<br>✅ エンタープライズ機能<br>✅ コンプライアンス強力<br>✅ レポート機能充実<br>✅ マルチプラットフォーム | ❌ 学習曲線非常に急<br>❌ エージェント必要<br>❌ セットアップ複雑<br>❌ Ansibleより複雑 |
| 9 | [**SaltStack**](https://saltproject.io/) | Python製構成管理・リモート実行ツール。高速、スケーラブル | 大規模構成管理、リモート実行、イベント駆動 | ✅ 高速(ZeroMQ)<br>✅ スケーラブル<br>✅ リモート実行強力<br>✅ イベント駆動<br>✅ 無料オープンソース | ❌ 学習曲線急<br>❌ ドキュメント分かりにくい<br>❌ Ansibleより複雑<br>❌ エージェント推奨 |
| 10 | [**Vagrant**](https://www.vagrantup.com/) | HashiCorp製開発環境構築ツール。VirtualBox/VMware/Docker対応 | ローカル開発環境構築、環境再現、チーム環境統一 | ✅ 開発環境統一<br>✅ シンプル設定<br>✅ プロビジョナー統合<br>✅ マルチプロバイダ<br>✅ 無料オープンソース | ❌ 本番環境不向き<br>❌ リソース使用量大<br>❌ ネットワーク設定複雑<br>❌ DockerComposeで代替可 |

---

## Azure専用インフラ構築ツール

Azureでのインフラ実装・構築に特化したIaCツール群です。Bicep、ARM Templates、Azure DevOps Pipelines等を活用したインフラコード実装を支援します。

### Azure IaC実装・デプロイツール（Top 6）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Azure Bicep**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure専用IaC DSL。実装からデプロイまで | Azureインフラ構築実装、リソースプロビジョニング | ✅ 簡潔な構文<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ デプロイ高速 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ 複雑な条件分岐弱い<br>❌ マルチクラウド不可 |
| 2 | [**ARM Templates**](https://learn.microsoft.com/azure/azure-resource-manager/templates/) | Azureネイティブ IaC。JSONテンプレート | Azureリソース実装、インフラデプロイ | ✅ Azure標準<br>✅ 全Azureリソース対応<br>✅ 無料<br>✅ デプロイ履歴追跡<br>✅ What-If機能 | ❌ JSON冗長<br>❌ Bicep推奨(後継)<br>❌ 学習曲線急<br>❌ エラーメッセージ分かりにくい |
| 3 | [**Azure DevOps Pipelines**](https://azure.microsoft.com/ja-jp/products/devops/pipelines/) | CI/CDサービス。インフラデプロイ自動化 | Infrastructure Pipeline、CI/CD、自動デプロイ | ✅ Azure統合優秀<br>✅ YAML Pipeline<br>✅ 並列ジョブ<br>✅ マルチプラットフォーム<br>✅ 月1800分無料 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ GitHub Actions比で情報少ない<br>❌ 学習コスト高 |
| 4 | [**Azure CLI**](https://learn.microsoft.com/cli/azure/) | Azureコマンドライン。デプロイスクリプト作成 | Azure操作自動化、デプロイスクリプト、CI/CD統合 | ✅ 完全無料<br>✅ クロスプラットフォーム<br>✅ スクリプト化容易<br>✅ Cloud Shell統合<br>✅ 全Azureリソース対応 | ❌ 状態管理なし<br>❌ べき等性保証なし<br>❌ 大規模にはIaC推奨<br>❌ エラーハンドリング弱い |
| 5 | [**Azure Automation**](https://learn.microsoft.com/azure/automation/) | 運用自動化。Runbook実行、構成管理 | インフラ自動化タスク、定期実行、構成管理 | ✅ スケジュール実行<br>✅ PowerShell/Python対応<br>✅ State Configuration(DSC)<br>✅ 更新管理<br>✅ 無料枠あり | ❌ 従量課金<br>❌ デバッグ困難<br>❌ 実行時間制限<br>❌ Runbook管理煩雑 |
| 6 | [**Azure Resource Graph**](https://learn.microsoft.com/azure/governance/resource-graph/) | 大規模リソースクエリ。構築済みリソース分析 | リソース棚卸、構成確認、コンプライアンスチェック | ✅ 高速クエリ<br>✅ KQL強力<br>✅ 無料<br>✅ サブスクリプション横断<br>✅ API統合 | ❌ KQL学習必要<br>❌ リアルタイム性やや低い<br>❌ 複雑なクエリ困難<br>❌ 視覚化機能弱い |

---

## AWS専用インフラ構築ツール

AWSでのインフラ実装・構築に特化したIaCツール群です。CloudFormation、CDK、CodePipeline等を活用したインフラコード実装を支援します。

### AWS IaC実装・デプロイツール（Top 5）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**AWS CloudFormation**](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。スタック管理、デプロイ | AWSインフラ構築実装、スタック管理、デプロイ | ✅ AWS完全統合<br>✅ 無料(リソース料金のみ)<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ 学習曲線急<br>❌ AWS専用 |
| 2 | [**AWS CDK**](https://aws.amazon.com/cdk/) | プログラマブルIaC。既存言語でインフラ実装 | プログラマブルインフラ構築、CloudFormation生成 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ IDE補完・型チェック<br>✅ テスト容易<br>✅ 無料 | ❌ 学習曲線急<br>❌ CloudFormation依存<br>❌ デバッグ難しい場合あり<br>❌ AWS専用 |
| 3 | [**AWS CodePipeline**](https://aws.amazon.com/codepipeline/) | フルマネージドCI/CD。インフラデプロイ自動化 | CI/CD、インフラパイプライン、自動デプロイ | ✅ AWSサービス統合<br>✅ フルマネージド<br>✅ ビジュアルパイプライン<br>✅ 並列/連続実行<br>✅ 従量課金 | ❌ 設定複雑<br>❌ AWS依存<br>❌ デバッグ困難<br>❌ コスト予測難しい |
| 4 | [**AWS CodeBuild**](https://aws.amazon.com/codebuild/) | フルマネージドビルドサービス。IaCビルド・テスト | CI/CD、ビルド、IaCテスト実行、検証 | ✅ フルマネージド<br>✅ スケーラブル<br>✅ Docker対応<br>✅ 並列ビルド<br>✅ 従量課金 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ コスト予測難しい<br>❌ ローカル実行困難 |
| 5 | [**AWS Systems Manager**](https://aws.amazon.com/systems-manager/) | 運用管理統合サービス。自動化、パッチ管理 | 運用自動化、パッチ管理、インベントリ管理 | ✅ 統合運用管理<br>✅ パラメータストア<br>✅ Session Manager<br>✅ Run Command<br>✅ 基本機能無料 | ❌ 機能多く複雑<br>❌ エージェント必要<br>❌ 学習コスト高<br>❌ 一部機能有料 |

---

## IPA公式資料・ガイド

| 資料名 | 概要 | 用途 | リンク |
|-------|------|------|--------|
| **クラウドセキュリティの歩き方** | クラウドの企画・実装・運用時のセキュリティ強化のためのガイドライン集約ポータル。国内外のガイドライン、クラウド事業者ホワイトペーパー、業界団体の文書を整理 | クラウドインフラセキュリティ設計、セキュリティ対策実装、コンプライアンス | [IPA公式サイト](https://www.ipa.go.jp/jinzai/ics/core_human_resource/final_project/2024/cloud-security.html) |
| **中小企業のためのクラウドサービス安全利用の手引き（2024年7月）** | クラウドサービスの安全な利用方法を解説。設定ミス防止、セキュリティ対策、インシデント対応を支援 | クラウド構築セキュリティ設定、設定ミス防止、セキュリティ基準策定 | [IPA公式サイト](https://www.ipa.go.jp/security/sme/f55m8k0000001wpl-att/outline_guidance_cloud.pdf) |
| **重要情報を扱うシステムの要求策定ガイド（2023年7月）** | 重要情報を扱うシステムの要求仕様策定を支援。クラウドサービス利用時の「自律性」と「利便性」のバランスを検討 | クラウドインフラ要件定義、セキュリティ要件策定、ガバナンス設計 | [IPA公式サイト](https://www.ipa.go.jp/digital/kaihatsu/system-youkyu.html) |
| **情報システムの信頼性向上に関するガイドライン（2012年6月）** | システムライフサイクルプロセスの管理手法を解説。運用・保守における信頼性向上を支援 | インフラ運用設計、監視設計、信頼性向上、障害対応プロセス | [IPA公式サイト](https://www.ipa.go.jp/archive/files/000004598.pdf) |
| **システム再構築を成功に導くユーザガイド 第2版（2018年2月）** | システム再構築・移行プロジェクトの成功要因を解説。移行計画、リスク管理を支援 | システム移行計画、インフラ移行、リスク管理、移行テスト | [IPA公式サイト](https://www.ipa.go.jp/sec/reports/20180226.html) |

---

## 5. CI/CD構築

## 10.0 IaCコード検証・テスト(事前チェック)

Azure Bicep や AWS CDK 等で記述されたIaCコードの品質・セキュリティを検証します。

### 対応項目
- IaCコード構文チェック
- セキュリティポリシー検証
- ベストプラクティス準拠チェック
- コスト見積もり

### 成果物
- IaCコード検証レポート
- セキュリティスキャン結果
- ポリシー準拠チェックリスト

### 推奨ツール(IaCテスト Top 10)

#### Azure (Bicep) 向けツール

| # | ツール名 | 概要 | 対象IaC | 料金 | メリット | デメリット |
|---|---------|------|---------|------|---------|-----------|
| 1 | [**Azure Bicep Linter**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Bicep公式リンター。ベストプラクティス準拠チェック | Azure Bicep | 🟢 完全無料(Bicep組込) | ✅ Bicep標準<br>✅ IDE統合(VSCode)<br>✅ リアルタイムエラー表示<br>✅ カスタムルール定義可<br>✅ ARM互換性検証 | ❌ Azure専用<br>❌ セキュリティチェック基本的<br>❌ ポリシー検証は別ツール必要<br>❌ 限定的ルールセット |
| 2 | [**Checkov**](https://www.checkov.io/) | Bridgecrew製IaCセキュリティスキャナー。1000+組込ポリシー | Terraform / CloudFormation / Bicep / CDK / K8s | 🟢 完全無料 | ✅ Bicep対応<br>✅ 組込ポリシー豊富<br>✅ CI/CD統合容易<br>✅ カスタムポリシー作成可<br>✅ SAST機能 | ❌ 誤検知やや多い<br>❌ ポリシーカスタマイズ複雑<br>❌ パフォーマンスやや遅い<br>❌ GUI なし |
| 3 | [**Azure Resource Manager Testing Toolkit (ARM-TTK)**](https://github.com/Azure/arm-ttk) | Azure公式ARM/Bicepテストツール | Azure Bicep / ARM | 🟢 完全無料 | ✅ Azure公式<br>✅ Bicep/ARM特化<br>✅ ベストプラクティス検証<br>✅ PowerShell統合 | ❌ Azure専用<br>❌ 機能限定的<br>❌ PowerShell必須 |
| 4 | [**OPA (Open Policy Agent)**](https://www.openpolicyagent.org/) | CNCF製汎用ポリシーエンジン。Regoでカスタムポリシー定義 | Terraform / K8s / CloudFormation / Bicep等 | 🟢 完全無料 | ✅ 柔軟なポリシー定義<br>✅ Azure Policy統合可<br>✅ Kubernetes標準<br>✅ CI/CD統合<br>✅ エンタープライズ実績 | ❌ Rego学習曲線急<br>❌ セットアップ複雑<br>❌ ポリシー記述手間<br>❌ 初心者には難しい |
| 5 | [**Terratest**](https://terratest.gruntwork.io/) | Go製インフラテストフレームワーク。実際にインフラを作成してテスト | Terraform / Packer / Docker / K8s / Bicep | 🟢 完全無料 | ✅ 実インフラテスト可能<br>✅ Azure対応<br>✅ 多様なIaC対応<br>✅ 統合テスト最適<br>✅ 並列実行対応 | ❌ Go言語必須<br>❌ 実行時間長い<br>❌ コスト発生(実インフラ作成)<br>❌ 学習曲線急 |
| 6 | [**tfsec**](https://aquasecurity.github.io/tfsec/) | Aqua製Terraformセキュリティスキャナー。高速・軽量 | Terraform (Azureプロバイダー) | 🟢 完全無料 | ✅ 高速実行<br>✅ Terraform専用最適化<br>✅ Azure特化ルールあり<br>✅ CI/CD統合容易<br>✅ JSON出力対応 | ❌ Terraform専用<br>❌ Bicep非対応<br>❌ GUI なし<br>❌ カスタムルール記述学習必要 |
| 7 | [**Terraform Validate**](https://www.terraform.io/) | Terraform公式構文チェックコマンド | Terraform (Azureプロバイダー) | 🟢 完全無料(Terraform組込) | ✅ Terraform標準<br>✅ 構文エラー即座検出<br>✅ 高速<br>✅ セットアップ不要<br>✅ AzureRMプロバイダースキーマ検証 | ❌ セキュリティチェックなし<br>❌ ベストプラクティス未検証<br>❌ 構文のみ検証<br>❌ カスタムルール不可 |
| 8 | [**Terraform Compliance**](https://terraform-compliance.com/) | TerraformコンプライアンステストツールBDD形式 | Terraform (Azureプロバイダー) | 🟢 完全無料 | ✅ BDD形式(Gherkin)<br>✅ 可読性高いテスト<br>✅ Azureポリシー定義可<br>✅ カスタムルール定義容易<br>✅ チーム共有しやすい | ❌ Terraform専用<br>❌ Bicep非対応<br>❌ コミュニティやや小<br>❌ 更新頻度低い |
| 9 | [**Infracost**](https://www.infracost.io/) | IaCコスト見積もりツール。Terraform/CloudFormation対応 | Terraform / CloudFormation / Pulumi | 🟢 無料プランあり / 💰 Pro: $50/月~ | ✅ Azure料金見積り<br>✅ PR差分コスト表示<br>✅ CI/CD統合<br>✅ ダッシュボード美しい<br>✅ 複数IaC対応 | ❌ 見積精度に限界<br>❌ 全Azureサービス非対応<br>❌ リアルタイム実コスト非表示<br>❌ 一部機能有料 |
| 10 | [**Pester**](https://pester.dev/) | PowerShell製テストフレームワーク。Azure/Windows環境テスト | PowerShell / Azure / Windows | 🟢 完全無料 | ✅ PowerShell標準<br>✅ Azure環境最適<br>✅ BDD形式<br>✅ モック機能<br>✅ ARM/Bicepテスト可 | ❌ PowerShell環境必須<br>❌ Linux環境やや弱い<br>❌ IaC専用ではない<br>❌ 学習曲線あり |

#### AWS (CDK/CloudFormation) 向けツール

| # | ツール名 | 概要 | 対象IaC | 料金 | メリット | デメリット |
|---|---------|------|---------|------|---------|-----------|
| 1 | [**CDK-nag**](https://github.com/cdklabs/cdk-nag) | AWS CDK向けベストプラクティスチェッカー | AWS CDK | 🟢 完全無料 | ✅ CDK専用最適化<br>✅ AWS Well-Architected準拠<br>✅ カスタムルール追加可<br>✅ CI/CD統合<br>✅ TypeScript/Python対応 | ❌ CDK専用<br>❌ CloudFormation非対応<br>❌ 実行時エラー検出のみ<br>❌ 情報やや少ない |
| 2 | [**CloudFormation Guard**](https://github.com/aws-cloudformation/cloudformation-guard) | AWS公式CloudFormationポリシー検証ツール | CloudFormation / CDK | 🟢 完全無料 | ✅ AWS公式<br>✅ カスタムルール定義<br>✅ JSON/YAML出力<br>✅ CI/CD統合<br>✅ CloudFormation特化 | ❌ CloudFormation専用<br>❌ Terraform非対応<br>❌ ルール記述やや複雑<br>❌ 情報・ドキュメント少ない |
| 3 | [**Checkov**](https://www.checkov.io/) | Bridgecrew製IaCセキュリティスキャナー。1000+組込ポリシー | Terraform / CloudFormation / Bicep / CDK / K8s | 🟢 完全無料 | ✅ CDK/CloudFormation対応<br>✅ 組込ポリシー豊富<br>✅ CI/CD統合容易<br>✅ カスタムポリシー作成可<br>✅ SAST機能 | ❌ 誤検知やや多い<br>❌ ポリシーカスタマイズ複雑<br>❌ パフォーマンスやや遅い<br>❌ GUI なし |
| 4 | [**AWS CDK Assertions**](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html) | AWS CDK公式テストライブラリ。スナップショットテスト | AWS CDK | 🟢 完全無料(CDK組込) | ✅ CDK公式<br>✅ TypeScript/Python対応<br>✅ スナップショットテスト<br>✅ 単体テスト最適<br>✅ Fine-Grained Assertions | ❌ CDK専用<br>❌ CloudFormation直接は不可<br>❌ 実インフラテスト不可<br>❌ セキュリティスキャン限定的 |
| 5 | [**OPA (Open Policy Agent)**](https://www.openpolicyagent.org/) | CNCF製汎用ポリシーエンジン。Regoでカスタムポリシー定義 | Terraform / K8s / CloudFormation等 | 🟢 完全無料 | ✅ 柔軟なポリシー定義<br>✅ AWS Service Control Policy統合可<br>✅ Kubernetes標準<br>✅ CI/CD統合<br>✅ エンタープライズ実績 | ❌ Rego学習曲線急<br>❌ セットアップ複雑<br>❌ ポリシー記述手間<br>❌ 初心者には難しい |
| 6 | [**Terratest**](https://terratest.gruntwork.io/) | Go製インフラテストフレームワーク。実際にインフラを作成してテスト | Terraform / Packer / Docker / K8s | 🟢 完全無料 | ✅ 実インフラテスト可能<br>✅ AWS対応充実<br>✅ 多様なIaC対応<br>✅ 統合テスト最適<br>✅ 並列実行対応 | ❌ Go言語必須<br>❌ 実行時間長い<br>❌ コスト発生(実インフラ作成)<br>❌ 学習曲線急 |
| 7 | [**tfsec**](https://aquasecurity.github.io/tfsec/) | Aqua製Terraformセキュリティスキャナー。高速・軽量 | Terraform (AWSプロバイダー) | 🟢 完全無料 | ✅ 高速実行<br>✅ Terraform専用最適化<br>✅ AWS特化ルール豊富<br>✅ CI/CD統合容易<br>✅ JSON出力対応 | ❌ Terraform専用<br>❌ CDK/CloudFormation非対応<br>❌ GUI なし<br>❌ カスタムルール記述学習必要 |
| 8 | [**Terraform Validate**](https://www.terraform.io/) | Terraform公式構文チェックコマンド | Terraform (AWSプロバイダー) | 🟢 完全無料(Terraform組込) | ✅ Terraform標準<br>✅ 構文エラー即座検出<br>✅ 高速<br>✅ セットアップ不要<br>✅ AWSプロバイダースキーマ検証 | ❌ セキュリティチェックなし<br>❌ ベストプラクティス未検証<br>❌ 構文のみ検証<br>❌ カスタムルール不可 |
| 9 | [**Terraform Compliance**](https://terraform-compliance.com/) | TerraformコンプライアンステストツールBDD形式 | Terraform (AWSプロバイダー) | 🟢 完全無料 | ✅ BDD形式(Gherkin)<br>✅ 可読性高いテスト<br>✅ AWSポリシー定義可<br>✅ カスタムルール定義容易<br>✅ チーム共有しやすい | ❌ Terraform専用<br>❌ CDK/CloudFormation非対応<br>❌ コミュニティやや小<br>❌ 更新頻度低い |
| 10 | [**Infracost**](https://www.infracost.io/) | IaCコスト見積もりツール。Terraform/CloudFormation対応 | Terraform / CloudFormation / Pulumi | 🟢 無料プランあり / 💰 Pro: $50/月~ | ✅ AWS料金見積り正確<br>✅ PR差分コスト表示<br>✅ CI/CD統合<br>✅ ダッシュボード美しい<br>✅ 複数IaC対応 | ❌ 見積精度に限界<br>❌ 全AWSサービス非対応<br>❌ リアルタイム実コスト非表示<br>❌ 一部機能有料 |


---

**関連ドキュメント**:
- [3. 基本設計（アプリケーション）](./dev_process_開発工程_3_基本設計_アプリケーション.md)
- [3. 基本設計（インフラ）](./dev_process_開発工程_3_基本設計_インフラ.md)
- [4. 詳細設計（アプリケーション）](./dev_process_開発工程_4_詳細設計_アプリケーション.md)
- [5. 実装（アプリケーション）](./dev_process_開発工程_5_実装_アプリケーション.md)
- [6. アプリケーションテスト](./dev_process_開発工程_6_アプリケーションテスト.md)
- [7. インフラテスト](./dev_process_開発工程_7_インフラテスト.md)

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
