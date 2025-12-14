# MSW (Mock Service Worker)

## 概要

MSW (Mock Service Worker)は、Service Worker APIを活用したJavaScript/TypeScript向けのAPIモックライブラリです。ブラウザとNode.js両方で動作し、実際のHTTPリクエストをネットワークレベルでインターセプトしてモックレスポンスを返します。従来のXHR/fetchのモンキーパッチ方式と異なり、アプリケーションコードに手を加えることなくAPIモックを実現します。開発環境、テスト、Storybookなど、フロントエンド開発のあらゆるシーンで活用できるモダンなモックツールです。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | https://mswjs.io/ |
| **料金** | 🟢 完全無料 |
| **ライセンス** | MIT License |
| **対応言語** | JavaScript、TypeScript |
| **動作環境** | ブラウザ（Service Worker）、Node.js（http/https） |
| **開発元** | Artem Zakharchenko |
| **初版リリース** | 2019年 |
| **最新バージョン** | 2.x（2024年時点） |

## 主な機能

### 1. ネットワークレベルでのインターセプト
- **Service Worker**: ブラウザのService Worker APIを利用したリクエスト傍受
- **Node.jsネイティブ**: Node.jsのhttp/httpsモジュールレベルでのインターセプト
- **非侵襲的**: アプリケーションコードの変更不要
- **透過性**: 開発者ツールのNetworkタブで通信が見える

### 2. RESTful APIモック
- **HTTPメソッド**: GET、POST、PUT、PATCH、DELETE等すべて対応
- **パスマッチング**: 静的パス、パラメータ、ワイルドカード、正規表現
- **クエリパラメータ**: URLクエリでのリクエスト識別
- **リクエストボディ**: JSON、FormData、テキストのマッチング

### 3. GraphQLモック
- **クエリ/ミューテーション**: GraphQL操作の個別モック
- **変数サポート**: GraphQL変数を使ったマッチング
- **型安全**: TypeScriptでの型定義サポート
- **フラグメント**: GraphQLフラグメントに対応

### 4. レスポンス定義
- **ステータスコード**: 任意のHTTPステータスを返却
- **ヘッダー**: カスタムレスポンスヘッダー設定
- **ボディ**: JSON、テキスト、バイナリ、ストリーム
- **遅延**: ネットワーク遅延のシミュレーション

### 5. リクエストハンドラー
- **条件分岐**: リクエスト内容に応じた動的レスポンス
- **状態管理**: ハンドラー内で状態を持つことが可能
- **エラーシミュレーション**: ネットワークエラー、タイムアウトの再現
- **ファイルアップロード**: multipart/form-dataの処理

### 6. 開発者体験
- **TypeScript完全サポート**: 型安全なモック定義
- **エラーメッセージ**: 分かりやすいエラー・警告メッセージ
- **デバッグ**: コンソールログでのリクエスト/レスポンス表示
- **Hot Reload**: 開発中のハンドラー変更が即座に反映

### 7. テスト統合
- **Jest**: Jestとのシームレスな統合
- **Vitest**: Vitestでの利用
- **Playwright/Cypress**: E2Eテストフレームワーク対応
- **セットアップ簡単**: beforeAll/afterAllで簡単にセットアップ

## 利用方法

### インストール

```bash
# npm
npm install msw --save-dev

# yarn
yarn add msw --dev

# pnpm
pnpm add -D msw
```

### 基本的な使い方

#### 1. RESTful APIのモック定義
```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  // GET /user → ユーザー情報を返す
  http.get('/user', () => {
    return HttpResponse.json({
      id: 1,
      name: 'Alice',
      email: 'alice@example.com'
    })
  }),

  // POST /login → ログイン処理
  http.post('/login', async ({ request }) => {
    const { username, password } = await request.json()

    if (username === 'admin' && password === 'password') {
      return HttpResponse.json(
        { token: 'abc123' },
        { status: 200 }
      )
    }

    return HttpResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    )
  }),

  // パスパラメータ
  http.get('/users/:userId', ({ params }) => {
    const { userId } = params
    return HttpResponse.json({
      id: userId,
      name: `User ${userId}`
    })
  }),

  // クエリパラメータ
  http.get('/search', ({ request }) => {
    const url = new URL(request.url)
    const query = url.searchParams.get('q')

    return HttpResponse.json({
      query,
      results: []
    })
  })
]
```

