# Zipkin

## 概要

Zipkinは、分散トレーシングシステムです。スパン収集、トレース可視化、依存関係分析により、マイクロサービスのレイテンシ問題特定、パフォーマンス監視を実現します。Twitter開発、OpenZipkin、軽量、Spring Cloud Sleuth統合で広く採用されています。

## 主な機能

### 1. 分散トレーシング
- **スパン**: 処理単位
- **トレース**: スパン連鎖
- **タグ**: メタデータ
- **アノテーション**: イベント

### 2. 可視化
- **トレースビュー**: タイムライン表示
- **依存関係**: サービス依存図
- **検索**: トレースID、サービス名
- **レイテンシ**: 分布分析

### 3. ストレージ
- **インメモリ**: 開発環境
- **MySQL**: RDBMS
- **Cassandra**: スケーラブル
- **Elasticsearch**: 全文検索

### 4. 統合
- **Spring Cloud Sleuth**: Spring統合
- **Brave**: Javaクライアント
- **OpenTelemetry**: 標準計装

## 利用方法

### インストール（Docker）

```bash
docker run -d --name zipkin \
  -p 9411:9411 \
  openzipkin/zipkin:latest

# Web UI: http://localhost:9411
```

### Spring Boot統合

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-sleuth-zipkin</artifactId>
</dependency>
```

```yaml
# application.yml
spring:
  application:
    name: my-service
  sleuth:
    sampler:
      probability: 1.0  # 100% サンプリング
  zipkin:
    base-url: http://localhost:9411
```

### Java（Brave）

```java
import brave.Tracing;
import brave.Span;
import brave.propagation.B3Propagation;
import zipkin2.reporter.AsyncReporter;
import zipkin2.reporter.okhttp3.OkHttpSender;

public class ZipkinExample {
    public static void main(String[] args) {
        // Zipkin Sender
        OkHttpSender sender = OkHttpSender.create("http://localhost:9411/api/v2/spans");
        AsyncReporter<Span> spanReporter = AsyncReporter.create(sender);

        // Tracing設定
        Tracing tracing = Tracing.newBuilder()
            .localServiceName("my-service")
            .spanReporter(spanReporter)
            .propagationFactory(B3Propagation.FACTORY)
            .build();

        // スパン作成
        Span span = tracing.tracer().nextSpan().name("my-operation").start();
        try {
            // 処理
            span.tag("user.id", "123");
            span.annotate("processing");
            doSomething();
        } finally {
            span.finish();
        }

        tracing.close();
        spanReporter.close();
    }
}
```

### Node.js（zipkin-js）

```javascript
const { Tracer, ExplicitContext, BatchRecorder } = require('zipkin');
const { HttpLogger } = require('zipkin-transport-http');

const recorder = new BatchRecorder({
  logger: new HttpLogger({
    endpoint: 'http://localhost:9411/api/v2/spans'
  })
});

const ctxImpl = new ExplicitContext();
const tracer = new Tracer({ ctxImpl, recorder, localServiceName: 'my-service' });

// スパン作成
tracer.scoped(() => {
  tracer.recordServiceName('my-service');
  tracer.recordRpc('my-operation');
  tracer.recordBinary('user.id', '123');

  // 処理
  doSomething();
});
```

### Python（py_zipkin）

```python
from py_zipkin.zipkin import zipkin_span
import requests

def http_transport(encoded_span):
    requests.post(
        'http://localhost:9411/api/v2/spans',
        data=encoded_span,
        headers={'Content-Type': 'application/json'}
    )

@zipkin_span(
    service_name='my-service',
    span_name='my-operation',
    transport_handler=http_transport,
    sample_rate=100.0
)
def my_function():
    # 処理
    do_something()
```

### Docker Compose（Zipkin + MySQL）

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: zipkin

  zipkin:
    image: openzipkin/zipkin
    ports:
      - "9411:9411"
    environment:
      STORAGE_TYPE: mysql
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASS: secret
    depends_on:
      - mysql
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Zipkin** | 🟢 無料 | オープンソース、Apache License |

## メリット

1. **無料**: オープンソース
2. **軽量**: シンプルアーキテクチャ
3. **Spring統合**: Spring Cloud Sleuth
4. **可視化**: 優れたUI
5. **ストレージ選択**: 複数バックエンド

## デメリット

1. **機能**: Jaegerより機能少ない
2. **スケール**: 大規模に限界
3. **長期保存**: 長期保存不向き
4. **分析機能**: 高度分析弱い

## 公式リンク

- **公式サイト**: [https://zipkin.io/](https://zipkin.io/)
- **ドキュメント**: [https://zipkin.io/pages/documentation.html](https://zipkin.io/pages/documentation.html)

## 関連ドキュメント

- [分散トレーシングツール一覧](../分散トレーシングツール/)
- [Jaeger](./Jaeger.md)
- [OpenTelemetry](./OpenTelemetry.md)

---

**カテゴリ**: 分散トレーシングツール
**対象工程**: マイクロサービス監視
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
