# AWS CDK Assertions

## 概要

**AWS CDK Assertions**は、AWS Cloud Development Kit（CDK）で作成したInfrastructure as Code（IaC）をテストするための公式テストライブラリです。スナップショットテスト、細粒度アサーション、テンプレート検証により、CDKスタックの品質を保証します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | IaCテストライブラリ（CDK専用） |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** |  無料 |
| **公式サイト** | https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html |
| **ドキュメント** | https://docs.aws.amazon.com/cdk/v2/guide/testing.html |

## 主な特徴

### 1. スナップショットテスト
- CloudFormationテンプレート全体の比較
- 意図しない変更の検出
- リグレッションテスト
- 初回生成時に基準スナップショット作成

### 2. 細粒度アサーション
- リソース存在確認
- リソースプロパティ検証
- リソース数カウント
- 部分一致検証

### 3. テストフレームワーク統合
- Jest（JavaScript/TypeScript）
- pytest（Python）
- JUnit（Java）
- NUnit（C#）

### 4. CI/CD統合
- GitHub Actions
- AWS CodeBuild
- GitLab CI/CD
- 自動テスト実行

## 使い方

### インストール

#### TypeScript/JavaScript

```bash
# CDK プロジェクト作成
npx cdk init app --language typescript
cd my-cdk-app

# テストライブラリは CDK v2 に同梱
# aws-cdk-lib/assertions が利用可能

# Jestインストール（テストランナー）
npm install --save-dev jest @types/jest ts-jest

# jest.config.js
cat > jest.config.js <<EOF
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.test.ts'],
};
EOF
```

#### Python

```bash
# CDK プロジェクト作成
cdk init app --language python
cd my-cdk-app

# 仮想環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# pytest インストール
pip install pytest
```

### 基本的なテスト（TypeScript）

```typescript
// lib/my-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 Bucket
    const bucket = new s3.Bucket(this, 'MyBucket', {
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Lambda Function
    const fn = new lambda.Function(this, 'MyFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline('exports.handler = async () => { return "Hello"; }'),
      environment: {
        BUCKET_NAME: bucket.bucketName,
      },
    });

    // Lambda に S3 読み取り権限付与
    bucket.grantRead(fn);
  }
}
```

```typescript
// test/my-stack.test.ts
import * as cdk from 'aws-cdk-lib';
import { Template, Match } from 'aws-cdk-lib/assertions';
import { MyStack } from '../lib/my-stack';

describe('MyStack', () => {
  let app: cdk.App;
  let stack: MyStack;
  let template: Template;

  beforeEach(() => {
    app = new cdk.App();
    stack = new MyStack(app, 'TestStack');
    template = Template.fromStack(stack);
  });

  // 1. スナップショットテスト
  test('Snapshot test', () => {
    expect(template.toJSON()).toMatchSnapshot();
  });

  // 2. リソース存在確認
  test('S3 bucket should be created', () => {
    template.resourceCountIs('AWS::S3::Bucket', 1);
  });

  test('Lambda function should be created', () => {
    template.resourceCountIs('AWS::Lambda::Function', 1);
  });

  // 3. リソースプロパティ検証
  test('S3 bucket should have versioning enabled', () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      VersioningConfiguration: {
        Status: 'Enabled',
      },
    });
  });

  test('S3 bucket should have encryption', () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      BucketEncryption: {
        ServerSideEncryptionConfiguration: Match.arrayWith([
          Match.objectLike({
            ServerSideEncryptionByDefault: {
              SSEAlgorithm: 'AES256',
            },
          }),
        ]),
      },
    });
  });

  test('Lambda function should have correct runtime', () => {
    template.hasResourceProperties('AWS::Lambda::Function', {
      Runtime: 'nodejs18.x',
      Handler: 'index.handler',
    });
  });

  // 4. 環境変数検証
  test('Lambda should have BUCKET_NAME environment variable', () => {
    template.hasResourceProperties('AWS::Lambda::Function', {
      Environment: {
        Variables: {
          BUCKET_NAME: Match.anyValue(),
        },
      },
    });
  });

  // 5. IAMポリシー検証
  test('Lambda should have S3 read permission', () => {
    template.hasResourceProperties('AWS::IAM::Policy', {
      PolicyDocument: {
        Statement: Match.arrayWith([
          Match.objectLike({
            Action: Match.arrayWith(['s3:GetObject*', 's3:GetBucket*', 's3:List*']),
            Effect: 'Allow',
          }),
        ]),
      },
    });
  });
});
```

