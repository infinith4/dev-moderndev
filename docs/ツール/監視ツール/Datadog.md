# Datadog

## 概要

Datadogは、クラウドスケールアプリケーション向けの統合監視・分析プラットフォームです。インフラストラクチャ、アプリケーション、ログ、セキュリティを一元的に監視し、リアルタイムでシステムの健全性を可視化します。

**主な特徴:**
- インフラストラクチャ監視（サーバー、コンテナ、クラウドサービス）
- アプリケーションパフォーマンス監視（APM）
- ログ管理と分析
- リアルユーザー監視（RUM）
- ネットワークパフォーマンス監視（NPM）
- セキュリティ監視
- 500以上の統合（AWS、Azure、GCP、Kubernetes等）
- カスタムダッシュボードとアラート

## 料金プラン

| プラン | 月額料金 | 主な機能 |
|--------|----------|----------|
| **Free** | 無料 | 5ホストまで、1日データ保持、基本メトリクス |
| **Pro** | $15/ホスト/月 | 無制限ホスト、15ヶ月データ保持、高度なアラート |
| **Enterprise** | $23/ホスト/月 | Pro機能 + SAML認証、監査ログ、SLA保証 |
| **APM Pro** | $31/ホスト/月 | Pro + APM（15日間トレース保持） |
| **APM Enterprise** | $40/ホスト/月 | Enterprise + APM機能 |
| **Log Management** | $0.10/GB取り込み | ログ収集、検索、分析（別途課金） |
| **RUM** | $0.60/1,000セッション | リアルユーザー監視（別途課金） |

※ 年間契約で割引あり

## メリット・デメリット

### メリット

1. **統合監視プラットフォーム**: インフラ、APM、ログ、セキュリティを一元管理
2. **豊富な統合**: 500以上のサービス・ツールとの連携
3. **強力な可視化**: カスタマイズ可能なダッシュボード
4. **リアルタイム監視**: 秒単位でのメトリクス収集
5. **高度なアラート**: 異常検知、予測アラート、複合条件
6. **スケーラビリティ**: 大規模システムに対応
7. **APM機能**: 分散トレーシング、パフォーマンス分析
8. **充実したAPI**: 自動化、カスタマイズが容易

### デメリット

1. **高額な料金**: 大規模環境では月額コストが高額
2. **複雑な料金体系**: ホスト数、ログ量、セッション数等で課金
3. **学習曲線**: 多機能ゆえに習得に時間がかかる
4. **データ保持期限**: プランによっては短期間のみ保存
5. **ログコスト**: ログ量が多いと費用が急増
6. **ベンダーロックイン**: Datadog固有の設定や機能に依存

## 利用できる開発工程

| 工程 | 活用度 | 主な用途 |
|------|--------|----------|
| 企画プロセス | ⭐⭐ | 既存システムのパフォーマンス分析 |
| 要件定義 | ⭐⭐⭐ | 非機能要件（性能、可用性）の定義 |
| アーキテクチャ設計 | ⭐⭐⭐⭐ | 監視設計、アラート設計 |
| 詳細設計 | ⭐⭐⭐ | メトリクス設計、ログ設計 |
| 開発 | ⭐⭐⭐⭐ | パフォーマンステスト、デバッグ |
| テスト | ⭐⭐⭐⭐⭐ | 負荷テスト、性能テスト監視 |
| リリース | ⭐⭐⭐⭐⭐ | デプロイ監視、カナリアリリース |
| 運用・保守 | ⭐⭐⭐⭐⭐ | 24/7監視、インシデント対応、キャパシティプランニング |

## 基本的な利用方法

### 1. アカウント作成とエージェントのインストール

