# CloudFormation Guard

## 概要

CloudFormation Guard（cfn-guard）は、AWSが提供するオープンソースのポリシー検証ツールです。独自のGuard DSL（ドメイン固有言語）を用いて、CloudFormationテンプレートやJSON/YAML形式のデータに対するコンプライアンスルールを宣言的に記述し、テンプレートがセキュリティポリシーやベストプラクティスに準拠しているかを自動検証します。CI/CDパイプラインに組み込むことで、デプロイ前のポリシー違反検出を実現し、ガバナンスの強化とインフラストラクチャの品質向上に貢献します。

## 主な機能

### 1. ポリシー検証
- **Guard DSL**: 宣言的なルール記述言語
- **テンプレート検証**: CloudFormation YAML/JSONの検証
- **Terraform対応**: Terraform planの出力にも適用可能
- **カスタムルール**: 独自のポリシールール定義

### 2. 組み込みルール
- **AWS規約ルール**: AWSベストプラクティスに基づくルール
- **CISベンチマーク**: CIS AWS Foundations対応ルール
- **NIST対応**: NISTフレームワーク対応ルール
- **PCI DSS**: 決済カード業界データセキュリティ基準

### 3. テスト機能
- **ユニットテスト**: `cfn-guard test` によるルールテスト
- **テストデータ**: PASS/FAILケースの定義
- **バリデーション**: ルール構文の事前検証

### 4. CI/CD統合
- **GitHub Actions**: ワークフローでの自動検証
- **AWS CodePipeline**: パイプライン統合
- **Pre-commit**: コミット前のポリシーチェック

### 5. レポーティング
- **詳細出力**: 違反箇所の詳細レポート
- **JSON出力**: 機械可読な結果出力
- **カスタムメッセージ**: ルールごとの説明メッセージ

## 利用方法

### インストール

```bash
# Homebrewでインストール（macOS/Linux）
brew install cloudformation-guard

# Cargoでインストール
cargo install cfn-guard

# バイナリダウンロード（Linux）
curl -Lo cfn-guard https://github.com/aws-cloudformation/cloudformation-guard/releases/latest/download/cfn-guard-v3-ubuntu-latest.tar.gz
tar -xzf cfn-guard-v3-ubuntu-latest.tar.gz

# バージョン確認
cfn-guard --version
```

### Guard DSLルールの作成

```ruby
# rules/security.guard

# S3バケットの暗号化を必須にする
rule s3_bucket_encryption {
    AWS::S3::Bucket {
        Properties.BucketEncryption.ServerSideEncryptionConfiguration[*] {
            ServerSideEncryptionByDefault.SSEAlgorithm in ["aws:kms", "AES256"]
                <<S3バケットにはサーバーサイド暗号化が必要です>>
        }
    }
}

# S3バケットのパブリックアクセスをブロック
rule s3_bucket_public_access {
    AWS::S3::Bucket {
        Properties.PublicAccessBlockConfiguration exists
        Properties.PublicAccessBlockConfiguration {
            BlockPublicAcls == true
            BlockPublicPolicy == true
            IgnorePublicAcls == true
            RestrictPublicBuckets == true
                <<S3バケットのパブリックアクセスを全てブロックしてください>>
        }
    }
}

# RDSインスタンスの暗号化を必須にする
rule rds_encryption {
    AWS::RDS::DBInstance {
        Properties.StorageEncrypted == true
            <<RDSインスタンスのストレージ暗号化が必要です>>
    }
}

# セキュリティグループで0.0.0.0/0からのSSHを禁止
rule no_open_ssh {
    AWS::EC2::SecurityGroup {
        Properties.SecurityGroupIngress[*] {
            when IpProtocol == "tcp" {
                when FromPort == 22 OR ToPort == 22 {
                    CidrIp != "0.0.0.0/0"
                        <<SSHポート(22)を全世界に公開しないでください>>
                }
            }
        }
    }
}
```

### CloudFormationテンプレートの検証

```bash
# 単一テンプレートの検証
cfn-guard validate \
  --data template.yaml \
  --rules rules/security.guard

# 複数ルールファイルで検証
cfn-guard validate \
  --data template.yaml \
  --rules rules/

# JSON形式で結果出力
cfn-guard validate \
  --data template.yaml \
  --rules rules/security.guard \
  --output-format json

# 詳細出力
cfn-guard validate \
  --data template.yaml \
  --rules rules/security.guard \
  --show-summary all
```

### 検証対象のCloudFormationテンプレート例

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: S3 Bucket with encryption

Resources:
  SecureBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-secure-bucket
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: alias/my-key
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      VersioningConfiguration:
        Status: Enabled
