# 開発工程_4_詳細設計（アプリケーション）

## 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**詳細設計プロセス（アプリケーション詳細設計）**における開発タスクと推奨ツールをまとめたものです。

### 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

## 4.1 アプリケーション詳細設計

### 主要タスク
- モジュールの詳細設計
- インタフェースの詳細設計
- データ構造の詳細設計
- アルゴリズムの詳細設計
- API設計・定義

### 推奨ツール（モデリング・設計 Top 10）

基本設計と共通のツールを使用しますが、より詳細なレベルでの設計を行います。

| # | ツール名 | 公式サイト | 概要 | 用途 | メリット | デメリット |
|---|---------|-----------|------|------|---------|-----------|
| 1 | **Enterprise Architect** | [https://sparxsystems.com/](https://sparxsystems.com/) | 多機能UMLモデリングツール。詳細設計からコード生成まで | クラス図、シーケンス図、状態遷移図、コード生成 | ✅ 詳細設計に最適<br>✅ コード生成・逆生成<br>✅ トレーサビリティ<br>✅ 多様な図に対応<br>✅ チーム開発対応 | ❌ 学習曲線非常に急<br>❌ UI複雑<br>❌ 機能過多<br>❌ 動作やや重い |
| 2 | **PlantUML** | [https://plantuml.com/](https://plantuml.com/) | テキストベースUML。Git管理、CI/CD統合に最適 | クラス図、シーケンス図、ER図、コンポーネント図 | ✅ テキストベース<br>✅ Git管理容易<br>✅ CI/CD統合<br>✅ 無料<br>✅ 差分管理容易 | ❌ GUI編集不可<br>❌ 記法学習必要<br>❌ 複雑な図困難<br>❌ レイアウト調整困難 |
| 3 | **Swagger/OpenAPI** | [https://swagger.io/](https://swagger.io/) | API設計・ドキュメント生成ツール。RESTful API定義標準 | REST API設計、API仕様書、インタラクティブドキュメント | ✅ API設計標準<br>✅ 自動ドキュメント生成<br>✅ モック生成<br>✅ コード生成<br>✅ 無料 | ❌ REST専用<br>❌ YAML記述やや複雑<br>❌ GraphQL非対応<br>❌ バージョン管理工夫必要 |
| 4 | **Postman** | [https://www.postman.com/](https://www.postman.com/) | API開発・テストプラットフォーム。設計・ドキュメント・テスト統合 | API設計、モックサーバー、API仕様書、コレクション管理 | ✅ API設計・テスト統合<br>✅ モックサーバー<br>✅ 自動ドキュメント<br>✅ チーム共有<br>✅ 無料プランあり | ❌ 無料版機能制限<br>❌ バージョン管理やや弱い<br>❌ 大規模では有料必須<br>❌ オフライン機能限定的 |
| 5 | **dbdiagram.io** | [https://dbdiagram.io/](https://dbdiagram.io/) | データベース設計ツール。ER図作成、SQL生成 | ER図作成、データベーススキーマ設計、DDL生成 | ✅ シンプルで使いやすい<br>✅ テキストベース<br>✅ SQL自動生成<br>✅ 共有容易<br>✅ 無料プランあり | ❌ 機能基本的<br>❌ 複雑なDB設計困難<br>❌ バージョン管理弱い<br>❌ オフライン不可 |
| 6 | **MySQL Workbench** | [https://www.mysql.com/products/workbench/](https://www.mysql.com/products/workbench/) | MySQL公式DB設計・管理ツール。ER図、SQL開発、管理 | データベース設計、ER図、SQL開発、リバースエンジニアリング | ✅ MySQL公式<br>✅ 完全無料<br>✅ ER図作成<br>✅ リバースエンジニアリング<br>✅ SQL開発環境 | ❌ MySQL専用<br>❌ UI古め<br>❌ 動作やや重い<br>❌ 学習コストあり |
| 7 | **draw.io (diagrams.net)** | [https://www.diagrams.net/](https://www.diagrams.net/) | 汎用図作成ツール。クラス図、ER図、フローチャート | クラス図、ER図、フローチャート、コンポーネント図 | ✅ 完全無料<br>✅ 多様な図対応<br>✅ テンプレート豊富<br>✅ GitHub/Drive統合<br>✅ ブラウザ/デスクトップ | ❌ 専門ツール比で機能劣る<br>❌ コード生成不可<br>❌ コラボ機能弱い<br>❌ 大規模管理困難 |
| 8 | **Visual Paradigm** | [https://www.visual-paradigm.com/](https://www.visual-paradigm.com/) | 総合モデリングツール。UML、ER、BPMN、コード生成 | 詳細設計、クラス図、ER図、コード生成、リバースエンジニアリング | ✅ 多機能統合<br>✅ コード生成豊富<br>✅ データベース設計<br>✅ リバースエンジニアリング<br>✅ チーム開発 | ❌ 高額（$99/月〜）<br>❌ 機能過多で複雑<br>❌ 動作重い<br>❌ 学習コスト高 |
| 9 | **Mermaid** | [https://mermaid.js.org/](https://mermaid.js.org/) | JavaScriptダイアグラムライブラリ。Markdown統合、Git管理 | フローチャート、シーケンス図、クラス図、ER図（Markdown内） | ✅ Markdown統合<br>✅ Git管理容易<br>✅ 無料オープンソース<br>✅ GitHub対応<br>✅ 軽量 | ❌ 機能限定的<br>❌ 複雑な図困難<br>❌ レイアウト制御弱い<br>❌ エクスポート形式限定 |
| 10 | **Stoplight Studio** | [https://stoplight.io/](https://stoplight.io/) | API設計プラットフォーム。OpenAPI、モック、ドキュメント | API詳細設計、OpenAPI定義、モックサーバー、ドキュメント | ✅ API設計特化<br>✅ ビジュアルエディタ<br>✅ モックサーバー<br>✅ Git統合<br>✅ 無料プランあり | ❌ API設計以外不向き<br>❌ 有料プラン推奨<br>❌ 学習コストあり<br>❌ 大規模では高額 |

### その他利用可能なツール

- StarUML
- astah*
- Lucidchart
- Cacoo
- pgModeler (PostgreSQL)
- DBeaver
- ERDPlus
- QuickDBD

---

## IPA公式資料・ガイド

| 資料名 | 概要 | 用途 | リンク |
|-------|------|------|--------|
| **組込みソフトウェア向け 設計ガイド [事例編] ESDR** | 組込みソフトウェアの設計品質向上のための実践的なガイド。詳細設計における設計プロセスとレビュー手法を解説 | プログラム詳細設計、クラス図・シーケンス図作成、設計レビュー、品質向上 | [IPA公式サイト](https://www.ipa.go.jp/archive/publish/qv6pgp0000001009-att/000005148.pdf) |
| **API標準設計ガイド・基礎編** | REST API詳細設計の標準的な設計手法を解説。詳細なエンドポイント設計、データモデル設計を支援 | API詳細設計、インターフェース詳細設計、RESTful API設計 | [IPA公式サイト](https://www.ipa.go.jp/digital/data/jod03a000000a82y-att/api_standard_design_guide.pdf) |
| **機能要件の合意形成ガイド（データモデル編）** | データベース物理設計における詳細な設計手法。テーブル定義、インデックス設計、正規化を支援 | データベース物理設計、物理ER図作成、テーブル定義書作成 | [IPA公式サイト](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) |

---

**関連ドキュメント**:
- [4. インフラ設計・構築](./dev_process_開発工程_4_インフラ設計・構築.md)
- [5. 実装（アプリケーション）](./dev_process_開発工程_5_実装_アプリケーション.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
