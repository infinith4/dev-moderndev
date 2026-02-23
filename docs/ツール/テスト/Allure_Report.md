# Allure Report

## 概要

Allure Reportは、テスト結果を視覚的にわかりやすく表示するためのオープンソースのレポーティングフレームワークである。JUnit、TestNG、pytest、Cucumber、Jest、Mocha等の主要テストフレームワークと連携し、インタラクティブなHTMLレポートを自動生成する。テスト結果のトレンド分析、タイムライン表示、カテゴリ分類、添付ファイル（スクリーンショット・ログ等）の表示機能を備え、CI/CDパイプラインに組み込むことで、テスト品質の継続的な可視化と改善サイクルを実現する。

## 主な機能

### 1. インタラクティブHTMLレポート
- **Overview**: テスト全体のサマリーダッシュボード
- **Suites**: テストスイート別の結果表示
- **Graphs**: 円グラフ・棒グラフによる統計表示
- **Timeline**: テスト実行のタイムライン表示

### 2. テスト結果分類
- **Categories**: エラー種別ごとの分類（Product Defects, Test Defects等）
- **Severity**: テストの重要度レベル設定（blocker, critical, normal, minor, trivial）
- **Behaviors**: BDD形式（Epic/Feature/Story）での階層表示
- **Packages**: パッケージ構造に沿った結果表示

### 3. トレンド分析
- **Trend**: 過去の実行結果との比較グラフ
- **Duration**: テスト実行時間の推移表示
- **Retry**: リトライ結果の追跡
- **History**: 各テストケースの実行履歴

### 4. 添付ファイルサポート
- **スクリーンショット**: UI テストの画面キャプチャ表示
- **ログファイル**: テスト実行時のログ添付
- **動画**: テスト実行の録画表示
- **カスタム添付**: JSON、XML、CSV等任意のファイル

### 5. テストフレームワーク連携
- **Java**: JUnit 4/5、TestNG、Cucumber-JVM
- **Python**: pytest、behave、Robot Framework
- **JavaScript**: Jest、Mocha、Jasmine、Cypress、Playwright
- **C#**: NUnit、xUnit.net、SpecFlow
- **その他**: Go、Ruby、PHP対応アダプタ

### 6. CI/CD統合
- **Jenkins**: Allure Jenkins Plugin
- **GitHub Actions**: allure-report アクション
- **GitLab CI**: アーティファクト連携
- **Azure DevOps**: パイプライン統合

## 利用方法

### インストール

```bash
# Homebrew (macOS/Linux)
brew install allure

# Scoop (Windows)
scoop install allure

# npm (Node.js)
npm install -g allure-commandline

# pip (Python)
pip install allure-commandline
```

### pytest連携

```bash
# アダプタインストール
pip install allure-pytest
```

```python
# test_example.py
import allure

@allure.feature("ユーザー管理")
@allure.story("ログイン機能")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success():
    """正常なログインのテスト"""
    with allure.step("ユーザー名とパスワードを入力"):
        username = "testuser"
        password = "password123"
    with allure.step("ログインボタンをクリック"):
        result = login(username, password)
    with allure.step("ログイン成功を確認"):
        assert result.status == "success"

@allure.feature("ユーザー管理")
@allure.story("ログイン機能")
def test_login_failure():
    """異常系ログインのテスト"""
    with allure.step("不正なパスワードでログイン"):
        result = login("testuser", "wrong_password")
    with allure.step("エラーメッセージを確認"):
        assert result.status == "failure"
```

```bash
# テスト実行とレポート生成
pytest --alluredir=allure-results
allure serve allure-results

# 静的HTMLレポート生成
allure generate allure-results -o allure-report --clean
```

### JUnit 5連携

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.qameta.allure</groupId>
    <artifactId>allure-junit5</artifactId>
    <version>2.25.0</version>
    <scope>test</scope>
</dependency>
```

```java
import io.qameta.allure.*;

@Epic("ユーザー管理")
@Feature("ログイン機能")
public class LoginTest {

