# Loki

## 概要

Lokiは、Grafana Labsが開発したログ集約システムです。Prometheusにインスパイアされた設計で、ログの全文インデックスを作成せずラベル（メタデータ）のみをインデックス化することで、低コスト・高効率なログ管理を実現します。Promtail、Grafana Alloy、Fluentd等のエージェントでログを収集し、GrafanaのExplore画面でLogQL（ログクエリ言語）を使ってログの検索・集約・可視化を行います。

## 主な機能

### 1. ログ収集・保存

- **ラベルインデックス**: ログ本文ではなくラベルのみインデックス化（低コスト）
- **チャンク保存**: ログデータを圧縮チャンクとしてオブジェクトストレージに保存
- **マルチテナント**: テナント分離によるマルチチーム運用
- **保持ポリシー**: ログの自動削除期間設定

### 2. LogQL（クエリ言語）

- **ログストリーム選択**: `{app="nginx", env="production"}`
- **フィルタ式**: `|= "error"`, `!= "timeout"`, `|~ "5[0-9]{2}"`
- **パーサー**: `| json`, `| logfmt`, `| pattern`, `| regexp`
- **メトリクスクエリ**: `rate()`, `count_over_time()`, `bytes_over_time()`
- **集約**: `sum`, `avg`, `max`, `min`, `topk`

### 3. ログ収集エージェント

- **Grafana Alloy**: Grafana公式のテレメトリコレクター（Promtail後継）
- **Promtail**: Loki専用の軽量ログ収集エージェント
- **Fluentd/Fluent Bit**: Loki出力プラグインで連携
- **Docker Driver**: Dockerログドライバーとして直接連携
- **Lambda Promtail**: AWS Lambda関数によるCloudWatch Logs転送

### 4. デプロイモード

- **Monolithic**: 全コンポーネントを1プロセスで実行（小規模向け）
- **Simple Scalable**: Read/Write/Backendの3コンポーネント分離
- **Microservices**: 各コンポーネントを個別にスケール（大規模向け）

## 利用方法

### インストール

```bash
# Docker Compose（Loki + Promtail + Grafana）
wget https://raw.githubusercontent.com/grafana/loki/main/production/docker-compose.yaml
docker compose up -d

# Helm（Kubernetes）
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install loki grafana/loki-stack \
  --namespace monitoring --create-namespace \
  --set grafana.enabled=true \
  --set promtail.enabled=true

# バイナリ
wget https://github.com/grafana/loki/releases/download/v3.0.0/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
./loki-linux-amd64 -config.file=loki-config.yaml
```

### Loki設定ファイル

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory
  replication_factor: 1
  path_prefix: /loki

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  filesystem:
    directory: /loki/chunks

limits_config:
  retention_period: 30d
  max_query_length: 721h

compactor:
  working_directory: /loki/compactor
  retention_enabled: true
```

### Promtail設定

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log

  - job_name: containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
```

### LogQLクエリ例

```logql
# 基本的なログ検索
{app="nginx"} |= "error"

# 正規表現フィルタ
{namespace="production"} |~ "status=(4|5)[0-9]{2}"

# JSONパース＋フィールドフィルタ
{app="api"} | json | status >= 500

# logfmtパース
{job="systemd"} | logfmt | level="error"

# メトリクスクエリ（5分間のエラーレート）
rate({app="nginx"} |= "error" [5m])

# ログ行数カウント（アプリ別Top 5）
topk(5, sum by(app) (count_over_time({namespace="production"}[1h])))

# ログボリューム集計
sum by(namespace) (bytes_over_time({job="containers"}[24h]))
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Loki（OSS）** | 無料 | AGPL v3、セルフホスト |
| **Grafana Cloud** | 無料枠あり / 有料 | マネージドLoki、50GB/月まで無料 |

## メリット

1. **低コスト**: 全文インデックス不要で、Elasticsearch比でストレージコストを大幅削減
2. **Prometheusライク**: ラベルベースのクエリモデルでPrometheus運用者に馴染みやすい
3. **Grafana統合**: Grafanaダッシュボードでメトリクスとログを同時に表示
4. **スケーラビリティ**: マイクロサービスモードで各コンポーネントを個別スケール
5. **オブジェクトストレージ**: S3/GCS/Azure Blob等の安価なストレージを活用
6. **LogQL**: PromQLに似た強力なクエリ言語でログの集約・分析が可能
7. **マルチテナント**: テナント分離によるセキュアなマルチチーム運用

## デメリット

1. **全文検索不可**: ラベルなしの自由文検索はElasticsearchに劣る
2. **ラベル設計重要**: 高カーディナリティなラベル設定はパフォーマンス劣化を招く
3. **学習コスト**: LogQLの習得やラベル設計のベストプラクティスの理解が必要
4. **Grafana依存**: ログの可視化にGrafanaが事実上必須
5. **リアルタイム性**: インジェスト遅延が発生する場合がある

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Elasticsearch** | 全文検索エンジン | Lokiより高機能だがコストが高い |
| **Fluentd + S3** | ログ転送 + ストレージ | Lokiよりシンプル、検索機能は弱い |
| **CloudWatch Logs** | AWSマネージド | AWS環境向け、Lokiよりベンダーロックイン |
| **Datadog Logs** | SaaS監視 | Lokiより高機能だが有料 |

## 公式リンク

- **公式サイト**: [https://grafana.com/oss/loki/](https://grafana.com/oss/loki/)
- **ドキュメント**: [https://grafana.com/docs/loki/latest/](https://grafana.com/docs/loki/latest/)
- **GitHub**: [https://github.com/grafana/loki](https://github.com/grafana/loki)
- **LogQLリファレンス**: [https://grafana.com/docs/loki/latest/query/](https://grafana.com/docs/loki/latest/query/)

## 関連ドキュメント

- [Alertmanager](./Alertmanager.md)
- [OpenTelemetry](./OpenTelemetry.md)

---

**カテゴリ**: 監視ロギング
**対象工程**: 運用・監視
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
