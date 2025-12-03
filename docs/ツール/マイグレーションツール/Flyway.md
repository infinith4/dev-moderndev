# Flyway

## 概要

Flyway は、Redgate が提供するオープンソースのデータベースマイグレーションツールです。SQL ベースまたは Java ベースのマイグレーションスクリプトを使用して、データベーススキーマのバージョン管理、適用、追跡を自動化します。シンプルで直感的な「マイグレーション as コード」アプローチにより、開発からプロダクションまでの一貫したデータベース管理を実現し、CI/CD パイプラインへのシームレスな統合が可能です。

## 主な特徴

### 1. シンプルな概念
- SQL ファーストアプローチ
- バージョン番号ベースの管理
- Up マイグレーションのみ（基本）
- 学習コストが低い

### 2. 幅広いデータベース対応
- Oracle、PostgreSQL、MySQL、SQL Server
- MariaDB、DB2、H2、SQLite
- Snowflake、Redshift、Cassandra
- 20以上のデータベースをサポート

### 3. 柔軟な実行環境
- コマンドライン（CLI）
- Java API
- Maven / Gradle プラグイン
- Docker
- Spring Boot 統合

### 4. エンタープライズ機能
- アンドゥ（Undo）マイグレーション
- ドライラン
- チェリーピック
- エラーオーバーライド
- Teams エディション

### 5. CI/CD 統合
- Jenkins、GitLab CI、GitHub Actions
- 自動化されたマイグレーション
- ロールバック戦略
- 本番環境への安全なデプロイ

## 主な機能

### コア機能

| 機能 | 説明 |
|------|------|
| Migrate | マイグレーションの適用 |
| Clean | すべてのオブジェクトを削除（開発用） |
| Info | マイグレーションステータスの表示 |
| Validate | 適用済みマイグレーションの検証 |
| Baseline | 既存DBの初期化 |
| Repair | スキーマ履歴テーブルの修復 |

### マイグレーションタイプ

| タイプ | 説明 |
|--------|------|
| Versioned | バージョン番号付き（V1__description.sql） |
| Undo | バージョンマイグレーションの取り消し |
| Repeatable | 繰り返し実行可能（R__description.sql） |
| Callback | ライフサイクルイベントフック |

## インストールとセットアップ

### コマンドライン（CLI）

```bash
# macOS (Homebrew)
brew install flyway

# Windows (Chocolatey)
choco install flyway-commandline

# Linux (手動)
wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.22.0/flyway-commandline-9.22.0-linux-x64.tar.gz | tar xvz
sudo ln -s `pwd`/flyway-9.22.0/flyway /usr/local/bin

# Docker
docker pull flyway/flyway
```

### Maven プロジェクト

```xml
<!-- pom.xml -->
<project>
  <build>
    <plugins>
      <plugin>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-maven-plugin</artifactId>
        <version>9.22.0</version>
        <configuration>
          <url>jdbc:postgresql://localhost:5432/mydb</url>
          <user>postgres</user>
          <password>secret</password>
          <locations>
            <location>classpath:db/migration</location>
          </locations>
        </configuration>
      </plugin>
    </plugins>
  </build>

  <dependencies>
    <dependency>
      <groupId>org.flywaydb</groupId>
      <artifactId>flyway-core</artifactId>
      <version>9.22.0</version>
    </dependency>
    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <version>42.6.0</version>
    </dependency>
  </dependencies>
</project>
```

### Gradle プロジェクト

```groovy
// build.gradle
plugins {
    id 'org.flywaydb.flyway' version '9.22.0'
}

dependencies {
    implementation 'org.flywaydb:flyway-core:9.22.0'
    implementation 'org.postgresql:postgresql:42.6.0'
}

flyway {
    url = 'jdbc:postgresql://localhost:5432/mydb'
    user = 'postgres'
    password = 'secret'
    locations = ['classpath:db/migration']
}
```

### Spring Boot プロジェクト

```properties
# application.properties
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=postgres
spring.datasource.password=secret

spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true
```

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
```

## 基本的な使い方

### 1. プロジェクト構造

```
my-project/
├── flyway.conf                    # 設定ファイル
└── sql/
    ├── V1__create_users_table.sql
    ├── V2__add_email_column.sql
    ├── V3__create_orders_table.sql
    └── R__view_user_summary.sql   # Repeatable
```

### 2. マイグレーションスクリプトの作成

```sql
-- V1__create_users_table.sql
-- バージョン: 1
-- 説明: ユーザーテーブルの作成

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
```

```sql
-- V2__add_email_column.sql
-- バージョン: 2
-- 説明: ユーザーテーブルにメールカラムを追加

-- 既に V1 で email があるため、このスクリプトは例示のみ
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
```

```sql
-- V3__create_orders_table.sql
-- バージョン: 3
-- 説明: 注文テーブルの作成

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

### 3. 命名規則

```
バージョンマイグレーション:
V<VERSION>__<DESCRIPTION>.sql

例:
V1__initial_schema.sql
V1.1__add_users_table.sql
V2__add_email_column.sql
V2.1__add_index.sql
V20240115120000__create_orders_table.sql  # タイムスタンプ形式

Repeatableマイグレーション:
R__<DESCRIPTION>.sql

例:
R__create_view_user_summary.sql
R__stored_procedure_calculate_total.sql
```

