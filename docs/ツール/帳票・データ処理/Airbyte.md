# Airbyte

## 概要

**Airbyte**は、オープンソースのELT（Extract, Load, Transform）データ統合プラットフォームです。300以上のデータソースとデスティネーションをサポートし、データパイプラインの構築を簡素化します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Airbyte Inc. |
| **種別** | ELT / データパイプライン |
| **ライセンス** | オープンソース（MIT License）+ Enterprise版 |
| **料金** | 🟡 一部無料（オープンソース版無料、Cloud版は従量課金） |
| **公式サイト** | https://airbyte.com/ |
| **ドキュメント** | https://docs.airbyte.com/ |

## 主な特徴

### 1. 豊富なコネクタライブラリ
- 300以上のビルトインコネクタ
- データベース（PostgreSQL, MySQL, MongoDB等）
- SaaS（Salesforce, HubSpot, Google Analytics等）
- クラウドストレージ（S3, GCS, Azure Blob等）
- データウェアハウス（BigQuery, Snowflake, Redshift等）

### 2. Connector Development Kit (CDK)
- Python/Java/Low-codeでカスタムコネクタ開発
- コネクタの自動テスト機能
- コミュニティによるコネクタ貢献

### 3. デプロイメントオプション
- **Airbyte Cloud**: マネージドサービス
- **Airbyte Open Source**: セルフホスト版（Docker/Kubernetes）
- **Airbyte Enterprise**: エンタープライズ機能追加版

### 4. スケーラビリティ
- 大規模データ同期に対応
- インクリメンタル同期（差分同期）
- 並列処理によるパフォーマンス最適化

## 使い方

### インストール（Docker Compose）

```bash
# Airbyteリポジトリをクローン
git clone https://github.com/airbytehq/airbyte.git
cd airbyte

# Docker Composeで起動
./run-ab-platform.sh

# ブラウザでアクセス
# http://localhost:8000
# 初期ユーザー: airbyte@example.com
# 初期パスワード: password
```

### 基本的なデータパイプライン設定

#### 1. ソース設定（PostgreSQL例）

```yaml
# source_config.json
{
  "sourceType": "postgres",
  "host": "db.example.com",
  "port": 5432,
  "database": "production_db",
  "username": "readonly_user",
  "password": "secure_password",
  "ssl": true,
  "replication_method": {
    "method": "CDC",
    "plugin": "pgoutput"
  }
}
```

#### 2. デスティネーション設定（Snowflake例）

```yaml
# destination_config.json
{
  "destinationType": "snowflake",
  "host": "account.snowflakecomputing.com",
  "role": "AIRBYTE_ROLE",
  "warehouse": "COMPUTE_WH",
  "database": "ANALYTICS_DB",
  "schema": "RAW_DATA",
  "username": "airbyte_user",
  "credentials": {
    "auth_type": "OAuth2.0"
  }
}
```

#### 3. 接続（Connection）設定

```yaml
# connection_config.yaml
name: "PostgreSQL to Snowflake Sync"
source_id: "source-postgres-001"
destination_id: "dest-snowflake-001"
schedule:
  units: 24
  timeUnit: hours
namespaceDefinition: customformat
namespaceFormat: "${SOURCE_NAMESPACE}"
prefix: "raw_"
syncCatalog:
  streams:
    - stream:
        name: "users"
        namespace: "public"
      config:
        syncMode: incremental
        cursorField: ["updated_at"]
        destinationSyncMode: append_dedup
        primaryKey: [["id"]]
```

### Kubernetes上へのデプロイ

```yaml
# airbyte-values.yaml
global:
  deploymentMode: oss

webapp:
  replicaCount: 2
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"

server:
  replicaCount: 2

worker:
  replicaCount: 3
  resources:
    requests:
      memory: "512Mi"
      cpu: "200m"
    limits:
      memory: "2Gi"
      cpu: "1000m"

postgresql:
  enabled: true
  postgresqlPassword: "airbyte_db_password"
```

```bash
# Helmチャートでインストール
helm repo add airbyte https://airbytehq.github.io/helm-charts
helm install airbyte airbyte/airbyte -f airbyte-values.yaml
```

### APIによる操作

```python
# airbyte_client.py
import requests
import json

AIRBYTE_URL = "http://localhost:8000/api/v1"

# 接続の作成
def create_connection():
    url = f"{AIRBYTE_URL}/connections/create"

    payload = {
        "sourceId": "source-postgres-001",
        "destinationId": "dest-snowflake-001",
        "syncCatalog": {
            "streams": [
                {
                    "stream": {
                        "name": "orders",
                        "namespace": "public"
                    },
                    "config": {
                        "syncMode": "incremental",
                        "cursorField": ["created_at"],
                        "destinationSyncMode": "append_dedup",
                        "primaryKey": [["order_id"]]
                    }
                }
            ]
        },
        "schedule": {
            "units": 6,
            "timeUnit": "hours"
        }
    }

    response = requests.post(url, json=payload)
    return response.json()

# 手動同期のトリガー
def trigger_sync(connection_id):
    url = f"{AIRBYTE_URL}/connections/sync"
    payload = {"connectionId": connection_id}

    response = requests.post(url, json=payload)
    return response.json()

# 同期ステータスの確認
def check_sync_status(job_id):
    url = f"{AIRBYTE_URL}/jobs/get"
    payload = {"id": job_id}

    response = requests.post(url, json=payload)
    return response.json()
```