```bash
# Datadog アカウント作成
# https://www.datadoghq.com/ からサインアップ

# Linux (Ubuntu/Debian) にDatadog Agentをインストール
DD_API_KEY=your_api_key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"

# Windows (PowerShell管理者権限)
$env:DD_API_KEY="your_api_key"; (Invoke-WebRequest -Uri https://s3.amazonaws.com/ddagent-windows-stable/ddagent-cli-latest.msi -OutFile ddagent-cli-latest.msi); Start-Process msiexec.exe -ArgumentList '/qn /i ddagent-cli-latest.msi'

# macOS
DD_API_KEY=your_api_key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"

# Docker
docker run -d --name datadog-agent \
  -e DD_API_KEY=your_api_key \
  -e DD_SITE="datadoghq.com" \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  gcr.io/datadoghq/agent:latest

# Kubernetes (Helm)
helm repo add datadog https://helm.datadoghq.com
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=your_api_key \
  --set datadog.site=datadoghq.com
```

### 2. エージェント設定

```yaml
# /etc/datadog-agent/datadog.yaml

api_key: your_api_key
site: datadoghq.com

# ホスト名（オプション）
hostname: web-server-01

# タグ設定
tags:
  - env:production
  - service:web
  - team:backend
  - region:ap-northeast-1

# ログ収集を有効化
logs_enabled: true

# APM（Application Performance Monitoring）を有効化
apm_config:
  enabled: true

# プロセス監視を有効化
process_config:
  enabled: true
```

### 3. カスタムメトリクスの送信

```python
# Python example
from datadog import initialize, statsd

options = {
    'api_key': 'your_api_key',
    'app_key': 'your_app_key'
}
initialize(**options)

# カウンターメトリクス
statsd.increment('web.page_views', tags=['page:home'])

# ゲージメトリクス
statsd.gauge('database.connections', 42, tags=['db:postgres'])

# ヒストグラム
statsd.histogram('request.response_time', 0.234, tags=['endpoint:/api/users'])

# タイミング
with statsd.timed('database.query.duration', tags=['query:select_users']):
    # データベースクエリ実行
    pass
```

```java
// Java example
import com.timgroup.statsd.StatsDClient;
import com.timgroup.statsd.NonBlockingStatsDClient;

StatsDClient statsd = new NonBlockingStatsDClient(
    "my.app",
    "localhost",
    8125,
    new String[]{"env:prod", "version:1.2.3"}
);

// カウンター
statsd.incrementCounter("api.requests");

// ゲージ
statsd.recordGaugeValue("queue.size", 123);

// ヒストグラム
statsd.recordHistogramValue("response.time", 234);
```

### 4. ダッシュボードの作成

```
Web UIでの作成:
1. Dashboards → New Dashboard
2. ウィジェットを追加:
   - Timeseries（時系列グラフ）
   - Query Value（単一値表示）
   - Heatmap（ヒートマップ）
   - Top List（ランキング）
3. メトリクスを選択（例: system.cpu.user）
4. グループ化、集約方法を設定
5. 保存

Terraformでの作成:
```

```hcl
resource "datadog_dashboard" "web_performance" {
  title       = "Web Application Performance"
  description = "Main performance dashboard"
  layout_type = "ordered"

  widget {
    timeseries_definition {
      title = "API Response Time"
      request {
        q = "avg:trace.flask.request.duration{env:prod,service:web-api}"
        display_type = "line"
      }
    }
  }

  widget {
    query_value_definition {
      title = "Error Rate"
      request {
        q = "sum:trace.flask.request.errors{env:prod}.as_count()"
        aggregator = "avg"
      }
    }
  }
}
```

## 工程別の活用方法

### アーキテクチャ設計での活用

**監視設計:**
```
監視項目の定義:
1. インフラメトリクス
   - CPU使用率: system.cpu.user, system.cpu.system
   - メモリ使用率: system.mem.used, system.mem.pct_usable
   - ディスクI/O: system.io.read_bytes, system.io.write_bytes
   - ネットワーク: system.net.bytes_rcvd, system.net.bytes_sent

2. アプリケーションメトリクス
   - リクエスト数: http.requests
   - レスポンスタイム: http.response_time
   - エラー率: http.errors
   - スループット: http.throughput

3. ビジネスメトリクス
   - ユーザー登録数: user.registrations
   - 注文数: orders.count
   - 売上: revenue.total
```

