# Celery

## 概要

**Celery**は、Pythonベースの分散タスクキューシステムです。非同期タスク実行、スケジューリング、リアルタイム処理により、Webアプリケーションの重い処理をバックグラウンドで実行し、レスポンス性能を向上させます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Ask Solem Hoel / オープンソースコミュニティ |
| **種別** | 分散タスクキュー・非同期処理フレームワーク |
| **ライセンス** | BSD License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://docs.celeryq.dev/ |
| **ドキュメント** | https://docs.celeryq.dev/en/stable/ |

## 主な特徴

### 1. 非同期タスク実行
- **遅延実行**: `task.delay()`で即座にリターン
- **結果取得**: AsyncResultオブジェクトで状態監視
- **チェイン・グループ**: タスクの連鎖・並列実行
- **優先度制御**: タスク優先度設定

### 2. メッセージブローカー対応
- **Redis**: 高速、開発・本番推奨
- **RabbitMQ**: 高機能、エンタープライズ向け
- **Amazon SQS**: クラウドネイティブ
- **その他**: Kafka、ZeroMQ対応

### 3. 定期実行（Celery Beat）
- **Crontab**: cron形式スケジュール
- **Interval**: 定期実行（秒/分/時間）
- **Solar**: 日の出・日の入りベース
- **動的スケジュール**: Django Admin連携

### 4. 結果バックエンド
- **Redis**: 高速、推奨
- **Database**: SQLAlchemy、Django ORM
- **Memcached**: キャッシュ
- **Elasticsearch**: 検索・分析

## 使い方

### セットアップ

```bash
# Celeryインストール（Redis使用）
pip install celery[redis]

# またはRabbitMQ使用
pip install celery[amqp]

# その他依存関係
pip install redis  # Redisクライアント
```

### 基本設定

```python
# celery_app.py
from celery import Celery

# Celeryアプリケーション作成
app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',  # メッセージブローカー
    backend='redis://localhost:6379/0'  # 結果バックエンド
)

# 設定
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Tokyo',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分
    task_soft_time_limit=25 * 60,  # 25分（警告）
)
```

### タスク定義

```python
# tasks.py
from celery_app import app
import time
import requests

@app.task
def add(x, y):
    """シンプルなタスク"""
    return x + y

@app.task(bind=True)
def long_task(self, iterations):
    """進捗を報告するタスク"""
    for i in range(iterations):
        time.sleep(1)
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': iterations}
        )
    return {'current': iterations, 'total': iterations, 'status': 'Complete!'}

@app.task(bind=True, max_retries=3)
def fetch_url(self, url):
    """リトライ機能付きタスク"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        # 指数バックオフでリトライ
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

@app.task
def send_email(to, subject, body):
    """メール送信タスク"""
    # メール送信処理
    print(f"Sending email to {to}: {subject}")
    return f"Email sent to {to}"
```

### タスク実行

```python
# main.py
from tasks import add, long_task, fetch_url, send_email

# 非同期実行
result = add.delay(4, 6)
print(f"Task ID: {result.id}")

# 結果取得（ブロッキング）
print(f"Result: {result.get(timeout=10)}")

# 状態確認
if result.ready():
    print("Task completed")
    print(f"Result: {result.result}")
elif result.failed():
    print("Task failed")
    print(f"Error: {result.traceback}")
else:
    print("Task pending or running")

# 進捗監視
task = long_task.delay(100)
while not task.ready():
    if task.state == 'PROGRESS':
        meta = task.info
        print(f"Progress: {meta['current']}/{meta['total']}")
    time.sleep(1)

# 複数タスク実行
results = [add.delay(i, i) for i in range(10)]
for result in results:
    print(result.get())
```

### Celery Worker起動

```bash
# Workerプロセス起動
celery -A celery_app worker --loglevel=info

# 複数ワーカー（並列処理）
celery -A celery_app worker --concurrency=4

# デーモン化（バックグラウンド）
celery -A celery_app worker --detach --loglevel=info --logfile=celery.log

# 特定キューのみ処理
celery -A celery_app worker -Q high_priority,default

# Autoscale（動的ワーカー数調整）
celery -A celery_app worker --autoscale=10,3  # max 10, min 3
```

### Celery Beat（定期実行）

```python
# celery_app.py
from celery import Celery
from celery.schedules import crontab

app = Celery('myapp', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,  # 30秒ごと
        'args': (16, 16)
    },
    'send-report-every-monday': {
        'task': 'tasks.send_weekly_report',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # 毎週月曜 9:00
    },
    'cleanup-every-night': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # 毎日 2:00
    },
}

app.conf.timezone = 'Asia/Tokyo'
```

```bash
# Beatスケジューラー起動
celery -A celery_app beat --loglevel=info

# Worker + Beat同時起動（開発環境のみ）
celery -A celery_app worker -B --loglevel=info
```

### Django統合

```python
# myproject/celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

```python
# myproject/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)
```

```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tokyo'
```

```python
# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification(user_id, message):
    from .models import User
    user = User.objects.get(id=user_id)
    send_mail(
        'Notification',
        message,
        'noreply@example.com',
        [user.email],
    )
    return f"Sent to {user.email}"
```

### Flask統合

```python
# app.py
from flask import Flask
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = make_celery(app)

@celery.task
def process_data(data):
    # 重い処理
    import time
    time.sleep(10)
    return f"Processed {len(data)} items"

@app.route('/process', methods=['POST'])
def process():
    data = request.json.get('data', [])
    task = process_data.delay(data)
    return {'task_id': task.id}, 202
