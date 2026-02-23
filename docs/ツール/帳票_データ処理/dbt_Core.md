# dbt Core

## 概要

dbt（data build tool）Coreは、データウェアハウス内のデータ変換をSQL + Jinjaテンプレートで管理するオープンソースのデータ変換ツールです。ELT（Extract, Load, Transform）パイプラインの「T」を担当し、モデル（SQLファイル）、ソース定義、テスト、ドキュメントをコードとして管理します。BigQuery、Snowflake、Redshift、PostgreSQLなどの主要データウェアハウスに対応し、`dbt run` / `dbt test` / `dbt docs` コマンドにより、データ変換の実行・検証・ドキュメント生成をCI/CDパイプラインに統合できます。

## 主な機能

### 1. モデル管理
- **SQLモデル**: SELECT文ベースのデータ変換定義
- **マテリアライゼーション**: table、view、incremental、ephemeral
- **Jinjaテンプレート**: 動的SQL生成
- **ref関数**: モデル間の依存関係管理

### 2. ソース・シード
- **ソース定義**: 外部テーブルの宣言とメタデータ管理
- **フレッシュネスチェック**: ソースデータの鮮度検証
- **シードファイル**: CSVデータのウェアハウスへのロード
- **スナップショット**: Slowly Changing Dimension（SCD Type 2）

### 3. テスト
- **スキーマテスト**: not_null、unique、accepted_values、relationships
- **カスタムテスト**: SQLベースのカスタムデータテスト
- **ユニットテスト**: モデルロジックの単体テスト
- **dbt-expectations**: 拡張テストパッケージ

### 4. ドキュメント
- **自動生成**: モデル・カラムのドキュメント自動生成
- **リネージグラフ**: データ系譜の可視化
- **description**: YAMLでのカラム説明記述
- **Webサーバー**: `dbt docs serve` でドキュメントサイト起動

### 5. パッケージ・マクロ
- **dbt Hub**: コミュニティパッケージの利用
- **マクロ**: 再利用可能なSQLテンプレート
- **カスタムマクロ**: プロジェクト固有のロジック定義
- **dbt-utils**: 汎用ユーティリティパッケージ

### 6. 対応ウェアハウス
- **BigQuery**: Google BigQuery
- **Snowflake**: Snowflake Data Cloud
- **Redshift**: Amazon Redshift
- **PostgreSQL**: PostgreSQL
- **Databricks**: Databricks SQL

## 利用方法

### インストール

```bash
# pip でインストール（アダプター含む）
pip install dbt-core dbt-bigquery
pip install dbt-core dbt-snowflake
pip install dbt-core dbt-redshift
pip install dbt-core dbt-postgres

# バージョン確認
dbt --version

# 新規プロジェクト作成
dbt init my_analytics
cd my_analytics
```

### プロジェクト構造

```
my_analytics/
  dbt_project.yml           # プロジェクト設定
  profiles.yml              # 接続設定（~/.dbt/ に配置推奨）
  packages.yml              # パッケージ依存
  models/
    staging/                 # ステージングモデル（ソースの整形）
      stg_orders.sql
      stg_customers.sql
      _stg_models.yml
    marts/                   # マートモデル（ビジネスロジック）
      dim_customers.sql
      fct_orders.sql
      _mart_models.yml
  tests/                     # カスタムテスト
    assert_positive_total.sql
  macros/                    # カスタムマクロ
    cents_to_dollars.sql
  seeds/                     # シードCSVファイル
    country_codes.csv
  snapshots/                 # スナップショット
    snap_orders.sql
  analyses/                  # アドホック分析SQL
```

### profiles.yml（接続設定）

```yaml
# ~/.dbt/profiles.yml
my_analytics:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: my-gcp-project
      dataset: analytics_dev
      threads: 4
      timeout_seconds: 300
      location: asia-northeast1

    prod:
      type: bigquery
      method: service-account
      project: my-gcp-project
      dataset: analytics_prod
      threads: 8
      timeout_seconds: 300
      location: asia-northeast1
      keyfile: /path/to/service-account.json
```

### dbt_project.yml

```yaml
# dbt_project.yml
name: 'my_analytics'
version: '1.0.0'
config-version: 2

profile: 'my_analytics'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

models:
  my_analytics:
    staging:
      +materialized: view
      +schema: staging
    marts:
      +materialized: table
      +schema: marts
```

### モデルの作成

```sql
-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        id as order_id,
        user_id as customer_id,
        order_date,
        status,
        amount as amount_cents,
        {{ cents_to_dollars('amount') }} as amount_dollars,
        created_at,
        updated_at
    from source
    where status != 'deleted'
)

select * from renamed
```

```sql
-- models/marts/dim_customers.sql
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_id,
        count(*) as total_orders,
        sum(amount_dollars) as total_spent,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from orders
    group by customer_id
),

final as (
    select
        c.customer_id,
        c.customer_name,
        c.email,
        c.created_at as customer_since,
        coalesce(co.total_orders, 0) as total_orders,
        coalesce(co.total_spent, 0) as total_spent,
        co.first_order_date,
        co.last_order_date
    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final
```

### スキーマ定義・テスト

