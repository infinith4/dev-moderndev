# Vite

## 概要

Viteは、次世代フロントエンドビルドツールです。ES Modules、esbuild（高速トランスパイル）、高速HMR（Hot Module Replacement）、開発サーバー、Rollupベースビルドにより、React、Vue、Svelte開発を高速化します。Evan You（Vue.js作者）開発、爆速起動、モダンWeb対応で急速に採用拡大中です。

## 主な機能

### 1. 開発サーバー
- **即座起動**: 高速起動
- **HMR**: 高速リロード
- **ES Modules**: ネイティブESM
- **esbuild**: 高速トランスパイル

### 2. ビルド
- **Rollup**: 本番ビルド
- **Tree Shaking**: 不要コード削除
- **コード分割**: 自動分割
- **最適化**: 圧縮、ハッシュ

### 3. プラグイン
- **React**: @vitejs/plugin-react
- **Vue**: @vitejs/plugin-vue
- **Svelte**: @sveltejs/vite-plugin-svelte
- **TypeScript**: ネイティブサポート

### 4. モダン
- **CSS**: PostCSS、Sass、Less
- **Assets**: 画像、フォント
- **JSON**: JSON import
- **WebAssembly**: WASM

## 利用方法

### プロジェクト作成

```bash
# Viteプロジェクト作成
npm create vite@latest my-app

# フレームワーク選択
# - vanilla
# - vue
# - react
# - preact
# - lit
# - svelte

cd my-app
npm install
npm run dev
```

### React

```bash
# Reactプロジェクト
npm create vite@latest my-react-app -- --template react

cd my-react-app
npm install
npm run dev  # http://localhost:5173
```

```javascript
// src/App.jsx
import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <h1>Vite + React</h1>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
    </div>
  )
}

export default App
```

### Vue

```bash
# Vueプロジェクト
npm create vite@latest my-vue-app -- --template vue

cd my-vue-app
npm install
npm run dev
```

```vue
<!-- src/App.vue -->
<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div class="app">
    <h1>Vite + Vue</h1>
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<style scoped>
.app {
  text-align: center;
}
</style>
```

### vite.config.js

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  },

  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom']
        }
      }
    }
  },

  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
```

### 環境変数

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App
```

```javascript
// 使用
console.log(import.meta.env.VITE_API_URL)
console.log(import.meta.env.VITE_APP_TITLE)
```

### TypeScript

```bash
# TypeScript テンプレート
npm create vite@latest my-ts-app -- --template react-ts

cd my-ts-app
npm install
npm run dev
```

```typescript
// src/App.tsx
import { useState } from 'react'

interface User {
  id: number
  name: string
}

function App() {
  const [user, setUser] = useState<User>({ id: 1, name: 'Alice' })

  return (
    <div>
      <h1>User: {user.name}</h1>
    </div>
  )
}

export default App
```

### CSS処理

```bash
# Sass インストール
npm install -D sass

# PostCSS プラグイン
npm install -D autoprefixer
```

```javascript
// vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    },
    postcss: {
      plugins: [
        require('autoprefixer')
      ]
    }
  }
})
```

### ビルド

```bash
# 開発
npm run dev

# ビルド
npm run build

# プレビュー
npm run preview

# 型チェック（TypeScript）
npm run type-check
```

### Docker

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### カスタムプラグイン

```javascript
// vite-plugin-custom.js
export default function customPlugin() {
  return {
    name: 'vite-plugin-custom',

    // 開発サーバー設定
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        console.log(`[custom] ${req.url}`)
        next()
      })
    },

    // トランスフォーム
    transform(code, id) {
      if (id.endsWith('.custom')) {
        return {
          code: `export default ${JSON.stringify(code)}`,
          map: null
        }
      }
    }
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Vite** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **爆速**: 高速起動・HMR
3. **モダン**: ES Modules、esbuild
4. **シンプル**: 簡単設定
5. **フレームワーク**: React、Vue、Svelte対応

## デメリット

1. **ブラウザ**: 古いブラウザ非対応
2. **エコシステム**: Webpack比較で小規模
3. **成熟度**: 比較的新しい
4. **プラグイン**: プラグイン少ない

## 公式リンク

- **公式サイト**: [https://vitejs.dev/](https://vitejs.dev/)
- **GitHub**: [https://github.com/vitejs/vite](https://github.com/vitejs/vite)

## 関連ドキュメント

- [ビルドツール一覧](../ビルドツール/)
- [Webpack](./Webpack.md)
- [Rollup](./Rollup.md)

---

**カテゴリ**: ビルドツール
**対象工程**: フロントエンドビルド
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
