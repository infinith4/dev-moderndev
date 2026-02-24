# NuGet

## 概要

NuGet は .NET エコシステムの標準パッケージ管理ツールである。`PackageReference` と `NuGet.config` を中心に依存解決、復元、公開を管理し、.NET アプリケーションとライブラリのビルド再現性を高める。

## 料金

| プラン | 内容 |
|------|------|
| NuGet CLI / dotnet CLI | 無料（OSS） |
| nuget.org | 公開パッケージレジストリを無料利用可能 |
| Private Feed | Azure Artifacts / GitHub Packages などは提供元プランに依存 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| .NET 標準統合 | `dotnet` CLI と Visual Studio に統合 |
| 宣言的依存管理 | `PackageReference` で依存を明示 |
| Central Package Management | 複数プロジェクトのバージョンを集中管理 |
| 複数フィード対応 | 公開/社内フィードを使い分け可能 |
| セキュリティ機能 | 脆弱性・非推奨パッケージを検知可能 |
| CI/CD 連携 | 復元、ビルド、公開をパイプライン化しやすい |

## 主な機能

### 依存関係管理機能

| 機能 | 説明 |
|------|------|
| `dotnet add package` | 依存パッケージを追加 |
| `dotnet restore` | 依存関係を復元 |
| `PackageReference` | プロジェクトファイルで依存を宣言 |
| `Directory.Packages.props` | バージョンを集中管理（CPM） |

### フィード/公開機能

| 機能 | 説明 |
|------|------|
| NuGet.config | フィードと認証設定を管理 |
| `dotnet nuget push` | パッケージ公開 |
| Source Mapping | フィードごとの利用範囲を制御 |
| API Key 管理 | 公開時認証を安全に運用 |

### 品質/運用機能

| 機能 | 説明 |
|------|------|
| `dotnet list package --outdated` | 更新候補の可視化 |
| `--vulnerable` | 脆弱性パッケージの検出 |
| `--deprecated` | 非推奨依存の確認 |
| キャッシュ管理 | 復元高速化と障害対応 |

## インストールとセットアップ

公式URL:
- [NuGet 公式ドキュメント](https://learn.microsoft.com/nuget/)
- [nuget.org](https://www.nuget.org/)
- [Central Package Management](https://learn.microsoft.com/nuget/consume-packages/central-package-management)

セットアップの要点:
1. .NET SDK をインストールし、`dotnet --version` を確認する。
2. プロジェクトで `PackageReference` を採用する。
3. 複数プロジェクトでは CPM を導入してバージョンを統一する。
4. `NuGet.config` で公開/社内フィードと認証を分離管理する。

## 基本的な使い方

1. `dotnet add package <name>` で依存を追加する。
2. `dotnet restore` で依存を復元する。
3. `dotnet list package --outdated` で更新候補を確認する。
4. ライブラリは `dotnet pack` で `.nupkg` を作成する。
5. `dotnet nuget push` で対象フィードへ公開する。

最小運用例:
- 依存追加: `dotnet add package Serilog`
- CI: `dotnet restore && dotnet build && dotnet test`

## メリット

- .NET 開発基盤に統合され、運用しやすい。
- PackageReference/CPM で依存バージョンを統制しやすい。
- 公開と社内配布を同じ仕組みで管理しやすい。
- 脆弱性確認を開発フローへ組み込みやすい。

## デメリット

- .NET 以外のエコシステムには適用できない。
- フィードが増えると認証・設定管理が複雑になる。
- 推移的依存の競合調整に時間がかかる場合がある。

## CI/CD での使用

CI では `dotnet restore` と `dotnet build/test` を固定し、依存復元から検証までを自動化する。CD では `dotnet pack` と `dotnet nuget push` を利用して、タグやバージョン規約に沿ってパッケージ配布を自動化できる。

## 他ツールとの比較

| ツール | 強み | 特徴 |
|------|------|------|
| NuGet | .NET 標準 | `dotnet` と統合しやすい |
| Paket | 厳密ロック | 依存管理の制御性が高い |
| npm | JS エコシステム | Node.js パッケージ管理向け |
| Maven | JVM エコシステム | Java/Scala の標準管理基盤 |

## ベストプラクティス

### 1. バージョン管理を集中化

- `Directory.Packages.props` でバージョンを統一する。
- 例外バージョンは最小限に抑える。

### 2. フィード運用を分離

- 公開フィードと社内フィードを明確に分ける。
- Source Mapping で混在利用を防ぐ。

### 3. 品質チェックを自動化

- `--vulnerable` と `--deprecated` を定期実行する。
- 重大脆弱性は CI 失敗条件として扱う。

## 公式ドキュメント

- 公式ドキュメント: https://learn.microsoft.com/nuget/
- nuget.org: https://www.nuget.org/
- CPM: https://learn.microsoft.com/nuget/consume-packages/central-package-management

## まとめ

- NuGet は .NET 向け依存管理と配布を標準化しやすい。
- PackageReference と CPM を使うと、複数プロジェクトの整合性を保ちやすい。
- CI/CD へ復元・検証・公開を組み込むことで、安定した配布運用を実現しやすい。
