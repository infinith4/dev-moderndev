# AWS Systems Manager

## 概要

AWS Systems Manager（旧SSM）は、Amazon Web Services公式のクラウド・オンプレミス統合管理サービスです。EC2インスタンス、オンプレミスサーバーの一元管理、パッチ管理、構成管理、オペレーション自動化、セッション管理を提供します。エージェントベースで、AWS CloudWatch、AWS Config、AWS Lambda等と統合し、ハイブリッドクラウド環境の運用効率化、コンプライアンス、セキュリティを実現します。

## 主な機能

### 1. セッション管理（Session Manager）
- **SSHレス接続**: ブラウザ・CLIからインスタンス接続
- **ポート転送**: ローカル→リモートポート転送
- **監査ログ**: セッション履歴記録
- **IAM認証**: SSHキー不要

### 2. パッチ管理（Patch Manager）
- **自動パッチ**: OS、アプリケーションパッチ
- **パッチベースライン**: コンプライアンス基準
- **スケジュール**: 定期パッチ適用
- **レポート**: パッチ状況ダッシュボード

### 3. オートメーション（Automation）
- **Runbook**: 自動化ドキュメント
- **AWS API統合**: EC2、RDS、Lambda操作
- **スケジュール実行**: 定期タスク
- **承認フロー**: 手動承認ステップ

### 4. パラメータストア（Parameter Store）
- **設定管理**: 階層型キーバリューストア
- **シークレット**: 暗号化パスワード、APIキー
- **バージョン管理**: パラメータ履歴
- **無料枠**: 10,000パラメータ無料

### 5. Run Command
- **リモート実行**: 複数インスタンス一括実行
- **スクリプト**: PowerShell、Bash、Python
- **ターゲット**: タグ、インスタンスID指定
- **結果確認**: コマンド実行結果取得

### 6. State Manager
- **構成管理**: Desired State Configuration
- **ドリフト検出**: 構成変更検出
- **自動修復**: 構成自動復元
- **スケジュール**: 定期構成チェック

## 利用方法

### Session Manager接続

```bash
# AWS CLI経由でSSH接続
aws ssm start-session --target i-1234567890abcdef0

# ポート転送（ローカル3306 → リモートRDS 3306）
aws ssm start-session \
  --target i-1234567890abcdef0 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["mydb.rds.amazonaws.com"],"portNumber":["3306"],"localPortNumber":["3306"]}'

# セッション履歴確認
aws ssm describe-sessions --state History
```

### Run Command実行

```bash
# 単一インスタンスでコマンド実行
aws ssm send-command \
  --instance-ids "i-1234567890abcdef0" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["sudo yum update -y"]'

# 複数インスタンス（タグ指定）
aws ssm send-command \
  --targets "Key=tag:Environment,Values=production" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["df -h","free -m"]'

# コマンド実行結果取得
aws ssm get-command-invocation \
  --command-id "command-id-12345" \
  --instance-id "i-1234567890abcdef0"
```

### Parameter Store

```bash
# パラメータ作成（プレーンテキスト）
aws ssm put-parameter \
  --name "/myapp/database/host" \
  --value "mydb.example.com" \
  --type "String"

# パラメータ作成（暗号化）
aws ssm put-parameter \
  --name "/myapp/database/password" \
  --value "SuperSecret123!" \
  --type "SecureString"

# パラメータ取得
aws ssm get-parameter \
  --name "/myapp/database/host"

# 暗号化パラメータ取得（復号化）
aws ssm get-parameter \
  --name "/myapp/database/password" \
  --with-decryption

# 階層パラメータ一覧
aws ssm get-parameters-by-path \
  --path "/myapp/database" \
  --recursive
```

### Automation Runbook

```yaml
# カスタムRunbook例（YAML）
schemaVersion: '0.3'
description: 'EC2 インスタンス自動スナップショット'
parameters:
  InstanceId:
    type: String
    description: 'EC2 Instance ID'

mainSteps:
  - name: createSnapshot
    action: 'aws:executeAwsApi'
    inputs:
      Service: ec2
      Api: CreateSnapshot
      VolumeId: '{{ InstanceId }}'
      Description: 'Automated snapshot'
  
  - name: waitForSnapshot
    action: 'aws:waitForAwsResourceProperty'
    inputs:
      Service: ec2
      Api: DescribeSnapshots
      SnapshotIds:
        - '{{ createSnapshot.SnapshotId }}'
      PropertySelector: '$.Snapshots[0].State'
      DesiredValues:
        - completed
```

