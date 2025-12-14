# Apache Cassandra

## 概要

**Apache Cassandra**は、高可用性・スケーラビリティを重視した分散NoSQLデータベースです。単一障害点なしのP2Pアーキテクチャ、線形スケーラビリティ、マルチデータセンター対応により、大規模・高トラフィックアプリケーションのデータ管理を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Apache Software Foundation |
| **種別** | 分散NoSQLデータベース（Wide Column Store） |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://cassandra.apache.org/ |
| **ドキュメント** | https://cassandra.apache.org/doc/latest/ |

## 主な特徴

### 1. 分散アーキテクチャ
- **P2Pトポロジー**: マスター不要、全ノード対等
- **単一障害点なし**: 任意ノード障害でも動作継続
- **線形スケーラビリティ**: ノード追加で性能向上
- **マルチデータセンター**: 地理的分散レプリケーション

### 2. 高可用性
- **レプリケーション**: データ複製（RF: Replication Factor）
- **整合性調整**: Eventual Consistency、Tunable Consistency
- **自動修復**: Hinted Handoff、Read Repair、Anti-Entropy Repair
- **ダウンタイムゼロ**: ローリングアップグレード

### 3. 高パフォーマンス
- **書き込み最適化**: LSM-Tree（Log-Structured Merge-Tree）
- **パーティショニング**: Consistent Hashing
- **圧縮**: LZ4、Snappy、Deflate
- **SSD最適化**: I/O効率化

### 4. CQL（Cassandra Query Language）
- SQL類似の構文
- プライマリーキー・セカンダリーインデックス
- バッチ処理
- UDF（User Defined Functions）

## 使い方

### セットアップ

#### Docker で起動

```bash
# Cassandra コンテナ起動
docker run --name cassandra -d \
  -p 9042:9042 \
  -e CASSANDRA_CLUSTER_NAME=MyCluster \
  cassandra:4.1

# CQLSHで接続
docker exec -it cassandra cqlsh

# または、ローカルからcqlsh
cqlsh localhost 9042
```

#### Linux インストール

```bash
# Javaインストール（OpenJDK 11推奨）
sudo apt update
sudo apt install openjdk-11-jdk

# Cassandraリポジトリ追加
echo "deb https://debian.cassandra.apache.org 41x main" | sudo tee /etc/apt/sources.list.d/cassandra.list
curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -

# Cassandraインストール
sudo apt update
sudo apt install cassandra

# サービス起動
sudo systemctl start cassandra
sudo systemctl enable cassandra

# ステータス確認
sudo systemctl status cassandra
nodetool status

# CQLSHで接続
cqlsh
```

#### 設定ファイル

```yaml
# /etc/cassandra/cassandra.yaml（主要設定）

cluster_name: 'MyCluster'

# データディレクトリ
data_file_directories:
  - /var/lib/cassandra/data

# コミットログディレクトリ
commitlog_directory: /var/lib/cassandra/commitlog

# リッスンアドレス
listen_address: localhost
rpc_address: localhost

# ポート
native_transport_port: 9042

# シード（クラスター構成時）
seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
      - seeds: "192.168.1.10,192.168.1.11,192.168.1.12"
```

### CQL 基本操作

#### キースペース（データベース）

```sql
-- キースペース作成
CREATE KEYSPACE IF NOT EXISTS myapp
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

-- キースペース使用
USE myapp;

-- キースペース一覧
DESCRIBE KEYSPACES;

-- キースペース詳細
DESCRIBE KEYSPACE myapp;

-- キースペース削除
DROP KEYSPACE myapp;
```

#### テーブル作成

```sql
-- ユーザーテーブル
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  email TEXT,
  name TEXT,
  age INT,
  created_at TIMESTAMP
);

-- 複合プライマリーキー
CREATE TABLE user_posts (
  user_id UUID,
  post_id TIMEUUID,
  title TEXT,
  content TEXT,
  created_at TIMESTAMP,
  PRIMARY KEY (user_id, post_id)
) WITH CLUSTERING ORDER BY (post_id DESC);

-- セカンダリインデックス
CREATE INDEX ON users (email);

-- テーブル一覧
DESCRIBE TABLES;

-- テーブル詳細
DESCRIBE TABLE users;
```

#### データ操作（CRUD）

```sql
-- INSERT
INSERT INTO users (user_id, email, name, age, created_at)
VALUES (uuid(), 'user@example.com', 'John Doe', 30, toTimestamp(now()));

-- SELECT
SELECT * FROM users;
SELECT user_id, email, name FROM users WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;

-- UPDATE
UPDATE users SET age = 31 WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;

-- DELETE
DELETE FROM users WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;

-- BATCH（複数操作のアトミック実行）
BEGIN BATCH
  INSERT INTO users (user_id, email, name) VALUES (uuid(), 'user1@example.com', 'User 1');
  INSERT INTO users (user_id, email, name) VALUES (uuid(), 'user2@example.com', 'User 2');
APPLY BATCH;
```

#### クエリ

