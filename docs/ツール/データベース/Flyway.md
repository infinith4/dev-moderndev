# Flyway

## 概要

Flywayは、データベーススキーマのバージョン管理とマイグレーションを自動化するオープンソースツールです。SQLベースのマイグレーションスクリプトを管理し、データベーススキーマの変更を追跡、適用します。

**主な特徴:**
- シンプルなSQLベースのマイグレーション
- バージョン管理とマイグレーション履歴の追跡
- 複数データベース対応（Oracle、SQL Server、PostgreSQL、MySQL等）
- コマンドライン、Java API、Maven/Gradleプラグイン対応
- クリーンなロールバック機能（有料版）
- チーム開発でのスキーマ競合検知
- CI/CDパイプラインへの統合が容易

## 料金プラン

| プラン | 料金 | 主な機能 |
|--------|------|----------|
| **Community Edition** | 無料 | 基本マイグレーション、バージョン管理、主要DB対応 |
| **Teams** | $350/年（5開発者） | リピータブルマイグレーション、ドライラン、複数スキーマ |
| **Enterprise** | 要問合せ | ロールバック、エラーオーバーライド、優先サポート |

※ Community Editionで多くの機能が利用可能

## メリット・デメリット

### メリット

1. **シンプルなSQL**: 学習コストが低く、既存のSQL知識で使える
2. **軽量**: 依存関係が少なく、導入が容易
3. **バージョン管理**: データベーススキーマの変更履歴を管理
4. **マルチDB対応**: 主要な商用・OSSデータベースをサポート
5. **CI/CD統合**: パイプラインに組み込みやすい
6. **べき等性**: 同じマイグレーションを複数回実行しても安全
7. **チーム開発**: 複数開発者のスキーマ変更を自動統合
8. **オープンソース**: Community Editionは無料

### デメリット

1. **ロールバック制限**: Community版ではロールバック機能なし
2. **複雑な変更**: 大規模なデータ移行は手動対応が必要
3. **競合解決**: 並行開発でのマイグレーション競合は手動解決
4. **テスト環境**: 本番前のテストが必須
5. **初回導入**: 既存データベースへの適用には準備が必要

## 利用できる開発工程

| 工程 | 活用度 | 主な用途 |
|------|--------|----------|
| 企画プロセス | ⭐ | データモデルの初期設計 |
| 要件定義 | ⭐⭐ | データ要件の定義 |
| アーキテクチャ設計 | ⭐⭐⭐⭐ | データベース設計、マイグレーション戦略 |
| 詳細設計 | ⭐⭐⭐⭐⭐ | テーブル設計、スキーマ設計 |
| 開発 | ⭐⭐⭐⭐⭐ | スキーマ変更、マイグレーション実行 |
| テスト | ⭐⭐⭐⭐⭐ | テストDB構築、データ準備 |
| リリース | ⭐⭐⭐⭐⭐ | 本番DBマイグレーション |
| 運用・保守 | ⭐⭐⭐⭐ | スキーマ修正、データ修正 |

## 基本的な利用方法

### 1. インストール

```bash
# コマンドラインツールのインストール

# macOS (Homebrew)
brew install flyway

# Windows (Chocolatey)
choco install flyway-commandline

# Linux (手動ダウンロード)
wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.22.3/flyway-commandline-9.22.3-linux-x64.tar.gz | tar xvz && sudo ln -s `pwd`/flyway-9.22.3/flyway /usr/local/bin

# Docker
docker pull flyway/flyway
```

**Maven依存関係:**
```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
    <version>9.22.3</version>
</dependency>

<!-- MySQLの場合 -->
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-mysql</artifactId>
    <version>9.22.3</version>
</dependency>
```

**Gradle依存関係:**
```gradle
dependencies {
    implementation 'org.flywaydb:flyway-core:9.22.3'
    implementation 'org.flywaydb:flyway-mysql:9.22.3'
}
```

### 2. プロジェクト構成

