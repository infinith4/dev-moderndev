# AWS CodeDeploy

## 概要

**AWS CodeDeploy**は、Amazon EC2、AWS Lambda、ECS、オンプレミスサーバーへのアプリケーションデプロイを自動化するAWSのフルマネージドデプロイサービスです。Blue/Greenデプロイ、カナリアデプロイ、自動ロールバックに対応し、ダウンタイムを最小化しながら安全なデプロイを実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | フルマネージドデプロイサービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 一部無料（EC2/オンプレ無料、ECS/Lambda有料） |
| **公式サイト** | https://aws.amazon.com/codedeploy/ |
| **ドキュメント** | https://docs.aws.amazon.com/codedeploy/ |

## 主な特徴

### 1. 多様なデプロイターゲット
- **Amazon EC2**: Auto Scaling Group統合
- **AWS Lambda**: バージョン管理・エイリアス連携
- **Amazon ECS**: Fargate、EC2起動タイプ対応
- **オンプレミスサーバー**: CodeDeploy Agentインストールで対応

### 2. デプロイ戦略
- **In-place（インプレース）**: 既存インスタンスを更新
- **Blue/Green**: 新環境作成後に切り替え
- **Canary（カナリア）**: 段階的トラフィック移行
- **Linear（リニア）**: 一定間隔でトラフィック増加

### 3. 自動ロールバック
- デプロイ失敗時の自動ロールバック
- CloudWatchアラーム連携
- 手動ロールバック
- デプロイ履歴管理

### 4. CI/CD統合
- AWS CodePipeline統合
- GitHub Actions
- GitLab CI/CD
- Jenkins連携

## 使い方

### セットアップ

#### EC2 インスタンスへのエージェントインストール

```bash
# Amazon Linux 2 / Amazon Linux 2023
sudo yum update -y
sudo yum install ruby wget -y

# CodeDeploy エージェントインストール（ap-northeast-1）
cd /home/ec2-user
wget https://aws-codedeploy-ap-northeast-1.s3.ap-northeast-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto

# エージェント起動確認
sudo service codedeploy-agent status

# 自動起動設定
sudo systemctl enable codedeploy-agent
```

```bash
# Ubuntu
sudo apt update
sudo apt install ruby wget -y

cd /tmp
wget https://aws-codedeploy-ap-northeast-1.s3.ap-northeast-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto

sudo systemctl start codedeploy-agent
sudo systemctl enable codedeploy-agent
```

#### IAM ロール設定

```json
// EC2用IAMロール（InstanceProfile）
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-deployment-bucket/*",
        "arn:aws:s3:::my-deployment-bucket"
      ]
    }
  ]
}

// CodeDeploy サービスロール
// AWS管理ポリシー: AWSCodeDeployRole を使用
```

### アプリケーション構成

#### appspec.yml（EC2/オンプレミス）

```yaml
# appspec.yml
version: 0.0
os: linux
files:
  # S3からファイルをコピー
  - source: /
    destination: /var/www/html/myapp
file_exists_behavior: OVERWRITE

permissions:
  # ファイル権限設定
  - object: /var/www/html/myapp
    owner: ec2-user
    group: ec2-user
    mode: 755
    type:
      - directory
  - object: /var/www/html/myapp
    owner: ec2-user
    group: ec2-user
    mode: 644
    type:
      - file

hooks:
  # ライフサイクルイベント
  ApplicationStop:
    - location: scripts/stop_application.sh
      timeout: 300
      runas: root

  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root

  AfterInstall:
    - location: scripts/configure_application.sh
      timeout: 300
      runas: ec2-user

  ApplicationStart:
    - location: scripts/start_application.sh
      timeout: 300
      runas: root

  ValidateService:
    - location: scripts/validate_service.sh
      timeout: 300
      runas: ec2-user
```

