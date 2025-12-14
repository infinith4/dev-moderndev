# Bamboo

## 概要

**Bamboo**は、Atlassian社が提供する継続的インテグレーション（CI）・継続的デプロイ（CD）サーバーです。Jira・Bitbucket・Confluenceとのシームレスな統合、強力なビルドパイプライン機能により、エンタープライズ向けの自動化されたソフトウェアデリバリーを実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Atlassian |
| **種別** | CI/CDサーバー |
| **ライセンス** | プロプライエタリ（商用） |
| **料金** | 🟡 有料（サーバー版・Data Center版） |
| **公式サイト** | https://www.atlassian.com/software/bamboo |
| **ドキュメント** | https://confluence.atlassian.com/bamboo/ |

## 主な特徴

### 1. Atlassian製品統合
- **Jira**: ビルド状況を課題に自動反映
- **Bitbucket**: プッシュトリガー、プルリクエスト連携
- **Confluence**: ビルドレポート埋め込み
- **HipChat/Stride**: 通知連携

### 2. ビルドパイプライン
- **Plans**: ビルド定義（複数ステージ）
- **Stages**: 並列実行可能なジョブグループ
- **Jobs**: 個別ビルドタスク
- **Tasks**: ビルドステップ（コンパイル、テスト、デプロイ）

### 3. デプロイメント
- **Deployment Projects**: 環境別デプロイ設定
- **Environments**: 開発、ステージング、本番環境
- **リリース**: バージョン管理されたデプロイ
- **承認ワークフロー**: 手動承認ゲート

### 4. 並列ビルド・スケーラビリティ
- リモートエージェント
- Elastic Bamboo（AWS連携で動的スケール）
- マトリックスビルド（複数環境並列）
- 分散ビルド

## 使い方

### セットアップ

#### インストール（Linux）

```bash
# Java 11インストール
sudo apt update
sudo apt install openjdk-11-jdk

# Bambooダウンロード
wget https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-9.2.0.tar.gz
tar -xzf atlassian-bamboo-9.2.0.tar.gz
cd atlassian-bamboo-9.2.0

# 設定
vi atlassian-bamboo/WEB-INF/classes/bamboo-init.properties
# bamboo.home=/var/atlassian/application-data/bamboo

# 起動
./bin/start-bamboo.sh

# ブラウザでアクセス
# http://localhost:8085

# セットアップウィザード
# - ライセンスキー入力
# - データベース設定（PostgreSQL/MySQL推奨）
# - 管理者アカウント作成
```

#### Docker での起動

```bash
# Docker Compose
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  bamboo:
    image: atlassian/bamboo-server:9.2
    ports:
      - "8085:8085"
      - "54663:54663"  # Remote Agent Port
    environment:
      - JVM_MINIMUM_MEMORY=2048m
      - JVM_MAXIMUM_MEMORY=4096m
      - ATL_JDBC_URL=jdbc:postgresql://db:5432/bamboo
      - ATL_JDBC_USER=bamboo
      - ATL_JDBC_PASSWORD=bamboo_password
      - ATL_DB_TYPE=postgresql
    volumes:
      - bamboo-data:/var/atlassian/application-data/bamboo
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=bamboo
      - POSTGRES_USER=bamboo
      - POSTGRES_PASSWORD=bamboo_password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  bamboo-data:
  postgres-data:
EOF

docker-compose up -d
```

### プロジェクト・プラン作成

```text
# Bamboo Web UI での操作

1. プロジェクト作成
   Create → Create Project
   - Project name: MyWebApp
   - Project key: WEBAPP

2. プラン作成
   Create → Create Plan
   - Plan name: Build and Test
   - Plan key: WEBAPP-BUILD
   - リポジトリ設定（Bitbucket/GitHub/GitLab）

3. ステージ設定
   Default Stage (並列実行可能なジョブ)
   └── Default Job

4. ジョブ設定
   - Source Code Checkout
   - Build Tasks
   - Test Tasks
```

