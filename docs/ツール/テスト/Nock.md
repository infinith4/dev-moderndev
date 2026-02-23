# Nock

## 概要

**Nock** は、Node.js環境でHTTPリクエストをモック・スタブ化するための強力なライブラリです。外部HTTPリクエストを完全に制御し、テストの信頼性と実行速度を向上させます。リクエストの記録・再生機能により、実際のAPIレスポンスを簡単にモック化できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | [https://github.com/nock/nock](https://github.com/nock/nock) |
| **GitHub** | [https://github.com/nock/nock](https://github.com/nock/nock) |
| **ライセンス** | MIT License |
| **開発元** | Nock Contributors |
| **対応技術** | Node.js / HTTP / HTTPS |
| **料金** |  無料・オープンソース |

## 主な機能

### 1. HTTPリクエストインターセプト
- すべての外部HTTPリクエストをインターセプト
- リクエストパターンマッチング
- レスポンス完全制御
- 実ネットワークアクセス防止

### 2. リクエスト記録・再生
- 実際のAPIリクエスト記録
- 記録したレスポンス再生
- フィクスチャファイル保存
- リプレイモード

### 3. 柔軟なマッチング
- URL完全一致・部分一致
- HTTPメソッド指定
- リクエストヘッダーマッチング
- リクエストボディマッチング

### 4. レスポンスカスタマイズ
- ステータスコード指定
- レスポンスヘッダー設定
- レスポンスボディ定義
- 遅延シミュレーション

### 5. テストフレームワーク統合
- Jest統合
- Mocha統合
- Ava統合
- Vitest統合

## メリット・デメリット

### メリット 

- **無料・オープンソース** - ライセンス費用不要
- **Node.jsテスト最適化** - Node.js環境に特化
- **HTTPリクエスト完全制御** - すべてのリクエスト制御可能
- **リクエスト記録・再生** - 実APIレスポンス活用
- **Jest/Mocha統合容易** - 主要テストフレームワーク対応
- **軽量で高速** - オーバーヘッド最小限
- **充実したドキュメント** - 学習しやすい

### デメリット 

- **Node.js専用** - ブラウザ環境非対応
- **ブラウザ非対応** - フロントエンド開発には別ツール必要
- **スタンドアロンサーバではない** - テストコード埋め込み型
- **GraphQL対応限定的** - REST API中心

## インストール・セットアップ

### npm/yarn/pnpmでインストール

```bash
# npm
npm install --save-dev nock

# yarn
yarn add --dev nock

# pnpm
pnpm add -D nock
```

### 基本的な使用方法

```javascript
const nock = require('nock')

// HTTPリクエストをモック
nock('https://api.example.com')
  .get('/users/123')
  .reply(200, {
    id: '123',
    name: 'John Doe',
    email: 'john@example.com'
  })

// 実際のコード実行
const response = await fetch('https://api.example.com/users/123')
const data = await response.json()
// data = { id: '123', name: 'John Doe', email: 'john@example.com' }
```

## 実践例

### 基本的なGETリクエストモック

```javascript
const nock = require('nock')
const axios = require('axios')

describe('User API', () => {
  test('ユーザー情報取得', async () => {
    // モック設定
    nock('https://api.example.com')
      .get('/users/123')
      .reply(200, {
        id: '123',
        name: 'John Doe'
      })

    // テスト実行
    const response = await axios.get('https://api.example.com/users/123')

    expect(response.data.id).toBe('123')
    expect(response.data.name).toBe('John Doe')
  })
})
```

### POSTリクエストのモック

```javascript
nock('https://api.example.com')
  .post('/users', {
    name: 'Jane Doe',
    email: 'jane@example.com'
  })
  .reply(201, {
    id: '456',
    name: 'Jane Doe',
    email: 'jane@example.com',
    createdAt: '2025-01-01T00:00:00Z'
  })
```

### リクエストヘッダーのマッチング

```javascript
nock('https://api.example.com')
  .get('/protected')
  .matchHeader('authorization', 'Bearer token123')
  .reply(200, { data: 'protected data' })
```

### クエリパラメータのマッチング

```javascript
nock('https://api.example.com')
  .get('/users')
  .query({ page: 1, limit: 10 })
  .reply(200, {
    users: [/* ... */],
    total: 100
  })
```

### エラーレスポンスのモック

```javascript
nock('https://api.example.com')
  .get('/users/999')
  .reply(404, {
    error: 'User not found'
  })

// ネットワークエラー
nock('https://api.example.com')
  .get('/timeout')
  .replyWithError('Network timeout')
```

### レスポンス遅延シミュレーション

```javascript
nock('https://api.example.com')
  .get('/slow')
  .delay(2000) // 2秒遅延
  .reply(200, { data: 'slow response' })
```

### リクエスト記録・再生

```javascript
const nock = require('nock')

// リクエスト記録モード
nock.recorder.rec({
  output_objects: true,
  dont_print: true
})

// 実際のAPIリクエスト実行
await fetch('https://api.example.com/users/123')

// 記録したリクエスト取得
const recordings = nock.recorder.play()

// ファイル保存
const fs = require('fs')
fs.writeFileSync('fixtures/users.json', JSON.stringify(recordings, null, 2))
```

```javascript
// 記録したリクエストを再生
const fixtures = require('./fixtures/users.json')

fixtures.forEach(fixture => {
  nock(fixture.scope)
    .intercept(fixture.path, fixture.method)
    .reply(fixture.status, fixture.response)
})
```

## ベストプラクティス

### テスト後のクリーンアップ

```javascript
const nock = require('nock')

describe('API Tests', () => {
  afterEach(() => {
    // すべてのモックをクリーンアップ
    nock.cleanAll()
  })

  test('テスト1', async () => {
    nock('https://api.example.com')
      .get('/resource')
      .reply(200, { data: 'test' })

    // テストコード...
  })
})
```

### モック未使用検出

```javascript
afterEach(() => {
  // 未使用のモックを検出
  if (!nock.isDone()) {
    console.error('未使用のモックがあります')
    nock.cleanAll()
    throw new Error('未使用のモック')
  }
})
```

### 実ネットワークアクセス禁止

```javascript
beforeAll(() => {
  // すべての実ネットワークアクセスを禁止
  nock.disableNetConnect()

  // localhost のみ許可（テストサーバー用）
  nock.enableNetConnect('127.0.0.1')
})

afterAll(() => {
  nock.enableNetConnect()
})
```

### 共通モックの再利用

```javascript
// mocks/userApi.js
const nock = require('nock')

function mockGetUser(id, data) {
  return nock('https://api.example.com')
    .get(`/users/${id}`)
    .reply(200, data)
}

function mockCreateUser(userData, responseData) {
  return nock('https://api.example.com')
    .post('/users', userData)
    .reply(201, responseData)
}

module.exports = { mockGetUser, mockCreateUser }
```

```javascript
// tests/user.test.js
const { mockGetUser } = require('../mocks/userApi')

test('ユーザー取得', async () => {
  mockGetUser('123', { id: '123', name: 'John' })

  // テストコード...
})
```

## CI/CD統合

### GitHub Actions設定例

```yaml
name: Tests with Nock

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run tests with Nock
        run: npm test
        env:
          NODE_ENV: test
```

## 関連ツール・連携

| ツール | 用途 | 連携方法 |
|--------|------|---------|
| **Jest** | テストフレームワーク | setupFiles設定 |
| **Mocha** | テストフレームワーク | before/after hooks |
| **Axios** | HTTPクライアント | 自動インターセプト |
| **node-fetch** | HTTPクライアント | 自動インターセプト |
| **Supertest** | APIテスト | 組み合わせ使用 |
| **Faker.js** | テストデータ生成 | レスポンスデータ生成 |

## 他ツールとの比較

| 機能 | Nock | MSW | WireMock | Sinon |
|------|------|-----|----------|-------|
| Node.js対応 |  |  |  |  |
| ブラウザ対応 |  |  |  |  |
| HTTPモック |  専用 |  |  |  汎用 |
| 記録・再生 |  |  |  |  |
| スタンドアロン |  |  |  |  |
| 学習曲線 | 低 | 中 | 中 | 中 |

## 推奨用途

### 最適なケース

- Node.jsバックエンドテスト
- REST APIクライアントテスト
- 外部API依存のユニットテスト
- CI/CD環境での高速テスト
- HTTPリクエスト記録・再生が必要

### 不向きなケース

- ブラウザベーステスト（MSW推奨）
- スタンドアロンモックサーバが必要（WireMock推奨）
- GraphQLメインのアプリ（MSW推奨）
- フロントエンド開発環境（MSW推奨）

## トラブルシューティング

### よくある問題

**問題**: モックが動作しない

```javascript
// 解決方法: URL完全一致確認
nock('https://api.example.com')  // 末尾スラッシュなし
  .get('/users')
  .reply(200, {})

//  正しい
await fetch('https://api.example.com/users')

//  間違い（末尾スラッシュ）
await fetch('https://api.example.com/users/')
```

**問題**: 未使用のモック警告

```javascript
// 解決方法: persist()で複数回使用許可
nock('https://api.example.com')
  .get('/resource')
  .reply(200, {})
  .persist()  // 複数回呼び出し許可
```

## 学習リソース

| リソース | URL |
|---------|-----|
| **公式ドキュメント** | [https://github.com/nock/nock](https://github.com/nock/nock) |
| **APIドキュメント** | [https://github.com/nock/nock#usage](https://github.com/nock/nock#usage) |
| **Examples** | [https://github.com/nock/nock/tree/main/tests](https://github.com/nock/nock/tree/main/tests) |

## 関連ドキュメント

- [開発工程_9_テスト（アプリケーション）](../../dev_process_開発工程_9_テスト_アプリケーション.md)
- [MSW (Mock Service Worker)](./MSW.md)
- [WireMock](./WireMock.md)
- [Jest](./Jest.md)
- [Mocha + Chai](./Mocha.md)

---

**最終更新日**: 2025年（令和7年）
**文書バージョン**: 1.0

