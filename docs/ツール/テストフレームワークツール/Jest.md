# Jest

## 概要

Jestは、Facebook製のJavaScriptテストフレームワークです。ゼロコンフィグ、スナップショットテスト、モック、カバレッジレポート、並列実行により、React、Vue、Node.jsアプリケーションの単体テスト・統合テストを実現します。高速、シンプル、React公式推奨で広く採用されています。

## 主な機能

### 1. テスト実行
- **ゼロコンフィグ**: 設定不要
- **並列実行**: 高速テスト
- **Watch モード**: 変更検知
- **カバレッジ**: コードカバレッジ

### 2. アサーション
- **Matchers**: expect API
- **非同期**: async/await、Promise
- **例外**: toThrow

### 3. モック
- **関数モック**: jest.fn()
- **モジュールモック**: jest.mock()
- **タイマーモック**: jest.useFakeTimers()
- **スパイ**: jest.spyOn()

### 4. スナップショット
- **UI テスト**: コンポーネントスナップショット
- **自動更新**: --updateSnapshot
- **差分表示**: 変更検出

## 利用方法

### インストール

```bash
npm install --save-dev jest

# package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

### 基本テスト

```javascript
// sum.js
function sum(a, b) {
  return a + b
}
module.exports = sum

// sum.test.js
const sum = require('./sum')

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3)
})

test('adds 5 + 10 to equal 15', () => {
  expect(sum(5, 10)).toBe(15)
})
```

```bash
npm test
```

### Matchers

```javascript
// matchers.test.js
test('toBe vs toEqual', () => {
  expect(2 + 2).toBe(4)  // 厳密等価
  expect({ name: 'Alice' }).toEqual({ name: 'Alice' })  // 値等価
})

test('truthiness', () => {
  expect(null).toBeNull()
  expect(undefined).toBeUndefined()
  expect(true).toBeTruthy()
  expect(false).toBeFalsy()
})

test('numbers', () => {
  expect(10).toBeGreaterThan(5)
  expect(10).toBeGreaterThanOrEqual(10)
  expect(10).toBeLessThan(20)
  expect(0.1 + 0.2).toBeCloseTo(0.3)
})

test('strings', () => {
  expect('team').not.toMatch(/I/)
  expect('team').toMatch(/tea/)
})

test('arrays and iterables', () => {
  const list = ['apple', 'banana', 'cherry']
  expect(list).toContain('banana')
  expect(list).toHaveLength(3)
})

test('exceptions', () => {
  expect(() => {
    throw new Error('Error!')
  }).toThrow('Error!')
})
```

### 非同期テスト

```javascript
// async.test.js
// Promise
test('fetches user data', () => {
  return fetchUser(1).then(data => {
    expect(data.name).toBe('Alice')
  })
})

// async/await
test('fetches user data async', async () => {
  const data = await fetchUser(1)
  expect(data.name).toBe('Alice')
})

// resolves/rejects
test('fetches user data with resolves', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ name: 'Alice' })
})

test('fetch fails with rejects', async () => {
  await expect(fetchUser(999)).rejects.toThrow('Not found')
})
```

### モック関数

```javascript
// mock.test.js
test('mock function', () => {
  const mockFn = jest.fn(x => x * 2)

  expect(mockFn(5)).toBe(10)
  expect(mockFn).toHaveBeenCalledWith(5)
  expect(mockFn).toHaveBeenCalledTimes(1)
})

test('mock implementation', () => {
  const mockFn = jest.fn()
  mockFn.mockReturnValue(42)

  expect(mockFn()).toBe(42)
})

test('mock promises', async () => {
  const mockFn = jest.fn()
  mockFn.mockResolvedValue({ id: 1, name: 'Alice' })

  const result = await mockFn()
  expect(result.name).toBe('Alice')
})
```

### モジュールモック

```javascript
// api.js
const axios = require('axios')

async function fetchUser(id) {
  const response = await axios.get(`/api/users/${id}`)
  return response.data
}

module.exports = fetchUser

// api.test.js
jest.mock('axios')
const axios = require('axios')
const fetchUser = require('./api')

test('fetches user from API', async () => {
  axios.get.mockResolvedValue({
    data: { id: 1, name: 'Alice' }
  })

  const user = await fetchUser(1)
  expect(user.name).toBe('Alice')
  expect(axios.get).toHaveBeenCalledWith('/api/users/1')
})
```

### React コンポーネントテスト

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

```javascript
// Button.jsx
import React from 'react'

function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>
}

export default Button

// Button.test.jsx
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import Button from './Button'

test('renders button with text', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})

test('calls onClick when clicked', () => {
  const handleClick = jest.fn()
  render(<Button onClick={handleClick}>Click me</Button>)

  fireEvent.click(screen.getByText('Click me'))
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

### スナップショットテスト

```javascript
// Component.test.jsx
import { render } from '@testing-library/react'
import Component from './Component'

test('matches snapshot', () => {
  const { container } = render(<Component name="Alice" />)
  expect(container.firstChild).toMatchSnapshot()
})
```

### Setup/Teardown

```javascript
// setup.test.js
beforeAll(() => {
  console.log('Run once before all tests')
})

afterAll(() => {
  console.log('Run once after all tests')
})

beforeEach(() => {
  console.log('Run before each test')
})

afterEach(() => {
  console.log('Run after each test')
})

test('test 1', () => {
  expect(true).toBe(true)
})

test('test 2', () => {
  expect(false).toBe(false)
})
```

### 設定ファイル

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/index.js'
  ],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '\\.(css|less|scss)$': 'identity-obj-proxy',
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest'
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Jest** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **ゼロコンフィグ**: 設定不要
3. **高速**: 並列実行
4. **モック**: 強力なモック機能
5. **React推奨**: React公式推奨

## デメリット

1. **重い**: 起動遅い
2. **メモリ**: メモリ消費大
3. **設定**: 高度設定複雑
4. **ESM**: ESM対応限定的

## 公式リンク

- **公式サイト**: [https://jestjs.io/](https://jestjs.io/)
- **ドキュメント**: [https://jestjs.io/docs/getting-started](https://jestjs.io/docs/getting-started)

## 関連ドキュメント

- [テストフレームワークツール一覧](../テストフレームワークツール/)
- [Vitest](./Vitest.md)
- [Mocha](./Mocha.md)

---

**カテゴリ**: テストフレームワークツール
**対象工程**: 単体テスト・統合テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
