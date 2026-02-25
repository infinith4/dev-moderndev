# GitHub Actions

## 概要

GitHub Actions は GitHub 上で動作する CI/CD 自動化基盤である。ワークフローを YAML で定義し、`push`、`pull_request`、手動実行などのイベントを起点にビルド、テスト、デプロイを実行できる。

## 料金

| プラン | 内容 |
|------|------|
| Public Repository | 無料で利用可能 |
| Private Repository | プランに応じた実行時間/ストレージ枠 |
| Self-hosted Runner | 自前実行基盤で柔軟に運用可能 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| GitHub統合 | リポジトリ設定だけで開始しやすい |
| YAML定義 | パイプラインをコードとして管理可能 |
| Marketplace | 再利用可能な Action が豊富 |
| マトリックス実行 | OS/言語バージョンの並列テスト対応 |
| シークレット管理 | 認証情報を安全に扱える |
| Environment保護 | 本番デプロイに承認ゲートを設定可能 |

## 主な機能

### ワークフロー機能

| 機能 | 説明 |
|------|------|
| Event Trigger | `push`、`pull_request`、`schedule` など |
| Job/Step 定義 | 依存関係を持つ処理を段階実行 |
| Matrix Strategy | 複数環境の並列検証 |
| Reusable Workflow | 共通処理を再利用して重複を削減 |

### 実行基盤機能

| 機能 | 説明 |
|------|------|
| GitHub-hosted Runner | すぐ使える実行環境 |
| Self-hosted Runner | 社内ネットワークや専用環境で実行 |
| Caching | 依存関係キャッシュで時間短縮 |
| Artifacts | ビルド成果物を保存・共有 |

### 運用管理機能

| 機能 | 説明 |
|------|------|
| Secrets / Variables | 環境別設定を安全に管理 |
| Environment Rules | 承認者やデプロイ条件を制御 |
| Workflow Logs | 失敗原因の解析を支援 |
| Status Checks | PR マージの品質ゲートに利用 |

## インストールとセットアップ

公式URL:
- [GitHub Actions](https://github.com/features/actions)
- [GitHub Actions Docs](https://docs.github.com/ja/actions)
- [Workflow Syntax](https://docs.github.com/ja/actions/using-workflows/workflow-syntax-for-github-actions)

セットアップの要点:
1. リポジトリに `.github/workflows/*.yml` を作成する。
2. 最初は build/test の最小パイプラインで開始する。
3. Secrets と Environment を設定し、認証情報を分離する。
4. 本番デプロイは承認ゲートを有効化する。

## 基本的な使い方

1. ワークフローファイルを作成し、トリガーを設定する。
2. `actions/checkout` と言語セットアップを定義する。
3. 依存インストール、テスト、ビルドを step として記述する。
4. PR 上で結果を確認し、失敗時ログを調査する。
5. 必要に応じてデプロイ job を追加する。

最小運用例:
- ファイル: `.github/workflows/ci.yml`
- トリガー: `pull_request`
- 実行: lint + test

## メリット

- GitHub 上で完結し、導入と運用がシンプル。
- Workflow as Code で変更履歴を追跡しやすい。
- Marketplace 活用で実装コストを下げやすい。

## デメリット

- 複雑なパイプラインは YAML が肥大化しやすい。
- GitHub 基盤への依存度が高くなる。
- Private リポジトリでは利用枠管理が必要。

## CI/CD での使用

PR 検証（lint/test）を必須化し、`main` マージ後にデプロイを実行する2段階運用が一般的である。さらに Environment 承認とロールバック手順を整備すると、本番運用の安定性が高まる。

## 他ツールとの比較

| ツール | 強み | 特徴 |
|------|------|------|
| GitHub Actions | GitHub統合 | PR と CI/CD を一体で運用しやすい |
| GitLab CI/CD | DevOps統合 | GitLab 環境で強力な一元管理 |
| Jenkins | 拡張性 | 自由度が高いが運用負荷が高め |
| CircleCI | SaaS CI | シンプル導入と高速実行に強み |

## ベストプラクティス

### 1. ワークフローを分割

- `ci.yml` と `deploy.yml` を分離して責務を明確化する。
- 共通処理は reusable workflow 化する。

### 2. 実行時間を最適化

- キャッシュと並列実行を活用する。
- 不要なトリガーを抑制してコストを管理する。

### 3. セキュアな運用を徹底

- Secrets を平文で扱わない。
- 本番 Environment に承認フローを設定する。

## 公式ドキュメント

- 公式サイト: https://github.com/features/actions
- Docs: https://docs.github.com/ja/actions
- Workflow Syntax: https://docs.github.com/ja/actions/using-workflows/workflow-syntax-for-github-actions

## まとめ

1. ** 導入容易 ** : GitHub Actions は GitHub と密に統合された CI/CD 基盤で導入しやすい。
2. ** 実装効率 ** : YAML 定義と Marketplace を活用すると、実装効率を高めやすい。
3. ** 安全運用 ** : 承認ゲートと Secrets 管理を組み合わせることで、安全なデプロイ運用を実現しやすい。
