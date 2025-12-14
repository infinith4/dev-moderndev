# AWS Config

## 概要

**AWS Config**は、AWSリソースの設定変更を継続的に記録・評価するフルマネージドサービスです。コンプライアンスチェック、セキュリティ監査、リソース変更履歴の追跡により、インフラの健全性とコンプライアンス準拠を保証します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | リソース設定管理・コンプライアンス監視サービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 従量課金（設定アイテム・ルール評価数） |
| **公式サイト** | https://aws.amazon.com/config/ |
| **ドキュメント** | https://docs.aws.amazon.com/config/ |

## 主な特徴

### 1. リソース設定記録
- 全AWSリソースの設定変更履歴
- 削除されたリソースの設定履歴
- リソース間の関係性マッピング
- S3への自動バックアップ

### 2. コンプライアンスルール
- **AWS管理ルール**: 100以上の事前定義ルール
- **カスタムルール**: Lambda関数で独自ルール作成
- **Conformance Packs**: 複数ルールのパッケージ化
- 自動修復（AWS Systems Manager連携）

### 3. 変更通知
- SNS通知
- EventBridge統合
- Lambda関数トリガー
- リアルタイム変更検出

### 4. マルチアカウント・リージョン対応
- AWS Organizations統合
- 集約ビュー（Aggregator）
- クロスリージョン集約
- 一元管理コンソール

## 使い方

### セットアップ

```bash
# AWS CLI で有効化
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig \
  --recording-group allSupported=true,includeGlobalResourceTypes=true

# 配信チャネル設定（S3）
aws configservice put-delivery-channel \
  --delivery-channel name=default,s3BucketName=my-config-bucket,snsTopicARN=arn:aws:sns:ap-northeast-1:123456789012:config-topic

# 記録開始
aws configservice start-configuration-recorder \
  --configuration-recorder-name default

# ステータス確認
aws configservice describe-configuration-recorder-status
```

### CloudFormation でのセットアップ

```yaml
# config-setup.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: AWS Config Setup

Resources:
  # S3 Bucket for Config
  ConfigBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::AccountId}-config-bucket"
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: DeleteOldVersions
            Status: Enabled
            NoncurrentVersionExpirationInDays: 90

  # S3 Bucket Policy
  ConfigBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref ConfigBucket
      PolicyDocument:
        Statement:
          - Sid: AWSConfigBucketPermissionsCheck
            Effect: Allow
            Principal:
              Service: config.amazonaws.com
            Action: s3:GetBucketAcl
            Resource: !GetAtt ConfigBucket.Arn
          - Sid: AWSConfigBucketExistenceCheck
            Effect: Allow
            Principal:
              Service: config.amazonaws.com
            Action: s3:ListBucket
            Resource: !GetAtt ConfigBucket.Arn
          - Sid: AWSConfigPutObject
            Effect: Allow
            Principal:
              Service: config.amazonaws.com
            Action: s3:PutObject
            Resource: !Sub "${ConfigBucket.Arn}/*"

  # SNS Topic
  ConfigTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: config-notifications

  # Configuration Recorder
  ConfigRecorder:
    Type: AWS::Config::ConfigurationRecorder
    Properties:
      Name: default
      RoleArn: !GetAtt ConfigRole.Arn
      RecordingGroup:
        AllSupported: true
        IncludeGlobalResourceTypes: true

  # Delivery Channel
  DeliveryChannel:
    Type: AWS::Config::DeliveryChannel
    Properties:
      Name: default
      S3BucketName: !Ref ConfigBucket
      SnsTopicARN: !Ref ConfigTopic

  # IAM Role for Config
  ConfigRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: config.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/ConfigRole
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetBucketVersioning
                  - s3:PutObject
                  - s3:GetObject
                Resource:
                  - !GetAtt ConfigBucket.Arn
                  - !Sub "${ConfigBucket.Arn}/*"
```

### AWS管理ルールの適用