```bash
# scripts/stop_application.sh
#!/bin/bash
echo "Stopping application..."
sudo systemctl stop myapp || true

# scripts/install_dependencies.sh
#!/bin/bash
echo "Installing dependencies..."
cd /var/www/html/myapp
npm install --production

# scripts/configure_application.sh
#!/bin/bash
echo "Configuring application..."
cd /var/www/html/myapp
cp .env.example .env
# 環境変数をSSM Parameter Storeから取得
export DB_HOST=$(aws ssm get-parameter --name /myapp/db/host --query 'Parameter.Value' --output text)
echo "DB_HOST=$DB_HOST" >> .env

# scripts/start_application.sh
#!/bin/bash
echo "Starting application..."
sudo systemctl start myapp
sudo systemctl enable myapp

# scripts/validate_service.sh
#!/bin/bash
echo "Validating service..."
# ヘルスチェック
curl -f http://localhost:3000/health || exit 1
echo "Service is healthy"
```

#### appspec.yml（Lambda）

```yaml
# appspec.yml
version: 0.0
Resources:
  - MyFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: "my-lambda-function"
        Alias: "live"
        CurrentVersion: "1"
        TargetVersion: "2"
Hooks:
  - BeforeAllowTraffic: "BeforeAllowTrafficHook"
  - AfterAllowTraffic: "AfterAllowTrafficHook"
```

```python
# BeforeAllowTrafficHook Lambda
import boto3
import json

def lambda_handler(event, context):
    # デプロイ前の検証
    codedeploy = boto3.client('codedeploy')
    deployment_id = event['DeploymentId']
    lifecycle_event_hook_execution_id = event['LifecycleEventHookExecutionId']

    try:
        # 検証ロジック
        print("Running pre-traffic validation...")

        # 成功通知
        codedeploy.put_lifecycle_event_hook_execution_status(
            deploymentId=deployment_id,
            lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
            status='Succeeded'
        )
    except Exception as e:
        # 失敗通知（デプロイ中止）
        codedeploy.put_lifecycle_event_hook_execution_status(
            deploymentId=deployment_id,
            lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
            status='Failed'
        )
        raise e
```

#### appspec.yaml（ECS）

```yaml
# appspec.yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "arn:aws:ecs:ap-northeast-1:123456789012:task-definition/my-task:2"
        LoadBalancerInfo:
          ContainerName: "my-container"
          ContainerPort: 80
Hooks:
  - BeforeInstall: "BeforeInstallHook"
  - AfterInstall: "AfterInstallHook"
  - AfterAllowTestTraffic: "TestTrafficHook"
  - BeforeAllowTraffic: "BeforeAllowTrafficHook"
  - AfterAllowTraffic: "AfterAllowTrafficHook"
```

### デプロイグループ作成

```bash
# CodeDeploy アプリケーション作成
aws deploy create-application \
  --application-name MyApp \
  --compute-platform Server  # Server, Lambda, ECS

# デプロイグループ作成（EC2）
aws deploy create-deployment-group \
  --application-name MyApp \
  --deployment-group-name Production \
  --service-role-arn arn:aws:iam::123456789012:role/CodeDeployServiceRole \
  --deployment-config-name CodeDeployDefault.AllAtOnce \
  --ec2-tag-filters Key=Environment,Value=Production,Type=KEY_AND_VALUE \
  --auto-scaling-groups my-asg

# Blue/Green デプロイグループ（EC2）
aws deploy create-deployment-group \
  --application-name MyApp \
  --deployment-group-name BlueGreen \
  --service-role-arn arn:aws:iam::123456789012:role/CodeDeployServiceRole \
  --deployment-config-name CodeDeployDefault.HalfAtATime \
  --ec2-tag-filters Key=Environment,Value=Production,Type=KEY_AND_VALUE \
  --blue-green-deployment-configuration \
    terminateBlueInstancesOnDeploymentSuccess={action=TERMINATE,terminationWaitTimeInMinutes=5},\
    deploymentReadyOption={actionOnTimeout=CONTINUE_DEPLOYMENT},\
    greenFleetProvisioningOption={action=COPY_AUTO_SCALING_GROUP}
```

### デプロイ実行

```bash
# アプリケーションをS3にアップロード
aws deploy push \
  --application-name MyApp \
  --s3-location s3://my-deployment-bucket/MyApp.zip \
  --source ./myapp

# デプロイ作成
aws deploy create-deployment \
  --application-name MyApp \
  --deployment-group-name Production \
  --s3-location bucket=my-deployment-bucket,key=MyApp.zip,bundleType=zip \
  --description "Deploy version 1.2.3"

# デプロイステータス確認
aws deploy get-deployment --deployment-id d-XXXXXXXXX

# デプロイ履歴確認
aws deploy list-deployments \
  --application-name MyApp \
  --deployment-group-name Production
```

