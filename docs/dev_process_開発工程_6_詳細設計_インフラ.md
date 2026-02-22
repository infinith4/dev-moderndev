# 開発工程_6_詳細設計（インフラ）

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. ネットワーク詳細設計](#2-ネットワーク詳細設計)
- [3. コンピュート詳細設計](#3-コンピュート詳細設計)
  - [3.1 Azure コンピュート設計](#31-azure-コンピュート設計)
  - [3.2 AWS コンピュート設計](#32-aws-コンピュート設計)
- [4. セキュリティ詳細設計](#4-セキュリティ詳細設計)
- [5. ストレージ・バックアップ詳細設計](#5-ストレージバックアップ詳細設計)
- [6. 監視・運用詳細設計](#6-監視運用詳細設計)
- [7. IaC実装設計](#7-iac実装設計)
- [8. 参考資料](#8-参考資料)

## 1. 概要

詳細設計（インフラ）のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- インフラ詳細設計
- 非機能要件の設計反映
- IaCを前提とした実装可能レベルへの具体化

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [非機能要求グレード（IPA）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | 可用性・性能・運用性・セキュリティ要件の具体化 |
| [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/) | Azure向け設計パターン、詳細化指針 |
| [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) | 詳細設計レビュー観点の統一 |

---

## 2. ネットワーク詳細設計
**成果物**
- ネットワーク詳細構成図
- サブネット/CIDR設計書
- ルーティング・疎通制御設計書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | ネットワーク構成図・経路図作成 | 無料 |
| [PlantUML](https://plantuml.com/) | ネットワーク構成のテキスト管理 | 無料 |
| [Terraform](https://www.terraform.io/) | ネットワーク構成のIaC詳細定義 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) | プライベートアドレス設計基準 |
| [Azure Virtual Network Documentation](https://learn.microsoft.com/azure/virtual-network/) | Azure VNet詳細設計 |
| [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/) | VPC、サブネット、ルート詳細設計 |

---

## 3. コンピュート詳細設計
**成果物**
- コンピュート方式選定書（VM/コンテナ/サーバーレス/バッチ）
- サイジング設計書（CPU/メモリ/同時実行）
- スケーリング方針書（水平/垂直、自動スケール）
- 実行基盤別の設計書（Azure/AWS）

### 3.1 Azure コンピュート設計

| サービス | 用途 | 料金 |
|---------|------|------|
| [Azure Virtual Machines](https://azure.microsoft.com/products/virtual-machines/) | 汎用VM実行基盤（長時間実行、OS制御） | 従量課金 |
| [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/products/kubernetes-service/) | Kubernetes実行基盤 | 従量課金 |
| [Azure Container Apps](https://azure.microsoft.com/products/container-apps/) | サーバーレスコンテナ実行 | 従量課金 |
| [Azure Functions](https://azure.microsoft.com/products/functions/) | サーバーレス実行（イベント駆動） | 従量課金 |
| [Azure Batch](https://azure.microsoft.com/products/batch/) | 大規模バッチ処理実行 | 従量課金 |
| [Azure App Service](https://azure.microsoft.com/products/app-service/) | Web/API実行基盤（PaaS） | 従量課金 |

### 3.2 AWS コンピュート設計

| サービス | 用途 | 料金 |
|---------|------|------|
| [Amazon EC2](https://aws.amazon.com/ec2/) | 汎用VM実行基盤（長時間実行、細かなOS制御） | 従量課金 |
| [Amazon ECS](https://aws.amazon.com/ecs/) | コンテナオーケストレーション（マネージド運用） | 従量課金 |
| [Amazon EKS](https://aws.amazon.com/eks/) | Kubernetes実行基盤（標準K8s運用） | 従量課金 |
| [AWS Lambda](https://aws.amazon.com/lambda/) | サーバーレス実行（イベント駆動、短時間処理） | 従量課金 |
| [AWS Batch](https://aws.amazon.com/batch/) | バッチジョブ実行（キューイング、並列処理） | 従量課金 |
| [AWS Fargate](https://aws.amazon.com/fargate/) | サーバーレスコンテナ実行（ECS/EKS連携） | 従量課金 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure Compute Decision Tree](https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree) | Azureコンピュート選定（VM/AKS/Functions等） |
| [Azure VM Sizes](https://learn.microsoft.com/azure/virtual-machines/sizes) | Azure VMサイジング設計 |
| [AWS Compute Services Overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html) | AWSでのコンピュート方式選定（VM/コンテナ/サーバーレス） |
| [AWS EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/) | AWS VMサイジング設計 |

---

## 4. セキュリティ詳細設計
**成果物**
- セキュリティグループ/NSG設計書
- IAM/RBAC設計書
- 暗号化・鍵管理設計書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Microsoft Threat Modeling Tool](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling) | 脅威分析（STRIDE） | 無料 |
| [Checkov](https://www.checkov.io/) | IaCセキュリティポリシー検証 | 無料 |
| [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) | ポリシーのコード化・準拠チェック | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) | セキュリティ設計観点の整理 |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | セキュリティ要件の確認基準 |
| [IPA セキュリティセンター](https://www.ipa.go.jp/security/) | 国内標準に沿った設計指針 |

---

## 5. ストレージ・バックアップ詳細設計
**成果物**
- ストレージ詳細設計書
- バックアップ設計書
- DR（災害復旧）手順書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | ストレージ/バックアップ構成図作成 | 無料 |
| [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) | 容量計画、RPO/RTO整理 | 無料枠あり |
| [Terraform](https://www.terraform.io/) | ストレージ/バックアップ設定のIaC管理 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure Storage Documentation](https://learn.microsoft.com/azure/storage/) | Azureストレージ設計 |
| [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/) | オブジェクトストレージ設計 |

---

## 6. 監視・運用詳細設計
**成果物**
- 監視設計書
- アラート定義書
- 運用Runbook

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Prometheus](https://prometheus.io/) | メトリクス収集・監視設計 | 無料 |
| [Grafana](https://grafana.com/) | ダッシュボード設計・可視化 | 無料枠あり |
| [Loki](https://grafana.com/oss/loki/) | ログ収集・分析設計 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Prometheus Best Practices](https://prometheus.io/docs/practices/) | メトリクス設計、アラート運用基準 |
| [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) | 運用手順、障害対応プロセス整備 |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | 運用品質特性の観点整理 |

---

## 7. IaC実装設計
**成果物**
- IaCモジュール設計書
- ポリシー/Lintルール定義
- デプロイ手順書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Terraform](https://www.terraform.io/) | マルチクラウドIaC設計 |
| [Azure Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC設計 |
| [AWS CloudFormation](https://aws.amazon.com/cloudformation/) | AWS IaC設計 |
| [tflint](https://github.com/terraform-linters/tflint) | Terraform静的解析 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Terraform Documentation](https://developer.hashicorp.com/terraform/docs) | モジュール設計、state管理 |
| [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC設計指針 |
| [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) | AWSテンプレート設計指針 |

---

## 8. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- [非機能要求グレード（IPA）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html)
