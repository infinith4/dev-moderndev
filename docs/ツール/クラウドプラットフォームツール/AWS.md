# AWS (Amazon Web Services)

## 概要

AWSは、Amazon提供のクラウドコンピューティングプラットフォームです。200+サービス（EC2、S3、RDS、Lambda等）、グローバルインフラ、従量課金、高可用性、スケーラビリティにより、インフラ構築・運用を効率化します。世界最大シェア、エンタープライズ採用で広く使用されています。

## 主な機能

### 1. コンピューティング
- **EC2**: 仮想サーバー
- **Lambda**: サーバーレス
- **ECS/EKS**: コンテナ
- **Fargate**: サーバーレスコンテナ

### 2. ストレージ
- **S3**: オブジェクトストレージ
- **EBS**: ブロックストレージ
- **EFS**: ファイルストレージ
- **Glacier**: アーカイブ

### 3. データベース
- **RDS**: マネージドDB
- **DynamoDB**: NoSQL
- **Aurora**: MySQL/PostgreSQL互換
- **ElastiCache**: インメモリDB

### 4. ネットワーク
- **VPC**: 仮想ネットワーク
- **CloudFront**: CDN
- **Route 53**: DNS
- **ELB**: ロードバランサー

## 利用方法

### アカウント作成

```
https://aws.amazon.com/

Sign up:
- Email
- クレジットカード
- 電話認証

Free Tier: 12ヶ月無料枠
```

### AWS CLI

```bash
# インストール
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 認証設定
aws configure
AWS Access Key ID: YOUR_ACCESS_KEY
AWS Secret Access Key: YOUR_SECRET_KEY
Default region: ap-northeast-1
Default output format: json

# バージョン確認
aws --version
```

### EC2インスタンス起動

```bash
# インスタンス一覧
aws ec2 describe-instances

# インスタンス起動
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-key \
  --security-groups my-sg

# インスタンス停止
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# インスタンス起動
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# インスタンス削除
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### S3バケット操作

```bash
# バケット作成
aws s3 mb s3://my-bucket

# ファイルアップロード
aws s3 cp file.txt s3://my-bucket/

# ファイルダウンロード
aws s3 cp s3://my-bucket/file.txt ./

# ファイル一覧
aws s3 ls s3://my-bucket/

# バケット削除
aws s3 rb s3://my-bucket --force
```

### Lambda関数

```javascript
// index.js
exports.handler = async (event) => {
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;
};
```

```bash
# 関数作成
zip function.zip index.js

aws lambda create-function \
  --function-name my-function \
  --runtime nodejs18.x \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler index.handler \
  --zip-file fileb://function.zip

# 関数実行
aws lambda invoke \
  --function-name my-function \
  --payload '{"key":"value"}' \
  output.txt

# 関数更新
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip
```

### RDSインスタンス

```bash
# インスタンス作成
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password password123 \
  --allocated-storage 20

# インスタンス一覧
aws rds describe-db-instances

# インスタンス削除
aws rds delete-db-instance \
  --db-instance-identifier mydb \
  --skip-final-snapshot
```

### CloudFormation（IaC）

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-cloudformation-bucket

  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-cf-function
      Runtime: nodejs18.x
      Handler: index.handler
      Role: !GetAtt LambdaRole.Arn
      Code:
        ZipFile: |
          exports.handler = async (event) => {
            return { statusCode: 200, body: 'Hello!' };
          };

  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
```

```bash
# スタック作成
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml

# スタック更新
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template.yaml

# スタック削除
aws cloudformation delete-stack --stack-name my-stack
```

### boto3（Python SDK）

```python
import boto3

# S3クライアント
s3 = boto3.client('s3')

# バケット一覧
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# ファイルアップロード
s3.upload_file('file.txt', 'my-bucket', 'file.txt')

# ファイルダウンロード
s3.download_file('my-bucket', 'file.txt', 'downloaded.txt')

# EC2クライアント
ec2 = boto3.client('ec2')

# インスタンス一覧
response = ec2.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"{instance['InstanceId']}: {instance['State']['Name']}")
```

### IAMユーザー・権限

```bash
# ユーザー作成
aws iam create-user --user-name john

# アクセスキー作成
aws iam create-access-key --user-name john

# ポリシーアタッチ
aws iam attach-user-policy \
  --user-name john \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# ユーザー一覧
aws iam list-users
```

### VPC・ネットワーク

```bash
# VPC作成
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# サブネット作成
aws ec2 create-subnet \
  --vpc-id vpc-123456 \
  --cidr-block 10.0.1.0/24

# セキュリティグループ作成
aws ec2 create-security-group \
  --group-name my-sg \
  --description "My security group" \
  --vpc-id vpc-123456

# インバウンドルール追加
aws ec2 authorize-security-group-ingress \
  --group-id sg-123456 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

## エディション・料金

| サービス | 料金モデル | 特徴 |
|---------|-----------|------|
| **EC2** |  従量課金 | インスタンスタイプ・時間課金 |
| **S3** |  従量課金 | ストレージ量・リクエスト数 |
| **Lambda** |  従量課金 | 実行回数・実行時間 |
| **Free Tier** |  12ヶ月無料 | EC2 750時間、S3 5GB等 |

## メリット

1. **豊富なサービス**: 200+サービス
2. **グローバルインフラ**: 30+リージョン
3. **従量課金**: 初期コスト不要
4. **高可用性**: 99.99% SLA
5. **エコシステム**: 豊富なツール・ドキュメント

## デメリット

1. **コスト**: 大規模で高額化
2. **複雑性**: 学習曲線steep
3. **ベンダーロックイン**: AWS依存
4. **料金体系**: 複雑で予測困難

## 公式リンク

- **公式サイト**: [https://aws.amazon.com/](https://aws.amazon.com/)
- **ドキュメント**: [https://docs.aws.amazon.com/](https://docs.aws.amazon.com/)

## 関連ドキュメント

- [クラウドプラットフォームツール一覧](../クラウドプラットフォームツール/)
- [Azure](./Azure.md)
- [GCP](./GCP.md)

---

**カテゴリ**: クラウドプラットフォームツール
**対象工程**: クラウドインフラ構築・運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0

