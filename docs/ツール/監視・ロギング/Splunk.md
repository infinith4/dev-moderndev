# Splunk

## 概要

Splunkは、マシンデータ（ログ、メトリクス、トレース）を収集・検索・分析・可視化する統合プラットフォームです。リアルタイムおよび履歴データの検索により、セキュリティ監視、運用監視、ビジネスインテリジェンス、コンプライアンス監査を実現します。Splunk Processing Language（SPL）による強力なクエリ機能と、ダッシュボード、アラート、レポートにより、ITインフラからアプリケーションまでの包括的な可視化を提供します。

## 主な機能

### 1. データ収集（Indexing）
- **Universal Forwarder**: 軽量エージェントでログ転送
- **Heavy Forwarder**: データフィルタリング・パース
- **Syslog**: 標準Syslogプロトコル
- **HTTP Event Collector (HEC)**: RESTful API経由でデータ送信
- **Database Connect**: RDBMS連携

### 2. 検索（Search）
- **SPL (Splunk Processing Language)**: 強力なクエリ言語
- **フィールド抽出**: 自動・手動フィールド抽出
- **正規表現**: パターンマッチング
- **統計関数**: stats、timechart、chart等
- **サブサーチ**: ネストされたクエリ

### 3. 可視化（Visualization）
- **ダッシュボード**: カスタマイズ可能なダッシュボード
- **チャート**: 折れ線、棒、円、ヒートマップ等
- **テーブル**: データテーブル表示
- **単一値**: KPI表示
- **地図**: 地理的データ可視化

### 4. アラート（Alerting）
- **リアルタイムアラート**: 条件一致時に即通知
- **スケジュールアラート**: 定期実行
- **通知**: Email、Slack、PagerDuty、Webhook
- **アクション**: スクリプト実行、チケット作成

### 5. レポート
- **スケジュールレポート**: 定期的にレポート生成
- **PDFエクスポート**: PDF形式で配信
- **CSVエクスポート**: データエクスポート

### 6. セキュリティ（Splunk Enterprise Security）
- **SIEM**: セキュリティ情報・イベント管理
- **脅威検知**: 異常検知、相関分析
- **インシデント管理**: セキュリティインシデント追跡
- **コンプライアンス**: 監査ログ管理

### 7. IT運用（Splunk IT Service Intelligence）
- **サービス監視**: ビジネスサービス可視化
- **異常検知**: 機械学習による異常検知
- **根本原因分析**: イベント相関分析

## 利用方法

### インストール（Splunk Enterprise）

```bash
# Linux (Ubuntu/Debian)
wget -O splunk.deb https://download.splunk.com/products/splunk/releases/.../splunk-x.x.x-linux-2.6-amd64.deb
sudo dpkg -i splunk.deb

# Splunk起動
sudo /opt/splunk/bin/splunk start --accept-license

# ブラウザで http://localhost:8000 にアクセス
# 管理者アカウント作成

# 自動起動設定
sudo /opt/splunk/bin/splunk enable boot-start
```

### Universal Forwarderセットアップ

```bash
# Universal Forwarderインストール
wget -O splunkforwarder.deb https://download.splunk.com/products/universalforwarder/releases/.../splunkforwarder-x.x.x-linux-2.6-amd64.deb
sudo dpkg -i splunkforwarder.deb

# Forwarder設定（Indexerへのデータ送信）
sudo /opt/splunkforwarder/bin/splunk add forward-server splunk-indexer:9997

# ログファイル監視設定
sudo /opt/splunkforwarder/bin/splunk add monitor /var/log/nginx/access.log -index main

# Forwarder起動
sudo /opt/splunkforwarder/bin/splunk start
```

### 基本的な検索（SPL）

```spl
# 全データ検索
index=main

# 特定キーワード検索
index=main error

# 時間範囲指定
index=main earliest=-1h

# フィールドによるフィルタ
index=main source="/var/log/nginx/access.log" status=500

# 統計（カウント）
index=main | stats count by status

# タイムチャート（時系列グラフ）
index=main | timechart count by status

# トップN
index=main | top limit=10 clientip

# テーブル表示
index=main | table _time, clientip, uri, status
```

### 高度な検索例

```spl
# エラーログの抽出・集計
index=main level=ERROR
| stats count by component
| sort -count

# レスポンスタイム分析
index=main source="/var/log/app.log"
| stats avg(response_time) as avg_time, max(response_time) as max_time by endpoint
| where avg_time > 1000

# 異常検知（標準偏差）
index=main
| timechart span=1h count
| eventstats avg(count) as avg, stdev(count) as stdev
| eval threshold=avg+3*stdev
| where count > threshold

# JOIN操作
index=main sourcetype=access_log
| join clientip [search index=main sourcetype=user_db | fields clientip, username]
| table _time, clientip, username, uri

# サブサーチ
index=main
[search index=main earliest=-1h status=500 | top limit=10 clientip | fields clientip]
| stats count by uri
```

### ダッシュボード作成

