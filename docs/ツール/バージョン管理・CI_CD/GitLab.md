# GitLab

## 概要

GitLabは、DevOpsプラットフォーム統合型のGitリポジトリ管理システムです。ソースコード管理、GitLab CI/CD、Issue管理、マージリクエスト、コンテナレジストリ、セキュリティスキャン、Kubernetes統合により、開発からデプロイまでの全工程を単一プラットフォームで実現します。セルフホスト可能、エンタープライズ採用で広く使用されています。

## 主な機能

### 1. リポジトリ管理
- **Git リポジトリ**: プライベート・パブリック
- **ブランチ管理**: ブランチ保護
- **マージリクエスト**: コードレビュー
- **コードオーナー**: CODEOWNERS

### 2. GitLab CI/CD
- **パイプライン**: .gitlab-ci.yml
- **Runner**: Shared/Specific Runner
- **環境**: dev、staging、production
- **Auto DevOps**: 自動CI/CD

### 3. Issue管理
- **Issue**: バグ・タスク管理
- **エピック**: 大規模機能
- **マイルストーン**: リリース管理
- **ボード**: カンバンボード

### 4. DevSecOps
- **SAST**: 静的解析
- **DAST**: 動的解析
- **依存関係スキャン**: 脆弱性検出
- **Container Scanning**: コンテナスキャン

## 利用方法

### リポジトリ作成

```bash
# GitLab.comでプロジェクト作成後
git clone https://gitlab.com/username/project.git
cd project

# または既存プロジェクト
git init
git remote add origin https://gitlab.com/username/project.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

### GitLab CI/CD（基本）

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

build-job:
  stage: build
  script:
    - echo "Building the app..."
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

test-job:
  stage: test
  script:
    - echo "Running tests..."
    - npm test
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

### Docker Build

```yaml
# .gitlab-ci.yml
image: docker:latest

services:
  - docker:dind

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

stages:
  - build
  - push

build-docker:
  stage: build
  script:
    - docker build -t $IMAGE_TAG .
    - docker tag $IMAGE_TAG $CI_REGISTRY_IMAGE:latest

push-docker:
  stage: push
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $IMAGE_TAG
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
```

### 環境別デプロイ

```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy

test:
  stage: test
  script:
    - npm test

deploy-staging:
  stage: deploy
  script:
    - echo "Deploying to staging..."
    - ./deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

### マトリックスビルド

```yaml
# .gitlab-ci.yml
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ['14', '16', '18']
        OS: ['ubuntu', 'alpine']
  image: node:${NODE_VERSION}-${OS}
  script:
    - npm install
    - npm test
```

### キャッシュ

```yaml
# .gitlab-ci.yml
variables:
  npm_config_cache: "$CI_PROJECT_DIR/.npm"

cache:
  key:
    files:
      - package-lock.json
  paths:
    - .npm/
    - node_modules/

build:
  script:
    - npm ci
    - npm run build
```

### Kubernetes デプロイ

```yaml
# .gitlab-ci.yml
deploy-k8s:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default
    - kubectl apply -f k8s/deployment.yaml
    - kubectl rollout status deployment/my-app
  only:
    - main
```

### マージリクエストテンプレート

```markdown
<!-- .gitlab/merge_request_templates/Default.md -->
## Description
Please include a summary of the change and which issue is fixed.

Closes #(issue)

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### コンテナレジストリ

```bash
# GitLab Container Registry

# ログイン
docker login registry.gitlab.com

# イメージビルド
docker build -t registry.gitlab.com/username/project/myapp:latest .

# プッシュ
docker push registry.gitlab.com/username/project/myapp:latest

# プル
docker pull registry.gitlab.com/username/project/myapp:latest
```

### セキュリティスキャン

```yaml
# .gitlab-ci.yml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

stages:
  - test
  - security

sast:
  stage: security

dependency_scanning:
  stage: security

container_scanning:
  stage: security
  variables:
    CI_APPLICATION_REPOSITORY: $CI_REGISTRY_IMAGE
    CI_APPLICATION_TAG: $CI_COMMIT_SHORT_SHA
```

### GitLab Runner（セルフホスト）

```bash
# GitLab Runnerインストール（Docker）
docker run -d --name gitlab-runner --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v gitlab-runner-config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest

# Runner登録
docker exec -it gitlab-runner gitlab-runner register \
  --url https://gitlab.com/ \
  --registration-token YOUR_TOKEN \
  --executor docker \
  --docker-image alpine:latest \
  --description "My Docker Runner"
```

### Auto DevOps

```yaml
# .gitlab-ci.yml
# Auto DevOps有効化（プロジェクト設定）
# Settings > CI/CD > Auto DevOps

# カスタマイズ
include:
  - template: Auto-DevOps.gitlab-ci.yml

variables:
  AUTO_DEVOPS_DOMAIN: example.com
  POSTGRES_ENABLED: "true"
  POSTGRES_VERSION: "13"
```

### GitLab API

```bash
# プロジェクト一覧
curl --header "PRIVATE-TOKEN: <your_access_token>" \
  "https://gitlab.com/api/v4/projects"

# Issue作成
curl --request POST \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --data "title=New Issue&description=Description" \
  "https://gitlab.com/api/v4/projects/:id/issues"

# パイプライン実行
curl --request POST \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  "https://gitlab.com/api/v4/projects/:id/pipeline?ref=main"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** | 🟢 無料 | 無制限プライベート、400 CI/CD分/月 |
| **Premium** | 💰 $19/ユーザー/月 | 10,000 CI/CD分/月、高度機能 |
| **Ultimate** | 💰 $99/ユーザー/月 | 50,000 CI/CD分/月、セキュリティ |
| **Self-Managed** | 🟢 無料/💰 | セルフホスト |

## メリット

1. **無料枠**: 無制限プライベート
2. **統合プラットフォーム**: DevOps全工程
3. **セルフホスト**: オンプレ可能
4. **CI/CD**: 強力なCI/CD
5. **セキュリティ**: セキュリティスキャン

## デメリット

1. **複雑性**: 機能多く複雑
2. **パフォーマンス**: GitHub比較で遅い
3. **コミュニティ**: GitHub比較で小規模
4. **UI**: UIやや複雑

## 公式リンク

- **公式サイト**: [https://about.gitlab.com/](https://about.gitlab.com/)
- **ドキュメント**: [https://docs.gitlab.com/](https://docs.gitlab.com/)

## 関連ドキュメント

- [バージョン管理ツール一覧](../バージョン管理ツール/)
- [GitHub](./GitHub.md)
- [Git](./Git.md)

---

**カテゴリ**: バージョン管理ツール
**対象工程**: ソースコード管理・DevOps
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
