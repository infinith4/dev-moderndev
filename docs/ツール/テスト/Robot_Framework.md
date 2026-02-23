# Robot Framework

## 概要

Robot Frameworkは、Python製のオープンソースキーワード駆動テスト自動化フレームワークです。受入テスト、E2Eテスト、RPA（ロボティック・プロセス・オートメーション）に広く利用されています。テストケースは人間が読みやすい表形式（`.robot`ファイル）で記述され、非開発者でもテストの内容を理解・レビューできます。SeleniumLibrary、RequestsLibrary、BrowserLibraryなど豊富な外部ライブラリを組み合わせることで、Web UI、API、データベース、モバイルなど多様なテスト対象をカバーできます。

## 主な機能

### 1. キーワード駆動テスト

- **BuiltInキーワード**: `Log`、`Should Be Equal`、`Run Keyword If`、`Set Variable`など標準キーワード群
- **ユーザーキーワード**: 複数キーワードを組み合わせた再利用可能なカスタムキーワードの定義
- **リソースファイル**: キーワードや変数を`.resource`ファイルに分離して共有
- **タグベース実行**: テストケースにタグを付与し、選択的に実行

### 2. テストライブラリ

- **SeleniumLibrary**: Selenium WebDriverベースのブラウザ操作自動化
- **BrowserLibrary**: Playwright ベースの次世代ブラウザ自動化
- **RequestsLibrary**: REST APIテスト用HTTPクライアント
- **DatabaseLibrary**: データベースへの接続・クエリ実行
- **SSHLibrary**: SSH経由のリモートコマンド実行
- **AppiumLibrary**: モバイルアプリのテスト自動化

### 3. レポート・ログ

- **HTML形式レポート**: テスト結果のサマリーレポート（`report.html`）自動生成
- **詳細ログ**: 各キーワードの実行詳細ログ（`log.html`）
- **XML出力**: `output.xml`による機械処理用結果ファイル
- **スクリーンショット**: テスト失敗時の自動スクリーンショット取得

### 4. データ駆動テスト

- **テストテンプレート**: `[Template]`によるデータ駆動テストの記述
- **変数ファイル**: Python/YAML/JSONから変数を読み込み
- **FOR ループ**: 繰り返し処理によるパラメータ化テスト

## 利用方法

### インストール

```bash
# pipでインストール
pip install robotframework

# SeleniumLibrary追加
pip install robotframework-seleniumlibrary

# RequestsLibrary追加
pip install robotframework-requests

# BrowserLibrary追加（Playwrightベース）
pip install robotframework-browser
rfbrowser init

# バージョン確認
robot --version
```

### 基本的なテストケース（.robotファイル）

```robot
*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}         https://example.com
${BROWSER}     chrome

*** Test Cases ***
ログインページが表示されること
    [Tags]    smoke
    Open Browser    ${URL}    ${BROWSER}
    Title Should Be    Example Domain
    [Teardown]    Close Browser

検索機能が正しく動作すること
    [Tags]    regression
    Open Browser    ${URL}/search    ${BROWSER}
    Input Text    id=search-input    Robot Framework
    Click Button    id=search-button
    Wait Until Element Is Visible    id=results
    Page Should Contain    検索結果
    [Teardown]    Close Browser
```

### APIテストの例

```robot
*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Test Cases ***
ユーザー一覧を取得できること
    Create Session    api    https://jsonplaceholder.typicode.com
    ${response}=    GET On Session    api    /users
    Status Should Be    200    ${response}
    ${length}=    Get Length    ${response.json()}
    Should Be True    ${length} > 0

ユーザーを作成できること
    Create Session    api    https://jsonplaceholder.typicode.com
    ${body}=    Create Dictionary    name=Test User    email=test@example.com
    ${response}=    POST On Session    api    /users    json=${body}
    Status Should Be    201    ${response}
```

### データ駆動テスト

