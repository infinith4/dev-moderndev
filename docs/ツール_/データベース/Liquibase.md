# Liquibase

## 概要

Liquibase は、オープンソースのデータベーススキーマ変更管理・マイグレーションツールです。XML、YAML、JSON、SQL など複数の形式でデータベース変更を定義し、データベースに依存しない抽象化レイヤーを提供します。Change Set（変更セット）ベースのアプローチにより、複雑な変更履歴の管理、ロールバック、条件分岐を柔軟に実現し、エンタープライズ環境での大規模なデータベース管理に適しています。

## 主な特徴

### 1. データベース非依存
- 60以上のデータベースをサポート
- データベース間のマイグレーション
- 抽象化された変更定義
- ベンダーロックインを回避

### 2. 柔軟な形式
- XML、YAML、JSON、SQL
- プログラマティックAPI
- 形式の混在が可能
- ベストな形式を選択可能

### 3. 高度な機能
- 前提条件（Preconditions）
- コンテキスト（条件付き実行）
- ロールバック
- 差分生成（Diff）
- リファクタリング

### 4. エンタープライズサポート
- Liquibase Pro（商用版）
- 高度なロールバック
- ストアドプロシージャの差分
- データ品質チェック

## 主な機能

### コア機能

| 機能 | 説明 |
|------|------|
| update | 変更の適用 |
| rollback | 変更の取り消し |
| diff | データベース間の差分検出 |
| generateChangeLog | 既存DBからChangeLog生成 |
| status | 未適用の変更を表示 |
| validate | ChangeLogの検証 |
| tag | 特定のポイントにタグ付け |

### Change Type（変更タイプ）

| タイプ | 説明 |
|--------|------|
| createTable | テーブル作成 |
| addColumn | カラム追加 |
| dropTable | テーブル削除 |
| createIndex | インデックス作成 |
| addForeignKeyConstraint | 外部キー制約追加 |
| insert | データ挿入 |
| update | データ更新 |
| sql | 生SQL実行 |
| sqlFile | SQLファイル実行 |
| customChange | カスタム変更 |

## インストールとセットアップ

### コマンドライン（CLI）

```bash
# macOS (Homebrew)
brew install liquibase

# Windows (Chocolatey)
choco install liquibase

# Linux (手動)
wget https://github.com/liquibase/liquibase/releases/download/v4.24.0/liquibase-4.24.0.tar.gz
tar -xzf liquibase-4.24.0.tar.gz
export PATH=$PATH:`pwd`/liquibase

# Docker
docker pull liquibase/liquibase
```

### Maven プロジェクト

```xml
<!-- pom.xml -->
<project>
  <build>
    <plugins>
      <plugin>
        <groupId>org.liquibase</groupId>
        <artifactId>liquibase-maven-plugin</artifactId>
        <version>4.24.0</version>
        <configuration>
          <propertyFile>liquibase.properties</propertyFile>
          <changeLogFile>src/main/resources/db/changelog/db.changelog-master.xml</changeLogFile>
        </configuration>
      </plugin>
    </plugins>
  </build>

  <dependencies>
    <dependency>
      <groupId>org.liquibase</groupId>
      <artifactId>liquibase-core</artifactId>
      <version>4.24.0</version>
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
    id 'org.liquibase.gradle' version '2.2.0'
}

dependencies {
    implementation 'org.liquibase:liquibase-core:4.24.0'
    liquibaseRuntime 'org.liquibase:liquibase-core:4.24.0'
    liquibaseRuntime 'org.postgresql:postgresql:42.6.0'
}

liquibase {
    activities {
        main {
            changeLogFile 'src/main/resources/db/changelog/db.changelog-master.xml'
            url 'jdbc:postgresql://localhost:5432/mydb'
            username 'postgres'
            password 'secret'
        }
    }
}
```

### Spring Boot プロジェクト

