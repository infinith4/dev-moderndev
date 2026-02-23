# Rancher

## 概要

Rancher は、SUSE が提供するオープンソースの Kubernetes 管理プラットフォームです。複数の Kubernetes クラスタを統合的に管理し、マルチクラスタ、マルチクラウド環境での運用を簡素化します。Web UI による直感的な操作、認証・認可、モニタリング、カタログアプリケーションのデプロイなど、エンタープライズ環境に必要な機能を包括的に提供します。

## 主な特徴

### 1. マルチクラスタ管理
- 単一の UI から複数の Kubernetes クラスタを管理
- オンプレミス、パブリッククラウド、エッジ環境に対応
- クラスタのプロビジョニング、アップグレード、削除
- 一元的なモニタリングとアラート

### 2. Kubernetes ディストリビューションの選択
- RKE (Rancher Kubernetes Engine)
- RKE2 (セキュリティ強化版)
- K3s (軽量版)
- 既存の EKS、GKE、AKS クラスタのインポート

### 3. 統合認証とアクセス制御
- Active Directory、LDAP、SAML、OAuth 統合
- ロールベースアクセス制御（RBAC）
- プロジェクトとネームスペースの階層管理
- マルチテナント対応

### 4. アプリケーションカタログ
- Helm チャートカタログ
- カスタムカタログの追加
- アプリケーションのバージョン管理
- ワンクリックデプロイ

### 5. 統合モニタリング
- Prometheus + Grafana の統合
- クラスタ、ノード、Pod レベルのメトリクス
- カスタムダッシュボード
- アラート管理

## 主な機能

### クラスタ管理機能

| 機能 | 説明 |
|------|------|
| クラスタプロビジョニング | AWS、Azure、GCP、vSphere等へのクラスタ作成 |
| クラスタインポート | 既存クラスタの Rancher への取り込み |
| クラスタアップグレード | Kubernetes バージョンのアップグレード |
| ノード管理 | ノードの追加、削除、ラベリング |
| バックアップ/リストア | etcd のバックアップとリストア |

### アプリケーション管理

| 機能 | 説明 |
|------|------|
| Workload 管理 | Deployment、StatefulSet、DaemonSet 管理 |
| Service Discovery | Service、Ingress の管理 |
| ConfigMap/Secret | 設定とシークレットの管理 |
| ストレージ管理 | PV、PVC、StorageClass の管理 |
| ネットワークポリシー | ネットワークセキュリティルール |

### セキュリティ機能

| 機能 | 説明 |
|------|------|
| RBAC | きめ細かなアクセス制御 |
| Pod Security Policies | Pod セキュリティポリシー管理 |
| ネットワークポリシー | トラフィック制御 |
| イメージスキャン | 脆弱性スキャン（Trivy統合） |
| 監査ログ | 操作ログの記録 |

## アーキテクチャ

### Rancher アーキテクチャ

```
┌─────────────────────────────────────────┐
│         Rancher Management Server       │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │   API    │  │   UI     │  │ Auth  │ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Cluster A│  │ Cluster B│  │ Cluster C│
│  (RKE2)  │  │  (K3s)   │  │  (EKS)   │
└──────────┘  └──────────┘  └──────────┘
```

### コンポーネント

- **Rancher Server**: 管理サーバー（中央コントロールプレーン）
- **Cluster Agent**: 各クラスタにデプロイされるエージェント
- **Node Agent**: 各ノードで動作するエージェント
- **Authentication Proxy**: 認証プロキシ

## インストールとセットアップ

### Rancher のインストール方法

#### 1. Docker による単一ノードインストール（開発/テスト用）

```bash
# Rancher サーバーの起動
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:latest

# アクセス
https://<SERVER_IP>

# 初期パスワードの取得
docker logs <container_id> 2>&1 | grep "Bootstrap Password:"
```

#### 2. Helm による本番環境インストール

