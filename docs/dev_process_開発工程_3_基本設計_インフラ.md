# 開発工程_3_基本設計（インフラ）

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**基本設計プロセス（インフラ基本設計）**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

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

**関連ドキュメント**:
- [3. 基本設計（アプリケーション）](./dev_process_開発工程_3_基本設計_アプリケーション.md)
- [4. 詳細設計](./dev_process_開発工程_4_詳細設計.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
