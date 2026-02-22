# Kubernetes (K8s)

## 概要

Kubernetes（K8s）は、Googleが開発したオープンソースのコンテナオーケストレーションプラットフォームです。2014年にリリースされ、Cloud Native Computing Foundation（CNCF）のフラグシッププロジェクトとして、コンテナ化されたアプリケーションのデプロイ、スケーリング、管理を自動化します。宣言的な設定によりインフラをコード化し、自己修復、水平スケーリング、サービスディスカバリ、ロードバランシング等の機能を提供します。マイクロサービスアーキテクチャの標準プラットフォームとして広く採用されています。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Kubernetes (OSS)** | 🟢 無料 | オープンソース、セルフホスト、Apache License 2.0 |
| **マネージドKubernetes** | | クラウドプロバイダーのマネージドサービス |
| - **Google GKE Standard** | 💰 $0.10/cluster/時間 + ノード | フルマネージド、自動アップグレード |
| - **Amazon EKS** | 💰 $0.10/cluster/時間 + ノード | AWS統合、Fargate対応 |
| - **Azure AKS** | 🟢 コントロールプレーン無料 + ノード | Azure統合、無料コントロールプレーン |
| - **DigitalOcean DOKS** | 💰 無料 + ノード | シンプル、低価格ノード |

**注意**: Kubernetes本体は無料。クラウド上のマネージドサービスはコントロールプレーン＋ワーカーノードの料金が発生。

## メリット・デメリット

### メリット
- ✅ **自動スケーリング**: 負荷に応じた自動的なPodスケーリング
- ✅ **自己修復**: 障害時の自動再起動、レプリカ再配置
- ✅ **宣言的設定**: YAMLでインフラを定義、Gitで管理可能
- ✅ **サービスディスカバリ**: 自動的なロードバランシング、DNS
- ✅ **ローリングアップデート**: ダウンタイムゼロのデプロイ
- ✅ **シークレット管理**: 機密情報の安全な管理
- ✅ **マルチクラウド**: AWS、Azure、GCP、オンプレミスで同一の運用
- ✅ **豊富なエコシステム**: Helm、Prometheus、Istio等の統合

### デメリット
- ❌ **複雑性**: 学習曲線が急、概念の理解に時間がかかる
- ❌ **オーバーヘッド**: 小規模アプリには過剰な機能
- ❌ **リソース消費**: コントロールプレーンに一定のリソースが必要
- ❌ **運用負荷**: セルフホスト時の保守・アップグレード負担
- ❌ **ネットワーク複雑性**: ネットワークポリシー、Ingress等の設定が複雑
- ❌ **デバッグ困難**: 分散システムのトラブルシューティングが難しい

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **6. 詳細設計（インフラ）** | K8sクラスター設計、マニフェスト設計 | K8s設計書、マニフェスト |
| **8. インフラ構築** | K8sクラスターのプロビジョニング | クラスター、名前空間 |
| **8-1. CI/CD** | 自動デプロイパイプライン構築 | デプロイマニフェスト |
| **10. テスト（インフラ）** | K8s設定のテスト、検証 | テスト結果 |
| **11. 導入** | 本番環境へのアプリケーションデプロイ | 本番マニフェスト、監視設定 |

## 基本的な利用方法

### 1. インストール

```bash
# kubectl（K8s CLIツール）のインストール

# macOS (Homebrew)
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Windows (Chocolatey)
choco install kubernetes-cli

# バージョン確認
kubectl version --client

# ローカルK8sクラスター（開発用）

# Minikube（シングルノードクラスター）
brew install minikube
minikube start

# Kind（Docker-in-Docker クラスター）
brew install kind
kind create cluster

# Docker Desktop（macOS/Windows）
# Settings → Kubernetes → Enable Kubernetes
```

### 2. 基本コマンド