```bash
# 前提: 既存の Kubernetes クラスタ

# Helm リポジトリの追加
helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
helm repo update

# cert-manager のインストール（証明書管理）
kubectl create namespace cattle-system
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.crds.yaml

helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.3

# Rancher のインストール
helm install rancher rancher-latest/rancher \
  --namespace cattle-system \
  --set hostname=rancher.example.com \
  --set bootstrapPassword=admin \
  --set ingress.tls.source=letsEncrypt \
  --set letsEncrypt.email=admin@example.com

# インストール確認
kubectl -n cattle-system rollout status deploy/rancher
kubectl -n cattle-system get deploy rancher
```

#### 3. RKE2 による高可用性インストール

```bash
# 3台のサーバーノードで HA 構成

# 最初のサーバーノード
curl -sfL https://get.rke2.io | sh -
systemctl enable rke2-server.service
systemctl start rke2-server.service

# トークンの取得
cat /var/lib/rancher/rke2/server/node-token

# 2台目、3台目のサーバーノード
curl -sfL https://get.rke2.io | sh -

mkdir -p /etc/rancher/rke2
cat > /etc/rancher/rke2/config.yaml <<EOF
server: https://<FIRST_SERVER_IP>:9345
token: <TOKEN>
EOF

systemctl enable rke2-server.service
systemctl start rke2-server.service

# Rancher を Helm でインストール（上記手順参照）
```

### 初期セットアップ

```
1. ブラウザで Rancher UI にアクセス
   https://rancher.example.com

2. 初期パスワードを入力

3. 新しいパスワードを設定

4. サーバー URL を確認

5. 利用規約に同意

6. ダッシュボードが表示される
```

## 基本的な使い方

### 1. クラスタの作成

#### カスタムクラスタ（RKE2）

```
1. Rancher UI で「Cluster Management」を選択
2. 「Create」をクリック
3. 「Custom」を選択
4. クラスタ名を入力
5. Kubernetes バージョンを選択
6. ノード登録コマンドをコピー
7. 各ノードで登録コマンドを実行

# ノード登録コマンド例
sudo docker run -d --privileged --restart=unless-stopped \
  --net=host -v /etc/kubernetes:/etc/kubernetes \
  -v /var/run:/var/run rancher/rancher-agent:v2.7.0 \
  --server https://rancher.example.com \
  --token <TOKEN> \
  --ca-checksum <CHECKSUM> \
  --etcd --controlplane --worker
```

#### クラウドプロバイダークラスタ（AWS EKS）

```
1. 「Create」→「Amazon EKS」を選択
2. AWS 認証情報を設定
   - Access Key
   - Secret Key
   - Region
3. クラスタ設定
   - クラスタ名
   - Kubernetes バージョン
   - VPC、サブネット
4. ノードグループ設定
   - インスタンスタイプ
   - ノード数（min/max/desired）
5. 「Create」をクリック
```

### 2. 既存クラスタのインポート

```bash
# 既存の EKS、GKE、AKS クラスタをインポート

1. Rancher UI で「Import Existing」を選択
2. クラスタ名を入力
3. インポートコマンドが表示される
4. kubectl で実行

# インポートコマンド例
kubectl apply -f https://rancher.example.com/v3/import/<CLUSTER_ID>.yaml

# インポート確認
# Rancher UI でクラスタが表示される
```

### 3. アプリケーションのデプロイ

#### Helm チャートからデプロイ

```
1. クラスタを選択
2. 「Apps & Marketplace」を選択
3. 「Charts」からアプリを検索（例: Nginx）
4. インストールをクリック
5. 設定値を入力
   - ネームスペース
   - レプリカ数
   - リソース制限
6. 「Install」をクリック
```

#### Workload の作成（GUI）

