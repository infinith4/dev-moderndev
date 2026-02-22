# MSW (Mock Service Worker)

## 概要

MSW（Mock Service Worker）は、Service Worker APIを活用してブラウザとNode.js両方で動作するAPIモックライブラリです。ネットワークレベルでリクエストをインターセプトし、実際のAPIと同じようにモックレスポンスを返します。REST APIとGraphQL両対応で、テストコードとの統合が容易、TypeScript完全対応により、モダンなフロントエンド開発に最適です。

## 主な機能

### 1. ブラウザ・Node.js両対応
- **Service Worker**: ブラウザでネットワークレベルモック
- **Node.js**: サーバーサイドテスト対応
- **統一API**: 同じコードで両環境動作
- **透過的**: アプリケーションコード変更不要

### 2. REST API・GraphQL対応
- **REST API**: HTTP メソッド全対応
- **GraphQL**: Query、Mutation、Subscription
- **型安全**: TypeScript型推論
- **リクエストマッチング**: URLパターン、ボディ検証

### 3. テストフレームワーク統合
- **Jest統合**: セットアップ簡単
- **Vitest統合**: Vite環境最適
- **Playwright統合**: E2Eテスト対応
- **Cypress統合**: E2Eテスト対応

### 4. 開発体験
- **TypeScript完全対応**: 型推論・補完
- **直感的API**: 宣言的な記述
- **デバッグ容易**: リクエスト/レスポンス表示
- **ホットリロード対応**: 開発モード

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

### ブラウザセットアップ

```bash
# Service Worker生成（public/ディレクトリに）
npx msw init public/ --save
```

### ハンドラ定義（REST API）

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  // GET /api/users
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ]);
  }),

  // GET /api/users/:id
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id: Number(id),
      name: `User ${id}`,
      email: `user${id}@example.com`,
    });
  }),

  // POST /api/users
  http.post('/api/users', async ({ request }) => {
    const newUser = await request.json();
    return HttpResponse.json(
      { id: 100, ...newUser },
      { status: 201 }
    );
  }),

  // エラーレスポンス
  http.get('/api/error', () => {
    return new HttpResponse(null, { status: 500 });
  }),
];
```

### ブラウザ用セットアップ

```typescript
// src/mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
```

```typescript
// src/index.tsx (開発モードのみ起動)
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

async function prepare() {
  if (process.env.NODE_ENV === 'development') {
    const { worker } = await import('./mocks/browser');
    return worker.start();
  }
  return Promise.resolve();
}

prepare().then(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
});
```

### Node.js用セットアップ（Jest）

```typescript
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```typescript
// src/setupTests.ts (Jest)
import { server } from './mocks/server';

// テスト開始前にサーバ起動
beforeAll(() => server.listen());

// 各テスト後にハンドラリセット
afterEach(() => server.resetHandlers());

// テスト終了後にサーバ停止
afterAll(() => server.close());
```

### テストコード例

```typescript
// UserList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { server } from './mocks/server';
import { http, HttpResponse } from 'msw';
import UserList from './UserList';

test('displays user list', async () => {
  render(<UserList />);

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
  });
});

test('handles error response', async () => {
  // テスト内でハンドラ上書き
  server.use(
    http.get('/api/users', () => {
      return new HttpResponse(null, { status: 500 });
    })
  );

  render(<UserList />);

  await waitFor(() => {
    expect(screen.getByText('Error loading users')).toBeInTheDocument();
  });
});
```

### GraphQL対応

```typescript
// src/mocks/handlers.ts
import { graphql, HttpResponse } from 'msw';

export const handlers = [
  graphql.query('GetUser', ({ query, variables }) => {
    return HttpResponse.json({
      data: {
        user: {
          id: variables.id,
          name: 'John Doe',
          email: 'john@example.com',
        },
      },
    });
  }),

  graphql.mutation('CreateUser', ({ query, variables }) => {
    return HttpResponse.json({
      data: {
        createUser: {
          id: 100,
          name: variables.name,
          email: variables.email,
        },
      },
    });
  }),
];
```

### リクエスト検証

```typescript
http.post('/api/users', async ({ request }) => {
  const body = await request.json();

  // バリデーション
  if (!body.name || !body.email) {
    return HttpResponse.json(
      { error: 'Name and email are required' },
      { status: 400 }
    );
  }

  return HttpResponse.json({ id: 100, ...body }, { status: 201 });
});
```

### 遅延シミュレーション

```typescript
import { delay, http, HttpResponse } from 'msw';

http.get('/api/slow-endpoint', async () => {
  await delay(2000); // 2秒遅延
  return HttpResponse.json({ status: 'ok' });
});
```

### 動的レスポンス

```typescript
http.get('/api/users/:id', ({ params, cookies, request }) => {
  const { id } = params;
  const url = new URL(request.url);
  const format = url.searchParams.get('format');

  if (format === 'xml') {
    return HttpResponse.xml('<user><id>1</id></user>');
  }

  return HttpResponse.json({ id, name: `User ${id}` });
});
```

### Vitest統合

```typescript
// vitest.setup.ts
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from './src/mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
  },
});
```

### Playwright統合

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'npm run dev',
    port: 3000,
  },
  use: {
    baseURL: 'http://localhost:3000',
  },
});
```

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  // MSWは開発モードで自動起動
  await page.goto('/');
});

test('displays mocked user list', async ({ page }) => {
  await expect(page.locator('text=John Doe')).toBeVisible();
});
```

### 環境別ハンドラ

```typescript
// src/mocks/handlers/development.ts
export const developmentHandlers = [
  http.get('/api/debug', () => {
    return HttpResponse.json({ env: 'development' });
  }),
];

// src/mocks/handlers/production.ts
export const productionHandlers = [
  http.get('/api/health', () => {
    return HttpResponse.json({ status: 'ok' });
  }),
];
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **MSW** | 🟢 完全無料 | オープンソース、フル機能 |

## メリット

1. **ブラウザ・Node.js両対応**: 統一API
2. **Service Worker活用**: ネットワークレベルモック
3. **テストコード統合容易**: Jest/Vitest統合簡単
4. **GraphQL対応**: Query/Mutation対応
5. **TypeScript完全対応**: 型安全・補完

## デメリット

1. **JavaScript/TypeScript環境必須**: 他言語不可
2. **スタンドアロンサーバではない**: ライブラリ形式のみ
3. **学習コスト中程度**: Service Worker概念理解必要
4. **ブラウザ互換性制限**: Service Worker対応ブラウザのみ

## 公式リンク

- **公式サイト**: [https://mswjs.io/](https://mswjs.io/)
- **ドキュメント**: [https://mswjs.io/docs/](https://mswjs.io/docs/)
- **GitHub**: [https://github.com/mswjs/msw](https://github.com/mswjs/msw)
- **npm**: [https://www.npmjs.com/package/msw](https://www.npmjs.com/package/msw)

## 関連ドキュメント

- [モックサーバツール一覧](../../dev_process_開発工程_9_テスト_アプリケーション.md#922-apiテスト用モックサーバツールtop-6)
- [Jest](./Jest.md)
- [Vitest](./Vitest.md)
- [Playwright](./Playwright.md)

---

**カテゴリ**: モックサーバ・APIテスト
**対象工程**: フロントエンド開発・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
