# 開発工程 8: 導入

> **参考**: IPA 共通フレーム2013
>
> この工程では、開発したシステムを本番環境へ移行し、安定的な運用を開始します。

## 概要

導入プロセスでは、以下の主要な活動を実施します：

- 移行計画の策定
- データ移行
- 本番環境へのデプロイ
- 運用開始
- 保守・運用体制の確立

---

## 8.1 移行プロセス

### 主要タスク
- 移行計画の策定
- 移行設計
- 移行プログラムの開発
- データ移行
- 移行テスト
- 本番移行

### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **Liquibase** | [https://www.liquibase.org/](https://www.liquibase.org/) | データベーススキーマ管理、バージョン管理、マイグレーション | ✅ DB変更履歴管理優秀<br>✅ ロールバック機能<br>✅ 多DB対応（MySQL/PostgreSQL/Oracle等）<br>✅ CI/CD統合<br>✅ 差分自動検出 | ❌ 複雑な変更は手動SQL必要<br>❌ 学習曲線やや急<br>❌ 大規模データ移行遅い<br>❌ 商用機能は有料 |
| 2 | **Flyway** | [https://flywaydb.org/](https://flywaydb.org/) | データベースマイグレーション、シンプル、信頼性高い | ✅ シンプルで学習容易<br>✅ SQL/Javaマイグレーション<br>✅ バージョン管理明確<br>✅ CI/CD統合容易<br>✅ 軽量高速 | ❌ ロールバック機能弱い（有料版）<br>❌ 複雑な移行には不向き<br>❌ NoSQL非対応<br>❌ GUI なし |
| 3 | **AWS Database Migration Service** | [https://aws.amazon.com/dms/](https://aws.amazon.com/dms/) | クラウドDBマイグレーション、最小ダウンタイム | ✅ 最小ダウンタイム移行<br>✅ 異種DB間移行対応<br>✅ 継続的レプリケーション<br>✅ スキーマ変換ツール統合<br>✅ フルマネージド | ❌ AWS依存<br>❌ コスト予測難しい<br>❌ 複雑な変換は手動<br>❌ パフォーマンス調整必要 |
| 4 | **Talend** | [https://www.talend.com/](https://www.talend.com/) | ETL/ELTツール、データ統合、データ移行 | ✅ GUI でETL設計<br>✅ 多様なデータソース対応<br>✅ データ品質管理<br>✅ ビッグデータ対応<br>✅ オープンソース版あり | ❌ 商用版高額<br>❌ リソース使用量大<br>❌ 学習コスト高い<br>❌ 複雑化しやすい |
| 5 | **Apache NiFi** | [https://nifi.apache.org/](https://nifi.apache.org/) | データフロー自動化、データ移行、リアルタイム処理 | ✅ ビジュアルデータフロー設計<br>✅ リアルタイムストリーミング<br>✅ 豊富なプロセッサ<br>✅ データプロビナンス追跡<br>✅ 無料オープンソース | ❌ リソース使用量大<br>❌ セットアップ複雑<br>❌ バッチ処理は他ツール推奨<br>❌ 学習曲線急 |
| 6 | **Informatica** | [https://www.informatica.com/](https://www.informatica.com/) | エンタープライズデータ統合、ETL、マスタデータ管理 | ✅ エンタープライズ級機能<br>✅ 多様なデータソース対応<br>✅ データ品質管理優秀<br>✅ AIデータ統合<br>✅ 大規模実績豊富 | ❌ 非常に高額<br>❌ 複雑で学習困難<br>❌ オーバースペック感<br>❌ ベンダーロックイン |
| 7 | **Pentaho Data Integration** | [https://www.hitachivantara.com/en-us/products/pentaho-platform/data-integration-analytics.html](https://www.hitachivantara.com/en-us/products/pentaho-platform/data-integration-analytics.html) | オープンソースETL、データ統合 | ✅ 無料オープンソース<br>✅ GUI でETL設計<br>✅ ビッグデータ対応<br>✅ コミュニティ大きい<br>✅ Java拡張可能 | ❌ エンタープライズ版は有料<br>❌ パフォーマンスやや劣る<br>❌ サポート限定的<br>❌ UI やや古い |
| 8 | **Airbyte** | [https://airbyte.com/](https://airbyte.com/) | オープンソースELT、API統合、データパイプライン | ✅ 豊富なコネクタ（300+）<br>✅ オープンソース<br>✅ API統合容易<br>✅ 増分同期対応<br>✅ セットアップ簡単 | ❌ 比較的新しい（2020〜）<br>❌ 変換機能弱い（dbt推奨）<br>❌ エンタープライズ機能有料<br>❌ 大規模では課題 |
| 9 | **Fivetran** | [https://www.fivetran.com/](https://www.fivetran.com/) | 自動データパイプライン、SaaS統合、メンテナンスフリー | ✅ 完全自動化<br>✅ メンテナンスフリー<br>✅ 豊富なコネクタ<br>✅ スキーマ変更自動対応<br>✅ 信頼性高い | ❌ 高額（従量課金）<br>❌ カスタマイズ性低い<br>❌ ベンダーロックイン<br>❌ 複雑な変換不可 |
| 10 | **dbt (data build tool)** | [https://www.getdbt.com/](https://www.getdbt.com/) | データ変換、分析エンジニアリング、SQLベース | ✅ SQLで変換記述<br>✅ バージョン管理容易<br>✅ テスト・ドキュメント自動化<br>✅ モジュール化・再利用<br>✅ オープンソース | ❌ データ抽出・ロード不可（ELTのT専用）<br>❌ SQL知識必須<br>❌ リアルタイム処理不可<br>❌ クラウド版は有料 |

### その他利用可能なツール

- Stitch
- Azure Data Factory
- Google DataFlow
- StreamSets
- Matillion

---

## 8.2 保守・運用プロセス

### 8.2.1 運用管理

#### 主要タスク
- システム監視
- ログ管理
- インシデント管理
- パフォーマンス管理

#### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **Datadog** | [https://www.datadoghq.com/](https://www.datadoghq.com/) | APM、インフラ監視、ログ管理、統合ダッシュボード | ✅ 統合監視プラットフォーム<br>✅ APM機能充実<br>✅ クラウド統合優秀<br>✅ ダッシュボード美しい<br>✅ アラート柔軟 | ❌ 高額（従量課金）<br>❌ 設定複雑<br>❌ データ保持期間短い<br>❌ ベンダーロックイン |
| 2 | **Prometheus + Grafana** | [https://prometheus.io/](https://prometheus.io/) / [https://grafana.com/](https://grafana.com/) | メトリクス収集、可視化、アラート、オープンソース | ✅ 完全無料オープンソース<br>✅ K8s標準監視<br>✅ PromQL強力<br>✅ 柔軟なアラート<br>✅ Grafana可視化優秀 | ❌ セットアップ・運用必要<br>❌ ログ管理別途必要<br>❌ 長期保存向かない<br>❌ 学習曲線やや急 |
| 3 | **ELK Stack** | [https://www.elastic.co/](https://www.elastic.co/) | Elasticsearch, Logstash, Kibana - ログ管理、検索、可視化 | ✅ 強力なログ検索<br>✅ 可視化優秀<br>✅ スケーラブル<br>✅ 多様なデータソース対応<br>✅ コミュニティ大きい | ❌ リソース使用量大<br>❌ 運用複雑<br>❌ 商用機能は有料<br>❌ チューニング必要 |
| 4 | **New Relic** | [https://newrelic.com/](https://newrelic.com/) | APM、オブザーバビリティ、エラートラッキング | ✅ APM優秀<br>✅ トランザクショントレース<br>✅ セットアップ簡単<br>✅ UIわかりやすい<br>✅ AIインサイト | ❌ 高額<br>❌ データ保持制限<br>❌ カスタマイズ性低い<br>❌ 一部機能制限 |
| 5 | **Sentry** | [https://sentry.io/](https://sentry.io/) | エラートラッキング、パフォーマンス監視、リアルタイムアラート | ✅ エラートラッキング最高<br>✅ スタックトレース詳細<br>✅ リリース追跡<br>✅ 多言語対応<br>✅ 統合容易 | ❌ エラー特化（監視は弱い）<br>❌ 有料版やや高い<br>❌ インフラ監視不可<br>❌ アラート多すぎ問題 |
| 6 | **Splunk** | [https://www.splunk.com/](https://www.splunk.com/) | ログ分析、セキュリティ監視、機械学習 | ✅ 強力なログ分析<br>✅ セキュリティ監視優秀<br>✅ 機械学習統合<br>✅ エンタープライズ実績<br>✅ 豊富なアプリ | ❌ 非常に高額<br>❌ リソース使用量大<br>❌ 学習曲線急<br>❌ ライセンス複雑 |
| 7 | **AppDynamics** | [https://www.appdynamics.com/](https://www.appdynamics.com/) | APM、ビジネストランザクション監視、根本原因分析 | ✅ ビジネスメトリクス連携<br>✅ トランザクション可視化<br>✅ 根本原因分析AI<br>✅ エンタープライズ機能<br>✅ Cisco統合 | ❌ 非常に高額<br>❌ 複雑<br>❌ セットアップ時間かかる<br>❌ オーバースペック感 |
| 8 | **Dynatrace** | [https://www.dynatrace.com/](https://www.dynatrace.com/) | フルスタック監視、AI分析、自動化 | ✅ AI自動分析（Davis）<br>✅ フルスタック監視<br>✅ 自動検出・計装<br>✅ 根本原因分析優秀<br>✅ スケーラブル | ❌ 非常に高額<br>❌ オーバースペック<br>❌ 学習コスト高い<br>❌ カスタマイズ複雑 |
| 9 | **Zabbix** | [https://www.zabbix.com/](https://www.zabbix.com/) | オープンソース監視、ネットワーク監視、アラート | ✅ 完全無料オープンソース<br>✅ ネットワーク監視強い<br>✅ 柔軟なアラート<br>✅ エージェント・エージェントレス両対応<br>✅ 大規模対応 | ❌ UI古い<br>❌ セットアップ複雑<br>❌ APM機能弱い<br>❌ クラウドネイティブ対応弱い |
| 10 | **CloudWatch** | [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/) | AWS監視、ログ管理、メトリクス | ✅ AWS完全統合<br>✅ 従量課金<br>✅ セットアップ容易<br>✅ ログインサイト強力<br>✅ アラーム設定簡単 | ❌ AWS専用<br>❌ UI やや使いにくい<br>❌ カスタムメトリクス高い<br>❌ 可視化弱い |

#### その他利用可能なツール

- Nagios
- Azure Monitor
- Google Cloud Operations
- Sumo Logic
- Loki (ログ集約)
- Jaeger (分散トレーシング)
- OpenTelemetry
- Vector
- Fluentd
- Logstash

---

### 8.2.2 問題管理・変更管理

#### 主要タスク
- インシデント管理
- 問題管理
- 変更管理
- サービスデスク

#### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **ServiceNow** | [https://www.servicenow.com/](https://www.servicenow.com/) | ITSM、インシデント管理、変更管理、統合プラットフォーム | ✅ エンタープライズ級ITSM<br>✅ 包括的ITIL対応<br>✅ ワークフロー自動化<br>✅ CMDB統合<br>✅ 拡張性高い | ❌ 非常に高額<br>❌ 複雑で学習困難<br>❌ セットアップ時間長い<br>❌ 小規模には過剰 |
| 2 | **Jira Service Management** | [https://www.atlassian.com/software/jira/service-management](https://www.atlassian.com/software/jira/service-management) | ITサービスデスク、インシデント管理、Jira統合 | ✅ Jira統合優秀<br>✅ 開発チーム親和性高い<br>✅ 柔軟なワークフロー<br>✅ ナレッジベース<br>✅ コスト比較的安い | ❌ ITIL完全準拠ではない<br>❌ エンタープライズ機能弱い<br>❌ 複雑な設定<br>❌ サードパーティ統合必要 |
| 3 | **Zendesk** | [https://www.zendesk.com/](https://www.zendesk.com/) | カスタマーサポート、チケット管理、ナレッジベース | ✅ UI優秀<br>✅ セットアップ簡単<br>✅ マルチチャネル対応<br>✅ AI機能充実<br>✅ 統合豊富 | ❌ ITSM機能基本的<br>❌ 高額（従量課金）<br>❌ カスタマイズ性やや低い<br>❌ エンタープライズ向けではない |
| 4 | **Freshservice** | [https://freshservice.com/](https://freshservice.com/) | ITSM、資産管理、自動化 | ✅ コスパ優秀<br>✅ UI直感的<br>✅ セットアップ簡単<br>✅ AI自動化<br>✅ 資産管理統合 | ❌ 大規模には不向き<br>❌ カスタマイズ性低い<br>❌ 統合機能やや弱い<br>❌ エンタープライズ機能制限 |
| 5 | **PagerDuty** | [https://www.pagerduty.com/](https://www.pagerduty.com/) | インシデント対応、オンコール管理、アラート集約 | ✅ インシデント対応最適<br>✅ アラート集約優秀<br>✅ オンコールスケジュール<br>✅ エスカレーション自動化<br>✅ 統合豊富（300+） | ❌ 高額<br>❌ ITSM機能限定的<br>❌ インシデント特化<br>❌ 通知多すぎ問題 |
| 6 | **BMC Remedy** | [https://www.bmc.com/it-solutions/remedy-itsm.html](https://www.bmc.com/it-solutions/remedy-itsm.html) | エンタープライズITSM、CMDB、変更管理 | ✅ エンタープライズ級<br>✅ ITIL完全対応<br>✅ 大規模実績豊富<br>✅ CMDB強力<br>✅ カスタマイズ性高い | ❌ 非常に高額<br>❌ 複雑で古い<br>❌ UI使いにくい<br>❌ 学習曲線非常に急 |
| 7 | **ManageEngine ServiceDesk Plus** | [https://www.manageengine.com/products/service-desk/](https://www.manageengine.com/products/service-desk/) | ITSM、ヘルプデスク、資産管理 | ✅ コスパ優秀<br>✅ 機能豊富<br>✅ 資産管理統合<br>✅ セルフホスト可能<br>✅ 中規模向け最適 | ❌ UI やや古い<br>❌ 大規模には不向き<br>❌ カスタマイズ複雑<br>❌ サポートやや弱い |
| 8 | **TOPdesk** | [https://www.topdesk.com/](https://www.topdesk.com/) | ITサービス管理、施設管理、知識管理 | ✅ UI使いやすい<br>✅ セットアップ簡単<br>✅ 施設管理統合<br>✅ 柔軟なワークフロー<br>✅ 中規模向け | ❌ 日本語情報少ない<br>❌ エンタープライズ機能弱い<br>❌ 統合機能限定的<br>❌ カスタマイズ性やや低い |
| 9 | **OpsGenie** | [https://www.atlassian.com/software/opsgenie](https://www.atlassian.com/software/opsgenie) | インシデント管理、アラート、オンコール | ✅ Atlassian統合<br>✅ アラート管理優秀<br>✅ オンコールスケジュール<br>✅ エスカレーション柔軟<br>✅ コスパ良い | ❌ ITSM機能限定的<br>❌ インシデント特化<br>❌ 変更管理弱い<br>❌ 通知設定複雑 |
| 10 | **VictorOps** | [https://victorops.com/](https://victorops.com/) | (現 Splunk On-Call) インシデント対応、ChatOps、コラボレーション | ✅ ChatOps統合<br>✅ オンコール管理<br>✅ インシデント対応迅速<br>✅ タイムライン可視化<br>✅ Splunk統合 | ❌ Splunk買収後変化<br>❌ ITSM機能限定的<br>❌ 価格上昇傾向<br>❌ 機能やや基本的 |

#### その他利用可能なツール

- Cherwell
- Ivanti (旧HEAT)
- SysAid
- Vivantio
- HaloITSM

---

## 8.3 デプロイ自動化

### 主要タスク
- デプロイパイプラインの構築
- 本番環境へのリリース
- ブルーグリーンデプロイ
- カナリアリリース

### 推奨ツール（CI/CDツールから抜粋 Top 5）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **GitHub Actions** | [https://github.com/features/actions](https://github.com/features/actions) | GitHub統合のCI/CDプラットフォーム。YAMLベースのワークフロー定義 | ✅ GitHub完全統合<br>✅ 豊富なマーケットプレイス<br>✅ 無料枠充実（月2000分）<br>✅ セットアップ簡単<br>✅ マトリックスビルド対応 | ❌ GitHub依存<br>❌ 複雑なワークフローは管理困難<br>❌ デバッグしにくい<br>❌ セルフホスト設定やや面倒 |
| 2 | **GitLab CI/CD** | [https://docs.gitlab.com/ee/ci/](https://docs.gitlab.com/ee/ci/) | GitLab統合のCI/CD。Auto DevOps機能で自動設定可能 | ✅ GitLab完全統合<br>✅ コンテナレジストリ内蔵<br>✅ Auto DevOps<br>✅ セルフホスト可能<br>✅ パイプライン可視化優秀 | ❌ GitLab専用<br>❌ 学習曲線やや急<br>❌ セルフホストは運用コスト高<br>❌ 並列実行制限あり（無料版） |
| 3 | **Azure DevOps Pipelines** | [https://azure.microsoft.com/ja-jp/products/devops/pipelines/](https://azure.microsoft.com/ja-jp/products/devops/pipelines/) | Microsoft製CI/CD。YAMLまたはGUIで設定可能 | ✅ Azure統合優秀<br>✅ Windows環境に強い<br>✅ マルチプラットフォーム<br>✅ 無料枠充実<br>✅ YAML/GUI両対応 | ❌ Azure外では利点薄い<br>❌ UI複雑<br>❌ ドキュメント分かりにくい<br>❌ セットアップやや面倒 |
| 4 | **AWS CodePipeline** | [https://aws.amazon.com/codepipeline/](https://aws.amazon.com/codepipeline/) | AWSフルマネージドCI/CD。他AWSサービスと緊密連携 | ✅ AWSサービス完全統合<br>✅ フルマネージド<br>✅ スケーラブル<br>✅ CodeBuild/CodeDeploy連携<br>✅ 従量課金 | ❌ AWS依存<br>❌ 学習曲線急<br>❌ AWS外での利用困難<br>❌ コスト予測難しい |
| 5 | **Argo CD** | [https://argo-cd.readthedocs.io/](https://argo-cd.readthedocs.io/) | KubernetesネイティブのGitOps継続的デリバリーツール | ✅ GitOps実装に最適<br>✅ Kubernetes完全統合<br>✅ 宣言的デプロイ<br>✅ 可視化優秀<br>✅ オープンソース | ❌ Kubernetes必須<br>❌ 学習コスト高い<br>❌ CI機能なし（CD専用）<br>❌ セットアップ複雑 |

---

## 8.4 クラウドサービス（Azure）

導入・運用に使用するAzureサービス：

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|----------|-----------|------|------|---------|-----------|
| 1 | **Azure Migrate** | [https://azure.microsoft.com/ja-jp/products/azure-migrate/](https://azure.microsoft.com/ja-jp/products/azure-migrate/) | Azureへの移行評価・実行ツール。オンプレ→クラウド移行支援 | オンプレミスからAzureへのワークロード移行、評価 | ✅ 移行評価・計画<br>✅ 依存関係可視化<br>✅ コスト見積<br>✅ 統合移行ツール<br>✅ 無料 | ❌ Azure専用<br>❌ 複雑な移行は手動作業必要<br>❌ 学習コスト高い<br>❌ VMware/Hyper-V中心 |
| 2 | **Azure Database Migration Service** | [https://azure.microsoft.com/ja-jp/products/database-migration/](https://azure.microsoft.com/ja-jp/products/database-migration/) | データベース移行サービス。最小ダウンタイムで移行 | SQL Server, MySQL, PostgreSQL等のAzureへの移行 | ✅ 最小ダウンタイム<br>✅ 異種DB移行対応<br>✅ 継続的同期<br>✅ スキーマ変換支援<br>✅ フルマネージド | ❌ Azure DB専用<br>❌ 複雑な移行は制限あり<br>❌ コスト予測難しい<br>❌ データ検証は別途必要 |
| 3 | **Azure Monitor** | [https://azure.microsoft.com/ja-jp/products/monitor/](https://azure.microsoft.com/ja-jp/products/monitor/) | フルスタック監視ソリューション。メトリクス、ログ、分散トレーシング統合 | 運用監視、APM、ログ分析、アラート設定 | ✅ Azure統合優秀<br>✅ Application Insights統合<br>✅ Log Analytics強力<br>✅ 多様なデータソース対応<br>✅ アラート柔軟 | ❌ 複雑で学習コスト高い<br>❌ コスト管理難しい<br>❌ UI分かりにくい<br>❌ クエリ言語（KQL）習得必要 |
| 4 | **Azure DevOps** | [https://azure.microsoft.com/ja-jp/products/devops/](https://azure.microsoft.com/ja-jp/products/devops/) | 統合DevOpsプラットフォーム。Boards、Repos、Pipelines、Artifacts | CI/CD、プロジェクト管理、リリース管理 | ✅ 統合DevOpsツール<br>✅ Azure統合優秀<br>✅ 無料枠充実<br>✅ エンタープライズ機能<br>✅ マルチプラットフォーム | ❌ UI複雑<br>❌ 学習曲線急<br>❌ GitHub Actionsと機能重複<br>❌ Azure外では利点薄い |
| 5 | **Azure Automation** | [https://azure.microsoft.com/ja-jp/products/automation/](https://azure.microsoft.com/ja-jp/products/automation/) | クラウド・オンプレ自動化サービス。Runbook、構成管理 | 運用自動化、パッチ管理、構成管理、スケジュール実行 | ✅ PowerShell/Python Runbook<br>✅ 更新管理統合<br>✅ スケジュール実行<br>✅ ハイブリッド対応<br>✅ 従量課金 | ❌ PowerShell中心（Windows寄り）<br>❌ 複雑なワークフローは困難<br>❌ デバッグ難しい<br>❌ 他ツール比で機能限定的 |

---

## 8.5 クラウドサービス（AWS）

導入・運用に使用するAWSサービス：

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|----------|-----------|------|------|---------|-----------|
| 1 | **AWS Migration Hub** | [https://aws.amazon.com/migration-hub/](https://aws.amazon.com/migration-hub/) | 移行プロジェクトの一元管理。進捗追跡、ツール統合 | AWS移行プロジェクトの計画・追跡・管理 | ✅ 移行進捗一元管理<br>✅ 複数移行ツール統合<br>✅ リソース追跡<br>✅ 無料（移行ツールは別料金）<br>✅ 依存関係可視化 | ❌ AWS専用<br>❌ 移行実行は別ツール必要<br>❌ 情報集約のみ<br>❌ リアルタイム性低い |
| 2 | **AWS Database Migration Service (DMS)** | [https://aws.amazon.com/dms/](https://aws.amazon.com/dms/) | データベース移行サービス。最小ダウンタイム、異種DB対応 | データベースのAWS移行、継続的レプリケーション | ✅ 最小ダウンタイム移行<br>✅ 異種DB間移行対応<br>✅ 継続的レプリケーション<br>✅ スキーマ変換ツール統合<br>✅ フルマネージド | ❌ 複雑な変換は手動<br>❌ パフォーマンス調整必要<br>❌ コスト予測難しい<br>❌ データ検証推奨 |
| 3 | **AWS CloudWatch** | [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/) | AWS統合監視サービス。メトリクス、ログ、アラーム | 運用監視、ログ管理、メトリクス収集、アラート | ✅ AWS完全統合<br>✅ 従量課金<br>✅ ログインサイト強力<br>✅ カスタムメトリクス対応<br>✅ アラーム・ダッシュボード | ❌ AWS専用<br>❌ UI使いにくい<br>❌ カスタムメトリクス高い<br>❌ 可視化機能弱い |
| 4 | **AWS Systems Manager** | [https://aws.amazon.com/systems-manager/](https://aws.amazon.com/systems-manager/) | 運用管理統合サービス。パッチ管理、自動化、パラメータストア | インフラ自動化、パッチ管理、構成管理、セッション管理 | ✅ 包括的運用管理<br>✅ Session Manager（SSHレス）<br>✅ パッチ自動化<br>✅ パラメータストア<br>✅ 基本無料 | ❌ 機能多すぎて複雑<br>❌ UI分かりにくい<br>❌ 学習コスト高い<br>❌ 一部機能有料 |
| 5 | **AWS CodeDeploy** | [https://aws.amazon.com/codedeploy/](https://aws.amazon.com/codedeploy/) | 自動デプロイサービス。EC2、Lambda、ECS、オンプレ対応 | アプリケーションの自動デプロイ、ブルーグリーン、カナリア | ✅ 自動デプロイ<br>✅ ブルーグリーン対応<br>✅ ロールバック機能<br>✅ EC2/Lambda/ECS対応<br>✅ 基本無料（EC2課金のみ） | ❌ 設定やや複雑<br>❌ デバッグ難しい<br>❌ CodePipeline統合推奨<br>❌ エラー時の対応面倒 |
| 6 | **AWS OpsWorks** | [https://aws.amazon.com/opsworks/](https://aws.amazon.com/opsworks/) | 構成管理サービス。Chef/Puppet統合 | インフラ構成管理、アプリケーションデプロイ自動化 | ✅ Chef/Puppet統合<br>✅ レイヤーベース設計<br>✅ 自動スケーリング<br>✅ AWS統合<br>✅ 従量課金 | ❌ やや古い（メンテナンスモード）<br>❌ 学習曲線急<br>❌ 複雑<br>❌ 他ツール推奨傾向 |

---

## 参考資料

- [IPA 共通フレーム2013](https://www.ipa.go.jp/)
- [高信頼化ソフトウェア開発手法ガイド](https://www.ipa.go.jp/)
- [アジャイル開発実践ガイドブック](https://www.ipa.go.jp/)
- [システム移行プロセスガイド](https://www.ipa.go.jp/)

---

**前の工程**: [7. インフラテスト](./dev_process_開発工程_7_インフラテスト.md)