```bash
# クラスター情報
kubectl cluster-info
kubectl get nodes

# Podの操作
kubectl get pods
kubectl get pods -n kube-system  # 特定名前空間
kubectl get pods -A  # 全名前空間
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- /bin/bash

# Deploymentの操作
kubectl get deployments
kubectl create deployment nginx --image=nginx:latest
kubectl scale deployment nginx --replicas=3
kubectl delete deployment nginx

# Serviceの操作
kubectl get services
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# 名前空間の操作
kubectl get namespaces
kubectl create namespace dev
kubectl config set-context --current --namespace=dev

# マニフェストの適用
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml

# ポートフォワード（ローカルアクセス）
kubectl port-forward pod/<pod-name> 8080:80
```

### 3. 基本的なマニフェスト

#### Deployment（デプロイメント）
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.24
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service（サービス）
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer  # ClusterIP, NodePort, LoadBalancer
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

#### ConfigMap（設定情報）
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgres://db:5432/myapp"
  log_level: "info"
  app.properties: |
    key1=value1
    key2=value2
```

#### Secret（機密情報）
```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  # Base64エンコードされた値
  username: YWRtaW4=  # admin
  password: cGFzc3dvcmQ=  # password
```

```bash
# Secretの作成（コマンドライン）
kubectl create secret generic app-secret \
  --from-literal=username=admin \
  --from-literal=password=password
```

## 工程別の活用方法

### 6. 詳細設計（インフラ）での活用

**目的**: K8sクラスターアーキテクチャの設計

**活用方法**:
- クラスター構成の設計
- 名前空間戦略
- リソース制限の設計
- ネットワークポリシーの設計

**実装例（マルチ環境設計）**:
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production

---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging

---
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: development
```

**ResourceQuota（リソース制限）**:
```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "50"
    services.loadbalancers: "5"
```

**NetworkPolicy（ネットワークポリシー）**:
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-from-frontend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

---

### 8. インフラ構築での活用

**目的**: K8sクラスターのプロビジョニング

**活用方法**:
- マネージドK8sクラスターの作成
- Helmチャートでのアプリケーションインストール
- Ingress Controllerの設定

**実装例（EKSクラスター作成 - Terraform）**:
```hcl
# eks-cluster.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "my-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 5

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
  }
}
```

```bash
# クラスター作成後の接続設定
aws eks update-kubeconfig --name my-cluster --region ap-northeast-1

# Helm（パッケージマネージャー）のインストール
brew install helm

# Ingress Controllerのインストール（NGINX）
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

**Ingress（L7ロードバランサー）**:
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8080
```

---

### 8-1. CI/CDでの活用

**目的**: 自動デプロイパイプラインの構築

**活用方法**:
- GitOpsワークフロー（ArgoCD、Flux）
- Helmチャートのデプロイ
- カナリアデプロイメント

**GitHub Actions統合**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

env:
  CLUSTER_NAME: my-cluster
  REGION: ap-northeast-1

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.REGION }}

      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name ${{ env.CLUSTER_NAME }} --region ${{ env.REGION }}

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
          kubectl rollout status deployment/myapp

      - name: Verify deployment
        run: |
          kubectl get pods
          kubectl get svc
```

**Helmチャート構造**:
```
mychart/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── _helpers.tpl
```

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: My Application Helm Chart
version: 1.0.0
appVersion: "1.0"

# values.yaml
replicaCount: 3

image:
  repository: myapp
  tag: "1.0"
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

```bash
# Helmチャートのデプロイ
helm install myapp ./mychart -f values-prod.yaml

# アップグレード
helm upgrade myapp ./mychart -f values-prod.yaml

# ロールバック
helm rollback myapp 1
```

---

### 10. テスト（インフラ）での活用

**目的**: K8s設定のテストと検証

**活用方法**:
- kubeval（マニフェスト検証）
- kube-score（ベストプラクティスチェック）
- Polaris（セキュリティ監査）

**実装例（マニフェスト検証）**:
```bash
# kubevalでYAMLバリデーション
docker run -v $(pwd):/data \
  garethr/kubeval /data/deployment.yaml

