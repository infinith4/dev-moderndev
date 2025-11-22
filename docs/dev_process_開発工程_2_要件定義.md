# 開発工程_2_要件定義

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**要件定義プロセス**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 2.1 システム要件定義

### 主要タスク
- 利害関係者の識別
- 要求事項の識別
- 要求事項の評価
- システム要件の定義
- システム要件の評価
- システム要件の合意

### 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **ONES Wiki** | [https://ones.com/](https://ones.com/) | AI活用の要件定義・ナレッジ管理ツール。ドキュメントコラボレーション強化 | 要件定義書作成、AI支援、ナレッジ管理、チーム協業 | ✅ AI要件定義支援<br>✅ リアルタイム共同編集<br>✅ ナレッジ蓄積・検索<br>✅ プロジェクト管理統合<br>✅ テンプレート豊富 | ❌ 比較的新しいサービス<br>❌ 日本語情報少ない<br>❌ 有料プラン必須<br>❌ 他ツールとの連携限定的 |
| 2 | **Confluence** | [https://www.atlassian.com/software/confluence](https://www.atlassian.com/software/confluence) | Atlassian製ナレッジベース。要件定義書作成・チーム協業に最適 | 要件定義書作成、ドキュメント管理、Wiki、承認フロー | ✅ JIRA完全統合<br>✅ 豊富なテンプレート<br>✅ バージョン管理<br>✅ 権限管理詳細<br>✅ 業界標準的存在 | ❌ 有料（$5.75/月〜）<br>❌ 大規模では動作重い<br>❌ UI複雑<br>❌ 検索機能やや弱い |
| 3 | **GEAR.indigo** | [https://www.gear-indigo.com/](https://www.gear-indigo.com/) | 2024年登場のAI駆動要件定義ツール。自然言語から設計書・コード生成 | AI駆動要件定義、自動設計書生成、トレーサビリティ管理 | ✅ AI自動設計書生成<br>✅ 自然言語インターフェース<br>✅ コード自動生成<br>✅ 要件トレーサビリティ<br>✅ 手戻り削減 | ❌ 非常に新しい（実績少）<br>❌ AI精度は発展途上<br>❌ 価格情報不明瞭<br>❌ 日本市場中心 |
| 4 | **Figma** | [https://www.figma.com/](https://www.figma.com/) | クラウドベースのUIデザインツール。プロトタイプ作成・デザイン仕様共有 | UIプロトタイプ作成、画面設計、デザイン仕様書、レビュー | ✅ ブラウザで完結<br>✅ リアルタイム共同編集<br>✅ プロトタイプ作成簡単<br>✅ デベロッパーハンドオフ<br>✅ 無料プランあり | ❌ オフライン作業不可<br>❌ 複雑な図は不向き<br>❌ プラグイン依存増えがち<br>❌ 大規模ファイルは重い |
| 5 | **VISLITE** | [https://www.vislite.com/](https://www.vislite.com/) | 手戻りゼロを目指す要件定義ツール。要件可視化・トレーサビリティ管理 | 要件可視化、トレーサビリティ管理、手戻り防止、Excel連携 | ✅ 要件の可視化優秀<br>✅ トレーサビリティ管理<br>✅ 手戻り防止機能<br>✅ 日本製で日本語完全対応<br>✅ Excel連携 | ❌ 知名度低い<br>❌ コミュニティ小さい<br>❌ 価格やや高め<br>❌ モダンUIではない |
| 6 | **Adobe XD** | [https://www.adobe.com/products/xd.html](https://www.adobe.com/products/xd.html) | AdobeのUI/UXデザインツール。プロトタイプ・デザインシステム構築 | UI/UXデザイン、プロトタイプ、デザインシステム、画面遷移 | ✅ Adobe製品統合<br>✅ デザインシステム構築<br>✅ プロトタイプ作成<br>✅ 音声UI対応<br>✅ 無料プランあり | ❌ Figmaに押され気味<br>❌ 開発停止の噂<br>❌ Adobeアカウント必須<br>❌ 重い動作 |
| 7 | **Sketch** | [https://www.sketch.com/](https://www.sketch.com/) | macOS専用UIデザインツール。デザイン業界標準の一つ | UIデザイン、プロトタイプ、デザインシステム、シンボル管理 | ✅ デザイナー愛用<br>✅ プラグイン豊富<br>✅ シンボル管理優秀<br>✅ デザインシステム対応<br>✅ 買い切り可能 | ❌ macOS専用<br>❌ Figmaに市場シェア奪われ中<br>❌ サブスク移行で不評<br>❌ コラボ機能Figma劣る |
| 8 | **Balsamiq** | [https://balsamiq.com/](https://balsamiq.com/) | 手書き風ワイヤーフレームツール。ラピッドプロトタイピングに最適 | 低忠実度ワイヤーフレーム、ラピッドプロトタイピング、初期設計 | ✅ 手書き風で低忠実度<br>✅ 素早くアイデア形成<br>✅ シンプルで学習容易<br>✅ デザイン議論に集中<br>✅ 買い切りプランあり | ❌ デザイン精度低い<br>❌ 最終デザインには不向き<br>❌ 機能限定的<br>❌ モダンではない |
| 9 | **Axure RP** | [https://www.axure.com/](https://www.axure.com/) | 高機能プロトタイプツール。インタラクション設計・詳細仕様書生成 | 高度なプロトタイプ、インタラクション設計、仕様書自動生成 | ✅ 高度なインタラクション<br>✅ 動的プロトタイプ<br>✅ 仕様書自動生成<br>✅ 条件分岐・変数対応<br>✅ エンタープライズ実績 | ❌ 学習曲線非常に急<br>❌ 高額（$25/月〜）<br>❌ UI古い<br>❌ 動作やや重い |
| 10 | **Jama Connect** | [https://www.jamasoftware.com/](https://www.jamasoftware.com/) | エンタープライズ要件管理ツール。トレーサビリティ・バリデーション | 要件管理、トレーサビリティ、承認フロー、規制対応 | ✅ 完全なトレーサビリティ<br>✅ レビュー・承認フロー<br>✅ 規制対応（医療・航空）<br>✅ テスト管理統合<br>✅ 変更影響分析 | ❌ 非常に高額<br>❌ 複雑で習得困難<br>❌ 小規模には過剰<br>❌ セットアップ時間大 |

### その他利用可能なツール

26. InVision
27. Marvel
28. UXPin
29. Mockplus
30. Proto.io
31. Justinmind
32. Reqtify
33. DOORS (IBM)
34. ReqView
35. Modern Requirements
36. Framer
37. Penpot
38. Lunacy
39. ProtoPie
40. Principle

---

## 2.2 業務要件定義

### 主要タスク
- 業務要件の定義
- 業務フローの作成
- 画面・帳票要件の定義
- 非機能要件の定義
- 業務要件の評価

---

## クラウドサービス（Azure / AWS）

要件定義フェーズでは、ドキュメント管理、コラボレーション、プロトタイプ環境としてクラウドサービスを活用します。

### Azure サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Azure DevOps Wiki** | [https://azure.microsoft.com/ja-jp/products/devops/](https://azure.microsoft.com/ja-jp/products/devops/) | Azure DevOps統合Wiki。要件定義書・仕様書管理 | 要件定義書作成、仕様書管理、Markdown記述、バージョン管理 | ✅ Azure DevOps統合<br>✅ Git連携<br>✅ Markdown記述<br>✅ バージョン管理<br>✅ 無料プランあり | ❌ Confluence比で機能少ない<br>❌ UI基本的<br>❌ テンプレート少ない<br>❌ エディタ改善余地 |
| 2 | **Microsoft 365 SharePoint** | [https://www.microsoft.com/microsoft-365/sharepoint/](https://www.microsoft.com/microsoft-365/sharepoint/) | エンタープライズドキュメント管理・共有プラットフォーム | 要件定義書管理、承認フロー、バージョン管理、権限管理 | ✅ Office 365完全統合<br>✅ 承認ワークフロー<br>✅ メタデータ管理<br>✅ 強力な権限管理<br>✅ エンタープライズ実績 | ❌ 複雑で学習困難<br>❌ カスタマイズに専門知識<br>❌ UI改善余地<br>❌ 有料（$5/月〜） |
| 3 | **Azure App Service (プロトタイプ環境)** | [https://azure.microsoft.com/ja-jp/products/app-service/](https://azure.microsoft.com/ja-jp/products/app-service/) | フルマネージドWebアプリホスティング。プロトタイプ検証環境 | プロトタイプWebアプリ展開、要件検証環境、デモ環境 | ✅ 迅速なデプロイ<br>✅ スケーリング自動<br>✅ CI/CD統合<br>✅ 多言語対応<br>✅ 無料枠あり | ❌ 従量課金でコスト予測難<br>❌ ベンダーロックイン<br>❌ 一部制約あり<br>❌ 複雑な構成困難 |
| 4 | **Azure Static Web Apps** | [https://azure.microsoft.com/ja-jp/products/app-service/static/](https://azure.microsoft.com/ja-jp/products/app-service/static/) | 静的Webアプリホスティング。プロトタイプ・デモサイト | UI/UXプロトタイプ公開、静的サイトデモ、レビュー環境 | ✅ 無料枠充実<br>✅ GitHub Actions統合<br>✅ グローバルCDN<br>✅ API統合可能<br>✅ セットアップ簡単 | ❌ 静的サイト限定<br>❌ サーバーサイド制限<br>❌ カスタムドメイン設定必要<br>❌ リージョン限定的 |

### AWS サービス

| # | サービス名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **AWS WorkDocs** | [https://aws.amazon.com/workdocs/](https://aws.amazon.com/workdocs/) | フルマネージド文書ストレージ・共同編集サービス | 要件定義書保存、共同編集、レビュー・コメント、承認フロー | ✅ 1TBストレージ<br>✅ リアルタイム共同編集<br>✅ バージョン管理<br>✅ コメント・承認機能<br>✅ AWS統合 | ❌ Microsoft 365より機能少ない<br>❌ デスクトップアプリ弱い<br>❌ 日本語サポート限定的<br>❌ エコシステム小 |
| 2 | **Amazon Honeycode** | [https://www.honeycode.aws/](https://www.honeycode.aws/) | ノーコードアプリ構築サービス。簡易プロトタイプ作成 | 業務アプリプロトタイプ、簡易ワークフロー、要件検証 | ✅ ノーコードで構築<br>✅ テンプレート豊富<br>✅ AWS統合<br>✅ モバイル対応<br>✅ 無料枠あり | ❌ 機能限定的<br>❌ 複雑なロジック困難<br>❌ エクスポート制限<br>❌ サービス継続性不透明 |
| 3 | **AWS Amplify (プロトタイプ環境)** | [https://aws.amazon.com/amplify/](https://aws.amazon.com/amplify/) | フルスタックアプリ開発・ホスティングプラットフォーム | プロトタイプWebアプリ展開、フロントエンド検証環境 | ✅ フロントエンド特化<br>✅ CI/CD統合<br>✅ React/Vue/Angular対応<br>✅ バックエンド統合<br>✅ 無料枠あり | ❌ AWS依存<br>❌ 学習曲線あり<br>❌ 従量課金<br>❌ 複雑な構成困難 |
| 4 | **Amazon S3 + CloudFront (静的サイトホスティング)** | [https://aws.amazon.com/s3/](https://aws.amazon.com/s3/) | 静的WebサイトホスティングとCDN配信 | UI/UXプロトタイプ公開、デモサイト、静的ドキュメント | ✅ 低コスト<br>✅ 高速配信（CDN）<br>✅ 高可用性<br>✅ スケーラブル<br>✅ S3 + CloudFront組み合わせ | ❌ 設定やや複雑<br>❌ 静的サイト限定<br>❌ HTTPS設定必要<br>❌ 管理コストあり |
| 5 | **AWS Lambda + API Gateway (プロトタイプAPI)** | [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/) | サーバーレスAPI構築。プロトタイプバックエンド | プロトタイプAPI、サーバーレスバックエンド、要件検証 | ✅ サーバーレス<br>✅ 従量課金（コスト削減）<br>✅ スケーラブル<br>✅ 多言語対応<br>✅ 無料枠あり | ❌ コールドスタート遅延<br>❌ デバッグ困難<br>❌ ステートレス設計必要<br>❌ 実行時間制限 |

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