```
project/
├── src/
│   └── main/
│       └── resources/
│           └── db/
│               └── migration/
│                   ├── V1__Create_users_table.sql
│                   ├── V2__Add_email_to_users.sql
│                   ├── V3__Create_orders_table.sql
│                   └── R__View_active_users.sql
├── flyway.conf
└── pom.xml or build.gradle
```

### 3. 設定ファイル

```properties
# flyway.conf
flyway.url=jdbc:postgresql://localhost:5432/mydb
flyway.user=postgres
flyway.password=secret
flyway.schemas=public
flyway.locations=filesystem:./sql,classpath:db/migration
```

```yaml
# application.yml (Spring Boot)
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
    baseline-version: 0
    url: jdbc:postgresql://localhost:5432/mydb
    user: postgres
    password: secret
    schemas: public
```

### 4. マイグレーションスクリプト

**バージョン管理マイグレーション（V__）:**
```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
```

```sql
-- V2__Add_email_verification.sql
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN verification_token VARCHAR(255);
```

**リピータブルマイグレーション（R__）:**
```sql
-- R__View_active_users.sql
CREATE OR REPLACE VIEW active_users AS
SELECT
    id,
    username,
    email,
    created_at
FROM users
WHERE email_verified = TRUE
ORDER BY created_at DESC;
```

### 5. 基本コマンド

```bash
# マイグレーション情報の確認
flyway info

# 未適用のマイグレーションを実行
flyway migrate

# データベースをクリーン（全データ削除）
flyway clean

# 現在の状態をベースラインとして設定
flyway baseline

# スキーマの検証
flyway validate

# マイグレーションの修復（失敗したマイグレーションの記録を削除）
flyway repair
```

## 工程別の活用方法

### アーキテクチャ設計での活用

**マイグレーション戦略:**
```
環境別戦略:
1. 開発環境
   - flyway clean + migrate で毎回クリーン構築
   - テストデータもマイグレーションで投入

2. ステージング環境
   - 本番を模擬したマイグレーションテスト
   - ロールバックテスト（Enterprise版）

3. 本番環境
   - baseline設定で既存DBに導入
   - ダウンタイムを最小化する戦略
   - バックアップ必須
```

**マルチスキーマ設計:**
```properties
# 複数スキーマの管理
flyway.schemas=public,app,audit
flyway.defaultSchema=app
flyway.createSchemas=true
```

### 詳細設計での活用

**命名規則:**
```
パターン: V{version}__{description}.sql

バージョン番号の例:
- V1__Initial_schema.sql
- V1.1__Add_user_fields.sql
- V2__Create_orders_table.sql
- V2.0.1__Fix_orders_constraint.sql
- V20231201__Add_payment_table.sql (日付ベース)

リピータブル:
- R__Create_views.sql
- R__Create_functions.sql
- R__Create_stored_procedures.sql
```

**データ型設計:**
```sql
-- V1__Create_product_table.sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    category_id BIGINT REFERENCES categories(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT positive_price CHECK (price >= 0),
    CONSTRAINT positive_stock CHECK (stock_quantity >= 0)
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = TRUE;
```

### 開発での活用

**ローカル開発:**
```bash
# Docker Composeでの使用例
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"

  flyway:
    image: flyway/flyway
    command: -url=jdbc:postgresql://db:5432/myapp -user=dev -password=devpass -connectRetries=60 migrate
    volumes:
      - ./sql:/flyway/sql
    depends_on:
      - db
```

**Spring Boot統合:**
```java
// Application.java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
        // Flywayは自動的に起動時に実行される
    }
}

// プログラマティックな制御
@Bean
public Flyway flyway(DataSource dataSource) {
    Flyway flyway = Flyway.configure()
        .dataSource(dataSource)
        .locations("classpath:db/migration")
        .baselineOnMigrate(true)
        .load();

    flyway.migrate();
    return flyway;
}
```