#### 2. ブラウザでのセットアップ
```typescript
// src/mocks/browser.ts
import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

export const worker = setupWorker(...handlers)
```

```typescript
// src/main.tsx (開発環境のみMSWを起動)
import { worker } from './mocks/browser'

if (process.env.NODE_ENV === 'development') {
  worker.start({
    onUnhandledRequest: 'warn' // モックされていないリクエストを警告
  })
}
```

```bash
# Service Workerファイルを生成（初回のみ）
npx msw init public/ --save
```

#### 3. Node.js（テスト）でのセットアップ
```typescript
// src/mocks/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

```typescript
// src/setupTests.ts (Jest/Vitest)
import { server } from './mocks/server'

// テスト開始前にサーバー起動
beforeAll(() => server.listen())

// 各テスト後にハンドラーをリセット
afterEach(() => server.resetHandlers())

// テスト終了後にサーバー停止
afterAll(() => server.close())
```

#### 4. テストでの使用例
```typescript
// UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { server } from './mocks/server'
import { http, HttpResponse } from 'msw'
import UserProfile from './UserProfile'

test('displays user name', async () => {
  render(<UserProfile userId={1} />)

  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument()
  })
})

test('handles error', async () => {
  // このテストのみエラーレスポンスを返す
  server.use(
    http.get('/user', () => {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      )
    })
  )

  render(<UserProfile userId={999} />)

  await waitFor(() => {
    expect(screen.getByText('Error: User not found')).toBeInTheDocument()
  })
})
```

#### 5. GraphQLのモック
```typescript
import { graphql, HttpResponse } from 'msw'

export const handlers = [
  // GraphQLクエリ
  graphql.query('GetUser', ({ variables }) => {
    const { id } = variables

    return HttpResponse.json({
      data: {
        user: {
          id,
          name: 'Alice',
          email: 'alice@example.com'
        }
      }
    })
  }),

  // GraphQLミューテーション
  graphql.mutation('CreateUser', async ({ variables }) => {
    const { input } = variables

    return HttpResponse.json({
      data: {
        createUser: {
          id: '123',
          ...input
        }
      }
    })
  })
]
```

#### 6. 遅延とエラーのシミュレーション
```typescript
import { http, HttpResponse, delay } from 'msw'

export const handlers = [
  // 固定遅延（2秒）
  http.get('/slow-api', async () => {
    await delay(2000)
    return HttpResponse.json({ data: 'slow response' })
  }),

  // ランダム遅延
  http.get('/variable-api', async () => {
    await delay(Math.random() * 3000)
    return HttpResponse.json({ data: 'variable response' })
  }),

  // ネットワークエラー
  http.get('/broken-api', () => {
    return HttpResponse.error()
  }),

  // タイムアウト
  http.get('/timeout-api', async () => {
    await delay('infinite')
  })
]
```

#### 7. 動的ハンドラー（状態管理）
```typescript
// カウンターの例
let count = 0

