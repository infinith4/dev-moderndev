# 開発工程_4_インフラ設計・構築

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**インフラ詳細設計およびインフラ構築プロセス**における開発タスクと推奨ツールをまとめたものです。

インフラ詳細設計では、基本設計で策定したインフラアーキテクチャを実装可能なレベルまで詳細化します。インフラ構築では、設計されたインフラストラクチャを Infrastructure as Code (IaC) を活用して実際に構築・プロビジョニングします。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 4. インフラ詳細設計

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

## Azure専用インフラ詳細設計ツール

Azureでのインフラ構築に特化したツール群です。Azure Resource Manager、Bicep、Azure Policy等を活用した詳細設計を支援します。

### Azure IaC・構成管理ツール（Top 10）

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

## AWS専用インフラ詳細設計ツール

AWSでのインフラ構築に特化したツール群です。CloudFormation、CDK、Service Catalog等を活用した詳細設計を支援します。

### AWS IaC・構成管理ツール（Top 10）

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

## 5. インフラ構築

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

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Terraform**](https://www.terraform.io/) | HashiCorp製マルチクラウドIaC。HCL言語、状態管理、モジュール化 | マルチクラウドインフラ構築、状態管理、モジュール再利用 | ✅ マルチクラウド対応<br>✅ 業界標準・実績豊富<br>✅ モジュール化・再利用容易<br>✅ 状態管理優秀<br>✅ プラン機能で事前確認 | ❌ 状態ファイル管理必要<br>❌ 学習曲線やや急<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料（Cloud） |
| 2 | [**AWS CloudFormation**](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。JSON/YAMLテンプレート、スタック管理 | AWSインフラ構築、スタック管理、ドリフト検出 | ✅ AWS完全統合<br>✅ 無料（AWS料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ AWS専用<br>❌ JSON/YAML冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る |
| 3 | [**Azure Bicep**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC DSL。ARM Templatesより簡潔、型安全 | Azureインフラ構築、リソースプロビジョニング、IaC | ✅ ARM Templatesより簡潔<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ モジュール化 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 4 | [**Ansible**](https://www.ansible.com/) | Red Hat製構成管理・自動化ツール。エージェントレス、YAML | サーバー構成管理、OS設定、ミドルウェア設定、デプロイ | ✅ エージェントレス<br>✅ YAML記述シンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ 無料オープンソース | ❌ 状態管理なし（べき等性は自己実装）<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 5 | [**Pulumi**](https://www.pulumi.com/) | プログラマブルIaC。TypeScript/Python/Go/C#、既存言語活用 | プログラマブルインフラ構築、既存言語でIaC、テスト容易 | ✅ 既存言語使用（TS/Python等）<br>✅ IDEサポート・補完<br>✅ テスト容易<br>✅ マルチクラウド対応<br>✅ 状態管理自動 | ❌ 比較的新しい（2018〜）<br>❌ Terraformより情報少ない<br>❌ 一部機能有料<br>❌ 言語依存性高い |
| 6 | [**AWS CDK**](https://aws.amazon.com/cdk/) | AWSプログラマブルIaC。TypeScript/Python/Java/C#、CloudFormation生成 | プログラマブルAWSインフラ構築、高レベル抽象化 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ CloudFormation自動生成<br>✅ IDE補完・型チェック<br>✅ 無料 | ❌ AWS専用<br>❌ CloudFormation依存<br>❌ 学習コストあり<br>❌ デバッグ難しい場合あり |
| 7 | [**Packer**](https://www.packer.io/) | HashiCorp製マシンイメージビルドツール。AMI、Docker、VM等 | マシンイメージ作成、AMI/コンテナビルド、イミュータブルインフラ | ✅ マルチプラットフォーム<br>✅ イミュータブルインフラ<br>✅ 並列ビルド<br>✅ プロビジョナー豊富<br>✅ 無料オープンソース | ❌ イメージビルド専用<br>❌ 状態管理なし<br>❌ 学習コストあり<br>❌ ビルド時間長い |
| 8 | [**Vagrant**](https://www.vagrantup.com/) | HashiCorp製開発環境構築ツール。VirtualBox/VMware/Docker対応 | ローカル開発環境構築、環境再現、チーム環境統一 | ✅ 開発環境統一<br>✅ シンプル設定<br>✅ プロビジョナー統合<br>✅ マルチプロバイダ<br>✅ 無料オープンソース | ❌ 本番環境不向き<br>❌ リソース使用量大<br>❌ ネットワーク設定複雑<br>❌ DockerComposeで代替可 |
| 9 | [**Chef**](https://www.chef.io/) | 構成管理ツール。Ruby DSL、インフラをコードで管理 | サーバー構成管理、コンプライアンス、自動化 | ✅ 大規模環境実績<br>✅ エンタープライズ機能<br>✅ コンプライアンス管理<br>✅ クラウド統合<br>✅ コミュニティ大きい | ❌ 学習曲線非常に急<br>❌ Ruby知識必要<br>❌ エージェント必要<br>❌ Ansibleより複雑 |
| 10 | [**SaltStack**](https://saltproject.io/) | Python製構成管理・リモート実行ツール。高速、スケーラブル | 大規模構成管理、リモート実行、イベント駆動 | ✅ 高速（ZeroMQ）<br>✅ スケーラブル<br>✅ リモート実行強力<br>✅ イベント駆動<br>✅ 無料オープンソース | ❌ 学習曲線急<br>❌ ドキュメント分かりにくい<br>❌ Ansibleより複雑<br>❌ エージェント推奨 |

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

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Azure Bicep**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure専用IaC DSL。実装からデプロイまで | Azureインフラ構築実装、リソースプロビジョニング | ✅ 簡潔な構文<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ デプロイ高速 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ 複雑な条件分岐弱い<br>❌ マルチクラウド不可 |
| 2 | [**Azure DevOps Pipelines**](https://azure.microsoft.com/ja-jp/products/devops/pipelines/) | CI/CDサービス。インフラデプロイ自動化 | Infrastructure Pipeline、CI/CD、自動デプロイ | ✅ Azure統合優秀<br>✅ YAML Pipeline<br>✅ 並列ジョブ<br>✅ マルチプラットフォーム<br>✅ 月1800分無料 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ GitHub Actions比で情報少ない<br>❌ 学習コスト高 |
| 3 | [**Azure CLI**](https://learn.microsoft.com/cli/azure/) | Azureコマンドライン。デプロイスクリプト作成 | Azure操作自動化、デプロイスクリプト、CI/CD統合 | ✅ 完全無料<br>✅ クロスプラットフォーム<br>✅ スクリプト化容易<br>✅ Cloud Shell統合<br>✅ 全Azureリソース対応 | ❌ 状態管理なし<br>❌ べき等性保証なし<br>❌ 大規模にはIaC推奨<br>❌ エラーハンドリング弱い |
| 4 | [**Azure Container Registry (ACR)**](https://azure.microsoft.com/ja-jp/products/container-registry/) | プライベートDockerレジストリ。イメージ管理 | Dockerイメージ管理、脆弱性スキャン、Geo-Replication | ✅ Azure統合<br>✅ 脆弱性スキャン<br>✅ Geo-Replication<br>✅ Webhooks<br>✅ タスク実行（ビルド） | ❌ Docker Hub比で高額<br>❌ 設定やや複雑<br>❌ 他クラウド連携弱い<br>❌ 一部機能有料版限定 |
| 5 | [**Azure Kubernetes Service (AKS)**](https://azure.microsoft.com/ja-jp/products/kubernetes-service/) | フルマネージドKubernetes。コンテナオーケストレーション | Kubernetesクラスタ構築、コンテナ運用、マイクロサービス | ✅ フルマネージド<br>✅ Azure統合優秀<br>✅ 自動アップグレード<br>✅ スケーリング自動<br>✅ 無料（ノード料金のみ） | ❌ Kubernetes学習必要<br>❌ 運用複雑<br>❌ コスト予測難しい<br>❌ トラブルシューティング困難 |
| 6 | [**ARM Templates**](https://learn.microsoft.com/azure/azure-resource-manager/templates/) | Azureネイティブ IaC。JSONテンプレート | Azureリソース実装、インフラデプロイ | ✅ Azure標準<br>✅ 全Azureリソース対応<br>✅ 無料<br>✅ デプロイ履歴追跡<br>✅ What-If機能 | ❌ JSON冗長<br>❌ Bicep推奨（後継）<br>❌ 学習曲線急<br>❌ エラーメッセージ分かりにくい |
| 7 | [**Azure Automation**](https://learn.microsoft.com/azure/automation/) | 運用自動化。Runbook実行、構成管理 | インフラ自動化タスク、定期実行、構成管理 | ✅ スケジュール実行<br>✅ PowerShell/Python対応<br>✅ State Configuration（DSC）<br>✅ 更新管理<br>✅ 無料枠あり | ❌ 従量課金<br>❌ デバッグ困難<br>❌ 実行時間制限<br>❌ Runbook管理煩雑 |
| 8 | [**Azure Monitor**](https://azure.microsoft.com/ja-jp/products/monitor/) | 統合監視サービス。メトリクス、ログ、アラート | インフラ監視、パフォーマンス監視、ログ分析 | ✅ Azure統合<br>✅ メトリクス・ログ統合<br>✅ Application Insights統合<br>✅ KQLクエリ<br>✅ アラート機能 | ❌ コスト高額<br>❌ ログ保持期間制限<br>❌ 学習コスト高<br>❌ 複雑なクエリ困難 |
| 9 | [**Azure Functions**](https://azure.microsoft.com/ja-jp/products/functions/) | サーバーレスコンピューティング。イベント駆動処理 | サーバーレスインフラ処理、イベント駆動、自動化タスク | ✅ サーバーレス<br>✅ 自動スケール<br>✅ 従量課金<br>✅ 多言語対応<br>✅ 無料枠充実 | ❌ コールドスタート遅延<br>❌ デバッグ困難<br>❌ ステートレス設計必要<br>❌ 実行時間制限 |
| 10 | [**Azure Resource Graph**](https://learn.microsoft.com/azure/governance/resource-graph/) | 大規模リソースクエリ。構築済みリソース分析 | リソース棚卸、構成確認、コンプライアンスチェック | ✅ 高速クエリ<br>✅ KQL強力<br>✅ 無料<br>✅ サブスクリプション横断<br>✅ API統合 | ❌ KQL学習必要<br>❌ リアルタイム性やや低い<br>❌ 複雑なクエリ困難<br>❌ 視覚化機能弱い |

---

## AWS専用インフラ構築ツール

AWSでのインフラ実装・構築に特化したツール群です。CloudFormation、CodePipeline、ECS/EKS等を活用した実装を支援します。

### AWS IaC実装・デプロイツール（Top 10）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**AWS CloudFormation**](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。スタック管理、デプロイ | AWSインフラ構築実装、スタック管理、デプロイ | ✅ AWS完全統合<br>✅ 無料（リソース料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ 学習曲線急<br>❌ AWS専用 |
| 2 | [**AWS CDK**](https://aws.amazon.com/cdk/) | プログラマブルIaC。既存言語でインフラ実装 | プログラマブルインフラ構築、CloudFormation生成 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ IDE補完・型チェック<br>✅ テスト容易<br>✅ 無料 | ❌ 学習曲線急<br>❌ CloudFormation依存<br>❌ デバッグ難しい場合あり<br>❌ AWS専用 |
| 3 | [**AWS CodePipeline**](https://aws.amazon.com/codepipeline/) | フルマネージドCI/CD。インフラデプロイ自動化 | CI/CD、インフラパイプライン、自動デプロイ | ✅ AWSサービス統合<br>✅ フルマネージド<br>✅ ビジュアルパイプライン<br>✅ 並列/連続実行<br>✅ 従量課金 | ❌ 設定複雑<br>❌ AWS依存<br>❌ デバッグ困難<br>❌ コスト予測難しい |
| 4 | [**AWS CodeBuild**](https://aws.amazon.com/codebuild/) | フルマネージドビルドサービス。コンテナビルド | CI/CD、ビルド、Dockerイメージビルド、テスト実行 | ✅ フルマネージド<br>✅ スケーラブル<br>✅ Docker対応<br>✅ 並列ビルド<br>✅ 従量課金 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ コスト予測難しい<br>❌ ローカル実行困難 |
| 5 | [**Amazon ECR**](https://aws.amazon.com/ecr/) | フルマネージドDockerレジストリ | Dockerイメージ管理、脆弱性スキャン、ECS/EKS統合 | ✅ AWS統合<br>✅ 脆弱性スキャン<br>✅ イメージ署名<br>✅ ライフサイクルポリシー<br>✅ IAM統合 | ❌ Docker Hub比で高額<br>❌ リージョン間転送コスト<br>❌ 設定やや複雑<br>❌ 他クラウド連携弱い |
| 6 | [**Amazon ECS**](https://aws.amazon.com/ecs/) | フルマネージドコンテナオーケストレーション | コンテナ運用、マイクロサービス、タスク実行 | ✅ フルマネージド<br>✅ Fargate統合<br>✅ AWS統合優秀<br>✅ スケーリング自動<br>✅ 無料（リソース料金のみ） | ❌ Kubernetes比で機能少<br>❌ AWS依存<br>❌ 学習曲線あり<br>❌ ECS独自概念 |
| 7 | [**Amazon EKS**](https://aws.amazon.com/eks/) | フルマネージドKubernetes | Kubernetesクラスタ構築、コンテナ運用 | ✅ Kubernetes標準<br>✅ フルマネージド<br>✅ AWS統合<br>✅ 自動アップグレード<br>✅ セキュリティ強化 | ❌ Kubernetes学習必要<br>❌ 運用複雑<br>❌ コントロールプレーン有料<br>❌ コスト高額 |
| 8 | [**AWS Systems Manager**](https://aws.amazon.com/systems-manager/) | 運用管理統合サービス。自動化、パッチ管理 | 運用自動化、パッチ管理、インベントリ管理 | ✅ 統合運用管理<br>✅ パラメータストア<br>✅ Session Manager<br>✅ Run Command<br>✅ 基本機能無料 | ❌ 機能多く複雑<br>❌ エージェント必要<br>❌ 学習コスト高<br>❌ 一部機能有料 |
| 9 | [**AWS Lambda**](https://aws.amazon.com/lambda/) | サーバーレスコンピューティング | サーバーレスインフラ処理、イベント駆動、自動化 | ✅ サーバーレス<br>✅ 自動スケール<br>✅ 従量課金<br>✅ 多言語対応<br>✅ 無料枠充実 | ❌ コールドスタート遅延<br>❌ デバッグ困難<br>❌ ステートレス設計必要<br>❌ 実行時間制限（15分） |
| 10 | [**Amazon CloudWatch**](https://aws.amazon.com/cloudwatch/) | 統合監視サービス。メトリクス、ログ、アラート | インフラ監視、ログ分析、メトリクス収集 | ✅ AWS統合<br>✅ メトリクス・ログ統合<br>✅ アラーム機能<br>✅ ダッシュボード<br>✅ Insights（ログ分析） | ❌ コスト高額<br>❌ ログ保持期間制限<br>❌ クエリ言語学習必要<br>❌ 複雑な分析困難 |

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

**関連ドキュメント**:
- [3. 基本設計（アプリケーション）](./dev_process_開発工程_3_基本設計_アプリケーション.md)
- [3. 基本設計（インフラ）](./dev_process_開発工程_3_基本設計_インフラ.md)
- [4. 詳細設計（アプリケーション）](./dev_process_開発工程_4_詳細設計_アプリケーション.md)
- [5. 実装（アプリケーション）](./dev_process_開発工程_5_実装_アプリケーション.md)
- [6. アプリケーションテスト](./dev_process_開発工程_6_アプリケーションテスト.md)
- [7. インフラテスト](./dev_process_開発工程_7_インフラテスト.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
