# Babel

## 概要

Babelは、JavaScriptトランスパイラです。ES6+→ES5変換、JSX（React）、TypeScript、プラグインアーキテクチャにより、最新JavaScript構文を古いブラウザ向けに変換します。@babel/preset-env（ターゲットブラウザ自動対応）、ポリフィル、Webpack/Rollup統合で広く採用されています。

## 主な機能

### 1. トランスパイル
- **ES6+**: アロー関数、class、async/await
- **JSX**: React JSX変換
- **TypeScript**: TS→JS
- **Flow**: Flow型削除

### 2. Presets
- **@babel/preset-env**: ターゲットブラウザ対応
- **@babel/preset-react**: React JSX
- **@babel/preset-typescript**: TypeScript
- **カスタムPreset**: 独自プリセット

### 3. Plugins
- **Transform**: 構文変換
- **Syntax**: 構文解析
- **Proposal**: Stage 0-3提案
- **カスタムPlugin**: 独自プラグイン

### 4. ポリフィル
- **core-js**: ポリフィル
- **regenerator-runtime**: async/await
- **自動注入**: 使用箇所のみ

## 利用方法

### インストール

```bash
npm install --save-dev @babel/core @babel/cli @babel/preset-env
```

### 基本設定

```javascript
// babel.config.json
{
  "presets": [
    [
      "@babel/preset-env",
      {
        "targets": {
          "browsers": [">0.25%", "not dead"]
        },
        "useBuiltIns": "usage",
        "corejs": 3
      }
    ]
  ]
}
```

### React

```bash
npm install --save-dev @babel/preset-react
```

```javascript
// babel.config.json
{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ]
}
```

```javascript
// src/App.jsx
import React from 'react'

function App() {
  return (
    <div className="app">
      <h1>Hello, React!</h1>
    </div>
  )
}

export default App
```

### TypeScript

```bash
npm install --save-dev @babel/preset-typescript
```

```javascript
// babel.config.json
{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-typescript"
  ]
}
```

```typescript
// src/index.ts
interface User {
  id: number
  name: string
}

const user: User = { id: 1, name: 'Alice' }
console.log(user.name)
```

### CLI実行

```bash
# ファイル変換
npx babel src/index.js -o dist/index.js

# ディレクトリ変換
npx babel src --out-dir dist

# Watch モード
npx babel src --watch --out-dir dist

# Source Maps
npx babel src --out-dir dist --source-maps
```

### Webpack統合

```bash
npm install --save-dev babel-loader
```

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      }
    ]
  }
}
```

### Rollup統合

```bash
npm install --save-dev @rollup/plugin-babel
```

```javascript
// rollup.config.js
import babel from '@rollup/plugin-babel'

export default {
  input: 'src/index.js',
  output: {
    file: 'dist/bundle.js',
    format: 'cjs'
  },
  plugins: [
    babel({
      babelHelpers: 'bundled',
      exclude: 'node_modules/**'
    })
  ]
}
```

### プラグイン

```bash
npm install --save-dev @babel/plugin-proposal-class-properties
```

```javascript
// babel.config.json
{
  "presets": ["@babel/preset-env"],
  "plugins": [
    "@babel/plugin-proposal-class-properties"
  ]
}
```

```javascript
// src/index.js
class User {
  // クラスプロパティ（Stage 3）
  name = 'Alice'

  greet = () => {
    console.log(`Hello, ${this.name}`)
  }
}

const user = new User()
user.greet()
```

### ポリフィル（core-js）

```bash
npm install core-js regenerator-runtime
```

```javascript
// babel.config.json
{
  "presets": [
    [
      "@babel/preset-env",
      {
        "useBuiltIns": "usage",
        "corejs": 3
      }
    ]
  ]
}
```

```javascript
// src/index.js
// Promise、Array.from等のポリフィルが自動注入
const promise = Promise.resolve(42)
const array = Array.from([1, 2, 3])

async function fetchData() {
  const response = await fetch('/api/data')
  return response.json()
}
```

### カスタムプラグイン

```javascript
// babel-plugin-custom.js
module.exports = function() {
  return {
    visitor: {
      Identifier(path) {
        if (path.node.name === 'foo') {
          path.node.name = 'bar'
        }
      }
    }
  }
}
```

```javascript
// babel.config.json
{
  "plugins": ["./babel-plugin-custom.js"]
}
```

### browserslist

```json
// package.json
{
  "browserslist": [
    ">0.2%",
    "not dead",
    "not op_mini all",
    "ie >= 11"
  ]
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Babel** | 🟢 無料 | オープンソース、MIT License |

## メリット

1. **無料**: オープンソース
2. **互換性**: 古いブラウザ対応
3. **プラグイン**: 豊富なプラグイン
4. **React/TS**: JSX、TypeScript対応
5. **エコシステム**: Webpack、Rollup統合

## デメリット

1. **ビルド遅延**: トランスパイル時間
2. **設定複雑**: プラグイン設定複雑
3. **バンドルサイズ**: ポリフィルサイズ増
4. **代替**: SWC、esbuild（高速）

## 公式リンク

- **公式サイト**: [https://babeljs.io/](https://babeljs.io/)
- **ドキュメント**: [https://babeljs.io/docs/](https://babeljs.io/docs/)

## 関連ドキュメント

- [トランスパイラツール一覧](../トランスパイラツール/)
- [TypeScript](./TypeScript.md)
- [SWC](./SWC.md)

---

**カテゴリ**: トランスパイラツール
**対象工程**: JavaScript トランスパイル
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
