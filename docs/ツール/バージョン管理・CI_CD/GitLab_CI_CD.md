# GitLab CI/CD

## 概要

GitLab CI/CDは、GitLabに統合された継続的インテグレーション/継続的デリバリーのプラットフォームです。`.gitlab-ci.yml`ファイルでパイプラインを定義し、ビルド、テスト、デプロイを自動化します。GitLabランナーを使用してジョブを実行し、セルフホスト型とクラウド型の両方に対応しています。DevOpsライフサイクル全体をカバーする包括的な機能を提供します。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Free** |  無料 | 400 CI/CDパイプライン分/月、5GBストレージ、コミュニティサポート |
| **Premium** |  $29/user/月 | 10,000 CI/CDパイプライン分/月、50GBストレージ、高度なCI/CD機能 |
| **Ultimate** |  $99/user/月 | 50,000 CI/CDパイプライン分/月、250GBストレージ、全機能利用可能 |
| **Self-managed (Free)** |  無料 | セルフホスト版、無制限パイプライン（リソース次第） |
| **追加ランナー** |  従量課金 | Linux: $0.008/分、Windows/macOS: 別料金 |

**注意**: セルフホスト版（GitLab CE/EE）では独自ランナーを使用するため、パイプライン実行時間の制限はありません。

## メリット・デメリット

### メリット
-  **オールインワン**: ソースコード管理からデプロイまで統合
-  **強力なパイプライン**: DAG（有向非巡回グラフ）による複雑なワークフロー対応
-  **環境管理**: dev/staging/prod環境を明示的に定義可能
-  **Auto DevOps**: 自動検出によるパイプライン生成
-  **セルフホスト可能**: 完全にオンプレミスで運用可能
-  **並列実行**: ジョブの並列実行、マトリックスビルド対応
-  **アーティファクト管理**: ビルド成果物の保存・共有
-  **Kubernetes統合**: ネイティブなK8s統合、GitOps対応

### デメリット
-  **学習曲線**: 高度な機能が多く初心者には複雑
-  **GitLab依存**: GitLabプラットフォーム専用
-  **リソース消費**: セルフホスト版はサーバーリソースを大量消費
-  **ランナー管理**: セルフホスト環境ではランナーの保守が必要
-  **料金**: プレミアム機能は比較的高額

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | マージリクエスト時の自動ビルド、テスト | パイプライン定義、ビルド結果 |
| **8-1. CI/CD** | 自動ビルド、テスト、デプロイパイプライン構築 | CI/CDパイプライン、デプロイ履歴 |
| **9. テスト（アプリケーション）** | 自動テスト実行、コードカバレッジ | テスト結果、品質レポート |
| **10. テスト（インフラ）** | インフラコードの検証、セキュリティスキャン | インフラテスト結果 |
| **11. 導入** | 本番環境への自動デプロイ、ロールバック | デプロイログ、環境ステータス |

## 基本的な利用方法

### 1. GitLab CI/CDの有効化

GitLabプロジェクトでは、`.gitlab-ci.yml`ファイルを追加するだけでCI/CDが有効になります。

```bash
# プロジェクトのルートディレクトリで
touch .gitlab-ci.yml

# ファイルを編集してコミット
git add .gitlab-ci.yml
git commit -m "Add GitLab CI/CD configuration"
git push
```

### 2. 基本的なパイプライン例

```yaml
# .gitlab-ci.yml
# パイプラインのステージ定義
stages:
  - build
  - test
  - deploy

# 変数定義
variables:
  NODE_VERSION: "20"
  DOCKER_IMAGE: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"

# ビルドジョブ
build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 day
  only:
    - main
    - develop

# テストジョブ
test:unit:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Coverage: \d+\.\d+/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:lint:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run lint

# デプロイジョブ
deploy:production:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying to production..."
    - ./deploy.sh production
  environment:
    name: production
    url: https://app.example.com
  only:
    - main
  when: manual  # 手動承認が必要
```

### 3. GitLabランナーのセットアップ（セルフホスト）

