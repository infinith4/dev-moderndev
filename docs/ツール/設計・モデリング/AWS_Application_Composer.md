# AWS Application Composer

## 概要

**AWS Application Composer**は、AWS Serverless Application Model（SAM）をビジュアルに設計できるAWS公式のビジュアルデザイナーです。ドラッグ&ドロップでサーバーレスアプリケーションのアーキテクチャを設計し、Infrastructure as Code（IaC）として自動生成します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | サーバーレスアプリケーションビジュアルデザイナー |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟢 無料（AWS利用料は別途） |
| **公式サイト** | https://aws.amazon.com/application-composer/ |
| **ドキュメント** | https://docs.aws.amazon.com/application-composer/ |

## 主な特徴

### 1. ビジュアル設計
- ドラッグ&ドロップでアーキテクチャ設計
- リアルタイムプレビュー
- AWSサービス間の接続を自動認識
- ベストプラクティステンプレート

### 2. IaC自動生成
- AWS SAMテンプレート自動生成
- YAML/JSON形式での出力
- 既存テンプレートのインポート・編集
- 双方向同期（ビジュアル ⇔ コード）

### 3. ローカル開発統合
- VS Code拡張機能
- AWS Toolkit for VS Code統合
- ローカルテスト（SAM CLI連携）
- Git統合

### 4. マルチサービス対応
- Lambda（関数）
- API Gateway（REST/HTTP/WebSocket）
- DynamoDB（データベース）
- S3（ストレージ）
- Step Functions（ワークフロー）
- EventBridge（イベント）
- SQS/SNS（メッセージング）
- Cognito（認証）

## 使い方

### AWS Console での使用

```text
# AWS Management Console からアクセス
1. AWS Console にログイン
2. "Application Composer" を検索
3. "Create project" をクリック
4. テンプレート選択または新規作成

# または、Lambda Console から
Lambda Console → Applications → Create application → Use Application Composer
```

### VS Code 拡張機能のインストール

```bash
# VS Code 拡張機能検索
# "AWS Toolkit" をインストール

# または、コマンドラインから
code --install-extension amazonwebservices.aws-toolkit-vscode

# Application Composer を起動
# Ctrl+Shift+P (Cmd+Shift+P on Mac)
# "AWS: Open Application Composer" を選択
```

### プロジェクト作成

#### 1. シンプルなREST API

```yaml
# template.yaml（自動生成）
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Simple REST API with Lambda and DynamoDB

Globals:
  Function:
    Timeout: 10
    Runtime: python3.11
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable

Resources:
  # API Gateway
  UsersApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Cors:
        AllowMethods: "'GET,POST,PUT,DELETE'"
        AllowHeaders: "'Content-Type,X-Amz-Date,Authorization'"
        AllowOrigin: "'*'"

  # Lambda Function - Get Users
  GetUsersFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/get_users/
      Handler: app.lambda_handler
      Events:
        GetUsers:
          Type: Api
          Properties:
            RestApiId: !Ref UsersApi
            Path: /users
            Method: GET
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref UsersTable

  # Lambda Function - Create User
  CreateUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/create_user/
      Handler: app.lambda_handler
      Events:
        CreateUser:
          Type: Api
          Properties:
            RestApiId: !Ref UsersApi
            Path: /users
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable

  # DynamoDB Table
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - AttributeName: userId
          AttributeType: S
      KeySchema:
        - AttributeName: userId
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST

Outputs:
  UsersApiUrl:
    Description: "API Gateway endpoint URL"
    Value: !Sub "https://${UsersApi}.execute-api.${AWS::Region}.amazonaws.com/prod/"
```

#### 2. イベント駆動アーキテクチャ

```yaml
# template.yaml（Application Composer で設計）
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Event-driven architecture with S3, Lambda, and SQS

Resources:
  # S3 Bucket
  UploadBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::StackName}-uploads"
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: !GetAtt ProcessImageFunction.Arn

  # Lambda Permission for S3
  S3InvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ProcessImageFunction
      Action: lambda:InvokeFunction
      Principal: s3.amazonaws.com
      SourceArn: !GetAtt UploadBucket.Arn

  # Lambda Function - Process Image
  ProcessImageFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/process_image/
      Handler: app.lambda_handler
      Runtime: python3.11
      Timeout: 60
      MemorySize: 512
      Environment:
        Variables:
          QUEUE_URL: !GetAtt ProcessingQueue.QueueUrl
      Policies:
        - S3ReadPolicy:
            BucketName: !Ref UploadBucket
        - SQSSendMessagePolicy:
            QueueName: !GetAtt ProcessingQueue.QueueName

  # SQS Queue
  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "${AWS::StackName}-processing-queue"
      VisibilityTimeout: 300
      MessageRetentionPeriod: 1209600  # 14 days

  # Lambda Function - Worker
  WorkerFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/worker/
      Handler: app.lambda_handler
      Runtime: python3.11
      Timeout: 300
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
```

