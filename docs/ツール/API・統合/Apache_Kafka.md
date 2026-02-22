# Apache Kafka

## 概要

Apache Kafkaは、高スループット分散メッセージングプラットフォームです。ログストリーミング、イベント駆動アーキテクチャ、リアルタイムデータパイプラインを実現し、LinkedIn開発のオープンソースプロジェクトとして、大規模データストリーミング処理で広く採用されています。Topic、Partition、Consumer Group、Kafka Streamsにより、スケーラブルなメッセージング基盤を提供します。

## 主な機能

### 1. メッセージング
- **Topic**: メッセージカテゴリ
- **Partition**: 並列処理
- **Replication**: レプリケーション

### 2. ストリーミング
- **Kafka Streams**: ストリーム処理
- **Kafka Connect**: データ統合
- **KSQL**: SQLライクストリーム処理

### 3. 高スループット
- **バッチ処理**: バッチ送信
- **圧縮**: メッセージ圧縮
- **ゼロコピー**: 高速転送

## 利用方法

### インストール（Docker）

```bash
# Zookeeper + Kafka
docker-compose up -d

# docker-compose.yml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
  
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
```

### Producer（Java）

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

Producer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("my-topic", "key", "Hello Kafka"));
producer.close();
```

### Consumer（Java）

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

Consumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("my-topic"));

while (true) {
  ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
  for (ConsumerRecord<String, String> record : records) {
    System.out.println(record.value());
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Apache Kafka** | 🟢 無料 | オープンソース、Apache License |
| **Confluent Cloud** | 💰 従量課金 | マネージドKafka |

## メリット

1. **高スループット**: 数百万msg/秒
2. **スケーラブル**: 水平スケール
3. **耐久性**: レプリケーション
4. **リアルタイム**: 低レイテンシ
5. **オープンソース**: 無料

## デメリット

1. **複雑性**: セットアップ複雑
2. **運用**: 運用負荷高い
3. **Zookeeper**: Zookeeper依存（KRaft移行中）
4. **学習曲線**: steep

## 公式リンク

- **公式サイト**: [https://kafka.apache.org/](https://kafka.apache.org/)
- **ドキュメント**: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)

## 関連ドキュメント

- [メッセージングツール一覧](../メッセージングツール/)
- [RabbitMQ](./RabbitMQ.md)

---

**カテゴリ**: メッセージングツール  
**対象工程**: ストリーミング処理  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
