# Azure Monitor

## 概要

Azure Monitorは、Microsoft Azure公式の包括的な監視ソリューションです。Azureリソース（VM、App Service、AKS等）のメトリクス、ログ、トレースを統合的に収集・分析し、Application Insights（APM）、Log Analytics、アラート、ダッシュボードを提供します。Azure環境のフルスタックオブザーバビリティを実現し、クラウドネイティブアプリケーションの可用性とパフォーマンスを最適化します。

## 主な機能

### 1. メトリクス
- **プラットフォームメトリクス**: CPU、メモリ、ネットワーク
- **カスタムメトリクス**: アプリケーション独自メトリクス
- **メトリクスエクスプローラー**: グラフ化
- **時系列データ**: 93日間保持

### 2. ログ（Log Analytics）
- **Log Analytics Workspace**: ログ集約
- **KQL（Kusto Query Language）**: 強力なクエリ言語
- **データソース**: VM、コンテナ、アプリログ
- **保持期間**: 最大2年

### 3. Application Insights
- **APM**: アプリケーションパフォーマンス監視
- **分散トレーシング**: マイクロサービス追跡
- **依存関係マップ**: サービス間の関係
- **ライブメトリクス**: リアルタイム監視

### 4. アラート
- **メトリクスアラート**: しきい値監視
- **ログアラート**: KQLクエリベース
- **アクショングループ**: Email、SMS、Webhook、Logic Apps
- **スマート検出**: 機械学習ベース異常検知

### 5. ダッシュボード
- **Azure Dashboard**: カスタムダッシュボード
- **Workbooks**: Jupyterスタイルのレポート
- **共有**: ロールベースアクセス制御

### 6. コンテナ監視
- **Container Insights**: AKSKubernetes監視
- **Prometheusメトリクス**: Prometheus統合
- **ログ**: コンテナログ収集

## 利用方法

### メトリクス表示

```bash
# Azure CLI
az monitor metrics list \
  --resource /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{vm-name} \
  --metric-names "Percentage CPU" \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --interval PT1H
```

### カスタムメトリクス送信

```csharp
// .NET
using Microsoft.ApplicationInsights;
using Microsoft.ApplicationInsights.Extensibility;

var config = TelemetryConfiguration.CreateDefault();
config.InstrumentationKey = "YOUR_INSTRUMENTATION_KEY";
var client = new TelemetryClient(config);

client.TrackMetric("PageViews", 123);
client.TrackEvent("UserLogin", new Dictionary<string, string> {
    { "UserId", "user123" },
    { "Success", "true" }
});
```

```python
# Python
from applicationinsights import TelemetryClient

tc = TelemetryClient('YOUR_INSTRUMENTATION_KEY')
tc.track_metric('PageViews', 123)
tc.track_event('UserLogin', {'UserId': 'user123'})
tc.flush()
```

### KQL（Kusto Query Language）

```kql
-- エラーログ検索
AzureDiagnostics
| where Level == "Error"
| order by TimeGenerated desc
| take 100

-- CPU使用率集計
Perf
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize avg(CounterValue) by bin(TimeGenerated, 5m), Computer
| render timechart

-- Application Insights - 失敗したリクエスト
requests
| where success == false
| summarize count() by resultCode, bin(timestamp, 1h)
| order by timestamp desc
```

### アラート作成

```bash
# メトリクスアラート（CPU 80%超過）
az monitor metrics alert create \
  --name high-cpu-alert \
  --resource-group myResourceGroup \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{vm} \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/microsoft.insights/actionGroups/{action-group}
```

### Application Insights統合

```javascript
// Node.js
const appInsights = require('applicationinsights');
appInsights.setup('YOUR_INSTRUMENTATION_KEY')
    .setAutoCollectRequests(true)
    .setAutoCollectPerformance(true)
    .setAutoCollectExceptions(true)
    .setAutoCollectDependencies(true)
    .start();

const client = appInsights.defaultClient;

// カスタムイベント
client.trackEvent({ name: 'UserPurchase', properties: { amount: 99.99 } });

// カスタムメトリクス
client.trackMetric({ name: 'QueueLength', value: 42 });
```

