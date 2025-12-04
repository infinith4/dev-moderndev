# Grafana

## 概要

Grafanaは、オープンソースのメトリクス可視化・ダッシュボードプラットフォームです。複数データソース（Prometheus、Elasticsearch、InfluxDB、MySQL等）、リアルタイムダッシュボード、アラート、プラグインエコシステムにより、監視データの統合可視化を実現します。豊富なグラフ種別、変数、アノテーションで、DevOps、SRE、ビジネス分析で広く採用されています。

## 主な機能

### 1. ダッシュボード
- **パネル**: グラフ、テーブル、ゲージ等
- **変数**: 動的フィルタ
- **テンプレート**: ダッシュボード再利用
- **アノテーション**: イベントマーカー

### 2. データソース
- **Prometheus**: メトリクス
- **Elasticsearch**: ログ
- **InfluxDB**: 時系列DB
- **MySQL/PostgreSQL**: RDBMS
- **Loki**: ログ集約

### 3. アラート
- **アラートルール**: しきい値
- **通知チャネル**: Slack、Email、PagerDuty
- **サイレンス**: アラート抑制

### 4. 可視化
- **Time Series**: 時系列グラフ
- **Bar Gauge**: バーゲージ
- **Stat**: 単一値
- **Table**: テーブル
- **Heatmap**: ヒートマップ

## 利用方法

### インストール（Docker）

```bash
docker run -d --name grafana \
  -p 3000:3000 \
  grafana/grafana-oss:latest

# Web UI: http://localhost:3000
# デフォルト: admin/admin
```

### Prometheus連携

```bash
# Prometheusデータソース追加
1. Configuration > Data Sources > Add data source
2. Prometheus選択
3. URL: http://prometheus:9090
4. Save & Test
```

### ダッシュボード作成

```json
{
  "dashboard": {
    "title": "System Metrics",
    "panels": [
      {
        "type": "graph",
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
          }
        ]
      }
    ]
  }
}
```

### Docker Compose（Prometheus + Grafana）

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana-oss
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

### API（ダッシュボード作成）

```bash
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d '{
    "dashboard": {
      "title": "My Dashboard",
      "panels": []
    }
  }'
```

### 変数（ダッシュボード）

```promql
# 変数定義（インスタンス一覧）
label_values(node_cpu_seconds_total, instance)

# パネルクエリで変数使用
node_cpu_seconds_total{instance="$instance"}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Grafana OSS** | 🟢 完全無料 | オープンソース、AGPLv3 License |
| **Grafana Cloud** | 🟢 無料枠あり | マネージドGrafana、無料枠: 10k series |
| **Grafana Enterprise** | 💰 要問い合わせ | エンタープライズ機能 |

## メリット

1. **完全無料**: オープンソース
2. **多データソース**: 30+データソース
3. **豊富な可視化**: 多様なグラフ
4. **プラグイン**: 拡張可能
5. **コミュニティ**: 大規模コミュニティ

## デメリット

1. **設定複雑**: 初期設定複雑
2. **パフォーマンス**: 大量パネルで遅延
3. **アラート**: アラート機能限定的
4. **学習曲線**: PromQL等の学習必要

## 公式リンク

- **公式サイト**: [https://grafana.com/](https://grafana.com/)
- **ドキュメント**: [https://grafana.com/docs/grafana/latest/](https://grafana.com/docs/grafana/latest/)

## 関連ドキュメント

- [可視化ツール一覧](../可視化ツール/)
- [Prometheus](../監視ツール/Prometheus.md)
- [Elasticsearch](../検索ツール/Elasticsearch.md)

---

**カテゴリ**: 可視化ツール
**対象工程**: メトリクス可視化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
