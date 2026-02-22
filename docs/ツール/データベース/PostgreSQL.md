# PostgreSQL

## 概要

PostgreSQLは、オープンソースのオブジェクトリレーショナルデータベース管理システム（ORDBMS）です。SQL標準準拠、ACID準拠、JSONB、全文検索、外部キー、トリガー、ストアドプロシージャにより、複雑なクエリ、トランザクション、地理情報システム（PostGIS）を実現します。高度なSQL機能、拡張性、エンタープライズグレードで広く採用されています。

## 主な機能

### 1. ORDBMS
- **SQL標準**: 完全準拠
- **ACID**: 完全ACID準拠
- **データ型**: JSONB、Array、UUID等
- **拡張**: カスタム型、関数

### 2. 高度機能
- **外部キー**: リレーション整合性
- **トリガー**: イベント駆動
- **ビュー**: マテリアライズドビュー
- **CTEs**: WITH句、再帰クエリ

### 3. JSON
- **JSONB**: バイナリJSON
- **インデックス**: GINインデックス
- **クエリ**: JSONパス

### 4. 拡張
- **PostGIS**: 地理情報システム
- **pgcrypto**: 暗号化
- **pg_stat_statements**: クエリ分析

## 利用方法

### インストール（Docker）

```bash
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_USER=user \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  postgres:15

# 接続
psql -h localhost -U user -d mydb
```

### 基本操作

```sql
-- データベース作成
CREATE DATABASE mydb;
\c mydb

-- テーブル作成
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- データ挿入
INSERT INTO users (name, email, metadata)
VALUES ('Alice', 'alice@example.com', '{"age": 30, "city": "Tokyo"}');

-- データ取得
SELECT * FROM users;

-- JSONクエリ
SELECT name, metadata->>'age' AS age FROM users WHERE metadata->>'city' = 'Tokyo';

-- 更新
UPDATE users SET metadata = metadata || '{"verified": true}' WHERE id = 1;
```

### インデックス

```sql
-- B-Treeインデックス
CREATE INDEX idx_email ON users(email);

-- GINインデックス（JSONB）
CREATE INDEX idx_metadata ON users USING GIN (metadata);

-- 部分インデックス
CREATE INDEX idx_active_users ON users(email) WHERE metadata->>'active' = 'true';

-- インデックス確認
\di
```

### 全文検索

```sql
-- 全文検索カラム追加
ALTER TABLE articles ADD COLUMN tsv tsvector;

-- 全文検索インデックス
CREATE INDEX idx_tsv ON articles USING GIN(tsv);

-- 全文検索
UPDATE articles SET tsv = to_tsvector('english', title || ' ' || body);

SELECT * FROM articles WHERE tsv @@ to_tsquery('postgresql & database');
```

### レプリケーション設定

```sql
-- postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_size = 64

-- スタンバイ設定
primary_conninfo = 'host=primary-host port=5432 user=replicator password=secret'
```

### Python接続（psycopg2）

```python
import psycopg2
import json

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='user',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

# データ挿入
cursor.execute(
    "INSERT INTO users (name, email, metadata) VALUES (%s, %s, %s)",
    ('Bob', 'bob@example.com', json.dumps({"age": 25}))
)
conn.commit()

# データ取得
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
```

### Node.js接続（pg）

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  user: 'user',
  password: 'password',
  database: 'mydb'
});

async function main() {
  // データ挿入
  await pool.query(
    'INSERT INTO users (name, email, metadata) VALUES ($1, $2, $3)',
    ['Charlie', 'charlie@example.com', { age: 28 }]
  );

  // データ取得
  const result = await pool.query('SELECT * FROM users');
  console.log(result.rows);

  await pool.end();
}

main();
```

### バックアップ・リストア

```bash
# バックアップ
pg_dump -U user mydb > backup.sql

# リストア
psql -U user mydb < backup.sql

# カスタムフォーマット
pg_dump -U user -Fc mydb > backup.dump
pg_restore -U user -d mydb backup.dump
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **PostgreSQL** | 🟢 無料 | オープンソース、PostgreSQL License |
| **AWS RDS PostgreSQL** | 💰 従量課金 | マネージドPostgreSQL |
| **Azure Database for PostgreSQL** | 💰 従量課金 | マネージドPostgreSQL |
| **Google Cloud SQL PostgreSQL** | 💰 従量課金 | マネージドPostgreSQL |

## メリット

1. **無料**: オープンソース
2. **SQL標準**: 完全準拠
3. **高度機能**: CTE、ウィンドウ関数
4. **JSONB**: NoSQL的機能
5. **拡張性**: PostGIS、pgcrypto

## デメリット

1. **書き込み**: MySQLより遅い場合
2. **学習曲線**: 高度機能の学習
3. **メモリ**: メモリ消費大
4. **レプリケーション**: 設定複雑

## 公式リンク

- **公式サイト**: [https://www.postgresql.org/](https://www.postgresql.org/)
- **ドキュメント**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

## 関連ドキュメント

- [データベースツール一覧](../データベースツール/)
- [MySQL](./MySQL.md)
- [PostGIS](./PostGIS.md)

---

**カテゴリ**: データベースツール
**対象工程**: データ永続化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
