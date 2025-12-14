# AWS Cost Explorer

## 概要

**AWS Cost Explorer**は、AWSのコストと使用状況を可視化・分析するためのフルマネージドサービスです。過去のコストデータの分析、将来のコスト予測、コスト最適化の推奨事項により、AWS支出の管理と最適化を支援します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | コスト管理・分析サービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 一部無料（基本機能無料、API利用有料） |
| **公式サイト** | https://aws.amazon.com/aws-cost-management/aws-cost-explorer/ |
| **ドキュメント** | https://docs.aws.amazon.com/cost-management/ |

## 主な特徴

### 1. コスト可視化
- **グラフィカルダッシュボード**: 棒グラフ、折れ線グラフ
- **期間指定**: 日次、月次、年次
- **グループ化**: サービス、リージョン、タグ別
- **フィルタリング**: リソース・タグによる詳細分析

### 2. コスト予測
- **12ヶ月先まで予測**: 機械学習ベース
- **信頼区間表示**: 予測の不確実性可視化
- **異常検知**: 通常パターンからの逸脱検出

### 3. コスト最適化推奨
- **リザーブドインスタンス推奨**: RIカバレッジ最適化
- **Savings Plans推奨**: コミットメント最適化
- **ライトサイジング**: 過剰リソース検出

### 4. レポート・アラート
- **カスタムレポート**: 保存・スケジュール配信
- **予算アラート**: AWS Budgets連携
- **APIアクセス**: プログラマティックアクセス

## 使い方

### 基本的な分析

#### コストダッシュボード

```text
# AWS Cost Explorer Console
https://console.aws.amazon.com/cost-management/home

# 1. 基本ダッシュボード
   - 月次コスト推移
   - サービス別コスト内訳
   - 前月比・前年比

# 2. 期間選択
   - 過去6ヶ月
   - 過去12ヶ月
   - カスタム期間

# 3. グループ化
   - サービス別
   - リージョン別
   - タグ別（例: Environment:Production）
   - アカウント別（Organizations）

# 4. フィルター
   - 特定サービス（例: EC2、S3、RDS）
   - 特定リージョン（例: ap-northeast-1）
   - 特定タグ（例: CostCenter=Marketing）
```

### AWS CLI でのコスト取得

```bash
# 過去3ヶ月のコスト取得（サービス別）
aws ce get-cost-and-usage \
  --time-period Start=2024-10-01,End=2025-01-01 \
  --granularity MONTHLY \
  --metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE

# 特定サービスのコスト（日次）
aws ce get-cost-and-usage \
  --time-period Start=2024-12-01,End=2024-12-31 \
  --granularity DAILY \
  --metrics "BlendedCost" \
  --filter '{
    "Dimensions": {
      "Key": "SERVICE",
      "Values": ["Amazon Elastic Compute Cloud - Compute"]
    }
  }'

# タグ別コスト
aws ce get-cost-and-usage \
  --time-period Start=2024-12-01,End=2025-01-01 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=TAG,Key=Environment

# JSONファイルに保存
aws ce get-cost-and-usage \
  --time-period Start=2024-12-01,End=2025-01-01 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --output json > cost-report.json
```

### Python でコスト分析

```python
# cost_analysis.py
import boto3
import pandas as pd
from datetime import datetime, timedelta

ce = boto3.client('ce')

# 過去6ヶ月のコスト取得
end_date = datetime.now().date()
start_date = end_date - timedelta(days=180)

response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=['BlendedCost', 'UnblendedCost'],
    GroupBy=[
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        }
    ]
)

# データフレーム変換
data = []
for result in response['ResultsByTime']:
    period = result['TimePeriod']['Start']
    for group in result['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['BlendedCost']['Amount'])
        data.append({
            'Period': period,
            'Service': service,
            'Cost': cost
        })

df = pd.DataFrame(data)
df_pivot = df.pivot(index='Service', columns='Period', values='Cost')

print(df_pivot)

# トップ10サービス
top_services = df.groupby('Service')['Cost'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Services by Cost:")
print(top_services)

# CSVエクスポート
df.to_csv('aws_cost_analysis.csv', index=False)
```

### コスト予測

```bash
# 次の3ヶ月のコスト予測
aws ce get-cost-forecast \
  --time-period Start=2025-01-01,End=2025-04-01 \
  --metric BLENDED_COST \
  --granularity MONTHLY

# 特定サービスのコスト予測
aws ce get-cost-forecast \
  --time-period Start=2025-01-01,End=2025-04-01 \
  --metric BLENDED_COST \
  --granularity MONTHLY \
  --filter '{
    "Dimensions": {
      "Key": "SERVICE",
      "Values": ["Amazon Elastic Compute Cloud - Compute"]
    }
  }'
```

### リザーブドインスタンス推奨

