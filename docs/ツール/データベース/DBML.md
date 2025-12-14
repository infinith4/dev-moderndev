# DBML (Database Markup Language)

## 概要

DBML（Database Markup Language）は、データベーススキーマを記述するためのオープンソースの DSL（ドメイン固有言語）です。人間が読みやすいシンプルな構文でテーブル、カラム、リレーションシップを定義し、ER図の自動生成やSQL DDLへの変換が可能です。dbdiagram.io が開発し、データベース設計のドキュメント化とビジュアライゼーションを効率化します。

## 主な特徴

### 1. シンプルな構文
- 直感的で読みやすい DSL
- 最小限のボイラープレート
- コードとしてのデータベース設計
- バージョン管理に最適

### 2. ビジュアライゼーション
- ER図の自動生成
- dbdiagram.io での可視化
- インタラクティブな図表
- PNG/PDF/SVG エクスポート

### 3. SQL 生成
- MySQL、PostgreSQL、SQL Server などの DDL 生成
- 逆方向のインポート（SQL → DBML）
- マイグレーションスクリプトの基盤
- ORM モデル生成のサポート

### 4. エコシステム
- CLI ツール（dbml-cli）
- プログラマティックな API
- VS Code 拡張機能
- CI/CD 統合

## 基本構文

### テーブル定義

```dbml
// 基本的なテーブル
Table users {
  id integer [primary key]
  username varchar(50) [not null, unique]
  email varchar(255) [unique]
  created_at timestamp [default: `now()`]
  status varchar(20) [default: 'active']

  Indexes {
    username [unique]
    email [unique]
    (created_at, status) [name: 'idx_created_status']
  }
}

// テーブルのエイリアスとノート
Table users as U {
  id integer [pk, increment] // primary key, auto-increment
  username varchar(50) [not null, unique, note: 'ユーザー名は一意']
  role_id integer [ref: > roles.id] // inline reference

  Note: 'ユーザーマスタテーブル'
}
```

### データ型

```dbml
Table data_types {
  // 数値型
  id integer [pk]
  age smallint
  salary bigint
  price decimal(10,2)
  rating float

  // 文字列型
  name varchar(100)
  description text
  status char(1)

  // 日付・時刻型
  created_at timestamp
  updated_at datetime
  birth_date date
  work_time time

  // 真偽値型
  is_active boolean

  // JSON型
  metadata json
  settings jsonb

  // その他
  file_data blob
  uuid_value uuid
}
```

### カラム属性

```dbml
Table products {
  id integer [
    pk,                    // primary key
    increment,             // auto-increment
    not null               // not null constraint
  ]

  name varchar(255) [
    not null,
    unique,
    default: 'Unnamed',
    note: '商品名'
  ]

  price decimal(10,2) [
    not null,
    default: 0.00,
    note: '価格（税込）'
  ]

  category_id integer [
    ref: > categories.id,  // foreign key
    note: 'カテゴリID'
  ]

  created_at timestamp [default: `now()`]
}
```

### リレーションシップ

```dbml
// 1対多（One-to-Many）
Ref: users.id < posts.user_id

// 多対1（Many-to-One）
Ref: posts.user_id > users.id

// 1対1（One-to-One）
Ref: users.id - user_profiles.user_id

// 多対多（Many-to-Many）
Ref: posts.id <> tags.id

// インライン定義
Table posts {
  id integer [pk]
  user_id integer [ref: > users.id]
  category_id integer [ref: > categories.id]
}

// 複合外部キー
Ref: order_items.(order_id, product_id) > products.(order_id, id)
```

### インデックス

```dbml
Table users {
  id integer [pk]
  email varchar(255)
  username varchar(50)
  created_at timestamp
  status varchar(20)

  Indexes {
    email [unique, name: 'idx_email']
    username [unique]
    (created_at, status) [name: 'idx_created_status']
    status [type: btree, note: 'ステータスインデックス']
  }
}
```

### Enum 型

```dbml
Enum user_status {
  active [note: 'アクティブユーザー']
  inactive
  suspended
  deleted
}

Enum order_status {
  pending
  processing
  completed
  cancelled
}

Table users {
  id integer [pk]
  status user_status [default: 'active']
}

Table orders {
  id integer [pk]
  status order_status [default: 'pending']
}
```

### テーブルグループ

```dbml
// テーブルをグループ化
TableGroup user_management {
  users
  user_profiles
  user_roles
}

TableGroup e_commerce {
  products
  orders
  order_items
}

Table users {
  id integer [pk]
}

Table user_profiles {
  id integer [pk]
  user_id integer [ref: - users.id]
}
```

