# 開発工程_5_実装（アプリケーション）

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

**関連ドキュメント**:
- [5. 実装（インフラ）](./dev_process_開発工程_5_実装_インフラ.md)
- [6. アプリケーションテスト](./dev_process_開発工程_6_アプリケーションテスト.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0
