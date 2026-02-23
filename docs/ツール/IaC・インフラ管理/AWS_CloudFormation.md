# AWS CloudFormation

## 概要

AWS CloudFormationは、Amazon Web Services（AWS）が提供するInfrastructure as Code（IaC）サービスです。JSON/YAMLテンプレートを使用してAWSリソースをモデル化し、プロビジョニングを自動化します。AWSネイティブのサービスとして、AWSの全リソースに対応し、スタック単位でのリソース管理が可能です。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **CloudFormation自体** |  無料 | テンプレート作成、スタック管理の利用は無料 |
| **プロビジョニングされたリソース** |  従量課金 | 作成されたAWSリソース（EC2、RDS等）の料金は別途発生 |

**注意**: CloudFormation自体は無料ですが、作成されたAWSリソース（EC2、RDS、S3等）は通常のAWS料金が発生します。

## メリット・デメリット

### メリット
-  **AWSネイティブ**: AWS公式サービス、全AWSリソースに完全対応
-  **無料**: CloudFormation自体に利用料金なし
-  **スタック管理**: 関連リソースをスタック単位で一括管理
-  **ドリフト検出**: 実際のリソースとテンプレートの差分を検出
-  **ロールバック機能**: デプロイ失敗時の自動ロールバック
-  **変更セット**: 変更内容を事前プレビュー可能
-  **IAM統合**: AWSの権限管理と完全統合
-  **クロススタック参照**: スタック間でリソースを共有可能

### デメリット
-  **AWS専用**: AWSリソースのみ対応、マルチクラウド不可
-  **YAML/JSON**: HCLと比較して冗長な記述
-  **ループ処理困難**: 繰り返し処理が苦手（マクロで対応可能）
-  **状態管理の限界**: Terraformのような明示的な状態ファイルなし
-  **エラーメッセージ**: エラー時のメッセージが分かりにくい場合あり
-  **実行時間**: 大規模スタックの更新に時間がかかる

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **4. 基本設計（インフラ）** | AWSインフラの基本構成設計 | CloudFormationテンプレート設計書 |
| **6. 詳細設計（インフラ）** | 詳細なリソース定義、パラメータ設計 | CloudFormationテンプレート |
| **8. インフラ構築** | 実際のAWSリソースのプロビジョニング | スタック、リソース |
| **11. 導入** | 本番環境へのインフラデプロイ | デプロイ手順書、本番スタック |

## 基本的な利用方法

### 1. AWS CLIのインストール

```bash
# macOS (Homebrew)
brew install awscli

# Windows (MSI Installer)
# https://aws.amazon.com/cli/からダウンロード

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# バージョン確認
aws --version

# 認証情報の設定
aws configure
```

### 2. 基本的なワークフロー

```bash
# 1. スタックの作成
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters file://parameters.json

# 2. スタックの更新
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template-updated.yaml

# 3. 変更セットの作成（プレビュー）
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name my-changes \
  --template-body file://template.yaml

# 4. スタックの削除
aws cloudformation delete-stack \
  --stack-name my-stack

# 5. スタックのステータス確認
aws cloudformation describe-stacks \
  --stack-name my-stack
```

### 3. 基本的なCloudFormationテンプレート例（YAML）

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPCとサブネットを作成する基本テンプレート'

Parameters:
  VpcCidr:
    Type: String
    Default: '10.0.0.0/16'
    Description: 'VPCのCIDRブロック'

Resources:
  # VPCの作成
  MainVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: main-vpc

  # パブリックサブネットの作成
  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.1.0/24'
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: public-subnet

Outputs:
  VPCId:
    Description: 'VPCのID'
    Value: !Ref MainVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC-ID'

  SubnetId:
    Description: 'パブリックサブネットのID'
    Value: !Ref PublicSubnet
    Export:
      Name: !Sub '${AWS::StackName}-Subnet-ID'
```

## 工程別の活用方法

### 4. 基本設計（インフラ）での活用

**目的**: AWSインフラの基本構成をCloudFormationで設計

**活用方法**:
- VPC、サブネット、セキュリティグループの構成設計
- リソース間の依存関係の明確化
- ネストされたスタックの設計
- パラメータとアウトプットの定義

**CloudFormation Designerの活用**:
AWS CloudFormation Designerを使用して、ビジュアルにインフラを設計できます。
- AWSコンソール → CloudFormation → デザイナー
- ドラッグ&ドロップでリソースを配置
- テンプレートの自動生成

**成果物**:
- CloudFormation設計書
- テンプレート構造図
- ネストスタック設計書

---

### 6. 詳細設計（インフラ）での活用

**目的**: 詳細なリソース定義とパラメータ設計

**活用方法**:
- 組み込み関数（Ref、GetAtt、Sub等）の活用
- 条件分岐（Conditions）の実装
- クロススタック参照の設計
- パラメータストアとの統合

**詳細設計例**:
```yaml
AWSTemplateFormatVersion: '2010-09-09'

Parameters:
  Environment:
    Type: String
    AllowedValues:
      - dev
      - staging
      - prod
    Description: '環境名'

Conditions:
  IsProduction: !Equals [!Ref Environment, prod]

