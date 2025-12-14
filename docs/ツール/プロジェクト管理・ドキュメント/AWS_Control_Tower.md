# AWS Control Tower

## 概要

**AWS Control Tower**は、マルチアカウントAWS環境のセットアップと管理を自動化するAWSのガバナンスサービスです。ベストプラクティスに基づいたランディングゾーン、ガードレール（ガバナンスルール）、アカウント管理機能により、セキュアで統制の取れたAWS環境を迅速に構築できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | マルチアカウントガバナンスサービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 従量課金（Organizations、Config等の料金） |
| **公式サイト** | https://aws.amazon.com/controltower/ |
| **ドキュメント** | https://docs.aws.amazon.com/controltower/ |

## 主な特徴

### 1. ランディングゾーン自動構築
- **マルチアカウント構造**: 本番、開発、監査用アカウント自動作成
- **OU（組織単位）**: 組織階層の自動設定
- **ネットワーク基盤**: VPC、サブネット自動構築
- **ログ集約**: CloudTrail、Config集約アカウント

### 2. ガードレール（ガバナンスルール）
- **予防的ガードレール**: SCP（Service Control Policy）で制限
- **検出的ガードレール**: AWS Configで違反検出
- **必須ガードレール**: 全アカウント強制適用
- **推奨/選択的ガードレール**: 任意適用

### 3. Account Factory
- セルフサービスアカウントプロビジョニング
- テンプレート化されたアカウント作成
- ベースライン設定自動適用
- AWS Service Catalog統合

### 4. 一元管理
- ダッシュボードでガバナンス状況可視化
- ドリフト検出（設定逸脱検出）
- 集中ログ管理
- コンプライアンス監視

## 使い方

### セットアップ

#### ランディングゾーン作成

```text
# AWS Control Tower セットアップ手順

1. 前提条件確認
   - マネジメントアカウントでログイン
   - Organizations未設定（または既存Organizationsを引き継ぎ）
   - 管理者権限

2. Control Tower コンソールアクセス
   https://console.aws.amazon.com/controltower/

3. "Set up landing zone" クリック

4. ランディングゾーン設定
   - ホームリージョン選択（例: ap-northeast-1）
   - 追加リージョン選択（オプション）
   - FoundationalOU作成
   - Log ArchiveアカウントとAuditアカウント自動作成

5. セットアップ実行（60-90分）
   - Organizations設定
   - OU作成
   - 共有アカウント作成
   - ガードレール適用
   - ログ集約設定
```

#### ランディングゾーン構造

```text
# デフォルトのOU構造

Root（Organizations ルート）
├── Security OU（セキュリティ専用）
│   ├── Log Archive Account（ログ集約アカウント）
│   └── Audit Account（監査アカウント）
│
├── Sandbox OU（開発・検証用）
│   ├── Dev Account 1
│   ├── Dev Account 2
│   └── Test Account
│
└── Production OU（本番環境）
    ├── Production Account 1
    └── Production Account 2

# カスタムOU追加可能
├── Infrastructure OU（共通インフラ）
├── Data OU（データレイク）
└── Partners OU（パートナー連携）
```

### アカウント作成（Account Factory）

#### Service Catalog経由でアカウント作成

```bash
# AWS CLI でアカウントプロビジョニング
aws servicecatalog provision-product \
  --product-id prod-abcdefgh12345678 \
  --provisioning-artifact-id pa-abcdefgh12345678 \
  --provisioned-product-name "ProductionApp1Account" \
  --provisioning-parameters \
    Key=AccountEmail,Value=app1-prod@example.com \
    Key=AccountName,Value="Production App1" \
    Key=ManagedOrganizationalUnit,Value="Production OU" \
    Key=SSOUserEmail,Value=admin@example.com \
    Key=SSOUserFirstName,Value=Admin \
    Key=SSOUserLastName,Value=User

# ステータス確認
aws servicecatalog describe-provisioned-product \
  --id pp-abcdefgh12345678
```

#### Terraform でアカウント作成

```hcl
# terraform/account-factory.tf
resource "aws_servicecatalog_provisioned_product" "new_account" {
  name                     = "ProductionApp2Account"
  product_id               = data.aws_servicecatalog_product.account_factory.id
  provisioning_artifact_id = data.aws_servicecatalog_product.account_factory.provisioning_artifact_ids[0]

  provisioning_parameters {
    key   = "AccountEmail"
    value = "app2-prod@example.com"
  }

  provisioning_parameters {
    key   = "AccountName"
    value = "Production App2"
  }

  provisioning_parameters {
    key   = "ManagedOrganizationalUnit"
    value = "Production OU"
  }

  provisioning_parameters {
    key   = "SSOUserEmail"
    value = "admin@example.com"
  }

  provisioning_parameters {
    key   = "SSOUserFirstName"
    value = "Admin"
  }

  provisioning_parameters {
    key   = "SSOUserLastName"
    value = "User"
  }
}

data "aws_servicecatalog_product" "account_factory" {
  name = "AWS Control Tower Account Factory"
}
```

