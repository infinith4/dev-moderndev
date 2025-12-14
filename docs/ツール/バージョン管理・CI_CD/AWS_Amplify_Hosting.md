# AWS Amplify Hosting

## 概要

**AWS Amplify Hosting**は、静的Webサイト・SPAをGitリポジトリから自動ビルド・デプロイできるフルマネージドホスティングサービスです。CI/CDパイプライン内蔵、グローバルCDN配信、カスタムドメイン対応により、モダンWebアプリケーションの継続的デプロイを簡単に実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | フルマネージドCI/CDホスティングサービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 従量課金（ビルド時間・データ転送量） |
| **公式サイト** | https://aws.amazon.com/amplify/hosting/ |
| **ドキュメント** | https://docs.aws.amazon.com/amplify/ |

## 主な特徴

### 1. Git統合CI/CD
- GitHub、GitLab、Bitbucket、AWS CodeCommit連携
- プッシュ時に自動ビルド・デプロイ
- プルリクエストプレビュー
- ブランチベースデプロイ

### 2. フレームワーク対応
- **React**: Create React App、Next.js
- **Vue.js**: Nuxt.js、Vue CLI
- **Angular**: Angular CLI
- **静的サイトジェネレーター**: Gatsby、Hugo、Jekyll、Eleventy

### 3. グローバルCDN配信
- Amazon CloudFront統合
- SSL/TLS証明書自動発行（ACM）
- カスタムドメイン対応
- 200以上のエッジロケーション

### 4. 開発者機能
- 環境変数管理
- ビルド設定カスタマイズ
- リダイレクト・リライト設定
- 基本認証（ステージング環境）
- モニタリング・ログ

## 使い方

### セットアップ

#### AWS Amplify Console からデプロイ

```bash
# 1. GitHubリポジトリを準備
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/my-app.git
git push -u origin main

# 2. AWS Amplify Console にアクセス
# https://console.aws.amazon.com/amplify/

# 3. "New app" → "Host web app" をクリック
# 4. GitHub を選択して認証
# 5. リポジトリとブランチを選択
# 6. ビルド設定を確認（自動検出）
# 7. デプロイ開始
```

#### Amplify CLI でデプロイ

```bash
# Amplify CLI インストール
npm install -g @aws-amplify/cli

# AWS認証情報設定
amplify configure

# プロジェクトで初期化
cd my-app
amplify init

# ホスティング追加
amplify add hosting

# ? Select the plugin module to execute: Hosting with Amplify Console
# ? Choose a type: Manual deployment

# デプロイ
amplify publish

# 自動デプロイ（CI/CD）設定
amplify add hosting
# ? Select the plugin module to execute: Hosting with Amplify Console
# ? Choose a type: Continuous deployment (Git-based deployments)
```

### React アプリケーションのデプロイ

#### Create React App

```bash
# プロジェクト作成
npx create-react-app my-react-app
cd my-react-app

# ビルド設定（amplify.yml）
cat > amplify.yml <<EOF
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
EOF

# Git にコミット
git add .
git commit -m "Add Amplify config"
git push
```

#### Next.js（SSG）

```bash
# Next.js プロジェクト作成
npx create-next-app@latest my-nextjs-app
cd my-nextjs-app

# next.config.js（Static Export設定）
cat > next.config.js <<EOF
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
EOF

# amplify.yml
cat > amplify.yml <<EOF
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: out
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
EOF
```

#### Next.js（SSR）

```yaml
# amplify.yml（SSR対応）
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
applications:
  - appRoot: /
    platform: WEB_COMPUTE
    buildSpec: amplify.yml
```

### 環境変数の設定

```bash
# AWS Console で設定
# Amplify Console → App settings → Environment variables
# KEY: REACT_APP_API_ENDPOINT
# VALUE: https://api.example.com

# または、Amplify CLI で設定
amplify env add

# ビルド時に参照
# REACT_APP_API_ENDPOINT は process.env.REACT_APP_API_ENDPOINT で取得可能
```