```properties
# application.properties
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=postgres
spring.datasource.password=secret

spring.liquibase.enabled=true
spring.liquibase.change-log=classpath:db/changelog/db.changelog-master.xml
```

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
```

## 基本的な使い方

### 1. プロジェクト構造

```
my-project/
├── liquibase.properties
└── db/
    └── changelog/
        ├── db.changelog-master.xml
        ├── changes/
        │   ├── v1.0/
        │   │   ├── 001-create-users-table.xml
        │   │   └── 002-add-email-column.xml
        │   └── v2.0/
        │       └── 001-create-orders-table.xml
        └── data/
            └── initial-data.xml
```

### 2. ChangeLog マスターファイル

```xml
<!-- db.changelog-master.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.24.xsd">

    <include file="db/changelog/changes/v1.0/001-create-users-table.xml"/>
    <include file="db/changelog/changes/v1.0/002-add-email-column.xml"/>
    <include file="db/changelog/changes/v2.0/001-create-orders-table.xml"/>
    <include file="db/changelog/data/initial-data.xml"/>

</databaseChangeLog>
```

### 3. Change Set の作成（XML）

```xml
<!-- 001-create-users-table.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.24.xsd">

    <changeSet id="001-create-users-table" author="john.doe">
        <createTable tableName="users">
            <column name="id" type="bigint" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="username" type="varchar(50)">
                <constraints nullable="false" unique="true"/>
            </column>
            <column name="email" type="varchar(255)"/>
            <column name="created_at" type="timestamp" defaultValueDate="CURRENT_TIMESTAMP"/>
        </createTable>

        <createIndex indexName="idx_users_username" tableName="users">
            <column name="username"/>
        </createIndex>

        <rollback>
            <dropTable tableName="users"/>
        </rollback>
    </changeSet>

</databaseChangeLog>
```

### 4. Change Set の作成（YAML）

```yaml
# 001-create-users-table.yaml
databaseChangeLog:
  - changeSet:
      id: 001-create-users-table
      author: john.doe
      changes:
        - createTable:
            tableName: users
            columns:
              - column:
                  name: id
                  type: bigint
                  autoIncrement: true
                  constraints:
                    primaryKey: true
                    nullable: false
              - column:
                  name: username
                  type: varchar(50)
                  constraints:
                    nullable: false
                    unique: true
              - column:
                  name: email
                  type: varchar(255)
              - column:
                  name: created_at
                  type: timestamp
                  defaultValueDate: CURRENT_TIMESTAMP
        - createIndex:
            indexName: idx_users_username
            tableName: users
            columns:
              - column:
                  name: username
      rollback:
        - dropTable:
            tableName: users
```

### 5. Change Set の作成（SQL）

```xml
<!-- 001-create-users-table.xml -->
<databaseChangeLog>
    <changeSet id="001-create-users-table" author="john.doe">
        <sqlFile path="sql/001-create-users-table.sql"/>
        <rollback>
            <sqlFile path="sql/rollback/001-create-users-table.sql"/>
        </rollback>
    </changeSet>
</databaseChangeLog>
```

```sql
-- sql/001-create-users-table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
```

### 6. コマンドライン実行

```bash
# liquibase.properties
url=jdbc:postgresql://localhost:5432/mydb
username=postgres
password=secret
changeLogFile=db/changelog/db.changelog-master.xml
driver=org.postgresql.Driver

# ステータス確認
liquibase status

# 変更の適用
liquibase update

# 特定のタグまでロールバック
liquibase rollback v1.0

# 差分の生成
liquibase diff \
  --referenceUrl=jdbc:postgresql://prod-server:5432/mydb \
  --referenceUsername=postgres \
  --referencePassword=secret

# 既存DBからChangeLog生成
liquibase generateChangeLog

# バリデーション
liquibase validate
```

## 高度な機能

### Preconditions（前提条件）

```xml
<changeSet id="002-add-column" author="john.doe">
    <preConditions onFail="MARK_RAN">
        <not>
            <columnExists tableName="users" columnName="phone"/>
        </not>
    </preConditions>

    <addColumn tableName="users">
        <column name="phone" type="varchar(20)"/>
    </addColumn>
