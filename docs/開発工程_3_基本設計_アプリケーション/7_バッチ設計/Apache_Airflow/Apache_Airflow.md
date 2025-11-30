# Apache Airflow（バッチ設計）

## 概要

Apache Airflowは、ワークフロー管理プラットフォームで、基本設計フェーズではバッチ処理フロー設計、ジョブスケジューリング設計、依存関係管理、エラーハンドリング設計に活用します。Pythonコードでバッチ処理を定義（DAG: Directed Acyclic Graph）し、可視化、実行、監視が可能です。

### 基本設計フェーズでの活用

- **バッチフロー設計**: タスクの依存関係と実行順序の定義
- **スケジュール設計**: 実行タイミング（日次、週次、月次、cron式）
- **リトライ設計**: エラー時の再試行ポリシー
- **並列実行設計**: 複数タスクの並列処理設計
- **データパイプライン設計**: ETL処理の設計
- **アラート設計**: 失敗時の通知設計

### 料金プラン

- **Apache Airflow**: 完全無料（Apache License 2.0）
- **Managed Airflow（AWS MWAA、Google Cloud Composer）**: 有料

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- Pythonコードでバッチ処理を定義（柔軟性が高い）
- Web UIでDAGの可視化と監視
- タスクの依存関係を明確に定義可能
- リトライ、アラート、並列実行等の機能が充実
- 豊富なプラグイン（Operator）でMySQL、PostgreSQL、S3等と連携

**デメリット**
- 学習コストが高い（Python、DAG概念の理解が必要）
- 小規模なバッチにはオーバースペック
- セットアップが複雑

## 利用方法

### 1. Apache Airflowのインストール

#### Dockerでのインストール（推奨）

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

#### pipでのインストール

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

### 2. DAG（Directed Acyclic Graph）の基本概念

DAGは、タスクの依存関係を表す有向非巡回グラフです。

**DAGの構成要素:**
- **Task（タスク）**: 個別の処理単位
- **Dependency（依存関係）**: タスク間の実行順序
- **Schedule（スケジュール）**: DAGの実行タイミング

**例: 日次売上集計バッチ**

```
[データ抽出] → [データ変換] → [データ集計] → [レポート生成] → [メール送信]
```

### 3. DAGファイルの作成

#### 例: 日次売上集計DAG

**ファイル配置:** `dags/daily_sales_report.py`

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.providers.amazon.aws.transfers.mysql_to_s3 import MySQLToS3Operator

# デフォルト引数
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,  # 過去の実行結果に依存しない
    'email': ['data-team@example.com'],
    'email_on_failure': True,  # 失敗時にメール通知
    'email_on_retry': False,
    'retries': 3,  # リトライ回数
    'retry_delay': timedelta(minutes=5),  # リトライ間隔
    'execution_timeout': timedelta(hours=2),  # タイムアウト時間
}

# DAG定義
dag = DAG(
    dag_id='daily_sales_report',
    default_args=default_args,
    description='日次売上集計バッチ処理',
    schedule_interval='0 2 * * *',  # 毎日2:00 AM実行（cron形式）
    start_date=datetime(2025, 1, 1),
    catchup=False,  # 過去の未実行分を実行しない
    tags=['sales', 'daily', 'report'],
)

# タスク1: データ抽出
def extract_sales_data(**context):
    """
    MySQLから前日の売上データを抽出
    """
    execution_date = context['execution_date']
    target_date = execution_date - timedelta(days=1)

    import mysql.connector

    conn = mysql.connector.connect(
        host='mysql-server',
        user='etl_user',
        password='password',
        database='sales_db'
    )
    cursor = conn.cursor()

    query = """
        SELECT
            order_id,
            customer_id,
            product_id,
            quantity,
            unit_price,
            total_amount,
            order_date
        FROM orders
        WHERE DATE(order_date) = %s
    """

    cursor.execute(query, (target_date.date(),))
    results = cursor.fetchall()

    # XComに保存（次のタスクに渡す）
    context['task_instance'].xcom_push(key='sales_data', value=results)

    cursor.close()
    conn.close()

    print(f"抽出件数: {len(results)}件")

