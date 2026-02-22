# 開発工程_11_導入（アプリケーション・インフラ）

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. データ移行導入](#2-データ移行導入)
- [3. デプロイ・リリース導入](#3-デプロイリリース導入)
- [4. 受入・本番切替](#4-受入本番切替)
- [5. 監視・ログ導入](#5-監視ログ導入)
- [6. 運用引き継ぎ](#6-運用引き継ぎ)
- [7. インシデント・変更管理立ち上げ](#7-インシデント変更管理立ち上げ)
- [8. 参考資料](#8-参考資料)

## 1. 概要

導入（アプリケーション・インフラ）のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- 本番環境への導入計画、移行計画の実施
- リリース手順に沿った展開、切戻し準備
- 監視/運用設定の有効化と確認
- 導入結果の記録、運用チームへの引き継ぎ

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [ITIL 4 の概要](https://www.axelos.com/certifications/itil-service-management) | 導入後運用プロセス（インシデント/変更）の共通化 |
| [NIST SP 800-34 Rev.1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) | バックアップ/復旧、切戻し計画の基準 |
| [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) | 本番運用開始時のRunbook整備 |

---

## 2. データ移行導入
**成果物**
- データ移行計画書
- 移行手順書
- 移行結果レポート

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Flyway](https://flywaydb.org/) | スキーマ移行とバージョン管理 | 無料 |
| [Liquibase](https://www.liquibase.com/) | DB変更管理と移行適用 | 無料枠あり |
| [Apache NiFi](https://nifi.apache.org/) | データフロー設計、変換、移送 | 無料 |
| [dbt Core](https://www.getdbt.com/product/dbt-core) | データ変換、検証、整合性確認 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Flyway Documentation](https://documentation.red-gate.com/flyway) | マイグレーション運用手順 |
| [Liquibase Documentation](https://docs.liquibase.com/) | 変更セット設計、ロールバック |
| [AWS DMS Documentation](https://docs.aws.amazon.com/dms/) | DB移行方式と検証観点 |

---

## 3. デプロイ・リリース導入
**成果物**
- リリース計画書
- デプロイ手順書
- 切戻し手順書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [GitHub Actions](https://github.com/features/actions) | デプロイパイプライン実行 | 無料枠あり |
| [GitLab CI/CD](https://about.gitlab.com/solutions/continuous-integration/) | 環境別デプロイ実行と承認 | 無料枠あり |
| [Docker](https://www.docker.com/) | コンテナイメージ作成/配布 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Deploying to environments (GitHub)](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment) | 環境別デプロイ設定 |
| [GitLab Environments](https://docs.gitlab.com/ee/ci/environments/) | 段階的リリースの設定 |

---

## 4. 受入・本番切替
**成果物**
- 受入テスト結果報告書
- 本番切替チェックリスト
- 切替判定記録

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Cucumber](https://cucumber.io/) | 受入観点のシナリオ定義、実行 | 無料 |
| [Playwright](https://playwright.dev/) | UI受入テスト自動化 | 無料 |
| [Selenium](https://www.selenium.dev/) | 回帰を含むブラウザ受入検証 | 無料 |
| [Robot Framework](https://robotframework.org/) | キーワード駆動での受入テスト実装 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Cucumber Documentation](https://cucumber.io/docs/) | Gherkinによる受入基準定義 |
| [Playwright Docs](https://playwright.dev/docs/intro) | 受入/E2Eテスト実装 |
| [Selenium Documentation](https://www.selenium.dev/documentation/) | ブラウザ自動化の運用 |

---

## 5. 監視・ログ導入
**成果物**
- 監視ダッシュボード
- アラート設定
- ログ収集設定

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Prometheus](https://prometheus.io/) | メトリクス監視設定 | 無料 |
| [Grafana](https://grafana.com/) | ダッシュボード/通知設定 | 無料枠あり |
| [Loki](https://grafana.com/oss/loki/) | ログ収集/検索基盤の導入 | 無料 |
| [OpenTelemetry](https://opentelemetry.io/) | トレース/メトリクス標準化 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Prometheus Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/) | 監視基盤初期構築 |
| [Grafana Documentation](https://grafana.com/docs/grafana/latest/) | ダッシュボード・通知構築 |
| [OpenTelemetry Documentation](https://opentelemetry.io/docs/) | 計測データの標準化 |

---

## 6. 運用引き継ぎ
**成果物**
- 運用Runbook
- 運用手順書
- 権限移管記録

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [GitHub Wiki](https://docs.github.com/communities/documenting-your-project-with-wikis) | 運用ドキュメント管理 | 無料 |
| [MkDocs](https://www.mkdocs.org/) | 運用ドキュメントの静的サイト化 | 無料 |
| [Docusaurus](https://docusaurus.io/) | 運用/手順ドキュメントサイト構築 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Google SRE - Production Readiness Review](https://sre.google/sre-book/production-readiness-review/) | 運用引き継ぎ時の確認観点 |
| [Runbook Best Practices](https://www.pagerduty.com/resources/learn/what-is-a-runbook/) | Runbook構成の標準化 |
| [GitHub Docs - Wikis](https://docs.github.com/communities/documenting-your-project-with-wikis/about-wikis) | Wiki運用手順 |

---

## 7. インシデント・変更管理立ち上げ
**成果物**
- インシデント対応フロー
- 変更管理フロー
- エスカレーションルール

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Zammad](https://zammad.com/) | サービスデスク、チケット管理 | 無料枠あり |
| [OpenProject](https://www.openproject.org/) | 変更管理、課題管理、承認管理 | 無料枠あり |
| [Grafana OnCall](https://grafana.com/products/cloud/oncall/) | 当番、通知、エスカレーション管理 | 無料枠あり |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [NIST SP 800-61 Rev.2](https://csrc.nist.gov/pubs/sp/800/61/r2/final) | インシデント対応プロセス |
| [Atlassian Incident Management Guide](https://www.atlassian.com/incident-management) | インシデント管理の実装観点 |
| [OpenProject Documentation](https://www.openproject.org/docs/) | 変更管理ワークフロー設定 |

---

## 8. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC/IEEE 12207:2017 / JIS X 0160:2012
- [開発工程_8_インフラ構築](./dev_process_開発工程_8_インフラ構築.md)
- [開発工程_8-1_CI/CD構築](./dev_process_開発工程_8-1_CICD.md)
- [開発工程_9_テスト_アプリケーション](./dev_process_開発工程_9_テスト_アプリケーション.md)
- [開発工程_10_テスト_インフラ](./dev_process_開発工程_10_テスト_インフラ.md)