```bash
# S3バケット暗号化チェック
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-bucket-encryption-enabled",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
    },
    "Scope": {
      "ComplianceResourceTypes": ["AWS::S3::Bucket"]
    }
  }'

# IAMパスワードポリシーチェック
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "iam-password-policy",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "IAM_PASSWORD_POLICY"
    },
    "InputParameters": "{\"RequireUppercaseCharacters\":\"true\",\"RequireLowercaseCharacters\":\"true\",\"RequireNumbers\":\"true\",\"MinimumPasswordLength\":\"14\"}"
  }'

# RDS暗号化チェック
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "rds-storage-encrypted",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "RDS_STORAGE_ENCRYPTED"
    },
    "Scope": {
      "ComplianceResourceTypes": ["AWS::RDS::DBInstance"]
    }
  }'

# EBS暗号化チェック
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "encrypted-volumes",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "ENCRYPTED_VOLUMES"
    },
    "Scope": {
      "ComplianceResourceTypes": ["AWS::EC2::Volume"]
    }
  }'
```

### カスタムルールの作成

```python
# lambda/custom_rule.py
import boto3
import json

def lambda_handler(event, context):
    """
    カスタムルール: EC2インスタンスが特定タグを持っているかチェック
    """
    config = boto3.client('config')

    # 評価対象リソース
    invoking_event = json.loads(event['invokingEvent'])
    configuration_item = invoking_event['configurationItem']
    resource_id = configuration_item['resourceId']

    # コンプライアンス判定
    compliance_type = 'COMPLIANT'
    annotation = 'Resource has required tags'

    # タグチェック
    tags = configuration_item.get('tags', {})
    required_tags = ['Environment', 'Owner', 'CostCenter']

    missing_tags = [tag for tag in required_tags if tag not in tags]

    if missing_tags:
        compliance_type = 'NON_COMPLIANT'
        annotation = f'Missing required tags: {", ".join(missing_tags)}'

    # 評価結果を送信
    config.put_evaluations(
        Evaluations=[
            {
                'ComplianceResourceType': configuration_item['resourceType'],
                'ComplianceResourceId': resource_id,
                'ComplianceType': compliance_type,
                'Annotation': annotation,
                'OrderingTimestamp': configuration_item['configurationItemCaptureTime']
            }
        ],
        ResultToken=event['resultToken']
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Evaluated {resource_id}: {compliance_type}')
    }
```

```yaml
# CloudFormation でカスタムルール登録
Resources:
  CustomRuleLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: config-custom-rule-required-tags
      Runtime: python3.11
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          # Lambda関数コード（上記参照）

  CustomConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: ec2-required-tags
      Description: Check if EC2 instances have required tags
      Scope:
        ComplianceResourceTypes:
          - AWS::EC2::Instance
      Source:
        Owner: CUSTOM_LAMBDA
        SourceIdentifier: !GetAtt CustomRuleLambda.Arn
        SourceDetails:
          - EventSource: aws.config
            MessageType: ConfigurationItemChangeNotification
```

### 自動修復（Remediation）

```yaml
# CloudFormation で自動修復設定
Resources:
  # ルール: S3パブリックアクセスブロック
  S3PublicAccessBlockRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED

  # 自動修復設定
  S3PublicAccessRemediation:
    Type: AWS::Config::RemediationConfiguration
    Properties:
      ConfigRuleName: !Ref S3PublicAccessBlockRule
      TargetType: SSM_DOCUMENT
      TargetIdentifier: AWS-PublishSNSNotification  # または独自のSSMドキュメント
      TargetVersion: "1"
      Parameters:
        AutomationAssumeRole:
          StaticValue:
            Values:
              - !GetAtt RemediationRole.Arn
        TopicArn:
          StaticValue:
            Values:
              - !Ref RemediationTopic
        Message:
          StaticValue:
            Values:
              - "S3 bucket public access detected and blocked"
      Automatic: true
      MaximumAutomaticAttempts: 3
      RetryAttemptSeconds: 60
```

### Conformance Packs（コンプライアンスパック）

