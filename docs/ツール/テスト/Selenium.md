# Selenium

## 概要

Seleniumは、Webブラウザの自動化を行うオープンソースのテスティングフレームワークです。実際のブラウザ（Chrome、Firefox、Safari、Edge等）を操作してE2E（エンドツーエンド）テストを実行できます。2004年に登場して以来、業界標準のブラウザ自動化ツールとして広く利用されており、Java、Python、C#、Ruby、JavaScript等の複数言語をサポートしています。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Selenium WebDriver** | 🟢 完全無料 | オープンソース、無制限利用、Apache License 2.0 |
| **Selenium Grid** | 🟢 完全無料 | 並列実行、複数ブラウザテスト |
| **Selenium IDE** | 🟢 完全無料 | ブラウザ拡張機能、レコード&プレイバック |

**注意**: Selenium自体は完全無料ですが、クラウドベースの実行環境（Sauce Labs、BrowserStack等）は有料です。

## メリット・デメリット

### メリット
- ✅ **完全無料**: オープンソース、商用利用も無料
- ✅ **実ブラウザ対応**: Chrome、Firefox、Safari、Edge等の実際のブラウザで実行
- ✅ **多言語対応**: Java、Python、C#、Ruby、JavaScript等
- ✅ **クロスブラウザ**: 複数ブラウザで同一テストを実行可能
- ✅ **成熟したエコシステム**: 長年の実績、豊富なドキュメント
- ✅ **柔軟性**: あらゆるWebアプリケーションに対応
- ✅ **並列実行**: Selenium Gridで大規模テスト可能
- ✅ **CI/CD統合**: 主要なCI/CDツールと統合可能

### デメリット
- ❌ **学習曲線**: 初心者には複雑、セットアップに時間がかかる
- ❌ **実行速度**: 実ブラウザを使うため遅い
- ❌ **メンテナンスコスト**: DOM変更に脆弱、テストが壊れやすい
- ❌ **デバッグ困難**: エラー時のデバッグが難しい
- ❌ **非同期処理**: 待機処理の実装が複雑
- ❌ **環境依存**: ブラウザドライバーのバージョン管理が必要

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **9. テスト（アプリケーション）** | E2Eテスト、UIテスト、回帰テスト | E2Eテストコード、テスト結果 |
| **11. 導入** | 本番環境のスモークテスト、受け入れテスト | 受け入れテスト結果 |

## 基本的な利用方法

### 1. インストール

#### Python
```bash
# Selenium WebDriverのインストール
pip install selenium

# ChromeDriverの自動管理（推奨）
pip install webdriver-manager

# 依存関係
# selenium==4.15.2
# webdriver-manager==4.0.1
```

#### Java (Maven)
```xml
<dependencies>
    <dependency>
        <groupId>org.seleniumhq.selenium</groupId>
        <artifactId>selenium-java</artifactId>
        <version>4.15.0</version>
    </dependency>
    <dependency>
        <groupId>io.github.bonigarcia</groupId>
        <artifactId>webdrivermanager</artifactId>
        <version>5.6.2</version>
    </dependency>
</dependencies>
```

#### JavaScript/Node.js
```bash
npm install selenium-webdriver
npm install chromedriver  # または geckodriver for Firefox
```

### 2. 基本的なテストの記述

#### Python
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# WebDriverの初期化（ChromeDriverを自動管理）
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Webページを開く
    driver.get("https://www.example.com")

    # タイトルの確認
    assert "Example Domain" in driver.title

    # 要素の検索とクリック
    element = driver.find_element(By.LINK_TEXT, "More information...")
    element.click()

    # 明示的な待機（最大10秒）
    wait = WebDriverWait(driver, 10)
    element = wait.until(
        EC.presence_of_element_located((By.ID, "content"))
    )

    # テキストの取得
    text = element.text
    print(f"Content: {text}")

finally:
    # ブラウザを閉じる
    driver.quit()
```

#### Java
```java
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import io.github.bonigarcia.wdm.WebDriverManager;

public class SeleniumTest {
    public static void main(String[] args) {
        // ChromeDriverのセットアップ
        WebDriverManager.chromedriver().setup();
        WebDriver driver = new ChromeDriver();

        try {
            // Webページを開く
            driver.get("https://www.example.com");

            // タイトルの確認
            assert driver.getTitle().contains("Example Domain");

            // 要素の検索とクリック
            WebElement element = driver.findElement(By.linkText("More information..."));
            element.click();

            // 明示的な待機
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            WebElement content = wait.until(
                ExpectedConditions.presenceOfElementLocated(By.id("content"))
            );

            System.out.println("Content: " + content.getText());

        } finally {
            driver.quit();
        }
    }
}
```

### 3. 要素の検索方法

```python
from selenium.webdriver.common.by import By

