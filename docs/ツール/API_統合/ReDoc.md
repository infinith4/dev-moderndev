# ReDoc

## 概要

ReDocは、OpenAPI（Swagger）仕様書から美しく読みやすいAPIドキュメントを自動生成するオープンソースツールです。Redocly社が開発し、レスポンシブデザイン、3カラムレイアウト、検索機能、サンプルコード生成により、開発者フレンドリーなAPIリファレンスを提供します。HTMLファイル1つで公開でき、SwaggerUIの代替として広く利用されています。

## 主な特徴

| 項目 | 内容 |
|------|------|
| 美しい3カラムレイアウト | ナビゲーション、説明、サンプルコードの同時表示 |
| レスポンシブデザイン | モバイル・デスクトップ両対応 |
| OpenAPI完全サポート | OpenAPI 3.x、Swagger 2.0対応 |
| 軽量・高速 | SwaggerUIより高速なレンダリング |
| 静的HTML出力 | 単一HTMLファイルで簡単に公開 |
| カスタマイズ | テーマ、ロゴ、カラー設定が柔軟 |
| 無料 | MIT License、オープンソース |

## 主な機能

### ドキュメント表示

| 機能 | 説明 |
|------|------|
| 3カラムレイアウト | ナビゲーション、説明、サンプルを同時表示 |
| 検索機能 | キーワードでAPI要素を検索 |
| ディープリンク | 特定エンドポイントへの直接リンク |
| 折りたたみ | セクションの展開/折りたたみ |

### OpenAPIサポート

| 機能 | 説明 |
|------|------|
| OpenAPI 3.x | 最新仕様対応 |
| Swagger 2.0 | レガシーサポート |
| 複数仕様書統合 | マルチファイル対応 |
| $ref解決 | 外部参照自動解決 |

### コードサンプル生成

| 機能 | 説明 |
|------|------|
| cURL | コマンドライン例 |
| JavaScript | fetch、axios |
| Python | requests |
| 多言語対応 | Ruby、PHP、Java等 |

## インストールとセットアップ

