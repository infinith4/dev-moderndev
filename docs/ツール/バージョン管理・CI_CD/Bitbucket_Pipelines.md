# Bitbucket Pipelines

## 概要

**Bitbucket Pipelines**は、Bitbucket統合のCI/CDサービスです。YAMLファイルでビルド定義、Dockerコンテナベースの実行環境、プルリクエスト連携により、コードからデプロイまでのパイプラインを自動化します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Atlassian |
| **種別** | CI/CDサービス（Bitbucket統合） |
| **ライセンス** | プロプライエタリ（SaaS） |
| **料金** | 🟡 従量課金（無料枠: 月50分） |
| **公式サイト** | https://bitbucket.org/product/features/pipelines |
| **ドキュメント** | https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/ |

## 主な特徴

### 1. Bitbucket統合
- リポジトリ直結型CI/CD
- プッシュ・プルリクエスト自動トリガー
- コードレビュー連携
- Jira課題連携

### 2. YAML設定
- `bitbucket-pipelines.yml`で設定
- バージョン管理されたビルド定義
- 再利用可能なステップ
- 条件分岐・並列実行

### 3. Dockerベース実行
- すべてのビルドがDockerコンテナで実行
- カスタムDockerイメージ利用可能
- Dockerサービス（DB、Redis等）
- Docker-in-Docker対応

### 4. デプロイメント
- 環境別デプロイ（Development、Staging、Production）
- 手動承認ゲート
- 変数・シークレット管理
- デプロイトリガー

## 使い方

### セットアップ

```yaml
# bitbucket-pipelines.yml（リポジトリルートに配置）

image: node:18  # デフォルトDockerイメージ

pipelines:
  default:  # すべてのブランチで実行
    - step:
        name: Build and Test
        caches:
          - node
        script:
          - npm install
          - npm test
          - npm run build
        artifacts:
          - dist/**
```

### 基本的なパイプライン

#### Node.js アプリケーション

```yaml
# bitbucket-pipelines.yml

image: node:18

definitions:
  caches:
    npm: $HOME/.npm

pipelines:
  default:
    - step:
        name: Install Dependencies
        caches:
          - node
          - npm
        script:
          - npm ci

    - step:
        name: Lint
        script:
          - npm run lint

    - step:
        name: Test
        script:
          - npm test
        artifacts:
          - coverage/**

    - step:
        name: Build
        script:
          - npm run build
        artifacts:
          - dist/**
```

#### Python アプリケーション

```yaml
# bitbucket-pipelines.yml

image: python:3.11

pipelines:
  default:
    - step:
        name: Test
        caches:
          - pip
        script:
          - pip install -r requirements.txt
          - pip install pytest pytest-cov
          - pytest --cov=src tests/
        artifacts:
          - .coverage
          - htmlcov/**

    - step:
        name: Lint
        script:
          - pip install flake8 black
          - flake8 src/
          - black --check src/
```

#### Java/Maven プロジェクト

```yaml
# bitbucket-pipelines.yml

image: maven:3.8-openjdk-17

pipelines:
  default:
    - step:
        name: Build and Test
        caches:
          - maven
        script:
          - mvn clean install
          - mvn test
        artifacts:
          - target/*.jar
```

### ブランチ別パイプライン

```yaml
# bitbucket-pipelines.yml

image: node:18

pipelines:
  # mainブランチ
  branches:
    main:
      - step:
          name: Build
          script:
            - npm ci
            - npm run build
          artifacts:
            - dist/**

      - step:
          name: Deploy to Production
          deployment: production
          trigger: manual  # 手動承認
          script:
            - pipe: atlassian/aws-s3-deploy:1.1.0
              variables:
                AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
                AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY
                AWS_DEFAULT_REGION: ap-northeast-1
                S3_BUCKET: my-production-bucket
                LOCAL_PATH: dist

    # developブランチ
    develop:
      - step:
          name: Build and Deploy to Staging
          deployment: staging
          script:
            - npm ci
            - npm run build
            - pipe: atlassian/aws-s3-deploy:1.1.0
              variables:
                AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
                AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY
                S3_BUCKET: my-staging-bucket
                LOCAL_PATH: dist

  # プルリクエスト
  pull-requests:
    '**':
      - step:
          name: PR Build and Test
          script:
            - npm ci
            - npm run lint
            - npm test
```

### 並列実行

```yaml
# bitbucket-pipelines.yml

image: node:18

pipelines:
  default:
    - parallel:
        - step:
            name: Lint
            script:
              - npm ci
              - npm run lint

        - step:
            name: Unit Tests
            script:
              - npm ci
              - npm run test:unit

        - step:
            name: Integration Tests
            script:
              - npm ci
              - npm run test:integration

    - step:
        name: Build
        script:
          - npm ci
          - npm run build
```

