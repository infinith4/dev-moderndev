# ソフトウェア開発プロセスガイド

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）が策定した「共通フレーム2013」に基づき、ソフトウェア開発の各工程におけるタスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

## IPA共通フレーム2013の構造

共通フレームでは、システム開発作業を **プロセス > アクティビティ > タスク** の階層で体系化し定義しています。

### プロセス群の分類

1. **合意プロセス**
   - 取得プロセス
   - 供給プロセス

2. **テクニカルプロセス**
   - 企画プロセス
   - 要件定義プロセス
   - システム開発プロセス
   - ソフトウェア実装プロセス

3. **運用・サービスプロセス**

4. **支援プロセス**

---

## 1. 企画プロセス

### 1.1 システム化構想の立案プロセス

#### 主要タスク
- 経営要求、経営課題の確認
- 対象となる業務の明確化
- 業務の方向性の明確化
- システム化構想の立案
- システム化構想の承認

#### 推奨ツール（生産性が高いもの Top 5）

1. **Miro** - オンラインホワイトボード、アイデア整理、ブレインストーミング
2. **Notion** - ドキュメント管理、ナレッジベース、プロジェクト管理
3. **Microsoft Visio** - プロセスフロー図作成、業務フロー可視化
4. **Lucidchart** - フローチャート、組織図、システム構成図作成
5. **JIRA** - プロジェクト管理、課題追跡、ロードマップ作成

#### その他利用可能なツール

6. Google Workspace (Docs, Sheets, Slides)
7. Microsoft 365 (Word, Excel, PowerPoint)
8. Confluence
9. Trello
10. Asana
11. monday.com
12. ClickUp
13. Basecamp
14. Smartsheet
15. Draw.io (diagrams.net)

### 1.2 システム化計画の立案プロセス

#### 主要タスク
- 対象業務の分析
- システム化機能の整理
- システム化の方式の策定
- 実施計画の策定
- システム化計画の承認

#### 推奨ツール（生産性が高いもの Top 5）

1. **Microsoft Project** - プロジェクト計画、スケジュール管理、リソース管理
2. **Redmine** - プロジェクト管理、ガントチャート、課題管理
3. **Lychee Redmine** - Redmine拡張、見やすいガントチャート
4. **Backlog** - プロジェクト管理、ガントチャート、バージョン管理
5. **Wrike** - プロジェクト計画、タスク管理、リソース最適化

#### その他利用可能なツール

16. Planview
17. Teamwork
18. ProofHub
19. OpenProject
20. GanttProject

---

## 2. 要件定義プロセス

### 2.1 システム要件定義

#### 主要タスク
- 利害関係者の識別
- 要求事項の識別
- 要求事項の評価
- システム要件の定義
- システム要件の評価
- システム要件の合意

#### 推奨ツール（生産性が高いもの Top 5）

1. **ONES Wiki** - AI活用要件定義、ドキュメントコラボレーション、ナレッジ蓄積
2. **Confluence** - 要件定義書作成、テンプレート管理、チーム協業
3. **GEAR.indigo** (2024年新) - AI駆動要件定義、自然言語から設計書生成、コード生成
4. **Figma** - UIワイヤーフレーム、プロトタイプ作成、デザイン仕様
5. **VISLITE** - 手戻りゼロの要件定義、要件可視化、トレーサビリティ

#### その他利用可能なツール

21. Adobe XD
22. Sketch
23. Balsamiq
24. Axure RP
25. InVision
26. Marvel
27. UXPin
28. Mockplus
29. Proto.io
30. Justinmind
31. Reqtify
32. DOORS (IBM)
33. Jama Connect
34. ReqView
35. Modern Requirements

### 2.2 業務要件定義

#### 主要タスク
- 業務要件の定義
- 業務フローの作成
- 画面・帳票要件の定義
- 非機能要件の定義
- 業務要件の評価

---

## 3. システム開発プロセス

### 3.1 システム方式設計

#### 主要タスク
- システム方式の策定
- システム構成の定義
- 外部インタフェースの定義
- ユーザインタフェースの設計
- データベース方式の設計

#### 推奨ツール（生産性が高いもの Top 5）

1. **Next Design** - システム設計、モデリング、トレーサビリティ、設計自動反映
2. **astah*** - UML、フローチャート、ER図、要求図、システムモデリング
3. **Enterprise Architect** - UMLモデリング、アーキテクチャ設計、要件管理
4. **draw.io (diagrams.net)** - システム構成図、ネットワーク図、無料
5. **PlantUML** - テキストベースUML、バージョン管理しやすい、CI/CD連携

#### その他利用可能なツール

36. StarUML
37. Visual Paradigm
38. Cacoo
39. Creately
40. Gliffy
41. ArchiMate
42. Structurizr
43. C4-PlantUML