### Match パターン

```typescript
import { Match } from 'aws-cdk-lib/assertions';

// 完全一致
template.hasResourceProperties('AWS::S3::Bucket', {
  BucketName: 'my-bucket-name',
});

// 任意の値
template.hasResourceProperties('AWS::Lambda::Function', {
  FunctionName: Match.anyValue(),
});

// 文字列パターン
template.hasResourceProperties('AWS::Lambda::Function', {
  FunctionName: Match.stringLikeRegexp('MyFunction-.*'),
});

// 配列に含まれる
template.hasResourceProperties('AWS::IAM::Policy', {
  PolicyDocument: {
    Statement: Match.arrayWith([
      Match.objectLike({
        Action: 's3:GetObject',
      }),
    ]),
  },
});

// オブジェクトの部分一致
template.hasResourceProperties('AWS::S3::Bucket', {
  Tags: Match.arrayWith([
    Match.objectLike({
      Key: 'Environment',
      Value: 'Production',
    }),
  ]),
});

// 存在しない（否定）
template.hasResourceProperties('AWS::S3::Bucket', {
  PublicAccessBlockConfiguration: Match.objectLike({
    BlockPublicAcls: true,
    BlockPublicPolicy: true,
    IgnorePublicAcls: true,
    RestrictPublicBuckets: true,
  }),
});

// 数値範囲
template.hasResourceProperties('AWS::Lambda::Function', {
  Timeout: Match.anyValue(),  // 任意の数値
});
```

### アウトプット検証

```typescript
// lib/my-stack.ts（Outputs追加）
export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'MyBucket');

    new cdk.CfnOutput(this, 'BucketName', {
      value: bucket.bucketName,
      description: 'The name of the S3 bucket',
      exportName: 'MyBucketName',
    });
  }
}

// test/my-stack.test.ts
test('Stack should have BucketName output', () => {
  template.hasOutput('BucketName', {
    Description: 'The name of the S3 bucket',
    Export: {
      Name: 'MyBucketName',
    },
  });
});
```

### Python でのテスト

```python
# app.py
import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_lambda as lambda_

class MyStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 Bucket
        bucket = s3.Bucket(
            self, "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # Lambda Function
        fn = lambda_.Function(
            self, "MyFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=lambda_.Code.from_inline("def handler(event, context): return 'Hello'"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
            },
        )

        bucket.grant_read(fn)
```

```python
# tests/test_my_stack.py
import aws_cdk as cdk
from aws_cdk.assertions import Template, Match
from app import MyStack

def test_s3_bucket_created():
    app = cdk.App()
    stack = MyStack(app, "TestStack")
    template = Template.from_stack(stack)

    # リソース数確認
    template.resource_count_is("AWS::S3::Bucket", 1)

def test_s3_bucket_has_versioning():
    app = cdk.App()
    stack = MyStack(app, "TestStack")
    template = Template.from_stack(stack)

    # プロパティ検証
    template.has_resource_properties("AWS::S3::Bucket", {
        "VersioningConfiguration": {
            "Status": "Enabled"
        }
    })

def test_lambda_has_environment_variable():
    app = cdk.App()
    stack = MyStack(app, "TestStack")
    template = Template.from_stack(stack)

    template.has_resource_properties("AWS::Lambda::Function", {
        "Environment": {
            "Variables": {
                "BUCKET_NAME": Match.any_value()
            }
        }
    })

def test_snapshot():
    app = cdk.App()
    stack = MyStack(app, "TestStack")
    template = Template.from_stack(stack)

    # スナップショットテスト（pytest-snapshot使用）
    assert template.to_json() == snapshot
```

