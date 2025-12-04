# Kubernetes

## 概要

Kubernetes（K8s）は、オープンソースのコンテナオーケストレーションプラットフォームです。Dockerコンテナのデプロイ、スケーリング、管理を自動化し、Pod、Service、Deployment、StatefulSet等のリソースでマイクロサービスアーキテクチャを実現します。セルフヒーリング、ローリングアップデート、サービスディスカバリー、負荷分散により、本番環境でのコンテナ運用を支援します。

## 主な機能

### 1. コンテナオーケストレーション
- **Pod**: コンテナグループ
- **Deployment**: レプリカセット管理
- **Service**: ロードバランシング
- **StatefulSet**: ステートフルアプリ

### 2. スケーリング
- **水平スケーリング**: レプリカ数調整
- **自動スケーリング**: HPA（Horizontal Pod Autoscaler）
- **垂直スケーリング**: VPA（Vertical Pod Autoscaler）

### 3. セルフヒーリング
- **ヘルスチェック**: Liveness、Readiness Probe
- **自動再起動**: 障害Pod再起動
- **ノード障害**: Pod再配置

### 4. ストレージ
- **PersistentVolume**: 永続化ストレージ
- **StatefulSet**: ステートフル管理
- **ConfigMap/Secret**: 設定・機密情報

## 利用方法

### インストール（minikube）

```bash
# minikubeインストール（ローカルK8s）
brew install minikube

# クラスター起動
minikube start

# kubectl確認
kubectl version
```

### Deployment作成

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
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
        image: nginx:1.25
        ports:
        - containerPort: 80
```

```bash
# デプロイ
kubectl apply -f deployment.yaml

# 確認
kubectl get deployments
kubectl get pods
```

### Service作成

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
```

```bash
kubectl apply -f service.yaml
kubectl get services
```

### スケーリング

```bash
# 手動スケール
kubectl scale deployment nginx-deployment --replicas=5

# オートスケール
kubectl autoscale deployment nginx-deployment --min=2 --max=10 --cpu-percent=80
```

### ローリングアップデート

```bash
# イメージ更新
kubectl set image deployment/nginx-deployment nginx=nginx:1.26

# ロールアウト確認
kubectl rollout status deployment/nginx-deployment

# ロールバック
kubectl rollout undo deployment/nginx-deployment
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Kubernetes** | 🟢 完全無料 | オープンソース、Apache License |
| **EKS（AWS）** | 💰 $0.10/時間 | マネージドK8s |
| **GKE（GCP）** | 💰 $0.10/時間 | マネージドK8s |
| **AKS（Azure）** | 🟢 無料 | コントロールプレーン無料 |

## メリット

1. **オープンソース**: 完全無料
2. **標準**: コンテナオーケストレーション標準
3. **スケーラブル**: 大規模対応
4. **セルフヒーリング**: 自動復旧
5. **エコシステム**: 豊富なツール

## デメリット

1. **複雑性**: 学習曲線steep
2. **運用**: 運用負荷高い
3. **リソース**: メモリ・CPU消費大
4. **小規模**: 小規模環境にオーバースペック

## 公式リンク

- **公式サイト**: [https://kubernetes.io/](https://kubernetes.io/)
- **ドキュメント**: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)

## 関連ドキュメント

- [オーケストレーションツール一覧](../オーケストレーションツール/)
- [Docker](../コンテナツール/Docker.md)
- [Helm](./Helm.md)

---

**カテゴリ**: オーケストレーションツール  
**対象工程**: コンテナ運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
