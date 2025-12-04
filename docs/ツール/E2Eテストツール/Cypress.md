# Cypress

## 概要

Cypressは、JavaScriptベースのE2E（End-to-End）テストフレームワークです。ブラウザ内実行、リアルタイムリロード、タイムトラベルデバッグ、自動待機により、React、Vue、Angular等のモダンWebアプリケーションの統合テストを効率化します。Cypress Cloud（旧Dashboard）、並列実行、スクリーンショット・ビデオ録画でCI/CD統合をサポートします。

## 主な機能

### 1. E2Eテスト
- **ブラウザ内実行**: Chrome、Edge、Firefox
- **自動待機**: 要素出現待機
- **リトライ**: 自動リトライ

### 2. 開発体験
- **Test Runner**: GUIテストランナー
- **タイムトラベル**: 実行履歴確認
- **リアルタイムリロード**: コード変更即反映

### 3. デバッグ
- **スクリーンショット**: 失敗時自動撮影
- **ビデオ録画**: テスト実行録画
- **Chrome DevTools**: ブラウザデバッグ

### 4. CI/CD
- **並列実行**: 複数マシン
- **Cypress Cloud**: テスト結果ダッシュボード

## 利用方法

### インストール

```bash
npm install --save-dev cypress

# 初期化
npx cypress open
```

### テストコード

```javascript
// cypress/e2e/login.cy.js
describe('Login Test', () => {
  it('should login successfully', () => {
    cy.visit('https://example.com/login')
    
    cy.get('#username').type('testuser')
    cy.get('#password').type('password123')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/dashboard')
    cy.contains('Welcome, testuser').should('be.visible')
  })
})
```

### 実行

```bash
# GUIモード
npx cypress open

# ヘッドレスモード
npx cypress run

# 特定ブラウザ
npx cypress run --browser chrome
```

### CI/CD統合

```yaml
# .github/workflows/cypress.yml
name: Cypress Tests

on: [push]

jobs:
  cypress-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: cypress-io/github-action@v5
        with:
          start: npm start
          wait-on: 'http://localhost:3000'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Cypress (OSS)** | 🟢 完全無料 | オープンソース、MIT License |
| **Cypress Cloud** | 💰 $75/月〜 | 並列実行、ダッシュボード |

## メリット

1. **完全無料**: オープンソース
2. **開発者体験**: 優れたDX
3. **自動待機**: 待機コード不要
4. **デバッグ**: タイムトラベル
5. **モダン**: React、Vue対応

## デメリット

1. **JavaScript専用**: JavaScriptのみ
2. **クロスブラウザ**: Safari非対応
3. **並列実行**: Cloud課金
4. **学習曲線**: 独自API

## 公式リンク

- **公式サイト**: [https://www.cypress.io/](https://www.cypress.io/)
- **ドキュメント**: [https://docs.cypress.io/](https://docs.cypress.io/)

## 関連ドキュメント

- [E2Eテストツール一覧](../E2Eテストツール/)
- [Playwright](./Playwright.md)
- [Selenium](./Selenium.md)

---

**カテゴリ**: E2Eテストツール  
**対象工程**: E2Eテスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
