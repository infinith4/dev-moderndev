# 開発工程_5_実装

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**実装プロセス（アプリケーション実装）**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 5.1 アプリケーション実装

### 主要タスク
- コーディング標準の確立
- プログラミング
- コードレビュー
- 単体テストの実施
- バージョン管理
- CI/CD構築

### 推奨開発環境・IDE（Top 5）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Visual Studio Code** | [https://code.visualstudio.com/](https://code.visualstudio.com/) | Microsoft製軽量コードエディタ。拡張機能エコシステム充実 | マルチ言語開発、Git統合、リモート開発、拡張機能 | ✅ 無料オープンソース<br>✅ 拡張機能豊富<br>✅ 多言語対応<br>✅ Git統合<br>✅ 軽量高速 | ❌ フルIDEではない<br>❌ 大規模PJ重い<br>❌ 初期設定時間必要<br>❌ デバッグ機能基本的 |
| 2 | **IntelliJ IDEA** | [https://www.jetbrains.com/idea/](https://www.jetbrains.com/idea/) | JetBrains製Java/Kotlin IDE。強力なリファクタリング | Java/Kotlin開発、Spring、Maven/Gradle、デバッグ | ✅ Java開発最適化<br>✅ リファクタリング強力<br>✅ コード補完優秀<br>✅ デバッガ高機能<br>✅ Spring統合 | ❌ 有料（Community版制限）<br>❌ メモリ使用量大<br>❌ 起動遅い<br>❌ 学習曲線急 |
| 3 | **Visual Studio** | [https://visualstudio.microsoft.com/](https://visualstudio.microsoft.com/) | Microsoft製フル機能IDE。.NET開発に最適化 | .NET開発、C#、ASP.NET、Azure統合、プロファイリング | ✅ .NET開発最適<br>✅ デバッガ非常に強力<br>✅ プロファイリング充実<br>✅ Azure統合<br>✅ Community版無料 | ❌ Windows中心<br>❌ 重い（数GB必要）<br>❌ 起動遅い<br>❌ .NET以外使いにくい |
| 4 | **PyCharm** | [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/) | JetBrains製Python専用IDE。Django/Flask対応 | Python開発、Django/Flask、Jupyter、データサイエンス | ✅ Python特化<br>✅ Django/Flask統合<br>✅ Jupyter対応<br>✅ データサイエンスツール<br>✅ リモート開発 | ❌ Professional版有料<br>❌ メモリ使用量大<br>❌ 起動遅い<br>❌ 軽量スクリプトには過剰 |
| 5 | **WebStorm** | [https://www.jetbrains.com/webstorm/](https://www.jetbrains.com/webstorm/) | JetBrains製JS/TS専用IDE。フロントエンド開発最適化 | JavaScript/TypeScript、Node.js、React/Vue/Angular | ✅ JS/TS特化<br>✅ Node/React/Vue統合<br>✅ デバッグ強力<br>✅ リファクタリング優秀<br>✅ パッケージ管理統合 | ❌ 有料（年$69）<br>❌ VSCodeで代替可<br>❌ メモリ使用量大<br>❌ 小規模PJには過剰 |

### バージョン管理（Top 5）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Git** | [https://git-scm.com/](https://git-scm.com/) | 分散型バージョン管理システム。業界標準 | ソースコード管理、ブランチ管理、履歴管理、コラボレーション | ✅ 業界標準<br>✅ 完全無料<br>✅ 分散型で高速<br>✅ ブランチ管理強力<br>✅ 全プラットフォーム対応 | ❌ 学習曲線やや急<br>❌ GUI必要<br>❌ 大容量ファイル苦手<br>❌ コンフリクト解決難しい |
| 2 | **GitHub** | [https://github.com/](https://github.com/) | 世界最大Gitホスティング。PR、CI/CD、コラボレーション | Gitリポジトリホスティング、PR、コードレビュー、CI/CD | ✅ 最大ユーザーベース<br>✅ PR・レビュー優秀<br>✅ Actions（CI/CD）<br>✅ OSS無料<br>✅ Copilot等AI機能 | ❌ プライベートリポジトリ制限（無料）<br>❌ Microsoft傘下<br>❌ セルフホスト不可<br>❌ 中国等で接続困難 |
| 3 | **GitLab** | [https://gitlab.com/](https://gitlab.com/) | DevOps統合プラットフォーム。CI/CD、セキュリティスキャン内蔵 | Git管理、CI/CD、DevSecOps、コンテナレジストリ | ✅ CI/CD完全統合<br>✅ セルフホスト可能<br>✅ DevSecOps機能<br>✅ コンテナレジストリ<br>✅ 無料プラン充実 | ❌ UIやや複雑<br>❌ GitHubよりユーザー少<br>❌ セルフホスト運用コスト<br>❌ 一部機能有料版限定 |
| 4 | **Bitbucket** | [https://bitbucket.org/](https://bitbucket.org/) | Atlassian製Gitホスティング。JIRA/Confluence統合 | Git管理、JIRA統合、PR、Bamboo CI連携 | ✅ JIRA完全統合<br>✅ Atlassianエコシステム<br>✅ 小規模チーム無料<br>✅ PR機能充実<br>✅ Bamboo CI連携 | ❌ GitHubより知名度低<br>❌ コミュニティ小<br>❌ Atlassian依存<br>❌ UI改善余地 |
| 5 | **Azure DevOps Repos** | [https://azure.microsoft.com/ja-jp/products/devops/repos/](https://azure.microsoft.com/ja-jp/products/devops/repos/) | Microsoft製Git管理。Azure DevOps統合 | Git管理、PR、Azure統合、エンタープライズ向け | ✅ Azure完全統合<br>✅ Git/TFVC両対応<br>✅ エンタープライズ機能<br>✅ 小規模無料（5ユーザー）<br>✅ PRポリシー詳細 | ❌ Azure以外では利点薄<br>❌ UI複雑<br>❌ OSSコミュニティ小<br>❌ 学習コスト高 |

### AI コード補完（Top 3）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **GitHub Copilot** | [https://github.com/features/copilot](https://github.com/features/copilot) | OpenAI Codex AIペアプログラマー | コード補完、コード生成、コメントからコード生成、リファクタリング | ✅ コード生成速度速い<br>✅ 多言語対応<br>✅ VSCode/JetBrains統合<br>✅ コメントからコード生成<br>✅ 生産性大幅向上 | ❌ 月額$10（有料）<br>❌ 生成コード品質ばらつき<br>❌ ライセンス問題懸念<br>❌ インターネット必須 |
| 2 | **Cursor** | [https://cursor.sh/](https://cursor.sh/) | AI統合型コードエディタ。VSCodeベースAI強化 | AI支援コーディング、コード編集・生成、チャット形式修正 | ✅ AI機能強力<br>✅ コード編集・生成直感的<br>✅ VSCode拡張互換<br>✅ チャット形式修正<br>✅ リファクタリング支援 | ❌ 有料プラン推奨（月$20）<br>❌ 新しく安定性に課題<br>❌ AI依存強い<br>❌ オフライン不可 |
| 3 | **Amazon CodeWhisperer** | [https://aws.amazon.com/codewhisperer/](https://aws.amazon.com/codewhisperer/) | AWS製AIコード生成。個人利用無料 | コード補完、セキュリティスキャン、リファレンス追跡 | ✅ 個人利用無料<br>✅ セキュリティスキャン内蔵<br>✅ リファレンス追跡<br>✅ AWS SDK最適化<br>✅ VSCode/JetBrains対応 | ❌ Copilot比で精度劣る<br>❌ AWS寄り<br>❌ 言語サポート限定的<br>❌ 企業利用は有料 |

---

## 5.2 インフラ構築

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

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Terraform** | [https://www.terraform.io/](https://www.terraform.io/) | HashiCorp製マルチクラウドIaC。HCL言語、状態管理、モジュール化 | マルチクラウドインフラ構築、状態管理、モジュール再利用 | ✅ マルチクラウド対応<br>✅ 業界標準・実績豊富<br>✅ モジュール化・再利用容易<br>✅ 状態管理優秀<br>✅ プラン機能で事前確認 | ❌ 状態ファイル管理必要<br>❌ 学習曲線やや急<br>❌ エラーメッセージ分かりにくい<br>❌ 一部機能有料（Cloud） |
| 2 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | AWSネイティブIaC。JSON/YAMLテンプレート、スタック管理 | AWSインフラ構築、スタック管理、ドリフト検出 | ✅ AWS完全統合<br>✅ 無料（AWS料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ AWS専用<br>❌ JSON/YAML冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る |
| 3 | **Azure Bicep** | [https://learn.microsoft.com/azure/azure-resource-manager/bicep/](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | Azure IaC DSL。ARM Templatesより簡潔、型安全 | Azureインフラ構築、リソースプロビジョニング、IaC | ✅ ARM Templatesより簡潔<br>✅ 型安全・IDE補完<br>✅ ARM自動変換<br>✅ 無料<br>✅ モジュール化 | ❌ Azure専用<br>❌ 比較的新しい<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 4 | **Ansible** | [https://www.ansible.com/](https://www.ansible.com/) | Red Hat製構成管理・自動化ツール。エージェントレス、YAML | サーバー構成管理、OS設定、ミドルウェア設定、デプロイ | ✅ エージェントレス<br>✅ YAML記述シンプル<br>✅ 構成管理・デプロイ両対応<br>✅ 学習曲線緩やか<br>✅ 無料オープンソース | ❌ 状態管理なし（べき等性は自己実装）<br>❌ 大規模で遅い<br>❌ エラーハンドリング弱い<br>❌ Windows対応やや弱い |
| 5 | **Pulumi** | [https://www.pulumi.com/](https://www.pulumi.com/) | プログラマブルIaC。TypeScript/Python/Go/C#、既存言語活用 | プログラマブルインフラ構築、既存言語でIaC、テスト容易 | ✅ 既存言語使用（TS/Python等）<br>✅ IDEサポート・補完<br>✅ テスト容易<br>✅ マルチクラウド対応<br>✅ 状態管理自動 | ❌ 比較的新しい（2018〜）<br>❌ Terraformより情報少ない<br>❌ 一部機能有料<br>❌ 言語依存性高い |
| 6 | **AWS CDK** | [https://aws.amazon.com/cdk/](https://aws.amazon.com/cdk/) | AWSプログラマブルIaC。TypeScript/Python/Java/C#、CloudFormation生成 | プログラマブルAWSインフラ構築、高レベル抽象化 | ✅ 既存言語使用可能<br>✅ 高レベル抽象化<br>✅ CloudFormation自動生成<br>✅ IDE補完・型チェック<br>✅ 無料 | ❌ AWS専用<br>❌ CloudFormation依存<br>❌ 学習コストあり<br>❌ デバッグ難しい場合あり |
| 7 | **Packer** | [https://www.packer.io/](https://www.packer.io/) | HashiCorp製マシンイメージビルドツール。AMI、Docker、VM等 | マシンイメージ作成、AMI/コンテナビルド、イミュータブルインフラ | ✅ マルチプラットフォーム<br>✅ イミュータブルインフラ<br>✅ 並列ビルド<br>✅ プロビジョナー豊富<br>✅ 無料オープンソース | ❌ イメージビルド専用<br>❌ 状態管理なし<br>❌ 学習コストあり<br>❌ ビルド時間長い |
| 8 | **Vagrant** | [https://www.vagrantup.com/](https://www.vagrantup.com/) | HashiCorp製開発環境構築ツール。VirtualBox/VMware/Docker対応 | ローカル開発環境構築、環境再現、チーム環境統一 | ✅ 開発環境統一<br>✅ シンプル設定<br>✅ プロビジョナー統合<br>✅ マルチプロバイダ<br>✅ 無料オープンソース | ❌ 本番環境不向き<br>❌ リソース使用量大<br>❌ ネットワーク設定複雑<br>❌ DockerComposeで代替可 |
| 9 | **Chef** | [https://www.chef.io/](https://www.chef.io/) | 構成管理ツール。Ruby DSL、インフラをコードで管理 | サーバー構成管理、コンプライアンス、自動化 | ✅ 大規模環境実績<br>✅ エンタープライズ機能<br>✅ コンプライアンス管理<br>✅ クラウド統合<br>✅ コミュニティ大きい | ❌ 学習曲線非常に急<br>❌ Ruby知識必要<br>❌ エージェント必要<br>❌ Ansibleより複雑 |
| 10 | **SaltStack** | [https://saltproject.io/](https://saltproject.io/) | Python製構成管理・リモート実行ツール。高速、スケーラブル | 大規模構成管理、リモート実行、イベント駆動 | ✅ 高速（ZeroMQ）<br>✅ スケーラブル<br>✅ リモート実行強力<br>✅ イベント駆動<br>✅ 無料オープンソース | ❌ 学習曲線急<br>❌ ドキュメント分かりにくい<br>❌ Ansibleより複雑<br>❌ エージェント推奨 |

### その他利用可能なツール

- Terragrunt（Terraform DRY化）
- ARM Templates（Azure標準IaC）
- Google Cloud Deployment Manager（GCP IaC）
- Crossplane（Kubernetesベース IaC）
- Puppet（構成管理）
- CFEngine（構成管理）
- NixOS（宣言的Linux）

---

## クラウドサービス（Azure / AWS）

実装フェーズでは、開発環境、CI/CD、コンテナ、コード管理のためのクラウドサービスを活用します。

### Azure サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Azure DevOps** | [https://azure.microsoft.com/ja-jp/products/devops/](https://azure.microsoft.com/ja-jp/products/devops/) | 統合DevOpsプラットフォーム。Repos、Pipelines、Boards統合 | Git管理、CI/CD、課題管理、アーティファクト管理 | ✅ 統合DevOps環境<br>✅ CI/CD強力<br>✅ Azure統合<br>✅ 5ユーザーまで無料<br>✅ YAML/GUI両対応 | ❌ UI複雑<br>❌ 学習コスト高<br>❌ Azure以外利点薄い<br>❌ セットアップやや面倒 |
| 2 | **Azure Pipelines** | [https://azure.microsoft.com/ja-jp/products/devops/pipelines/](https://azure.microsoft.com/ja-jp/products/devops/pipelines/) | CI/CDサービス。マルチプラットフォーム、並列ジョブ | CI/CD、ビルド、テスト、デプロイ自動化 | ✅ 月1800分無料<br>✅ マルチプラットフォーム<br>✅ GitHub統合<br>✅ YAML/ビジュアル<br>✅ 並列ジョブ | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ GitHub Actionsより情報少ない<br>❌ Azure外利点薄い |
| 3 | **Azure Container Registry** | [https://azure.microsoft.com/ja-jp/products/container-registry/](https://azure.microsoft.com/ja-jp/products/container-registry/) | プライベートDockerレジストリ。イメージ管理、脆弱性スキャン | Dockerイメージ管理、脆弱性スキャン、Geo-Replication | ✅ Azure統合<br>✅ 脆弱性スキャン<br>✅ Geo-Replication<br>✅ Webhooks<br>✅ アクセス制御 | ❌ Docker Hub比で高額<br>❌ 設定やや複雑<br>❌ 他クラウドとの連携弱い<br>❌ 一部機能有料版限定 |
| 4 | **Azure App Service** | [https://azure.microsoft.com/ja-jp/products/app-service/](https://azure.microsoft.com/ja-jp/products/app-service/) | フルマネージドWebアプリホスティング。CI/CD統合 | Webアプリデプロイ、開発環境、ステージング環境 | ✅ フルマネージド<br>✅ CI/CD統合<br>✅ スロット（ステージング）<br>✅ スケーリング自動<br>✅ 多言語対応 | ❌ コスト予測難しい<br>❌ ベンダーロックイン<br>❌ カスタマイズ制限<br>❌ コールドスタート遅延 |
| 5 | **GitHub Codespaces** | [https://github.com/features/codespaces](https://github.com/features/codespaces) | クラウド開発環境。VSCodeブラウザ版、即座セットアップ | クラウド開発環境、リモート開発、環境統一 | ✅ 環境セットアップ不要<br>✅ VSCode統合<br>✅ GPU対応<br>✅ dotfiles同期<br>✅ 無料枠あり | ❌ 従量課金<br>❌ オフライン不可<br>❌ ネットワーク依存<br>❌ カスタマイズ制限 |

### AWS サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **AWS CodeCommit** | [https://aws.amazon.com/codecommit/](https://aws.amazon.com/codecommit/) | フルマネージドGitリポジトリ。セキュア、スケーラブル | プライベートGitリポジトリ、ソースコード管理 | ✅ フルマネージド<br>✅ 無制限リポジトリ<br>✅ IAM統合<br>✅ 暗号化<br>✅ 5ユーザーまで無料 | ❌ GitHubより機能少ない<br>❌ コミュニティ小<br>❌ UI基本的<br>❌ エコシステム弱い |
| 2 | **AWS CodeBuild** | [https://aws.amazon.com/codebuild/](https://aws.amazon.com/codebuild/) | フルマネージドビルドサービス。Docker対応、従量課金 | CI/CD、ビルド、テスト実行、Dockerイメージビルド | ✅ フルマネージド<br>✅ スケーラブル<br>✅ Docker対応<br>✅ 並列ビルド<br>✅ 従量課金 | ❌ 設定複雑<br>❌ デバッグ困難<br>❌ コスト予測難しい<br>❌ GitHub Actions比で機能劣る |
| 3 | **AWS CodePipeline** | [https://aws.amazon.com/codepipeline/](https://aws.amazon.com/codepipeline/) | フルマネージドCI/CD。ビルド、テスト、デプロイ自動化 | CI/CD、リリースパイプライン、デプロイ自動化 | ✅ AWSサービス統合<br>✅ フルマネージド<br>✅ ビジュアルパイプライン<br>✅ 並列/連続実行<br>✅ 従量課金 | ❌ AWS依存<br>❌ 学習曲線急<br>❌ AWS外利用困難<br>❌ コスト予測難しい |
| 4 | **Amazon ECR** | [https://aws.amazon.com/ecr/](https://aws.amazon.com/ecr/) | フルマネージドDockerレジストリ。脆弱性スキャン、イメージ署名 | Dockerイメージ管理、脆弱性スキャン、ECS/EKS統合 | ✅ AWS統合<br>✅ 脆弱性スキャン<br>✅ イメージ署名<br>✅ ライフサイクルポリシー<br>✅ IAM統合 | ❌ Docker Hub比で高額<br>❌ リージョン間転送コスト<br>❌ 設定やや複雑<br>❌ 他クラウド連携弱い |
| 5 | **AWS Cloud9** | [https://aws.amazon.com/cloud9/](https://aws.amazon.com/cloud9/) | クラウド統合開発環境。ブラウザベース、リアルタイム協業 | クラウドIDE、ペアプログラミング、サーバーレス開発 | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ サーバーレス開発最適<br>✅ ターミナル統合<br>✅ 無料（EC2料金のみ） | ❌ ローカルIDEより機能劣る<br>❌ ネットワーク依存<br>❌ カスタマイズ制限<br>❌ オフライン不可 |
| 6 | **AWS Lambda** | [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/) | サーバーレスコンピューティング。イベント駆動、自動スケール | サーバーレス実装、API実装、イベント処理 | ✅ サーバーレス<br>✅ 自動スケール<br>✅ 従量課金<br>✅ 多言語対応<br>✅ 無料枠充実 | ❌ コールドスタート遅延<br>❌ デバッグ困難<br>❌ ステートレス設計必要<br>❌ 実行時間制限（15分） |

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
