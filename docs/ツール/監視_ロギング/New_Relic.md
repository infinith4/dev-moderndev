# New Relic

## 概要

New Relicは、フルスタックオブザーバビリティプラットフォームです。APM（Application Performance Monitoring）、インフラ監視、ログ管理、分散トレーシング、リアルユーザーモニタリング（RUM）、合成監視を統合し、アプリケーションとインフラの包括的な可視化を提供します。SaaS型で提供され、数分でセットアップ可能、AIによる異常検知とインシデント分析により、迅速な問題解決を実現します。

## 主な機能

### 1. APM（Application Performance Monitoring）
- **トランザクション追跡**: リクエスト単位のパフォーマンス
- **エラー分析**: スタックトレース、エラー率
- **外部サービス**: API、データベース呼び出し
- **分散トレーシング**: マイクロサービス間の追跡
- **言語サポート**: Java、Python、Node.js、Go、Ruby、.NET等

### 2. インフラ監視
- **ホスト監視**: CPU、メモリ、ディスク、ネットワーク
- **コンテナ監視**: Docker、Kubernetes
- **クラウド統合**: AWS、Azure、GCP
- **ネットワーク監視**: トラフィック、レイテンシ

### 3. ログ管理
- **ログ集約**: 全サービスのログ統合
- **ログ検索**: 高速フルテキスト検索
- **ログコンテキスト**: APMトレースとログ連携
- **アラート**: ログパターンベースアラート

### 4. ブラウザ監視（RUM）
- **ページロード時間**: フロントエンドパフォーマンス
- **JavaScriptエラー**: クライアント側エラー追跡
- **AJAXリクエスト**: API呼び出し監視
- **セッションリプレイ**: ユーザー操作記録

### 5. 合成監視（Synthetic Monitoring）
- **死活監視**: エンドポイント可用性
- **シナリオテスト**: Selenium風のブラウザテスト
- **APIテスト**: REST API監視
- **グローバル監視**: 世界各地からのアクセス

### 6. アラート・通知
- **カスタムアラート**: メトリクスベースアラート
- **通知チャネル**: Email、Slack、PagerDuty、Webhook
- **AIベース**: 異常検知、ノイズ削減
- **インシデント管理**: アラート集約

## 利用方法

### エージェントインストール

#### Node.js APM

```bash
# npmインストール
npm install newrelic --save

# 設定ファイル生成
cp node_modules/newrelic/newrelic.js ./newrelic.js

# newrelic.js編集
exports.config = {
  app_name: ['My Application'],
  license_key: 'YOUR_LICENSE_KEY',
  logging: {
    level: 'info'
  }
}

# アプリケーション起動時にロード
# app.js
require('newrelic');
const express = require('express');
// ...
```

#### Java APM

```bash
# エージェントダウンロード
wget https://download.newrelic.com/newrelic/java-agent/newrelic-agent/current/newrelic-java.zip
unzip newrelic-java.zip

# newrelic.yml編集
license_key: YOUR_LICENSE_KEY
app_name: My Java Application

# JVM起動時にエージェント指定
java -javaagent:/path/to/newrelic.jar -jar myapp.jar
```

#### Python APM

```bash
# pipインストール
pip install newrelic

# 設定ファイル生成
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini

# アプリケーション起動
newrelic-admin run-program python app.py
```

### インフラエージェント

```bash
# Linux（Ubuntu/Debian）
curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash && \
  sudo NEW_RELIC_API_KEY=YOUR_API_KEY \
  NEW_RELIC_ACCOUNT_ID=YOUR_ACCOUNT_ID \
  /usr/local/bin/newrelic install

# Docker
docker run \
  -d \
  --name newrelic-infra \
  --network=host \
  --cap-add=SYS_PTRACE \
  --privileged \
  -v "/:/host:ro" \
  -v "/var/run/docker.sock:/var/run/docker.sock" \
  -e NRIA_LICENSE_KEY=YOUR_LICENSE_KEY \
  newrelic/infrastructure:latest
```

### Kubernetes統合

```yaml
# values.yaml (Helm)
global:
  licenseKey: YOUR_LICENSE_KEY
  cluster: my-k8s-cluster

# Helmインストール
helm repo add newrelic https://helm-charts.newrelic.com
helm install newrelic-bundle newrelic/nri-bundle \
  --namespace newrelic --create-namespace \
  -f values.yaml
```

