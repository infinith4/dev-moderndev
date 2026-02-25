# Maven

## 概要

Maven は Java プロジェクト向けのビルド・依存管理ツールである。`pom.xml` を中心に、コンパイル、テスト、パッケージング、配布までの手順を標準化し、開発環境と CI 環境の再現性を高める。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（Apache License 2.0） |
| 商用利用 | ライセンス上利用可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 標準ライフサイクル | `validate`〜`deploy` まで段階実行を統一 |
| 依存管理 | Maven Central 等から依存を自動解決 |
| 宣言的設定 | `pom.xml` で構成を明示管理 |
| 拡張性 | Plugin によりビルド機能を追加可能 |
| マルチモジュール | 大規模プロジェクトを分割管理しやすい |
| 実績 | Java エコシステムで長期運用の採用実績が多い |

## 主な機能

### ビルド機能

| 機能 | 説明 |
|------|------|
| `compile` | ソースをコンパイル |
| `test` | テストコードを実行 |
| `package` | JAR/WAR などの成果物を生成 |
| `install/deploy` | ローカル/リモートリポジトリへ公開 |

### 依存管理機能

| 機能 | 説明 |
|------|------|
| Dependency Resolution | 推移的依存を含めて自動解決 |
| Scope 制御 | `compile`/`test`/`runtime` など適用範囲を指定 |
| DependencyManagement | バージョンを一元管理 |
| BOM 利用 | 複数ライブラリの整合性を維持 |

### 運用機能

| 機能 | 説明 |
|------|------|
| Parent POM | 共通設定の集約 |
| Profiles | 環境別ビルド設定の切替 |
| Plugin 連携 | Checkstyle、SpotBugs など品質工程を統合 |
| Multi-module Build | 複数モジュールを一括ビルド |

## インストールとセットアップ

公式URL:
- [Apache Maven 公式サイト](https://maven.apache.org/)
- [Maven Guides](https://maven.apache.org/guides/)
- [Maven Plugin Index](https://maven.apache.org/plugins/index.html)
- [Maven Central](https://search.maven.org/)

セットアップの要点:
1. JDK と Maven をインストールし、`mvn -v` で確認する。
2. `pom.xml` にプロジェクト情報と依存を定義する。
3. 必要に応じて `settings.xml` でリポジトリ/プロキシを設定する。
4. チーム共通の Plugin 設定は Parent POM に集約する。

## 基本的な使い方

1. 最小の `pom.xml` を作成してプロジェクトを初期化する。
2. `mvn clean test` でビルドとテストの基本動作を確認する。
3. 依存追加後は `dependency:tree` で競合を確認する。
4. リリース時は `mvn clean package` で成果物を生成する。
5. 配布が必要な場合は `deploy` を実行してリポジトリへ公開する。

最小運用例:
- ビルド: `mvn clean package`
- 依存確認: `mvn dependency:tree`

## メリット

- Java ビルド手順を標準化しやすい。
- 依存関係を宣言的に管理でき、再現性を保ちやすい。
- Plugin 連携で品質チェックを統合しやすい。
- マルチモジュール構成の運用に適している。

## デメリット

- `pom.xml` が大規模化すると可読性が下がりやすい。
- 依存競合発生時の調査と調整に時間がかかる。
- Plugin 過多の構成はビルド速度と保守性を下げやすい。

## CI/CD での使用

CI では `mvn -B clean verify` を基本コマンドにして、ローカルと同一手順で検証する運用が一般的である。CD では成果物をリポジトリへ配布し、デプロイジョブから同じ成果物を利用することで、環境差分による不具合を減らしやすい。

## 他ツールとの比較

| ツール | 主な用途 | 特徴 |
|------|------|------|
| Maven | Java ビルド/依存管理 | 標準ライフサイクルで運用を統一しやすい |
| Gradle | ビルド自動化 | 柔軟性と高速化に強み |
| Bazel | 大規模ビルド | 厳密再現性と高速性に強い |
| Ant | ビルド自動化 | 手続き的で自由度は高いが標準化しづらい |

## ベストプラクティス

### 1. 依存バージョンを統制

- `dependencyManagement` や BOM でバージョンを統一する。
- 不要依存を定期的に整理する。

### 2. 共通設定を集約

- Parent POM に Plugin とルールを集約する。
- モジュールごとの重複設定を減らす。

### 3. CI とローカルを一致

- 開発者と CI で同じ Maven コマンドを使う。
- 失敗時に `surefire-reports` を確認できるようにする。

## 公式ドキュメント

- 公式サイト: https://maven.apache.org/
- Guides: https://maven.apache.org/guides/
- Plugin Index: https://maven.apache.org/plugins/index.html
- Maven Central: https://search.maven.org/

## まとめ

1. ** 標準化 ** : Maven は Java プロジェクトのビルドと依存管理を標準化しやすい。
2. ** 品質向上 ** : `pom.xml`、BOM、Parent POM の設計が運用品質を左右する。
3. ** 自動運用 ** : CI/CD と同一手順で運用することで、ビルド再現性を高めやすい。

