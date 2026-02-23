# Cucumber

## 概要

Cucumberは、振る舞い駆動開発（BDD: Behavior Driven Development）を実現するオープンソースのテスティングフレームワークである。Gherkinと呼ばれる自然言語に近い構文（Given/When/Then）でテストシナリオを記述し、ビジネスサイドと開発チームの間で共通理解可能な「生きたドキュメント（Living Documentation）」としてのFeatureファイルを作成する。Java、Ruby、JavaScript、Python、C#等の主要言語に対応し、記述されたGherkinシナリオをステップ定義（Step Definitions）を通じて実行可能なテストコードに変換する。受入テスト・結合テストにおいて、ビジネス要件とテストコードの一致を保証する。

## 主な機能

### 1. Gherkin構文
- **Feature**: テスト対象機能の説明
- **Scenario**: 個別のテストシナリオ定義
- **Given**: テストの前提条件
- **When**: テスト対象のアクション
- **Then**: 期待される結果の検証
- **And/But**: 条件・アクション・検証の追加

### 2. シナリオテンプレート
- **Scenario Outline**: パラメータ化されたシナリオ
- **Examples**: テストデータテーブルの定義
- **Data Tables**: ステップ内でのテーブルデータ受け渡し
- **Doc Strings**: 複数行テキストの受け渡し

### 3. タグとフィルタリング
- **@tag**: シナリオ・Featureへのタグ付け
- **タグフィルタ**: 特定タグのシナリオのみ実行
- **@wip**: 開発中シナリオの管理
- **@smoke/@regression**: テスト種別による分類

### 4. フック機能
- **Before/After**: シナリオ前後の処理
- **BeforeAll/AfterAll**: 全テスト前後の処理
- **BeforeStep/AfterStep**: ステップ前後の処理
- **条件付きフック**: タグベースのフック実行制御

### 5. 多言語対応
- **Java**: cucumber-java / cucumber-junit / cucumber-spring
- **JavaScript**: @cucumber/cucumber (Node.js)
- **Ruby**: cucumber-ruby
- **Python**: behave（Cucumber互換）
- **C#**: SpecFlow（Cucumber互換）

### 6. レポート・統合
- **HTMLレポート**: 組み込みHTMLレポート生成
- **JSONレポート**: CI/CD連携用JSON出力
- **JUnitレポート**: JUnit XML形式出力
- **Allure連携**: Allure Report用アダプタ
- **Cucumber Reports**: クラウドレポートサービス

## 利用方法

### インストール（Java + Maven）

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-java</artifactId>
        <version>7.20.1</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-junit-platform-engine</artifactId>
        <version>7.20.1</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.platform</groupId>
        <artifactId>junit-platform-suite</artifactId>
        <version>1.11.3</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Featureファイル作成

```gherkin
# src/test/resources/features/login.feature
Feature: ログイン機能
  ユーザーがシステムにログインできることを確認する

  Background:
    Given ログインページが表示されている

  Scenario: 正常なログイン
    When ユーザー名 "testuser" を入力する
    And パスワード "password123" を入力する
    And ログインボタンをクリックする
    Then ホーム画面が表示される
    And ウェルカムメッセージ "ようこそ、testuser さん" が表示される

  Scenario: パスワード誤りによるログイン失敗
    When ユーザー名 "testuser" を入力する
    And パスワード "wrong_password" を入力する
    And ログインボタンをクリックする
    Then エラーメッセージ "認証に失敗しました" が表示される

  Scenario Outline: 入力バリデーション
    When ユーザー名 "<username>" を入力する
    And パスワード "<password>" を入力する
    And ログインボタンをクリックする
    Then エラーメッセージ "<error>" が表示される

    Examples:
      | username  | password    | error                    |
      |           | password123 | ユーザー名を入力してください |
      | testuser  |             | パスワードを入力してください |
      |           |             | ユーザー名を入力してください |
```

### ステップ定義（Java）

```java
// src/test/java/steps/LoginSteps.java
package steps;

import io.cucumber.java.ja.*;
import io.cucumber.java.Before;
import io.cucumber.java.After;
import static org.junit.jupiter.api.Assertions.*;

public class LoginSteps {
    private LoginPage loginPage;
    private String currentMessage;

    @Before
    public void setUp() {
        loginPage = new LoginPage();
    }

    @Given("ログインページが表示されている")
    public void ログインページが表示されている() {
        loginPage.open();
        assertTrue(loginPage.isDisplayed());
    }

    @When("ユーザー名 {string} を入力する")
    public void ユーザー名を入力する(String username) {
        loginPage.enterUsername(username);
    }

    @When("パスワード {string} を入力する")
    public void パスワードを入力する(String password) {
        loginPage.enterPassword(password);
    }

    @When("ログインボタンをクリックする")
    public void ログインボタンをクリックする() {
        loginPage.clickLogin();
    }

    @Then("ホーム画面が表示される")
    public void ホーム画面が表示される() {
        assertTrue(loginPage.isHomeDisplayed());
    }

    @Then("ウェルカムメッセージ {string} が表示される")
    public void ウェルカムメッセージが表示される(String message) {
        assertEquals(message, loginPage.getWelcomeMessage());
    }

    @Then("エラーメッセージ {string} が表示される")
    public void エラーメッセージが表示される(String error) {
        assertEquals(error, loginPage.getErrorMessage());
    }
}
```

