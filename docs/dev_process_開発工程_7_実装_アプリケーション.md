# 開発工程_5_実装（アプリケーション）

## 1. 概要

本ドキュメントは、IPA（独立行政法人 情報処理推進機構）の「共通フレーム2013」に基づく**実装プロセス（アプリケーション実装）**における開発タスクと推奨ツールをまとめたものです。

言語ごと（Java、C#、Python、TypeScript）に最適化されたツールと開発環境を記載しています。

### 1.1. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC 12207:2008 / JIS X 0160:2012

---

### 1.2. 共通

**対応項目**
- プログラミング
- コードレビュー
- CI/CD構築

---

## 2. プログラミング

**対応項目**
- プログラミング

### 2.1. 言語別推奨ツール

#### 2.1.1. Java 開発ツール

| カテゴリ | ツール名 | 概要 | メリット | デメリット |
|---------|---------|------|---------|-----------|
| **IDE** | [**IntelliJ IDEA**](https://www.jetbrains.com/idea/) | JetBrains製Java/Kotlin IDE。強力なリファクタリング | ✅ Java開発最適化<br>✅ リファクタリング強力<br>✅ Spring統合<br>✅ Maven/Gradle統合 | ❌ 有料（Community版制限）<br>❌ メモリ使用量大<br>❌ 起動遅い |
| **IDE** | [**Eclipse**](https://www.eclipse.org/) | オープンソースJava IDE。プラグイン豊富 | ✅ 完全無料<br>✅ プラグイン豊富<br>✅ 長い実績<br>✅ エンタープライズ採用多 | ❌ 動作重い<br>❌ UI古い<br>❌ IntelliJ比で機能劣る |
| **ビルドツール** | [**Maven**](https://maven.apache.org/) | Apache製ビルドツール。POM.xml設定 | ✅ 業界標準<br>✅ 依存関係管理<br>✅ プラグイン豊富<br>✅ CI/CD統合容易 | ❌ XML冗長<br>❌ ビルド遅い<br>❌ 柔軟性低い |
| **ビルドツール** | [**Gradle**](https://gradle.org/) | Groovy/Kotlin DSLビルドツール。高速・柔軟 | ✅ Maven比で高速<br>✅ 柔軟な設定<br>✅ Kotlin DSL<br>✅ Android公式 | ❌ 学習曲線急<br>❌ ビルド時間予測困難<br>❌ Maven比で情報少ない |
| **フレームワーク** | [**Spring Boot**](https://spring.io/projects/spring-boot) | エンタープライズJavaフレームワーク | ✅ エンタープライズ標準<br>✅ 自動設定<br>✅ マイクロサービス対応<br>✅ 豊富なスターター | ❌ 学習コスト高<br>❌ 重い<br>❌ 設定複雑化しやすい |
| **テスト** | [**JUnit 5**](https://junit.org/junit5/) | Java単体テストフレームワーク | ✅ 業界標準<br>✅ アノテーション豊富<br>✅ IDE統合<br>✅ パラメータ化テスト | ❌ モックは別ライブラリ必要<br>❌ 複雑なテスト設定困難 |
| **モック** | [**Mockito**](https://site.mockito.org/) | Javaモックフレームワーク | ✅ 使いやすい<br>✅ JUnit統合<br>✅ スパイ機能<br>✅ 無料 | ❌ 静的メソッドモック困難<br>❌ final classモック制限 |
| **コード品質** | [**SonarQube**](https://www.sonarqube.org/) | コード品質・セキュリティ分析 | ✅ 包括的分析<br>✅ CI/CD統合<br>✅ セキュリティ脆弱性検出<br>✅ 技術的負債可視化 | ❌ セットアップ複雑<br>❌ リソース使用量大<br>❌ 一部機能有料 |
| **リンター** | [**Checkstyle**](https://checkstyle.sourceforge.io/) | Javaコーディング規約チェック | ✅ カスタマイズ可能<br>✅ Maven/Gradle統合<br>✅ Google/Sun規約サポート<br>✅ 無料 | ❌ 設定ファイル複雑<br>❌ 誤検知あり |
| **フォーマッター** | [**Google Java Format**](https://github.com/google/google-java-format) | Google製Javaフォーマッター | ✅ 一貫したスタイル<br>✅ IDE統合<br>✅ 無料<br>✅ 議論不要 | ❌ カスタマイズ不可<br>❌ Google Styleのみ |

---

#### 2.1.2. C# 開発ツール

| カテゴリ | ツール名 | 概要 | メリット | デメリット |
|---------|---------|------|---------|-----------|
| **IDE** | [**Visual Studio**](https://visualstudio.microsoft.com/) | Microsoft製フル機能IDE。.NET開発に最適化 | ✅ .NET開発最適<br>✅ デバッガ非常に強力<br>✅ プロファイリング充実<br>✅ Azure統合<br>✅ Community版無料 | ❌ Windows中心<br>❌ 重い（数GB必要）<br>❌ 起動遅い |
| **IDE** | [**Rider**](https://www.jetbrains.com/rider/) | JetBrains製.NET IDE。クロスプラットフォーム | ✅ Windows/Mac/Linux対応<br>✅ ReSharper統合<br>✅ Unity統合<br>✅ 高速 | ❌ 有料（年$149）<br>❌ VS比で機能少ない |
| **ビルドツール** | [**MSBuild**](https://github.com/dotnet/msbuild) | Microsoft製.NETビルドツール | ✅ Visual Studio統合<br>✅ .NET標準<br>✅ NuGet統合<br>✅ 無料 | ❌ Windows依存強<br>❌ XML設定<br>❌ 他言語非対応 |
| **パッケージマネージャー** | [**NuGet**](https://www.nuget.org/) | .NETパッケージマネージャー | ✅ .NET標準<br>✅ Visual Studio統合<br>✅ 豊富なパッケージ<br>✅ 無料 | ❌ 依存関係地獄<br>❌ パッケージ品質ばらつき |
| **フレームワーク** | [**ASP.NET Core**](https://dotnet.microsoft.com/apps/aspnet) | Microsoft製Webフレームワーク。クロスプラットフォーム | ✅ 高性能<br>✅ クロスプラットフォーム<br>✅ モダンアーキテクチャ<br>✅ 無料オープンソース | ❌ 頻繁な変更<br>❌ 学習コスト高<br>❌ レガシー移行困難 |
| **テスト** | [**xUnit**](https://xunit.net/) | .NET単体テストフレームワーク | ✅ モダン設計<br>✅ 並列実行<br>✅ .NET Core対応<br>✅ Visual Studio統合 | ❌ セットアップテストやや複雑<br>❌ NUnit比で情報少ない |
| **テスト** | [**NUnit**](https://nunit.org/) | .NET単体テストフレームワーク。歴史長い | ✅ 長い実績<br>✅ 豊富な機能<br>✅ パラメータ化テスト<br>✅ 無料 | ❌ xUnit比で古い<br>❌ 並列実行弱い |
| **モック** | [**Moq**](https://github.com/moq/moq4) | .NETモックフレームワーク | ✅ 使いやすい<br>✅ Linq to Mocks<br>✅ .NET統合<br>✅ 無料 | ❌ 学習曲線あり<br>❌ エラーメッセージ分かりにくい |
| **コード品質** | [**ReSharper**](https://www.jetbrains.com/resharper/) | Visual Studio拡張。リファクタリング・分析 | ✅ 強力なリファクタリング<br>✅ コード分析<br>✅ ナビゲーション高速<br>✅ 生産性向上 | ❌ 有料（年$149）<br>❌ VS動作重くなる<br>❌ Rider推奨 |
| **フォーマッター** | [**EditorConfig**](https://editorconfig.org/) | エディタ横断コーディングスタイル設定 | ✅ エディタ横断<br>✅ .editorconfig設定<br>✅ Visual Studio標準サポート<br>✅ 無料 | ❌ 機能限定的<br>❌ 全ルール非対応 |

---

#### 2.1.3. Python 開発ツール

| カテゴリ | ツール名 | 概要 | メリット | デメリット |
|---------|---------|------|---------|-----------|
| **IDE** | [**PyCharm**](https://www.jetbrains.com/pycharm/) | JetBrains製Python専用IDE。Django/Flask対応 | ✅ Python特化<br>✅ Django/Flask統合<br>✅ Jupyter対応<br>✅ データサイエンスツール<br>✅ リモート開発 | ❌ Professional版有料<br>❌ メモリ使用量大<br>❌ 起動遅い |
| **IDE** | [**VS Code + Python拡張**](https://code.visualstudio.com/) | 軽量エディタ + Python拡張 | ✅ 無料<br>✅ 軽量<br>✅ Jupyter統合<br>✅ リモート開発<br>✅ 拡張機能豊富 | ❌ PyCharm比で機能劣る<br>❌ 初期設定必要<br>❌ デバッグ弱い |
| **パッケージマネージャー** | [**pip**](https://pip.pypa.io/) | Python標準パッケージマネージャー | ✅ Python標準<br>✅ PyPI統合<br>✅ 簡単インストール<br>✅ 無料 | ❌ 依存関係解決弱い<br>❌ 環境管理別途必要 |
| **パッケージマネージャー** | [**Poetry**](https://python-poetry.org/) | モダンPython依存関係管理 | ✅ 依存関係解決優秀<br>✅ pyproject.toml<br>✅ 仮想環境自動管理<br>✅ ビルド・公開統合 | ❌ 学習コスト<br>❌ pip比で遅い<br>❌ 一部ライブラリ非互換 |
| **環境管理** | [**venv**](https://docs.python.org/3/library/venv.html) | Python標準仮想環境 | ✅ Python標準<br>✅ 軽量<br>✅ セットアップ簡単<br>✅ 無料 | ❌ 機能最小限<br>❌ バージョン管理別途必要 |
| **環境管理** | [**pyenv**](https://github.com/pyenv/pyenv) | Pythonバージョン管理 | ✅ 複数バージョン管理<br>✅ プロジェクト別設定<br>✅ 無料<br>✅ Unix系最適 | ❌ Windows非公式<br>❌ セットアップやや複雑 |
| **フレームワーク** | [**Django**](https://www.djangoproject.com/) | Pythonフルスタックフレームワーク | ✅ バッテリー同梱<br>✅ ORM強力<br>✅ Admin画面自動生成<br>✅ セキュリティ強固 | ❌ 重い<br>❌ 学習曲線急<br>❌ 小規模には過剰 |
| **フレームワーク** | [**FastAPI**](https://fastapi.tiangolo.com/) | モダン高速APIフレームワーク | ✅ 非常に高速<br>✅ 自動ドキュメント生成<br>✅ 型ヒント活用<br>✅ 非同期対応 | ❌ 比較的新しい<br>❌ フルスタックではない<br>❌ Django比で機能少ない |
| **テスト** | [**pytest**](https://pytest.org/) | Python単体テストフレームワーク | ✅ シンプルな構文<br>✅ フィクスチャ強力<br>✅ プラグイン豊富<br>✅ パラメータ化テスト | ❌ 学習コスト<br>❌ 標準ライブラリではない |
| **リンター** | [**Ruff**](https://github.com/astral-sh/ruff) | 超高速Pythonリンター（Rust製） | ✅ 非常に高速<br>✅ Flake8/pylint置換<br>✅ 自動修正<br>✅ 設定簡単 | ❌ 比較的新しい<br>❌ 一部ルール非対応 |
| **リンター** | [**pylint**](https://pylint.org/) | 包括的Pythonリンター | ✅ 詳細な分析<br>✅ カスタマイズ可能<br>✅ コード品質スコア<br>✅ 無料 | ❌ 遅い<br>❌ 誤検知多い<br>❌ 設定複雑 |
| **フォーマッター** | [**Black**](https://black.readthedocs.io/) | 妥協なしPythonフォーマッター | ✅ 一貫したスタイル<br>✅ 設定不要<br>✅ 高速<br>✅ Git統合 | ❌ カスタマイズ不可<br>❌ 好みに合わない場合あり |
| **型チェック** | [**mypy**](http://mypy-lang.org/) | Python静的型チェッカー | ✅ 型安全性向上<br>✅ IDE統合<br>✅ 段階的導入可能<br>✅ 無料 | ❌ 実行時チェックなし<br>❌ ライブラリスタブ必要<br>❌ 学習コスト |

---

#### 2.1.4. TypeScript 開発ツール

| カテゴリ | ツール名 | 概要 | メリット | デメリット |
|---------|---------|------|---------|-----------|
| **IDE** | [**VS Code**](https://code.visualstudio.com/) | Microsoft製軽量エディタ。TypeScript標準サポート | ✅ TypeScript最適化<br>✅ 無料<br>✅ 拡張機能豊富<br>✅ IntelliSense強力<br>✅ デバッガ統合 | ❌ 大規模PJ重い<br>❌ フルIDEではない |
| **IDE** | [**WebStorm**](https://www.jetbrains.com/webstorm/) | JetBrains製JS/TS専用IDE | ✅ TypeScript特化<br>✅ リファクタリング強力<br>✅ Node/React/Vue統合<br>✅ デバッグ優秀 | ❌ 有料（年$69）<br>❌ VSCodeで代替可<br>❌ メモリ使用量大 |
| **ランタイム** | [**Node.js**](https://nodejs.org/) | JavaScriptランタイム | ✅ 業界標準<br>✅ npm統合<br>✅ 豊富なライブラリ<br>✅ 無料 | ❌ バージョン管理必要<br>❌ シングルスレッド |
| **パッケージマネージャー** | [**npm**](https://www.npmjs.com/) | Node.js標準パッケージマネージャー | ✅ Node.js標準<br>✅ 最大パッケージ数<br>✅ package.json<br>✅ 無料 | ❌ 遅い<br>❌ node_modules肥大化<br>❌ セキュリティ懸念 |
| **パッケージマネージャー** | [**pnpm**](https://pnpm.io/) | 高速・効率的パッケージマネージャー | ✅ npm比で高速<br>✅ ディスク効率的<br>✅ モノレポ対応<br>✅ 厳密な依存解決 | ❌ npmより認知度低<br>❌ 一部ツール非互換 |
| **パッケージマネージャー** | [**Yarn**](https://yarnpkg.com/) | Facebook製パッケージマネージャー | ✅ npm比で高速<br>✅ ロックファイル<br>✅ ワークスペース<br>✅ オフラインモード | ❌ pnpm比で遅い<br>❌ npm比で利点減少 |
| **ビルドツール** | [**Vite**](https://vitejs.dev/) | 次世代フロントエンドビルドツール | ✅ 非常に高速<br>✅ HMR高速<br>✅ TypeScript標準対応<br>✅ プラグイン豊富 | ❌ 比較的新しい<br>❌ レガシーブラウザサポート弱い |
| **ビルドツール** | [**Webpack**](https://webpack.js.org/) | モジュールバンドラー。業界標準 | ✅ 業界標準<br>✅ 高度なカスタマイズ<br>✅ プラグイン豊富<br>✅ 本番最適化 | ❌ 設定複雑<br>❌ ビルド遅い<br>❌ Vite推奨 |
| **フレームワーク** | [**React**](https://react.dev/) | Meta製UIライブラリ | ✅ 最大ユーザーベース<br>✅ コンポーネント指向<br>✅ TypeScript統合<br>✅ エコシステム充実 | ❌ フルフレームワークではない<br>❌ 状態管理別途必要<br>❌ 学習曲線 |
| **フレームワーク** | [**Next.js**](https://nextjs.org/) | Reactフルスタックフレームワーク | ✅ SSR/SSG<br>✅ ファイルベースルーティング<br>✅ TypeScript標準<br>✅ Vercel統合 | ❌ Vercel依存<br>❌ 頻繁な破壊的変更<br>❌ 複雑化しやすい |
| **フレームワーク** | [**Vue.js**](https://vuejs.org/) | プログレッシブJavaScriptフレームワーク | ✅ 学習曲線緩やか<br>✅ 公式ツール充実<br>✅ TypeScript対応<br>✅ 柔軟 | ❌ React比でエコシステム小<br>❌ 企業採用少ない |
| **テスト** | [**Vitest**](https://vitest.dev/) | Vite対応高速ユニットテスト | ✅ 非常に高速<br>✅ Vite統合<br>✅ Jest互換API<br>✅ TypeScript標準 | ❌ 比較的新しい<br>❌ Jestより情報少ない |
| **テスト** | [**Jest**](https://jestjs.io/) | JavaScriptテストフレームワーク | ✅ 業界標準<br>✅ 設定ゼロ<br>✅ スナップショットテスト<br>✅ モック機能 | ❌ 遅い<br>❌ Vitest推奨<br>❌ ESM対応弱い |
| **E2Eテスト** | [**Playwright**](https://playwright.dev/) | Microsoft製E2Eテスト | ✅ クロスブラウザ<br>✅ 高速<br>✅ TypeScript標準<br>✅ 自動待機 | ❌ 学習コスト<br>❌ セットアップやや複雑 |
| **リンター** | [**ESLint**](https://eslint.org/) | JavaScript/TypeScriptリンター | ✅ 業界標準<br>✅ カスタマイズ可能<br>✅ TypeScript対応<br>✅ 自動修正 | ❌ 設定複雑<br>❌ パフォーマンスやや遅い |
| **フォーマッター** | [**Prettier**](https://prettier.io/) | コードフォーマッター | ✅ 一貫したスタイル<br>✅ 多言語対応<br>✅ ESLint統合<br>✅ 設定最小限 | ❌ カスタマイズ限定的<br>❌ 好みに合わない場合あり |
3. | **型チェック** | [**TypeScript**](https://www.typescriptlang.org/) | TypeScript公式コンパイラ | ✅ 型安全性<br>✅ IDE統合<br>✅ 段階的導入可能<br>✅ 無料 | ❌ ビルドステップ必要<br>❌ 学習コスト<br>❌ 型定義必要 |
---

### 3.1. 汎用開発ツール

## 4. コードレビュー

**対応項目**
- コードレビュー


## 5.1. AI コード補完（全言語共通）

| # | ツール名 | 概要 | メリット | デメリット |
|---|---------|------|---------|-----------|
| 1 | [**GitHub Copilot**](https://github.com/features/copilot) | OpenAI Codex AIペアプログラマー | ✅ コード生成速度速い<br>✅ 多言語対応<br>✅ VSCode/JetBrains統合<br>✅ 生産性大幅向上 | ❌ 月額$10（有料）<br>❌ 生成コード品質ばらつき<br>❌ インターネット必須 |
| 2 | [**Cursor**](https://cursor.sh/) | AI統合型コードエディタ。VSCodeベース | ✅ AI機能強力<br>✅ コード編集・生成直感的<br>✅ VSCode拡張互換<br>✅ チャット形式修正 | ❌ 有料プラン推奨（月$20）<br>❌ 新しく安定性に課題<br>❌ AI依存強い |
| 3 | [**Amazon CodeWhisperer**](https://aws.amazon.com/codewhisperer/) | AWS製AIコード生成。個人利用無料 | ✅ 個人利用無料<br>✅ セキュリティスキャン内蔵<br>✅ AWS SDK最適化<br>✅ VSCode/JetBrains対応 | ❌ Copilot比で精度劣る<br>❌ AWS寄り<br>❌ 言語サポート限定的 |

---


**関連ドキュメント**:
- [4. インフラ設計・構築](./dev_process_開発工程_4_インフラ設計・構築.md)
- [6. アプリケーションテスト](./dev_process_開発工程_6_アプリケーションテスト.md)

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 2.0
