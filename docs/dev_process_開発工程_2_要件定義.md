# 開発工程_2_要件定義

## 1. 概要

要件定義プロセスのタスクと推奨ツール、有用なドキュメントを記載した。

### 1.1. 参考資料
- [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf)（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）

---

### 1.2. 共通

**対応項目**
- 利害関係者の識別
- 要求事項の識別
- 要求事項の評価
- システム要件の定義
- システム要件の評価
- システム要件の合意

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [ユーザのための要件定義ガイド 第2版](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | システム要件定義、業務要件定義、要件定義プロセス全般、要件定義書作成 |
| [機能要件の合意形成ガイド（画面編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 画面設計、画面仕様書作成、画面レイアウト設計、画面遷移図作成 |
| [機能要件の合意形成ガイド（データモデル編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | データベース論理設計、ER図作成、概念モデリング、データディクショナリ作成 |
| [機能要件の合意形成ガイド（バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | バッチ処理設計、バッチ仕様書作成、外部インターフェース設計 |


---

## 2. 業務分析
**成果物**
- ビジネスプロセス関連図
- 業務機能構成表
- システム化業務フロー

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | フローチャート・BPMN図 | 無料 |
| [Bizagi Modeler](https://www.bizagi.com/) | BPMN2.0準拠のプロセス図作成 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [ユーザのための要件定義ガイド 第2版（業務分析）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | 業務分析、業務フロー整理、改善ポイント抽出 |
| **[BPMN 2.0](https://www.omg.org/spec/BPMN/2.0/PDF)** [OMG公式サイト](https://www.omg.org/spec/BPMN/2.0) | BPMN図作成、記法統一、レビュー効率化 |

## 3. ユースケース分析
**成果物**
- ユースケース図・一覧・記述
- ビジネスルール一覧・定義書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [PlantUML](https://plantuml.com/) | テキストベースUML（Git管理可） | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [ユーザのための要件定義ガイド 第2版（ユースケース）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html) | ユースケース記述、業務ルール整理、受入観点定義 |
| [UML 仕様（Use Case）](https://www.omg.org/spec/UML/) | アクター/ユースケースの表記統一 |

---

## 4. 画面要件定義
**成果物**
- 画面一覧
- 画面遷移図
- 画面レイアウト

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Figma](https://www.figma.com/) | 画面設計・ワイヤーフレーム・プロトタイプ作成 | 無料プランあり |
| [Pencil](https://www.pencil.dev/) | オープンソースのワイヤーフレーム・モックアップ作成 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（画面編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 画面一覧、画面遷移図、画面レイアウト定義 |
| [WCAG 2.2](https://waic.jp/translations/WCAG22/) | UI要件、アクセシビリティ観点定義 |

---

## 5. 帳票要件定義
**成果物**
- 帳票一覧
- 帳票レイアウト

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [JasperReports](https://community.jaspersoft.com/) | OSS帳票エンジン（Java） | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（画面編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 帳票項目定義、レイアウト要件整理 |
| [ISO 32000（PDF）](https://www.iso.org/standard/75839.html) | PDF帳票の出力要件定義 |

---

## 6. ファイル要件定義（機能要件定義）

**対応項目**
- ファイル要件定義

**成果物**
- ファイル一覧
- ファイルレイアウト

| ツール名 | 用途 |
|---------|------|
| [**Microsoft Excel**](https://www.microsoft.com/microsoft-365/excel) | ファイルレイアウト定義、データ項目一覧、形式定義 |
| [**CSV Spec Validator**](https://github.com/) | CSVファイル仕様定義 | 

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | ファイルレイアウト定義、外部インターフェース定義 |
| [CSV/TSV形式標準](https://www.ietf.org/rfc/rfc4180.txt) | CSVファイル定義、文字コード定義、エスケープ処理 |
| [文字コード標準（UTF-8/Shift_JIS）](https://unicode.org/) | 文字コード定義、エンコーディング、文字化け対策 |

---

## 7. バッチ処理要件定義
**成果物**
- バッチ一覧
- バッチ処理フロー

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | バッチ処理フロー・ジョブ依存関係の可視化 | 無料 |
| [PlantUML](https://plantuml.com/) | テキストベースのバッチ処理フロー定義 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | バッチ一覧作成、ジョブ設計、エラーハンドリング定義 |
| [crontab guru](https://crontab.guru/) | バッチスケジュール定義、実行タイミング検証 |

---

## 8. システム方針検討
**成果物**
- システム構成図
- ソフトウェア構成図

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Draw.io](https://www.diagrams.net/) | システム構成図・ネットワーク構成図の作成 | 無料 |
| [PlantUML](https://plantuml.com/) | C4/UMLによるソフトウェア構成の可視化 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) | システム方針検討、非機能観点レビュー、技術選定 |
| [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/) | システム構成方針、冗長化設計、運用設計 |
| [C4 Model](https://c4model.com/) | ソフトウェア構成図、責務分割、境界整理 |

---

## 9. 概念モデリング
**成果物**
- 概念モデル
- 用語集

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [ERDPlus](https://erdplus.com/) | オンラインER図・SQL生成 | 無料 |
| [MySQL Workbench](https://www.mysql.com/products/workbench/) | ER図・DB設計 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [機能要件の合意形成ガイド（データモデル編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 概念モデル、用語統一、関連整理 |
| [ISO/IEC 11179 概要](https://www.iso.org/standard/35343.html) | 用語集整備、属性定義、命名規約統一 |

---

## 10. 外部システム連携要件定義
**成果物**
- 外部システム関連図
- 外部インターフェース一覧

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Swagger/OpenAPI](https://swagger.io/) | REST API仕様記述標準 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [OpenAPI Specification](https://www.openapis.org/) | 外部IF定義、API契約の明確化 |
| [機能要件の合意形成ガイド（バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html) | 外部システム関連図、連携方式定義 |

---

## 11. 非機能要件定義
**成果物**
- 非機能要件定義書

| ツール名 | 用途 |
|---------|------|
| [IPA 非機能要求グレード（Excel版）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | 6大分類118項目の非機能要件定義テンプレート |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [非機能要求グレード](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/hikinou/ent03-b.html) | 可用性、性能、運用、セキュリティ要件定義 |
| [ISO/IEC 25010](https://www.iso.org/standard/35733.html) | 品質特性の整理、非機能分類 |

---

## 12. 参考資料
- [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf)
- [ユーザのための要件定義ガイド 第2版](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html)
- [機能要件の合意形成ガイド（画面/データモデル/バッチ編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html)
