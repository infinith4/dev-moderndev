# Playwright

## 概要

Playwright は、Microsoft が開発したオープンソースのブラウザ自動化・E2E（End-to-End）テストフレームワークです。Chromium、Firefox、WebKit（Safari）をサポートし、クロスブラウザテストを単一の API で実行できます。高速で信頼性の高い自動テスト、自動待機機能、強力なデバッグツールにより、モダンな Web アプリケーションのテスト自動化を効率化します。

## 主な特徴

### 1. クロスブラウザ対応
- Chromium（Chrome、Edge）
- Firefox
- WebKit（Safari）
- 単一の API で全ブラウザをサポート
- モバイルエミュレーション

### 2. 自動待機
- 要素の表示を自動的に待機
- ネットワークリクエストの完了を待機
- アニメーションの完了を待機
- 明示的な sleep 不要

### 3. 強力なセレクタ
- CSS、XPath、テキスト、役割（role）ベース
- 連鎖セレクタ
- React、Vue のコンポーネントセレクタ
- カスタムセレクタエンジン

### 4. ネットワーク制御
- リクエスト/レスポンスのインターセプト
- モックレスポンス
- ネットワーク条件のシミュレーション
- WebSocket のテスト

### 5. 並列実行
- テストの並列実行
- ワーカープロセスによる分離
- シャーディング
- 高速なテスト実行

### 6. 優れた開発者体験
- コードジェネレーター（Codegen）
- インスペクター
- トレースビューアー
- タイムトラベルデバッグ

## 主な機能

### テスト機能

| 機能 | 説明 |
|------|------|
| ブラウザコンテキスト | 独立したセッション管理 |
| マルチタブ | 複数タブ・ウィンドウの操作 |
| iFrame | iFrame 内の要素操作 |
| ファイルアップロード | ファイル選択のテスト |
| ダウンロード | ファイルダウンロードの検証 |
| 認証 | HTTP認証、Cookie管理 |
| ジオロケーション | 位置情報のシミュレーション |
| パーミッション | ブラウザパーミッションの制御 |

### アサーション機能

| 機能 | 説明 |
|------|------|
| Web-First Assertions | 自動リトライ付きアサーション |
| Visual Comparison | スクリーンショット比較 |
| Accessibility Testing | アクセシビリティチェック |
| Custom Matchers | カスタムマッチャー |

### レポート機能

| 機能 | 説明 |
|------|------|
| HTML Reporter | インタラクティブなHTMLレポート |
| JUnit Reporter | CI/CD統合用XMLレポート |
| JSON Reporter | プログラマティックな解析用 |
| トレースビューアー | 詳細な実行履歴の可視化 |

## インストールとセットアップ

### Node.js プロジェクト

```bash
# 新規プロジェクトの作成
npm init playwright@latest

# 既存プロジェクトに追加
npm install -D @playwright/test

# ブラウザのインストール
npx playwright install

# 特定のブラウザのみ
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

### TypeScript プロジェクト

```bash
# TypeScript サポート付きでインストール
npm init playwright@latest -- --typescript

# 既存プロジェクトに追加
npm install -D @playwright/test typescript
npx tsc --init
```

### Python

```bash
# pip でインストール
pip install playwright

# ブラウザのインストール
playwright install

# 特定のブラウザのみ
playwright install chromium
```

### Java

```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.microsoft.playwright</groupId>
    <artifactId>playwright</artifactId>
    <version>1.40.0</version>
</dependency>
```

```bash
# CLI のインストール
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

### .NET (C#)

```bash
# NuGet パッケージのインストール
dotnet add package Microsoft.Playwright

# ブラウザのインストール
pwsh bin/Debug/net6.0/playwright.ps1 install
```

## 基本的な使い方

### テストの作成（TypeScript/JavaScript）

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test';