```bash
# RIカバレッジレポート
aws ce get-reservation-coverage \
  --time-period Start=2024-12-01,End=2025-01-01 \
  --granularity MONTHLY

# RI購入推奨
aws ce get-reservation-purchase-recommendation \
  --service "Amazon Elastic Compute Cloud - Compute" \
  --lookback-period-in-days THIRTY_DAYS \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT

# Savings Plans推奨
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --lookback-period-in-days THIRTY_DAYS \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT
```

### カスタムレポート作成

```python
# custom_report.py
import boto3
import json
from datetime import datetime, timedelta

ce = boto3.client('ce')

def create_monthly_cost_report():
    """月次コストレポート（サービス・タグ別）"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    # サービス別コスト
    service_response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    # タグ別コスト（Environment）
    tag_response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[{'Type': 'TAG', 'Key': 'Environment'}]
    )

    report = {
        'period': f"{start_date} to {end_date}",
        'service_costs': [],
        'environment_costs': []
    }

    # サービス別集計
    for result in service_response['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            if cost > 0:
                report['service_costs'].append({
                    'service': service,
                    'cost': round(cost, 2)
                })

    # 環境別集計
    for result in tag_response['ResultsByTime']:
        for group in result['Groups']:
            env = group['Keys'][0]
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            if cost > 0:
                report['environment_costs'].append({
                    'environment': env,
                    'cost': round(cost, 2)
                })

    # ソート（コスト降順）
    report['service_costs'].sort(key=lambda x: x['cost'], reverse=True)
    report['environment_costs'].sort(key=lambda x: x['cost'], reverse=True)

    return report

# レポート生成
report = create_monthly_cost_report()
print(json.dumps(report, indent=2))

# S3に保存
s3 = boto3.client('s3')
s3.put_object(
    Bucket='my-cost-reports',
    Key=f"cost-report-{datetime.now().strftime('%Y-%m-%d')}.json",
    Body=json.dumps(report, indent=2)
)
```

### AWS Budgets連携

```yaml
# CloudFormation で予算アラート設定
Resources:
  MonthlyBudget:
    Type: AWS::Budgets::Budget
    Properties:
      Budget:
        BudgetName: Monthly-AWS-Budget
        BudgetLimit:
          Amount: 1000
          Unit: USD
        TimeUnit: MONTHLY
        BudgetType: COST
        CostFilters:
          # 本番環境のみ
          TagKeyValue:
            - "user:Environment$Production"
      NotificationsWithSubscribers:
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 80
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: EMAIL
              Address: team@example.com
        - Notification:
            NotificationType: FORECASTED
            ComparisonOperator: GREATER_THAN
            Threshold: 100
            ThresholdType: PERCENTAGE
          Subscribers:
            - SubscriptionType: EMAIL
              Address: team@example.com
```

### ダッシュボード自動化

```python
# dashboard_automation.py
import boto3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generate_cost_dashboard():
    ce = boto3.client('ce')

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=90)

    # コスト取得
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['BlendedCost']
    )

    dates = []
    costs = []

    for result in response['ResultsByTime']:
        dates.append(result['TimePeriod']['Start'])
        costs.append(float(result['Total']['BlendedCost']['Amount']))

    # グラフ作成
    plt.figure(figsize=(12, 6))
    plt.plot(dates, costs, marker='o')
    plt.title('AWS Daily Cost Trend (Last 90 Days)')
    plt.xlabel('Date')
    plt.ylabel('Cost (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('cost_dashboard.png')

    # S3にアップロード
    s3 = boto3.client('s3')
    s3.upload_file(
        'cost_dashboard.png',
        'my-cost-dashboards',
        f"dashboard-{datetime.now().strftime('%Y-%m-%d')}.png"
    )

    print("Dashboard generated and uploaded to S3")

# 毎日実行（Lambda + EventBridge）
generate_cost_dashboard()
```

### EventBridge で定期レポート

