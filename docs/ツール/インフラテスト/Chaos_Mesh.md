# Chaos Mesh

## 概要

Chaos Meshは、Kubernetes環境向けのオープンソースカオスエンジニアリングプラットフォームである。CNCFインキュベーティングプロジェクトとして、Kubernetes Custom Resource Definitions（CRD）を活用した宣言的な障害注入実験を提供する。Pod障害、ネットワーク遅延・パケットロス、I/Oフォールトインジェクション、DNS障害、ストレステスト等の多様な障害シナリオをYAMLマニフェストで定義し、Webダッシュボードによる実験管理と結果の可視化を実現する。本番環境に近い条件下でシステムの耐障害性を検証し、信頼性向上に寄与する。

## 主な機能

### 1. Pod障害注入
- **Pod Kill**: 指定PodのコンテナをKill
- **Pod Failure**: Podを一定時間利用不可に設定
- **Container Kill**: 特定コンテナのプロセス停止
- **Pod Chaos**: ラベルセレクタによる対象Pod選択

### 2. ネットワーク障害注入
- **Delay**: ネットワーク遅延の追加（レイテンシ注入）
- **Loss**: パケットロスの発生
- **Duplicate**: パケット重複の発生
- **Corrupt**: パケット破損の注入
- **Partition**: ネットワーク分断の発生
- **Bandwidth**: 帯域制限の設定

### 3. I/O障害注入
- **Latency**: ファイルシステム操作への遅延注入
- **Fault**: I/Oエラーの発生（errno指定）
- **AttrOverride**: ファイル属性の書き換え
- **対象指定**: パス、メソッド（read/write/open等）で対象操作を絞込

### 4. ストレステスト
- **CPU Stress**: CPU負荷の注入（コア数・負荷率指定）
- **Memory Stress**: メモリ消費の注入（サイズ指定）
- **対象指定**: 特定コンテナ・Pod への限定適用

### 5. DNS障害
- **DNS Error**: DNS解決エラーの注入
- **DNS Random**: ランダムなDNS応答の返却
- **パターン指定**: ドメイン名パターンでフィルタリング

### 6. 時刻障害
- **Time Skew**: コンテナ内の時刻をオフセット
- **対象プロセス**: 特定プロセスへの時刻変更適用

### 7. Webダッシュボード
- **実験管理**: GUI上で障害実験の作成・開始・停止
- **ワークフロー**: 複数の障害実験を順次・並列実行
- **スケジュール**: Cron形式での定期実行設定
- **イベント表示**: 実験の実行状態・結果の可視化

## 利用方法

### インストール（Helm）

```bash
# Helm リポジトリ追加
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm repo update

# Chaos Mesh インストール
kubectl create namespace chaos-mesh
helm install chaos-mesh chaos-mesh/chaos-mesh \
  --namespace chaos-mesh \
  --set chaosDaemon.runtime=containerd \
  --set chaosDaemon.socketPath=/run/containerd/containerd.sock \
  --version 2.7.0

# インストール確認
kubectl get pods -n chaos-mesh
```

### Pod Kill 実験

```yaml
# pod-kill.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-example
  namespace: default
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces:
      - default
    labelSelectors:
      app: my-application
  duration: "30s"
  gracePeriod: 0
```

```bash
# 実験の適用
kubectl apply -f pod-kill.yaml

# 実験状態の確認
kubectl get podchaos -n default

# 実験の削除（障害停止）
kubectl delete -f pod-kill.yaml
```

### ネットワーク遅延注入

```yaml
# network-delay.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-example
  namespace: default
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - default
    labelSelectors:
      app: my-application
  delay:
    latency: "200ms"
    jitter: "50ms"
    correlation: "25"
  direction: to
  target:
    selector:
      namespaces:
        - default
      labelSelectors:
        app: database
    mode: all
  duration: "5m"
```

### I/Oフォールトインジェクション

```yaml
# io-fault.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: IOChaos
metadata:
  name: io-fault-example
  namespace: default
spec:
  action: fault
  mode: one
  selector:
    namespaces:
      - default
    labelSelectors:
      app: my-application
  volumePath: /data
  path: "/data/**"
  errno: 5  # EIO
  percent: 50
  duration: "3m"
```

### CPU/メモリストレス

```yaml
# stress-test.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: cpu-stress-example
  namespace: default
spec:
  mode: one
  selector:
    namespaces:
      - default
    labelSelectors:
      app: my-application
  stressors:
    cpu:
      workers: 2
      load: 80
    memory:
      workers: 1
      size: "256MB"
  duration: "5m"
```

### ワークフロー定義