test('基本的なナビゲーション', async ({ page }) => {
  // ページに移動
  await page.goto('https://example.com');

  // タイトルを検証
  await expect(page).toHaveTitle(/Example Domain/);

  // リンクをクリック
  await page.click('a[href="/about"]');

  // URLを検証
  await expect(page).toHaveURL(/.*about/);
});

test('フォーム入力', async ({ page }) => {
  await page.goto('https://example.com/form');

  // 入力フィールドに値を入力
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'secret123');

  // チェックボックスをチェック
  await page.check('#remember-me');

  // ドロップダウンを選択
  await page.selectOption('#country', 'Japan');

  // ボタンをクリック
  await page.click('button[type="submit"]');

  // 成功メッセージを検証
  await expect(page.locator('.success-message')).toBeVisible();
  await expect(page.locator('.success-message')).toHaveText('Login successful');
});

test('API モック', async ({ page }) => {
  // APIレスポンスをモック
  await page.route('**/api/users', (route) => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([
        { id: 1, name: 'John Doe' },
        { id: 2, name: 'Jane Smith' }
      ])
    });
  });

  await page.goto('https://example.com/users');

  // モックデータが表示されることを検証
  await expect(page.locator('.user-list')).toContainText('John Doe');
  await expect(page.locator('.user-list')).toContainText('Jane Smith');
});
```

### セレクタの使い方

```typescript
// CSS セレクタ
await page.click('button.submit');
await page.click('#login-button');

// テキストセレクタ
await page.click('text=Login');
await page.click('text=/Log.*in/i'); // 正規表現

// 役割（Role）ベースセレクタ（推奨）
await page.click('role=button[name="Login"]');
await page.click('role=textbox[name="Username"]');

// XPath
await page.click('xpath=//button[@type="submit"]');

// 連鎖セレクタ
await page.click('.modal >> button.submit');
await page.click('article:has-text("News") >> role=button');

// Playwright 推奨のセレクタ（getByRole, getByText 等）
await page.getByRole('button', { name: 'Login' }).click();
await page.getByText('Welcome').click();
await page.getByLabel('Username').fill('testuser');
await page.getByPlaceholder('Enter your email').fill('test@example.com');
await page.getByTestId('submit-button').click();
```

### アサーション

```typescript
// Web-First Assertions（自動リトライ）
await expect(page).toHaveTitle(/Expected Title/);
await expect(page).toHaveURL(/expected-url/);

await expect(page.locator('.message')).toBeVisible();
await expect(page.locator('.message')).toBeHidden();
await expect(page.locator('.message')).toHaveText('Success');
await expect(page.locator('.message')).toContainText('Success');
await expect(page.locator('.count')).toHaveCount(5);

await expect(page.locator('#checkbox')).toBeChecked();
await expect(page.locator('#input')).toHaveValue('expected value');
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('button')).toBeDisabled();

// スクリーンショット比較
await expect(page).toHaveScreenshot('homepage.png');
await expect(page.locator('.header')).toHaveScreenshot('header.png');
```

### 設定ファイル

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // テストディレクトリ
  testDir: './tests',

  // タイムアウト
  timeout: 30000,

  // リトライ
  retries: process.env.CI ? 2 : 0,

  // 並列実行のワーカー数
  workers: process.env.CI ? 1 : undefined,

  // レポーター
  reporter: [
    ['html'],
    ['junit', { outputFile: 'results.xml' }],
    ['json', { outputFile: 'results.json' }]
  ],

  // 共通の use オプション
  use: {
    // ベース URL
    baseURL: 'http://localhost:3000',

    // トレース
    trace: 'on-first-retry',

    // スクリーンショット
    screenshot: 'only-on-failure',

    // ビデオ
    video: 'retain-on-failure',

    // ヘッドレスモード
    headless: true,
  },

  // プロジェクト（ブラウザ設定）
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // 開発サーバーの起動
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

## 高度な機能

### Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.getByLabel('Username');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test('ログインテスト', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('testuser', 'password123');

  await expect(page).toHaveURL(/dashboard/);
});
```