### 3.2 ソフトウェア方式設計

#### 主要タスク
- ソフトウェア構成の定義
- ソフトウェア方式の設計
- インタフェースの設計
- データベースの詳細設計

### 3.3 ソフトウェア詳細設計

#### 主要タスク
- モジュールの詳細設計
- インタフェースの詳細設計
- データ構造の詳細設計
- アルゴリズムの詳細設計

---

## 4. ソフトウェア実装プロセス

### 4.1 プログラミング

#### 主要タスク
- コーディング標準の確立
- プログラミング
- コードレビュー
- 単体テストの実施

#### 推奨ツール（生産性が高いもの Top 5）

1. **Visual Studio Code** - 軽量エディタ、拡張機能豊富、多言語対応、Git連携
2. **IntelliJ IDEA** - Java/Kotlin開発、リファクタリング支援、コード解析
3. **GitHub Copilot** - AI コード補完、コード生成、生産性向上
4. **Cursor** - AI統合エディタ、コード生成、リファクタリング支援
5. **JetBrains AI Assistant** - AI コード補完、コード説明、テスト生成

#### その他利用可能なツール

44. Eclipse
45. NetBeans
46. PyCharm
47. WebStorm
48. Rider
49. Android Studio
50. Xcode
51. Sublime Text
52. Atom
53. Vim/Neovim
54. Emacs
55. Tabnine (AIコード補完)
56. Amazon CodeWhisperer
57. Codeium

### 4.2 バージョン管理

#### 推奨ツール（生産性が高いもの Top 5）

1. **Git** - 分散型バージョン管理、業界標準
2. **GitHub** - コード管理、PR、CI/CD、コラボレーション
3. **GitLab** - コード管理、CI/CD統合、DevSecOps
4. **Bitbucket** - Git管理、JIRA連携、Atlassian統合
5. **Azure DevOps Repos** - Git管理、Microsoft環境統合

#### その他利用可能なツール

58. Gitea
59. Gogs
60. SourceTree (GUIクライアント)
61. GitKraken (GUIクライアント)
62. Fork (GUIクライアント)

---

## 5. ソフトウェアテストプロセス

### 5.1 単体テスト

#### 主要タスク
- テスト計画の作成
- テストケースの設計
- テストデータの作成
- テストの実施
- 不具合の記録・追跡

#### 推奨ツール（生産性が高いもの Top 5）

1. **JUnit** (Java) - 単体テストフレームワーク、アサーション、モック
2. **pytest** (Python) - テストフレームワーク、フィクスチャ、パラメータ化
3. **Jest** (JavaScript/TypeScript) - テストフレームワーク、カバレッジ、スナップショット
4. **NUnit** (.NET) - .NET単体テスト、パラメータ化テスト
5. **RSpec** (Ruby) - BDDフレームワーク、読みやすいテスト

#### その他利用可能なツール

63. Mocha
64. Jasmine
65. Vitest
66. xUnit
67. MSTest
68. TestNG
69. Spock
70. unittest (Python標準)

### 5.2 結合テスト

#### 主要タスク
- 結合テスト計画の作成
- インタフェーステスト
- 統合テスト
- テストの実施
- 不具合の管理

#### 推奨ツール（生産性が高いもの Top 5）

1. **Postman** - APIテスト、HTTPリクエスト、自動化、コレクション管理
2. **Selenium** - Webブラウザ自動化、E2Eテスト、多言語対応
3. **Cypress** - モダンE2Eテスト、高速、デバッグしやすい
4. **Playwright** - ブラウザ自動化、クロスブラウザ、高速・安定
5. **REST Assured** - REST APIテスト、Java、BDD対応

#### その他利用可能なツール

71. SoapUI
72. Karate
73. TestCafe
74. Puppeteer
75. WebdriverIO
76. Appium (モバイル)
77. Espresso (Android)
78. XCUITest (iOS)

### 5.3 システムテスト

#### 主要タスク
- システムテスト計画の作成
- 機能テスト
- 性能テスト
- セキュリティテスト
- ユーザビリティテスト

#### 推奨ツール（生産性が高いもの Top 5）

1. **JMeter** - 負荷テスト、性能テスト、ストレステスト
2. **Gatling** - 高性能負荷テスト、スケーラブル、レポート豊富
3. **Locust** - Python負荷テスト、分散テスト、シンプル
4. **k6** - モダン負荷テスト、開発者フレンドリー、CI/CD統合
5. **OWASP ZAP** - セキュリティテスト、脆弱性スキャン、ペネトレーションテスト

#### その他利用可能なツール

79. Burp Suite
80. SonarQube (静的解析・セキュリティ)
81. Checkmarx
82. Veracode
83. LoadRunner
84. BlazeMeter
85. Azure Load Testing

---

## 6. CI/CDとテスト自動化

