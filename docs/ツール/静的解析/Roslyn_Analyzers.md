# Roslyn Analyzers

## 概要

Roslyn Analyzers は .NET コードを静的解析して品質問題や規約違反を検出する機能群である。コンパイル時に警告やエラーとして可視化でき、品質基準の自動適用に有効。

## 料金

| 区分 | 内容 |
|------|------|
| 標準 Analyzer | 無料 |
| 補足 | 一部サードパーティ Analyzer は有料の場合あり |

## 主な特徴

| 項目 | 内容 |
|------|------|
| .NET 統合 | ビルドと IDE に直接統合 |
| ルール可変 | 重大度を Warning/Error で調整 |
| 自動修正支援 | Code Fix で修正を補助 |
| 継続運用 | CI に組み込みやすい |
| 規約適用 | チーム標準ルールを機械的に適用可能 |

## 主な機能

### 解析機能

| 機能 | 説明 |
|------|------|
| コード品質検証 | バグや可読性問題を検出 |
| スタイル検証 | 命名・書式ルールを適用 |
| セキュリティ検証 | 一部脆弱性パターンを検知 |
| API 使用検証 | 非推奨 API 利用を警告 |

### 設定機能

| 機能 | 説明 |
|------|------|
| `.editorconfig` 連携 | ルール設定をコード管理 |
| 重大度制御 | ルールごとに警告レベル設定 |
| ルール除外 | 対象外条件を明示管理 |
| カスタム Analyzer | 独自ルール追加が可能 |

### 運用機能

| 機能 | 説明 |
|------|------|
| IDE 即時検出 | 開発中に問題を確認 |
| ビルドゲート | 違反をビルド失敗へ反映 |
| レビュー支援 | 指摘観点を統一 |
| 長期保守 | 規約逸脱を継続抑制 |

## インストールとセットアップ

公式URL:
- [Roslyn Analyzer Rules](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview)
- [.NET Code Analysis](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/)

セットアップ手順:
1. プロジェクトに Analyzer パッケージを導入する。
2. `.editorconfig` でルール重大度を定義する。
3. まず警告運用で始め、安定後にエラー化する。

## 基本的な使い方

1. 既定ルールを有効化して現状課題を把握する。
2. 重大ルールから優先的に対応する。
3. 新規コードは違反ゼロを基準に運用する。
4. 例外ルールは理由と期限を残して管理する。

最小コマンド:
- 検証: `dotnet build`

## メリット

- .NET 開発フローに自然に組み込める
- 品質問題を早期検出できる
- 規約統一とレビュー効率化に有効
- 継続的な品質ゲートを作りやすい

## デメリット

- ルール数が多く初期調整が必要
- 過剰設定はノイズを増やす
- 既存コード適用時に対応コストが高くなる

## 他ツールとの比較

| ツール | 主な用途 | 特徴 |
|------|------|------|
| Roslyn Analyzers | .NET 静的解析 | IDE/ビルド統合が強い |
| StyleCop Analyzers | スタイル規約 | 命名・書式規約に強い |
| SonarQube | 品質可視化 | 多言語横断でメトリクス管理 |
| ReSharper | コード解析支援 | IDE 補助機能が豊富 |

## ベストプラクティス

### 1. 優先度で段階導入

- 重大な品質問題ルールから適用する
- ノイズを抑えつつ厳格化する

### 2. 設定をコード管理

- `.editorconfig` をリポジトリ管理する
- 変更はレビューで合意する

### 3. ビルドゲート化

- 重要違反をエラー扱いにする
- CI で継続的にチェックする

## 公式ドキュメント

- 概要: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview
- ルール: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/
- 設定: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/configuration-options

## まとめ

1. Roslyn Analyzers は .NET 品質管理の基盤として有効。
2. 段階導入と設定管理でノイズを抑えられる。
3. CI で継続適用することで品質を維持できる。