### プロジェクト定義

```dbml
Project ecommerce_db {
  database_type: 'PostgreSQL'
  Note: 'Eコマースシステムのデータベーススキーマ'
}

Table users {
  // ...
}
```

## 実践例

### Eコマースシステム

```dbml
Project ecommerce {
  database_type: 'PostgreSQL'
  Note: 'Eコマースプラットフォーム'
}

// ユーザー管理
Table users {
  id integer [pk, increment]
  email varchar(255) [unique, not null]
  password_hash varchar(255) [not null]
  first_name varchar(50)
  last_name varchar(50)
  created_at timestamp [default: `now()`]
  updated_at timestamp

  Indexes {
    email [unique, name: 'idx_email']
  }

  Note: 'ユーザーマスタ'
}

Table user_profiles {
  id integer [pk, increment]
  user_id integer [ref: - users.id, not null, unique]
  phone varchar(20)
  address text
  city varchar(100)
  country varchar(100)
  postal_code varchar(20)

  Note: 'ユーザー詳細情報'
}

// 商品管理
Table categories {
  id integer [pk, increment]
  name varchar(100) [not null]
  slug varchar(100) [unique]
  parent_id integer [ref: > categories.id]
  created_at timestamp [default: `now()`]

  Note: 'カテゴリマスタ（階層構造）'
}

Table products {
  id integer [pk, increment]
  category_id integer [ref: > categories.id, not null]
  name varchar(255) [not null]
  slug varchar(255) [unique]
  description text
  price decimal(10,2) [not null]
  stock_quantity integer [default: 0]
  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
  updated_at timestamp

  Indexes {
    slug [unique]
    (category_id, is_active)
  }

  Note: '商品マスタ'
}

Table product_images {
  id integer [pk, increment]
  product_id integer [ref: > products.id, not null]
  image_url varchar(500) [not null]
  sort_order integer [default: 0]
  is_primary boolean [default: false]

  Indexes {
    (product_id, sort_order)
  }
}

// 注文管理
Enum order_status {
  pending
  processing
  shipped
  delivered
  cancelled
  refunded
}

Table orders {
  id integer [pk, increment]
  user_id integer [ref: > users.id, not null]
  status order_status [default: 'pending']
  total_amount decimal(10,2) [not null]
  shipping_address text [not null]
  billing_address text [not null]
  payment_method varchar(50)
  created_at timestamp [default: `now()`]
  updated_at timestamp

  Indexes {
    user_id
    (status, created_at)
  }

  Note: '注文ヘッダー'
}

Table order_items {
  id integer [pk, increment]
  order_id integer [ref: > orders.id, not null]
  product_id integer [ref: > products.id, not null]
  quantity integer [not null]
  unit_price decimal(10,2) [not null]
  subtotal decimal(10,2) [not null]

  Indexes {
    order_id
    product_id
  }

  Note: '注文明細'
}

// レビュー
Table reviews {
  id integer [pk, increment]
  product_id integer [ref: > products.id, not null]
  user_id integer [ref: > users.id, not null]
  rating integer [not null, note: '1-5の評価']
  comment text
  created_at timestamp [default: `now()`]

  Indexes {
    product_id
    user_id
    (product_id, rating)
  }
}

// テーブルグループ
TableGroup user_management {
  users
  user_profiles
}

TableGroup product_catalog {
  categories
  products
  product_images
}

TableGroup order_processing {
  orders
  order_items
}
```

### ブログシステム

```dbml
Project blog_system {
  database_type: 'MySQL'
  Note: 'ブログプラットフォームのスキーマ'
}

Table users {
  id integer [pk, increment]
  username varchar(50) [unique, not null]
  email varchar(255) [unique, not null]
  role varchar(20) [default: 'author']
  created_at timestamp [default: `now()`]
}

Table posts {
  id integer [pk, increment]
  author_id integer [ref: > users.id, not null]
  title varchar(255) [not null]
  slug varchar(255) [unique]
  content text [not null]
  excerpt text
  status varchar(20) [default: 'draft']
  published_at timestamp
  created_at timestamp [default: `now()`]
  updated_at timestamp

  Indexes {
    slug [unique]
    author_id
    (status, published_at)
  }
}

Table categories {
  id integer [pk, increment]
  name varchar(100) [unique, not null]
  slug varchar(100) [unique]
}

Table tags {
  id integer [pk, increment]
  name varchar(50) [unique, not null]
  slug varchar(50) [unique]
}

Table post_categories {
  post_id integer [ref: > posts.id]
  category_id integer [ref: > categories.id]

  Indexes {
    (post_id, category_id) [pk]
  }
}

Table post_tags {
  post_id integer [ref: > posts.id]
  tag_id integer [ref: > tags.id]

  Indexes {
    (post_id, tag_id) [pk]
  }
}

Table comments {
  id integer [pk, increment]
  post_id integer [ref: > posts.id, not null]
  user_id integer [ref: > users.id]
  parent_id integer [ref: > comments.id]
  content text [not null]
  created_at timestamp [default: `now()`]

  Indexes {
    post_id
    parent_id
  }
}
```