### ガードレールの設定

#### 必須ガードレール（Mandatory）

```text
# 自動適用される必須ガードレール（抜粋）

1. CloudTrail有効化
   - すべてのアカウントでCloudTrail有効
   - Log Archiveアカウントに集約

2. AWS Config有効化
   - リソース設定変更を記録
   - コンプライアンスチェック

3. ルートユーザーMFA
   - ルートユーザーMFA有効化を推奨

4. ログ保護
   - Log ArchiveアカウントのS3バケット削除禁止
   - ログ改ざん防止
```

#### 推奨ガードレール（Strongly Recommended）

```bash
# AWS Console で推奨ガードレール有効化
# Control Tower → Guardrails → Browse guardrails
# "Disallow internet connection through RDP" を選択して有効化

# または、AWS CLI（CloudFormation経由）
aws cloudformation create-stack \
  --stack-name enable-rdp-guardrail \
  --template-body file://guardrail-rdp.yaml
```

```yaml
# guardrail-rdp.yaml（例）
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  SCPPolicy:
    Type: AWS::Organizations::Policy
    Properties:
      Name: DisallowRDPInternet
      Type: SERVICE_CONTROL_POLICY
      Content: |
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Deny",
              "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:AuthorizeSecurityGroupEgress"
              ],
              "Resource": "*",
              "Condition": {
                "StringEquals": {
                  "ec2:IpProtocol": "tcp",
                  "ec2:FromPort": "3389",
                  "ec2:ToPort": "3389"
                }
              }
            }
          ]
        }
      TargetIds:
        - !Ref ProductionOU
```

#### 選択的ガードレール（Elective）

```text
# 選択的ガードレール例

1. S3バケット暗号化
   - すべてのS3バケットで暗号化を強制

2. EBSボリューム暗号化
   - 暗号化されていないEBSボリューム作成禁止

3. RDSバックアップ
   - RDSインスタンス自動バックアップ有効化を検出

4. 未使用IAMロール
   - 90日間未使用のIAMロール検出
```

### カスタマイズ可能なランディングゾーン（CfCT）

```yaml
# Customizations for Control Tower (CfCT)
# manifest.yaml
version: 2021-03-15

resources:
  # カスタムStackSets
  - name: CustomVPCConfig
    resource_file: templates/vpc-config.yaml
    deploy_method: stack_set
    deployment_targets:
      accounts:
        - Production OU
    regions:
      - ap-northeast-1

  # カスタムConfig Rules
  - name: CustomConfigRules
    resource_file: templates/config-rules.yaml
    deploy_method: stack_set
    deployment_targets:
      organizational_units:
        - Production OU
        - Sandbox OU

portfolios:
  # Service Catalog製品追加
  - name: CustomAccountFactory
    owner: Platform Team
    description: Custom account factory products
    products:
      - name: DataLakeAccount
        owner: Data Team
        template: templates/data-lake-account.yaml
```

### ドリフト検出

```bash
# ドリフト検出（設定逸脱確認）
# Control Tower Console → Drift detection

# ドリフトが検出された場合
# 1. 原因特定（CloudTrailログ確認）
# 2. 手動修正
# 3. または、ランディングゾーン再セットアップ

# ドリフトの種類
# - OU削除
# - SCPポリシー変更
# - 共有アカウントのIAMロール変更
# - CloudTrail/Config無効化
```

### SSO（AWS IAM Identity Center）統合

