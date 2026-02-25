# Pencil

## 概要

Pencil は、IDE 内で動作するベクターデザインツールである。`.pen` ファイルをGit管理しながら、デザインとコードを同じリポジトリで運用できる。MCP 経由で AI アシスタントと連携し、UI 生成や Design to Code を実行できる。

本ドキュメントは `https://www.pencil.dev/` の Pencil を対象としている（旧OSSの「Pencil Project」とは別製品）。

## 料金

| プラン | 内容 |
|------|------|
| Pencil | 無料（2026年2月24日時点） |
| 商用利用 | 可能（契約・利用規約は最新情報を確認） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| IDE 統合 | VS Code / Cursor などでデザイン編集が可能 |
| Design as Code | `.pen` をGitでバージョン管理できる |
| AI 連携 | MCP 経由で UI 生成・コード生成を実行可能 |
| トークン運用 | 色・余白・文字などを変数化して再利用できる |
| 連携性 | React/Next.js/Vue/Svelte などへ出力しやすい |

## 主な機能

### デザイン編集機能

| 機能 | 説明 |
|------|------|
| Infinite Canvas | IDE 内でキャンバスを拡張しながら設計できる |
| コンポーネント | 再利用可能な UI パーツを定義・更新できる |
| 変数（トークン） | 色・余白・文字スタイルを統一管理できる |
| Figma 取り込み | フレームのコピー&ペーストで移行を補助できる |

### Design as Code 機能

| 機能 | 説明 |
|------|------|
| `.pen` ファイル管理 | デザイン成果物をテキストとして保存・管理できる |
| Git 連携 | コードと同じブランチ戦略で差分管理できる |
| リポジトリ同居 | 実装コードとデザインファイルの整合を維持しやすい |

### AI 連携機能

| 機能 | 説明 |
|------|------|
| MCP サーバー | Pencil 起動時にローカル MCP を利用可能 |
| プロンプト生成 | 画面やコンポーネントを自然言語で生成できる |
| Design to Code | React/Next.js/Vue/Svelte/HTML+CSS へ変換できる |
| トークン同期 | CSS 変数や Tailwind 設定との同期を支援 |

## インストールとセットアップ

公式URL:
- [Pencil 公式サイト](https://www.pencil.dev/)
- [Downloads](https://www.pencil.dev/downloads)
- [Pricing](https://www.pencil.dev/pricing)
- [Pencil Docs](https://docs.pencil.dev/)
- [Installation](https://docs.pencil.dev/getting-started/installation)
- [Authentication](https://docs.pencil.dev/getting-started/authentication)

セットアップの要点:
1. Desktop 版または IDE 拡張（VS Code / Cursor）を導入する。
2. 初回起動時にメール認証でアクティベーションする。
3. AI 連携を使う場合は Claude Code などの認証を先に完了する。
4. リポジトリ内に `.pen` ファイルを作成し、Git 管理を開始する。

## 基本的な使い方

1. `design.pen` などのファイルを作成し、画面フレームを定義する。
2. コンポーネントと変数を作成して UI ルールを揃える。
3. 必要に応じて `Cmd/Ctrl + K` で AI 指示を実行する。
4. Design to Code で実装コードを生成し、既存コードへ反映する。
5. `.pen` と実装コードを同じコミットで管理し、変更理由を追跡する。

最小運用例:
- デザインファイル: `design.pen`
- 運用単位: 「画面変更 + トークン変更 + 実装変更」を1コミットにまとめる

## メリット

- IDE 内で設計から実装まで進められ、作業切替コストを下げられる
- `.pen` をGit管理できるため、設計変更履歴を追跡しやすい
- AI 連携により、初期画面や部品の作成スピードを上げられる
- デザイントークンを実装へ反映しやすく、UI 一貫性を保ちやすい

## デメリット

- リアルタイム共同編集は前提ではなく、Git ベースの協業が中心になる
- 自動保存に依存せず、手動保存とコミット運用が必要になる
- Undo/Redo が複雑な編集では不足する場合があり、こまめなコミットが必要
- AI 機能は認証や利用環境に依存するため、初期セットアップが必要

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|-----------|-----------|
| 要件定義（画面要件） | 画面ラフ、導線検討、初期UI合意 | 画面ワイヤー、画面フロー |
| 基本設計（アプリ） | コンポーネント化、デザイントークン定義、画面設計 | 画面設計書、コンポーネント定義 |
| 詳細設計〜実装 | Design→Code生成、既存コードとの同期調整 | フロントエンド実装、スタイル定義 |
| 保守・改修 | 既存画面の差分設計、トークン更新反映 | 改修デザイン、更新済みUIコード |

## 他ツールとの比較

| ツール | 特徴 | 向いているケース |
|------|------|------|
| Pencil | IDE 統合、Design as Code、AI 連携 | 実装と設計を同一リポジトリで管理したい |
| Figma | クラウド協業、コメント、デザインレビュー | 非エンジニア含む大人数で共同編集したい |
| Penpot | OSS、Webベース、共同編集 | OSS 中心でブラウザ運用を重視したい |

## ベストプラクティス

### 1. デザイン変更と実装変更を同時管理

- `.pen` 変更とコード変更を同一PRでレビューする
- 「画面仕様変更」をコミットメッセージに明記する

### 2. 変数（トークン）を先に定義

- 色・余白・タイポグラフィを先に変数化する
- ハードコード値を減らし、変更影響を局所化する

### 3. AI 生成物をそのまま採用しない

- 生成後に命名規約、アクセシビリティ、レスポンシブを確認する
- 既存デザインシステムとの整合性チェックをレビュー項目に入れる

## 公式ドキュメント

- 公式サイト: https://www.pencil.dev/
- ダウンロード: https://www.pencil.dev/downloads
- 料金: https://www.pencil.dev/pricing
- ドキュメント: https://docs.pencil.dev/
- Installation: https://docs.pencil.dev/getting-started/installation
- Authentication: https://docs.pencil.dev/getting-started/authentication
- AI Integration: https://docs.pencil.dev/getting-started/ai-integration
- Design to Code: https://docs.pencil.dev/design-and-code/design-to-code

## まとめ

1. ** 統合運用 ** : デザイン資産をコード資産と同じ運用で扱いたいチームに適したツールである。
2. ** 往復短縮 ** : IDE 統合と AI 連携により、設計から実装までの往復を短縮できる。
3. ** Git中心 ** : 共同編集や運用ルールはGit中心で設計する必要がある。

---

**カテゴリ**: デザインツール
**対象工程**: 要件定義・基本設計・実装
**最終更新**: 2026年2月24日
**ドキュメントバージョン**: 2.1