# kube-scoreでベストプラクティスチェック
docker run -v $(pwd):/project \
  zegl/kube-score:latest score /project/deployment.yaml

# Polarisでセキュリティ監査
kubectl apply -f https://github.com/FairwindsOps/polaris/releases/latest/download/dashboard.yaml
kubectl port-forward -n polaris svc/polaris-dashboard 8080:80
```

**CI/CDでの検証**:
```yaml
# .github/workflows/validate.yml
name: Validate Kubernetes Manifests

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Validate with kubeval
        uses: instrumenta/kubeval-action@master
        with:
          files: k8s/

      - name: Check with kube-score
        run: |
          docker run -v $(pwd):/project \
            zegl/kube-score:latest score /project/k8s/*.yaml
```

---

### 11. 導入での活用

**目的**: 本番環境への安全なデプロイ

**活用方法**:
- ブルー/グリーンデプロイメント
- カナリアリリース
- ロールバック手順

**実装例（カナリアデプロイメント）**:
```yaml
# deployment-stable.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
  labels:
    app: myapp
    version: stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      version: stable
  template:
    metadata:
      labels:
        app: myapp
        version: stable
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0

---
# deployment-canary.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
  labels:
    app: myapp
    version: canary
spec:
  replicas: 1  # 10%のトラフィック
  selector:
    matchLabels:
      app: myapp
      version: canary
  template:
    metadata:
      labels:
        app: myapp
        version: canary
    spec:
      containers:
      - name: myapp
        image: myapp:1.1.0

---
# service.yaml (両方のDeploymentを対象)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp  # versionラベルを含めない
  ports:
  - port: 80
    targetPort: 8080
```

**StatefulSet（ステートフルアプリ）**:
```yaml
# statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## 公式ドキュメント

- [Kubernetes 公式サイト](https://kubernetes.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [Kubernetes GitHub Repository](https://github.com/kubernetes/kubernetes)
- [Helm Documentation](https://helm.sh/docs/)

## 学習リソース

### チュートリアル
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/) - ブラウザでK8s実習
- [Katacoda Kubernetes Scenarios](https://www.katacoda.com/courses/kubernetes)

### 書籍
- "Kubernetes: Up and Running" by Kelsey Hightower (O'Reilly)
- "Kubernetes in Action" by Marko Lukša (Manning)
- "The Kubernetes Book" by Nigel Poulton

### 動画・コース
- [Kubernetes Tutorial for Beginners](https://www.youtube.com/results?search_query=kubernetes+tutorial)
- [Certified Kubernetes Administrator (CKA)](https://www.cncf.io/certification/cka/)
- [Udemy - Kubernetes Mastery](https://www.udemy.com/topic/kubernetes/)

### コミュニティ
- [Kubernetes Slack](https://slack.k8s.io/)
- [Kubernetes GitHub Discussions](https://github.com/kubernetes/kubernetes/discussions)
- [Stack Overflow - Kubernetes](https://stackoverflow.com/questions/tagged/kubernetes)

## 関連リンク

### ツール
- [Helm](https://helm.sh/) - K8sパッケージマネージャー
- [ArgoCD](https://argo-cd.readthedocs.io/) - GitOps継続的デリバリー
- [Flux](https://fluxcd.io/) - GitOps ツールキット
- [Lens](https://k8slens.dev/) - K8s IDE
- [k9s](https://k9scli.io/) - ターミナルベースK8s管理

### 監視・ログ
- [Prometheus](https://prometheus.io/) - モニタリング
- [Grafana](https://grafana.com/) - 可視化
- [ELK Stack](https://www.elastic.co/elk-stack) - ログ管理
- [Loki](https://grafana.com/oss/loki/) - ログ集約

### ベストプラクティス
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [12 Factor App](https://12factor.net/)
- [Production Best Practices](https://learnk8s.io/production-best-practices)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
