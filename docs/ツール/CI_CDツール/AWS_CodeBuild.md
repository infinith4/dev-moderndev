# AWS CodeBuild

## 概要

AWS CodeBuildは、Amazon Web Services公式のフルマネージドCI/CDビルドサービスです。ソースコードをコンパイル、テスト実行、デプロイ可能なアーティファクト生成まで自動化し、サーバープロビジョニング不要でスケーラブルなビルド環境を提供します。AWS CodePipeline、GitHub、Bitbucket等と統合し、Docker、Lambda、ECS等へのデプロイをサポートします。

## 主な機能

### 1. ビルド環境
- **マネージドイメージ**: Ubuntu、Amazon Linux、Windows Server
- **カスタムDocker**: ECRからカスタムイメージ
- **コンピューティング**: 1〜72 vCPU、3〜145 GB RAM
- **GPU対応**: 機械学習モデル学習

### 2. ソース統合
- **GitHub**: Webhook自動ビルド
- **Bitbucket**: Pull Request連携
- **AWS CodeCommit**: AWS Git リポジトリ
- **S3**: アーティファクトソース

### 3. ビルド設定
- **buildspec.yml**: ビルド定義ファイル
- **環境変数**: Parameter Store、Secrets Manager統合
- **キャッシュ**: S3、ローカルキャッシュ
- **並列ビルド**: マトリクスビルド

### 4. テスト・レポート
- **テストレポート**: JUnit、Cucumber、TestNG
- **カバレッジ**: コードカバレッジ
- **ログ**: CloudWatch Logs
- **通知**: SNS、EventBridge

### 5. アーティファクト
- **S3保存**: ビルド成果物
- **ECR**: Docker イメージ
- **暗号化**: KMS暗号化
- **バージョン管理**: アーティファクトバージョニング

### 6. セキュリティ
- **IAM**: ロールベースアクセス
- **VPC**: プライベートネットワーク
- **Secrets**: 機密情報管理
- **CodeGuru**: セキュリティスキャン

## 利用方法

### buildspec.yml基本例

```yaml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
  
  build:
    commands:
      - echo Build started on `date`
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG
  
  post_build:
    commands:
      - echo Build completed on `date`
      - docker push $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG

artifacts:
  files:
    - '**/*'
```

### Node.jsプロジェクト

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 18
    commands:
      - npm install
  
  pre_build:
    commands:
      - npm run lint
      - npm run test
  
  build:
    commands:
      - npm run build
  
  post_build:
    commands:
      - aws s3 sync ./dist s3://$BUCKET_NAME --delete

artifacts:
  files:
    - 'dist/**/*'
  
cache:
  paths:
    - 'node_modules/**/*'
```

### Java/Maven プロジェクト

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      java: corretto17
  
  pre_build:
    commands:
      - mvn clean
  
  build:
    commands:
      - mvn package
  
  post_build:
    commands:
      - echo Build completed

artifacts:
  files:
    - target/*.jar

cache:
  paths:
    - '/root/.m2/**/*'
```

### テストレポート

```yaml
version: 0.2

phases:
  build:
    commands:
      - npm test

reports:
  jest_reports:
    files:
      - 'test-results/junit.xml'
    file-format: 'JUNITXML'
  
  coverage_reports:
    files:
      - 'coverage/clover.xml'
    file-format: 'CLOVERXML'
```

### マトリクスビルド

```yaml
version: 0.2

batch:
  build-matrix:
    static:
      ignore-failure: false
    dynamic:
      env:
        variables:
          NODE_VERSION:
            - 16
            - 18
            - 20

phases:
  install:
    runtime-versions:
      nodejs: $NODE_VERSION
  build:
    commands:
      - npm test
```

### プロジェクト作成（AWS CLI）

```bash
# ビルドプロジェクト作成
aws codebuild create-project \
  --name my-build-project \
  --source type=GITHUB,location=https://github.com/user/repo \
  --artifacts type=S3,location=my-bucket \
  --environment type=LINUX_CONTAINER,image=aws/codebuild/standard:7.0,computeType=BUILD_GENERAL1_SMALL \
  --service-role arn:aws:iam::123456789012:role/CodeBuildRole

# ビルド開始
aws codebuild start-build \
  --project-name my-build-project

# ビルド状態確認
aws codebuild batch-get-builds \
  --ids my-build-project:build-id
```