```javascript
// src/config.js
const config = {
  apiEndpoint: process.env.REACT_APP_API_ENDPOINT || 'http://localhost:3001',
  environment: process.env.REACT_APP_ENV || 'development',
};

export default config;
```

### カスタムドメインの設定

```bash
# AWS Console で設定
# Amplify Console → App settings → Domain management → Add domain

# 1. ドメイン名入力（例: example.com）
# 2. DNS設定（Route 53 または外部DNS）
#    - CNAME レコード追加
#    - Amplify が提供するDNS値を設定
# 3. SSL証明書自動発行（ACM）
# 4. 5-10分で設定完了

# サブドメイン設定
# www.example.com → main ブランチ
# dev.example.com → develop ブランチ
```

### リダイレクト・リライト設定

```json
// Amplify Console → App settings → Rewrites and redirects
[
  {
    "source": "/old-page",
    "target": "/new-page",
    "status": "301",
    "condition": null
  },
  {
    "source": "/blog/<year>/<month>/<day>/<slug>",
    "target": "/blog/<slug>",
    "status": "301",
    "condition": null
  },
  {
    "source": "</^[^.]+$|\\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|ttf|map|json)$)([^.]+$)/>",
    "target": "/index.html",
    "status": "200",
    "condition": null
  }
]
```

### プルリクエストプレビュー

```yaml
# GitHub でプルリクエスト作成時に自動生成
# https://<pr-number>.<app-id>.amplifyapp.com

# 設定（Amplify Console）
# App settings → Previews
# "Enable pull request previews" をオン

# 自動削除設定
# Pull request merged/closed 時に自動削除
```

### モノレポ対応

```yaml
# amplify.yml（モノレポ）
version: 1
applications:
  - appRoot: packages/frontend
    frontend:
      phases:
        preBuild:
          commands:
            - cd packages/frontend
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: packages/frontend/build
        files:
          - '**/*'
      cache:
        paths:
          - packages/frontend/node_modules/**/*

  - appRoot: packages/admin
    frontend:
      phases:
        preBuild:
          commands:
            - cd packages/admin
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: packages/admin/build
        files:
          - '**/*'
```

### パフォーマンス最適化

```yaml
# amplify.yml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci --production=false
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
  customHeaders:
    - pattern: '**/*'
      headers:
        - key: 'Cache-Control'
          value: 'public, max-age=31536000, immutable'
    - pattern: 'index.html'
      headers:
        - key: 'Cache-Control'
          value: 'no-cache, no-store, must-revalidate'
```

### ビルドログの確認

```bash
# AWS Console でログ確認
# Amplify Console → <App> → <Branch> → Build details

# ビルド失敗時のデバッグ
# 1. ビルドログで失敗箇所を確認
# 2. 環境変数の確認
# 3. ビルド設定（amplify.yml）の確認
# 4. Node.jsバージョンの確認

# Node.jsバージョン指定
# amplify.yml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - nvm install 18
        - nvm use 18
        - node -v
        - npm ci
```

### 基本認証（ステージング保護）