```robot
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
ログイン検証
    [Template]    ログインテスト実行
    admin       password123    Welcome
    user1       pass456        Welcome
    invalid     wrong          Login Failed

*** Keywords ***
ログインテスト実行
    [Arguments]    ${username}    ${password}    ${expected}
    Open Browser    https://example.com/login    chrome
    Input Text    id=username    ${username}
    Input Text    id=password    ${password}
    Click Button    id=login-btn
    Page Should Contain    ${expected}
    [Teardown]    Close Browser
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/robot-tests.yml
name: Robot Framework Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install robotframework
          pip install robotframework-seleniumlibrary
          pip install robotframework-requests
      - name: Run Robot Framework tests
        run: |
          robot --outputdir results tests/
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: robot-results
          path: results/
```

### Jenkins Pipeline統合

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install robotframework robotframework-seleniumlibrary'
                sh 'robot --outputdir results --xunit xunit.xml tests/'
            }
            post {
                always {
                    robot outputPath: 'results',
                          logFileName: 'log.html',
                          outputFileName: 'output.xml',
                          reportFileName: 'report.html'
                    junit 'results/xunit.xml'
                }
            }
        }
    }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Robot Framework（OSS）** | 無料 | Apache License 2.0、全機能利用可能 |
| **Robocorp（RPA向け）** | 無料/有料 | Robot FrameworkベースのRPAプラットフォーム |

## メリット

1. **可読性が高い**: 非開発者でもテストケースの内容を理解・レビューできる
2. **豊富なライブラリ**: SeleniumLibrary、RequestsLibrary、DatabaseLibraryなど多数の外部ライブラリが利用可能
3. **拡張性**: Pythonでカスタムライブラリを容易に作成可能
4. **レポート自動生成**: HTML形式の詳細レポート・ログを標準で出力
5. **タグベース実行**: テストの選択実行やスキップが柔軟に設定可能
6. **データ駆動テスト**: テンプレート機能でパラメータ化テストを簡潔に記述
7. **RPA対応**: テスト自動化だけでなくRPA用途にも活用可能
8. **CI/CD統合**: Jenkins、GitHub Actions、GitLab CIなど主要CIツールとの統合が容易

## デメリット

1. **キーワード設計の難しさ**: 大規模プロジェクトではキーワードの粒度・命名規則の統制が必要
2. **実行速度**: Pythonベースのため、コンパイル言語のフレームワークと比較すると実行速度が劣る
3. **IDEサポートが限定的**: `.robot`ファイル向けの高度なIDE支援はVSCode拡張に依存
4. **デバッグ**: キーワード駆動のためステップ実行デバッグがやや困難
5. **学習コスト**: Robot Framework独自の構文やキーワードの習得が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Selenium** | ブラウザ自動化ライブラリ | Robot Frameworkより低レベル、直接コードで制御 |
| **Playwright** | Microsoft製ブラウザ自動化 | 高速、自動待機機能が充実 |
| **Cypress** | JavaScript E2Eテスト | フロントエンド特化、開発者向け |
| **Cucumber** | BDDテストフレームワーク | Gherkin構文、ステップ定義が必要 |
| **pytest** | Pythonテストフレームワーク | Robot Frameworkより開発者向け、コードベース |

## 公式リンク

- **公式サイト**: [https://robotframework.org/](https://robotframework.org/)
- **ユーザーガイド**: [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
- **GitHub**: [https://github.com/robotframework/robotframework](https://github.com/robotframework/robotframework)
- **ライブラリ一覧**: [https://robotframework.org/#libraries](https://robotframework.org/#libraries)
- **PyPI**: [https://pypi.org/project/robotframework/](https://pypi.org/project/robotframework/)

## 関連ドキュメント

- [Selenium](./Selenium.md)
- [Cucumber](./Cucumber.md)
- [Playwright](./Playwright.md)
- [Appium](./Appium.md)

---

**カテゴリ**: テスト
**対象工程**: 受入テスト・E2Eテスト・RPA
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