### 4. コマンドライン実行

```bash
# 設定ファイル (flyway.conf)
flyway.url=jdbc:postgresql://localhost:5432/mydb
flyway.user=postgres
flyway.password=secret
flyway.locations=filesystem:./sql

# マイグレーション情報の表示
flyway info

# マイグレーションの適用
flyway migrate

# バリデーション
flyway validate

# ベースライン（既存DBの初期化）
flyway baseline -baselineVersion=1

# クリーンアップ（開発環境のみ！）
flyway clean

# 修復
flyway repair
```

### 5. Java API での実行

```java
import org.flywaydb.core.Flyway;

public class FlywayExample {
    public static void main(String[] args) {
        // Flyway インスタンスの作成
        Flyway flyway = Flyway.configure()
            .dataSource("jdbc:postgresql://localhost:5432/mydb", "postgres", "secret")
            .locations("classpath:db/migration")
            .load();

        // マイグレーション情報の表示
        flyway.info();

        // マイグレーションの適用
        int migrationsApplied = flyway.migrate().migrationsExecuted;
        System.out.println("Applied " + migrationsApplied + " migrations");

        // バリデーション
        flyway.validate();
    }
}
```

## 高度な機能

### Undo マイグレーション（Teams/Enterprise）

```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

-- U1__create_users_table.sql（Undoスクリプト）
DROP TABLE users;
```

```bash
# Undo の実行
flyway undo
```

### Repeatable マイグレーション

```sql
-- R__view_user_summary.sql
-- Repeatableマイグレーション: チェックサムが変わるたびに再実行

CREATE OR REPLACE VIEW user_summary AS
SELECT
    u.id,
    u.username,
    u.email,
    COUNT(o.id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username, u.email;
```

### プレースホルダー

```sql
-- V1__create_schema.sql
CREATE SCHEMA ${schema_name};

CREATE TABLE ${schema_name}.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50)
);
```

```bash
# コマンドライン
flyway migrate -placeholders.schema_name=myapp

# 設定ファイル
flyway.placeholders.schema_name=myapp
```

### コールバック

```sql
-- beforeMigrate.sql
-- すべてのマイグレーション前に実行
SET lock_timeout = '10s';

-- afterMigrate.sql
-- すべてのマイグレーション後に実行
VACUUM ANALYZE;
```

```java
// Java API でのコールバック
flyway.configure()
    .callbacks(new BaseFlywayCallback() {
        @Override
        public void beforeMigrate(Connection connection) {
            // マイグレーション前の処理
        }

        @Override
        public void afterMigrate(Connection connection) {
            // マイグレーション後の処理
        }
    })
    .load();
```

### ドライラン（Teams/Enterprise）

```bash
# ドライランモード: 実際には適用せず、SQLを出力
flyway migrate -dryRunOutput=dryrun.sql

# 出力されたSQLを確認
cat dryrun.sql

# 問題なければ実際に適用
flyway migrate
```

## CI/CD 統合

### GitHub Actions

```yaml
name: Database Migration

on:
  push:
    branches: [ main ]
    paths:
      - 'db/migration/**'

jobs:
  migrate:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3

    - name: Setup Flyway
      run: |
        wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.22.0/flyway-commandline-9.22.0-linux-x64.tar.gz | tar xvz
        sudo ln -s `pwd`/flyway-9.22.0/flyway /usr/local/bin

    - name: Run Flyway Info
      run: |
        flyway info \
          -url=jdbc:postgresql://localhost:5432/testdb \
          -user=postgres \
          -password=postgres \
          -locations=filesystem:./db/migration

    - name: Run Flyway Migrate
      run: |
        flyway migrate \
          -url=jdbc:postgresql://localhost:5432/testdb \
          -user=postgres \
          -password=postgres \
          -locations=filesystem:./db/migration

    - name: Validate Migration
      run: |
        flyway validate \
          -url=jdbc:postgresql://localhost:5432/testdb \
          -user=postgres \
          -password=postgres \
          -locations=filesystem:./db/migration
```

### GitLab CI