```bash
# AWS Console で設定
# Amplify Console → App settings → Access control

# ブランチ単位で設定
# develop ブランチ: 基本認証有効
# main ブランチ: 基本認証無効

# ユーザー名: admin
# パスワード: your-secure-password
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | 開発環境自動デプロイ | 開発ブランチの継続的デプロイ |
| **テスト** | プレビュー環境 | プルリクエスト毎のプレビュー生成 |
| **導入** | ステージング環境 | main/develop ブランチ自動デプロイ |
| **導入** | 本番環境 | production ブランチ自動デプロイ |

## メリット

- **フルマネージド**: インフラ管理不要、自動スケーリング
- **Git統合CI/CD**: プッシュ時に自動ビルド・デプロイ
- **グローバルCDN**: CloudFront統合で高速配信
- **SSL証明書自動**: ACM統合で証明書自動発行・更新
- **プレビュー環境**: プルリクエスト毎にプレビュー生成
- **フレームワーク自動検出**: React、Vue.js、Next.js等を自動認識
- **無料枠あり**: 月1,000ビルド分、15GB転送まで無料
- **モニタリング**: CloudWatchメトリクス統合

## デメリット

- **従量課金**: ビルド時間・データ転送量で課金
- **ビルド時間制限**: 最大30分/ビルド
- **AWS専用**: マルチクラウド非対応
- **サーバーサイド制限**: SSRは追加設定が必要（Next.js等）
- **カスタマイズ制限**: 高度なサーバー設定は困難
- **ビルド環境固定**: Dockerカスタマイズ不可

## 類似ツールとの比較

| サービス | 特徴 | 料金 | 適用場面 |
|----------|------|------|----------|
| **Amplify Hosting** | AWS統合、CI/CD内蔵 | 従量課金 | AWSエコシステム |
| **Vercel** | Next.js最適化、Edge Functions | 無料〜有料 | Next.js、モダンSPA |
| **Netlify** | プラグインエコシステム | 無料〜有料 | 静的サイト、Jamstack |
| **GitHub Pages** | 無料、Git統合 | 無料 | 個人プロジェクト、ドキュメント |

## ベストプラクティス

### 1. ブランチ戦略

```text
# Gitフロー連携
main        → 本番環境（production.example.com）
staging     → ステージング環境（staging.example.com）
develop     → 開発環境（dev.example.com、基本認証）
feature/*   → プレビュー環境（PR毎に自動生成）
```

### 2. 環境変数の管理

```bash
# 環境別に環境変数を設定
# Production（main ブランチ）
REACT_APP_API_ENDPOINT=https://api.example.com
REACT_APP_ENV=production

# Staging（staging ブランチ）
REACT_APP_API_ENDPOINT=https://api-staging.example.com
REACT_APP_ENV=staging

# Development（develop ブランチ）
REACT_APP_API_ENDPOINT=https://api-dev.example.com
REACT_APP_ENV=development
```

### 3. キャッシュ戦略

```yaml
# amplify.yml - 適切なキャッシュ設定
customHeaders:
  # 静的アセット（長期キャッシュ）
  - pattern: '/static/**'
    headers:
      - key: 'Cache-Control'
        value: 'public, max-age=31536000, immutable'

  # HTML（キャッシュ無効）
  - pattern: '/**/*.html'
    headers:
      - key: 'Cache-Control'
        value: 'no-cache, no-store, must-revalidate'

  # API プロキシ（キャッシュ無効）
  - pattern: '/api/**'
    headers:
      - key: 'Cache-Control'
        value: 'no-cache'
```

### 4. コスト最適化

```yaml
# ビルドキャッシュ活用
version: 1
frontend:
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*  # Next.js
      - .cache/**/*       # Gatsby

# 差分ビルドの活用
# - 変更がないブランチは自動スキップ
# - プルリクエストプレビューは必要時のみ生成
```

### 5. セキュリティ

```yaml
# セキュリティヘッダー設定
customHeaders:
  - pattern: '**/*'
    headers:
      - key: 'Strict-Transport-Security'
        value: 'max-age=31536000; includeSubDomains'
      - key: 'X-Frame-Options'
        value: 'DENY'
      - key: 'X-Content-Type-Options'
        value: 'nosniff'
      - key: 'X-XSS-Protection'
        value: '1; mode=block'
      - key: 'Referrer-Policy'
        value: 'strict-origin-when-cross-origin'
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/amplify/hosting/
- **ドキュメント**: https://docs.aws.amazon.com/amplify/
- **料金**: https://aws.amazon.com/amplify/pricing/
- **チュートリアル**: https://docs.aws.amazon.com/amplify/latest/userguide/welcome.html
- **GitHub**: https://github.com/aws-amplify

## まとめ

AWS Amplify Hostingは、静的Webサイト・SPAをGitリポジトリから自動ビルド・デプロイできるフルマネージドホスティングサービスです。CI/CDパイプライン内蔵、グローバルCDN配信、SSL証明書自動発行により、モダンWebアプリケーションの継続的デプロイを簡単に実現します。React、Vue.js、Next.js等のフレームワークを自動認識し、プルリクエストプレビューや環境別デプロイなど、開発者に優しい機能を提供します。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS Amplify Hosting 2024+
