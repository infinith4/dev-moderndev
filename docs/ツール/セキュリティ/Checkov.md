# Checkov

## 概要

Checkov は、Infrastructure as Code（IaC）を対象にした静的セキュリティスキャンツールである。Terraform、CloudFormation、Kubernetes、Dockerfile などを解析し、デプロイ前に設定不備やコンプライアンス違反を検出できる。Shift Left Security を実践する IaC セキュリティゲートとして利用しやすい。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（Apache License 2.0） |
| 商用利用 | ライセンス上可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| IaC 多言語対応 | Terraform、CloudFormation、Kubernetes、Dockerfile などを解析 |
| ポリシーベース検査 | ベストプラクティスや規制要件をルール化して検出 |
| CI/CD 統合 | GitHub Actions、GitLab CI、Jenkins へ組み込みやすい |
| カスタムポリシー | 組織独自ルールを追加可能 |
| レポート出力 | CLI、JSON、SARIF、JUnit 形式を出力可能 |
| ローカル実行 | 開発端末から即時スキャンできる |

## 主な機能

### IaC スキャン機能

| 機能 | 説明 |
|------|------|
| ディレクトリスキャン | プロジェクト全体をまとめて解析 |
| ファイルスキャン | 対象ファイルを指定して解析 |
| フレームワーク指定 | Terraform/Kubernetes 等に限定して実行 |
| 複合解析 | 複数 IaC フレームワークを同時に検査 |

### フィルタリング・レポート機能

| 機能 | 説明 |
|------|------|
| `--skip-check` | 特定チェックを除外 |
| 重要度フィルタ | 重大度に応じた結果抽出 |
| 複数出力形式 | JSON、SARIF、JUnit などで出力 |
| コンパクト表示 | 合格項目を省略し、要対応に集中 |

### カスタムポリシー機能

| 機能 | 説明 |
|------|------|
| カスタムチェック追加 | 組織基準に合わせたルール実装 |
| 外部チェック読込 | ポリシーを別ディレクトリで管理 |
| 設定ファイル管理 | `.checkov.yaml` で実行条件を統一 |
| 例外管理 | 正当な例外を明示的に運用 |

## インストールとセットアップ

公式URL:
- [Checkov 公式サイト](https://www.checkov.io/)
- [Checkov Documentation](https://www.checkov.io/1.Welcome/Quick%20Start.html)
- [Checkov GitHub Repository](https://github.com/bridgecrewio/checkov)
- [Policy Index](https://www.checkov.io/5.Policy%20Index/all.html)

セットアップの要点:
1. `pip` または Docker で Checkov を導入する。
2. スキャン対象フレームワークと対象ディレクトリを決める。
3. `.checkov.yaml` で除外ルールと出力形式を統一する。
4. CI で自動実行し、重大項目をマージ条件に組み込む。

## 基本的な使い方

1. `checkov -d .` で IaC 全体をスキャンする。
2. 必要に応じて `--framework` で対象を限定する。
3. `--skip-check` と設定ファイルで例外を管理する。
4. `-o sarif` で結果をセキュリティダッシュボードへ連携する。
5. 検出結果を修正し、再スキャンで解消を確認する。

最小実行例:
- 全体スキャン: `checkov -d .`
- Terraform限定: `checkov --framework terraform -d terraform/`
- SARIF出力: `checkov -d . -o sarif --output-file-path results.sarif`

## メリット

- デプロイ前に IaC のリスクを早期検出しやすい。
- 複数 IaC を同一ツールで検査でき、運用を統一しやすい。
- CI 連携でセキュリティチェックを自動化しやすい。

## デメリット

- プロジェクト規模が大きいとスキャン時間が長くなりやすい。
- 誤検知対策として例外ルール整備が必要になる。
- カスタムポリシー運用にはルール保守コストがかかる。

## Docker での使用

Docker イメージ（`bridgecrew/checkov`）を利用すると、ローカル環境差分を抑えて実行しやすい。CI でも同一イメージを使うと再現性を保ちやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Checkov | IaC セキュリティ検査 | 対応IaCが広く、CI統合しやすい |
| tfsec | Terraform 検査 | Terraform 特化で導入が軽量 |
| Terrascan | IaC 検査 | Rego ベースでポリシー管理しやすい |
| Trivy | 画像/依存/IaC 検査 | コンテナ脆弱性と併用しやすい |

## ベストプラクティス

### 1. 設定ファイルを標準化

- `.checkov.yaml` をリポジトリ管理し、実行条件を固定する。
- 環境差分（dev/prod）の基準を明確に分ける。

### 2. 例外管理を明示化

- `skip-check` は理由付きで記録する。
- 期限付きで見直す運用を設ける。

### 3. CI ゲートを段階導入

- まず可視化（soft fail）で現状把握する。
- 重大度基準を決めて hard fail へ移行する。

## 公式ドキュメント

- 公式サイト: https://www.checkov.io/
- Documentation: https://www.checkov.io/1.Welcome/Quick%20Start.html
- Policy Index: https://www.checkov.io/5.Policy%20Index/all.html
- GitHub: https://github.com/bridgecrewio/checkov

## まとめ

1. **早期発見** : IaC をデプロイ前に検査し、設定不備を早期に発見しやすい。
2. **統一管理** : 複数フレームワークを一元的に扱え、セキュリティ運用を統一しやすい。
3. **継続防御** : CI/CD に組み込むことで、継続的なセキュリティゲートを実装しやすい。
