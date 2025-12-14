# AWS DataSync

## 概要

**AWS DataSync**は、オンプレミスストレージとAWSストレージ間、またはAWSストレージサービス間のデータ転送を自動化・高速化するフルマネージドサービスです。暗号化、データ整合性検証、帯域幅制御により、安全で効率的な大規模データ移行・同期を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | データ転送・同期サービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 従量課金（転送データ量） |
| **公式サイト** | https://aws.amazon.com/datasync/ |
| **ドキュメント** | https://docs.aws.amazon.com/datasync/ |

## 主な特徴

### 1. 高速データ転送
- 専用ネットワークプロトコル最適化
- 並列転送（最大10Gbps）
- 増分転送（差分のみ）
- 自動圧縮

### 2. 多様なデータソース対応
- **オンプレミス**: NFS、SMB、HDFS、オブジェクトストレージ
- **AWS**: S3、EFS、FSx for Windows File Server、FSx for Lustre、FSx for OpenZFS、FSx for NetApp ONTAP
- **エッジ**: AWS Snowcone（オフライン転送）

### 3. データ整合性・セキュリティ
- 自動データ整合性検証
- 暗号化（転送中・保管時）
- VPC Endpoint対応
- IAM・リソースポリシー

### 4. 自動化・スケジューリング
- EventBridge統合でスケジュール実行
- Lambda統合で自動化
- モニタリング（CloudWatch）
- 詳細ログ

## 使い方

### セットアップ

#### DataSync Agent（オンプレミス → AWS）

```bash
# 1. DataSync Agent OVAダウンロード
# https://docs.aws.amazon.com/datasync/latest/userguide/deploy-agents.html

# 2. VMware / Hyper-V / KVM に Deploy

# 3. Agent 起動後、アクティベーション
# ブラウザで http://<agent-ip>/ にアクセス
# AWS Region選択、Activation Keyを取得

# 4. AWS CLI でエージェント登録
aws datasync create-agent \
  --agent-name "OnPremAgent01" \
  --activation-key "<activation-key>" \
  --region ap-northeast-1

# エージェント確認
aws datasync list-agents
```

### ロケーション設定

#### NFS ロケーション（オンプレミス）

```bash
# NFS サーバーをソースロケーションとして登録
aws datasync create-location-nfs \
  --server-hostname nfs.example.com \
  --subdirectory /data/backups \
  --on-prem-config AgentArns=arn:aws:datasync:ap-northeast-1:123456789012:agent/agent-12345678 \
  --mount-options Version=NFS4_1

# ロケーション確認
aws datasync describe-location-nfs \
  --location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-12345678
```

#### SMB ロケーション（Windows File Server）

```bash
# SMB サーバーをソースロケーションとして登録
aws datasync create-location-smb \
  --server-hostname smb.example.com \
  --subdirectory /share/data \
  --user Administrator \
  --password <password> \
  --agent-arns arn:aws:datasync:ap-northeast-1:123456789012:agent/agent-12345678
```

#### S3 ロケーション

```bash
# S3バケットをデスティネーションとして登録
aws datasync create-location-s3 \
  --s3-bucket-arn arn:aws:s3:::my-backup-bucket \
  --s3-storage-class STANDARD_IA \
  --s3-config '{
    "BucketAccessRoleArn": "arn:aws:iam::123456789012:role/DataSyncS3Role"
  }'
```

#### EFS ロケーション

```bash
# EFS をデスティネーションとして登録
aws datasync create-location-efs \
  --efs-filesystem-arn arn:aws:elasticfilesystem:ap-northeast-1:123456789012:file-system/fs-12345678 \
  --ec2-config '{
    "SubnetArn": "arn:aws:ec2:ap-northeast-1:123456789012:subnet/subnet-12345678",
    "SecurityGroupArns": ["arn:aws:ec2:ap-northeast-1:123456789012:security-group/sg-12345678"]
  }'
```

### タスク作成

```bash
# DataSync タスク作成（NFS → S3）
aws datasync create-task \
  --source-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-nfs-12345 \
  --destination-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-s3-67890 \
  --name "DailyBackupToS3" \
  --options '{
    "VerifyMode": "POINT_IN_TIME_CONSISTENT",
    "OverwriteMode": "ALWAYS",
    "PreserveDeletedFiles": "PRESERVE",
    "PreserveDevices": "NONE",
    "PosixPermissions": "PRESERVE",
    "BytesPerSecond": 104857600,
    "TaskQueueing": "ENABLED",
    "LogLevel": "TRANSFER"
  }' \
  --schedule '{
    "ScheduleExpression": "cron(0 2 * * ? *)"
  }' \
  --cloudwatch-log-group-arn arn:aws:logs:ap-northeast-1:123456789012:log-group:/aws/datasync

# タスク確認
aws datasync describe-task \
  --task-arn arn:aws:datasync:ap-northeast-1:123456789012:task/task-12345678
```

### タスク実行

