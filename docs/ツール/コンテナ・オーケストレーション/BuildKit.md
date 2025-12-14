# BuildKit

## 概要

**BuildKit**は、Docker社が開発した次世代のDockerイメージビルドエンジンです。並列ビルド、ビルドキャッシュの最適化、マルチステージビルドの高速化により、従来のDockerビルドを大幅に高速化し、効率的なコンテナイメージ作成を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Docker, Inc. / Moby Project |
| **種別** | コンテナイメージビルドエンジン |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://github.com/moby/buildkit |
| **ドキュメント** | https://docs.docker.com/build/buildkit/ |

## 主な特徴

### 1. 高速ビルド
- **並列ビルド**: 独立したレイヤーを並列実行
- **インクリメンタルビルド**: 変更部分のみ再ビルド
- **効率的なキャッシュ**: 高度なキャッシュアルゴリズム
- **遅延評価**: 不要なレイヤーはスキップ

### 2. 高度なキャッシング
- **ローカルキャッシュ**: ビルド履歴を保存
- **レジストリキャッシュ**: Docker Registryからキャッシュ取得
- **インラインキャッシュ**: イメージにキャッシュメタデータ埋め込み
- **S3/GCSキャッシュ**: クラウドストレージ連携

### 3. 新しいDockerfile機能
- **マウント機能**: `RUN --mount`でビルド時マウント
- **シークレット**: `RUN --mount=type=secret`で安全に機密情報利用
- **SSHフォワーディング**: `RUN --mount=type=ssh`でプライベートリポジトリアクセス
- **ヒアドキュメント**: 複数行コマンドの記述簡素化

### 4. マルチプラットフォームビルド
- **クロスプラットフォーム**: AMD64、ARM64等を同時ビルド
- **QEMU統合**: エミュレーションで異なるアーキテクチャビルド
- **マニフェスト自動生成**: マルチアーキテクチャイメージ

## 使い方

### セットアップ

#### Docker Desktop（macOS/Windows）

```bash
# Docker Desktop 18.09+は自動的にBuildKit対応

# BuildKit有効化（環境変数）
export DOCKER_BUILDKIT=1

# または、デーモン設定
# ~/.docker/daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

#### Linux

```bash
# Docker CE 18.09+ インストール済み前提

# BuildKit有効化
export DOCKER_BUILDKIT=1

# 永続化（~/.bashrc等に追加）
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc

# または、デーモン設定
sudo vi /etc/docker/daemon.json
{
  "features": {
    "buildkit": true
  }
}

sudo systemctl restart docker
```

#### Buildx（Docker CLI Plugin）

```bash
# Buildxインストール（Docker 19.03+に同梱）
docker buildx version

# Builderインスタンス作成
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap

# ビルド実行
docker buildx build -t myapp:latest .
```

### 基本的なビルド

```bash
# BuildKitでビルド
DOCKER_BUILDKIT=1 docker build -t myapp:latest .

# Buildx使用
docker buildx build -t myapp:latest .

# プログレス表示形式
docker buildx build --progress=plain -t myapp:latest .
# plain: 詳細ログ
# auto: デフォルト（TTY検出）
# tty: リアルタイム進捗バー
```

### 新しいDockerfile機能

#### RUN --mount（ビルド時マウント）

```dockerfile
# Dockerfile

# ===== キャッシュマウント =====
# node_modules, .npmをキャッシュ
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .
RUN npm run build

# ===== シークレットマウント =====
# .npmrcの認証情報を安全に利用
FROM node:18 AS private-deps

WORKDIR /app
COPY package*.json ./

RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci

# ===== SSHマウント =====
# プライベートGitリポジトリからクローン
FROM alpine:latest AS git-clone

RUN apk add --no-cache git openssh-client

RUN --mount=type=ssh \
    git clone git@github.com:private-org/private-repo.git /app

# ===== バインドマウント =====
# ホストのファイルを一時的にマウント
FROM golang:1.21 AS builder

WORKDIR /app
COPY go.mod go.sum ./

RUN --mount=type=bind,source=vendor,target=vendor \
    --mount=type=cache,target=/go/pkg/mod \
    go build -mod=vendor -o app .