```bash
# Linux (Ubuntu/Debian)
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner

# ランナーの登録
sudo gitlab-runner register

# 入力事項:
# - GitLab URL: https://gitlab.com/ (または自社のGitLab URL)
# - Registration token: プロジェクト Settings → CI/CD → Runners
# - Description: my-runner
# - Tags: docker,linux
# - Executor: docker
# - Default image: alpine:latest

# ランナーの起動
sudo gitlab-runner start

# ステータス確認
sudo gitlab-runner status
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: コード品質の維持、マージリクエストの自動検証

**活用方法**:
- マージリクエストパイプライン
- コードフォーマットチェック
- 静的解析
- 依存関係の脆弱性スキャン

**実装例（マージリクエスト検証）**:
```yaml
# .gitlab-ci.yml
stages:
  - quality
  - security

# マージリクエストのみで実行
.mr-rules:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

code-quality:
  extends: .mr-rules
  stage: quality
  image: python:3.11
  before_script:
    - pip install black flake8 mypy
  script:
    - black --check .
    - flake8 . --max-line-length=88
    - mypy . --strict
  allow_failure: false

security-scan:
  extends: .mr-rules
  stage: security
  image: python:3.11
  script:
    - pip install safety bandit
    - safety check --json
    - bandit -r . -f json -o bandit-report.json
  artifacts:
    reports:
      sast: bandit-report.json

dependency-scanning:
  stage: security
  include:
    - template: Security/Dependency-Scanning.gitlab-ci.yml
```

---

### 8-1. CI/CDでの活用

**目的**: エンド・ツー・エンドの自動化パイプライン構築

**活用方法**:
- DAG（有向非巡回グラフ）パイプライン
- 動的子パイプライン
- 環境別デプロイ戦略
- アーティファクト管理

**実装例（DAGパイプライン）**:
```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - package
  - deploy

variables:
  DOCKER_REGISTRY: registry.gitlab.com/$CI_PROJECT_PATH

# ビルドジョブ（並列実行）
build:frontend:
  stage: build
  image: node:20
  script:
    - cd frontend
    - npm ci
    - npm run build
  artifacts:
    paths:
      - frontend/dist/

