# Capybara

## 概要

**Capybara**は、Webアプリケーションの統合テスト（受け入れテスト）を実際のユーザー操作でシミュレートするRuby製テストフレームワークです。複数のドライバー（Rack::Test、Selenium、Cuprite等）をサポートし、RSpec・Cucumber・Minitest統合により、ブラウザ自動化テストを簡潔に記述できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | オープンソースコミュニティ |
| **種別** | Webアプリケーション統合テストフレームワーク |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://teamcapybara.github.io/capybara/ |
| **ドキュメント** | https://rubydoc.info/github/teamcapybara/capybara |

## 主な特徴

### 1. 高レベルAPI
- ユーザー視点のテスト記述
- セレクターの抽象化
- 自動待機（Ajax対応）
- 直感的なDSL

### 2. 複数ドライバーサポート
- **Rack::Test**: 高速、JavaScript非対応
- **Selenium**: 実ブラウザ、JavaScript対応
- **Cuprite**: ヘッドレスChrome
- **Poltergeist**: PhantomJS（非推奨）

### 3. テストフレームワーク統合
- **RSpec**: BDD統合
- **Cucumber**: Gherkin構文
- **Minitest**: Rails標準
- **Test::Unit**: Ruby標準

### 4. JavaScript対応
- Ajax自動待機
- モーダル・ドロップダウン操作
- ブラウザイベント（クリック、hover等）
- スクリーンショット

## 使い方

### セットアップ

```ruby
# Gemfile
group :test do
  gem 'capybara'
  gem 'selenium-webdriver'  # Seleniumドライバー
  # または
  gem 'cuprite'             # Cupriteドライバー（推奨）
end

bundle install
```

#### RSpec統合

```ruby
# spec/spec_helper.rb または spec/rails_helper.rb
require 'capybara/rspec'

RSpec.configure do |config|
  config.include Capybara::DSL, type: :feature
end

# Seleniumドライバー設定
Capybara.register_driver :selenium_chrome do |app|
  Capybara::Selenium::Driver.new(app, browser: :chrome)
end

Capybara.register_driver :selenium_chrome_headless do |app|
  options = Selenium::WebDriver::Chrome::Options.new
  options.add_argument('--headless')
  options.add_argument('--disable-gpu')
  options.add_argument('--no-sandbox')

  Capybara::Selenium::Driver.new(app, browser: :chrome, options: options)
end

# デフォルトドライバー
Capybara.default_driver = :rack_test          # JavaScript不要
Capybara.javascript_driver = :selenium_chrome_headless  # JavaScript必要
```

#### Cupriteドライバー（推奨）

```ruby
# Gemfile
gem 'cuprite'

# spec/rails_helper.rb
require 'capybara/cuprite'

Capybara.register_driver :cuprite do |app|
  Capybara::Cuprite::Driver.new(app, window_size: [1200, 800])
end

Capybara.javascript_driver = :cuprite
```

### 基本的なテスト

```ruby
# spec/features/user_login_spec.rb
require 'rails_helper'

RSpec.feature 'ユーザーログイン', type: :feature do
  scenario 'ユーザーが正常にログインできる' do
    # ページ遷移
    visit '/login'

    # フォーム入力
    fill_in 'Email', with: 'user@example.com'
    fill_in 'Password', with: 'password123'

    # ボタンクリック
    click_button 'ログイン'

    # アサーション
    expect(page).to have_content 'ログインしました'
    expect(page).to have_current_path '/dashboard'
  end

  scenario 'ログインに失敗する' do
    visit '/login'

    fill_in 'Email', with: 'invalid@example.com'
    fill_in 'Password', with: 'wrongpassword'
    click_button 'ログイン'

    expect(page).to have_content 'メールアドレスまたはパスワードが正しくありません'
  end
end
```

### Capybara DSL

#### ページ操作

```ruby
# ページ遷移
visit '/users'
visit root_path

# リンククリック
click_link 'ユーザー一覧'
click_link '編集', href: '/users/1/edit'

# ボタンクリック
click_button '送信'
click_button 'Submit', id: 'submit-btn'

# フォーム入力
fill_in 'Username', with: 'john_doe'
fill_in 'user[email]', with: 'john@example.com'

# チェックボックス
check 'I agree to terms'
uncheck 'Send me emails'

# ラジオボタン
choose 'Male'

# セレクトボックス
select 'Tokyo', from: 'City'

# ファイルアップロード
attach_file 'Avatar', '/path/to/file.jpg'
```

#### アサーション