```

### ルールのテスト

```bash
# テストの実行
cfn-guard test \
  --rules-file rules/security.guard \
  --test-data tests/security_tests.yaml
```

```yaml
# tests/security_tests.yaml
- name: S3バケット暗号化テスト - 合格ケース
  input:
    Resources:
      TestBucket:
        Type: AWS::S3::Bucket
        Properties:
          BucketEncryption:
            ServerSideEncryptionConfiguration:
              - ServerSideEncryptionByDefault:
                  SSEAlgorithm: aws:kms
  expectations:
    rules:
      s3_bucket_encryption: PASS

- name: S3バケット暗号化テスト - 不合格ケース
  input:
    Resources:
      TestBucket:
        Type: AWS::S3::Bucket
        Properties:
          BucketName: no-encryption-bucket
  expectations:
    rules:
      s3_bucket_encryption: FAIL
```

### CI/CD統合

```yaml
# .github/workflows/cfn-guard.yml
name: CloudFormation Guard

on:
  push:
    paths:
      - 'cloudformation/**'
  pull_request:
    paths:
      - 'cloudformation/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install cfn-guard
        run: |
          curl -Lo cfn-guard.tar.gz https://github.com/aws-cloudformation/cloudformation-guard/releases/latest/download/cfn-guard-v3-ubuntu-latest.tar.gz
          tar -xzf cfn-guard.tar.gz
          sudo mv cfn-guard /usr/local/bin/

      - name: Run guard tests
        run: |
          cfn-guard test \
            --rules-file rules/security.guard \
            --test-data tests/

      - name: Validate templates
        run: |
          cfn-guard validate \
            --data cloudformation/ \
            --rules rules/ \
            --show-summary all
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **CloudFormation Guard** | 無料 | オープンソース、Apache-2.0 License |

## メリット

### 主な利点

1. **ポリシーの自動検証**: テンプレートのコンプライアンスを自動化
2. **宣言的ルール**: Guard DSLによる直感的なルール記述
3. **シフトレフト**: デプロイ前のポリシー違反検出
4. **AWS公式**: AWSが開発・メンテナンスするオープンソース
5. **テスト可能**: ルール自体のユニットテストが可能
6. **CI/CD統合**: パイプラインでの自動検証
7. **組み込みルール**: CIS、NIST等の標準ルールが利用可能
8. **Terraform対応**: CloudFormation以外のデータにも適用可能
9. **カスタムメッセージ**: 違反時のわかりやすいエラーメッセージ
10. **軽量**: 単一バイナリでの実行

## デメリット

### 制約・課題

1. **Guard DSL学習**: 独自DSLの習得が必要
2. **ルール保守**: ポリシー変更に伴うルールの継続的メンテナンス
3. **複雑な条件**: 複雑なビジネスロジックの表現に限界がある
4. **エコシステム**: OPAやSentinelと比較してコミュニティが小さい
5. **デバッグ**: ルールのデバッグが困難な場合がある
6. **AWS中心**: AWS以外のクラウドでの活用は限定的
7. **ドキュメント**: 日本語ドキュメントが少ない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **OPA/Rego** | 汎用ポリシーエンジン | Guard DSLより汎用だが学習曲線が大きい |
| **Checkov** | IaCセキュリティスキャナー | マルチクラウド対応だがカスタムルール記述が異なる |
| **cfn-lint** | CloudFormation構文チェッカー | ポリシーではなく構文チェックに特化 |
| **Sentinel** | HashiCorp製ポリシー言語 | Terraform Enterpriseに統合 |
| **AWS Config Rules** | AWSマネージドルール | デプロイ後の検出（事前検証ではない） |

## 公式リンク

- **GitHub**: [https://github.com/aws-cloudformation/cloudformation-guard](https://github.com/aws-cloudformation/cloudformation-guard)
- **ドキュメント**: [https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html)
- **Guard DSLリファレンス**: [https://github.com/aws-cloudformation/cloudformation-guard/blob/main/docs/GUARD_RULES.md](https://github.com/aws-cloudformation/cloudformation-guard/blob/main/docs/GUARD_RULES.md)
- **組み込みルール**: [https://github.com/aws-cloudformation/aws-guard-rules-registry](https://github.com/aws-cloudformation/aws-guard-rules-registry)

## 関連ドキュメント

- [IaCインフラ管理一覧](../IaCインフラ管理/)
- [tflint](./tflint.md)
- [セキュリティツール](../セキュリティ/)

---

**カテゴリ**: IaCインフラ管理
**対象工程**: 設計・実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