build:backend:
  stage: build
  image: maven:3.9-openjdk-21
  script:
    - cd backend
    - mvn clean package
  artifacts:
    paths:
      - backend/target/*.jar

# テストジョブ（並列実行、ビルドに依存）
test:frontend:
  stage: test
  needs: ["build:frontend"]
  image: node:20
  script:
    - cd frontend
    - npm ci
    - npm test

test:backend:
  stage: test
  needs: ["build:backend"]
  image: maven:3.9-openjdk-21
  script:
    - cd backend
    - mvn test

# E2Eテスト（両方のビルドに依存）
test:e2e:
  stage: test
  needs: ["build:frontend", "build:backend"]
  image: cypress/base:20
  services:
    - name: selenium/standalone-chrome:latest
  script:
    - npm run test:e2e

# パッケージング（テスト成功後）
package:docker:
  stage: package
  needs: ["test:frontend", "test:backend"]
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_REGISTRY:$CI_COMMIT_SHORT_SHA .
    - docker push $DOCKER_REGISTRY:$CI_COMMIT_SHORT_SHA

# デプロイ（環境別）
deploy:staging:
  stage: deploy
  needs: ["package:docker"]
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop:staging
  script:
    - kubectl set image deployment/myapp myapp=$DOCKER_REGISTRY:$CI_COMMIT_SHORT_SHA
  only:
    - develop

deploy:production:
  stage: deploy
  needs: ["package:docker"]
  environment:
    name: production
    url: https://app.example.com
  script:
    - kubectl set image deployment/myapp myapp=$DOCKER_REGISTRY:$CI_COMMIT_SHORT_SHA
  only:
    - main
  when: manual

# 環境停止ジョブ
stop:staging:
  stage: deploy
  environment:
    name: staging
    action: stop
  script:
    - kubectl delete deployment myapp
  when: manual
```

---

### 9. テスト（アプリケーション）での活用

**目的**: 包括的なテストの自動実行、品質メトリクスの収集

**活用方法**:
- マトリックステスト（複数バージョン/環境）
- カバレッジレポート統合
- パフォーマンステスト
- アクセシビリティテスト

**実装例（マトリックステスト）**:
```yaml
# .gitlab-ci.yml
.test-template:
  stage: test
  script:
    - npm ci
    - npm test
  coverage: '/Statements\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

# マトリックスジョブ（並列実行）
test:matrix:
  extends: .test-template
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "21"]
        OS: ["ubuntu-latest", "alpine"]
  image: node:${NODE_VERSION}-${OS}

# パフォーマンステスト
test:performance:
  stage: test
  image: grafana/k6:latest
  script:
    - k6 run --out json=performance.json performance-tests.js
  artifacts:
    reports:
      performance: performance.json

# アクセシビリティテスト
test:accessibility:
  stage: test
  image: cypress/browsers:latest
  script:
    - npm ci
    - npm run test:a11y
  artifacts:
    reports:
      accessibility: a11y-report.json
```

---

### 10. テスト（インフラ）での活用

**目的**: Infrastructure as Codeの検証、セキュリティスキャン

**活用方法**:
- Terraformの検証とplan
- コンテナイメージのスキャン
- インフラセキュリティチェック
- コンプライアンステスト

**実装例（インフラテスト）**:
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - scan
  - deploy

# Terraformバリデーション
terraform:validate:
  stage: validate
  image: hashicorp/terraform:1.6
  before_script:
    - cd terraform/
    - terraform init
  script:
    - terraform fmt -check -recursive
    - terraform validate
  artifacts:
    paths:
      - terraform/.terraform/

# Terraformプラン
terraform:plan:
  stage: validate
  image: hashicorp/terraform:1.6
  needs: ["terraform:validate"]
  script:
    - cd terraform/
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - terraform/tfplan

# インフラセキュリティスキャン
security:terraform:
  stage: scan
  image: bridgecrew/checkov:latest
  script:
    - checkov -d terraform/ --framework terraform --output json --output-file checkov-report.json
  artifacts:
    reports:
      sast: checkov-report.json
  allow_failure: true

# コンテナイメージスキャン
security:container:
  stage: scan
  image: aquasec/trivy:latest
  services:
    - docker:dind
  script:
    - trivy image --format json --output trivy-report.json $DOCKER_REGISTRY:$CI_COMMIT_SHORT_SHA
  artifacts:
    reports:
      container_scanning: trivy-report.json

# Kubernetesマニフェスト検証
kubernetes:validate:
  stage: validate
  image: alpine/k8s:1.28.0
  script:
    - kubectl apply --dry-run=client -f k8s/
    - kubectl apply --dry-run=server -f k8s/
```

---

### 11. 導入での活用

**目的**: 本番環境への安全で信頼性の高いデプロイ

**活用方法**:
- ブルー/グリーンデプロイメント
- カナリアリリース
- 承認ゲート
- 自動ロールバック
- リリース追跡

**実装例（カナリアデプロイメント）**:
```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy:canary
  - deploy:production
  - rollback

variables:
  KUBE_NAMESPACE: production

# ビルドステージ
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# カナリアデプロイ（10%のトラフィック）
deploy:canary:
  stage: deploy:canary
  image: alpine/k8s:1.28.0
  environment:
    name: production/canary
    url: https://app.example.com
  script:
    - kubectl set image deployment/myapp-canary myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - kubectl scale deployment/myapp-canary --replicas=2
    - kubectl scale deployment/myapp-stable --replicas=18
  only:
    - main

# ヘルスチェック
healthcheck:canary:
  stage: deploy:canary
  needs: ["deploy:canary"]
  script:
    - sleep 60
    - |
      for i in {1..10}; do
        curl -f https://app.example.com/health || exit 1
        sleep 10
      done
    - echo "Canary health check passed"

# 本番デプロイ（100%のトラフィック）
deploy:production:
  stage: deploy:production
  needs: ["healthcheck:canary"]
  image: alpine/k8s:1.28.0
  environment:
    name: production
    url: https://app.example.com
    on_stop: rollback:production
  script:
    - kubectl set image deployment/myapp-stable myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - kubectl scale deployment/myapp-stable --replicas=20
    - kubectl scale deployment/myapp-canary --replicas=0
  only:
    - main
  when: manual  # 手動承認

# ロールバック
rollback:production:
  stage: rollback
  image: alpine/k8s:1.28.0
  environment:
    name: production
    action: stop
  script:
    - |
      PREVIOUS_IMAGE=$(kubectl get deployment/myapp-stable -o jsonpath='{.spec.template.spec.containers[0].image}' --previous-revision)
      kubectl set image deployment/myapp-stable myapp=$PREVIOUS_IMAGE
      kubectl scale deployment/myapp-canary --replicas=0
  when: manual
  only:
    - main

# リリースノート作成
release:
  stage: deploy:production
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  needs: ["deploy:production"]
  script:
    - echo "Creating release"
  release:
    tag_name: $CI_COMMIT_TAG
    description: './CHANGELOG.md'
  only:
    - tags
```

## 公式ドキュメント

- [GitLab CI/CD 公式サイト](https://about.gitlab.com/features/continuous-integration/)
- [GitLab CI/CD ドキュメント](https://docs.gitlab.com/ee/ci/)
- [.gitlab-ci.yml リファレンス](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab Runner](https://docs.gitlab.com/runner/)
- [GitLab CI/CD Examples](https://docs.gitlab.com/ee/ci/examples/)
- [GitLab CI/CD Templates](https://gitlab.com/gitlab-org/gitlab/-/tree/master/lib/gitlab/ci/templates)

## 学習リソース

### チュートリアル
- [GitLab CI/CD Quickstart](https://docs.gitlab.com/ee/ci/quick_start/)
- [GitLab CI/CD Pipeline Configuration](https://docs.gitlab.com/ee/ci/pipelines/)
- [GitLab Learn](https://about.gitlab.com/learn/) - 公式学習リソース

### 書籍・コース
- "GitLab CI/CD Quick Start Guide" by Jonathon Johnson
- "Mastering GitLab 12" by Joost Evertse
- LinkedIn Learning - GitLab CI/CD
- Udemy - GitLab CI: Pipelines, CI/CD and DevOps for Beginners

### 動画
- [GitLab CI/CD Tutorial for Beginners](https://www.youtube.com/results?search_query=gitlab+ci+cd+tutorial)
- [GitLab Official YouTube Channel](https://www.youtube.com/@Gitlab)
- [GitLab Commit Conference Sessions](https://about.gitlab.com/events/commit/)

### コミュニティ
- [GitLab Forum](https://forum.gitlab.com/)
- [GitLab Discord](https://discord.gg/gitlab)
- [r/gitlab (Reddit)](https://www.reddit.com/r/gitlab/)
- [Stack Overflow - GitLab CI](https://stackoverflow.com/questions/tagged/gitlab-ci)

## 関連リンク

### 関連ツール
- [GitLab Runner](https://docs.gitlab.com/runner/) - CI/CDジョブ実行エージェント
- [Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/) - 自動パイプライン生成
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/) - Dockerイメージレジストリ
- [GitLab Package Registry](https://docs.gitlab.com/ee/user/packages/) - アーティファクト管理
- [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/) - 静的サイトホスティング

### CI/CDテンプレート
- [CI/CD Templates](https://gitlab.com/gitlab-org/gitlab/-/tree/master/lib/gitlab/ci/templates) - 公式テンプレート集
- [Security Templates](https://docs.gitlab.com/ee/user/application_security/) - セキュリティスキャン用テンプレート
- [Deploy Templates](https://docs.gitlab.com/ee/ci/cloud_deployment/) - クラウドデプロイ用テンプレート

### ベストプラクティス
- [GitLab CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [GitLab Security Best Practices](https://docs.gitlab.com/ee/ci/security/)
- [Awesome GitLab CI](https://github.com/SubhanRaj/awesome-gitlab-ci) - リソース集

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