### Patch Manager

```bash
# パッチベースライン作成
aws ssm create-patch-baseline \
  --name "Production-Baseline" \
  --operating-system "AMAZON_LINUX_2" \
  --approval-rules 'PatchRules=[{PatchFilterGroup={PatchFilters=[{Key=CLASSIFICATION,Values=[Security,Bugfix]}]},ApproveAfterDays=7}]'

# パッチグループ登録
aws ssm register-patch-baseline-for-patch-group \
  --baseline-id "pb-1234567890abcdef0" \
  --patch-group "Production-Servers"

# パッチ適用実行
aws ssm send-command \
  --document-name "AWS-RunPatchBaseline" \
  --targets "Key=tag:PatchGroup,Values=Production-Servers" \
  --parameters 'Operation=Install'
```

### State Manager

```bash
# State Manager Association作成（定期実行）
aws ssm create-association \
  --name "AWS-UpdateSSMAgent" \
  --targets "Key=instanceids,Values=*" \
  --schedule-expression "cron(0 2 ? * SUN *)"

# Association確認
aws ssm describe-association \
  --association-id "assoc-1234567890abcdef0"
```

### Lambda統合

```python
# Lambda関数でParameter Store使用
import boto3
import os

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    # パラメータ取得
    response = ssm.get_parameter(
        Name='/myapp/database/password',
        WithDecryption=True
    )
    password = response['Parameter']['Value']
    
    # データベース接続
    # ...
    
    return {
        'statusCode': 200,
        'body': 'Success'
    }
```

## エディション・料金

| サービス | 価格 | 特徴 |
|---------|------|------|
| **Session Manager** | 🟢 無料 | セッション管理無料 |
| **Run Command** | 🟢 無料 | コマンド実行無料 |
| **Parameter Store** | 🟢 10,000パラメータ無料 | Standard 無料、Advanced $0.05/パラメータ/月 |
| **Patch Manager** | 🟢 無料 | パッチ管理無料 |
| **Automation** | 💰 $0.002/ステップ | Automation実行課金 |
| **State Manager** | 🟢 無料 | Association実行無料 |

## メリット

### ✅ 主な利点

1. **SSHレス**: Session Managerでセキュア接続
2. **ハイブリッド**: AWS、オンプレミス統合管理
3. **パッチ自動化**: Patch Manager
4. **Parameter Store**: 無料設定管理
5. **Run Command**: 一括リモート実行
6. **監査ログ**: CloudTrail、CloudWatch統合
7. **IAM統合**: きめ細かいアクセス制御
8. **エージェント**: SSM Agent自動インストール（Amazon Linux）
9. **Automation**: Runbook自動化
10. **コスト**: 多くの機能が無料

## デメリット

### ❌ 制約・課題

1. **AWS中心**: AWS環境が前提
2. **エージェント**: SSM Agentインストール必要
3. **学習曲線**: 機能多数で複雑
4. **Automation制限**: 100並列実行まで
5. **Parameter Store制限**: Standard 4KB、Advanced 8KB
6. **Run Command遅延**: 即時実行ではない
7. **UI**: コンソールUI複雑
8. **ドキュメント**: 一部わかりにくい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Ansible** | オープンソース構成管理 | Systems Managerよりマルチクラウド |
| **Chef / Puppet** | 構成管理ツール | Systems Managerより高機能だが複雑 |
| **Azure Automation** | Azure自動化 | Systems Managerと類似（Azure版） |
| **Terraform** | IaC | Systems Managerより宣言的 |
| **HashiCorp Vault** | シークレット管理 | Parameter Storeより高機能 |

## 公式リンク

- **公式サイト**: [https://aws.amazon.com/systems-manager/](https://aws.amazon.com/systems-manager/)
- **ドキュメント**: [https://docs.aws.amazon.com/systems-manager/](https://docs.aws.amazon.com/systems-manager/)
- **料金**: [https://aws.amazon.com/systems-manager/pricing/](https://aws.amazon.com/systems-manager/pricing/)
- **Automation Runbook**: [https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-documents.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-documents.html)

## 関連ドキュメント

- [システム管理ツール一覧](../システム管理ツール/)
- [AWS CLI](../CLIツール/AWS_CLI.md)
- [Ansible](../IaCツール/Ansible.md)
- [AWS運用ベストプラクティス](../../best-practices/aws-operations.md)

---

**カテゴリ**: システム管理ツール  
**対象工程**: 運用、インフラ構築  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
