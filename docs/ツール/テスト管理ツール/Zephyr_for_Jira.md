# Zephyr for Jira

## 概要

Zephyr for Jiraは、Atlassian Jiraに統合されたテスト管理ツールです。Jira課題（Issue）とシームレスに連携し、テストケース作成、テスト実行、結果記録、レポート生成をJira内で完結できます。アジャイル・ウォーターフォール両方の開発手法に対応し、テストプロセスの可視化とトレーサビリティを向上させます。

## 主な機能

### 1. テストケース管理
- **テストケース作成**: Jira内でテストケース記述
- **ステップ管理**: テスト手順のステップ化
- **前提条件**: テスト実行の前提条件記載
- **期待結果**: 各ステップの期待結果定義

### 2. テスト実行管理
- **テストサイクル**: スプリント・リリース単位でテスト管理
- **テスト実行記録**: 合格/不合格/スキップ/ブロック
- **欠陥リンク**: テスト失敗時にJira課題へリンク
- **エビデンス添付**: スクリーンショット、ログ添付

### 3. Jira統合
- **要件トレーサビリティ**: Jira Story ⇔ Test連携
- **ワークフロー統合**: Jiraステータスと同期
- **ダッシュボード**: Jiraダッシュボードにテストメトリクス表示
- **課題リンク**: 不具合チケットと自動リンク

### 4. レポート・メトリクス
- **テストサマリー**: 実行率、合格率
- **トレーサビリティマトリクス**: 要件 ⇔ テストカバレッジ
- **欠陥分析**: 不具合傾向分析
- **カスタムレポート**: カスタマイズ可能なレポート

### 5. アジャイル対応
- **スプリント連携**: Jiraスプリントとテストサイクル連動
- **カンバンボード**: テスト進捗可視化
- **バーンダウン**: テスト進捗チャート
- **自動化統合**: CI/CDパイプライン連携

### 6. 自動化テスト統合
- **Cucumber**: BDDテスト連携
- **Selenium**: E2Eテスト結果取り込み
- **JUnit/TestNG**: ユニットテスト結果
- **Jenkins/Bamboo**: CI/CD統合

## 利用方法

### インストール（Jira Cloud）

```
1. Jira管理者でログイン
2. Settings → Apps → Find new apps
3. "Zephyr Scale" または "Zephyr Squad" を検索
4. Install（30日間無料トライアル）
5. ライセンス購入後、継続利用
```

### Zephyr Squadの基本操作

```
# テストケース作成
1. Jira Project → Tests → Create Test
2. Summary: "ログイン機能テスト"
3. Steps:
   - Step 1: ユーザー名とパスワードを入力
     Expected Result: 入力フィールドに値が表示される
   - Step 2: ログインボタンをクリック
     Expected Result: ダッシュボード画面に遷移する

# テストサイクル作成
1. Tests → Test Cycles → Create Test Cycle
2. Name: "Sprint 10 テスト"
3. Version: v1.2.0
4. 開始日・終了日設定

# テスト実行
1. Test Cycle を開く
2. Add Tests → テストケース選択
3. Execute → テストを実行
4. 各ステップの結果を記録（Pass / Fail / WIP / Blocked）
5. 失敗時はDefect（不具合）をリンク

# 不具合リンク
1. テスト失敗時に "Create Defect"
2. Jira Bugチケットが自動作成され、テストにリンク
```

### Zephyr Scaleの高度な機能

```
# フォルダ構造でテストケース整理
Tests/
  ├── Smoke Tests/
  │   ├── Login Test
  │   └── Logout Test
  ├── Regression Tests/
  │   └── Payment Flow Test
  └── Integration Tests/

# テストプラン作成
1. Test Plans → Create Test Plan
2. テストサイクルを複数含むプラン作成
3. リリース全体のテスト計画管理

# トレーサビリティ
1. Test Case → Link → "Tests" → Jira Story
2. 要件（Story）とテストケースの紐付け
3. Traceability Report で要件カバレッジ確認
```

### 自動化テスト統合（Cucumber）

```gherkin
# feature/login.feature
Feature: Login functionality

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should be redirected to dashboard

# Cucumberテスト実行後、結果をZephyrへ送信
mvn test -Dcucumber.options="--plugin io.cucumber.jira.ZephyrReporter"
```

### REST APIでテスト結果送信