export const handlers = [
  http.get('/counter', () => {
    return HttpResponse.json({ count })
  }),

  http.post('/counter/increment', () => {
    count++
    return HttpResponse.json({ count })
  }),

  http.post('/counter/reset', () => {
    count = 0
    return HttpResponse.json({ count })
  })
]
```

#### 8. リクエストボディの検証
```typescript
http.post('/users', async ({ request }) => {
  const body = await request.json()

  // バリデーション
  if (!body.name || !body.email) {
    return HttpResponse.json(
      { error: 'Name and email are required' },
      { status: 400 }
    )
  }

  // 成功レスポンス
  return HttpResponse.json(
    { id: '123', ...body },
    { status: 201 }
  )
})
```

#### 9. Cookieとヘッダー
```typescript
http.get('/protected', ({ request, cookies }) => {
  const authToken = cookies.authToken
  const authHeader = request.headers.get('Authorization')

  if (!authToken && !authHeader) {
    return HttpResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  return HttpResponse.json(
    { data: 'protected resource' },
    {
      headers: {
        'Set-Cookie': 'sessionId=xyz; HttpOnly; Secure',
        'X-Custom-Header': 'value'
      }
    }
  )
})
```

## メリット

### 1. 非侵襲的
✅ アプリケーションコードの変更不要
✅ 本番コードにモックロジックが混入しない
✅ APIクライアントの実装を問わない（fetch、axios、ky等すべて対応）

### 2. 開発とテストの一貫性
✅ 同じハンドラーを開発環境とテストで共有
✅ ブラウザとNode.jsで同じコードが動く
✅ DRY原則の徹底

### 3. リアルな動作
✅ 実際のHTTPリクエストとして動作
✅ ブラウザ開発者ツールのNetworkタブでリクエストを確認可能
✅ リダイレクト、CORS、Cookieなど実環境と同じ挙動

### 4. TypeScript完全サポート
✅ 型安全なハンドラー定義
✅ リクエスト/レスポンスの型推論
✅ IDE補完が効く

### 5. 軽量・高速
✅ ブラウザネイティブのService Worker API利用
✅ 追加のサーバー不要
✅ メモリ消費が少ない

### 6. GraphQL対応
✅ REST APIとGraphQLを統一的に扱える
✅ 型安全なGraphQLモック
✅ Apollo ClientやUrqlなど主要クライアントに対応

### 7. 優れた開発者体験
✅ 直感的なAPI設計
✅ 詳細なエラーメッセージ
✅ 豊富なドキュメントと事例

## デメリット

### 1. Service Worker依存（ブラウザ）
❌ Service Worker非対応ブラウザでは動作しない（IE11等）
❌ HTTPSまたはlocalhostが必要
❌ Service Workerの初回登録に少し時間がかかる

### 2. 学習コスト
❌ Service Workerの仕組みの理解が必要
❌ 従来のXHR/fetchモンキーパッチと異なるアプローチ
❌ 初期セットアップがやや複雑

### 3. JavaScript/TypeScript専用
❌ 他言語（Java、Python等）では使用不可
❌ フロントエンド以外のテストには不向き
❌ マルチ言語環境では別ツールが必要

### 4. 複雑なシナリオ
❌ 状態遷移が複雑な場合はハンドラーが煩雑に
❌ プロキシ/録画機能がない
❌ スタブの永続化機能がない

### 5. デバッグ
❌ ハンドラー内のエラーが見つけにくい場合がある
❌ Service Workerのライフサイクルに注意が必要
❌ ブラウザ再読み込み時の挙動に癖がある

## ユースケース

### 1. フロントエンド開発
- バックエンドAPIの開発を待たずにUI実装
- ローカル開発環境でのAPIモック
- エラーケースや境界値のテスト

### 2. ユニット・統合テスト
- Reactコンポーネントのテスト（Jest、Vitest）
- APIクライアントのテスト
- 状態管理（Redux、Zustand等）のテスト

### 3. E2Eテスト
- Playwright、Cypress、Puppeteerでの利用
- 外部APIに依存しない安定したテスト
- ネットワークエラーのシミュレーション

### 4. Storybook
- コンポーネントカタログでのAPIモック
- インタラクティブなデモ環境
- デザイナーとの協業

### 5. プロトタイピング
- 素早いプロトタイプ作成
- クライアントへのデモ
- ユーザビリティテスト

## 類似ツールとの比較

| ツール | 料金 | 対応環境 | 特徴 |
|--------|------|----------|------|
| **MSW** | 🟢 無料 | Browser/Node.js | Service Worker利用、非侵襲的 |
| WireMock | 🟢 無料 | 言語非依存 | Java/スタンドアロン、成熟 |
| MockServer | 🟢 無料 | 言語非依存 | OpenAPI統合、UI |
| Nock | 🟢 無料 | Node.js | HTTPモック特化、軽量 |
| Mirage.js | 🟢 無料 | Browser | フルスタックモック、ORM |
| json-server | 🟢 無料 | Node.js | JSONベース、超軽量 |

### MSWを選ぶべきケース
- React、Vue、Angularなどのフロントエンド開発
- TypeScriptで型安全にモックを定義したい
- 開発環境とテストで同じモックを使いたい
- ブラウザとNode.js両方でモックが必要

### 他ツールを検討すべきケース
- バックエンドやマイクロサービスのモック → **WireMock**、**MockServer**
- Node.jsのみでHTTPモック → **Nock**
- データモデルとの統合が必要 → **Mirage.js**
- 超軽量なモックサーバー → **json-server**

## ベストプラクティス

### 1. ハンドラーの整理
```typescript
// ドメイン別にファイル分割
// src/mocks/handlers/user.ts
export const userHandlers = [...]

// src/mocks/handlers/product.ts
export const productHandlers = [...]

// src/mocks/handlers/index.ts
export const handlers = [
  ...userHandlers,
  ...productHandlers
]
```

### 2. 環境別の設定
```typescript
// 開発環境: すべてモック
if (process.env.NODE_ENV === 'development') {
  worker.start()
}

// ステージング: 未実装APIのみモック
if (process.env.VITE_ENABLE_MSW === 'true') {
  worker.start({
    onUnhandledRequest: 'bypass' // モックされていないリクエストは実APIに
  })
}
```

### 3. リアルなデータ生成
```typescript
import { faker } from '@faker-js/faker'

http.get('/users', () => {
  const users = Array.from({ length: 20 }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar()
  }))

  return HttpResponse.json(users)
})
```

### 4. ページネーション
```typescript
http.get('/posts', ({ request }) => {
  const url = new URL(request.url)
  const page = parseInt(url.searchParams.get('page') || '1')
  const limit = parseInt(url.searchParams.get('limit') || '10')

  const allPosts = generatePosts(100)
  const start = (page - 1) * limit
  const end = start + limit

  return HttpResponse.json({
    data: allPosts.slice(start, end),
    pagination: {
      page,
      limit,
      total: allPosts.length
    }
  })
})
```

### 5. テストごとのカスタマイズ
```typescript
test('error handling', async () => {
  // 一時的にハンドラーを上書き
  server.use(
    http.get('/user', () => {
      return new HttpResponse(null, { status: 500 })
    })
  )

  // テスト実行
  render(<UserProfile />)
  expect(await screen.findByText('Error occurred')).toBeInTheDocument()

  // afterEach()でリセットされるため、他のテストに影響なし
})
```

### 6. デバッグログ
```typescript
worker.start({
  onUnhandledRequest(request, print) {
    // 自社APIのみ警告
    if (request.url.includes('api.mycompany.com')) {
      print.warning()
    }
  }
})
```

### 7. 型安全なハンドラー
```typescript
interface User {
  id: string
  name: string
  email: string
}

