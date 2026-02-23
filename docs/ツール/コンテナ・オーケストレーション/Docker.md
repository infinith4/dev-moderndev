# Docker

## 概要

Dockerは、アプリケーションをコンテナと呼ばれる軽量で移植可能な環境にパッケージ化するためのプラットフォームです。2013年に登場して以来、コンテナ技術のデファクトスタンダードとなり、「Build once, Run anywhere」を実現します。開発環境と本番環境の差異を解消し、マイクロサービスアーキテクチャの普及に大きく貢献しました。Dockerfileによるインフラのコード化、Docker Composeによる複数コンテナの管理、Docker Hubでのイメージ共有など、包括的なエコシステムを提供します。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Docker Desktop (Personal)** |  無料 | 個人・小規模企業（従業員250名未満、年間収益$10M未満） |
| **Docker Desktop (Pro)** |  $5/user/月 | 商用利用、複数組織、優先サポート |
| **Docker Desktop (Team)** |  $7/user/月 | チーム管理、イメージアクセス管理、SSO |
| **Docker Desktop (Business)** |  $21/user/月 | 組織全体管理、SLA、専用サポート |
| **Docker Hub Free** |  無料 | 無制限パブリックリポジトリ、1プライベートリポジトリ |
| **Docker Hub Pro** |  $5/月 | 無制限プライベートリポジトリ、並列ビルド |

**注意**: Docker Engine（Linux）は無料のオープンソース。Docker Desktopは商用利用で有料（一定規模以上の企業）。

## メリット・デメリット

### メリット
-  **環境の一貫性**: 開発・テスト・本番で同一環境を保証
-  **軽量**: 仮想マシンより高速起動、少ないリソース消費
-  **移植性**: どこでも同じように動作（Linux、Windows、macOS）
-  **分離性**: アプリケーションと依存関係を隔離
-  **バージョン管理**: Dockerイメージをタグでバージョン管理
-  **スケーラビリティ**: 同一イメージから複数コンテナを簡単に起動
-  **豊富なエコシステム**: Docker Hub、公式イメージ、多数のツール
-  **CI/CDとの親和性**: パイプラインに容易に組み込み可能

### デメリット
-  **学習曲線**: コンテナ概念、ネットワーク、ストレージの理解が必要
-  **Windows/macOSのオーバーヘッド**: Linux VM経由で動作、性能低下
-  **データ永続化**: ボリューム管理が複雑になる場合も
-  **セキュリティ**: 設定ミスで脆弱性が発生する可能性
-  **商用ライセンス**: 大企業ではDocker Desktop有料化
-  **GUI制限**: コンテナ内でGUIアプリは動作困難

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | ローカル開発環境の構築、依存関係管理 | Dockerfile、docker-compose.yml |
| **8. インフラ構築** | コンテナベースインフラの構築 | コンテナイメージ、レジストリ |
| **8-1. CI/CD** | ビルド・テスト・デプロイの自動化 | CI/CDパイプライン、イメージ |
| **9. テスト（アプリケーション）** | テスト環境の迅速な構築・破棄 | テストコンテナ、テスト結果 |
| **10. テスト（インフラ）** | インフラテスト、イメージスキャン | セキュリティレポート |
| **11. 導入** | 本番環境へのコンテナデプロイ | 本番イメージ、デプロイ設定 |

## 基本的な利用方法

### 1. インストール

```bash
# Docker Desktop (macOS/Windows)
# https://www.docker.com/products/docker-desktop からダウンロード

# Docker Engine (Linux - Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# ユーザーをdockerグループに追加（sudoなしで実行可能に）
sudo usermod -aG docker $USER

# バージョン確認
docker --version
docker-compose --version

# Docker動作確認
docker run hello-world
```

### 2. 基本コマンド