extract_task = PythonOperator(
    task_id='extract_sales_data',
    python_callable=extract_sales_data,
    provide_context=True,
    dag=dag,
)

# タスク2: データ変換
def transform_sales_data(**context):
    """
    抽出したデータを変換・クレンジング
    """
    # XComから前のタスクの結果を取得
    sales_data = context['task_instance'].xcom_pull(
        task_ids='extract_sales_data',
        key='sales_data'
    )

    import pandas as pd

    # DataFrameに変換
    df = pd.DataFrame(sales_data, columns=[
        'order_id', 'customer_id', 'product_id',
        'quantity', 'unit_price', 'total_amount', 'order_date'
    ])

    # データクレンジング
    df = df.dropna()  # NULL値除去
    df = df[df['total_amount'] >= 0]  # 負の金額除去

    # 変換済みデータをXComに保存
    context['task_instance'].xcom_push(
        key='transformed_data',
        value=df.to_dict('records')
    )

    print(f"変換後件数: {len(df)}件")

transform_task = PythonOperator(
    task_id='transform_sales_data',
    python_callable=transform_sales_data,
    provide_context=True,
    dag=dag,
)

# タスク3: データ集計
def aggregate_sales_data(**context):
    """
    商品別・カテゴリ別の売上集計
    """
    transformed_data = context['task_instance'].xcom_pull(
        task_ids='transform_sales_data',
        key='transformed_data'
    )

    import pandas as pd

    df = pd.DataFrame(transformed_data)

    # 商品別集計
    product_summary = df.groupby('product_id').agg({
        'quantity': 'sum',
        'total_amount': 'sum'
    }).reset_index()

    # 集計結果をXComに保存
    context['task_instance'].xcom_push(
        key='product_summary',
        value=product_summary.to_dict('records')
    )

    print(f"集計完了: {len(product_summary)}商品")

aggregate_task = PythonOperator(
    task_id='aggregate_sales_data',
    python_callable=aggregate_sales_data,
    provide_context=True,
    dag=dag,
)

# タスク4: レポート生成（SQL実行）
generate_report_sql = MySqlOperator(
    task_id='generate_report',
    mysql_conn_id='mysql_default',
    sql="""
        INSERT INTO daily_sales_summary (
            report_date,
            total_orders,
            total_revenue,
            created_at
        )
        SELECT
            '{{ ds }}' AS report_date,
            COUNT(*) AS total_orders,
            SUM(total_amount) AS total_revenue,
            NOW() AS created_at
        FROM orders
        WHERE DATE(order_date) = '{{ ds }}'
    """,
    dag=dag,
)

# タスク5: S3へのエクスポート
export_to_s3 = MySQLToS3Operator(
    task_id='export_to_s3',
    mysql_conn_id='mysql_default',
    query="""
        SELECT * FROM daily_sales_summary
        WHERE report_date = '{{ ds }}'
    """,
    s3_bucket='sales-reports',
    s3_key='daily/{{ ds }}/sales_summary.csv',
    replace=True,
    dag=dag,
)

# タスク6: 完了通知
def send_completion_email(**context):
    """
    処理完了メールを送信
    """
    execution_date = context['execution_date']

    from airflow.utils.email import send_email

    send_email(
        to=['manager@example.com'],
        subject=f'[Airflow] 日次売上集計完了 - {execution_date.date()}',
        html_content=f"""
        <h3>日次売上集計が完了しました</h3>
        <p>実行日: {execution_date.date()}</p>
        <p>S3: s3://sales-reports/daily/{execution_date.date()}/sales_summary.csv</p>
        """
    )

notification_task = PythonOperator(
    task_id='send_completion_email',
    python_callable=send_completion_email,
    provide_context=True,
    dag=dag,
)

