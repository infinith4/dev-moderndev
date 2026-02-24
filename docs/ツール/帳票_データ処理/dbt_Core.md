# dbt Core

## 概要

dbt（data build tool）Coreは、データウェアハウス内のデータ変換をSQL + Jinjaテンプレートで管理するオープンソースのデータ変換ツールです。ELT（Extract, Load, Transform）パイプラインの「T」を担当し、モデル（SQLファイル）、ソース定義、テスト、ドキュメントをコードとして管理します。BigQuery、Snowflake、Redshift、PostgreSQL等の主要データウェアハウスに対応しています。

## 主な特徴

| 項目 | 内容 |
|------|------|
| ライセンス | Apache License 2.0（無料） |
| 言語 | SQL + Jinjaテンプレート |
| 対応DWH | BigQuery、Snowflake、Redshift、PostgreSQL、Databricks |
| バージョン管理 | Gitによるデータ変換のコード管理 |
| テスト内蔵 | スキーマテスト・カスタムテストの自動化 |
| ドキュメント | リネージグラフとカラム説明の自動生成 |
| 有料版 | dbt Cloud（Team: $100/シート/月、Enterprise: 要問合せ） |

## 主な機能

### モデル管理

| 機能 | 説明 |
|------|------|
| SQLモデル | SELECT文ベースのデータ変換定義 |
| マテリアライゼーション | table、view、incremental、ephemeralの選択 |
| Jinjaテンプレート | 動的SQL生成 |
| ref関数 | モデル間の依存関係管理 |

### ソース・シード

| 機能 | 説明 |
|------|------|
| ソース定義 | 外部テーブルの宣言とメタデータ管理 |
| フレッシュネスチェック | ソースデータの鮮度検証 |
| シードファイル | CSVデータのウェアハウスへのロード |
| スナップショット | Slowly Changing Dimension（SCD Type 2） |

### テスト

| 機能 | 説明 |
|------|------|
| スキーマテスト | not_null、unique、accepted_values、relationships |
| カスタムテスト | SQLベースのカスタムデータテスト |
| ユニットテスト | モデルロジックの単体テスト |
| dbt-expectations | 拡張テストパッケージ |

### ドキュメント・パッケージ

| 機能 | 説明 |
|------|------|
| 自動生成 | モデル・カラムのドキュメント自動生成 |
| リネージグラフ | データ系譜の可視化 |
| dbt Hub | コミュニティパッケージの利用 |
| マクロ | 再利用可能なSQLテンプレート |

## インストールとセットアップ