```ruby
# コンテンツ確認
expect(page).to have_content 'Welcome'
expect(page).to have_text 'Hello World', exact: true

# CSS/XPath
expect(page).to have_css 'h1', text: 'Title'
expect(page).to have_xpath '//div[@class="alert"]'

# リンク・ボタン
expect(page).to have_link 'Home'
expect(page).to have_button 'Submit'

# フィールド
expect(page).to have_field 'Email', with: 'user@example.com'
expect(page).to have_checked_field 'I agree'
expect(page).to have_unchecked_field 'Send emails'

# セレクト
expect(page).to have_select 'Country', selected: 'Japan'

# URL
expect(page).to have_current_path '/users'
expect(current_url).to eq 'http://localhost:3000/users'
```

#### セレクター

```ruby
# CSS
find('#user-name')
find('.alert-danger')
find('div.user-card', text: 'John')

# XPath
find(:xpath, '//div[@id="content"]')

# ID
find_by_id('username')

# テキスト
find('a', text: 'Click me')
find('button', text: /submit/i)  # 正規表現

# 複数要素
all('li').count
all('.user-card').each do |card|
  expect(card).to have_content 'User'
end

# 最初/最後
first('li').click
find('li', match: :first).click
```

#### JavaScript対応テスト

```ruby
# spec/features/ajax_spec.rb
require 'rails_helper'

RSpec.feature 'Ajax操作', type: :feature, js: true do
  scenario 'Ajax でユーザーを削除' do
    user = create(:user, name: 'John')

    visit users_path

    within "#user_#{user.id}" do
      click_link '削除'
    end

    # Ajaxリクエスト完了を待機
    expect(page).not_to have_content 'John'

    # モーダル操作
    within '.modal' do
      expect(page).to have_content '本当に削除しますか？'
      click_button '確認'
    end

    expect(page).to have_content 'ユーザーを削除しました'
  end
end
```

### スコープ（within）

```ruby
# 特定要素内で操作
within '#login-form' do
  fill_in 'Email', with: 'user@example.com'
  fill_in 'Password', with: 'password'
  click_button 'ログイン'
end

# テーブル行単位
within 'table tbody tr:first-child' do
  click_link '編集'
end

# CSS
within '.user-card[data-id="123"]' do
  expect(page).to have_content 'John Doe'
end
```

### 待機

```ruby
# デフォルト待機時間（全体設定）
Capybara.default_max_wait_time = 5  # 5秒

# 要素が表示されるまで待機（自動）
expect(page).to have_content 'Loading complete'

# 明示的待機
using_wait_time(10) do
  expect(page).to have_css '.ajax-content'
end

# 要素が消えるまで待機
expect(page).not_to have_css '.loading-spinner'
```

### スクリーンショット

```ruby
# スクリーンショット保存
save_screenshot('screenshot.png')
save_and_open_screenshot  # 保存して自動的に開く

# 失敗時に自動保存
RSpec.configure do |config|
  config.after(:each, type: :feature) do |example|
    if example.exception
      meta = example.metadata
      filename = File.basename(meta[:file_path])
      line_number = meta[:line_number]
      screenshot_name = "screenshot-#{filename}-#{line_number}.png"
      save_screenshot(screenshot_name)
    end
  end
end
```

### ページオブジェクトパターン

```ruby
# spec/support/pages/login_page.rb
class LoginPage
  include Capybara::DSL

  def visit_page
    visit '/login'
  end

  def fill_email(email)
    fill_in 'Email', with: email
  end

  def fill_password(password)
    fill_in 'Password', with: password
  end

  def submit
    click_button 'ログイン'
  end

  def login(email, password)
    fill_email(email)
    fill_password(password)
    submit
  end

  def error_message
    find('.alert-danger').text
  end
end
```

```ruby
# spec/features/user_login_spec.rb
RSpec.feature 'ユーザーログイン', type: :feature do
  let(:login_page) { LoginPage.new }

  scenario 'ユーザーが正常にログインできる' do
    login_page.visit_page
    login_page.login('user@example.com', 'password123')

    expect(page).to have_content 'ログインしました'
  end
end
```

### Cucumber統合

```ruby
# Gemfile
gem 'cucumber-rails', require: false

# features/support/env.rb
require 'cucumber/rails'
require 'capybara/cucumber'

Capybara.javascript_driver = :selenium_chrome_headless
```

