# Xray

## 概要

Xrayは、Atlassian Jiraに統合されるテスト管理アドオンです。Jira課題としてテストケース、テストセット、テストプラン、テスト実行を管理し、要件（Story/Epic）→テストケース→不具合（Bug）の完全なトレーサビリティを実現します。JUnit/TestNG/pytest等の自動テスト結果のインポート、Cucumber/Behaveとの BDD統合、REST APIによるCI/CDパイプライン連携に対応し、Jiraを離れることなくテストライフサイクル全体を管理できます。

## 主な機能

### 1. テスト管理（Jira課題タイプ）

- **Test**: テストケースの定義（手動ステップ、Gherkin、汎用）
- **Test Set**: テストケースのグループ化
- **Test Plan**: テスト計画（リリース/スプリントに紐づけ）
- **Test Execution**: テスト実行と結果記録
- **Pre-Condition**: テストの前提条件定義

### 2. トレーサビリティ

- **要件カバレッジ**: Story/Epic→Testの紐付けとカバレッジ率表示
- **不具合リンク**: テスト失敗→Bugチケットの自動/手動リンク
- **カバレッジレポート**: 要件ごとのテスト充足度可視化
- **インパクト分析**: 要件変更時の影響テストケース特定

### 3. BDD（振る舞い駆動開発）

- **Gherkinエディタ**: Jira上でFeature/Scenarioを直接編集
- **Cucumber統合**: Feature fileのエクスポート/インポート
- **Behave統合**: Python BDDフレームワーク対応
- **自動同期**: Gherkinシナリオとテスト結果の自動同期

### 4. 自動テスト統合

- **JUnit/TestNG**: Javaテスト結果のインポート
- **pytest**: Pythonテスト結果のインポート
- **Robot Framework**: RFテスト結果のインポート
- **NUnit/xUnit**: .NETテスト結果のインポート
- **Cucumber JSON**: BDDテスト結果のインポート

### 5. レポート・ダッシュボード

- **テスト実行レポート**: 合格/不合格/未実行の進捗表示
- **トレーサビリティマトリクス**: 要件×テストのカバレッジマトリクス
- **Jiraダッシュボードガジェット**: カスタムダッシュボードへの統合
- **リリースレポート**: リリースバージョンごとのテスト品質サマリ

## 利用方法

### インストール

```
# Jira Cloud版
1. Atlassian Marketplace で "Xray Test Management for Jira" を検索
2. "Try it free" で30日間トライアル開始
3. Jiraプロジェクトの課題タイプにXrayタイプが自動追加される

# Jira Data Center版
1. Jira管理画面 → Manage apps → Find new apps
2. "Xray" を検索してインストール
3. ライセンスキーを入力
```

### テストケース作成（手動テスト）

```
1. Jiraプロジェクトで「Create Issue」→ 課題タイプ「Test」を選択
2. テストタイプ: 「Manual」を選択
3. テストステップを追加:
   Step 1: ログインページにアクセスする → Expected: ログインフォームが表示される
   Step 2: ユーザー名とパスワードを入力する → Expected: 入力が反映される
   Step 3: ログインボタンをクリックする → Expected: ダッシュボードに遷移する
4. 要件（Story）にリンク: 「Tests」リンクで対象Storyを紐付け
```

### REST APIによるテスト結果インポート

```bash
# JUnit XML結果のインポート
curl -X POST "https://yourjira.atlassian.net/rest/raven/2.0/import/execution/junit" \
  -H "Content-Type: multipart/form-data" \
  -H "Authorization: Bearer ${XRAY_TOKEN}" \
  -F "file=@test-results.xml" \
  -F "projectKey=MYPROJ" \
  -F "testPlanKey=MYPROJ-100"

# Cucumber JSON結果のインポート
curl -X POST "https://yourjira.atlassian.net/rest/raven/2.0/import/execution/cucumber" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${XRAY_TOKEN}" \
  -d @cucumber-report.json

# GraphQL API（Xray Cloud）
curl -X POST "https://xray.cloud.getxray.app/api/v2/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${XRAY_TOKEN}" \
  -d '{"query": "{ getTests(jql: \"project = MYPROJ\", limit: 10) { results { issueId jira(fields: [\"summary\"]) } } }"}'
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/xray-report.yml
name: Test & Report to Xray

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: pytest --junitxml=results.xml
      - name: Import Results to Xray
        env:
          XRAY_CLIENT_ID: ${{ secrets.XRAY_CLIENT_ID }}
          XRAY_CLIENT_SECRET: ${{ secrets.XRAY_CLIENT_SECRET }}
        run: |
          # Xray Cloud認証トークン取得
          TOKEN=$(curl -s -X POST "https://xray.cloud.getxray.app/api/v2/authenticate" \
            -H "Content-Type: application/json" \
            -d "{\"client_id\": \"$XRAY_CLIENT_ID\", \"client_secret\": \"$XRAY_CLIENT_SECRET\"}" | tr -d '"')
          # JUnit結果インポート
          curl -X POST "https://xray.cloud.getxray.app/api/v2/import/execution/junit" \
            -H "Content-Type: application/xml" \
            -H "Authorization: Bearer $TOKEN" \
            --data-binary @results.xml
```