```yaml
# conformance-pack-template.yaml
Resources:
  SecurityBestPracticesConformancePack:
    Type: AWS::Config::ConformancePack
    Properties:
      ConformancePackName: security-best-practices
      TemplateBody: |
        Resources:
          # S3暗号化
          S3BucketEncryptionEnabled:
            Type: AWS::Config::ConfigRule
            Properties:
              ConfigRuleName: s3-bucket-encryption-enabled
              Source:
                Owner: AWS
                SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED

          # IAMパスワードポリシー
          IAMPasswordPolicy:
            Type: AWS::Config::ConfigRule
            Properties:
              ConfigRuleName: iam-password-policy
              Source:
                Owner: AWS
                SourceIdentifier: IAM_PASSWORD_POLICY
              InputParameters:
                RequireUppercaseCharacters: true
                RequireLowercaseCharacters: true
                RequireNumbers: true
                MinimumPasswordLength: 14

          # RDS暗号化
          RDSStorageEncrypted:
            Type: AWS::Config::ConfigRule
            Properties:
              ConfigRuleName: rds-storage-encrypted
              Source:
                Owner: AWS
                SourceIdentifier: RDS_STORAGE_ENCRYPTED

          # VPC Flow Logs
          VPCFlowLogsEnabled:
            Type: AWS::Config::ConfigRule
            Properties:
              ConfigRuleName: vpc-flow-logs-enabled
              Source:
                Owner: AWS
                SourceIdentifier: VPC_FLOW_LOGS_ENABLED
```

```bash
# Conformance Pack デプロイ
aws configservice put-conformance-pack \
  --conformance-pack-name security-best-practices \
  --template-s3-uri s3://my-config-bucket/conformance-pack-template.yaml
```

### コンプライアンスレポート

```bash
# コンプライアンスサマリー取得
aws configservice describe-compliance-by-config-rule

# 特定ルールの詳細
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name s3-bucket-encryption-enabled

# 非準拠リソースリスト
aws configservice describe-compliance-by-resource \
  --resource-type AWS::S3::Bucket \
  --compliance-types NON_COMPLIANT

# JSON形式でエクスポート
aws configservice describe-compliance-by-config-rule \
  --output json > compliance-report.json
```

### EventBridge 統合（自動アラート）

```yaml
# CloudFormation で EventBridge ルール設定
Resources:
  ConfigComplianceChangeRule:
    Type: AWS::Events::Rule
    Properties:
      Name: config-compliance-change
      Description: Trigger on Config compliance changes
      EventPattern:
        source:
          - aws.config
        detail-type:
          - Config Rules Compliance Change
        detail:
          messageType:
            - ComplianceChangeNotification
          newEvaluationResult:
            complianceType:
              - NON_COMPLIANT
      State: ENABLED
      Targets:
        - Arn: !Ref AlertTopic
          Id: SNSTopic
        - Arn: !GetAtt AlertLambda.Arn
          Id: LambdaFunction

  # Lambda でSlack通知
  AlertLambda:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.11
      Handler: index.lambda_handler
      Code:
        ZipFile: |
          import json
          import urllib.request

          def lambda_handler(event, context):
              detail = event['detail']
              rule_name = detail['configRuleName']
              resource_id = detail['resourceId']
              compliance_type = detail['newEvaluationResult']['complianceType']

              message = {
                  'text': f':warning: Config Rule Violation\nRule: {rule_name}\nResource: {resource_id}\nStatus: {compliance_type}'
              }

              req = urllib.request.Request(
                  os.environ['SLACK_WEBHOOK_URL'],
                  data=json.dumps(message).encode(),
                  headers={'Content-Type': 'application/json'}
              )
              urllib.request.urlopen(req)

              return {'statusCode': 200}
      Environment:
        Variables:
          SLACK_WEBHOOK_URL: !Ref SlackWebhookUrl
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **詳細設計（インフラ）** | 設計ルール定義 | コンプライアンスルール策定 |
| **実装（インフラ）** | リソース設定追跡 | 構成変更の記録・監視 |
| **テスト（インフラ）** | コンプライアンステスト | ルール準拠確認 |
| **運用** | 継続的監視 | セキュリティ・コンプライアンス監視 |

## メリット

- **継続的監視**: リソース設定変更をリアルタイム追跡
- **コンプライアンス自動化**: 100以上のAWS管理ルール
- **変更履歴**: 削除済みリソースを含む完全な履歴
- **自動修復**: 非準拠リソースの自動修正
- **マルチアカウント対応**: Organizations統合で一元管理
- **統合性**: EventBridge、SNS、Lambda連携
- **監査証跡**: S3バックアップで長期保存

## デメリット

- **従量課金**: 設定アイテム・ルール評価数で課金（コスト増加リスク）
- **初期設定複雑**: S3、SNS、IAMロール等の設定が必要
- **リアルタイム性制限**: 最大15分の遅延（設定記録）
- **カスタムルール開発**: Lambda関数作成スキルが必要
- **大量アラート**: 適切な閾値設定がないとアラート過多

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **AWS Config** | AWS全般 | 従量課金 | AWSコンプライアンス管理 |
| **Cloud Custodian** | マルチクラウド | 無料 | オープンソース、YAML定義 |
| **Terraform Sentinel** | Terraform | 有料 | IaCポリシーチェック |
| **Azure Policy** | Azure | 無料 | Azureコンプライアンス |

## ベストプラクティス

### 1. 段階的導入

```text
Phase 1: 重要リソースのみ記録
  - EC2、RDS、S3等の重要リソース
  - コスト抑制

