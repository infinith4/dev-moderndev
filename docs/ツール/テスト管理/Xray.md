# Xray

## 概要

Xray は、Jira に統合されるテスト管理ツールである。要件、テストケース、実行結果、不具合を Jira 課題として連携し、トレーサビリティを強化しやすい。手動テストと自動テストの結果統合にも対応する。

## 料金

| プラン | 内容 |
|------|------|
| Xray Cloud / Data Center | 有料 |
| Trial | 無料トライアルあり |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Jira完全統合 | 課題管理とテスト管理を同一基盤で運用 |
| トレーサビリティ | 要件→テスト→不具合を追跡しやすい |
| BDD対応 | Gherkin シナリオ連携が可能 |
| 自動結果取込 | JUnit/pytest/Cucumber などを取り込み可能 |
| API連携 | REST/GraphQL で自動化しやすい |
| レポート機能 | カバレッジと実行進捗を可視化 |

## 主な機能

### テスト管理機能

| 機能 | 説明 |
|------|------|
| Test Issue | テストケースを課題として管理 |
| Test Plan | リリース単位で計画管理 |
| Test Execution | 実行結果を記録・追跡 |
| Pre-Condition | テスト前提条件を定義 |

### トレーサビリティ機能

| 機能 | 説明 |
|------|------|
| 要件リンク | Story/Epic と Test を紐付け |
| 不具合リンク | 失敗結果を Bug に接続 |
| カバレッジ確認 | 要件単位のテスト充足を可視化 |
| 影響分析 | 変更時の再テスト対象を把握 |

### 自動化連携機能

| 機能 | 説明 |
|------|------|
| JUnit/pytest取込 | 自動テスト結果を反映 |
| Cucumber連携 | BDDシナリオ結果を取り込み |
| CI連携 | GitHub Actions/Jenkins 等と連携 |
| API操作 | 実行結果登録を自動化 |

## インストールとセットアップ

公式URL:
- [Xray 公式サイト](https://www.getxray.app/)
- [Documentation](https://docs.getxray.app/)
- [Atlassian Marketplace](https://marketplace.atlassian.com/apps/1211769/xray-test-management-for-jira)
- [API Reference](https://docs.getxray.app/display/XRAYCLOUD/REST+API)

セットアップの要点:
1. Jira に Xray アプリを導入する。
2. プロジェクトに Test / Test Plan / Test Execution を有効化する。
3. 要件課題とテスト課題のリンクルールを決める。
4. CI からの結果インポート方式を統一する。

## 基本的な使い方

1. Test 課題で手動テストケースを作成する。
2. Story/Epic とリンクして要件カバレッジを確保する。
3. Test Plan と Test Execution を作成して実行する。
4. 失敗時は Bug と関連付けて対応状況を追跡する。
5. 自動テスト結果を API でインポートする。

最小実行例:
- 手動運用: `Test` + `Test Execution` で結果記録
- 自動連携: JUnit XML を Xray API へ送信

## メリット

- Jira運用と統合し、情報分散を減らしやすい。
- 要件カバレッジを可視化し、監査対応を行いやすい。
- BDD/自動テスト結果を同一画面で管理しやすい。

## デメリット

- Jira 未導入環境では活用しづらい。
- 利用規模に応じたライセンスコストが必要。
- 課題タイプ設計を誤ると運用が複雑化しやすい。

## CI/CD での使用

CI ではテスト実行後に JUnit/Cucumber 結果を Xray に送信し、手動テスト結果と統合する。PR 単位で結果連携を固定化すると、リリース判断の透明性を高めやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Xray | Jira統合テスト管理 | トレーサビリティとBDD連携に強い |
| Zephyr for Jira | Jira統合管理 | Jira標準運用に寄せやすい |
| TestRail | 独立テスト管理 | Jira非依存で運用しやすい |
| Allure Report | テスト結果可視化 | レポート特化 |

## ベストプラクティス

### 1. リンクモデルを標準化

- 要件、テスト、不具合のリンク規則を固定する。
- 例外ケースの扱いも定義する。

### 2. 自動結果取込を運用化

- CI 成果物を常に Xray へ反映する。
- 失敗時もインポート処理を止めない。

### 3. カバレッジ指標を定点監視

- 要件カバレッジ率をリリース判定に組み込む。
- 欠落要件を定期的に棚卸しする。

## 公式ドキュメント

- 公式サイト: https://www.getxray.app/
- Documentation: https://docs.getxray.app/
- Marketplace: https://marketplace.atlassian.com/apps/1211769/xray-test-management-for-jira
- API: https://docs.getxray.app/display/XRAYCLOUD/REST+API

## まとめ

- Jira統合で要件から不具合までの追跡を一元化しやすい。
- 手動/自動テストを統合し、品質状況を可視化しやすい。
- リンク規則とCI取込を標準化すると、運用を安定化しやすい。
