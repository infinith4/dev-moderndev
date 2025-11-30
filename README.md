# dev-moderndev

Modern Development Documentation - IPA共通フレーム2013に基づく開発工程ドキュメントとツールガイド

## 📚 概要

本リポジトリは、IPA（情報処理推進機構）の「共通フレーム2013」に基づいた開発工程のドキュメントと、各工程で使用する推奨ツールの詳細ガイドを提供します。

## 🗂️ ドキュメント構成

### 開発工程ドキュメント

1. **[要件定義](./docs/dev_process_開発工程_2_要件定義.md)**
   - 業務分析、ユースケース分析、画面要件定義、帳票要件定義
   - ファイル要件定義、概念モデリング、外部システム連携要件定義
   - システム方針検討、非機能要件定義

2. **[基本設計（アプリケーション）](./docs/dev_process_開発工程_3_基本設計_アプリケーション.md)**
   - アプリケーション方式設計、画面設計、帳票設計
   - ファイル設計、データベース論理設計
   - 外部システムI/F設計、バッチ設計

3. **[基本設計（インフラ）](./docs/dev_process_開発工程_4_基本設計_インフラ.md)**
   - ネットワーク構成図、サーバー構成図・ハードウェア仕様書
   - ストレージ設計書、セキュリティ設計書
   - 可用性・冗長性設計書、監視・運用設計書

### ツールガイド

- **[📑 ツール索引](./docs/ツール索引.md)** - 全ツールの一覧とカテゴリ別分類、工程別マッピング

#### カテゴリ別ツールドキュメント

**図作成・モデリングツール**
- [Draw.io](./docs/ツール/作図ツール/Draw.io.md) - 無料の多目的図作成ツール
- [Lucidchart](./docs/ツール/作図ツール/Lucidchart.md) - クラウドベースの協業図作成ツール
- [PlantUML](./docs/ツール/作図ツール/PlantUML.md) - テキストベースのUMLツール
- [Microsoft Visio](./docs/ツール/作図ツール/Microsoft_Visio.md) - Microsoft製図作成ツール

**UI/UXデザインツール**
- [Figma](./docs/ツール/UI_UXツール/Figma.md) - クラウドベースのUI/UXデザインツール
- [Adobe XD](./docs/ツール/UI_UXツール/Adobe_XD.md) - Adobe製UI/UXデザインツール

**データベース設計ツール**
- [MySQL Workbench](./docs/ツール/データベースツール/MySQL_Workbench.md) - MySQL公式ER図・DB設計ツール
- [ERDPlus](./docs/ツール/データベースツール/ERDPlus.md) - オンラインER図作成ツール

**API設計・テストツール**
- [Postman](./docs/ツール/APIツール/Postman.md) - API開発・テストプラットフォーム
- [Swagger/OpenAPI](./docs/ツール/APIツール/Swagger_OpenAPI.md) - API仕様書標準フォーマット

**帳票設計ツール**
- [JasperReports](./docs/ツール/帳票ツール/JasperReports.md) - オープンソースJava帳票ツール
- [LibreOffice](./docs/ツール/帳票ツール/LibreOffice.md) - 無料オフィススイート
- [Microsoft Excel](./docs/ツール/帳票ツール/Microsoft_Excel.md) - Excel帳票設計

**バッチ処理ツール**
- [Apache Airflow](./docs/ツール/バッチ処理ツール/Apache_Airflow.md) - ワークフロー管理プラットフォーム

**UMLツール**
- [Enterprise Architect](./docs/ツール/UMLツール/Enterprise_Architect.md) - エンタープライズUMLツール
- [Visual Paradigm](./docs/ツール/UMLツール/Visual_Paradigm.md) - UMLモデリングツール

**プロセスモデリングツール**
- [Bizagi Modeler](./docs/ツール/プロセスモデリングツール/Bizagi_Modeler.md) - BPMNプロセスモデリング
- [Process Street](./docs/ツール/プロセスモデリングツール/Process_Street.md) - プロセス文書化ツール