### Log Analytics エージェント

```bash
# Linux VM
wget https://raw.githubusercontent.com/Microsoft/OMS-Agent-for-Linux/master/installer/scripts/onboard_agent.sh
sh onboard_agent.sh -w <WORKSPACE_ID> -s <WORKSPACE_KEY>

# Windows VM（PowerShell）
$WorkspaceId = "YOUR_WORKSPACE_ID"
$WorkspaceKey = "YOUR_WORKSPACE_KEY"
$mma = New-Object -ComObject 'AgentConfigManager.MgmtSvcCfg'
$mma.AddCloudWorkspace($WorkspaceId, $WorkspaceKey)
$mma.ReloadConfiguration()
```

### Container Insights (AKS)

```bash
# AKS クラスターで有効化
az aks enable-addons \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --addons monitoring \
  --workspace-resource-id /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{workspace}
```

## エディション・料金

| 項目 | 価格 | 特徴 |
|------|------|------|
| **Log Analytics** | 💰 $2.76/GB | データ取り込み（最初5GB/日は無料） |
| **Application Insights** | 💰 $2.88/GB | テレメトリデータ（最初5GB/月は無料） |
| **アラート** | 💰 $0.10/アラート/月 | メトリクスアラート |
| **メトリクス** | 🟢 無料 | プラットフォームメトリクス |

## メリット

### ✅ 主な利点

1. **Azure統合**: Azureリソース標準監視
2. **Application Insights**: 強力なAPM
3. **KQL**: 柔軟なクエリ言語
4. **マルチクラウド**: AWS、GCP、オンプレも監視可能
5. **無料枠**: 一定量まで無料
6. **分散トレーシング**: マイクロサービス対応
7. **Workbooks**: 高度なレポート
8. **コンテナ監視**: AKS完全統合
9. **機械学習**: スマート検出
10. **マネージド**: 運用不要

## デメリット

### ❌ 制約・課題

1. **コスト**: 大規模ログで高額
2. **学習曲線**: KQL習得必要
3. **UI複雑**: 機能多数で初心者には難しい
4. **Azure最適化**: 他クラウドは機能制限
5. **保持期間**: デフォルト90日
6. **クエリ性能**: 大規模データで遅延
7. **サンプリング**: Application Insightsでサンプリング発生
8. **リアルタイム**: 数分の遅延あり

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Datadog** | マルチクラウド、APM | Azure Monitorより統合UI |
| **New Relic** | APM、オブザーバビリティ | Azure Monitorより使いやすい |
| **CloudWatch** | AWS環境 | Azure Monitorと類似（AWS版） |
| **Grafana + Prometheus** | オープンソース | Azure Monitorより柔軟 |
| **Dynatrace** | エンタープライズAPM | Azure Monitorより高機能だが高価 |

## 公式リンク

- **公式サイト**: [https://azure.microsoft.com/services/monitor/](https://azure.microsoft.com/services/monitor/)
- **ドキュメント**: [https://docs.microsoft.com/azure/azure-monitor/](https://docs.microsoft.com/azure/azure-monitor/)
- **KQLリファレンス**: [https://docs.microsoft.com/azure/data-explorer/kusto/query/](https://docs.microsoft.com/azure/data-explorer/kusto/query/)
- **Application Insights**: [https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- **料金**: [https://azure.microsoft.com/pricing/details/monitor/](https://azure.microsoft.com/pricing/details/monitor/)

## 関連ドキュメント

- [監視ツール一覧](../監視ツール/)
- [CloudWatch](./CloudWatch.md)
- [Datadog](./Datadog.md)
- [Application Insights](./Application_Insights.md)
- [Azure監視ベストプラクティス](../../best-practices/azure-monitoring.md)

---

**カテゴリ**: 監視ツール  
**対象工程**: 運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