### フィクスチャ

```typescript
// fixtures/test-base.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

type MyFixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // ログイン処理
    await page.goto('/login');
    await page.fill('#username', 'testuser');
    await page.fill('#password', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');

    await use(page);
  },
});

export { expect } from '@playwright/test';

// tests/dashboard.spec.ts
import { test, expect } from './fixtures/test-base';

test('ダッシュボードテスト', async ({ authenticatedPage }) => {
  // 既にログイン済みの状態でテスト開始
  await expect(authenticatedPage.locator('h1')).toHaveText('Dashboard');
});
```

### ネットワークインターセプト

```typescript
test('API インターセプト', async ({ page }) => {
  // リクエストをブロック
  await page.route('**/*.{png,jpg,jpeg}', (route) => route.abort());

  // レスポンスを変更
  await page.route('**/api/user', (route) => {
    const response = route.fetch();
    response.then((res) => {
      const body = res.json();
      body.then((json) => {
        json.name = 'Modified Name';
        route.fulfill({ response: res, json });
      });
    });
  });

  // リクエスト/レスポンスのログ
  page.on('request', (request) => {
    console.log('>>', request.method(), request.url());
  });

  page.on('response', (response) => {
    console.log('<<', response.status(), response.url());
  });

  await page.goto('https://example.com');
});
```

### ストレージステート（認証の永続化）

```typescript
// auth.setup.ts - 認証セットアップ
import { test as setup } from '@playwright/test';

setup('認証', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');

  // ストレージステートを保存
  await page.context().storageState({ path: 'auth.json' });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'auth.json', // 保存した認証情報を使用
      },
      dependencies: ['setup'], // setup を先に実行
    },
  ],
});
```

### トレース

```typescript
// テスト実行時にトレースを有効化
// playwright.config.ts
use: {
  trace: 'on-first-retry', // 最初のリトライ時にトレースを記録
  // または
  trace: 'on', // 常にトレースを記録
}

// トレースビューアーの起動
npx playwright show-trace trace.zip
```

### コンポーネントテスト

```typescript
// tests/Button.spec.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import Button from './Button';

test('ボタンのクリック', async ({ mount }) => {
  let clicked = false;
  const component = await mount(
    <Button onClick={() => { clicked = true; }}>
      Click me
    </Button>
  );

  await component.click();
  expect(clicked).toBe(true);
});
```

## コードジェネレーター

```bash
# コードジェネレーターの起動
npx playwright codegen https://example.com

# 特定のブラウザで起動
npx playwright codegen --browser=firefox https://example.com

# モバイルエミュレーション
npx playwright codegen --device="iPhone 12" https://example.com

# 認証付き
npx playwright codegen --save-storage=auth.json https://example.com

# 保存した認証情報を使用
npx playwright codegen --load-storage=auth.json https://example.com
```

## テストの実行

```bash
# すべてのテストを実行
npx playwright test

# 特定のファイルを実行
npx playwright test tests/login.spec.ts

# ヘッドモードで実行（ブラウザが表示される）
npx playwright test --headed

# 特定のブラウザで実行
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# デバッグモード
npx playwright test --debug

# UI モード（インタラクティブ）
npx playwright test --ui

# 並列実行のワーカー数を指定
npx playwright test --workers=4

# 失敗したテストのみ再実行
npx playwright test --last-failed

# レポーターの指定
npx playwright test --reporter=html
npx playwright test --reporter=dot

# HTMLレポートの表示
npx playwright show-report
```

## CI/CD 統合

### GitHub Actions

```yaml
name: Playwright Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - uses: actions/setup-node@v3
      with:
        node-version: 18

    - name: Install dependencies
      run: npm ci

    - name: Install Playwright Browsers
      run: npx playwright install --with-deps

    - name: Run Playwright tests
      run: npx playwright test

    - uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30

    - uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: test-results/
        retention-days: 30
```

### GitLab CI

