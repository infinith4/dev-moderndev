# npm

## 概要

npm は Node.js 標準のパッケージ管理ツールである。`package.json` と `package-lock.json` を中心に依存関係、スクリプト実行、パッケージ公開を管理し、JavaScript/TypeScript 開発の再現性と効率を高める。

## 料金

| プラン | 内容 |
|------|------|
| npm CLI | 無料（OSS） |
| npm Public Registry | 公開パッケージは無料で利用可能 |
| npm Teams/Enterprise | 組織向けの有償機能を提供 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Node.js 標準同梱 | 追加導入の手間が少ない |
| 巨大エコシステム | 多数の公開パッケージを利用可能 |
| lockfile 管理 | 依存バージョンを固定して再現性を確保 |
| scripts 実行 | ビルド・テスト・lint を統一実行 |
| workspaces 対応 | monorepo 運用を標準機能で支援 |
| レジストリ連携 | 公開/社内レジストリを使い分け可能 |

## 主な機能

### 依存関係管理機能

| 機能 | 説明 |
|------|------|
| `npm install` | 依存パッケージを追加・解決 |
| `npm ci` | lockfile ベースで高速かつ厳密に復元 |
| `npm update` | 依存パッケージを更新 |
| `npm uninstall` | 不要パッケージを削除 |

### 実行/開発支援機能

| 機能 | 説明 |
|------|------|
| npm scripts | 開発タスクを `package.json` に集約 |
| lifecycle hooks | pre/post フックで処理を自動化 |
| `npm run` | 環境差分を吸収してコマンド実行 |
| workspaces | 複数パッケージを一括管理 |

### 配布/運用機能

| 機能 | 説明 |
|------|------|
| `npm publish` | パッケージ公開 |
| `.npmrc` | レジストリと認証情報を設定 |
| `npm audit` | 脆弱性情報を確認 |
| `npm outdated` | 更新候補を可視化 |

## インストールとセットアップ

公式URL:
- [npm 公式サイト](https://www.npmjs.com/)
- [npm Docs](https://docs.npmjs.com/)
- [npm CLI](https://docs.npmjs.com/cli/v10/commands)

セットアップの要点:
1. Node.js をインストールし、`node -v` と `npm -v` を確認する。
2. `npm init` で `package.json` を作成する。
3. チーム運用では `package-lock.json` を必ずコミットする。
4. 社内レジストリ利用時は `.npmrc` と認証を整備する。

## 基本的な使い方

1. `npm init -y` でプロジェクト設定を作成する。
2. `npm install <package>` で依存を追加する。
3. `npm run test` や `npm run build` を scripts から実行する。
4. CI では `npm ci` を使って依存を復元する。
5. ライブラリ配布時は `npm version` 後に `npm publish` する。

最小運用例:
- 開発依存: `npm install -D eslint jest`
- CI: `npm ci && npm test`

## メリット

- Node.js 開発で標準的に利用でき、導入しやすい。
- lockfile により環境差分を抑えやすい。
- scripts と連携して開発手順を統一しやすい。
- 公開・社内パッケージ配布の両方に対応しやすい。

## デメリット

- 大規模依存ではインストール時間が長くなりやすい。
- 依存ツリーが複雑化すると調査コストが上がる。
- レジストリやトークン管理を誤ると供給リスクが発生する。

## CI/CD での使用

CI では `npm ci` を標準にして、lockfile どおりに依存を復元する運用が推奨される。リリース時はタグやバージョン規約と連携して `npm publish` を自動化すると、配布の再現性を保ちやすい。

## 他ツールとの比較

| ツール | 強み | 特徴 |
|------|------|------|
| npm | 標準性 | Node.js 同梱で導入しやすい |
| Yarn | 速度/機能 | ワークスペース運用と安定性に強み |
| pnpm | 省容量 | 重複依存を抑えて高速化しやすい |
| Bun | 高速実行 | ランタイム統合で高速な開発体験 |

## ベストプラクティス

### 1. lockfile を運用の基準にする

- `package-lock.json` を必ずバージョン管理する。
- CI では `npm ci` を固定で使う。

### 2. scripts を標準化する

- `lint/test/build` のコマンド名を統一する。
- ローカルと CI の実行手順を一致させる。

### 3. セキュリティ運用を継続する

- `npm audit` の定期実行を組み込む。
- 依存更新ポリシー（頻度、承認）を決める。

## 公式ドキュメント

- 公式サイト: https://www.npmjs.com/
- Docs: https://docs.npmjs.com/
- CLI Commands: https://docs.npmjs.com/cli/v10/commands

## まとめ

1. ** 標準基盤 ** : npm は Node.js 開発の標準パッケージ管理として導入しやすい。
2. ** 再現性 ** : lockfile と `npm ci` を徹底すると、ビルド再現性を高めやすい。
3. ** 一貫性 ** : scripts と公開運用を整備することで、開発から配布まで一貫管理しやすい。
