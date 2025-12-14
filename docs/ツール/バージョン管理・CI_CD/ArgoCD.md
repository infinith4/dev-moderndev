# ArgoCD

## 概要

**ArgoCD**は、Kubernetes向けのGitOps継続的デリバリー（CD）ツールです。Gitリポジトリをアプリケーション定義の信頼できる唯一の情報源（Single Source of Truth）として、Kubernetesクラスタへのデプロイを自動化・可視化します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Argo Project（CNCF Graduated Project） |
| **種別** | GitOps継続的デリバリーツール |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://argo-cd.readthedocs.io/ |
| **ドキュメント** | https://argo-cd.readthedocs.io/en/stable/ |

## 主な特徴

### 1. GitOps原則
- Gitリポジトリが唯一の信頼できる情報源
- 宣言的なKubernetesマニフェスト管理
- 自動同期・ヘルスチェック
- Git履歴によるロールバック

### 2. マルチテナント・マルチクラスタ
- 複数クラスタの一元管理
- RBAC統合（Kubernetes RBAC、SSO）
- プロジェクト・アプリケーション分離

### 3. 豊富なマニフェスト対応
- Kubernetes YAML
- Helm Charts
- Kustomize
- Jsonnet
- Custom Config Management Plugins

### 4. WebUI・CLI
- リアルタイム可視化
- リソース依存関係の可視化
- Diff表示・手動同期
- CLI（argocd）による操作

## 使い方

### インストール

#### Kubernetesクラスタへのインストール

```bash
# ArgoCD Namespace作成
kubectl create namespace argocd

# ArgoCD インストール
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# ArgoCD Serverをポートフォワード
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 初期パスワード取得
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# ブラウザでアクセス
# https://localhost:8080
# ユーザー: admin
# パスワード: （上記で取得したパスワード）
```

#### ArgoCD CLI インストール

```bash
# macOS
brew install argocd

# Linux
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

# Windows
choco install argocd-cli

# CLIログイン
argocd login localhost:8080 --username admin --password <initial-password>

# パスワード変更
argocd account update-password
```

### アプリケーション登録

#### CLI でのアプリケーション作成

```bash
# アプリケーション作成
argocd app create guestbook \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default

# アプリケーション同期
argocd app sync guestbook

# アプリケーション状態確認
argocd app get guestbook

# アプリケーション一覧
argocd app list
```

#### YAML マニフェストでのアプリケーション定義

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  # プロジェクト
  project: default

  # ソースリポジトリ
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook

  # デプロイ先クラスタ
  destination:
    server: https://kubernetes.default.svc
    namespace: default

  # 同期ポリシー
  syncPolicy:
    automated:
      prune: true          # 削除されたリソースを自動削除
      selfHeal: true       # 手動変更を自動修正
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

```bash
# アプリケーションデプロイ
kubectl apply -f application.yaml
```

### Helmチャートのデプロイ

```yaml
# helm-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-helm
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: nginx
    targetRevision: 15.4.4
    helm:
      releaseName: my-nginx
      parameters:
        - name: replicaCount
          value: "3"
        - name: service.type
          value: LoadBalancer
      values: |
        image:
          tag: 1.25.0
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
  destination:
    server: https://kubernetes.default.svc
    namespace: nginx
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Kustomize のデプロイ

```yaml
# kustomize-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kustomize-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/your-repo.git
    targetRevision: main
    path: overlays/production
    kustomize:
      namePrefix: prod-
      commonLabels:
        environment: production
      images:
        - nginx:1.25.0=nginx:1.25.1  # イメージオーバーライド
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### マルチクラスタ管理

```bash
# 外部クラスタ登録
kubectl config use-context production-cluster
argocd cluster add production-cluster --name production

# クラスタ一覧
argocd cluster list

# 外部クラスタへのデプロイ
argocd app create prod-app \
  --repo https://github.com/your-org/your-repo.git \
  --path manifests/production \
  --dest-name production \
  --dest-namespace default
```

### プロジェクト管理

```yaml
# project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-a
  namespace: argocd
spec:
  description: Team A Project

  # ソースリポジトリ制限
  sourceRepos:
    - https://github.com/team-a/*

  # デプロイ先制限
  destinations:
    - namespace: team-a-*
      server: https://kubernetes.default.svc

  # クラスタリソース制限（Cluster-scoped resources）
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
    - group: 'rbac.authorization.k8s.io'
      kind: ClusterRole

  # Namespace リソース制限
  namespaceResourceWhitelist:
    - group: 'apps'
      kind: Deployment
    - group: ''
      kind: Service
    - group: ''
      kind: ConfigMap

  # RBAC
  roles:
    - name: developer
      description: Developers for Team A
      policies:
        - p, proj:team-a:developer, applications, get, team-a/*, allow
        - p, proj:team-a:developer, applications, sync, team-a/*, allow
      groups:
        - team-a-developers
```

### Webhook 設定（自動同期トリガー）

