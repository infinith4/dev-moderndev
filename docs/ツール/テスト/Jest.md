# Jest

## 概要

Jestは、Meta（旧Facebook）が開発したJavaScript/TypeScriptのための包括的なテストフレームワークです。ゼロコンフィグで動作し、高速な並列テスト実行、組み込みのモック機能、スナップショットテスト、コードカバレッジレポートなど、モダンなフロントエンド開発に必要な機能を全て備えています。React、Vue.js、Angular等の主要フレームワークに対応し、特にReactとの親和性が高いです。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Jest** |  無料 | オープンソース、無制限利用、MIT License |

**注意**: Jestは無料のオープンソースプロジェクトです。商用利用も制限なく可能です。

## メリット・デメリット

### メリット
-  **ゼロコンフィグ**: 初期設定なしで即座に使える
-  **無料**: オープンソース、商用利用も無料
-  **高速**: 並列実行、インテリジェントなテストランにより高速
-  **オールインワン**: アサーション、モック、カバレッジが全て組み込み
-  **スナップショットテスト**: UI変更を簡単に検出
-  **監視モード**: ファイル変更を検知して自動再実行
-  **React統合**: React Testing Libraryと完全統合
-  **TypeScript対応**: tsupport標準サポート

### デメリット
-  **JavaScript/TypeScript専用**: 他言語では使用不可
-  **設定の複雑さ**: 高度な設定は複雑になりがち
-  **ブラウザ環境**: 実際のブラウザではなくjsdomで動作（E2Eには不向き）
-  **学習コスト**: モック機能が強力な分、使いこなすには習熟が必要

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | ユニットテスト、コンポーネントテスト | テストコード、スナップショット |
| **9. テスト（アプリケーション）** | 自動テスト実行、リグレッションテスト | テストレポート、カバレッジレポート |

## 基本的な利用方法

### 1. インストール

```bash
# npm
npm install --save-dev jest

# yarn
yarn add --dev jest

# TypeScript対応
npm install --save-dev jest @types/jest ts-jest

# React対応
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# package.jsonにスクリプト追加
# {
#   "scripts": {
#     "test": "jest",
#     "test:watch": "jest --watch",
#     "test:coverage": "jest --coverage"
#   }
# }
```

### 2. 基本的なテストの記述

```javascript
// calculator.js
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export function divide(a, b) {
  if (b === 0) {
    throw new Error('Division by zero');
  }
  return a / b;
}

// calculator.test.js
import { add, subtract, divide } from './calculator';

describe('Calculator', () => {
  test('adds 2 + 3 to equal 5', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('subtracts 5 - 3 to equal 2', () => {
    expect(subtract(5, 3)).toBe(2);
  });

  test('divides 10 / 2 to equal 5', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('throws error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });
});
```

### 3. テストの実行

```bash
# 全テストを実行
npm test

# 監視モード（ファイル変更を検知して自動再実行）
npm run test:watch

# カバレッジレポート生成
npm run test:coverage

# 特定のファイルのみ実行
jest calculator.test.js

# テスト名でフィルタリング
jest -t "adds"

# 変更されたファイルのテストのみ実行
jest --onlyChanged
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: テスト駆動開発（TDD）、コンポーネントの品質保証

**活用方法**:
- ユニットテストの作成
- Reactコンポーネントのテスト
- モックを使った非同期処理のテスト
- スナップショットテストでUI変更検出

**実装例（Reactコンポーネントテスト）**:
```javascript
// Button.jsx
import React from 'react';

export function Button({ onClick, children, disabled }) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

// Button.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Button } from './Button';

describe('Button Component', () => {
  test('renders button with text', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
  });

  test('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('does not call onClick when disabled', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} disabled>Click me</Button>);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(handleClick).not.toHaveBeenCalled();
    expect(button).toBeDisabled();
  });
});
```

**非同期処理のテスト**:
```javascript
// api.js
export async function fetchUser(userId) {
  const response = await fetch(`https://api.example.com/users/${userId}`);
  if (!response.ok) {
    throw new Error('User not found');
  }
  return response.json();
}

// api.test.js
import { fetchUser } from './api';

// グローバルfetchをモック化
global.fetch = jest.fn();

