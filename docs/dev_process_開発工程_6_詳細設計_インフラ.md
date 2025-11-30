# 開発工程_6_詳細設計_インフラ

## 1. 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**インフラ詳細設計およびインフラ構築プロセス**における開発タスクと推奨ツールをまとめたものです。

インフラ詳細設計では、基本設計で策定したインフラアーキテクチャを実装可能なレベルまで詳細化します。インフラ構築では、設計されたインフラストラクチャを Infrastructure as Code (IaC) を活用して実際に構築・プロビジョニングします。

---

## 2. インフラ詳細設計

インフラ詳細設計では、基本設計で策定したインフラアーキテクチャを実装可能なレベルまで詳細化します。

### 2.1. 主要タスク
- ネットワーク詳細設計（CIDR、サブネット、ルーティングテーブル）
- サーバー構成詳細設計（インスタンスサイズ、OS、ミドルウェア）
- セキュリティ詳細設計（セキュリティグループ、ファイアウォールルール、暗号化）
- ストレージ詳細設計（容量、IOPS、バックアップポリシー）
- バックアップ・DR詳細設計（RPO/RTO、復旧手順）
- 監視・運用詳細設計（メトリクス、アラート、ログ保持）
- パフォーマンス設計（スケーリング戦略、キャッシュ戦略）

