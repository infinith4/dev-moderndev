# Allure Report

## 概要

Allure Report は、テスト結果を可視化するレポーティングツールである。JUnit、pytest、Cucumber などの結果を集約し、HTML レポートとして共有できる。テスト失敗の傾向や履歴を追跡し、品質レビューを効率化しやすい。

## 料金

| プラン | 内容 |
|------|------|
| Allure Report | 無料（オープンソース） |
| Allure TestOps | 有料（テスト管理機能を拡張） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| レポート可視化 | テスト結果をダッシュボード表示 |
| 多FW対応 | JUnit、TestNG、pytest、Cucumber 等と連携 |
| 履歴比較 | 過去実行とのトレンド分析が可能 |
| 添付ファイル | スクリーンショット、ログ、動画を表示可能 |
| CI連携 | Jenkins、GitHub Actions、GitLab CI と連携可能 |
| BDD表示 | Epic/Feature/Story で結果整理が可能 |

## 主な機能

### レポート表示機能

| 機能 | 説明 |
|------|------|
| Overview | 実行結果の要約を表示 |
| Suites | テストスイート単位で結果を確認 |
| Timeline | 実行時間と並列状況を可視化 |
| Categories | 失敗分類をルール化して表示 |

### 分析機能

| 機能 | 説明 |
|------|------|
| Trend | 成功率や失敗率の推移を追跡 |
| Duration | 実行時間の変化を比較 |
| Retry | リトライ状況を記録 |
| History | テストケース単位の履歴を保持 |

### 連携機能

| 機能 | 説明 |
|------|------|
| Adapter連携 | テストFW別アダプタで結果収集 |
| CLI生成 | `allure generate/serve` でレポート作成 |
| CIパイプライン | 自動実行後にレポート配布 |
| 静的公開 | GitHub Pages 等で共有可能 |

## インストールとセットアップ

公式URL:
- [Allure 公式サイト](https://allurereport.org/)
- [Documentation](https://allurereport.org/docs/)
- [GitHub](https://github.com/allure-framework)

セットアップの要点:
1. CLI（brew/npm等）を導入する。
2. テストFW向けアダプタを追加する。
3. テスト実行時に `allure-results` を出力する。
4. `allure generate` でレポートを生成して共有する。

## 基本的な使い方

1. テスト実行時に Allure 用結果を出力する。
2. `allure serve allure-results` でローカル確認する。
3. `allure generate` で静的レポートを生成する。
4. 失敗ケースにログ・スクリーンショットを添付する。
5. CI で毎回生成し、履歴比較を実施する。

最小実行例:
- 実行: `pytest --alluredir=allure-results`
- 表示: `allure serve allure-results`
- 生成: `allure generate allure-results -o allure-report --clean`

## メリット

- テスト結果の可視化で障害分析を進めやすい。
- 多様なテストFWを同一形式で扱いやすい。
- CI 連携により継続的な品質レポートを作りやすい。

## デメリット

- 履歴管理には成果物保存設計が必要。
- 高度なチーム管理は TestOps（有料）前提になりやすい。
- 初期にアダプタ設定と運用ルールの整備が必要。

## CI/CD での使用

CI ではテスト実行後に `allure-results` をアーティファクト保存し、レポートを静的公開する運用が一般的である。失敗時もレポート生成を継続する設定にすると、原因調査を行いやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Allure Report | テスト結果可視化 | 多FW対応と履歴分析に強い |
| ExtentReports | Java中心レポート | 実装は簡易だが分析機能は限定的 |
| ReportPortal | テスト分析基盤 | 高機能だが運用構築コストが高い |
| TestRail | テスト管理全般 | ケース管理中心でレポート特化ではない |

## ベストプラクティス

### 1. 結果添付を標準化

- 失敗時にスクリーンショットとログを必ず添付する。
- 重要テストにはステップ情報を明示する。

### 2. カテゴリルールを整備

- Product Defect / Test Defect の分類基準を決める。
- 誤分類を定期的に見直す。

### 3. 履歴を継続保存

- 直近N回の結果を保存し推移を監視する。
- リリース判定に成功率トレンドを利用する。

## 公式ドキュメント

- 公式サイト: https://allurereport.org/
- Documentation: https://allurereport.org/docs/
- GitHub: https://github.com/allure-framework
- pytest連携: https://allurereport.org/docs/pytest/

## まとめ

1. ** 可視化 ** : テスト結果を可視化し、失敗分析と共有を進めやすい。
2. ** 統一管理 ** : 多様なテストフレームワークを統一形式で管理しやすい。
3. ** 継続改善 ** : CIと履歴保存を組み合わせると、品質改善を継続しやすい。
