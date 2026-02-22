# ELK Stack

## 概要

ELK Stackは、Elasticsearch、Logstash、Kibanaの3つのオープンソースツールを組み合わせたログ管理・分析プラットフォームです。Elastic社が開発し、大規模ログデータの収集、保存、検索、可視化を実現します。近年はBeats（軽量データシッパー）を加えてElastic Stack（旧称ELK Stack）と呼ばれ、アプリケーション監視、セキュリティ分析、ビジネスインテリジェンスに広く利用されています。

## 主な機能

### 1. Elasticsearch
- **分散検索エンジン**: Luceneベース全文検索
- **スケーラブル**: 水平スケーリング対応
- **リアルタイム**: 準リアルタイム検索
- **RESTful API**: HTTPベースのAPI

### 2. Logstash
- **データパイプライン**: ログ収集・変換・送信
- **多様な入力**: ファイル、Syslog、Kafka、JDBC等
- **フィルタ**: Grok、Mutate、Date等
- **多様な出力**: Elasticsearch、S3、Kafka等

### 3. Kibana
- **データ可視化**: グラフ、チャート、ダッシュボード
- **Discover**: ログ検索・フィルタリング
- **Canvas**: カスタムダッシュボード
- **Alerting**: アラート設定

### 4. Beats
- **Filebeat**: ログファイル収集
- **Metricbeat**: システムメトリクス収集
- **Packetbeat**: ネットワークトラフィック
- **Auditbeat**: 監査データ
- **Heartbeat**: 死活監視

### 5. セキュリティ
- **SIEM**: セキュリティ情報・イベント管理
- **脅威検知**: 異常検知、機械学習
- **監査ログ**: アクセスログ管理

## 利用方法

### Dockerで起動

```yaml
# docker-compose.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - 9200:9200
    volumes:
      - es-data:/usr/share/elasticsearch/data
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    ports:
      - 5044:5044
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - 5601:5601
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  es-data:
```

```bash
docker-compose up -d
```

### Logstash設定

```ruby
# logstash.conf
input {
  beats {
    port => 5044
  }
  
  file {
    path => "/var/log/nginx/access.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
  
  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
  }
  
  geoip {
    source => "clientip"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "nginx-logs-%{+YYYY.MM.dd}"
  }
  
  stdout {
    codec => rubydebug
  }
}
```

### Filebeat設定

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/nginx/access.log
      - /var/log/nginx/error.log

output.logstash:
  hosts: ["localhost:5044"]
```

```bash
# Filebeat起動
sudo filebeat -e -c filebeat.yml
```

### Kibana ダッシュボード作成

```
1. Kibana UI（http://localhost:5601）にアクセス
2. Management → Index Patterns → Create index pattern
   - Index pattern name: nginx-logs-*
   - Time field: @timestamp

3. Discover → ログ検索
   - KQL: response:500
   - 時間範囲: Last 24 hours

4. Visualize → Create visualization
   - Pie chart: Status code distribution
   - Line chart: Requests over time
   - Table: Top IPs

5. Dashboard → Create dashboard
   - 複数の可視化を追加
   - 保存
```

### Elasticsearch クエリ

```bash
# インデックス一覧
curl -X GET "localhost:9200/_cat/indices?v"

# ドキュメント検索
curl -X GET "localhost:9200/nginx-logs-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "response": "500"
    }
  }
}
'

# 集計
curl -X GET "localhost:9200/nginx-logs-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "status_codes": {
      "terms": {
        "field": "response.keyword"
      }
    }
  }
}
'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Elastic Stack (OSS)** | 🟢 無料 | オープンソース、Apache License 2.0 |
| **Elastic Cloud** | 💰 従量課金 | マネージドサービス、$0.10/時間~ |
| **Enterprise** | 💰 要問い合わせ | 高度なセキュリティ、サポート、SLA |

## メリット

### ✅ 主な利点

1. **無料**: オープンソース版
2. **スケーラブル**: PB級データ対応
3. **リアルタイム**: 準リアルタイム検索
4. **柔軟な検索**: Lucene、KQL
5. **可視化**: Kibanaで豊富なグラフ
6. **多様なデータソース**: Beats、Logstash
7. **エコシステム**: 豊富なプラグイン
8. **SIEM**: セキュリティ分析
9. **機械学習**: 異常検知
10. **コミュニティ**: 活発なコミュニティ

## デメリット

### ❌ 制約・課題

1. **リソース消費**: 大量のメモリ・CPU必要
2. **複雑性**: 設定・運用が複雑
3. **コスト**: Elastic Cloudは高額
4. **学習曲線**: Elasticsearch習得に時間
5. **メンテナンス**: クラスター管理が必要
6. **ディスク**: 大量のストレージ必要
7. **ライセンス変更**: Elastic License（一部機能）
8. **バージョンアップ**: アップグレードに注意必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Splunk** | 商用、エンタープライズ | ELKより高機能だが高価 |
| **Datadog** | SaaS、APM統合 | ELKより簡単だが有料 |
| **Graylog** | オープンソース | ELKよりシンプル |
| **Loki + Grafana** | 軽量、Prometheus統合 | ELKより軽量 |
| **Sumo Logic** | SaaS | ELKよりマネージド |

## 公式リンク

- **Elastic公式**: [https://www.elastic.co/](https://www.elastic.co/)
- **Elasticsearch**: [https://www.elastic.co/elasticsearch/](https://www.elastic.co/elasticsearch/)
- **Logstash**: [https://www.elastic.co/logstash/](https://www.elastic.co/logstash/)
- **Kibana**: [https://www.elastic.co/kibana/](https://www.elastic.co/kibana/)
- **Beats**: [https://www.elastic.co/beats/](https://www.elastic.co/beats/)
- **ドキュメント**: [https://www.elastic.co/guide/](https://www.elastic.co/guide/)

## 関連ドキュメント

- [監視ツール一覧](../監視ツール/)
- [Splunk](./Splunk.md)
- [Datadog](./Datadog.md)
- [Prometheus](./Prometheus.md)
- [ログ管理ベストプラクティス](../../best-practices/log-management.md)

---

**カテゴリ**: 監視ツール  
**対象工程**: 運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