### ビルド設定（Java/Maven）

```yaml
# Bamboo Specs (as Code)
# bamboo-specs/bamboo.yaml
---
version: 2
plan:
  project-key: WEBAPP
  key: BUILD
  name: Build and Test

stages:
  - Build:
      manual: false
      final: false
      jobs:
        - Build:
            key: BUILD
            tasks:
              - checkout:
                  force-clean-build: false
                  description: Checkout Default Repository
              - script:
                  interpreter: SHELL
                  scripts:
                    - |-
                      mvn clean compile
                  description: Maven Compile
              - script:
                  interpreter: SHELL
                  scripts:
                    - |-
                      mvn test
                  description: Run Tests
              - junit:
                  test-results: target/surefire-reports/*.xml
                  description: Parse JUnit Test Results
            artifacts:
              - name: WAR file
                pattern: target/*.war
                shared: true
                required: false

  - Deploy to Staging:
      manual: false
      final: false
      jobs:
        - Deploy:
            key: DEPLOY
            tasks:
              - clean
              - artifact-download:
                  artifacts:
                    - name: WAR file
              - script:
                  interpreter: SHELL
                  scripts:
                    - |-
                      scp target/*.war user@staging-server:/opt/tomcat/webapps/
                  description: Deploy to Staging

triggers:
  - polling:
      period: '180'

branches:
  create: for-pull-request
  delete:
    after-deleted-days: 7
    after-inactive-days: 30

notifications:
  - events:
      - plan-completed
    recipients:
      - emails:
          - team@example.com
```

### Node.js プロジェクト

```yaml
# bamboo.yaml
---
version: 2
plan:
  project-key: WEBAPP
  key: FRONTEND
  name: Frontend Build

stages:
  - Build:
      jobs:
        - Build:
            key: BUILD
            docker:
              image: node:18
              volumes:
                ${bamboo.working.directory}: /opt/bamboo
            tasks:
              - checkout
              - script:
                  scripts:
                    - npm ci
                  description: Install Dependencies
              - script:
                  scripts:
                    - npm run build
                  description: Build
              - script:
                  scripts:
                    - npm test
                  description: Run Tests
            artifacts:
              - name: Build Output
                pattern: dist/**
                shared: true

  - Deploy:
      jobs:
        - Deploy to S3:
            key: S3
            tasks:
              - artifact-download:
                  artifacts:
                    - name: Build Output
              - script:
                  scripts:
                    - aws s3 sync dist/ s3://my-website-bucket/ --delete
                  description: Deploy to S3
```

### Docker ビルド

```yaml
# bamboo.yaml
---
version: 2
plan:
  project-key: WEBAPP
  key: DOCKER
  name: Docker Build and Push

stages:
  - Build:
      jobs:
        - Docker Build:
            key: BUILD
            tasks:
              - checkout
              - script:
                  scripts:
                    - docker build -t myapp:${bamboo.buildNumber} .
                    - docker tag myapp:${bamboo.buildNumber} myregistry.com/myapp:${bamboo.buildNumber}
                    - docker tag myapp:${bamboo.buildNumber} myregistry.com/myapp:latest
                  description: Build Docker Image
              - script:
                  scripts:
                    - docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD myregistry.com
                    - docker push myregistry.com/myapp:${bamboo.buildNumber}
                    - docker push myregistry.com/myapp:latest
                  description: Push Docker Image

variables:
  DOCKER_USERNAME: admin
  DOCKER_PASSWORD: ${bamboo.DOCKER_PASSWORD}  # Bamboo Variables (暗号化)
```

### デプロイメントプロジェクト

```text
# Deployment Project 作成

1. Deploy → Create Deployment Project
   - Name: MyWebApp Deployment
   - Plan: WEBAPP-BUILD

2. 環境設定
   - Development
   - Staging
   - Production

3. 環境別タスク設定（Staging）
   Tasks:
   - Artifact Download
   - SSH Task: Deploy to Server
   - Script: Health Check

4. トリガー設定
   - After successful build plan: WEBAPP-BUILD
   - Manual approval for Production

5. 変数設定（環境別）
   Staging:
   - SERVER_HOST: staging.example.com
   - DB_CONNECTION: jdbc:postgresql://db-staging/webapp

   Production:
   - SERVER_HOST: prod.example.com
   - DB_CONNECTION: jdbc:postgresql://db-prod/webapp
```

