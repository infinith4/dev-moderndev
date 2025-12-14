# Calabash

## 概要

**Calabash**は、iOS・Androidアプリの自動UIテストフレームワークです。Cucumber統合により、自然言語（Gherkin）でテストシナリオを記述でき、実機・エミュレーターでのクロスプラットフォームテストを実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Xamarin（現Microsoft） |
| **種別** | モバイルアプリUIテストフレームワーク |
| **ライセンス** | Eclipse Public License 1.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | http://calaba.sh/ |
| **ドキュメント** | https://github.com/calabash |

**注意**: Calabashは2020年にメンテナンス終了が発表されました。後継として、Xamarin.UITest、Appium等への移行が推奨されています。

## 主な特徴

### 1. クロスプラットフォーム
- **iOS**: calabash-ios
- **Android**: calabash-android
- 同一テストコードで両プラットフォーム実行可能

### 2. Cucumber統合
- Gherkin構文（Given-When-Then）
- 自然言語でシナリオ記述
- ステップ定義の再利用
- タグによるシナリオフィルタ

### 3. 実機・エミュレーター対応
- iOS Simulator
- Android Emulator
- 実デバイス（USB接続）
- クラウドテストサービス連携

### 4. ページオブジェクトパターン
- 画面要素の抽象化
- テストコードの保守性向上
- 再利用可能なヘルパーメソッド

## 使い方

### セットアップ

#### Ruby環境（共通）

```bash
# Ruby 2.3+インストール（推奨: rbenvまたはrvm）
rbenv install 2.7.0
rbenv global 2.7.0

# Calabash gemインストール
gem install calabash-cucumber
```

#### Android セットアップ

```bash
# calabash-android インストール
gem install calabash-android

# APKリサイン（テスト用）
calabash-android resign your-app.apk

# テストサーバー埋め込み（初回のみ）
calabash-android build your-app.apk

# これにより your-app-test.apk が生成される
```

#### iOS セットアップ

```bash
# calabash-ios インストール
gem install calabash-cucumber

# Xcodeプロジェクトに Calabash framework追加
# または、CocoaPods使用
```

```ruby
# Podfile
target 'YourAppTests' do
  pod 'Calabash', '~> 0.23'
end
```

```bash
pod install

# Xcodeで Calabash-calフレームワーク追加
# Build Settings → Framework Search Paths
# $(inherited) $(SRCROOT)/Pods/Calabash
```

### プロジェクト作成

```bash
# 新規Calabashプロジェクト作成
calabash-android gen

# または、iOS
calabash-ios gen

# 以下のディレクトリ構成が生成される
features/
├── step_definitions/     # ステップ定義
├── support/              # サポートファイル
│   ├── app_installation_hooks.rb
│   ├── app_life_cycle_hooks.rb
│   └── env.rb
└── *.feature            # フィーチャーファイル
```

### フィーチャーファイル（Gherkin）

```gherkin
# features/login.feature
Feature: Login
  ユーザーがログインできることを確認する

  Scenario: 正常なログイン
    Given アプリを起動する
    When メールアドレス "user@example.com" を入力する
    And パスワード "password123" を入力する
    And "ログイン" ボタンをタップする
    Then "ようこそ" というテキストが表示される

  Scenario: ログイン失敗
    Given アプリを起動する
    When メールアドレス "invalid@example.com" を入力する
    And パスワード "wrongpassword" を入力する
    And "ログイン" ボタンをタップする
    Then "ログインに失敗しました" というエラーが表示される
```

### ステップ定義（Ruby）

```ruby
# features/step_definitions/login_steps.rb

Given(/^アプリを起動する$/) do
  # アプリは自動的に起動される
  wait_for_element_exists("* id:'email_field'")
end

When(/^メールアドレス "([^"]*)" を入力する$/) do |email|
  enter_text("* id:'email_field'", email)
end

When(/^パスワード "([^"]*)" を入力する$/) do |password|
  enter_text("* id:'password_field'", password)
end

When(/^"([^"]*)" ボタンをタップする$/) do |button_text|
  touch("* marked:'#{button_text}'")
end

Then(/^"([^"]*)" というテキストが表示される$/) do |text|
  wait_for_element_exists("* marked:'#{text}'")
end

Then(/^"([^"]*)" というエラーが表示される$/) do |error_text|
  wait_for_element_exists("* marked:'#{error_text}'")
end
```

