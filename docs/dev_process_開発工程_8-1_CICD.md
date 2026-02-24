# 開発工程_8-1_CI/CD構築

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. ソース管理・トリガー構築](#2-ソース管理トリガー構築)
- [3. ビルド・テスト構築](#3-ビルドテスト構築)
- [4. セキュリティ検証構築](#4-セキュリティ検証構築)
- [5. アーティファクト管理構築](#5-アーティファクト管理構築)
- [6. デプロイパイプライン構築](#6-デプロイパイプライン構築)
- [7. 監視・運用構築](#7-監視運用構築)
- [8. 参考資料](#8-参考資料)

## 1. 概要

CI/CD構築のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- パイプライン定義ファイルの実装
- 自動ビルド/テスト/デプロイの実装
- 失敗時通知、再実行、ロールバック手順の実装
- 変更履歴と実行ログの管理

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [CI/CD on GitHub Actions](https://docs.github.com/actions/guides/about-continuous-integration) | CI/CD構築の基本フロー確認 |
| [GitLab CI/CD documentation](https://docs.gitlab.com/ee/ci/) | GitLabでのパイプライン構築手順 |

---

## 2. ソース管理・トリガー構築
**成果物**
- ブランチ保護設定
- パイプライントリガー設定（push/PR/tag/schedule）
- 実行条件定義（対象ブランチ、パスフィルタ）

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [GitHub Actions](https://github.com/features/actions) | push/PR/tagをトリガーとしたCI実行 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitHub_Actions.md) |
| [GitLab CI/CD](https://about.gitlab.com/solutions/continuous-integration/) | GitLabリポジトリ起点のパイプライン実行 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitLab_CI_CD.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Events that trigger workflows](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows) | GitHub Actionsのトリガー設定 |
| [Pipeline configuration reference](https://docs.gitlab.com/ee/ci/yaml/) | `.gitlab-ci.yml` の定義方法 |

---

## 3. ビルド・テスト構築
**成果物**
- ビルドジョブ定義
- テストジョブ定義（単体/結合）
- テスト結果レポート

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [GitHub Actions](https://github.com/features/actions) | ビルド/テストワークフロー実装 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitHub_Actions.md) |
| [GitLab CI/CD](https://about.gitlab.com/solutions/continuous-integration/) | ステージ分割でのビルド/テスト実装 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitLab_CI_CD.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) | ワークフロー定義の記述方法 |
| [GitLab CI/CD Pipeline Efficiency](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency/) | 並列化/キャッシュ最適化 |

---

## 4. セキュリティ検証構築
**成果物**
- SAST/依存関係/IaCスキャン設定
- シークレット検出設定
- セキュリティゲート定義（失敗条件）

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Trivy](https://trivy.dev/) | コンテナ/依存関係/IaCの脆弱性検出 | [詳細](./ツール/セキュリティ/Trivy.md) |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | シークレット漏えい検出 |  |
| [Checkov](https://www.checkov.io/) | IaCセキュリティポリシー検証 | [詳細](./ツール/セキュリティ/Checkov.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [GitHub Actions Security hardening](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions) | パイプラインのセキュリティ強化 |
| [OWASP CI/CD Security Guidance](https://owasp.org/www-project-top-10-ci-cd-security-risks/) | CI/CDセキュリティ観点の確認 |
| [Trivy Documentation](https://trivy.dev/latest/docs/) | CI組み込み時の設定方法 |

---

## 5. アーティファクト管理構築
**成果物**
- アーティファクト保存ルール
- バージョニングルール
- 保持期間/削除ポリシー

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [GitHub Packages](https://github.com/features/packages) | コンテナ/パッケージ保存 | 無料枠あり |  |
| [GitLab Package Registry](https://docs.gitlab.com/ee/user/packages/package_registry/) | GitLab内アーティファクト管理 | 無料枠あり |  |
| [JFrog Artifactory OSS](https://jfrog.com/open-source/) | 汎用アーティファクト管理 | 無料 | [詳細](./ツール/バージョン管理_CI_CD/JFrog_Artifactory_OSS.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Store and share data with workflow artifacts](https://docs.github.com/actions/using-workflows/storing-workflow-data-as-artifacts) | GitHub Actionsアーティファクト管理 |
| [Job artifacts](https://docs.gitlab.com/ee/ci/jobs/job_artifacts.html) | GitLabジョブ成果物の管理 |
| [Artifactory Documentation](https://jfrog.com/help/r/jfrog-artifactory-documentation/welcome-to-jfrog-artifactory) | リポジトリ管理・保持設定 |

---

## 6. デプロイパイプライン構築
**成果物**
- 環境別デプロイ定義（dev/stg/prod）
- 承認フロー設定
- ロールバック手順

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [GitHub Actions](https://github.com/features/actions) | 環境別デプロイジョブ実装 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitHub_Actions.md) |
| [GitLab CI/CD](https://about.gitlab.com/solutions/continuous-integration/) | 段階的デプロイと承認フロー実装 | 無料枠あり | [詳細](./ツール/バージョン管理_CI_CD/GitLab_CI_CD.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Deploying to environments](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment) | GitHub環境別デプロイ設定 |
| [Environments and deployments](https://docs.gitlab.com/ee/ci/environments/) | GitLab環境管理とデプロイ設定 |

---

## 7. 監視・運用構築
**成果物**
- パイプライン監視ダッシュボード
- 失敗通知設定
- 運用Runbook（再実行/復旧）

| ツール名 | 用途 | 料金 | 詳細 |
|---------|------|------|------|
| [Prometheus](https://prometheus.io/) | CI/CD実行メトリクス収集 | 無料 | [詳細](./ツール/監視_ロギング/Prometheus.md) |
| [Grafana](https://grafana.com/) | 実行状況の可視化/アラート設定 | 無料枠あり | [詳細](./ツール/監視_ロギング/Grafana.md) |
| [Slack](https://slack.com/) | 失敗通知、承認依頼通知 | 無料枠あり | [詳細](./ツール/コラボレーションツール/Slack.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Monitor workflows](https://docs.github.com/actions/monitoring-and-troubleshooting-workflows/monitoring-workflows) | GitHub Actionsの実行監視 |
| [GitLab CI/CD analytics](https://docs.gitlab.com/ee/user/analytics/ci_cd_analytics.html) | GitLabパイプライン可視化 |
| [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) | 運用手順と障害対応の整備 |

---

## 8. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