### Jira 連携

```yaml
# Jira課題との連携

# コミットメッセージに課題キー含める
git commit -m "WEBAPP-123 ログイン機能の実装"

# Bamboo → Jira 自動連携
# - ビルド状況がJira課題に表示
# - デプロイ状況も追跡
# - リリースノート自動生成

# Jira Issue Collector（Bamboo設定）
Settings → Jira Integration
- Jira URL: https://jira.example.com
- Application Link設定
```

### リモートエージェント

```bash
# リモートエージェントセットアップ

# 1. Bambooサーバーでエージェント認証トークン作成
# Settings → Agents → Remote Agents → Install Remote Agent

# 2. エージェントマシンでインストール
wget https://bamboo.example.com/agentServer/agentInstaller/atlassian-bamboo-agent-installer-9.2.0.jar
java -jar atlassian-bamboo-agent-installer-9.2.0.jar https://bamboo.example.com/agentServer/

# 3. エージェント起動
cd bamboo-agent-home/bin
./bamboo-agent.sh start

# 4. Bambooサーバーで承認
# Settings → Agents → Remote Agents → Approve Agent

# 5. Capability設定（自動検出 or 手動追加）
# - JDK 11
# - Maven 3.8
# - Node.js 18
# - Docker
```

### Elastic Bamboo（AWS連携）

```text
# AWS EC2でオンデマンドエージェント起動

1. Elastic Bamboo有効化
   Settings → Elastic Bamboo
   - AWS Credentials設定
   - AMI選択（Bamboo Agent AMI）
   - Instance Type: t3.medium

2. 設定
   - 最小インスタンス数: 0
   - 最大インスタンス数: 10
   - アイドルシャットダウン: 10分

3. 自動スケール
   - ビルドキューが溜まるとEC2起動
   - ビルド完了後、アイドル時間経過で自動停止
   - コスト最適化
```

### REST API

```python
# bamboo_api.py
import requests
from requests.auth import HTTPBasicAuth

BAMBOO_URL = "https://bamboo.example.com"
USERNAME = "admin"
API_TOKEN = "your-api-token"

auth = HTTPBasicAuth(USERNAME, API_TOKEN)

def get_build_status(plan_key):
    """ビルドステータス取得"""
    url = f"{BAMBOO_URL}/rest/api/latest/result/{plan_key}"
    response = requests.get(url, auth=auth)
    return response.json()

def trigger_build(plan_key):
    """ビルド実行"""
    url = f"{BAMBOO_URL}/rest/api/latest/queue/{plan_key}"
    response = requests.post(url, auth=auth)
    return response.json()

def get_deployment_status(deployment_id):
    """デプロイステータス取得"""
    url = f"{BAMBOO_URL}/rest/api/latest/deploy/environment/{deployment_id}/results"
    response = requests.get(url, auth=auth)
    return response.json()

# 使用例
status = get_build_status("WEBAPP-BUILD")
print(f"Build: {status['results']['result'][0]['buildNumber']}")
print(f"State: {status['results']['result'][0]['state']}")
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | CI（継続的インテグレーション） | コミット毎の自動ビルド・テスト |
| **テスト** | 自動テスト実行 | ユニット・統合テスト自動化 |
| **導入** | CD（継続的デプロイ） | ステージング・本番環境自動デプロイ |
| **運用** | 監視・通知 | ビルド失敗通知、レポート |

## メリット

- **Atlassian統合**: Jira・Bitbucket・Confluenceとシームレス連携
- **強力なパイプライン**: ステージ・ジョブ・タスクの階層構造
- **並列ビルド**: リモートエージェントで高速化
- **Elastic Bamboo**: AWS連携でオンデマンドスケール
- **エンタープライズ向け**: 権限管理、監査ログ
- **Bamboo Specs**: YAML/Javaでビルド定義をコード化
- **デプロイメント**: 環境別デプロイ、承認ワークフロー

## デメリット

- **有料**: オープンソース版なし、ライセンス費用が高額
- **学習曲線**: 設定が複雑、初期セットアップに時間
- **リソース消費**: Java VMで動作、メモリ消費大
- **クラウド版終了**: Bamboo Cloudは2022年に終了、サーバー版のみ
- **コミュニティ小**: Jenkins・GitLab CIに比べユーザーベース小
- **プラグイン少**: Jenkins程の拡張性はない

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Bamboo** | Atlassian統合 | 有料 | Atlassian環境 |
| **Jenkins** | オープンソース、高拡張性 | 無料 | 汎用CI/CD |
| **GitLab CI** | Git統合、YAML定義 | 無料〜有料 | GitLab利用環境 |
| **TeamCity** | JetBrains製、強力IDE統合 | 無料〜有料 | JetBrains環境 |

## ベストプラクティス

### 1. Plan構成

```text
# 階層的なPlan設計

