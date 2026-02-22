# Fluentd

## 概要

Fluentdは、オープンソースのログ収集・転送ツールです。プラグインアーキテクチャ（1000+）、統一ログレイヤー、Input/Output/Filter、JSON構造化により、多様なログソース（アプリ、サーバー、コンテナ）からデータ収集し、Elasticsearch、S3、BigQuery、Kafkaに転送します。CNCF卒業プロジェクト、Kubernetes統合で広く採用されています。

## 主な機能

### 1. ログ収集
- **Tail**: ログファイル監視
- **HTTP**: HTTP POST
- **Syslog**: Syslogサーバー
- **Forward**: Fluentd間転送

### 2. フィルター
- **Parser**: ログパース
- **Record Transformer**: レコード変換
- **Grep**: フィルタリング
- **Geoip**: IPジオロケーション

### 3. 出力
- **Elasticsearch**: ELK統合
- **S3**: AWS S3
- **Kafka**: Kafkaプロデューサー
- **BigQuery**: Google BigQuery
- **MongoDB**: MongoDB

### 4. バッファリング
- **メモリバッファ**: インメモリ
- **ファイルバッファ**: ディスク永続化
- **リトライ**: 自動リトライ

## 利用方法

### インストール（Docker）

```bash
docker run -d --name fluentd \
  -p 24224:24224 \
  -v $(pwd)/fluent.conf:/fluentd/etc/fluent.conf \
  fluent/fluentd:latest
```

### 基本設定

```ruby
# fluent.conf
<source>
  @type tail
  path /var/log/app/*.log
  pos_file /var/log/fluentd/app.pos
  tag app.log
  <parse>
    @type json
  </parse>
</source>

<filter app.log>
  @type record_transformer
  <record>
    hostname "#{Socket.gethostname}"
    timestamp ${time}
  </record>
</filter>

<match app.log>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name app-logs
  type_name _doc
  logstash_format true
</match>
```

### Nginx/Apache ログ

```ruby
<source>
  @type tail
  path /var/log/nginx/access.log
  pos_file /var/log/fluentd/nginx.pos
  tag nginx.access
  <parse>
    @type nginx
  </parse>
</source>

<match nginx.access>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name nginx-logs-%Y.%m.%d
</match>
```

### Docker ログ

```ruby
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<filter docker.**>
  @type parser
  key_name log
  <parse>
    @type json
  </parse>
</filter>

<match docker.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix docker
</match>
```

### Kubernetes統合（DaemonSet）

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: fluentd
  template:
    metadata:
      labels:
        k8s-app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.default.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### 複数出力

```ruby
<match app.log>
  @type copy

  <store>
    @type elasticsearch
    host elasticsearch
    port 9200
    index_name app-logs
  </store>

  <store>
    @type s3
    aws_key_id YOUR_KEY
    aws_sec_key YOUR_SECRET
    s3_bucket my-logs
    s3_region us-east-1
    path logs/
  </store>

  <store>
    @type stdout
  </store>
</match>
```

### バッファリング

```ruby
<match app.log>
  @type elasticsearch
  host elasticsearch
  port 9200

  <buffer>
    @type file
    path /var/log/fluentd/buffer
    flush_interval 10s
    retry_max_interval 30s
    retry_forever true
  </buffer>
</match>
```

### アプリケーション統合（Ruby）

```ruby
require 'fluent-logger'

log = Fluent::Logger::FluentLogger.new('app', host: 'localhost', port: 24224)

log.post('event', {
  message: 'User logged in',
  user_id: 123,
  timestamp: Time.now.to_i
})
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Fluentd** | 🟢 無料 | オープンソース、Apache License |
| **Fluentd Cloud** | 💰 従量課金 | マネージドFluentd |

## メリット

1. **無料**: オープンソース
2. **豊富なプラグイン**: 1000+プラグイン
3. **軽量**: Logstashより軽量
4. **統一ログ**: 統一ログレイヤー
5. **Kubernetes**: K8sネイティブ

## デメリット

1. **Rubyベース**: Ruby依存
2. **学習曲線**: 設定学習必要
3. **パフォーマンス**: 高負荷時遅延
4. **複雑なパース**: 複雑なログパース困難

## 公式リンク

- **公式サイト**: [https://www.fluentd.org/](https://www.fluentd.org/)
- **ドキュメント**: [https://docs.fluentd.org/](https://docs.fluentd.org/)

## 関連ドキュメント

- [ログ収集ツール一覧](../ログ収集ツール/)
- [Logstash](../ログ処理ツール/Logstash.md)
- [Fluent Bit](./Fluent_Bit.md)

---

**カテゴリ**: ログ収集ツール
**対象工程**: ログ収集・転送
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
