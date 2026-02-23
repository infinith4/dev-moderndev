# Litmus

## 概要

Litmusは、CNCFインキュベーティングプロジェクトのKubernetesネイティブなカオスエンジニアリングプラットフォームです。ChaosHub経由で提供される豊富なカオス実験（Pod削除、ネットワーク遅延、CPU負荷、ディスクI/O等）をKubernetesクラスタ上で実行し、システムの耐障害性を検証します。ChaosCenter（Webダッシュボード）で実験の作成・スケジューリング・結果分析を一元管理でき、GitOpsモードによるカオス実験のバージョン管理にも対応しています。

## 主な機能

### 1. カオス実験

- **Pod Chaos**: Pod削除、コンテナキル、Pod I/Oストレス
- **Network Chaos**: ネットワーク遅延、パケットロス、DNS障害
- **Node Chaos**: ノードドレイン、ノードCPU/メモリ負荷、ノードリスタート
- **Stress Chaos**: CPU/メモリ/ディスクI/Oストレス注入
- **AWS/GCP/Azure Chaos**: クラウドリソース（EC2、VM等）の障害注入

### 2. ChaosCenter

- **Webダッシュボード**: カオス実験の作成・管理・モニタリング
- **ワークフロー**: 複数の実験を組み合わせたカオスシナリオ定義
- **スケジューリング**: Cron式による定期的なカオス実験実行
- **チーム管理**: マルチテナント対応のプロジェクト・ユーザー管理
- **レジリエンススコア**: 実験結果に基づくシステム耐障害性スコア

### 3. ChaosHub

- **実験カタログ**: 50以上のカオス実験テンプレート
- **カスタムHub**: 独自の実験テンプレートリポジトリ
- **バージョン管理**: Git連携による実験定義の管理

### 4. GitOps対応

- **ChaosEngine CR**: KubernetesカスタムリソースでカオスExperimentを定義
- **宣言的管理**: YAML定義によるカオス実験のGitOps運用
- **ArgoCD/Flux連携**: GitOpsツールとの統合

## 利用方法

### インストール

```bash
# Helmによるインストール
helm repo add litmuschaos https://litmuschaos.github.io/litmus-helm/
helm repo update

# Litmus 3.x（ChaosCenter込み）のインストール
helm install litmus litmuschaos/litmus \
  --namespace litmus --create-namespace

# ChaosCenter UIへのアクセス（デフォルト: admin/litmus）
kubectl port-forward svc/litmusportal-frontend-service -n litmus 9091:9091

# kubectl によるインストール
kubectl apply -f https://litmuschaos.github.io/litmus/3.0.0/litmus-3.0.0.yaml
```

### カオス実験の定義（ChaosEngine CR）

```yaml
# pod-delete-experiment.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: default
spec:
  engineState: active
  appinfo:
    appns: default
    applabel: app=nginx
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "30"
            - name: CHAOS_INTERVAL
              value: "10"
            - name: FORCE
              value: "false"
```

```bash
# 実験の実行
kubectl apply -f pod-delete-experiment.yaml

# 結果の確認
kubectl get chaosresult nginx-chaos-pod-delete -n default -o yaml
```

### ネットワーク遅延実験

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: network-chaos
  namespace: default
spec:
  engineState: active
  appinfo:
    appns: default
    applabel: app=myapp
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-network-latency
      spec:
        components:
          env:
            - name: NETWORK_LATENCY
              value: "200"
            - name: TOTAL_CHAOS_DURATION
              value: "60"
            - name: NETWORK_INTERFACE
              value: "eth0"
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/chaos-test.yml
name: Litmus Chaos Test

on:
  schedule:
    - cron: '0 2 * * 1'

jobs:
  chaos:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v4
      - name: Apply Chaos Experiment
        run: kubectl apply -f chaos-experiments/
      - name: Wait for Completion
        run: |
          sleep 120
          kubectl get chaosresult -n default -o json | jq '.items[].status.experimentStatus.verdict'
      - name: Verify Resilience Score
        run: |
          VERDICT=$(kubectl get chaosresult -n default -o jsonpath='{.items[0].status.experimentStatus.verdict}')
          if [ "$VERDICT" != "Pass" ]; then exit 1; fi
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Litmus（OSS）** | 無料 | Apache License 2.0、CNCFインキュベーティング |
| **Harness Chaos Engineering** | 有料 | エンタープライズサポート、SaaS版ChaosCenter |

## メリット

1. **CNCFプロジェクト**: CNCFインキュベーティングプロジェクトとしてコミュニティが活発
2. **Kubernetesネイティブ**: CRDベースでKubernetesの運用に自然に統合
3. **ChaosCenter**: WebUIで実験の管理・可視化が容易
4. **豊富な実験**: ChaosHubで50以上のカオス実験テンプレートを提供
5. **GitOps対応**: YAML定義による宣言的なカオス実験管理
6. **マルチクラウド**: AWS、GCP、Azure等のクラウドリソース障害注入に対応
7. **レジリエンススコア**: 定量的なシステム耐障害性評価

## デメリット

1. **Kubernetes専用**: Kubernetes以外の環境には非対応
2. **学習コスト**: ChaosEngine、ChaosExperiment等のCRD概念の理解が必要
3. **リソース消費**: ChaosCenterの常駐コンポーネントがクラスタリソースを消費
4. **実験設計**: 効果的なカオス実験のシナリオ設計にはSRE知識が必要
5. **本番適用リスク**: 不適切な設定で本番サービスに影響を与える可能性

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Chaos Mesh** | CNCFインキュベーティング | Litmusと同等のK8sカオスエンジニアリング、Dashboard内蔵 |
| **Gremlin** | 商用カオスプラットフォーム | Litmusよりエンタープライズ向け、SaaS提供 |
| **AWS Fault Injection Service** | AWSネイティブ | AWS環境専用、マネージドサービス |
| **Chaos Toolkit** | 汎用カオスツール | K8s以外も対応、Python拡張可能 |

## 公式リンク

- **公式サイト**: [https://litmuschaos.io/](https://litmuschaos.io/)
- **ドキュメント**: [https://docs.litmuschaos.io/](https://docs.litmuschaos.io/)
- **GitHub**: [https://github.com/litmuschaos/litmus](https://github.com/litmuschaos/litmus)
- **ChaosHub**: [https://hub.litmuschaos.io/](https://hub.litmuschaos.io/)
- **CNCF**: [https://www.cncf.io/projects/litmus/](https://www.cncf.io/projects/litmus/)

## 関連ドキュメント

- [Chaos Mesh](./Chaos_Mesh.md)

---

**カテゴリ**: テスト
**対象工程**: テスト・運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