### 2.2. 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Terraform**](https://www.terraform.io/) | IaCツール。詳細なリソース定義、状態管理、モジュール化 | インフラ詳細設計コード化、リソース定義、プロビジョニング | ✅ マルチクラウド対応<br>✅ 詳細なリソース定義<br>✅ 状態管理優秀<br>✅ モジュール再利用<br>✅ プラン機能で事前確認 | ❌ 学習曲線急<br>❌ 状態ファイル管理必要<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料 |
| 2 | [**AWS CloudFormation**](https://aws.amazon.com/cloudformation/) | AWS標準IaC。詳細なリソース定義、スタック管理 | AWSインフラ詳細設計、リソース定義、ドリフト検出 | ✅ AWS完全統合<br>✅ 無料<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ AWS専用<br>❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る |
| 3 | [**Azure Bicep**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC DSL。ARM Templatesより簡潔、型安全 | Azureインフラ詳細設計、リソース定義、IaC | ✅ 簡潔な構文<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ モジュール化 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 4 | [**Ansible**](https://www.ansible.com/) | 構成管理ツール。サーバー設定自動化、エージェントレス | サーバー構成詳細設計、OS設定、ミドルウェア設定 | ✅ エージェントレス<br>✅ YAML記述シンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ 無料オープンソース | ❌ 状態管理なし<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 5 | [**Lucidchart**](https://www.lucidchart.com/) | 詳細ネットワーク図作成。CIDR、サブネット、ルーティング図 | ネットワーク詳細設計図、サブネット設計、ルーティング図 | ✅ 詳細図作成可能<br>✅ AWS/Azureアイコン<br>✅ リアルタイム協業<br>✅ テンプレート<br>✅ Visio互換 | ❌ 有料（$7.95/月〜）<br>❌ オフライン不可<br>❌ IaC生成不可<br>❌ 実インフラ連携なし |
| 6 | [**Microsoft Visio**](https://www.microsoft.com/microsoft-365/visio/) | 詳細ネットワーク図・ラック図作成 | ネットワーク詳細設計図、ラック配置図、配線図、フロア図 | ✅ 詳細図作成に最適<br>✅ 豊富なステンシル<br>✅ データリンク機能<br>✅ Microsoft 365統合<br>✅ エンタープライズ標準 | ❌ 高額（$5〜15/月）<br>❌ Windows中心<br>❌ クラウド図作成は他ツール推奨<br>❌ 学習曲線急 |
| 7 | [**Palo Alto Expedition**](https://www.paloaltonetworks.com/) | ファイアウォール設計・移行ツール | セキュリティ詳細設計、ファイアウォールルール設計、ポリシー分析 | ✅ セキュリティポリシー分析<br>✅ ルール最適化<br>✅ 移行支援<br>✅ ベストプラクティス提案<br>✅ 無料 | ❌ Palo Alto専用<br>❌ セットアップ複雑<br>❌ 学習コスト高い<br>❌ 他ベンダーFW非対応 |
| 8 | [**AWS Well-Architected Tool**](https://aws.amazon.com/well-architected-tool/) | 詳細設計レビューツール。6つの柱評価 | アーキテクチャレビュー、詳細設計評価、改善提案 | ✅ 無料<br>✅ ベストプラクティス評価<br>✅ 改善提案自動生成<br>✅ レポート出力<br>✅ セキュリティ・パフォーマンス評価 | ❌ AWS専用<br>❌ 質問項目多数<br>❌ 全項目対応困難<br>❌ 実装は別途必要 |
| 9 | [**Checkov**](https://www.checkov.io/) | IaCセキュリティスキャンツール。Terraform/CloudFormation/Kubernetes対応 | IaCセキュリティレビュー、ポリシーチェック、ベストプラクティス検証 | ✅ 無料オープンソース<br>✅ 多IaC対応<br>✅ CI/CD統合<br>✅ カスタムポリシー<br>✅ 800+組込ポリシー | ❌ 誤検知あり<br>❌ ポリシーカスタマイズ複雑<br>❌ パフォーマンスやや遅い<br>❌ GUI なし |
| 10 | [**Infracost**](https://www.infracost.io/) | IaCコスト見積ツール。Terraform/CloudFormationコスト計算 | インフラコスト見積、予算管理、コスト最適化 | ✅ Terraform/CloudFormation対応<br>✅ CI/CD統合<br>✅ PR差分コスト表示<br>✅ 無料プランあり<br>✅ 詳細コスト内訳 | ❌ 見積精度に限界<br>❌ 全サービス非対応<br>❌ リアルタイムコストなし<br>❌ 一部機能有料 |

### 2.3. その他利用可能なツール

- Pulumi（プログラマブルIaC）
- AWS CDK（プログラマブルIaC）
- CloudCraft（インフラ図・コスト見積）
- draw.io（無料図作成）
- tfsec（Terraformセキュリティスキャン）
- Terragrunt（Terraform DRY化）
- OPA（Open Policy Agent - ポリシーエンジン）
- Sentinel（HashiCorp Policy as Code）

---

## 3. Azure専用インフラ詳細設計ツール

Azureでのインフラ構築に特化したツール群です。Azure Resource Manager、Bicep、Azure Policy等を活用した詳細設計を支援します。

### 3.1. Azure IaC・構成管理ツール（Top 10）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Azure Bicep**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure専用IaC DSL。ARM Templatesより簡潔で型安全 | Azureリソース定義、インフラ詳細設計、デプロイ自動化 | ✅ 簡潔な構文<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ モジュール化容易 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 2 | [**ARM Templates**](https://learn.microsoft.com/azure/azure-resource-manager/templates/) | Azureネイティブ IaC。JSON形式、宣言的デプロイ | Azureリソース定義、インフラコード化、テンプレート管理 | ✅ Azure標準<br>✅ 全Azureリソース対応<br>✅ 無料<br>✅ バージョン管理可能<br>✅ デプロイ履歴追跡 | ❌ JSON冗長<br>❌ 学習曲線急<br>❌ Bicep推奨（後継）<br>❌ エラーメッセージ分かりにくい |
| 3 | [**Azure Policy**](https://learn.microsoft.com/azure/governance/policy/) | ガバナンス・コンプライアンス管理。リソース制約定義 | コンプライアンス管理、リソースポリシー定義、監査 | ✅ コンプライアンス自動化<br>✅ 組み込みポリシー豊富<br>✅ カスタムポリシー定義可<br>✅ 無料<br>✅ リソース自動修復 | ❌ 学習コスト高<br>❌ 複雑なポリシー記述困難<br>❌ デバッグ難しい<br>❌ 誤設定でデプロイブロック |
| 4 | [**Azure Blueprints**](https://learn.microsoft.com/azure/governance/blueprints/) | 環境テンプレート管理。ARM、Policy、RBACを一括定義 | 環境標準化、コンプライアンス、マルチサブスクリプション管理 | ✅ 環境一括定義<br>✅ バージョン管理<br>✅ コンプライアンス強制<br>✅ 無料<br>✅ 標準化推進 | ❌ 機能複雑<br>❌ 学習コスト高<br>❌ 小規模環境には過剰<br>❌ デプロイ時間長い |
| 5 | [**Azure DevOps**](https://azure.microsoft.com/ja-jp/products/devops/) | CI/CD統合プラットフォーム。IaCコード管理・デプロイ自動化 | IaCコード管理、CI/CD、Infrastructure Pipeline | ✅ Azure統合優秀<br>✅ CI/CD強力<br>✅ 5ユーザーまで無料<br>✅ YAML Pipeline<br>✅ Git統合 | ❌ UI複雑<br>❌ 学習コスト高<br>❌ GitHub Actions比で情報少ない<br>❌ セットアップやや面倒 |
| 6 | [**Azure CLI**](https://learn.microsoft.com/cli/azure/) | Azureコマンドラインインターフェース。スクリプト自動化 | Azure操作自動化、スクリプト作成、リソース管理 | ✅ 完全無料<br>✅ クロスプラットフォーム<br>✅ スクリプト化容易<br>✅ 全Azureリソース対応<br>✅ Cloud Shell統合 | ❌ 状態管理なし<br>❌ 大規模環境にはIaC推奨<br>❌ エラーハンドリング弱い<br>❌ べき等性保証なし |
| 7 | [**Azure PowerShell**](https://learn.microsoft.com/powershell/azure/) | PowerShellモジュール。Windowsネイティブ自動化 | Windows環境での自動化、スクリプト作成、管理タスク | ✅ PowerShell統合<br>✅ Windows管理者に親和性高<br>✅ オブジェクト指向<br>✅ 無料<br>✅ Active Directory統合 | ❌ Windowsバイアス<br>❌ 学習曲線急（PowerShell）<br>❌ Linux環境では利点薄い<br>❌ IaC代替にはならない |
| 8 | [**Azure Resource Graph**](https://learn.microsoft.com/azure/governance/resource-graph/) | 大規模リソースクエリ。KQL言語で高速検索 | リソース棚卸、構成分析、コンプライアンスチェック | ✅ 高速クエリ（数千リソース）<br>✅ KQL強力<br>✅ 無料<br>✅ サブスクリプション横断検索<br>✅ API統合 | ❌ KQL学習必要<br>❌ 複雑なクエリ困難<br>❌ リアルタイム性やや低い<br>❌ 視覚化機能弱い |
| 9 | [**Azure Automation**](https://learn.microsoft.com/azure/automation/) | 運用自動化サービス。Runbook、構成管理、更新管理 | 定期タスク自動化、構成管理、パッチ管理 | ✅ スケジュール実行<br>✅ PowerShell/Python対応<br>✅ State Configuration（DSC）<br>✅ 更新管理統合<br>✅ 無料枠あり | ❌ 従量課金<br>❌ デバッグ困難<br>❌ 実行時間制限<br>❌ Runbook管理煩雑 |
| 10 | [**Azure Arc**](https://azure.microsoft.com/ja-jp/products/azure-arc/) | ハイブリッド・マルチクラウド管理。オンプレ・他クラウド統合管理 | ハイブリッドクラウド管理、オンプレサーバー管理、統合ガバナンス | ✅ ハイブリッド統合管理<br>✅ Azureポリシー適用可<br>✅ GitOps対応<br>✅ Kubernetes管理<br>✅ SQL Server管理 | ❌ 複雑な構成<br>❌ 学習コスト高<br>❌ 一部機能有料<br>❌ ネットワーク要件厳しい |

---

## 4. AWS専用インフラ詳細設計ツール

AWSでのインフラ構築に特化したツール群です。CloudFormation、CDK、Service Catalog等を活用した詳細設計を支援します。

### 4.1. AWS IaC・構成管理ツール（Top 10）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**AWS CloudFormation**](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。YAML/JSON、スタック管理 | AWSリソース定義、インフラ詳細設計、スタック管理 | ✅ AWS完全統合<br>✅ 無料（リソース料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る<br>❌ AWS専用 |
| 2 | [**AWS CDK**](https://aws.amazon.com/cdk/) | プログラマブルIaC。TypeScript/Python/Java/C#でCloudFormation生成 | プログラマブルインフラ定義、高レベル抽象化、IaC | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ IDE補完・型チェック<br>✅ CloudFormation自動生成<br>✅ 無料 | ❌ 学習曲線急<br>❌ CloudFormation依存<br>❌ デバッグ難しい場合あり<br>❌ AWS専用 |
| 3 | [**AWS CLI**](https://aws.amazon.com/cli/) | AWSコマンドラインインターフェース。スクリプト自動化 | AWS操作自動化、スクリプト作成、リソース管理 | ✅ 完全無料<br>✅ クロスプラットフォーム<br>✅ 全AWSサービス対応<br>✅ スクリプト化容易<br>✅ CloudShell統合 | ❌ 状態管理なし<br>❌ 大規模環境にはIaC推奨<br>❌ エラーハンドリング弱い<br>❌ べき等性保証なし |
| 4 | [**AWS Service Catalog**](https://aws.amazon.com/servicecatalog/) | ITサービスカタログ管理。承認済みリソーステンプレート配布 | インフラテンプレート管理、標準化、ガバナンス | ✅ インフラ標準化<br>✅ セルフサービス提供<br>✅ バージョン管理<br>✅ タグ強制<br>✅ 無料（リソース料金のみ） | ❌ 初期セットアップ複雑<br>❌ 学習コスト高<br>❌ 小規模には過剰<br>❌ UI改善余地 |
| 5 | [**AWS Config**](https://aws.amazon.com/config/) | リソース構成管理・監査。構成変更履歴、コンプライアンスチェック | 構成変更追跡、コンプライアンス監査、リソース棚卸 | ✅ 構成変更履歴記録<br>✅ コンプライアンスルール<br>✅ リソースリレーションシップ可視化<br>✅ 自動修復<br>✅ 他サービス統合 | ❌ 従量課金（やや高額）<br>❌ データ保持期間制限<br>❌ リアルタイム性低い<br>❌ ルール作成複雑 |
| 6 | [**AWS Systems Manager**](https://aws.amazon.com/systems-manager/) | 運用管理統合サービス。パッチ管理、構成管理、自動化 | 運用自動化、パッチ管理、インベントリ管理、Run Command | ✅ 統合運用管理<br>✅ エージェントベース<br>✅ パラメータストア<br>✅ Session Manager（SSH代替）<br>✅ 基本機能無料 | ❌ 機能多く複雑<br>❌ エージェント必要<br>❌ 学習コスト高<br>❌ 一部機能有料 |
| 7 | [**AWS Control Tower**](https://aws.amazon.com/controltower/) | マルチアカウント環境セットアップ・ガバナンス。ランディングゾーン自動構築 | マルチアカウント管理、ガバナンス、セキュリティベースライン | ✅ マルチアカウント自動化<br>✅ ガードレール（ガバナンス）<br>✅ アカウント自動プロビジョニング<br>✅ AWS Organizations統合<br>✅ 無料（リソース料金のみ） | ❌ 大規模組織向け<br>❌ 初期セットアップ時間かかる<br>❌ カスタマイズ制限<br>❌ 既存環境移行困難 |
| 8 | [**CloudFormation Designer**](https://aws.amazon.com/cloudformation/) | ビジュアルインフラ設計ツール。ドラッグ&ドロップ | インフラ構成図作成、CloudFormationテンプレート生成、視覚的設計 | ✅ ビジュアル設計<br>✅ CloudFormation自動生成<br>✅ 無料<br>✅ テンプレート可視化<br>✅ 初心者向け | ❌ 機能限定的<br>❌ 複雑な構成困難<br>❌ 手動編集推奨<br>❌ レイアウト自動調整弱い |
| 9 | [**AWS Application Composer**](https://aws.amazon.com/application-composer/) | サーバーレスアプリ視覚設計。Lambda、API Gateway等 | サーバーレス詳細設計、SAMテンプレート生成、視覚的設計 | ✅ サーバーレス特化<br>✅ ビジュアル設計<br>✅ SAM/CloudFormation生成<br>✅ リアルタイムプレビュー<br>✅ 無料 | ❌ サーバーレス限定<br>❌ 比較的新しい<br>❌ EC2等非対応<br>❌ 複雑なワークフロー困難 |
| 10 | [**AWS OpsWorks**](https://aws.amazon.com/opsworks/) | 構成管理サービス。Chef/Puppet統合 | 構成管理、アプリデプロイ、レイヤー管理 | ✅ Chef/Puppet統合<br>✅ レイヤー概念<br>✅ 自動スケーリング<br>✅ ライフサイクルイベント<br>✅ 無料（リソース料金のみ） | ❌ 学習曲線急<br>❌ 新規プロジェクト非推奨<br>❌ Systems Manager推奨（後継）<br>❌ コミュニティ縮小 |

---


## 5. バージョン管理（全言語共通）

| # | ツール名 | 概要 | メリット | デメリット |
|---|---------|------|---------|-----------|
| 1 | [**Git**](https://git-scm.com/) | 分散型バージョン管理システム。業界標準 | ✅ 業界標準<br>✅ 完全無料<br>✅ 分散型で高速<br>✅ ブランチ管理強力 | ❌ 学習曲線やや急<br>❌ GUI必要<br>❌ 大容量ファイル苦手 |
| 2 | [**GitHub**](https://github.com/) | 世界最大Gitホスティング。PR、CI/CD | ✅ 最大ユーザーベース<br>✅ PR・レビュー優秀<br>✅ Actions（CI/CD）<br>✅ Copilot等AI機能 | ❌ プライベートリポジトリ制限（無料）<br>❌ セルフホスト不可 |
| 3 | [**GitLab**](https://gitlab.com/) | DevOps統合プラットフォーム。CI/CD内蔵 | ✅ CI/CD完全統合<br>✅ セルフホスト可能<br>✅ DevSecOps機能<br>✅ 無料プラン充実 | ❌ UIやや複雑<br>❌ GitHubよりユーザー少 |


### 5.1. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012


**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
