# Grafana（監視・運用設計書）

## 概要

Grafanaは、オープンソースのメトリクス可視化・ダッシュボードツールで、基本設計（インフラ）フェーズでは監視ダッシュボード設計、アラート定義、メトリクス可視化設計に活用します。Prometheus、InfluxDB、Elasticsearch等の複数のデータソースに対応し、インフラ監視の設計に最適です。

### 基本設計（インフラ）フェーズでの活用

- **監視ダッシュボード設計**: CPU、メモリ、ネットワークトラフィック等の可視化設計
- **アラート定義**: 閾値設定、通知先設定、エスカレーション設計
- **メトリクス設計**: 収集するメトリクスの定義、保存期間設計
- **ログ可視化設計**: Lokiと統合したログ可視化
- **SLA/SLO監視設計**: 稼働率、レスポンスタイムの監視設計

### 料金プラン

- **Grafana OSS**: 完全無料（オンプレミス、セルフホスト）
- **Grafana Cloud Free**: 無料（3ユーザー、14日間保存）
- **Grafana Cloud Pro**: $45/月（10ユーザー、13ヶ月保存）
- **Grafana Cloud Advanced**: $200/月（無制限ユーザー、カスタム保存）
- **Grafana Enterprise**: カスタム価格（Enterprise機能、サポート）

### メリット・デメリット

**メリット**
- 完全無料（OSS版）
- 複数のデータソースに対応（Prometheus、InfluxDB、Elasticsearch等）
- 豊富なプラグイン（100種類以上のデータソース）
- ダッシュボードの自由度が高い
- アラート機能が充実
- コミュニティが活発

**デメリット**
- 初期構築が複雑（セットアップが必要）
- 統計分析機能は限定的
- Cloud版は高額
- 学習曲線がやや急

## 利用方法

### 1. Grafana OSS版のインストール

#### Dockerでのインストール（推奨）

```bash
# Grafanaコンテナの起動
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana-oss:latest

# ブラウザでアクセス: http://localhost:3000
# デフォルトログイン:
#   ユーザー名: admin
#   パスワード: admin
```

#### パッケージ管理でのインストール（Ubuntu）

```bash
# GPGキーの追加
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

# リポジトリの追加
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

# Grafanaのインストール
sudo apt update
sudo apt install grafana

# Grafanaの起動
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 2. データソースの設定

#### Prometheus データソースの追加

**前提: Prometheusが稼働中（例: http://localhost:9090）**

1. Grafana UIにログイン（http://localhost:3000）
2. 左サイドバー「Configuration」→「Data Sources」
3. 「Add data source」をクリック
4. 「Prometheus」を選択
5. 設定:
   - **Name**: Prometheus
   - **URL**: `http://prometheus:9090`（Dockerの場合はコンテナ名）
   - **Access**: Server（デフォルト）
6. 「Save & Test」をクリック

### 3. 監視ダッシュボードの設計

#### 例: サーバーインフラ監視ダッシュボード

**監視項目:**
- CPU使用率
- メモリ使用率
- ディスク使用率
- ネットワークトラフィック
- システムロード

**ダッシュボード作成手順:**

**1. 新規ダッシュボードの作成**

1. 左サイドバー「+」→「Dashboard」
2. 「Add new panel」をクリック

**2. CPU使用率パネルの作成**

1. パネルタイトル: "CPU使用率"
2. 「Query」タブで以下のPromQLを入力:

```promql
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

3. 「Visualization」でグラフタイプを選択: "Time series"
4. 「Panel options」で設定:
   - **Unit**: Percent (0-100)
   - **Min**: 0
   - **Max**: 100
5. 「Thresholds」で閾値を設定:
   - 警告: 70%（黄色）
   - 危険: 90%（赤色）

**3. メモリ使用率パネルの作成**

PromQLクエリ:

```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

**4. ディスク使用率パネルの作成**

PromQLクエリ:

```promql
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100
```

**5. ネットワークトラフィックパネルの作成**

PromQLクエリ（受信）:

```promql
irate(node_network_receive_bytes_total{device!="lo"}[5m])
```

PromQLクエリ（送信）:

```promql
irate(node_network_transmit_bytes_total{device!="lo"}[5m])
```

### 4. パネルレイアウトの設計

#### ダッシュボードレイアウト例