```

### チェイン・グループ

```python
# tasks.py
from celery import chain, group, chord
from celery_app import app

@app.task
def multiply(x, y):
    return x * y

@app.task
def add(x, y):
    return x + y

@app.task
def summarize(results):
    return sum(results)

# チェイン（順次実行）
result = chain(add.s(2, 2), multiply.s(4)).apply_async()
# (2 + 2) * 4 = 16
print(result.get())

# グループ（並列実行）
job = group([
    add.s(2, 2),
    add.s(4, 4),
    add.s(8, 8),
])
result = job.apply_async()
print(result.get())  # [4, 8, 16]

# Chord（並列実行 → 結果を集約）
callback = summarize.s()
header = group([add.s(i, i) for i in range(10)])
result = chord(header)(callback)
print(result.get())  # 90
```

### 監視（Flower）

```bash
# Flowerインストール
pip install flower

# Flower起動
celery -A celery_app flower

# ブラウザでアクセス
# http://localhost:5555
```

### エラーハンドリング

```python
# tasks.py
from celery import Task
from celery_app import app

class CallbackTask(Task):
    """カスタムタスククラス"""
    def on_success(self, retval, task_id, args, kwargs):
        print(f"Task {task_id} succeeded: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} failed: {exc}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} retrying: {exc}")

@app.task(base=CallbackTask, bind=True, max_retries=3)
def risky_task(self, data):
    try:
        # リスクのある処理
        if not data:
            raise ValueError("Empty data")
        return process(data)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
```

### Docker構成

```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: python app.py
    ports:
      - "5000:5000"
    depends_on:
      - redis
    environment:
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0

  celery_worker:
    build: .
    command: celery -A celery_app worker --loglevel=info
    depends_on:
      - redis
    environment:
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0

  celery_beat:
    build: .
    command: celery -A celery_app beat --loglevel=info
    depends_on:
      - redis
    environment:
      CELERY_BROKER_URL: redis://redis:6379/0

  flower:
    build: .
    command: celery -A celery_app flower
    ports:
      - "5555:5555"
    depends_on:
      - redis
    environment:
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | 非同期処理 | 重い処理のバックグラウンド実行 |
| **実装** | バッチ処理 | データ集計・変換処理 |
| **運用** | 定期実行 | レポート生成、クリーンアップ |
| **運用** | スケーリング | 負荷分散、水平スケーリング |

## メリット

- **非同期処理**: Webレスポンスの高速化
- **分散実行**: 複数ワーカーで負荷分散
- **スケジューリング**: Cron代替、柔軟な定期実行
- **リトライ機能**: 失敗時の自動再試行
- **監視ツール**: Flower、Prometheus統合
- **言語統合**: Python、Django、Flask
- **無料**: オープンソース

## デメリット

- **インフラ複雑化**: Redis/RabbitMQ必須
- **デバッグ困難**: 非同期処理のデバッグ
- **メモリ使用量**: 大量タスクでメモリ消費
- **シリアライズ制限**: JSON対応型のみ
- **Python専用**: 他言語は別ツール必要
- **設定複雑**: 本番環境の最適化が難しい

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Celery** | Python、分散、豊富な機能 | 無料 | Djangoアプリ、データ処理 |
| **RQ (Redis Queue)** | シンプル、Redis専用 | 無料 | 軽量タスク、Flask |
| **Dramatiq** | モダン、高速 | 無料 | Python汎用 |
| **AWS SQS + Lambda** | サーバーレス、マネージド | 従量課金 | クラウドネイティブ |

## ベストプラクティス

### 1. タスク設計

```python
# 冪等性を保つ
@app.task
def process_order(order_id):
    order = Order.objects.get(id=order_id)
    if order.status == 'processed':
        return 'Already processed'
    # 処理
    order.status = 'processed'
    order.save()
```

### 2. タイムアウト設定

```python
# タイムアウト・リトライ設定
@app.task(
    time_limit=300,  # 5分でKILL
    soft_time_limit=240,  # 4分で警告
    max_retries=3,
    default_retry_delay=60
)
def long_running_task():
    pass
```

### 3. 優先度キュー

```python
# 設定
app.conf.task_routes = {
    'tasks.high_priority_task': {'queue': 'high'},
    'tasks.low_priority_task': {'queue': 'low'},
}

# Worker起動
# celery -A celery_app worker -Q high,default
# celery -A celery_app worker -Q low
```

### 4. 監視・ロギング

```python
# タスク実行時間監視
from celery.signals import task_prerun, task_postrun
import time

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, **kwargs):
    print(f"Task {task_id} started")

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, **kwargs):
    print(f"Task {task_id} completed")
```

## 公式リソース

- **公式サイト**: https://docs.celeryq.dev/
- **ドキュメント**: https://docs.celeryq.dev/en/stable/
- **GitHub**: https://github.com/celery/celery
- **Flower**: https://flower.readthedocs.io/
- **チュートリアル**: https://docs.celeryq.dev/en/stable/getting-started/

## まとめ

Celeryは、Pythonベースの分散タスクキューシステムです。非同期タスク実行、定期スケジューリング、リトライ機能により、Webアプリケーションの重い処理をバックグラウンドで実行し、レスポンス性能を向上させます。Django・Flask統合、豊富な監視ツールにより、本番環境でのスケーラブルなタスク処理を実現します。

---

**最終更新**: 2025-12-10
**対象バージョン**: Celery 5.3+