```bash
# タスク手動実行
aws datasync start-task-execution \
  --task-arn arn:aws:datasync:ap-northeast-1:123456789012:task/task-12345678

# 実行ステータス確認
aws datasync describe-task-execution \
  --task-execution-arn arn:aws:datasync:ap-northeast-1:123456789012:task/task-12345678/execution/exec-12345678

# 実行履歴確認
aws datasync list-task-executions \
  --task-arn arn:aws:datasync:ap-northeast-1:123456789012:task/task-12345678
```

### CloudFormation でのセットアップ

```yaml
# datasync-stack.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: AWS DataSync Setup

Parameters:
  NFSServerHostname:
    Type: String
    Default: nfs.example.com

  S3BucketName:
    Type: String
    Default: my-backup-bucket

Resources:
  # IAM Role for DataSync S3 Access
  DataSyncS3Role:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: datasync.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonS3FullAccess

  # S3 Bucket
  BackupBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref S3BucketName
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToIA
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
          - Id: TransitionToGlacier
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER

  # DataSync NFS Location
  NFSLocation:
    Type: AWS::DataSync::LocationNFS
    Properties:
      ServerHostname: !Ref NFSServerHostname
      Subdirectory: /data/backups
      OnPremConfig:
        AgentArns:
          - !Sub "arn:aws:datasync:${AWS::Region}:${AWS::AccountId}:agent/${AgentId}"

  # DataSync S3 Location
  S3Location:
    Type: AWS::DataSync::LocationS3
    Properties:
      S3BucketArn: !GetAtt BackupBucket.Arn
      S3StorageClass: STANDARD_IA
      S3Config:
        BucketAccessRoleArn: !GetAtt DataSyncS3Role.Arn

  # DataSync Task
  BackupTask:
    Type: AWS::DataSync::Task
    Properties:
      SourceLocationArn: !Ref NFSLocation
      DestinationLocationArn: !Ref S3Location
      Name: DailyBackupToS3
      Options:
        VerifyMode: POINT_IN_TIME_CONSISTENT
        OverwriteMode: ALWAYS
        PreserveDeletedFiles: PRESERVE
        LogLevel: TRANSFER
      Schedule:
        ScheduleExpression: "cron(0 2 * * ? *)"  # 毎日2:00 UTC
      CloudWatchLogGroupArn: !GetAtt LogGroup.Arn

  # CloudWatch Log Group
  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/datasync/backup-task
      RetentionInDays: 30

Outputs:
  TaskArn:
    Value: !Ref BackupTask
    Description: DataSync Task ARN
```

### 実践例

#### 1. オンプレミス NFS → S3（日次バックアップ）

```bash
# スケジュール: 毎日午前2時（JST）
# ScheduleExpression: "cron(0 17 * * ? *)"  # 17:00 UTC = 02:00 JST

aws datasync create-task \
  --source-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-nfs \
  --destination-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-s3 \
  --name "DailyNFSToS3Backup" \
  --options '{
    "VerifyMode": "POINT_IN_TIME_CONSISTENT",
    "OverwriteMode": "ALWAYS",
    "PreserveDeletedFiles": "PRESERVE",
    "LogLevel": "TRANSFER"
  }' \
  --schedule '{
    "ScheduleExpression": "cron(0 17 * * ? *)"
  }' \
  --includes '[
    {"FilterType": "SIMPLE_PATTERN", "Value": "/backups/*"}
  ]' \
  --excludes '[
    {"FilterType": "SIMPLE_PATTERN", "Value": "*.tmp"},
    {"FilterType": "SIMPLE_PATTERN", "Value": "*.log"}
  ]'
```

#### 2. S3 → EFS（データ同期）

```bash
# S3からEFSへデータ同期（開発環境セットアップ）
aws datasync create-task \
  --source-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-s3 \
  --destination-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-efs \
  --name "S3ToEFSSync" \
  --options '{
    "VerifyMode": "ONLY_FILES_TRANSFERRED",
    "OverwriteMode": "NEVER",
    "Uid": "NONE",
    "Gid": "NONE"
  }'

# 手動実行
aws datasync start-task-execution \
  --task-arn arn:aws:datasync:ap-northeast-1:123456789012:task/task-s3-efs
```

#### 3. EFS → EFS（クロスリージョン DR）

```bash
# ap-northeast-1 → us-west-2（DR用）
aws datasync create-task \
  --source-location-arn arn:aws:datasync:ap-northeast-1:123456789012:location/loc-efs-tokyo \
  --destination-location-arn arn:aws:datasync:us-west-2:123456789012:location/loc-efs-oregon \
  --name "EFSDRReplication" \
  --options '{
    "VerifyMode": "POINT_IN_TIME_CONSISTENT",
    "OverwriteMode": "ALWAYS",
    "TransferMode": "CHANGED"
  }' \
  --schedule '{
    "ScheduleExpression": "cron(0 */6 * * ? *)"
  }'
```

### モニタリング