## ツールとエコシステム

### dbdiagram.io

```
公式 Web エディタ: https://dbdiagram.io/

機能:
- リアルタイムプレビュー
- ER図の自動生成
- SQL エクスポート
- PNG/PDF/SVG エクスポート
- 共有リンク生成
- インポート機能（SQL、Rails、Laravel等）

使い方:
1. https://dbdiagram.io/ にアクセス
2. DBML コードを入力
3. リアルタイムで図が更新される
4. Export メニューからSQLやPDFをダウンロード
```

### dbml-cli

```bash
# インストール
npm install -g @dbml/cli

# DBML → SQL 変換
dbml2sql schema.dbml --mysql -o schema.sql
dbml2sql schema.dbml --postgres -o schema.sql
dbml2sql schema.dbml --mssql -o schema.sql

# SQL → DBML 変換
sql2dbml schema.sql --mysql -o schema.dbml
sql2dbml schema.sql --postgres -o schema.dbml

# JSON 形式で出力
dbml2sql schema.dbml --postgres --json -o schema.json

# ヘルプ
dbml2sql --help
```

### VS Code 拡張機能

```
拡張機能名: DBML Language

機能:
- シンタックスハイライト
- コードスニペット
- エラー検出
- オートコンプリート
- フォーマッター

インストール:
1. VS Code の拡張機能マーケットプレイスで "DBML" を検索
2. インストール
3. .dbml ファイルを開く
```

### プログラマティック API

```javascript
// JavaScript/TypeScript での使用
const { Parser, exporter } = require('@dbml/core');

// DBML のパース
const dbml = `
  Table users {
    id integer [pk]
    username varchar(50)
  }
`;

const database = Parser.parse(dbml, 'dbml');

// PostgreSQL にエクスポート
const sql = exporter.export(database, 'postgres');
console.log(sql);

// MySQL にエクスポート
const mysqlSql = exporter.export(database, 'mysql');
console.log(mysqlSql);

// JSON にエクスポート
const json = JSON.stringify(database, null, 2);
console.log(json);
```

### Python での使用

```python
# pydbml パッケージ
pip install pydbml

# 使用例
from pydbml import PyDBML

# DBML ファイルの読み込み
parsed = PyDBML(open('schema.dbml').read())

# テーブル情報の取得
for table in parsed.tables:
    print(f"Table: {table.name}")
    for column in table.columns:
        print(f"  - {column.name}: {column.type}")

# SQL 生成
sql = parsed.to_sql('postgres')
print(sql)
```

## SQL エクスポート

### PostgreSQL

```bash
dbml2sql schema.dbml --postgres -o schema.sql
```

```sql
-- 生成される SQL（例）
CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar(50) UNIQUE NOT NULL,
  "email" varchar(255) UNIQUE,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "posts" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer NOT NULL,
  "title" varchar(255) NOT NULL,
  "content" text
);

CREATE INDEX ON "users" ("username");

ALTER TABLE "posts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
```

### MySQL

```bash
dbml2sql schema.dbml --mysql -o schema.sql
```

```sql
-- 生成される SQL（例）
CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(50) UNIQUE NOT NULL,
  `email` varchar(255) UNIQUE,
  `created_at` timestamp DEFAULT (now())
);

CREATE TABLE `posts` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text
);

CREATE INDEX `idx_username` ON `users` (`username`);

ALTER TABLE `posts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
```

## CI/CD 統合

### GitHub Actions

```yaml
name: Database Schema Validation

on:
  pull_request:
    paths:
      - 'db/schema.dbml'

