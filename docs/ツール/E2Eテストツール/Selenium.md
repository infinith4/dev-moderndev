# Selenium

## 概要

Seleniumは、Webブラウザ自動化テストフレームワークです。WebDriver API、クロスブラウザ対応（Chrome、Firefox、Safari、Edge）、多言語サポート（Java、Python、C#、JavaScript等）により、E2Eテスト、リグレッションテスト、Webスクレイピングを実現します。Selenium Grid、Selenium IDE、クラウドサービス連携で、Web自動化のデファクトスタンダードです。

## 主な機能

### 1. WebDriver
- **ブラウザ操作**: クリック、入力、ナビゲーション
- **要素検索**: ID、CSS Selector、XPath
- **待機**: 明示的待機、暗黙的待機

### 2. クロスブラウザ
- **Chrome**: ChromeDriver
- **Firefox**: GeckoDriver
- **Safari**: SafariDriver
- **Edge**: EdgeDriver

### 3. 多言語
- **Java**: Selenium Java
- **Python**: Selenium Python
- **JavaScript**: Selenium WebDriver for Node.js
- **C#**: Selenium .NET

### 4. Selenium Grid
- **並列実行**: 複数ブラウザ・OS
- **リモート実行**: 分散テスト

## 利用方法

### インストール（Python）

```bash
pip install selenium

# ChromeDriverダウンロード
# https://chromedriver.chromium.org/
```

### Python（基本）

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ドライバー起動
driver = webdriver.Chrome()

# ページ遷移
driver.get("https://example.com")

# 要素検索・操作
username = driver.find_element(By.ID, "username")
username.send_keys("testuser")

password = driver.find_element(By.ID, "password")
password.send_keys("password123")

submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_btn.click()

# 明示的待機
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, "welcome"))
)

assert "Welcome" in element.text

# 終了
driver.quit()
```

### Java

```java
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.By;

public class SeleniumTest {
    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();

        driver.get("https://example.com");

        driver.findElement(By.id("username")).sendKeys("testuser");
        driver.findElement(By.id("password")).sendKeys("password123");
        driver.findElement(By.cssSelector("button[type='submit']")).click();

        String pageTitle = driver.getTitle();
        assert pageTitle.contains("Dashboard");

        driver.quit();
    }
}
```

### JavaScript（Node.js）

```javascript
const { Builder, By, until } = require('selenium-webdriver');

(async function example() {
  let driver = await new Builder().forBrowser('chrome').build();

  try {
    await driver.get('https://example.com');

    await driver.findElement(By.id('username')).sendKeys('testuser');
    await driver.findElement(By.id('password')).sendKeys('password123');
    await driver.findElement(By.css("button[type='submit']")).click();

    await driver.wait(until.titleContains('Dashboard'), 5000);
  } finally {
    await driver.quit();
  }
})();
```

### Selenium Grid（Docker）

```bash
# Hub起動
docker run -d -p 4444:4444 --name selenium-hub selenium/hub

# Chrome Node接続
docker run -d --link selenium-hub:hub selenium/node-chrome

# テスト実行（リモートWebDriver）
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=webdriver.ChromeOptions()
)
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Selenium** | 🟢 完全無料 | オープンソース、Apache License |

## メリット

1. **完全無料**: オープンソース
2. **クロスブラウザ**: 4ブラウザ対応
3. **多言語**: 10+言語
4. **標準**: Web自動化標準
5. **コミュニティ**: 大規模コミュニティ

## デメリット

1. **遅い**: ブラウザ起動遅延
2. **待機**: 明示的待機必要
3. **メンテナンス**: テストメンテコスト高
4. **並列実行**: Grid設定複雑

## 公式リンク

- **公式サイト**: [https://www.selenium.dev/](https://www.selenium.dev/)
- **ドキュメント**: [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/)

## 関連ドキュメント

- [E2Eテストツール一覧](../E2Eテストツール/)
- [Cypress](./Cypress.md)
- [Playwright](./Playwright.md)

---

**カテゴリ**: E2Eテストツール
**対象工程**: E2Eテスト・ブラウザ自動化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
