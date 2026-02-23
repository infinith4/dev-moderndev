# Appium

## 概要

Appiumは、iOS、Android、Windowsアプリケーションの自動テストを実現するオープンソースのモバイルテスト自動化フレームワークである。W3C WebDriverプロトコルをベースとし、ネイティブアプリ、ハイブリッドアプリ、モバイルWebアプリのクロスプラットフォームテストを単一のAPIで実行できる。テスト対象アプリの再コンパイルやSDKの埋め込みが不要であり、Java、Python、JavaScript、Ruby、C#等の複数プログラミング言語でテストスクリプトを記述可能である。Appium 2.xではドライバ・プラグインアーキテクチャが導入され、拡張性と柔軟性が大幅に向上した。

## 主な機能

### 1. クロスプラットフォーム対応
- **iOS**: XCUITestドライバによるiOS自動テスト
- **Android**: UiAutomator2ドライバによるAndroid自動テスト
- **Windows**: WinAppDriverによるWindowsデスクトップアプリテスト
- **マルチプラットフォーム**: 同一テストコードで複数OS対応

### 2. アプリ種別対応
- **ネイティブアプリ**: iOS/Android SDKで開発されたアプリ
- **ハイブリッドアプリ**: WebView埋め込み型アプリ（Cordova/Ionic等）
- **モバイルWebアプリ**: モバイルブラウザ上のWebサイト
- **Flutter**: flutter-driverによるFlutterアプリテスト

### 3. 要素検索・操作
- **ID/Accessibility ID**: アクセシビリティ識別子による要素特定
- **XPath**: XML構造による要素検索
- **Class Name**: UIコンポーネントクラスによる検索
- **UIAutomator Selector**: Android固有のセレクタ
- **iOS Predicate/Class Chain**: iOS固有の検索方式

### 4. 高度な操作
- **ジェスチャー**: タップ、スワイプ、ピンチ、長押し
- **マルチタッチ**: 複数指での同時操作
- **キーボード操作**: テキスト入力、キー送信
- **画面回転**: ポートレート/ランドスケープ切替
- **通知操作**: プッシュ通知のハンドリング

### 5. Appium 2.x アーキテクチャ
- **ドライバプラグイン方式**: 必要なドライバのみインストール
- **プラグインシステム**: 機能拡張が容易
- **ECMAScript対応**: モダンなコードベース
- **CLIの改善**: appium driver/plugin管理コマンド

### 6. デバイスファーム連携
- **BrowserStack**: クラウドデバイステスト
- **Sauce Labs**: 並列実行・デバイスクラウド
- **AWS Device Farm**: AWSデバイステスト
- **ローカル**: 実機・エミュレータ/シミュレータ

## 利用方法

### インストール

```bash
# Node.js が必要（v16以上推奨）
# Appium 2.x インストール
npm install -g appium

# ドライバインストール
appium driver install uiautomator2   # Android用
appium driver install xcuitest       # iOS用

# インストール確認
appium driver list --installed

# Appiumサーバー起動
appium
```

### 環境セットアップ（Android）

```bash
# Android SDK のセットアップ
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/emulator

# Java JDK の確認
java -version

# appium-doctor で環境チェック
npm install -g appium-doctor
appium-doctor --android
```

### Desired Capabilities設定

```python
# Python - Android テスト例
from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.app = "/path/to/app.apk"
options.automation_name = "UiAutomator2"
options.no_reset = True

driver = webdriver.Remote(
    command_executor="http://localhost:4723",
    options=options
)
```

```python
# Python - iOS テスト例
from appium import webdriver
from appium.options.ios import XCUITestOptions

options = XCUITestOptions()
options.platform_name = "iOS"
options.device_name = "iPhone 15 Pro"
options.platform_version = "17.0"
options.app = "/path/to/app.ipa"
options.automation_name = "XCUITest"

driver = webdriver.Remote(
    command_executor="http://localhost:4723",
    options=options
)
```

### テストスクリプト例（Python）

```python
# test_login.py
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    def setup_method(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.app = "/path/to/app.apk"
        options.automation_name = "UiAutomator2"
        self.driver = webdriver.Remote(
            "http://localhost:4723", options=options
        )
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        self.driver.quit()

    def test_successful_login(self):
        """正常系ログインテスト"""
        # ユーザー名入力
        username = self.wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "username_field")
            )
        )
        username.send_keys("testuser")

        # パスワード入力
        password = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "password_field"
        )
        password.send_keys("password123")

        # ログインボタンタップ
        login_btn = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "login_button"
        )
        login_btn.click()

        # ホーム画面の表示確認
        home = self.wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "home_screen")
            )
        )
        assert home.is_displayed()
```

