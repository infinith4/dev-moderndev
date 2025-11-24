# 開発工程_10_テスト（インフラ）

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**インフラテストプロセス**における開発タスクと推奨ツールをまとめたものです。

**Azure（Bicep）やAWS（CDK）等のIaC（Infrastructure as Code）を使用してインフラを構築したことを前提**に、以下のテスト工程を実施します：

- **IaCコードの検証・テスト**（構文チェック、ポリシー検証、セキュリティスキャン）
- **インフラ単体テスト**（設定値確認、リソース作成確認、起動停止確認）
- **インフラ結合テスト**（疎通確認、機能連携、ネットワーク接続テスト）
- **インフラ総合テスト**（障害テスト、負荷テスト、セキュリティテスト、運用テスト）
- **性能・スケーラビリティテスト**
- **監視・運用テスト**

---

## 10.0 IaCコード検証・テスト（事前チェック）

Azure Bicep や AWS CDK 等で記述されたIaCコードの品質・セキュリティを検証します。

### 対応項目
- IaCコード構文チェック
- セキュリティポリシー検証
- ベストプラクティス準拠チェック
- コスト見積もり

### 成果物
- IaCコード検証レポート
- セキュリティスキャン結果
- ポリシー準拠チェックリスト

### 推奨ツール（IaCテスト Top 10）

