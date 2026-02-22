# MongoDB

## 概要

MongoDBは、ドキュメント指向NoSQLデータベースです。BSON（Binary JSON）、スキーマレス、レプリカセット、シャーディング、集計パイプラインにより、柔軟なデータモデル、水平スケール、リアルタイムアプリケーションを実現します。MongoDB Inc.開発、高パフォーマンス、MEAN/MERNスタックで広く採用されています。

## 主な機能

### 1. ドキュメント指向
- **BSON**: JSONライク
- **スキーマレス**: 柔軟な構造
- **埋め込み**: ネストドキュメント
- **配列**: 配列フィールド

### 2. クエリ
- **リッチクエリ**: フィールド、範囲、正規表現
- **インデックス**: 単一、複合、地理空間
- **集計パイプライン**: $match、$group、$project
- **全文検索**: テキスト検索

### 3. スケーリング
- **レプリカセット**: 自動フェイルオーバー
- **シャーディング**: 水平スケール
- **負荷分散**: 自動バランシング

### 4. トランザクション
- **ACID**: マルチドキュメントトランザクション
- **セッション**: トランザクションセッション

## 利用方法

### インストール（Docker）

```bash
docker run -d --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -p 27017:27017 \
  mongo:7.0

# 接続
mongosh --username admin --password secret
```

### 基本操作

```javascript
// データベース切り替え
use mydb

// コレクション作成・ドキュメント挿入
db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  age: 30,
  tags: ["developer", "javascript"],
  address: {
    city: "Tokyo",
    country: "Japan"
  }
})

// 複数ドキュメント挿入
db.users.insertMany([
  { name: "Bob", email: "bob@example.com", age: 25 },
  { name: "Charlie", email: "charlie@example.com", age: 35 }
])

// 検索
db.users.find()
db.users.find({ age: { $gte: 30 } })
db.users.find({ "address.city": "Tokyo" })

// 更新
db.users.updateOne(
  { name: "Alice" },
  { $set: { age: 31 }, $push: { tags: "mongodb" } }
)

// 削除
db.users.deleteOne({ name: "Bob" })
```

### インデックス

```javascript
// 単一フィールドインデックス
db.users.createIndex({ email: 1 })

// 複合インデックス
db.users.createIndex({ name: 1, age: -1 })

// ユニークインデックス
db.users.createIndex({ email: 1 }, { unique: true })

// テキストインデックス
db.articles.createIndex({ title: "text", body: "text" })

// インデックス確認
db.users.getIndexes()
```

### 集計パイプライン

```javascript
db.orders.aggregate([
  // フィルター
  { $match: { status: "completed" } },

  // グループ化
  { $group: {
    _id: "$customerId",
    totalAmount: { $sum: "$amount" },
    count: { $sum: 1 }
  }},

  // ソート
  { $sort: { totalAmount: -1 } },

  // 制限
  { $limit: 10 }
])
```

### Node.js接続

```javascript
const { MongoClient } = require('mongodb');

const uri = 'mongodb://admin:secret@localhost:27017';
const client = new MongoClient(uri);

async function main() {
  await client.connect();
  const db = client.db('mydb');
  const users = db.collection('users');

  // 挿入
  await users.insertOne({
    name: 'David',
    email: 'david@example.com',
    age: 28
  });

  // 検索
  const result = await users.find({ age: { $gte: 25 } }).toArray();
  console.log(result);

  // 更新
  await users.updateOne(
    { name: 'David' },
    { $set: { age: 29 } }
  );

  await client.close();
}

main();
```

### Python接続（pymongo）

```python
from pymongo import MongoClient

client = MongoClient('mongodb://admin:secret@localhost:27017/')
db = client['mydb']
users = db['users']

# 挿入
users.insert_one({
    'name': 'Eve',
    'email': 'eve@example.com',
    'age': 27
})

# 検索
for user in users.find({'age': {'$gte': 25}}):
    print(user)

# 更新
users.update_one(
    {'name': 'Eve'},
    {'$set': {'age': 28}}
)

# 削除
users.delete_one({'name': 'Eve'})

client.close()
```

### レプリカセット設定

```yaml
# docker-compose.yml
version: '3.8'
services:
  mongo1:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27017:27017"

  mongo2:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27018:27017"

  mongo3:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27019:27017"
```

```javascript
// レプリカセット初期化
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
```

### トランザクション

```javascript
const session = client.startSession();

try {
  await session.withTransaction(async () => {
    await accounts.updateOne(
      { _id: 1 },
      { $inc: { balance: -100 } },
      { session }
    );

    await accounts.updateOne(
      { _id: 2 },
      { $inc: { balance: 100 } },
      { session }
    );
  });
} finally {
  await session.endSession();
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **MongoDB Community** | 🟢 無料 | オープンソース、SSPL License |
| **MongoDB Atlas** | 🟢 無料枠あり | マネージドMongoDB、512MB無料 |
| **MongoDB Enterprise** | 💰 商用ライセンス | エンタープライズ機能 |

## メリット

1. **無料**: オープンソース
2. **スキーマレス**: 柔軟なデータ構造
3. **スケーラブル**: シャーディング
4. **高パフォーマンス**: 高速読み書き
5. **MEAN/MERN**: Webスタック標準

## デメリット

1. **メモリ**: メモリ消費大
2. **トランザクション**: RDBMS比較で制限
3. **ディスク**: ディスク使用量大
4. **ライセンス**: SSPL議論

## 公式リンク

- **公式サイト**: [https://www.mongodb.com/](https://www.mongodb.com/)
- **ドキュメント**: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)

## 関連ドキュメント

- [NoSQLデータベースツール一覧](../NoSQLデータベースツール/)
- [Redis](../キャッシュツール/Redis.md)
- [Cassandra](./Cassandra.md)

---

**カテゴリ**: NoSQLデータベースツール
**対象工程**: データ永続化・NoSQL
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