### カスタムメトリクス

```javascript
// Node.js
const newrelic = require('newrelic');

// カスタムメトリクス記録
newrelic.recordMetric('Custom/MyMetric', 42);

// カスタムイベント
newrelic.recordCustomEvent('MyEvent', {
  user_id: 'user123',
  action: 'purchase',
  amount: 99.99
});
```

### NRQL（New Relic Query Language）

```sql
-- APMトランザクション平均応答時間
SELECT average(duration) 
FROM Transaction 
WHERE appName = 'My Application' 
SINCE 1 hour ago

-- エラー率
SELECT percentage(count(*), WHERE error IS true) 
FROM Transaction 
SINCE 1 day ago

-- トップ10遅いトランザクション
SELECT average(duration), count(*) 
FROM Transaction 
WHERE appName = 'My Application' 
FACET name 
SINCE 1 hour ago 
LIMIT 10

-- インフラCPU使用率
SELECT average(cpuPercent) 
FROM SystemSample 
WHERE hostname LIKE 'prod-%' 
FACET hostname 
SINCE 1 hour ago 
TIMESERIES
```

### アラート設定

```
1. Alerts & AI → Alert conditions → Create a condition
2. Select a product: APM
3. Define thresholds:
   - Metric: Response time (web)
   - Threshold: > 2 seconds for at least 5 minutes
4. Notification channels: Slack, Email, PagerDuty
5. Save condition
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** |  無料 | 100GB/月データ、1ユーザー、基本機能 |
| **Standard** |  $0.30/GB | 従量課金、無制限ユーザー |
| **Pro** |  $0.50/GB | 高度な機能、15ヶ月データ保持 |
| **Enterprise** |  $0.75/GB | セキュリティ、サポート、SLA |

## メリット

###  主な利点

1. **オールインワン**: APM、インフラ、ログ、RUM統合
2. **無料プラン**: 100GB/月まで無料
3. **多言語対応**: Java、Python、Node.js等
4. **分散トレーシング**: マイクロサービス可視化
5. **AI機能**: 異常検知、根本原因分析
6. **SaaS**: セットアップ数分、メンテナンス不要
7. **スケーラブル**: 大規模環境対応
8. **豊富な統合**: AWS、K8s、Slack等
9. **リアルタイム**: ライブダッシュボード
10. **コミュニティ**: 豊富なドキュメント、サポート

## デメリット

###  制約・課題

1. **コスト**: 大規模データで高額
2. **データ保持**: Free版は8日間のみ
3. **ベンダーロックイン**: New Relic固有機能
4. **学習曲線**: NRQL習得必要
5. **オンプレミス不可**: SaaSのみ
6. **カスタマイズ**: ダッシュボードのカスタマイズに制約
7. **データ送信**: エージェント通信でオーバーヘッド
8. **複雑な料金**: データ量の見積もり困難

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Datadog** | オールインワン監視 | New Relicと類似、料金体系異なる |
| **Dynatrace** | AI駆動APM | New Relicより高機能だが高価 |
| **Splunk** | ログ管理、SIEM | New Relicよりログ分析強い |
| **Grafana + Prometheus** | オープンソース | New Relicより無料だが構築必要 |
| **AppDynamics** | エンタープライズAPM | New Relicより高機能だが高価 |

## 公式リンク

- **公式サイト**: [https://newrelic.com/](https://newrelic.com/)
- **ドキュメント**: [https://docs.newrelic.com/](https://docs.newrelic.com/)
- **サインアップ**: [https://newrelic.com/signup](https://newrelic.com/signup)
- **GitHub**: [https://github.com/newrelic](https://github.com/newrelic)
- **University**: [https://learn.newrelic.com/](https://learn.newrelic.com/)

## 関連ドキュメント

- [監視ツール一覧](../監視ツール/)
- [Datadog](./Datadog.md)
- [Splunk](./Splunk.md)
- [Prometheus](./Prometheus.md)
- [アプリケーション監視ベストプラクティス](../../best-practices/application-monitoring.md)

---

**カテゴリ**: 監視ツール  
**対象工程**: 運用、パフォーマンステスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0