```
┌──────────────────────────────────────────────────────┐
│ サーバーインフラ監視ダッシュボード                        │
└──────────────────────────────────────────────────────┘
┌─────────────────┬─────────────────┬─────────────────┐
│ CPU使用率       │ メモリ使用率     │ ディスク使用率   │
│ [ゲージ 75%]    │ [ゲージ 60%]    │ [ゲージ 45%]    │
└─────────────────┴─────────────────┴─────────────────┘
┌──────────────────────────────────────────────────────┐
│ CPU使用率推移（時系列グラフ）                           │
│ [折れ線グラフ]                                         │
└──────────────────────────────────────────────────────┘
┌────────────────────────────┬─────────────────────────┐
│ ネットワークトラフィック      │ システムロード           │
│ [エリアグラフ]              │ [折れ線グラフ]           │
└────────────────────────────┴─────────────────────────┘
```

**レイアウト設定:**

1. パネルをドラッグ＆ドロップで配置
2. サイズを調整（グリッド単位）
3. 「Dashboard settings」→「Variables」で変数を設定（例: `$instance`）

### 5. アラート設定の設計

#### CPU使用率アラートの設定

**アラート条件:**
- CPU使用率が90%を5分間超えた場合にアラート

**設定手順:**

1. CPU使用率パネルを選択
2. 「Alert」タブをクリック
3. 「Create Alert」をクリック
4. アラートルールを設定:

```
Rule name: High CPU Usage
Evaluate: Every 1m for 5m

Conditions:
WHEN avg() OF query(A, 5m, now) IS ABOVE 90
```

5. 通知設定:
   - **Notification channel**: Email、Slack、PagerDuty等を選択
   - **Message**: "CPU使用率が90%を超えています: {{ $values }}"

### 6. 通知チャネルの設定

#### Slack通知の設定

1. 「Alerting」→「Notification channels」
2. 「Add channel」をクリック
3. 設定:
   - **Name**: Slack Alerts
   - **Type**: Slack
   - **Webhook URL**: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`
   - **Channel**: `#ops-alerts`
4. 「Test」をクリックして通知確認

#### Email通知の設定

1. Grafana設定ファイル（`/etc/grafana/grafana.ini`）を編集:

```ini
[smtp]
enabled = true
host = smtp.gmail.com:587
user = your-email@gmail.com
password = your-app-password
from_address = grafana@example.com
from_name = Grafana
```

2. Grafanaを再起動:

```bash
sudo systemctl restart grafana-server
```

3. 通知チャネルでEmail typeを選択

### 7. テンプレート変数の活用

#### インスタンス選択変数の設定

**用途:** ダッシュボード上部のドロップダウンでサーバーを切り替え

1. 「Dashboard settings」→「Variables」
2. 「Add variable」をクリック
3. 設定:
   - **Name**: `instance`
   - **Type**: Query
   - **Data source**: Prometheus
   - **Query**: `label_values(node_cpu_seconds_total, instance)`
   - **Multi-value**: 有効（複数選択可能）

4. パネルのクエリで変数を使用:

```promql
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle", instance=~"$instance"}[5m])) * 100)
```

### 8. 公式ダッシュボードのインポート

#### Node Exporterダッシュボードのインポート

1. 「+」→「Import」
2. Grafana.com Dashboard ID: `1860`（Node Exporter Full）を入力
3. 「Load」をクリック
4. データソースを選択
5. 「Import」をクリック

**人気のダッシュボードID:**
- **1860**: Node Exporter Full
- **3662**: Prometheus 2.0 Stats
- **7362**: Kubernetes Cluster Monitoring
- **11074**: MySQL Overview

### 9. ログ可視化（Loki統合）

#### Lokiデータソースの追加

1. 「Configuration」→「Data Sources」→「Add data source」
2. 「Loki」を選択
3. URL: `http://loki:3100`
4. 「Save & Test」

#### ログパネルの作成

1. 新規パネルを作成
2. クエリ:

```logql
{job="varlogs"} |= "error"
```

3. Visualization: Logs
4. オプション:
   - **Show labels**: 有効
   - **Enable LogQL**: 有効

### 10. SLA/SLO監視ダッシュボード

#### SLO（Service Level Objective）の可視化

**例: Webサービスの可用性SLO 99.9%**

**Success Rateの計算:**

