# Cloud Foundry

## 概要

**Cloud Foundry**は、オープンソースのPaaS（Platform as a Service）プラットフォームです。アプリケーション中心のデプロイモデル、マルチクラウド対応、ビルドパック機構により、開発者がインフラを意識せずにアプリケーションをデプロイ・スケーリングできる環境を提供します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Cloud Foundry Foundation / Pivotal（VMware） |
| **種別** | PaaSプラットフォーム（オープンソース） |
| **ライセンス** | Apache 2.0 License（オープンソース） |
| **料金** | 🟢 無料（セルフホスト） / 🟡 有料（マネージドサービス） |
| **公式サイト** | https://www.cloudfoundry.org/ |
| **ドキュメント** | https://docs.cloudfoundry.org/ |

## 主な特徴

### 1. アプリケーション中心
- **cf push**: 1コマンドでデプロイ
- **ビルドパック**: 自動言語検出・依存解決
- **マニフェスト**: `manifest.yml`で設定管理
- **ルーティング**: 自動URLマッピング

### 2. マルチクラウド対応
- **AWS**: Pivotal Cloud Foundry（PCF）
- **Azure**: Azure Spring Apps
- **Google Cloud**: GKE上でKubeCF
- **オンプレミス**: BOSH deployments

### 3. サービスマーケットプレイス
- **データベース**: MySQL、PostgreSQL、MongoDB
- **キャッシュ**: Redis、Memcached
- **メッセージング**: RabbitMQ、Kafka
- **バインディング**: 環境変数自動注入

### 4. スケーリング・自己修復
- **水平スケーリング**: インスタンス数増減
- **垂直スケーリング**: メモリ・ディスク調整
- **ヘルスチェック**: 自動再起動
- **ゼロダウンタイム**: ローリングデプロイ

## 使い方

### セットアップ（CF CLI）

```bash
# Cloud Foundry CLI インストール（Mac）
brew install cloudfoundry/tap/cf-cli

# または、Linux/Windows公式インストーラー
# https://github.com/cloudfoundry/cli/releases

# バージョン確認
cf version

# ログイン
cf login -a https://api.run.pivotal.io
# Email: your-email@example.com
# Password: your-password
# Org: your-org
# Space: development

# 接続先確認
cf target
```

### アプリケーションデプロイ

```bash
# Node.js アプリ例
# package.json
{
  "name": "myapp",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}

# index.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello from Cloud Foundry!');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

# デプロイ
cf push myapp
```

### マニフェストファイル

```yaml
# manifest.yml
applications:
- name: myapp
  memory: 256M
  instances: 2
  buildpacks:
    - nodejs_buildpack
  command: npm start
  env:
    NODE_ENV: production
  routes:
    - route: myapp.cfapps.io
  services:
    - myapp-db
    - myapp-redis
```

```bash
# マニフェストを使ってデプロイ
cf push
```

### ビルドパック

```bash
# 利用可能なビルドパック確認
cf buildpacks

# カスタムビルドパック指定
cf push myapp -b https://github.com/cloudfoundry/nodejs-buildpack.git

# 複数ビルドパック（manifest.yml）
applications:
- name: myapp
  buildpacks:
    - nodejs_buildpack
    - https://github.com/custom/buildpack.git
```

### サービスバインディング

```bash
# サービス一覧確認
cf marketplace

# サービスインスタンス作成
cf create-service p-mysql 100mb myapp-db

# サービスバインディング
cf bind-service myapp myapp-db

# 環境変数確認（VCAP_SERVICES）
cf env myapp

# アプリ再起動（環境変数反映）
cf restage myapp
```

```javascript
// Node.js でサービス接続
const cfenv = require('cfenv');
const appEnv = cfenv.getAppEnv();

// MySQL接続情報取得
const mysqlCreds = appEnv.getServiceCreds('myapp-db');
const mysql = require('mysql');

const connection = mysql.createConnection({
  host: mysqlCreds.hostname,
  user: mysqlCreds.username,
  password: mysqlCreds.password,
  database: mysqlCreds.name
});
```

