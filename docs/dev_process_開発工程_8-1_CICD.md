# 開発工程_8-1_CI/CD構築

## 1. 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**CI/CD（Continuous Integration / Continuous Delivery）構築プロセス**における開発タスクと推奨ツールをまとめたものです。

CI/CDでは、[開発工程_8_インフラ構築](./dev_process_開発工程_8_インフラ構築.md) によって構築されたインフラストラクチャ上で[開発工程_7_実装_アプリケーション](./dev_process_開発工程_7_実装_アプリケーション.md) によって実装されたアプリケーションを自動ビルド・テスト・デプロイします。

## 2. CI/CDとは

### 2.1 CI (Continuous Integration) - 継続的インテグレーション

コードの変更を頻繁にメインブランチに統合し、自動ビルド・自動テストを実行することで、品質を維持しながら開発速度を向上させる手法です。

### 2.2 CD (Continuous Delivery / Deployment) - 継続的デリバリー/デプロイ

- **Continuous Delivery（継続的デリバリー）**: 本番環境へのリリースをいつでも実行できる状態を維持
- **Continuous Deployment（継続的デプロイ）**: テストを通過したコードを自動的に本番環境へデプロイ

## 3. CI/CD構築

### 3.1. 主要タスク

- **ソースコード管理**: Git、GitHub、GitLab等でのバージョン管理
- **自動ビルド**: コミット/プルリクエスト時の自動ビルド実行
- **自動テスト**: 単体テスト、結合テスト、E2Eテストの自動実行
- **静的解析**: コード品質チェック、セキュリティスキャン
- **アーティファクト管理**: ビルド成果物の保管・バージョン管理
- **自動デプロイ**: ステージング・本番環境への自動デプロイ
- **環境管理**: 開発・ステージング・本番環境の管理
- **ロールバック**: デプロイ失敗時の自動ロールバック
- **通知・レポート**: ビルド/デプロイ結果の通知

### 3.2. 対応項目

- IaCコード構文チェック
- セキュリティポリシー検証
- ベストプラクティス準拠チェック
- アプリケーションコード構文チェック
- セキュリティスキャン
- ポリシー準拠チェック

### 3.3. 成果物

- CI/CDパイプライン定義ファイル
- ビルド・テストレポート
- セキュリティスキャン結果
- デプロイ履歴・ログ
- パフォーマンスメトリクス

## 4. 推奨ツール（マルチクラウド対応 CI/CD - Top 10）