### Cucumber BDD統合

```gherkin
# login.feature（Xrayから同期）
@MYPROJ-200
Feature: ユーザーログイン

  @MYPROJ-201
  Scenario: 正常なログイン
    Given ログインページが表示されている
    When ユーザー名 "admin" とパスワード "password" を入力する
    And ログインボタンをクリックする
    Then ダッシュボードが表示される

  @MYPROJ-202
  Scenario: 不正なパスワードでログイン
    Given ログインページが表示されている
    When ユーザー名 "admin" とパスワード "wrong" を入力する
    And ログインボタンをクリックする
    Then エラーメッセージが表示される
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Xray Cloud** | 有料（ユーザー数ベース/月額） | Jira Cloud向け、SaaS |
| **Xray Data Center** | 有料（年額） | Jira Data Center向け、オンプレミス |
| **Free Trial** | 30日間無料 | 全機能利用可能 |

## メリット

1. **Jira完全統合**: テストケースがJira課題として管理され、検索・フィルタ・ワークフローを活用可能
2. **トレーサビリティ**: 要件→テスト→不具合の完全な追跡とカバレッジ可視化
3. **BDD対応**: Gherkinエディタ＋Cucumber統合でBDDワークフローを実現
4. **自動テスト統合**: JUnit/pytest/NUnit等の結果を自動インポート
5. **REST/GraphQL API**: CI/CDパイプラインとの柔軟な連携
6. **豊富なレポート**: テスト進捗、カバレッジ、トレーサビリティマトリクスの自動生成
7. **マーケットプレイス上位**: Jiraテスト管理アドオンで最も評価が高い

## デメリット

1. **Jira依存**: Jiraを使用していないチームには導入不可
2. **ライセンス費用**: ユーザー数が多いとコストが大きくなる
3. **学習コスト**: Test/Test Set/Test Plan/Test Execution等の概念理解が必要
4. **Jira Cloud制限**: Jira Cloud版はData Center版より一部機能が制限される
5. **パフォーマンス**: 大規模プロジェクトでJiraのパフォーマンスに影響する場合がある

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Zephyr Scale** | Jiraアドオン | Xrayと同等のJira統合、UIが異なる |
| **TestRail** | 独立テスト管理ツール | Xrayよりスタンドアロン、Jira外で管理 |
| **Azure Test Plans** | Azure DevOps機能 | Microsoft環境向け、Azure DevOps統合 |
| **qTest** | テスト管理プラットフォーム | Xrayより大規模向け、独立プラットフォーム |

## 公式リンク

- **公式サイト**: [https://www.getxray.app/](https://www.getxray.app/)
- **ドキュメント**: [https://docs.getxray.app/](https://docs.getxray.app/)
- **Atlassian Marketplace**: [https://marketplace.atlassian.com/apps/1211769/xray-test-management-for-jira](https://marketplace.atlassian.com/apps/1211769/xray-test-management-for-jira)
- **API Reference**: [https://docs.getxray.app/display/XRAYCLOUD/REST+API](https://docs.getxray.app/display/XRAYCLOUD/REST+API)
- **GitHub（Examples）**: [https://github.com/Xray-App](https://github.com/Xray-App)

## 関連ドキュメント

- [TestRail](./TestRail.md)
- [Cucumber](./Cucumber.md)
- [Allure Report](./Allure_Report.md)

---

**カテゴリ**: テスト
**対象工程**: テスト管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
