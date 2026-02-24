# Apache Airflow

## 概要

Apache Airflowは、Pythonベースのワークフロー管理プラットフォームで、バッチ処理フロー設計、ジョブスケジューリング、依存関係管理、エラーハンドリングに活用します。DAG（Directed Acyclic Graph）としてタスクの依存関係をコードで定義し、Web UIによる可視化、実行、監視が可能です。

## 主な特徴

| 項目 | 内容 |
|------|------|
| 開発元 | Apache Software Foundation |
| ライセンス | Apache License 2.0（無料） |
| 言語 | Python |
| UI | Web UIでDAGの可視化・監視 |
| スケジューリング | cron形式・プリセットによる柔軟なスケジュール |
| 拡張性 | 豊富なOperatorプラグインでMySQL、PostgreSQL、S3等と連携 |
| マネージドサービス | AWS MWAA、Google Cloud Composer（有料） |

## 主な機能

### DAG管理

| 機能 | 説明 |
|------|------|
| DAG定義 | Pythonコードでタスクの依存関係を定義 |
| スケジュール設定 | cron式・プリセットによる実行タイミング制御 |
| 条件分岐 | BranchPythonOperatorによるデータ量等に応じた処理分岐 |
| 並列実行 | 複数タスクの並列処理 |

### データ連携

| 機能 | 説明 |
|------|------|
| XCom | タスク間のデータ受け渡し（Cross-Communication） |
| センサー | 外部イベントやファイルの存在を待機（FileSensor等） |
| Operator | MySQL、S3、Slack等との豊富な連携プラグイン |

### エラーハンドリング・監視

| 機能 | 説明 |
|------|------|
| リトライ | 回数、間隔、指数バックオフの設定 |
| タイムアウト | タスク単位のタイムアウト設定 |
| コールバック | on_failure_callbackによるSlack等への通知 |
| Web UI監視 | Graph View、Gantt Chart、Tree View、ログ確認 |

## インストールとセットアップ

公式URL:
- [Apache Airflow](https://airflow.apache.org/)
- [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)

### Dockerでのインストール（推奨）

```bash
# Docker Composeファイルをダウンロード
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'

# ユーザーIDを設定
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Airflowを起動
docker-compose up airflow-init
docker-compose up

# WebUIにアクセス: http://localhost:8080
# ユーザー名: airflow
# パスワード: airflow
```

### pipでのインストール

```bash
# Python 3.8以上が必要
pip install apache-airflow==2.8.0

# 初期化
airflow db init

# ユーザー作成
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Webサーバー起動
airflow webserver --port 8080

# スケジューラー起動（別ターミナル）
airflow scheduler
```

## 基本的な使い方

### 1. DAGファイルの作成

DAGは、タスクの依存関係を表す有向非巡回グラフです。ファイルは `dags/` ディレクトリに配置します。

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# デフォルト引数
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# DAG定義
dag = DAG(
    dag_id='daily_sales_report',
    default_args=default_args,
    description='日次売上集計バッチ処理',
    schedule_interval='0 2 * * *',  # 毎日2:00 AM実行
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['sales', 'daily', 'report'],
)
```

### 2. タスクの定義とデータ受け渡し

```python
def extract_sales_data(**context):
    """MySQLから前日の売上データを抽出"""
    execution_date = context['execution_date']
    target_date = execution_date - timedelta(days=1)
    # データ抽出処理...
    context['task_instance'].xcom_push(key='sales_data', value=results)

extract_task = PythonOperator(
    task_id='extract_sales_data',
    python_callable=extract_sales_data,
    provide_context=True,
    dag=dag,
)

def transform_sales_data(**context):
    """抽出したデータを変換・クレンジング"""
    sales_data = context['task_instance'].xcom_pull(
        task_ids='extract_sales_data', key='sales_data'
    )
    # 変換処理...

transform_task = PythonOperator(
    task_id='transform_sales_data',
    python_callable=transform_sales_data,
    provide_context=True,
    dag=dag,
)

# タスク依存関係の定義
extract_task >> transform_task
```

### 3. スケジュール設定

| スケジュール | cron式 | 説明 |
|------------|--------|------|
| 毎日2時 | `0 2 * * *` | 日次バッチ |
| 毎週月曜2時 | `0 2 * * 1` | 週次バッチ |
| 毎月1日2時 | `0 2 1 * *` | 月次バッチ |
| 毎時0分 | `0 * * * *` | 時間単位バッチ |
| 15分ごと | `*/15 * * * *` | 短時間間隔バッチ |

プリセット: `@daily`、`@hourly`、`@weekly`、`@monthly`、`@yearly`

### 4. 条件分岐

```python
from airflow.operators.python import BranchPythonOperator

def check_data_volume(**context):
    sales_data = context['task_instance'].xcom_pull(
        task_ids='extract_sales_data', key='sales_data'
    )
    if len(sales_data) > 10000:
        return 'heavy_processing'
    else:
        return 'light_processing'

branch_task = BranchPythonOperator(
    task_id='check_data_volume',
    python_callable=check_data_volume,
    provide_context=True,
    dag=dag,
)
```

### 5. エラーハンドリング

```python
def on_failure_callback(context):
    """タスク失敗時のSlack通知"""
    task_instance = context['task_instance']
    exception = context.get('exception')
    from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
    slack = SlackWebhookHook(slack_webhook_conn_id='slack_webhook')
    slack.send(text=f"Task Failed: {task_instance.task_id}\nError: {exception}")

task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    execution_timeout=timedelta(hours=2),
    on_failure_callback=on_failure_callback,
    dag=dag,
)
```

### 6. センサー

```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id='wait_for_csv',
    filepath='/data/input/sales_{{ ds }}.csv',
    poke_interval=60,
    timeout=3600,
    mode='poke',
    dag=dag,
)