```

```bash
# シークレット指定してビルド
docker buildx build \
  --secret id=npmrc,src=$HOME/.npmrc \
  -t myapp:latest .

# SSH Agentフォワーディング
docker buildx build \
  --ssh default \
  -t myapp:latest .
```

#### ヒアドキュメント

```dockerfile
# Dockerfile

FROM python:3.11

# ===== ヒアドキュメントで複数行スクリプト =====
RUN <<EOF
apt-get update
apt-get install -y \
    git \
    curl \
    vim
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF

# ===== ファイル作成 =====
COPY <<EOF /app/config.yaml
server:
  host: 0.0.0.0
  port: 8080
database:
  host: db
  port: 5432
EOF

# ===== Pythonスクリプト埋め込み =====
RUN python3 <<'EOF'
import json
import os

config = {
    "app_name": os.getenv("APP_NAME", "myapp"),
    "version": "1.0.0"
}

with open("/app/config.json", "w") as f:
    json.dump(config, f, indent=2)
EOF
```

### キャッシュ戦略

#### インラインキャッシュ

```bash
# キャッシュ有効化してビルド
docker buildx build \
  --cache-to=type=inline \
  --cache-from=type=registry,ref=myregistry.com/myapp:cache \
  -t myapp:latest \
  --push .

# 2回目以降のビルドでキャッシュ利用
docker buildx build \
  --cache-from=type=registry,ref=myregistry.com/myapp:cache \
  -t myapp:latest .
```

#### レジストリキャッシュ

```bash
# 専用キャッシュイメージをレジストリに保存
docker buildx build \
  --cache-to=type=registry,ref=myregistry.com/myapp:buildcache,mode=max \
  --cache-from=type=registry,ref=myregistry.com/myapp:buildcache \
  -t myapp:latest \
  --push .

# mode=max: すべてのレイヤーをキャッシュ（推奨）
# mode=min: 最終レイヤーのみキャッシュ
```

#### ローカルキャッシュ

```bash
# ローカルディレクトリにキャッシュ保存
docker buildx build \
  --cache-to=type=local,dest=/tmp/buildkit-cache \
  --cache-from=type=local,src=/tmp/buildkit-cache \
  -t myapp:latest .
```

#### S3/GCSキャッシュ

```bash
# S3キャッシュ（要: AWS認証情報）
docker buildx build \
  --cache-to=type=s3,region=ap-northeast-1,bucket=my-buildkit-cache \
  --cache-from=type=s3,region=ap-northeast-1,bucket=my-buildkit-cache \
  -t myapp:latest .
```

### マルチプラットフォームビルド

```bash
# AMD64とARM64を同時ビルド
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myregistry.com/myapp:latest \
  --push .

# 個別にビルド
docker buildx build \
  --platform linux/amd64 \
  -t myapp:amd64 .

docker buildx build \
  --platform linux/arm64 \
  -t myapp:arm64 .
```

```dockerfile
# Dockerfile（マルチアーキテクチャ対応）

FROM --platform=$BUILDPLATFORM golang:1.21 AS builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

WORKDIR /app
COPY . .

# クロスコンパイル
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -o app .

FROM alpine:latest
COPY --from=builder /app/app /usr/local/bin/app
ENTRYPOINT ["app"]
```

### ビルド高速化の実例

#### Node.jsアプリケーション

```dockerfile
# Dockerfile

FROM node:18 AS builder

WORKDIR /app

# 依存関係のみ先にインストール（キャッシュ活用）
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --production=false

# ソースコードコピー
COPY . .

# ビルド
RUN --mount=type=cache,target=/root/.npm \
    npm run build

# 本番イメージ
FROM node:18-slim

WORKDIR /app

# 本番依存関係のみインストール
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --production

# ビルド成果物コピー
COPY --from=builder /app/dist ./dist

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

#### Go アプリケーション

```dockerfile
# Dockerfile

FROM golang:1.21 AS builder

WORKDIR /app

# Go modulesキャッシュ
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# ビルド
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -o app .

# 最小イメージ
FROM scratch
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
```

#### Python アプリケーション

```dockerfile
# Dockerfile

FROM python:3.11-slim AS builder

WORKDIR /app

# システム依存関係
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# 本番イメージ
FROM python:3.11-slim

WORKDIR /app

# ビルドしたパッケージコピー
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["python", "app.py"]
```

