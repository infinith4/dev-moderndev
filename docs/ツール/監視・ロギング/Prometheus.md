# Prometheus（監視・運用設計書）

## 概要

Prometheusは、オープンソースの時系列データベース・監視システムで、基本設計（インフラ）フェーズではメトリクス収集設計、監視基盤設計、アラートルール設計に活用します。Kubernetes環境での標準的な監視ツールであり、Pull型メトリクス収集、柔軟なクエリ言語（PromQL）、スケーラブルな設計が特徴です。

### 基本設計（インフラ）フェーズでの活用

- **メトリクス収集設計**: 収集するメトリクスの定義、Exporter選定
- **監視基盤設計**: Prometheus server構成、保存期間設計
- **アラートルール設計**: 閾値設定、アラート条件の定義
- **Service Discovery設計**: 動的な監視対象の自動検出設計
- **Federation設計**: 複数Prometheus serverの統合設計

### 料金プラン

- **Prometheus**: 完全無料（Apache License 2.0）

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- Kubernetesの標準監視ツール
- スケーラブル（大規模環境に対応）
- 柔軟なクエリ言語（PromQL）
- 豊富なExporter（100種類以上）
- Pull型で監視対象への負荷が少ない

**デメリット**
- 初期構築が複雑（セットアップが必要）
- ログ管理機能がない（Lokiとの連携が必要）
- 学習曲線がやや急
- クラスタリング機能が限定的（Federation、Thanos等の追加ツールが必要）

## 利用方法

### 1. Prometheusのインストール

#### Dockerでのインストール（推奨）

**1. Prometheus設定ファイルの作成**

`prometheus.yml`:

```yaml
global:
  scrape_interval: 15s  # メトリクス収集間隔
  evaluation_interval: 15s  # アラートルール評価間隔

# Alertmanager設定
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# アラートルールファイル
rule_files:
  - "alert_rules.yml"

# メトリクス収集対象（scrape configs）
scrape_configs:
  # Prometheus自身の監視
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter（サーバーメトリクス）
  - job_name: 'node'
    static_configs:
      - targets:
          - 'node-exporter:9100'
        labels:
          environment: 'production'
          role: 'web-server'
```

**2. Dockerコンテナの起動**

```bash
# Prometheusコンテナの起動
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v prometheus-data:/prometheus \
  --name prometheus \
  prom/prometheus:latest

# Web UIにアクセス: http://localhost:9090
```

#### Docker Composeでの起動（Prometheus + Node Exporter + Grafana）

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'  # 30日間保存

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"

  grafana:
    image: grafana/grafana-oss:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus-data:
  grafana-data:
```

起動:

```bash
docker-compose up -d
```

### 2. Exporterの選定と設定

#### Node Exporter（サーバーメトリクス）

**提供メトリクス:**
- CPU使用率
- メモリ使用率
- ディスク使用率
- ネットワークトラフィック
- ファイルシステム情報

**起動:**

```bash
docker run -d \
  -p 9100:9100 \
  --name node-exporter \
  --net="host" \
  prom/node-exporter:latest
```

**Prometheus設定に追加:**

```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['server1:9100', 'server2:9100', 'server3:9100']
        labels:
          environment: 'production'
```

#### Blackbox Exporter（エンドポイント監視）

**用途:** HTTPエンドポイント、DNS、TCP、ICMPの監視

**設定例（`blackbox.yml`）:**

```yaml
modules:
  http_2xx:
    prober: http
    http:
      method: GET
      valid_status_codes: [200]
      preferred_ip_protocol: "ip4"

  http_post_json:
    prober: http
    http:
      method: POST
      headers:
        Content-Type: application/json
      body: '{"key":"value"}'
