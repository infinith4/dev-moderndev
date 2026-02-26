# 開発工程_4_基本設計（インフラ）

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. ネットワーク設計](#2-ネットワーク設計)
- [3. サーバー・コンピュート設計](#3-サーバーコンピュート設計)
- [4. ストレージ設計](#4-ストレージ設計)
- [5. セキュリティ設計](#5-セキュリティ設計)
- [6. 可用性・冗長性設計](#6-可用性冗長性設計)
- [7. 監視・運用設計](#7-監視運用設計)
- [8. 参考資料](#8-参考資料)

## 1. 概要

基本設計（インフラ）のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- インフラ基本設計
- 非機能要件の具体化（性能・可用性・運用性・セキュリティ）
- 設計成果物の作成・レビュー

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [非機能要求グレード（IPA）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | 可用性・性能・運用性・保守性・セキュリティ要件の整理 |
| [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/) | Azure向け設計パターン、参照アーキテクチャ確認 |
| [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) | クラウド設計原則、設計レビュー観点の統一 |

---

## 2. ネットワーク設計
**成果物**
- ネットワーク構成図
- サブネット/CIDR設計書
- ルーティング/FWポリシー設計書

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | ネットワーク構成図、通信経路図の作成 | [詳細](./ツール/設計_モデリング/Draw.io.md) |
| [PlantUML](https://plantuml.com/) | ネットワーク構成をテキスト管理 | [詳細](./ツール/設計_モデリング/PlantUML.md) |
| [Terraform](https://www.terraform.io/) | ネットワーク構成のIaC定義 | [詳細](./ツール/IaC_インフラ管理/Terraform.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) | プライベートIPアドレス設計基準 |
| [Azure Virtual Network Documentation](https://learn.microsoft.com/azure/virtual-network/) | Azure VNet設計、接続設計 |
| [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/) | VPC、サブネット、ルート設計 |

---

## 3. サーバー・コンピュート設計
**成果物**
- サーバー構成図
- インスタンス/VMサイジング表
- オートスケール方針書

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | サーバー構成図、構成パターン図作成 | [詳細](./ツール/設計_モデリング/Draw.io.md) |
| [Diagrams (Python)](https://diagrams.mingrammer.com/) | 構成図のコード化と再利用 | [詳細](./ツール/プロジェクト管理_ドキュメント/Diagrams.md) |
| [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) | Azure VM/サービス費用試算 | |
| [AWS Pricing Calculator](https://calculator.aws/) | インスタンス費用試算 | |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure VM Sizes](https://learn.microsoft.com/azure/virtual-machines/sizes) | VMサイズ選定 |
| [AWS EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/) | インスタンスタイプ選定 |

---

## 4. ストレージ設計
**成果物**
- ストレージ構成図
- 容量計画書
- バックアップ/保持ポリシー

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Draw.io](https://www.diagrams.net/) | ストレージ構成図作成 | 無料 | [詳細](./ツール/設計_モデリング/Draw.io.md) |
| [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) | 容量計画・コスト試算表の作成 | 無料枠あり | [詳細](./ツール/帳票_データ処理/Microsoft_Excel.md) |
| [Terraform](https://www.terraform.io/) | ストレージ構成のIaC定義 | 無料 | [詳細](./ツール/IaC_インフラ管理/Terraform.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure Storage Documentation](https://learn.microsoft.com/azure/storage/) | Azureストレージ設計 |
| [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/) | オブジェクトストレージ設計 |

---

## 5. セキュリティ設計
**成果物**
- セキュリティ設計書
- IAM/認可設計書
- 暗号化・鍵管理方針

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Microsoft Threat Modeling Tool](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling) | 脅威分析（STRIDE） | [詳細](./ツール/セキュリティ/Microsoft_Threat_Modeling_Tool.md) |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | セキュリティ要件チェックリスト | [詳細](./ツール/標準_ガイドライン/OWASP_ASVS.md) |
| [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) | ポリシーのコード化・検証 | [詳細](./ツール/IaC_インフラ管理/OPA.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) | セキュリティ設計観点の整理 |
| [Azure セキュリティ ドキュメント](https://learn.microsoft.com/ja-jp/azure/security/) | Azureの包括的なセキュリティ機能とベストプラクティスの参照 |
| [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/) | クラウドセキュリティ設計 |
| [IPA セキュリティセンター](https://www.ipa.go.jp/security/) | 国内標準に沿った設計指針 |

---

## 6. 可用性・冗長性設計
**成果物**
- 可用性設計書
- 冗長化構成図
- フェイルオーバー手順書

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Draw.io](https://www.diagrams.net/) | 冗長化・障害対策構成図作成 | 無料 | [詳細](./ツール/設計_モデリング/Draw.io.md) |
| [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) | SLA/SLO、RTO/RPO計画の整理 | 無料枠あり | [詳細](./ツール/帳票_データ処理/Microsoft_Excel.md) |
| [Terraform](https://www.terraform.io/) | 冗長構成のIaC実装設計 | 無料 | [詳細](./ツール/IaC_インフラ管理/Terraform.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Site Reliability Engineering Book](https://sre.google/sre-book/table-of-contents/) | 可用性・SLO設計の基礎 |
| [Azure Reliability Documentation](https://learn.microsoft.com/azure/reliability/) | Azure可用性設計の実装指針 |
| [AWS Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/) | 信頼性設計の標準観点 |

---

## 7. 監視・運用設計
**成果物**
- 運用設計書
- 監視設計書
- アラート定義書
- 運用手順書（Runbook）

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Prometheus](https://prometheus.io/) | メトリクス収集・監視設計 | 無料 | [詳細](./ツール/監視_ロギング/Prometheus.md) |
| [Grafana](https://grafana.com/) | ダッシュボード設計・可視化 | 無料枠あり | [詳細](./ツール/監視_ロギング/Grafana.md) |
| [Loki](https://grafana.com/oss/loki/) | ログ収集・分析設計 | 無料 | [詳細](./ツール/監視_ロギング/Loki.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Prometheus Best Practices](https://prometheus.io/docs/practices/) | メトリクス設計、アラート運用基準 |
| [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) | 運用手順、障害対応プロセス整備 |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | 運用品質特性の観点整理 |

---

## 8. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC/IEEE 12207:2017 / JIS X 0160:2012
- [非機能要求グレード（IPA）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html)