### デプロイ設定

#### カスタムデプロイ設定

```bash
# カナリアデプロイ（10%を5分間、その後全体）
aws deploy create-deployment-config \
  --deployment-config-name Custom-Canary10Percent5Minutes \
  --compute-platform Lambda \
  --traffic-routing-config '{
    "type": "TimeBasedCanary",
    "timeBasedCanary": {
      "canaryPercentage": 10,
      "canaryInterval": 5
    }
  }'

# リニアデプロイ（10%ずつ1分間隔）
aws deploy create-deployment-config \
  --deployment-config-name Custom-Linear10PercentEvery1Minute \
  --compute-platform Lambda \
  --traffic-routing-config '{
    "type": "TimeBasedLinear",
    "timeBasedLinear": {
      "linearPercentage": 10,
      "linearInterval": 1
    }
  }'
```

### 自動ロールバック設定

```json
// Auto Rollback設定
{
  "autoRollbackConfiguration": {
    "enabled": true,
    "events": [
      "DEPLOYMENT_FAILURE",
      "DEPLOYMENT_STOP_ON_ALARM"
    ]
  },
  "alarmConfiguration": {
    "enabled": true,
    "alarms": [
      {
        "name": "MyApp-ErrorRate-Alarm"
      },
      {
        "name": "MyApp-Latency-Alarm"
      }
    ]
  }
}
```

### CI/CD パイプライン統合

#### AWS CodePipeline

```yaml
# cloudformation/pipeline.yaml
Resources:
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      RoleArn: !GetAtt PipelineRole.Arn
      Stages:
        # Source Stage
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: ThirdParty
                Provider: GitHub
                Version: 1
              Configuration:
                Owner: myorg
                Repo: myapp
                Branch: main
                OAuthToken: !Ref GitHubToken
              OutputArtifacts:
                - Name: SourceOutput

        # Build Stage
        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: 1
              InputArtifacts:
                - Name: SourceOutput
              OutputArtifacts:
                - Name: BuildOutput
              Configuration:
                ProjectName: !Ref CodeBuildProject

        # Deploy Stage
        - Name: Deploy
          Actions:
            - Name: DeployAction
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: CodeDeploy
                Version: 1
              InputArtifacts:
                - Name: BuildOutput
              Configuration:
                ApplicationName: MyApp
                DeploymentGroupName: Production
```

#### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy with CodeDeploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-northeast-1

      - name: Create deployment package
        run: |
          zip -r deployment.zip . \
            -x "*.git*" \
            -x "node_modules/*" \
            -x "tests/*"

      - name: Upload to S3
        run: |
          aws s3 cp deployment.zip s3://my-deployment-bucket/MyApp-${{ github.sha }}.zip

      - name: Create CodeDeploy deployment
        run: |
          aws deploy create-deployment \
            --application-name MyApp \
            --deployment-group-name Production \
            --s3-location bucket=my-deployment-bucket,key=MyApp-${{ github.sha }}.zip,bundleType=zip \
            --description "Deploy commit ${{ github.sha }}"
```

### Lambda デプロイ（SAM統合）

```yaml
# template.yaml（SAM）
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    AutoPublishAlias: live
    DeploymentPreference:
      Type: Canary10Percent5Minutes
      Alarms:
        - !Ref ErrorAlarm
      Hooks:
        PreTraffic: !Ref PreTrafficHook
        PostTraffic: !Ref PostTrafficHook

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.lambda_handler
      Runtime: python3.11

  ErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmDescription: Lambda Error Rate
      MetricName: Errors
      Namespace: AWS/Lambda
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold

  PreTrafficHook:
    Type: AWS::Serverless::Function
    Properties:
      Handler: hooks.pre_traffic_hook
      Runtime: python3.11
      CodeUri: hooks/
      DeploymentPreference:
        Enabled: false

  PostTrafficHook:
    Type: AWS::Serverless::Function
    Properties:
      Handler: hooks.post_traffic_hook
      Runtime: python3.11
      CodeUri: hooks/
      DeploymentPreference:
        Enabled: false
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | 開発環境デプロイ | 開発ブランチの自動デプロイ |
| **テスト** | ステージング環境デプロイ | テスト環境へのBlue/Greenデプロイ |
| **導入** | 本番環境デプロイ | カナリア/リニアデプロイで安全リリース |
| **運用** | ロールバック | 問題発生時の迅速なロールバック |

