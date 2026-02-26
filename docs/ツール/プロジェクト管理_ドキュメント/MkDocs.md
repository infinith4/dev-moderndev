# MkDocs

## 概要

MkDocs は、Markdown から技術ドキュメントサイトを生成する静的サイトジェネレーターである。Python ベースで導入しやすく、軽量な構成で開発チーム向けのドキュメントポータルを整備しやすい。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（オープンソース） |
| 商用利用 | ライセンス上利用可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Markdown 中心 | テキストベースで文書を管理可能 |
| 設定がシンプル | `mkdocs.yml` でサイト構成を定義 |
| テーマ対応 | Material などのテーマを適用可能 |
| プレビュー機能 | ローカルで即時確認可能 |
| 静的出力 | CDN・静的ホスティングへ配信しやすい |
| Python 連携 | 既存 Python 開発環境と統合しやすい |

## 主な機能

### ドキュメント生成機能

| 機能 | 説明 |
|------|------|
| Markdown 変換 | 文書を HTML へ変換 |
| ナビゲーション設定 | 階層メニューを構成 |
| ページ構成管理 | 章立てを `mkdocs.yml` で定義 |
| ローカルサーバ | 変更を即時プレビュー |

### 拡張/表現機能

| 機能 | 説明 |
|------|------|
| テーマ | Material 等で UI を拡張 |
| Plugin | 検索・多言語・図表機能を追加 |
| Markdown 拡張 | コードハイライトや警告ブロックを利用 |
| 目次生成 | セクション見出しを自動反映 |

### 運用連携機能

| 機能 | 説明 |
|------|------|
| Git 管理 | 文書差分レビューを実施しやすい |
| CI/CD 統合 | build と deploy を自動化可能 |
| 静的ホスティング連携 | GitHub Pages などへ配信可能 |
| 品質チェック | リンク切れや構文エラーを検知しやすい |

## インストールとセットアップ

公式URL:
- [MkDocs 公式サイト](https://www.mkdocs.org/)
- [MkDocs User Guide](https://www.mkdocs.org/user-guide/)
- [Deploying Docs](https://www.mkdocs.org/user-guide/deploying-your-docs/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

セットアップの要点:
1. Python 環境に `mkdocs` をインストールする。
2. `mkdocs new` で初期構成を作成する。
3. `mkdocs.yml` でナビゲーションを定義する。
4. CI で `mkdocs build` を実行して品質を担保する。

## 基本的な使い方

1. `docs/` 配下に Markdown を追加する。
2. `mkdocs.yml` でページ順を定義する。
3. `mkdocs serve` でローカルプレビューする。
4. `mkdocs build` で静的ファイルを生成する。
5. 生成物をホスティング環境へ公開する。

最小運用例:
- プレビュー: `mkdocs serve`
- ビルド: `mkdocs build`

## メリット

- 導入が軽量で、短期間で文書基盤を構築しやすい。
- Markdown 管理によりレビューと差分追跡がしやすい。
- テーマとプラグインで段階的に拡張しやすい。
- 静的サイトとして運用コストを抑えやすい。

## デメリット

- 大規模サイトでは情報設計を明確にしないと複雑化しやすい。
- 高度な UI カスタマイズは追加実装が必要。
- 動的機能が必要な場合は別基盤と組み合わせが必要。

## CI/CD での使用

PR 時に `mkdocs build` とリンクチェックを実施し、main マージ後に静的サイトへ自動デプロイする運用が有効である。これにより文書更新の反映遅れを減らしやすい。

## 他ツールとの比較

| ツール | 主な用途 | 特徴 |
|------|------|------|
| MkDocs | 技術ドキュメントサイト | Python ベースで軽量導入しやすい |
| Docusaurus | 技術ドキュメントサイト | バージョン管理と拡張性に強い |
| Sphinx | 技術文書生成 | Python API 文書連携に強い |
| GitBook | SaaS ドキュメント | 非技術ユーザーにも扱いやすい |

## ベストプラクティス

### 1. 情報構造を先に定義

- 章立てと分類ルールを先に決める。
- 文書テンプレートで書式を統一する。

### 2. 品質チェックを自動化

- CI で build とリンク検証を必須化する。
- Broken link を公開前に修正する。

### 3. 公開フローを標準化

- 配信先と公開手順を固定化する。
- リリースノートと文書更新を同期する。

## 公式ドキュメント

- 公式サイト: https://www.mkdocs.org/
- User Guide: https://www.mkdocs.org/user-guide/
- Deploying Docs: https://www.mkdocs.org/user-guide/deploying-your-docs/
- Material for MkDocs: https://squidfunk.github.io/mkdocs-material/

## まとめ

1. **実務利点1** : MkDocs は軽量な技術ドキュメント基盤を構築しやすい。
2. **実務利点2** : Markdown と Git 管理により、更新差分の追跡を進めやすい。
3. **情報共有** : CI/CD 連携により、公開品質と反映速度を両立しやすい。