#### 3. Step Functions ワークフロー

```yaml
# template.yaml（Application Composer で設計）
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Order processing workflow with Step Functions

Resources:
  # Step Functions State Machine
  OrderWorkflow:
    Type: AWS::Serverless::StateMachine
    Properties:
      DefinitionUri: statemachine/order_workflow.asl.json
      Policies:
        - LambdaInvokePolicy:
            FunctionName: !Ref ValidateOrderFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref ProcessPaymentFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref FulfillOrderFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref SendNotificationFunction

  # Lambda - Validate Order
  ValidateOrderFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/validate_order/
      Handler: app.lambda_handler
      Runtime: python3.11

  # Lambda - Process Payment
  ProcessPaymentFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/process_payment/
      Handler: app.lambda_handler
      Runtime: python3.11

  # Lambda - Fulfill Order
  FulfillOrderFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/fulfill_order/
      Handler: app.lambda_handler
      Runtime: python3.11

  # Lambda - Send Notification
  SendNotificationFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/send_notification/
      Handler: app.lambda_handler
      Runtime: python3.11
```

```json
// statemachine/order_workflow.asl.json
{
  "Comment": "Order processing workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "${ValidateOrderFunctionArn}",
      "Next": "ProcessPayment",
      "Catch": [
        {
          "ErrorEquals": ["ValidationError"],
          "Next": "OrderFailed"
        }
      ]
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "${ProcessPaymentFunctionArn}",
      "Next": "FulfillOrder",
      "Catch": [
        {
          "ErrorEquals": ["PaymentError"],
          "Next": "OrderFailed"
        }
      ]
    },
    "FulfillOrder": {
      "Type": "Task",
      "Resource": "${FulfillOrderFunctionArn}",
      "Next": "SendNotification"
    },
    "SendNotification": {
      "Type": "Task",
      "Resource": "${SendNotificationFunctionArn}",
      "End": true
    },
    "OrderFailed": {
      "Type": "Fail",
      "Cause": "Order processing failed"
    }
  }
}
```

### ビジュアルエディタの使い方

```text
# Application Composer UI 操作

1. リソースパレット（左側）
   - Lambda、API Gateway、DynamoDB等のAWSサービスアイコン
   - ドラッグ&ドロップでキャンバスに配置

2. キャンバス（中央）
   - リソース間を線で接続
   - 接続すると自動的にIAMポリシー・イベント設定が生成

3. プロパティパネル（右側）
   - 選択したリソースの設定
   - 環境変数、タイムアウト、メモリサイズ等

4. コードビュー（下部）
   - 生成されたSAMテンプレートをリアルタイム表示
   - 直接編集も可能（ビジュアルに反映）

# 接続の種類
- Lambda ← API Gateway: API エンドポイント
- Lambda → DynamoDB: データベースアクセス
- S3 → Lambda: イベントトリガー
- Lambda → SQS: メッセージ送信
- SQS → Lambda: イベントソース
```

### ローカルでのテスト

```bash
# SAM CLI でローカル実行
sam build

# API をローカルで起動
sam local start-api
# http://localhost:3000 でアクセス可能

# 特定のLambda関数を実行
sam local invoke GetUsersFunction -e events/get_users.json

# DynamoDB Local と連携
docker run -p 8000:8000 amazon/dynamodb-local
sam local start-api --docker-network host
```

### デプロイ

```bash
# SAM CLI でデプロイ
sam deploy --guided

# 初回デプロイ時の設定
# Stack Name: my-serverless-app
# AWS Region: ap-northeast-1
# Confirm changes: y
# Allow SAM CLI IAM role creation: y
# Save arguments to configuration file: y

# 2回目以降は設定不要
sam deploy

# デプロイ後の確認
aws cloudformation describe-stacks \
  --stack-name my-serverless-app \
  --query 'Stacks[0].Outputs'
```