**監視・運用ツール**
- [Grafana](./docs/ツール/監視ツール/Grafana.md) - オープンソースメトリクス可視化ツール
- [Prometheus](./docs/ツール/監視ツール/Prometheus.md) - 時系列データベース・監視システム

**データ処理ツール**
- [Python Pandas](./docs/ツール/データ処理ツール/Python_Pandas.md) - データ分析・処理ライブラリ

**標準・ガイドライン**
- [IPA非機能要求グレード](./docs/ツール/標準・ガイドライン/IPA_非機能要求グレード.md) - 非機能要件定義ガイド

## 🚀 クイックスタート

### 1. ツールを探す

開発工程に応じて適切なツールを探す場合:

```
1. 📑 ツール索引を開く
2. 工程別ツールマッピングを確認
3. 各ツールのドキュメントリンクをクリック
```

### 2. 工程別ドキュメントを確認

各開発工程の詳細を確認する場合:

```
1. docs/dev_process_開発工程_X_フェーズ名.md を開く
2. 該当するセクションを確認
3. 推奨ツールのドキュメントリンクをクリック
```

### 3. ツールの使い方を学ぶ

特定のツールの使い方を学ぶ場合:

```
1. docs/ツール/カテゴリ名/ツール名.md を開く（またはツール索引から検索）
2. 概要、料金プラン、メリット・デメリットを確認
3. 工程別の活用方法セクションで、該当する開発工程での使い方を確認
4. 公式ドキュメントリンクで詳細を学習
```

## 📖 主要ドキュメント

| ドキュメント | 説明 | リンク |
|------------|------|--------|
| ツール索引 | 全ツールの一覧と工程別マッピング | [📑 ツール索引](./docs/ツール索引.md) |
| 要件定義 | 業務分析、ユースケース分析、非機能要件等 | [📄 要件定義](./docs/dev_process_開発工程_2_要件定義.md) |
| 基本設計（アプリ） | 画面設計、DB設計、API設計等 | [📄 基本設計（アプリ）](./docs/dev_process_開発工程_3_基本設計_アプリケーション.md) |
| 基本設計（インフラ） | ネットワーク設計、監視設計等 | [📄 基本設計（インフラ）](./docs/dev_process_開発工程_4_基本設計_インフラ.md) |
| タスク管理 | プロジェクト改善タスク | [📋 TASKS.md](./TASKS.md) |

## 🛠️ ツール選定ガイド

### 無料ツールで始める

予算が限られている場合は、以下の無料ツールがおすすめ:

- **図作成**: Draw.io, PlantUML
- **UI/UX**: Figma (無料プラン)
- **DB設計**: MySQL Workbench, ERDPlus
- **API**: Postman (無料プラン), Swagger/OpenAPI
- **帳票**: LibreOffice
- **インフラ**: AWS CloudFormation Designer, Diagrams (Python)
- **監視**: Grafana (OSS版), Prometheus

### チーム協業に適したツール

チームでの協業が必要な場合:

- **図作成**: Lucidchart (有料)
- **UI/UX**: Figma (有料プラン)
- **API**: Postman (Team プラン)

### エンタープライズ向けツール

大規模プロジェクト、エンタープライズ案件の場合:

- **図作成**: Microsoft Visio
- **UI/UX**: Adobe XD
- **監視**: Datadog, New Relic (有料)

## 📚 参考資料

- [IPA 共通フレーム2013](https://www.ipa.go.jp/)
- [非機能要求グレード（IPA）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Microsoft Azure Architecture Center](https://docs.microsoft.com/azure/architecture/)

## 🤝 コントリビューション

本リポジトリへの貢献を歓迎します。以下の方法でコントリビュートできます:

1. ツールドキュメントの追加・改善
2. 新しい開発工程ドキュメントの追加
3. 誤字脱字の修正
4. 使用例の追加

## 📝 ライセンス

本リポジトリのドキュメントはMITライセンスの下で公開されています。

---

**最終更新日**: 2025年（令和7年）
**バージョン**: 2.0
