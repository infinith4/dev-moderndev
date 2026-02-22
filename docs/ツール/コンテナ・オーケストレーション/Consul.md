# Consul

## 概要

Consulは、HashiCorp製のサービスメッシュ・サービスディスカバリツールです。サービス登録・検出、ヘルスチェック、分散Key-Valueストア、サービスメッシュ（サイドカープロキシ）により、マイクロサービスのサービスディスカバリー、構成管理、セキュアな通信を実現します。DNS、HTTP API、マルチデータセンター、Kubernetes統合で広く採用されています。

## 主な機能

### 1. サービスディスカバリ
- **サービス登録**: 自動登録
- **DNS**: DNSクエリ
- **HTTP API**: REST API
- **ヘルスチェック**: サービス監視

### 2. ヘルスチェック
- **HTTP**: HTTPエンドポイント
- **TCP**: TCP接続
- **Script**: カスタムスクリプト
- **TTL**: TTLベース

### 3. Key-Value ストア
- **分散KV**: 分散ストレージ
- **Watch**: 変更監視
- **セッション**: 分散ロック
- **ACL**: アクセス制御

### 4. サービスメッシュ
- **Connect**: mTLS通信
- **サイドカープロキシ**: Envoyプロキシ
- **Intention**: トラフィック制御
- **Gateway**: イングレス/エグレス

## 利用方法

### インストール（Docker）

```bash
# 開発モード
docker run -d --name consul \
  -p 8500:8500 \
  -p 8600:8600/udp \
  consul:latest agent -dev -ui -client=0.0.0.0

# Web UI: http://localhost:8500
```

### サービス登録

```bash
# サービス定義
cat > web-service.json <<EOF
{
  "service": {
    "name": "web",
    "tags": ["rails"],
    "port": 8000,
    "check": {
      "http": "http://localhost:8000/health",
      "interval": "10s"
    }
  }
}
EOF

# サービス登録
consul services register web-service.json
```

### DNS クエリ

```bash
# サービス検索（DNS）
dig @127.0.0.1 -p 8600 web.service.consul

# SRVレコード
dig @127.0.0.1 -p 8600 web.service.consul SRV
```

### HTTP API

```bash
# サービス一覧
curl http://localhost:8500/v1/catalog/services

# サービス詳細
curl http://localhost:8500/v1/catalog/service/web

# ヘルシーなインスタンス
curl http://localhost:8500/v1/health/service/web?passing
```

### Key-Value ストア

```bash
# 値の書き込み
consul kv put config/app/db_host "db.example.com"

# 値の読み取り
consul kv get config/app/db_host

# 削除
consul kv delete config/app/db_host

# ディレクトリ一覧
consul kv get -recurse config/
```

### Go クライアント

```go
package main

import (
    "fmt"
    "github.com/hashicorp/consul/api"
)

func main() {
    config := api.DefaultConfig()
    client, err := api.NewClient(config)
    if err != nil {
        panic(err)
    }

    // サービス登録
    registration := &api.AgentServiceRegistration{
        Name: "my-service",
        Port: 8080,
        Check: &api.AgentServiceCheck{
            HTTP:     "http://localhost:8080/health",
            Interval: "10s",
        },
    }
    client.Agent().ServiceRegister(registration)

    // サービス検索
    services, _, err := client.Health().Service("web", "", true, nil)
    if err != nil {
        panic(err)
    }

    for _, service := range services {
        fmt.Printf("Service: %s:%d\n", service.Service.Address, service.Service.Port)
    }

    // KV操作
    kv := client.KV()
    kv.Put(&api.KVPair{Key: "config/db", Value: []byte("localhost")}, nil)

    pair, _, _ := kv.Get("config/db", nil)
    fmt.Println(string(pair.Value))
}
```

### Docker Compose（3ノードクラスタ）

```yaml
version: '3.8'
services:
  consul-server1:
    image: consul:latest
    command: agent -server -bootstrap-expect=3 -ui -client=0.0.0.0
    environment:
      CONSUL_BIND_INTERFACE: eth0
    ports:
      - "8500:8500"

  consul-server2:
    image: consul:latest
    command: agent -server -retry-join=consul-server1
    environment:
      CONSUL_BIND_INTERFACE: eth0

  consul-server3:
    image: consul:latest
    command: agent -server -retry-join=consul-server1
    environment:
      CONSUL_BIND_INTERFACE: eth0
```

### Kubernetes統合

```yaml
# ServiceDefaults (Connect)
apiVersion: consul.hashicorp.com/v1alpha1
kind: ServiceDefaults
metadata:
  name: web
spec:
  protocol: http
```

### ヘルスチェック設定

```json
{
  "service": {
    "name": "web",
    "port": 8000,
    "checks": [
      {
        "http": "http://localhost:8000/health",
        "interval": "10s",
        "timeout": "1s"
      },
      {
        "tcp": "localhost:8000",
        "interval": "10s"
      }
    ]
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Consul OSS** | 🟢 無料 | オープンソース、MPL License |
| **Consul Enterprise** | 💰 要問い合わせ | 複製、管理機能 |
| **HCP Consul** | 💰 従量課金 | マネージドConsul |

## メリット

1. **無料**: オープンソース
2. **サービスディスカバリ**: DNS、HTTP
3. **ヘルスチェック**: 自動監視
4. **サービスメッシュ**: mTLS通信
5. **マルチDC**: 複数データセンター

## デメリット

1. **複雑性**: 学習曲線steep
2. **運用**: クラスタ運用複雑
3. **リソース**: メモリ消費
4. **小規模**: 小規模環境にオーバースペック

## 公式リンク

- **公式サイト**: [https://www.consul.io/](https://www.consul.io/)
- **ドキュメント**: [https://www.consul.io/docs](https://www.consul.io/docs)

## 関連ドキュメント

- [サービスディスカバリツール一覧](../サービスディスカバリツール/)
- [Kubernetes](../オーケストレーションツール/Kubernetes.md)
- [Istio](../サービスメッシュツール/Istio.md)

---

**カテゴリ**: サービスディスカバリツール
**対象工程**: マイクロサービス運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
