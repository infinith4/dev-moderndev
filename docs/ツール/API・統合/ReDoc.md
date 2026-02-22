# ReDoc

## 概要

ReDocは、OpenAPI（Swagger）仕様書から美しく読みやすいAPIドキュメントを自動生成するオープンソースツールです。Redocly社が開発し、レスポンシブデザイン、3カラムレイアウト、検索機能、サンプルコード生成により、開発者フレンドリーなAPIリファレンスを提供します。HTMLファイル1つで公開でき、SwaggerUIの代替として広く利用されています。

## 主な機能

### 1. 美しいドキュメント
- **3カラムレイアウト**: ナビゲーション、説明、サンプルコード
- **レスポンシブデザイン**: モバイル・デスクトップ対応
- **ダークモード**: テーマ切り替え
- **カスタムスタイル**: CSS、ロゴ、カラー設定

### 2. OpenAPI完全サポート
- **OpenAPI 3.x**: 最新仕様対応
- **Swagger 2.0**: レガシーサポート
- **複数仕様書**: マルチファイル統合
- **$ref解決**: 外部参照自動解決

### 3. インタラクティブ機能
- **検索**: キーワード検索
- **ディープリンク**: 特定エンドポイントへの直接リンク
- **折りたたみ**: セクション展開/折りたたみ
- **コピー**: コードサンプル1クリックコピー

### 4. コードサンプル生成
- **cURL**: コマンドライン例
- **JavaScript**: fetch、axios
- **Python**: requests
- **Ruby、PHP、Java等**: 多言語対応

### 5. 高速レンダリング
- **軽量**: SwaggerUIより高速
- **パフォーマンス最適化**: 大規模API対応
- **遅延ロード**: 必要なセクションのみ読み込み

### 6. 公開オプション
- **静的HTML**: 単一HTMLファイル
- **CDN**: jsDelivrから読み込み
- **Docker**: コンテナでホスト
- **React Component**: React統合

## 利用方法

### 基本的な使い方（CDN）

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

### CLI（単一HTMLファイル生成）

```bash
# npmでインストール
npm install -g @redocly/cli

# OpenAPIファイルからHTML生成
redocly build-docs openapi.yaml -o index.html

# ローカルサーバー起動（プレビュー）
redocly preview-docs openapi.yaml

# ブラウザで http://localhost:8080 にアクセス
```

### Node.jsプロジェクトに統合

```bash
# インストール
npm install redoc

# package.json
{
  "scripts": {
    "docs": "redocly build-docs openapi.yaml -o docs/index.html"
  }
}

# 実行
npm run docs
```

### カスタマイズ（テーマ設定）

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Custom API Docs</title>
</head>
<body>
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
</body>
</html>
```

### React Component

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

### Docker

```bash
# Dockerイメージ取得
docker pull redocly/redoc

# コンテナ起動
docker run -p 8080:80 \
  -v $(pwd)/openapi.yaml:/usr/share/nginx/html/openapi.yaml \
  -e SPEC_URL=openapi.yaml \
  redocly/redoc
```

### GitHub Pages公開

```yaml
# .github/workflows/docs.yml
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

### 詳細オプション

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

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **ReDoc Community** | 🟢 無料 | オープンソース、MIT License |
| **Redocly CLI** | 🟢 無料 | コマンドラインツール |
| **Redocly Platform** | 💰 $0～要問い合わせ | ホスティング、チーム協業、カスタムドメイン |

## メリット

### ✅ 主な利点

1. **美しいデザイン**: SwaggerUIより洗練されたUI
2. **読みやすい**: 3カラムレイアウト、大規模API対応
3. **無料**: オープンソース、MIT License
4. **軽量**: SwaggerUIより高速
5. **レスポンシブ**: モバイル対応
6. **検索機能**: キーワード検索
7. **カスタマイズ**: テーマ、ロゴ、カラー設定
8. **簡単公開**: 単一HTMLファイル
9. **React統合**: Reactコンポーネントとして利用
10. **SSR対応**: サーバーサイドレンダリング

## デメリット

### ❌ 制約・課題

1. **Try It Out不可**: APIテスト機能なし（表示のみ）
2. **編集不可**: OpenAPI仕様書の編集はできない
3. **認証テスト不可**: SwaggerUIのような認証フローなし
4. **カスタマイズ限定**: 高度なカスタマイズには制約
5. **プラグインなし**: 拡張機能エコシステム未整備
6. **学習コスト**: 高度な設定はドキュメント参照必要
7. **デバッグ困難**: 仕様書エラー時の診断が難しい
8. **JavaScript必須**: NoScriptでは動作しない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Swagger UI** | Try It Out、APIテスト | ReDocよりインタラクティブ |
| **Stoplight Elements** | モダンUI、Try It Out | ReDocと類似、テスト機能あり |
| **RapiDoc** | Web Component、軽量 | ReDocよりカスタマイズ容易 |
| **Scalar** | モダンAPI Docs、高速 | ReDocより新しい |
| **Postman Docs** | Postman統合 | ReDocよりPostmanエコシステム |

## 公式リンク

- **公式サイト**: [https://redocly.com/redoc](https://redocly.com/redoc)
- **GitHub**: [https://github.com/Redocly/redoc](https://github.com/Redocly/redoc)
- **デモ**: [https://redocly.github.io/redoc/](https://redocly.github.io/redoc/)
- **ドキュメント**: [https://redocly.com/docs/redoc/](https://redocly.com/docs/redoc/)
- **Redocly CLI**: [https://redocly.com/docs/cli/](https://redocly.com/docs/cli/)

## 関連ドキュメント

- [APIツール一覧](../APIツール/)
- [Swagger/OpenAPI](./Swagger_OpenAPI.md)
- [Stoplight Studio](./Stoplight_Studio.md)
- [Postman](./Postman.md)
- [APIドキュメントベストプラクティス](../../best-practices/api-documentation.md)

---

**カテゴリ**: APIツール  
**対象工程**: 設計、実装、運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