公式URL:
- [dbt 公式サイト](https://www.getdbt.com/)
- [dbt ドキュメント](https://docs.getdbt.com/)

```bash
# pip でインストール（アダプター含む）
pip install dbt-core dbt-bigquery
pip install dbt-core dbt-snowflake
pip install dbt-core dbt-postgres

# バージョン確認
dbt --version

# 新規プロジェクト作成
dbt init my_analytics
cd my_analytics
```

## 基本的な使い方

### 1. プロジェクト構造

```
my_analytics/
  dbt_project.yml           # プロジェクト設定
  profiles.yml              # 接続設定（~/.dbt/ に配置推奨）
  packages.yml              # パッケージ依存
  models/
    staging/                 # ステージングモデル（ソースの整形）
      stg_orders.sql
      _stg_models.yml
    marts/                   # マートモデル（ビジネスロジック）
      dim_customers.sql
      fct_orders.sql
      _mart_models.yml
  tests/                     # カスタムテスト
  macros/                    # カスタムマクロ
  seeds/                     # シードCSVファイル
  snapshots/                 # スナップショット
```

### 2. モデルの作成

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
        {{ cents_to_dollars('amount') }} as amount_dollars,
        created_at
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
        coalesce(co.total_orders, 0) as total_orders,
        coalesce(co.total_spent, 0) as total_spent
    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final
```

### 3. スキーマ定義・テスト

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
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}

models:
  - name: stg_orders
    description: "整形済み注文データ"
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
```

### 4. 実行コマンド

```bash
# 依存パッケージのインストール
dbt deps

# 全モデルの実行
dbt run

# 特定モデルのみ実行
dbt run --select stg_orders

# 上流モデルを含めて実行
dbt run --select +fct_orders

# テストの実行
dbt test

# ソースのフレッシュネスチェック
dbt source freshness

# ドキュメント生成・表示
dbt docs generate
dbt docs serve --port 8080

# デバッグ（接続テスト）
dbt debug
```

## CI/CD 統合

### GitHub Actions

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
```

## 他ツールとの比較

### dbt Core vs SQLMesh

| 機能 | dbt Core | SQLMesh |
|------|----------|---------|
| 互換性 | デファクト標準 | dbt互換 |
| 仮想環境 | 限定的 | 強力 |
| 差分実行 | incrementalモデル | ネイティブ対応 |
| コミュニティ | 非常に大きい | 成長中 |

### dbt Core vs Apache Spark

| 機能 | dbt Core | Apache Spark |
|------|----------|-------------|
| 対象 | DWH内のデータ変換 | 汎用分散データ処理 |
| 言語 | SQL + Jinja | Python/Scala/SQL |
| 学習曲線 | 低い | 高い |
| リアルタイム | 非対応 | 対応 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| データウェアハウス構築 | 分析基盤のデータ変換 | staging/martsレイヤーでデータを段階的に整形 |
| データ品質管理 | データの正確性検証 | スキーマテストとフレッシュネスチェックで品質を自動検証 |
| ドキュメント管理 | データカタログの維持 | dbt docsでリネージグラフとカラム説明を自動生成 |
| CI/CDパイプライン | データ変換の継続的テスト | GitHub ActionsでPR毎にモデル実行とテストを自動化 |

## ベストプラクティス

### 1. モデル設計

- staging/martsのレイヤー構成を遵守
- ref関数で明示的にモデル間の依存関係を管理
- incrementalモデルで大規模テーブルの差分更新を活用

### 2. テスト

- 全モデルの主キーにunique + not_nullテストを設定
- ソースにフレッシュネスチェックを必ず定義
- カスタムテストでビジネスルールの整合性を検証

### 3. 運用

- profiles.ymlはリポジトリにコミットせず、CI/CD変数で管理
- dbt packagesを活用し、共通処理を再利用
- `dbt run --full-refresh` は計画的に実施（コスト注意）

## トラブルシューティング

### よくある問題と解決策

#### 1. dbt debug で接続エラー

```
原因: profiles.ymlの設定が不正、またはDWHへのネットワーク接続ができない
解決策: `dbt debug` でエラー内容を確認し、profiles.ymlの接続設定を修正する
```

#### 2. incrementalモデルでデータ重複

```
原因: unique_keyの指定漏れ、またはロジックの不整合
解決策: unique_keyを正しく設定し、必要に応じて `dbt run --full-refresh` で再構築する
```

#### 3. モデルの依存関係エラー

```
原因: ref()で参照しているモデルが存在しない、またはスペルミス
解決策: `dbt compile` でコンパイルエラーを確認し、モデル名を修正する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: [https://www.getdbt.com/](https://www.getdbt.com/)
- ドキュメント: [https://docs.getdbt.com/](https://docs.getdbt.com/)
- dbt Learn: [https://courses.getdbt.com/](https://courses.getdbt.com/)

### コミュニティ
- GitHub: [https://github.com/dbt-labs/dbt-core](https://github.com/dbt-labs/dbt-core)
- dbt Hub: [https://hub.getdbt.com/](https://hub.getdbt.com/)
- コミュニティ: [https://community.getdbt.com/](https://community.getdbt.com/)

## まとめ

dbt Coreは、以下の場面で特に有用です:

1. **データウェアハウスの変換管理** - SQLベースでデータ変換を定義し、Gitでバージョン管理
2. **データ品質の自動検証** - テストとフレッシュネスチェックをCI/CDに統合し、品質を継続的に担保
3. **データカタログの自動生成** - リネージグラフとカラム説明でデータの可視性を向上

SQLに慣れたデータエンジニアにとって、データ変換パイプラインの標準ツールとして活用できます。