```sql
-- WHERE句（プライマリーキーのみ）
SELECT * FROM user_posts WHERE user_id = 123e4567-e89b-12d3-a456-426614174000;

-- ALLOW FILTERING（非推奨、全スキャン）
SELECT * FROM users WHERE age > 25 ALLOW FILTERING;

-- LIMIT
SELECT * FROM users LIMIT 10;

-- ORDER BY（クラスタリングキーのみ）
SELECT * FROM user_posts WHERE user_id = 123e4567-e89b-12d3-a456-426614174000
ORDER BY post_id DESC;

-- COUNT
SELECT COUNT(*) FROM users;

-- TTL（Time To Live）
INSERT INTO users (user_id, email, name) VALUES (uuid(), 'temp@example.com', 'Temp User')
USING TTL 3600;  -- 1時間後に自動削除
```

### アプリケーション統合

#### Python（cassandra-driver）

```python
# requirements.txt
cassandra-driver

# app.py
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

# 接続
auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
cluster = Cluster(['localhost'], auth_provider=auth_provider)
session = cluster.connect('myapp')

# INSERT
user_id = uuid.uuid4()
session.execute(
    """
    INSERT INTO users (user_id, email, name, age)
    VALUES (%s, %s, %s, %s)
    """,
    (user_id, 'user@example.com', 'John Doe', 30)
)

# SELECT
rows = session.execute("SELECT * FROM users WHERE user_id = %s", [user_id])
for row in rows:
    print(f"User: {row.name}, Email: {row.email}")

# プリペアドステートメント（パフォーマンス向上）
prepared = session.prepare("SELECT * FROM users WHERE user_id = ?")
result = session.execute(prepared, [user_id])

# 非同期実行
future = session.execute_async("SELECT * FROM users")
rows = future.result()

# クローズ
cluster.shutdown()
```

#### Java（Datastax Driver）

```java
// pom.xml
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-core</artifactId>
    <version>4.15.0</version>
</dependency>

// CassandraExample.java
import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.ResultSet;
import com.datastax.oss.driver.api.core.cql.Row;
import java.net.InetSocketAddress;
import java.util.UUID;

public class CassandraExample {
    public static void main(String[] args) {
        // 接続
        try (CqlSession session = CqlSession.builder()
                .addContactPoint(new InetSocketAddress("localhost", 9042))
                .withLocalDatacenter("datacenter1")
                .withKeyspace("myapp")
                .build()) {

            // INSERT
            UUID userId = UUID.randomUUID();
            session.execute(
                "INSERT INTO users (user_id, email, name, age) VALUES (?, ?, ?, ?)",
                userId, "user@example.com", "John Doe", 30
            );

            // SELECT
            ResultSet rs = session.execute(
                "SELECT * FROM users WHERE user_id = ?",
                userId
            );

            for (Row row : rs) {
                System.out.println("Name: " + row.getString("name"));
            }
        }
    }
}
```

#### Node.js（cassandra-driver）

```javascript
// package.json
// "cassandra-driver": "^4.7.0"

// app.js
const cassandra = require('cassandra-driver');

// 接続
const client = new cassandra.Client({
  contactPoints: ['localhost'],
  localDataCenter: 'datacenter1',
  keyspace: 'myapp'
});

async function main() {
  await client.connect();

  // INSERT
  const userId = cassandra.types.Uuid.random();
  await client.execute(
    'INSERT INTO users (user_id, email, name, age) VALUES (?, ?, ?, ?)',
    [userId, 'user@example.com', 'John Doe', 30],
    { prepare: true }
  );

  // SELECT
  const result = await client.execute(
    'SELECT * FROM users WHERE user_id = ?',
    [userId],
    { prepare: true }
  );

  result.rows.forEach(row => {
    console.log('User:', row.name, 'Email:', row.email);
  });

  await client.shutdown();
}

main().catch(console.error);
```

### クラスター構成

```yaml
# 3ノードクラスター（各ノードの設定）

# Node 1 (192.168.1.10)
cluster_name: 'MyCluster'
listen_address: 192.168.1.10
rpc_address: 192.168.1.10
seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
      - seeds: "192.168.1.10,192.168.1.11"

# Node 2 (192.168.1.11)
cluster_name: 'MyCluster'
listen_address: 192.168.1.11
rpc_address: 192.168.1.11
seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
      - seeds: "192.168.1.10,192.168.1.11"

# Node 3 (192.168.1.12)
cluster_name: 'MyCluster'
listen_address: 192.168.1.12
rpc_address: 192.168.1.12
seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
      - seeds: "192.168.1.10,192.168.1.11"
```

```bash
# クラスターステータス確認
nodetool status

# 出力例:
# Datacenter: datacenter1
# =======================
# Status=Up/Down
# |/ State=Normal/Leaving/Joining/Moving
# --  Address        Load       Tokens  Owns    Host ID                               Rack
# UN  192.168.1.10   100 KB     256     33.3%   abc123...                             rack1
# UN  192.168.1.11   95 KB      256     33.3%   def456...                             rack1
# UN  192.168.1.12   98 KB      256     33.4%   ghi789...                             rack1
```

### 整合性レベル

