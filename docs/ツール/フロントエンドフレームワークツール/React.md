# React

## 概要

Reactは、Facebook製のUI構築JavaScriptライブラリです。コンポーネントベース、仮想DOM、宣言的UI、Hooks（useState、useEffect）により、インタラクティブなWebアプリケーション・SPAを実現します。大規模エコシステム、React Native（モバイル）、Next.js（SSR）で広く採用されています。

## 主な機能

### 1. コンポーネント
- **関数コンポーネント**: 関数ベース
- **JSX**: HTML-like構文
- **Props**: データ受け渡し
- **Children**: 子要素

### 2. Hooks
- **useState**: 状態管理
- **useEffect**: 副作用
- **useContext**: コンテキスト
- **useMemo/useCallback**: メモ化

### 3. 仮想DOM
- **差分検出**: 効率的更新
- **再レンダリング**: 最小限更新
- **Reconciliation**: 調整アルゴリズム

### 4. エコシステム
- **React Router**: ルーティング
- **Redux/Zustand**: 状態管理
- **Next.js**: SSR/SSG
- **React Native**: モバイル

## 利用方法

### プロジェクト作成

```bash
# Create React App
npx create-react-app my-app
cd my-app
npm start

# Vite（推奨）
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

### 基本コンポーネント

```javascript
// App.jsx
import React from 'react'

function App() {
  return (
    <div className="app">
      <h1>Hello, React!</h1>
      <p>Welcome to React application.</p>
    </div>
  )
}

export default App
```

### Props

```javascript
// Greeting.jsx
function Greeting({ name, age }) {
  return (
    <div>
      <h2>Hello, {name}!</h2>
      <p>Age: {age}</p>
    </div>
  )
}

// App.jsx
function App() {
  return (
    <div>
      <Greeting name="Alice" age={30} />
      <Greeting name="Bob" age={25} />
    </div>
  )
}
```

### useState（状態管理）

```javascript
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  )
}
```

### useEffect（副作用）

```javascript
import { useState, useEffect } from 'react'

function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchUser() {
      setLoading(true)
      const response = await fetch(`/api/users/${userId}`)
      const data = await response.json()
      setUser(data)
      setLoading(false)
    }

    fetchUser()
  }, [userId])  // userIdが変わったら再実行

  if (loading) return <p>Loading...</p>
  if (!user) return <p>User not found</p>

  return (
    <div>
      <h2>{user.name}</h2>
      <p>Email: {user.email}</p>
    </div>
  )
}
```

### イベントハンドリング

```javascript
function Form() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Submitted:', { name, email })
    alert(`Name: ${name}, Email: ${email}`)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Submit</button>
    </form>
  )
}
```

### 条件レンダリング

```javascript
function LoginStatus({ isLoggedIn, username }) {
  return (
    <div>
      {isLoggedIn ? (
        <p>Welcome back, {username}!</p>
      ) : (
        <p>Please log in.</p>
      )}
    </div>
  )
}

// && 演算子
function Notification({ message }) {
  return (
    <div>
      {message && <div className="alert">{message}</div>}
    </div>
  )
}
```

### リストレンダリング

```javascript
function UserList({ users }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          {user.name} - {user.email}
        </li>
      ))}
    </ul>
  )
}

function App() {
  const users = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' },
    { id: 3, name: 'Charlie', email: 'charlie@example.com' }
  ]

  return <UserList users={users} />
}
```

### useContext（グローバル状態）

```javascript
import { createContext, useContext, useState } from 'react'

// コンテキスト作成
const ThemeContext = createContext()

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// コンテキスト使用
function ThemeButton() {
  const { theme, setTheme } = useContext(ThemeContext)

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  )
}

// App
function App() {
  return (
    <ThemeProvider>
      <ThemeButton />
    </ThemeProvider>
  )
}
```

### カスタムHooks

```javascript
// useFetch.js
function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)
        const response = await fetch(url)
        const json = await response.json()
        setData(json)
      } catch (err) {
        setError(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error }
}

// 使用例
function Users() {
  const { data, loading, error } = useFetch('/api/users')

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error.message}</p>

  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

### React Router

```bash
npm install react-router-dom
```

```javascript
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/users">Users</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<Users />} />
        <Route path="/users/:id" element={<UserDetail />} />
      </Routes>
    </BrowserRouter>
  )
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **React** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **大規模エコシステム**: 豊富なライブラリ
3. **コンポーネント**: 再利用可能
4. **仮想DOM**: 高速レンダリング
5. **React Native**: モバイル対応

## デメリット

1. **学習曲線**: JSX、Hooks学習
2. **エコシステム**: 選択肢多く複雑
3. **SEO**: CSRでSEO課題
4. **ビルドサイズ**: バンドルサイズ大

## 公式リンク

- **公式サイト**: [https://react.dev/](https://react.dev/)
- **ドキュメント**: [https://react.dev/learn](https://react.dev/learn)

## 関連ドキュメント

- [フロントエンドフレームワークツール一覧](../フロントエンドフレームワークツール/)
- [Next.js](./Next.js.md)
- [Vue.js](./Vue.js.md)

---

**カテゴリ**: フロントエンドフレームワークツール
**対象工程**: フロントエンド開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
