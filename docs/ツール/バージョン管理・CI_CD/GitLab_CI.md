# GitLab CI/CD

## 概要

GitLab CI/CDは、GitLab統合のCI/CD自動化プラットフォームです。.gitlab-ci.yml、パイプライン、ジョブ、Runnerにより、ビルド、テスト、デプロイを自動化します。GitLabリポジトリネイティブ、Docker統合、Kubernetes統合、Auto DevOpsで、ソースコード管理とCI/CDをシームレスに統合します。

## 主な機能

### 1. パイプライン
- **ステージ**: build、test、deploy
- **ジョブ**: 並列実行
- **パイプライン変数**: 環境変数
- **条件分岐**: rules、only/except

### 2. Runner
- **Shared Runner**: GitLab提供
- **Specific Runner**: プロジェクト専用
- **Docker Executor**: Dockerコンテナ
- **Kubernetes Executor**: K8sポッド

### 3. Artifacts
- **ビルド成果物**: アーティファクト管理
- **依存関係**: ジョブ間依存
- **キャッシュ**: 依存関係キャッシュ

### 4. 環境
- **環境管理**: dev、staging、production
- **デプロイメント**: 環境別デプロイ
- **ロールバック**: 環境ロールバック

## 利用方法

### .gitlab-ci.yml（基本）

```yaml
stages:
  - build
  - test
  - deploy

build-job:
  stage: build
  script:
    - echo "Building the app..."
    - mvn clean package
  artifacts:
    paths:
      - target/*.jar
    expire_in: 1 hour

test-job:
  stage: test
  script:
    - echo "Running tests..."
    - mvn test
  dependencies:
    - build-job

deploy-job:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - ./deploy.sh
  only:
    - main
```

### Docker統合

```yaml
image: maven:3.8.6-openjdk-11

stages:
  - build
  - test

build:
  stage: build
  script:
    - mvn clean package
  artifacts:
    paths:
      - target/*.jar

test:
  stage: test
  script:
    - mvn test
```

### Docker Build

```yaml
build-docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker tag myapp:$CI_COMMIT_SHA myapp:latest
    - docker push myapp:latest
  only:
    - main
```

### 変数・環境

```yaml
variables:
  APP_VERSION: "1.0.0"
  DEPLOY_ENV: "production"

deploy:
  stage: deploy
  script:
    - echo "Deploying version $APP_VERSION to $DEPLOY_ENV"
    - kubectl set image deployment/myapp myapp=myapp:$CI_COMMIT_SHA
  environment:
    name: production
    url: https://example.com
  only:
    - main
```

### 条件分岐（rules）

```yaml
build:
  stage: build
  script:
    - mvn clean package
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  rules:
    - if: '$CI_COMMIT_TAG'
      when: manual
    - when: never
```

### キャッシュ

```yaml
cache:
  paths:
    - node_modules/
    - .m2/repository/

build:
  stage: build
  script:
    - npm install
    - npm run build
```

### 並列実行

```yaml
test:
  stage: test
  script:
    - npm test
  parallel:
    matrix:
      - NODE_VERSION: ["14", "16", "18"]
        OS: ["ubuntu", "alpine"]
```

### GitLab Runner登録

```bash
# Runner登録
gitlab-runner register \
  --url https://gitlab.com/ \
  --registration-token PROJECT_TOKEN \
  --executor docker \
  --description "My Docker Runner" \
  --docker-image "alpine:latest"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **GitLab Free** | 🟢 無料 | 400 CI/CD minutes/月 |
| **GitLab Premium** | 💰 $19/月 | 10,000 CI/CD minutes/月 |
| **GitLab Ultimate** | 💰 $99/月 | 50,000 CI/CD minutes/月 |
| **Self-Managed** | 🟢 無料 | 無制限（自己ホスト） |

## メリット

1. **統合**: GitLabネイティブ
2. **無料枠**: 400分/月無料
3. **Docker統合**: Dockerネイティブ
4. **Self-Managed**: 自己ホスト可能
5. **Auto DevOps**: 自動CI/CD

## デメリット

1. **分数制限**: 無料枠400分
2. **Runnerスペック**: Shared Runner限定的
3. **複雑性**: 高度機能複雑
4. **学習曲線**: YAML学習必要

## 公式リンク

- **公式サイト**: [https://about.gitlab.com/](https://about.gitlab.com/)
- **ドキュメント**: [https://docs.gitlab.com/ee/ci/](https://docs.gitlab.com/ee/ci/)

## 関連ドキュメント

- [CI/CDツール一覧](../CI_CDツール/)
- [Jenkins](./Jenkins.md)
- [GitHub Actions](./GitHub_Actions.md)

---

**カテゴリ**: CI/CDツール
**対象工程**: 継続的インテグレーション・デプロイ
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
