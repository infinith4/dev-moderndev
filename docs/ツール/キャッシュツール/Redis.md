# Redis

## 概要

Redisは、インメモリデータストア・キャッシュサーバーです。Key-Value型NoSQLデータベースとして、高速な読み書き、データ構造（String、List、Set、Hash、Sorted Set）、Pub/Sub、永続化、レプリケーション、クラスタリングにより、セッション管理、キャッシング、リアルタイムランキング、メッセージキューを実現します。

## 主な機能

### 1. データ構造
- **String**: 文字列、数値
- **List**: リスト（FIFO/LIFO）
- **Set**: 重複なし集合
- **Hash**: フィールド-値マップ
- **Sorted Set**: スコア付きソート集合

### 2. パフォーマンス
- **インメモリ**: マイクロ秒レベル
- **パイプライン**: バッチ処理
- **Lua スクリプト**: アトミック操作

### 3. 高可用性
- **レプリケーション**: マスター-スレーブ
- **Redis Sentinel**: 自動フェイルオーバー
- **Redis Cluster**: 水平スケール

## 利用方法

### インストール（Docker）

```bash
docker run -d --name redis \
  -p 6379:6379 \
  redis:latest

# Redis CLI
docker exec -it redis redis-cli
```

### 基本操作

```bash
# String
SET mykey "Hello"
GET mykey
INCR counter

# List
LPUSH mylist "world"
LPUSH mylist "hello"
LRANGE mylist 0 -1

# Set
SADD myset "apple"
SADD myset "banana"
SMEMBERS myset

# Hash
HSET user:1 name "Alice"
HSET user:1 age 30
HGETALL user:1

# Sorted Set
ZADD ranking 100 "player1"
ZADD ranking 200 "player2"
ZRANGE ranking 0 -1 WITHSCORES
```

### Node.js（ioredis）

```javascript
const Redis = require('ioredis');
const redis = new Redis();

// Set/Get
await redis.set('key', 'value');
const value = await redis.get('key');

// TTL付き
await redis.setex('session:123', 3600, 'data');

// Pub/Sub
redis.subscribe('channel');
redis.on('message', (channel, message) => {
  console.log(`Received: ${message}`);
});

redis.publish('channel', 'Hello!');
```

### Python（redis-py）

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set/Get
r.set('key', 'value')
value = r.get('key')

# List
r.lpush('mylist', 'item1', 'item2')
items = r.lrange('mylist', 0, -1)

# TTL
r.setex('temp', 60, 'expires in 60s')
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Redis (OSS)** | 🟢 完全無料 | オープンソース、BSD License |
| **Redis Enterprise** | 💰 商用ライセンス | マルチテナント、アクティブ-アクティブ |
| **AWS ElastiCache** | 💰 従量課金 | マネージドRedis |
| **Azure Cache** | 💰 従量課金 | マネージドRedis |

## メリット

1. **高速**: マイクロ秒レベルレイテンシ
2. **完全無料**: オープンソース
3. **豊富な型**: 5つのデータ構造
4. **永続化**: RDB、AOF
5. **多言語**: 豊富なクライアント

## デメリット

1. **メモリ依存**: メモリサイズ制限
2. **データ型制限**: 複雑なクエリ不可
3. **トランザクション**: 限定的
4. **運用**: クラスタ運用複雑

## 公式リンク

- **公式サイト**: [https://redis.io/](https://redis.io/)
- **ドキュメント**: [https://redis.io/docs/](https://redis.io/docs/)

## 関連ドキュメント

- [キャッシュツール一覧](../キャッシュツール/)
- [Memcached](./Memcached.md)

---

**カテゴリ**: キャッシュツール
**対象工程**: パフォーマンス最適化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