describe('API', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('fetches user successfully', async () => {
    const mockUser = { id: 1, name: 'John Doe' };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const user = await fetchUser(1);

    expect(user).toEqual(mockUser);
    expect(fetch).toHaveBeenCalledWith('https://api.example.com/users/1');
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  test('throws error when user not found', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
    });

    await expect(fetchUser(999)).rejects.toThrow('User not found');
  });
});
```

**モック関数の活用**:
```javascript
// モック関数の作成
const mockFn = jest.fn();

// 戻り値の設定
mockFn.mockReturnValue(42);
mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2);

// Promiseを返すモック
mockFn.mockResolvedValue('success');
mockFn.mockRejectedValue(new Error('failed'));

// 実装をモック
mockFn.mockImplementation((x) => x * 2);

// モジュール全体をモック
jest.mock('./userService');
import { UserService } from './userService';
UserService.getUser = jest.fn().mockResolvedValue({ id: 1, name: 'John' });

// 部分的なモック
jest.mock('./config', () => ({
  ...jest.requireActual('./config'),
  apiUrl: 'http://test.example.com',
}));

// アサーション
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('last arg');
expect(mockFn).toHaveReturnedWith(42);
```

**スナップショットテスト**:
```javascript
// Card.jsx
export function Card({ title, description }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}

// Card.test.jsx
import { render } from '@testing-library/react';
import { Card } from './Card';

test('Card renders correctly', () => {
  const { container } = render(
    <Card title="Test Title" description="Test Description" />
  );

  // 初回実行時にスナップショットを保存
  // 2回目以降は保存されたスナップショットと比較
  expect(container.firstChild).toMatchSnapshot();
});

// スナップショットの更新
// npm test -- -u
```

**パラメータ化テスト（test.each）**:
```javascript
describe('Password Validator', () => {
  test.each([
    ['Pass123!', true],
    ['SecureP@ssw0rd', true],
    ['MyP@ssw0rd123', true],
    ['short', false],
    ['nouppercase123!', false],
    ['NOLOWERCASE123!', false],
  ])('validates password "%s" as %s', (password, expected) => {
    expect(isValidPassword(password)).toBe(expected);
  });
});

// オブジェクト配列での記述
describe('User Creation', () => {
  test.each([
    { username: 'admin', email: 'admin@example.com', valid: true },
    { username: 'user', email: 'user@example.com', valid: true },
    { username: 'guest', email: '', valid: false },
  ])('creates user with $username and $email: $valid', ({ username, email, valid }) => {
    const user = new User(username, email);
    expect(user.isValid()).toBe(valid);
  });
});
```

**セットアップとティアダウン**:
```javascript
describe('Database Tests', () => {
  let database;

  // 全テスト実行前に1回だけ実行
  beforeAll(async () => {
    database = await connectDatabase();
  });

  // 各テスト実行前に実行
  beforeEach(async () => {
    await database.clearAll();
  });

  // 各テスト実行後に実行
  afterEach(async () => {
    // クリーンアップ
  });

  // 全テスト実行後に1回だけ実行
  afterAll(async () => {
    await database.disconnect();
  });

  test('inserts user', async () => {
    await database.insert({ name: 'John' });
    const users = await database.findAll();
    expect(users).toHaveLength(1);
  });
});
```

---

### 9. テスト（アプリケーション）での活用

**目的**: CI/CDでの自動テスト、品質メトリクスの取得

**活用方法**:
- カバレッジ測定
- CI/CDパイプライン統合
- テストレポート生成
- パフォーマンス監視

**Jest設定ファイル（jest.config.js）**:
```javascript
module.exports = {
  // テスト環境
  testEnvironment: 'jsdom', // または 'node'

  // セットアップファイル
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // モジュールパスのマッピング
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },

  // トランスフォーム
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
  },

  // カバレッジ設定
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  // テストファイルのパターン
  testMatch: [
    '**/__tests__/**/*.(test|spec).(js|jsx|ts|tsx)',
    '**/*.(test|spec).(js|jsx|ts|tsx)',
  ],

  // 除外パターン
  testPathIgnorePatterns: ['/node_modules/', '/dist/'],

  // モジュール拡張子
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json'],
};
```

**カバレッジレポート**:
```bash
# カバレッジ測定
npm run test:coverage

# カバレッジしきい値チェック
# jest.config.jsのcoverageThresholdで設定