</changeSet>
```

### Context（コンテキスト）

```xml
<!-- 開発環境のみ実行 -->
<changeSet id="insert-test-data" author="john.doe" context="dev">
    <insert tableName="users">
        <column name="username" value="testuser"/>
        <column name="email" value="test@example.com"/>
    </insert>
</changeSet>

<!-- 本番環境のみ実行 -->
<changeSet id="create-prod-index" author="john.doe" context="prod">
    <createIndex indexName="idx_users_email" tableName="users">
        <column name="email"/>
    </createIndex>
</changeSet>
```

```bash
# コンテキストを指定して実行
liquibase update --contexts=dev
liquibase update --contexts=prod
```

### Labels（ラベル）

```xml
<changeSet id="feature-x" author="john.doe" labels="feature-x,version-2.0">
    <addColumn tableName="users">
        <column name="avatar_url" type="varchar(500)"/>
    </addColumn>
</changeSet>
```

```bash
# ラベルを指定して実行
liquibase update --labels="feature-x"
```

### ロールバック

```xml
<!-- 自動ロールバック（サポートされているChange Typeの場合） -->
<changeSet id="add-column" author="john.doe">
    <addColumn tableName="users">
        <column name="age" type="int"/>
    </addColumn>
    <!-- rollback は自動生成される: dropColumn -->
</changeSet>

<!-- 手動ロールバック -->
<changeSet id="complex-change" author="john.doe">
    <sql>
        -- 複雑な変更
    </sql>
    <rollback>
        <sql>
            -- ロールバック用SQL
        </sql>
    </rollback>
</changeSet>

<!-- 空のロールバック（ロールバック不可） -->
<changeSet id="no-rollback" author="john.doe">
    <sql>DELETE FROM old_table;</sql>
    <rollback/>
</changeSet>
```

```bash
# ロールバックの実行
liquibase rollback v1.0         # タグまでロールバック
liquibase rollbackCount 3       # 3つの変更をロールバック
liquibase rollbackToDate 2024-01-15  # 日付までロールバック
```

### 差分とマージ

```bash
# 2つのデータベース間の差分を検出
liquibase diff \
  --url=jdbc:postgresql://localhost:5432/dev_db \
  --username=postgres \
  --password=secret \
  --referenceUrl=jdbc:postgresql://prod-server:5432/prod_db \
  --referenceUsername=postgres \
  --referencePassword=secret

# 差分をChangeLogとして生成
liquibase diffChangeLog \
  --url=jdbc:postgresql://localhost:5432/dev_db \
  --referenceUrl=jdbc:postgresql://prod-server:5432/prod_db \
  --changeLogFile=diff.xml
```

### Java API

```java
import liquibase.Liquibase;
import liquibase.database.Database;
import liquibase.database.DatabaseFactory;
import liquibase.database.jvm.JdbcConnection;
import liquibase.resource.ClassLoaderResourceAccessor;

import java.sql.Connection;
import java.sql.DriverManager;

public class LiquibaseExample {
    public static void main(String[] args) throws Exception {
        Connection connection = DriverManager.getConnection(
            "jdbc:postgresql://localhost:5432/mydb",
            "postgres",
            "secret"
        );

        Database database = DatabaseFactory.getInstance()
            .findCorrectDatabaseImplementation(new JdbcConnection(connection));

        Liquibase liquibase = new Liquibase(
            "db/changelog/db.changelog-master.xml",
            new ClassLoaderResourceAccessor(),
            database
        );

        // 変更の適用
        liquibase.update("");

        // ステータス確認
        System.out.println(liquibase.getChangeSetStatuses("").size() + " change sets");

        // ロールバック
        // liquibase.rollback(3, "");

        connection.close();
    }
}
```

## CI/CD統合

### GitHub Actions

```yaml
name: Database Migration