```

**Prometheus設定:**

```yaml
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://example.com
          - https://api.example.com/health
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
```

#### 主要なExporter一覧

| Exporter | 用途 | メトリクス |
|----------|------|----------|
| Node Exporter | サーバー監視 | CPU、メモリ、ディスク、ネットワーク |
| MySQL Exporter | MySQL監視 | クエリ数、接続数、スロークエリ |
| PostgreSQL Exporter | PostgreSQL監視 | クエリ数、トランザクション数 |
| Redis Exporter | Redis監視 | コマンド数、メモリ使用量 |
| Nginx Exporter | Nginx監視 | リクエスト数、レスポンスタイム |
| Blackbox Exporter | エンドポイント監視 | HTTPステータス、応答時間 |
| Kubernetes Exporter | Kubernetes監視 | Pod、Node、コンテナメトリクス |

### 3. PromQLの基本

#### 基本的なクエリ

**即時ベクトル（現在の値）:**

```promql
# CPU使用率
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# メモリ使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# ディスク使用率
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100
```

**範囲ベクトル（時間範囲）:**

```promql
# 過去5分間のHTTPリクエスト数
http_requests_total[5m]

# 過去1時間のCPU使用率
node_cpu_seconds_total[1h]
```

#### 集約関数

```promql
# 平均CPU使用率（全インスタンス）
avg(node_cpu_seconds_total)

# 最大メモリ使用率
max(node_memory_MemTotal_bytes)

# 合計HTTPリクエスト数
sum(http_requests_total)

# インスタンスごとの平均
avg by(instance) (node_cpu_seconds_total)
```

#### レート計算

```promql
# 1秒あたりのHTTPリクエスト数
rate(http_requests_total[5m])

# 1秒あたりのネットワーク受信バイト数
irate(node_network_receive_bytes_total[5m])
```

### 4. アラートルールの設計

#### アラートルールファイル（`alert_rules.yml`）

```yaml
groups:
  - name: infrastructure_alerts
    interval: 30s
    rules:
      # CPU使用率アラート
      - alert: HighCPUUsage
        expr: |
          100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

      # メモリ使用率アラート
      - alert: HighMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 95
        for: 2m
        labels:
          severity: critical
          team: infrastructure
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value }}% on {{ $labels.instance }}"

      # ディスク使用率アラート
      - alert: HighDiskUsage
        expr: |
          (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100 > 85
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "High disk usage on {{ $labels.instance }}"
          description: "Disk usage is {{ $value }}% on {{ $labels.instance }}"

      # サービスダウンアラート
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
          team: sre
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 1 minute"

      # HTTPエラー率アラート
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100 > 5
        for: 2m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High HTTP error rate"
          description: "HTTP 5xx error rate is {{ $value }}%"
```

### 5. Alertmanager設定

#### Alertmanager設定ファイル（`alertmanager.yml`）

```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  routes:
    # Critical alertsはPagerDutyへ
    - match:
        severity: critical
      receiver: 'pagerduty'
      continue: true

    # Warning alertsはSlackへ
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}'

  - name: 'slack'
    slack_configs:
      - channel: '#ops-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}\n{{ .Annotations.description }}{{ end }}'
        send_resolved: true
```

### 6. Service Discoveryの設定

#### Kubernetesでの自動検出

```yaml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

#### EC2での自動検出（AWS）

```yaml
scrape_configs:
  - job_name: 'ec2-discovery'
    ec2_sd_configs:
      - region: ap-northeast-1
        access_key: YOUR_ACCESS_KEY
        secret_key: YOUR_SECRET_KEY
        port: 9100
    relabel_configs:
      - source_labels: [__meta_ec2_tag_Environment]
        target_label: environment
      - source_labels: [__meta_ec2_instance_id]
        target_label: instance_id
```

### 7. 保存期間設計

#### TSDB保存期間の設定

```bash
# 起動オプションで設定
prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --storage.tsdb.retention.time=30d \  # 30日間保存
  --storage.tsdb.retention.size=50GB    # 最大50GB
```

**保存期間の設計例:**

| メトリクスタイプ | 保存期間 | 理由 |
|---------------|---------|------|
| インフラメトリクス（CPU、メモリ） | 30日 | 直近1ヶ月のトレンド分析 |
| アプリケーションメトリクス | 14日 | 短期的なパフォーマンス分析 |
| ビジネスメトリクス | 90日 | 長期トレンド分析、レポート作成 |

