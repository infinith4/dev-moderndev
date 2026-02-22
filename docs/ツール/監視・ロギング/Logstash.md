# Logstash

## 概要

Logstashは、Elastic Stack（ELK）のログ収集・変換・転送パイプラインです。Input、Filter、Outputプラグイン、Grok（パース）、JSON変換により、多様なログソース（ファイル、Syslog、Beats、Kafka）からデータ収集・変換し、Elasticsearch、S3、監視ツールに転送します。200+プラグイン、リアルタイム処理で広く採用されています。

## 主な機能

### 1. Input
- **ファイル**: ログファイル読み込み
- **Beats**: Filebeat、Metricbeat
- **Syslog**: Syslogサーバー
- **Kafka**: Kafkaコンシューマー
- **HTTP**: HTTP POST
- **JDBC**: データベース

### 2. Filter
- **Grok**: ログパース
- **Mutate**: フィールド操作
- **Date**: 日付パース
- **JSON**: JSON変換
- **GeoIP**: IPジオロケーション

### 3. Output
- **Elasticsearch**: ELK統合
- **S3**: AWS S3
- **Kafka**: Kafkaプロデューサー
- **File**: ファイル出力
- **HTTP**: HTTP POST

## 利用方法

### インストール（Docker）

```bash
docker run -d --name logstash \
  -v $(pwd)/logstash.conf:/usr/share/logstash/pipeline/logstash.conf \
  docker.elastic.co/logstash/logstash:8.11.0
```

### 基本設定

```ruby
# logstash.conf
input {
  file {
    path => "/var/log/app/*.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
  }

  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "app-logs-%{+YYYY.MM.dd}"
  }

  stdout {
    codec => rubydebug
  }
}
```

### Grokパターン

```ruby
filter {
  grok {
    match => {
      "message" => "%{IP:client_ip} - - \[%{HTTPDATE:timestamp}\] \"%{WORD:method} %{URIPATHPARAM:request} HTTP/%{NUMBER:http_version}\" %{NUMBER:response_code} %{NUMBER:bytes}"
    }
  }
}
```

### JSON変換

```ruby
input {
  http {
    port => 8080
    codec => json
  }
}

filter {
  json {
    source => "message"
  }

  mutate {
    add_field => { "[@metadata][index]" => "json-logs" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[@metadata][index]}-%{+YYYY.MM.dd}"
  }
}
```

### Beats統合

```ruby
# Filebeat → Logstash
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][log_type] == "nginx" {
    grok {
      match => { "message" => "%{NGINXACCESS}" }
    }
  } else if [fields][log_type] == "apache" {
    grok {
      match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[fields][log_type]}-%{+YYYY.MM.dd}"
  }
}
```

### Kafka統合

```ruby
input {
  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["app-logs"]
    codec => json
  }
}

filter {
  mutate {
    add_field => { "[@metadata][index]" => "kafka-logs" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[@metadata][index]}-%{+YYYY.MM.dd}"
  }
}
```

### Docker Compose（ELK Stack）

```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

### 条件分岐

```ruby
filter {
  if [level] == "ERROR" {
    mutate {
      add_tag => ["error"]
    }
  }

  if [response_code] >= 500 {
    mutate {
      add_tag => ["server_error"]
    }
  }
}

output {
  if "error" in [tags] {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "error-logs-%{+YYYY.MM.dd}"
    }
  } else {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "app-logs-%{+YYYY.MM.dd}"
    }
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Logstash OSS** | 🟢 無料 | オープンソース、Apache License |
| **Elastic Cloud** | 💰 $95/月〜 | マネージドELK Stack |

## メリット

1. **無料**: オープンソース
2. **豊富なプラグイン**: 200+プラグイン
3. **Grok**: 強力なログパース
4. **Elastic Stack**: ELK統合
5. **柔軟性**: 多様なInput/Output

## デメリット

1. **メモリ**: メモリ消費大
2. **複雑性**: 設定複雑
3. **パフォーマンス**: CPU消費大
4. **代替**: Fluentd、Vector等

## 公式リンク

- **公式サイト**: [https://www.elastic.co/logstash](https://www.elastic.co/logstash)
- **ドキュメント**: [https://www.elastic.co/guide/en/logstash/current/index.html](https://www.elastic.co/guide/en/logstash/current/index.html)

## 関連ドキュメント

- [ログ処理ツール一覧](../ログ処理ツール/)
- [Elasticsearch](../検索ツール/Elasticsearch.md)
- [Kibana](../可視化ツール/Kibana.md)
- [Fluentd](./Fluentd.md)

---

**カテゴリ**: ログ処理ツール
**対象工程**: ログ収集・変換
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
