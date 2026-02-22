# Prettier

## 概要

Prettierは、「妥協なし」（Opinionated）のコードフォーマッターです。JavaScript、TypeScript、HTML、CSS、JSON、Markdown等の多様な言語をサポートし、一貫したコードスタイルを自動的に適用します。設定をほとんど必要とせず、チーム全体で統一されたフォーマットを強制することで、コードレビューでのスタイル議論を排除します。

## 主な機能

### 1. 多言語対応
- **JavaScript/TypeScript**: ES2024、JSX、TSX
- **HTML/CSS**: SCSS、Less
- **JSON/YAML**: 設定ファイル
- **Markdown**: ドキュメント
- **GraphQL**: クエリ
- **その他**: Vue、Angular、Svelte

### 2. 自動フォーマット
- コード整形
- インデント統一
- 行長制限
- セミコロン・カンマ追加/削除
- 引用符統一

### 3. エディタ統合
- VS Code拡張
- JetBrains IDE
- Vim/Emacs
- Atom、Sublime Text
- 保存時自動フォーマット

### 4. Git統合
- Pre-commitフック
- lint-staged統合
- CI/CDチェック

### 5. カスタマイズ最小限
- 設定項目は意図的に少ない
- チーム間の議論を削減
- 「Prettier Way」を採用

## 利用方法

### インストール

```bash
# npm
npm install --save-dev prettier

# yarn
yarn add --dev prettier

# pnpm
pnpm add -D prettier
```

### 設定ファイル作成

```javascript
// .prettierrc.js
module.exports = {
  semi: true,                // セミコロン追加
  trailingComma: 'es5',      // ES5互換のカンマ
  singleQuote: true,         // シングルクォート使用
  printWidth: 80,            // 行長80文字
  tabWidth: 2,               // インデント2スペース
  useTabs: false,            // スペース使用
  arrowParens: 'always',     // アロー関数の括弧
  endOfLine: 'lf',           // 改行コードLF
}
```

```json
// .prettierrc.json（代替形式）
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### 無視ファイル設定

```
# .prettierignore
node_modules
dist
build
coverage
*.min.js
*.min.css
package-lock.json
yarn.lock
```

### 実行

```bash
# package.json
{
  "scripts": {
    "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,json,css,md}\"",
    "format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx,json,css,md}\""
  }
}

# 実行
npm run format        # フォーマット実行
npm run format:check  # チェックのみ（CI用）

# CLIで直接実行
npx prettier --write src/index.js
npx prettier --check "src/**/*.js"
```

### VS Code統合

```json
// .vscode/settings.json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### ESLint統合

```bash
# eslint-config-prettierインストール（ESLintとの競合回避）
npm install --save-dev eslint-config-prettier
```

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'prettier', // 最後に追加（Prettierのルールを優先）
  ],
}
```

### Pre-commitフック（lint-staged + husky）

```bash
# インストール
npm install --save-dev husky lint-staged

# huskyセットアップ
npx husky-init
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,json,css,md}": [
      "prettier --write",
      "git add"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

## CI/CD統合

### GitHub Actions

```yaml
name: Code Format Check

on: [push, pull_request]

jobs:
  prettier:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Check code formatting
        run: npm run format:check
```

## 料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Prettier** | 🟢 無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **設定不要**: ほぼゼロコンフィグで利用開始
2. **一貫性**: チーム全体で統一されたスタイル
3. **議論削減**: スタイル議論をコードレビューから排除
4. **多言語対応**: JS/TS/HTML/CSS/JSON/Markdown等
5. **エディタ統合**: 保存時自動フォーマット
6. **高速**: 大規模コードベースでも高速
7. **無料**: 無料、MIT License
8. **ESLint統合**: 競合せずに併用可能
9. **Git統合**: Pre-commitフックで強制
10. **コミュニティ**: 広く採用、豊富な情報

## デメリット

### ❌ 制約・課題

1. **カスタマイズ限定**: 設定項目が少ない
2. **Opinionated**: Prettierのスタイルに従う必要
3. **既存コード**: 大量のフォーマット変更が発生
4. **Git履歴**: 一括フォーマットでコミット履歴が汚れる
5. **言語サポート**: 一部言語は非対応
6. **スタイル固定**: 好みのスタイルに変更困難
7. **破壊的変更**: バージョンアップでフォーマット変更の可能性
8. **ビルド時間**: 大規模プロジェクトでは実行時間増加

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **ESLint (--fix)**: | リンター+フォーマット | Prettierほど厳格ではない |
| **Beautify** | 古典的フォーマッター | Prettierより設定柔軟だが非推奨 |
| **Standard** | ゼロコンフィグJS | Prettierと類似だがJS専用 |
| **dprint** | Rust製、高速 | Prettierより高速だが成熟度低い |
| **Biome** | Rust製、リンター+フォーマッター | Prettierより高速だが新しい |

## 公式リンク

- **公式サイト**: [https://prettier.io/](https://prettier.io/)
- **Playground**: [https://prettier.io/playground/](https://prettier.io/playground/)
- **ドキュメント**: [https://prettier.io/docs/](https://prettier.io/docs/)
- **GitHub**: [https://github.com/prettier/prettier](https://github.com/prettier/prettier)
- **VS Code拡張**: [https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

## 関連ドキュメント

- [開発ツール一覧](../開発ツール/)
- [ESLint](./ESLint.md)
- [コードフォーマットベストプラクティス](../../best-practices/code-formatting.md)
- [Prettierセットアップガイド](../../best-practices/prettier-setup.md)

---

**カテゴリ**: 開発ツール  
**対象工程**: 実装  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