**複雑なデータ移行:**
```sql
-- V5__Migrate_user_data.sql
-- 段階的なデータ移行

-- ステップ1: 新テーブル作成
CREATE TABLE users_new (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    full_name VARCHAR(200),
    created_at TIMESTAMP
);

-- ステップ2: データコピー
INSERT INTO users_new (id, username, email, full_name, created_at)
SELECT
    id,
    username,
    email,
    CONCAT(first_name, ' ', last_name) AS full_name,
    created_at
FROM users_old;

-- ステップ3: インデックス作成
CREATE UNIQUE INDEX idx_users_new_username ON users_new(username);
CREATE INDEX idx_users_new_email ON users_new(email);

-- ステップ4: 古いテーブルをリネーム（後で削除）
ALTER TABLE users_old RENAME TO users_old_backup;
ALTER TABLE users_new RENAME TO users;

-- ステップ5: シーケンス調整
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
```

### テストでの活用

**テストデータ準備:**
```sql
-- V999__Test_data.sql (開発環境のみ)
INSERT INTO users (username, email, email_verified) VALUES
    ('testuser1', 'test1@example.com', TRUE),
    ('testuser2', 'test2@example.com', TRUE),
    ('testuser3', 'test3@example.com', FALSE);

INSERT INTO products (name, price, stock_quantity) VALUES
    ('Product A', 1000.00, 10),
    ('Product B', 2000.00, 5),
    ('Product C', 500.00, 20);
```

**統合テスト:**
```java
@SpringBootTest
@Testcontainers
public class UserRepositoryTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void properties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        // Flywayが自動的にマイグレーション実行
    }

    @Test
    void testFindByUsername() {
        // テーブルは既にFlywayで作成済み
        User user = userRepository.findByUsername("testuser");
        assertNotNull(user);
    }
}
```

### リリースでの活用

**本番デプロイ:**
```bash
# デプロイスクリプト例
#!/bin/bash

# バックアップ
pg_dump -h prod-db -U app_user myapp > backup_$(date +%Y%m%d_%H%M%S).sql

# マイグレーション情報確認
flyway -configFiles=flyway-prod.conf info

# ドライラン（Teams版以上）
# flyway -configFiles=flyway-prod.conf -dryRunOutput=dryrun.sql migrate

# マイグレーション実行
flyway -configFiles=flyway-prod.conf migrate

# 検証
flyway -configFiles=flyway-prod.conf validate

echo "Migration completed successfully"
```

**ブルーグリーンデプロイ:**
```sql
-- 段階的カラム追加（ダウンタイムゼロ）

-- V10__Add_user_status_step1.sql
-- ステップ1: NULL許可で新カラム追加
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- V11__Add_user_status_step2.sql
-- ステップ2: 既存データに値を設定
UPDATE users SET status = 'active' WHERE email_verified = TRUE;
UPDATE users SET status = 'inactive' WHERE email_verified = FALSE;

-- V12__Add_user_status_step3.sql
-- ステップ3: NOT NULL制約追加
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'inactive';
```

**CI/CDパイプライン統合:**
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Flyway migrations
        uses: docker://flyway/flyway:latest
        with:
          args: -url=jdbc:postgresql://${{ secrets.DB_HOST }}:5432/${{ secrets.DB_NAME }}
                -user=${{ secrets.DB_USER }}
                -password=${{ secrets.DB_PASSWORD }}
                -locations=filesystem:./sql
                migrate
```

### 運用・保守での活用

**スキーマ修正:**
```sql
-- V20__Fix_constraint.sql
-- 制約の修正

ALTER TABLE orders DROP CONSTRAINT orders_user_id_fkey;

ALTER TABLE orders ADD CONSTRAINT orders_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE;
```

**パフォーマンス改善:**
```sql
-- V21__Add_performance_indexes.sql
-- スロークエリ対策のインデックス追加

CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 部分インデックス
CREATE INDEX idx_orders_pending ON orders(created_at)
    WHERE status = 'pending';

