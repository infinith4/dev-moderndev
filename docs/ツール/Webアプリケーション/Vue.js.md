# Vue.js

## 概要

Vue.jsは、プログレッシブJavaScriptフレームワークです。リアクティブデータバインディング、コンポーネントベース、Single File Component（SFC）、Composition API、Vue Router・Vuex統合により、インタラクティブなWebアプリケーション・SPAを実現します。Evan You開発、学習曲線緩やか、軽量で広く採用されています。

## 主な機能

### 1. リアクティブ
- **データバインディング**: 双方向バインディング
- **リアクティブ**: 自動更新
- **Computed**: 算出プロパティ
- **Watch**: 監視

### 2. コンポーネント
- **SFC**: .vueファイル
- **Props**: データ受け渡し
- **Emit**: イベント発火
- **Slots**: スロット

### 3. Composition API
- **setup()**: 新API
- **ref/reactive**: リアクティブ変数
- **computed**: 算出プロパティ
- **watch**: 監視

### 4. エコシステム
- **Vue Router**: ルーティング
- **Pinia/Vuex**: 状態管理
- **Nuxt.js**: SSR/SSG
- **Vite**: ビルドツール

## 利用方法

### プロジェクト作成

```bash
# Vue CLI
npm install -g @vue/cli
vue create my-app
cd my-app
npm run serve

# Vite（推奨）
npm create vite@latest my-app -- --template vue
cd my-app
npm install
npm run dev
```

### 基本コンポーネント

```vue
<!-- App.vue -->
<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: 'Hello, Vue!',
      count: 0
    }
  }
}
</script>

<style scoped>
#app {
  text-align: center;
}
</style>
```

### Composition API

```vue
<template>
  <div>
    <h1>{{ message }}</h1>
    <p>Count: {{ count }}</p>
    <button @click="increment">Increment</button>
    <p>Double: {{ double }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const message = ref('Hello, Vue 3!')
const count = ref(0)

const double = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>
```

### Props & Emit

```vue
<!-- Child.vue -->
<template>
  <div>
    <h2>{{ title }}</h2>
    <p>Count: {{ count }}</p>
    <button @click="handleClick">Increment</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  title: String,
  count: Number
})

const emit = defineEmits(['increment'])

function handleClick() {
  emit('increment')
}
</script>

<!-- Parent.vue -->
<template>
  <div>
    <Child :title="title" :count="count" @increment="count++" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Child from './Child.vue'

const title = ref('Counter')
const count = ref(0)
</script>
```

### v-if / v-for

```vue
<template>
  <div>
    <!-- 条件レンダリング -->
    <p v-if="isLoggedIn">Welcome back, {{ username }}!</p>
    <p v-else>Please log in.</p>

    <!-- リストレンダリング -->
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.name }} - {{ user.email }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isLoggedIn = ref(true)
const username = ref('Alice')

const users = ref([
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
  { id: 3, name: 'Charlie', email: 'charlie@example.com' }
])
</script>
```

### フォーム

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="form.name" placeholder="Name" />
    <input v-model="form.email" type="email" placeholder="Email" />
    <textarea v-model="form.message" placeholder="Message"></textarea>
    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  name: '',
  email: '',
  message: ''
})

function handleSubmit() {
  console.log('Submitted:', form)
  alert(`Name: ${form.name}, Email: ${form.email}`)
}
</script>
```

### Lifecycle Hooks

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const data = ref(null)

onMounted(async () => {
  console.log('Component mounted')
  const response = await fetch('/api/data')
  data.value = await response.json()
})

onUnmounted(() => {
  console.log('Component unmounted')
})
</script>
```

### Watch

```vue
<script setup>
import { ref, watch } from 'vue'

const userId = ref(1)
const user = ref(null)

watch(userId, async (newId) => {
  const response = await fetch(`/api/users/${newId}`)
  user.value = await response.json()
})
</script>
```

### Vue Router

```bash
npm install vue-router@4
```

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/users/:id', component: () => import('../views/UserDetail.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

```vue
<!-- App.vue -->
<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
  </nav>
  <router-view />
</template>
```

### Pinia（状態管理）

```bash
npm install pinia
```

```javascript
// stores/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  getters: {
    double: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    }
  }
})

// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
```

```vue
<!-- Component.vue -->
<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <p>Double: {{ counter.double }}</p>
    <button @click="counter.increment()">Increment</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>
```

### カスタムComposables

```javascript
// composables/useFetch.js
import { ref } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const loading = ref(true)
  const error = ref(null)

  async function fetchData() {
    try {
      loading.value = true
      const response = await fetch(url)
      data.value = await response.json()
    } catch (err) {
      error.value = err
    } finally {
      loading.value = false
    }
  }

  fetchData()

  return { data, loading, error }
}

// 使用例
<script setup>
import { useFetch } from '@/composables/useFetch'

const { data, loading, error } = useFetch('/api/users')
</script>
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Vue.js** | 🟢 無料 | オープンソース、MIT License |

## メリット

1. **無料**: オープンソース
2. **学習曲線**: 学習容易
3. **軽量**: 小さいバンドルサイズ
4. **SFC**: .vueファイル
5. **Composition API**: 柔軟な構成

## デメリット

1. **エコシステム**: React比較で小規模
2. **企業サポート**: 企業バックなし
3. **TypeScript**: TS対応改善中
4. **大規模**: 大規模アプリで課題

## 公式リンク

- **公式サイト**: [https://vuejs.org/](https://vuejs.org/)
- **ドキュメント**: [https://vuejs.org/guide/](https://vuejs.org/guide/)

## 関連ドキュメント

- [フロントエンドフレームワークツール一覧](../フロントエンドフレームワークツール/)
- [Nuxt.js](./Nuxt.js.md)
- [React](./React.md)

---

**カテゴリ**: フロントエンドフレームワークツール
**対象工程**: フロントエンド開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