### スケーリング

```bash
# 水平スケーリング（インスタンス数）
cf scale myapp -i 5

# 垂直スケーリング（メモリ）
cf scale myapp -m 512M

# ディスク容量
cf scale myapp -k 1G

# オートスケーリング（App Autoscaler）
cf create-service app-autoscaler standard myapp-autoscaler
cf bind-service myapp myapp-autoscaler
```

### ルーティング

```bash
# ルート一覧
cf routes

# カスタムルート追加
cf map-route myapp cfapps.io --hostname myapp-prod

# ルート削除
cf unmap-route myapp cfapps.io --hostname myapp-staging

# ドメイン追加
cf create-domain my-org example.com
cf map-route myapp example.com --hostname www
```

### ログ・監視

```bash
# リアルタイムログ
cf logs myapp

# 過去ログ
cf logs myapp --recent

# アプリケーション状態
cf app myapp

# イベント履歴
cf events myapp

# メトリクス（プラグイン）
cf install-plugin -r CF-Community "log-cache"
cf tail myapp
```

### ゼロダウンタイムデプロイ

```bash
# Blue-Green デプロイ
# 1. 新バージョンデプロイ（別名）
cf push myapp-green

# 2. ルート切り替え
cf map-route myapp-green cfapps.io --hostname myapp
cf unmap-route myapp-blue cfapps.io --hostname myapp

# 3. 旧バージョン削除
cf delete myapp-blue

# または、cf-plugin-blue-green 使用
cf install-plugin -r CF-Community blue-green-deploy
cf blue-green-deploy myapp
```

### 環境変数

```bash
# 環境変数設定
cf set-env myapp API_KEY abc123
cf set-env myapp DATABASE_URL postgres://...

# 環境変数確認
cf env myapp

# 環境変数削除
cf unset-env myapp API_KEY

# 再起動（環境変数反映）
cf restart myapp
```

### マルチテナンシー

```bash
# 組織（Org）作成
cf create-org my-organization

# スペース（Space）作成
cf create-space development -o my-organization
cf create-space staging -o my-organization
cf create-space production -o my-organization

# ターゲット切り替え
cf target -o my-organization -s development

# ユーザー権限管理
cf set-org-role user@example.com my-organization OrgManager
cf set-space-role user@example.com my-organization development SpaceDeveloper
```

### CI/CD統合

#### Concourse CI

```yaml
# ci/pipeline.yml
resources:
- name: app-repo
  type: git
  source:
    uri: https://github.com/username/myapp.git
    branch: main

- name: cf-prod
  type: cf
  source:
    api: https://api.run.pivotal.io
    username: ((cf-username))
    password: ((cf-password))
    organization: my-org
    space: production

jobs:
- name: test-and-deploy
  plan:
  - get: app-repo
    trigger: true
  - task: run-tests
    file: app-repo/ci/test.yml
  - put: cf-prod
    params:
      manifest: app-repo/manifest.yml
      path: app-repo
```

#### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Foundry

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install CF CLI
        run: |
          wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
          echo "deb https://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
          sudo apt-get update
          sudo apt-get install cf7-cli

      - name: Deploy to Cloud Foundry
        env:
          CF_API: ${{ secrets.CF_API }}
          CF_USERNAME: ${{ secrets.CF_USERNAME }}
          CF_PASSWORD: ${{ secrets.CF_PASSWORD }}
          CF_ORG: ${{ secrets.CF_ORG }}
          CF_SPACE: ${{ secrets.CF_SPACE }}
        run: |
          cf login -a $CF_API -u $CF_USERNAME -p $CF_PASSWORD -o $CF_ORG -s $CF_SPACE
          cf push
```

### Docker対応

```bash
# Dockerイメージからデプロイ
cf push myapp --docker-image myregistry/myapp:latest

# Dockerfileからビルド（diego-docker）
cf push myapp --docker-image myregistry/myapp:$(git rev-parse --short HEAD)
```

```yaml
# manifest.yml
applications:
- name: myapp
  docker:
    image: myregistry/myapp:latest
  instances: 2
  memory: 512M
