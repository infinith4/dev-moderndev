# Travis CI

## 概要

Travis CIは、GitHubネイティブのCI/CDプラットフォームです。.travis.yml、マトリックスビルド、複数言語サポート（Ruby、Python、Node.js、Java等）、GitHub統合により、オープンソースプロジェクトのビルド・テスト・デプロイを自動化します。オープンソース無料、シンプルな設定、GitHub統合で広く採用されています。

## 主な機能

### 1. CI/CD
- **自動ビルド**: プッシュ、PRトリガー
- **マトリックスビルド**: 複数環境
- **言語サポート**: 20+言語
- **デプロイ**: Heroku、AWS、GitHub Pages

### 2. マトリックス
- **複数バージョン**: Node 14、16、18等
- **複数OS**: Linux、macOS、Windows
- **並列実行**: 並列ジョブ

### 3. キャッシュ
- **依存関係**: npm、pip、Maven
- **ディレクトリ**: カスタムキャッシュ

### 4. 統合
- **GitHub**: ネイティブ統合
- **通知**: Slack、Email
- **ステータスバッジ**: README表示

## 利用方法

### 基本設定

```yaml
# .travis.yml
language: node_js
node_js:
  - "18"

script:
  - npm test
```

### マルチ言語

```yaml
# Python
language: python
python:
  - "3.9"
  - "3.10"
  - "3.11"

install:
  - pip install -r requirements.txt

script:
  - pytest
```

### マトリックスビルド

```yaml
language: node_js

node_js:
  - "14"
  - "16"
  - "18"

os:
  - linux
  - osx
  - windows

env:
  - NODE_ENV=development
  - NODE_ENV=production

script:
  - npm test
```

### ビルドステージ

```yaml
language: node_js
node_js:
  - "18"

jobs:
  include:
    - stage: test
      script: npm test

    - stage: build
      script: npm run build

    - stage: deploy
      script: ./deploy.sh
      if: branch = main

stages:
  - test
  - build
  - deploy
```

### キャッシュ

```yaml
language: node_js
node_js:
  - "18"

cache:
  directories:
    - node_modules

before_install:
  - npm install -g npm@latest

install:
  - npm ci

script:
  - npm test
```

### Docker

```yaml
language: minimal

services:
  - docker

script:
  - docker build -t myapp .
  - docker run myapp npm test

after_success:
  - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
  - docker push myapp:latest
```

### デプロイ（Heroku）

```yaml
language: node_js
node_js:
  - "18"

script:
  - npm test

deploy:
  provider: heroku
  api_key:
    secure: $HEROKU_API_KEY
  app: my-app-name
  on:
    branch: main
```

### デプロイ（GitHub Pages）

```yaml
language: node_js
node_js:
  - "18"

script:
  - npm run build

deploy:
  provider: pages
  skip_cleanup: true
  github_token: $GITHUB_TOKEN
  local_dir: dist
  on:
    branch: main
```

### 環境変数

```yaml
language: node_js
node_js:
  - "18"

env:
  global:
    - API_URL=https://api.example.com
    - secure: "encrypted_api_key"

script:
  - echo "API URL is $API_URL"
  - npm test
```

### 条件分岐

```yaml
language: node_js
node_js:
  - "18"

jobs:
  include:
    - script: npm run lint
      if: type = pull_request

    - script: npm test
      if: branch = main

    - script: ./deploy.sh
      if: tag IS present
```

### 通知

```yaml
notifications:
  email:
    recipients:
      - dev@example.com
    on_success: change
    on_failure: always

  slack:
    rooms:
      - secure: "encrypted_slack_token"
    on_success: always
    on_failure: always
```

### ステータスバッジ

```markdown
# README.md
[![Build Status](https://travis-ci.org/username/repo.svg?branch=main)](https://travis-ci.org/username/repo)
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Travis CI (OSS)** | 🟢 無料 | オープンソースプロジェクト |
| **Free Plan** | 🟢 10,000分/月 | プライベートリポジトリ |
| **Starter** | 💰 $69/月 | 無制限ビルド、1並列 |
| **Premium** | 💰 $129/月 | 無制限ビルド、2並列 |

## メリット

1. **オープンソース無料**: OSS完全無料
2. **GitHub統合**: ネイティブ統合
3. **シンプル**: 簡単設定
4. **マトリックス**: 複数環境並列
5. **成熟**: 長年の実績

## デメリット

1. **有料化**: プライベートリポジトリ有料
2. **パフォーマンス**: ビルド遅延
3. **機能制限**: 高度機能少ない
4. **代替台頭**: GitHub Actions台頭

## 公式リンク

- **公式サイト**: [https://www.travis-ci.com/](https://www.travis-ci.com/)
- **ドキュメント**: [https://docs.travis-ci.com/](https://docs.travis-ci.com/)

## 関連ドキュメント

- [CI/CDツール一覧](../CI_CDツール/)
- [GitHub Actions](./GitHub_Actions.md)
- [CircleCI](./CircleCI.md)

---

**カテゴリ**: CI/CDツール
**対象工程**: 継続的インテグレーション・デプロイ
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
