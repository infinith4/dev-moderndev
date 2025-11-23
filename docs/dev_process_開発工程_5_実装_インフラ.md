# 開発工程_5_実装（インフラ）

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**実装プロセス（インフラ構築）**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

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

**関連ドキュメント**:
- [5. 実装（アプリケーション）](./dev_process_開発工程_5_実装_アプリケーション.md)
- [6. アプリケーションテスト](./dev_process_開発工程_6_アプリケーションテスト.md)
- [7. インフラテスト](./dev_process_開発工程_7_インフラテスト.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