### テスト実行クラス

```java
// src/test/java/RunCucumberTest.java
import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.*;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "steps")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
    value = "pretty, html:target/cucumber-report.html, json:target/cucumber.json")
public class RunCucumberTest {
}
```

### インストール（JavaScript）

```bash
# Node.jsプロジェクトでのセットアップ
npm install --save-dev @cucumber/cucumber
```

### ステップ定義（JavaScript）

```javascript
// features/step_definitions/login_steps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const assert = require('assert');

Given('ログインページが表示されている', function () {
  this.loginPage = new LoginPage();
  this.loginPage.open();
});

When('ユーザー名 {string} を入力する', function (username) {
  this.loginPage.enterUsername(username);
});

When('パスワード {string} を入力する', function (password) {
  this.loginPage.enterPassword(password);
});

When('ログインボタンをクリックする', function () {
  this.result = this.loginPage.clickLogin();
});

Then('ホーム画面が表示される', function () {
  assert.strictEqual(this.result.page, 'home');
});

Then('エラーメッセージ {string} が表示される', function (expected) {
  assert.strictEqual(this.result.error, expected);
});
```

```bash
# テスト実行
npx cucumber-js

# タグフィルタ付き実行
npx cucumber-js --tags "@smoke"

# 特定Featureのみ
npx cucumber-js features/login.feature
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/bdd-test.yml
name: BDD Tests

on: [push, pull_request]

jobs:
  cucumber-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Run Cucumber Tests
        run: mvn test -Dcucumber.filter.tags="@smoke or @regression"
      - name: Upload Cucumber Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: cucumber-report
          path: target/cucumber-report.html
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Cucumber OSS** | 無料 | オープンソース、MIT License |
| **Cucumber Reports** | 無料 | クラウドレポートサービス（パブリックリポジトリ） |
| **SmartBear CucumberStudio** | 有料（要問合せ） | BDDコラボレーション、テスト管理、チーム機能 |

## メリット

1. **ビジネスとの共通言語**: Gherkin構文により非エンジニアでもテストシナリオを理解・レビュー可能
2. **生きたドキュメント**: Featureファイルが仕様書とテストの両方の役割を果たす
3. **多言語対応**: Java、JavaScript、Ruby、Python、C#で利用可能
4. **シナリオ再利用**: Scenario OutlineとExamplesでデータ駆動テストが容易
5. **タグ管理**: テストの分類・フィルタリングによる柔軟な実行制御
6. **CI/CD統合**: JUnit/JSON レポート出力でCI/CDパイプラインと容易に連携
7. **BDDプロセス促進**: 開発前にシナリオを定義することで要件の明確化を促進
8. **日本語対応**: Gherkinは日本語キーワードに対応しており、日本語でシナリオ記述可能
9. **豊富なプラグイン**: Allure、Selenium、REST Assured等との連携プラグイン
10. **コミュニティ**: 大規模で活発なコミュニティとドキュメント

## デメリット

1. **シナリオ保守コスト**: Featureファイルとステップ定義の両方の保守が必要
2. **ステップ重複**: 類似ステップの重複・乱立が起きやすい
3. **実行速度**: ステップ解析のオーバーヘッドにより純粋なユニットテストより遅い
4. **過剰な詳細**: UI操作レベルの詳細なシナリオを書きがちで保守性が低下する
5. **学習コスト**: BDDの考え方とGherkin記法の習熟にチーム全体の教育が必要
6. **正規表現の複雑さ**: ステップ定義のパターンマッチングが複雑になりやすい
7. **デバッグ難度**: Featureファイルからステップ定義への遷移が分かりにくい場合がある
8. **チーム合意の必要性**: BDDプロセスの導入にはチーム全体の理解と協力が不可欠

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **SpecFlow** | C#/.NET向けBDD | CucumberのC#版、Visual Studio統合が強い |
| **behave** | Python向けBDD | CucumberのPython版、シンプルなAPI |
| **JBehave** | Java向けBDD | Cucumberより先発だがコミュニティが小さい |
| **Gauge** | ThoughtWorks製BDD | CucumberよりMarkdown寄りの構文 |
| **Robot Framework** | 汎用テスト自動化 | Cucumberよりキーワード駆動、Python基盤 |

## 公式リンク

- **公式サイト**: [https://cucumber.io/](https://cucumber.io/)
- **ドキュメント**: [https://cucumber.io/docs/cucumber/](https://cucumber.io/docs/cucumber/)
- **Gherkin構文**: [https://cucumber.io/docs/gherkin/](https://cucumber.io/docs/gherkin/)
- **GitHub**: [https://github.com/cucumber](https://github.com/cucumber)
- **Cucumber Reports**: [https://reports.cucumber.io/](https://reports.cucumber.io/)

## 関連ドキュメント

- [テストツール一覧](../テスト/)
- [Allure Report](./Allure_Report.md)
- [Robot Framework](./Robot_Framework.md)
- [Selenium](./Selenium.md)
- [BDDベストプラクティス](../../best-practices/bdd.md)

---

**カテゴリ**: テスト
**対象工程**: 要件定義・テスト・品質管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