### CodePipeline統合

```yaml
# CodePipeline定義（抜粋）
- Name: Build
  Actions:
    - Name: BuildAction
      ActionTypeId:
        Category: Build
        Owner: AWS
        Provider: CodeBuild
        Version: 1
      Configuration:
        ProjectName: my-build-project
      InputArtifacts:
        - Name: SourceOutput
      OutputArtifacts:
        - Name: BuildOutput
```

### 環境変数・Secrets

```yaml
version: 0.2

env:
  variables:
    ENV: production
  parameter-store:
    DB_PASSWORD: /myapp/db/password
  secrets-manager:
    API_KEY: prod/api:key

phases:
  build:
    commands:
      - echo "Environment: $ENV"
      - echo "DB Password: $DB_PASSWORD"
      - echo "API Key: $API_KEY"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Linux** | 💰 $0.005/ビルド分 | general1.small (3GB RAM) |
| **Linux** | 💰 $0.01/ビルド分 | general1.medium (7GB RAM) |
| **Linux** | 💰 $0.02/ビルド分 | general1.large (15GB RAM) |
| **Windows** | 💰 $0.02/ビルド分 | general1.medium (7GB RAM) |
| **無料枠** | 🟢 100分/月 | general1.small 無料枠 |

## メリット

### ✅ 主な利点

1. **フルマネージド**: サーバー管理不要
2. **スケーラブル**: 自動スケーリング
3. **従量課金**: ビルド時間のみ課金
4. **AWS統合**: CodePipeline、ECR、S3連携
5. **カスタムDocker**: 柔軟なビルド環境
6. **並列ビルド**: マトリクスビルド対応
7. **セキュリティ**: IAM、VPC、KMS統合
8. **テストレポート**: JUnit、Cucumber対応
9. **キャッシュ**: ビルド高速化
10. **GPU対応**: ML/DLワークロード

## デメリット

### ❌ 制約・課題

1. **AWS専用**: AWSのみ対応
2. **ビルド時間制限**: 最大8時間
3. **学習曲線**: buildspec.yml習得必要
4. **ローカルテスト**: ローカル実行が難しい
5. **UI**: GUIは基本的
6. **コスト**: 頻繁ビルドで高額化
7. **キャッシュ制限**: S3キャッシュは遅い
8. **デバッグ**: ビルドエラーデバッグが煩雑

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **GitHub Actions** | GitHub統合CI/CD | AWS CodeBuildよりGitHub特化 |
| **GitLab CI/CD** | GitLab統合 | AWS CodeBuildと類似 |
| **Jenkins** | オープンソースCI/CD | AWS CodeBuildより柔軟だが管理必要 |
| **CircleCI** | クラウドCI/CD | AWS CodeBuildと類似 |
| **Azure DevOps Pipelines** | Azure CI/CD | AWS CodeBuildと類似（Azure版） |

## 公式リンク

- **公式サイト**: [https://aws.amazon.com/codebuild/](https://aws.amazon.com/codebuild/)
- **ドキュメント**: [https://docs.aws.amazon.com/codebuild/](https://docs.aws.amazon.com/codebuild/)
- **料金**: [https://aws.amazon.com/codebuild/pricing/](https://aws.amazon.com/codebuild/pricing/)
- **buildspec リファレンス**: [https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)

## 関連ドキュメント

- [CI/CDツール一覧](../CI_CDツール/)
- [GitHub Actions](./GitHub_Actions.md)
- [AWS CodePipeline](./AWS_CodePipeline.md)
- [AWS CodeDeploy](../デプロイツール/AWS_CodeDeploy.md)
- [CI/CDベストプラクティス](../../best-practices/cicd.md)

---

**カテゴリ**: CI/CDツール  
**対象工程**: ビルド、テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
