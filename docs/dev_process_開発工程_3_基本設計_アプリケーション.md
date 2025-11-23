# 開発工程_3_基本設計（アプリケーション）

## 1. 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**基本設計プロセス（アプリケーション基本設計）**における開発タスクと推奨ツールをまとめたものです。

### 1.1. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

### 1.2. 共通

#### 1.2.1. 推奨ツール（生産性が高いもの Top 10）

| # | ツール名 | 概要 | 用途 | メリット | デメリット |
|---|---------|------|------|---------|-----------|
| 1 | [**Next Design**](https://www.nextdesign.app/) | 日本製モデリングツール。トレーサビリティと設計自動反映に強み | システム設計、要件トレーサビリティ、モデリング、設計書生成 | ✅ 日本語完全対応<br>✅ トレーサビリティ管理<br>✅ 設計変更自動反映<br>✅ カスタマイズ性高い<br>✅ 日本のシステム開発に最適化 | ❌ 知名度低い（海外）<br>❌ 高額<br>❌ 学習曲線やや急<br>❌ コミュニティ小さい |
| 2 | [**astah***](https://astah.net/) | 日本製UMLツール。UML、フローチャート、ER図、マインドマップ対応 | UML図作成、ER図、フローチャート、システム設計 | ✅ 日本語ネイティブ<br>✅ 買い切り可能<br>✅ 軽量で高速<br>✅ 多様な図に対応<br>✅ 教育機関無料 | ❌ Enterprise Architectより機能少<br>❌ 海外シェア低い<br>❌ クラウド機能弱い<br>❌ コラボ機能限定的 |
| 3 | [**Enterprise Architect**](https://sparxsystems.com/) | 多機能UMLモデリングツール。エンタープライズアーキテクチャ設計 | エンタープライズアーキテクチャ設計、UML、コード生成、要件管理 | ✅ 非常に多機能<br>✅ 要件からコード生成まで<br>✅ 多様なモデリング言語対応<br>✅ チーム開発対応<br>✅ 買い切り（$159〜） | ❌ 学習曲線非常に急<br>❌ UI複雑<br>❌ 機能過多で迷う<br>❌ 動作やや重い |
| 4 | [**draw.io (diagrams.net)**](https://www.diagrams.net/) | 無料のオンライン図作成ツール。システム構成図、ネットワーク図など | システム構成図、ネットワーク図、アーキテクチャ図、フローチャート | ✅ 完全無料<br>✅ ブラウザで動作<br>✅ テンプレート豊富<br>✅ Google Drive/GitHub統合<br>✅ インストール不要 | ❌ UML機能は基本的<br>❌ コラボ機能弱い<br>❌ モデリング自動化なし<br>❌ 大規模図は管理困難 |
| 5 | [**PlantUML**](https://plantuml.com/) | テキストベースUMLツール。コードとして管理、バージョン管理容易 | UML図（クラス図、シーケンス図等）、テキストベース設計書、Git管理 | ✅ テキストで記述<br>✅ Git管理容易<br>✅ CI/CD統合可能<br>✅ 無料オープンソース<br>✅ 多様な図対応 | ❌ テキスト記法学習必要<br>❌ GUI編集不可<br>❌ 複雑な図は困難<br>❌ レイアウト自動で調整困難 |
| 6 | [**StarUML**](https://staruml.io/) | モダンUIのUMLツール。拡張機能とテーマカスタマイズ | UMLモデリング、コード生成・逆生成、設計書作成 | ✅ モダンで美しいUI<br>✅ 軽量で高速<br>✅ 拡張機能対応<br>✅ コード生成・逆生成<br>✅ 安価（$89買い切り） | ❌ Enterprise Architectより機能少<br>❌ チーム開発機能弱い<br>❌ 日本語ドキュメント少ない<br>❌ サポート限定的 |
| 7 | [**Visual Paradigm**](https://www.visual-paradigm.com/) | UML、BPMN、ER図など多様なモデリング。プロジェクト管理統合 | UML/BPMN/ER図、プロジェクト管理、コード生成、シミュレーション | ✅ 多様なダイアグラム<br>✅ BPMNシミュレーション<br>✅ プロジェクト管理統合<br>✅ コード生成豊富<br>✅ チーム開発対応 | ❌ 高額（$99/月〜）<br>❌ 機能過多で複雑<br>❌ 動作やや重い<br>❌ 学習コスト高 |
| 8 | [**Cacoo**](https://cacoo.com/) | 日本製オンライン図作成ツール。リアルタイム協業に強み | システム構成図、ワイヤーフレーム、フローチャート、共同編集 | ✅ リアルタイム共同編集<br>✅ 日本語完全対応<br>✅ テンプレート豊富<br>✅ プレゼンモード<br>✅ クラウド管理 | ❌ 有料（$6/月〜）<br>❌ UML機能限定的<br>❌ オフライン不可<br>❌ 高度なモデリング不向き |
| 9 | [**Structurizr**](https://structurizr.com/) | C4モデル専用アーキテクチャ可視化ツール。コードとして管理 | C4モデルアーキテクチャ設計、コードベース設計書、バージョン管理 | ✅ C4モデル特化<br>✅ コードで記述（DSL）<br>✅ バージョン管理容易<br>✅ 自動レイアウト<br>✅ マルチビュー対応 | ❌ C4モデル以外不向き<br>❌ DSL学習必要<br>❌ 有料（$7.50/月〜）<br>❌ GUI編集不可 |
| 10 | [**ArchiMate (Archi)**](https://www.archimatetool.com/) | エンタープライズアーキテクチャモデリング。ArchiMate標準準拠 | エンタープライズアーキテクチャ、業務・アプリ・技術アーキテクチャ設計 | ✅ 完全無料オープンソース<br>✅ ArchiMate標準準拠<br>✅ EA設計に最適<br>✅ プラグイン拡張可能<br>✅ クロスプラットフォーム | ❌ 学習曲線急<br>❌ ArchiMate知識必須<br>❌ UI古い<br>❌ 小規模開発には過剰 |

<!-- 
#### 1.2.3. その他利用可能なツール

- Creately
- Gliffy
- C4-PlantUML
- Mermaid
- yUML
- Modelio
- GenMyModel
- LucidChart
- CloudSkew
- Dia -->

## 2. 画面設計

**対応項目**
- 画面設計

**成果物**
- 画面標準
- 画面仕様書
  - 画面レイアウト
  - 画面項目定義、テーブル項目マッピング定義
  - 画面入力チェック仕様書
  - 画面処理仕様書

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**Figma**](https://www.figma.com/) | ワイヤーフレーム、UI/UXデザイン、プロトタイプ | ✅ リアルタイム協業<br>✅ インタラクティブプロトタイプ<br>✅ デザインシステム管理<br>✅ 開発者への共有容易 |
| [**Adobe XD**](https://www.adobe.com/jp/products/xd/) | ワイヤーフレーム、UI/UXデザイン、プロトタイプ | ✅ UX/UIに特化<br>✅ Adobe体系との統合<br>✅ 多彩なプラグイン<br>✅ クラウドシェア機能 |
| [**Mockito / MockFlow**](https://www.mockflow.com/) | 低・中忠実度ワイヤーフレーム | ✅ 軽量で導入簡単<br>✅ テンプレート豊富<br>✅ コスト低い<br>✅ 協業機能 |
| [**Sketch**](https://www.sketch.com/) | UI/UXデザイン、ワイヤーフレーム | ✅ デザイナー向けUIツール<br>✅ 豊富なプラグイン<br>✅ Mac対応<br>✅ デザインシステム管理 |
| [**draw.io**](https://www.diagrams.net/) | 低コストワイヤーフレーム、画面フロー図 | ✅ 無料<br>✅ テンプレート豊富<br>✅ ブラウザで動作<br>✅ Git統合可能 |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **UI/UX設計ガイドライン** | 使いやすい画面設計の基本原則 | [Nielsen Norman ガイドライン](https://www.nngroup.com/articles/usability-101-introduction-to-usability/) |
| **アクセシビリティガイドライン（WCAG 2.1）** | 誰もが使える画面設計の基準 | [W3C WCAG](https://www.w3.org/WAI/WCAG21/quickref/) |
| **IPA ユーザーインターフェース設計ガイド** | 日本の基準に準拠した画面設計手法 | [IPA公式サイト](https://www.ipa.go.jp/) |

---

## 3. 帳票設計

**対応項目**
- 帳票設計

**成果物**
- 帳票仕様書
  - 帳票レイアウト
  - 帳票項目定義、テーブル項目マッピング定義

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**JasperReports / JasperStudio**](https://community.jaspersoft.com/project/jasperreports-library) | 帳票設計、帳票生成エンジン | ✅ Java標準のオープンソース<br>✅ 複雑な帳票設計に対応<br>✅ 多様なデータソース対応<br>✅ PDF/Excel/CSV等多形式出力 |
| [**Crystal Reports**](https://www.sap.com/products/technology/crystal-reports.html) | 企業向け帳票ツール | ✅ 高度な帳票設計機能<br>✅ 大規模バッチ対応<br>✅ 多形式出力<br>✅ エンタープライズ実績 |
| [**Apache POI**](https://poi.apache.org/) | Excelベースの帳票生成 | ✅ Javaで帳票を完全制御<br>✅ 複雑なレイアウト対応<br>✅ オープンソース無料<br>✅ プログラマブル |
| [**BIRT (Business Intelligence and Reporting Tools)**](https://projects.eclipse.org/projects/technology.birt) | エンタープライズレポーティング | ✅ Eclipse統合<br>✅ 複雑な帳票対応<br>✅ オープンソース<br>✅ デザイナーツール付属 |
| [**LibreOffice / OpenOffice**](https://www.libreoffice.org/) | 帳票テンプレート作成、検討用 | ✅ 無料オープンソース<br>✅ テンプレート設計<br>✅ マクロ対応<br>✅ クロスプラットフォーム |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **帳票設計の基本** | 使いやすい帳票設計のガイドラインと事例 | [IPA情報発信](https://www.ipa.go.jp/) |
| **JasperReports ドキュメント** | JasperReportsの詳細な使用方法 | [JasperReports ドキュメント](https://community.jaspersoft.com/documentation) |

---

## 4. ファイル設計

**対応項目**
- ファイル設計

**成果物**
- ファイル仕様書（外部入出力ファイル）
  - ファイルレイアウト定義
  - ファイル項目定義、テーブル項目マッピング定義

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**ERDPlus / Lucidchart**](https://www.lucidchart.com/) | ファイル構造図、ER図作成 | ✅ ファイルレイアウト可視化<br>✅ テンプレート豊富<br>✅ 協業機能<br>✅ 多形式エクスポート |
| [**Notepad++ / VSCode**](https://code.visualstudio.com/) | ファイルフォーマット定義、テスト用ダミー生成 | ✅ テキストベース管理<br>✅ 正規表現対応<br>✅ プラグイン豊富<br>✅ Git統合 |
| [**Python/Pandas**](https://pandas.pydata.org/) | ファイル解析、変換スクリプト | ✅ CSV/Excel/JSON解析<br>✅ データ変換自動化<br>✅ テスト用ダミーデータ生成<br>✅ 統計分析 |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **ファイルフォーマット仕様書テンプレート** | ファイル設計書の作成テンプレート | [IPA事例](https://www.ipa.go.jp/) |
| **CSV/JSON/XMLスキーマガイド** | 各ファイルフォーマットの設計ガイド | [W3C Schema](https://www.w3.org/XML/Schema/) |

---

## 5. データベース論理設計

**対応項目**
- データベース論理設計

**成果物**
- 論理ER図
- テーブル定義書

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**MySQL Workbench**](https://www.mysql.com/jp/products/workbench/) | ER図設計、SQL生成、データベース管理 | ✅ 無料で高機能<br>✅ MySQL標準ツール<br>✅ SQL自動生成<br>✅ リバースエンジニアリング対応 |
| [**ERDPlus**](https://erdplus.com/) | 無料のオンラインER図作成 | ✅ 完全無料<br>✅ ブラウザで動作<br>✅ SQL生成機能<br>✅ 複数データベース対応 |
| [**pgAdmin (PostgreSQL)**](https://www.pgadmin.org/) | PostgreSQL向けDB設計ツール | ✅ PostgreSQL標準ツール<br>✅ ER図エクスポート<br>✅ クエリビルダー<br>✅ リバースエンジニアリング |
| [**Power Designer**](https://www.powerdesigner.de/) | エンタープライズレベルのER図設計 | ✅ 複雑なER図対応<br>✅ 多様なDBMS対応<br>✅ 物理・論理モデル変換<br>✅ ドキュメント自動生成 |
| [**Lucidchart**](https://www.lucidchart.com/) | ER図設計、アーキテクチャ図 | ✅ リアルタイム協業<br>✅ テンプレート豊富<br>✅ 多形式エクスポート<br>✅ 初心者向け |
| [**draw.io**](https://www.diagrams.net/) | 低コストER図作成 | ✅ 完全無料<br>✅ ブラウザで動作<br>✅ Git統合<br>✅ テンプレート豊富 |
| [**Dataedo**](https://dataedo.com/) | データベース自動ドキュメント化 | ✅ リバースエンジニアリング<br>✅ ドキュメント自動生成<br>✅ 複数DBサポート<br>✅ チーム共有機能 |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **データベース設計ガイドライン** | 正規化と最適化の基本 | [IPA情報発信](https://www.ipa.go.jp/) |
| **ER図の書き方** | 実践的なER図設計のベストプラクティス | [Lucidchart ガイド](https://www.lucidchart.com/pages/ja/er-diagram) |
| **データ正規化について** | 第1正規形から第3正規形の解説 | [DB標準設計](https://www.ipa.go.jp/) |

---

## 6. 外部システムI/F設計

**対応項目**
- 外部システムI/F設計

**成果物**
- 外部システムI/F仕様書

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**Postman**](https://www.postman.com/) | API設計・テスト・ドキュメント生成 | ✅ API仕様書作成<br>✅ テスト実行・自動化<br>✅ チーム共有機能<br>✅ 無料プランあり |
| [**Swagger / OpenAPI**](https://swagger.io/) | API仕様標準、ドキュメント自動生成 | ✅ 業界標準フォーマット<br>✅ 仕様からコード生成<br>✅ インタラクティブドキュメント<br>✅ オープンソース |
| [**Insomnia**](https://insomnia.rest/) | API設計・テスト（Postmanの代替） | ✅ オープンソース無料<br>✅ GraphQL対応<br>✅ プラグイン豊富<br>✅ ローカル管理 |
| [**ReDoc**](https://redoc.ly/) | OpenAPIドキュメント自動生成 | ✅ 美しいドキュメント生成<br>✅ OpenAPI連携<br>✅ レスポンシブ対応<br>✅ 無料 |
| [**API Blueprint / APIB**](https://apiblueprint.org/) | マークダウンベースのAPI仕様 | ✅ テキストベース管理<br>✅ Git管理容易<br>✅ ドキュメント自動生成<br>✅ 軽量 |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **API標準設計ガイド・基礎編** | REST API設計の標準的な設計手法を解説。外部システム連携の設計に有用 | [IPA公式サイト](https://www.ipa.go.jp/digital/data/jod03a000000a82y-att/api_standard_design_guide.pdf) |
| **OpenAPI 3.0 仕様書** | REST API仕様の標準フォーマット | [OpenAPI 公式](https://spec.openapis.org/oas/v3.0.3) |
| **RESTful API設計ベストプラクティス** | マイクロサービス・API連携の設計ガイド | [RESTful API チュートリアル](https://www.restapitutorial.com/) |
| **GraphQL設計ガイド** | GraphQL APIの設計とベストプラクティス | [GraphQL 公式](https://graphql.org/learn/best-practices/) |

---

## 7. バッチ設計

**対応項目**
- バッチ設計

**成果物**
- バッチ設計書
  - バッチフロー図
  - バッチジョブスケジュール仕様書
  - バッチ入出力ファイル定義
  - エラーハンドリング仕様書

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**Apache Airflow**](https://airflow.apache.org/) | バッチスケジュール管理、ワークフロー定義 | ✅ オープンソース無料<br>✅ DAG（有向非環グラフ）で定義<br>✅ スケーラビリティ高い<br>✅ 監視・ロギング充実 |
| [**Spring Batch**](https://spring.io/projects/spring-batch) | Java向けバッチフレームワーク | ✅ Java標準<br>✅ トランザクション管理<br>✅ リスタート機能<br>✅ 大量データ処理対応 |
| [**Quartz Scheduler**](http://www.quartz-scheduler.org/) | Javaジョブスケジューリング | ✅ Java標準<br>✅ Cron式対応<br>✅ クラスタリング対応<br>✅ 軽量で安定 |
| [**Kubernetes / CronJob**](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) | コンテナ環境のバッチスケジューリング | ✅ クラウドネイティブ<br>✅ スケーラビリティ<br>✅ 高可用性<br>✅ 監視統合 |
| [**draw.io / PlantUML**](https://www.diagrams.net/) | バッチフロー図作成 | ✅ 無料<br>✅ テンプレート豊富<br>✅ バージョン管理容易<br>✅ ブラウザで動作 |
| [**GitLab / GitHub Actions**](https://github.com/) | CI/CDベースのバッチスケジューリング | ✅ Git統合<br>✅ バージョン管理<br>✅ ログ保存<br>✅ コスト効率的 |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **バッチ処理設計ガイドライン** | バッチ系システムの設計・実装ベストプラクティス | [IPA情報発信](https://www.ipa.go.jp/) |
| **Apache Airflow チュートリアル** | バッチワークフロー定義の実践ガイド | [Airflow ドキュメント](https://airflow.apache.org/docs/) |
| **Spring Batch リファレンス** | Java向けバッチフレームワークの詳細 | [Spring Batch ドキュメント](https://docs.spring.io/spring-batch/docs/current/reference/html/index.html) |
| **バッチエラーハンドリング設計** | 再実行・リトライ戦略の設計 | [信頼性設計ガイド](https://www.ipa.go.jp/) |

---

## 8. セキュリティ設計

**対応項目**
- セキュリティ要件の基本設計への反映

**成果物**
- セキュリティ設計書
  - 認証・認可仕様書
  - 暗号化・通信セキュリティ仕様書
  - 監査ログ仕様書

**有用なツール**
| ツール名 | 用途 | 理由 |
|---------|------|------|
| [**Threat Modeling (Microsoft Threat Modeling Tool)**](https://microsoft.com/en-us/securityriskmanagement/threatmodeling) | セキュリティ脅威分析 | ✅ 無料<br>✅ 脅威分類体系搭載<br>✅ 図式化<br>✅ 対策提案自動生成 |
| [**OWASP Top 10ガイド**](https://owasp.org/www-project-top-ten/) | Webアプリケーション脅威対策 | ✅ セキュリティベストプラクティス<br>✅ 業界標準<br>✅ 無料<br>✅ 定期更新 |
| [**JWT.io**](https://jwt.io/) | JWT（JSON Web Token）仕様確認・検証 | ✅ トークン設計支援<br>✅ デバッガ機能<br>✅ ライブラリ情報<br>✅ 無料 |

**有用なドキュメント**
| 資料名 | 概要 | リンク |
|-------|------|--------|
| **OWASP API Security Top 10** | API セキュリティ脅威対策 | [OWASP](https://owasp.org/www-project-api-security/) |
| **IPA セキュリティガイドライン** | 日本の標準セキュリティ設計ガイド | [IPA 公式](https://www.ipa.go.jp/security/) |
| **マイナンバー・個人情報保護対応ガイド** | 個人情報保護法対応設計 | [IPA マイナンバー対応](https://www.ipa.go.jp/about/press/20150209.html) |

---

## 9. IPA公式資料・ガイド

---

**関連ドキュメント**:
- [3. 基本設計（インフラ）](./dev_process_開発工程_3_基本設計_インフラ.md)
- [4. 詳細設計](./dev_process_開発工程_4_詳細設計.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.1