**注**: Azure専用ツールは「Azure専用CI/CDツール」、AWS専用ツールは「AWS専用CI/CDツール」セクションを参照してください。

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|-----------|
| 1 | [**GitHub Actions**](https://github.com/features/actions) | GitHub統合CI/CD。YAML定義、豊富なマーケットプレイス | CI/CD、自動ビルド・テスト・デプロイ、GitHubワークフロー自動化 | 🟢 パブリックリポジトリ無料 / 💰 プライベート月2000分無料、超過従量課金 | ✅ GitHub完全統合<br>✅ マーケットプレイス豊富<br>✅ YAML記述シンプル<br>✅ マルチクラウド対応<br>✅ セルフホストランナー | ❌ GitHub依存<br>❌ 複雑なワークフロー困難<br>❌ デバッグやや困難<br>❌ 実行時間制限あり |
| 2 | [**GitLab CI/CD**](https://docs.gitlab.com/ee/ci/) | GitLab統合CI/CD。.gitlab-ci.yml、Auto DevOps | CI/CD、自動ビルド・テスト・デプロイ、GitLabワークフロー | 🟢 Free版あり / 💰 Premium/Ultimate有料 | ✅ GitLab完全統合<br>✅ Auto DevOps<br>✅ コンテナレジストリ統合<br>✅ Kubernetesデプロイ容易<br>✅ セルフホスト可能 | ❌ GitLab依存<br>❌ 設定複雑化しやすい<br>❌ リソース使用量大<br>❌ 学習曲線やや急 |
| 3 | [**Jenkins**](https://www.jenkins.io/) | オープンソースCI/CD。プラグイン豊富、高カスタマイズ性 | CI/CD、自動ビルド・テスト・デプロイ、複雑なパイプライン | 🟢 完全無料(オープンソース) | ✅ 高カスタマイズ性<br>✅ プラグイン超豊富<br>✅ セルフホスト<br>✅ 実績豊富<br>✅ コミュニティ大きい | ❌ セットアップ複雑<br>❌ UI古い<br>❌ 保守運用コスト高<br>❌ セキュリティ管理必要 |
| 4 | [**CircleCI**](https://circleci.com/) | クラウドCI/CD。高速実行、Docker/Kubernetes対応 | CI/CD、自動ビルド・テスト、コンテナビルド | 🟢 Free版(月6000分) / 💰 Performance/Scale有料 | ✅ 高速実行<br>✅ Docker/K8s統合<br>✅ 並列実行<br>✅ キャッシュ優秀<br>✅ YAML記述 | ❌ 無料枠少ない<br>❌ 有料版高額<br>❌ セルフホスト不可(Free)<br>❌ 複雑な設定困難 |
| 5 | [**ArgoCD**](https://argo-cd.readthedocs.io/) | KubernetesネイティブCD。GitOps、宣言的デプロイ | Kubernetes GitOps、自動同期、マニフェスト管理 | 🟢 完全無料(オープンソース) | ✅ GitOps標準<br>✅ Kubernetes完全統合<br>✅ 宣言的管理<br>✅ 差分可視化<br>✅ マルチクラスタ対応 | ❌ Kubernetes必須<br>❌ 学習曲線急<br>❌ CI機能なし(CD専用)<br>❌ セットアップ必要 |
| 6 | [**Tekton**](https://tekton.dev/) | KubernetesネイティブCI/CD。Cloud Native、CRD定義 | Kubernetes CI/CD、パイプライン、Cloud Nativeビルド | 🟢 完全無料(オープンソース) | ✅ Cloud Native<br>✅ Kubernetesネイティブ<br>✅ 再利用可能コンポーネント<br>✅ ベンダーニュートラル<br>✅ CNCF卒業プロジェクト | ❌ Kubernetes必須<br>❌ 学習曲線非常に急<br>❌ UI基本的(Dashboardは別)<br>❌ 複雑なYAML |
| 7 | [**Travis CI**](https://www.travis-ci.com/) | クラウドCI/CD。.travis.yml、GitHub統合 | CI/CD、自動ビルド・テスト、オープンソースプロジェクト | 🟢 OSS無料 / 💰 有料プラン | ✅ GitHub統合<br>✅ シンプル設定<br>✅ OSS無料<br>✅ マルチプラットフォーム<br>✅ マトリクスビルド | ❌ 有料版高額<br>❌ 実行速度やや遅い<br>❌ GitHub Actions台頭<br>❌ 機能限定的 |
| 8 | [**Drone**](https://www.drone.io/) | コンテナネイティブCI/CD。Docker Pipeline、プラグイン | CI/CD、Dockerビルド、軽量パイプライン | 🟢 オープンソース版無料 / 💰 Enterprise有料 | ✅ 軽量・高速<br>✅ コンテナネイティブ<br>✅ シンプル設定<br>✅ セルフホスト容易<br>✅ 多Git統合 | ❌ プラグイン少ない<br>❌ コミュニティ小<br>❌ ドキュメントやや少ない<br>❌ UI基本的 |
| 9 | [**TeamCity**](https://www.jetbrains.com/teamcity/) | JetBrains製CI/CD。強力UI、複雑ビルド対応 | CI/CD、エンタープライズビルド、複雑パイプライン | 🟢 Free版(3 agents, 100 builds) / 💰 Professional/Enterprise有料 | ✅ 強力なUI<br>✅ ビルド連鎖<br>✅ 多言語対応<br>✅ IDE統合(JetBrains)<br>✅ セルフホスト | ❌ 無料版制限強い<br>❌ 有料版高額<br>❌ リソース使用量大<br>❌ セットアップ複雑 |
| 10 | [**Bamboo**](https://www.atlassian.com/software/bamboo) | Atlassian製CI/CD。Jira/Bitbucket統合 | CI/CD、Atlassianエコシステム、ビルド・デプロイ | 💰 有料(Server/Data Center) / 🟢 10 jobs無料 | ✅ Jira完全統合<br>✅ Bitbucket統合<br>✅ 並列ビルド<br>✅ デプロイプロジェクト<br>✅ エンタープライズ向け | ❌ 有料のみ<br>❌ 高額<br>❌ セットアップ複雑<br>❌ GitHub Actions比で柔軟性低い |

---

## 5. Azure専用CI/CDツール

Azureエコシステムに最適化されたCI/CDツール群です。

### 5.1 Azure CI/CDツール（Top 3）

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|-----------|
| 1 | [**Azure DevOps Pipelines**](https://azure.microsoft.com/ja-jp/products/devops/pipelines/) | Azure統合CI/CD。YAML Pipeline、マルチプラットフォーム | CI/CD、ビルド・テスト・デプロイ、Infrastructure Pipeline | 🟢 月1800分無料 / 💰 超過従量課金 | ✅ Azure完全統合<br>✅ YAML Pipeline<br>✅ 並列ジョブ<br>✅ マルチプラットフォーム<br>✅ セルフホストエージェント | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ GitHub Actions比で情報少ない<br>❌ Azure依存 |
| 2 | [**Azure Container Registry Tasks (ACR Tasks)**](https://learn.microsoft.com/azure/container-registry/container-registry-tasks-overview) | ACR統合ビルド。コンテナイメージ自動ビルド | コンテナイメージビルド、マルチステップタスク、自動ビルド | 🟢 使用量課金 | ✅ ACR統合<br>✅ コンテナビルド特化<br>✅ トリガー豊富<br>✅ マルチステップタスク<br>✅ クロスリージョンビルド | ❌ コンテナ専用<br>❌ 複雑なパイプライン困難<br>❌ 他CI/CD比で機能少ない<br>❌ Azure専用 |
| 3 | [**Azure Release Pipelines**](https://learn.microsoft.com/azure/devops/pipelines/release/) | Azure DevOpsリリース管理。承認ゲート、ステージ管理 | リリース管理、承認フロー、ステージ別デプロイ | 🟢 Azure DevOps料金に含む | ✅ 視覚的パイプライン<br>✅ 承認ゲート<br>✅ ステージ管理<br>✅ ロールバック機能<br>✅ Azure統合 | ❌ YAML Pipelineで代替推奨<br>❌ Classic Pipelines(旧世代)<br>❌ 学習コスト高<br>❌ 柔軟性低い |

---

## 6. AWS専用CI/CDツール

AWSエコシステムに最適化されたCI/CDツール群です。

### 6.1 AWS CI/CDツール（Top 4）

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|-----------|
| 1 | [**AWS CodePipeline**](https://aws.amazon.com/codepipeline/) | AWSネイティブCI/CD。視覚的パイプライン、AWSサービス統合 | CI/CD、パイプライン管理、自動デプロイ | 🟢 月1パイプライン無料 / 💰 超過$1/pipeline/月 | ✅ AWSサービス完全統合<br>✅ 視覚的パイプライン<br>✅ 並列・連続実行<br>✅ サードパーティ統合<br>✅ CloudWatch統合 | ❌ 設定複雑<br>❌ AWS依存<br>❌ デバッグ困難<br>❌ パイプライン課金 |
| 2 | [**AWS CodeBuild**](https://aws.amazon.com/codebuild/) | フルマネージドビルドサービス。スケーラブル、Docker対応 | CI、ビルド、Dockerイメージビルド、テスト実行 | 🟢 月100分無料 / 💰 超過従量課金(ビルド分数) | ✅ フルマネージド<br>✅ スケーラブル<br>✅ Docker対応<br>✅ 並列ビルド<br>✅ カスタムビルド環境 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ コスト予測難しい<br>❌ ローカル実行困難 |
| 3 | [**AWS CodeDeploy**](https://aws.amazon.com/codedeploy/) | デプロイ自動化サービス。ローリング更新、Blue/Green | アプリケーションデプロイ、EC2/Lambda/ECS自動デプロイ | 🟢 EC2/Lambda無料 / 💰 ECS/Fargate有料 | ✅ 多様なデプロイ戦略<br>✅ ロールバック自動<br>✅ Blue/Greenデプロイ<br>✅ モニタリング統合<br>✅ オンプレ対応 | ❌ 設定複雑<br>❌ AppSpec学習必要<br>❌ ECS/Fargate有料<br>❌ トラブルシューティング困難 |
| 4 | [**AWS Amplify Hosting**](https://aws.amazon.com/amplify/hosting/) | フロントエンド特化CI/CD。Git連携、SSR対応 | フロントエンドCI/CD、Webホスティング、SSR/SSGビルド | 🟢 月1000分無料 / 💰 超過従量課金 | ✅ フロントエンド特化<br>✅ Git統合<br>✅ プレビュー環境自動<br>✅ SSR/SSG対応<br>✅ CDN統合 | ❌ フロントエンド専用<br>❌ カスタマイズ性低い<br>❌ ビルド時間長い場合あり<br>❌ 複雑な設定困難 |

---

## 7. CI/CDベストプラクティス

### 7.1 パイプライン設計

- **ステージ分離**: Build → Test → Deploy のステージを明確に分離
- **並列実行**: 独立したテストは並列実行でパイプライン高速化
- **失敗時の早期停止**: エラー検出時は即座にパイプライン停止
- **キャッシュ活用**: 依存関係やビルド成果物のキャッシュで高速化

### 7.2 セキュリティ

- **シークレット管理**: 認証情報は環境変数やシークレット管理ツール使用
- **最小権限の原則**: CI/CDに必要最小限の権限のみ付与
- **セキュリティスキャン**: SAST/DASTツール統合
- **依存関係チェック**: 脆弱性スキャンの自動化

### 7.3 モニタリング

- **パイプライン成功率**: ビルド/デプロイ成功率の監視
- **実行時間**: パイプライン実行時間の追跡・最適化
- **通知設定**: Slack/Teams/Email等への結果通知
- **ログ保存**: ビルド/デプロイログの長期保存

### 7.4 ブランチ戦略

- **Gitフロー採用**: main/develop/feature/release/hotfixブランチ戦略
- **プルリクエスト必須**: コードレビュー + 自動テスト必須
- **保護ブランチ**: mainブランチへの直接プッシュ禁止
- **タグ付けルール**: リリース時のバージョンタグ付け

---

**関連ドキュメント**:
- [7. 実装（アプリケーション）](./dev_process_開発工程_7_実装_アプリケーション.md)
- [8. インフラ構築](./dev_process_開発工程_8_インフラ構築.md)
- [9. アプリケーションテスト](./dev_process_開発工程_9_テスト_アプリケーション.md)
- [10. インフラテスト](./dev_process_開発工程_10_テスト_インフラ.md)

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