```sql
-- 整合性レベル設定
CONSISTENCY QUORUM;  -- 読み書き共に過半数

-- 読み取り整合性レベル
-- ONE: 1ノードから応答
-- QUORUM: 過半数ノードから応答
-- ALL: 全ノードから応答

-- 書き込み整合性レベル
-- ANY: 少なくとも1ノード（Hinted Handoff含む）
-- ONE: 1ノードに書き込み
-- QUORUM: 過半数ノードに書き込み
-- ALL: 全ノードに書き込み
```

### バックアップ・復元

```bash
# スナップショット作成
nodetool snapshot -t backup_20250106 myapp

# スナップショット確認
nodetool listsnapshots

# スナップショット削除
nodetool clearsnapshot -t backup_20250106

# データディレクトリからスナップショットコピー
# /var/lib/cassandra/data/myapp/users-*/snapshots/backup_20250106/

# 復元（スナップショットからコピー）
# 1. Cassandra停止
# 2. スナップショットをdataディレクトリにコピー
# 3. Cassandra起動
# 4. nodetool repair
```

### モニタリング

```bash
# nodetoolコマンド

# ステータス
nodetool status

# 統計情報
nodetool info
nodetool tpstats  # Thread Pool統計
nodetool cfstats  # テーブル統計

# 圧縮状況
nodetool compactionstats

# ヒープ使用状況
nodetool gcstats

# 修復
nodetool repair
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | スケーラビリティ設計 | 分散DB要件定義 |
| **設計** | データモデリング | パーティション設計 |
| **実装** | アプリ開発 | CQLクエリ実装 |
| **運用** | スケールアウト | ノード追加・運用 |

## メリット

- **高可用性**: 単一障害点なし、自動フェイルオーバー
- **線形スケーラビリティ**: ノード追加で性能向上
- **書き込み性能**: LSM-Treeで高速書き込み
- **マルチデータセンター**: 地理的分散対応
- **CQL**: SQL類似で学習容易
- **オープンソース**: 無料、カスタマイズ可能

## デメリット

- **JOIN不可**: 非正規化設計必須
- **トランザクション制限**: ACID保証弱い（Lightweight Transaction除く）
- **ディスク消費**: レプリケーションで増加
- **運用複雑**: クラスター管理、チューニングが必要
- **学習曲線**: データモデリング、整合性モデルの理解
- **クエリ制限**: プライマリーキー以外の検索困難

## 類似ツールとの比較

| ツール | 特徴 | 整合性 | 適用場面 |
|--------|------|--------|----------|
| **Cassandra** | 書き込み重視、線形スケール | Eventual | 大規模書き込み |
| **MongoDB** | ドキュメント、柔軟 | Strong | 柔軟なスキーマ |
| **HBase** | Hadoop統合 | Strong | ビッグデータ分析 |
| **DynamoDB** | AWS管理、低レイテンシ | Eventual | AWSエコシステム |

## ベストプラクティス

### 1. データモデリング

```sql
-- ❌ 悪い例（JOIN前提）
-- users テーブル
-- posts テーブル（外部キー: user_id）

-- ✅ 良い例（非正規化、クエリ駆動設計）
CREATE TABLE user_posts (
  user_id UUID,
  post_id TIMEUUID,
  title TEXT,
  content TEXT,
  PRIMARY KEY (user_id, post_id)
);

-- ユーザーごとの投稿取得が高速
SELECT * FROM user_posts WHERE user_id = ?;
```

### 2. パーティションキー設計

```sql
-- ❌ ホットパーティション（全データが1パーティション）
CREATE TABLE logs (
  log_type TEXT,
  timestamp TIMESTAMP,
  message TEXT,
  PRIMARY KEY (log_type, timestamp)
);

-- ✅ パーティション分散
CREATE TABLE logs (
  date TEXT,       -- 日付でパーティション分割
  log_type TEXT,
  timestamp TIMESTAMP,
  message TEXT,
  PRIMARY KEY ((date, log_type), timestamp)
);
```

### 3. 整合性レベル

```text
# R + W > RF（強整合性）
# R=QUORUM, W=QUORUM, RF=3
# → 読み書き共に過半数で強整合性

# R=1, W=1, RF=3（高速、結果整合性）
# → 高スループット、最終的整合性
```

## 公式リソース

- **公式サイト**: https://cassandra.apache.org/
- **ドキュメント**: https://cassandra.apache.org/doc/latest/
- **DataStax Academy**: https://www.datastax.com/dev/datastax-academy（無料コース）
- **GitHub**: https://github.com/apache/cassandra
- **Planet Cassandra**: https://planetcassandra.org/

## まとめ

Apache Cassandraは、高可用性・スケーラビリティを重視した分散NoSQLデータベースです。P2Pアーキテクチャ、線形スケーラビリティ、マルチデータセンター対応により、大規模・高トラフィックアプリケーションのデータ管理を実現します。Instagram、Netflix、Apple等の大規模サービスで採用されており、書き込み重視・高可用性要件に最適なデータベースです。

---

**最終更新**: 2025-12-06
**対象バージョン**: Apache Cassandra 4.1+