| # | ツール名 | 概要 | 対象IaC | 料金 | メリット | デメリット |
|---|---------|------|---------|------|---------|-----------|
| 1 | [**Checkov**](https://www.checkov.io/) | Bridgecrew製IaCセキュリティスキャナー。1000+組込ポリシー | Terraform / CloudFormation / Bicep / CDK / K8s | 🟢 完全無料 | ✅ 多様なIaC対応<br>✅ 組込ポリシー豊富<br>✅ CI/CD統合容易<br>✅ カスタムポリシー作成可<br>✅ SAST機能 | ❌ 誤検知やや多い<br>❌ ポリシーカスタマイズ複雑<br>❌ パフォーマンスやや遅い<br>❌ GUI なし |
| 2 | [**tfsec**](https://aquasecurity.github.io/tfsec/) | Aqua製Terraformセキュリティスキャナー。高速・軽量 | Terraform | 🟢 完全無料 | ✅ 高速実行<br>✅ Terraform専用最適化<br>✅ カスタムチェック追加可<br>✅ CI/CD統合容易<br>✅ JSON出力対応 | ❌ Terraform専用<br>❌ Checkovより検出少ない<br>❌ GUI なし<br>❌ カスタムルール記述学習必要 |
| 3 | [**Terraform Validate**](https://www.terraform.io/) | Terraform公式構文チェックコマンド | Terraform | 🟢 完全無料（Terraform組込） | ✅ Terraform標準<br>✅ 構文エラー即座検出<br>✅ 高速<br>✅ セットアップ不要<br>✅ プロバイダースキーマ検証 | ❌ セキュリティチェックなし<br>❌ ベストプラクティス未検証<br>❌ 構文のみ検証<br>❌ カスタムルール不可 |
| 4 | [**Azure Bicep Linter**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Bicep公式リンター。ベストプラクティス準拠チェック | Azure Bicep | 🟢 完全無料（Bicep組込） | ✅ Bicep標準<br>✅ IDE統合（VSCode）<br>✅ リアルタイムエラー表示<br>✅ カスタムルール定義可<br>✅ ARM互換性検証 | ❌ Azure専用<br>❌ セキュリティチェック基本的<br>❌ ポリシー検証は別ツール必要<br>❌ 限定的ルールセット |
| 5 | [**CDK-nag**](https://github.com/cdklabs/cdk-nag) | AWS CDK向けベストプラクティスチェッカー | AWS CDK | 🟢 完全無料 | ✅ CDK専用最適化<br>✅ AWS Well-Architected準拠<br>✅ カスタムルール追加可<br>✅ CI/CD統合<br>✅ TypeScript/Python対応 | ❌ CDK専用<br>❌ CloudFormation非対応<br>❌ 実行時エラー検出のみ<br>❌ 情報やや少ない |
| 6 | [**Infracost**](https://www.infracost.io/) | IaCコスト見積もりツール。Terraform/CloudFormation対応 | Terraform / CloudFormation / Pulumi | 🟢 無料プランあり / 💰 Pro: $50/月～ | ✅ コスト見積り正確<br>✅ PR差分コスト表示<br>✅ CI/CD統合<br>✅ ダッシュボード美しい<br>✅ 複数IaC対応 | ❌ 見積精度に限界<br>❌ 全サービス非対応<br>❌ リアルタイム実コスト非表示<br>❌ 一部機能有料 |
| 7 | [**OPA (Open Policy Agent)**](https://www.openpolicyagent.org/) | CNCF製汎用ポリシーエンジン。Regoでカスタムポリシー定義 | Terraform / K8s / CloudFormation等 | 🟢 完全無料 | ✅ 柔軟なポリシー定義<br>✅ 多様なデータソース対応<br>✅ Kubernetes標準<br>✅ CI/CD統合<br>✅ エンタープライズ実績 | ❌ Rego学習曲線急<br>❌ セットアップ複雑<br>❌ ポリシー記述手間<br>❌ 初心者には難しい |
| 8 | [**Terraform Compliance**](https://terraform-compliance.com/) | TerraformコンプライアンステストツールBDD形式 | Terraform | 🟢 完全無料 | ✅ BDD形式（Gherkin）<br>✅ 可読性高いテスト<br>✅ CI/CD統合<br>✅ カスタムルール定義容易<br>✅ チーム共有しやすい | ❌ Terraform専用<br>❌ セキュリティスキャンは弱い<br>❌ コミュニティやや小<br>❌ 更新頻度低い |
| 9 | [**CloudFormation Guard**](https://github.com/aws-cloudformation/cloudformation-guard) | AWS公式CloudFormationポリシー検証ツール | CloudFormation / CDK | 🟢 完全無料 | ✅ AWS公式<br>✅ カスタムルール定義<br>✅ JSON/YAML出力<br>✅ CI/CD統合<br>✅ CloudFormation特化 | ❌ CloudFormation専用<br>❌ Terraform非対応<br>❌ ルール記述やや複雑<br>❌ 情報・ドキュメント少ない |
| 10 | [**Terratest**](https://terratest.gruntwork.io/) | Go製インフラテストフレームワーク。実際にインフラを作成してテスト | Terraform / Packer / Docker / K8s | 🟢 完全無料 | ✅ 実インフラテスト可能<br>✅ Go言語テストフレームワーク<br>✅ 多様なIaC対応<br>✅ 統合テスト最適<br>✅ 並列実行対応 | ❌ Go言語必須<br>❌ 実行時間長い<br>❌ コスト発生（実インフラ作成）<br>❌ 学習曲線急 |

---

## 10.1 インフラ単体テスト

Azure Bicep / AWS CDK で構築されたインフラリソースの個別テストを実施します。

**対応項目**
- 設定値の確認（パラメータチェック）
- 起動・停止確認

**成果物**
- 単体テスト仕様書
- 単体テスト結果報告書
- パラメータシート

### 推奨ツール（インフラ単体テスト Top 10）

| # | ツール名 | 概要 | 対象 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|-----------|
| 1 | [**Terratest**](https://terratest.gruntwork.io/) | Go製インフラテストフレームワーク。実際にインフラを作成してテスト | Terraform / CloudFormation / Bicep / CDK | 🟢 完全無料 | ✅ 実インフラテスト可能<br>✅ 単体テスト最適<br>✅ パラメータ検証<br>✅ Go言語テストフレームワーク | ❌ Go言語必須<br>❌ 実行時間長い<br>❌ コスト発生（実インフラ作成） |
| 2 | [**InSpec**](https://www.inspec.io/) | Chef製インフラテストフレームワーク。Ruby DSL、コンプライアンステスト | クラウド / サーバー / コンテナ | 🟢 完全無料 | ✅ 可読性高いDSL<br>✅ クラウド・サーバー両対応<br>✅ コンプライアンステスト強い<br>✅ 実行後検証に最適 | ❌ Ruby知識必要<br>❌ 学習曲線やや急<br>❌ パフォーマンスやや遅い |
| 3 | [**Serverspec**](https://serverspec.org/) | Ruby製サーバーテストフレームワーク。RSpec構文、SSH接続テスト | サーバー / VM | 🟢 完全無料 | ✅ RSpec構文で可読性高い<br>✅ 既存サーバーテスト容易<br>✅ SSH接続テスト<br>✅ コミュニティ大きい | ❌ クラウドネイティブ対応弱い<br>❌ IaCテストには不向き<br>❌ 古い（更新少ない） |
| 4 | [**Azure Resource Manager Testing Toolkit**](https://github.com/Azure/arm-ttk) | Azure公式ARM/Bicepテストツール。ベストプラクティス検証 | Azure Bicep / ARM | 🟢 完全無料 | ✅ Azure公式<br>✅ Bicep/ARM特化<br>✅ ベストプラクティス検証<br>✅ PowerShell統合 | ❌ Azure専用<br>❌ 機能限定的<br>❌ PowerShell必須 |
| 5 | [**AWS CDK Assertions**](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html) | AWS CDK公式テストライブラリ。スナップショットテスト、Fine-Grained Assertions | AWS CDK | 🟢 完全無料（CDK組込） | ✅ CDK公式<br>✅ TypeScript/Python対応<br>✅ スナップショットテスト<br>✅ 単体テスト最適 | ❌ CDK専用<br>❌ CloudFormation直接は不可<br>❌ 実インフラテスト不可 |
| 6 | [**Kitchen-Terraform**](https://github.com/newcontext-oss/kitchen-terraform) | Test Kitchen + Terraform統合テストツール。InSpec組合せ | Terraform | 🟢 完全無料 | ✅ Test Kitchen統合<br>✅ InSpecテスト記述<br>✅ 実インフラテスト<br>✅ マトリクステスト対応 | ❌ セットアップ複雑<br>❌ 実行時間長い<br>❌ Ruby知識必要 |
| 7 | [**Pester**](https://pester.dev/) | PowerShell製テストフレームワーク。Azure/Windows環境テスト | PowerShell / Azure / Windows | 🟢 完全無料 | ✅ PowerShell標準<br>✅ Windows/Azure環境最適<br>✅ BDD形式<br>✅ モック機能 | ❌ PowerShell環境必須<br>❌ Linux環境やや弱い<br>❌ IaC専用ではない |
| 8 | [**Goss**](https://github.com/goss-org/goss) | YAML製高速サーバーテストツール。シンプル、軽量、並列実行 | サーバー / コンテナ | 🟢 完全無料 | ✅ 非常に高速<br>✅ YAMLでシンプル<br>✅ 並列実行<br>✅ CI/CD統合容易 | ❌ 機能シンプル（拡張性低い）<br>❌ クラウドAPI未対応<br>❌ コミュニティ小 |
| 9 | [**Azure CLI / AWS CLI**](https://docs.microsoft.com/cli/azure/) | クラウド公式CLIツール。スクリプトでパラメータ検証 | Azure / AWS | 🟢 完全無料 | ✅ 公式ツール<br>✅ 全リソース対応<br>✅ スクリプト化容易<br>✅ 実リソース確認 | ❌ テストフレームワークではない<br>❌ テスト記述手間<br>❌ 構造化されていない |
| 10 | [**Pulumi Testing**](https://www.pulumi.com/docs/guides/testing/) | Pulumi公式テストフレームワーク。Unit / Property / Integration Test | Pulumi | 🟢 完全無料 | ✅ Pulumi公式<br>✅ 既存言語テストフレームワーク利用<br>✅ モック機能<br>✅ 単体テスト容易 | ❌ Pulumi専用<br>❌ 比較的新しい<br>❌ 情報少ない |

---

## 10.2 インフラ結合テスト

複数のインフラリソース間の接続・連携をテストします。

**対応項目**
- 疎通確認
- 機能連携

**成果物**
- 結合テスト仕様書
- 結合テスト結果報告書
- ネットワーク疎通確認シート

### 推奨ツール（インフラ結合テスト Top 10）

| # | ツール名 | 概要 | 対象 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|-----------|
| 1 | [**Azure Network Watcher**](https://azure.microsoft.com/ja-jp/products/network-watcher/) | Azure公式ネットワーク診断ツール。接続テスト、パケットキャプチャ | Azure | 🟢 使用量課金 | ✅ Azure公式<br>✅ ネットワーク疎通確認<br>✅ VPN診断<br>✅ NSGフローログ | ❌ Azure VNet専用<br>❌ リアルタイム性やや低い<br>❌ ストレージコスト別途 |
| 2 | [**AWS VPC Reachability Analyzer**](https://aws.amazon.com/vpc/features/) | AWS公式ネットワーク到達性分析ツール。経路確認、設定検証 | AWS | 🟢 使用量課金 | ✅ AWS公式<br>✅ ネットワーク経路可視化<br>✅ セキュリティグループ検証<br>✅ 実トラフィック不要 | ❌ AWS VPC専用<br>❌ 分析コストかかる<br>❌ リアルタイムではない |
| 3 | [**curl / wget**](https://curl.se/) | HTTP/HTTPSエンドポイント疎通確認。シンプル、高速 | HTTP/HTTPS | 🟢 完全無料 | ✅ 標準ツール<br>✅ シンプル<br>✅ スクリプト化容易<br>✅ デバッグ情報詳細 | ❌ HTTP専用<br>❌ テストフレームワークではない<br>❌ 複雑なテスト困難 |
| 4 | [**nc (netcat)**](https://nc110.sourceforge.io/) | TCP/UDPポート疎通確認。低レベルネットワークテスト | TCP/UDP | 🟢 完全無料 | ✅ 低レベルテスト可能<br>✅ ポート疎通確認<br>✅ 軽量・高速<br>✅ スクリプト化容易 | ❌ 機能シンプル<br>❌ HTTPSには不向き<br>❌ テストフレームワークではない |
| 5 | [**Terratest**](https://terratest.gruntwork.io/) | Go製インフラテストフレームワーク。実環境での統合テスト | Terraform / CloudFormation / Bicep / CDK | 🟢 完全無料 | ✅ 実インフラテスト<br>✅ HTTPエンドポイントテスト<br>✅ SSH接続テスト<br>✅ リトライ機能 | ❌ Go言語必須<br>❌ 実行時間長い<br>❌ コスト発生（実インフラ作成） |
| 6 | [**InSpec**](https://www.inspec.io/) | Chef製インフラテストフレームワーク。クラウドリソース連携テスト | クラウド / サーバー | 🟢 完全無料 | ✅ クラウドAPI統合<br>✅ リソース連携確認<br>✅ コンプライアンステスト<br>✅ Ruby DSL | ❌ Ruby知識必要<br>❌ セットアップやや複雑<br>❌ パフォーマンスやや遅い |
| 7 | [**Postman / Newman**](https://www.postman.com/) | APIテストツール。RESTful API疎通・機能確認、CI/CD統合 | REST API | 🟢 無料版あり / 💰 有料版 | ✅ GUI/CUI両対応<br>✅ API疎通確認容易<br>✅ コレクション管理<br>✅ Newman（CLI）でCI/CD統合 | ❌ API専用<br>❌ インフラ低レベルテスト不可<br>❌ 有料版やや高い |
| 8 | [**Azure CLI / AWS CLI**](https://docs.microsoft.com/cli/azure/) | クラウド公式CLI。リソース連携確認、設定検証 | Azure / AWS | 🟢 完全無料 | ✅ 公式ツール<br>✅ 全リソース対応<br>✅ スクリプト化容易<br>✅ 実リソース確認 | ❌ テストフレームワークではない<br>❌ テスト記述手間<br>❌ 構造化されていない |
| 9 | [**k6**](https://k6.io/) | Grafana製負荷テストツール。HTTP/WebSocket疎通・性能テスト | HTTP / WebSocket / gRPC | 🟢 無料版あり / 💰 Cloud有料 | ✅ JavaScriptテスト記述<br>✅ HTTP疎通確認<br>✅ 負荷テスト統合<br>✅ CI/CD統合 | ❌ HTTP系専用<br>❌ インフラ低レベルテスト不可<br>❌ Cloud版有料 |
| 10 | [**Pytest + Requests**](https://docs.pytest.org/) | Python製テストフレームワーク + HTTPライブラリ。APIテスト | HTTP API | 🟢 完全無料 | ✅ Python標準的<br>✅ Requests でHTTPテスト容易<br>✅ モック機能<br>✅ 柔軟なテスト記述 | ❌ HTTP専用<br>❌ 低レベルネットワークテスト不向き<br>❌ セットアップ必要 |

---

## 10.3 インフラ総合テスト

実環境に近い条件で、インフラ全体の統合テスト・非機能テストを実施します。

**対応項目**
- 障害テスト
- 負荷テスト
- セキュリティテスト
- 運用テスト

### 推奨ツール（インフラ総合テスト Top 10）

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|-----------|
| 1 | [**Azure Load Testing**](https://azure.microsoft.com/ja-jp/products/load-testing/) | Azure公式負荷テストサービス。JMeterベース、大規模分散テスト | 負荷テスト、性能テスト | 🟢 使用量課金 | ✅ Azure統合<br>✅ JMeter互換<br>✅ 大規模分散実行<br>✅ CI/CD統合<br>✅ Azure Monitor統合 | ❌ JMeterベースのみ<br>❌ カスタマイズ性やや低い<br>❌ コスト予測難しい |
| 2 | [**AWS Fault Injection Simulator (FIS)**](https://aws.amazon.com/fis/) | AWS公式カオスエンジニアリングサービス。障害注入テスト | 障害テスト、耐障害性確認 | 🟢 使用量課金 | ✅ AWS公式<br>✅ 制御された障害注入<br>✅ 実環境テスト<br>✅ ロールバック機能<br>✅ AWS Systems Manager統合 | ❌ AWS専用<br>❌ 実行コストかかる<br>❌ 設定複雑<br>❌ 比較的新しいサービス |
| 3 | [**Chaos Mesh**](https://chaos-mesh.org/) | CNCF製Kubernetesカオスエンジニアリングツール。障害注入 | 障害テスト（K8s） | 🟢 完全無料 | ✅ K8s専用<br>✅ 多様な障害シナリオ<br>✅ Web UI<br>✅ CRD定義で宣言的<br>✅ オープンソース | ❌ K8s専用<br>❌ 学習曲線やや急<br>❌ 本番環境注意必要<br>❌ セットアップ必要 |
| 4 | [**k6**](https://k6.io/) | Grafana製負荷テストツール。JavaScript記述、CI/CD統合 | 負荷テスト、性能テスト | 🟢 無料版あり / 💰 Cloud有料 | ✅ JavaScriptテスト記述<br>✅ HTTP/WebSocket/gRPC対応<br>✅ CI/CD統合容易<br>✅ クラウド分散実行可<br>✅ Grafana統合 | ❌ ブラウザベース負荷は別ツール必要<br>❌ Cloud版有料<br>❌ UIテスト不可 |
| 5 | [**JMeter**](https://jmeter.apache.org/) | Apache製負荷テストツール。GUI/CUI、多様なプロトコル対応 | 負荷テスト、性能テスト | 🟢 完全無料 | ✅ 業界標準<br>✅ 多様なプロトコル対応<br>✅ GUI/CUI両対応<br>✅ プラグイン豊富<br>✅ コミュニティ大きい | ❌ Java必須<br>❌ リソース使用量大<br>❌ 学習曲線急<br>❌ UIやや古い |
| 6 | [**Locust**](https://locust.io/) | Python製負荷テストツール。コード定義、分散実行、Web UI | 負荷テスト、性能テスト | 🟢 完全無料 | ✅ Pythonコード記述<br>✅ 分散実行<br>✅ リアルタイムWeb UI<br>✅ CI/CD統合<br>✅ 軽量 | ❌ HTTP専用（拡張必要）<br>❌ JMeterより機能少ない<br>❌ プロトコルサポート限定的 |
| 7 | [**Gatling**](https://gatling.io/) | Scala製高性能負荷テストツール。非同期、Scala/Java/Kotlin記述 | 負荷テスト、性能テスト | 🟢 無料版あり / 💰 Enterprise有料 | ✅ 高性能（非同期）<br>✅ Scala/Java/Kotlin記述<br>✅ レポート美しい<br>✅ CI/CD統合<br>✅ RESTful API対応 | ❌ Scala知識推奨<br>❌ 学習曲線やや急<br>❌ Enterprise版高額<br>❌ プロトコルサポート限定的 |
| 8 | [**Microsoft Defender for Cloud**](https://azure.microsoft.com/ja-jp/products/defender-for-cloud/) | Azure/AWS/GCPセキュリティポスチャ管理。脅威保護、コンプライアンス | セキュリティテスト、脆弱性評価 | 💰 有料（一部無料） | ✅ マルチクラウド対応<br>✅ 包括的セキュリティ管理<br>✅ 脅威インテリジェンス<br>✅ コンプライアンス評価<br>✅ 自動修復推奨 | ❌ 有料機能多い<br>❌ アラート多すぎ問題<br>❌ 設定複雑<br>❌ 誤検知あり |
| 9 | [**Prowler**](https://github.com/prowler-cloud/prowler) | オープンソースクラウドセキュリティツール。AWS/Azure/GCP/K8s対応 | セキュリティテスト、コンプライアンスチェック | 🟢 完全無料 / 💰 SaaS有料 | ✅ マルチクラウド対応<br>✅ 250+セキュリティチェック<br>✅ CIS Benchmark準拠<br>✅ CI/CD統合<br>✅ オープンソース | ❌ CLI中心（GUI なし）<br>❌ 自動修復機能なし<br>❌ レポート基本的<br>❌ セットアップ必要 |
| 10 | [**Azure Monitor / CloudWatch**](https://azure.microsoft.com/ja-jp/products/monitor/) | クラウド公式監視サービス。運用テスト、メトリクス監視 | 運用テスト、監視確認 | 🟢 使用量課金 | ✅ クラウド統合優秀<br>✅ メトリクス・ログ統合<br>✅ アラート設定<br>✅ ダッシュボード<br>✅ 公式サポート | ❌ クラウド依存<br>❌ UI分かりにくい<br>❌ コスト管理必要<br>❌ カスタマイズ複雑 |

---

## 参考: IaC開発・コンテナ・監視・セキュリティツール

インフラテストと合わせて活用されるツール群です。

### IaC開発ツール

| ツール名 | 概要 | 用途 |
|---------|------|------|
| [**Terraform**](https://www.terraform.io/) | HashiCorp製マルチクラウドIaC | IaCテンプレート作成、マルチクラウド管理 |
| [**Azure Bicep**](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure公式IaC言語 | Azure専用IaC |
| [**AWS CDK**](https://aws.amazon.com/cdk/) | AWSプログラマブルIaC | AWS専用IaC、TypeScript/Python等 |
| [**Pulumi**](https://www.pulumi.com/) | プログラマブルIaC | マルチクラウド、既存言語使用 |
| [**Ansible**](https://www.ansible.com/) | 構成管理ツール | サーバー設定自動化 |

### コンテナ・オーケストレーション

| ツール名 | 概要 | 用途 |
|---------|------|------|
| [**Docker**](https://www.docker.com/) | コンテナ化プラットフォーム | コンテナイメージ作成・実行 |
| [**Kubernetes**](https://kubernetes.io/) | コンテナオーケストレーション | コンテナ管理、スケーリング |
| [**Helm**](https://helm.sh/) | K8sパッケージマネージャ | K8sアプリケーション管理 |
| [**Amazon EKS**](https://aws.amazon.com/eks/) / [**Azure AKS**](https://azure.microsoft.com/ja-jp/products/kubernetes-service/) | マネージドK8sサービス | K8s運用負荷軽減 |

### 監視・運用管理

| ツール名 | 概要 | 用途 |
|---------|------|------|
| [**Azure Monitor**](https://azure.microsoft.com/ja-jp/products/monitor/) | Azure監視サービス | Azureリソース監視、APM |
| [**Amazon CloudWatch**](https://aws.amazon.com/cloudwatch/) | AWS監視サービス | AWSリソース監視、ログ管理 |
| [**Prometheus + Grafana**](https://prometheus.io/) | オープンソース監視 | メトリクス収集・可視化 |
| [**Datadog**](https://www.datadoghq.com/) | 統合監視プラットフォーム | インフラ・APM統合監視 |
| [**ELK Stack**](https://www.elastic.co/) | ログ管理プラットフォーム | ログ収集・検索・可視化 |

### セキュリティ・脆弱性管理

| ツール名 | 概要 | 用途 |
|---------|------|------|
| [**Snyk**](https://snyk.io/) | 開発者向けセキュリティ | 依存関係・コンテナ・IaCスキャン |
| [**Trivy**](https://trivy.dev/) | 包括的脆弱性スキャナー | コンテナ・IaC・ファイルシステムスキャン |
| [**Checkov**](https://www.checkov.io/) | IaCセキュリティスキャナー | Terraform/Bicep/CDKセキュリティ検証 |
| [**SonarQube**](https://www.sonarqube.org/) | コード品質・セキュリティ | SAST、コード品質分析 |

---

## 参考資料

- [IPA 共通フレーム2013](https://www.ipa.go.jp/)
- [高信頼化ソフトウェア開発手法ガイド](https://www.ipa.go.jp/)
- [DX実践手引書](https://www.ipa.go.jp/)
- [クラウドネイティブ開発実践ガイド](https://www.ipa.go.jp/)
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

**次の工程**: [8. 導入](./dev_process_開発工程_8_導入.md)
