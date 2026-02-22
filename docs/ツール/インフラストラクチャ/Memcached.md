# Memcached

## 概要

Memcachedは、分散メモリオブジェクトキャッシュシステムです。Key-Value型、インメモリストレージ、LRU（Least Recently Used）削除、分散アーキテクチャにより、データベースクエリ、APIレスポンス、セッションデータのキャッシングを実現します。シンプル、高速、スケーラブルで広く採用されています。

## 主な機能

### 1. キャッシング
- **Key-Value**: シンプルなKV
- **インメモリ**: 高速アクセス
- **TTL**: 有効期限
- **LRU**: 自動削除

### 2. 分散
- **クライアント分散**: クライアント側ハッシング
- **一貫性ハッシング**: スケーラブル
- **マルチサーバー**: 複数ノード

### 3. プロトコル
- **テキスト**: ASCII プロトコル
- **バイナリ**: バイナリプロトコル
- **TCP/UDP**: 両対応

### 4. シンプル
- **軽量**: 軽量設計
- **高速**: マイクロ秒レベル
- **Easy**: 簡単セットアップ

## 利用方法

### インストール（Docker）

```bash
docker run -d --name memcached \
  -p 11211:11211 \
  memcached:latest

# メモリサイズ指定
docker run -d --name memcached \
  -p 11211:11211 \
  memcached:latest memcached -m 512
```

### Python（pymemcache）

```python
from pymemcache.client import base

# 接続
client = base.Client(('localhost', 11211))

# セット
client.set('key', 'value')
client.set('user:123', b'{"name": "Alice", "age": 30}', expire=3600)

# ゲット
value = client.get('key')
print(value)  # b'value'

# 削除
client.delete('key')

# インクリメント
client.set('counter', 0)
client.incr('counter', 1)  # 1
client.incr('counter', 5)  # 6

# 複数操作
client.set_many({'key1': 'value1', 'key2': 'value2'})
values = client.get_many(['key1', 'key2'])

client.close()
```

### Node.js（memjs）

```javascript
const memjs = require('memjs');

const client = memjs.Client.create('localhost:11211');

// セット
await client.set('key', 'value');
await client.set('user:123', JSON.stringify({ name: 'Bob', age: 25 }), { expires: 3600 });

// ゲット
const { value } = await client.get('key');
console.log(value.toString());  // 'value'

// 削除
await client.delete('key');

// インクリメント
await client.set('counter', '0');
await client.increment('counter', 1);

client.close();
```

### PHP

```php
<?php
$memcached = new Memcached();
$memcached->addServer('localhost', 11211);

// セット
$memcached->set('key', 'value');
$memcached->set('user:123', json_encode(['name' => 'Charlie', 'age' => 35]), 3600);

// ゲット
$value = $memcached->get('key');
echo $value;  // 'value'

// 削除
$memcached->delete('key');

// インクリメント
$memcached->set('counter', 0);
$memcached->increment('counter', 1);  // 1
$memcached->increment('counter', 5);  // 6

// 複数操作
$memcached->setMulti([
    'key1' => 'value1',
    'key2' => 'value2'
]);
$values = $memcached->getMulti(['key1', 'key2']);
?>
```

### Java（spymemcached）

```java
import net.spy.memcached.MemcachedClient;
import java.net.InetSocketAddress;

public class MemcachedExample {
    public static void main(String[] args) throws Exception {
        MemcachedClient client = new MemcachedClient(
            new InetSocketAddress("localhost", 11211)
        );

        // セット
        client.set("key", 3600, "value");
        client.set("user:123", 3600, "{\"name\":\"David\",\"age\":40}");

        // ゲット
        Object value = client.get("key");
        System.out.println(value);  // value

        // 削除
        client.delete("key");

        // インクリメント
        client.set("counter", 0, "0");
        client.incr("counter", 1);  // 1
        client.incr("counter", 5);  // 6

        client.shutdown();
    }
}
```

### 分散セットアップ

```python
from pymemcache.client.hash import HashClient

# 複数サーバー
servers = [
    ('server1', 11211),
    ('server2', 11211),
    ('server3', 11211)
]

client = HashClient(servers)

# 一貫性ハッシングで自動分散
client.set('key1', 'value1')  # server2に保存
client.set('key2', 'value2')  # server1に保存
client.set('key3', 'value3')  # server3に保存

value = client.get('key1')
client.close()
```

### セッションキャッシング（Express）

```javascript
const express = require('express');
const session = require('express-session');
const MemcachedStore = require('connect-memcached')(session);

const app = express();

app.use(session({
  secret: 'my-secret',
  resave: false,
  saveUninitialized: false,
  store: new MemcachedStore({
    hosts: ['localhost:11211'],
    secret: 'session-secret'
  })
}));

app.get('/', (req, res) => {
  if (req.session.views) {
    req.session.views++;
  } else {
    req.session.views = 1;
  }
  res.send(`Views: ${req.session.views}`);
});

app.listen(3000);
```

### Docker Compose（分散）

```yaml
version: '3.8'
services:
  memcached1:
    image: memcached:latest
    command: memcached -m 256
    ports:
      - "11211:11211"

  memcached2:
    image: memcached:latest
    command: memcached -m 256
    ports:
      - "11212:11211"

  memcached3:
    image: memcached:latest
    command: memcached -m 256
    ports:
      - "11213:11211"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Memcached** | 🟢 無料 | オープンソース、BSD License |
| **AWS ElastiCache Memcached** | 💰 従量課金 | マネージドMemcached |

## メリット

1. **無料**: オープンソース
2. **高速**: マイクロ秒レベル
3. **シンプル**: 簡単設定
4. **スケーラブル**: 分散アーキテクチャ
5. **軽量**: 低リソース

## デメリット

1. **永続化**: 非永続化
2. **データ型**: Key-Valueのみ
3. **レプリケーション**: 非対応
4. **クラスタリング**: クライアント側

## 公式リンク

- **公式サイト**: [https://memcached.org/](https://memcached.org/)
- **GitHub**: [https://github.com/memcached/memcached](https://github.com/memcached/memcached)

## 関連ドキュメント

- [キャッシュツール一覧](../キャッシュツール/)
- [Redis](./Redis.md)
- [Varnish](./Varnish.md)

---

**カテゴリ**: キャッシュツール
**対象工程**: パフォーマンス最適化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
