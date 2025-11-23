# DevSecOps実践ガイド

## 概要

本ガイドは、開発プロセスにセキュリティを統合する「DevSecOps」の実践方法を体系的にまとめたものです。従来の「開発後のセキュリティチェック」から、「開発プロセス全体にセキュリティを組み込む」アプローチへの転換を支援します。

### 対象読者
- セキュリティエンジニア
- DevOpsエンジニア
- 開発チームリーダー
- アプリケーション開発者
- システムアーキテクト
- CISO（最高情報セキュリティ責任者）

---

## 目次

1. [DevSecOpsとは](#devsecopsとは)
2. [DevSecOpsの必要性](#devsecopsの必要性)
3. [Shift Left（シフトレフト）](#shift-leftシフトレフト)
4. [DevSecOpsの原則](#devsecopsの原則)
5. [CI/CDパイプラインへのセキュリティ統合](#cicdパイプラインへのセキュリティ統合)
6. [セキュリティテスト手法](#セキュリティテスト手法)
7. [コンテナセキュリティ](#コンテナセキュリティ)
8. [シークレット管理](#シークレット管理)
9. [脆弱性管理](#脆弱性管理)
10. [セキュリティ監視とインシデント対応](#セキュリティ監視とインシデント対応)
11. [コンプライアンスと監査](#コンプライアンスと監査)
12. [組織とプロセス](#組織とプロセス)
13. [推奨ツールとサービス](#推奨ツールとサービス)
14. [ベストプラクティス](#ベストプラクティス)
15. [成熟度モデル](#成熟度モデル)
16. [参考資料](#参考資料)

---

## DevSecOpsとは

### 定義

**DevSecOps**（Development, Security, Operations）は、開発（Dev）、セキュリティ（Sec）、運用（Ops）を統合し、**ソフトウェア開発ライフサイクル全体にセキュリティを組み込む**文化、プラクティス、ツールの集合です。

### DevOpsとの違い

```
[従来のDevOps]
開発 → テスト → デプロイ → 運用
                    ↓
            セキュリティチェック（後付け）

[DevSecOps]
開発（セキュリティ統合） → テスト（セキュリティテスト）
  → デプロイ（セキュアな設定） → 運用（継続的監視）
```

### 核心的な考え方

- **セキュリティは後付けではない**: 最初から組み込む
- **全員の責任**: 開発者もセキュリティを意識
- **自動化**: セキュリティチェックを自動化
- **継続的改善**: 継続的なセキュリティ向上

---

## DevSecOpsの必要性

### 1. セキュリティ脅威の増大

**統計**:
- サイバー攻撃は年々増加・高度化
- データ漏洩の平均コスト: 約4億円以上（IBM調査）
- セキュリティインシデントの70%以上がアプリケーション層

### 2. 開発スピードとセキュリティの両立

**課題**:
- アジャイル開発・DevOpsで開発サイクルが高速化
- 従来の「開発後のセキュリティ審査」では間に合わない
- リリース直前の脆弱性発見は多大なコスト

**解決策**:
- 開発初期からセキュリティを組み込む
- 自動化による高速かつ継続的なチェック

### 3. コンプライアンス要求

**規制**:
- GDPR（EU一般データ保護規則）
- 個人情報保護法
- PCI DSS（クレジットカード業界）
- SOC 2、ISO 27001

### 4. クラウド・マイクロサービスの普及

**新たな課題**:
- 複雑なアーキテクチャ
- 動的なインフラ
- API経由の攻撃
- コンテナ・Kubernetesのセキュリティ

### 5. サプライチェーン攻撃

**リスク**:
- オープンソースライブラリの脆弱性
- 依存関係の脆弱性（Log4Shell等）
- ビルドパイプラインへの侵入

---

## Shift Left（シフトレフト）

### 概念

**Shift Left**（左にシフト）は、開発プロセスの**より早い段階（左側）でセキュリティ対策を実施**する考え方です。

```
時間軸: 左 ────────────────────────→ 右

[従来]
要件 → 設計 → 実装 → テスト → デプロイ → 運用 → セキュリティ監査
                                              ↑
                                         ここで初めて

[Shift Left]
要件 → 設計 → 実装 → テスト → デプロイ → 運用
 ↓      ↓      ↓      ↓       ↓      ↓
セキュリティ要件定義、脅威モデリング、SAST、DAST、セキュアデプロイ、監視
```

### メリット

#### 1. 早期発見・早期修正
- バグ修正コストは後工程ほど高い
- 要件段階: 1x
- 設計段階: 6x
- 実装段階: 15x
- テスト段階: 60-100x
- 本番環境: 100x以上

#### 2. セキュリティ品質の向上
- 設計段階での脅威モデリング
- コーディング段階でのセキュアコーディング

#### 3. 開発速度の維持
- 手戻りの削減
- リリース直前のブロッカー回避

### 実践方法

#### 要件定義フェーズ
- セキュリティ要件の定義
- プライバシー要件の定義
- コンプライアンス要件の確認

#### 設計フェーズ
- 脅威モデリング（STRIDE、DREAD）
- セキュリティアーキテクチャレビュー
- データフロー図の作成

#### 実装フェーズ
- セキュアコーディング標準の適用
- 静的解析（SAST）
- 依存関係スキャン（SCA）

#### テストフェーズ
- 動的解析（DAST）
- ペネトレーションテスト
- セキュリティテストケース

---

## DevSecOpsの原則

### 1. セキュリティは全員の責任

**文化の変革**:
- ❌ セキュリティチームだけの仕事
- ✅ 開発者、運用者も含めた全員の責任

**実践**:
- セキュリティトレーニング
- セキュアコーディングガイドライン
- セキュリティチャンピオン制度

### 2. 自動化ファースト

**原則**:
- 手動プロセスは自動化
- CI/CDパイプラインに統合
- 高速フィードバック

**自動化対象**:
- 静的解析（SAST）
- 依存関係スキャン（SCA）
- コンテナスキャン
- IaC（Infrastructure as Code）スキャン
- シークレットスキャン

### 3. 継続的モニタリング

**実践**:
- リアルタイム脅威検知
- ログの集約・分析
- 異常検知
- インシデント対応の自動化

### 4. コンプライアンス as Code

**実践**:
- ポリシーのコード化
- 自動コンプライアンスチェック
- 監査証跡の自動収集

### 5. Defense in Depth（多層防御）

**レイヤー**:
1. ネットワーク層
2. ホスト層
3. アプリケーション層
4. データ層
5. ユーザー層

---

## CI/CDパイプラインへのセキュリティ統合

### セキュアCI/CDパイプライン

```
[1. ソースコード管理]
    ↓
  シークレットスキャン
    ↓
[2. ビルド]
    ↓
  静的解析（SAST）
  依存関係スキャン（SCA）
  ライセンスチェック
    ↓
[3. コンテナイメージ作成]
    ↓
  コンテナスキャン
  イメージ署名
    ↓
[4. ステージング環境デプロイ]
    ↓
  動的解析（DAST）
  API セキュリティテスト
  インフラスキャン（IaC）
    ↓
[5. セキュリティゲート]
    ↓
  脆弱性評価
  承認プロセス
    ↓
[6. 本番環境デプロイ]
    ↓
  セキュアな設定
  最小権限の原則
    ↓
[7. 運用監視]
    ↓
  継続的監視
  脅威検知
  インシデント対応
```

### パイプライン各ステージの詳細

#### ステージ1: コミット時

**実施項目**:
- ✅ シークレットスキャン（パスワード、APIキーの検出）
- ✅ Gitコミットの署名検証
- ✅ Pre-commitフックでのローカルチェック

**ツール**:
- **git-secrets**
- **TruffleHog**
- **Gitleaks**

#### ステージ2: ビルド時

**実施項目**:
- ✅ 静的アプリケーションセキュリティテスト（SAST）
- ✅ ソフトウェアコンポジション分析（SCA）
- ✅ コード品質チェック
- ✅ ライセンスコンプライアンス

**ツール**:
- **SonarQube** - SAST、コード品質
- **Snyk** - SCA、依存関係スキャン
- **Checkmarx** - SAST
- **Semgrep** - 静的解析

#### ステージ3: コンテナイメージ

**実施項目**:
- ✅ ベースイメージの脆弱性スキャン
- ✅ イメージレイヤーのスキャン
- ✅ 設定のベストプラクティスチェック
- ✅ イメージ署名（Cosign）

**ツール**:
- **Trivy** - コンテナスキャン
- **Grype** - 脆弱性スキャン
- **Clair** - コンテナスキャン
- **Aqua Security** - 包括的コンテナセキュリティ

#### ステージ4: デプロイ前テスト

**実施項目**:
- ✅ 動的アプリケーションセキュリティテスト（DAST）
- ✅ APIセキュリティテスト
- ✅ インフラストラクチャスキャン（IaC）
- ✅ ペネトレーションテスト（定期的）

**ツール**:
- **OWASP ZAP** - DAST
- **Burp Suite** - セキュリティテスト
- **Postman** - APIテスト
- **Checkov** - IaCスキャン

#### ステージ5: セキュリティゲート

**実施項目**:
- ✅ 脆弱性スコアリング（CVSS）
- ✅ ポリシー適合チェック
- ✅ 承認フロー（重大な脆弱性がある場合）

**基準例**:
```yaml
security_policy:
  critical_vulnerabilities: 0  # Critical: デプロイブロック
  high_vulnerabilities: 3      # High: 3件まで許容
  medium_vulnerabilities: 10   # Medium: 10件まで許容
  low_vulnerabilities: 無制限
```

#### ステージ6: デプロイ

**実施項目**:
- ✅ 最小権限の原則（IAM、RBAC）
- ✅ シークレットの安全な注入
- ✅ ネットワークポリシーの適用
- ✅ セキュリティコンテキストの設定

#### ステージ7: 運用監視

**実施項目**:
- ✅ ランタイムセキュリティ監視
- ✅ 異常検知
- ✅ ログ分析
- ✅ 脅威インテリジェンス

---

## セキュリティテスト手法

### 1. SAST（Static Application Security Testing）

**定義**: ソースコードの静的解析

**特徴**:
- コードを実行せずに分析
- 開発初期段階で実施
- 誤検知（False Positive）が多い傾向

**検出内容**:
- SQLインジェクション
- クロスサイトスクリプティング（XSS）
- バッファオーバーフロー
- ハードコードされた認証情報
- 不適切なエラーハンドリング

**推奨ツール**:
- **SonarQube** - オープンソース、多言語対応
- **Checkmarx** - エンタープライズ
- **Fortify** - 包括的SAST
- **Semgrep** - 高速、カスタマイズ可能

**実装例（CI/CD）**:
```yaml
# GitHub Actions
- name: SonarQube Scan
  uses: SonarSource/sonarcloud-github-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 2. DAST（Dynamic Application Security Testing）

**定義**: 実行中のアプリケーションへの動的テスト

**特徴**:
- ブラックボックステスト
- 実際の攻撃をシミュレート
- 誤検知が少ない

**検出内容**:
- 認証・認可の不備
- セッション管理の脆弱性
- 設定ミス
- サーバー側の脆弱性

**推奨ツール**:
- **OWASP ZAP** - オープンソース
- **Burp Suite** - 業界標準
- **Acunetix** - 自動スキャン
- **Netsparker** - 自動化に優れる

**実装例**:
```yaml
# ZAP Baseline Scan
- name: ZAP Scan
  uses: zaproxy/action-baseline@v0.7.0
  with:
    target: 'https://staging.example.com'
```

### 3. SCA（Software Composition Analysis）

**定義**: オープンソースコンポーネント・依存関係の脆弱性スキャン

**特徴**:
- ライブラリの既知脆弱性を検出
- ライセンスコンプライアンス
- サプライチェーンリスク管理

**検出内容**:
- 既知の脆弱性（CVE）
- ライセンス違反
- 古いバージョンの使用
- 推奨される修正バージョン

**推奨ツール**:
- **Snyk** - 開発者フレンドリー、自動修正提案
- **Dependabot** (GitHub) - 自動PR作成
- **WhiteSource/Mend** - エンタープライズ
- **OWASP Dependency-Check** - オープンソース

**実装例**:
```yaml
# Snyk
- name: Run Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### 4. IAST（Interactive Application Security Testing）

**定義**: SASTとDASTの中間、アプリケーション内部から監視

**特徴**:
- ランタイムエージェントを使用
- 誤検知が少ない
- 詳細なコンテキスト情報

**推奨ツール**:
- **Contrast Security**
- **Seeker** (Synopsys)

### 5. RASP（Runtime Application Self-Protection）

**定義**: ランタイムでの攻撃検知・防御

**特徴**:
- アプリケーション内に組み込まれたセキュリティ
- リアルタイムの脅威検知
- 自動的な攻撃ブロック

**推奨ツール**:
- **Contrast Security**
- **Imperva RASP**

### 6. ペネトレーションテスト

**定義**: 実際の攻撃を模擬したセキュリティテスト

**タイミング**:
- リリース前
- 定期的（年1〜2回）
- 重大な変更後

**実施方法**:
- 専門のペンテスターに依頼
- Bug Bountyプログラム

---

## コンテナセキュリティ

### コンテナセキュリティの重要性

**課題**:
- イメージに含まれる脆弱性
- 設定ミス
- ランタイムでの攻撃
- オーケストレーション（Kubernetes）のセキュリティ

### イメージスキャン

#### ベースイメージの選定

**ベストプラクティス**:
- ✅ 最小限のベースイメージ（Alpine、Distroless）
- ✅ 公式イメージの使用
- ✅ 定期的な更新

**例**:
```dockerfile
# 推奨: Distroless
FROM gcr.io/distroless/nodejs18-debian11

# 非推奨: 肥大化したイメージ
FROM ubuntu:latest
RUN apt-get update && apt-get install -y nodejs
```

#### スキャンツール

**Trivy**（推奨）:
```bash
# イメージスキャン
trivy image myapp:latest

# 高・重大のみ表示
trivy image --severity HIGH,CRITICAL myapp:latest

# CI/CD統合
trivy image --exit-code 1 --severity CRITICAL myapp:latest
```

**Grype**:
```bash
grype myapp:latest
```

**Clair**:
- CoreOS製
- APIベース

### Dockerfile のベストプラクティス

```dockerfile
# 1. 最小限のベースイメージ
FROM node:18-alpine AS base

# 2. 非rootユーザーで実行
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# 3. 不要なファイルを除外（.dockerignore使用）
WORKDIR /app
COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --only=production

# 4. マルチステージビルド
FROM base AS build
COPY --chown=nodejs:nodejs . .
RUN npm run build

FROM base AS production
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Kubernetesセキュリティ

#### Pod Security Standards

**3つのレベル**:
1. **Privileged**: 制限なし
2. **Baseline**: 最小限の制限
3. **Restricted**: 厳格な制限（推奨）

**実装例**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
```

#### Network Policies

**デフォルト拒否**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

**特定の通信のみ許可**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

#### RBAC（Role-Based Access Control）

**最小権限の原則**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
- kind: ServiceAccount
  name: myapp
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ランタイムセキュリティ

**Falco**:
- Kubernetesランタイムセキュリティ
- 異常な動作の検知

**検知例**:
- シェルの実行
- 特権コンテナの起動
- 機密ファイルへのアクセス
- ネットワークスキャン

---

## シークレット管理

### シークレット管理の重要性

**危険な例**:
```python
# ❌ ハードコーディング
API_KEY = "abc123def456"
DATABASE_URL = "postgres://user:password@localhost/db"
```

**問題点**:
- バージョン管理にコミット
- 誰でも閲覧可能
- ローテーションが困難

### ベストプラクティス

#### 1. 環境変数

**基本的なアプローチ**:
```python
# ✅ 環境変数から読み取り
import os
API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

**限界**:
- プロセスのメモリに平文で存在
- ログに出力される可能性

#### 2. シークレット管理サービス

**HashiCorp Vault**:
```bash
# シークレットの保存
vault kv put secret/myapp/config api_key=abc123

# シークレットの取得
vault kv get secret/myapp/config
```

**AWS Secrets Manager**:
```python
import boto3

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='myapp/api-key')
secret = response['SecretString']
```

**Azure Key Vault**:
```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)
secret = client.get_secret("api-key")
```

**Google Secret Manager**:
```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = "projects/my-project/secrets/api-key/versions/latest"
response = client.access_secret_version(request={"name": name})
secret = response.payload.data.decode("UTF-8")
```

#### 3. Kubernetes Secrets

**作成**:
```bash
kubectl create secret generic myapp-secrets \
  --from-literal=api-key=abc123 \
  --from-literal=db-password=secret
```

**使用**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: myapp-secrets
          key: api-key
```

**暗号化**:
```yaml
# Kubernetes Secrets の暗号化（EncryptionConfiguration）
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:
        keys:
        - name: key1
          secret: <base64 encoded secret>
```

#### 4. External Secrets Operator

**Vault、AWS Secrets Managerなどと統合**:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-external-secret
spec:
  secretStoreRef:
    name: vault-backend
  target:
    name: myapp-secrets
  data:
  - secretKey: api-key
    remoteRef:
      key: secret/data/myapp
      property: api_key
```

### シークレットスキャン

**ツール**:
- **TruffleHog** - Gitリポジトリスキャン
- **Gitleaks** - シークレット検出
- **git-secrets** - コミット前チェック

**GitHub Actions例**:
```yaml
- name: Gitleaks Scan
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### シークレットローテーション

**ベストプラクティス**:
- 定期的なローテーション（30〜90日）
- 自動化されたローテーション
- 侵害検知時の即座の無効化

---

## 脆弱性管理

### 脆弱性管理プロセス

```
1. 発見（Discovery）
   ↓
2. 評価（Assessment）
   ↓
3. 優先順位付け（Prioritization）
   ↓
4. 修正（Remediation）
   ↓
5. 検証（Verification）
   ↓
6. 報告（Reporting）
```

### 脆弱性スコアリング

#### CVSS（Common Vulnerability Scoring System）

**スコア範囲**:
- **9.0-10.0**: Critical（緊急）
- **7.0-8.9**: High（高）
- **4.0-6.9**: Medium（中）
- **0.1-3.9**: Low（低）

**対応期限の例**:
```
Critical: 24時間以内
High:     1週間以内
Medium:   1ヶ月以内
Low:      次回定期メンテナンス
```

### SLA（Service Level Agreement）

**例**:
```yaml
vulnerability_sla:
  critical:
    detection_to_fix: 24h
    fix_to_deploy: 24h
  high:
    detection_to_fix: 7d
    fix_to_deploy: 3d
  medium:
    detection_to_fix: 30d
    fix_to_deploy: 7d
```

### 脆弱性データベース

- **NVD（National Vulnerability Database）**
- **CVE（Common Vulnerabilities and Exposures）**
- **GitHub Advisory Database**
- **Snyk Vulnerability DB**

### パッチ管理

**自動化**:
- Dependabot（GitHub）
- Renovate Bot
- Snyk自動修正

**Dependabot設定例**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
```

---

## セキュリティ監視とインシデント対応

### セキュリティ監視

#### ログ収集・分析

**収集対象**:
- アプリケーションログ
- アクセスログ
- セキュリティイベント
- 認証・認可ログ
- システムログ

**SIEM（Security Information and Event Management）**:
- **Splunk**
- **Elastic Security**
- **AWS Security Hub**
- **Azure Sentinel**

#### 異常検知

**検知項目**:
- 不正なログイン試行
- 異常なトラフィックパターン
- 権限昇格の試み
- データ流出の兆候
- マルウェア活動

**ツール**:
- **Falco** - Kubernetesランタイムセキュリティ
- **OSSEC** - ホストベースIDS
- **Wazuh** - セキュリティ監視

### インシデント対応

#### インシデント対応プロセス

```
1. 準備（Preparation）
   ↓
2. 検知・分析（Detection & Analysis）
   ↓
3. 封じ込め（Containment）
   ↓
4. 根絶（Eradication）
   ↓
5. 復旧（Recovery）
   ↓
6. 事後レビュー（Post-Incident Review）
```

#### インシデント対応計画

**含めるべき項目**:
- ✅ 連絡体制（エスカレーションパス）
- ✅ 役割と責任
- ✅ 対応手順書（Runbook）
- ✅ コミュニケーションプラン
- ✅ ログ保全手順

#### 自動化されたインシデント対応

**SOAR（Security Orchestration, Automation and Response）**:
- **Splunk SOAR**
- **Cortex XSOAR** (Palo Alto)
- **IBM Resilient**

**例**:
```
異常検知 → 自動隔離 → 担当者通知 → 調査 → 修復 → 報告
```

---

## コンプライアンスと監査

### コンプライアンス要件

#### 主要な規制・標準

**GDPR（一般データ保護規則）**:
- 個人データの保護
- データ主体の権利
- データ侵害の通知（72時間以内）

**PCI DSS（Payment Card Industry Data Security Standard）**:
- クレジットカード情報の保護
- 12の要件

**SOC 2**:
- サービス組織の内部統制
- 5つの信頼サービス基準

**ISO 27001**:
- 情報セキュリティマネジメントシステム

### Compliance as Code

**ポリシーのコード化**:

**Open Policy Agent (OPA)**:
```rego
# Kubernetes Podのセキュリティポリシー
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.securityContext.runAsNonRoot
    msg = "Pods must run as non-root user"
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged
    msg = sprintf("Privileged container not allowed: %v", [container.name])
}
```

**Kyverno**:
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  validationFailureAction: enforce
  rules:
  - name: check-runAsNonRoot
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Running as root is not allowed"
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
```

### 監査ログ

**記録すべき項目**:
- 認証イベント
- 権限変更
- リソースアクセス
- 設定変更
- セキュリティイベント

**Kubernetes Audit Log**:
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: RequestResponse
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
- level: Metadata
  resources:
  - group: ""
    resources: ["pods"]
```

---

## 組織とプロセス

### セキュリティチャンピオン制度

**概念**:
各開発チームにセキュリティ担当者（チャンピオン）を配置

**役割**:
- セキュリティベストプラクティスの普及
- セキュリティレビュー
- セキュリティトレーニングの実施
- セキュリティチームとの橋渡し

### セキュリティトレーニング

**トレーニング内容**:
1. **セキュアコーディング**: OWASP Top 10、SQLインジェクション、XSS
2. **脅威モデリング**: STRIDE、DREAD
3. **DevSecOpsツール**: SAST、DAST、SCA
4. **インシデント対応**: 初動対応、エスカレーション

**推奨プログラム**:
- **OWASP WebGoat** - ハンズオン学習
- **HackTheBox** - 実践的トレーニング
- **Secure Code Warrior** - ゲーミフィケーション

### セキュリティゲートレビュー

**フェーズゲート**:
```
設計レビュー → 実装レビュー → リリース前レビュー
     ↓              ↓                  ↓
脅威モデリング   コードレビュー   ペネトレーションテスト
```

### バグバウンティプログラム

**メリット**:
- 外部の専門家による発見
- 継続的なセキュリティテスト
- コスト効率的

**プラットフォーム**:
- **HackerOne**
- **Bugcrowd**
- **Synack**

---

## 推奨ツールとサービス

### カテゴリ別推奨ツール

#### SAST（静的解析）
1. **SonarQube** - オープンソース、多言語、コード品質
2. **Checkmarx** - エンタープライズ、詳細な分析
3. **Semgrep** - 高速、カスタマイズ可能
4. **Fortify** - 包括的、大規模組織向け
5. **CodeQL** (GitHub) - セマンティック解析

#### DAST（動的解析）
1. **OWASP ZAP** - オープンソース、CI/CD統合
2. **Burp Suite** - 業界標準、手動+自動
3. **Acunetix** - 高度な自動スキャン
4. **Netsparker** - 自動化に優れる
5. **AppScan** (HCL) - エンタープライズ

#### SCA（依存関係スキャン）
1. **Snyk** - 開発者フレンドリー、自動修正
2. **Dependabot** (GitHub) - 自動PR作成、無料
3. **WhiteSource/Mend** - ライセンス管理
4. **Sonatype Nexus IQ** - ソフトウェアサプライチェーン
5. **OWASP Dependency-Check** - オープンソース

#### コンテナセキュリティ
1. **Trivy** - 高速、包括的、オープンソース
2. **Grype** - Ancホstイン、高精度
3. **Aqua Security** - ランタイム保護
4. **Sysdig Secure** - ランタイム監視
5. **Prisma Cloud** (Palo Alto) - 包括的クラウドセキュリティ

#### シークレット管理
1. **HashiCorp Vault** - 業界標準、多機能
2. **AWS Secrets Manager** - AWS統合
3. **Azure Key Vault** - Azure統合
4. **Google Secret Manager** - GCP統合
5. **CyberArk** - エンタープライズ

#### IaCスキャン
1. **Checkov** - Terraform、Kubernetes、Docker
2. **Terrascan** - Terraform専門
3. **tfsec** - Terraform、高速
4. **KICS** (Checkmarx) - マルチクラウド
5. **Prowler** - AWS専門

#### セキュリティ監視
1. **Datadog Security Monitoring** - 統合監視
2. **Splunk** - SIEM、ログ分析
3. **Elastic Security** - オープンソース、SIEM
4. **Falco** - Kubernetesランタイム
5. **Wazuh** - ホストベースIDS

#### API セキュリティ
1. **42Crunch** - API セキュリティプラットフォーム
2. **Salt Security** - API保護
3. **Postman** - APIテスト、モニタリング
4. **OWASP ZAP** - APIスキャン

### 統合プラットフォーム

**包括的DevSecOpsプラットフォーム**:
1. **Snyk** - SAST、SCA、コンテナ、IaC
2. **GitLab Ultimate** - ビルトインセキュリティ
3. **GitHub Advanced Security** - GitHub統合
4. **Checkmarx One** - 統合プラットフォーム
5. **Veracode** - アプリケーションセキュリティ

---

## ベストプラクティス

### 1. セキュリティを文化に

✅ **セキュリティは全員の責任**
- 開発者教育
- セキュリティチャンピオン
- 失敗から学ぶ文化

✅ **Shift Left**
- 設計段階から考慮
- 早期発見・早期修正

### 2. 自動化を徹底

✅ **CI/CDパイプラインに統合**
- すべてのコミットでスキャン
- 自動デプロイメントゲート
- 継続的監視

✅ **手動作業の削減**
- 自動パッチ適用
- 自動コンプライアンスチェック

### 3. 最小権限の原則

✅ **アクセス制御**
- 必要最小限の権限
- Just-In-Time（JIT）アクセス
- 定期的な権限レビュー

✅ **ネットワークセグメンテーション**
- マイクロセグメンテーション
- ゼロトラストネットワーク

### 4. Defense in Depth（多層防御）

✅ **複数のセキュリティレイヤー**
- ネットワーク層
- ホスト層
- アプリケーション層
- データ層

✅ **単一障害点の排除**
- 冗長化
- フェイルセーフ設計

### 5. 継続的改善

✅ **メトリクスの測定**
- 脆弱性検出数
- 修正までの時間（MTTR）
- デプロイ頻度
- セキュリティインシデント数

✅ **定期的なレビュー**
- セキュリティポリシーの見直し
- ツールの評価
- プロセスの最適化

### 6. 透明性とコミュニケーション

✅ **セキュリティ状況の可視化**
- ダッシュボード
- 定期レポート
- ステークホルダーへの報告

✅ **インシデントの共有**
- ポストモーテム
- 学びの共有

### 7. サプライチェーンセキュリティ

✅ **依存関係の管理**
- SBOMの作成
- 定期的なスキャン
- 信頼できるソースからの取得

✅ **ビルドパイプラインの保護**
- 署名検証
- 改ざん検知

---

## 成熟度モデル

### DevSecOps成熟度レベル

#### レベル1: 初期（Ad-hoc）

**特徴**:
- セキュリティは後付け
- 手動のセキュリティチェック
- インシデント対応が反応的

**実施項目**:
- 基本的なセキュリティツールの導入
- セキュリティ方針の策定

#### レベル2: 管理（Managed）

**特徴**:
- 一部の自動化
- CI/CDに基本的なセキュリティチェック
- セキュリティトレーニングの開始

**実施項目**:
- SAST、SCAの導入
- コンテナスキャン
- シークレット管理の導入

#### レベル3: 定義（Defined）

**特徴**:
- セキュリティプロセスが定義・文書化
- CI/CDパイプライン全体にセキュリティ統合
- セキュリティチャンピオン制度

**実施項目**:
- DAST導入
- 脅威モデリング
- セキュリティゲート
- コンプライアンス自動化

#### レベル4: 測定（Quantitatively Managed）

**特徴**:
- セキュリティメトリクスの測定
- データドリブンな意思決定
- 継続的監視

**実施項目**:
- セキュリティダッシュボード
- SLA設定
- インシデント対応の自動化

#### レベル5: 最適化（Optimizing）

**特徴**:
- 継続的改善
- プロアクティブなセキュリティ
- AIを活用した脅威検知

**実施項目**:
- カオスエンジニアリング
- バグバウンティ
- ゼロトラストアーキテクチャ

### 成熟度評価チェックリスト

```
□ SAST/DAST/SCAツールの導入
□ CI/CDパイプラインへのセキュリティ統合
□ コンテナスキャン
□ シークレット管理
□ 脆弱性管理プロセス
□ セキュリティトレーニング
□ インシデント対応計画
□ セキュリティ監視
□ コンプライアンス自動化
□ セキュリティメトリクス測定
□ 定期的なペネトレーションテスト
□ バグバウンティプログラム
□ セキュリティチャンピオン制度
□ 脅威モデリング
□ ゼロトラストアーキテクチャ
```

---

## 実装ロードマップ

### フェーズ1: 基礎構築（1〜3ヶ月）

**目標**: 基本的なセキュリティツールの導入

**実施項目**:
1. **ツール導入**
   - ✅ SCA（Snyk, Dependabot）
   - ✅ シークレットスキャン（Gitleaks）
   - ✅ コンテナスキャン（Trivy）

2. **プロセス**
   - ✅ セキュリティポリシー策定
   - ✅ セキュリティトレーニング計画

3. **文化**
   - ✅ セキュリティ意識の向上
   - ✅ セキュリティチャンピオン選定

### フェーズ2: CI/CD統合（3〜6ヶ月）

**目標**: CI/CDパイプラインへのセキュリティ統合

**実施項目**:
1. **ツール統合**
   - ✅ SAST（SonarQube）
   - ✅ DAST（OWASP ZAP）
   - ✅ IaCスキャン（Checkov）

2. **プロセス**
   - ✅ セキュリティゲートの設定
   - ✅ 脆弱性管理プロセス
   - ✅ パッチ管理の自動化

3. **監視**
   - ✅ 基本的なセキュリティ監視
   - ✅ ログ集約

### フェーズ3: 成熟化（6〜12ヶ月）

**目標**: プロアクティブなセキュリティ

**実施項目**:
1. **高度なツール**
   - ✅ ランタイムセキュリティ（Falco）
   - ✅ SIEM導入
   - ✅ 脅威インテリジェンス

2. **プロセス**
   - ✅ 脅威モデリング
   - ✅ ペネトレーションテスト
   - ✅ インシデント対応の自動化

3. **文化**
   - ✅ バグバウンティ
   - ✅ セキュリティカルチャーの定着

### フェーズ4: 最適化（12ヶ月〜）

**目標**: 継続的改善

**実施項目**:
1. **メトリクス**
   - ✅ セキュリティダッシュボード
   - ✅ データドリブンな意思決定

2. **高度な実践**
   - ✅ ゼロトラストアーキテクチャ
   - ✅ AIを活用した脅威検知
   - ✅ カオスエンジニアリング

---

## まとめ

### DevSecOps成功の鍵

1. ✅ **セキュリティは全員の責任**: 開発者、運用者、セキュリティチーム全員が関与
2. ✅ **Shift Left**: 開発プロセスの早い段階からセキュリティを組み込む
3. ✅ **自動化**: CI/CDパイプラインにセキュリティツールを統合
4. ✅ **継続的監視**: リアルタイムの脅威検知と対応
5. ✅ **文化の変革**: セキュリティ意識の向上、失敗から学ぶ
6. ✅ **最小権限**: 必要最小限のアクセス権限
7. ✅ **多層防御**: 複数のセキュリティレイヤー
8. ✅ **メトリクス測定**: データドリブンな改善
9. ✅ **コンプライアンス as Code**: ポリシーの自動化
10. ✅ **継続的改善**: 定期的なレビューと最適化

### 次のアクション

1. 現在のセキュリティ成熟度を評価
2. セキュリティポリシーを策定
3. 優先順位の高いツールから導入（SCA、SAST）
4. CI/CDパイプラインに統合
5. セキュリティトレーニングを実施
6. メトリクスを測定し、継続的に改善

### 重要な考え方

DevSecOpsは**ツールの導入だけではなく、文化とプロセスの変革**です。

- セキュリティを後付けにしない
- 開発速度を犠牲にしない
- セキュリティと開発の協力関係を構築
- 失敗を許容し、学びに変える

---

## 参考資料

### 公式リソース

**OWASP（Open Web Application Security Project）**:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)

**NIST（National Institute of Standards and Technology）**:
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

**CIS（Center for Internet Security）**:
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [CIS Controls](https://www.cisecurity.org/controls/)

### ツールリソース

**オープンソースツール**:
- [OWASP ZAP](https://www.zaproxy.org/)
- [SonarQube](https://www.sonarqube.org/)
- [Trivy](https://github.com/aquasecurity/trivy)
- [Falco](https://falco.org/)

**コマーシャルツール**:
- [Snyk](https://snyk.io/)
- [Checkmarx](https://www.checkmarx.com/)
- [Veracode](https://www.veracode.com/)

### 学習リソース

**書籍**:
- 「DevSecOps」Jim Bird
- 「The DevOps Handbook」Gene Kim他
- 「Security Engineering」Ross Anderson

**オンライン学習**:
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [PentesterLab](https://pentesterlab.com/)

### 関連ドキュメント

- [開発プロセスガイド](./dev_process.md)
- [DX推進ロードマップ](./dx_roadmap.md)
- [マイクロサービスアーキテクチャ設計ガイド](./microservices_guide.md)
- [アジャイル/スクラム開発プロセスガイド](./agile_scrum_guide.md)

---

**文書バージョン**: 1.0
**最終更新日**: 2025年11月22日
**作成**: IPA資料に基づく開発プロセスガイド作成プロジェクト
