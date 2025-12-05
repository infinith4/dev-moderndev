# Cypress

## 概要

Cypressは、モダンなWebアプリケーションのための次世代E2E（エンドツーエンド）テストフレームワークです。2017年に登場し、Seleniumの課題を解決するために設計されました。ブラウザ内で直接実行されるため高速で、自動待機機能、タイムトラベルデバッグ、リアルタイムリロード等の開発者フレンドリーな機能を備えています。JavaScript/TypeScriptで記述し、主にReact、Vue.js、Angular等のSPAに最適化されています。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Cypress (OSS)** | 🟢 完全無料 | オープンソース、ローカル実行、無制限テスト |
| **Cypress Cloud Free** | 🟢 無料 | 500テスト結果/月、3ユーザー、30日間のデータ保持 |
| **Cypress Cloud Starter** | 💰 $75/月 | 5,000テスト結果/月、5ユーザー、90日間保持 |
| **Cypress Cloud Team** | 💰 $300/月 | 20,000テスト結果/月、20ユーザー、1年間保持 |
| **Cypress Cloud Business** | 💰 $600/月 | 100,000テスト結果/月、無制限ユーザー、2年間保持、SSO |
| **Cypress Cloud Enterprise** | 💰 見積もり必要 | 無制限、専用サポート、SLA |

**注意**: オープンソース版は完全無料。Cypress Cloud（旧Dashboard）は録画・分析・並列実行等の追加機能を提供。

## メリット・デメリット

### メリット
- ✅ **完全無料（OSS版）**: オープンソース、商用利用も無料
- ✅ **高速**: ブラウザ内で直接実行、Seleniumより圧倒的に速い
- ✅ **自動待機**: 要素が表示されるまで自動的に待機、明示的なwait不要
- ✅ **タイムトラベル**: 各ステップのスナップショットを保存、デバッグが容易
- ✅ **リアルタイムリロード**: テストコード変更時に自動再実行
- ✅ **優れたUI**: Test Runnerの視覚的なフィードバックが優秀
- ✅ **ネットワークモック**: APIリクエストを簡単にスタブ/モック可能
- ✅ **スクリーンショット/動画**: 失敗時に自動記録

### デメリット
- ❌ **JavaScript/TypeScript専用**: 他言語では使用不可
- ❌ **Chromiumベース**: Chrome/Edge/Electronのみ（Firefoxは実験的）
- ❌ **複数タブ不可**: 単一タブのテストのみ（iframe対応は可能）
- ❌ **サードパーティサイト制限**: 異なるオリジンへのナビゲーションに制約
- ❌ **モバイルブラウザ非対応**: iOS/Androidブラウザでは動作しない

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | コンポーネントテスト、統合テスト | テストコード、スナップショット |
| **9. テスト（アプリケーション）** | E2Eテスト、UIテスト、APIテスト | E2Eテスト結果、動画、スクリーンショット |
| **11. 導入** | 本番環境のスモークテスト | スモークテスト結果 |

## 基本的な利用方法

### 1. インストール

```bash
# npm
npm install --save-dev cypress

# yarn
yarn add --dev cypress

# Cypressを開く
npx cypress open

# package.jsonにスクリプト追加
# {
#   "scripts": {
#     "cypress:open": "cypress open",
#     "cypress:run": "cypress run",
#     "cypress:run:chrome": "cypress run --browser chrome",
#     "cypress:run:headed": "cypress run --headed"
#   }
# }
```

### 2. 基本的なテストの記述

```javascript
// cypress/e2e/login.cy.js
describe('Login Page', () => {
  beforeEach(() => {
    // 各テスト前にログインページを開く
    cy.visit('https://example.com/login');
  });

  it('successfully loads', () => {
    // ページが正しく読み込まれることを確認
    cy.url().should('include', '/login');
    cy.get('h1').should('contain', 'Login');
  });

  it('can login with valid credentials', () => {
    // フォームに入力
    cy.get('#username').type('testuser');
    cy.get('#password').type('SecurePass123!');

    // ログインボタンをクリック
    cy.get('button[type="submit"]').click();

    // ダッシュボードにリダイレクトされることを確認
    cy.url().should('include', '/dashboard');
    cy.get('#dashboard').should('be.visible');
  });

  it('shows error with invalid credentials', () => {
    cy.get('#username').type('invalid');
    cy.get('#password').type('wrong');
    cy.get('button[type="submit"]').click();

    // エラーメッセージが表示されることを確認
    cy.get('.error-message')
      .should('be.visible')
      .and('contain', 'Invalid credentials');
  });
});
```