Phase 2: AWS管理ルール適用
  - セキュリティベースライン
  - 暗号化、パブリックアクセス制御

Phase 3: カスタムルール追加
  - 組織固有のポリシー
  - タグ規則、命名規則

Phase 4: 自動修復有効化
  - 自動修復スクリプト実装
  - SSM Automationドキュメント
```

### 2. コスト最適化

```bash
# 重要リソースのみ記録
aws configservice put-configuration-recorder \
  --configuration-recorder '{
    "name": "default",
    "roleARN": "arn:aws:iam::123456789012:role/ConfigRole",
    "recordingGroup": {
      "allSupported": false,
      "resourceTypes": [
        "AWS::EC2::Instance",
        "AWS::RDS::DBInstance",
        "AWS::S3::Bucket",
        "AWS::IAM::Role"
      ]
    }
  }'

# S3ライフサイクルポリシー（古いログ削除）
# 90日後にGlacier、365日後に削除
```

### 3. アラート最適化

```yaml
# 重要度別通知
Resources:
  CriticalAlertRule:
    Type: AWS::Events::Rule
    Properties:
      EventPattern:
        source:
          - aws.config
        detail:
          configRuleName:
            - s3-bucket-public-read-prohibited
            - iam-root-access-key-check
            - rds-storage-encrypted
      Targets:
        - Arn: !Ref CriticalAlertTopic  # 即座に通知

  WarningAlertRule:
    Type: AWS::Events::Rule
    Properties:
      EventPattern:
        source:
          - aws.config
        detail:
          configRuleName:
            - ec2-required-tags
            - unused-iam-user
      Targets:
        - Arn: !Ref WarningAlertTopic  # 日次サマリー
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/config/
- **ドキュメント**: https://docs.aws.amazon.com/config/
- **料金**: https://aws.amazon.com/config/pricing/
- **管理ルール一覧**: https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html
- **Conformance Packs**: https://docs.aws.amazon.com/config/latest/developerguide/conformance-packs.html

## まとめ

AWS Configは、AWSリソースの設定変更を継続的に記録・評価するフルマネージドサービスです。コンプライアンスチェック、セキュリティ監査、リソース変更履歴の追跡により、インフラの健全性とコンプライアンス準拠を保証します。100以上のAWS管理ルール、カスタムルール作成、自動修復機能により、セキュリティとコンプライアンスの自動化を実現します。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS Config 2024+