**アラート設計:**
```
重要度別アラート:
Critical:
- CPU使用率 > 90% が 5分間継続
- メモリ使用率 > 95%
- エラー率 > 5%
- レスポンスタイム > 2秒

Warning:
- CPU使用率 > 70% が 10分間継続
- メモリ使用率 > 80%
- エラー率 > 1%
```

### 開発での活用

**APM統合:**
```python
# Flask アプリケーション
from ddtrace import tracer, patch_all
patch_all()

from flask import Flask
app = Flask(__name__)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    # トレースが自動的に記録される
    with tracer.trace("database.query", service="postgres"):
        user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return user

# カスタムスパン
with tracer.trace("custom.operation", resource="process_data"):
    result = process_data()
```

```java
// Spring Boot アプリケーション
// application.properties
dd.service=my-spring-app
dd.env=production
dd.version=1.0.0
dd.logs.injection=true

// JVMオプション
-javaagent:/path/to/dd-java-agent.jar
-Ddd.service=my-spring-app
-Ddd.env=production
```

**ログ収集:**
```yaml
# /etc/datadog-agent/conf.d/custom_logs.yaml
logs:
  - type: file
    path: /var/log/myapp/application.log
    service: web-api
    source: java
    sourcecategory: sourcecode
    tags:
      - env:production

  - type: file
    path: /var/log/nginx/access.log
    service: nginx
    source: nginx
    sourcecategory: http_web_access
```

### テストでの活用

**負荷テスト監視:**
```python
# 負荷テスト実行中のモニタリング
import requests
from datadog import statsd

def load_test():
    for i in range(1000):
        start_time = time.time()
        try:
            response = requests.get('https://api.example.com/users')
            duration = time.time() - start_time

            statsd.histogram('load_test.response_time', duration)
            statsd.increment('load_test.requests')

            if response.status_code != 200:
                statsd.increment('load_test.errors')
        except Exception as e:
            statsd.increment('load_test.exceptions')
```

**パフォーマンステスト:**
```
監視項目:
1. レスポンスタイム（p50, p95, p99）
2. スループット（req/sec）
3. エラー率
4. データベース接続数
5. キュー長
6. CPU/メモリ使用率

ダッシュボード:
- 時系列グラフで推移を可視化
- ベースラインとの比較
- ボトルネック箇所の特定
```

### リリースでの活用

**デプロイメント追跡:**
```bash
# Datadogにデプロイイベントを送信
curl -X POST "https://api.datadoghq.com/api/v1/events" \
  -H "Content-Type: application/json" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -d '{
    "title": "Deployed version 2.5.0 to production",
    "text": "Release notes: https://github.com/myorg/myapp/releases/tag/v2.5.0",
    "tags": ["env:production", "version:2.5.0"],
    "alert_type": "info"
  }'
```

**カナリアリリース監視:**
```
モニタリング設定:
1. カナリアインスタンスにタグ付け（canary:true）
2. カナリアと本番のメトリクスを比較
   - エラー率
   - レスポンスタイム
   - リソース使用率
3. 異常検知で自動ロールバック

アラート:
- カナリアのエラー率 > 本番エラー率 × 2
- カナリアのレスポンスタイム > 本番 × 1.5
```

### 運用・保守での活用

**インシデント対応:**
```
ワークフロー:
1. アラート受信（PagerDuty、Slack等と連携）
2. Datadogダッシュボードで状況確認
3. APMトレースで問題箇所を特定
4. ログで詳細原因を調査
5. メトリクスで影響範囲を確認
6. 対応後、ポストモーテム用にイベントを記録
```