### CI/CD統合

```yaml
# .github/workflows/deploy.yml
name: Deploy Serverless App

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup SAM CLI
        uses: aws-actions/setup-sam@v2

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-northeast-1

      - name: SAM Build
        run: sam build

      - name: SAM Deploy
        run: sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | アーキテクチャ検討 | サーバーレス構成の可視化 |
| **基本設計** | システム設計 | AWSサービス構成図作成 |
| **詳細設計** | IaC設計 | SAMテンプレート自動生成 |
| **実装** | サーバーレス開発 | Lambda、API Gateway実装 |

## メリット

- **ビジュアル設計**: ドラッグ&ドロップで直感的にアーキテクチャ設計
- **IaC自動生成**: SAMテンプレートを自動生成、手動記述不要
- **ベストプラクティス**: AWS推奨構成を自動適用
- **双方向同期**: ビジュアル編集とコード編集が相互反映
- **無料**: AWS利用料のみ、ツール自体は無料
- **VS Code統合**: ローカル開発環境で利用可能
- **SAM CLI連携**: ローカルテスト・デプロイが容易
- **学習コスト低**: AWSサービス構成を視覚的に理解

## デメリット

- **SAM限定**: CloudFormation、Terraform等には非対応
- **サーバーレス特化**: EC2、ECS等の非サーバーレスは非対応
- **カスタマイズ制限**: 複雑なカスタムリソースは直接編集が必要
- **AWS専用**: マルチクラウド非対応
- **ブラウザ版制限**: 大規模プロジェクトではVS Code推奨
- **学習曲線**: SAM、CloudFormationの基礎知識が必要

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Application Composer** | AWS SAM | 無料 | AWSサーバーレス設計 |
| **AWS CloudFormation Designer** | CloudFormation | 無料 | AWS全般IaC設計 |
| **Terraform Visual** | Terraform | 有料 | マルチクラウドIaC |
| **Serverless Framework Dashboard** | Serverless | 無料〜有料 | サーバーレス開発全般 |

## ベストプラクティス

### 1. リソース命名規則

```yaml
# 環境変数で命名規則統一
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-MyFunction-${Environment}"
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
```

### 2. パラメータ化

```yaml
# Parameters セクションで環境差分を吸収
Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod

  LogRetentionDays:
    Type: Number
    Default: 7
    Description: CloudWatch Logs retention period

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
```

### 3. セキュリティベストプラクティス

```yaml
# 最小権限の原則
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Policies:
        # ❌ 広すぎる権限
        # - AmazonDynamoDBFullAccess

        # ✅ 必要最小限の権限
        - DynamoDBReadPolicy:
            TableName: !Ref MyTable
```

### 4. 環境変数の管理

```yaml
# SSM Parameter Store / Secrets Manager 利用
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          # ❌ ハードコード
          # API_KEY: "12345abcde"

          # ✅ SSM Parameter Store参照
          API_KEY: !Sub "{{resolve:ssm:/myapp/${Environment}/api-key}}"

          # ✅ Secrets Manager参照
          DB_PASSWORD: !Sub "{{resolve:secretsmanager:MyDBSecret:SecretString:password}}"
```

### 5. テスト戦略

```bash
# ユニットテスト（Lambda関数）
pytest tests/unit/

# 統合テスト（ローカル）
sam local start-api &
pytest tests/integration/

# E2Eテスト（デプロイ後）
pytest tests/e2e/ --stack-name my-serverless-app
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/application-composer/
- **ドキュメント**: https://docs.aws.amazon.com/application-composer/
- **SAM CLI**: https://docs.aws.amazon.com/serverless-application-model/
- **チュートリアル**: https://aws.amazon.com/getting-started/hands-on/build-serverless-app-application-composer/
- **VS Code拡張機能**: https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode

## まとめ

AWS Application Composerは、サーバーレスアプリケーションをビジュアルに設計し、AWS SAMテンプレートを自動生成できるAWS公式ツールです。ドラッグ&ドロップの直感的な操作でアーキテクチャを設計でき、IaCのベストプラクティスを自動適用します。無料で利用でき、VS Code統合やSAM CLI連携により、ローカル開発からデプロイまでシームレスなワークフローを実現します。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS Application Composer 2024+
