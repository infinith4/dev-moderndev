# 開発工程_10_テスト（インフラ）

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. インフラ単体テスト](#2-インフラ単体テスト)
- [3. インフラ結合テスト](#3-インフラ結合テスト)
- [4. インフラ総合・障害テスト](#4-インフラ総合障害テスト)
- [5. セキュリティ・コンプライアンステスト](#5-セキュリティコンプライアンステスト)
- [6. 性能・スケーラビリティテスト](#6-性能スケーラビリティテスト)
- [7. 監視・運用テスト](#7-監視運用テスト)
- [8. 参考資料](#8-参考資料)

## 1. 概要

テスト（インフラ）のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- IaC適用結果の検証
- ネットワーク/認証/ストレージの接続確認
- 障害復旧、バックアップ、運用手順の検証
- テスト結果の記録、是正、再実施

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [ISO/IEC/IEEE 29119 overview](https://www.softwaretestingstandards.org/iso-29119/) | インフラテスト成果物、管理観点の共通化 |
| [NIST SP 800-34 Rev.1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) | バックアップ/復旧テストの基準 |
| [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/) | 運用・信頼性・セキュリティ観点でのテスト観点整理 |
| [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) | 運用・信頼性・セキュリティ観点でのテスト観点整理 |

---

## 2. インフラ単体テスト
**成果物**
- 単体テスト仕様書
- リソース設定確認結果
- テスト実行レポート

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Terratest](https://terratest.gruntwork.io/) | IaCで作成したリソースの単体検証 | [詳細](./ツール/インフラテスト/Terratest.md) |
| [Pester](https://pester.dev/) | PowerShellベースの検証テスト | [詳細](./ツール/単体テスト/Pester.md) |
| [Goss](https://github.com/goss-org/goss) | サーバー設定値・サービス状態の検証 | |
| [ARM/Bicep テスト ツールキット (arm-ttk)](https://github.com/Azure/arm-ttk) | Azure ARM/Bicepテンプレート検証 | |
| [AWS CDK Assertions](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html) | AWS CDKテンプレート検証 | [詳細](./ツール/インフラテスト/AWS_CDK_Assertions.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Terratest Documentation](https://terratest.gruntwork.io/docs/) | テスト記述パターンと実行方法 |
| [Pester Documentation](https://pester.dev/docs/quick-start) | PowerShellテスト実装 |
| [ARM Template Test Toolkit](https://learn.microsoft.com/azure/azure-resource-manager/templates/test-toolkit) | Azureテンプレートの単体検証ルール確認 |
| [AWS CDK Testing Guide](https://docs.aws.amazon.com/cdk/v2/guide/testing.html) | CDK単体テスト設計 |

---

## 3. インフラ結合テスト
**成果物**
- 結合テスト仕様書
- 疎通確認結果
- 連携テスト結果レポート

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Azure CLI](https://learn.microsoft.com/cli/azure/) | Azureリソース連携確認 | [詳細](./ツール/CLI_運用管理/Azure_CLI.md) |
| [AWS CLI](https://aws.amazon.com/cli/) | AWSリソース連携確認 | |
| [InSpec](https://www.inspec.io/) | リソース状態、設定準拠の結合確認 | [詳細](./ツール/インフラテスト/InSpec.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Azure CLI Documentation](https://learn.microsoft.com/cli/azure/) | Azure接続性/設定確認の実施方法 |
| [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) | AWS接続性/設定確認の実施方法 |
| [InSpec Documentation](https://docs.chef.io/inspec/) | 構成検証コードの実装 |

---

## 4. インフラ総合・障害テスト
**成果物**
- 総合テスト計画書
- 障害注入テスト結果
- 復旧手順検証レポート

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Chaos Mesh](https://chaos-mesh.org/) | Kubernetes環境での障害注入テスト | [詳細](./ツール/インフラテスト/Chaos_Mesh.md) |
| [Litmus](https://litmuschaos.io/) | カオスエンジニアリングの実施 | [詳細](./ツール/インフラテスト/Litmus.md) |
| [k6](https://k6.io/) | 障害時のAPI応答劣化確認 | [詳細](./ツール/性能テスト/k6.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Principles of Chaos Engineering](https://principlesofchaos.org/) | 障害テスト設計の基本原則 |
| [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) | 障害対応手順、復旧訓練の設計 |
| [Litmus Docs](https://docs.litmuschaos.io/) | 障害注入シナリオの作成方法 |

---

## 5. セキュリティ・コンプライアンステスト
**成果物**
- セキュリティ検証レポート
- 脆弱性診断結果
- 準拠チェック結果

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Checkov](https://www.checkov.io/) | IaCセキュリティポリシー検証 | [詳細](./ツール/セキュリティ/Checkov.md) |
| [Trivy](https://trivy.dev/) | コンテナ/IaC脆弱性スキャン | [詳細](./ツール/セキュリティ/Trivy.md) |
| [OWASP ZAP](https://www.zaproxy.org/) | 公開エンドポイント脆弱性検証 | [詳細](./ツール/セキュリティ/OWASP_ZAP.md) |
| [CloudFormation Guard](https://github.com/aws-cloudformation/cloudformation-guard) | CloudFormationポリシー準拠検証 | [詳細](./ツール/IaC_インフラ管理/CloudFormation_Guard.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | 脆弱性観点の優先度整理 |
| [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) | セキュリティ評価観点の整理 |
| [Checkov Documentation](https://www.checkov.io/documentation.html) | CI組み込み、ルール適用方法 |

---

## 6. 性能・スケーラビリティテスト
**成果物**
- 負荷試験計画書
- 性能測定結果
- スケール試験レポート

| ツール名 | 用途 |
|---------|------|
| [Apache JMeter](https://jmeter.apache.org/) | 負荷・性能テスト実行 |
| [k6](https://k6.io/) | スクリプトベース性能試験 |
| [Locust](https://locust.io/) | 分散負荷試験 |
| [Prometheus](https://prometheus.io/) | テスト中メトリクス収集 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html) | シナリオ作成と結果分析 |
| [k6 Docs](https://grafana.com/docs/k6/latest/) | 負荷試験スクリプト実装 |
| [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) | 測定指標収集設定 |

---

## 7. 監視・運用テスト
**成果物**
- 監視テスト結果
- アラート試験結果
- 運用Runbook検証結果

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Grafana](https://grafana.com/) | テスト時可視化、しきい値確認 | 無料枠あり |
| [Loki](https://grafana.com/oss/loki/) | ログ収集/検索の運用試験 | 無料 |
| [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) | 通知経路、通知条件の検証 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Grafana Alerting documentation](https://grafana.com/docs/grafana/latest/alerting/) | アラート試験設計 |
| [Loki Documentation](https://grafana.com/docs/loki/latest/) | ログ運用試験の実装 |
| [Prometheus Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/) | 通知ルール/経路設定 |

---

## 8. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC/IEEE 12207:2017 / JIS X 0160:2012