### 8. Federation設計（複数Prometheus統合）

#### Federation設定

**シナリオ:** リージョンごとにPrometheusを配置し、中央Prometheusで統合

**中央Prometheusの設定:**

```yaml
scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job="prometheus"}'
        - '{__name__=~"job:.*"}'
    static_configs:
      - targets:
          - 'prometheus-tokyo:9090'
          - 'prometheus-osaka:9090'
          - 'prometheus-singapore:9090'
```

### 9. 監視設計書への統合

#### 監視設計書の構成

**1. メトリクス収集設計**

| 監視対象 | Exporter | メトリクス | 収集間隔 | 保存期間 |
|---------|---------|----------|---------|---------|
| Webサーバー | Node Exporter | CPU、メモリ、ディスク、ネットワーク | 15秒 | 30日 |
| MySQL | MySQL Exporter | クエリ数、接続数、スロークエリ | 30秒 | 30日 |
| APIエンドポイント | Blackbox Exporter | HTTPステータス、レスポンスタイム | 30秒 | 14日 |

**2. アラートルール一覧**

| アラート名 | 条件 | 評価期間 | Severity | 通知先 |
|-----------|------|---------|---------|--------|
| HighCPUUsage | CPU > 90% | 5分 | warning | Slack |
| HighMemoryUsage | Memory > 95% | 2分 | critical | PagerDuty |
| ServiceDown | up == 0 | 1分 | critical | PagerDuty |
| HighErrorRate | Error rate > 5% | 2分 | critical | Slack, PagerDuty |

**3. Prometheus構成図**

```
┌────────────────────────────────────────┐
│ 中央Prometheus                          │
│ (Federation Master)                    │
└────────────┬───────────────────────────┘
             ↓ (Federate)
    ┌────────┴──────────────┬────────────┐
    ↓                       ↓            ↓
┌─────────────┐      ┌─────────────┐  ┌─────────────┐
│ Prometheus  │      │ Prometheus  │  │ Prometheus  │
│ Tokyo       │      │ Osaka       │  │ Singapore   │
└────┬────────┘      └────┬────────┘  └────┬────────┘
     ↓                    ↓                ↓
┌─────────────┐      ┌─────────────┐  ┌─────────────┐
│ Node        │      │ Node        │  │ Node        │
│ Exporters   │      │ Exporters   │  │ Exporters   │
└─────────────┘      └─────────────┘  └─────────────┘
```

### 10. ベストプラクティス

#### メトリクス設計

- **命名規則**: `<metric_name>{label1="value1", label2="value2"}`
- **ラベル**: 環境（environment）、リージョン（region）、ロール（role）等を付与
- **カーディナリティ**: ラベルの組み合わせが多すぎないように注意

#### アラートルール設計

- **評価期間（`for`）**: 短すぎる瞬間的なスパイクを無視
- **Severity分類**: critical、warning、infoの3段階
- **通知先**: criticalはPagerDuty、warningはSlack

#### データ保存設計

- **保存期間**: 用途に応じて設定（直近分析は短期、トレンド分析は長期）
- **ストレージ容量**: メトリクス数、保存期間から算出
- **バックアップ**: TSDBのスナップショットを定期取得

## 公式ドキュメント

- **公式サイト**: [Prometheus](https://prometheus.io/)
- **ドキュメント**: [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- **PromQL**: [Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
- **Exporters**: [Exporter List](https://prometheus.io/docs/instrumenting/exporters/)
- **Best Practices**: [Best Practices](https://prometheus.io/docs/practices/)

## 学習リソース

- **入門ガイド**: [Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/)
- **YouTube**: [Prometheus Monitoring](https://www.youtube.com/results?search_query=prometheus+monitoring+tutorial)
- **PromQL Tutorial**: [PromQL for Humans](https://timber.io/blog/promql-for-humans/)

## 関連リンク

- [Grafana](https://grafana.com/)（可視化ツール）
- [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)（アラート通知）
- [Thanos](https://thanos.io/)（長期保存、高可用性）
- [Cortex](https://cortexmetrics.io/)（マルチテナント、スケーラブル）
