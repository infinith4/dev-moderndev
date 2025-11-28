# 開発工程_2_要件定義

## 1. 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**要件定義プロセス**における開発タスクと推奨ツールをまとめたものです。

### 1.1. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

### 1.2. 共通

**対応項目**
- 利害関係者の識別
- 要求事項の識別
- 要求事項の評価
- システム要件の定義
- システム要件の評価
- システム要件の合意

**推奨ツール（生産性が高いもの Top 10）**

| # | ツール名 | 概要 | 用途 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|---------|-----------|---------------|---------------|
| 1 | [**ONES Wiki**](https://ones.com/) | AI活用の要件定義・ナレッジ管理ツール。ドキュメントコラボレーション強化 | 要件定義書作成、AI支援、ナレッジ管理、チーム協業 | ✅ AI要件定義支援<br>✅ リアルタイム共同編集<br>✅ ナレッジ蓄積・検索<br>✅ プロジェクト管理統合<br>✅ テンプレート豊富 | ❌ 比較的新しいサービス<br>❌ 日本語情報少ない<br>❌ 有料プラン必須<br>❌ 他ツールとの連携限定的 | AI補助を活用して自然言語から要件定義書を生成。テンプレートからページ作成し、チームで共同編集。 | [公式ドキュメント](https://ones.com/wiki) |
| 2 | [**Confluence**](https://www.atlassian.com/software/confluence) | Atlassian製ナレッジベース。要件定義書作成・チーム協業に最適 | 要件定義書作成、ドキュメント管理、Wiki、承認フロー | ✅ JIRA完全統合<br>✅ 豊富なテンプレート<br>✅ バージョン管理<br>✅ 権限管理詳細<br>✅ 業界標準的存在 | ❌ 有料（$5.75/月〜）<br>❌ 大規模では動作重い<br>❌ UI複雑<br>❌ 検索機能やや弱い | スペース作成→テンプレート選択→要件定義ページ作成→チームで共同編集→JIRA課題とリンク | [公式チュートリアル](https://www.atlassian.com/software/confluence/guides) |
| 3 | [**GEAR.indigo**](https://www.gear-indigo.com/) | 2024年登場のAI駆動要件定義ツール。自然言語から設計書・コード生成 | AI駆動要件定義、自動設計書生成、トレーサビリティ管理 | ✅ AI自動設計書生成<br>✅ 自然言語インターフェース<br>✅ コード自動生成<br>✅ 要件トレーサビリティ<br>✅ 手戻り削減 | ❌ 非常に新しい（実績少）<br>❌ AI精度は発展途上<br>❌ 価格情報不明瞭<br>❌ 日本市場中心 | 自然言語で要件を入力→AI が設計書・ER図・画面設計を自動生成→トレーサビリティマトリクス確認 | [公式サイト](https://www.gear-indigo.com/) |
| 4 | [**Figma**](https://www.figma.com/) | クラウドベースのUIデザインツール。プロトタイプ作成・デザイン仕様共有 | UIプロトタイプ作成、画面設計、デザイン仕様書、レビュー | ✅ ブラウザで完結<br>✅ リアルタイム共同編集<br>✅ プロトタイプ作成簡単<br>✅ デベロッパーハンドオフ<br>✅ 無料プランあり | ❌ オフライン作業不可<br>❌ 複雑な図は不向き<br>❌ プラグイン依存増えがち<br>❌ 大規模ファイルは重い | 新規ファイル作成→フレーム配置→コンポーネント作成→プロトタイプモードで画面遷移設定→共有リンク生成 | [Learn Figma](https://help.figma.com/hc/en-us) |
| 5 | [**VISLITE**](https://www.vislite.com/) | 手戻りゼロを目指す要件定義ツール。要件可視化・トレーサビリティ管理 | 要件可視化、トレーサビリティ管理、手戻り防止、Excel連携 | ✅ 要件の可視化優秀<br>✅ トレーサビリティ管理<br>✅ 手戻り防止機能<br>✅ 日本製で日本語完全対応<br>✅ Excel連携 | ❌ 知名度低い<br>❌ コミュニティ小さい<br>❌ 価格やや高め<br>❌ モダンUIではない | Excelで要件一覧作成→VISLITEにインポート→要件間の関連性を可視化→トレーサビリティマトリクス生成 | [公式マニュアル](https://www.vislite.com/support) |
| 6 | [**Adobe XD**](https://www.adobe.com/products/xd.html) | AdobeのUI/UXデザインツール。プロトタイプ・デザインシステム構築 | UI/UXデザイン、プロトタイプ、デザインシステム、画面遷移 | ✅ Adobe製品統合<br>✅ デザインシステム構築<br>✅ プロトタイプ作成<br>✅ 音声UI対応<br>✅ 無料プランあり | ❌ Figmaに押され気味<br>❌ 開発停止の噂<br>❌ Adobeアカウント必須<br>❌ 重い動作 | アートボード作成→UIコンポーネント配置→プロトタイプモードで画面遷移→プレビュー・共有 | [Adobe XD Learn](https://helpx.adobe.com/xd/tutorials.html) |
| 7 | [**Sketch**](https://www.sketch.com/) | macOS専用UIデザインツール。デザイン業界標準の一つ | UIデザイン、プロトタイプ、デザインシステム、シンボル管理 | ✅ デザイナー愛用<br>✅ プラグイン豊富<br>✅ シンボル管理優秀<br>✅ デザインシステム対応<br>✅ 買い切り可能 | ❌ macOS専用<br>❌ Figmaに市場シェア奪われ中<br>❌ サブスク移行で不評<br>❌ コラボ機能Figma劣る | アートボード作成→シンボル（再利用コンポーネント）作成→レイヤースタイル適用→プラグインで拡張 | [Sketch Documentation](https://www.sketch.com/docs/) |
| 8 | [**Balsamiq**](https://balsamiq.com/) | 手書き風ワイヤーフレームツール。ラピッドプロトタイピングに最適 | 低忠実度ワイヤーフレーム、ラピッドプロトタイピング、初期設計 | ✅ 手書き風で低忠実度<br>✅ 素早くアイデア形成<br>✅ シンプルで学習容易<br>✅ デザイン議論に集中<br>✅ 買い切りプランあり | ❌ デザイン精度低い<br>❌ 最終デザインには不向き<br>❌ 機能限定的<br>❌ モダンではない | 新規プロジェクト作成→UIコントロールをドラッグ&ドロップ→手書き風で配置→PDF/PNG出力 | [Balsamiq Tutorials](https://balsamiq.com/learn/) |
| 9 | [**Axure RP**](https://www.axure.com/) | 高機能プロトタイプツール。インタラクション設計・詳細仕様書生成 | 高度なプロトタイプ、インタラクション設計、仕様書自動生成 | ✅ 高度なインタラクション<br>✅ 動的プロトタイプ<br>✅ 仕様書自動生成<br>✅ 条件分岐・変数対応<br>✅ エンタープライズ実績 | ❌ 学習曲線非常に急<br>❌ 高額（$25/月〜）<br>❌ UI古い<br>❌ 動作やや重い | ページ作成→ウィジェット配置→インタラクション設定（条件・変数）→仕様書自動生成→HTMLプロトタイプ出力 | [Axure Tutorials](https://www.axure.com/support/training) |
| 10 | [**Jama Connect**](https://www.jamasoftware.com/) | エンタープライズ要件管理ツール。トレーサビリティ・バリデーション | 要件管理、トレーサビリティ、承認フロー、規制対応 | ✅ 完全なトレーサビリティ<br>✅ レビュー・承認フロー<br>✅ 規制対応（医療・航空）<br>✅ テスト管理統合<br>✅ 変更影響分析 | ❌ 非常に高額<br>❌ 複雑で習得困難<br>❌ 小規模には過剰<br>❌ セットアップ時間大 | プロジェクト作成→要件アイテム登録→関係性設定→レビューフロー設定→トレーサビリティマトリクス確認 | [Jama Software University](https://community.jamasoftware.com/learn) |

**有用なドキュメント**

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **ユーザのための要件定義ガイド 第2版** | 要件定義における128のポイントを実践的に解説（498ページ）。業界・職種別の要件定義プロセスとテンプレートを提供 | システム要件定義、業務要件定義、要件定義プロセス全般、要件定義書作成 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | PDFをダウンロード→目次から該当章を参照→チェックリスト活用→テンプレート利用 | [PDF直接DL](https://www.ipa.go.jp/archive/files/000071810.pdf) |
| **機能要件の合意形成ガイド（画面編）** | 画面仕様の合意形成手法を解説。画面設計における発注者・受注者間のコミュニケーション改善を支援 | 画面設計、画面仕様書作成、画面レイアウト設計、画面遷移図作成 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→画面設計テンプレート使用→画面一覧・遷移図・レイアウト作成→ステークホルダーと合意 | [機能要件合意形成ガイド](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **機能要件の合意形成ガイド（データモデル編）** | データモデル設計における合意形成手法。ER図作成、正規化プロセスを支援 | データベース論理設計、ER図作成、概念モデリング、データディクショナリ作成 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→概念モデル作成→正規化プロセス実施→ER図作成→データディクショナリ整備 | [機能要件合意形成ガイド](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **機能要件の合意形成ガイド（バッチ編）** | バッチ処理設計における合意形成手法。バッチ設計の標準化を支援 | バッチ処理設計、バッチ仕様書作成、外部インターフェース設計 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→バッチ一覧作成→ジョブネット図作成→外部IF定義→エラーハンドリング設計 | [機能要件合意形成ガイド](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |


<!-- ### その他利用可能なツール

1.  InVision
2.  Marvel
3.  UXPin
4.  Mockplus
5.  Proto.io
6.  Justinmind
7.  Reqtify
8.  DOORS (IBM)
9.  ReqView
10. Modern Requirements
11. Framer
12. Penpot
13. Lunacy
14. ProtoPie
15. Principle -->

## 2. 業務分析

**対応項目**
- 業務分析

**成果物**
- ビジネスプロセス関連図
- 業務機能構成表
- システム化業務フロー

### 2.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Bizagi Modeler**](https://www.bizagi.com/en/products/bpm-suite/modeler) | ビジネスプロセスモデリングツール。BPMN2.0完全準拠 | ビジネスプロセス図作成、BPMN図、業務フロー可視化 | 🟢 完全無料 | ✅ 完全無料<br>✅ BPMN2.0準拠<br>✅ プロセスシミュレーション<br>✅ Word/PDF出力<br>✅ 日本語対応 | ❌ オンライン協業弱い<br>❌ クラウド版は有料<br>❌ UI古め<br>❌ 学習曲線あり | インストール→新規プロセス作成→BPMN要素（タスク、ゲートウェイ等）配置→プロセスフロー作成→シミュレーション→Word/PDF出力 | [Bizagi Documentation](https://help.bizagi.com/bpm-suite/en/) |
| 2 | [**Lucidchart**](https://www.lucidchart.com/) | クラウド図表作成ツール。業務フロー・BPMN対応 | ビジネスプロセス図、フローチャート、組織図、BPMN | 🟢 Free版 / 💰 Individual($7.95/月) | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ テンプレート豊富<br>✅ BPMN対応<br>✅ 統合機能豊富 | ❌ 無料版制限あり<br>❌ 有料版やや高額<br>❌ オフライン不可<br>❌ 複雑な図は重い | アカウント作成→BPMNテンプレート選択→図形ライブラリから要素配置→コネクタで接続→チーム共有 | [Lucidchart Tutorials](https://www.lucidchart.com/pages/tutorial) |
| 3 | [**Microsoft Visio**](https://www.microsoft.com/microsoft-365/visio/) | プロフェッショナル図表作成ツール。業務フロー・組織図作成 | 業務フロー図、組織図、BPMN、プロセスマッピング | 💰 Plan 1($5/月) / 💰 Plan 2($15/月) | ✅ Microsoft 365統合<br>✅ 図形ライブラリ豊富<br>✅ エンタープライズ標準<br>✅ データ連携機能<br>✅ BPMN対応 | ❌ 高額<br>❌ Windows/Web中心<br>❌ 学習コストあり<br>❌ モダンツールより重い | 起動→BPMN/フローチャートテンプレート選択→ステンシルから図形配置→コネクタで接続→データリンク設定 | [Visio Help](https://support.microsoft.com/visio) |
| 4 | [**Draw.io (diagrams.net)**](https://www.diagrams.net/) | 完全無料のオンライン図作成ツール。BPMN・フローチャート対応 | ビジネスプロセス図、フローチャート、BPMN、組織図 | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ ブラウザ/デスクトップ両対応<br>✅ Google Drive統合<br>✅ BPMN対応 | ❌ リアルタイム協業弱い<br>❌ テンプレート少ない<br>❌ UI古め<br>❌ 高度機能限定的 | サイト訪問→保存先選択（Google Drive/OneDrive/ローカル）→BPMNライブラリ選択→図形配置→エクスポート | [Draw.io User Manual](https://www.drawio.com/doc/) |
| 5 | [**Process Street**](https://www.process.st/) | プロセス管理・ワークフロー自動化ツール。チェックリスト・SOP管理 | 業務プロセス標準化、チェックリスト、SOP管理、ワークフロー | 🟢 Free版 / 💰 Pro($25/月) | ✅ プロセス実行管理<br>✅ チェックリスト機能<br>✅ 条件分岐対応<br>✅ データ収集<br>✅ API統合 | ❌ 複雑なBPMNには不向き<br>❌ 有料版高め<br>❌ 日本語情報少ない<br>❌ 図表作成機能弱い | アカウント作成→新規プロセステンプレート作成→タスク・チェックリスト追加→条件分岐設定→実行・モニタリング | [Process Street Academy](https://www.process.st/help/) |

### 2.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **ユーザのための要件定義ガイド 第2版 - 第3章 業務分析** | 業務分析の進め方、現状業務の可視化、問題点抽出手法を解説 | 業務分析、現状業務可視化、業務フロー作成、業務課題抽出 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | PDFダウンロード→第3章参照→現状業務フロー作成→問題点抽出→To-Be業務フロー設計 | [PDF直接DL](https://www.ipa.go.jp/archive/files/000071810.pdf) |
| **BPMN 2.0仕様書** | ビジネスプロセスモデリング表記法の国際標準仕様 | BPMN図作成、プロセスモデリング標準、記法学習 | [OMG公式サイト](https://www.omg.org/spec/BPMN/) | PDFダウンロード→BPMN要素（タスク、イベント、ゲートウェイ）を学習→標準記法に従って業務フロー作成 | [BPMN 2.0 Spec PDF](https://www.omg.org/spec/BPMN/2.0/PDF) |
| **ビジネスプロセスモデリング入門** | IPAによるビジネスプロセスモデリングの基礎解説 | 業務プロセス可視化、モデリング手法、業務改善 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | IPAサイトから資料ダウンロード→プロセスモデリング基礎を学習→実務でのモデリング手法を適用 | [IPA資料一覧](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |

---

## 3. ユースケース分析（機能要件定義）

**対応項目**
- ユースケース分析

**成果物**
- ユースケース図
- ユースケース一覧
- ユースケース記述
- ビジネスルール一覧
- ビジネスルール定義書

### 3.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Enterprise Architect**](https://sparxsystems.com/) | UMLモデリングツール。ユースケース図・クラス図等に対応 | UML図作成、ユースケース図、クラス図、シーケンス図 | 💰 Desktop($159買切) / 💰 Pro($339買切) | ✅ UML完全対応<br>✅ コード生成可能<br>✅ トレーサビリティ管理<br>✅ 買い切りライセンス<br>✅ エンタープライズ実績 | ❌ UI古い<br>❌ 学習曲線急<br>❌ Windows中心<br>❌ クラウド協業弱い | インストール→プロジェクト作成→Use Caseダイアグラム選択→アクター・ユースケース配置→関連線設定→詳細記述追加 | [公式チュートリアル](https://sparxsystems.com/resources/tutorials/) |
| 2 | [**Visual Paradigm**](https://www.visual-paradigm.com/) | UML/SysMLモデリングツール。ユースケース駆動開発支援 | UML図、ユースケース図、アクティビティ図、要件管理 | 🟢 Community版無料 / 💰 Standard($6/月〜) | ✅ UML/SysML対応<br>✅ オンライン協業<br>✅ テンプレート豊富<br>✅ Community版無料<br>✅ アジャイル対応 | ❌ 有料版高額<br>❌ UI複雑<br>❌ 大規模モデル重い<br>❌ 日本語情報少ない | アカウント作成→プロジェクト作成→ユースケース図テンプレート選択→アクター・ユースケース追加→関連設定→HTML出力 | [公式ガイド](https://www.visual-paradigm.com/tutorials/) |
| 3 | [**Lucidchart**](https://www.lucidchart.com/) | クラウド図表作成ツール。UML・ユースケース図対応 | ユースケース図、UML図、フローチャート、ER図 | 🟢 Free版 / 💰 Individual($7.95/月) | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ UMLテンプレート<br>✅ 直感的操作<br>✅ 統合機能豊富 | ❌ 無料版制限あり<br>❌ 厳密なUML検証なし<br>❌ コード生成不可<br>❌ 複雑モデル困難 | アカウント作成→UMLユースケース図テンプレート選択→図形ライブラリからアクター・ユースケース配置→関連線接続→チーム共有 | [Lucidchart UMLガイド](https://www.lucidchart.com/pages/uml-use-case-diagram) |
| 4 | [**Draw.io (diagrams.net)**](https://www.diagrams.net/) | 完全無料のオンライン図作成ツール。UML対応 | ユースケース図、UML図、フローチャート | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ UMLテンプレート<br>✅ Google Drive統合<br>✅ 軽量 | ❌ リアルタイム協業弱い<br>❌ UML検証なし<br>❌ テンプレート少ない<br>❌ 高度機能なし | サイト訪問→保存先選択→UMLライブラリ有効化→アクター・ユースケース図形配置→コネクタ接続→PNG/SVG出力 | [Draw.io UML Tutorial](https://www.drawio.com/blog/uml-use-case-diagrams) |
| 5 | [**PlantUML**](https://plantuml.com/) | テキストベースUML図生成ツール。コードからUML自動生成 | ユースケース図、クラス図、シーケンス図、テキストベースUML | 🟢 完全無料 | ✅ 完全無料<br>✅ テキストベース<br>✅ バージョン管理容易<br>✅ CI/CD統合可能<br>✅ 自動生成 | ❌ GUI編集不可<br>❌ 学習曲線あり<br>❌ レイアウト制御困難<br>❌ 複雑図は困難 | テキストエディタで@startuml記述→アクター・ユースケース定義→関連記述→PlantUMLでレンダリング→PNG/SVG出力 | [PlantUML Use Case](https://plantuml.com/use-case-diagram) |

### 3.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **ユーザのための要件定義ガイド 第2版 - 第4章 機能要件定義** | ユースケース分析の進め方、ユースケース図・記述の作成方法を解説 | ユースケース図作成、ユースケース記述、アクター定義 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | PDFダウンロード→第4章参照→ユースケース抽出手法を学習→ユースケース図・記述テンプレート活用 | [PDF直接DL](https://www.ipa.go.jp/archive/files/000071810.pdf) |
| **UML 2.5仕様書** | UML（統一モデリング言語）の国際標準仕様 | UML図作成、ユースケース図標準、記法学習 | [OMG公式サイト](https://www.omg.org/spec/UML/) | PDFダウンロード→Use Case Diagrams章参照→標準記法に従ってユースケース図作成→関連・汎化等の記法確認 | [UML 2.5 Spec](https://www.omg.org/spec/UML/2.5/PDF) |
| **ビジネスルール管理入門** | ビジネスルールの抽出・管理手法の解説 | ビジネスルール定義、ルール管理、ルール一覧作成 | 各種技術書 | 技術書購入/図書館で借りる→ビジネスルール抽出手法学習→ルール分類・管理手法適用→ルール一覧作成 | 各書籍の出版社サイト |

---

## 4. 画面要件定義（機能要件定義）

**対応項目**
- 画面要件定義

**成果物**
- 画面一覧
- 画面遷移図
- 画面レイアウト

### 4.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Figma**](https://www.figma.com/) | クラウドベースのUIデザインツール。プロトタイプ作成 | 画面設計、UIプロトタイプ、デザイン仕様書、画面遷移図 | 🟢 Free版 / 💰 Professional($12/月) | ✅ ブラウザで完結<br>✅ リアルタイム共同編集<br>✅ プロトタイプ作成簡単<br>✅ デベロッパーハンドオフ<br>✅ 無料プランあり | ❌ オフライン作業不可<br>❌ 複雑な図は不向き<br>❌ プラグイン依存増えがち<br>❌ 大規模ファイルは重い | アカウント作成→新規デザインファイル作成→フレーム配置→コンポーネント作成→プロトタイプモードで画面遷移設定→共有リンク生成 | [Figma Tutorial](https://help.figma.com/hc/en-us/categories/360002051613-Get-started) |
| 2 | [**Adobe XD**](https://www.adobe.com/products/xd.html) | AdobeのUI/UXデザインツール。プロトタイプ作成 | UI/UXデザイン、プロトタイプ、画面遷移、デザインシステム | 🟢 Free Starter / 💰 Single App($11.99/月) | ✅ Adobe製品統合<br>✅ デザインシステム構築<br>✅ プロトタイプ作成<br>✅ 音声UI対応<br>✅ 無料プランあり | ❌ Figmaに押され気味<br>❌ 開発停止の噂<br>❌ Adobeアカウント必須<br>❌ 重い動作 | アカウント作成→アートボード作成→UIコンポーネント配置→プロトタイプモードで遷移設定→プレビュー・共有 | [Adobe XD Learn](https://helpx.adobe.com/xd/tutorials.html) |
| 3 | [**Axure RP**](https://www.axure.com/) | 高機能プロトタイプツール。インタラクション設計・仕様書生成 | 高度なプロトタイプ、画面仕様書、インタラクション設計 | 💰 Pro($25/月) / 💰 Team($42/月) | ✅ 高度なインタラクション<br>✅ 動的プロトタイプ<br>✅ 仕様書自動生成<br>✅ 条件分岐・変数対応<br>✅ エンタープライズ実績 | ❌ 学習曲線非常に急<br>❌ 高額<br>❌ UI古い<br>❌ 動作やや重い | プロジェクト作成→ページ作成→ウィジェット配置→インタラクション設定(条件・変数)→仕様書自動生成→HTMLプロトタイプ出力 | [Axure Tutorials](https://www.axure.com/support/training) |
| 4 | [**Balsamiq**](https://balsamiq.com/) | 手書き風ワイヤーフレームツール。低忠実度プロトタイプ | ワイヤーフレーム、ラピッドプロトタイピング、初期画面設計 | 💰 Cloud($9/月) / 💰 Desktop($89買切) | ✅ 手書き風で低忠実度<br>✅ 素早くアイデア形成<br>✅ シンプルで学習容易<br>✅ デザイン議論に集中<br>✅ 買い切りプランあり | ❌ デザイン精度低い<br>❌ 最終デザインには不向き<br>❌ 機能限定的<br>❌ モダンではない | 新規プロジェクト作成→UIコントロールをドラッグ&ドロップ→手書き風で画面レイアウト作成→リンク設定→PDF/PNG出力 | [Balsamiq Tutorials](https://balsamiq.com/learn/) |
| 5 | [**Sketch**](https://www.sketch.com/) | macOS専用UIデザインツール。画面設計・デザインシステム | UIデザイン、画面設計、デザインシステム、シンボル管理 | 💰 Standard($10/月) / 💰 Business($20/月) | ✅ デザイナー愛用<br>✅ プラグイン豊富<br>✅ シンボル管理優秀<br>✅ デザインシステム対応 | ❌ macOS専用<br>❌ Figmaに市場シェア奪われ中<br>❌ サブスク移行で不評<br>❌ コラボ機能Figma劣る | アートボード作成→シンボル(再利用コンポーネント)作成→レイヤースタイル適用→プラグインで機能拡張→Export | [Sketch Documentation](https://www.sketch.com/docs/) |

### 4.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **機能要件の合意形成ガイド（画面編）** | 画面仕様の合意形成手法を解説。画面設計におけるコミュニケーション改善 | 画面設計、画面仕様書作成、画面レイアウト設計、画面遷移図 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→画面設計テンプレート参照→画面一覧・遷移図・レイアウト作成→ステークホルダーと合意形成 | [機能要件ガイド一覧](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **Webユーザビリティ・ガイドライン** | Webサイト・アプリケーションのユーザビリティ設計指針 | 画面設計、ユーザビリティ設計、UI設計、アクセシビリティ | 各種ガイドライン | ガイドライン参照→ユーザビリティ原則を学習→画面設計に適用→ユーザビリティテスト実施 | 各組織のガイドライン公式サイト |
| **Material Design Guidelines** | GoogleのデザインシステムとUI設計ガイドライン | UI設計、画面デザイン、コンポーネント設計、レスポンシブデザイン | [Material Design](https://material.io/design) | サイト訪問→デザイン原則学習→コンポーネントライブラリ参照→レイアウトグリッド適用→画面設計に反映 | [Material Design](https://m3.material.io/) |

---

## 5. 帳票要件定義（機能要件定義）

**対応項目**
- 帳票要件定義

**成果物**
- 帳票一覧
- 帳票レイアウト

### 5.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Crystal Reports**](https://www.sap.com/products/crystal-reports.html) | SAP製帳票設計ツール。業界標準の帳票作成 | 帳票設計、レポート作成、PDF/Excel出力 | 💰 Developer($495買切) | ✅ 業界標準<br>✅ 強力な帳票機能<br>✅ 多様なデータソース対応<br>✅ エンタープライズ実績<br>✅ 買い切りライセンス | ❌ 高額<br>❌ Windows専用<br>❌ 学習曲線急<br>❌ UI古い | インストール→新規レポート作成→データソース接続→フィールド配置→グループ化・集計設定→PDF/Excel出力 | [Crystal Reports ガイド](https://help.sap.com/docs/SAP_CRYSTAL_REPORTS) |
| 2 | [**Jaspersoft Studio**](https://community.jaspersoft.com/) | オープンソース帳票設計ツール。JasperReportsデザイナー | 帳票設計、レポート作成、PDFレポート | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ Javaベース<br>✅ Eclipse統合<br>✅ 多様な出力形式 | ❌ Java必須<br>❌ 学習曲線あり<br>❌ UI改善余地<br>❌ 日本語情報少ない | インストール→新規Jasperレポート作成→データソース設定→バンド配置→フィールドドラッグ→プレビュー→PDF出力 | [Jaspersoft Tutorials](https://community.jaspersoft.com/documentation) |
| 3 | [**Microsoft Excel**](https://www.microsoft.com/microsoft-365/excel) | 表計算ソフト。帳票レイアウト設計に活用 | 帳票レイアウト設計、テンプレート作成、サンプル作成 | 💰 Microsoft 365($6.99/月〜) | ✅ 広く普及<br>✅ 操作習熟者多い<br>✅ レイアウト設計容易<br>✅ 印刷プレビュー充実<br>✅ テンプレート豊富 | ❌ 帳票専用ツールではない<br>❌ 複雑な帳票困難<br>❌ 有料<br>❌ バージョン管理困難 | Excel起動→ページレイアウト設定→帳票項目配置→罫線・書式設定→印刷プレビュー確認→PDF出力 | [Excel ヘルプ](https://support.microsoft.com/excel) |
| 4 | [**BIRT (Business Intelligence and Reporting Tools)**](https://eclipse.github.io/birt-website/) | Eclipse製オープンソース帳票ツール | 帳票設計、BI レポート、データ可視化 | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ Eclipse統合<br>✅ Webベースレポート<br>✅ Javaベース | ❌ 学習曲線急<br>❌ UI古い<br>❌ セットアップ複雑<br>❌ 日本語情報少ない | Eclipse+BIRTインストール→新規レポートデザイン→データセット作成→レイアウト配置→パラメータ設定→プレビュー | [BIRT Documentation](https://eclipse.github.io/birt-website/documentation/) |
| 5 | [**LibreOffice Calc**](https://www.libreoffice.org/) | 無料オープンソース表計算ソフト。帳票レイアウト設計 | 帳票レイアウト設計、テンプレート作成 | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ Office互換<br>✅ PDF出力<br>✅ マクロ対応 | ❌ Excel完全互換ではない<br>❌ 機能やや劣る<br>❌ 帳票専用ではない<br>❌ テンプレート少ない | LibreOffice Calc起動→ページスタイル設定→帳票レイアウト作成→書式設定→PDF直接エクスポート | [LibreOffice ヘルプ](https://help.libreoffice.org/) |

### 5.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **帳票設計ガイドライン** | 帳票設計の標準化・ベストプラクティス | 帳票設計、レイアウト標準化、帳票一覧作成 | 各種企業内標準 | 社内ガイドライン参照→帳票命名規則確認→レイアウト標準に従って設計→帳票一覧作成 | 各組織の内部文書 |
| **PDF/A標準仕様** | 長期保存用PDF規格の国際標準 | 帳票アーカイブ、長期保存、電子帳簿保存法対応 | [ISO公式サイト](https://www.iso.org/) | ISO仕様書ダウンロード→PDF/A-1/2/3の違いを学習→帳票出力時にPDF/A準拠設定→検証ツールで確認 | [PDF/A Info](https://www.pdfa.org/) |

---

## 6. ファイル要件定義（機能要件定義）

**対応項目**
- ファイル要件定義

**成果物**
- ファイル一覧
- ファイルレイアウト

### 6.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Microsoft Excel**](https://www.microsoft.com/microsoft-365/excel) | 表計算ソフト。ファイルレイアウト定義書作成 | ファイルレイアウト定義、データ項目一覧、形式定義 | 💰 Microsoft 365($6.99/月〜) | ✅ 広く普及<br>✅ 表形式データ管理得意<br>✅ フィルタ・ソート機能<br>✅ テンプレート豊富 | ❌ バージョン管理困難<br>❌ 大規模データは重い<br>❌ 有料<br>❌ 複数人同時編集制限 | Excel起動→ファイル定義テンプレート作成→項目名・型・桁数・必須等を列定義→データ項目を行追加→フィルタで管理 | [Excel ヘルプ](https://support.microsoft.com/excel) |
| 2 | [**Confluence**](https://www.atlassian.com/software/confluence) | ドキュメント管理ツール。ファイル定義書管理 | ファイル定義書作成、バージョン管理、チーム共有 | 🟢 Free(10users) / 💰 Standard($6.05/月〜) | ✅ バージョン管理<br>✅ JIRA統合<br>✅ テーブル機能<br>✅ 承認フロー<br>✅ 検索機能 | ❌ 有料版必要(大規模)<br>❌ エディタやや使いにくい<br>❌ 表計算機能弱い<br>❌ セットアップ必要 | スペース作成→ページ作成→テーブルマクロでファイル定義表作成→項目追加→バージョン管理・承認フロー設定 | [Confluence ガイド](https://www.atlassian.com/software/confluence/guides) |
| 3 | [**Notion**](https://www.notion.so/) | オールインワンワークスペース。データベース機能充実 | ファイル定義書、データ項目管理、データベース管理 | 🟢 Personal Free / 💰 Plus($10/月) | ✅ データベース機能<br>✅ カスタマイズ性高い<br>✅ テンプレート豊富<br>✅ 個人利用無料<br>✅ リアルタイム協業 | ❌ Excel互換性なし<br>❌ 大量データで遅い<br>❌ エクスポート制限<br>❌ 学習曲線あり | アカウント作成→データベース作成→プロパティ(項目名、型、桁数等)設定→ファイル項目を行追加→ビュー・フィルタ設定 | [Notion ガイド](https://www.notion.so/help/guides) |
| 4 | [**CSV Spec Validator**](https://github.com/) | CSVファイル仕様検証ツール | CSVファイル仕様定義、バリデーション、形式チェック | 🟢 オープンソース多数 | ✅ 無料ツール多数<br>✅ 自動検証可能<br>✅ CI/CD統合可能<br>✅ スクリプト化可能 | ❌ 標準ツールなし<br>❌ 各自開発必要<br>❌ GUI少ない<br>❌ 学習必要 | GitHubでCSV検証ツール検索→スキーマ定義(JSON/YAML)作成→検証スクリプト実行→CI/CDパイプラインに統合 | [GitHub検索](https://github.com/search?q=csv+validator) |

### 6.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **機能要件の合意形成ガイド（バッチ編）** | バッチ処理・ファイル連携における仕様定義手法 | ファイルレイアウト定義、外部インターフェース定義 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→ファイルレイアウト定義テンプレート参照→項目定義作成→文字コード・区切り文字等を明記 | [機能要件ガイド一覧](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **CSV/TSV形式標準** | RFC 4180等のCSVファイル形式標準 | CSVファイル定義、文字コード定義、エスケープ処理 | [RFC 4180](https://www.ietf.org/rfc/rfc4180.txt) | RFC 4180ダウンロード→CSV形式ルール確認→区切り文字・引用符・改行の扱いを仕様書に記載 | [RFC 4180 Text](https://www.ietf.org/rfc/rfc4180.txt) |
| **文字コード標準（UTF-8/Shift_JIS）** | 文字コード規格の標準仕様 | 文字コード定義、エンコーディング、文字化け対策 | 各種標準化団体 | Unicode/文字コード標準を学習→ファイル定義で文字コード明記→BOM有無・改行コード指定 | [Unicode公式](https://unicode.org/) |

---

## 7. 概念モデリング（機能要件定義）

**対応項目**
- 概念モデリング

**成果物**
- 概念モデル
- 用語集

### 7.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**ERDPlus**](https://erdplus.com/) | 無料オンラインERD作成ツール。教育向け | ER図作成、概念モデリング、論理モデリング | 🟢 完全無料 | ✅ 完全無料<br>✅ ブラウザベース<br>✅ シンプルで使いやすい<br>✅ SQL自動生成<br>✅ 学習容易 | ❌ 機能基本的<br>❌ エンタープライズ向けでない<br>❌ 協業機能弱い<br>❌ エクスポート制限 | サイト訪問→新規ER図作成→エンティティ追加→属性定義→リレーションシップ設定→SQL自動生成 | [ERDPlus Tutorial](https://erdplus.com/documentation) |
| 2 | [**MySQL Workbench**](https://www.mysql.com/products/workbench/) | MySQLモデリングツール。ER図・SQL生成 | ER図作成、データベース設計、SQL生成 | 🟢 完全無料 | ✅ 完全無料<br>✅ MySQL統合<br>✅ フォワード/リバースエンジニアリング<br>✅ SQL自動生成<br>✅ クロスプラットフォーム | ❌ MySQL特化<br>❌ 概念モデルやや弱い<br>❌ UI改善余地<br>❌ 学習曲線あり | インストール→EERダイアグラム作成→テーブル追加→カラム・主キー定義→リレーション設定→SQL生成 | [Workbench Manual](https://dev.mysql.com/doc/workbench/en/) |
| 3 | [**pgModeler**](https://pgmodeler.io/) | PostgreSQL用モデリングツール。ER図作成 | ER図作成、PostgreSQL設計、SQL生成 | 🟢 Free / 💰 寄付推奨 | ✅ PostgreSQL特化<br>✅ ER図作成優秀<br>✅ SQL自動生成<br>✅ オープンソース<br>✅ リバースエンジニアリング | ❌ PostgreSQL専用<br>❌ UI改善余地<br>❌ ドキュメント少ない<br>❌ 日本語情報少ない | インストール→新規モデル作成→テーブル追加→カラム・制約定義→リレーションシップ作成→DDL生成 | [pgModeler Wiki](https://github.com/pgmodeler/pgmodeler/wiki) |
| 4 | [**Lucidchart**](https://www.lucidchart.com/) | クラウド図表作成ツール。ER図対応 | ER図、概念モデル、UML図、データフロー図 | 🟢 Free版 / 💰 Individual($7.95/月) | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ テンプレート豊富<br>✅ ERDテンプレート<br>✅ 統合機能豊富 | ❌ 無料版制限あり<br>❌ SQL生成不可<br>❌ DB統合なし<br>❌ 有料版高額 | アカウント作成→ERDテンプレート選択→エンティティ図形配置→属性追加→リレーションシップ接続→チーム共有 | [Lucidchart ERD Guide](https://www.lucidchart.com/pages/er-diagrams) |
| 5 | [**Enterprise Architect**](https://sparxsystems.com/) | UMLモデリングツール。データモデリング対応 | ER図、クラス図、概念モデル、トレーサビリティ管理 | 💰 Desktop($159買切) / 💰 Pro($339買切) | ✅ UML完全対応<br>✅ データモデリング強力<br>✅ トレーサビリティ管理<br>✅ コード生成<br>✅ エンタープライズ実績 | ❌ 高額<br>❌ 学習曲線急<br>❌ UI古い<br>❌ Windows中心 | プロジェクト作成→Data Modelダイアグラム追加→エンティティ配置→属性・主キー定義→リレーション設定→DDL生成 | [EA Data Modeling](https://sparxsystems.com/resources/tutorials/) |

### 7.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **機能要件の合意形成ガイド（データモデル編）** | データモデル設計における合意形成手法。ER図作成・正規化 | データベース論理設計、ER図作成、概念モデリング | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→概念モデル作成手法学習→正規化プロセス実施→ER図作成→データディクショナリ整備 | [機能要件ガイド一覧](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **データベース正規化理論** | 正規化の理論と実践手法 | 第1〜第3正規形、BCNF、正規化プロセス | 各種技術書 | 技術書購入/図書館で借りる→正規化理論学習→第1〜3正規形適用→BCNF確認→データモデル最適化 | 各書籍の出版社サイト |
| **ER図記法標準（IE記法/IDEF1X）** | ER図の記法標準 | ER図作成、エンティティ定義、リレーション定義 | 各種標準資料 | 記法標準資料参照→IE記法/IDEF1X/Crow's Foot記法を学習→標準記法でER図作成→カーディナリティ表現 | [ER図記法解説サイト](https://www.lucidchart.com/pages/ER-diagram-symbols-and-meaning) |

---

## 8. 外部システム連携要件定義（機能要件定義）

**対応項目**
- 外部システム連携要件定義

**成果物**
- 外部システム関連図
- 外部インターフェース一覧

### 8.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Postman**](https://www.postman.com/) | API開発・テストプラットフォーム。API仕様書作成 | API仕様書、APIテスト、外部IF定義、REST/SOAP | 🟢 Free版 / 💰 Basic($14/月) | ✅ API開発標準ツール<br>✅ OpenAPI対応<br>✅ ドキュメント自動生成<br>✅ コレクション管理<br>✅ モックサーバー | ❌ 無料版制限あり<br>❌ 複雑なワークフロー困難<br>❌ チーム機能は有料<br>❌ 学習曲線あり | アカウント作成→コレクション作成→APIリクエスト定義→レスポンス例追加→ドキュメント自動生成→チーム共有 | [Postman Learning](https://learning.postman.com/) |
| 2 | [**Swagger/OpenAPI**](https://swagger.io/) | API仕様記述標準。REST API仕様書作成 | REST API仕様書、API設計、自動ドキュメント生成 | 🟢 完全無料 | ✅ 完全無料<br>✅ 業界標準<br>✅ コード自動生成<br>✅ UIドキュメント自動生成<br>✅ バリデーション | ❌ YAML/JSON記述必要<br>❌ 学習曲線あり<br>❌ REST専用<br>❌ 複雑API表現困難 | OpenAPI仕様(YAML/JSON)記述→パス・メソッド・パラメータ定義→レスポンススキーマ定義→Swagger UIで確認 | [OpenAPI Guide](https://swagger.io/docs/specification/about/) |
| 3 | [**Lucidchart**](https://www.lucidchart.com/) | クラウド図表作成ツール。システム連携図作成 | 外部システム関連図、データフロー図、連携図 | 🟢 Free版 / 💰 Individual($7.95/月) | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ テンプレート豊富<br>✅ AWS/Azure統合<br>✅ 直感的操作 | ❌ 無料版制限あり<br>❌ 有料版高額<br>❌ オフライン不可<br>❌ API仕様書作成不可 | アカウント作成→システム構成図テンプレート選択→システムコンポーネント配置→データフロー矢印追加→チーム共有 | [Lucidchart Tutorials](https://www.lucidchart.com/pages/tutorial) |
| 4 | [**Draw.io (diagrams.net)**](https://www.diagrams.net/) | 完全無料の図作成ツール。システム連携図作成 | 外部システム関連図、データフロー図、シーケンス図 | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ AWS/Azureアイコン<br>✅ Google Drive統合<br>✅ 軽量 | ❌ リアルタイム協業弱い<br>❌ テンプレート少ない<br>❌ UI古め<br>❌ API仕様書作成不可 | サイト訪問→保存先選択→AWS/Azureライブラリ有効化→システムアイコン配置→コネクタで接続→Export | [Draw.io User Manual](https://www.drawio.com/doc/) |
| 5 | [**Enterprise Architect**](https://sparxsystems.com/) | UMLモデリングツール。シーケンス図・コンポーネント図 | シーケンス図、コンポーネント図、インターフェース定義 | 💰 Desktop($159買切) / 💰 Pro($339買切) | ✅ UML完全対応<br>✅ シーケンス図優秀<br>✅ トレーサビリティ管理<br>✅ コード生成<br>✅ エンタープライズ実績 | ❌ 高額<br>❌ 学習曲線急<br>❌ UI古い<br>❌ Windows中心 | プロジェクト作成→Sequenceダイアグラム追加→ライフライン配置→メッセージ定義→インタラクション設定→仕様書生成 | [EA Tutorials](https://sparxsystems.com/resources/tutorials/) |

### 8.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **機能要件の合意形成ガイド（バッチ編）** | 外部システム連携・インターフェース定義の手法 | 外部インターフェース定義、連携仕様書、データ交換仕様 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→外部IF定義テンプレート参照→連携方式・プロトコル・データ形式定義→エラーハンドリング設計 | [機能要件ガイド一覧](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **OpenAPI Specification** | REST APIの標準仕様記述フォーマット | REST API仕様書、API設計、インターフェース定義 | [OpenAPI公式サイト](https://www.openapis.org/) | 仕様書ダウンロード→OpenAPI 3.0/3.1記法学習→YAML/JSONでAPI定義→バリデーションツールで検証 | [OpenAPI Spec](https://spec.openapis.org/oas/latest.html) |
| **Web API設計ベストプラクティス** | REST API設計の原則とパターン | API設計、RESTful設計、HTTPメソッド、ステータスコード | 各種技術書 | 技術書購入/Web記事参照→RESTful設計原則学習→リソース設計・URI設計→HTTPメソッド・ステータスコード適用 | [REST API Tutorial](https://restfulapi.net/) |

---

## 9. バッチ処理要件定義（機能要件定義）

**対応項目**
- バッチ処理要件定義

**成果物**
- バッチ一覧

### 9.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Microsoft Excel**](https://www.microsoft.com/microsoft-365/excel) | 表計算ソフト。バッチ一覧・仕様書作成 | バッチ一覧、バッチ仕様書、スケジュール定義 | 💰 Microsoft 365($6.99/月〜) | ✅ 広く普及<br>✅ 表形式管理得意<br>✅ フィルタ・ソート<br>✅ テンプレート豊富<br>✅ ガントチャート作成可 | ❌ バージョン管理困難<br>❌ 大規模データ重い<br>❌ 有料<br>❌ 複数人同時編集制限 | Excel起動→バッチ一覧テンプレート作成→バッチID・名称・起動時刻・処理内容等を定義→依存関係記載→管理 | [Excel ヘルプ](https://support.microsoft.com/excel) |
| 2 | [**Confluence**](https://www.atlassian.com/software/confluence) | ドキュメント管理ツール。バッチ仕様書管理 | バッチ仕様書、ドキュメント管理、バージョン管理 | 🟢 Free(10users) / 💰 Standard($6.05/月〜) | ✅ バージョン管理<br>✅ JIRA統合<br>✅ テーブル機能<br>✅ 承認フロー<br>✅ 検索機能 | ❌ 有料版必要(大規模)<br>❌ エディタやや使いにくい<br>❌ 表計算機能弱い<br>❌ セットアップ必要 | スペース作成→バッチ仕様ページ作成→テーブルでバッチ定義→処理フロー図挿入→バージョン管理 | [Confluence ガイド](https://www.atlassian.com/software/confluence/guides) |
| 3 | [**Lucidchart**](https://www.lucidchart.com/) | クラウド図表作成ツール。バッチフロー図作成 | バッチフロー図、ジョブネット図、処理フロー | 🟢 Free版 / 💰 Individual($7.95/月) | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ フローチャート作成<br>✅ テンプレート豊富<br>✅ 統合機能 | ❌ 無料版制限あり<br>❌ 有料版高額<br>❌ オフライン不可<br>❌ 複雑なジョブネット困難 | アカウント作成→フローチャートテンプレート選択→バッチ処理ボックス配置→依存関係矢印接続→スケジュール記載 | [Lucidchart Tutorials](https://www.lucidchart.com/pages/tutorial) |
| 4 | [**Draw.io (diagrams.net)**](https://www.diagrams.net/) | 完全無料の図作成ツール。バッチフロー図作成 | バッチフロー図、ジョブネット図、処理フロー | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ フローチャート作成<br>✅ Google Drive統合<br>✅ 軽量 | ❌ リアルタイム協業弱い<br>❌ テンプレート少ない<br>❌ UI古め<br>❌ 複雑ジョブネット困難 | サイト訪問→保存先選択→フローチャート図形配置→バッチ処理ボックス追加→依存関係線接続→Export | [Draw.io User Manual](https://www.drawio.com/doc/) |
| 5 | [**JP1/AJS (Hitachi)**](https://www.hitachi.co.jp/products/it/software/jobmanagement/) | 日立製ジョブ管理ソフト。エンタープライズバッチ管理 | ジョブネット設計、スケジュール管理、バッチ運用 | 💰 Enterprise(見積必要) | ✅ エンタープライズ実績<br>✅ ジョブネット管理強力<br>✅ スケジューラー統合<br>✅ 監視機能<br>✅ 日本市場シェア高 | ❌ 非常に高額<br>❌ 大規模向け<br>❌ 学習曲線急<br>❌ セットアップ複雑 | インストール→ジョブネット定義→ジョブユニット作成→先行・後続関係設定→スケジュール登録→実行監視 | [JP1/AJS マニュアル](https://www.hitachi.co.jp/products/it/software/jobmanagement/documentation/) |

### 9.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **機能要件の合意形成ガイド（バッチ編）** | バッチ処理設計における合意形成手法。バッチ設計の標準化 | バッチ処理設計、バッチ仕様書作成、ジョブネット設計 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | PDFダウンロード→バッチ一覧テンプレート参照→ジョブネット図作成→エラーハンドリング・リトライ設計 | [機能要件ガイド一覧](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **バッチ処理設計パターン** | 一般的なバッチ処理パターンとベストプラクティス | バッチ設計、エラーハンドリング、リトライ設計、ログ設計 | 各種技術書 | 技術書購入/Web記事参照→バッチパターン学習→エラーハンドリング設計→リトライ・ログ設計適用 | 各書籍の出版社サイト |
| **Cron/スケジューラー仕様** | バッチスケジューリングの標準仕様 | スケジュール定義、Cron式、タイムゾーン設計 | 各種技術資料 | Cron式の記法学習→分・時・日・月・曜日の指定方法確認→タイムゾーン設定→スケジュール定義 | [Crontab Guru](https://crontab.guru/) |

---

## 10. システム方針検討（機能要件定義）

**対応項目**
- システム方針検討

**成果物**
- システム構成図
- ソフトウェア構成図

### 10.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**Lucidchart**](https://www.lucidchart.com/) | クラウド図表作成ツール。システム構成図作成 | システム構成図、ネットワーク図、アーキテクチャ図 | 🟢 Free版 / 💰 Individual($7.95/月) | ✅ ブラウザベース<br>✅ リアルタイム協業<br>✅ AWS/Azureアイコン豊富<br>✅ テンプレート多数<br>✅ 統合機能 | ❌ 無料版制限あり<br>❌ 有料版高額<br>❌ オフライン不可<br>❌ 複雑な図は重い | アカウント作成→システム構成図テンプレート選択→クラウド/サーバーアイコン配置→ネットワーク接続→レイヤー分け | [Lucidchart Tutorials](https://www.lucidchart.com/pages/tutorial) |
| 2 | [**Draw.io (diagrams.net)**](https://www.diagrams.net/) | 完全無料の図作成ツール。システム構成図作成 | システム構成図、ネットワーク図、アーキテクチャ図 | 🟢 完全無料 | ✅ 完全無料<br>✅ オープンソース<br>✅ AWS/Azureアイコン<br>✅ Google Drive統合<br>✅ 軽量 | ❌ リアルタイム協業弱い<br>❌ テンプレート少ない<br>❌ UI古め<br>❌ 高度機能限定的 | サイト訪問→保存先選択→AWS/Azureライブラリ有効化→インフラアイコン配置→接続線追加→Export | [Draw.io User Manual](https://www.drawio.com/doc/) |
| 3 | [**Microsoft Visio**](https://www.microsoft.com/microsoft-365/visio/) | プロフェッショナル図表作成ツール。システム構成図 | システム構成図、ネットワーク図、インフラ構成図 | 💰 Plan 1($5/月) / 💰 Plan 2($15/月) | ✅ Microsoft 365統合<br>✅ 図形ライブラリ豊富<br>✅ エンタープライズ標準<br>✅ データ連携機能<br>✅ ネットワーク図強力 | ❌ 高額<br>❌ Windows/Web中心<br>❌ 学習コストあり<br>❌ モダンツールより重い | Visio起動→ネットワークテンプレート選択→ステンシルからサーバー/ネットワーク機器配置→コネクタで接続→保存 | [Visio Help](https://support.microsoft.com/visio) |
| 4 | [**C4 Model + PlantUML**](https://c4model.com/) | ソフトウェアアーキテクチャ可視化手法。階層的構成図 | ソフトウェア構成図、アーキテクチャ図、コンテキスト図 | 🟢 完全無料 | ✅ 完全無料<br>✅ 階層的アーキテクチャ表現<br>✅ テキストベース<br>✅ バージョン管理容易<br>✅ CI/CD統合可能 | ❌ 学習曲線あり<br>❌ GUI編集不可<br>❌ レイアウト制御困難<br>❌ 知名度やや低い | C4記法学習→Context/Container/Component/Code図を階層的に作成→PlantUMLで記述→レンダリング→PNG出力 | [C4 Model Guide](https://c4model.com/) |
| 5 | [**Enterprise Architect**](https://sparxsystems.com/) | UMLモデリングツール。コンポーネント図・配置図 | コンポーネント図、配置図、パッケージ図、アーキテクチャ設計 | 💰 Desktop($159買切) / 💰 Pro($339買切) | ✅ UML完全対応<br>✅ アーキテクチャモデリング<br>✅ トレーサビリティ管理<br>✅ コード生成<br>✅ エンタープライズ実績 | ❌ 高額<br>❌ 学習曲線急<br>❌ UI古い<br>❌ Windows中心 | プロジェクト作成→Deploymentダイアグラム追加→ノード配置→コンポーネント配置→関連設定→仕様書生成 | [EA Tutorials](https://sparxsystems.com/resources/tutorials/) |

### 10.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **システム基盤設計ガイド** | システム基盤・アーキテクチャ設計の標準手法 | システム構成設計、アーキテクチャパターン、技術選定 | 各種技術書 | 技術書購入/図書館で借りる→アーキテクチャパターン学習→非機能要件に基づく技術選定→システム構成設計 | 各書籍の出版社サイト |
| **AWS Well-Architected Framework** | AWSクラウドアーキテクチャ設計のベストプラクティス | クラウド構成設計、AWS設計原則、セキュリティ設計 | [AWS公式サイト](https://aws.amazon.com/architecture/well-architected/) | サイト訪問→6つの柱(運用/セキュリティ/信頼性/パフォーマンス/コスト/持続可能性)学習→設計レビュー実施 | [Well-Architected Tool](https://aws.amazon.com/well-architected-tool/) |
| **Azure Architecture Center** | Azureクラウドアーキテクチャパターンとベストプラクティス | Azure構成設計、アーキテクチャパターン、リファレンス | [Microsoft公式サイト](https://learn.microsoft.com/azure/architecture/) | サイトアクセス→アーキテクチャパターン検索→リファレンスアーキテクチャ参照→自システムに適用 | [Azure Architecture](https://learn.microsoft.com/azure/architecture/) |
| **C4 Model Documentation** | ソフトウェアアーキテクチャ可視化の階層的モデリング手法 | ソフトウェア構成図、アーキテクチャ設計、システムコンテキスト | [C4 Model公式サイト](https://c4model.com/) | サイト訪問→C4モデル概念学習→Context/Container/Component/Codeの4レベルで階層的に設計→図作成 | [C4 Model](https://c4model.com/) |

---

## 11. 非機能要件定義

**対応項目**
- 非機能要件定義

**成果物**
- 非機能要件定義書

### 11.1 推奨ツール

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット | 利用方法の説明 | 利用方法リンク |
|---|---------|------|------|------|---------|-----------|---------------|---------------|
| 1 | [**IPA 非機能要求グレード利用ガイド（Excel版）**](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | IPAの非機能要求グレードExcelテンプレート | 非機能要件定義、要件グレード設定、合意形成 | 🟢 完全無料 | ✅ 完全無料<br>✅ IPA標準テンプレート<br>✅ 118要求項目網羅<br>✅ 日本語完全対応<br>✅ Excel形式で使いやすい | ❌ Excel依存<br>❌ バージョン管理困難<br>❌ 協業機能弱い<br>❌ 自動化困難 | IPAサイトからExcelテンプレートDL→6大分類118項目を確認→各項目のグレード(要求レベル)設定→合意形成 | [非機能要求グレード](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) |
| 2 | [**Confluence**](https://www.atlassian.com/software/confluence) | ドキュメント管理ツール。非機能要件定義書管理 | 非機能要件定義書、ドキュメント管理、バージョン管理 | 🟢 Free(10users) / 💰 Standard($6.05/月〜) | ✅ バージョン管理<br>✅ JIRA統合<br>✅ テンプレート機能<br>✅ 承認フロー<br>✅ 検索機能 | ❌ 有料版必要(大規模)<br>❌ エディタやや使いにくい<br>❌ 表計算機能弱い<br>❌ セットアップ必要 | スペース作成→非機能要件ページ作成→テーブルで要件項目定義→性能・可用性等を分類→バージョン管理 | [Confluence ガイド](https://www.atlassian.com/software/confluence/guides) |
| 3 | [**Microsoft Excel / Google Sheets**](https://www.microsoft.com/microsoft-365/excel) | 表計算ソフト。非機能要件一覧作成 | 非機能要件一覧、要件項目管理、グレード設定 | 💰 Microsoft 365($6.99/月〜) / 🟢 Google無料 | ✅ 広く普及<br>✅ 表形式管理得意<br>✅ フィルタ・ソート<br>✅ テンプレート作成容易<br>✅ 計算式利用可能 | ❌ バージョン管理困難<br>❌ 大規模データ重い<br>❌ Excel有料<br>❌ 複数人同時編集制限 | Excel/Sheets起動→非機能要件一覧テンプレート作成→分類・項目・目標値・測定方法を列定義→要件追加→管理 | [Excel ヘルプ](https://support.microsoft.com/excel) |
| 4 | [**Notion**](https://www.notion.so/) | オールインワンワークスペース。データベース機能 | 非機能要件定義、データベース管理、要件トレーサビリティ | 🟢 Personal Free / 💰 Plus($10/月) | ✅ データベース機能<br>✅ カスタマイズ性高い<br>✅ テンプレート豊富<br>✅ 個人利用無料<br>✅ リアルタイム協業 | ❌ Excel互換性なし<br>❌ 大量データで遅い<br>❌ エクスポート制限<br>❌ 学習曲線あり | アカウント作成→データベース作成→プロパティ(分類、項目、目標値等)設定→非機能要件を行追加→関連付け | [Notion ガイド](https://www.notion.so/help/guides) |
| 5 | [**Jama Connect**](https://www.jamasoftware.com/) | エンタープライズ要件管理ツール。非機能要件管理対応 | 非機能要件管理、トレーサビリティ、承認フロー、規制対応 | 💰 Enterprise(見積必要) | ✅ 完全なトレーサビリティ<br>✅ レビュー・承認フロー<br>✅ 規制対応（医療・航空）<br>✅ テスト管理統合<br>✅ 変更影響分析 | ❌ 非常に高額<br>❌ 複雑で習得困難<br>❌ 小規模には過剰<br>❌ セットアップ時間大 | プロジェクト作成→非機能要件アイテム登録→トレーサビリティ設定→レビューフロー定義→承認プロセス実行 | [Jama University](https://community.jamasoftware.com/learn) |

### 11.2 有用なドキュメント

| 資料名 | 概要 | 用途 | リンク | 利用方法の説明 | 利用方法リンク |
|-------|------|------|--------|---------------|---------------|
| **非機能要求グレード** | 6大分類118要求項目と230指標からなる非機能要件定義の標準フレームワーク。要件の見える化と合意形成を支援 | 非機能要件定義、性能要件、可用性要件、セキュリティ要件、運用要件 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | IPAサイトからExcelテンプレートDL→6大分類(可用性・性能・運用等)118項目確認→グレード設定→合意形成 | [非機能要求グレード](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) |
| **非機能要求グレード利用ガイド** | 非機能要求グレードの利用方法、要件設定の進め方を詳細解説 | 非機能要件定義プロセス、グレード設定、合意形成手法 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | PDFダウンロード→利用ガイド参照→グレード設定手順学習→ステークホルダーとの合意形成プロセス実施 | [利用ガイドDL](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) |
| **システム基盤非機能要求グレード** | システム基盤（インフラ）に特化した非機能要求グレード | インフラ非機能要件、性能設計、可用性設計、拡張性設計 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | IPAサイトからシステム基盤版DL→インフラ観点の非機能要件確認→性能・可用性・拡張性のグレード設定 | [システム基盤版](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) |
| **ISO/IEC 25010（SQuaRE）** | ソフトウェア品質特性の国際標準。非機能要件の分類体系 | 品質特性定義、非機能要件分類、品質評価 | [ISO公式サイト](https://www.iso.org/) | ISO仕様書参照→8つの品質特性(機能適合性・性能効率性・互換性等)学習→品質要件定義に適用 | [ISO/IEC 25010](https://www.iso.org/standard/35733.html) |


**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