```yaml
# CloudFormation
Resources:
  CostReportFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: DailyCostReport
      Runtime: python3.11
      Handler: index.lambda_handler
      Code:
        ZipFile: |
          import boto3
          import json
          from datetime import datetime, timedelta

          def lambda_handler(event, context):
              ce = boto3.client('ce')
              sns = boto3.client('sns')

              # 昨日のコスト取得
              yesterday = (datetime.now() - timedelta(days=1)).date()
              response = ce.get_cost_and_usage(
                  TimePeriod={
                      'Start': yesterday.strftime('%Y-%m-%d'),
                      'End': datetime.now().strftime('%Y-%m-%d')
                  },
                  Granularity='DAILY',
                  Metrics=['BlendedCost']
              )

              cost = response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']

              # SNS通知
              sns.publish(
                  TopicArn=os.environ['SNS_TOPIC_ARN'],
                  Subject=f"Daily AWS Cost Report - {yesterday}",
                  Message=f"Yesterday's AWS cost: ${float(cost):.2f}"
              )

              return {'statusCode': 200}

      Environment:
        Variables:
          SNS_TOPIC_ARN: !Ref CostReportTopic

  DailySchedule:
    Type: AWS::Events::Rule
    Properties:
      ScheduleExpression: "cron(0 9 * * ? *)"  # 毎日9:00 JST
      State: ENABLED
      Targets:
        - Arn: !GetAtt CostReportFunction.Arn
          Id: CostReportTarget
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **企画** | コスト見積もり | 初期コスト予測 |
| **実装** | コスト追跡 | 開発環境コスト監視 |
| **テスト** | コスト最適化 | リソース使用状況分析 |
| **運用** | コスト管理 | 継続的コスト監視・最適化 |

## メリット

- **無料基本機能**: コンソールでの基本分析は無料
- **包括的可視化**: 全AWSサービスのコスト統合
- **コスト予測**: 機械学習ベースの将来予測
- **最適化推奨**: RI・Savings Plans推奨
- **タグベース分析**: プロジェクト・環境別コスト把握
- **API利用可能**: プログラマティックアクセス
- **Budgets連携**: 予算アラート統合

## デメリット

- **API利用有料**: $0.01/リクエスト
- **24時間遅延**: データ反映に最大24時間
- **データ保持期間**: 最大14ヶ月（それ以前はエクスポート必要）
- **タグ要件**: コストアロケーションタグの事前設定が必要
- **予測精度**: 使用パターン変化時に精度低下
- **組織設定**: マルチアカウント分析にはOrganizations必要

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Cost Explorer** | AWS | 一部無料 | AWS標準コスト分析 |
| **CloudHealth（VMware）** | マルチクラウド | 有料 | 高度な分析・最適化 |
| **Cloudability** | マルチクラウド | 有料 | エンタープライズ向け |
| **AWS Cost Anomaly Detection** | AWS | 無料 | 異常検知特化 |

## ベストプラクティス

### 1. コストアロケーションタグ戦略

```bash
# 推奨タグ
Environment: Production, Staging, Development
CostCenter: Engineering, Marketing, Sales
Project: ProjectA, ProjectB
Owner: team@example.com

# タグの有効化（AWS Billing Console）
# Billing → Cost allocation tags → Activate tags
```

### 2. 定期レポート自動化

```python
# 週次コストレポート（Slack通知）
import boto3
import json
import urllib.request
from datetime import datetime, timedelta

def weekly_cost_report():
    ce = boto3.client('ce')

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        GroupBy=[{'Type': 'TAG', 'Key': 'Environment'}]
    )

    # 環境別集計
    env_costs = {}
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            env = group['Keys'][0]
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            env_costs[env] = env_costs.get(env, 0) + cost

    # Slack通知
    message = {
        'text': f'*Weekly AWS Cost Report*\n{start_date} ~ {end_date}',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '\n'.join([f'• {env}: ${cost:.2f}' for env, cost in env_costs.items()])
                }
            }
        ]
    }

    req = urllib.request.Request(
        os.environ['SLACK_WEBHOOK_URL'],
        data=json.dumps(message).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
```

### 3. コスト異常アラート

```python
# 日次コスト異常検知
def detect_cost_anomaly():
    ce = boto3.client('ce')

    # 過去30日の平均コスト
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['BlendedCost']
    )

    costs = [float(r['Total']['BlendedCost']['Amount']) for r in response['ResultsByTime']]
    avg_cost = sum(costs) / len(costs)
    std_dev = (sum((x - avg_cost) ** 2 for x in costs) / len(costs)) ** 0.5

    # 昨日のコスト
    yesterday_cost = costs[-1]

    # 異常判定（平均 + 2σ を超える）
    if yesterday_cost > avg_cost + 2 * std_dev:
        send_alert(f"Cost anomaly detected: ${yesterday_cost:.2f} (avg: ${avg_cost:.2f})")
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/aws-cost-management/aws-cost-explorer/
- **ドキュメント**: https://docs.aws.amazon.com/cost-management/
- **料金**: https://aws.amazon.com/aws-cost-management/pricing/
- **API リファレンス**: https://docs.aws.amazon.com/cost-management/latest/APIReference/
- **ベストプラクティス**: https://aws.amazon.com/aws-cost-management/cost-optimization/

## まとめ

AWS Cost Explorerは、AWSのコストと使用状況を可視化・分析するフルマネージドサービスです。過去のコストデータ分析、将来のコスト予測、コスト最適化推奨により、AWS支出の管理と最適化を支援します。基本機能は無料で、タグベース分析やAPI利用により、プログラマティックなコスト管理も可能です。AWS利用において必須のコスト管理ツールです。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS Cost Explorer 2024+