```yaml
# models/staging/_stg_models.yml
version: 2

sources:
  - name: raw
    database: my-gcp-project
    schema: raw_data
    tables:
      - name: orders
        description: "注文の生データ"
        loaded_at_field: updated_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
      - name: customers
        description: "顧客の生データ"

models:
  - name: stg_orders
    description: "整形済み注文データ"
    columns:
      - name: order_id
        description: "注文の一意識別子"
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "顧客ID"
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: status
        description: "注文ステータス"
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
      - name: amount_dollars
        description: "注文金額（ドル）"
        tests:
          - not_null
```

### マクロの作成

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round(cast({{ column_name }} as numeric) / 100, {{ precision }})
{% endmacro %}
```

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
```

### 実行コマンド

```bash
# 依存パッケージのインストール
dbt deps

# 全モデルの実行
dbt run

# 特定モデルのみ実行
dbt run --select stg_orders
dbt run --select marts.dim_customers

# 上流モデルを含めて実行（+プレフィックス）
dbt run --select +fct_orders

# テストの実行
dbt test

# 特定モデルのテストのみ実行
dbt test --select stg_orders

# ソースのフレッシュネスチェック
dbt source freshness

# シードデータのロード
dbt seed

# ドキュメント生成・表示
dbt docs generate
dbt docs serve --port 8080

# スナップショット実行
dbt snapshot

# フルリフレッシュ（incrementalモデルの再構築）
dbt run --full-refresh

# コンパイル（SQLの確認のみ）
dbt compile --select dim_customers

# デバッグ（接続テスト）
dbt debug
```

### CI/CD統合

```yaml
# .github/workflows/dbt.yml
name: dbt CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  dbt-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dbt
        run: pip install dbt-core dbt-bigquery

      - name: Setup profiles
        run: |
          mkdir -p ~/.dbt
          echo "$DBT_PROFILES" > ~/.dbt/profiles.yml
        env:
          DBT_PROFILES: ${{ secrets.DBT_PROFILES_YML }}

      - name: Install packages
        run: dbt deps

      - name: Run models
        run: dbt run --target ci

      - name: Run tests
        run: dbt test --target ci

      - name: Check source freshness
        run: dbt source freshness --target ci

      - name: Generate docs
        run: dbt docs generate --target ci
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **dbt Core** | 無料 | オープンソース、Apache-2.0 License |
| **dbt Cloud Developer** | 無料 | 1開発者、1プロジェクト |
| **dbt Cloud Team** | $100/シート/月 | チーム向け、CI/CD統合 |
| **dbt Cloud Enterprise** | 要問合せ | SSO、RBAC、監査ログ |

## メリット

### 主な利点

1. **SQLベース**: データエンジニアが慣れたSQLで変換を定義
2. **バージョン管理**: Gitによるデータ変換のコード管理
3. **テスト内蔵**: データ品質テストの自動化
4. **ドキュメント自動生成**: リネージグラフとカラム説明
5. **DRY原則**: マクロとref関数による再利用性
6. **マルチウェアハウス**: 主要DWHに幅広く対応
7. **incrementalモデル**: 差分更新による効率的なデータ処理
8. **パッケージ**: dbt Hubによるコミュニティパッケージ
9. **CI/CD統合**: データパイプラインの継続的テスト
10. **活発なコミュニティ**: 大規模なユーザーコミュニティ

## デメリット

### 制約・課題

1. **T のみ**: ELTのTransformのみ（Extract/Loadは別ツール必要）
2. **学習曲線**: Jinja テンプレートとdbt固有概念の習得
3. **デバッグ**: コンパイル後SQLのデバッグが困難な場合がある
4. **大規模モデル**: モデル数が増大すると依存関係管理が複雑
5. **リアルタイム非対応**: バッチ処理前提の設計
6. **Python モデル**: SQLモデルと比較してPythonモデルの機能が限定的
7. **ウェアハウスコスト**: 頻繁なフルリフレッシュはコスト増加
8. **設定分散**: profiles.yml、dbt_project.yml、schema.ymlの設定が分散

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **SQLMesh** | dbt互換のデータ変換ツール | dbtより仮想環境が強力 |
| **Dataform** | Google Cloudのデータ変換 | BigQuery特化、Google買収 |
| **Apache Spark** | 分散データ処理 | dbtより汎用だが学習曲線が大きい |
| **Airflow** | ワークフローオーケストレーション | dbtはAirflowのタスクとして利用可 |
| **Fivetran Transformations** | Fivetranのデータ変換 | ETLツールとの一体型 |

## 公式リンク

- **公式サイト**: [https://www.getdbt.com/](https://www.getdbt.com/)
- **ドキュメント**: [https://docs.getdbt.com/](https://docs.getdbt.com/)
- **GitHub**: [https://github.com/dbt-labs/dbt-core](https://github.com/dbt-labs/dbt-core)
- **dbt Hub**: [https://hub.getdbt.com/](https://hub.getdbt.com/)
- **コミュニティ**: [https://community.getdbt.com/](https://community.getdbt.com/)
- **dbt Learn**: [https://courses.getdbt.com/](https://courses.getdbt.com/)

## 関連ドキュメント

- [帳票データ処理一覧](../帳票データ処理/)
- [監視ロギング](../監視ロギング/)

---

**カテゴリ**: 帳票データ処理
**対象工程**: 実装・運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