```
1. クラスタ → プロジェクト → Workloads を選択
2. 「Create」→「Deployment」を選択
3. 基本情報
   - 名前: nginx-app
   - コンテナイメージ: nginx:latest
   - レプリカ数: 3
4. ポート設定
   - コンテナポート: 80
5. リソース制限
   - CPU: 100m
   - Memory: 128Mi
6. 「Launch」をクリック
```

### 4. Service と Ingress の設定

#### Service の作成

```
1. Workloads → Service Discovery → Services
2. 「Create」をクリック
3. 設定
   - 名前: nginx-service
   - ターゲット Workload: nginx-app
   - ポートマッピング: 80 → 80
   - タイプ: ClusterIP
4. 「Save」をクリック
```

#### Ingress の作成

```
1. Service Discovery → Ingresses
2. 「Create」をクリック
3. 設定
   - 名前: nginx-ingress
   - ホスト: nginx.example.com
   - パス: /
   - ターゲット Service: nginx-service
   - ポート: 80
4. TLS 設定（オプション）
   - Secret を選択
5. 「Save」をクリック
```

## ユーザーとアクセス管理

### ユーザーの追加

```
1. 右上のユーザーアイコン → Users & Authentication
2. 「Users」タブ → 「Create」
3. ユーザー情報
   - Username
   - Password
   - Display Name
4. Global Permissions（グローバル権限）
   - Administrator
   - Standard User
   - User-Base（制限付きユーザー）
5. 「Create」をクリック
```

### プロジェクトとロール

```
# プロジェクトの作成
1. クラスタ → Projects/Namespaces
2. 「Create Project」をクリック
3. プロジェクト名を入力
4. メンバーを追加
   - Owner: 完全な権限
   - Member: 読み書き権限
   - Read Only: 読み取り専用
5. 「Create」をクリック

# ロールの種類
- Cluster Owner: クラスタ全体の管理
- Cluster Member: クラスタ内のリソース操作
- Project Owner: プロジェクト管理
- Project Member: プロジェクト内のリソース操作
- Read Only: 読み取り専用
```

### 認証プロバイダーの設定

#### Active Directory 統合

```
1. Security → Authentication
2. 「Active Directory」を選択
3. 設定
   - Server: ldap.example.com
   - Port: 389 (LDAP) / 636 (LDAPS)
   - Service Account: CN=rancher,OU=users,DC=example,DC=com
   - Password: <パスワード>
   - User Search Base: OU=users,DC=example,DC=com
   - Group Search Base: OU=groups,DC=example,DC=com
4. 「Authenticate」でテスト
5. 「Enable」をクリック
```

## モニタリングとロギング

### モニタリングの有効化

```
1. クラスタ → Monitoring
2. 「Enable Monitoring」をクリック
3. 設定
   - Prometheus Retention: 12h
   - Storage: 50Gi
   - Resource Limits
4. 「Enable」をクリック

# Grafana ダッシュボードにアクセス
1. Cluster Tools → Monitoring
2. 「Grafana」をクリック
```

### カスタムダッシュボード

```yaml
# custom-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-dashboard
  namespace: cattle-monitoring-system
  labels:
    grafana_dashboard: "1"
data:
  custom-dashboard.json: |
    {
      "dashboard": {
        "title": "Custom Dashboard",
        "panels": [
          {
            "type": "graph",
            "title": "CPU Usage",
            "targets": [
              {
                "expr": "sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)"
              }
            ]
          }
        ]
      }
    }
```

### ロギングの設定

```
1. クラスタ → Logging
2. 「Enable Logging」をクリック
3. 出力先の選択
   - Elasticsearch
   - Splunk
   - Kafka
   - Fluentd
   - Syslog
4. 出力先の設定
   - Elasticsearch の場合:
     - Endpoint: http://elasticsearch:9200
     - Index Pattern: rancher-logs
5. 「Enable」をクリック
```

## バックアップとリストア

### etcd バックアップ