### 主要タスク
- CI/CDパイプライン構築
- ビルド自動化
- テスト自動化
- デプロイ自動化
- モニタリング

#### 推奨ツール（生産性が高いもの Top 5）

1. **GitHub Actions** - CI/CD、GitHub統合、豊富なアクション、無料枠
2. **GitLab CI/CD** - GitLab統合、Auto DevOps、コンテナレジストリ
3. **Jenkins** - オープンソース、プラグイン豊富、柔軟なカスタマイズ
4. **CircleCI** - 高速ビルド、並列実行、Docker対応
5. **Azure DevOps Pipelines** - Microsoft環境統合、YAML定義、マルチプラットフォーム

#### その他利用可能なツール

86. Travis CI
87. TeamCity
88. Bamboo
89. AWS CodePipeline
90. Google Cloud Build
91. Drone CI
92. Buildkite
93. Harness
94. Argo CD
95. Spinnaker
96. Tekton
97. Flux

---

## 7. コード品質・静的解析

#### 推奨ツール（生産性が高いもの Top 5）

1. **SonarQube** - コード品質管理、バグ検出、セキュリティ、技術的負債可視化
2. **ESLint** (JavaScript/TypeScript) - Linter、コードスタイル、自動修正
3. **Pylint** (Python) - 静的解析、コード品質チェック、PEP8準拠
4. **RuboCop** (Ruby) - 静的解析、コードスタイル、自動修正
5. **Checkstyle** (Java) - コードスタイルチェック、標準準拠

#### その他利用可能なツール

98. PMD
99. FindBugs/SpotBugs
100. Prettier (フォーマッター)
101. Black (Pythonフォーマッター)
102. gofmt (Goフォーマッター)
103. ClangFormat (C/C++)
104. StyleCop (.NET)
105. TSLint (非推奨、ESLint推奨)

---

## 8. 移行プロセス

### 主要タスク
- 移行計画の策定
- 移行設計
- 移行プログラムの開発
- データ移行
- 移行テスト
- 本番移行

#### 推奨ツール（生産性が高いもの Top 5）

1. **Liquibase** - データベーススキーマ管理、バージョン管理、マイグレーション
2. **Flyway** - データベースマイグレーション、シンプル、信頼性高い
3. **AWS Database Migration Service** - クラウドDBマイグレーション、最小ダウンタイム
4. **Talend** - ETL/ELTツール、データ統合、データ移行
5. **Apache NiFi** - データフロー自動化、データ移行、リアルタイム処理

#### その他利用可能なツール

106. Informatica
107. Pentaho Data Integration
108. Airbyte
109. Fivetran
110. Stitch

---

## 9. 保守・運用プロセス

### 9.1 運用管理

#### 主要タスク
- システム監視
- ログ管理
- インシデント管理
- パフォーマンス管理

#### 推奨ツール（生産性が高いもの Top 5）

1. **Datadog** - APM、インフラ監視、ログ管理、統合ダッシュボード
2. **Prometheus + Grafana** - メトリクス収集、可視化、アラート、オープンソース
3. **ELK Stack (Elasticsearch, Logstash, Kibana)** - ログ管理、検索、可視化
4. **New Relic** - APM、オブザーバビリティ、エラートラッキング
5. **Sentry** - エラートラッキング、パフォーマンス監視、リアルタイムアラート

#### その他利用可能なツール

111. Splunk
112. AppDynamics
113. Dynatrace
114. Zabbix
115. Nagios
116. CloudWatch (AWS)
117. Azure Monitor
118. Google Cloud Operations

### 9.2 問題管理・変更管理

#### 推奨ツール（生産性が高いもの Top 5）

1. **ServiceNow** - ITSM、インシデント管理、変更管理、統合プラットフォーム
2. **Jira Service Management** - ITサービスデスク、インシデント管理、Jira統合
3. **Zendesk** - カスタマーサポート、チケット管理、ナレッジベース
4. **Freshservice** - ITSM、資産管理、自動化
5. **PagerDuty** - インシデント対応、オンコール管理、アラート集約

#### その他利用可能なツール

119. BMC Remedy
120. ManageEngine ServiceDesk Plus
121. TOPdesk

---

## 10. ドキュメント管理

#### 推奨ツール（生産性が高いもの Top 5）

1. **Notion** - オールインワンワークスペース、ドキュメント、Wiki、プロジェクト管理
2. **Confluence** - チーム協業、ナレッジベース、ドキュメント管理
3. **GitBook** - 開発ドキュメント、API仕様、バージョン管理
4. **Read the Docs** - ドキュメント自動生成、ホスティング、Sphinx統合
5. **Docusaurus** - モダンドキュメントサイト、React製、バージョン管理

#### その他利用可能なツール

122. MkDocs
123. VuePress
124. Docsify
125. Wiki.js
126. BookStack

