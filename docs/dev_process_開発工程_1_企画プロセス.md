# 開発工程_1_企画プロセス

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**企画プロセス**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 1.1 システム化構想の立案プロセス

### 主要タスク
- 経営要求、経営課題の確認
- 対象となる業務の明確化
- 業務の方向性の明確化
- システム化構想の立案
- システム化構想の承認

### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Miro** | [https://miro.com/](https://miro.com/) | オンラインホワイトボード。リアルタイム協業とアイデア整理 | ブレインストーミング、アイデア整理、ワークショップ、マインドマップ | ✅ リアルタイム協業優秀<br>✅ テンプレート豊富<br>✅ 直感的UI<br>✅ 外部ツール統合<br>✅ 無限キャンバス | ❌ 無料版機能制限<br>❌ 大規模ボード重い<br>❌ オフライン不可<br>❌ 有料版やや高額（$8/月〜） |
| 2 | **Notion** | [https://www.notion.so/](https://www.notion.so/) | オールインワンワークスペース。ドキュメント、Wiki、タスク管理統合 | ドキュメント管理、ナレッジベース、プロジェクト管理、議事録 | ✅ 多機能統合<br>✅ カスタマイズ性高い<br>✅ データベース機能<br>✅ テンプレート豊富<br>✅ 個人利用無料 | ❌ 学習曲線やや急<br>❌ オフライン機能限定的<br>❌ 大量データで遅い<br>❌ 検索機能やや弱い |
| 3 | **Microsoft Visio** | [https://www.microsoft.com/microsoft-365/visio/](https://www.microsoft.com/microsoft-365/visio/) | プロフェッショナル図表作成ツール。プロセスフロー、組織図、ネットワーク図 | プロセスフロー図、業務フロー可視化、組織図、システム構成図 | ✅ Microsoft 365統合<br>✅ 図形ライブラリ豊富<br>✅ エンタープライズ標準<br>✅ データ連携機能<br>✅ 共同編集対応 | ❌ 高額（$5〜15/月）<br>❌ Windows/Web中心<br>❌ 学習コストあり<br>❌ モダンツールより重い |
| 4 | **Lucidchart** | [https://www.lucidchart.com/](https://www.lucidchart.com/) | クラウド図表作成ツール。フローチャート、組織図、システム構成図 | フローチャート、組織図、システム構成図、UML図、ワイヤーフレーム | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ テンプレート豊富<br>✅ Google/Microsoft統合<br>✅ 直感的操作 | ❌ 無料版制限あり<br>❌ 有料版やや高額（$7.95/月〜）<br>❌ オフライン不可<br>❌ 複雑な図は重い |
| 5 | **JIRA** | [https://www.atlassian.com/software/jira](https://www.atlassian.com/software/jira) | Atlassian製プロジェクト管理・課題追跡ツール。アジャイル開発対応 | プロジェクト管理、課題追跡、ロードマップ作成、スプリント管理 | ✅ アジャイル開発に最適<br>✅ カスタマイズ性高い<br>✅ Atlassian統合<br>✅ レポート充実<br>✅ 大規模実績豊富 | ❌ 学習曲線急<br>❌ UI複雑<br>❌ 小規模には過剰<br>❌ 設定が煩雑 |
| 6 | **Confluence** | [https://www.atlassian.com/software/confluence](https://www.atlassian.com/software/confluence) | Atlassian製チーム協業・ナレッジベースツール。ドキュメント管理 | 企画ドキュメント作成、チーム協業、Wiki、テンプレート管理 | ✅ JIRA完全統合<br>✅ テンプレート豊富<br>✅ バージョン管理<br>✅ 権限管理充実<br>✅ マクロ機能強力 | ❌ エディタやや使いにくい<br>❌ 検索機能改善余地<br>❌ 有料（$6.05/月〜）<br>❌ セルフホスト運用負荷 |
| 7 | **Google Workspace** | [https://workspace.google.com/](https://workspace.google.com/) | Google統合オフィススイート。Docs、Sheets、Slides、Drive | リアルタイム共同編集、文書作成、スプレッドシート、プレゼン | ✅ リアルタイム共同編集<br>✅ クラウド自動保存<br>✅ デバイス間同期<br>✅ 無料版充実<br>✅ 直感的UI | ❌ オフライン機能限定的<br>❌ Microsoft Office互換性<br>❌ 複雑な機能少ない<br>❌ 企業版は有料 |
| 8 | **Trello** | [https://trello.com/](https://trello.com/) | Atlassian製カンバンボードツール。視覚的タスク管理 | カンバンボード、タスク管理、視覚的プロジェクト管理、進捗追跡 | ✅ シンプルで直感的<br>✅ 無料版充実<br>✅ Power-Ups拡張<br>✅ モバイル対応<br>✅ 学習容易 | ❌ 大規模管理困難<br>❌ レポート機能弱い<br>❌ ガントチャート別途必要<br>❌ 複雑な依存関係非対応 |
| 9 | **Draw.io (diagrams.net)** | [https://www.diagrams.net/](https://www.diagrams.net/) | 完全無料のオンライン図作成ツール。オープンソース | 図表作成、フローチャート、ネットワーク図、UML図 | ✅ 完全無料<br>✅ オープンソース<br>✅ ブラウザ/デスクトップ両対応<br>✅ Google Drive/GitHub統合<br>✅ 軽量 | ❌ リアルタイム協業弱い<br>❌ テンプレート少ない<br>❌ UI古め<br>❌ 高度機能限定的 |
| 10 | **Asana** | [https://asana.com/](https://asana.com/) | プロジェクト・タスク管理ツール。チーム協業とワークフロー自動化 | タスク管理、プロジェクト計画、チーム協業、ワークフロー管理 | ✅ UI美しく使いやすい<br>✅ ビュー切替（リスト/ボード/タイムライン）<br>✅ 自動化機能<br>✅ 統合豊富<br>✅ 無料版あり | ❌ 無料版制限多い<br>❌ 学習コストあり<br>❌ モバイルアプリやや重い<br>❌ 大規模では有料必須 |

### その他利用可能なツール

11. Microsoft 365 (Word, Excel, PowerPoint)
12. monday.com
13. ClickUp
14. Basecamp
15. Smartsheet
16. FigJam
17. Mural
18. Whimsical
19. Creately
20. MindMeister

---

## 1.2 システム化計画の立案プロセス

### 主要タスク
- 対象業務の分析
- システム化機能の整理
- システム化の方式の策定
- 実施計画の策定
- システム化計画の承認

### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Microsoft Project** | [https://www.microsoft.com/microsoft-365/project/](https://www.microsoft.com/microsoft-365/project/) | Microsoft製プロジェクト管理ツール。ガントチャート、リソース管理 | プロジェクト計画、スケジュール管理、リソース管理、コスト管理 | ✅ エンタープライズ標準<br>✅ 強力なスケジュール機能<br>✅ Microsoft 365統合<br>✅ リソース最適化<br>✅ 詳細レポート | ❌ 高額（$10〜55/月）<br>❌ 学習曲線急<br>❌ Windows中心<br>❌ 小規模には過剰 |
| 2 | **Redmine** | [https://www.redmine.org/](https://www.redmine.org/) | オープンソースプロジェクト管理。課題追跡、ガントチャート、Wiki | プロジェクト管理、ガントチャート、課題管理、時間管理 | ✅ 完全無料オープンソース<br>✅ プラグイン豊富<br>✅ セルフホスト可能<br>✅ カスタマイズ性高い<br>✅ 多言語対応 | ❌ UI古い<br>❌ セットアップ必要<br>❌ モダンツールより機能劣る<br>❌ パフォーマンス課題 |
| 3 | **Lychee Redmine** | [https://lychee-redmine.jp/](https://lychee-redmine.jp/) | Redmine拡張日本製PM。ガントチャート、カンバン、EVM | Redmine拡張、見やすいガントチャート、プロジェクト可視化 | ✅ Redmine完全統合<br>✅ 日本語完全対応<br>✅ UI大幅改善<br>✅ ガントチャート優秀<br>✅ 日本企業向け | ❌ 有料（$10/月〜）<br>❌ Redmine必須<br>❌ 海外知名度低い<br>❌ クラウド版は制限あり |
| 4 | **Backlog** | [https://backlog.com/](https://backlog.com/) | 日本製プロジェクト管理。課題管理、ガントチャート、Git統合 | プロジェクト管理、ガントチャート、バージョン管理、Wiki | ✅ 日本語ネイティブ<br>✅ UI使いやすい<br>✅ Git/SVN統合<br>✅ ガントチャート見やすい<br>✅ 日本企業多数採用 | ❌ 有料（$35/月〜）<br>❌ 海外では知名度低<br>❌ 大規模では高額<br>❌ API制限あり |
| 5 | **Wrike** | [https://www.wrike.com/](https://www.wrike.com/) | クラウドPM。タスク管理、ガントチャート、リソース最適化 | プロジェクト計画、タスク管理、リソース最適化、レポート | ✅ リソース管理強力<br>✅ カスタマイズ性高い<br>✅ 自動化機能<br>✅ 統合豊富<br>✅ テンプレート充実 | ❌ 高額（$9.80/月〜）<br>❌ 学習曲線やや急<br>❌ 無料版機能制限大<br>❌ 日本語サポート限定的 |
| 6 | **Planview** | [https://www.planview.com/](https://www.planview.com/) | エンタープライズPPM。ポートフォリオ管理、リソース最適化 | エンタープライズPPM、ポートフォリオ管理、戦略的計画 | ✅ エンタープライズ向け<br>✅ ポートフォリオ管理強力<br>✅ 戦略的計画対応<br>✅ AI機能<br>✅ 大規模実績 | ❌ 非常に高額<br>❌ 複雑で学習困難<br>❌ 中小企業には過剰<br>❌ 導入コスト高い |
| 7 | **Teamwork** | [https://www.teamwork.com/](https://www.teamwork.com/) | プロジェクト管理・収益性追跡。時間管理、請求書発行 | プロジェクト管理、時間追跡、収益性分析、クライアント管理 | ✅ 時間追跡優秀<br>✅ 収益性分析<br>✅ 請求書機能<br>✅ クライアント管理<br>✅ UI使いやすい | ❌ 有料（$10/月〜）<br>❌ 一部機能高額プラン限定<br>❌ ガントチャート基本的<br>❌ 大規模では高額 |
| 8 | **ProofHub** | [https://www.proofhub.com/](https://www.proofhub.com/) | オールインワンPM。ガントチャート、タイムトラッキング、校正機能 | オールインワンPM、ガントチャート、タイムトラッキング、校正 | ✅ 買い切りプランあり<br>✅ ユーザー数無制限<br>✅ 校正機能内蔵<br>✅ チャット機能<br>✅ シンプルUI | ❌ 機能やや基本的<br>❌ カスタマイズ性低い<br>❌ 統合少ない<br>❌ モバイルアプリ改善余地 |
| 9 | **OpenProject** | [https://www.openproject.org/](https://www.openproject.org/) | オープンソースPM。アジャイル対応、ガントチャート、コスト管理 | オープンソースPM、アジャイル対応、ガントチャート、コスト追跡 | ✅ オープンソース<br>✅ セルフホスト可能<br>✅ アジャイル/ウォーターフォール両対応<br>✅ ガントチャート優秀<br>✅ Community版無料 | ❌ セットアップ必要<br>❌ UI改善余地<br>❌ 一部機能有料版限定<br>❌ サポート限定的 |
| 10 | **GanttProject** | [https://www.ganttproject.biz/](https://www.ganttproject.biz/) | デスクトップガントチャートツール。完全無料、オフライン利用 | デスクトップガントチャート、プロジェクト計画、オフライン作業 | ✅ 完全無料<br>✅ オープンソース<br>✅ オフライン利用可<br>✅ シンプルで軽量<br>✅ クロスプラットフォーム | ❌ クラウド機能なし<br>❌ チーム協業困難<br>❌ 機能基本的<br>❌ UI古い |

### その他利用可能なツール

21. Smartsheet
22. Airtable
23. ClickUp
24. Monday.com
25. Atlassian Portfolio

---

## クラウドサービス（Azure / AWS）

企画フェーズでは主にドキュメント管理、コラボレーションツールとしてクラウドサービスを活用します。

### Azure サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Azure DevOps Boards** | [https://azure.microsoft.com/ja-jp/products/devops/boards/](https://azure.microsoft.com/ja-jp/products/devops/boards/) | プロジェクト計画・追跡ツール。カンバン、スプリント、クエリ | 課題管理、スプリント計画、バックログ管理、レポート | ✅ Azure統合優秀<br>✅ カスタマイズ可能<br>✅ 5ユーザーまで無料<br>✅ テンプレート豊富<br>✅ レポート機能充実 | ❌ UI複雑<br>❌ 学習コスト高い<br>❌ Azure以外では利点薄い<br>❌ セットアップやや面倒 |
| 2 | **Microsoft 365 (Azure AD統合)** | [https://www.microsoft.com/microsoft-365](https://www.microsoft.com/microsoft-365) | Azure Active Directory統合のMicrosoft 365。シームレスな認証 | 企画ドキュメント作成、共同編集、ファイル共有 | ✅ Azure AD統合<br>✅ シングルサインオン<br>✅ 高度なセキュリティ<br>✅ コンプライアンス機能<br>✅ Teams統合 | ❌ 有料（$6/月〜）<br>❌ ライセンス複雑<br>❌ 管理者設定必要<br>❌ オンプレ移行困難 |
| 3 | **Azure Repos** | [https://azure.microsoft.com/ja-jp/products/devops/repos/](https://azure.microsoft.com/ja-jp/products/devops/repos/) | Git リポジトリホスティング。コード管理、レビュー | ドキュメントバージョン管理、設計書・仕様書のGit管理 | ✅ 無制限プライベートリポジトリ<br>✅ Azure DevOps統合<br>✅ PRレビュー機能<br>✅ ブランチポリシー<br>✅ 無料プランあり | ❌ GitHub比で機能少ない<br>❌ UI複雑<br>❌ コミュニティ小さい<br>❌ Azureアカウント必要 |

### AWS サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **AWS WorkDocs** | [https://aws.amazon.com/workdocs/](https://aws.amazon.com/workdocs/) | フルマネージド文書ストレージ・共同編集サービス | 企画ドキュメント保存、共同編集、コメント・フィードバック | ✅ 1TBストレージ<br>✅ リアルタイム共同編集<br>✅ バージョン管理<br>✅ コメント・承認機能<br>✅ AWS統合 | ❌ Microsoft 365より機能少ない<br>❌ デスクトップアプリ弱い<br>❌ 日本語サポート限定的<br>❌ エコシステム小 |
| 2 | **Amazon Chime** | [https://aws.amazon.com/chime/](https://aws.amazon.com/chime/) | ビデオ会議・チャットサービス。画面共有、レコーディング | オンライン会議、企画ミーティング、画面共有、ブレインストーミング | ✅ AWS統合<br>✅ セキュアな通信<br>✅ 画面共有・レコーディング<br>✅ 従量課金<br>✅ プラグイン不要 | ❌ Zoom/Teams比で機能少ない<br>❌ ユーザーインターフェース改善余地<br>❌ 市場シェア低い<br>❌ エコシステム小 |
| 3 | **AWS Wickr** | [https://aws.amazon.com/wickr/](https://aws.amazon.com/wickr/) | エンドツーエンド暗号化メッセージングサービス | 機密性の高い企画情報のセキュアな共有、チャット | ✅ エンドツーエンド暗号化<br>✅ FIPS 140-2準拠<br>✅ コンプライアンス対応<br>✅ ファイル共有暗号化<br>✅ 自己破壊メッセージ | ❌ 一般的なチャットツールより複雑<br>❌ 有料プランのみ<br>❌ 学習コスト<br>❌ 統合限定的 |

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