### 3. Cypressの実行

```bash
# インタラクティブモード（Test Runner）
npm run cypress:open

# ヘッドレスモード（CI/CD向け）
npm run cypress:run

# 特定のブラウザで実行
npm run cypress:run --browser chrome
npm run cypress:run --browser edge
npm run cypress:run --browser electron

# 特定のテストファイルのみ実行
npm run cypress:run --spec "cypress/e2e/login.cy.js"

# 並列実行（Cypress Cloud必須）
npm run cypress:run --parallel --record --key <record-key>
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: コンポーネントテスト、統合テスト、TDD開発

**活用方法**:
- Reactコンポーネントの単体テスト
- カスタムコマンドで再利用性向上
- フィクスチャでテストデータ管理
- APIモックでフロントエンド開発を加速

**実装例（Reactコンポーネントテスト）**:
```javascript
// cypress/component/Button.cy.jsx
import React from 'react';
import { mount } from 'cypress/react';
import Button from '../../src/components/Button';

describe('Button Component', () => {
  it('renders with text', () => {
    mount(<Button>Click me</Button>);
    cy.get('button').should('contain', 'Click me');
  });

  it('calls onClick when clicked', () => {
    const onClickSpy = cy.spy().as('onClickSpy');
    mount(<Button onClick={onClickSpy}>Click me</Button>);

    cy.get('button').click();
    cy.get('@onClickSpy').should('have.been.calledOnce');
  });

  it('is disabled when disabled prop is true', () => {
    mount(<Button disabled>Click me</Button>);
    cy.get('button').should('be.disabled');
  });
});
```

**カスタムコマンド**:
```javascript
// cypress/support/commands.js

// ログインコマンド
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login');
  cy.get('#username').type(username);
  cy.get('#password').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('include', '/dashboard');
});

// APIログイン（より高速）
Cypress.Commands.add('loginByAPI', (username, password) => {
  cy.request('POST', '/api/auth/login', {
    username,
    password,
  }).then((response) => {
    window.localStorage.setItem('authToken', response.body.token);
  });
});

// 使用例
it('can access dashboard after login', () => {
  cy.login('testuser', 'password');
  cy.get('#dashboard').should('be.visible');
});
```

**フィクスチャ（テストデータ）**:
```javascript
// cypress/fixtures/users.json
{
  "validUser": {
    "username": "testuser",
    "password": "SecurePass123!",
    "email": "test@example.com"
  },
  "adminUser": {
    "username": "admin",
    "password": "AdminPass123!",
    "email": "admin@example.com"
  }
}