```promql
sum(rate(http_requests_total{status=~"2.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100
```

**SLOパネルの作成:**

1. パネルタイトル: "SLO: 可用性"
2. Visualization: Stat（ゲージ）
3. Threshold:
   - 99.9% 以上: 緑
   - 99.0% - 99.9%: 黄
   - 99.0% 未満: 赤

### 11. ダッシュボード設計のベストプラクティス

#### レイアウト設計

- **重要なメトリクスを上部に配置**: CPU、メモリ、エラー率等
- **詳細グラフを下部に配置**: 時系列グラフ、ログ
- **色分け**: 緑（正常）、黄（警告）、赤（危険）

#### パネル設計

- **単位の統一**: %, Bytes, requests/sec等
- **凡例の表示**: メトリクスの説明を表示
- **閾値の視覚化**: 警告線、危険線を表示

#### 変数の活用

- インスタンス選択、時間範囲選択、環境選択（dev/staging/prod）

### 12. 監視設計書への統合

#### 監視設計書の構成

**1. 監視対象一覧**

| 監視対象 | メトリクス | 閾値（警告） | 閾値（危険） | 通知先 | 備考 |
|---------|----------|------------|------------|--------|------|
| Webサーバー | CPU使用率 | 70% | 90% | Slack #ops | 5分間持続 |
| Webサーバー | メモリ使用率 | 80% | 95% | Slack #ops | 即時通知 |
| DBサーバー | ディスク使用率 | 80% | 90% | Slack #ops, Email | 即時通知 |
| API | エラー率 | 1% | 5% | PagerDuty | 即時通知 |

**2. ダッシュボード一覧**

| ダッシュボード名 | 用途 | 監視対象 | 更新間隔 |
|---------------|------|---------|---------|
| インフラ概要 | 全体監視 | 全サーバー | 15秒 |
| Webサーバー詳細 | Web層監視 | Webサーバー | 10秒 |
| DBサーバー詳細 | DB層監視 | DBサーバー | 10秒 |
| SLA/SLO監視 | サービスレベル監視 | API、サービス | 1分 |

**3. アラートルール一覧**

| アラート名 | 条件 | 評価間隔 | 通知先 | エスカレーション |
|-----------|------|---------|--------|---------------|
| High CPU | CPU > 90% for 5m | 1分 | Slack | 30分後にPagerDuty |
| High Memory | Memory > 95% | 1分 | Slack | 即時 |
| API Error Rate | Error rate > 5% | 1分 | PagerDuty | 即時 |

**4. Grafanaダッシュボード画像**

設計したダッシュボードをPNG/PDFでエクスポートして添付

### 13. エクスポート機能

#### ダッシュボードのエクスポート

**JSON形式:**

1. ダッシュボードを開く
2. 「Dashboard settings」→「JSON Model」
3. JSONをコピーまたはダウンロード

**PNG/PDF形式:**

1. ダッシュボードを開く
2. 「Share」→「Export」
3. 「Snapshot」を選択してPNG/PDF生成

### 14. バージョン管理

#### ダッシュボードJSON のGit管理

```bash
# ダッシュボードJSONをエクスポート
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:3000/api/dashboards/uid/YOUR_DASHBOARD_UID \
  > dashboard.json

# Git管理
git add dashboard.json
git commit -m "Add infrastructure monitoring dashboard"
git push
```

## 公式ドキュメント

- **公式サイト**: [Grafana](https://grafana.com/)
- **ドキュメント**: [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- **ダッシュボード**: [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- **アラートガイド**: [Alerting Guide](https://grafana.com/docs/grafana/latest/alerting/)
- **プラグイン**: [Grafana Plugins](https://grafana.com/grafana/plugins/)

## 学習リソース

- **チュートリアル**: [Getting Started with Grafana](https://grafana.com/docs/grafana/latest/getting-started/)
- **YouTube**: [Grafana Official Channel](https://www.youtube.com/c/Grafana)
- **Grafana Play**: [Demo Site](https://play.grafana.org/)（デモサイトで試せる）

## 関連リンク

- [Prometheus](https://prometheus.io/)（メトリクス収集ツール）
- [Loki](https://grafana.com/oss/loki/)（ログ集約ツール）
- [Datadog](https://www.datadoghq.com/)（商用監視ツール）
- [New Relic](https://newrelic.com/)（APM・監視ツール）