---

## 11. コンテナ・オーケストレーション

#### 推奨ツール（生産性が高いもの Top 5）

1. **Docker** - コンテナ化、軽量、環境再現性、開発環境統一
2. **Kubernetes** - コンテナオーケストレーション、スケーリング、サービスメッシュ
3. **Docker Compose** - マルチコンテナ管理、開発環境定義、シンプル
4. **Helm** - Kubernetesパッケージマネージャ、チャート管理、テンプレート
5. **Rancher** - Kubernetes管理、マルチクラスタ、GUI管理

#### その他利用可能なツール

127. OpenShift
128. Amazon ECS
129. Amazon EKS
130. Azure Kubernetes Service (AKS)
131. Google Kubernetes Engine (GKE)

---

## 12. インフラストラクチャ as Code (IaC)

#### 推奨ツール（生産性が高いもの Top 5）

1. **Terraform** - マルチクラウドIaC、宣言的、状態管理、モジュール化
2. **AWS CloudFormation** - AWS専用IaC、JSONYAMLテンプレート、スタック管理
3. **Ansible** - 構成管理、自動化、エージェントレス、YAML
4. **Pulumi** - プログラマブルIaC、TypeScript/Python/Go、既存言語活用
5. **Azure Resource Manager (ARM) Templates** - Azure専用IaC、JSON定義

#### その他利用可能なツール

132. Chef
133. Puppet
134. SaltStack
135. CloudFormation
136. CDK (AWS Cloud Development Kit)
137. Bicep

---

## 13. コラボレーション・コミュニケーション

#### 推奨ツール（生産性が高いもの Top 5）

1. **Slack** - チーム通信、チャンネル、統合豊富、リモートワーク最適
2. **Microsoft Teams** - チャット、会議、ファイル共有、Microsoft 365統合
3. **Discord** - 音声・テキスト通信、開発者コミュニティ、画面共有
4. **Zoom** - ビデオ会議、ウェビナー、画面共有、レコーディング
5. **Google Meet** - ビデオ会議、Google Workspace統合、簡単参加

#### その他利用可能なツール

138. Mattermost
139. Rocket.Chat
140. Webex

---

## 14. セキュリティ・脆弱性管理

#### 推奨ツール（生産性が高いもの Top 5）

1. **Snyk** - 依存関係スキャン、脆弱性検出、自動修正提案、CI/CD統合
2. **Dependabot** (GitHub) - 依存関係更新自動化、セキュリティアラート、PR自動作成
3. **Trivy** - コンテナスキャン、IaCスキャン、高速、包括的
4. **SonarQube** - SAST、コード品質、セキュリティホットスポット
5. **OWASP Dependency-Check** - 依存関係脆弱性スキャン、オープンソース

#### その他利用可能なツール

141. Aqua Security
142. Prisma Cloud
143. Clair
144. Grype
145. WhiteSource/Mend

---

## まとめ：各工程で最も推奨される5つのツール

### 企画フェーズ
1. Miro（アイデア整理）
2. Notion（ドキュメント管理）
3. Microsoft Visio（プロセス可視化）
4. JIRA（プロジェクト管理）
5. Microsoft Project（計画管理）

### 要件定義フェーズ
1. ONES Wiki（AI活用要件定義）
2. Confluence（要件定義書作成）
3. GEAR.indigo（AI駆動設計）
4. Figma（UIプロトタイプ）
5. VISLITE（要件可視化）

### 設計フェーズ
1. Next Design（システム設計）
2. astah*（UMLモデリング）
3. Enterprise Architect（アーキテクチャ設計）
4. draw.io（システム構成図）
5. PlantUML（テキストベースUML）

### 実装フェーズ
1. Visual Studio Code（エディタ）
2. GitHub Copilot（AI コード補完）
3. Git（バージョン管理）
4. GitHub（コード管理・協業）
5. SonarQube（コード品質）

### テストフェーズ
1. pytest/JUnit（単体テスト）
2. Selenium/Cypress（E2Eテスト）
3. Postman（APIテスト）
4. JMeter（性能テスト）
5. OWASP ZAP（セキュリティテスト）

### CI/CD・DevOps
1. GitHub Actions（CI/CD）
2. Docker（コンテナ化）
3. Kubernetes（オーケストレーション）
4. Terraform（IaC）
5. Datadog（監視）

---

## 参考リンク

- [IPA 共通フレーム2013](https://www.ipa.go.jp/publish/secbooks20130304.html)
- [IPA システム開発・保守](https://www.ipa.go.jp/digital/kaihatsu/index.html)
- [ISO/IEC 12207 (Wikipedia)](https://ja.wikipedia.org/wiki/ISO/IEC_12207)
- [共通フレーム (Wikipedia)](https://ja.wikipedia.org/wiki/共通フレーム)

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