```

### Java Spring Boot

```yaml
# manifest.yml
applications:
- name: myapp
  memory: 1G
  instances: 2
  path: target/myapp-0.0.1-SNAPSHOT.jar
  buildpacks:
    - java_buildpack
  env:
    JBP_CONFIG_OPEN_JDK_JRE: '{ jre: { version: 17.+ } }'
    SPRING_PROFILES_ACTIVE: cloud
```

```bash
# ビルド・デプロイ
mvn clean package
cf push
```

### セキュリティ

```bash
# セキュリティグループ確認
cf security-groups

# アプリケーション固有のセキュリティグループ
cf create-security-group myapp-sg security-group.json
cf bind-security-group myapp-sg my-org --space production

# security-group.json
[
  {
    "protocol": "tcp",
    "destination": "10.0.0.0/8",
    "ports": "3306"
  }
]
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | 開発環境 | ローカル開発、迅速なデプロイ |
| **テスト** | ステージング環境 | 本番相当環境でのテスト |
| **導入** | 本番デプロイ | ゼロダウンタイムリリース |
| **運用** | スケーリング | オートスケール、負荷対応 |

## メリット

- **開発者フレンドリー**: `cf push`で即デプロイ
- **マルチクラウド**: AWS、Azure、GCP対応
- **ビルドパック**: 言語自動検出・依存解決
- **サービスバインディング**: DB・キャッシュ自動連携
- **スケーラビリティ**: 水平・垂直スケーリング
- **ゼロダウンタイム**: ローリングデプロイ
- **オープンソース**: カスタマイズ可能

## デメリット

- **学習曲線**: PaaS概念、BOSH運用
- **カスタマイズ制約**: インフラレベル制御困難
- **コスト**: マネージドサービスは従量課金
- **ベンダーロックイン**: CF固有機能依存
- **コンテナ比較**: Kubernetesに比べ柔軟性低
- **レガシー**: モダンツール（K8s）への移行トレンド

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Cloud Foundry** | PaaS、ビルドパック、マルチクラウド | 無料/有料 | エンタープライズ、レガシー移行 |
| **Kubernetes** | コンテナオーケストレーション、柔軟性 | 無料/有料 | クラウドネイティブ、マイクロサービス |
| **Heroku** | シンプルPaaS、開発者向け | 無料/有料 | スタートアップ、プロトタイプ |
| **AWS Elastic Beanstalk** | AWS PaaS、マネージド | 無料（EC2課金） | AWS中心 |

## ベストプラクティス

### 1. マニフェストファイルの活用

```yaml
# manifest.yml で環境統一
applications:
- name: myapp
  memory: 512M
  instances: 2
  buildpacks:
    - nodejs_buildpack
```

### 2. 環境変数でシークレット管理

```bash
# 機密情報は環境変数で
cf set-env myapp DATABASE_URL $DATABASE_URL
```

### 3. ゼロダウンタイムデプロイ

```bash
# Blue-Green デプロイ採用
cf blue-green-deploy myapp
```

### 4. オートスケール設定

```yaml
# autoscaling.yml
instance_min_count: 2
instance_max_count: 10
scaling_rules:
- metric_type: cpu
  threshold: 75
```

## 公式リソース

- **公式サイト**: https://www.cloudfoundry.org/
- **ドキュメント**: https://docs.cloudfoundry.org/
- **GitHub**: https://github.com/cloudfoundry
- **コミュニティ**: https://www.cloudfoundry.org/community/
- **Slack**: https://slack.cloudfoundry.org/

## まとめ

Cloud Foundryは、オープンソースのPaaSプラットフォームです。アプリケーション中心のデプロイモデル、ビルドパック機構、マルチクラウド対応により、開発者がインフラを意識せずにアプリケーションをデプロイ・スケーリングできる環境を提供します。エンタープライズグレードの機能により、大規模組織のクラウド移行を支援します。

---

**最終更新**: 2025-12-10
**対象バージョン**: Cloud Foundry v8+
