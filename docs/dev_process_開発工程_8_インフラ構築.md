# 開発工程_8_インフラ構築

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. ネットワーク構築](#2-ネットワーク構築)
- [3. コンピュート構築](#3-コンピュート構築)
  - [3.1 Azure コンピュート構築](#31-azure-コンピュート構築)
  - [3.2 AWS コンピュート構築](#32-aws-コンピュート構築)
- [4. セキュリティ構築](#4-セキュリティ構築)
- [5. ストレージ・バックアップ構築](#5-ストレージバックアップ構築)
- [6. 監視・運用基盤構築](#6-監視運用基盤構築)
- [7. IaC検証・テスト](#7-iac検証テスト)
- [8. 参考資料](#8-参考資料)

## 1. 概要

インフラ構築のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- IaCコードの適用（`plan` / `apply` / `deploy`）
- クラウドリソースの構築・初期設定
- 構成管理と変更履歴管理
- 構築後の動作検証と運用引き渡し

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Terraform CLI Commands](https://developer.hashicorp.com/terraform/cli/commands) | `init/plan/apply` など構築時の基本コマンド確認 |
| [Azure Resource Manager documentation](https://learn.microsoft.com/azure/azure-resource-manager/) | Azureでのリソースデプロイと管理手順 |
| [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/) | AWSでのスタック作成・更新・ロールバック手順 |

---

## 2. ネットワーク構築
**成果物**
- ネットワーク実装済み構成図
- ルート/ACL/NSG設定定義
- 疎通確認レポート（疎通元/先、ポート、結果）

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Terraform](https://www.terraform.io/) | VNet/VPC/Subnet/Route/NSG等の一括構築 | [詳細](./ツール/IaC_インフラ管理/Terraform.md) |
| [Azure CLI](https://learn.microsoft.com/cli/azure/) | Azureネットワークリソースの作成・更新・確認 | [詳細](./ツール/CLI_運用管理/Azure_CLI.md) |
| [AWS CLI](https://aws.amazon.com/cli/) | AWSネットワークリソースの作成・更新・確認 | [詳細](./ツール/CLI_運用管理/AWS_CLI.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Quickstart: Create a virtual network using Azure portal](https://learn.microsoft.com/azure/virtual-network/quick-create-portal) | Azure VNetの初期構築手順 |
| [Getting started with Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-getting-started.html) | AWS VPCの初期構築手順 |
| [Azure Network Watcher documentation](https://learn.microsoft.com/azure/network-watcher/) | Azure疎通確認・診断手順 |

---

## 3. コンピュート構築
**成果物**
- コンピュート実装一覧（サービス名、リージョン、用途）
- スケーリング設定
- デプロイ実行ログ（適用日時、適用者、結果）

### 3.1 Azure コンピュート構築

| サービス | 用途 | 料金 |
|---------|------|------|
| [Azure Virtual Machines](https://azure.microsoft.com/products/virtual-machines/) | VM作成、拡張機能設定、起動確認 | 従量課金 |
| [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/products/kubernetes-service/) | クラスター作成、ノードプール設定、接続確認 | 従量課金 |
| [Azure Container Apps](https://azure.microsoft.com/products/container-apps/) | コンテナアプリ作成、リビジョン反映 | 従量課金 |
| [Azure Functions](https://azure.microsoft.com/products/functions/) | Function App作成、デプロイ反映 | 従量課金 |
| [Azure Batch](https://azure.microsoft.com/products/batch/) | Batchアカウント/プール/ジョブ作成 | 従量課金 |

### 3.2 AWS コンピュート構築

| サービス | 用途 | 料金 |
|---------|------|------|
| [Amazon EC2](https://aws.amazon.com/ec2/) | インスタンス作成、起動テンプレート設定、起動確認 | 従量課金 |
| [Amazon ECS](https://aws.amazon.com/ecs/) | クラスター/サービス作成、タスク定義反映 | 従量課金 |
| [Amazon EKS](https://aws.amazon.com/eks/) | クラスター作成、ノードグループ設定、接続確認 | 従量課金 |
| [AWS Lambda](https://aws.amazon.com/lambda/) | 関数作成、デプロイ、実行確認 | 従量課金 |
| [AWS Batch](https://aws.amazon.com/batch/) | Compute Environment/Queue/Job定義の構築 | 従量課金 |
| [AWS Fargate](https://aws.amazon.com/fargate/) | サーバーレスコンテナの実行基盤構築 | 従量課金 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Quickstart: Create a Linux virtual machine in Azure](https://learn.microsoft.com/azure/virtual-machines/linux/quick-create-portal) | Azure VMの構築手順 |
| [Deploy an Azure Kubernetes Service (AKS) cluster](https://learn.microsoft.com/azure/aks/learn/quick-kubernetes-deploy-cli) | AKS構築手順 |
| [Get started with Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html) | EC2構築手順 |
| [Getting started with Amazon ECS using Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html) | ECS/Fargate構築手順 |

---

## 4. セキュリティ構築
**成果物**
- セキュリティ設定反映結果（FW/NSG/SG）
- IAM/RBAC適用結果（ロール、権限範囲）
- セキュリティ検証レポート（検知事項、是正結果）

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Checkov](https://www.checkov.io/) | 適用前IaCセキュリティ検証 | [詳細](./ツール/セキュリティ/Checkov.md) |
| [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) | 構築設定のポリシー準拠チェック | [詳細](./ツール/IaC_インフラ管理/OPA.md) |
| [Trivy](https://trivy.dev/) | コンテナイメージ/設定の脆弱性スキャン | [詳細](./ツール/セキュリティ/Trivy.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure security baseline for Azure Virtual Machines](https://learn.microsoft.com/security/benchmark/azure/baselines/virtual-machines-security-baseline) | Azure VM構築時のセキュリティ設定基準 |
| [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html) | AWS構築時のセキュリティ実装基準 |
| [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) | OS/ミドルウェアのハードニング確認 |

---

## 5. ストレージ・バックアップ構築
**成果物**
- ストレージ作成結果（容量、冗長方式、暗号化設定）
- バックアップ設定定義（世代、保持期間、取得頻度）
- 復旧手順テスト結果（RTO/RPO達成可否）

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Terraform](https://www.terraform.io/) | ストレージ/バックアップ構成の適用 | [詳細](./ツール/IaC_インフラ管理/Terraform.md) |
| [AzCopy](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10) | Azureストレージへのデータ転送/初期投入 | [詳細](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10) |
| [AWS CLI](https://aws.amazon.com/cli/) | S3同期、ライフサイクル設定適用 |  |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure Storage documentation](https://learn.microsoft.com/azure/storage/) | Azureストレージ構築・運用手順 |
| [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html) | AWSバックアップ構築手順 |
| [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) | S3構築・データ保護設定 |

---

## 6. 監視・運用基盤構築
**成果物**
- 監視ダッシュボード（メトリクス/ログ）
- アラート設定（閾値、通知先、抑止条件）
- 運用Runbook（障害一次対応、復旧手順）

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Prometheus](https://prometheus.io/) | メトリクス収集とアラート基盤構築 | 無料 | [詳細](./ツール/監視_ロギング/Prometheus.md) |
| [Grafana](https://grafana.com/) | ダッシュボード・通知ルール構築 | 無料枠あり | [詳細](./ツール/監視_ロギング/Grafana.md) |
| [Loki](https://grafana.com/oss/loki/) | ログ収集/検索基盤構築 | 無料 | [詳細](./ツール/監視_ロギング/Loki.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) | 収集設定、ルール設定、運用構築 |
| [Grafana Alerting documentation](https://grafana.com/docs/grafana/latest/alerting/) | アラート設定の実装手順 |
| [Loki Documentation](https://grafana.com/docs/loki/latest/) | ログ収集基盤の構築手順 |

---

## 7. IaC検証・テスト
**成果物**
- IaC検証レポート
- セキュリティスキャン結果（重大度別）
- ポリシー準拠チェック結果（違反/是正）

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Terraform](https://www.terraform.io/) | `validate` / `plan` による適用前検証 | [詳細](./ツール/IaC_インフラ管理/Terraform.md) |
| [Azure Bicep Linter](https://learn.microsoft.com/azure/azure-resource-manager/bicep/linter) | Bicep構文・ベストプラクティスチェック |  |
| [CloudFormation Guard](https://github.com/aws-cloudformation/cloudformation-guard) | CloudFormationポリシー検証 | [詳細](./ツール/IaC_インフラ管理/CloudFormation_Guard.md) |
| [Checkov](https://www.checkov.io/) | IaCセキュリティスキャン | [詳細](./ツール/セキュリティ/Checkov.md) |
| [Terratest](https://terratest.gruntwork.io/) | 実環境インフラテスト | [詳細](./ツール/インフラテスト/Terratest.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Validate your Bicep files](https://learn.microsoft.com/azure/azure-resource-manager/bicep/linter) | Bicep適用前検証 |
| [Use AWS CloudFormation Guard](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html) | CloudFormationポリシー検証手順 |
| [Terraform Test](https://developer.hashicorp.com/terraform/language/tests) | Terraformテストと検証の実施方法 |

---

## 8. 参考資料
- [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf)
- [非機能要求グレード（IPA）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html)