```yaml
# GitHub Webhook設定
# Settings → Webhooks → Add webhook
Payload URL: https://argocd.example.com/api/webhook
Content type: application/json
Secret: <your-webhook-secret>
Events: Just the push event
```

### Notifications（通知設定）

```yaml
# argocd-notifications-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} is now running new version.
    slack:
      attachments: |
        [{
          "title": "{{ .app.metadata.name}}",
          "title_link":"{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "#18be52",
          "fields": [
          {
            "title": "Sync Status",
            "value": "{{.app.status.sync.status}}",
            "short": true
          },
          {
            "title": "Repository",
            "value": "{{.app.spec.source.repoURL}}",
            "short": true
          }
          ]
        }]
  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-deployed]
```

### Image Updater統合

```yaml
# argocd-image-updater
# 新しいコンテナイメージを自動検出してGitリポジトリを更新

# Application にアノテーション追加
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  annotations:
    argocd-image-updater.argoproj.io/image-list: myimage=nginx
    argocd-image-updater.argoproj.io/myimage.update-strategy: latest
    argocd-image-updater.argoproj.io/write-back-method: git
spec:
  # ... 省略
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **CI/CD構築** | GitOps CD実装 | Kubernetes デプロイ自動化 |
| **テスト** | ステージング環境デプロイ | テスト環境への自動デプロイ |
| **導入** | 本番環境デプロイ | 本番リリース・ロールバック |

## メリット

- **GitOps原則**: Gitが唯一の信頼できる情報源、監査証跡
- **自動同期・自己修復**: 手動変更を自動修正、Drift検出
- **マルチクラスタ対応**: 複数Kubernetesクラスタを一元管理
- **可視化**: WebUIでリアルタイム可視化、リソース依存関係表示
- **ロールバック容易**: Git履歴で任意のバージョンにロールバック
- **RBAC統合**: Kubernetes RBAC、SSO（OIDC、SAML）対応
- **無料・オープンソース**: CNCF Graduated Project、活発なコミュニティ

## デメリット

- **Kubernetes専用**: Kubernetesクラスタが必須
- **学習曲線**: GitOps概念、ArgoCD固有機能の習得が必要
- **リソース消費**: ArgoCD自体がKubernetesリソースを消費
- **複雑なワークフローには制限**: 複雑なCI/CDパイプラインはArgo Workflowsと併用推奨
- **Gitリポジトリ依存**: Gitダウン時にデプロイ不可

## 類似ツールとの比較

| ツール | 特徴 | コスト | 適用場面 |
|--------|------|--------|----------|
| **ArgoCD** | GitOps CD、Kubernetes特化 | 無料 | Kubernetesデプロイ自動化 |
| **Flux** | GitOps CD、軽量 | 無料 | Kubernetesデプロイ自動化 |
| **Spinnaker** | マルチクラウドCD | 無料 | 複雑なデプロイパイプライン |
| **Jenkins X** | Kubernetes CI/CD | 無料 | Jenkins統合、Kubernetes |

## ベストプラクティス

### 1. App of Apps パターン

```yaml
# app-of-apps.yaml（親アプリケーション）
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/argocd-apps.git
    targetRevision: HEAD
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```yaml
# apps/app1.yaml（子アプリケーション）
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app1
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/app1.git
    targetRevision: HEAD
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: app1
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 2. 環境別リポジトリ構成

```text
your-repo/
├── base/                 # 共通マニフェスト
│   ├── deployment.yaml
│   └── service.yaml
├── overlays/
│   ├── development/      # 開発環境
│   │   └── kustomization.yaml
│   ├── staging/          # ステージング環境
│   │   └── kustomization.yaml
│   └── production/       # 本番環境
│       └── kustomization.yaml
```

### 3. Sync Waves（デプロイ順序制御）

```yaml
# database.yaml（最初にデプロイ）
apiVersion: v1
kind: ConfigMap
metadata:
  name: database-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"
---
# application.yaml（データベース後にデプロイ）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

### 4. Health Assessment（カスタムヘルスチェック）

```yaml
# argocd-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.argoproj.io_Rollout: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.phase == "Healthy" then
        hs.status = "Healthy"
        hs.message = "Rollout is healthy"
        return hs
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for rollout"
    return hs
```

## 公式リソース

- **公式サイト**: https://argo-cd.readthedocs.io/
- **GitHub**: https://github.com/argoproj/argo-cd
- **ドキュメント**: https://argo-cd.readthedocs.io/en/stable/
- **Getting Started**: https://argo-cd.readthedocs.io/en/stable/getting_started/
- **Best Practices**: https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/

## まとめ

ArgoCDは、GitOps原則に基づくKubernetes向け継続的デリバリーツールです。Gitリポジトリを唯一の信頼できる情報源として、Kubernetesクラスタへのデプロイを自動化・可視化します。無料でありながら、マルチクラスタ管理、自動同期、RBAC統合などエンタープライズレベルの機能を提供し、Kubernetesデプロイの標準ツールとして広く採用されています。

---

**最終更新**: 2025-12-06
**対象バージョン**: ArgoCD v2.9+