**異常検知:**
```
機械学習ベースの異常検知:
1. Monitors → New Monitor → Anomaly
2. メトリクスを選択（例: request.response_time）
3. 検知感度を設定（Basic/Agile/Robust）
4. アラート条件を設定
5. 通知先を設定（Slack、Email、PagerDuty等）

予測アラート:
1. Monitors → New Monitor → Forecast
2. メトリクスを選択（例: disk.used）
3. 予測期間を設定（1日、1週間等）
4. しきい値を設定
5. 「ディスク容量が3日以内に枯渇する」等を予測
```

**SLO（Service Level Objective）管理:**
```
SLO設定:
1. Service Level Objectives → New SLO
2. SLIメトリクスを選択:
   - 可用性: (成功リクエスト数 / 全リクエスト数) × 100
   - レイテンシ: p99レスポンスタイム < 500ms
3. 目標値を設定（例: 99.9%）
4. 期間を設定（30日、90日等）
5. エラーバジェットを監視
```

## 公式ドキュメント

- **公式サイト**: https://www.datadoghq.com/
- **ドキュメント**: https://docs.datadoghq.com/
- **API リファレンス**: https://docs.datadoghq.com/api/latest/
- **統合一覧**: https://docs.datadoghq.com/integrations/
- **ブログ**: https://www.datadoghq.com/blog/

## 学習リソース

### 公式リソース

1. **Datadog Learning Center**
   - URL: https://learn.datadoghq.com/
   - 無料のオンライントレーニング

2. **Datadog 認定プログラム**
   - Datadog Fundamentals Certification
   - 無料で受験可能

3. **Datadog YouTube チャンネル**
   - URL: https://www.youtube.com/c/Datadoghq
   - チュートリアル、ウェビナー

### 外部リソース

1. **Udemy コース**
   - 「Datadog Fundamentals」
   - 監視の基礎から応用まで

2. **GitHub Examples**
   - URL: https://github.com/DataDog/
   - サンプルコード、統合例

## 関連リンク

### 統合ツール

- **AWS統合**: EC2、RDS、Lambda、ECS等
- **Azure統合**: Virtual Machines、SQL Database等
- **GCP統合**: Compute Engine、Cloud SQL等
- **Kubernetes**: フルスタック監視
- **Docker**: コンテナ監視
- **Jenkins**: CI/CD監視
- **Slack**: アラート通知
- **PagerDuty**: インシデント管理

### 代替・補完ツール

**監視プラットフォーム:**
- **New Relic**: APM中心の監視
- **Dynatrace**: AI駆動の監視
- **AppDynamics**: アプリケーション監視
- **Prometheus + Grafana**: オープンソース監視
- **Splunk**: ログ分析中心
- **Elastic Stack (ELK)**: ログ・メトリクス監視

**特化型ツール:**
- **Sentry**: エラー追跡
- **Pingdom**: 外形監視
- **StatusPage**: ステータスページ

## ベストプラクティス

### タグ戦略

```yaml
# 推奨タグ構造
tags:
  # 環境
  - env:production
  - env:staging
  - env:development

  # サービス
  - service:web-api
  - service:worker

  # チーム
  - team:backend
  - team:frontend

  # バージョン
  - version:2.5.0

  # インフラ
  - region:ap-northeast-1
  - availability_zone:ap-northeast-1a
  - instance_type:t3.medium

  # ビジネス
  - cost_center:engineering
  - project:user-authentication
```

### メトリクス命名規則

```
パターン: <namespace>.<object>.<action>.<context>

例:
- web.request.duration
- database.query.count
- cache.hit.rate
- queue.message.size
- user.registration.count
```

### アラート疲労の防止

```
ベストプラクティス:
1. 重要なアラートのみ設定
2. 閾値は実績ベースで調整
3. ノイズの多いアラートは無効化
4. 複合条件を活用（AND/OR）
5. 通知スケジュールを設定（勤務時間外は重要なもののみ）
6. アラートの定期レビュー
```
