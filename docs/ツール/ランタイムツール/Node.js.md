# Node.js

## 概要

Node.jsは、Chrome V8 JavaScript エンジンベースのJavaScriptランタイム環境です。非同期I/O、イベント駆動、npm（パッケージマネージャー）、シングルスレッド、高パフォーマンスにより、サーバーサイド・CLI・ツール開発を実現します。Ryan Dahl開発、MEAN/MERNスタック、フロントエンド/バックエンド統一言語で広く採用されています。

## 主な機能

### 1. 非同期I/O
- **イベント駆動**: イベントループ
- **非ブロッキング**: 非同期処理
- **コールバック**: コールバック関数
- **Promise/async**: Promise、async/await

### 2. npm
- **パッケージマネージャー**: 世界最大
- **package.json**: 依存関係管理
- **npm scripts**: スクリプト実行
- **npx**: パッケージ実行

### 3. 組み込みモジュール
- **fs**: ファイルシステム
- **http**: HTTPサーバー
- **path**: パス操作
- **crypto**: 暗号化

### 4. エコシステム
- **Express**: Webフレームワーク
- **Socket.io**: WebSocket
- **Sequelize**: ORM
- **Jest**: テストフレームワーク

## 利用方法

### インストール

```bash
# macOS (Homebrew)
brew install node

# Windows (Chocolatey)
choco install nodejs

# nvm（Node Version Manager）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# バージョン確認
node -v
npm -v
```

### 基本プログラム

```javascript
// hello.js
console.log('Hello, Node.js!')

// 実行
// node hello.js
```

### HTTPサーバー

```javascript
// server.js
const http = require('http')

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('Hello, World!\n')
})

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/')
})

// 実行
// node server.js
```

### ファイルシステム

```javascript
// file.js
const fs = require('fs')

// 同期読み込み
const data = fs.readFileSync('file.txt', 'utf8')
console.log(data)

// 非同期読み込み
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) throw err
  console.log(data)
})

// Promise
const fsPromises = require('fs').promises

async function readFile() {
  try {
    const data = await fsPromises.readFile('file.txt', 'utf8')
    console.log(data)
  } catch (err) {
    console.error(err)
  }
}

// ファイル書き込み
fs.writeFile('output.txt', 'Hello, Node.js!', (err) => {
  if (err) throw err
  console.log('File written!')
})
```

### npmパッケージ管理

```bash
# プロジェクト初期化
npm init -y

# パッケージインストール
npm install express
npm install -D nodemon jest

# グローバルインストール
npm install -g typescript

# パッケージ削除
npm uninstall express

# パッケージ更新
npm update

# 依存関係確認
npm list
npm outdated
```

### package.json

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "My Node.js app",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "tsc"
  },
  "keywords": ["node", "express"],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^2.0.20",
    "jest": "^29.5.0"
  }
}
```

### Expressサーバー

```javascript
// app.js
const express = require('express')
const app = express()

app.use(express.json())

app.get('/', (req, res) => {
  res.send('Hello, Express!')
})

app.get('/api/users', (req, res) => {
  res.json([
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' }
  ])
})

app.post('/api/users', (req, res) => {
  const user = req.body
  res.status(201).json(user)
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000')
})
```

### 非同期処理

```javascript
// callback.js
function fetchData(callback) {
  setTimeout(() => {
    callback(null, { data: 'result' })
  }, 1000)
}

fetchData((err, data) => {
  if (err) return console.error(err)
  console.log(data)
})

// Promise
function fetchDataPromise() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({ data: 'result' })
    }, 1000)
  })
}

fetchDataPromise()
  .then(data => console.log(data))
  .catch(err => console.error(err))

// async/await
async function fetchDataAsync() {
  try {
    const data = await fetchDataPromise()
    console.log(data)
  } catch (err) {
    console.error(err)
  }
}

fetchDataAsync()
```

### 環境変数

```bash
# .env
PORT=3000
DB_HOST=localhost
DB_USER=root
DB_PASS=secret
```

```javascript
// dotenv使用
require('dotenv').config()

const port = process.env.PORT || 3000
const dbHost = process.env.DB_HOST

console.log(`Server port: ${port}`)
console.log(`DB host: ${dbHost}`)
```

### モジュール

```javascript
// math.js
function add(a, b) {
  return a + b
}

function subtract(a, b) {
  return a - b
}

module.exports = { add, subtract }

// または
exports.add = add
exports.subtract = subtract

// app.js
const math = require('./math')

console.log(math.add(5, 3))  // 8
console.log(math.subtract(5, 3))  // 2

// ES Modules (package.json に "type": "module")
// math.mjs
export function add(a, b) {
  return a + b
}

// app.mjs
import { add } from './math.mjs'
console.log(add(5, 3))
```

### Streams

```javascript
const fs = require('fs')

// Readable Stream
const readStream = fs.createReadStream('large-file.txt', 'utf8')

readStream.on('data', (chunk) => {
  console.log('Chunk:', chunk)
})

readStream.on('end', () => {
  console.log('Finished reading')
})

// Writable Stream
const writeStream = fs.createWriteStream('output.txt')
writeStream.write('Hello, ')
writeStream.write('World!')
writeStream.end()

// Pipe
const readStream = fs.createReadStream('input.txt')
const writeStream = fs.createWriteStream('output.txt')
readStream.pipe(writeStream)
```

### Child Processes

```javascript
const { exec, spawn } = require('child_process')

// exec
exec('ls -la', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error}`)
    return
  }
  console.log(`Output: ${stdout}`)
})

// spawn
const ls = spawn('ls', ['-la'])

ls.stdout.on('data', (data) => {
  console.log(`Output: ${data}`)
})

ls.on('close', (code) => {
  console.log(`Process exited with code ${code}`)
})
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Node.js** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **JavaScript**: フロント/バック統一
3. **高速**: V8エンジン
4. **npm**: 世界最大のパッケージ
5. **非同期**: 高並行性

## デメリット

1. **シングルスレッド**: CPU集約的処理不向き
2. **コールバック地獄**: 複雑な非同期
3. **型**: JavaScript動的型
4. **成熟度**: 他言語比較で若い

## 公式リンク

- **公式サイト**: [https://nodejs.org/](https://nodejs.org/)
- **ドキュメント**: [https://nodejs.org/docs/](https://nodejs.org/docs/)

## 関連ドキュメント

- [ランタイムツール一覧](../ランタイムツール/)
- [npm](../パッケージ管理ツール/npm.md)
- [Express.js](../Webフレームワークツール/Express.js.md)

---

**カテゴリ**: ランタイムツール
**対象工程**: JavaScript実行環境
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
