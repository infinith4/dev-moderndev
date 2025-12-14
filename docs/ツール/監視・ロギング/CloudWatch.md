# Amazon CloudWatch

## 概要

Amazon CloudWatchは、AWS公式の監視・ログ管理サービスです。AWSリソース（EC2、RDS、Lambda等）のメトリクス収集、ログ集約、アラート設定、ダッシュボード作成を統合的に提供します。リアルタイムでAWSインフラとアプリケーションを監視し、自動スケーリングやインシデント対応を自動化します。AWS環境の可観測性を実現する標準ツールです。

## 主な機能

### 1. メトリクス監視
- **基本メトリクス**: EC2 CPU、メモリ、ディスク
- **カスタムメトリクス**: アプリケーション独自メトリクス
- **統計**: 平均、合計、最小、最大、パーセンタイル
- **時系列データ**: 最大15ヶ月保持

### 2. ログ管理
- **CloudWatch Logs**: ログ集約
- **ログストリーム**: アプリケーションログ
- **Logs Insights**: SQLライクなクエリ
- **サブスクリプション**: Lambda、Kinesis連携

### 3. アラーム
- **メトリクスアラーム**: しきい値監視
- **複合アラーム**: 複数条件
- **アクション**: SNS、Auto Scaling、EC2、Systems Manager
- **異常検知**: 機械学習ベース

### 4. ダッシュボード
- **カスタムダッシュボード**: グラフ、数値
- **自動更新**: リアルタイム表示
- **共有**: URLで共有

### 5. Events / EventBridge
- **イベント駆動**: AWSリソース変更検知
- **スケジュール**: Cronジョブ
- **ターゲット**: Lambda、SNS、Step Functions

### 6. Container Insights
- **ECS/EKS監視**: コンテナメトリクス
- **Prometheus統合**: Prometheusメトリクス収集

## 利用方法

### 基本メトリクス表示

```bash
# AWS CLI
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --period 3600 \
  --statistics Average
```

### カスタムメトリクス送信

```python
# Python (boto3)
import boto3

cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'PageViews',
            'Value': 123,
            'Unit': 'Count',
            'Timestamp': datetime.utcnow()
        }
    ]
)
```

```javascript
// Node.js
const { CloudWatchClient, PutMetricDataCommand } = require('@aws-sdk/client-cloudwatch');

const client = new CloudWatchClient({ region: 'us-east-1' });

const command = new PutMetricDataCommand({
  Namespace: 'MyApp',
  MetricData: [
    {
      MetricName: 'PageViews',
      Value: 123,
      Unit: 'Count',
      Timestamp: new Date()
    }
  ]
});

await client.send(command);
```

### ログ送信

```python
# Python
import boto3
import time

logs = boto3.client('logs')

logs.put_log_events(
    logGroupName='/aws/lambda/my-function',
    logStreamName='2024/01/01/stream',
    logEvents=[
        {
            'message': 'User login successful',
            'timestamp': int(time.time() * 1000)
        }
    ]
)
```

### Logs Insights クエリ

```sql
-- エラーログ検索
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100

-- レスポンスタイム集計
fields @timestamp, duration
| stats avg(duration), max(duration), count() by bin(5m)
| sort @timestamp desc

-- 特定ユーザーのアクション
fields @timestamp, user_id, action
| filter user_id = "user123"
| sort @timestamp desc
```

### アラーム作成

```bash
# CPU使用率アラーム
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu-alarm \
  --alarm-description "Alert when CPU exceeds 80%" \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic
```

### Lambda統合

```python
# Lambda関数
import json
import boto3

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    # メトリクス送信
    cloudwatch.put_metric_data(
        Namespace='MyLambda',
        MetricData=[{
            'MetricName': 'Invocations',
            'Value': 1,
            'Unit': 'Count'
        }]
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
```

### Container Insights (ECS)

```json
# ECS Task Definition
{
  "family": "my-app",
  "containerDefinitions": [{
    "name": "app",
    "image": "myapp:latest",
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/my-app",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
```

## エディション・料金

| 項目 | 価格 | 特徴 |
|------|------|------|
| **メトリクス** | 💰 $0.30/メトリクス/月 | カスタムメトリクス（10万リクエストまで無料） |
| **ログ** | 💰 $0.50/GB | ログ取り込み |
| **ログ保存** | 💰 $0.03/GB | 月額保存料 |
| **アラーム** | 💰 $0.10/アラーム/月 | 標準メトリクス（10アラームまで無料） |
| **ダッシュボード** | 💰 $3/ダッシュボード/月 | 3ダッシュボードまで無料 |

## メリット

### ✅ 主な利点

1. **AWS統合**: AWSリソース標準監視
2. **自動収集**: EC2等の基本メトリクス自動
3. **無料枠**: 一定量まで無料
4. **リアルタイム**: 1分間隔メトリクス
5. **Logs Insights**: 強力なログクエリ
6. **EventBridge統合**: イベント駆動自動化
7. **IAM統合**: AWSセキュリティ統合
8. **Container Insights**: ECS/EKS対応
9. **異常検知**: 機械学習ベース
10. **マネージド**: 運用不要

## デメリット

### ❌ 制約・課題

1. **AWS限定**: AWS環境のみ
2. **コスト**: 大規模ログで高額
3. **クエリ性能**: Logs Insightsは大規模で遅延
4. **保持期間**: デフォルトは短い
5. **UI**: Datadog等より使いにくい
6. **マルチクラウド**: 他クラウド監視不可
7. **アラート遅延**: 1分以上かかる場合あり
8. **ダッシュボード**: カスタマイズ性に限界

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Datadog** | マルチクラウド、APM | CloudWatchより高機能だが高価 |
| **New Relic** | APM、オブザーバビリティ | CloudWatchより包括的 |
| **Grafana + Prometheus** | オープンソース | CloudWatchより柔軟 |
| **Splunk** | エンタープライズログ管理 | CloudWatchより強力だが高価 |
| **Azure Monitor** | Azure環境 | CloudWatchと類似（Azure版） |

## 公式リンク

- **公式サイト**: [https://aws.amazon.com/cloudwatch/](https://aws.amazon.com/cloudwatch/)
- **ドキュメント**: [https://docs.aws.amazon.com/cloudwatch/](https://docs.aws.amazon.com/cloudwatch/)
- **料金**: [https://aws.amazon.com/cloudwatch/pricing/](https://aws.amazon.com/cloudwatch/pricing/)
- **Logs Insights**: [https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)

## 関連ドキュメント

- [監視ツール一覧](../監視ツール/)
- [Azure Monitor](./Azure_Monitor.md)
- [Datadog](./Datadog.md)
- [Prometheus](./Prometheus.md)
- [AWS監視ベストプラクティス](../../best-practices/aws-monitoring.md)

---

**カテゴリ**: 監視ツール  
**対象工程**: 運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
