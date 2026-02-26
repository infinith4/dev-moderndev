# .NET Coding Conventions

## 概要

.NET Coding Conventions は .NET 開発での命名、設計、可読性、保守性を統一するための規約群である。チームで共通ルールを持つことで、レビュー効率と品質の一貫性を高められる。

## 料金

| 区分 | 内容 |
|------|------|
| 規約自体 | 無料（ガイドライン） |
| 補足 | 適用支援ツール（IDE/Analyzer）に有料製品が含まれる場合あり |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 読みやすさ重視 | 一貫した命名・構造を維持 |
| 品質向上 | 典型的な実装ミスを減らしやすい |
| チーム共有 | 新規参加者も同じ基準で実装可能 |
| 自動化可能 | Analyzer/Formatter で機械的に適用 |
| 長期保守向き | リファクタや拡張時の負担を軽減 |

## 主な機能

### 規約定義

| 機能 | 説明 |
|------|------|
| 命名規則 | クラス、メソッド、変数などの命名統一 |
| コード構造 | ファイル構成、責務分割、依存方向を整理 |
| 例外処理方針 | エラー処理の統一 |
| 非同期規約 | `async/await` 利用パターンの統一 |

### 自動適用支援

| 機能 | 説明 |
|------|------|
| EditorConfig | フォーマット設定を共通化 |
| Roslyn Analyzer | 規約違反を自動検知 |
| Code Fix | 修正提案で適用を支援 |
| CI 検証 | ルール逸脱をビルド段階で検出 |

### 運用機能

| 機能 | 説明 |
|------|------|
| ルールバージョン管理 | 規約変更の追跡 |
| 例外ルール管理 | 特例箇所を明示管理 |
| レビュー基準統一 | 指摘基準のブレを抑制 |
| 教育資料化 | チームオンボーディングに活用 |

## インストールとセットアップ

公式URL:
- [.NET コーディング規約](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [C# コーディングスタイル](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/style-guide)

セットアップ手順:
1. チーム向け規約ドキュメントを定義する。
2. `.editorconfig` と Analyzer 設定に規約を反映する。
3. IDE と CI で同じルールセットを適用する。

## 基本的な使い方

1. まず命名とフォーマットの最小規約を決める。
2. 次に Analyzer 警告レベルを定義し、違反を可視化する。
3. ルールは段階導入し、開発阻害を避ける。
4. 定期的に規約を見直し、実態に合わせて更新する。

最小コマンド:
- 参考: `dotnet format --verify-no-changes`

## メリット

- コード品質のばらつきを減らせる
- レビュー効率が向上する
- 新規参加者の立ち上がりが早くなる
- 長期運用で保守性を確保しやすい

## デメリット

- 初期合意に時間がかかる
- 厳しすぎる規約は開発速度を下げる
- 例外運用が曖昧だと形骸化する

## 他ツールとの比較

| 項目 | 主な用途 | 特徴 |
|------|------|------|
| .NET Coding Conventions | 規約基準 | 方針定義の土台 |
| Roslyn Analyzers | 規約検証 | 自動検知・修正支援 |
| StyleCop Analyzers | C# スタイル検証 | 詳細な規約適用に強い |
| dotnet format | 整形適用 | フォーマット統一を自動化 |

## ベストプラクティス

### 1. 最小ルールから開始

- 命名・フォーマット中心で始める
- チーム負荷を見ながら拡張する

### 2. ツールで自動化

- IDE だけでなく CI でも検証する
- 手動レビュー依存を減らす

### 3. 例外を管理

- 例外は理由と期限を残す
- 定期的に例外を整理する

## 公式ドキュメント

- 規約: https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions
- スタイルガイド: https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/style-guide
- EditorConfig: https://learn.microsoft.com/dotnet/fundamentals/code-analysis/code-style-rule-options

## まとめ

1. **共通化** : .NET 規約は品質基準の共通言語として有効。
2. **自動化** : Analyzer と EditorConfig による自動化で運用が安定する。
3. **段階性** : 規約は段階導入と定期見直しが成功しやすい。