// テストでの使用
describe('User Registration', () => {
  it('can register with valid data', () => {
    cy.fixture('users').then((users) => {
      const { username, password, email } = users.validUser;

      cy.visit('/register');
      cy.get('#username').type(username);
      cy.get('#email').type(email);
      cy.get('#password').type(password);
      cy.get('button[type="submit"]').click();

      cy.url().should('include', '/welcome');
    });
  });
});
```

**APIモッキング（cy.intercept）**:
```javascript
describe('User List', () => {
  beforeEach(() => {
    // APIレスポンスをモック
    cy.intercept('GET', '/api/users', {
      statusCode: 200,
      body: [
        { id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
      ],
    }).as('getUsers');

    cy.visit('/users');
  });

  it('displays user list', () => {
    // APIリクエストが完了するまで待機
    cy.wait('@getUsers');

    // ユーザーリストが表示されることを確認
    cy.get('.user-list').should('have.length', 2);
    cy.contains('John Doe').should('be.visible');
    cy.contains('Jane Smith').should('be.visible');
  });

  it('handles API error gracefully', () => {
    // エラーレスポンスをモック
    cy.intercept('GET', '/api/users', {
      statusCode: 500,
      body: { error: 'Internal Server Error' },
    }).as('getUsersError');

    cy.visit('/users');
    cy.wait('@getUsersError');

    // エラーメッセージが表示される
    cy.get('.error-message').should('contain', 'Failed to load users');
  });
});
```

---

### 9. テスト（アプリケーション）での活用

**目的**: 包括的なE2Eテスト、クロスブラウザテスト

**活用方法**:
- ユーザーシナリオのテスト
- フォームバリデーションテスト
- ナビゲーションフローテスト
- レスポンシブデザインテスト

**実装例（E2Eシナリオテスト）**:
```javascript
// cypress/e2e/e-commerce.cy.js
describe('E-Commerce User Flow', () => {
  beforeEach(() => {
    // 各テスト前にホームページを開く
    cy.visit('/');

    // ログイン
    cy.loginByAPI('testuser', 'password');
  });

  it('complete purchase flow', () => {
    // 商品を検索
    cy.get('#search-input').type('laptop');
    cy.get('#search-button').click();

    // 検索結果から商品を選択
    cy.contains('.product-card', 'MacBook Pro').click();

    // 商品詳細ページでカートに追加
    cy.get('#add-to-cart').click();
    cy.contains('Added to cart').should('be.visible');

    // カートを開く
    cy.get('#cart-icon').click();
    cy.url().should('include', '/cart');

    // 商品がカートにあることを確認
    cy.contains('MacBook Pro').should('be.visible');
    cy.get('.cart-item').should('have.length', 1);

    // チェックアウトへ進む
    cy.get('#checkout-button').click();
    cy.url().should('include', '/checkout');

    // 配送先情報を入力
    cy.get('#address').type('123 Main St');
    cy.get('#city').type('San Francisco');
    cy.get('#zip').type('94102');

    // 支払い情報を入力（テスト用）
    cy.get('#card-number').type('4242424242424242');
    cy.get('#expiry').type('12/25');
    cy.get('#cvv').type('123');

    // 注文を確定
    cy.get('#place-order').click();

    // 注文完了ページを確認
    cy.url().should('include', '/order-confirmation');
    cy.contains('Order Confirmed').should('be.visible');
    cy.get('#order-number').should('exist');
  });
});
```

**Cypress設定ファイル（cypress.config.js）**:
```javascript
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    setupNodeEvents(on, config) {
      // プラグイン設定
    },

    // ビューポート設定
    viewportWidth: 1280,
    viewportHeight: 720,

    // タイムアウト設定
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 30000,

    // スクリーンショット・動画
    screenshotsFolder: 'cypress/screenshots',
    videosFolder: 'cypress/videos',
    video: true,
    screenshotOnRunFailure: true,

    // テストファイルパターン
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',

    // テスト分離
    testIsolation: true,

    // 並列実行設定
    numTestsKeptInMemory: 0,
  },

  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
    specPattern: 'cypress/component/**/*.cy.{js,jsx,ts,tsx}',
  },

  // 環境変数
  env: {
    apiUrl: 'https://api.example.com',
    coverage: false,
  },
});
```

**TypeScript対応**:
```typescript
// cypress/e2e/login.cy.ts
describe('Login Page', () => {
  interface User {
    username: string;
    password: string;
  }

  const validUser: User = {
    username: 'testuser',
    password: 'SecurePass123!',
  };

  it('can login with valid credentials', () => {
    cy.visit('/login');

    cy.get<HTMLInputElement>('#username').type(validUser.username);
    cy.get<HTMLInputElement>('#password').type(validUser.password);

    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/dashboard');
  });
});
```

**CI/CD統合（GitHub Actions）**:
```yaml
# .github/workflows/cypress.yml
name: Cypress E2E Tests

on: [push, pull_request]

jobs:
  cypress-run:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Cypress run
        uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm start
          wait-on: 'http://localhost:3000'
          browser: chrome
          record: true
          parallel: true
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: cypress-screenshots
          path: cypress/screenshots

      - name: Upload videos
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: cypress-videos
          path: cypress/videos