# 特定のファイルのカバレッジ
jest --coverage --collectCoverageFrom='src/components/**/*.{js,jsx}'

# HTMLレポート生成（coverage/lcov-report/index.html）
# 自動的に生成される
```

**CI/CD統合（GitHub Actions）**:
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 21]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage --ci

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

      - name: Archive test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: |
            coverage/
            junit.xml
```

**テストレポート生成**:
```javascript
// jest.config.js
module.exports = {
  reporters: [
    'default',
    [
      'jest-junit',
      {
        outputDirectory: 'test-results',
        outputName: 'junit.xml',
      },
    ],
    [
      'jest-html-reporter',
      {
        pageTitle: 'Test Report',
        outputPath: 'test-results/test-report.html',
      },
    ],
  ],
};

// インストール
// npm install --save-dev jest-junit jest-html-reporter
```

**パフォーマンステスト**:
```javascript
describe('Performance Tests', () => {
  test('function executes within time limit', () => {
    const start = performance.now();
    const result = expensiveOperation();
    const end = performance.now();

    expect(end - start).toBeLessThan(1000); // 1秒以内
  });

  test('handles large dataset efficiently', () => {
    const largeArray = Array.from({ length: 10000 }, (_, i) => i);

    const start = performance.now();
    const result = processLargeArray(largeArray);
    const end = performance.now();

    expect(result).toHaveLength(10000);
    expect(end - start).toBeLessThan(100); // 100ms以内
  });
});
```

**並列実行とパフォーマンス最適化**:
```bash
# 並列実行のワーカー数を指定
jest --maxWorkers=4

# CPUコア数の50%を使用
jest --maxWorkers=50%

# キャッシュクリア
jest --clearCache

# 失敗したテストのみ再実行
jest --onlyFailures

# 関連するテストのみ実行（変更検出）
jest --onlyChanged
```

## 公式ドキュメント

- [Jest 公式サイト](https://jestjs.io/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Jest API Reference](https://jestjs.io/docs/api)
- [Jest GitHub Repository](https://github.com/facebook/jest)
- [Jest Cheat Sheet](https://github.com/sapegin/jest-cheat-sheet)

## 学習リソース

### チュートリアル
- [Jest Getting Started](https://jestjs.io/docs/getting-started)
- [Testing React with Jest and Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Jest Tutorial by Valentin Iuga](https://www.valentinog.com/blog/jest/)

### 書籍
- "Testing JavaScript Applications" by Lucas da Costa (Manning)
- "React Testing Cookbook" by the React team

### 動画・コース
- [Jest Tutorial for Beginners](https://www.youtube.com/results?search_query=jest+tutorial)
- [Testing JavaScript with Kent C. Dodds](https://testingjavascript.com/)
- [Udemy - Jest Testing Course](https://www.udemy.com/topic/jest/)

### コミュニティ
- [Jest Discord](https://discord.gg/j6FKKQQrW9)
- [Stack Overflow - Jest](https://stackoverflow.com/questions/tagged/jestjs)
- [Jest GitHub Discussions](https://github.com/facebook/jest/discussions)

## 関連リンク

### 関連ツール
- [React Testing Library](https://testing-library.com/react) - Reactコンポーネントテスト
- [@testing-library/jest-dom](https://github.com/testing-library/jest-dom) - カスタムマッチャー
- [ts-jest](https://kulshekhar.github.io/ts-jest/) - TypeScript対応
- [babel-jest](https://jestjs.io/docs/getting-started#using-babel) - Babel変換
- [jest-junit](https://github.com/jest-community/jest-junit) - JUnitレポート出力

### 便利なライブラリ
- [jest-extended](https://jest-extended.jestcommunity.dev/) - 追加マッチャー
- [jest-dom](https://testing-library.com/docs/ecosystem-jest-dom/) - DOM用マッチャー
- [jest-axe](https://github.com/nickcolley/jest-axe) - アクセシビリティテスト
- [jest-image-snapshot](https://github.com/americanexpress/jest-image-snapshot) - ビジュアルリグレッションテスト
- [msw](https://mswjs.io/) - APIモック（Service Worker）

### ベストプラクティス
- [Jest Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)
- [Common Testing Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Effective Snapshot Testing](https://kentcdodds.com/blog/effective-snapshot-testing)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