# タスク依存関係の定義
extract_task >> transform_task >> aggregate_task
aggregate_task >> generate_report_sql >> export_to_s3 >> notification_task
```

### 4. スケジュール設定

#### Cron形式でのスケジュール

| スケジュール | cron式 | 説明 |
|------------|--------|------|
| 毎日2時 | `0 2 * * *` | 日次バッチ |
| 毎週月曜2時 | `0 2 * * 1` | 週次バッチ |
| 毎月1日2時 | `0 2 1 * *` | 月次バッチ |
| 毎時0分 | `0 * * * *` | 時間単位バッチ |
| 15分ごと | `*/15 * * * *` | 短時間間隔バッチ |

#### プリセットスケジュール

```python
from airflow.timetables.trigger import CronTriggerTimetable

dag = DAG(
    dag_id='hourly_batch',
    schedule_interval='@hourly',  # 毎時0分実行
    # その他のプリセット:
    # '@daily' - 毎日0時
    # '@weekly' - 毎週日曜0時
    # '@monthly' - 毎月1日0時
    # '@yearly' - 毎年1月1日0時
)
```

### 5. タスク間のデータ受け渡し（XCom）

XCom（Cross-Communication）を使用してタスク間でデータを共有:

```python
# データをプッシュ
context['task_instance'].xcom_push(key='my_data', value={'count': 100})

# データをプル
data = context['task_instance'].xcom_pull(
    task_ids='previous_task',
    key='my_data'
)
```

### 6. 条件分岐（BranchPythonOperator）

#### 例: データ量に応じた処理分岐

```python
from airflow.operators.python import BranchPythonOperator

def check_data_volume(**context):
    """
    データ量をチェックして処理を分岐
    """
    sales_data = context['task_instance'].xcom_pull(
        task_ids='extract_sales_data',
        key='sales_data'
    )

    if len(sales_data) > 10000:
        return 'heavy_processing'  # 大量データ処理タスクへ
    else:
        return 'light_processing'  # 軽量処理タスクへ

branch_task = BranchPythonOperator(
    task_id='check_data_volume',
    python_callable=check_data_volume,
    provide_context=True,
    dag=dag,
)

heavy_task = BashOperator(
    task_id='heavy_processing',
    bash_command='python heavy_process.py',
    dag=dag,
)

light_task = BashOperator(
    task_id='light_processing',
    bash_command='python light_process.py',
    dag=dag,
)

extract_task >> branch_task >> [heavy_task, light_task]
```

### 7. 並列実行

#### 複数タスクの並列実行

```python
# タスク定義
task_a = PythonOperator(task_id='task_a', ...)
task_b = PythonOperator(task_id='task_b', ...)
task_c = PythonOperator(task_id='task_c', ...)
task_d = PythonOperator(task_id='task_d', ...)

# 並列実行の依存関係
#       task_a
#      /      \
#  task_b    task_c
#      \      /
#       task_d

task_a >> [task_b, task_c]  # task_a実行後、task_bとtask_cを並列実行
[task_b, task_c] >> task_d  # 両方完了後、task_d実行
```

### 8. エラーハンドリング

#### リトライとタイムアウト

```python
task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    retries=3,  # 最大3回リトライ
    retry_delay=timedelta(minutes=5),  # 5分間隔でリトライ
    retry_exponential_backoff=True,  # 指数バックオフ（5分、10分、20分）
    max_retry_delay=timedelta(hours=1),  # 最大リトライ間隔
    execution_timeout=timedelta(hours=2),  # 2時間でタイムアウト
    dag=dag,
)
```

#### エラー時のコールバック

```python
def on_failure_callback(context):
    """
    タスク失敗時のコールバック関数
    """
    task_instance = context['task_instance']
    exception = context.get('exception')

    # Slackに通知
    from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
    slack = SlackWebhookHook(slack_webhook_conn_id='slack_webhook')
    slack.send(
        text=f"❌ Task Failed: {task_instance.task_id}\nError: {exception}"
    )

