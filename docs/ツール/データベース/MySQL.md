# MySQL

## 概要

MySQLは、オープンソースのリレーショナルデータベース管理システム（RDBMS）です。SQL、ACID準拠、レプリケーション、パーティショニング、ストアドプロシージャにより、Webアプリケーション、エンタープライズシステムのデータ永続化を実現します。Oracle開発、高速、スケーラブル、LAMP/LEMP スタックで広く採用されています。

## 主な機能

### 1. RDBMS
- **SQL**: 標準SQL
- **ACID**: トランザクション
- **ストレージエンジン**: InnoDB、MyISAM
- **インデックス**: B-Tree、Hash

### 2. レプリケーション
- **マスター-スレーブ**: 非同期レプリケーション
- **マスター-マスター**: 双方向レプリケーション
- **Group Replication**: 自動フェイルオーバー

### 3. パフォーマンス
- **クエリキャッシュ**: キャッシング
- **パーティショニング**: 水平分割
- **インデックス**: 高速検索

### 4. セキュリティ
- **ユーザー管理**: 権限管理
- **SSL/TLS**: 暗号化通信
- **監査**: 監査ログ

## 利用方法

### インストール（Docker）

```bash
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=password \
  -p 3306:3306 \
  mysql:8.0

# 接続
mysql -h localhost -u user -p mydb
```

### 基本操作

```sql
-- データベース作成
CREATE DATABASE mydb;
USE mydb;

-- テーブル作成
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- データ挿入
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- データ取得
SELECT * FROM users;

-- 更新
UPDATE users SET name = 'Alice Smith' WHERE id = 1;

-- 削除
DELETE FROM users WHERE id = 1;
```

### インデックス

```sql
-- インデックス作成
CREATE INDEX idx_email ON users(email);

-- 複合インデックス
CREATE INDEX idx_name_email ON users(name, email);

-- ユニークインデックス
CREATE UNIQUE INDEX idx_unique_email ON users(email);

-- インデックス確認
SHOW INDEX FROM users;
```

### レプリケーション設定

```sql
-- マスター設定
-- my.cnf
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW

-- スレーブ設定
CHANGE MASTER TO
  MASTER_HOST='master-host',
  MASTER_USER='repl_user',
  MASTER_PASSWORD='password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=107;

START SLAVE;
SHOW SLAVE STATUS\G
```

### Python接続

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='user',
    password='password',
    database='mydb'
)

cursor = conn.cursor()

# データ挿入
cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ('Bob', 'bob@example.com'))
conn.commit()

# データ取得
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
```

### Node.js接続

```javascript
const mysql = require('mysql2/promise');

async function main() {
  const connection = await mysql.createConnection({
    host: 'localhost',
    user: 'user',
    password: 'password',
    database: 'mydb'
  });

  // データ挿入
  await connection.execute(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    ['Charlie', 'charlie@example.com']
  );

  // データ取得
  const [rows] = await connection.execute('SELECT * FROM users');
  console.log(rows);

  await connection.end();
}

main();
```

### バックアップ・リストア

```bash
# バックアップ
mysqldump -u user -p mydb > backup.sql

# リストア
mysql -u user -p mydb < backup.sql

# 全データベースバックアップ
mysqldump -u root -p --all-databases > all_backup.sql
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **MySQL Community** | 🟢 完全無料 | オープンソース、GPLv2 License |
| **MySQL Enterprise** | 💰 $5,000/年〜 | サポート、監視、バックアップ |
| **AWS RDS MySQL** | 💰 従量課金 | マネージドMySQL |
| **Azure Database for MySQL** | 💰 従量課金 | マネージドMySQL |

## メリット

1. **完全無料**: オープンソース
2. **成熟**: 長年の実績
3. **高速**: 読み取り高速
4. **エコシステム**: 豊富なツール
5. **LAMP/LEMP**: Web標準スタック

## デメリット

1. **複雑なクエリ**: PostgreSQLより遅い
2. **全文検索**: 限定的
3. **Oracle**: Oracle買収後の方向性
4. **ライセンス**: GPLv2制約

## 公式リンク

- **公式サイト**: [https://www.mysql.com/](https://www.mysql.com/)
- **ドキュメント**: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)

## 関連ドキュメント

- [データベースツール一覧](../データベースツール/)
- [PostgreSQL](./PostgreSQL.md)
- [MariaDB](./MariaDB.md)

---

**カテゴリ**: データベースツール
**対象工程**: データ永続化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