```gherkin
# features/user_login.feature
Feature: ユーザーログイン
  ユーザーがログインできることを確認する

  Scenario: 正常なログイン
    Given ユーザー "user@example.com" が存在する
    When ログインページを開く
    And メールアドレス "user@example.com" を入力する
    And パスワード "password123" を入力する
    And "ログイン" ボタンをクリックする
    Then "ログインしました" と表示される
```

```ruby
# features/step_definitions/login_steps.rb
Given('ユーザー {string} が存在する') do |email|
  create(:user, email: email, password: 'password123')
end

When('ログインページを開く') do
  visit '/login'
end

When('メールアドレス {string} を入力する') do |email|
  fill_in 'Email', with: email
end

When('パスワード {string} を入力する') do |password|
  fill_in 'Password', with: password
end

When('{string} ボタンをクリックする') do |button_text|
  click_button button_text
end

Then('{string} と表示される') do |text|
  expect(page).to have_content text
end
```

### CI/CD統合

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Setup Chrome
        uses: browser-actions/setup-chrome@latest

      - name: Setup Database
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
        run: |
          bin/rails db:create
          bin/rails db:schema:load

      - name: Run Feature Tests
        env:
          RAILS_ENV: test
        run: |
          bundle exec rspec spec/features
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | TDD/BDD | テスト駆動開発 |
| **テスト** | 統合テスト | エンドツーエンドテスト |
| **テスト** | 受け入れテスト | ユーザーストーリー検証 |
| **回帰テスト** | CI/CD | 自動回帰テスト |

## メリット

- **高レベルAPI**: ユーザー視点の直感的テスト
- **ドライバー選択**: Selenium、Cuprite等切替可能
- **自動待機**: Ajax・非同期処理対応
- **Ruby統合**: RSpec、Cucumber、Rails統合
- **柔軟**: ページオブジェクト、カスタムヘルパー
- **成熟**: 長期実績、安定性

## デメリット

- **実行速度**: ブラウザ起動で遅い（特にSelenium）
- **Ruby専用**: 他言語では使用不可
- **デバッグ困難**: 失敗時の原因特定が難しい
- **脆弱性**: セレクター変更で壊れやすい
- **CI環境設定**: ヘッドレスブラウザ設定が必要

## 類似ツールとの比較

| ツール | 言語 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **Capybara** | Ruby | Rails統合、高レベルAPI | Rails アプリ |
| **Selenium** | 多言語 | W3C標準、広く使用 | クロス言語 |
| **Cypress** | JavaScript | 高速、DX優れる | モダンJS |
| **Playwright** | 多言語 | 高速、信頼性高 | モダン環境全般 |

## ベストプラクティス

### 1. Rack::TestとSeleniumの使い分け

```ruby
# JavaScript不要 → Rack::Test（高速）
RSpec.feature 'ユーザー一覧', type: :feature do
  scenario 'ユーザーが表示される' do
    # Rack::Testで実行（高速）
  end
end

# JavaScript必要 → Selenium/Cuprite
RSpec.feature 'Ajax削除', type: :feature, js: true do
  scenario 'ユーザーをAjaxで削除' do
    # Selenium/Cupriteで実行
  end
end
```

### 2. 安定したセレクター

```ruby
# ❌ 悪い例（脆弱）
find('div.container > div:nth-child(3) > a').click

# ✅ 良い例（data属性）
find('[data-test="delete-button"]').click

# HTML側
# <button data-test="delete-button">削除</button>
```

### 3. 待機戦略

```ruby
# ❌ 悪い例（固定待機）
sleep 3

# ✅ 良い例（条件待機）
expect(page).to have_css '.ajax-content'
```

### 4. ページオブジェクト

```ruby
# 画面要素・操作を抽象化
class LoginPage
  include Capybara::DSL

  def login(email, password)
    fill_in 'Email', with: email
    fill_in 'Password', with: password
    click_button 'ログイン'
  end
end
```

## 公式リソース

- **公式サイト**: https://teamcapybara.github.io/capybara/
- **GitHub**: https://github.com/teamcapybara/capybara
- **API ドキュメント**: https://rubydoc.info/github/teamcapybara/capybara
- **Cuprite**: https://github.com/rubycdp/cuprite

## まとめ

Capybaraは、Webアプリケーションの統合テストを実際のユーザー操作でシミュレートするRuby製フレームワークです。高レベルAPI、複数ドライバー対応、自動待機により、ブラウザ自動化テストを簡潔に記述できます。Rails開発において、RSpec・Cucumber統合により、BDD・受け入れテストのデファクトスタンダードとして広く採用されています。

---

**最終更新**: 2025-12-06
**対象バージョン**: Capybara 3.39+
