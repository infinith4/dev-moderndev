# OpenTelemetry

## 概要

OpenTelemetry（OTel）は、CNCFのグラデュエーテッドプロジェクトとして開発されているオブザーバビリティのためのオープン標準フレームワークです。トレース、メトリクス、ログの3つのテレメトリデータを、ベンダー非依存の統一されたAPI・SDK・プロトコル（OTLP）で生成・収集・エクスポートします。Java、Python、Go、.NET、Node.js、Ruby等の主要言語のSDKを提供し、OpenTelemetry Collectorを経由してJaeger、Prometheus、Grafana、Datadog等の任意のバックエンドに送信できます。

## 主な機能

### 1. テレメトリデータ

- **Traces**: 分散トレーシング（Span、Context Propagation）
- **Metrics**: カウンター、ヒストグラム、ゲージ等のメトリクス
- **Logs**: 構造化ログの収集・コンテキスト付与
- **Baggage**: リクエスト間のコンテキスト伝播

### 2. コンポーネント

- **API**: テレメトリデータ生成のためのインターフェース定義
- **SDK**: API実装（サンプリング、バッチ処理、エクスポート）
- **OTLP**: テレメトリデータ転送のための標準プロトコル
- **Auto-Instrumentation**: フレームワーク・ライブラリの自動計装

### 3. OpenTelemetry Collector

- **Receiver**: OTLP、Jaeger、Prometheus等のデータ受信
- **Processor**: バッチ処理、フィルタリング、属性変換
- **Exporter**: Jaeger、Prometheus、Loki、OTLP等へのデータ送信
- **Connector**: パイプライン間のデータ接続

### 4. 対応言語SDK

- **Java**: Spring Boot自動計装、gRPC/HTTP計装
- **Python**: Django、Flask、FastAPI自動計装
- **Go**: net/http、gRPC計装
- **.NET**: ASP.NET Core自動計装
- **Node.js**: Express、Fastify自動計装
- **Ruby**: Rails、Sinatra計装

## 利用方法

### OpenTelemetry Collectorの導入

```bash
# Docker
docker run --name otel-collector -d \
  -p 4317:4317 -p 4318:4318 -p 8888:8888 \
  -v $(pwd)/otel-collector-config.yaml:/etc/otelcol/config.yaml \
  otel/opentelemetry-collector-contrib

# Helm（Kubernetes）
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install otel-collector open-telemetry/opentelemetry-collector \
  --namespace monitoring --create-namespace \
  --set mode=deployment
```

### Collector設定ファイル

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true
  prometheus:
    endpoint: 0.0.0.0:8889
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/jaeger]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki]
```

### Java SDK（Spring Boot）

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
</dependency>
```

```yaml
# application.yml
otel:
  exporter:
    otlp:
      endpoint: http://otel-collector:4318
  resource:
    attributes:
      service.name: my-spring-app
      deployment.environment: production
  traces:
    sampler: parentbased_traceidratio
    sampler.arg: 0.1
```

### Python SDK

```bash
# インストール
pip install opentelemetry-api opentelemetry-sdk
pip install opentelemetry-exporter-otlp
pip install opentelemetry-instrumentation-flask
pip install opentelemetry-instrumentation-requests

# 自動計装（ゼロコード変更）
opentelemetry-instrument \
  --traces_exporter otlp \
  --metrics_exporter otlp \
  --service_name my-flask-app \
  --exporter_otlp_endpoint http://otel-collector:4318 \
  python app.py
```

```python
# 手動計装の例
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Tracer設定
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-service")

# カスタムSpan
with tracer.start_as_current_span("process-order") as span:
    span.set_attribute("order.id", "12345")
    span.set_attribute("order.amount", 99.99)
    # 処理ロジック
```

### Node.js SDK

```javascript
// tracing.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: 'my-node-app',
});

sdk.start();
```

```bash
# 起動
node --require ./tracing.js app.js
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **OpenTelemetry** | 無料 | オープンソース、Apache License 2.0、CNCFグラデュエーテッド |

## メリット

1. **ベンダー非依存**: OTLP標準により、バックエンドを自由に選択・変更可能
2. **3シグナル統合**: トレース・メトリクス・ログを統一的なAPIで管理
3. **自動計装**: フレームワーク対応の自動計装でコード変更なしに計測開始
4. **CNCFグラデュエーテッド**: KubernetesやPrometheusと同等の成熟度
5. **多言語対応**: Java、Python、Go、.NET、Node.js等の公式SDK
6. **Collector**: パイプラインの中間処理（フィルタ、変換、サンプリング）が柔軟
7. **エコシステム**: Jaeger、Prometheus、Grafana、Datadog等の主要ツールと統合

## デメリット

1. **学習コスト**: API/SDK/Collector/OTLPの概念と設定の理解が必要
2. **SDKの成熟度差**: 言語によってSDKの安定度・機能が異なる（Logs APIは一部Stable未達）
3. **設定の複雑さ**: Collector設定のパイプライン構築が複雑になりやすい
4. **オーバーヘッド**: 計装によるアプリケーションのパフォーマンス影響
5. **バックエンド別**: 可視化にはJaeger、Grafana等の別ツールが必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Jaeger** | 分散トレーシング | OTelのトレースバックエンドとして使用、トレース特化 |
| **Datadog APM** | SaaS APM | OTelより統合的だが有料 |
| **New Relic** | SaaS APM | OTelデータの受信に対応、独自エージェントも提供 |
| **AWS X-Ray** | AWSトレーシング | AWS環境向け、OTelエクスポーターで連携可能 |

## 公式リンク

- **公式サイト**: [https://opentelemetry.io/](https://opentelemetry.io/)
- **ドキュメント**: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
- **GitHub**: [https://github.com/open-telemetry](https://github.com/open-telemetry)
- **Collector**: [https://github.com/open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector)
- **CNCF**: [https://www.cncf.io/projects/opentelemetry/](https://www.cncf.io/projects/opentelemetry/)
- **Registry（計装一覧）**: [https://opentelemetry.io/ecosystem/registry/](https://opentelemetry.io/ecosystem/registry/)

## 関連ドキュメント

- [Alertmanager](./Alertmanager.md)
- [Loki](./Loki.md)

---

**カテゴリ**: 監視ロギング
**対象工程**: 実装・運用・監視
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