    @Test
    @Severity(SeverityLevel.CRITICAL)
    @Description("正常なログインのテスト")
    void testLoginSuccess() {
        Allure.step("ユーザー名とパスワードを入力");
        Allure.step("ログインボタンをクリック");
        Allure.step("ログイン成功を確認");
    }
}
```

### カテゴリ定義

```json
// categories.json (allure-results ディレクトリに配置)
[
  {
    "name": "Product Defects",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*AssertionError.*"
  },
  {
    "name": "Test Defects",
    "matchedStatuses": ["broken"],
    "messageRegex": ".*NullPointerException.*"
  },
  {
    "name": "Known Issues",
    "matchedStatuses": ["failed"],
    "flaky": true
  }
]
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/test-report.yml
name: Test with Allure Report

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pytest allure-pytest
      - run: pytest --alluredir=allure-results
        continue-on-error: true
      - name: Get Allure history
        uses: actions/checkout@v4
        if: always()
        with:
          ref: gh-pages
          path: gh-pages
        continue-on-error: true
      - name: Generate Allure Report
        uses: simple-elf/allure-report-action@v1.9
        if: always()
        with:
          allure_results: allure-results
          allure_history: allure-history
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        if: always()
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: allure-history
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Allure Report** | 無料 | オープンソース、Apache 2.0 License |
| **Allure TestOps** | 有料（要問合せ） | テスト管理、チーム連携、ダッシュボード、Allure Report上位版 |

## メリット

1. **視覚的に優れたレポート**: インタラクティブなHTMLレポートでテスト結果を直感的に把握できる
2. **多言語・多フレームワーク対応**: Java、Python、JavaScript、C#等の主要言語・フレームワークと連携可能
3. **トレンド分析**: 過去の実行結果と比較してテスト品質の推移を追跡できる
4. **ステップ表示**: テスト内の各ステップが可視化され、障害箇所の特定が容易
5. **添付ファイル対応**: スクリーンショットやログを直接レポートに埋め込み可能
6. **CI/CD統合**: Jenkins、GitHub Actions、GitLab CI等と容易に連携
7. **BDD対応**: Epic/Feature/Story形式での結果表示が可能
8. **オープンソース**: 無料で利用でき、活発なコミュニティサポート
9. **カテゴリ分類**: エラーを自動分類し、Product DefectsとTest Defectsを区別可能
10. **軽量**: CLIツールのみで動作し、複雑なインフラ不要

## デメリット

1. **レポート保存管理**: 静的HTMLファイルのホスティング・保存方針の設計が必要
2. **Allure TestOps依存**: 高度なチーム連携機能は有料版が必要
3. **初期設定コスト**: テストフレームワークごとにアダプタ設定が必要
4. **履歴データ管理**: トレンド表示には過去のallure-resultsの保持が必要
5. **大量テスト時のパフォーマンス**: テストケース数が非常に多い場合、レポート生成に時間がかかる
6. **カスタマイズ制限**: レポートのレイアウト・デザインの変更は限定的
7. **Java依存**: Allure CLIの実行にJava Runtime Environmentが必要
8. **学習コスト**: アノテーション・デコレータの効果的な活用には習熟が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **ExtentReports** | Java/C#向けHTMLレポート | Allureより設定が簡単だがトレンド機能が弱い |
| **ReportPortal** | AI分析付きレポート管理 | Allureより高機能だがサーバー構築が必要 |
| **TestRail** | テスト管理ツール | Allureより管理機能充実だが有料 |
| **Mochawesome** | Mocha専用レポート | Allureよりシンプルだが対応FW限定 |
| **pytest-html** | pytest専用HTMLレポート | Allureより軽量だが機能が限定的 |

## 公式リンク

- **公式サイト**: [https://allurereport.org/](https://allurereport.org/)
- **ドキュメント**: [https://allurereport.org/docs/](https://allurereport.org/docs/)
- **GitHub**: [https://github.com/allure-framework](https://github.com/allure-framework)
- **Allure pytest**: [https://allurereport.org/docs/pytest/](https://allurereport.org/docs/pytest/)
- **Allure JUnit 5**: [https://allurereport.org/docs/junit5/](https://allurereport.org/docs/junit5/)

## 関連ドキュメント

- [テストツール一覧](../テスト/)
- [pytest](./pytest.md)
- [JUnit](./JUnit.md)
- [Cucumber](./Cucumber.md)
- [CI/CDベストプラクティス](../../best-practices/cicd.md)

---

**カテゴリ**: テスト
**対象工程**: テスト・品質管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