```

---

### 11. 導入での活用

**目的**: 本番環境のスモークテスト、重要フローの検証

**活用方法**:
- デプロイ後のスモークテスト
- クリティカルパスの動作確認
- 本番環境の健全性チェック

**実装例（本番スモークテスト）**:
```javascript
// cypress/e2e/smoke-tests.cy.js
describe('Production Smoke Tests', () => {
  before(() => {
    // 本番環境のURL
    Cypress.config('baseUrl', 'https://app.example.com');
  });

  it('homepage loads successfully', () => {
    cy.visit('/');
    cy.get('body').should('be.visible');
    cy.title().should('not.be.empty');
  });

  it('login page is accessible', () => {
    cy.visit('/login');
    cy.get('#login-form').should('be.visible');
    cy.get('#username').should('exist');
    cy.get('#password').should('exist');
  });

  it('API health check passes', () => {
    cy.request('GET', 'https://api.example.com/health').then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('status', 'ok');
    });
  });

  it('critical user flow works', () => {
    // ログイン
    cy.visit('/login');
    cy.get('#username').type(Cypress.env('PROD_USERNAME'));
    cy.get('#password').type(Cypress.env('PROD_PASSWORD'));
    cy.get('button[type="submit"]').click();

    // ダッシュボードが表示される
    cy.url().should('include', '/dashboard');
    cy.get('#dashboard').should('be.visible');

    // ログアウト
    cy.get('#logout-button').click();
    cy.url().should('include', '/login');
  });
});

// 実行コマンド
// npx cypress run --spec "cypress/e2e/smoke-tests.cy.js" --env PROD_USERNAME=user,PROD_PASSWORD=pass
```

## 公式ドキュメント

- [Cypress 公式サイト](https://www.cypress.io/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Cypress API Reference](https://docs.cypress.io/api/table-of-contents)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Cypress GitHub Repository](https://github.com/cypress-io/cypress)
- [Cypress Cloud](https://www.cypress.io/cloud)

## 学習リソース

### チュートリアル
- [Cypress Getting Started](https://docs.cypress.io/guides/getting-started/installing-cypress)
- [Real World App（サンプルアプリ）](https://github.com/cypress-io/cypress-realworld-app)
- [Cypress Tutorial by Gleb Bahmutov](https://glebbahmutov.com/blog/tags/cypress/)

### 書籍
- "End-to-End Web Testing with Cypress" by Waweru Mwaura (Packt)
- "Cypress Cookbook" by the Cypress team

### 動画・コース
- [Cypress Tutorial for Beginners](https://www.youtube.com/results?search_query=cypress+tutorial)
- [Test Automation University - Cypress](https://testautomationu.applitools.com/cypress-tutorial/)
- [Udemy - Cypress: Web Automation Testing](https://www.udemy.com/topic/cypress/)

### コミュニティ
- [Cypress Discord](https://discord.com/invite/cypress)
- [Stack Overflow - Cypress](https://stackoverflow.com/questions/tagged/cypress)
- [Cypress GitHub Discussions](https://github.com/cypress-io/cypress/discussions)

## 関連リンク

### プラグイン
- [cypress-axe](https://github.com/component-driven/cypress-axe) - アクセシビリティテスト
- [cypress-real-events](https://github.com/dmtrKovalenko/cypress-real-events) - 実際のブラウザイベント
- [@cypress/code-coverage](https://github.com/cypress-io/code-coverage) - コードカバレッジ
- [cypress-file-upload](https://github.com/abramenal/cypress-file-upload) - ファイルアップロード
- [cypress-iframe](https://github.com/kuceb/cypress-iframe) - iframe操作

### 統合ツール
- [Cypress Testing Library](https://testing-library.com/docs/cypress-testing-library/intro/) - Testing Library統合
- [Cypress + Percy](https://docs.percy.io/docs/cypress) - ビジュアルテスト
- [Cypress + Cucumber](https://github.com/badeball/cypress-cucumber-preprocessor) - BDD
- [Cypress + TypeScript](https://docs.cypress.io/guides/tooling/typescript-support)

### ベストプラクティス
- [Best Practices Guide](https://docs.cypress.io/guides/references/best-practices)
- [Selecting Elements](https://docs.cypress.io/guides/references/best-practices#Selecting-Elements)
- [Organizing Tests](https://docs.cypress.io/guides/references/best-practices#Organizing-Tests)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
