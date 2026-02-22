# Istio

## 概要

Istioは、Kubernetesネイティブのサービスメッシュプラットフォームです。マイクロサービス間の通信を制御し、トラフィック管理、セキュリティ（mTLS）、可観測性（メトリクス、トレース、ログ）を提供します。Envoyサイドカープロキシ、VirtualService、DestinationRuleにより、アプリケーションコード変更なしでサービス間通信を高度に制御します。

## 主な機能

### 1. トラフィック管理
- **ルーティング**: A/Bテスト、カナリアデプロイ
- **負荷分散**: ラウンドロビン、重み付け
- **タイムアウト**: リクエストタイムアウト
- **リトライ**: 自動リトライ

### 2. セキュリティ
- **mTLS**: 相互TLS認証
- **認証**: JWT認証
- **認可**: RBAC

### 3. 可観測性
- **メトリクス**: Prometheus統合
- **トレース**: Jaeger統合
- **ログ**: アクセスログ

## 利用方法

### インストール

```bash
# Istioダウンロード
curl -L https://istio.io/downloadIstio | sh -

# Istioインストール
istioctl install --set profile=demo -y

# namespace有効化
kubectl label namespace default istio-injection=enabled
```

### VirtualService

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
```

### カナリアデプロイ

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - route:
    - destination:
        host: my-service
        subset: v1
      weight: 90
    - destination:
        host: my-service
        subset: v2
      weight: 10
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Istio** | 🟢 無料 | オープンソース、Apache License |

## メリット

1. **無料**: オープンソース
2. **トラフィック制御**: 高度なルーティング
3. **mTLS**: セキュア通信
4. **可観測性**: メトリクス、トレース
5. **Kubernetes統合**: K8sネイティブ

## デメリット

1. **複雑性**: 学習曲線steep
2. **リソース**: メモリ・CPU消費大
3. **デバッグ**: トラブルシュート難しい
4. **小規模**: 小規模環境にオーバースペック

## 公式リンク

- **公式サイト**: [https://istio.io/](https://istio.io/)
- **ドキュメント**: [https://istio.io/latest/docs/](https://istio.io/latest/docs/)

## 関連ドキュメント

- [サービスメッシュツール一覧](../サービスメッシュツール/)
- [Kubernetes](../オーケストレーションツール/Kubernetes.md)

---

**カテゴリ**: サービスメッシュツール  
**対象工程**: マイクロサービス運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