### テストスクリプト例（Java）

```java
// LoginTest.java
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.jupiter.api.*;
import java.net.URL;

public class LoginTest {
    private AndroidDriver driver;

    @BeforeEach
    void setUp() throws Exception {
        UiAutomator2Options options = new UiAutomator2Options()
            .setDeviceName("emulator-5554")
            .setApp("/path/to/app.apk");

        driver = new AndroidDriver(
            new URL("http://localhost:4723"), options
        );
    }

    @AfterEach
    void tearDown() {
        if (driver != null) driver.quit();
    }

    @Test
    void testSuccessfulLogin() {
        driver.findElement(AppiumBy.accessibilityId("username_field"))
              .sendKeys("testuser");
        driver.findElement(AppiumBy.accessibilityId("password_field"))
              .sendKeys("password123");
        driver.findElement(AppiumBy.accessibilityId("login_button"))
              .click();
        assert driver.findElement(
            AppiumBy.accessibilityId("home_screen")
        ).isDisplayed();
    }
}
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/appium-test.yml
name: Appium Tests

on: [push, pull_request]

jobs:
  android-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3
      - name: Start Android Emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: |
            npm install -g appium
            appium driver install uiautomator2
            appium &
            sleep 10
            pip install pytest Appium-Python-Client
            pytest tests/mobile/ --junitxml=results.xml
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Appium** | 無料 | オープンソース、Apache 2.0 License |
| **Appium Inspector** | 無料 | GUI要素検査ツール |
| **BrowserStack** | 有料（$29/月〜） | クラウドデバイスファーム連携 |
| **Sauce Labs** | 有料（要問合せ） | クラウドテスト実行基盤 |

## メリット

1. **クロスプラットフォーム**: 単一APIでiOS・Android両方のテストを記述可能
2. **多言語対応**: Java、Python、JavaScript、Ruby、C#等でテスト記述可能
3. **アプリ改変不要**: テスト対象アプリのソースコード変更やSDK埋め込みが不要
4. **WebDriver標準**: W3C WebDriverプロトコル準拠で既存のSeleniumスキルを活用
5. **オープンソース**: 無料で利用でき、大規模コミュニティによるサポート
6. **デバイスファーム連携**: BrowserStack、Sauce Labs等のクラウドサービスと統合可能
7. **ネイティブ/ハイブリッド/Web対応**: アプリ種別を問わずテスト可能
8. **実機・エミュレータ両対応**: 開発時はエミュレータ、リリース前は実機で検証
9. **プラグイン拡張**: Appium 2.xのプラグインシステムで機能追加が容易
10. **Appium Inspector**: GUIでの要素特定・操作検証が可能

## デメリット

1. **環境構築の複雑さ**: Android SDK、Xcode、Java等の事前セットアップが必要
2. **実行速度**: Selenium WebDriverベースのため、ネイティブテストツールより遅い
3. **フレークテスト**: デバイス状態やネットワークに依存した不安定なテストが発生しやすい
4. **iOS制約**: macOS環境が必須、Xcodeバージョン依存
5. **要素特定の困難さ**: 動的UIやカスタムコンポーネントの要素特定が難しい場合がある
6. **デバッグ難度**: テスト失敗時の原因特定が複雑になりやすい
7. **バージョン追従**: OS・デバイスのアップデートへの追従コストが高い
8. **並列実行**: 複数デバイスでの並列テスト実行には追加設定が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Espresso** | Android公式テストFW | Appiumより高速だがAndroid限定 |
| **XCUITest** | iOS公式テストFW | Appiumより高速だがiOS限定 |
| **Detox** | React Native向け | Appiumより高速だがRN限定 |
| **Maestro** | モバイルUI テストFW | Appiumよりシンプルだが機能限定 |
| **Flutter Driver** | Flutter公式テスト | Appiumより安定だがFlutter限定 |

## 公式リンク

- **公式サイト**: [https://appium.io/](https://appium.io/)
- **ドキュメント**: [https://appium.io/docs/en/latest/](https://appium.io/docs/en/latest/)
- **GitHub**: [https://github.com/appium/appium](https://github.com/appium/appium)
- **Appium Inspector**: [https://github.com/appium/appium-inspector](https://github.com/appium/appium-inspector)
- **Appium Python Client**: [https://github.com/appium/python-client](https://github.com/appium/python-client)

## 関連ドキュメント

- [テストツール一覧](../テスト/)
- [Selenium](./Selenium.md)
- [Cucumber](./Cucumber.md)
- [Allure Report](./Allure_Report.md)
- [モバイルテストベストプラクティス](../../best-practices/mobile-testing.md)

---

**カテゴリ**: テスト
**対象工程**: テスト・品質管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