```xml
<!-- dashboard.xml -->
<dashboard>
  <label>Application Monitoring</label>
  <row>
    <panel>
      <title>Error Count (Last 24h)</title>
      <single>
        <search>
          <query>
            index=main level=ERROR earliest=-24h
            | stats count
          </query>
        </search>
      </single>
    </panel>
    
    <panel>
      <title>Requests by Status Code</title>
      <chart>
        <search>
          <query>
            index=main earliest=-1h
            | timechart count by status
          </query>
        </search>
        <option name="charting.chart">line</option>
      </chart>
    </panel>
  </row>
  
  <row>
    <panel>
      <title>Top 10 Slow Endpoints</title>
      <table>
        <search>
          <query>
            index=main earliest=-1h
            | stats avg(response_time) as avg_time by endpoint
            | sort -avg_time
            | head 10
          </query>
        </search>
      </table>
    </panel>
  </row>
</dashboard>
```

### アラート設定

```spl
# アラート検索（エラー率が5%超過）
index=main
| stats count(eval(status>=500)) as errors, count as total
| eval error_rate = (errors/total)*100
| where error_rate > 5

# アラート設定
1. 検索保存 → Save As → Alert
2. Title: "High Error Rate"
3. Trigger Condition: "Number of Results is greater than 0"
4. Throttle: "Suppress results for 5 minutes"
5. Actions:
   - Send email
   - Run script
   - Send to Slack
```

### HTTP Event Collector（HEC）でデータ送信

```bash
# HEC設定
1. Settings → Data Inputs → HTTP Event Collector → New Token
2. トークン生成（例: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX）

# curlでデータ送信
curl -k "https://splunk-server:8088/services/collector" \
  -H "Authorization: Splunk XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" \
  -d '{
    "event": {
      "message": "Application started",
      "severity": "INFO",
      "user": "admin"
    },
    "sourcetype": "app_log",
    "index": "main"
  }'
```

### Pythonアプリからのログ送信

```python
import requests
import json

SPLUNK_HEC_URL = "https://splunk-server:8088/services/collector"
SPLUNK_HEC_TOKEN = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

def send_to_splunk(event_data):
    headers = {
        "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "event": event_data,
        "sourcetype": "python_app",
        "index": "main"
    }
    response = requests.post(SPLUNK_HEC_URL, headers=headers, data=json.dumps(payload), verify=False)
    return response.status_code

# 使用例
send_to_splunk({"message": "User logged in", "user_id": 123})
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Splunk Free** | 🟢 無料 | 500MB/日まで、機能制限あり |
| **Splunk Cloud** | 💰 従量課金 | マネージドクラウド、$0.15/GB/日程度 |
| **Splunk Enterprise** | 💰 ライセンス制 | オンプレミス、$1,800～/GB/日 |
| **Splunk Enterprise Security** | 💰 要問い合わせ | SIEM機能追加 |

## メリット

### ✅ 主な利点

1. **強力な検索**: SPLによる柔軟なクエリ
2. **スケーラビリティ**: PB級のデータ処理
3. **リアルタイム**: ストリーミング検索・アラート
4. **多様なデータソース**: ログ、メトリクス、ネットワークトラフィック等
5. **可視化**: 豊富なチャート・ダッシュボード
6. **機械学習**: 異常検知、予測分析
7. **セキュリティ**: SIEM、脅威ハンティング
8. **拡張性**: アプリ・アドオンで機能拡張
9. **コミュニティ**: Splunkbase、豊富な情報
10. **エンタープライズサポート**: 充実したサポート

## デメリット

### ❌ 制約・課題

1. **高コスト**: データ量に応じた高額なライセンス
2. **学習曲線**: SPL習得に時間がかかる
3. **リソース消費**: 大量のメモリ・ストレージ必要
4. **インデックス遅延**: リアルタイム性に限界
5. **設定複雑**: 大規模環境では設定が煩雑
6. **ライセンス制限**: 無料版は500MB/日まで
7. **ベンダーロックイン**: Splunk固有のSPL
8. **代替ツール台頭**: ELK Stackより高価

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **ELK Stack (Elasticsearch, Logstash, Kibana)** | オープンソース、無料 | Splunkより安価だが機能少ない |
| **Datadog** | SaaS監視、APM | Splunkよりモダン、使いやすい |
| **Sumo Logic** | クラウドネイティブログ管理 | Splunkと類似、SaaS |
| **Graylog** | オープンソースログ管理 | Splunkより無料だが機能限定的 |
| **New Relic** | APM、ログ管理 | Splunkよりアプリケーション監視強い |

## 公式リンク

- **公式サイト**: [https://www.splunk.com/](https://www.splunk.com/)
- **Splunk Free**: [https://www.splunk.com/en_us/download/splunk-enterprise.html](https://www.splunk.com/en_us/download/splunk-enterprise.html)
- **ドキュメント**: [https://docs.splunk.com/](https://docs.splunk.com/)
- **Splunkbase (Apps)**: [https://splunkbase.splunk.com/](https://splunkbase.splunk.com/)
- **Splunk Education**: [https://www.splunk.com/en_us/training.html](https://www.splunk.com/en_us/training.html)

## 関連ドキュメント

- [監視ツール一覧](../監視ツール/)
- [Datadog](./Datadog.md)
- [ELK Stack](./ELK_Stack.md)
- [Prometheus](./Prometheus.md)
- [ログ管理ベストプラクティス](../../best-practices/log-management.md)

---

**カテゴリ**: 監視ツール  
**対象工程**: 運用、セキュリティ  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