http.get<never, never, User>('/user', () => {
  return HttpResponse.json({
    id: '1',
    name: 'Alice',
    email: 'alice@example.com'
  })
})
```

## 公式リンク

- **公式サイト**: https://mswjs.io/
- **ドキュメント**: https://mswjs.io/docs/
- **GitHub**: https://github.com/mswjs/msw
- **Discord**: https://discord.gg/mswjs
- **Examples**: https://github.com/mswjs/examples

## 関連ツール

- [Mockito](./Mockito.md) - Javaメソッドレベルモック
- [WireMock](./WireMock.md) - HTTP APIモックの定番
- [MockServer](./MockServer.md) - OpenAPI統合モックサーバー
- [Postman](./Postman.md) - API開発・テストツール
- [Faker.js](https://fakerjs.dev/) - テストデータ生成
- [Storybook](https://storybook.js.org/) - UIコンポーネントカタログ

## まとめ

MSW (Mock Service Worker)は、Service Worker APIを活用したモダンなJavaScript/TypeScriptのAPIモックライブラリです。非侵襲的なアプローチにより、アプリケーションコードを変更することなく、ネットワークレベルでリクエストをインターセプトしてモックレスポンスを返します。

ブラウザとNode.js両方で同じハンドラーを使えるため、開発環境とテスト環境で一貫したモックを提供できます。TypeScriptの型安全性、直感的なAPI、豊富なドキュメントにより、優れた開発者体験を実現しています。

React、Vue、Angularなどのモダンフロントエンド開発において、MSWはAPIモックのデファクトスタンダードとなりつつあり、積極的に採用する価値があります。
