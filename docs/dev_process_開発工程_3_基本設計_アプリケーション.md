# 開発工程_3_基本設計（アプリケーション）

- [1. 概要](#1-概要)
  - [1.1. 共通](#11-共通)
- [2. 画面設計](#2-画面設計)
- [3. 帳票設計](#3-帳票設計)
- [4. ファイル設計](#4-ファイル設計)
- [5. データベース論理設計](#5-データベース論理設計)
- [6. 外部システムI/F設計](#6-外部システムif設計)
- [7. バッチ設計](#7-バッチ設計)
- [8. セキュリティ設計](#8-セキュリティ設計)
- [9. 運用設計](#9-運用設計)
- [10. 参考資料](#10-参考資料)

## 1. 概要

基本設計（アプリケーション）のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.1. 共通

**対応項目**
- アプリケーション基本設計
- 設計方針の定義
- 設計成果物の作成・レビュー

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [ユーザのための要件定義ガイド 第2版](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | 要件から基本設計への落とし込み |
| [機能要件の合意形成ガイド（画面編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 画面設計・画面仕様の合意形成 |
| [機能要件の合意形成ガイド（データモデル編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | データモデル設計・用語統一 |
| [機能要件の合意形成ガイド（バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | バッチ処理・連携仕様の整理 |

---

## 2. 画面設計
**成果物**
- 画面標準
- 画面仕様書
- 画面遷移図

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Figma](https://www.figma.com/) | 画面設計・ワイヤーフレーム・プロトタイプ作成 | 無料プランあり | [詳細](./ツール/デザインツール/Figma.md) |
| [Pencil](https://www.pencil.dev/) | オープンソースのワイヤーフレーム・モックアップ作成 | 無料 | [詳細](./ツール/デザインツール/Pencil.md) |
| [Draw.io](https://www.diagrams.net/) | 画面遷移図・UIフロー作成 | 無料 | [詳細](./ツール/設計_モデリング/Draw.io.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（画面編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 画面一覧、画面遷移図、画面仕様の定義 |
| [WCAG 2.2](https://waic.jp/translations/WCAG22/) | アクセシビリティ観点の設計基準 |

---

## 3. 帳票設計
**成果物**
- 帳票仕様書
- 帳票レイアウト
- 帳票項目定義

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [JasperReports](https://community.jaspersoft.com/) | 帳票テンプレート設計・生成 | 無料 | [詳細](./ツール/帳票_データ処理/JasperReports.md) |
| [LibreOffice](https://www.libreoffice.org/) | 帳票レイアウト検討・テンプレート作成 | 無料 | [詳細](./ツール/帳票_データ処理/LibreOffice.md) |
| [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) | 帳票レイアウト定義、項目一覧作成 | 無料枠あり | [詳細](./ツール/帳票_データ処理/Microsoft_Excel.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（画面編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 表示項目定義、レイアウト要件整理 |
| [ISO 32000（PDF）](https://www.iso.org/standard/75839.html) | PDF帳票の出力要件定義 |

---

## 4. ファイル設計
**成果物**
- ファイル仕様書
- ファイルレイアウト定義
- ファイル項目定義

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Visual Studio Code](https://code.visualstudio.com/) | ファイル仕様のテキスト定義・レビュー | [詳細](./ツール/IDEツール/VS_Code.md) |
| [Draw.io](https://www.diagrams.net/) | ファイルレイアウト図・関連図作成 | [詳細](./ツール/設計_モデリング/Draw.io.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [CSV/TSV形式標準](https://www.ietf.org/rfc/rfc4180.txt) | CSVファイル定義、改行・エスケープ規則 |
| [文字コード標準（UTF-8/Shift_JIS）](https://unicode.org/) | 文字コード定義、文字化け対策 |

---

## 5. データベース論理設計
**成果物**
- 論理ER図
- テーブル定義書
- データ項目定義

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [MySQL Workbench](https://www.mysql.com/products/workbench/) | ER図作成・テーブル設計 | [詳細](./ツール/データベース/MySQL_Workbench.md) |
| [ERDPlus](https://erdplus.com/) | オンラインER図作成・SQL生成 | [詳細](./ツール/データベース/ERDPlus.md) |
| [Draw.io](https://www.diagrams.net/) | 論理データモデルの可視化 | [詳細](./ツール/設計_モデリング/Draw.io.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（データモデル編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 概念・論理モデルの整理、用語統一 |
| [ISO/IEC 11179 概要](https://www.iso.org/standard/35343.html) | データ要素定義、メタデータ管理 |

---

## 6. 外部システムI/F設計
**成果物**
- 外部システムI/F仕様書
- API仕様書
- 連携項目定義

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Swagger / OpenAPI](https://openapi.com/) | API仕様定義（REST） | 無料 | [詳細](./ツール/API_統合/Swagger_OpenAPI.md) |
| [Apidog](./ツール/API_統合/Apidog.md) | API仕様設計、モック生成、テストケース管理 | 無料枠あり | [詳細](./ツール/API_統合/Apidog.md) |
| [ReDoc](https://redocly.com/redoc/) | OpenAPI仕様のドキュメント化 | 無料 | [詳細](./ツール/API_統合/ReDoc.md) |
| [Draw.io](https://www.diagrams.net/) | 外部連携図・データフロー図作成 | 無料 | [詳細](./ツール/設計_モデリング/Draw.io.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | API契約の明確化、インターフェース定義 |
| [REST API Tutorial](https://restfulapi.net/) | REST設計方針、HTTP設計ルール整理 |

---

## 7. バッチ設計
**成果物**
- バッチ設計書
- バッチフロー図
- バッチジョブスケジュール仕様書

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Apache Airflow](https://airflow.apache.org/) | バッチワークフロー設計・ジョブオーケストレーション | [詳細](./ツール/帳票_データ処理/Apache_Airflow.md) |
| [Quartz Scheduler](https://www.quartz-scheduler.org/) | ジョブスケジュール設計（Cronベース） | [詳細](./ツール/バッチ処理_スケジューラ/Quartz_Scheduler.md) |
| [Draw.io](https://www.diagrams.net/) | バッチフロー可視化 | [詳細](./ツール/設計_モデリング/Draw.io.md) |
| [PlantUML](https://plantuml.com/) | バッチ処理フロー・シーケンスのテキストベース設計 | [詳細](./ツール/設計_モデリング/PlantUML.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | バッチ一覧、実行順序、異常系設計 |
| [crontab guru](https://crontab.guru/) | Cron式の検証、実行タイミング定義 |
| [Future Enterprise Arch Guidelines - バッチ処理方式設計ガイドライン](https://future-architect.github.io/arch-guidelines/documents/forBatch/batch_guidelines.html) | バッチ処理アーキテクチャ、ジョブ設計、運用設計の指針 |

---

## 8. セキュリティ設計
**成果物**
- セキュリティ設計書
- 認証・認可仕様書
- 監査ログ仕様書

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Microsoft Threat Modeling Tool](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling) | 脅威分析（STRIDE） | [詳細](./ツール/セキュリティ/Microsoft_Threat_Modeling_Tool.md) |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | 主要脆弱性観点の設計レビュー | [詳細](./ツール/標準_ガイドライン/OWASP_Top_10.md) |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | セキュリティ要件のチェック基準 | [詳細](./ツール/標準_ガイドライン/OWASP_ASVS.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [OWASP API Security Top 10](https://owasp.org/www-project-api-security/) | APIセキュリティ要件の整理 |
| [IPA セキュリティセンター](https://www.ipa.go.jp/security/) | 国内標準に沿ったセキュリティ設計 |

---

## 9. 運用設計
**成果物**
- 監視方針書
- バックアップ構成設計書
- 構成管理方針書

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [SRE Fundamentals - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | 監視方針（SLI/SLO、アラート設計）の基準 |
| [NIST SP 800-34 Rev.1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) | バックアップ/復旧方針、事業継続計画の基準 |

---

## 10. 参考資料
- [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf)
- [ユーザのための要件定義ガイド 第2版](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html)
- [機能要件の合意形成ガイド（画面/データモデル/バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html)