### CI/CD パイプライン統合

#### GitHub Actions

```yaml
# .github/workflows/cdk-test.yml
name: CDK Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: CDK Synth
        run: npx cdk synth

      - name: CDK Diff (if PR)
        if: github.event_name == 'pull_request'
        run: |
          npx cdk diff --no-fail || true
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: ap-northeast-1
```

#### AWS CodeBuild

```yaml
# buildspec.yml
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 18
    commands:
      - npm install -g aws-cdk
      - npm ci

  pre_build:
    commands:
      - echo "Running tests..."
      - npm test

  build:
    commands:
      - echo "Synthesizing CDK..."
      - cdk synth

  post_build:
    commands:
      - echo "Build completed"

artifacts:
  files:
    - cdk.out/**/*

cache:
  paths:
    - node_modules/**/*
```

### 高度なテストパターン

#### セキュリティチェック

```typescript
// test/security.test.ts
import { Template, Match } from 'aws-cdk-lib/assertions';

test('S3 bucket should block public access', () => {
  template.hasResourceProperties('AWS::S3::Bucket', {
    PublicAccessBlockConfiguration: {
      BlockPublicAcls: true,
      BlockPublicPolicy: true,
      IgnorePublicAcls: true,
      RestrictPublicBuckets: true,
    },
  });
});

test('Lambda function should not have admin permissions', () => {
  const policies = template.findResources('AWS::IAM::Policy');

  Object.values(policies).forEach((policy: any) => {
    const statements = policy.Properties.PolicyDocument.Statement;
    statements.forEach((statement: any) => {
      expect(statement.Action).not.toContain('*');
      expect(statement.Resource).not.toEqual('*');
    });
  });
});
```

#### カスタムアサーション

```typescript
// test/helpers/custom-assertions.ts
import { Template } from 'aws-cdk-lib/assertions';

export function assertHasEncryption(template: Template, resourceType: string) {
  const resources = template.findResources(resourceType);

  Object.keys(resources).forEach(logicalId => {
    const resource = resources[logicalId];

    if (resourceType === 'AWS::S3::Bucket') {
      expect(resource.Properties.BucketEncryption).toBeDefined();
    } else if (resourceType === 'AWS::RDS::DBInstance') {
      expect(resource.Properties.StorageEncrypted).toBe(true);
    }
  });
}

// 使用例
test('All S3 buckets should be encrypted', () => {
  assertHasEncryption(template, 'AWS::S3::Bucket');
});
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **詳細設計（インフラ）** | IaC設計検証 | CDKスタック設計の妥当性確認 |
| **実装（インフラ）** | TDD開発 | テスト駆動でIaC実装 |
| **テスト（インフラ）** | リグレッションテスト | スナップショットテストで変更検出 |
| **CI/CD構築** | 自動テスト | パイプラインでのIaC品質保証 |

## メリット

- **AWS公式**: CDK公式テストライブラリ、信頼性高い
- **無料**: オープンソース、ライセンス費用不要
- **型安全**: TypeScript/Python等の型システム活用
- **細粒度テスト**: リソース単位での詳細検証
- **スナップショット**: 意図しない変更の検出
- **CI/CD統合容易**: Jest/pytest等の標準ツールと統合
- **ドキュメント充実**: AWS公式ドキュメント完備

## デメリット

- **CDK専用**: CloudFormation、Terraformには非対応
- **実環境テスト不可**: テンプレート検証のみ、実デプロイテストは別途必要
- **学習曲線**: CDK、CloudFormation、テストフレームワークの知識が必要
- **スナップショット管理**: スナップショットファイルのメンテナンスが必要
- **実行時間**: 大規模スタックではテスト実行時間が長い

## 類似ツールとの比較

| ツール | 対象IaC | 特徴 | 適用場面 |
|--------|---------|------|----------|
| **CDK Assertions** | AWS CDK | AWS公式、型安全 | CDK開発 |
| **cfn-lint** | CloudFormation | ベストプラクティスチェック | CloudFormation全般 |
| **Checkov** | Terraform, CFN, ARM | セキュリティ重視 | マルチIaC |
| **terraform-compliance** | Terraform | BDD形式テスト | Terraform開発 |

## ベストプラクティス

### 1. テストの階層化

```typescript
// ユニットテスト（リソース単位）
describe('S3 Bucket', () => {
  test('should be created', () => {
    template.resourceCountIs('AWS::S3::Bucket', 1);
  });

  test('should have versioning', () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      VersioningConfiguration: { Status: 'Enabled' },
    });
  });
});

