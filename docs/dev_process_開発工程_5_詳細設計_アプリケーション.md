# 開発工程_4_詳細設計（アプリケーション）

## 1. 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**詳細設計プロセス（アプリケーション詳細設計）**における開発タスクと推奨ツールをまとめたものです。

### 1.1. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

### 1.2. 共通

**推奨ツール（モデリング・設計 Top 10）**

基本設計と共通のツールを使用しますが、より詳細なレベルでの設計を行います。

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **PlantUML** | [https://plantuml.com/](https://plantuml.com/) | テキストベースUML。Git管理、CI/CD統合に最適 | クラス図、シーケンス図、ER図、コンポーネント図 | ✅ テキストベース<br>✅ Git管理容易<br>✅ CI/CD統合<br>✅ 無料<br>✅ 差分管理容易 | ❌ GUI編集不可<br>❌ 記法学習必要<br>❌ 複雑な図困難<br>❌ レイアウト調整困難 |
| 2 | **Swagger/OpenAPI** | [https://swagger.io/](https://swagger.io/) | API設計・ドキュメント生成ツール。RESTful API定義標準 | REST API設計、API仕様書、インタラクティブドキュメント | ✅ API設計標準<br>✅ 自動ドキュメント生成<br>✅ モック生成<br>✅ コード生成<br>✅ 無料 | ❌ REST専用<br>❌ YAML記述やや複雑<br>❌ GraphQL非対応<br>❌ バージョン管理工夫必要 |
| 3 | **Postman** | [https://www.postman.com/](https://www.postman.com/) | API開発・テストプラットフォーム。設計・ドキュメント・テスト統合 | API設計、モックサーバー、API仕様書、コレクション管理 | ✅ API設計・テスト統合<br>✅ モックサーバー<br>✅ 自動ドキュメント<br>✅ チーム共有<br>✅ 無料プランあり | ❌ 無料版機能制限<br>❌ バージョン管理やや弱い<br>❌ 大規模では有料必須<br>❌ オフライン機能限定的 |
| 4 | **dbdiagram.io** | [https://dbdiagram.io/](https://dbdiagram.io/) | データベース設計ツール。ER図作成、SQL生成 | ER図作成、データベーススキーマ設計、DDL生成 | ✅ シンプルで使いやすい<br>✅ テキストベース<br>✅ SQL自動生成<br>✅ 共有容易<br>✅ 無料プランあり | ❌ 機能基本的<br>❌ 複雑なDB設計困難<br>❌ バージョン管理弱い<br>❌ オフライン不可 |
| 5 | **MySQL Workbench** | [https://www.mysql.com/products/workbench/](https://www.mysql.com/products/workbench/) | MySQL公式DB設計・管理ツール。ER図、SQL開発、管理 | データベース設計、ER図、SQL開発、リバースエンジニアリング | ✅ MySQL公式<br>✅ 完全無料<br>✅ ER図作成<br>✅ リバースエンジニアリング<br>✅ SQL開発環境 | ❌ MySQL専用<br>❌ UI古め<br>❌ 動作やや重い<br>❌ 学習コストあり |
| 6 | **draw.io (diagrams.net)** | [https://www.diagrams.net/](https://www.diagrams.net/) | 汎用図作成ツール。クラス図、ER図、フローチャート | クラス図、ER図、フローチャート、コンポーネント図 | ✅ 完全無料<br>✅ 多様な図対応<br>✅ テンプレート豊富<br>✅ GitHub/Drive統合<br>✅ ブラウザ/デスクトップ | ❌ 専門ツール比で機能劣る<br>❌ コード生成不可<br>❌ コラボ機能弱い<br>❌ 大規模管理困難 |
| 7 | **Visual Paradigm** | [https://www.visual-paradigm.com/](https://www.visual-paradigm.com/) | 総合モデリングツール。UML、ER、BPMN、コード生成 | 詳細設計、クラス図、ER図、コード生成、リバースエンジニアリング | ✅ 多機能統合<br>✅ コード生成豊富<br>✅ データベース設計<br>✅ リバースエンジニアリング<br>✅ チーム開発 | ❌ 高額（$99/月〜）<br>❌ 機能過多で複雑<br>❌ 動作重い<br>❌ 学習コスト高 |
| 8 | **Mermaid** | [https://mermaid.js.org/](https://mermaid.js.org/) | JavaScriptダイアグラムライブラリ。Markdown統合、Git管理 | フローチャート、シーケンス図、クラス図、ER図（Markdown内） | ✅ Markdown統合<br>✅ Git管理容易<br>✅ 無料オープンソース<br>✅ GitHub対応<br>✅ 軽量 | ❌ 機能限定的<br>❌ 複雑な図困難<br>❌ レイアウト制御弱い<br>❌ エクスポート形式限定 |
| 9 | **Stoplight Studio** | [https://stoplight.io/](https://stoplight.io/) | API設計プラットフォーム。OpenAPI、モック、ドキュメント | API詳細設計、OpenAPI定義、モックサーバー、ドキュメント | ✅ API設計特化<br>✅ ビジュアルエディタ<br>✅ モックサーバー<br>✅ Git統合<br>✅ 無料プランあり | ❌ API設計以外不向き<br>❌ 有料プラン推奨<br>❌ 学習コストあり<br>❌ 大規模では高額 |

<!-- ### その他利用可能なツール

- StarUML
- astah*
- Lucidchart
- Cacoo
- pgModeler (PostgreSQL)
- DBeaver
- ERDPlus
- QuickDBD -->

---

---

## 2. プログラム設計

**対応項目**
- プログラム設計

**成果物**
- クラス図
- シーケンス図
- ステートマシン図
- コンポーネント図

**有用なツール**

| ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---------|------|------|------|---------|----------|
| [**PlantUML**](https://plantuml.com/) | テキストベースUML。Git管理、CI/CD統合に最適。 | クラス図、シーケンス図、ER図、コンポーネント図、ステート図 | 🟢 完全無料 | ✅ テキストで記述<br>✅ Git管理容易<br>✅ CI/CD統合可能<br>✅ 差分管理容易<br>✅ 完全無料 | ❌ GUI編集不可<br>❌ 記法学習必要<br>❌ 複雑な図困難<br>❌ レイアウト調整困難 |
| [**draw.io**](https://www.diagrams.net/) | 汎用図作成ツール。クラス図、ER図、フローチャートに対応。 | クラス図、ER図、フローチャート、コンポーネント図、デプロイメント図 | 🟢 完全無料 | ✅ 完全無料<br>✅ 多様な図対応<br>✅ テンプレート豊富<br>✅ GitHub/Drive統合<br>✅ ブラウザ/デスクトップ対応 | ❌ 専門ツール比で機能劣る<br>❌ コード生成不可<br>❌ コラボ機能弱い<br>❌ 大規模管理困難 |
| [**Mermaid**](https://mermaid.js.org/) | JavaScriptダイアグラムライブラリ。Markdown統合、Git管理に最適。 | フローチャート、シーケンス図、クラス図、ER図（Markdown内）、ガントチャート | 🟢 完全無料 | ✅ Markdown統合<br>✅ Git管理容易<br>✅ 無料オープンソース<br>✅ GitHub対応<br>✅ 軽量で高速 | ❌ 機能限定的<br>❌ 複雑な図困難<br>❌ レイアウト制御弱い<br>❌ エクスポート形式限定 |
| [**Visual Paradigm**](https://www.visual-paradigm.com/) | 総合モデリングツール。UML、ER、BPMN、コード生成対応。 | 詳細設計、クラス図、ER図、コード生成、リバースエンジニアリング | 💰 $99/月～<br>🟢 Community Edition無料 | ✅ 多機能統合<br>✅ コード生成豊富<br>✅ データベース設計<br>✅ リバースエンジニアリング<br>✅ チーム開発対応 | ❌ 高額（$99/月～）<br>❌ 機能過多で複雑<br>❌ 動作重い<br>❌ 学習コスト高い |
| [**StarUML**](https://staruml.io/) | モダンUIのUMLツール。拡張機能とテーマカスタマイズに対応。 | UMLモデリング、クラス図、ER図、コード生成・逆生成 | 💰 $89（買い切り）<br>💰 $4.99/月（サブスク） | ✅ モダンで美しいUI<br>✅ 軽量で高速<br>✅ 拡張機能対応<br>✅ コード生成・逆生成<br>✅ 安価 | ❌ 商用ツール比で機能少<br>❌ チーム開発機能弱い<br>❌ 日本語ドキュメント少ない<br>❌ サポート限定的 |

**有用なドキュメント**

| 資料名 | 概要 | リンク |
|-------|------|--------|
| **UML2.5仕様書** | UML標準仕様。クラス図、シーケンス図の詳細説明 | [OMG 公式](https://www.omg.org/) |
| **デザインパターン（GOF）** | オブジェクト指向設計の24個のデザインパターン | [Wikipedia](https://en.wikipedia.org/wiki/Software_design_pattern) |
| **SOLID原則ガイド** | オブジェクト指向設計の5つの基本原則 | [Martin Fowler Blog](https://martinfowler.com/) |

---

## 3. API詳細設計

**対応項目**
- API詳細設計

**成果物**
- API仕様書
- エンドポイント定義書
- リクエスト/レスポンススキーマ定義
- エラーハンドリング仕様

**有用なツール**

| ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---------|------|------|------|---------|----------|
| [**Swagger/OpenAPI**](https://swagger.io/) | API設計・ドキュメント生成ツール。RESTful API定義標準。 | REST API設計、API仕様書、インタラクティブドキュメント、モック生成 | 🟢 完全無料 | ✅ API設計業界標準<br>✅ 自動ドキュメント生成<br>✅ モック生成機能<br>✅ コード生成<br>✅ 多言語対応 | ❌ REST専用<br>❌ YAML記述やや複雑<br>❌ GraphQL非対応<br>❌ バージョン管理工夫必要 |
| [**Postman**](https://www.postman.com/) | API開発・テストプラットフォーム。設計・テスト統合。 | API設計、モックサーバー、API仕様書、テスト、コレクション管理 | 🟢 無料プランあり<br>💰 Pro: $12/月<br>💰 Business: $25/月 | ✅ API設計・テスト統合<br>✅ モックサーバー<br>✅ 自動ドキュメント<br>✅ チーム共有<br>✅ 直感的UI | ❌ 無料版機能制限<br>❌ バージョン管理やや弱い<br>❌ 大規模では有料必須<br>❌ オフライン機能限定的 |
| [**Stoplight Studio**](https://stoplight.io/) | API設計プラットフォーム。OpenAPI、モック、ドキュメント。 | API詳細設計、OpenAPI定義、モックサーバー、ドキュメント生成 | 🟢 無料プランあり<br>💰 Pro: $79/月<br>💰 Team: カスタム価格 | ✅ API設計特化<br>✅ ビジュアルエディタ<br>✅ モックサーバー<br>✅ Git統合<br>✅ OpenAPI完全対応 | ❌ API設計以外不向き<br>❌ 有料プラン推奨<br>❌ 学習コストあり<br>❌ 大規模では高額 |
| [**ReDoc**](https://redoc.ly/) | OpenAPIドキュメント自動生成。美しいドキュメント出力。 | API仕様書生成、ドキュメント、インタラクティブリファレンス | 🟢 完全無料 | ✅ 美しいドキュメント生成<br>✅ OpenAPI連携<br>✅ レスポンシブ対応<br>✅ 無料<br>✅ 導入簡単 | ❌ ドキュメント生成のみ<br>❌ API設計機能なし<br>❌ カスタマイズ限定的<br>❌ エディタ機能なし |
| [**Insomnia**](https://insomnia.rest/) | API設計・テストツール。Postmanのオープンソース代替。 | API設計、テスト、GraphQL対応、モック | 🟢 完全無料 | ✅ オープンソース無料<br>✅ GraphQL対応<br>✅ プラグイン豊富<br>✅ ローカル管理<br>✅ 軽量 | ❌ ユーザー数少ない<br>❌ ドキュメント生成は弱い<br>❌ 機能はPostmanより劣る<br>❌ コミュニティ規模小さい |

**有用なドキュメント**

| 資料名 | 概要 | リンク |
|-------|------|--------|
| **REST API設計ガイド** | RESTful APIの設計ベストプラクティス | [REST Tutorial](https://www.restapitutorial.com/) |
| **OpenAPI 3.0仕様** | OpenAPI標準仕様書 | [OpenAPI Spec](https://spec.openapis.org/oas/v3.0.3) |
| **API標準設計ガイド・詳細編（IPA）** | REST API詳細設計の標準的な設計手法 | [IPA 公式](https://www.ipa.go.jp/digital/data/jod03a000000a82y-att/api_standard_design_guide.pdf) |
| **GraphQL設計ガイド** | GraphQL APIの設計とベストプラクティス | [GraphQL 公式](https://graphql.org/learn/best-practices/) |

---

## 4. 実装方針策定

**対応項目**
- 実装方針策定

**成果物**
- 実装ガイド
- コーディング規約
- 命名規則
- ディレクトリ構成

**有用なツール**

| ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---------|------|------|------|---------|----------|
| [**ESLint**](https://eslint.org/) | JavaScriptコード解析ツール。コーディング規約の自動チェック。 | コード品質管理、コーディング規約の自動適用、スタイルガイド | 🟢 完全無料 | ✅ 完全無料<br>✅ 完全カスタマイズ可能<br>✅ プラグイン豊富<br>✅ IDE統合<br>✅ 自動修正機能 | ❌ JavaScript/TypeScript専用<br>❌ 初期設定が複雑<br>❌ ルール数多く学習必要<br>❌ パフォーマンス調整必要 |
| [**Prettier**](https://prettier.io/) | コードフォーマッター。自動的に統一されたコード形式を適用。 | コード自動フォーマット、スタイル統一、コーディング規約適用 | 🟢 完全無料 | ✅ 完全無料<br>✅ 複数言語対応<br>✅ 設定最小限<br>✅ IDE統合<br>✅ 自動修正 | ❌ カスタマイズ限定的<br>❌ 完全無料ため機能限定<br>❌ スタイル微調整困難<br>❌ 学習曲線やや急 |
| [**SonarQube**](https://www.sonarqube.org/) | コード品質管理プラットフォーム。コード分析、品質基準管理。 | コード品質管理、テストカバレッジ管理、技術負債追跡 | 🟢 Community無料<br>💰 Developer: $330/年<br>💰 Enterprise: 見積 | ✅ 包括的なコード分析<br>✅ テストカバレッジ管理<br>✅ セキュリティスキャン<br>✅ トレンド追跡<br>✅ 複数言語対応 | ❌ セットアップが複雑<br>❌ 企業版は高額<br>❌ 保守運用負荷高い<br>❌ 学習曲線が急 |
| [**Google Style Guides**](https://google.github.io/styleguide/) | Google公式コーディング規約。複数言語対応。 | コーディング規約、ベストプラクティス、実装方針 | 🟢 完全無料 | ✅ 業界標準<br>✅ 複数言語対応<br>✅ 詳細かつ実践的<br>✅ 無料<br>✅ 業界で高い評価 | ❌ Google流で団体に不合致の可能性<br>❌ カスタマイズ必要<br>❌ 全言語カバーせず<br>❌ 定期更新が必要 |
| [**Markdown**](https://www.markdownguide.org/) | テキストベースのドキュメント形式。実装ガイド、規約書作成に最適。 | 実装ガイド、コーディング規約、ドキュメント作成 | 🟢 完全無料 | ✅ テキストベース<br>✅ Git管理容易<br>✅ バージョン管理<br>✅ 軽量で高速<br>✅ 多くのツール対応 | ❌ 凝ったレイアウト困難<br>❌ 大規模ドキュメント管理困難<br>❌ バージョン管理工夫必要<br>❌ テンプレート機能限定 |

**有用なドキュメント**

| 資料名 | 概要 | リンク |
|-------|------|--------|
| **Clean Code** | Robert C. Martin著。コード品質の必読書 | [Amazon](https://www.amazon.com/) |
| **Code Complete** | Steve McConnell著。実装ベストプラクティス | [Amazon](https://www.amazon.com/) |
| **Google Python Style Guide** | Python公式コーディング規約 | [Google](https://google.github.io/styleguide/pyguide.html) |
| **Microsoft C# Coding Conventions** | C#公式コーディング規約 | [Microsoft](https://docs.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions) |

---

## 5. データベース物理設計

**対応項目**
- データベース物理設計

**成果物**
- 物理ER図
- テーブル定義書
- インデックス設計書
- パーティショニング設計書

**有用なツール**

| ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---------|------|------|------|---------|----------|
| [**MySQL Workbench**](https://www.mysql.com/products/workbench/) | MySQL公式DB設計・管理ツール。ER図、SQL開発、管理。 | データベース設計、ER図、SQL開発、リバースエンジニアリング | 🟢 完全無料 | ✅ MySQL公式<br>✅ 完全無料<br>✅ ER図作成<br>✅ リバースエンジニアリング<br>✅ SQL開発環境 | ❌ MySQL専用<br>❌ UI古め<br>❌ 動作やや重い<br>❌ 学習コストあり |
| [**dbdiagram.io**](https://dbdiagram.io/) | データベース設計ツール。ER図作成、SQL生成。 | ER図作成、データベーススキーマ設計、DDL生成、共有 | 🟢 無料プランあり<br>💰 Premium: $12/月 | ✅ シンプルで使いやすい<br>✅ テキストベース<br>✅ SQL自動生成<br>✅ 共有容易<br>✅ ブラウザで動作 | ❌ 機能基本的<br>❌ 複雑なDB設計困難<br>❌ バージョン管理弱い<br>❌ オフライン不可 |
| [**DBeaver**](https://dbeaver.io/) | 統合DB管理ツール。複数DB対応、ER図作成。 | データベース管理、ER図作成、SQL開発、リバースエンジニアリング | 🟢 Community無料<br>💰 Pro: $99.99/年<br>💰 Enterprise: カスタム | ✅ 複数DB対応<br>✅ 機能充実<br>✅ ER図作成<br>✅ リバースエンジニアリング<br>✅ Community無料 | ❌ UI複雑<br>❌ 学習曲線が急<br>❌ 動作やや重い<br>❌ Pro版で高額 |
| [**pgModeler**](https://pgmodeler.io/) | PostgreSQL向けER図ツール。物理設計に最適。 | PostgreSQL ER図作成、テーブル定義、DDL生成 | 🟢 無料<br>💰 Pro: 一度限りの購入 | ✅ PostgreSQL特化<br>✅ 無料<br>✅ ER図作成<br>✅ DDL生成<br>✅ リバースエンジニアリング | ❌ PostgreSQL専用<br>❌ 他DBサポートなし<br>❌ UI古め<br>❌ コミュニティ規模小さい |
| [**tbls**](./ツール/データベース/tbls.md) | 既存DBからER図・ドキュメント自動生成CLI。リバースエンジニアリング特化。 | 既存DBドキュメント化、ER図自動生成、CI/CD統合 | 🟢 完全無料 | ✅ リバースエンジニアリング<br>✅ 多様なDB対応<br>✅ Markdown/ER図自動生成<br>✅ CI/CD統合容易<br>✅ PlantUML/Mermaid出力 | ❌ CLI専用（GUI非対応）<br>❌ フォワード設計不可<br>❌ インタラクティブ編集不可<br>❌ 学習コスト |
| [**draw.io**](https://www.diagrams.net/) | 汎用図作成ツール。ER図、テーブル定義図に対応。 | ER図作成、データベース構造図、物理設計図 | 🟢 完全無料 | ✅ 完全無料<br>✅ 多様な図対応<br>✅ テンプレート豊富<br>✅ GitHub/Drive統合<br>✅ ブラウザ/デスクトップ | ❌ DB設計機能限定<br>❌ SQL生成不可<br>❌ コード生成不可<br>❌ 大規模管理困難 |

**有用なドキュメント**

| 資料名 | 概要 | リンク |
|-------|------|--------|
| **データベース設計ガイドライン（IPA）** | 正規化と最適化の基本、物理設計のポイント | [IPA 公式](https://www.ipa.go.jp/) |
| **PostgreSQL ドキュメント** | PostgreSQL物理設計、パーティショニングガイド | [PostgreSQL](https://www.postgresql.org/docs/) |
| **MySQL 最適化ガイド** | MySQL物理設計、インデックス設計 | [MySQL Docs](https://dev.mysql.com/doc/) |
| **データベース正規化ガイド** | 第1～3正規形、BCNF解説 | [Wikipedia](https://en.wikipedia.org/wiki/Database_normalization) |

---

## 6. 開発環境構築

**対応項目**
- 開発環境構築

**成果物**
- 開発構築手順書
- 開発環境セットアップスクリプト
- Docker/仮想環境設定
- IDE設定ファイル

**有用なツール**

| ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---------|------|------|------|---------|----------|
| [**DevContainer (VS Code)**](https://code.visualstudio.com/docs/devcontainers/containers) | コンテナベース開発環境。VS Code統合で即座に開発開始。 | 開発環境構築、チーム環境統一、リモート開発、Docker開発 | 🟢 完全無料 | ✅ 完全無料<br>✅ 環境統一容易<br>✅ VS Code統合<br>✅ 設定ファイル共有<br>✅ 即座に開発開始 | ❌ VS Code必須<br>❌ Docker必要<br>❌ 初期ビルド時間<br>❌ リソース消費多い |
| [**Docker**](https://www.docker.com/) | コンテナ化プラットフォーム。開発環境の標準化。 | 開発環境構築、環境標準化、マイクロサービス開発 | 🟢 完全無料 | ✅ 完全無料<br>✅ 環境標準化<br>✅ 再現性高い<br>✅ 本番環境と同一<br>✅ デプロイメント簡単 | ❌ 学習曲線が急<br>❌ Windowsでは制限あり<br>❌ リソース消費多い<br>❌ ネットワーク設定複雑 |
| [**Vagrant**](https://www.vagrantup.com/) | 仮想マシン管理ツール。開発環境を簡単に構築・共有。 | 開発環境構築、チーム間での環境統一、オンプレ開発 | 🟢 完全無料 | ✅ 完全無料<br>✅ 環境再現性高い<br>✅ マルチプラットフォーム<br>✅ スクリプト自動化<br>✅ チーム共有容易 | ❌ 仮想マシン起動が遅い<br>❌ Dockerより重い<br>❌ リソース消費多い<br>❌ ディスク容量多要 |
| [**VS Code**](https://code.visualstudio.com/) | 軽量マルチ言語コードエディタ。拡張機能で機能拡張。 | 開発環境、IDE、デバッグ環境、ターミナル | 🟢 完全無料 | ✅ 完全無料<br>✅ 軽量で高速<br>✅ 拡張機能豊富<br>✅ 複数言語対応<br>✅ Git統合 | ❌ IDE比で機能やや少ない<br>❌ 大規模プロジェクト向けでない<br>❌ 標準設定では限定的<br>❌ メモリ使用量増加 |
| [**JetBrains IDEs**](https://www.jetbrains.com/) | 言語別フル機能IDE。IntelliJ、PyCharm、WebStormなど。 | フル機能開発環境、デバッグ、リファクタリング、テスト | 💰 $99～299/年<br>🟢 Community無料版あり | ✅ フル機能IDE<br>✅ 高度な機能<br>✅ デバッグ優秀<br>✅ リファクタリング豊富<br>✅ チーム開発対応 | ❌ 高額（商用は$99~/年）<br>❌ 動作重い<br>❌ 学習曲線が急<br>❌ メモリ使用量多い |
| [**Git**](https://git-scm.com/) | 分散バージョン管理システム。チーム開発の標準。 | バージョン管理、チーム開発、ブランチ管理、コンフリクト解決 | 🟢 完全無料 | ✅ 完全無料<br>✅ 業界標準<br>✅ 分散管理<br>✅ ブランチ管理優秀<br>✅ パフォーマンス高い | ❌ 学習曲線が急<br>❌ コマンドライン主体<br>❌ マージ競合管理複雑<br>❌ GUI使いにくい |
| [**GitHub / GitLab**](https://github.com/) | リモートリポジトリ、CI/CD、チーム開発プラットフォーム。 | リモートリポジトリ管理、CI/CD、プロジェクト管理、ドキュメント | 🟢 無料プランあり<br>💰 Pro: $4/月<br>💰 Team: $21/月 | ✅ リモート管理<br>✅ CI/CD統合<br>✅ イシュー管理<br>✅ プルリクエスト<br>✅ ドキュメント統合 | ❌ ネットワーク依存<br>❌ プライベートは有料<br>❌ 大規模では高額<br>❌ エンタープライズは別途 |

**有用なドキュメント**

| 資料名 | 概要 | リンク |
|-------|------|--------|
| **Docker公式ドキュメント** | Docker導入・運用ガイド | [Docker Docs](https://docs.docker.com/) |
| **Vagrant公式ガイド** | Vagrant環境構築ガイド | [Vagrant](https://www.vagrantup.com/docs) |
| **Git 完全ガイド** | Git基本操作からチーム開発まで | [Pro Git Book](https://git-scm.com/book) |
| **開発環境構築ベストプラクティス（IPA）** | 開発環境の標準化、構築手順 | [IPA 公式](https://www.ipa.go.jp/) |

---

## 総合推奨ツール（詳細設計 Top 10）

| # | ツール名 | 概要 | 用途 | 料金 | メリット | デメリット |
|---|---------|------|------|------|---------|----------|
| 1 | [**PlantUML**](https://plantuml.com/) | テキストベースUML。Git管理、CI/CD統合に最適。 | クラス図、シーケンス図、ER図、コンポーネント図、バージョン管理 | 🟢 完全無料 | ✅ テキストベース<br>✅ Git管理容易<br>✅ CI/CD統合<br>✅ 無料<br>✅ 差分管理 | ❌ GUI編集不可<br>❌ 記法学習必要<br>❌ 複雑な図困難<br>❌ レイアウト調整困難 |
| 2 | [**Swagger/OpenAPI**](https://swagger.io/) | API設計・ドキュメント生成ツール。REST API定義標準。 | API設計、仕様書、ドキュメント、モック、コード生成 | 🟢 完全無料 | ✅ 業界標準<br>✅ ドキュメント自動生成<br>✅ モック生成<br>✅ コード生成<br>✅ 多言語対応 | ❌ REST専用<br>❌ YAML記述複雑<br>❌ GraphQL非対応<br>❌ バージョン管理工夫必要 |
| 3 | [**Postman**](https://www.postman.com/) | API開発・テストプラットフォーム。設計・テスト統合。 | API設計、テスト、モックサーバー、ドキュメント、コレクション | 🟢 無料プランあり<br>💰 Pro: $12/月 | ✅ 設計・テスト統合<br>✅ モックサーバー<br>✅ 自動ドキュメント<br>✅ チーム共有<br>✅ 直感的UI | ❌ 無料版機能制限<br>❌ バージョン管理弱い<br>❌ 大規模では有料<br>❌ オフライン限定的 |
| 4 | [**Docker**](https://www.docker.com/) | コンテナ化プラットフォーム。開発環境標準化。 | 開発環境構築、標準化、本番環境統一、マイクロサービス | 🟢 完全無料 | ✅ 完全無料<br>✅ 環境標準化<br>✅ 再現性高い<br>✅ 本番統一<br>✅ デプロイ簡単 | ❌ 学習曲線急<br>❌ Windows制限<br>❌ リソース多量<br>❌ ネットワーク複雑 |
| 5 | [**dbdiagram.io**](https://dbdiagram.io/) | データベース設計ツール。ER図作成、SQL生成。 | ER図作成、スキーマ設計、DDL生成、共有 | 🟢 無料プランあり<br>💰 Premium: $12/月 | ✅ シンプル<br>✅ テキストベース<br>✅ SQL自動生成<br>✅ 共有容易<br>✅ ブラウザ動作 | ❌ 機能基本的<br>❌ 複雑設計困難<br>❌ バージョン管理弱い<br>❌ オフライン不可 |
| 6 | [**MySQL Workbench**](https://www.mysql.com/products/workbench/) | MySQL公式DB設計・管理ツール。ER図、SQL開発。 | DB設計、ER図、SQL開発、リバースエンジニアリング | 🟢 完全無料 | ✅ MySQL公式<br>✅ 完全無料<br>✅ ER図作成<br>✅ リバース機能<br>✅ SQL環境 | ❌ MySQL専用<br>❌ UI古め<br>❌ 動作重い<br>❌ 学習コスト |
| 7 | [**VS Code**](https://code.visualstudio.com/) | 軽量マルチ言語エディタ。拡張機能豊富。 | コード編集、デバッグ、ターミナル、Git統合、拡張機能 | 🟢 完全無料 | ✅ 完全無料<br>✅ 軽量高速<br>✅ 拡張機能豊富<br>✅ 複数言語<br>✅ Git統合 | ❌ IDE比で機能少<br>❌ 大規模向けでない<br>❌ 標準では限定<br>❌ メモリ増加 |
| 8 | [**draw.io**](https://www.diagrams.net/) | 汎用図作成ツール。UML、ER、フローチャート対応。 | 各種図作成、ER図、クラス図、フローチャート | 🟢 完全無料 | ✅ 完全無料<br>✅ 多様な図<br>✅ テンプレート<br>✅ GitHub統合<br>✅ ブラウザ/デスク | ❌ 機能比限定<br>❌ コード生成不可<br>❌ コラボ弱い<br>❌ 大規模困難 |
| 9 | [**Git / GitHub**](https://github.com/) | 分散バージョン管理・チーム開発プラットフォーム。 | コード管理、チーム開発、CI/CD、リポジトリ、プロジェクト管理 | 🟢 無料プランあり<br>💰 Pro: $4/月 | ✅ 業界標準<br>✅ 分散管理<br>✅ CI/CD統合<br>✅ チーム機能<br>✅ リモート対応 | ❌ 学習曲線急<br>❌ CLI主体<br>❌ マージ複雑<br>❌ 大規模は高額 |

---

## IPA公式資料・ガイド

| 資料名 | 概要 | 用途 | リンク |
|-------|------|------|--------|
| **組込みソフトウェア向け設計ガイド [事例編] ESDR** | 組込みソフトウェアの設計品質向上のための実践的ガイド。詳細設計における設計プロセスとレビュー手法を解説。 | プログラム詳細設計、クラス図・シーケンス図作成、設計レビュー、品質向上 | [IPA公式](https://www.ipa.go.jp/archive/publish/qv6pgp0000001009-att/000005148.pdf) |
| **API標準設計ガイド・詳細編** | REST API詳細設計の標準的な設計手法。詳細なエンドポイント設計、データモデル設計を支援。 | API詳細設計、インターフェース詳細設計、RESTful API実装 | [IPA公式](https://www.ipa.go.jp/digital/data/jod03a000000a82y-att/api_standard_design_guide.pdf) |
| **機能要件の合意形成ガイド（データモデル編）** | データベース物理設計における詳細な設計手法。テーブル定義、インデックス設計、正規化を支援。 | データベース物理設計、物理ER図作成、テーブル定義書作成、インデックス設計 | [IPA公式](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |
| **詳細設計書の書き方** | 詳細設計書作成のポイント、設計レビュー基準を解説。 | 詳細設計書作成、品質基準、レビュー方法 | [IPA 公式](https://www.ipa.go.jp/) |

---

---

**関連ドキュメント**:
- [4. インフラ設計・構築](./dev_process_開発工程_4_インフラ設計・構築.md)
- [5. 実装（アプリケーション）](./dev_process_開発工程_5_実装_アプリケーション.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
