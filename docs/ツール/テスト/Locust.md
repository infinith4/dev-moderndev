# Locust

## 概要

Locustは、Pythonで記述するオープンソースの負荷テスト・パフォーマンステストツールです。Pythonコードでユーザー挙動を定義することで、柔軟で強力なテストシナリオを作成できます。分散実行により数百万の同時ユーザーをシミュレートでき、WebベースのリアルタイムUIでテスト結果を可視化します。開発者フレンドリーなコードベースのアプローチが特徴です。

## 主な機能

### 1. Pythonベース
- Pythonコードでシナリオ記述
- 柔軟なロジック実装
- 既存Pythonライブラリ活用
- バージョン管理容易

### 2. 分散負荷テスト
- マスター・ワーカー構成
- 複数マシンからの並列実行
- 数百万ユーザーシミュレート
- 動的ワーカー追加

### 3. Web UI
- リアルタイムグラフ
- 応答時間分布
- リクエスト統計
- 失敗率モニタリング

### 4. HTTP/WebSocketサポート
- REST API テスト
- WebSocket テスト
- カスタムクライアント作成可能

### 5. レポート
- HTML レポート生成
- CSV エクスポート
- カスタムメトリクス

## 利用方法

### インストール

```bash
# pip
pip install locust

# バージョン確認
locust --version
```

### 基本的なLocustfile作成

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # ユーザーの待機時間（秒）
    wait_time = between(1, 3)
    
    @task(3)  # 重み付け（3倍の頻度で実行）
    def view_items(self):
        self.client.get("/api/items")
    
    @task(1)
    def view_item(self):
        item_id = 1
        self.client.get(f"/api/items/{item_id}")
    
    @task(2)
    def create_item(self):
        self.client.post("/api/items", json={
            "name": "Test Item",
            "price": 100
        })
    
    def on_start(self):
        # 各ユーザーの開始時に1回実行
        self.client.post("/login", json={
            "username": "test",
            "password": "test123"
        })
```

### 認証・ヘッダー設定

```python
from locust import HttpUser, task

class AuthenticatedUser(HttpUser):
    def on_start(self):
        # ログイン
        response = self.client.post("/auth/login", json={
            "username": "user@example.com",
            "password": "password"
        })
        # トークン取得
        self.token = response.json()["token"]
    
    @task
    def get_profile(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/profile", headers=headers)
```

### カスタムレスポンス検証

```python
from locust import HttpUser, task
import json

class APIUser(HttpUser):
    @task
    def get_users(self):
        with self.client.get("/api/users", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    response.success()
                else:
                    response.failure("No users returned")
            else:
                response.failure(f"Got status code {response.status_code}")
```

### 実行

```bash
# Web UI起動
locust -f locustfile.py

# ブラウザで http://localhost:8089 にアクセス
# Number of users: 100
# Spawn rate: 10 (users/sec)
# Host: https://api.example.com
# Start swarming

# CLI実行（ヘッドレス）
locust -f locustfile.py --headless \
  --users 100 --spawn-rate 10 \
  --host https://api.example.com \
  --run-time 5m \
  --html report.html
```

### 分散実行

```bash
# マスターノード
locust -f locustfile.py --master

# ワーカーノード（別マシンで実行）
locust -f locustfile.py --worker --master-host=192.168.1.100

# 複数ワーカー（同一マシン）
locust -f locustfile.py --worker --master-host=localhost &
locust -f locustfile.py --worker --master-host=localhost &
locust -f locustfile.py --worker --master-host=localhost &
```

## CI/CD統合

### GitHub Actions

```yaml
name: Load Test

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜日
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Locust
        run: pip install locust
      
      - name: Run Load Test
        run: |
          locust -f locustfile.py --headless \
            --users 100 --spawn-rate 10 \
            --host https://staging.example.com \
            --run-time 5m \
            --html report.html \
            --csv results
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: locust-report
          path: |
            report.html
            results_*.csv
```

### Docker実行

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY locustfile.py .
CMD ["locust", "-f", "locustfile.py"]
```

```bash
# ビルド
docker build -t my-locust-test .

# 実行
docker run -p 8089:8089 my-locust-test
```

## 料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Locust (Community)** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **Pythonベース**: 開発者にとって習得容易
2. **柔軟性**: 複雑なロジックもPythonで記述可能
3. **分散テスト**: 数百万ユーザーシミュレート
4. **Web UI**: リアルタイムグラフ・モニタリング
5. **軽量**: JMeterよりリソース消費少ない
6. **コードベース**: Git管理、レビュー容易
7. **無料**: 完全無料、MIT License
8. **拡張性**: カスタムクライアント作成可能
9. **CI/CD統合**: ヘッドレスモードで自動化
10. **モダン**: 継続的な開発・改善

## デメリット

### ❌ 制約・課題

1. **プロトコル制限**: HTTP/WebSocketのみ（JDBC、FTP等非対応）
2. **GUI不要論**: GUIテストシナリオ作成には不向き
3. **Pythonスキル必要**: コード記述必須
4. **レポート**: JMeterやGatlingほど詳細ではない
5. **プラグイン**: JMeterほどエコシステム豊富ではない
6. **JavaScript非対応**: ブラウザレンダリング不可
7. **学習曲線**: コードベースのため初心者には敷居高い
8. **メトリクス**: 詳細なパフォーマンス分析機能は限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **JMeter** | GUI、多様なプロトコル | Locustよりプロトコル対応広い |
| **Gatling** | Scala、DSL、詳細レポート | Locustよりレポート豊富 |
| **k6** | JavaScript、CLI重視 | Locustと類似、JavaScriptベース |
| **Artillery** | Node.js、YAML設定 | Locustよりシンプル |
| **wrk** | C言語、超軽量 | Locustより機能限定的 |

## 公式リンク

- **公式サイト**: [https://locust.io/](https://locust.io/)
- **ドキュメント**: [https://docs.locust.io/](https://docs.locust.io/)
- **GitHub**: [https://github.com/locustio/locust](https://github.com/locustio/locust)
- **Examples**: [https://github.com/locustio/locust/tree/master/examples](https://github.com/locustio/locust/tree/master/examples)

## 関連ドキュメント

- [テストツール一覧](../テストツール/)
- [JMeter](./JMeter.md)
- [Gatling](./Gatling.md)
- [k6](./k6.md)
- [パフォーマンステストベストプラクティス](../../best-practices/performance-testing.md)

---

**カテゴリ**: テストツール  
**対象工程**: テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
