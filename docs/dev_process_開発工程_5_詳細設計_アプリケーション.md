# 開発工程_4_詳細設計（アプリケーション）

- [1. プログラム設計](#1-プログラム設計)
- [2. API詳細設計](#2-api詳細設計)
- [3. 実装方針策定](#3-実装方針策定)
  - [3.1 Java](#31-java)
  - [3.2 C#](#32-c)
  - [3.3 Python](#33-python)
  - [3.4 TypeScript](#34-typescript)
- [4. データベース物理設計](#4-データベース物理設計)
- [5. 開発環境構築](#5-開発環境構築)
- [6. 参考資料](#6-参考資料)

詳細設計（アプリケーション）のタスクと推奨ツール、有用なドキュメントを記載した。

---

## 1. プログラム設計
**成果物**
- クラス図
- シーケンス図
- ステートマシン図
- コンポーネント図

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [PlantUML](https://plantuml.com/) | テキストベースUML | 無料 |
| [Draw.io](https://www.diagrams.net/) | 汎用UML・フローチャート | 無料 |
| [Mermaid](https://mermaid.js.org/) | Markdown統合ダイアグラム | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [UML Specification](https://www.omg.org/spec/UML/) | クラス図・シーケンス図の表記統一 |
| [PlantUML Guide](https://plantuml.com/guide) | テキストベース設計図の記述ルール統一 |

## 2. API詳細設計
**成果物**
- API仕様書
- エンドポイント定義
- リクエスト/レスポンススキーマ
- エラーハンドリング仕様

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Swagger/OpenAPI](https://openapi.com/) | REST API仕様定義 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | API契約定義、リクエスト/レスポンス標準化 |
| [HTTP Semantics (RFC 9110)](https://www.rfc-editor.org/rfc/rfc9110) | HTTPメソッド、ステータスコード設計基準 |

## 3. 実装方針策定
**成果物**
- 実装ガイド
- コーディング規約
- 命名規則
- ディレクトリ構成

### 3.1 Java

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Checkstyle](https://checkstyle.sourceforge.io/) | Javaコーディング規約チェック | 無料 |
| [SpotBugs](https://spotbugs.github.io/) | 静的解析による不具合検出 | 無料 |
| [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) | 命名規則・コーディング規約の標準化 | 無料 |

### 3.2 C#

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers) | C#コーディング規約チェック | 無料 |
| [Roslyn Analyzers](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview) | .NET静的解析と設計ルール適用 | 無料 |
| [.NET Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions) | 命名規則・設計方針の標準化 | 無料 |

### 3.3 Python

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Ruff](https://docs.astral.sh/ruff/) | Pythonの高速Lint・フォーマット | 無料 |
| [Black](https://black.readthedocs.io/) | コード自動フォーマット | 無料 |
| [PEP 8](https://peps.python.org/pep-0008/) | コーディング規約・命名規則の基準 | 無料 |

### 3.4 TypeScript

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [ESLint](https://eslint.org/) | JS/TSコーディング規約チェック | 無料 |
| [Prettier](https://prettier.io/) | コード自動フォーマット | 無料 |
| [TypeScript ESLint](https://typescript-eslint.io/) | TypeScript向け静的解析ルール適用 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Java Language and VM Specifications](https://docs.oracle.com/javase/specs/) | Java言語仕様の最新版確認、実装方針の基準化 |
| [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) | Java実装規約・命名規則の標準化 |
| [.NET Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions) | C#実装方針・コーディング規約の統一 |
| [PEP 8](https://peps.python.org/pep-0008/) | Python実装規約・命名規則の統一 |
| [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) | TypeScript設計方針・型設計の標準化 |
| [EditorConfig Specification](https://spec.editorconfig.org/) | 言語横断のフォーマット・スタイル運用ルール統一 |

## 4. データベース物理設計
**成果物**
- 物理ER図
- テーブル定義書
- インデックス設計書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [MySQL Workbench](https://www.mysql.com/products/workbench/) | ER図・リバースエンジニアリング | 無料 |
| [tbls](https://github.com/k1LoW/tbls) | 既存DBからER図・ドキュメント自動生成 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [SQL Style Guide](https://www.sqlstyle.guide/) | SQL命名規約・可読性ルール統一 |
| [ISO/IEC 11179 概要](https://www.iso.org/standard/35343.html) | データ項目定義・メタデータ標準化 |

## 5. 開発環境構築
**成果物**
- 構築手順書
- 開発環境一式

| ツール名 | 用途 |
|---------|------|
| [DevContainer](https://code.visualstudio.com/docs/devcontainers/containers) | コンテナベース統一開発環境 |
| [Docker](https://www.docker.com/) | 環境標準化・コンテナ化 |
| [Rancher Desktop](https://rancherdesktop.io/) | ローカルKubernetes/コンテナ実行環境 |
| [VS Code](https://code.visualstudio.com/) | 軽量マルチ言語エディタ |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Dev Container Specification](https://containers.dev/) | 開発環境定義の標準化 |
| [Docker Docs](https://docs.docker.com/) | コンテナ化手順、開発環境運用の標準化 |
| [VS Code Documentation](https://code.visualstudio.com/docs) | 開発環境設定、拡張機能運用の共通化 |

---

## 6. 参考資料
- IPA 共通フレーム2013 / ISO/IEC/IEEE 12207:2017
- [IPA API標準設計ガイド](https://www.ipa.go.jp/digital/data/jod03a000000a82y-att/api_standard_design_guide.pdf)
- [IPA 機能要件の合意形成ガイド（データモデル編）](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/index.html)