```bash
# イメージの取得
docker pull nginx:latest

# イメージ一覧
docker images

# コンテナの起動
docker run -d -p 8080:80 --name my-nginx nginx:latest

# 実行中のコンテナ一覧
docker ps

# 全コンテナ一覧（停止中も含む）
docker ps -a

# コンテナの停止
docker stop my-nginx

# コンテナの削除
docker rm my-nginx

# イメージの削除
docker rmi nginx:latest

# コンテナ内でコマンド実行
docker exec -it my-nginx bash

# ログの確認
docker logs my-nginx

# コンテナの詳細情報
docker inspect my-nginx
```

### 3. Dockerfileの作成

```dockerfile
# Dockerfile (Node.jsアプリケーション例)
FROM node:20-alpine

# 作業ディレクトリの設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係のインストール
RUN npm ci --only=production

# アプリケーションコードをコピー
COPY . .

# ポート3000を公開
EXPOSE 3000

# 非rootユーザーで実行
USER node

# アプリケーションの起動
CMD ["node", "server.js"]
```

```bash
# イメージのビルド
docker build -t myapp:1.0 .

# タグ付き実行
docker run -d -p 3000:3000 --name myapp myapp:1.0
```

### 4. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Webアプリケーション
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network

  # データベース
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  # Redis
  redis:
    image: redis:7-alpine
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# ログ確認
docker-compose logs -f

# 再ビルド
docker-compose build

# スケーリング
docker-compose up -d --scale web=3
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: 開発環境の標準化、依存関係の分離

**活用方法**:
- ローカル開発環境の構築
- データベース・キャッシュ等のサービス起動
- マイクロサービスの並行開発

**実装例（開発環境構築）**:

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      # ホットリロード用にソースをマウント
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    command: npm run dev

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    volumes:
      - postgres-dev:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  postgres-dev:
```

```dockerfile
# Dockerfile.dev
FROM node:20

WORKDIR /app

# nodemonをグローバルインストール
RUN npm install -g nodemon

COPY package*.json ./
RUN npm install

# ソースはボリュームマウント

CMD ["npm", "run", "dev"]
```

**マルチステージビルド（最適化）**:
```dockerfile
# Dockerfile (マルチステージビルド)

# ビルドステージ
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 本番ステージ
FROM node:20-alpine

WORKDIR /app

# 本番依存関係のみインストール
COPY package*.json ./
RUN npm ci --only=production

# ビルド成果物をコピー
COPY --from=builder /app/dist ./dist

EXPOSE 3000

USER node

CMD ["node", "dist/server.js"]
```

---

### 8. インフラ構築での活用

**目的**: コンテナベースインフラの構築

**活用方法**:
- コンテナレジストリの構築
- プライベートレジストリの管理
- イメージのタグ戦略

**実装例（Docker Registry）**:
```yaml
# docker-compose.registry.yml
version: '3.8'

services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /data
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
    volumes:
      - registry-data:/data
      - ./auth:/auth

volumes:
  registry-data:
```

```bash
# 認証ファイルの作成
mkdir auth
docker run --rm --entrypoint htpasswd \
  httpd:2 -Bbn myuser mypassword > auth/htpasswd

# レジストリ起動
docker-compose -f docker-compose.registry.yml up -d

# イメージのプッシュ
docker tag myapp:1.0 localhost:5000/myapp:1.0
docker push localhost:5000/myapp:1.0
```

**イメージのタグ戦略**:
```bash
# セマンティックバージョニング
docker build -t myapp:1.2.3 .
docker tag myapp:1.2.3 myapp:1.2
docker tag myapp:1.2.3 myapp:1
docker tag myapp:1.2.3 myapp:latest

# Git commit SHAをタグに
GIT_SHA=$(git rev-parse --short HEAD)
docker build -t myapp:${GIT_SHA} .
docker tag myapp:${GIT_SHA} myapp:latest

# ビルド番号をタグに
docker build -t myapp:build-${BUILD_NUMBER} .
```

---

### 8-1. CI/CDでの活用

**目的**: ビルド・テスト・デプロイの自動化

**活用方法**:
- CI/CDパイプラインでのイメージビルド
- 自動テスト実行
- コンテナレジストリへのプッシュ

**GitHub Actions統合**:
```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