### CI/CD統合

#### GitHub Actions

```yaml
# .github/workflows/docker-build.yml
name: Docker Build

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Registry
        uses: docker/login-action@v2
        with:
          registry: myregistry.com
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and Push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: myregistry.com/myapp:${{ github.sha }},myregistry.com/myapp:latest
          cache-from: type=registry,ref=myregistry.com/myapp:buildcache
          cache-to: type=registry,ref=myregistry.com/myapp:buildcache,mode=max
          platforms: linux/amd64,linux/arm64
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
build:
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_BUILDKIT: 1
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker buildx create --use
    - docker buildx build
      --cache-from=type=registry,ref=$CI_REGISTRY_IMAGE:buildcache
      --cache-to=type=registry,ref=$CI_REGISTRY_IMAGE:buildcache,mode=max
      --push
      --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      --tag $CI_REGISTRY_IMAGE:latest
      .
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | ローカル開発 | 高速ビルドで開発効率向上 |
| **テスト** | CI環境ビルド | キャッシュ活用で高速化 |
| **導入** | 本番イメージビルド | マルチアーキテクチャ対応 |
| **運用** | 定期ビルド | 効率的なキャッシュ管理 |

## メリット

- **高速ビルド**: 並列実行、効率的キャッシュ
- **柔軟なキャッシュ**: レジストリ、S3、GCS対応
- **新機能**: シークレット、SSHマウント等
- **マルチプラットフォーム**: クロスアーキテクチャビルド
- **オープンソース**: 無料、コミュニティ活発
- **Docker標準**: Docker 18.09+でネイティブサポート

## デメリット

- **学習曲線**: 新しい機能・概念の習得必要
- **互換性**: 一部古いDockerfileは修正必要
- **デバッグ困難**: 並列実行でエラー箇所特定困難な場合
- **キャッシュ管理**: 適切なキャッシュ戦略設計が必要

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **BuildKit** | Docker公式、高速 | 無料 | Docker標準環境 |
| **Kaniko** | K8s特化、rootless | 無料 | Kubernetes環境 |
| **Buildah** | OCI標準、Dockerfileなし可 | 無料 | Podman環境 |
| **img** | rootless、セキュア | 無料 | 非特権環境 |

## ベストプラクティス

### 1. レイヤーキャッシュ最適化

```dockerfile
# ❌ 悪い例（変更頻度高いファイルを先にコピー）
COPY . .
RUN npm install

# ✅ 良い例（依存関係ファイルのみ先にコピー）
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm npm install
COPY . .
```

### 2. マウントキャッシュ活用

```dockerfile
# npm/pip/go mod等のキャッシュディレクトリをマウント
RUN --mount=type=cache,target=/root/.npm npm ci
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/go/pkg/mod go mod download
```

### 3. マルチステージビルド

```dockerfile
# ビルド環境
FROM node:18 AS builder
RUN --mount=type=cache,target=/root/.npm npm ci
RUN npm run build

# 本番環境（最小化）
FROM node:18-slim
COPY --from=builder /app/dist ./dist
```

### 4. シークレット管理

```dockerfile
# ❌ 悪い例（シークレットがレイヤーに残る）
ARG NPM_TOKEN
RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc && \
    npm install && \
    rm .npmrc

# ✅ 良い例（シークレットマウント）
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install
```

## 公式リソース

- **GitHub**: https://github.com/moby/buildkit
- **ドキュメント**: https://docs.docker.com/build/buildkit/
- **Dockerfile リファレンス**: https://docs.docker.com/engine/reference/builder/
- **Buildx**: https://docs.docker.com/buildx/working-with-buildx/
- **Best Practices**: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

## まとめ

BuildKitは、Docker社が開発した次世代のDockerイメージビルドエンジンです。並列ビルド、高度なキャッシング、新しいDockerfile機能により、従来のDockerビルドを大幅に高速化します。Docker 18.09+でネイティブサポートされ、無料で利用可能なため、すべてのDockerユーザーにとって必須の最適化技術です。

---

**最終更新**: 2025-12-06
**対象バージョン**: BuildKit 0.12+, Docker 24+