## メリット

- **マネージドサービス**: インフラ管理不要
- **多様なターゲット**: EC2、Lambda、ECS、オンプレミス対応
- **デプロイ戦略豊富**: In-place、Blue/Green、Canary、Linear
- **自動ロールバック**: 失敗時の自動復旧
- **無料枠あり**: EC2/オンプレミスデプロイは無料
- **CI/CD統合**: CodePipeline、GitHub Actions等と統合容易
- **きめ細かい制御**: ライフサイクルフックで詳細制御

## デメリット

- **学習曲線**: appspec.yml、ライフサイクルイベントの理解が必要
- **Lambda/ECS有料**: Lambda/ECSデプロイは従量課金
- **エージェント管理**: EC2ではCodeDeploy Agentのインストール・管理が必要
- **デバッグ困難**: デプロイ失敗時のトラブルシューティングが複雑
- **AWS専用**: マルチクラウド非対応

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **CodeDeploy** | AWS全般 | 一部無料 | AWSデプロイ自動化 |
| **Jenkins** | 汎用 | 無料 | オンプレミス・マルチクラウド |
| **Spinnaker** | マルチクラウド | 無料 | Netflix製、大規模デプロイ |
| **Octopus Deploy** | .NET特化 | 有料 | Windowsアプリケーション |

## ベストプラクティス

### 1. ヘルスチェックの実装

```bash
# scripts/validate_service.sh
#!/bin/bash
MAX_RETRIES=5
RETRY_INTERVAL=10

for i in $(seq 1 $MAX_RETRIES); do
  echo "Health check attempt $i/$MAX_RETRIES"

  # HTTP ヘルスチェック
  if curl -f http://localhost:3000/health; then
    echo "Service is healthy"
    exit 0
  fi

  sleep $RETRY_INTERVAL
done

echo "Service health check failed"
exit 1
```

### 2. 段階的デプロイ

```yaml
# カナリアデプロイ設定
DeploymentConfig: CodeDeployDefault.LambdaCanary10Percent5Minutes

# 10% → 5分待機 → 100%
# CloudWatchアラームで監視
# エラー率上昇時は自動ロールバック
```

### 3. 環境変数の外部管理

```bash
# scripts/configure_application.sh
#!/bin/bash
# SSM Parameter Store から環境変数取得
export DB_HOST=$(aws ssm get-parameter --name /myapp/prod/db/host --query 'Parameter.Value' --output text)
export DB_PASSWORD=$(aws ssm get-parameter --name /myapp/prod/db/password --with-decryption --query 'Parameter.Value' --output text)

# .env ファイル生成
cat > /var/www/html/myapp/.env <<EOF
DB_HOST=$DB_HOST
DB_PASSWORD=$DB_PASSWORD
NODE_ENV=production
EOF
```

### 4. デプロイ通知

```bash
# scripts/validate_service.sh
#!/bin/bash
# Slack通知
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"Deployment succeeded: MyApp v$VERSION\"}" \
  $SLACK_WEBHOOK_URL
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/codedeploy/
- **ドキュメント**: https://docs.aws.amazon.com/codedeploy/
- **料金**: https://aws.amazon.com/codedeploy/pricing/
- **チュートリアル**: https://docs.aws.amazon.com/codedeploy/latest/userguide/tutorials.html
- **サンプル**: https://github.com/aws-samples/aws-codedeploy-samples

## まとめ

AWS CodeDeployは、EC2、Lambda、ECS、オンプレミスサーバーへのアプリケーションデプロイを自動化するフルマネージドサービスです。Blue/Greenデプロイ、カナリアデプロイ、自動ロールバック機能により、ダウンタイムを最小化しながら安全なデプロイを実現します。EC2/オンプレミスデプロイは無料で、CI/CDパイプラインとの統合も容易なため、AWS環境でのデプロイ自動化には最適なツールです。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS CodeDeploy 2024+
