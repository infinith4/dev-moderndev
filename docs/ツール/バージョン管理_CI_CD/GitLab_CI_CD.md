# GitLab CI/CD

## 概要

GitLab CI/CD は GitLab に統合された継続的インテグレーション/デリバリー機能である。`.gitlab-ci.yml` でパイプラインを定義し、ビルド、テスト、デプロイを自動化できる。Runner 実行基盤により、クラウド環境とオンプレ環境の両方に対応する。

## 料金

| プラン | 内容 |
|------|------|
| Free | 基本的な CI/CD 機能を利用可能 |
| Premium | 高度な運用管理・スケール機能を拡張 |
| Ultimate | セキュリティ/コンプライアンス連携を強化 |
| Self-Managed | 自前 Runner で柔軟に運用可能 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| YAML定義 | パイプラインをコード管理できる |
| Stage/Job構成 | 処理順序を段階的に設計可能 |
| Runner実行 | Shared/Specific Runner を選択可能 |
| Environment管理 | 環境別デプロイと履歴追跡に対応 |
| Artifact管理 | 成果物をジョブ間で受け渡し可能 |
| セキュリティ連携 | スキャンテンプレートを利用可能 |

## 主な機能

### パイプライン機能

| 機能 | 説明 |
|------|------|
| `stages` / `jobs` | 実行単位を定義 |
| `rules` / `only` / `except` | 実行条件を制御 |
| `needs` | DAG 形式で並列化 |
| `parallel` | マトリックス実行に対応 |

### 配布/デプロイ機能

| 機能 | 説明 |
|------|------|
| `artifacts` | ビルド成果物を保存・共有 |
| `cache` | 依存取得を高速化 |
| `environment` | 環境ごとのデプロイ履歴を管理 |
| `when: manual` | 承認付きデプロイを実装 |

### 運用/セキュリティ機能

| 機能 | 説明 |
|------|------|
| Runner 管理 | 実行基盤の負荷分散 |
| Variables/Secrets | 認証情報と設定値を安全管理 |
| テンプレート利用 | 公式 CI テンプレートを活用 |
| Security Job | SAST/Dependency Scanning と連携 |

## インストールとセットアップ

公式URL:
- [GitLab CI/CD](https://about.gitlab.com/features/continuous-integration/)
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [`.gitlab-ci.yml` Reference](https://docs.gitlab.com/ee/ci/yaml/)

セットアップの要点:
1. プロジェクトルートに `.gitlab-ci.yml` を配置する。
2. 最小構成（build/test）から開始する。
3. 必要に応じて Shared Runner または Specific Runner を設定する。
4. Variables/Secrets と環境別デプロイルールを定義する。

## 基本的な使い方

1. `stages` と `jobs` を定義して commit する。
2. push をトリガーにパイプラインを実行する。
3. 失敗ジョブのログを確認し、修正して再実行する。
4. `main` へのマージ後にデプロイ job を実行する。
5. 必要に応じて `manual` ジョブで承認フローを入れる。

最小運用例:
- stage: `build` → `test`
- 条件: MR では test のみ、本番は manual deploy

## メリット

- GitLab と一体運用でき、設定の一貫性を保ちやすい。
- Runner と DAG 機能でスケールしやすい。
- 環境管理やセキュリティ連携を組み込みやすい。

## デメリット

- 高度な設定では YAML が複雑化しやすい。
- Runner 設計を誤ると実行待ちが増えやすい。
- 多機能ゆえに学習コストが高くなりやすい。

## CI/CD での使用

Merge Request では品質検証ジョブ（lint/test/scan）を実行し、`main` への反映後にデプロイを実施する構成が一般的である。`environment` と `manual` を組み合わせると、段階的リリースと承認統制を実装しやすい。

## 他ツールとの比較

| ツール | 強み | 特徴 |
|------|------|------|
| GitLab CI/CD | GitLab統合 | SCM と同一基盤で一元管理 |
| GitHub Actions | GitHub統合 | Marketplace 活用が容易 |
| Jenkins | 拡張性 | 自由度が高いが管理負荷が高い |
| CircleCI | SaaS CI | 導入が速くシンプル運用向き |

## ベストプラクティス

### 1. 段階的にパイプラインを育てる

- 最初は build/test に限定する。
- 安定後に deploy/scan を追加する。

### 2. 実行効率を可視化

- `cache` と `needs` を使って待ち時間を短縮する。
- 失敗しやすい job を分離して再実行性を高める。

### 3. 本番デプロイを統制

- production は `manual` と承認必須で運用する。
- ロールバック手順を job として用意する。

## 公式ドキュメント

- 公式サイト: https://about.gitlab.com/features/continuous-integration/
- Docs: https://docs.gitlab.com/ee/ci/
- YAML Reference: https://docs.gitlab.com/ee/ci/yaml/

## まとめ

1. ** 一貫管理 ** : GitLab CI/CD は `.gitlab-ci.yml` ベースで自動化を一貫管理しやすい。
2. ** 柔軟設計 ** : Runner と環境機能を活用すると、組織要件に合わせた運用を設計できる。
3. ** 安全配信 ** : 品質ゲートと承認フローを組み込むことで、安全なリリースを実現しやすい。