task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    on_failure_callback=on_failure_callback,
    dag=dag,
)
```

### 9. センサー（Sensor）

外部イベントやファイルの存在を待機:

#### ファイルセンサー

```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id='wait_for_csv',
    filepath='/data/input/sales_{{ ds }}.csv',
    poke_interval=60,  # 60秒ごとにチェック
    timeout=3600,  # 1時間待機
    mode='poke',  # poke（ポーリング）またはreschedule
    dag=dag,
)

wait_for_file >> extract_task
```

### 10. バッチ設計書の作成

#### バッチ設計書の構成

**1. バッチ概要**

| 項目 | 内容 |
|------|------|
| バッチID | daily_sales_report |
| バッチ名 | 日次売上集計バッチ |
| 目的 | 前日の売上データを集計し、レポートを生成 |
| 実行タイミング | 毎日2:00 AM |
| 実行時間 | 約30分（推定） |
| 依存バッチ | なし |

**2. タスク一覧**

| No. | タスクID | タスク名 | 処理内容 | 想定実行時間 |
|-----|---------|---------|---------|------------|
| 1 | extract_sales_data | データ抽出 | MySQLから前日売上データを抽出 | 5分 |
| 2 | transform_sales_data | データ変換 | データクレンジング | 3分 |
| 3 | aggregate_sales_data | データ集計 | 商品別・カテゴリ別集計 | 10分 |
| 4 | generate_report | レポート生成 | サマリーテーブルへ登録 | 2分 |
| 5 | export_to_s3 | S3エクスポート | CSVファイルをS3に保存 | 5分 |
| 6 | send_completion_email | 完了通知 | 処理完了メール送信 | 1分 |

**3. データフロー図**

```
┌──────────────┐
│ MySQLデータベース │
└───────┬──────┘
        ↓ (抽出)
┌──────────────┐
│ XCom: sales_data │
└───────┬──────┘
        ↓ (変換)
┌─────────────────┐
│ XCom: transformed_data │
└───────┬─────────┘
        ↓ (集計)
┌─────────────────┐
│ XCom: product_summary │
└───────┬─────────┘
        ↓ (登録)
┌─────────────────┐
│ daily_sales_summary │
└───────┬─────────┘
        ↓ (エクスポート)
┌─────────────────┐
│ S3: sales_summary.csv │
└─────────────────┘
```

**4. エラーハンドリング**

| エラーケース | 対処方法 |
|------------|---------|
| データベース接続失敗 | 5分間隔で3回リトライ |
| データ抽出件数0件 | ログに記録し、処理継続 |
| S3アップロード失敗 | リトライ後、メール通知 |
| タイムアウト（2時間） | 処理を中断し、アラート送信 |

**5. 監視・アラート**

| 監視項目 | 閾値 | アラート先 |
|---------|------|-----------|
| 実行時間 | 60分以上 | data-team@example.com |
| タスク失敗 | 1回でも失敗 | data-team@example.com, Slack |
| データ件数 | 0件 | 警告ログ |

### 11. Web UIでの監視

Airflow Web UI（http://localhost:8080）で以下を確認:

- **DAGs**: DAG一覧と実行履歴
- **Graph View**: DAGの依存関係を可視化
- **Gantt Chart**: タスクの実行時間をガントチャートで表示
- **Tree View**: 過去の実行履歴をツリー表示
- **Logs**: 各タスクの実行ログ

## 公式ドキュメント

- **公式サイト**: [Apache Airflow](https://airflow.apache.org/)
- **ドキュメント**: [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- **チュートリアル**: [Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- **Concepts**: [Core Concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)

## 学習リソース

- **公式チュートリアル**: [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- **YouTube**: [Apache Airflow Tutorial](https://www.youtube.com/results?search_query=apache+airflow+tutorial)
- **Udemy**: [Apache Airflow Course](https://www.udemy.com/topic/apache-airflow/)

## 関連リンク

- [AWS MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/)（マネージドAirflow）
- [Google Cloud Composer](https://cloud.google.com/composer)（マネージドAirflow）
- [Prefect](https://www.prefect.io/)（Airflow代替ツール）
- [Dagster](https://dagster.io/)（データオーケストレーションツール）
