# Alertmanager

## 概要

Alertmanagerは、Prometheusエコシステムのアラート通知管理コンポーネントです。Prometheusサーバーから送信されるアラートを受信し、重複排除（Deduplication）、グルーピング、抑制（Inhibition）、サイレンス（Silence）の処理を行った上で、Slack、Email、PagerDuty、OpsGenie等の通知先にルーティングします。ラベルベースのルーティングツリーにより、チーム・重要度・サービス別の柔軟な通知制御が可能です。

## 主な機能

### 1. アラートルーティング

- **ルーティングツリー**: ラベルマッチングによる階層的な通知先振り分け
- **グルーピング**: 同一ラベルのアラートをまとめて1通知に集約
- **group_wait**: グループ内の初回アラート待機時間
- **group_interval**: 同一グループへの追加アラート送信間隔
- **repeat_interval**: 未解決アラートの再通知間隔

### 2. 重複排除・抑制

- **Deduplication**: 同一アラートの重複通知を自動排除
- **Inhibition**: 特定のアラートが発火中は関連アラートを抑制
- **Silence**: Web UIまたはAPIから一時的にアラートをミュート

### 3. 通知先（Receiver）

- **Slack**: チャンネル・メンション指定、カスタムテンプレート
- **Email**: SMTP経由のメール通知
- **PagerDuty**: インシデント自動作成
- **OpsGenie**: アラート作成・エスカレーション
- **Webhook**: 任意のHTTPエンドポイントへの通知
- **Microsoft Teams**: Teams チャンネルへの通知

### 4. 高可用性

- **クラスタリング**: Gossipプロトコルによる複数インスタンスの同期
- **Deduplication across instances**: クラスタ間での重複排除
- **自動フェイルオーバー**: インスタンス障害時の自動引き継ぎ

## 利用方法

### インストール

```bash
# バイナリダウンロード
wget https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz
tar xvfz alertmanager-0.27.0.linux-amd64.tar.gz

# Docker
docker run --name alertmanager -d -p 9093:9093 \
  -v /path/to/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager

# Helm（Kubernetes）
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install alertmanager prometheus-community/alertmanager
```

### 設定ファイル（alertmanager.yml）

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX'

route:
  receiver: 'default-slack'
  group_by: ['alertname', 'namespace']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    # Critical アラートは PagerDuty へ
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      group_wait: 10s
      repeat_interval: 1h

    # Warning アラートは Slack #alerts-warning へ
    - match:
        severity: warning
      receiver: 'slack-warning'
      group_wait: 1m

    # チーム別ルーティング
    - match_re:
        team: 'platform|infra'
      receiver: 'slack-platform'

receivers:
  - name: 'default-slack'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<PagerDuty-Service-Key>'
        severity: critical

  - name: 'slack-warning'
    slack_configs:
      - channel: '#alerts-warning'
        send_resolved: true

  - name: 'slack-platform'
    slack_configs:
      - channel: '#platform-alerts'

inhibit_rules:
  # Critical が発火中は同一 alertname の Warning を抑制
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'namespace']
```

### Prometheus側のアラートルール設定

```yaml
# prometheus/alert-rules.yml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.instance }}"
```

### amtool（CLI）

```bash
# アラート一覧
amtool alert --alertmanager.url=http://localhost:9093

# サイレンス作成（2時間メンテナンス）
amtool silence add \
  --alertmanager.url=http://localhost:9093 \
  --author="admin" \
  --comment="Scheduled maintenance" \
  --duration=2h \
  alertname="HighLatency" namespace="production"

# サイレンス一覧
amtool silence query --alertmanager.url=http://localhost:9093

# 設定ファイルの検証
amtool check-config alertmanager.yml
```

### クラスタリング（高可用性）

```bash
# インスタンス1
alertmanager --config.file=alertmanager.yml \
  --cluster.listen-address=0.0.0.0:9094

# インスタンス2（インスタンス1に接続）
alertmanager --config.file=alertmanager.yml \
  --cluster.listen-address=0.0.0.0:9094 \
  --cluster.peer=instance1:9094
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Alertmanager** | 無料 | オープンソース、Apache License 2.0 |
| **Grafana Cloud** | 有料 | マネージドAlertmanager、Grafana OnCall連携 |

## メリット

1. **Prometheus標準**: Prometheusエコシステムの公式アラート管理コンポーネント
2. **グルーピング**: 大量のアラートを集約して通知疲れを軽減
3. **ラベルベースルーティング**: チーム・サービス・重要度別の柔軟な振り分け
4. **Inhibition**: 上位障害発生時に下位アラートを自動抑制
5. **高可用性**: Gossipプロトコルによるクラスタリング対応
6. **Web UI**: サイレンスの管理やアラート状態の確認がブラウザで可能
7. **テンプレート**: Go templateによる通知メッセージのカスタマイズ

## デメリット

1. **設定の複雑さ**: ルーティングツリーとインヒビションルールの設計が複雑
2. **Prometheus依存**: Prometheus以外の監視ツールとの連携は限定的
3. **通知カスタマイズ**: Go templateの記法は直感的でない場合がある
4. **エスカレーション**: 段階的なエスカレーション機能が組み込みでない
5. **永続化なし**: アラート履歴の長期保存機能がない（外部ストレージが必要）

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Grafana OnCall** | インシデント管理 | Alertmanagerより高度なオンコール管理・エスカレーション |
| **PagerDuty** | インシデント管理SaaS | Alertmanagerの通知先として使用、より高機能 |
| **OpsGenie** | アラート管理SaaS | Atlassian統合、スケジュール管理が充実 |
| **Karma** | Alertmanager UI | Alertmanagerのマルチクラスタ対応ダッシュボード |

## 公式リンク

- **公式ドキュメント**: [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)
- **GitHub**: [https://github.com/prometheus/alertmanager](https://github.com/prometheus/alertmanager)
- **設定リファレンス**: [https://prometheus.io/docs/alerting/latest/configuration/](https://prometheus.io/docs/alerting/latest/configuration/)
- **通知テンプレート**: [https://prometheus.io/docs/alerting/latest/notification_examples/](https://prometheus.io/docs/alerting/latest/notification_examples/)

## 関連ドキュメント

- [Loki](./Loki.md)
- [OpenTelemetry](./OpenTelemetry.md)

---

**カテゴリ**: 監視ロギング
**対象工程**: 運用・監視
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
