# Express.js

## 概要

Express.jsは、Node.js向けのミニマルなWebアプリケーションフレームワークです。ルーティング、ミドルウェア、テンプレートエンジン、HTTPユーティリティにより、REST API、Webアプリケーション、マイクロサービスを構築します。シンプル、柔軟、MEAN/MERNスタック、Node.jsデファクトスタンダードで広く採用されています。

## 主な機能

### 1. ルーティング
- **HTTP メソッド**: GET、POST、PUT、DELETE
- **パスパラメータ**: /users/:id
- **クエリパラメータ**: ?name=value
- **ルートグループ**: Router

### 2. ミドルウェア
- **アプリケーションレベル**: app.use()
- **ルーターレベル**: router.use()
- **エラーハンドリング**: 4引数ミドルウェア
- **サードパーティ**: cors、helmet等

### 3. リクエスト・レスポンス
- **req.body**: リクエストボディ
- **req.params**: パスパラメータ
- **req.query**: クエリパラメータ
- **res.json()**: JSON レスポンス

### 4. テンプレート
- **EJS**: Embedded JavaScript
- **Pug**: テンプレートエンジン
- **Handlebars**: ロジックレステンプレート

## 利用方法

### インストール

```bash
mkdir my-app
cd my-app
npm init -y
npm install express
```

### 基本サーバー

```javascript
// app.js
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello, Express!')
})

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`)
})
```

```bash
node app.js
```

### ルーティング

```javascript
const express = require('express')
const app = express()

// GET
app.get('/users', (req, res) => {
  res.json([
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' }
  ])
})

// GET with path parameter
app.get('/users/:id', (req, res) => {
  const userId = req.params.id
  res.json({ id: userId, name: 'Alice' })
})

// POST
app.post('/users', (req, res) => {
  const user = req.body
  res.status(201).json({ id: 3, ...user })
})

// PUT
app.put('/users/:id', (req, res) => {
  const userId = req.params.id
  const user = req.body
  res.json({ id: userId, ...user })
})

// DELETE
app.delete('/users/:id', (req, res) => {
  res.status(204).send()
})

app.listen(3000)
```

### ミドルウェア

```javascript
const express = require('express')
const app = express()

// ビルトインミドルウェア
app.use(express.json())  // JSON パース
app.use(express.urlencoded({ extended: true }))  // URLエンコードパース
app.use(express.static('public'))  // 静的ファイル

// カスタムミドルウェア
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`)
  next()
})

// ルート固有ミドルウェア
function authenticate(req, res, next) {
  const token = req.headers.authorization
  if (token === 'secret-token') {
    next()
  } else {
    res.status(401).json({ error: 'Unauthorized' })
  }
}

app.get('/protected', authenticate, (req, res) => {
  res.json({ message: 'Protected resource' })
})

app.listen(3000)
```

### エラーハンドリング

```javascript
const express = require('express')
const app = express()

app.get('/error', (req, res, next) => {
  const error = new Error('Something went wrong!')
  error.status = 500
  next(error)
})

// エラーハンドリングミドルウェア（4引数）
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(err.status || 500).json({
    error: err.message
  })
})

app.listen(3000)
```

### REST API

```javascript
const express = require('express')
const app = express()

app.use(express.json())

let users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
]

// GET all users
app.get('/api/users', (req, res) => {
  res.json(users)
})

// GET user by ID
app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id))
  if (!user) return res.status(404).json({ error: 'User not found' })
  res.json(user)
})

// POST create user
app.post('/api/users', (req, res) => {
  const newUser = {
    id: users.length + 1,
    name: req.body.name,
    email: req.body.email
  }
  users.push(newUser)
  res.status(201).json(newUser)
})

// PUT update user
app.put('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id))
  if (!user) return res.status(404).json({ error: 'User not found' })

  user.name = req.body.name || user.name
  user.email = req.body.email || user.email
  res.json(user)
})

// DELETE user
app.delete('/api/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id))
  if (index === -1) return res.status(404).json({ error: 'User not found' })

  users.splice(index, 1)
  res.status(204).send()
})

app.listen(3000)
```

### Router

```javascript
// routes/users.js
const express = require('express')
const router = express.Router()

router.get('/', (req, res) => {
  res.json([{ id: 1, name: 'Alice' }])
})

router.get('/:id', (req, res) => {
  res.json({ id: req.params.id, name: 'Alice' })
})

router.post('/', (req, res) => {
  res.status(201).json(req.body)
})

module.exports = router

// app.js
const express = require('express')
const usersRouter = require('./routes/users')

const app = express()
app.use(express.json())

app.use('/api/users', usersRouter)

app.listen(3000)
```

### データベース統合（MongoDB）

```javascript
const express = require('express')
const mongoose = require('mongoose')

const app = express()
app.use(express.json())

// MongoDB接続
mongoose.connect('mongodb://localhost:27017/mydb')

// スキーマ
const userSchema = new mongoose.Schema({
  name: String,
  email: String
})

const User = mongoose.model('User', userSchema)

// REST API
app.get('/api/users', async (req, res) => {
  const users = await User.find()
  res.json(users)
})

app.post('/api/users', async (req, res) => {
  const user = new User(req.body)
  await user.save()
  res.status(201).json(user)
})

app.listen(3000)
```

### CORS設定

```bash
npm install cors
```

```javascript
const express = require('express')
const cors = require('cors')

const app = express()

// すべてのオリジン許可
app.use(cors())

// 特定オリジンのみ
app.use(cors({
  origin: 'http://localhost:5173',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true
}))

app.get('/api/data', (req, res) => {
  res.json({ message: 'CORS enabled' })
})

app.listen(3000)
```

### セキュリティ（Helmet）

```bash
npm install helmet
```

```javascript
const express = require('express')
const helmet = require('helmet')

const app = express()

app.use(helmet())  // セキュリティヘッダー設定

app.get('/', (req, res) => {
  res.send('Secured with Helmet')
})

app.listen(3000)
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Express.js** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **シンプル**: ミニマル設計
3. **柔軟**: 自由度高い
4. **エコシステム**: 豊富なミドルウェア
5. **MEAN/MERN**: スタック標準

## デメリット

1. **構造化**: 構造化不十分
2. **非同期エラー**: エラーハンドリング手動
3. **TypeScript**: TS対応手動
4. **代替**: NestJS、Fastify（新しい）

## 公式リンク

- **公式サイト**: [https://expressjs.com/](https://expressjs.com/)
- **ドキュメント**: [https://expressjs.com/en/4x/api.html](https://expressjs.com/en/4x/api.html)

## 関連ドキュメント

- [Webフレームワークツール一覧](../Webフレームワークツール/)
- [Node.js](../ランタイムツール/Node.js.md)
- [NestJS](./NestJS.md)

---

**カテゴリ**: Webフレームワークツール
**対象工程**: バックエンド開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
