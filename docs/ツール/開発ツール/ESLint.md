# ESLint

## 概要

ESLintは、JavaScriptおよびTypeScriptのための静的コード解析ツールです。コードの品質問題、潜在的なバグ、スタイル違反を検出し、自動修正機能により一貫したコーディング規約を強制します。プラグインシステムにより、React、Vue、Node.js等のフレームワーク固有のルールを追加でき、CI/CDパイプラインに統合することで、チーム全体のコード品質を保証します。

## 主な機能

### 1. 静的解析
- **構文エラー**: JavaScriptの構文ミス検出
- **潜在的バグ**: 未定義変数、到達不能コード
- **ベストプラクティス**: 推奨コーディングパターン
- **型チェック**: TypeScript統合

### 2. 自動修正
- **--fix**: 自動修正可能なルール適用
- **スタイル統一**: インデント、引用符、セミコロン
- **インポート整理**: 未使用インポート削除

### 3. カスタマイズ可能
- **設定ファイル**: .eslintrc.js、.eslintrc.json
- **ルールカスタマイズ**: error、warn、off
- **共有設定**: eslint-config-airbnb等
- **カスタムルール**: プラグイン作成

### 4. フレームワーク対応
- **React**: eslint-plugin-react
- **Vue**: eslint-plugin-vue
- **TypeScript**: @typescript-eslint
- **Node.js**: eslint-plugin-node

### 5. エディタ統合
- **VS Code**: 拡張機能
- **IntelliJ IDEA**: プラグイン
- **Vim/Emacs**: 統合
- **リアルタイム**: 保存時自動チェック

### 6. CI/CD統合
- **GitHub Actions**: アクションとして実行
- **GitLab CI**: パイプライン統合
- **Pre-commit Hook**: コミット前チェック

## 利用方法

### インストール

```bash
# npm
npm install --save-dev eslint

# yarn
yarn add --dev eslint

# pnpm
pnpm add -D eslint

# 初期化
npx eslint --init
```

### 設定ファイル作成

```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
    '@typescript-eslint',
  ],
  rules: {
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'no-unused-vars': 'warn',
    'no-console': 'off',
  },
};
```

### 実行

```bash
# package.json
{
  "scripts": {
    "lint": "eslint src/**/*.{js,jsx,ts,tsx}",
    "lint:fix": "eslint src/**/*.{js,jsx,ts,tsx} --fix"
  }
}

# 実行
npm run lint
npm run lint:fix

# 特定ファイル
npx eslint src/index.js

# 自動修正
npx eslint src/index.js --fix
```

### TypeScript統合

```bash
# インストール
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

```javascript
// .eslintrc.js
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-unused-vars': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off',
  },
};
```

### React統合

```bash
# インストール
npm install --save-dev eslint-plugin-react eslint-plugin-react-hooks
```

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  plugins: ['react', 'react-hooks'],
  settings: {
    react: {
      version: 'detect',
    },
  },
  rules: {
    'react/prop-types': 'off',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
};
```

### Prettier統合

```bash
# インストール
npm install --save-dev eslint-config-prettier eslint-plugin-prettier
```

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:prettier/recommended', // 最後に追加
  ],
};
```

### 無視設定

```
# .eslintignore
node_modules
dist
build
coverage
*.min.js
*.bundle.js
```

### Pre-commit Hook

```bash
# husky + lint-staged インストール
npm install --save-dev husky lint-staged
npx husky-init
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "git add"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
npx lint-staged
```

### CI/CD統合

```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  eslint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **ESLint** | 🟢 無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **無料**: オープンソース、MIT License
2. **自動修正**: --fixで自動修正
3. **高度にカスタマイズ可能**: ルール細かく設定
4. **プラグインエコシステム**: React、Vue、TypeScript対応
5. **エディタ統合**: VS Code、IntelliJ等
6. **CI/CD統合**: GitHub Actions等
7. **Prettier統合**: フォーマッターと併用
8. **業界標準**: JavaScript開発の標準ツール
9. **アクティブ開発**: 継続的な改善
10. **大規模対応**: エンタープライズプロジェクトに対応

## デメリット

### ❌ 制約・課題

1. **設定複雑**: 初期設定が煩雑
2. **ルール多数**: 覚えるルールが多い
3. **パフォーマンス**: 大規模プロジェクトで遅延
4. **競合**: Prettierとルール競合の可能性
5. **学習曲線**: 初心者には難しい
6. **過剰な警告**: デフォルト設定で警告多数
7. **TypeScript**: 一部TypeScript固有機能は制限
8. **メンテナンス**: ルール設定の継続的メンテナンス必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Biome** | Rust製、高速 | ESLintより高速だが新しい |
| **Rome** | 統合ツール | ESLintよりオールインワン |
| **TSLint** | TypeScript専用（非推奨） | ESLintに統合済み |
| **Standard** | ゼロコンフィグ | ESLintより設定不要 |
| **XO** | Opinionated ESLint | ESLintより設定簡単 |

## 公式リンク

- **公式サイト**: [https://eslint.org/](https://eslint.org/)
- **ドキュメント**: [https://eslint.org/docs/](https://eslint.org/docs/)
- **ルール**: [https://eslint.org/docs/rules/](https://eslint.org/docs/rules/)
- **GitHub**: [https://github.com/eslint/eslint](https://github.com/eslint/eslint)
- **Playground**: [https://eslint.org/play/](https://eslint.org/play/)

## 関連ドキュメント

- [開発ツール一覧](../開発ツール/)
- [Prettier](./Prettier.md)
- [TypeScript](../プログラミング言語/TypeScript.md)
- [コード品質ベストプラクティス](../../best-practices/code-quality.md)

---

**カテゴリ**: 開発ツール  
**対象工程**: 実装  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