// 統合テスト（スタック全体）
describe('Integration', () => {
  test('Lambda should have access to S3', () => {
    template.hasResourceProperties('AWS::IAM::Policy', {
      PolicyDocument: Match.objectLike({
        Statement: Match.arrayWith([
          Match.objectLike({
            Action: Match.arrayWith(['s3:GetObject*']),
          }),
        ]),
      }),
    });
  });
});

// スナップショットテスト
test('Full stack snapshot', () => {
  expect(template.toJSON()).toMatchSnapshot();
});
```

### 2. セキュリティテストの自動化

```typescript
// test/security-standards.test.ts
describe('Security Standards', () => {
  test('All S3 buckets must block public access', () => {
    const buckets = template.findResources('AWS::S3::Bucket');

    Object.keys(buckets).forEach(logicalId => {
      template.hasResourceProperties('AWS::S3::Bucket', {
        PublicAccessBlockConfiguration: {
          BlockPublicAcls: true,
          BlockPublicPolicy: true,
          IgnorePublicAcls: true,
          RestrictPublicBuckets: true,
        },
      });
    });
  });

  test('All Lambda functions must have timeout < 300s', () => {
    const functions = template.findResources('AWS::Lambda::Function');

    Object.values(functions).forEach((fn: any) => {
      const timeout = fn.Properties.Timeout || 3;
      expect(timeout).toBeLessThanOrEqual(300);
    });
  });
});
```

### 3. 環境別テスト

```typescript
// test/environment.test.ts
describe.each(['dev', 'staging', 'prod'])('Environment: %s', (env) => {
  let template: Template;

  beforeEach(() => {
    const app = new cdk.App();
    const stack = new MyStack(app, 'TestStack', {
      env: { account: '123456789012', region: 'ap-northeast-1' },
      environment: env,
    });
    template = Template.fromStack(stack);
  });

  test(`should have correct tags for ${env}`, () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      Tags: Match.arrayWith([
        { Key: 'Environment', Value: env },
      ]),
    });
  });
});
```

## 公式リソース

- **公式ドキュメント**: https://docs.aws.amazon.com/cdk/v2/guide/testing.html
- **API リファレンス**: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.assertions-readme.html
- **GitHub**: https://github.com/aws/aws-cdk
- **Workshop**: https://cdkworkshop.com/
- **Examples**: https://github.com/aws-samples/aws-cdk-examples

## まとめ

AWS CDK Assertionsは、AWS CDKで作成したIaCをテストするための公式テストライブラリです。スナップショットテスト、細粒度アサーション、テンプレート検証により、CDKスタックの品質を保証します。型安全なテストコードで、リソース存在確認からセキュリティチェックまで幅広いテストが可能です。無料で利用でき、CI/CD統合も容易なため、CDK開発において必須のツールとして広く採用されています。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS CDK v2.0+