jobs:
  validate-schema:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dbml-cli
      run: npm install -g @dbml/cli

    - name: Validate DBML Syntax
      run: |
        dbml2sql db/schema.dbml --postgres --dry-run

    - name: Generate SQL
      run: |
        dbml2sql db/schema.dbml --postgres -o db/schema.sql

    - name: Generate MySQL SQL
      run: |
        dbml2sql db/schema.dbml --mysql -o db/schema_mysql.sql

    - name: Upload Artifacts
      uses: actions/upload-artifact@v3
      with:
        name: sql-schemas
        path: |
          db/schema.sql
          db/schema_mysql.sql

    - name: Generate ER Diagram
      run: |
        # dbdiagram.io API を使用（要 API キー）
        # または他の ER 図生成ツールを使用
```

### GitLab CI

```yaml
stages:
  - validate
  - generate

validate_dbml:
  stage: validate
  image: node:18
  before_script:
    - npm install -g @dbml/cli
  script:
    - dbml2sql db/schema.dbml --postgres --dry-run
  only:
    changes:
      - db/schema.dbml

generate_sql:
  stage: generate
  image: node:18
  before_script:
    - npm install -g @dbml/cli
  script:
    - dbml2sql db/schema.dbml --postgres -o db/schema.sql
    - dbml2sql db/schema.dbml --mysql -o db/schema_mysql.sql
  artifacts:
    paths:
      - db/*.sql
    expire_in: 30 days
  only:
    - main
```

## マイグレーションツールとの統合

### Alembic (Python)

```python
# alembic/versions/001_initial.py
from alembic import op
import sqlalchemy as sa

# DBML から生成した SQL を元に
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

def downgrade():
    op.drop_table('users')
```

### Flyway (Java)

```sql
-- V1__initial_schema.sql
-- DBML から生成
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username varchar(50) UNIQUE NOT NULL,
  email varchar(255) UNIQUE,
  created_at timestamp DEFAULT now()
);
```

### Django (Python)

```python
# models.py を DBML から生成
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
        ]
```

## ベストプラクティス

### 1. ファイル構成

```
project/
├── db/
│   ├── schema.dbml           # メインスキーマ
│   ├── schema.sql            # 生成された SQL
│   └── modules/              # モジュール分割
│       ├── users.dbml
│       ├── products.dbml
│       └── orders.dbml
├── docs/
│   └── er-diagram.png        # ER図
└── README.md
```

### 2. コメントの活用

```dbml
Table users {
  id integer [pk, increment]
  username varchar(50) [not null, note: '''
    ユーザー名
    - 3文字以上50文字以内
    - 英数字とアンダースコアのみ
    - 一意である必要がある
  ''']

  Note: '''
  ## ユーザーマスタテーブル

  アプリケーションのユーザー情報を管理する中核テーブル

  ### 制約
  - username は一意
  - email は一意（オプショナル）

  ### 関連テーブル
  - user_profiles: 1対1
  - posts: 1対多
  - orders: 1対多
  '''
}
```

### 3. バージョン管理

```dbml
Project myapp {
  database_type: 'PostgreSQL'
  Note: '''
  Version: 2.0.0
  Last Updated: 2024-01-15
  Author: Database Team
  '''
}
```

### 4. 命名規則

```dbml
// テーブル名: 複数形、スネークケース
Table user_profiles { }
Table order_items { }

// カラム名: スネークケース
Table users {
  id integer [pk]
  first_name varchar(50)
  created_at timestamp
  is_active boolean
}

// インデックス名: idx_ プレフィックス
Indexes {
  (email) [name: 'idx_email']
  (username, created_at) [name: 'idx_username_created']
}
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://www.dbml.org/
- ドキュメント: https://www.dbml.org/docs/
- dbdiagram.io: https://dbdiagram.io/
- GitHub: https://github.com/holistics/dbml

### ツール
- dbml-cli: https://www.npmjs.com/package/@dbml/cli
- VS Code Extension: https://marketplace.visualstudio.com/items?itemName=matt-meyers.vscode-dbml
- pydbml: https://pypi.org/project/pydbml/

### チュートリアル
- Getting Started: https://www.dbml.org/docs/#intro
- Syntax Guide: https://www.dbml.org/docs/#table-definition
- Examples: https://dbdiagram.io/d

## まとめ

DBML は、以下の場面で特に有用です:

1. **データベース設計のドキュメント化** - 人間が読みやすい形式でスキーマを記述
2. **ER図の自動生成** - コードから図を生成し、常に最新の状態を維持
3. **チーム協業** - Git によるバージョン管理、レビュー、マージ
4. **マルチデータベース対応** - 複数のDBMSに対応したSQL生成

シンプルで強力な DSL により、データベース設計を「コードとして」管理し、開発ワークフローに統合できます。