```yaml
stages:
  - test

playwright_tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  script:
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
      - test-results/
    expire_in: 30 days
  only:
    - main
    - merge_requests
```

### Docker

```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# テストを実行
CMD ["npx", "playwright", "test"]
```

```bash
# Docker でテストを実行
docker build -t playwright-tests .
docker run --rm playwright-tests

# または docker-compose
# docker-compose.yml
version: '3'
services:
  playwright:
    image: mcr.microsoft.com/playwright:v1.40.0-focal
    volumes:
      - .:/app
    working_dir: /app
    command: npx playwright test
```

## Python での使用

```python
# tests/test_example.py
from playwright.sync_api import Page, expect

def test_basic_navigation(page: Page):
    page.goto("https://example.com")
    expect(page).to_have_title("Example Domain")

def test_form_submission(page: Page):
    page.goto("https://example.com/form")
    page.fill("#username", "testuser")
    page.fill("#password", "secret123")
    page.click('button[type="submit"]')
    expect(page.locator(".success-message")).to_be_visible()

# pytest で実行
pytest tests/

# 特定のブラウザで実行
pytest tests/ --browser firefox
pytest tests/ --browser webkit

# ヘッドモード
pytest tests/ --headed
```

## ベストプラクティス

### 1. Web-First Assertions を使用

```typescript
// ❌ 悪い例
expect(await page.locator('.message').textContent()).toBe('Success');

// ✅ 良い例（自動リトライあり）
await expect(page.locator('.message')).toHaveText('Success');
```

### 2. 役割ベースセレクタを優先

```typescript
// ❌ CSS セレクタ（脆弱）
await page.click('.btn-primary');

// ✅ 役割ベースセレクタ（堅牢）
await page.getByRole('button', { name: 'Submit' }).click();
```

### 3. Page Object Model を使用

```typescript
// テストロジックとページ操作を分離
// 保守性と再利用性が向上
```

### 4. 並列実行を活用

```typescript
// playwright.config.ts
workers: process.env.CI ? 4 : undefined,
```

### 5. トレースとスクリーンショットを記録

```typescript
use: {
  trace: 'on-first-retry',
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

## トラブルシューティング

### よくある問題と解決策

#### 1. タイムアウトエラー

```typescript
// タイムアウトを延長
await page.goto('https://example.com', { timeout: 60000 });

// 特定の要素のタイムアウト
await expect(page.locator('.slow-element')).toBeVisible({ timeout: 10000 });
```

#### 2. 要素が見つからない

```typescript
// 待機を追加
await page.waitForSelector('.dynamic-content');

// または Web-First Assertions を使用（自動待機）
await expect(page.locator('.dynamic-content')).toBeVisible();
```

#### 3. 認証の問題

```typescript
// ストレージステートを使用
// または各テストで認証情報をセットアップ
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://playwright.dev/
- ドキュメント: https://playwright.dev/docs/intro
- API リファレンス: https://playwright.dev/docs/api/class-playwright
- GitHub: https://github.com/microsoft/playwright

### コミュニティ
- Discord: https://aka.ms/playwright/discord
- Stack Overflow: https://stackoverflow.com/questions/tagged/playwright
- Twitter: @playwrightweb

### チュートリアル
- Getting Started: https://playwright.dev/docs/intro
- Best Practices: https://playwright.dev/docs/best-practices
- Video Tutorials: https://www.youtube.com/@Playwrightdev

## まとめ

Playwright は、以下の場面で特に有用です:

1. **クロスブラウザE2Eテスト** - 単一APIで複数ブラウザをサポート
2. **高速で安定したテスト** - 自動待機、並列実行による効率化
3. **モダンWebアプリのテスト** - SPA、PWA、モバイルアプリの自動化
4. **CI/CD統合** - Docker対応、豊富なレポート機能

自動待機、強力なセレクタ、優れた開発者体験により、信頼性の高いE2Eテストを効率的に構築できます。
