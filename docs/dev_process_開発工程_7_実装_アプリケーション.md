# 開発工程_7_実装（アプリケーション）

- [1. プログラミング](#1-プログラミング)
  - [1.1 モックツール](#11-モックツール)
      - [Java](#java)
      - [C#](#c)
      - [Python](#python)
      - [TypeScript](#typescript)
  - [1.2 モックサーバー](#12-モックサーバー)
- [2. ビルド・パッケージ管理](#2-ビルドパッケージ管理)
- [3. 実装規約・品質管理](#3-実装規約品質管理)
  - [3.1 Java](#31-java)
  - [3.2 C#](#32-c)
  - [3.3 Python](#33-python)
  - [3.4 TypeScript](#34-typescript)
- [4. コードレビュー](#4-コードレビュー)
- [5. テスト実装](#5-テスト実装)
- [6. CI/CD連携](#6-cicd連携)
- [7. 参考資料](#7-参考資料)

実装（アプリケーション）のタスクと推奨ツール、有用なドキュメントを記載した。

---

## 1. プログラミング
**成果物**
- ソースコード
- ビルド成果物

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Visual Studio Code](https://code.visualstudio.com/) | 汎用実装、デバッグ、拡張機能運用 | 無料 | [詳細](./ツール/IDEツール/VS_Code.md) |
| [IntelliJ IDEA Community](https://www.jetbrains.com/idea/download/) | Java中心の実装・リファクタリング | 無料 | [詳細](./ツール/IDEツール/IntelliJ_IDEA.md) |
| [Visual Studio](https://visualstudio.microsoft.com/vs/) | C#/.NET 実装・デバッグ | 有料 | [詳細](./ツール/IDEツール/Visual_Studio.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Clean Code / Clean Architecture](https://blog.cleancoder.com/) | 実装レイヤー分割、依存方向設計 |
| [Refactoring Catalog](https://refactoring.com/catalog/) | リファクタリング方針の標準化 |

### 1.1 モックツール

##### Java

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Mockito](https://site.mockito.org/) | 単体テスト時の依存オブジェクトのモック化 | [詳細](./ツール/API_統合/Mockito.md) |

##### C#

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Moq](https://github.com/devlooped/moq) | .NET単体テストでのモック/スタブ作成 | [詳細](./ツール/単体テスト/Moq.md) |

##### Python

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) | 標準ライブラリでのモック/パッチ適用 | [詳細](./ツール/単体テスト/unittest_mock.md) |

##### TypeScript

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [MSW (Mock Service Worker)](https://mswjs.io/) | ブラウザ/Node.jsでのAPIモック | [詳細](./ツール/APIテスト/MSW.md) |
| [ts-mockito](https://github.com/NagRock/ts-mockito) | TypeScript向けモック作成と振る舞い定義 |  |

### 1.2 モックサーバー

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [WireMock](https://wiremock.org/) | HTTP APIモックサーバによる外部依存のテスト | [詳細](./ツール/APIテスト/WireMock.md) |
| [MockServer](https://www.mock-server.com/) | HTTP/HTTPSモック・スタブ、リクエスト検証 | [詳細](./ツール/APIテスト/MockServer.md) |
| [Mountebank](https://www.mbtest.org/) | 複数プロトコル対応のサービス仮想化 | [詳細](./ツール/API_統合/Mountebank.md) |
| [Prism](https://stoplight.io/open-source/prism) | OpenAPIからのモックサーバ自動生成 | [詳細](./ツール/APIテスト/Prism.md) |
| [Nock](https://github.com/nock/nock) | Node.js向けHTTPリクエストのモック | [詳細](./ツール/APIテスト/Nock.md) |

**有用なドキュメント（モック）**

| 資料名 | 用途 |
|-------|------|
| [Mockito Documentation](https://github.com/mockito/mockito/wiki) | Javaモックの基本パターン、検証手法の統一 |
| [Moq Quickstart](https://github.com/devlooped/moq/wiki/Quickstart) | C#モック作成、セットアップ、検証手順の標準化 |
| [unittest.mock — Python Docs](https://docs.python.org/3/library/unittest.mock.html) | Python標準モックのパッチ・スタブ利用指針 |
| [ts-mockito README](https://github.com/NagRock/ts-mockito) | TypeScriptモック記法、振る舞い定義の統一 |
| [WireMock Documentation](https://wiremock.org/docs/) | モックサーバ構築、スタブ定義、検証手順 |
| [MockServer Documentation](https://www.mock-server.com/#documentation) | モックサーバ設定、期待値検証、プロキシ活用 |


## 2. ビルド・パッケージ管理
**成果物**
- ビルド設定ファイル
- 依存関係定義
- ビルド手順書

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Maven](https://maven.apache.org/) | Javaビルド・依存管理 | [詳細](./ツール/ビルド_タスク管理/Maven.md) |
| [NuGet](https://www.nuget.org/) | .NETパッケージ管理 | [詳細](./ツール/パッケージ管理ツール/NuGet.md) |
| [Poetry](https://python-poetry.org/) | Python依存管理・仮想環境管理 | [詳細](./ツール/パッケージ管理ツール/Poetry.md) |
| [pnpm](https://pnpm.io/) | TypeScript依存管理・モノレポ管理 |  |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Maven Guides](https://maven.apache.org/guides/) | Mavenプロジェクト構成・依存管理標準化 |
| [NuGet Documentation](https://learn.microsoft.com/nuget/) | .NET依存関係管理・公開手順 |
| [Poetry Docs](https://python-poetry.org/docs/) | Pythonプロジェクト運用標準化 |
| [pnpm Docs](https://pnpm.io/) | JavaScript/TypeScript依存管理最適化 |

## 3. 実装規約・品質管理
**成果物**
- コーディング規約
- 命名規則
- 静的解析設定
- フォーマッタ設定

### 3.1 Java

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Checkstyle](https://checkstyle.sourceforge.io/) | Javaコーディング規約チェック | [詳細](./ツール/Formatter_Linter/Checkstyle.md) |
| [SpotBugs](https://spotbugs.github.io/) | 静的解析による不具合検出 | [詳細](./ツール/静的解析_型チェック/SpotBugs.md) |
| [Google Java Format](https://github.com/google/google-java-format) | Javaコード自動整形 | [詳細](./ツール/Formatter_Linter/Google_Java_Format.md) |

### 3.2 C#

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers) | C#コーディング規約チェック |  |
| [Roslyn Analyzers](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview) | .NET静的解析ルール適用 | [詳細](./ツール/静的解析_型チェック/Roslyn_Analyzers.md) |
| [EditorConfig](https://editorconfig.org/) | C#コードスタイル統一 | [詳細](./ツール/Formatter_Linter/EditorConfig.md) |

### 3.3 Python

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Ruff](https://docs.astral.sh/ruff/) | Python静的解析・整形 | [詳細](./ツール/Formatter_Linter/Ruff.md) |
| [Black](https://black.readthedocs.io/) | Pythonコード自動整形 | [詳細](./ツール/Formatter_Linter/Black.md) |
| [mypy](https://mypy-lang.org/) | 型チェック | [詳細](./ツール/静的解析_型チェック/mypy.md) |

### 3.4 TypeScript

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [ESLint](https://eslint.org/) | TypeScript静的解析 | [詳細](./ツール/Formatter_Linter/ESLint.md) |
| [TypeScript ESLint](https://typescript-eslint.io/) | TypeScript専用ルール適用 |  |
| [Prettier](https://prettier.io/) | コード自動整形 | [詳細](./ツール/Formatter_Linter/Prettier.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Java Language and VM Specifications](https://docs.oracle.com/javase/specs/) | Java実装仕様の確認 |
| [.NET Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions) | C#命名規約・実装規約統一 |
| [PEP 8](https://peps.python.org/pep-0008/) | Pythonコーディング規約統一 |
| [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) | TypeScript実装指針・型設計 |

## 4. コードレビュー
**成果物**
- レビュー観点チェックリスト
- レビュー記録
- 修正履歴

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [GitHub Pull Requests](https://github.com/features/code-review) | レビュー運用・差分確認 | 無料枠あり |  |
| [GitLab Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/) | レビュー運用・承認フロー | 無料枠あり |  |
| [Danger](https://danger.systems/) | PR自動レビューコメント | 無料 | [詳細](./ツール/バージョン管理_CI_CD/Danger.md) |
| [Reviewdog](https://github.com/reviewdog/reviewdog) | Lint/静的解析結果をPRコメントとして自動通知 | 無料 | [詳細](./ツール/バージョン管理_CI_CD/Reviewdog.md) |
| [CodeRabbit](https://www.coderabbit.ai/) | AIによるPRレビュー、改善提案コメントの自動生成 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/CodeRabbit.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Code Review Developer Guide](https://google.github.io/eng-practices/review/) | レビュー観点、コメント品質基準 |
| [Conventional Commits](https://www.conventionalcommits.org/) | 変更履歴・レビュー粒度の標準化 |

## 5. テスト実装
**成果物**
- 単体テストコード
- テスト実行レポート
- カバレッジレポート

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [JUnit 5](https://junit.org/junit5/) | Java単体テスト | [詳細](./ツール/単体テスト/JUnit.md) |
| [xUnit](https://xunit.net/) | C#単体テスト | [詳細](./ツール/単体テスト/xUnit_net.md) |
| [pytest](https://pytest.org/) | Python単体テスト | [詳細](./ツール/単体テスト/pytest.md) |
| [Vitest](https://vitest.dev/) | TypeScript単体テスト | [詳細](./ツール/単体テスト/Vitest.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [JUnit User Guide](https://junit.org/junit5/docs/current/user-guide/) | Javaテスト実装標準化 |
| [xUnit Documentation](https://xunit.net/docs/getting-started/v2/getting-started) | .NETテスト基準統一 |
| [pytest Documentation](https://docs.pytest.org/) | Pythonテスト設計の標準化 |
| [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/) | テスト観点の統一 |

## 6. CI/CD連携
**成果物**
- CI定義ファイル
- 自動テストジョブ
- 品質ゲート設定

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [GitHub Actions](https://github.com/features/actions) | CIパイプライン実行 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitHub_Actions.md) |
| [GitLab CI/CD](https://docs.gitlab.com/ee/ci/) | CI/CDパイプライン実行 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitLab_CI_CD.md) |
| [SonarQube Community](https://www.sonarsource.com/products/sonarqube/) | 静的解析・品質ゲート | 無料 | [詳細](./ツール/コード品質ツール/SonarQube.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [GitHub Actions Docs](https://docs.github.com/actions) | CI設計、ワークフロー標準化 |
| [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/) | パイプライン設計・運用標準化 |
| [SonarQube Docs](https://docs.sonarsource.com/sonarqube/latest/) | 品質ゲート運用・静的解析基準 |

---

## 7. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- [IPA 組込みソフトウェア向け 設計ガイド（事例編）ESDR](https://www.ipa.go.jp/)
- [Google Engineering Practices](https://google.github.io/eng-practices/)