```python
# monitoring.py
import boto3
from datetime import datetime, timedelta

datasync = boto3.client('datasync')
cloudwatch = boto3.client('cloudwatch')

def monitor_datasync_task(task_arn):
    """DataSync タスク実行監視"""
    # 最新の実行ステータス
    response = datasync.list_task_executions(
        TaskArn=task_arn,
        MaxResults=1
    )

    if not response['TaskExecutions']:
        print("No executions found")
        return

    execution = response['TaskExecutions'][0]
    exec_arn = execution['TaskExecutionArn']

    # 詳細情報取得
    details = datasync.describe_task_execution(
        TaskExecutionArn=exec_arn
    )

    print(f"Status: {details['Status']}")
    print(f"BytesTransferred: {details.get('BytesTransferred', 0) / (1024**3):.2f} GB")
    print(f"FilesTransferred: {details.get('FilesTransferred', 0)}")

    # CloudWatch メトリクス取得
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)

    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/DataSync',
        MetricName='BytesTransferred',
        Dimensions=[
            {'Name': 'TaskId', 'Value': task_arn.split('/')[-1]}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Sum']
    )

    print("\nTransfer Rate:")
    for datapoint in metrics['Datapoints']:
        rate_mbps = datapoint['Sum'] / (1024**2) / 5  # 5分あたり
        print(f"{datapoint['Timestamp']}: {rate_mbps:.2f} MB/s")

# 使用例
task_arn = "arn:aws:datasync:ap-northeast-1:123456789012:task/task-12345678"
monitor_datasync_task(task_arn)
```

### アラート設定

```yaml
# cloudformation/datasync-alerts.yaml
Resources:
  TaskFailedAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: DataSync-Task-Failed
      MetricName: TaskExecutionStatus
      Namespace: AWS/DataSync
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      Dimensions:
        - Name: TaskId
          Value: !Ref DataSyncTask
      AlarmActions:
        - !Ref AlertTopic

  LowThroughputAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: DataSync-Low-Throughput
      MetricName: BytesTransferred
      Namespace: AWS/DataSync
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10485760  # 10 MB/s
      ComparisonOperator: LessThanThreshold
      Dimensions:
        - Name: TaskId
          Value: !Ref DataSyncTask
      AlarmActions:
        - !Ref AlertTopic
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **導入** | データマイグレーション | オンプレミス→AWS移行 |
| **実装** | 開発環境データ同期 | 本番データの開発環境同期 |
| **テスト** | テストデータ準備 | S3→EFS データロード |
| **運用** | バックアップ | 定期バックアップ自動化 |

## メリット

- **高速転送**: 最大10Gbps、専用プロトコル最適化
- **自動化**: スケジュール実行、EventBridge統合
- **データ整合性**: 自動検証、エラーハンドリング
- **増分転送**: 差分のみ転送でコスト削減
- **セキュアリティ**: 暗号化、VPC Endpoint対応
- **多様なソース**: NFS、SMB、S3、EFS、FSx対応
- **マネージドサービス**: インフラ管理不要

## デメリット

- **従量課金**: 転送データ量で課金（大規模移行はコスト増）
- **Agent管理**: オンプレミス環境ではAgent必要
- **ネットワーク帯域**: 帯域幅が狭い場合は転送時間増
- **リアルタイム同期不可**: スケジュール実行のみ
- **初期設定複雑**: ロケーション・タスク設定が多い

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **DataSync** | AWS全般 | 従量課金 | AWS大規模データ転送 |
| **AWS Transfer Family** | SFTP/FTPS/FTP | 従量課金 | レガシープロトコル対応 |
| **Snowball** | オフライン転送 | デバイスレンタル | PB級オフライン転送 |
| **rsync** | 汎用 | 無料 | 小規模・手動転送 |

## ベストプラクティス

### 1. 帯域幅制御

```bash
# ビジネスアワー外に高速転送、営業時間は帯域制限
aws datasync create-task \
  --options '{
    "BytesPerSecond": 52428800
  }'
```

### 2. フィルタリング

```bash
# 必要なファイルのみ転送
aws datasync create-task \
  --includes '[
    {"FilterType": "SIMPLE_PATTERN", "Value": "/data/*.csv"},
    {"FilterType": "SIMPLE_PATTERN", "Value": "/logs/202501*.log"}
  ]' \
  --excludes '[
    {"FilterType": "SIMPLE_PATTERN", "Value": "*.tmp"},
    {"FilterType": "SIMPLE_PATTERN", "Value": ".DS_Store"}
  ]'
```

### 3. 段階的移行

```text
Phase 1: パイロット転送（小規模データ）
Phase 2: 履歴データ転送（大規模）
Phase 3: 最終差分転送（カットオーバー直前）
Phase 4: 継続同期（本番稼働後）
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/datasync/
- **ドキュメント**: https://docs.aws.amazon.com/datasync/
- **料金**: https://aws.amazon.com/datasync/pricing/
- **FAQ**: https://aws.amazon.com/datasync/faqs/
- **ワークショップ**: https://datasync-workshop.aws-management.tools/

## まとめ

AWS DataSyncは、オンプレミスとAWS間、またはAWSサービス間のデータ転送を自動化・高速化するフルマネージドサービスです。暗号化、データ整合性検証、帯域幅制御により、安全で効率的な大規模データ移行・同期を実現します。スケジュール実行、増分転送、多様なデータソース対応により、クラウド移行やバックアップ自動化に最適なツールです。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS DataSync 2024+