### Dockerイメージビルド

```yaml
# bitbucket-pipelines.yml

image: atlassian/default-image:3

pipelines:
  default:
    - step:
        name: Build and Push Docker Image
        services:
          - docker
        script:
          # Dockerビルド
          - docker build -t myapp:${BITBUCKET_BUILD_NUMBER} .
          - docker tag myapp:${BITBUCKET_BUILD_NUMBER} myregistry.com/myapp:${BITBUCKET_BUILD_NUMBER}
          - docker tag myapp:${BITBUCKET_BUILD_NUMBER} myregistry.com/myapp:latest

          # Docker Hub / ECR にプッシュ
          - docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
          - docker push myregistry.com/myapp:${BITBUCKET_BUILD_NUMBER}
          - docker push myregistry.com/myapp:latest

definitions:
  services:
    docker:
      memory: 3072  # Docker-in-Docker用メモリ
```

### Pipes（再利用可能なコンポーネント）

```yaml
# bitbucket-pipelines.yml

image: node:18

pipelines:
  default:
    - step:
        name: Build
        script:
          - npm ci
          - npm run build
        artifacts:
          - dist/**

    # AWS S3デプロイ（Pipe使用）
    - step:
        name: Deploy to S3
        script:
          - pipe: atlassian/aws-s3-deploy:1.1.0
            variables:
              AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
              AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY
              AWS_DEFAULT_REGION: ap-northeast-1
              S3_BUCKET: my-website-bucket
              LOCAL_PATH: dist
              ACL: public-read

    # Slack通知（Pipe使用）
    - step:
        name: Notify Slack
        script:
          - pipe: atlassian/slack-notify:2.0.0
            variables:
              WEBHOOK_URL: $SLACK_WEBHOOK_URL
              MESSAGE: "Deployment completed: Build #${BITBUCKET_BUILD_NUMBER}"
```

### データベースサービス

```yaml
# bitbucket-pipelines.yml

image: python:3.11

definitions:
  services:
    postgres:
      image: postgres:13
      environment:
        POSTGRES_DB: testdb
        POSTGRES_USER: testuser
        POSTGRES_PASSWORD: testpass

    redis:
      image: redis:7

pipelines:
  default:
    - step:
        name: Integration Tests
        services:
          - postgres
          - redis
        script:
          - pip install -r requirements.txt
          - export DATABASE_URL=postgresql://testuser:testpass@localhost:5432/testdb
          - export REDIS_URL=redis://localhost:6379
          - pytest tests/integration/
```

### カスタムDockerイメージ

```yaml
# bitbucket-pipelines.yml

pipelines:
  default:
    - step:
        name: Build with Custom Image
        image: mycompany/build-env:1.0  # カスタムイメージ
        script:
          - ./build.sh
          - ./test.sh
```

### 環境変数・シークレット

```yaml
# bitbucket-pipelines.yml

pipelines:
  default:
    - step:
        name: Deploy
        script:
          # リポジトリ設定で定義した変数を使用
          - echo "API Key: $API_KEY"
          - echo "Database: $DATABASE_URL"

          # デプロイスクリプト実行
          - ./deploy.sh

# 変数設定場所:
# Repository settings → Pipelines → Variables
# - API_KEY (Secured: チェック)
# - DATABASE_URL
```

### アーティファクト

```yaml
# bitbucket-pipelines.yml

pipelines:
  default:
    - step:
        name: Build
        script:
          - npm run build
        artifacts:
          - dist/**  # 次のステップで利用可能

    - step:
        name: Test Artifacts
        script:
          - ls -la dist/  # 前ステップのアーティファクトにアクセス
```

### キャッシュ

```yaml
# bitbucket-pipelines.yml

definitions:
  caches:
    npm: $HOME/.npm
    gradle: ~/.gradle

pipelines:
  default:
    - step:
        name: Build
        caches:
          - node  # ビルトインキャッシュ (node_modules)
          - npm   # カスタムキャッシュ
        script:
          - npm ci
          - npm run build
```

### デプロイメント環境

```yaml
# bitbucket-pipelines.yml

pipelines:
  branches:
    main:
      - step:
          name: Deploy to Production
          deployment: production  # 環境: production
          trigger: manual         # 手動承認
          script:
            - ./deploy-prod.sh

    develop:
      - step:
          name: Deploy to Staging
          deployment: staging     # 環境: staging
          script:
            - ./deploy-staging.sh

# デプロイ履歴・ロールバック機能
# Repository → Deployments から確認
```

### スケジュール実行

```yaml
# bitbucket-pipelines.yml

pipelines:
  # 毎日午前2時（UTC）に実行
  custom:
    nightly-build:
      - step:
          name: Nightly Full Test
          script:
            - npm ci
            - npm run test:full
            - npm run test:e2e

# スケジュール設定:
# Repository settings → Pipelines → Schedules
# - Name: Nightly Build
# - Branch: develop
# - Pipeline: nightly-build
# - Cron: 0 2 * * *
```