on:
  push:
    branches: [ main ]

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
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3

    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'

    - name: Run Liquibase Status
      run: |
        ./mvnw liquibase:status \
          -Dliquibase.url=jdbc:postgresql://localhost:5432/testdb \
          -Dliquibase.username=postgres \
          -Dliquibase.password=postgres

    - name: Run Liquibase Update
      run: |
        ./mvnw liquibase:update \
          -Dliquibase.url=jdbc:postgresql://localhost:5432/testdb \
          -Dliquibase.username=postgres \
          -Dliquibase.password=postgres

    - name: Validate Migration
      run: |
        ./mvnw liquibase:validate \
          -Dliquibase.url=jdbc:postgresql://localhost:5432/testdb \
          -Dliquibase.username=postgres \
          -Dliquibase.password=postgres
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

  liquibase:
    image: liquibase/liquibase:4.24
    command: update
    volumes:
      - ./db/changelog:/liquibase/changelog
    environment:
      - LIQUIBASE_COMMAND_URL=jdbc:postgresql://postgres:5432/mydb
      - LIQUIBASE_COMMAND_USERNAME=postgres
      - LIQUIBASE_COMMAND_PASSWORD=secret
      - LIQUIBASE_COMMAND_CHANGELOG_FILE=changelog/db.changelog-master.xml
    depends_on:
      - postgres
```

## ベストプラクティス

### 1. Change Set の設計

```xml
<!-- ✓ 小さく原子的な変更 -->
<changeSet id="add-email-column" author="john">
    <addColumn tableName="users">
        <column name="email" type="varchar(255)"/>
    </addColumn>
</changeSet>

<!-- ✗ 大きすぎる変更 -->
<changeSet id="entire-schema" author="john">
    <!-- 何十ものテーブル作成... -->
</changeSet>

<!-- ✓ ユニークなID -->
<changeSet id="20240115-001-add-column" author="john">
    ...
</changeSet>
```

### 2. ロールバックの定義

```xml
<!-- サポートされている変更は自動ロールバック -->
<changeSet id="add-column" author="john">
    <addColumn tableName="users">
        <column name="phone" type="varchar(20)"/>
    </addColumn>
</changeSet>

<!-- 複雑な変更は明示的にロールバックを定義 -->
<changeSet id="complex-migration" author="john">
    <sql>
        -- 複雑なデータ移行
    </sql>
    <rollback>
        <sql>
            -- ロールバック手順
        </sql>
    </rollback>
</changeSet>
```

### 3. コンテキストの活用

```xml
<!-- 環境別の変更 -->
<changeSet id="dev-test-data" author="john" context="dev,test">
    <insert tableName="users">
        <column name="username" value="testuser"/>
    </insert>
</changeSet>

<changeSet id="prod-performance" author="john" context="prod">
    <createIndex indexName="idx_perf" tableName="orders">
        <column name="created_at"/>
    </createIndex>
</changeSet>
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://www.liquibase.org/
- ドキュメント: https://docs.liquibase.com/
- GitHub: https://github.com/liquibase/liquibase
- Liquibase Hub: https://hub.liquibase.com/

### コミュニティ
- Forum: https://forum.liquibase.org/
- Stack Overflow: [liquibase]タグ
- Twitter: @liquibase

### チュートリアル
- Getting Started: https://docs.liquibase.com/start/home.html
- Best Practices: https://www.liquibase.org/get-started/best-practices

## まとめ

Liquibase は、以下の場面で特に有用です:

1. **エンタープライズ環境** - 複雑な変更管理、前提条件、コンテキスト
2. **データベース非依存** - マルチデータベース対応、ポータビリティ
3. **高度なロールバック** - 柔軟なロールバック戦略
4. **チーム開発** - Change Set ベースの変更管理

Flyway よりも複雑ですが、より高度な機能とデータベース非依存性を提供します。