**GitLab CI/CD統合**:
```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - push

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $IMAGE_TAG .
    - docker save $IMAGE_TAG > image.tar
  artifacts:
    paths:
      - image.tar

test:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker load < image.tar
    - docker run --rm $IMAGE_TAG npm test

push:
  stage: push
  image: docker:latest
  services:
    - docker:dind
  only:
    - main
  script:
    - docker load < image.tar
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $IMAGE_TAG
    - docker tag $IMAGE_TAG $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
```

---

### 9. テスト（アプリケーション）での活用

**目的**: テスト環境の迅速な構築

**活用方法**:
- 統合テスト環境の自動構築
- テストコンテナの利用
- E2Eテスト環境

**実装例（テストコンテナ）**:
```yaml
# docker-compose.test.yml
version: '3.8'

services:
  test:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      - NODE_ENV=test
      - DB_HOST=test-db
      - REDIS_HOST=test-redis
    depends_on:
      - test-db
      - test-redis
    command: npm test

  test-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    tmpfs:
      - /var/lib/postgresql/data

  test-redis:
    image: redis:7-alpine
    tmpfs:
      - /data
```

```bash
# テストの実行
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# クリーンアップ
docker-compose -f docker-compose.test.yml down -v
```

---

### 10. テスト（インフラ）での活用

**目的**: コンテナイメージのセキュリティスキャン

**活用方法**:
- 脆弱性スキャン
- ベストプラクティスチェック
- イメージサイズ最適化

**実装例（セキュリティスキャン）**:
```bash
# Trivyでイメージスキャン
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myapp:latest

# Dockleでベストプラクティスチェック
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  goodwithtech/dockle myapp:latest

# Snykでイメージスキャン
snyk container test myapp:latest

# Hadolintでdockerfileのリンティング
docker run --rm -i hadolint/hadolint < Dockerfile
```

---

### 11. 導入での活用

**目的**: 本番環境へのコンテナデプロイ

**活用方法**:
- 本番環境でのコンテナ実行
- ヘルスチェック
- ログ管理

**実装例（本番環境設定）**:
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    image: myapp:${VERSION}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    ports:
      - "80:3000"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 公式ドキュメント

- [Docker 公式サイト](https://www.docker.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)

## 学習リソース

### チュートリアル
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Play with Docker](https://labs.play-with-docker.com/) - ブラウザでDocker実習
- [Docker Curriculum](https://docker-curriculum.com/)

### 書籍
- "Docker Deep Dive" by Nigel Poulton
- "Docker: Up & Running" by Sean Kane & Karl Matthias (O'Reilly)
- "The Docker Book" by James Turnbull

### 動画・コース
- [Docker Tutorial for Beginners](https://www.youtube.com/results?search_query=docker+tutorial)
- [Docker Mastery](https://www.udemy.com/course/docker-mastery/)
- [Pluralsight - Docker Path](https://www.pluralsight.com/paths/docker)

### コミュニティ
- [Docker Community](https://www.docker.com/community/)
- [Docker Forums](https://forums.docker.com/)
- [Stack Overflow - Docker](https://stackoverflow.com/questions/tagged/docker)

## 関連リンク

### 関連ツール
- [Docker Compose](https://docs.docker.com/compose/) - 複数コンテナ管理
- [Docker Buildx](https://docs.docker.com/buildx/) - マルチプラットフォームビルド
- [Dive](https://github.com/wagoodman/dive) - イメージレイヤー分析
- [ctop](https://github.com/bcicen/ctop) - コンテナtopツール
- [Portainer](https://www.portainer.io/) - Docker管理GUI

### セキュリティツール
- [Trivy](https://github.com/aquasecurity/trivy) - 脆弱性スキャナー
- [Dockle](https://github.com/goodwithtech/dockle) - ベストプラクティスチェッカー
- [Hadolint](https://github.com/hadolint/hadolint) - Dockerfileリンター
- [Docker Bench Security](https://github.com/docker/docker-bench-security) - セキュリティ監査

### ベストプラクティス
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Production-ready Docker](https://testdriven.io/blog/docker-best-practices/)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