### マトリックスビルド

```yaml
# bitbucket-pipelines.yml

image: node:18

definitions:
  steps:
    - step: &test-template
        name: Test
        script:
          - npm ci
          - npm test

pipelines:
  default:
    - parallel:
        - step:
            <<: *test-template
            image: node:16
            name: Test Node 16

        - step:
            <<: *test-template
            image: node:18
            name: Test Node 18

        - step:
            <<: *test-template
            image: node:20
            name: Test Node 20
```

### Monorepo対応

```yaml
# bitbucket-pipelines.yml

pipelines:
  default:
    - step:
        name: Build Frontend
        condition:
          changesets:
            includePaths:
              - "packages/frontend/**"
        script:
          - cd packages/frontend
          - npm ci
          - npm run build

    - step:
        name: Build Backend
        condition:
          changesets:
            includePaths:
              - "packages/backend/**"
        script:
          - cd packages/backend
          - npm ci
          - npm run build
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | CI | プッシュ毎の自動ビルド・テスト |
| **テスト** | 自動テスト | プルリクエストでテスト自動実行 |
| **導入** | CD | ブランチ別自動デプロイ |
| **運用** | 定期実行 | スケジュールビルド |

## メリット

- **Bitbucket統合**: リポジトリと一体化、設定簡単
- **YAML設定**: バージョン管理、コードレビュー対象
- **Dockerベース**: 環境の一貫性、再現性
- **無料枠**: 月50分無料（小規模プロジェクト十分）
- **Pipes**: 再利用可能なコンポーネント
- **Jira連携**: 課題との自動連携
- **並列実行**: ビルド時間短縮

## デメリット

- **従量課金**: ビルド時間で課金（大規模プロジェクトは高コスト）
- **実行時間制限**: 最大2時間/ビルド
- **Bitbucket専用**: 他Git ホスティング非対応
- **カスタマイズ制限**: セルフホスト型Jenkins等に比べ柔軟性低
- **デバッグ困難**: ローカル実行不可、トライ&エラー必要

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Bitbucket Pipelines** | Bitbucket統合 | 従量課金 | Bitbucket利用環境 |
| **GitHub Actions** | GitHub統合 | 従量課金 | GitHub利用環境 |
| **GitLab CI** | GitLab統合 | 無料〜有料 | GitLab利用環境 |
| **CircleCI** | 高速、Docker重視 | 無料〜有料 | マルチプラットフォーム |

## ベストプラクティス

### 1. キャッシュ活用

```yaml
definitions:
  caches:
    npm: $HOME/.npm
    composer: ~/.composer

pipelines:
  default:
    - step:
        caches:
          - node
          - npm
        script:
          - npm ci  # node_modules キャッシュ活用
```

### 2. 並列実行でビルド高速化

```yaml
pipelines:
  default:
    - parallel:
        - step:
            name: Lint
            script: npm run lint
        - step:
            name: Test
            script: npm test
        - step:
            name: Build
            script: npm run build
```

### 3. 環境別デプロイ

```yaml
pipelines:
  branches:
    develop:
      - step:
          deployment: staging
          script: ./deploy-staging.sh

    main:
      - step:
          deployment: production
          trigger: manual  # 本番は手動承認
          script: ./deploy-prod.sh
```

### 4. Pipes活用

```yaml
# AWS、Azure、GCP等のPipesを活用
- pipe: atlassian/aws-s3-deploy:1.1.0
- pipe: atlassian/azure-web-apps-deploy:1.0.0
- pipe: microsoft/azure-cli-run:1.0.0
```

### 5. 変数管理

```text
# Repository settings → Pipelines → Variables

- API_KEY (Secured: ✓)
- DATABASE_URL (Secured: ✓)
- SLACK_WEBHOOK_URL
```

## 公式リソース

- **公式サイト**: https://bitbucket.org/product/features/pipelines
- **ドキュメント**: https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/
- **Pipes**: https://bitbucket.org/product/features/pipelines/integrations
- **料金**: https://bitbucket.org/product/pricing
- **サンプル**: https://bitbucket.org/atlassian/bitbucket-pipelines-examples

## まとめ

Bitbucket Pipelinesは、Bitbucket統合のCI/CDサービスです。YAMLファイルでビルド定義、Dockerコンテナベースの実行環境、プルリクエスト連携により、コードからデプロイまでのパイプラインを自動化します。Bitbucketユーザーにとって、追加インフラ不要で即座にCI/CDを開始できる最適なソリューションです。

---

**最終更新**: 2025-12-06
**対象バージョン**: Bitbucket Pipelines 2024+
