# Trivy

## 概要

Trivy は、コンテナイメージ、依存ライブラリ、IaC、シークレットを横断的に検査できるセキュリティスキャナーである。1つのCLIで複数対象を扱えるため、開発からデプロイ前までのセキュリティチェックを統合しやすい。

## 料金

| プラン | 内容 |
|------|------|
| Trivy OSS | 無料（Apache License 2.0） |
| Aqua Platform | 有料（ポリシー管理や統合ダッシュボードを拡張） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| オールインワン検査 | 脆弱性、設定ミス、シークレット、ライセンスを検査 |
| 対象の広さ | イメージ、FS、Repo、Kubernetes、SBOM を検査可能 |
| 高速実行 | 軽量CLIでローカル/CI実行しやすい |
| CI/CD 親和性 | SARIF 連携でセキュリティゲートを作りやすい |
| SBOM 対応 | CycloneDX / SPDX を出力可能 |
| シンプル導入 | 初期設定なしで開始しやすい |

## 主な機能

### スキャン機能

| 機能 | 説明 |
|------|------|
| イメージスキャン | OS/言語依存の脆弱性を検出 |
| ファイルシステムスキャン | ローカルコードと依存を検査 |
| IaC スキャン | Terraform/Kubernetes 等の設定ミス検出 |
| Kubernetes スキャン | クラスタ設定とワークロードを確認 |

### 検査カテゴリ機能

| 機能 | 説明 |
|------|------|
| `vuln` | 既知脆弱性（CVE）の検出 |
| `misconfig` | 設定不備の検出 |
| `secret` | シークレット漏えい検出 |
| `license` | ライセンス分類と監査支援 |

### 出力・連携機能

| 機能 | 説明 |
|------|------|
| Table/JSON | ローカル確認と機械処理に対応 |
| SARIF | GitHub Code Scanning 連携 |
| SBOM 出力 | CycloneDX/SPDX 形式で出力 |
| 重大度フィルタ | HIGH/CRITICAL などで絞り込み |

## インストールとセットアップ

公式URL:
- [Trivy 公式サイト](https://trivy.dev/)
- [Trivy ドキュメント](https://trivy.dev/docs/)
- [GitHub](https://github.com/aquasecurity/trivy)
- [GitHub Action](https://github.com/aquasecurity/trivy-action)

セットアップの要点:
1. CLI（brew/apt）または Docker イメージで導入する。
2. 対象（image/fs/k8s）とスキャナー種別を決める。
3. 重大度閾値と出力形式（SARIF/JSON）を統一する。
4. CI でスキャンを実行し、結果をアーティファクト化する。

## 基本的な使い方

1. `trivy image` でコンテナイメージを検査する。
2. `trivy fs` でリポジトリやIaC設定を検査する。
3. `--severity` で重要度フィルタを設定する。
4. `--format sarif` でセキュリティ基盤へ連携する。
5. 修正後に再スキャンして結果を比較する。

最小実行例:
- イメージ: `trivy image --severity HIGH,CRITICAL nginx:latest`
- FS: `trivy fs --scanners vuln,misconfig,secret .`
- SARIF: `trivy image --format sarif -o trivy.sarif myapp:latest`

## メリット

- 複数対象を1ツールで検査でき、運用を統一しやすい。
- 実行が速く、CIに組み込みやすい。
- SARIF/SBOM対応で他システム連携しやすい。

## デメリット

- 誤検知や修正不能CVEへの運用ルールが必要。
- 初回DB取得やネットワーク制約の対処が必要な場合がある。
- 高度な組織統制は商用機能前提になる。

## Docker での使用

Docker イメージ（`aquasec/trivy`）を使うと、ローカルとCIで同じ実行環境を保ちやすい。イメージタグを固定し、DB更新タイミングを制御すると再現性を確保しやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Trivy | イメージ/依存/IaC 検査 | 対象が広く統合運用しやすい |
| OWASP Dependency-Check | 依存脆弱性 | 依存検査に特化 |
| Grype | イメージ/SBOM | 軽量な脆弱性検査に強い |
| Snyk | SCA + 修正提案 | 修正支援機能が強い（有料機能あり） |

## ベストプラクティス

### 1. 重大度基準を統一

- HIGH/CRITICAL をゲート条件として定義する。
- 環境ごとに fail/soft-fail を使い分ける。

### 2. スキャン対象を役割分担

- PRでは `fs`、ビルド後は `image` を実行する。
- IaC とシークレット検査を同時に回す。

### 3. 結果管理を継続

- SARIF/JSON を保存し、推移を追跡する。
- 例外対応はチケット化して期限管理する。

## 公式ドキュメント

- 公式サイト: https://trivy.dev/
- ドキュメント: https://trivy.dev/docs/
- GitHub: https://github.com/aquasecurity/trivy
- GitHub Action: https://github.com/aquasecurity/trivy-action

## まとめ

- 脆弱性、設定不備、シークレットを一体で検査しやすい。
- CI/CD 連携により、継続的なセキュリティゲートを作りやすい。
- 重大度基準と例外運用を決めることで、実務運用を安定化しやすい。
