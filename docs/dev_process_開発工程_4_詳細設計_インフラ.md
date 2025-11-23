# 開発工程_4_詳細設計（インフラ）

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**詳細設計プロセス（インフラ詳細設計）**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 4.2 インフラ詳細設計

インフラ詳細設計では、基本設計で策定したインフラアーキテクチャを実装可能なレベルまで詳細化します。

### 主要タスク
- ネットワーク詳細設計（CIDR、サブネット、ルーティングテーブル）
- サーバー構成詳細設計（インスタンスサイズ、OS、ミドルウェア）
- セキュリティ詳細設計（セキュリティグループ、ファイアウォールルール、暗号化）
- ストレージ詳細設計（容量、IOPS、バックアップポリシー）
- バックアップ・DR詳細設計（RPO/RTO、復旧手順）
- 監視・運用詳細設計（メトリクス、アラート、ログ保持）
- パフォーマンス設計（スケーリング戦略、キャッシュ戦略）

### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Terraform** | [https://www.terraform.io/](https://www.terraform.io/) | IaCツール。詳細なリソース定義、状態管理、モジュール化 | インフラ詳細設計コード化、リソース定義、プロビジョニング | ✅ マルチクラウド対応<br>✅ 詳細なリソース定義<br>✅ 状態管理優秀<br>✅ モジュール再利用<br>✅ プラン機能で事前確認 | ❌ 学習曲線急<br>❌ 状態ファイル管理必要<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料 |
| 2 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | AWS標準IaC。詳細なリソース定義、スタック管理 | AWSインフラ詳細設計、リソース定義、ドリフト検出 | ✅ AWS完全統合<br>✅ 無料<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ AWS専用<br>❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る |
| 3 | **Azure Bicep** | [https://learn.microsoft.com/azure/azure-resource-manager/bicep/](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC DSL。ARM Templatesより簡潔、型安全 | Azureインフラ詳細設計、リソース定義、IaC | ✅ 簡潔な構文<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ モジュール化 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 4 | **Ansible** | [https://www.ansible.com/](https://www.ansible.com/) | 構成管理ツール。サーバー設定自動化、エージェントレス | サーバー構成詳細設計、OS設定、ミドルウェア設定 | ✅ エージェントレス<br>✅ YAML記述シンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ 無料オープンソース | ❌ 状態管理なし<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 5 | **Lucidchart** | [https://www.lucidchart.com/](https://www.lucidchart.com/) | 詳細ネットワーク図作成。CIDR、サブネット、ルーティング図 | ネットワーク詳細設計図、サブネット設計、ルーティング図 | ✅ 詳細図作成可能<br>✅ AWS/Azureアイコン<br>✅ リアルタイム協業<br>✅ テンプレート<br>✅ Visio互換 | ❌ 有料（$7.95/月〜）<br>❌ オフライン不可<br>❌ IaC生成不可<br>❌ 実インフラ連携なし |
| 6 | **Microsoft Visio** | [https://www.microsoft.com/microsoft-365/visio/](https://www.microsoft.com/microsoft-365/visio/) | 詳細ネットワーク図・ラック図作成 | ネットワーク詳細設計図、ラック配置図、配線図、フロア図 | ✅ 詳細図作成に最適<br>✅ 豊富なステンシル<br>✅ データリンク機能<br>✅ Microsoft 365統合<br>✅ エンタープライズ標準 | ❌ 高額（$5〜15/月）<br>❌ Windows中心<br>❌ クラウド図作成は他ツール推奨<br>❌ 学習曲線急 |
| 7 | **Palo Alto Expedition** | [https://www.paloaltonetworks.com/](https://www.paloaltonetworks.com/) | ファイアウォール設計・移行ツール | セキュリティ詳細設計、ファイアウォールルール設計、ポリシー分析 | ✅ セキュリティポリシー分析<br>✅ ルール最適化<br>✅ 移行支援<br>✅ ベストプラクティス提案<br>✅ 無料 | ❌ Palo Alto専用<br>❌ セットアップ複雑<br>❌ 学習コスト高い<br>❌ 他ベンダーFW非対応 |
| 8 | **AWS Well-Architected Tool** | [https://aws.amazon.com/well-architected-tool/](https://aws.amazon.com/well-architected-tool/) | 詳細設計レビューツール。6つの柱評価 | アーキテクチャレビュー、詳細設計評価、改善提案 | ✅ 無料<br>✅ ベストプラクティス評価<br>✅ 改善提案自動生成<br>✅ レポート出力<br>✅ セキュリティ・パフォーマンス評価 | ❌ AWS専用<br>❌ 質問項目多数<br>❌ 全項目対応困難<br>❌ 実装は別途必要 |
| 9 | **Checkov** | [https://www.checkov.io/](https://www.checkov.io/) | IaCセキュリティスキャンツール。Terraform/CloudFormation/Kubernetes対応 | IaCセキュリティレビュー、ポリシーチェック、ベストプラクティス検証 | ✅ 無料オープンソース<br>✅ 多IaC対応<br>✅ CI/CD統合<br>✅ カスタムポリシー<br>✅ 800+組込ポリシー | ❌ 誤検知あり<br>❌ ポリシーカスタマイズ複雑<br>❌ パフォーマンスやや遅い<br>❌ GUI なし |
| 10 | **Infracost** | [https://www.infracost.io/](https://www.infracost.io/) | IaCコスト見積ツール。Terraform/CloudFormationコスト計算 | インフラコスト見積、予算管理、コスト最適化 | ✅ Terraform/CloudFormation対応<br>✅ CI/CD統合<br>✅ PR差分コスト表示<br>✅ 無料プランあり<br>✅ 詳細コスト内訳 | ❌ 見積精度に限界<br>❌ 全サービス非対応<br>❌ リアルタイムコストなし<br>❌ 一部機能有料 |

### その他利用可能なツール

- Pulumi（プログラマブルIaC）
- AWS CDK（プログラマブルIaC）
- CloudCraft（インフラ図・コスト見積）
- draw.io（無料図作成）
- tfsec（Terraformセキュリティスキャン）
- Terragrunt（Terraform DRY化）
- OPA（Open Policy Agent - ポリシーエンジン）
- Sentinel（HashiCorp Policy as Code）

---

**関連ドキュメント**:
- [4. 詳細設計（アプリケーション）](./dev_process_開発工程_4_詳細設計_アプリケーション.md)
- [5. 実装](./dev_process_開発工程_5_実装.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
