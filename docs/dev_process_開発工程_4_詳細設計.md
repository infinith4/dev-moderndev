# 開発工程_4_詳細設計

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**詳細設計プロセス**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 4.1 アプリケーション詳細設計

### 主要タスク
- モジュールの詳細設計
- インタフェースの詳細設計
- データ構造の詳細設計
- アルゴリズムの詳細設計
- API設計・定義

### 推奨ツール（モデリング・設計 Top 10）

基本設計と共通のツールを使用しますが、より詳細なレベルでの設計を行います。

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Enterprise Architect** | [https://sparxsystems.com/](https://sparxsystems.com/) | 多機能UMLモデリングツール。詳細設計からコード生成まで | クラス図、シーケンス図、状態遷移図、コード生成 | ✅ 詳細設計に最適<br>✅ コード生成・逆生成<br>✅ トレーサビリティ<br>✅ 多様な図に対応<br>✅ チーム開発対応 | ❌ 学習曲線非常に急<br>❌ UI複雑<br>❌ 機能過多<br>❌ 動作やや重い |
| 2 | **PlantUML** | [https://plantuml.com/](https://plantuml.com/) | テキストベースUML。Git管理、CI/CD統合に最適 | クラス図、シーケンス図、ER図、コンポーネント図 | ✅ テキストベース<br>✅ Git管理容易<br>✅ CI/CD統合<br>✅ 無料<br>✅ 差分管理容易 | ❌ GUI編集不可<br>❌ 記法学習必要<br>❌ 複雑な図困難<br>❌ レイアウト調整困難 |
| 3 | **Swagger/OpenAPI** | [https://swagger.io/](https://swagger.io/) | API設計・ドキュメント生成ツール。RESTful API定義標準 | REST API設計、API仕様書、インタラクティブドキュメント | ✅ API設計標準<br>✅ 自動ドキュメント生成<br>✅ モック生成<br>✅ コード生成<br>✅ 無料 | ❌ REST専用<br>❌ YAML記述やや複雑<br>❌ GraphQL非対応<br>❌ バージョン管理工夫必要 |
| 4 | **Postman** | [https://www.postman.com/](https://www.postman.com/) | API開発・テストプラットフォーム。設計・ドキュメント・テスト統合 | API設計、モックサーバー、API仕様書、コレクション管理 | ✅ API設計・テスト統合<br>✅ モックサーバー<br>✅ 自動ドキュメント<br>✅ チーム共有<br>✅ 無料プランあり | ❌ 無料版機能制限<br>❌ バージョン管理やや弱い<br>❌ 大規模では有料必須<br>❌ オフライン機能限定的 |
| 5 | **dbdiagram.io** | [https://dbdiagram.io/](https://dbdiagram.io/) | データベース設計ツール。ER図作成、SQL生成 | ER図作成、データベーススキーマ設計、DDL生成 | ✅ シンプルで使いやすい<br>✅ テキストベース<br>✅ SQL自動生成<br>✅ 共有容易<br>✅ 無料プランあり | ❌ 機能基本的<br>❌ 複雑なDB設計困難<br>❌ バージョン管理弱い<br>❌ オフライン不可 |
| 6 | **MySQL Workbench** | [https://www.mysql.com/products/workbench/](https://www.mysql.com/products/workbench/) | MySQL公式DB設計・管理ツール。ER図、SQL開発、管理 | データベース設計、ER図、SQL開発、リバースエンジニアリング | ✅ MySQL公式<br>✅ 完全無料<br>✅ ER図作成<br>✅ リバースエンジニアリング<br>✅ SQL開発環境 | ❌ MySQL専用<br>❌ UI古め<br>❌ 動作やや重い<br>❌ 学習コストあり |
| 7 | **draw.io (diagrams.net)** | [https://www.diagrams.net/](https://www.diagrams.net/) | 汎用図作成ツール。クラス図、ER図、フローチャート | クラス図、ER図、フローチャート、コンポーネント図 | ✅ 完全無料<br>✅ 多様な図対応<br>✅ テンプレート豊富<br>✅ GitHub/Drive統合<br>✅ ブラウザ/デスクトップ | ❌ 専門ツール比で機能劣る<br>❌ コード生成不可<br>❌ コラボ機能弱い<br>❌ 大規模管理困難 |
| 8 | **Visual Paradigm** | [https://www.visual-paradigm.com/](https://www.visual-paradigm.com/) | 総合モデリングツール。UML、ER、BPMN、コード生成 | 詳細設計、クラス図、ER図、コード生成、リバースエンジニアリング | ✅ 多機能統合<br>✅ コード生成豊富<br>✅ データベース設計<br>✅ リバースエンジニアリング<br>✅ チーム開発 | ❌ 高額（$99/月〜）<br>❌ 機能過多で複雑<br>❌ 動作重い<br>❌ 学習コスト高 |
| 9 | **Mermaid** | [https://mermaid.js.org/](https://mermaid.js.org/) | JavaScriptダイアグラムライブラリ。Markdown統合、Git管理 | フローチャート、シーケンス図、クラス図、ER図（Markdown内） | ✅ Markdown統合<br>✅ Git管理容易<br>✅ 無料オープンソース<br>✅ GitHub対応<br>✅ 軽量 | ❌ 機能限定的<br>❌ 複雑な図困難<br>❌ レイアウト制御弱い<br>❌ エクスポート形式限定 |
| 10 | **Stoplight Studio** | [https://stoplight.io/](https://stoplight.io/) | API設計プラットフォーム。OpenAPI、モック、ドキュメント | API詳細設計、OpenAPI定義、モックサーバー、ドキュメント | ✅ API設計特化<br>✅ ビジュアルエディタ<br>✅ モックサーバー<br>✅ Git統合<br>✅ 無料プランあり | ❌ API設計以外不向き<br>❌ 有料プラン推奨<br>❌ 学習コストあり<br>❌ 大規模では高額 |

### その他利用可能なツール

- StarUML
- astah*
- Lucidchart
- Cacoo
- pgModeler (PostgreSQL)
- DBeaver
- ERDPlus
- QuickDBD

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

## クラウドサービス（Azure / AWS）

詳細設計フェーズでは、実装に近いレベルでのインフラ設計、API設計、データベース設計を行います。

### Azure サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Azure API Management** | [https://azure.microsoft.com/ja-jp/products/api-management/](https://azure.microsoft.com/ja-jp/products/api-management/) | フルマネージドAPIゲートウェイ。API設計、公開、管理、監視 | API設計・定義、API Gateway、開発者ポータル、APIドキュメント | ✅ 統合API管理<br>✅ 開発者ポータル自動生成<br>✅ OpenAPI統合<br>✅ ポリシー管理<br>✅ 分析・監視 | ❌ 高額（$50/月〜）<br>❌ 学習曲線急<br>❌ 小規模には過剰<br>❌ 設定複雑 |
| 2 | **Azure SQL Database** | [https://azure.microsoft.com/ja-jp/products/azure-sql/database/](https://azure.microsoft.com/ja-jp/products/azure-sql/database/) | フルマネージドSQL Serverデータベース。高可用性、自動バックアップ | データベース詳細設計、スキーマ設計、パフォーマンスチューニング | ✅ フルマネージド<br>✅ 自動バックアップ<br>✅ スケーリング自動<br>✅ 高可用性<br>✅ Azure統合 | ❌ SQL Server専用<br>❌ コスト予測難しい<br>❌ 一部機能制限<br>❌ ベンダーロックイン |
| 3 | **Azure Cosmos DB** | [https://azure.microsoft.com/ja-jp/products/cosmos-db/](https://azure.microsoft.com/ja-jp/products/cosmos-db/) | グローバル分散NoSQLデータベース。低レイテンシ、マルチモデル | NoSQLデータベース設計、グローバルアプリ、マルチリージョン | ✅ グローバル分散<br>✅ 低レイテンシ保証<br>✅ マルチモデル（Document/Key-Value/Graph）<br>✅ スケーラブル<br>✅ 無料枠あり | ❌ 高コスト<br>❌ 学習曲線急<br>❌ クエリ性能要注意<br>❌ トランザクション制限 |
| 4 | **Azure Bicep** | [https://learn.microsoft.com/azure/azure-resource-manager/bicep/](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | インフラコード定義DSL。ARM Templatesより簡潔 | インフラ詳細設計、リソース定義、IaC | ✅ 簡潔な構文<br>✅ 型安全<br>✅ IDE補完<br>✅ ARM自動変換<br>✅ 無料 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 5 | **Azure Virtual Network** | [https://azure.microsoft.com/ja-jp/products/virtual-network/](https://azure.microsoft.com/ja-jp/products/virtual-network/) | 仮想ネットワークサービス。サブネット、NSG、ルーティング | ネットワーク詳細設計、サブネット設計、セキュリティ設計 | ✅ 柔軟なネットワーク設計<br>✅ NSGでセキュリティ制御<br>✅ VPN/ExpressRoute接続<br>✅ ピアリング<br>✅ 無料（データ転送のみ課金） | ❌ 設定複雑<br>❌ トラブルシューティング困難<br>❌ IP枯渇リスク<br>❌ 設計ミスのコスト高 |

### AWS サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Amazon API Gateway** | [https://aws.amazon.com/api-gateway/](https://aws.amazon.com/api-gateway/) | フルマネージドAPIゲートウェイ。REST/HTTP/WebSocket API作成・公開 | API設計・定義、API Gateway、認証・認可、スロットリング | ✅ Lambda統合<br>✅ REST/HTTP/WebSocket対応<br>✅ 認証・認可統合<br>✅ スロットリング・キャッシュ<br>✅ 従量課金 | ❌ 学習曲線急<br>❌ コスト予測難しい<br>❌ デバッグ困難<br>❌ 制限多い |
| 2 | **Amazon RDS** | [https://aws.amazon.com/rds/](https://aws.amazon.com/rds/) | フルマネージドリレーショナルデータベース。MySQL/PostgreSQL/Oracle/SQL Server | データベース詳細設計、スキーマ設計、高可用性設計 | ✅ フルマネージド<br>✅ 自動バックアップ<br>✅ マルチAZ高可用性<br>✅ 複数DB選択可<br>✅ リードレプリカ | ❌ コスト高め<br>❌ 一部カスタマイズ制限<br>❌ ストレージ上限あり<br>❌ ベンダーロックイン |
| 3 | **Amazon DynamoDB** | [https://aws.amazon.com/dynamodb/](https://aws.amazon.com/dynamodb/) | フルマネージドNoSQLデータベース。ミリ秒レイテンシ、無制限スケール | NoSQLデータベース設計、高速アクセス、スケーラブル設計 | ✅ ミリ秒レイテンシ<br>✅ 無制限スケール<br>✅ フルマネージド<br>✅ Global Tables<br>✅ 無料枠あり | ❌ データモデリング難しい<br>❌ クエリ制限多い<br>❌ コスト予測難しい<br>❌ 移行困難 |
| 4 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | インフラコード定義。YAML/JSON、スタック管理 | インフラ詳細設計、リソース定義、IaC、ドリフト検出 | ✅ AWS標準IaC<br>✅ 無料（リソース料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet<br>✅ スタック管理 | ❌ YAML/JSON冗長<br>❌ エラー対応困難<br>❌ Terraform比で機能劣る<br>❌ AWS専用 |
| 5 | **Amazon VPC** | [https://aws.amazon.com/vpc/](https://aws.amazon.com/vpc/) | 仮想プライベートクラウド。ネットワーク分離、セキュリティ制御 | ネットワーク詳細設計、サブネット設計、セキュリティグループ設計 | ✅ 柔軟なネットワーク設計<br>✅ セキュリティグループ<br>✅ VPN/Direct Connect<br>✅ VPCピアリング<br>✅ 無料 | ❌ 設定複雑<br>❌ トラブルシューティング困難<br>❌ IP CIDR変更不可<br>❌ 設計ミスのコスト高 |
| 6 | **AWS AppSync** | [https://aws.amazon.com/appsync/](https://aws.amazon.com/appsync/) | フルマネージドGraphQL API。リアルタイムデータ同期、オフライン対応 | GraphQL API設計、リアルタイムアプリ、モバイルバックエンド | ✅ GraphQL対応<br>✅ リアルタイム同期<br>✅ オフライン対応<br>✅ Lambda統合<br>✅ DynamoDB Direct統合 | ❌ GraphQL学習必要<br>❌ コスト予測難しい<br>❌ デバッグ困難<br>❌ REST比で複雑 |

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