公式URL:
- [ReDoc 公式サイト](https://redocly.com/redoc)
- [GitHub リポジトリ](https://github.com/Redocly/redoc)
- [Redocly CLI](https://redocly.com/docs/cli/)

## 基本的な使い方

### 1. CDNで利用（最もシンプル）

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>API Documentation</title>
  <style>
    body {
      margin: 0;
      padding: 0;
    }
  </style>
</head>
<body>
  <redoc spec-url="https://api.example.com/openapi.yaml"></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

### 2. CLIで静的HTML生成

```bash
# npmでインストール
npm install -g @redocly/cli

# OpenAPIファイルからHTML生成
redocly build-docs openapi.yaml -o index.html

# ローカルサーバー起動（プレビュー）
redocly preview-docs openapi.yaml
# ブラウザで http://localhost:8080 にアクセス
```

### 3. カスタマイズ（テーマ設定）

```html
<redoc spec-url="openapi.yaml" theme='{
    "colors": {
      "primary": {
        "main": "#00A86B"
      }
    },
    "typography": {
      "fontSize": "16px",
      "fontFamily": "Roboto, sans-serif"
    },
    "sidebar": {
      "backgroundColor": "#f5f5f5"
    },
    "logo": {
      "maxHeight": "50px"
    }
  }'></redoc>
<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
```

### 4. React Component

```jsx
import { RedocStandalone } from 'redoc';

function ApiDocs() {
  return (
    <RedocStandalone
      specUrl="https://api.example.com/openapi.yaml"
      options={{
        nativeScrollbars: true,
        theme: {
          colors: {
            primary: { main: '#00A86B' }
          }
        }
      }}
    />
  );
}

export default ApiDocs;
```

### 5. 詳細オプション

```html
<redoc
  spec-url="openapi.yaml"
  hide-download-button
  disable-search
  expand-responses="200,201"
  expand-single-schema-field
  hide-hostname
  hide-loading
  lazy-rendering
  native-scrollbars
  no-auto-auth
  path-in-middle-panel
  required-props-first
  sort-props-alphabetically
  theme='{"colors": {"primary": {"main": "#00A86B"}}}'
></redoc>
```

## CI/CD 統合

### GitHub Actions（GitHub Pages公開）

```yaml
name: Deploy API Docs

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Redocly CLI
        run: npm install -g @redocly/cli

      - name: Build docs
        run: redocly build-docs openapi.yaml -o index.html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

### GitLab CI

```yaml
deploy_docs:
  stage: deploy
  image: node:24
  before_script:
    - npm install -g @redocly/cli
  script:
    - redocly build-docs openapi.yaml -o public/index.html
  artifacts:
    paths:
      - public
```

## Docker での使用

### Dockerfile 例

```dockerfile
FROM node:24-alpine AS builder
RUN npm install -g @redocly/cli
WORKDIR /app
COPY openapi.yaml .
RUN redocly build-docs openapi.yaml -o index.html

FROM nginx:alpine
COPY --from=builder /app/index.html /usr/share/nginx/html/
```

### docker-compose.yml 例

```yaml
version: '3.8'
services:
  redoc:
    image: redocly/redoc
    ports:
      - "8080:80"
    volumes:
      - ./openapi.yaml:/usr/share/nginx/html/openapi.yaml
    environment:
      SPEC_URL: openapi.yaml
```

## 他ツールとの比較

### ReDoc vs Swagger UI

| 機能 | ReDoc | Swagger UI |
|------|-------|------------|
| デザイン | 3カラム、美しい | 標準的 |
| Try It Out | なし（表示のみ） | あり（APIテスト可能） |
| パフォーマンス | 高速 | 標準 |
| カスタマイズ | テーマ設定 | CSSカスタマイズ |
| 検索 | あり | なし |

### ReDoc vs Stoplight Elements

| 機能 | ReDoc | Stoplight Elements |
|------|-------|-------------------|
| Try It Out | なし | あり |
| デザイン | 3カラム | モダン |
| React統合 | あり | あり |
| 無料利用 | 完全無料 | 無料版あり |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| APIリファレンス公開 | 外部開発者向けドキュメント | OpenAPIから美しいドキュメントを自動生成 |
| 社内APIドキュメント | チーム間のAPI仕様共有 | 静的HTMLをイントラネットで公開 |
| GitHub Pages公開 | 無料でAPIドキュメントをホスト | CI/CDでビルドし自動デプロイ |

## ベストプラクティス

### 1. OpenAPI定義の充実

- examplesを充実させることでドキュメントの品質が向上する
- descriptionフィールドにMarkdown記法を使用して詳細な説明を記述する
- スキーマの再利用（$ref）でドキュメントの一貫性を保つ

### 2. テーマのカスタマイズ

- 企業のブランドカラーに合わせたテーマ設定を行う
- ロゴを設定してブランドアイデンティティを確立する
- フォントサイズやフォントファミリーを調整して読みやすさを向上させる

### 3. CI/CDでの自動生成

- OpenAPI定義の変更時に自動でドキュメントをビルド・デプロイする
- バリデーション（redocly lint）をCIに組み込む

## トラブルシューティング

### よくある問題と解決策

#### 1. OpenAPI仕様のパースエラー

```
原因: YAMLの構文エラーまたはOpenAPI仕様の違反
解決策:
- redocly lint openapi.yaml でバリデーションを実行
- オンラインのOpenAPIバリデータで確認
```

#### 2. $refが解決されない

```
原因: 外部参照ファイルのパスが正しくない
解決策:
- 相対パスを確認する
- redocly bundle で単一ファイルにバンドルする
```

#### 3. カスタムテーマが反映されない

```
原因: JSON形式のテーマ設定が不正
解決策:
- theme属性のJSON構文を確認する
- ブラウザのコンソールでエラーを確認する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://redocly.com/redoc
- ドキュメント: https://redocly.com/docs/redoc/

### コミュニティ
- GitHub: https://github.com/Redocly/redoc

### チュートリアル
- Getting Started: https://redocly.com/docs/redoc/quickstart/
- デモ: https://redocly.github.io/redoc/

## まとめ

ReDocは、以下の場面で特に有用です:

1. **APIドキュメント公開** - OpenAPIから美しい3カラムレイアウトのドキュメントを自動生成
2. **静的サイトホスティング** - 単一HTMLファイルでGitHub PagesやS3に簡単にデプロイ
3. **ブランディング** - テーマカスタマイズでブランドに合ったドキュメントを作成

SwaggerUIより美しいデザインと高速なレンダリングで、APIドキュメントの閲覧体験を向上させる。
