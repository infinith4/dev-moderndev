# TestRail

## 概要

TestRailは、Gurock Software（現IDERA）が提供するWebベースのテスト管理プラットフォームです。テストケースの作成・管理、テスト計画の策定、テスト実行の記録、結果のレポーティングを一元管理します。Jira、Azure DevOps、GitHub等のプロジェクト管理ツールとの統合、JUnit/pytest等の自動テスト結果のインポート、REST APIによるカスタム連携に対応し、手動テストと自動テストの統合管理を実現します。

## 主な機能

### 1. テストケース管理

- **テストケース作成**: ステップ・期待結果・前提条件を含むケース定義
- **セクション分類**: ツリー構造によるテストケースの階層管理
- **テストタイプ**: 機能テスト、回帰テスト、スモークテスト等のラベル
- **テンプレート**: カスタムテンプレートによるケース標準化
- **カスタムフィールド**: 自動化状態、優先度等の追加フィールド定義

### 2. テスト計画・実行

- **テストラン**: テストケースのサブセットを選択して実行管理
- **テストプラン**: 複数のテストランをまとめた計画管理
- **マイルストーン**: リリースサイクルに紐づいたテスト進捗管理
- **テスト結果**: Passed/Failed/Blocked/Retest等のステータス記録
- **再テスト**: 失敗ケースの再テスト実行とステータス追跡

### 3. レポート・ダッシュボード

- **進捗レポート**: テスト実行の進捗率・合格率をリアルタイム表示
- **比較レポート**: 複数テストラン間の結果比較
- **欠陥レポート**: 不具合発見率の推移分析
- **カスタムレポート**: 条件指定による任意のレポート生成

### 4. 自動テスト統合

- **REST API**: テスト結果の自動アップロード
- **JUnit XML**: 自動テスト結果のインポート
- **Webhook**: テスト完了イベントの通知
- **CLI**: コマンドラインからのテスト結果送信

### 5. 外部ツール連携

- **Jira**: 不具合チケットの自動作成・リンク
- **Azure DevOps**: Work Itemとの双方向連携
- **GitHub**: Issue連携
- **Slack**: テスト結果の通知

## 利用方法

### セットアップ

```
1. https://www.testrail.com/ でアカウント作成（Cloud版）
   または オンプレミス版をサーバーにインストール
2. プロジェクトを作成
3. テストスイート/セクションを定義
4. テストケースを作成
5. テストランを作成して実行開始
```

### REST APIによるテスト結果送信

```bash
# テストランの結果追加
curl -X POST "https://yourinstance.testrail.io/index.php?/api/v2/add_result/12345" \
  -H "Content-Type: application/json" \
  -u "user@example.com:api_key" \
  -d '{
    "status_id": 1,
    "comment": "Test passed successfully",
    "elapsed": "30s"
  }'

# テスト結果の一括追加
curl -X POST "https://yourinstance.testrail.io/index.php?/api/v2/add_results_for_run/1" \
  -H "Content-Type: application/json" \
  -u "user@example.com:api_key" \
  -d '{
    "results": [
      {"case_id": 1, "status_id": 1, "comment": "Passed"},
      {"case_id": 2, "status_id": 5, "comment": "Failed", "defects": "JIRA-123"}
    ]
  }'
```

### Python連携（pytest-testrail）

```bash
# プラグインインストール
pip install pytest-testrail
```

```python
# conftest.py
import pytest

# テストケースIDを紐付け
@pytest.mark.testrail('C12345')
def test_login():
    assert login("user", "pass") == True

@pytest.mark.testrail('C12346')
def test_logout():
    assert logout() == True
```

```bash
# TestRailに結果を送信しながらテスト実行
pytest --testrail \
  --tr-url=https://yourinstance.testrail.io \
  --tr-email=user@example.com \
  --tr-password=api_key \
  --tr-testrun-name="Automated Run"
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/test-report.yml
name: Test & Report to TestRail

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: |
          pytest --junitxml=results.xml
      - name: Upload to TestRail
        env:
          TESTRAIL_URL: ${{ secrets.TESTRAIL_URL }}
          TESTRAIL_USER: ${{ secrets.TESTRAIL_USER }}
          TESTRAIL_KEY: ${{ secrets.TESTRAIL_KEY }}
        run: |
          pip install trcli
          trcli -y -h "$TESTRAIL_URL" \
            --project "MyProject" \
            -u "$TESTRAIL_USER" \
            -p "$TESTRAIL_KEY" \
            parse_junit \
            --title "Automated Run $(date)" \
            -f results.xml
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **TestRail Cloud** | 有料（ユーザー単位/月額） | SaaS版、即時利用可能 |
| **TestRail Server** | 有料（年額） | オンプレミス版、自社サーバーに配置 |
| **Free Trial** | 30日間無料 | 全機能利用可能 |

## メリット

1. **テスト資産一元管理**: テストケース・計画・結果・不具合を一箇所で管理
2. **トレーサビリティ**: 要件→テストケース→不具合の追跡が容易
3. **豊富なレポート**: 進捗率、合格率、欠陥分析等のレポートを自動生成
4. **自動テスト統合**: REST API/JUnit/trcliで自動テスト結果を統合
5. **Jira連携**: 不具合チケットの自動作成・双方向リンク
6. **マイルストーン管理**: リリースサイクルに紐づいたテスト進捗の可視化
7. **カスタマイズ**: カスタムフィールド・テンプレート・ワークフローの定義

## デメリット

1. **有料**: 無料版がなく、ユーザー数に応じたライセンス費用が発生
2. **学習コスト**: テストスイート/ラン/プランの概念理解とプロセス設計が必要
3. **過剰管理**: 小規模プロジェクトにはオーバースペックになりやすい
4. **UIの古さ**: モダンなSaaSツールと比較するとUI/UXが古め
5. **カスタマイズ制限**: レポートやワークフローのカスタマイズに限界がある

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Xray for Jira** | Jiraアドオン | TestRailよりJira統合が深い、Jira内で完結 |
| **Zephyr Scale** | Jiraアドオン | TestRailと同等機能、Jira内でテスト管理 |
| **qTest** | テスト管理プラットフォーム | TestRailより大規模向け、AI機能搭載 |
| **Azure Test Plans** | Azure DevOps機能 | TestRailよりMicrosoft統合が強い |

## 公式リンク

- **公式サイト**: [https://www.testrail.com/](https://www.testrail.com/)
- **ドキュメント**: [https://support.testrail.com/](https://support.testrail.com/)
- **API Reference**: [https://support.testrail.com/hc/en-us/articles/7077196481428-Introduction-to-the-TestRail-API](https://support.testrail.com/hc/en-us/articles/7077196481428-Introduction-to-the-TestRail-API)
- **trcli**: [https://github.com/gurock/trcli](https://github.com/gurock/trcli)

## 関連ドキュメント

- [Xray](./Xray.md)
- [Allure Report](./Allure_Report.md)

---

**カテゴリ**: テスト
**対象工程**: テスト管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