# IDで検索
element = driver.find_element(By.ID, "username")

# Class名で検索
elements = driver.find_elements(By.CLASS_NAME, "btn")

# タグ名で検索
elements = driver.find_elements(By.TAG_NAME, "a")

# リンクテキストで検索
element = driver.find_element(By.LINK_TEXT, "Click here")

# 部分的なリンクテキストで検索
element = driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

# Name属性で検索
element = driver.find_element(By.NAME, "email")

# CSSセレクターで検索
element = driver.find_element(By.CSS_SELECTOR, "#login > input[type='submit']")

# XPathで検索
element = driver.find_element(By.XPATH, "//button[@class='submit']")
```

## 工程別の活用方法

### 9. テスト（アプリケーション）での活用

**目的**: E2Eテスト、UIテスト、クロスブラウザテスト

**活用方法**:
- ユーザーシナリオのテスト
- フォーム送信テスト
- ログイン/ログアウトフロー
- クロスブラウザ互換性テスト

**実装例（ログインテスト - pytest統合）**:
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestLogin:

    @pytest.fixture
    def driver(self):
        """各テストの前後でブラウザを起動・終了"""
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.implicitly_wait(10)  # 暗黙的な待機
        yield driver
        driver.quit()

    def test_successful_login(self, driver):
        """正常なログインテスト"""
        # ログインページを開く
        driver.get("https://example.com/login")

        # ユーザー名とパスワードを入力
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")

        username_input.send_keys("testuser")
        password_input.send_keys("TestPass123!")

        # ログインボタンをクリック
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # ダッシュボードにリダイレクトされることを確認
        wait = WebDriverWait(driver, 10)
        dashboard = wait.until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )

        assert dashboard.is_displayed()
        assert driver.current_url == "https://example.com/dashboard"

    def test_invalid_credentials(self, driver):
        """無効な認証情報でのログイン失敗"""
        driver.get("https://example.com/login")

        driver.find_element(By.ID, "username").send_keys("invalid")
        driver.find_element(By.ID, "password").send_keys("wrong")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # エラーメッセージが表示されることを確認
        wait = WebDriverWait(driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error"))
        )

        assert "Invalid credentials" in error_message.text

    def test_empty_form_submission(self, driver):
        """空フォーム送信のバリデーション"""
        driver.get("https://example.com/login")

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        # HTML5バリデーションメッセージを確認
        username_input = driver.find_element(By.ID, "username")
        validation_message = username_input.get_attribute("validationMessage")

        assert validation_message != ""
```

**Page Object Model（POM）パターン**:
```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """ログインページのPage Object"""

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://example.com/login"

        # ロケーター定義
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.error_message = (By.CLASS_NAME, "error")

    def open(self):
        """ログインページを開く"""
        self.driver.get(self.url)
        return self

    def enter_username(self, username):
        """ユーザー名を入力"""
        element = self.driver.find_element(*self.username_input)
        element.clear()
        element.send_keys(username)
        return self

    def enter_password(self, password):
        """パスワードを入力"""
        element = self.driver.find_element(*self.password_input)
        element.clear()
        element.send_keys(password)
        return self

    def click_login(self):
        """ログインボタンをクリック"""
        self.driver.find_element(*self.login_button).click()
        return self

    def get_error_message(self):
        """エラーメッセージを取得"""
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located(self.error_message))
        return element.text

# テストでの使用
def test_login_with_pom(driver):
    """Page Object Modelを使ったテスト"""
    login_page = LoginPage(driver)

    login_page.open() \
        .enter_username("testuser") \
        .enter_password("TestPass123!") \
        .click_login()

    # ダッシュボードに遷移していることを確認
    assert driver.current_url == "https://example.com/dashboard"
```

**クロスブラウザテスト**:
```python
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

@pytest.fixture(params=["chrome", "firefox", "edge"])
def multi_browser_driver(request):
    """複数ブラウザでテストを実行"""
    browser = request.param

    if browser == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    elif browser == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_homepage_loads_on_all_browsers(multi_browser_driver):
    """全ブラウザでホームページが読み込まれる"""
    multi_browser_driver.get("https://example.com")
    assert "Example Domain" in multi_browser_driver.title
```