Resources:
  # 本番環境のみMulti-AZ
  Database:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: !If [IsProduction, db.m5.large, db.t3.medium]
      MultiAZ: !If [IsProduction, true, false]
      AllocatedStorage: !If [IsProduction, 100, 20]
      Engine: postgres
      MasterUsername: !Sub '{{resolve:secretsmanager:${DBSecret}:SecretString:username}}'
      MasterUserPassword: !Sub '{{resolve:secretsmanager:${DBSecret}:SecretString:password}}'
```

**ベストプラクティス**:
- パラメータは環境別ファイルで管理
- 機密情報はSecrets Manager/Systems Manager Parameter Storeを使用
- 大規模な構成はネストスタックで分割

---

### 8. インフラ構築での活用

**目的**: 実際のAWSリソースのプロビジョニング

**活用方法**:
- 環境別スタックのデプロイ
- スタックセット（複数リージョン/アカウント）の活用
- ドリフト検出による構成チェック
- スタックポリシーによる保護

**スタックセットの活用**:
```bash
# スタックセットの作成（複数リージョンにデプロイ）
aws cloudformation create-stack-set \
  --stack-set-name my-stackset \
  --template-body file://template.yaml \
  --parameters file://parameters.json

# スタックインスタンスの追加
aws cloudformation create-stack-instances \
  --stack-set-name my-stackset \
  --accounts 123456789012 \
  --regions us-east-1 ap-northeast-1
```

**ドリフト検出**:
```bash
# ドリフト検出の開始
aws cloudformation detect-stack-drift \
  --stack-name my-stack

# ドリフト検出結果の確認
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-stack
```

---

### 11. 導入での活用

**目的**: 本番環境への安全なデプロイ

**活用方法**:
- CI/CDパイプラインとの統合
- 変更セットによる事前レビュー
- ロールバック手順の準備
- スタックポリシーによる重要リソースの保護

**CI/CD統合例（AWS CodePipeline）**:
```yaml
# buildspec.yml
version: 0.2

phases:
  install:
    commands:
      - pip install cfn-lint
  build:
    commands:
      # CloudFormationテンプレートの検証
      - cfn-lint template.yaml

      # 変更セットの作成
      - |
        aws cloudformation create-change-set \
          --stack-name my-stack \
          --change-set-name pipeline-changes-$(date +%s) \
          --template-body file://template.yaml \
          --parameters file://parameters.json

artifacts:
  files:
    - template.yaml
    - parameters.json
```

**スタックポリシー（重要リソースの保護）**:
```json
{
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "Update:Delete",
      "Resource": "LogicalResourceId/ProductionDatabase"
    },
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "Update:*",
      "Resource": "*"
    }
  ]
}
```

## 公式ドキュメント

- [AWS CloudFormation 公式サイト](https://aws.amazon.com/cloudformation/)
- [AWS CloudFormation ドキュメント](https://docs.aws.amazon.com/cloudformation/)
- [AWS CloudFormation テンプレートリファレンス](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html)
- [AWS CloudFormation ベストプラクティス](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
- [AWS CloudFormation Designer](https://console.aws.amazon.com/cloudformation/designer)
- [AWS CDK](https://aws.amazon.com/cdk/) - プログラミング言語でCloudFormationを生成

## 学習リソース

### チュートリアル
- [AWS CloudFormation Getting Started](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.html)
- [AWS CloudFormation Workshop](https://catalog.workshops.aws/cfn101/en-US)
- [AWS CloudFormation Samples](https://github.com/awslabs/aws-cloudformation-templates)

### 書籍
- "AWS CloudFormation Master Class" (Udemy)
- "Infrastructure as Code" by Kief Morris

### 動画・コース
- [AWS Training - CloudFormation](https://www.aws.training/Details/eLearning?id=42343)
- [Udemy - AWS CloudFormation](https://www.udemy.com/topic/aws-cloudformation/)
- [YouTube - AWS CloudFormation Tutorial](https://www.youtube.com/results?search_query=aws+cloudformation+tutorial)

### コミュニティ
- [AWS CloudFormation GitHub](https://github.com/aws-cloudformation/)
- [AWS re:Post - CloudFormation](https://repost.aws/tags/TAgOdRefu6ShempO3dWPEofg/aws-cloud-formation)
- [Stack Overflow - CloudFormation](https://stackoverflow.com/questions/tagged/amazon-cloudformation)

## 関連リンク

### 関連ツール
- [AWS CDK](https://aws.amazon.com/cdk/) - TypeScript/Python等でCloudFormationを生成
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) - CloudFormationテンプレートのリンター
- [CloudFormation Guard](https://github.com/aws-cloudformation/cloudformation-guard) - ポリシー検証ツール
- [Former2](https://former2.com/) - 既存AWSリソースからCloudFormation生成
- [Taskcat](https://github.com/aws-ia/taskcat) - CloudFormationテンプレートのテストツール
- [Sceptre](https://sceptre.cloudreach.com/) - CloudFormationのラッパーツール

### AWS公式リソース
- [AWS Quick Starts](https://aws.amazon.com/quickstart/) - 検証済みCloudFormationテンプレート集
- [AWS Solutions Library](https://aws.amazon.com/solutions/) - AWSソリューションのCloudFormationテンプレート
- [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) - カスタムリソース

### ベストプラクティス
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
- [AWS Security Best Practices for CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/security-best-practices.html)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