### Calabash API

```ruby
# 要素の操作

# タップ
touch("button")
touch("* id:'login_button'")
touch("* marked:'Login'")

# テキスト入力
enter_text("* id:'email'", "user@example.com")
clear_text("* id:'email'")

# スワイプ
swipe(:left)
swipe(:right, query: "* id:'carousel'")

# スクロール
scroll("scrollView", :down)
scroll_to_mark("Section 3")

# 待機
wait_for_element_exists("* id:'welcome_message'", timeout: 10)
wait_for_elements_do_not_exist("* id:'loading_spinner'")

# アサーション
element_exists("* id:'username'")
element_does_not_exist("* id:'error_message'")

# スクリーンショット
screenshot_embed(name: "login_screen")
```

### ページオブジェクトパターン

```ruby
# features/support/pages/login_page.rb
class LoginPage
  def initialize(world)
    @world = world
  end

  def email_field
    "* id:'email_field'"
  end

  def password_field
    "* id:'password_field'"
  end

  def login_button
    "* id:'login_button'"
  end

  def enter_email(email)
    @world.enter_text(email_field, email)
  end

  def enter_password(password)
    @world.enter_text(password_field, password)
  end

  def tap_login
    @world.touch(login_button)
  end

  def login(email, password)
    enter_email(email)
    enter_password(password)
    tap_login
  end
end
```

```ruby
# features/step_definitions/login_steps.rb（Page Object使用）
require_relative '../support/pages/login_page'

Given(/^アプリを起動する$/) do
  @login_page = LoginPage.new(self)
end

When(/^メールアドレス "([^"]*)" とパスワード "([^"]*)" でログインする$/) do |email, password|
  @login_page.login(email, password)
end
```

### Android固有の操作

```ruby
# Androidキーイベント
press_back_button
press_menu_button
press_enter_button

# アプリのインストール・起動
reinstall_apps
start_test_server_in_background

# デバイス情報取得
device_info = device.model_name
puts "Testing on: #{device_info}"
```

### iOS固有の操作

```ruby
# iOSキーボード
keyboard_enter_text("Hello")
touch("* marked:'Return'")  # Returnキー

# デバイス回転
rotate(:left)
rotate(:right)

# バックグラウンド遷移
send_app_to_background(5)  # 5秒間バックグラウンド
```

### テスト実行

```bash
# Androidテスト実行
calabash-android run your-app-test.apk

# 特定フィーチャー実行
calabash-android run your-app-test.apk features/login.feature

# タグでフィルタ
calabash-android run your-app-test.apk --tags @smoke

# iOSテスト実行
calabash-ios console
> start_test_server_in_background
> query("*")

# Cucumberオプション
cucumber features/ --format html --out report.html
cucumber features/ --format json --out report.json
```

### CI/CD統合

#### Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Build APK') {
            steps {
                sh './gradlew assembleDebug'
            }
        }

        stage('Resign APK') {
            steps {
                sh 'calabash-android resign app/build/outputs/apk/debug/app-debug.apk'
                sh 'calabash-android build app/build/outputs/apk/debug/app-debug.apk'
            }
        }

        stage('Run Calabash Tests') {
            steps {
                sh 'calabash-android run app/build/outputs/apk/debug/app-debug-test.apk'
            }
        }

        stage('Generate Report') {
            steps {
                cucumber buildStatus: 'SUCCESS',
                         fileIncludePattern: '**/*.json',
                         jsonReportDirectory: 'reports'
            }
        }
    }
}
```

#### GitHub Actions

```yaml
# .github/workflows/calabash-test.yml
name: Calabash Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  android-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: 2.7
          bundler-cache: true

      - name: Install Calabash
        run: |
          gem install calabash-android
          gem install cucumber

      - name: Build APK
        run: ./gradlew assembleDebug

      - name: Resign APK
        run: |
          calabash-android resign app/build/outputs/apk/debug/app-debug.apk
          calabash-android build app/build/outputs/apk/debug/app-debug.apk

      - name: Start Emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 29
          script: calabash-android run app/build/outputs/apk/debug/app-debug-test.apk

      - name: Upload Test Results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: reports/
