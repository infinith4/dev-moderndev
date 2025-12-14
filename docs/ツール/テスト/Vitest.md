# Vitest

## 概要

Vitestは、Vite対応の超高速ユニットテストフレームワークです。Viteの高速なHMR（Hot Module Replacement）とトランスフォーム機能を活用し、Jestと互換性のあるAPIを提供しながら、TypeScript、JSX、ESMをネイティブサポートします。Viteプロジェクトとのシームレスな統合により、開発体験を損なわずにテストを実行できます。

## 主な機能

### 1. 超高速実行
- Viteのトランスフォームを再利用
- ESMネイティブサポート
- 並列実行デフォルト
- Watch モード高速

### 2. Jest互換API
- expect、describe、it/test
- スナップショットテスト
- モック関数
- 既存Jestテストの移行容易

### 3. TypeScript・JSX対応
- 追加設定不要でTypeScript対応
- JSX/TSXネイティブサポート
- 型安全なテスト

### 4. Vite統合
- vite.config.ts でテスト設定
- プラグインエコシステム活用
- 開発サーバーとテストで同じ設定

### 5. UI・カバレッジ
- Vitest UI（ブラウザベースUI）
- Istanbul/c8によるカバレッジ
- インタラクティブなテスト結果表示

### 6. コンポーネントテスト
- Vue Test Utils統合
- React Testing Library対応
- Svelte Testing Library対応

## 利用方法

### インストール

```bash
# npm
npm install -D vitest

# yarn
yarn add -D vitest

# pnpm
pnpm add -D vitest
```

### 設定（vite.config.ts）

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom', // または 'node', 'happy-dom'
    setupFiles: './tests/setup.ts',
    coverage: {
      provider: 'istanbul', // または 'c8'
      reporter: ['text', 'json', 'html'],
    },
  },
})
```

### 基本テスト例

```typescript
// src/utils/sum.test.ts
import { describe, it, expect } from 'vitest'
import { sum } from './sum'

describe('sum', () => {
  it('adds two numbers', () => {
    expect(sum(1, 2)).toBe(3)
  })

  it('handles negative numbers', () => {
    expect(sum(-1, -2)).toBe(-3)
  })
})
```

### モックテスト

```typescript
import { describe, it, expect, vi } from 'vitest'
import { fetchUser } from './api'

// モック作成
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}))

describe('fetchUser', () => {
  it('returns user data', async () => {
    const mockUser = { id: 1, name: 'Test User' }
    vi.mocked(fetchUser).mockResolvedValue(mockUser)

    const user = await fetchUser(1)
    expect(user).toEqual(mockUser)
    expect(fetchUser).toHaveBeenCalledWith(1)
  })
})
```

### Reactコンポーネントテスト

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Button from './Button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    await userEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### スナップショットテスト

```typescript
import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import Component from './Component'

describe('Component', () => {
  it('matches snapshot', () => {
    const { container } = render(<Component />)
    expect(container.firstChild).toMatchSnapshot()
  })
})
```

### テスト実行

```bash
# package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}

# 実行
npm run test           # Watch モード
npm run test -- --run  # 1回のみ実行
npm run test:ui        # UI モード
npm run test:coverage  # カバレッジ計測
```

## CI/CD統合

### GitHub Actions

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test -- --run
      
      - name: Generate coverage
        run: npm run test:coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
```

## メリット

### ✅ 主な利点

1. **超高速**: Jestの10-20倍高速
2. **Vite統合**: 開発サーバーとテストで同じ設定
3. **Jest互換**: 既存テストの移行容易
4. **TypeScript標準**: 追加設定不要
5. **ESMネイティブ**: モダンJavaScript対応
6. **Watch モード高速**: HMR活用
7. **UI機能**: ブラウザベースの視覚的テスト結果
8. **並列実行**: デフォルトで並列
9. **軽量**: 依存関係少ない
10. **アクティブ開発**: 継続的な改善

## デメリット

### ❌ 制約・課題

1. **比較的新しい**: Jestより情報・事例少ない
2. **エコシステム**: Jestほどプラグイン豊富ではない
3. **完全互換ではない**: 一部Jestの機能は非対応
4. **Node.js専用機能**: 一部環境依存の機能に制約
5. **学習コスト**: Viteに不慣れな場合は追加学習必要
6. **ブラウザテスト**: Playwright/Cypressが別途必要
7. **スナップショット**: Jestとフォーマット異なる
8. **Windows**: 一部機能でパス問題の可能性

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Jest** | 業界標準、豊富なエコシステム | Vitestより遅いが成熟 |
| **Mocha + Chai** | 柔軟、古い | Vitestより設定必要 |
| **AVA** | 並列実行、シンプル | Vitestより機能少ない |
| **uvu** | 超軽量 | Vitestより機能限定的 |
| **Jasmine** | 古典的、独立型 | Vitestより古い |

## 公式リンク

- **公式サイト**: [https://vitest.dev/](https://vitest.dev/)
- **GitHub**: [https://github.com/vitest-dev/vitest](https://github.com/vitest-dev/vitest)
- **ドキュメント**: [https://vitest.dev/guide/](https://vitest.dev/guide/)
- **API**: [https://vitest.dev/api/](https://vitest.dev/api/)
- **Examples**: [https://github.com/vitest-dev/vitest/tree/main/examples](https://github.com/vitest-dev/vitest/tree/main/examples)

## 関連ドキュメント

- [テストツール一覧](../テストツール/)
- [Jest](./Jest.md)
- [Cypress](./Cypress.md)
- [Viteプロジェクト設定](../../best-practices/vite-setup.md)
- [ユニットテストベストプラクティス](../../best-practices/unit-testing.md)

---

**カテゴリ**: テストツール  
**対象工程**: 実装、テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
