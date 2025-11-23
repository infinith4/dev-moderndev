# 開発工程_3_基本設計

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**基本設計プロセス**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 3.1 アプリケーション基本設計

### 3.1.1 システム方式設計

#### 主要タスク
- システム方式の策定
- システム構成の定義
- 外部インタフェースの定義
- ユーザインタフェースの設計
- データベース方式の設計

#### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Next Design** | [https://www.nextdesign.app/](https://www.nextdesign.app/) | 日本製モデリングツール。トレーサビリティと設計自動反映に強み | システム設計、要件トレーサビリティ、モデリング、設計書生成 | ✅ 日本語完全対応<br>✅ トレーサビリティ管理<br>✅ 設計変更自動反映<br>✅ カスタマイズ性高い<br>✅ 日本のシステム開発に最適化 | ❌ 知名度低い（海外）<br>❌ 高額<br>❌ 学習曲線やや急<br>❌ コミュニティ小さい |
| 2 | **astah*** | [https://astah.net/](https://astah.net/) | 日本製UMLツール。UML、フローチャート、ER図、マインドマップ対応 | UML図作成、ER図、フローチャート、システム設計 | ✅ 日本語ネイティブ<br>✅ 買い切り可能<br>✅ 軽量で高速<br>✅ 多様な図に対応<br>✅ 教育機関無料 | ❌ Enterprise Architectより機能少<br>❌ 海外シェア低い<br>❌ クラウド機能弱い<br>❌ コラボ機能限定的 |
| 3 | **Enterprise Architect** | [https://sparxsystems.com/](https://sparxsystems.com/) | 多機能UMLモデリングツール。エンタープライズアーキテクチャ設計 | エンタープライズアーキテクチャ設計、UML、コード生成、要件管理 | ✅ 非常に多機能<br>✅ 要件からコード生成まで<br>✅ 多様なモデリング言語対応<br>✅ チーム開発対応<br>✅ 買い切り（$159〜） | ❌ 学習曲線非常に急<br>❌ UI複雑<br>❌ 機能過多で迷う<br>❌ 動作やや重い |
| 4 | **draw.io (diagrams.net)** | [https://www.diagrams.net/](https://www.diagrams.net/) | 無料のオンライン図作成ツール。システム構成図、ネットワーク図など | システム構成図、ネットワーク図、アーキテクチャ図、フローチャート | ✅ 完全無料<br>✅ ブラウザで動作<br>✅ テンプレート豊富<br>✅ Google Drive/GitHub統合<br>✅ インストール不要 | ❌ UML機能は基本的<br>❌ コラボ機能弱い<br>❌ モデリング自動化なし<br>❌ 大規模図は管理困難 |
| 5 | **PlantUML** | [https://plantuml.com/](https://plantuml.com/) | テキストベースUMLツール。コードとして管理、バージョン管理容易 | UML図（クラス図、シーケンス図等）、テキストベース設計書、Git管理 | ✅ テキストで記述<br>✅ Git管理容易<br>✅ CI/CD統合可能<br>✅ 無料オープンソース<br>✅ 多様な図対応 | ❌ テキスト記法学習必要<br>❌ GUI編集不可<br>❌ 複雑な図は困難<br>❌ レイアウト自動で調整困難 |
| 6 | **StarUML** | [https://staruml.io/](https://staruml.io/) | モダンUIのUMLツール。拡張機能とテーマカスタマイズ | UMLモデリング、コード生成・逆生成、設計書作成 | ✅ モダンで美しいUI<br>✅ 軽量で高速<br>✅ 拡張機能対応<br>✅ コード生成・逆生成<br>✅ 安価（$89買い切り） | ❌ Enterprise Architectより機能少<br>❌ チーム開発機能弱い<br>❌ 日本語ドキュメント少ない<br>❌ サポート限定的 |
| 7 | **Visual Paradigm** | [https://www.visual-paradigm.com/](https://www.visual-paradigm.com/) | UML、BPMN、ER図など多様なモデリング。プロジェクト管理統合 | UML/BPMN/ER図、プロジェクト管理、コード生成、シミュレーション | ✅ 多様なダイアグラム<br>✅ BPMNシミュレーション<br>✅ プロジェクト管理統合<br>✅ コード生成豊富<br>✅ チーム開発対応 | ❌ 高額（$99/月〜）<br>❌ 機能過多で複雑<br>❌ 動作やや重い<br>❌ 学習コスト高 |
| 8 | **Cacoo** | [https://cacoo.com/](https://cacoo.com/) | 日本製オンライン図作成ツール。リアルタイム協業に強み | システム構成図、ワイヤーフレーム、フローチャート、共同編集 | ✅ リアルタイム共同編集<br>✅ 日本語完全対応<br>✅ テンプレート豊富<br>✅ プレゼンモード<br>✅ クラウド管理 | ❌ 有料（$6/月〜）<br>❌ UML機能限定的<br>❌ オフライン不可<br>❌ 高度なモデリング不向き |
| 9 | **Structurizr** | [https://structurizr.com/](https://structurizr.com/) | C4モデル専用アーキテクチャ可視化ツール。コードとして管理 | C4モデルアーキテクチャ設計、コードベース設計書、バージョン管理 | ✅ C4モデル特化<br>✅ コードで記述（DSL）<br>✅ バージョン管理容易<br>✅ 自動レイアウト<br>✅ マルチビュー対応 | ❌ C4モデル以外不向き<br>❌ DSL学習必要<br>❌ 有料（$7.50/月〜）<br>❌ GUI編集不可 |
| 10 | **ArchiMate (Archi)** | [https://www.archimatetool.com/](https://www.archimatetool.com/) | エンタープライズアーキテクチャモデリング。ArchiMate標準準拠 | エンタープライズアーキテクチャ、業務・アプリ・技術アーキテクチャ設計 | ✅ 完全無料オープンソース<br>✅ ArchiMate標準準拠<br>✅ EA設計に最適<br>✅ プラグイン拡張可能<br>✅ クロスプラットフォーム | ❌ 学習曲線急<br>❌ ArchiMate知識必須<br>❌ UI古い<br>❌ 小規模開発には過剰 |

### その他利用可能なツール

41. Creately
42. Gliffy
43. C4-PlantUML
44. Mermaid
45. yUML
46. Modelio
47. GenMyModel
48. LucidChart
49. CloudSkew
50. Dia

---

### 3.1.2 ソフトウェア方式設計

#### 主要タスク
- ソフトウェア構成の定義
- ソフトウェア方式の設計
- インタフェースの設計
- データベースの論理設計

---

## 3.2 インフラ基本設計

インフラ基本設計では、システムを稼働させるための基盤となるインフラストラクチャを設計します。

### 主要タスク
- ネットワーク構成の設計
- サーバー構成の設計
- ストレージ設計
- セキュリティ設計（ファイアウォール、アクセス制御）
- 可用性・冗長性設計
- バックアップ・災害復旧設計
- スケーラビリティ設計
- 監視・運用設計

### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Lucidchart** | [https://www.lucidchart.com/](https://www.lucidchart.com/) | クラウド図作成ツール。ネットワーク図、インフラ構成図に強み | ネットワーク図、インフラ構成図、クラウドアーキテクチャ図 | ✅ リアルタイム協業<br>✅ AWS/Azure/GCPアイコン豊富<br>✅ Visio互換<br>✅ テンプレート充実<br>✅ 自動レイアウト | ❌ 有料（$7.95/月〜）<br>❌ オフライン不可<br>❌ 複雑な図は遅い<br>❌ IaC生成不可 |
| 2 | **CloudCraft** | [https://www.cloudcraft.co/](https://www.cloudcraft.co/) | AWS/Azureインフラ可視化ツール。3D/2D図、コスト見積、実インフラスキャン | AWSアーキテクチャ図、コスト見積、インフラ可視化 | ✅ 美しい3D図<br>✅ リアルタイムコスト見積<br>✅ AWSアカウント連携<br>✅ 実インフラスキャン<br>✅ エクスポート豊富 | ❌ AWS/Azure専用<br>❌ 有料（$49/月〜）<br>❌ GCP非対応<br>❌ オンプレ環境非対応 |
| 3 | **draw.io (diagrams.net)** | [https://www.diagrams.net/](https://www.diagrams.net/) | 無料の図作成ツール。AWS/Azure/GCPアイコン対応 | インフラ構成図、ネットワーク図、システム構成図 | ✅ 完全無料<br>✅ AWS/Azure/GCPアイコン<br>✅ オフライン利用可<br>✅ Git連携<br>✅ インストール不要 | ❌ コスト見積不可<br>❌ 実インフラ連携なし<br>❌ コラボ機能弱い<br>❌ 自動レイアウト弱い |
| 4 | **Microsoft Visio** | [https://www.microsoft.com/microsoft-365/visio/](https://www.microsoft.com/microsoft-365/visio/) | Microsoftの図作成ツール。ネットワーク図、フロア図に強み | ネットワーク図、ラック図、データセンターレイアウト、フローチャート | ✅ エンタープライズ標準<br>✅ 豊富なステンシル<br>✅ Microsoft 365統合<br>✅ 高度な図作成<br>✅ データリンク機能 | ❌ 高額（$5〜15/月）<br>❌ Windows中心<br>❌ クラウド図はLucidchart推奨<br>❌ 学習曲線やや急 |
| 5 | **Terraform** | [https://www.terraform.io/](https://www.terraform.io/) | IaCツール。設計段階からコードで記述、マルチクラウド対応 | インフラ設計をコード化、マルチクラウドリソース定義、状態管理 | ✅ マルチクラウド対応<br>✅ コードで設計記述<br>✅ 状態管理優秀<br>✅ モジュール再利用<br>✅ プラン機能 | ❌ 学習曲線急<br>❌ 図の可視化弱い<br>❌ 状態ファイル管理必要<br>❌ 一部機能有料 |
| 6 | **Hava.io** | [https://www.hava.io/](https://www.hava.io/) | クラウドインフラ自動可視化ツール。AWS/Azure/GCP実環境スキャン | 実インフラ自動図生成、ドキュメント自動化、変更追跡 | ✅ 実インフラ自動スキャン<br>✅ ドキュメント自動生成<br>✅ 変更追跡・履歴<br>✅ セキュリティグループ可視化<br>✅ PDF/PNG出力 | ❌ 有料（$149/月〜）<br>❌ 手動編集不可<br>❌ デザインカスタマイズ不可<br>❌ リアルタイムコスト見積なし |
| 7 | **Cloudockit** | [https://www.cloudockit.com/](https://www.cloudockit.com/) | Azure/AWS自動ドキュメント生成ツール。Word/Excel出力 | インフラドキュメント自動生成、構成図、設計書作成 | ✅ 自動ドキュメント生成<br>✅ Word/Excel出力<br>✅ Visio統合<br>✅ スケジュール実行<br>✅ 詳細設計書生成 | ❌ 有料（$400/月〜）<br>❌ 図の美しさやや劣る<br>❌ リアルタイム性低い<br>❌ カスタマイズ困難 |
| 8 | **AWS CloudFormation Designer** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | AWSインフラ視覚設計ツール。CloudFormationテンプレート生成 | AWSインフラ構成図、CloudFormation設計、視覚的設計 | ✅ 無料<br>✅ CloudFormation自動生成<br>✅ ビジュアル設計<br>✅ AWS完全統合<br>✅ テンプレート可視化 | ❌ AWS専用<br>❌ 機能限定的<br>❌ 複雑な構成困難<br>❌ レイアウト自動調整弱い |
| 9 | **PlantUML (C4-PlantUML)** | [https://plantuml.com/](https://plantuml.com/) | テキストベースインフラ図作成。C4モデル、デプロイメント図 | インフラ構成図（コード記述）、デプロイメント図、Git管理 | ✅ テキストで記述<br>✅ Git管理容易<br>✅ バージョン管理<br>✅ CI/CD統合<br>✅ 無料 | ❌ 記法学習必要<br>❌ 複雑な図困難<br>❌ レイアウト制御困難<br>❌ クラウドアイコン少ない |
| 10 | **Diagrams (Python)** | [https://diagrams.mingrammer.com/](https://diagrams.mingrammer.com/) | Pythonコードでクラウドインフラ図生成。AWS/Azure/GCP/K8s対応 | インフラ構成図（Pythonコード）、コードベース図作成、自動生成 | ✅ Pythonで記述<br>✅ Git管理容易<br>✅ AWS/Azure/GCP/K8sアイコン<br>✅ プログラマブル<br>✅ 無料オープンソース | ❌ Python知識必須<br>❌ レイアウト調整困難<br>❌ GUI編集不可<br>❌ コラボ機能なし |

### その他利用可能なツール

- Gliffy
- Creately
- Cacoo
- Miro
- Azure Bicep（IaC）
- AWS CDK（IaC）
- Pulumi（IaC）

---

## クラウドサービス（Azure / AWS）

基本設計フェーズでは、アーキテクチャ設計、インフラ設計、設計レビューのためのクラウドサービスを活用します。

### Azure サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Azure Architecture Center** | [https://learn.microsoft.com/azure/architecture/](https://learn.microsoft.com/azure/architecture/) | Azureアーキテクチャのベストプラクティス集。参照アーキテクチャ、設計パターン | アーキテクチャ設計、ベストプラクティス参照、設計パターン選定 | ✅ Microsoft公式ガイド<br>✅ 詳細な参照アーキテクチャ<br>✅ 無料アクセス<br>✅ 定期的更新<br>✅ コード例豊富 | ❌ Azure特化<br>❌ 情報量膨大で取捨選択必要<br>❌ 日本語翻訳やや遅い<br>❌ 実装詳細は別途調査必要 |
| 2 | **Azure Well-Architected Framework** | [https://learn.microsoft.com/azure/well-architected/](https://learn.microsoft.com/azure/well-architected/) | 5つの柱（コスト最適化、運用性、パフォーマンス、信頼性、セキュリティ）に基づく設計原則 | アーキテクチャレビュー、設計評価、ベストプラクティス適用 | ✅ 体系的な設計原則<br>✅ チェックリスト形式<br>✅ 無料ツール<br>✅ レビュー機能<br>✅ 推奨事項自動生成 | ❌ Azure専用<br>❌ 学習コストあり<br>❌ 全項目対応は困難<br>❌ 実装は別途必要 |
| 3 | **Azure Resource Manager (ARM) Templates** | [https://learn.microsoft.com/azure/azure-resource-manager/](https://learn.microsoft.com/azure/azure-resource-manager/) | インフラをコードで定義。JSON形式、宣言的デプロイ | インフラ設計、リソース構成定義、テンプレート管理 | ✅ Azure標準IaC<br>✅ 宣言的定義<br>✅ バージョン管理可能<br>✅ 再現性高い<br>✅ 無料 | ❌ JSON冗長<br>❌ 学習曲線急<br>❌ Terraform比で機能劣る<br>❌ エラーメッセージ分かりにくい |
| 4 | **Azure Bicep** | [https://learn.microsoft.com/azure/azure-resource-manager/bicep/](https://learn.microsoft.com/azure/azure-resource-manager/bicep/) | ARM Templatesの改良版DSL。簡潔な構文、型安全 | インフラ設計、リソース定義、ARMテンプレート生成 | ✅ ARM Templatesより簡潔<br>✅ 型安全<br>✅ IDE補完対応<br>✅ ARM自動変換<br>✅ 無料 | ❌ 比較的新しい<br>❌ Azure専用<br>❌ Terraformより情報少ない<br>❌ マルチクラウド不可 |
| 5 | **Azure DevOps Wiki** | [https://azure.microsoft.com/ja-jp/products/devops/](https://azure.microsoft.com/ja-jp/products/devops/) | 設計書・仕様書管理Wiki | 設計書作成、アーキテクチャドキュメント、技術仕様書管理 | ✅ Azure DevOps統合<br>✅ Markdown記述<br>✅ Git連携<br>✅ バージョン管理<br>✅ 無料プランあり | ❌ Confluence比で機能少ない<br>❌ UI基本的<br>❌ テンプレート少ない<br>❌ エディタ改善余地 |

### AWS サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **AWS Architecture Center** | [https://aws.amazon.com/architecture/](https://aws.amazon.com/architecture/) | AWSアーキテクチャのベストプラクティス集。参照アーキテクチャ、図表、ホワイトペーパー | アーキテクチャ設計、ベストプラクティス参照、設計パターン選定 | ✅ AWS公式ガイド<br>✅ 詳細な参照アーキテクチャ<br>✅ 無料アクセス<br>✅ ホワイトペーパー豊富<br>✅ 業界別ソリューション | ❌ AWS特化<br>❌ 情報量膨大<br>❌ 日本語翻訳やや遅い<br>❌ 実装詳細は別途調査必要 |
| 2 | **AWS Well-Architected Tool** | [https://aws.amazon.com/well-architected-tool/](https://aws.amazon.com/well-architected-tool/) | 6つの柱に基づくアーキテクチャレビューツール。無料、ベストプラクティス評価 | アーキテクチャレビュー、設計評価、改善提案取得 | ✅ 無料ツール<br>✅ ベストプラクティス評価<br>✅ 改善提案自動生成<br>✅ レポート出力<br>✅ 継続的レビュー | ❌ AWS専用<br>❌ 質問項目多数（学習コスト）<br>❌ 全項目対応は困難<br>❌ 実装は別途必要 |
| 3 | **AWS CloudFormation** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | インフラをコードで定義。YAML/JSON、スタック管理、ドリフト検出 | インフラ設計、リソース構成定義、スタック管理 | ✅ AWS標準IaC<br>✅ 無料（リソース料金のみ）<br>✅ ドリフト検出<br>✅ ChangeSet事前確認<br>✅ AWSサポート対象 | ❌ YAML/JSON冗長<br>❌ エラーロールバック面倒<br>❌ Terraform比で機能劣る<br>❌ AWS専用 |
| 4 | **AWS CloudFormation Designer** | [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/) | ビジュアルインフラ設計ツール。ドラッグ&ドロップでリソース配置 | インフラ構成図作成、CloudFormationテンプレート生成、視覚的設計 | ✅ ビジュアル設計<br>✅ CloudFormation自動生成<br>✅ 無料<br>✅ テンプレート可視化<br>✅ 初心者向け | ❌ 機能限定的<br>❌ 複雑な構成困難<br>❌ 手動編集推奨<br>❌ レイアウト自動調整弱い |
| 5 | **AWS Application Composer** | [https://aws.amazon.com/application-composer/](https://aws.amazon.com/application-composer/) | サーバーレスアプリケーション視覚設計ツール。Lambda、API Gateway等 | サーバーレスアーキテクチャ設計、SAMテンプレート生成、視覚的設計 | ✅ サーバーレス特化<br>✅ ビジュアル設計<br>✅ SAM/CloudFormation生成<br>✅ リアルタイムプレビュー<br>✅ 無料 | ❌ サーバーレス限定<br>❌ 比較的新しい<br>❌ EC2等非対応<br>❌ 複雑なワークフロー困難 |
| 6 | **Amazon WorkDocs** | [https://aws.amazon.com/workdocs/](https://aws.amazon.com/workdocs/) | 設計書・ドキュメント管理 | 設計書保存、レビュー・コメント、バージョン管理、承認フロー | ✅ 1TBストレージ<br>✅ バージョン管理<br>✅ コメント・承認機能<br>✅ AWS統合<br>✅ セキュア | ❌ Microsoft 365より機能少ない<br>❌ デスクトップアプリ弱い<br>❌ 日本語サポート限定的<br>❌ エコシステム小 |

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