```yaml
# workflow.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: Workflow
metadata:
  name: chaos-workflow
  namespace: default
spec:
  entry: serial-chaos
  templates:
    - name: serial-chaos
      templateType: Serial
      children:
        - network-delay-step
        - pod-kill-step
    - name: network-delay-step
      templateType: NetworkChaos
      deadline: "5m"
      networkChaos:
        action: delay
        mode: one
        selector:
          labelSelectors:
            app: my-application
        delay:
          latency: "100ms"
        duration: "3m"
    - name: pod-kill-step
      templateType: PodChaos
      deadline: "2m"
      podChaos:
        action: pod-kill
        mode: one
        selector:
          labelSelectors:
            app: my-application
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/chaos-test.yml
name: Chaos Engineering Tests

on:
  schedule:
    - cron: '0 2 * * 1'  # 毎週月曜 AM2:00

jobs:
  chaos-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Kind cluster
        uses: helm/kind-action@v1
      - name: Install Chaos Mesh
        run: |
          helm repo add chaos-mesh https://charts.chaos-mesh.org
          helm install chaos-mesh chaos-mesh/chaos-mesh \
            --namespace chaos-mesh --create-namespace \
            --set chaosDaemon.runtime=containerd \
            --set chaosDaemon.socketPath=/run/containerd/containerd.sock
      - name: Deploy application
        run: kubectl apply -f k8s/
      - name: Run chaos experiments
        run: |
          kubectl apply -f chaos/network-delay.yaml
          sleep 180
          kubectl delete -f chaos/network-delay.yaml
      - name: Verify application health
        run: |
          kubectl get pods
          curl -sf http://localhost:8080/health || exit 1
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Chaos Mesh** | 無料 | オープンソース、Apache 2.0 License、CNCFインキュベーティングプロジェクト |

## メリット

1. **Kubernetes ネイティブ**: CRDベースで宣言的に障害実験を定義・管理できる
2. **豊富な障害タイプ**: Pod、ネットワーク、I/O、DNS、ストレス、時刻等の多様な障害注入に対応
3. **Webダッシュボード**: GUIで実験の作成・管理・監視が容易
4. **ワークフロー**: 複数の障害実験を組み合わせた複合シナリオを実行可能
5. **スコープ制御**: ラベルセレクタ・Namespaceで障害の影響範囲を厳密に制御
6. **CNCF公式**: CNCFインキュベーティングプロジェクトとして信頼性が高い
7. **GitOps対応**: YAMLマニフェストでバージョン管理・レビュー可能
8. **スケジュール実行**: 定期的なカオス実験の自動実行が可能
9. **権限管理**: RBAC連携で実験実行の権限制御が可能
10. **軽量**: サイドカー不要でオーバーヘッドが小さい

## デメリット

1. **Kubernetes限定**: Kubernetes環境でのみ利用可能で、VM・ベアメタルには非対応
2. **本番リスク**: 障害注入の設定ミスにより本番環境に影響を与える可能性がある
3. **学習コスト**: カオスエンジニアリングの原則とCRD仕様の理解が必要
4. **モニタリング依存**: 実験結果の評価には別途監視基盤（Prometheus等）が必要
5. **Namespace分離**: 実験スコープの設計を誤ると意図しないサービスに影響する
6. **デバッグ難度**: 障害注入が原因かアプリケーションバグかの切り分けが難しい場合がある
7. **ステートフルアプリ**: データベース等のステートフルワークロードへの障害注入には細心の注意が必要
8. **ダッシュボード制約**: 大規模クラスタでの実験履歴管理には外部ストレージ連携が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Litmus** | CNCFカオスエンジニアリング | Chaos Meshよりハブ（実験テンプレート）が充実 |
| **Gremlin** | SaaS型カオスエンジニアリング | Chaos Meshより機能豊富だが有料 |
| **Chaos Monkey** | Netflix製カオスツール | Chaos Meshより歴史が長いがK8s対応は限定的 |
| **AWS FIS** | AWSフォールトインジェクション | AWS環境特化だがマルチクラウド非対応 |
| **Pumba** | Docker向けカオスツール | Chaos MeshよりシンプルだがK8sネイティブでない |

## 公式リンク

- **公式サイト**: [https://chaos-mesh.org/](https://chaos-mesh.org/)
- **ドキュメント**: [https://chaos-mesh.org/docs/](https://chaos-mesh.org/docs/)
- **GitHub**: [https://github.com/chaos-mesh/chaos-mesh](https://github.com/chaos-mesh/chaos-mesh)
- **ダッシュボード**: [https://chaos-mesh.org/docs/manage-dashboard/](https://chaos-mesh.org/docs/manage-dashboard/)
- **CNCF**: [https://www.cncf.io/projects/chaos-mesh/](https://www.cncf.io/projects/chaos-mesh/)

## 関連ドキュメント

- [テストツール一覧](../テスト/)
- [Litmus](./Litmus.md)
- [Kubernetes](../IaCインフラ管理/Kubernetes.md)
- [Prometheus](../監視ロギング/Prometheus.md)
- [カオスエンジニアリングベストプラクティス](../../best-practices/chaos-engineering.md)

---

**カテゴリ**: テスト
**対象工程**: テスト・品質管理・運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