```bash
# Zephyr Scale API例（テスト実行結果送信）
curl -X POST "https://api.zephyrscale.smartbear.com/v2/testexecutions" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "projectKey": "PROJ",
    "testCaseKey": "PROJ-T123",
    "testCycleKey": "PROJ-R1",
    "statusName": "Pass",
    "executedById": "user@example.com",
    "executionTime": 5000,
    "comment": "テスト成功"
  }'
```

### Jenkins統合

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Publish to Zephyr') {
            steps {
                // Zephyr Scaleプラグインでテスト結果送信
                zephyrScale(
                    serverAddress: 'https://api.zephyrscale.smartbear.com',
                    projectKey: 'PROJ',
                    autoCreateTestCases: true,
                    testResultsFile: 'target/surefire-reports/*.xml'
                )
            }
        }
    }
}
```

## エディション・料金

### Zephyr Squad (シンプル版)

| エディション | 価格（月額） | 特徴 |
|-------------|-------------|------|
| **Free** | 🟢 無料 | 10ユーザーまで、基本機能 |
| **Standard** | 💰 $10/ユーザー | カスタムフィールド、レポート |
| **Premium** | 💰 $30/ユーザー | API、自動化統合、高度なレポート |

### Zephyr Scale (エンタープライズ版)

| エディション | 価格（月額） | 特徴 |
|-------------|-------------|------|
| **Free** | 🟢 無料 | 10ユーザーまで、基本機能 |
| **Standard** | 💰 $39/ユーザー | テストプラン、フォルダ階層、カスタムフィールド |
| **Premium** | 💰 $59/ユーザー | API、BDD、CI/CD統合、SLA |
| **Enterprise** | 💰 要問い合わせ | オンプレミス、専用サポート |

## メリット

### ✅ 主な利点

1. **Jira統合**: シームレスなJira連携
2. **トレーサビリティ**: 要件 ⇔ テストの紐付け
3. **アジャイル対応**: スプリント・カンバン統合
4. **自動化統合**: Cucumber、Selenium、JUnit連携
5. **CI/CD統合**: Jenkins、Bamboo、GitHub Actions
6. **レポート機能**: テストメトリクス可視化
7. **学習容易**: Jiraユーザーなら習得容易
8. **無料プラン**: 10ユーザーまで無料
9. **エコシステム**: Atlassianエコシステム活用
10. **サポート**: Atlassianの充実したサポート

## デメリット

### ❌ 制約・課題

1. **Jira依存**: Jiraライセンス必須
2. **コスト**: ユーザー数増加で高額
3. **パフォーマンス**: 大規模テストケースで遅延
4. **カスタマイズ制限**: UIカスタマイズに限界
5. **学習曲線**: 高度な機能は習得に時間
6. **オフライン不可**: クラウド版はインターネット必須
7. **移行困難**: 他ツールからの移行が手間
8. **Squadとの違い**: SquadとScaleで機能差大きい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **TestRail** | 専用テスト管理ツール | Zephyrより高機能だがJira統合弱い |
| **Xray for Jira** | Jira統合テスト管理 | Zephyrと類似、競合製品 |
| **qTest** | エンタープライズテスト管理 | Zephyrより高機能だが高価 |
| **PractiTest** | クラウドテスト管理 | Zephyrより専門的 |
| **TestLink** | オープンソーステスト管理 | Zephyrより無料だが機能限定的 |

## 公式リンク

- **Zephyr Scale**: [https://www.getzephyr.com/products/zephyr-scale](https://www.getzephyr.com/products/zephyr-scale)
- **Zephyr Squad**: [https://www.getzephyr.com/products/zephyr-squad](https://www.getzephyr.com/products/zephyr-squad)
- **ドキュメント**: [https://support.smartbear.com/zephyr-scale-cloud/docs/](https://support.smartbear.com/zephyr-scale-cloud/docs/)
- **API**: [https://support.smartbear.com/zephyr-scale-cloud/api-docs/](https://support.smartbear.com/zephyr-scale-cloud/api-docs/)
- **Marketplace**: [https://marketplace.atlassian.com/apps/1213259/zephyr-scale-test-management-for-jira](https://marketplace.atlassian.com/apps/1213259/zephyr-scale-test-management-for-jira)

## 関連ドキュメント

- [テスト管理ツール一覧](../テスト管理ツール/)
- [JIRA](../プロジェクト管理ツール/JIRA.md)
- [Selenium](../テストツール/Selenium.md)
- [Cucumber](../テストツール/Cucumber.md)
- [テスト管理ベストプラクティス](../../best-practices/test-management.md)

---

**カテゴリ**: テスト管理ツール  
**対象工程**: テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
