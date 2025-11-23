# 開発工程 7: インフラテスト

> **参考**: IPA 共通フレーム2013
>
> この工程では、インフラストラクチャの品質・性能・セキュリティを検証し、本番環境への準備を整えます。

## 概要

インフラテストでは、以下の主要な活動を実施します：

- インフラ環境の構築・検証
- 性能・負荷テスト
- セキュリティテスト
- 監視・運用テスト
- IaC（Infrastructure as Code）の検証
- コンテナ・オーケストレーションのテスト

---

## 7.1 インフラストラクチャ as Code (IaC)

### 主要タスク
- IaCテンプレートの作成
- インフラ構成のコード化
- 環境の自動プロビジョニング
- 構成ドリフトの検出

### 推奨ツール（生産性が高いもの Top 5）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **Terraform** | [https://www.terraform.io/](https://www.terraform.io/) | HashiCorp製マルチクラウドIaC。HCL言語、状態管理、モジュール化 | ✅ マルチクラウド対応<br>✅ 業界標準・実績豊富<br>✅ モジュール化・再利用容易<br>✅ 状態管理優秀<br>✅ プランで事前確認可 | ❌ 状態ファイル管理必要<br>❌ 学習曲線やや急<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料（Cloud） |
| 2 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。JSON/YAMLテンプレート、スタック管理 | ✅ AWS完全統合<br>✅ 無料（AWS料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ AWS専用<br>❌ JSON/YAML冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る |
| 3 | **Ansible** | [https://www.ansible.com/](https://www.ansible.com/) | Red Hat製構成管理・自動化ツール。エージェントレス、YAML、シンプル | ✅ エージェントレス<br>✅ YAML記述でシンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ コミュニティ大きい | ❌ 状態管理なし（べき等性は自己実装）<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 4 | **Pulumi** | [https://www.pulumi.com/](https://www.pulumi.com/) | プログラマブルIaC。TypeScript/Python/Go/C#、既存言語活用 | ✅ 既存言語使用（TS/Python等）<br>✅ IDEサポート・補完<br>✅ テスト容易<br>✅ マルチクラウド対応<br>✅ 状態管理自動 | ❌ 比較的新しい（2018〜）<br>❌ Terraformより情報少ない<br>❌ 一部機能有料<br>❌ 言語依存性高い |
| 5 | **AWS CDK** | [https://aws.amazon.com/cdk/](https://aws.amazon.com/cdk/) | AWSプログラマブルIaC。TypeScript/Python/Java/C#、CloudFormation生成 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ CloudFormation自動生成<br>✅ IDE補完・型チェック<br>✅ 無料 | ❌ AWS専用<br>❌ CloudFormation依存<br>❌ 学習コストあり<br>❌ デバッグ難しい場合あり |

### その他利用可能なツール

- Crossplane
- Terragrunt
- Packer
- Vagrant
- Cloud-Init

---

## 7.2 コンテナ・オーケストレーション

### 主要タスク
- コンテナイメージのビルド・テスト
- Kubernetesマニフェストの検証
- コンテナオーケストレーションのテスト
- ヘルスチェック・リソース制限の確認

### 推奨ツール（生産性が高いもの Top 5）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **Docker** | [https://www.docker.com/](https://www.docker.com/) | コンテナ化プラットフォーム。アプリケーションと依存関係をパッケージ化 | ✅ 業界標準・デファクト<br>✅ 環境再現性高い<br>✅ 軽量で高速起動<br>✅ 豊富なイメージライブラリ<br>✅ 開発環境統一 | ❌ Windows環境やや複雑<br>❌ ネットワーク設定難しい<br>❌ 本番運用はオーケストレータ必須<br>❌ セキュリティ設定必要 |
| 2 | **Kubernetes (K8s)** | [https://kubernetes.io/](https://kubernetes.io/) | コンテナオーケストレーションプラットフォーム。自動デプロイ、スケーリング、管理 | ✅ 業界標準オーケストレータ<br>✅ 自動スケーリング・自己修復<br>✅ 宣言的設定<br>✅ クラウドネイティブ標準<br>✅ 大規模実績豊富 | ❌ 学習曲線非常に急<br>❌ 複雑で運用困難<br>❌ リソース使用量大<br>❌ 小規模には過剰 |
| 3 | **Docker Compose** | [https://docs.docker.com/compose/](https://docs.docker.com/compose/) | マルチコンテナ定義・管理ツール。YAMLで開発環境定義 | ✅ シンプルで学習容易<br>✅ 開発環境に最適<br>✅ YAML定義でバージョン管理<br>✅ Docker統合<br>✅ 無料 | ❌ 本番環境不向き<br>❌ スケーリング機能弱い<br>❌ 単一ホスト限定<br>❌ K8sより機能少ない |
| 4 | **Helm** | [https://helm.sh/](https://helm.sh/) | Kubernetesパッケージマネージャ。アプリケーションをチャートで管理 | ✅ K8s標準パッケージマネージャ<br>✅ 再利用可能なチャート<br>✅ バージョン管理・ロールバック<br>✅ テンプレート機能<br>✅ 無料オープンソース | ❌ K8s必須<br>❌ テンプレート複雑化しやすい<br>❌ デバッグ難しい<br>❌ 学習コストあり |
| 5 | **Amazon EKS** | [https://aws.amazon.com/eks/](https://aws.amazon.com/eks/) | AWSマネージドKubernetesサービス。運用負荷軽減 | ✅ K8sマネージド<br>✅ AWS統合優秀<br>✅ 自動アップグレード<br>✅ IAM統合<br>✅ 高可用性 | ❌ AWS依存<br>❌ コスト高め<br>❌ 一部機能制限<br>❌ 他クラウドへの移行困難 |

### その他利用可能なツール

- Podman
- containerd
- CRI-O
- k3s (軽量K8s)
- Nomad (HashiCorp)
- Docker Swarm
- Portainer
- Lens (K8s IDE)
- K9s (K8s CLI)
- Kustomize

---

## 7.3 監視・運用管理

### 主要タスク
- システム監視の設定
- ログ管理システムの構築
- メトリクス収集・可視化
- アラート設定

### 推奨ツール（生産性が高いもの Top 10）

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

### その他利用可能なツール

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

## 7.4 セキュリティ・脆弱性管理

### 主要タスク
- インフラ脆弱性スキャン
- コンテナイメージスキャン
- IaCセキュリティ検証
- セキュリティポリシーの適用

### 推奨ツール（生産性が高いもの Top 5）

| # | ツール名 | 公式サイト | 説明 | メリット | デメリット |
|---|---------|-----------|------|---------|-----------|
| 1 | **Snyk** | [https://snyk.io/](https://snyk.io/) | 開発者向けセキュリティプラットフォーム。依存関係、コンテナ、IaCスキャン | ✅ 依存関係脆弱性検出<br>✅ 自動修正PR作成<br>✅ IDE/CI/CD統合<br>✅ コンテナ・IaCスキャン<br>✅ 開発者フレンドリー | ❌ 無料版制限多い<br>❌ 有料版高額<br>❌ 誤検知やや多い<br>❌ 大規模では遅い |
| 2 | **Trivy** | [https://trivy.dev/](https://trivy.dev/) | Aqua製包括的脆弱性スキャナー。コンテナ、IaC、ファイルシステムスキャン | ✅ 高速で包括的<br>✅ 完全無料オープンソース<br>✅ コンテナ・IaC・SBOM対応<br>✅ CI/CD統合容易<br>✅ オフライン動作可 | ❌ 誤検知やや多い<br>❌ GUI なし<br>❌ 修正提案機能なし<br>❌ ライセンス管理弱い |
| 3 | **Dependabot** | [https://github.com/dependabot](https://github.com/dependabot) | GitHub統合依存関係更新ツール。セキュリティアラート、PR自動作成 | ✅ GitHub完全統合<br>✅ 完全無料<br>✅ 自動PR作成<br>✅ セキュリティアドバイザリ<br>✅ 設定簡単 | ❌ GitHub専用<br>❌ 機能基本的<br>❌ カスタマイズ性低い<br>❌ Snykより機能少ない |
| 4 | **SonarQube** | [https://www.sonarqube.org/](https://www.sonarqube.org/) | コード品質・セキュリティプラットフォーム。SAST、セキュリティホットスポット | ✅ コード品質・セキュリティ統合<br>✅ OWASP Top 10対応<br>✅ 多言語対応<br>✅ 技術的負債可視化<br>✅ Community版無料 | ❌ セキュリティ機能は基本的<br>❌ セットアップ・運用必要<br>❌ 専用ツールより検出少ない<br>❌ リソース使用量大 |
| 5 | **OWASP Dependency-Check** | [https://owasp.org/www-project-dependency-check/](https://owasp.org/www-project-dependency-check/) | OWASP製依存関係脆弱性スキャナー。NVD連携、オープンソース | ✅ 完全無料オープンソース<br>✅ NVD（国家脆弱性DB）連携<br>✅ 多言語対応<br>✅ CI/CD統合<br>✅ SBOM生成 | ❌ 実行速度遅い<br>❌ 誤検知多い<br>❌ 修正提案なし<br>❌ UIやや古い |

### その他利用可能なツール

- Anchore
- JFrog Xray
- GitLab Security Scanning
- GitHub Advanced Security
- Contrast Security

---

## 7.5 クラウドサービス（Azure）

インフラテストに使用するAzureサービス：

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|----------|-----------|------|------|---------|-----------|
| 1 | **Azure Monitor** | [https://azure.microsoft.com/ja-jp/products/monitor/](https://azure.microsoft.com/ja-jp/products/monitor/) | フルスタック監視ソリューション。メトリクス、ログ、分散トレーシング統合 | インフラ監視、APM、ログ分析、アラート設定 | ✅ Azure統合優秀<br>✅ Application Insights統合<br>✅ Log Analytics強力<br>✅ 多様なデータソース対応<br>✅ アラート柔軟 | ❌ 複雑で学習コスト高い<br>❌ コスト管理難しい<br>❌ UI分かりにくい<br>❌ クエリ言語（KQL）習得必要 |
| 2 | **Azure DevTest Labs** | [https://azure.microsoft.com/ja-jp/products/devtest-lab/](https://azure.microsoft.com/ja-jp/products/devtest-lab/) | テスト環境自動プロビジョニング。コスト管理、自動シャットダウン | テスト環境の迅速な構築・破棄、コスト最適化 | ✅ テスト環境コスト削減<br>✅ 自動シャットダウン<br>✅ テンプレート再利用<br>✅ クォータ管理<br>✅ Azure統合 | ❌ DevTest専用（本番不可）<br>❌ 機能制限あり<br>❌ 設定やや複雑<br>❌ 大規模では管理困難 |
| 3 | **Azure Network Watcher** | [https://azure.microsoft.com/ja-jp/products/network-watcher/](https://azure.microsoft.com/ja-jp/products/network-watcher/) | ネットワーク監視・診断ツール。パケットキャプチャ、フロー分析 | ネットワーク診断、接続テスト、トラフィック分析 | ✅ ネットワーク可視化<br>✅ パケットキャプチャ<br>✅ VPN診断<br>✅ NSGフローログ<br>✅ 接続トラブルシュート | ❌ Azure VNet専用<br>❌ リアルタイム性やや低い<br>❌ ストレージコスト別途<br>❌ 詳細分析は別ツール必要 |
| 4 | **Azure Security Center** | [https://azure.microsoft.com/ja-jp/products/defender-for-cloud/](https://azure.microsoft.com/ja-jp/products/defender-for-cloud/) | (現 Microsoft Defender for Cloud) クラウドセキュリティポスチャ管理、脅威保護 | セキュリティ評価、脆弱性スキャン、コンプライアンス管理 | ✅ 包括的セキュリティ管理<br>✅ 脅威インテリジェンス<br>✅ コンプライアンス評価<br>✅ 自動修復推奨<br>✅ マルチクラウド対応 | ❌ 有料機能多い<br>❌ アラート多すぎ問題<br>❌ 設定複雑<br>❌ 誤検知あり |
| 5 | **Azure Load Testing** | [https://azure.microsoft.com/ja-jp/products/load-testing/](https://azure.microsoft.com/ja-jp/products/load-testing/) | フルマネージド負荷テストサービス。JMeterベース、大規模分散テスト | インフラ性能テスト、スケーラビリティ検証、負荷試験 | ✅ JMeter互換<br>✅ 大規模分散実行<br>✅ CI/CD統合<br>✅ Azure Monitor統合<br>✅ セットアップ不要 | ❌ JMeterベースのみ<br>❌ カスタマイズ性やや低い<br>❌ コスト予測難しい<br>❌ 比較的新しいサービス |

---

## 7.6 クラウドサービス（AWS）

インフラテストに使用するAWSサービス：

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|----------|-----------|------|------|---------|-----------|
| 1 | **Amazon CloudWatch** | [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/) | AWS統合監視サービス。メトリクス、ログ、アラーム、ダッシュボード | インフラ監視、ログ管理、メトリクス収集、アラート | ✅ AWS完全統合<br>✅ 従量課金<br>✅ ログインサイト強力<br>✅ カスタムメトリクス対応<br>✅ アラーム・ダッシュボード | ❌ AWS専用<br>❌ UI使いにくい<br>❌ カスタムメトリクス高い<br>❌ 可視化機能弱い |
| 2 | **AWS X-Ray** | [https://aws.amazon.com/xray/](https://aws.amazon.com/xray/) | 分散トレーシングサービス。マイクロサービス・サーバーレスのパフォーマンス分析 | 分散トレーシング、パフォーマンスボトルネック分析、エラー追跡 | ✅ AWS Lambda/ECS統合<br>✅ サービスマップ可視化<br>✅ レイテンシ分析<br>✅ エラー検出<br>✅ 従量課金 | ❌ AWS依存<br>❌ 計装コード必要<br>❌ サンプリングレート制限<br>❌ コスト管理必要 |
| 3 | **AWS Config** | [https://aws.amazon.com/config/](https://aws.amazon.com/config/) | AWSリソース構成管理・監査サービス。変更追跡、コンプライアンス評価 | 構成管理、コンプライアンスチェック、ドリフト検出、監査 | ✅ リソース変更追跡<br>✅ コンプライアンスルール<br>✅ 構成履歴記録<br>✅ 自動修復（SSM連携）<br>✅ マルチアカウント対応 | ❌ コストかかる<br>❌ ルール作成複雑<br>❌ リアルタイム性低い<br>❌ ストレージコスト別途 |
| 4 | **Amazon Inspector** | [https://aws.amazon.com/inspector/](https://aws.amazon.com/inspector/) | 自動脆弱性管理サービス。EC2、ECR、Lambdaスキャン | インフラ脆弱性スキャン、コンテナスキャン、リスク評価 | ✅ 自動継続スキャン<br>✅ EC2/ECR/Lambda対応<br>✅ CVE自動検出<br>✅ リスクスコアリング<br>✅ 従量課金 | ❌ AWS リソース限定<br>❌ 修正は手動<br>❌ 誤検知あり<br>❌ カスタマイズ性低い |
| 5 | **AWS Systems Manager** | [https://aws.amazon.com/systems-manager/](https://aws.amazon.com/systems-manager/) | 運用管理統合サービス。パッチ管理、コンプライアンス、自動化 | インフラ自動化、パッチ管理、セッション管理、パラメータストア | ✅ 包括的運用管理<br>✅ Session Manager（SSHレス）<br>✅ パッチ自動化<br>✅ パラメータストア<br>✅ 基本無料 | ❌ 機能多すぎて複雑<br>❌ UI分かりにくい<br>❌ 学習コスト高い<br>❌ 一部機能有料 |
| 6 | **AWS Trusted Advisor** | [https://aws.amazon.com/premiumsupport/technology/trusted-advisor/](https://aws.amazon.com/premiumsupport/technology/trusted-advisor/) | AWSベストプラクティス推奨サービス。コスト最適化、セキュリティ、パフォーマンス | インフラ最適化推奨、セキュリティチェック、コスト削減提案 | ✅ ベストプラクティス推奨<br>✅ コスト最適化提案<br>✅ セキュリティチェック<br>✅ パフォーマンス改善<br>✅ 基本チェック無料 | ❌ 詳細チェックは有料（Business以上）<br>❌ 自動修復なし<br>❌ リアルタイム性低い<br>❌ カスタムチェック不可 |

---

## 参考資料

- [IPA 共通フレーム2013](https://www.ipa.go.jp/)
- [高信頼化ソフトウェア開発手法ガイド](https://www.ipa.go.jp/)
- [DX実践手引書](https://www.ipa.go.jp/)
- [クラウドネイティブ開発実践ガイド](https://www.ipa.go.jp/)

---

**次の工程**: [8. 導入](./dev_process_開発工程_8_導入.md)