### dbtとの統合

```yaml
# profiles.yml
airbyte_dbt:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: your_account
      user: dbt_user
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: DBT_ROLE
      database: ANALYTICS_DB
      warehouse: TRANSFORM_WH
      schema: transformed
      threads: 4
```

```sql
-- models/staging/stg_users.sql
-- Airbyteから取り込んだデータを変換
{{
    config(
        materialized='incremental',
        unique_key='user_id'
    )
}}

select
    _airbyte_raw_id,
    cast(_airbyte_data:id as integer) as user_id,
    cast(_airbyte_data:email as varchar) as email,
    cast(_airbyte_data:created_at as timestamp) as created_at,
    _airbyte_emitted_at as loaded_at
from {{ source('airbyte_raw', 'users') }}

{% if is_incremental() %}
where _airbyte_emitted_at > (select max(loaded_at) from {{ this }})
{% endif %}
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | データパイプライン実装 | 外部データソースとの統合 |
| **テスト** | データ統合テスト | テスト環境へのデータ同期 |
| **導入** | 本番データ移行 | 旧システムから新システムへのデータ移行 |

## メリット

- **オープンソース**: 無料で利用可能、コミュニティサポート
- **豊富なコネクタ**: 300以上のデータソースに対応
- **カスタマイズ性**: CDKで独自コネクタ開発が容易
- **デプロイの柔軟性**: Cloud、セルフホスト、Enterprise版から選択可能
- **スケーラビリティ**: 大規模データ同期に対応
- **dbt統合**: データ変換ワークフローとシームレス連携
- **API完備**: プログラマティックな操作が可能

## デメリット

- **初期学習コスト**: コネクタ設定・スケジュール管理の理解が必要
- **リソース消費**: 大規模同期時にはCPU・メモリを消費
- **複雑な変換には不向き**: Extract/Loadが主機能、複雑な変換はdbt等と併用推奨
- **Cloud版のコスト**: データ量が増えると従量課金が高額化
- **セルフホスト版の運用負荷**: インフラ管理・アップデート対応が必要

## 類似ツールとの比較

| ツール | 特徴 | コスト | 適用場面 |
|--------|------|--------|----------|
| **Airbyte** | オープンソースELT、300+コネクタ | 無料〜従量課金 | コスト重視・カスタマイズ重視 |
| **Fivetran** | マネージドELT、500+コネクタ | 有料（従量課金） | エンタープライズ、運用負荷削減 |
| **Stitch Data** | Talend製ELT | 有料 | Talendエコシステム利用 |
| **Apache NiFi** | データフロー自動化 | 無料 | 複雑なデータフロー制御 |

## ベストプラクティス

### 1. インクリメンタル同期の活用

```yaml
# ベストプラクティス: カーソルフィールドで差分同期
syncMode: incremental
cursorField: ["updated_at"]
destinationSyncMode: append_dedup
primaryKey: [["id"]]
```

### 2. スケジュール設定の最適化

```yaml
# データ鮮度とリソース消費のバランス
schedule:
  units: 6  # 6時間ごと（業務要件に応じて調整）
  timeUnit: hours
```

### 3. 監視とアラート

```python
# Prometheus監視例
import requests
from prometheus_client import Gauge

sync_status_gauge = Gauge('airbyte_sync_status', 'Airbyte sync job status', ['connection'])

def monitor_connections():
    connections = get_all_connections()
    for conn in connections:
        latest_job = get_latest_job(conn['connectionId'])
        status = 1 if latest_job['status'] == 'succeeded' else 0
        sync_status_gauge.labels(connection=conn['name']).set(status)
```

## 公式リソース

- **公式サイト**: https://airbyte.com/
- **ドキュメント**: https://docs.airbyte.com/
- **GitHub**: https://github.com/airbytehq/airbyte
- **コネクタカタログ**: https://docs.airbyte.com/integrations/
- **コミュニティSlack**: https://airbyte.com/community

## まとめ

Airbyteは、オープンソースのELTプラットフォームとして、データ統合・移行作業を大幅に効率化します。豊富なコネクタ、カスタマイズ性、dbtとの統合により、現代のデータスタックに最適なツールです。導入フェーズのデータ移行から、本番運用時の継続的なデータ同期まで、幅広く活用できます。

---

**最終更新**: 2025-12-06
**対象バージョン**: Airbyte v0.50+