Project: MyWebApp
├── Plan: Build and Test (WEBAPP-BUILD)
│   ├── Stage: Build
│   │   └── Job: Compile & Unit Test
│   ├── Stage: Integration Test
│   │   └── Job: API Tests
│   └── Stage: Package
│       └── Job: Create Artifacts
│
└── Plan: Code Quality (WEBAPP-QUALITY)
    ├── Stage: Static Analysis
    │   ├── Job: SonarQube Scan
    │   └── Job: Dependency Check
    └── Stage: Security Scan
        └── Job: OWASP ZAP
```

### 2. 変数管理

```text
# グローバル変数（Settings → Global Variables）
DOCKER_REGISTRY: myregistry.com
SONAR_URL: https://sonar.example.com

# プラン変数（Plan → Variables）
APP_VERSION: 1.2.0

# 環境変数（Deployment Environment → Variables）
Staging:
  API_ENDPOINT: https://api-staging.example.com
Production:
  API_ENDPOINT: https://api.example.com

# 暗号化変数（Password/Secret）
DB_PASSWORD: ******（暗号化）
```

### 3. アーティファクト管理

```yaml
# ビルドアーティファクトの共有

# Build Job
artifacts:
  - name: Application JAR
    pattern: target/*.jar
    shared: true  # 後続ステージで利用可能

# Deploy Job
tasks:
  - artifact-download:
      artifacts:
        - name: Application JAR
      source-plan: WEBAPP-BUILD
```

### 4. 並列実行

```yaml
# マトリックスビルド（複数環境並列）

stages:
  - Test:
      jobs:
        - Test Java 11:
            key: TEST11
            docker:
              image: openjdk:11
        - Test Java 17:
            key: TEST17
            docker:
              image: openjdk:17
        - Test Java 21:
            key: TEST21
            docker:
              image: openjdk:21
```

## 公式リソース

- **公式サイト**: https://www.atlassian.com/software/bamboo
- **ドキュメント**: https://confluence.atlassian.com/bamboo/
- **Bamboo Specs**: https://docs.atlassian.com/bamboo-specs-docs/
- **API**: https://docs.atlassian.com/bamboo/REST/latest/
- **料金**: https://www.atlassian.com/software/bamboo/pricing

## まとめ

Bambooは、Atlassian社が提供するエンタープライズ向けCI/CDサーバーです。Jira・Bitbucket・Confluenceとのシームレスな統合、強力なビルドパイプライン、Elastic Bambooによる動的スケールにより、Atlassian製品を中心とした開発環境に最適化されています。有料ライセンスが必要ですが、エンタープライズ向けの機能と信頼性を提供します。

---

**最終更新**: 2025-12-06
**対象バージョン**: Bamboo 9.2+