```yaml
stages:
  - validate
  - migrate

variables:
  FLYWAY_VERSION: "9.22.0"
  DB_URL: "jdbc:postgresql://postgres:5432/mydb"
  DB_USER: "postgres"
  DB_PASSWORD: "secret"

.flyway_base:
  image: flyway/flyway:${FLYWAY_VERSION}
  services:
    - postgres:15
  variables:
    POSTGRES_DB: mydb
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: secret

validate:
  extends: .flyway_base
  stage: validate
  script:
    - flyway info -url=${DB_URL} -user=${DB_USER} -password=${DB_PASSWORD}
    - flyway validate -url=${DB_URL} -user=${DB_USER} -password=${DB_PASSWORD}

migrate:
  extends: .flyway_base
  stage: migrate
  script:
    - flyway migrate -url=${DB_URL} -user=${DB_USER} -password=${DB_PASSWORD}
  only:
    - main
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    environment {
        DB_URL = 'jdbc:postgresql://db-server:5432/mydb'
        DB_USER = credentials('db-user')
        DB_PASSWORD = credentials('db-password')
    }

    stages {
        stage('Flyway Info') {
            steps {
                sh '''
                    flyway info \
                        -url=${DB_URL} \
                        -user=${DB_USER} \
                        -password=${DB_PASSWORD} \
                        -locations=filesystem:./db/migration
                '''
            }
        }

        stage('Flyway Migrate') {
            steps {
                sh '''
                    flyway migrate \
                        -url=${DB_URL} \
                        -user=${DB_USER} \
                        -password=${DB_PASSWORD} \
                        -locations=filesystem:./db/migration
                '''
            }
        }

        stage('Validate') {
            steps {
                sh '''
                    flyway validate \
                        -url=${DB_URL} \
                        -user=${DB_USER} \
                        -password=${DB_PASSWORD} \
                        -locations=filesystem:./db/migration
                '''
            }
        }
    }

    post {
        failure {
            mail to: 'team@example.com',
                 subject: "Flyway Migration Failed: ${env.JOB_NAME}",
                 body: "Build failed: ${env.BUILD_URL}"
        }
    }
}
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  flyway:
    image: flyway/flyway:9.22.0
    command: migrate
    volumes:
      - ./sql:/flyway/sql
    environment:
      - FLYWAY_URL=jdbc:postgresql://postgres:5432/mydb
      - FLYWAY_USER=postgres
      - FLYWAY_PASSWORD=secret
      - FLYWAY_LOCATIONS=filesystem:/flyway/sql
    depends_on:
      - postgres

volumes:
  postgres_data:
```

```bash
# マイグレーションの実行
docker-compose up flyway

# Info の確認
docker-compose run flyway info

# Clean（開発環境のみ）
docker-compose run flyway clean
```

## ベストプラクティス

### 1. バージョン管理戦略

```
# セマンティックバージョニング
V1.0.0__initial_schema.sql
V1.1.0__add_users_table.sql
V1.1.1__fix_users_index.sql
V2.0.0__breaking_change.sql

# タイムスタンプ方式
V20240115120000__create_orders.sql
V20240115130000__add_status_column.sql

# シーケンシャル番号（推奨）
V001__initial_schema.sql
V002__add_users.sql
V003__add_orders.sql
```

### 2. マイグレーションの原則

```sql
-- ✓ 小さく分割する
V1__create_users.sql
V2__create_orders.sql

-- ✗ 大きすぎるマイグレーション
V1__entire_schema.sql

-- ✓ べき等性を保つ
CREATE TABLE IF NOT EXISTS users (...);

-- ✓ トランザクションを意識
BEGIN;
-- マイグレーション処理
COMMIT;
```

### 3. 環境分離

```bash
# 開発環境
flyway migrate -configFiles=flyway-dev.conf

# ステージング環境
flyway migrate -configFiles=flyway-staging.conf

# 本番環境
flyway migrate -configFiles=flyway-prod.conf
```

### 4. ロールバック戦略

```
# 基本: 前方のみ（Forward-only）
- Undo マイグレーションは避ける
- 問題があれば新しいマイグレーションで修正

# 緊急時: バックアップからリストア
- マイグレーション前にバックアップ
- 問題があればリストアして再試行
```

## トラブルシューティング

### よくある問題と解決策

#### 1. チェックサム不一致

```
原因: 適用済みマイグレーションが変更された
解決策:
# 履歴を修復（注意して使用）
flyway repair

# または、マイグレーションを元に戻す
```

#### 2. ベースライン

```
原因: 既存DBにFlywayを導入
解決策:
# 既存DBをバージョン1としてベースライン化
flyway baseline -baselineVersion=1

# その後、V2以降のマイグレーションを適用
flyway migrate
```

#### 3. マイグレーション失敗

```
原因: SQLエラー、権限不足等
解決策:
1. エラーメッセージを確認
2. 手動でDBを修正
3. flyway repair でスキーマ履歴を修復
4. 再度 migrate 実行
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://flywaydb.org/
- ドキュメント: https://flywaydb.org/documentation/
- GitHub: https://github.com/flyway/flyway
- Maven Central: https://mvnrepository.com/artifact/org.flywaydb/flyway-core

### コミュニティ
- Stack Overflow: [flyway]タグ
- GitHub Discussions: https://github.com/flyway/flyway/discussions
- Twitter: @flywaydb

### チュートリアル
- Getting Started: https://flywaydb.org/documentation/getstarted/
- Tutorials: https://flywaydb.org/documentation/tutorials/
- Videos: YouTube - Flyway

## まとめ

Flyway は、以下の場面で特に有用です:

1. **シンプルなマイグレーション** - SQLファーストアプローチで学習コストが低い
2. **CI/CD統合** - 自動化されたデータベース管理
3. **幅広いDB対応** - 20以上のデータベースをサポート
4. **チーム開発** - バージョン管理でスキーマ変更を追跡

データベーススキーマのバージョン管理をシンプルかつ確実に実現するデファクトスタンダードツールです。
