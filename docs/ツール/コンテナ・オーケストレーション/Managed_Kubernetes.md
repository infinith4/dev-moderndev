# Amazon EKS / Azure AKS

## 概要

**Amazon EKS（Elastic Kubernetes Service）**と**Azure AKS（Azure Kubernetes Service）**は、クラウドプロバイダーが提供するマネージドKubernetesサービスです。コントロールプレーンの管理を自動化し、Kubernetesクラスタの運用負荷を大幅に削減します。

## 基本情報

### Amazon EKS

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | マネージドKubernetesサービス |
| **ライセンス** | プロプライエタリ（Kubernetes自体はOSS） |
| **料金** | 🟡 一部無料（コントロールプレーン: $0.10/時間、ワーカーノード別途） |
| **公式サイト** | https://aws.amazon.com/eks/ |
| **ドキュメント** | https://docs.aws.amazon.com/eks/ |

### Azure AKS

| 項目 | 内容 |
|------|------|
| **開発元** | Microsoft Azure |
| **種別** | マネージドKubernetesサービス |
| **ライセンス** | プロプライエタリ（Kubernetes自体はOSS） |
| **料金** | 🟡 一部無料（コントロールプレーン無料、ワーカーノード別途、Uptime SLA有料） |
| **公式サイト** | https://azure.microsoft.com/services/kubernetes-service/ |
| **ドキュメント** | https://docs.microsoft.com/azure/aks/ |

## 主な特徴

### Amazon EKS

#### 1. AWS統合
- **ELB/ALB**: Kubernetesサービスとの自動統合
- **IAM**: KubernetesのRBACとIAMの統合認証
- **ECR**: プライベートコンテナレジストリ連携
- **VPC**: ネットワークセキュリティ統合

#### 2. マネージドノードグループ
- 自動スケーリング（Cluster Autoscaler）
- マネージドノードアップデート
- EC2 Spot Instancesサポート

#### 3. Fargate統合
- サーバーレスコンテナ実行
- ノード管理不要

### Azure AKS

#### 1. Azure統合
- **Azure Load Balancer**: 自動ロードバランサー作成
- **Azure AD**: Azure ADとの統合認証
- **ACR**: Azure Container Registry連携
- **Azure Monitor**: 統合監視

#### 2. ノードプール管理
- 複数ノードプール（システム/ユーザー）
- 自動スケーリング
- Spot VMサポート

#### 3. 無料コントロールプレーン
- コントロールプレーン料金無料（AWSより低コスト）
- Uptime SLA（99.95%）はオプション有料

## 使い方

### Amazon EKS

#### クラスタ作成（eksctl使用）

```bash
# eksctlのインストール
brew install eksctl  # macOS
# または
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# クラスタ作成
eksctl create cluster \
  --name my-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4 \
  --managed
```

#### クラスタ設定ファイル（cluster.yaml）

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: production-cluster
  region: ap-northeast-1
  version: "1.28"

vpc:
  cidr: 10.0.0.0/16
  nat:
    gateway: Single

iam:
  withOIDC: true
  serviceAccounts:
    - metadata:
        name: aws-load-balancer-controller
        namespace: kube-system
      wellKnownPolicies:
        awsLoadBalancerController: true

managedNodeGroups:
  - name: ng-1
    instanceType: t3.medium
    desiredCapacity: 3
    minSize: 1
    maxSize: 5
    volumeSize: 20
    ssh:
      allow: true
      publicKeyName: my-key
    labels:
      role: worker
    tags:
      nodegroup-role: worker
    iam:
      withAddonPolicies:
        ebs: true
        fsx: true
        efs: true

addons:
  - name: vpc-cni
  - name: coredns
  - name: kube-proxy
```

```bash
# 設定ファイルからクラスタ作成
eksctl create cluster -f cluster.yaml
```

#### kubectlでの操作

```bash
# kubeconfig更新
aws eks update-kubeconfig --region ap-northeast-1 --name production-cluster

# ノード確認
kubectl get nodes

# サンプルアプリケーションデプロイ
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# LoadBalancer確認
kubectl get svc nginx
```

### Azure AKS

#### クラスタ作成（Azure CLI使用）

```bash
# Azure CLIインストール
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Azureログイン
az login

# リソースグループ作成
az group create --name myResourceGroup --location japaneast

# AKSクラスタ作成
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-managed-identity \
  --generate-ssh-keys \
  --network-plugin azure \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5
```

#### Bicepテンプレート（aks.bicep）

```bicep
param clusterName string = 'myAKSCluster'
param location string = resourceGroup().location
param dnsPrefix string = 'myaks'
param kubernetesVersion string = '1.28.3'

resource aks 'Microsoft.ContainerService/managedClusters@2023-09-01' = {
  name: clusterName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: dnsPrefix
    kubernetesVersion: kubernetesVersion
    enableRBAC: true
    aadProfile: {
      managed: true
      enableAzureRBAC: true
    }
    agentPoolProfiles: [
      {
        name: 'systempool'
        count: 3
        vmSize: 'Standard_D2s_v3'
        mode: 'System'
        osType: 'Linux'
        osSKU: 'Ubuntu'
        enableAutoScaling: true
        minCount: 1
        maxCount: 5
      }
      {
        name: 'userpool'
        count: 2
        vmSize: 'Standard_D4s_v3'
        mode: 'User'
        osType: 'Linux'
        enableAutoScaling: true
        minCount: 1
        maxCount: 10
      }
    ]
    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'azure'
      loadBalancerSku: 'standard'
    }
    addonProfiles: {
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: logAnalyticsWorkspace.id
        }
      }
      azurePolicy: {
        enabled: true
      }
    }
  }
}

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: '${clusterName}-logs'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

