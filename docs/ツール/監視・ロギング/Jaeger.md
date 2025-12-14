# Jaeger

## 概要

Jaegerは、オープンソースの分散トレーシングシステムです。OpenTracing/OpenTelemetry準拠、スパン収集、トレース可視化、依存関係分析により、マイクロサービスアーキテクチャのパフォーマンス監視、ボトルネック特定、レイテンシ分析を実現します。Uber開発、CNCF卒業プロジェクト、Kubernetes統合で広く採用されています。

## 主な機能

### 1. 分散トレーシング
- **スパン**: 処理単位
- **トレース**: スパン連鎖
- **コンテキスト伝播**: サービス間
- **サンプリング**: トレースサンプリング

### 2. 可視化
- **トレースビュー**: 時系列表示
- **サービス依存関係**: DAGグラフ
- **レイテンシ分析**: P95、P99
- **エラー追跡**: エラースパン

### 3. バックエンド
- **Cassandra**: スケーラブルストレージ
- **Elasticsearch**: 全文検索
- **Kafka**: ストリーミング
- **インメモリ**: 開発環境

### 4. 統合
- **OpenTelemetry**: 標準計装
- **Kubernetes**: K8s統合
- **Istio**: サービスメッシュ

## 利用方法

### インストール（Docker）

```bash
# All-in-oneモード（開発用）
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 6831:6831/udp \
  jaegertracing/all-in-one:latest

# Web UI: http://localhost:16686
```

### Python計装（OpenTelemetry）

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Tracerプロバイダ設定
resource = Resource.create({"service.name": "my-service"})
provider = TracerProvider(resource=resource)

# Jaeger Exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# スパン作成
with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("user.id", "123")
    span.set_attribute("http.method", "GET")
    # 処理
    result = do_something()
    span.set_attribute("result", result)
```

### Go計装

```go
package main

import (
    "context"
    "io"
    "log"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
)

func initTracer() (func(), error) {
    exporter, err := jaeger.New(jaeger.WithAgentEndpoint())
    if err != nil {
        return nil, err
    }

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("my-service"),
        )),
    )

    otel.SetTracerProvider(tp)

    return func() {
        if err := tp.Shutdown(context.Background()); err != nil {
            log.Fatal(err)
        }
    }, nil
}

func main() {
    shutdown, err := initTracer()
    if err != nil {
        log.Fatal(err)
    }
    defer shutdown()

    tracer := otel.Tracer("my-service")
    ctx, span := tracer.Start(context.Background(), "my-operation")
    defer span.End()

    // 処理
    doSomething(ctx)
}
```

### Kubernetes統合

```yaml
# jaeger-operator
apiVersion: v1
kind: Namespace
metadata:
  name: observability

---
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: observability
spec:
  strategy: allInOne
  ingress:
    enabled: true
```

### サンプリング設定

```json
{
  "service_strategies": [
    {
      "service": "my-service",
      "type": "probabilistic",
      "param": 0.5
    }
  ],
  "default_strategy": {
    "type": "probabilistic",
    "param": 0.1
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Jaeger** | 🟢 完全無料 | オープンソース、Apache License |

## メリット

1. **完全無料**: オープンソース
2. **標準準拠**: OpenTelemetry
3. **可視化**: 優れたUI
4. **スケーラブル**: Cassandra、Elasticsearch
5. **Kubernetes**: K8sネイティブ

## デメリット

1. **複雑性**: セットアップ複雑
2. **運用**: バックエンド運用必要
3. **計装**: アプリ計装必要
4. **ストレージ**: 大量データストレージコスト

## 公式リンク

- **公式サイト**: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
- **ドキュメント**: [https://www.jaegertracing.io/docs/](https://www.jaegertracing.io/docs/)

## 関連ドキュメント

- [分散トレーシングツール一覧](../分散トレーシングツール/)
- [Zipkin](./Zipkin.md)
- [OpenTelemetry](./OpenTelemetry.md)

---

**カテゴリ**: 分散トレーシングツール
**対象工程**: マイクロサービス監視
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
