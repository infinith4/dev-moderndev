# npm

## 概要

npmは、Node.js標準のパッケージ管理ツールです。package.json、npm registry（200万+パッケージ）、バージョン管理、依存関係解決、スクリプト実行により、JavaScript/Node.jsプロジェクトを効率化します。Node.js同梱、世界最大のパッケージレジストリで広く使用されています。

## 主な機能

### 1. パッケージ管理
- **インストール**: npm install
- **削除**: npm uninstall
- **更新**: npm update
- **検索**: npm search

### 2. バージョン管理
- **セマンティックバージョニング**: x.y.z
- **package-lock.json**: 依存関係ロック
- **バージョン範囲**: ^, ~, >=
- **npmレジストリ**: 公開・プライベート

### 3. スクリプト
- **npm scripts**: タスク実行
- **ライフサイクル**: pre/post hooks
- **カスタムスクリプト**: ビルド、テスト等
- **環境変数**: プロセス間共有

### 4. ワークスペース
- **monorepo**: 複数パッケージ管理
- **共有依存**: 重複排除
- **ローカルリンク**: npm link
- **npm workspaces**: 公式サポート

## 利用方法

### インストール

```bash
# Node.jsインストール時に自動インストール
node --version
npm --version

# npm更新
npm install -g npm
```

### プロジェクト初期化

```bash
# package.json作成
npm init

# デフォルト設定で作成
npm init -y

# package.json
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

### パッケージインストール

```bash
# ローカルインストール（production依存）
npm install express
npm install axios lodash

# 開発依存
npm install --save-dev jest eslint

# グローバルインストール
npm install -g typescript

# 特定バージョン
npm install express@4.18.0

# 最新版
npm install express@latest

# すべての依存関係インストール
npm install
```

### パッケージ管理

```bash
# パッケージ削除
npm uninstall express

# パッケージ更新
npm update express

# 全パッケージ更新
npm update

# パッケージ一覧
npm list
npm list --depth=0

# グローバルパッケージ一覧
npm list -g --depth=0

# パッケージ情報
npm show express
npm view express version

# 古いパッケージ確認
npm outdated
```

### package.json

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "My application",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "build": "webpack --mode production",
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "dependencies": {
    "express": "^4.18.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "nodemon": "^3.0.0"
  },
  "keywords": ["node", "express"],
  "author": "Your Name",
  "license": "MIT"
}
```

### npmスクリプト

```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "build": "webpack --mode production",
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "clean": "rm -rf dist",
    "prebuild": "npm run clean",
    "postbuild": "echo Build complete!"
  }
}
```

```bash
# スクリプト実行
npm run dev
npm test
npm start

# 環境変数渡し
NODE_ENV=production npm start
```

### セマンティックバージョニング

```json
{
  "dependencies": {
    "express": "4.18.0",      // 完全一致
    "axios": "^1.0.0",        // 1.x.x（メジャー固定）
    "lodash": "~4.17.0",      // 4.17.x（マイナー固定）
    "react": ">=18.0.0",      // 18.0.0以上
    "vue": "18.0.0 - 18.2.0"  // 範囲指定
  }
}
```

### package-lock.json

```bash
# 依存関係固定
npm install  # package-lock.json生成

# CI/CD
npm ci  # package-lock.jsonから厳密にインストール（高速）

# package-lock.json更新
npm install express@latest
```

### npmスクリプトフック

```json
{
  "scripts": {
    "pretest": "npm run lint",
    "test": "jest",
    "posttest": "echo Tests complete!",

    "prebuild": "npm run clean",
    "build": "webpack",
    "postbuild": "npm run copy-assets"
  }
}
```

### ワークスペース（monorepo）

```json
// package.json（ルート）
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*"
  ]
}
```

```
my-monorepo/
├── package.json
├── packages/
│   ├── web/
│   │   └── package.json
│   ├── api/
│   │   └── package.json
│   └── shared/
│       └── package.json
```

```bash
# ワークスペース全体依存インストール
npm install

# 特定ワークスペースで実行
npm run build --workspace=packages/web

# 全ワークスペースで実行
npm run test --workspaces
```

### プライベートレジストリ

```bash
# .npmrcファイル
registry=https://registry.npmjs.org/
@mycompany:registry=https://npm.mycompany.com/

# スコープ付きパッケージ
npm install @mycompany/my-package

# 認証
npm login --registry=https://npm.mycompany.com/
```

### パッケージ公開

```bash
# npmアカウント作成
npm adduser

# パッケージ公開
npm publish

# スコープ付き
npm publish --access public

# バージョンアップ
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0

npm publish
```

### npmキャッシュ

```bash
# キャッシュ確認
npm cache verify

# キャッシュクリア
npm cache clean --force

# キャッシュパス
npm config get cache
```

### 設定

```bash
# 設定確認
npm config list

# 設定取得
npm config get registry

# 設定設定
npm config set registry https://registry.npmjs.org/

# 初期設定
npm config set init-author-name "Your Name"
npm config set init-license "MIT"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **npm CLI** |  無料 | オープンソース |
| **npm registry** |  無料 | 公開パッケージ無料 |
| **npm Teams** |  $7/ユーザー/月 | プライベートパッケージ無制限 |
| **npm Enterprise** |  要問い合わせ | オンプレミスレジストリ |

## メリット

1. **無料**: オープンソース
2. **豊富なパッケージ**: 200万+パッケージ
3. **Node.js統合**: デフォルト搭載
4. **簡単**: シンプルなコマンド
5. **エコシステム**: 巨大コミュニティ

## デメリット

1. **速度**: yarn/pnpmより遅い
2. **依存解決**: 複雑な依存で問題
3. **ディスク**: node_modules肥大化
4. **セキュリティ**: 脆弱性リスク

## 公式リンク

- **公式サイト**: [https://www.npmjs.com/](https://www.npmjs.com/)
- **ドキュメント**: [https://docs.npmjs.com/](https://docs.npmjs.com/)

## 関連ドキュメント

- [パッケージ管理ツール一覧](../パッケージ管理ツール/)
- [Node.js](../ランタイムツール/Node.js.md)
- [Yarn](./Yarn.md)

---

**カテゴリ**: パッケージ管理ツール
**対象工程**: JavaScript/Node.js開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0