-- 複合インデックス
CREATE INDEX idx_order_items_composite
    ON order_items(order_id, product_id, quantity);
```

**データ修正:**
```sql
-- V22__Fix_invalid_data.sql
-- 不正データの修正

-- 負の価格を修正
UPDATE products SET price = 0 WHERE price < 0;

-- 重複メールアドレスの解決
WITH duplicates AS (
    SELECT email, MIN(id) as keep_id
    FROM users
    GROUP BY email
    HAVING COUNT(*) > 1
)
UPDATE users u
SET email = u.email || '_dup_' || u.id
WHERE EXISTS (
    SELECT 1 FROM duplicates d
    WHERE u.email = d.email AND u.id != d.keep_id
);
```

## 公式ドキュメント

- **公式サイト**: https://flywaydb.org/
- **ドキュメント**: https://documentation.red-gate.com/fd
- **コマンドラインリファレンス**: https://documentation.red-gate.com/fd/command-line-184127404.html
- **GitHub**: https://github.com/flyway/flyway

## 学習リソース

### 公式リソース

1. **Flyway Documentation**
   - URL: https://documentation.red-gate.com/fd
   - 包括的なドキュメント

2. **Flyway Quickstart Guides**
   - URL: https://flywaydb.org/documentation/getstarted/
   - 各種フレームワーク向けクイックスタート

3. **Flyway Blog**
   - URL: https://flywaydb.org/blog
   - ベストプラクティス、Tips

### 外部リソース

1. **Baeldung - Flyway Tutorials**
   - URL: https://www.baeldung.com/database-migrations-with-flyway
   - Spring Boot統合チュートリアル

2. **YouTube チュートリアル**
   - Flyway基礎から応用まで

## 関連リンク

### データベース対応

**サポートされるデータベース:**
- PostgreSQL
- MySQL/MariaDB
- Oracle Database
- SQL Server
- DB2
- SQLite
- H2
- HSQLDB
- Derby
- Snowflake
- Redshift
- CockroachDB

### 代替ツール

**マイグレーションツール:**
- **Liquibase**: XML/YAML/JSONベースのマイグレーション
- **dbmate**: シンプルなマイグレーションツール
- **golang-migrate**: Go製マイグレーションツール
- **Alembic**: Python（SQLAlchemy）用マイグレーション
- **Active Record Migrations**: Rails用マイグレーション
- **Knex.js**: Node.js用マイグレーション

### ベストプラクティス

**マイグレーションファイル作成ルール:**
```
1. 1マイグレーション1目的
   ❌ V1__Create_all_tables.sql (複数テーブル作成)
   ✅ V1__Create_users_table.sql
   ✅ V2__Create_orders_table.sql

2. バージョン番号は連番または日付
   ✅ V1, V2, V3...
   ✅ V20231201, V20231202...

3. 説明的な名前
   ❌ V5__Update.sql
   ✅ V5__Add_email_verification_to_users.sql

4. 小さく頻繁にマイグレーション
   - 大きな変更は複数に分割
   - レビューしやすいサイズ

5. べき等性を考慮
   - IF NOT EXISTS を活用
   - CREATE OR REPLACE を使用
```

**本番適用チェックリスト:**
```
□ バックアップ取得完了
□ ステージング環境でテスト完了
□ ロールバック手順を準備
□ ダウンタイムの許容時間を確認
□ マイグレーション時間を見積もり
□ 関係者への事前通知
□ モニタリング準備
□ flyway info で確認
□ ドライラン実行（可能であれば）
□ 本番実行
□ flyway validate で検証
□ アプリケーション動作確認
```

**エラーハンドリング:**
```
マイグレーション失敗時:
1. flyway info でステータス確認
2. エラーログを確認
3. データベースの状態を確認
4. 必要に応じて手動修正
5. flyway repair でマイグレーション履歴を修復
6. 再度 flyway migrate
```