```

### クラウドテストサービス連携

```bash
# AWS Device Farm連携
# calabash-android run your-app-test.apk を
# Device Farmにアップロード・実行

# Sauce Labs連携
# Sauce Labs Real Device Cloudで実行可能
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | 開発中テスト | 機能実装後の動作確認 |
| **テスト** | 回帰テスト | UI変更の影響確認 |
| **テスト** | 受け入れテスト | ビジネス要件の検証 |
| **CI/CD** | 自動テスト | プッシュ毎の自動実行 |

## メリット

- **クロスプラットフォーム**: iOS・Android共通コード
- **自然言語**: Gherkinで非エンジニアも理解可能
- **実機テスト**: エミュレーター・実デバイス対応
- **Cucumber統合**: BDD（振る舞い駆動開発）
- **オープンソース**: 無料、カスタマイズ可能
- **コミュニティ**: 豊富なドキュメント・サンプル

## デメリット

- **メンテナンス終了**: 2020年終了、後継ツール推奨
- **セットアップ複雑**: APKリサイン、フレームワーク追加必要
- **実行速度**: 実機テストは時間がかかる
- **デバッグ困難**: エラー箇所の特定が難しい
- **最新OS非対応**: iOS 14+、Android 11+で問題
- **代替ツール推奨**: Appium、Espresso、XCUITest

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Calabash** | Cucumber統合、BDD | 無料（非推奨） | レガシープロジェクト |
| **Appium** | 多言語対応、W3C標準 | 無料 | クロスプラットフォーム |
| **Espresso** | Android公式、高速 | 無料 | Android専用 |
| **XCUITest** | iOS公式、Swift | 無料 | iOS専用 |

## ベストプラクティス

### 1. ページオブジェクトパターン

```ruby
# 画面要素を抽象化
class HomePage
  def search_field; "* id:'search'"; end
  def search(query)
    enter_text(search_field, query)
    press_enter_button
  end
end
```

### 2. 待機戦略

```ruby
# 要素が現れるまで待機
wait_for_element_exists("* id:'result'", timeout: 10)

# スピナー消失まで待機
wait_for_elements_do_not_exist("* id:'loading'")
```

### 3. タグによるシナリオ分類

```gherkin
@smoke @login
Scenario: 正常なログイン

@regression @payment
Scenario: 決済処理
```

```bash
# スモークテストのみ実行
cucumber --tags @smoke

# スモークテスト以外
cucumber --tags ~@smoke
```

### 4. スクリーンショット活用

```ruby
# 失敗時スクリーンショット
After do |scenario|
  if scenario.failed?
    screenshot_embed(name: "failure_#{scenario.name}")
  end
end
```

## 公式リソース

- **公式サイト**: http://calaba.sh/
- **GitHub**: https://github.com/calabash
- **ドキュメント**: https://github.com/calabash/calabash-android/wiki
- **移行ガイド**: https://github.com/calabash/calabash/wiki/Calabash-EOL

## まとめ

Calabashは、iOS・AndroidアプリのクロスプラットフォームUIテストフレームワークです。Cucumber統合により、自然言語でテストシナリオを記述でき、BDD開発をサポートします。ただし、2020年にメンテナンス終了が発表されており、新規プロジェクトではAppium、Espresso、XCUITest等の後継ツールの使用が推奨されています。

---

**最終更新**: 2025-12-06
**メンテナンス状況**: 終了（2020年）
**推奨代替ツール**: Appium、Espresso（Android）、XCUITest（iOS）