output controlPlaneFQDN string = aks.properties.fqdn
```

```bash
# Bicepでデプロイ
az deployment group create \
  --resource-group myResourceGroup \
  --template-file aks.bicep
```

#### kubectlでの操作

```bash
# kubeconfig取得
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# ノード確認
kubectl get nodes

# アプリケーションデプロイ
kubectl apply -f https://k8s.io/examples/application/deployment.yaml

# Azure Load Balancerでサービス公開
kubectl expose deployment nginx-deployment --type=LoadBalancer --port=80
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **インフラ構築** | Kubernetesクラスタ構築 | 本番環境・ステージング環境構築 |
| **テスト** | コンテナ化アプリケーションテスト | 統合テスト・E2Eテスト環境 |
| **導入** | コンテナオーケストレーション | アプリケーションデプロイ・スケーリング |

## メリット

### 共通メリット
- **コントロールプレーン管理不要**: アップグレード・パッチ適用が自動化
- **高可用性**: マルチAZ構成でコントロールプレーンを冗長化
- **スケーラビリティ**: 自動スケーリング対応
- **クラウドサービス統合**: ロードバランサー・ストレージ・監視との統合
- **セキュリティ**: IAM/Azure AD統合、ネットワークポリシー

### Amazon EKS固有
- **Fargate統合**: サーバーレスコンテナ実行
- **EC2 Spot Instances**: コスト削減
- **AWS豊富なサービス統合**: 200+サービスとの連携

### Azure AKS固有
- **無料コントロールプレーン**: EKSより低コスト
- **Azure AD統合**: エンタープライズ認証
- **Azure Monitor統合**: Container Insightsで詳細監視

## デメリット

### 共通デメリット
- **ベンダーロックイン**: クラウド固有機能への依存
- **学習曲線**: Kubernetes + クラウド固有機能の習得が必要
- **ワーカーノードコスト**: 最小構成でも月数万円のコスト
- **複雑性**: 小規模アプリケーションにはオーバーエンジニアリング

### Amazon EKS固有
- **コントロールプレーン有料**: $0.10/時間（約$73/月）
- **VPC CNIの複雑性**: IPアドレス管理が複雑

### Azure AKS固有
- **Uptime SLA有料**: 99.95% SLAには追加料金
- **Azure固有の制約**: 一部Kubernetes機能に制限

## 類似ツールとの比較

| サービス | 料金 | 特徴 | 適用場面 |
|---------|------|------|----------|
| **Amazon EKS** | コントロールプレーン有料 | AWS統合、Fargate | AWS環境 |
| **Azure AKS** | コントロールプレーン無料 | Azure AD統合、低コスト | Azure環境 |
| **Google GKE** | コントロールプレーン無料 | Autopilot機能 | GCP環境 |
| **自前Kubernetes** | インフラコストのみ | 完全制御 | オンプレミス・マルチクラウド |

## ベストプラクティス

### 1. ノードグループの分離

```yaml
# EKS例: システムとアプリケーションでノードグループを分離
managedNodeGroups:
  - name: system-nodes
    instanceType: t3.small
    labels:
      workload-type: system
    taints:
      - key: CriticalAddonsOnly
        value: "true"
        effect: NoSchedule

  - name: app-nodes
    instanceType: t3.medium
    labels:
      workload-type: application
```

### 2. オートスケーリングの設定

```bash
# AKS例: Cluster Autoscaler有効化
az aks update \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --enable-cluster-autoscaler \
  --min-count 3 \
  --max-count 10
```

### 3. コスト最適化

```yaml
# Spot Instancesの活用（EKS）
managedNodeGroups:
  - name: spot-nodes
    instanceTypes:
      - t3.medium
      - t3a.medium
    spot: true
    minSize: 0
    maxSize: 10
```

### 4. 監視とロギング

```bash
# EKS: CloudWatch Container Insights有効化
eksctl utils update-cluster-logging \
  --enable-types all \
  --region ap-northeast-1 \
  --cluster production-cluster

# AKS: Azure Monitor有効化済み（addonProfilesで設定）
```

## 公式リソース

### Amazon EKS
- **公式サイト**: https://aws.amazon.com/eks/
- **ドキュメント**: https://docs.aws.amazon.com/eks/
- **ベストプラクティス**: https://aws.github.io/aws-eks-best-practices/
- **eksctl**: https://eksctl.io/

### Azure AKS
- **公式サイト**: https://azure.microsoft.com/services/kubernetes-service/
- **ドキュメント**: https://docs.microsoft.com/azure/aks/
- **ベストプラクティス**: https://docs.microsoft.com/azure/aks/best-practices
- **Azure CLI**: https://docs.microsoft.com/cli/azure/aks

## まとめ

Amazon EKSとAzure AKSは、Kubernetesの運用負荷を大幅に削減するマネージドサービスです。EKSはAWS統合とFargateサポートが強み、AKSは無料コントロールプレーンとAzure AD統合が魅力です。クラウド環境に応じて選択し、コンテナオーケストレーションの複雑性を抽象化することで、アプリケーション開発に集中できます。

---

**最終更新**: 2025-12-06
**対象バージョン**: EKS 1.28+ / AKS 1.28+
