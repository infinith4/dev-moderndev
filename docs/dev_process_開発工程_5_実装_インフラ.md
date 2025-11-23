# 開発工程_5_実装（インフラ）

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**実装プロセス（インフラ構築）**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 5.2 インフラ構築

実装フェーズでは、設計されたインフラストラクチャを実際に構築・プロビジョニングします。Infrastructure as Code (IaC) を活用した自動化、再現性、バージョン管理可能なインフラ構築が推奨されます。

### 主要タスク
- IaCコードの実装（Terraform、CloudFormation等）
- インフラのプロビジョニング・構築
- 環境構築の自動化
- 構成管理コードの実装（Ansible等）
- インフラCI/CDパイプラインの構築
- マシンイメージのビルド（AMI、コンテナイメージ等）
- ネットワーク・セキュリティグループの設定
- インフラコードのテスト

### 推奨ツール（Infrastructure as Code - Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Terraform** | [https://www.terraform.io/](https://www.terraform.io/) | HashiCorp製マルチクラウドIaC。HCL言語、状態管理、モジュール化 | マルチクラウドインフラ構築、状態管理、モジュール再利用 | ✅ マルチクラウド対応<br>✅ 業界標準・実績豊富<br>✅ モジュール化・再利用容易<br>✅ 状態管理優秀<br>✅ プラン機能で事前確認 | ❌ 状態ファイル管理必要<br>❌ 学習曲線やや急<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料（Cloud） |
| 2 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。JSON/YAMLテンプレート、スタック管理 | AWSインフラ構築、スタック管理、ドリフト検出 | ✅ AWS完全統合<br>✅ 無料（AWS料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ AWS専用<br>❌ JSON/YAML冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る |
| 3 | **Azure Bicep** | [https://learn.microsoft.com/azure/azure-resource-manager/bicep/](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC DSL。ARM Templatesより簡潔、型安全 | Azureインフラ構築、リソースプロビジョニング、IaC | ✅ ARM Templatesより簡潔<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ モジュール化 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 4 | **Ansible** | [https://www.ansible.com/](https://www.ansible.com/) | Red Hat製構成管理・自動化ツール。エージェントレス、YAML | サーバー構成管理、OS設定、ミドルウェア設定、デプロイ | ✅ エージェントレス<br>✅ YAML記述シンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ 無料オープンソース | ❌ 状態管理なし（べき等性は自己実装）<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 5 | **Pulumi** | [https://www.pulumi.com/](https://www.pulumi.com/) | プログラマブルIaC。TypeScript/Python/Go/C#、既存言語活用 | プログラマブルインフラ構築、既存言語でIaC、テスト容易 | ✅ 既存言語使用（TS/Python等）<br>✅ IDEサポート・補完<br>✅ テスト容易<br>✅ マルチクラウド対応<br>✅ 状態管理自動 | ❌ 比較的新しい（2018〜）<br>❌ Terraformより情報少ない<br>❌ 一部機能有料<br>❌ 言語依存性高い |
| 6 | **AWS CDK** | [https://aws.amazon.com/cdk/](https://aws.amazon.com/cdk/) | AWSプログラマブルIaC。TypeScript/Python/Java/C#、CloudFormation生成 | プログラマブルAWSインフラ構築、高レベル抽象化 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ CloudFormation自動生成<br>✅ IDE補完・型チェック<br>✅ 無料 | ❌ AWS専用<br>❌ CloudFormation依存<br>❌ 学習コストあり<br>❌ デバッグ難しい場合あり |
| 7 | **Packer** | [https://www.packer.io/](https://www.packer.io/) | HashiCorp製マシンイメージビルドツール。AMI、Docker、VM等 | マシンイメージ作成、AMI/コンテナビルド、イミュータブルインフラ | ✅ マルチプラットフォーム<br>✅ イミュータブルインフラ<br>✅ 並列ビルド<br>✅ プロビジョナー豊富<br>✅ 無料オープンソース | ❌ イメージビルド専用<br>❌ 状態管理なし<br>❌ 学習コストあり<br>❌ ビルド時間長い |
| 8 | **Vagrant** | [https://www.vagrantup.com/](https://www.vagrantup.com/) | HashiCorp製開発環境構築ツール。VirtualBox/VMware/Docker対応 | ローカル開発環境構築、環境再現、チーム環境統一 | ✅ 開発環境統一<br>✅ シンプル設定<br>✅ プロビジョナー統合<br>✅ マルチプロバイダ<br>✅ 無料オープンソース | ❌ 本番環境不向き<br>❌ リソース使用量大<br>❌ ネットワーク設定複雑<br>❌ DockerComposeで代替可 |
| 9 | **Chef** | [https://www.chef.io/](https://www.chef.io/) | 構成管理ツール。Ruby DSL、インフラをコードで管理 | サーバー構成管理、コンプライアンス、自動化 | ✅ 大規模環境実績<br>✅ エンタープライズ機能<br>✅ コンプライアンス管理<br>✅ クラウド統合<br>✅ コミュニティ大きい | ❌ 学習曲線非常に急<br>❌ Ruby知識必要<br>❌ エージェント必要<br>❌ Ansibleより複雑 |
| 10 | **SaltStack** | [https://saltproject.io/](https://saltproject.io/) | Python製構成管理・リモート実行ツール。高速、スケーラブル | 大規模構成管理、リモート実行、イベント駆動 | ✅ 高速（ZeroMQ）<br>✅ スケーラブル<br>✅ リモート実行強力<br>✅ イベント駆動<br>✅ 無料オープンソース | ❌ 学習曲線急<br>❌ ドキュメント分かりにくい<br>❌ Ansibleより複雑<br>❌ エージェント推奨 |

### その他利用可能なツール

- Terragrunt（Terraform DRY化）
- ARM Templates（Azure標準IaC）
- Google Cloud Deployment Manager（GCP IaC）
- Crossplane（Kubernetesベース IaC）
- Puppet（構成管理）
- CFEngine（構成管理）
- NixOS（宣言的Linux）

---

## Azure専用インフラ構築ツール

Azureでのインフラ実装・構築に特化したツール群です。Bicep、Azure DevOps Pipelines、Azure Container Registry等を活用した実装を支援します。

### Azure IaC実装・デプロイツール（Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Azure Bicep** | [https://learn.microsoft.com/azure/azure-resource-manager/bicep/](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure専用IaC DSL。実装からデプロイまで | Azureインフラ構築実装、リソースプロビジョニング | ✅ 簡潔な構文<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ デプロイ高速 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ 複雑な条件分岐弱い<br>❌ マルチクラウド不可 |
| 2 | **Azure DevOps Pipelines** | [https://azure.microsoft.com/ja-jp/products/devops/pipelines/](https://azure.microsoft.com/ja-jp/products/devops/pipelines/) | CI/CDサービス。インフラデプロイ自動化 | Infrastructure Pipeline、CI/CD、自動デプロイ | ✅ Azure統合優秀<br>✅ YAML Pipeline<br>✅ 並列ジョブ<br>✅ マルチプラットフォーム<br>✅ 月1800分無料 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ GitHub Actions比で情報少ない<br>❌ 学習コスト高 |
| 3 | **Azure CLI** | [https://learn.microsoft.com/cli/azure/](https://learn.microsoft.com/cli/azure/) | Azureコマンドライン。デプロイスクリプト作成 | Azure操作自動化、デプロイスクリプト、CI/CD統合 | ✅ 完全無料<br>✅ クロスプラットフォーム<br>✅ スクリプト化容易<br>✅ Cloud Shell統合<br>✅ 全Azureリソース対応 | ❌ 状態管理なし<br>❌ べき等性保証なし<br>❌ 大規模にはIaC推奨<br>❌ エラーハンドリング弱い |
| 4 | **Azure Container Registry (ACR)** | [https://azure.microsoft.com/ja-jp/products/container-registry/](https://azure.microsoft.com/ja-jp/products/container-registry/) | プライベートDockerレジストリ。イメージ管理 | Dockerイメージ管理、脆弱性スキャン、Geo-Replication | ✅ Azure統合<br>✅ 脆弱性スキャン<br>✅ Geo-Replication<br>✅ Webhooks<br>✅ タスク実行（ビルド） | ❌ Docker Hub比で高額<br>❌ 設定やや複雑<br>❌ 他クラウド連携弱い<br>❌ 一部機能有料版限定 |
| 5 | **Azure Kubernetes Service (AKS)** | [https://azure.microsoft.com/ja-jp/products/kubernetes-service/](https://azure.microsoft.com/ja-jp/products/kubernetes-service/) | フルマネージドKubernetes。コンテナオーケストレーション | Kubernetesクラスタ構築、コンテナ運用、マイクロサービス | ✅ フルマネージド<br>✅ Azure統合優秀<br>✅ 自動アップグレード<br>✅ スケーリング自動<br>✅ 無料（ノード料金のみ） | ❌ Kubernetes学習必要<br>❌ 運用複雑<br>❌ コスト予測難しい<br>❌ トラブルシューティング困難 |
| 6 | **Azure Resource Manager (ARM) Templates** | [https://learn.microsoft.com/azure/azure-resource-manager/templates/](https://learn.microsoft.com/azure/azure-resource-manager/templates/) | Azureネイティブ IaC。JSONテンプレート | Azureリソース実装、インフラデプロイ | ✅ Azure標準<br>✅ 全Azureリソース対応<br>✅ 無料<br>✅ デプロイ履歴追跡<br>✅ What-If機能 | ❌ JSON冗長<br>❌ Bicep推奨（後継）<br>❌ 学習曲線急<br>❌ エラーメッセージ分かりにくい |
| 7 | **Azure Automation** | [https://learn.microsoft.com/azure/automation/](https://learn.microsoft.com/azure/automation/) | 運用自動化。Runbook実行、構成管理 | インフラ自動化タスク、定期実行、構成管理 | ✅ スケジュール実行<br>✅ PowerShell/Python対応<br>✅ State Configuration（DSC）<br>✅ 更新管理<br>✅ 無料枠あり | ❌ 従量課金<br>❌ デバッグ困難<br>❌ 実行時間制限<br>❌ Runbook管理煩雑 |
| 8 | **Azure Monitor** | [https://azure.microsoft.com/ja-jp/products/monitor/](https://azure.microsoft.com/ja-jp/products/monitor/) | 統合監視サービス。メトリクス、ログ、アラート | インフラ監視、パフォーマンス監視、ログ分析 | ✅ Azure統合<br>✅ メトリクス・ログ統合<br>✅ Application Insights統合<br>✅ KQLクエリ<br>✅ アラート機能 | ❌ コスト高額<br>❌ ログ保持期間制限<br>❌ 学習コスト高<br>❌ 複雑なクエリ困難 |
| 9 | **Azure Functions** | [https://azure.microsoft.com/ja-jp/products/functions/](https://azure.microsoft.com/ja-jp/products/functions/) | サーバーレスコンピューティング。イベント駆動処理 | サーバーレスインフラ処理、イベント駆動、自動化タスク | ✅ サーバーレス<br>✅ 自動スケール<br>✅ 従量課金<br>✅ 多言語対応<br>✅ 無料枠充実 | ❌ コールドスタート遅延<br>❌ デバッグ困難<br>❌ ステートレス設計必要<br>❌ 実行時間制限 |
| 10 | **Azure Resource Graph** | [https://learn.microsoft.com/azure/governance/resource-graph/](https://learn.microsoft.com/azure/governance/resource-graph/) | 大規模リソースクエリ。構築済みリソース分析 | リソース棚卸、構成確認、コンプライアンスチェック | ✅ 高速クエリ<br>✅ KQL強力<br>✅ 無料<br>✅ サブスクリプション横断<br>✅ API統合 | ❌ KQL学習必要<br>❌ リアルタイム性やや低い<br>❌ 複雑なクエリ困難<br>❌ 視覚化機能弱い |

---

## AWS専用インフラ構築ツール

AWSでのインフラ実装・構築に特化したツール群です。CloudFormation、CodePipeline、ECS/EKS等を活用した実装を支援します。

### AWS IaC実装・デプロイツール（Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。スタック管理、デプロイ | AWSインフラ構築実装、スタック管理、デプロイ | ✅ AWS完全統合<br>✅ 無料（リソース料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ 学習曲線急<br>❌ AWS専用 |
| 2 | **AWS CDK (Cloud Development Kit)** | [https://aws.amazon.com/cdk/](https://aws.amazon.com/cdk/) | プログラマブルIaC。既存言語でインフラ実装 | プログラマブルインフラ構築、CloudFormation生成 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ IDE補完・型チェック<br>✅ テスト容易<br>✅ 無料 | ❌ 学習曲線急<br>❌ CloudFormation依存<br>❌ デバッグ難しい場合あり<br>❌ AWS専用 |
| 3 | **AWS CodePipeline** | [https://aws.amazon.com/codepipeline/](https://aws.amazon.com/codepipeline/) | フルマネージドCI/CD。インフラデプロイ自動化 | CI/CD、インフラパイプライン、自動デプロイ | ✅ AWSサービス統合<br>✅ フルマネージド<br>✅ ビジュアルパイプライン<br>✅ 並列/連続実行<br>✅ 従量課金 | ❌ 設定複雑<br>❌ AWS依存<br>❌ デバッグ困難<br>❌ コスト予測難しい |
| 4 | **AWS CodeBuild** | [https://aws.amazon.com/codebuild/](https://aws.amazon.com/codebuild/) | フルマネージドビルドサービス。コンテナビルド | CI/CD、ビルド、Dockerイメージビルド、テスト実行 | ✅ フルマネージド<br>✅ スケーラブル<br>✅ Docker対応<br>✅ 並列ビルド<br>✅ 従量課金 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ コスト予測難しい<br>❌ ローカル実行困難 |
| 5 | **Amazon ECR (Elastic Container Registry)** | [https://aws.amazon.com/ecr/](https://aws.amazon.com/ecr/) | フルマネージドDockerレジストリ | Dockerイメージ管理、脆弱性スキャン、ECS/EKS統合 | ✅ AWS統合<br>✅ 脆弱性スキャン<br>✅ イメージ署名<br>✅ ライフサイクルポリシー<br>✅ IAM統合 | ❌ Docker Hub比で高額<br>❌ リージョン間転送コスト<br>❌ 設定やや複雑<br>❌ 他クラウド連携弱い |
| 6 | **Amazon ECS (Elastic Container Service)** | [https://aws.amazon.com/ecs/](https://aws.amazon.com/ecs/) | フルマネージドコンテナオーケストレーション | コンテナ運用、マイクロサービス、タスク実行 | ✅ フルマネージド<br>✅ Fargate統合<br>✅ AWS統合優秀<br>✅ スケーリング自動<br>✅ 無料（リソース料金のみ） | ❌ Kubernetes比で機能少<br>❌ AWS依存<br>❌ 学習曲線あり<br>❌ ECS独自概念 |
| 7 | **Amazon EKS (Elastic Kubernetes Service)** | [https://aws.amazon.com/eks/](https://aws.amazon.com/eks/) | フルマネージドKubernetes | Kubernetesクラスタ構築、コンテナ運用 | ✅ Kubernetes標準<br>✅ フルマネージド<br>✅ AWS統合<br>✅ 自動アップグレード<br>✅ セキュリティ強化 | ❌ Kubernetes学習必要<br>❌ 運用複雑<br>❌ コントロールプレーン有料<br>❌ コスト高額 |
| 8 | **AWS Systems Manager** | [https://aws.amazon.com/systems-manager/](https://aws.amazon.com/systems-manager/) | 運用管理統合サービス。自動化、パッチ管理 | 運用自動化、パッチ管理、インベントリ管理 | ✅ 統合運用管理<br>✅ パラメータストア<br>✅ Session Manager<br>✅ Run Command<br>✅ 基本機能無料 | ❌ 機能多く複雑<br>❌ エージェント必要<br>❌ 学習コスト高<br>❌ 一部機能有料 |
| 9 | **AWS Lambda** | [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/) | サーバーレスコンピューティング | サーバーレスインフラ処理、イベント駆動、自動化 | ✅ サーバーレス<br>✅ 自動スケール<br>✅ 従量課金<br>✅ 多言語対応<br>✅ 無料枠充実 | ❌ コールドスタート遅延<br>❌ デバッグ困難<br>❌ ステートレス設計必要<br>❌ 実行時間制限（15分） |
| 10 | **AWS CloudWatch** | [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/) | 統合監視サービス。メトリクス、ログ、アラート | インフラ監視、ログ分析、メトリクス収集 | ✅ AWS統合<br>✅ メトリクス・ログ統合<br>✅ アラーム機能<br>✅ ダッシュボード<br>✅ Insights（ログ分析） | ❌ コスト高額<br>❌ ログ保持期間制限<br>❌ クエリ言語学習必要<br>❌ 複雑な分析困難 |

---

**関連ドキュメント**:
- [5. 実装（アプリケーション）](./dev_process_開発工程_5_実装_アプリケーション.md)
- [6. アプリケーションテスト](./dev_process_開発工程_6_アプリケーションテスト.md)
- [7. インフラテスト](./dev_process_開発工程_7_インフラテスト.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