```bash
# Rancher UI からのバックアップ
1. クラスタ → Snapshots
2. 「Take Snapshot」をクリック
3. スナップショット名を入力
4. 「Save」をクリック

# 定期バックアップの設定
1. クラスタ → Edit Config
2. 「Advanced」→「etcd」
3. バックアップ設定
   - Interval Hours: 12
   - Retention: 6
   - S3 Backup（オプション）
     - Bucket Name
     - Region
     - Access Key / Secret Key
4. 「Save」をクリック
```

### クラスタのリストア

```bash
# スナップショットからのリストア
1. クラスタ → Snapshots
2. リストアしたいスナップショットを選択
3. 「Restore」をクリック
4. 確認してリストアを実行

# CLI からのリストア（RKE2）
rke2 server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/rke2/server/db/snapshots/snapshot.db
```

## CI/CD 統合

### Fleet（GitOps）

```yaml
# fleet.yaml
defaultNamespace: default

helm:
  chart: nginx
  repo: https://charts.bitnami.com/bitnami
  version: 13.2.0
  values:
    replicaCount: 3
    service:
      type: LoadBalancer

# Git リポジトリの登録
1. Continuous Delivery → Git Repos
2. 「Create」をクリック
3. 設定
   - Name: my-apps
   - Repository URL: https://github.com/user/fleet-apps
   - Branch: main
   - Paths: charts/*
4. ターゲットクラスタを選択
5. 「Create」をクリック
```

### Rancher CLI

```bash
# Rancher CLI のインストール
# GitHub releases からダウンロード
wget https://github.com/rancher/cli/releases/download/v2.7.0/rancher-linux-amd64-v2.7.0.tar.gz
tar -xzf rancher-linux-amd64-v2.7.0.tar.gz
sudo mv rancher-v2.7.0/rancher /usr/local/bin/

# ログイン
rancher login https://rancher.example.com --token <API_TOKEN>

# クラスタの一覧
rancher clusters ls

# コンテキストの切り替え
rancher context switch

# kubectl コマンドの実行
rancher kubectl get nodes
rancher kubectl get pods --all-namespaces
```

## トラブルシューティング

### よくある問題と解決策

#### 1. Rancher Server にアクセスできない

```bash
# コンテナの状態確認
docker ps -a | grep rancher
docker logs <container_id>

# ポートの確認
netstat -tuln | grep -E '80|443'

# ファイアウォールの確認
sudo firewall-cmd --list-all
```

#### 2. クラスタエージェントが接続できない

```bash
# エージェント Pod の確認
kubectl -n cattle-system get pods

# ログの確認
kubectl -n cattle-system logs -l app=cattle-cluster-agent

# ネットワーク接続の確認
curl -k https://rancher.example.com/ping
```

#### 3. ノードが NotReady 状態

```bash
# ノードの詳細確認
kubectl describe node <node-name>

# kubelet ログの確認
journalctl -u kubelet -f

# Docker/containerd の確認
systemctl status docker
systemctl status containerd
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://www.rancher.com/
- ドキュメント: https://rancher.com/docs/
- GitHub: https://github.com/rancher/rancher

### コミュニティ
- Slack: https://slack.rancher.io/
- フォーラム: https://forums.rancher.com/
- YouTube: https://www.youtube.com/c/Rancher

### トレーニング
- Academy: https://academy.rancher.com/
- Certification: https://www.rancher.com/training-certification

## まとめ

Rancher は、以下の場面で特に有用です:

1. **マルチクラスタ管理** - 複数の Kubernetes クラスタを統一的に管理
2. **マルチクラウド運用** - AWS、Azure、GCP、オンプレミスの混在環境
3. **エンタープライズセキュリティ** - RBAC、認証統合、ポリシー管理
4. **運用の簡素化** - GUI による直感的な操作、アプリカタログ

Kubernetes の複雑さを抽象化し、エンタープライズグレードの管理機能を提供することで、大規模な Kubernetes 環境の運用を効率化します。