**Selenium Grid（並列実行）**:
```python
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Selenium Gridハブに接続
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME
)

try:
    driver.get("https://example.com")
    # テスト実行
finally:
    driver.quit()

# Selenium Grid起動コマンド
# java -jar selenium-server-standalone.jar -role hub
# java -jar selenium-server-standalone.jar -role node -hub http://localhost:4444/grid/register
```

---

### 11. 導入での活用

**目的**: 本番環境のスモークテスト、受け入れテスト

**活用方法**:
- デプロイ後のスモークテスト
- 重要機能の動作確認
- ユーザー受け入れテスト（UAT）自動化

**実装例（スモークテスト）**:
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.smoke
class TestProductionSmokeTests:
    """本番環境スモークテスト"""

    @pytest.fixture(scope="class")
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # ヘッドレスモード
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    @pytest.mark.smoke
    def test_homepage_loads(self, driver):
        """ホームページが正常に読み込まれる"""
        driver.get("https://app.example.com")

        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        assert driver.title != ""
        assert element.is_displayed()

    @pytest.mark.smoke
    def test_login_page_accessible(self, driver):
        """ログインページにアクセスできる"""
        driver.get("https://app.example.com/login")

        login_form = driver.find_element(By.ID, "login-form")
        assert login_form.is_displayed()

    @pytest.mark.smoke
    def test_api_endpoint_responds(self, driver):
        """APIエンドポイントが応答する"""
        import requests

        response = requests.get("https://api.example.com/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @pytest.mark.smoke
    def test_critical_user_flow(self, driver):
        """重要なユーザーフローが動作する"""
        # ログイン
        driver.get("https://app.example.com/login")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # ダッシュボードが表示される
        wait = WebDriverWait(driver, 10)
        dashboard = wait.until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )
        assert dashboard.is_displayed()

# CI/CDでの実行
# pytest -m smoke --html=smoke-test-report.html
```

## 公式ドキュメント

- [Selenium 公式サイト](https://www.selenium.dev/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Selenium WebDriver API](https://www.selenium.dev/selenium/docs/api/py/)
- [Selenium Grid](https://www.selenium.dev/documentation/grid/)
- [Selenium IDE](https://www.selenium.dev/selenium-ide/)
- [Selenium GitHub Repository](https://github.com/SeleniumHQ/selenium)

## 学習リソース

### チュートリアル
- [Selenium Python Bindings](https://selenium-python.readthedocs.io/)
- [Selenium with Java](https://www.selenium.dev/documentation/webdriver/)
- [Selenium Tutorial by Guru99](https://www.guru99.com/selenium-tutorial.html)

### 書籍
- "Selenium WebDriver Recipes in Python" by Zhimin Zhan
- "Test Automation using Selenium WebDriver with Java" by Navneesh Garg
- "Selenium Design Patterns and Best Practices" by Dima Kovalenko

### 動画・コース
- [Selenium Tutorial for Beginners](https://www.youtube.com/results?search_query=selenium+tutorial)
- [Test Automation University - Selenium WebDriver](https://testautomationu.applitools.com/selenium-webdriver-python-tutorial/)
- [Udemy - Selenium WebDriver with Java](https://www.udemy.com/topic/selenium/)

### コミュニティ
- [Selenium Community Chat](https://www.selenium.dev/support/#ChatRoom)
- [Stack Overflow - Selenium](https://stackoverflow.com/questions/tagged/selenium)
- [Selenium Users Google Group](https://groups.google.com/g/selenium-users)

## 関連リンク

### 関連ツール
- [WebDriverManager](https://github.com/bonigarcia/webdrivermanager) - ドライバー自動管理（Java）
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) - ドライバー自動管理（Python）
- [pytest-selenium](https://pytest-selenium.readthedocs.io/) - pytest統合
- [Robot Framework](https://robotframework.org/) - Seleniumラッパー、キーワード駆動テスト

### クラウドサービス
- [Sauce Labs](https://saucelabs.com/) - クラウドSelenium実行環境
- [BrowserStack](https://www.browserstack.com/) - クラウドブラウザテスト
- [LambdaTest](https://www.lambdatest.com/) - クロスブラウザテスト
- [Selenium Grid on Docker](https://github.com/SeleniumHQ/docker-selenium) - Docker環境

### ベストプラクティス
- [Selenium Best Practices](https://www.selenium.dev/documentation/test_practices/)
- [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Selenium Design Patterns](https://www.selenium.dev/documentation/test_practices/encouraged/)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
