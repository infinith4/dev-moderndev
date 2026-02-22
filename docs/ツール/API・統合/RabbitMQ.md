# RabbitMQ

## 概要

RabbitMQは、オープンソースのメッセージブローカーです。AMQP（Advanced Message Queuing Protocol）をサポートし、非同期メッセージング、タスクキュー、Pub/Sub、RPC、メッセージルーティングにより、マイクロサービス間の疎結合通信を実現します。Erlang実装、高可用性、管理UI、多言語クライアント（Java、Python、Node.js等）で広く採用されています。

## 主な機能

### 1. メッセージング
- **キュー**: FIFO メッセージキュー
- **Exchange**: メッセージルーティング
- **Binding**: Queue-Exchange紐付け

### 2. パターン
- **Work Queue**: タスクキュー
- **Pub/Sub**: ファンアウト
- **Routing**: トピックルーティング
- **RPC**: リクエスト/レスポンス

### 3. 高可用性
- **クラスタリング**: 複数ノード
- **ミラーリング**: キューレプリケーション
- **永続化**: ディスク永続化

## 利用方法

### インストール（Docker）

```bash
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management

# 管理UI: http://localhost:15672
# デフォルト: guest/guest
```

### Python（pika）

```python
import pika

# 接続
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# キュー作成
channel.queue_declare(queue='hello')

# メッセージ送信
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='Hello World!')

# メッセージ受信
def callback(ch, method, properties, body):
    print(f"Received {body}")

channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True)

channel.start_consuming()
```

### Node.js（amqplib）

```javascript
const amqp = require('amqplib');

async function send() {
  const conn = await amqp.connect('amqp://localhost');
  const ch = await conn.createChannel();
  const queue = 'hello';
  
  await ch.assertQueue(queue);
  ch.sendToQueue(queue, Buffer.from('Hello World!'));
  
  await ch.close();
  await conn.close();
}

async function receive() {
  const conn = await amqp.connect('amqp://localhost');
  const ch = await conn.createChannel();
  const queue = 'hello';
  
  await ch.assertQueue(queue);
  ch.consume(queue, (msg) => {
    console.log(`Received: ${msg.content.toString()}`);
    ch.ack(msg);
  });
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **RabbitMQ** | 🟢 無料 | オープンソース、MPL License |

## メリット

1. **無料**: オープンソース
2. **AMQP**: 標準プロトコル
3. **多言語**: 豊富なクライアント
4. **管理UI**: Webベース管理
5. **高可用性**: クラスタリング

## デメリット

1. **パフォーマンス**: Kafkaより遅い
2. **スケール**: 大規模には不向き
3. **メモリ**: メモリ消費大
4. **複雑性**: 設定複雑

## 公式リンク

- **公式サイト**: [https://www.rabbitmq.com/](https://www.rabbitmq.com/)
- **ドキュメント**: [https://www.rabbitmq.com/documentation.html](https://www.rabbitmq.com/documentation.html)

## 関連ドキュメント

- [メッセージングツール一覧](../メッセージングツール/)
- [Apache Kafka](./Apache_Kafka.md)

---

**カテゴリ**: メッセージングツール  
**対象工程**: 非同期処理  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