wait_for_file >> extract_task
```

## Docker での使用

### docker-compose.yml 例

```yaml
# Docker Composeファイルをダウンロード
# curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'

# カスタマイズ例
version: '3.8'
services:
  airflow-webserver:
    image: apache/airflow:2.8.0
    command: webserver
    ports:
      - "8080:8080"
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
    volumes:
      - ./dags:/opt/airflow/dags

  airflow-scheduler:
    image: apache/airflow:2.8.0
    command: scheduler
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
    volumes:
      - ./dags:/opt/airflow/dags
```

## 他ツールとの比較

### Apache Airflow vs Prefect

| 機能 | Apache Airflow | Prefect |
|------|---------------|---------|
| DAG定義 | Python（静的DAG） | Python（動的フロー） |
| UI | Web UI標準搭載 | Cloud UIまたはOSS Server |
| スケジューリング | 内蔵 | Prefect Server/Cloud |
| 学習コスト | 高い | 比較的低い |
| コミュニティ | 非常に大きい | 成長中 |

### Apache Airflow vs Dagster

| 機能 | Apache Airflow | Dagster |
|------|---------------|---------|
| コンセプト | タスクベース | アセットベース |
| テスト | 限定的 | ネイティブサポート |
| 型安全性 | なし | あり |
| ローカル開発 | 複雑 | 簡易 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| 日次ETLバッチ | データウェアハウスへのデータ集約 | DAGでデータ抽出・変換・ロード処理を自動化 |
| レポート自動生成 | 売上・KPIレポートの自動配信 | データ集計後にメールやSlackで通知 |
| データパイプライン | 複数データソースの統合 | Operatorで各種データソースを連携 |
| ML パイプライン | モデルの学習・評価・デプロイ | PythonOperatorで学習タスクをオーケストレーション |

## ベストプラクティス

### 1. DAG設計

- タスクの粒度を適切に保つ（1タスク=1責務）
- XComで大量データを渡さない（外部ストレージを利用）
- `catchup=False` でDAG作成時の過去分実行を防止

### 2. エラーハンドリング

- すべてのDAGに `on_failure_callback` を設定
- リトライ回数と間隔を適切に設定
- `execution_timeout` でタスクの暴走を防止

### 3. 運用

- DAGファイルはGitで管理
- テスト環境でDAGの動作確認を行ってからデプロイ
- Web UIの監視機能を活用し、失敗タスクを即座に検知

## トラブルシューティング

### よくある問題と解決策

#### 1. DAGがWeb UIに表示されない

```
原因: DAGファイルにインポートエラーや構文エラーがある
解決策: `python dags/my_dag.py` でファイルを直接実行してエラーを確認する
```

#### 2. タスクがスケジュール通りに実行されない

```
原因: スケジューラーが停止している、またはDAGが一時停止されている
解決策: `airflow scheduler` が稼働していることを確認し、Web UIでDAGのトグルをONにする
```

#### 3. XComでのデータ受け渡し失敗

```
原因: XComに保存するデータが大きすぎる（デフォルト上限あり）
解決策: 大きなデータはS3やGCS等の外部ストレージに保存し、パスのみをXComで渡す
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: [https://airflow.apache.org/](https://airflow.apache.org/)
- ドキュメント: [https://airflow.apache.org/docs/apache-airflow/stable/index.html](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- チュートリアル: [https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)

### コミュニティ
- GitHub: [https://github.com/apache/airflow](https://github.com/apache/airflow)
- AWS MWAA: [https://aws.amazon.com/managed-workflows-for-apache-airflow/](https://aws.amazon.com/managed-workflows-for-apache-airflow/)
- Google Cloud Composer: [https://cloud.google.com/composer](https://cloud.google.com/composer)

## まとめ

Apache Airflowは、以下の場面で特に有用です:

1. **データパイプラインの自動化** - DAGでETL処理の依存関係を明確に定義し、スケジュール実行を自動化
2. **バッチ処理の監視・管理** - Web UIでDAGの実行状況をリアルタイム監視し、障害時に即座に対応
3. **複雑なワークフローの設計** - 条件分岐、並列実行、センサーを組み合わせた柔軟なワークフロー構築

Pythonの知識があるチームにとって、データオーケストレーションのデファクトスタンダードとして活用できます。