```bash
# Control Tower は自動的に IAM Identity Center を有効化

# SSO設定
# 1. IAM Identity Center コンソールへ
# 2. ユーザー/グループ作成
# 3. Permission Sets作成（例: AdministratorAccess、ReadOnly）
# 4. アカウント・OUにPermission Setsを割り当て

# マルチアカウントアクセス
# https://<your-directory>.awsapps.com/start
# ユーザーは1つのポータルから全アカウントにアクセス
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **企画** | マルチアカウント戦略 | アカウント・OU構造設計 |
| **詳細設計（インフラ）** | ガバナンスルール定義 | ガードレール選定・カスタマイズ |
| **実装（インフラ）** | アカウントプロビジョニング | Account Factoryで自動作成 |
| **運用** | ガバナンス監視 | コンプライアンス継続監視 |

## メリット

- **自動化**: マルチアカウント環境を数時間で構築
- **ベストプラクティス**: AWSガバナンスベストプラクティス適用
- **セルフサービス**: Account Factoryでユーザー自身がアカウント作成
- **ガードレール**: セキュリティ・コンプライアンスルール自動適用
- **集中管理**: ダッシュボードで全アカウント監視
- **ドリフト検出**: 設定逸脱の自動検出
- **SSO統合**: 一元的なユーザー認証

## デメリット

- **初期設定時間**: ランディングゾーンセットアップに60-90分
- **既存環境統合困難**: 既存Organizationsからの移行は複雑
- **カスタマイズ制限**: ランディングゾーンのカスタマイズには追加ツール（CfCT）が必要
- **コスト**: Organizations、Config、CloudTrail等の従量課金
- **ホームリージョン固定**: セットアップ後のホームリージョン変更不可
- **削除困難**: ランディングゾーン削除は手動作業が多い

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Control Tower** | AWS | 従量課金 | AWSマルチアカウント自動化 |
| **AWS Organizations** | AWS | 無料 | 手動マルチアカウント管理 |
| **Azure Lighthouse** | Azure | 無料 | Azureマルチテナント管理 |
| **Terraform Cloud** | マルチクラウド | 有料 | IaCベースマルチアカウント |

## ベストプラクティス

### 1. OU構造設計

```text
# 推奨OU構造

Root
├── Security OU（必須）
│   ├── Log Archive Account
│   └── Audit Account
│
├── Infrastructure OU（共通インフラ）
│   ├── Network Account（Transit Gateway等）
│   └── Shared Services Account（Active Directory等）
│
├── Sandbox OU（開発・検証）
│   ├── Developer Sandbox Accounts（個人用）
│   └── Team Sandbox Accounts（チーム用）
│
├── Workloads OU（ワークロード）
│   ├── Development OU
│   ├── Staging OU
│   └── Production OU
│
└── Suspended OU（停止アカウント）
    └── Decommissioned Accounts
```

### 2. ガードレール戦略

```text
# 段階的ガードレール適用

Phase 1: 必須ガードレール（全OU）
  - CloudTrail有効化
  - AWS Config有効化
  - ルートユーザーMFA

Phase 2: セキュリティベースライン（全OU）
  - S3バケット暗号化
  - EBSボリューム暗号化
  - RDSストレージ暗号化

Phase 3: 本番環境強化（Production OU）
  - RDPインターネットアクセス禁止
  - SSHインターネットアクセス禁止
  - リージョン制限

Phase 4: コスト最適化（Sandbox OU）
  - 大型インスタンス作成禁止
  - 未使用リソース検出
```

### 3. Account Factory カスタマイズ

```yaml
# CfCT でAccount Factory製品追加
# manifest.yaml
portfolios:
  - name: CustomAccountTypes
    products:
      # データレイク専用アカウント
      - name: DataLakeAccount
        template: templates/data-lake-account.yaml
        parameters:
          - VpcCidr: 10.1.0.0/16
          - EnableDataSync: true

      # マイクロサービス専用アカウント
      - name: MicroserviceAccount
        template: templates/microservice-account.yaml
        parameters:
          - EKSClusterEnabled: true
          - ServiceMeshEnabled: true
```

### 4. コスト管理

```yaml
# ガードレールでコスト制御
Resources:
  CostControlSCP:
    Type: AWS::Organizations::Policy
    Properties:
      Type: SERVICE_CONTROL_POLICY
      Content: |
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Deny",
              "Action": [
                "ec2:RunInstances"
              ],
              "Resource": "arn:aws:ec2:*:*:instance/*",
              "Condition": {
                "StringNotLike": {
                  "ec2:InstanceType": [
                    "t3.*",
                    "t3a.*",
                    "t4g.*"
                  ]
                }
              }
            }
          ]
        }
      TargetIds:
        - !Ref SandboxOU
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/controltower/
- **ドキュメント**: https://docs.aws.amazon.com/controltower/
- **ベストプラクティス**: https://docs.aws.amazon.com/controltower/latest/userguide/best-practices.html
- **Customizations for Control Tower**: https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/
- **Workshop**: https://controltower.aws-management.tools/

## まとめ

AWS Control Towerは、マルチアカウントAWS環境のセットアップと管理を自動化するガバナンスサービスです。ランディングゾーン自動構築、ガードレール、Account Factoryにより、セキュアで統制の取れたAWS環境を迅速に構築できます。AWS Organizationsの上位レイヤーとして機能し、ベストプラクティスに基づいたガバナンスを提供します。大規模AWS環境のガバナンス自動化には必須のサービスです。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS Control Tower 2024+
