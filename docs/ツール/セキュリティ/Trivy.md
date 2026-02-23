# Trivy

## 概要

Trivyは、Aqua Security製のオールインワンセキュリティスキャナーです。コンテナイメージ、ファイルシステム、Gitリポジトリ、Kubernetesクラスタ、IaCファイルなど多様なターゲットを対象に、脆弱性（CVE）、設定ミス、シークレット漏洩、ライセンス違反を検出します。脆弱性データベースは6時間ごとに自動更新され、スキャン時にDB取得を行うため、常に最新の状態でチェックが可能です。

## 主な機能

### 1. スキャンターゲット

- **container image**: コンテナイメージの脆弱性・設定ミス・シークレット検出
- **filesystem**: ローカルファイルシステムの依存関係・脆弱性スキャン
- **repository**: Gitリポジトリのリモートスキャン
- **kubernetes**: Kubernetesクラスタのセキュリティ評価
- **rootfs**: ルートファイルシステムのスキャン
- **sbom**: 既存SBOMの脆弱性・ライセンス分析

### 2. スキャナー

- **vuln**: OSパッケージ・言語パッケージの既知脆弱性（CVE）検出
- **misconfig**: Dockerfile、Kubernetes YAML、Terraform等の設定ミス検出
- **secret**: ハードコードされたパスワード、APIキー、トークンの検出
- **license**: オープンソースライセンスの検出・分類

### 3. 対応言語・パッケージマネージャ

- **OS**: Alpine、Debian、Ubuntu、RHEL、Amazon Linux等
- **言語**: Java（Maven/Gradle）、Node.js（npm/yarn）、Python（pip/Poetry）、Go、Rust、Ruby、.NET（NuGet）
- **IaC**: Terraform、CloudFormation、Kubernetes、Docker、Helm

### 4. 出力形式

- **table**: ターミナル向けテーブル表示（デフォルト）
- **json**: 機械処理用JSON
- **sarif**: GitHub Code Scanning / IDE連携用SARIF
- **cyclonedx**: CycloneDX形式のSBOM
- **spdx-json**: SPDX形式のSBOM

## 利用方法

### インストール

```bash
# Homebrew
brew install trivy

# apt（Debian/Ubuntu）
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install trivy

# Docker
docker run --rm aquasec/trivy image python:3.12-slim

# バージョン確認
trivy --version
```

### コンテナイメージスキャン

```bash
# 基本的なイメージスキャン
trivy image python:3.12-slim

# 重要度フィルタ（HIGH以上のみ表示）
trivy image --severity HIGH,CRITICAL nginx:latest

# 全スキャナー有効化（脆弱性+設定ミス+シークレット）
trivy image --scanners vuln,misconfig,secret nginx:latest

# TARアーカイブからスキャン
trivy image --input myapp.tar

# SBOM生成（CycloneDX形式）
trivy image --format cyclonedx --output sbom.json myapp:latest
```

### ファイルシステムスキャン

```bash
# プロジェクトの依存関係スキャン
trivy fs .

# IaCファイルの設定ミスチェック
trivy fs --scanners misconfig ./terraform/

# シークレット検出
trivy fs --scanners secret .
```

### Kubernetesスキャン

```bash
# クラスタ全体のスキャン
trivy k8s --report summary cluster

# 特定ネームスペース
trivy k8s --include-namespaces production --report all
```

### trivy.yamlによる設定

```yaml
# trivy.yaml
severity:
  - HIGH
  - CRITICAL

scan:
  scanners:
    - vuln
    - misconfig
    - secret

vulnerability:
  ignore-unfixed: true

output:
  - format: table
  - format: json
    output: results.json
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/trivy.yml
name: Trivy Security Scan

on: [push, pull_request]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Trivy（OSS）** | 無料 | オープンソース、Apache License 2.0 |
| **Aqua Platform** | 有料 | エンタープライズ管理、ポリシー管理、ダッシュボード |

## メリット

1. **オールインワン**: 脆弱性、設定ミス、シークレット、ライセンスを1ツールで検出
2. **高速**: 初回DB取得後は秒単位でスキャン完了
3. **DB自動更新**: 6時間ごとに脆弱性データベースが自動更新
4. **幅広い対応**: コンテナ、ファイルシステム、K8s、IaC、SBOM等
5. **SARIF出力**: GitHub Code Scanningとの直接連携
6. **SBOM生成**: CycloneDX / SPDX形式でSBOM出力
7. **ゼロコンフィグ**: インストール後すぐに使える
8. **GitHub Action**: 公式アクションでCI/CD統合が容易

## デメリット

1. **偽陽性**: 一部の脆弱性で誤検出が発生する場合がある
2. **初回DB取得**: 初回スキャン時にDBダウンロードが必要（エアギャップ環境では事前準備要）
3. **修正なし脆弱性**: unfixed CVEが大量に報告される場合がある
4. **カスタムポリシー**: 高度なポリシー管理はAqua Platform（有料）が必要
5. **OS依存**: Windows対応は限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Grype** | Anchore製脆弱性スキャナー | Trivyよりシンプル、SBOM特化 |
| **Snyk** | 商用SCAツール | Trivyより修正提案が充実だが有料 |
| **OWASP Dependency-Check** | 依存関係脆弱性検査 | Trivyよりコンテナ対応弱い |
| **Clair** | コンテナ脆弱性スキャナー | コンテナ特化、Trivyの方が対応範囲広い |

## 公式リンク

- **公式サイト**: [https://trivy.dev/](https://trivy.dev/)
- **ドキュメント**: [https://trivy.dev/docs/](https://trivy.dev/docs/)
- **GitHub**: [https://github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)
- **GitHub Action**: [https://github.com/aquasecurity/trivy-action](https://github.com/aquasecurity/trivy-action)
- **Aqua Security**: [https://www.aquasec.com/products/trivy/](https://www.aquasec.com/products/trivy/)

## 関連ドキュメント

- [OWASP Dependency-Check](./OWASP_Dependency_Check.md)
- [ESLint](../開発ツール/ESLint.md)

---

**カテゴリ**: セキュリティ
**対象工程**: 実装・テスト・運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
