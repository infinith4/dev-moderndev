# Webpack

## 概要

Webpackは、JavaScript向けモジュールバンドラーです。モジュール解決、依存関係解析、コード分割、ローダー（CSS、画像等）、プラグイン、最適化により、フロントエンドビルドを効率化します。React、Vue、Angular等で標準採用、エコシステム豊富で広く使用されています。

## 主な機能

### 1. モジュールバンドル
- **ES Modules**: import/export
- **CommonJS**: require/module.exports
- **依存関係解析**: グラフ構築
- **バンドル**: 単一ファイル出力

### 2. ローダー
- **babel-loader**: トランスパイル
- **css-loader/style-loader**: CSS
- **file-loader/url-loader**: 画像・フォント
- **ts-loader**: TypeScript

### 3. プラグイン
- **HtmlWebpackPlugin**: HTML生成
- **MiniCssExtractPlugin**: CSS抽出
- **TerserPlugin**: 最小化
- **DefinePlugin**: 環境変数

### 4. 最適化
- **コード分割**: チャンク分割
- **Tree Shaking**: 未使用コード削除
- **ミニファイ**: 圧縮
- **キャッシュ**: ハッシュファイル名

## 利用方法

### インストール

```bash
# プロジェクト初期化
npm init -y

# Webpackインストール
npm install --save-dev webpack webpack-cli

# 開発サーバー
npm install --save-dev webpack-dev-server
```

### 基本設定

```javascript
// webpack.config.js
const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
};
```

```bash
# ビルド
npx webpack

# または package.json
{
  "scripts": {
    "build": "webpack"
  }
}

npm run build
```

### Babel統合

```bash
# Babelインストール
npm install --save-dev babel-loader @babel/core @babel/preset-env
```

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  }
};
```

### CSS処理

```bash
# CSSローダー
npm install --save-dev css-loader style-loader
npm install --save-dev mini-css-extract-plugin
```

```javascript
// webpack.config.js
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css'
    })
  ]
};
```

### 画像・ファイル処理

```javascript
// webpack.config.js (Webpack 5)
module.exports = {
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif|svg)$/,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name].[hash][ext]'
        }
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name].[hash][ext]'
        }
      }
    ]
  }
};
```

### HTML生成

```bash
npm install --save-dev html-webpack-plugin
```

```javascript
// webpack.config.js
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      filename: 'index.html'
    })
  ]
};
```

### 開発サーバー

```javascript
// webpack.config.js
module.exports = {
  devServer: {
    static: './dist',
    port: 3000,
    hot: true,
    open: true
  }
};
```

```json
// package.json
{
  "scripts": {
    "dev": "webpack serve --mode development",
    "build": "webpack --mode production"
  }
}
```

```bash
npm run dev
```

### コード分割

```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        },
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true
        }
      }
    }
  }
};
```

```javascript
// 動的インポート
// src/index.js
import('./module').then(module => {
  module.default();
});

// lazy loading
const loadModule = async () => {
  const { default: module } = await import('./module');
  module();
};
```

### 環境変数

```javascript
// webpack.config.js
const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
      'process.env.API_URL': JSON.stringify('https://api.example.com')
    })
  ]
};
```

```javascript
// src/config.js
const apiUrl = process.env.API_URL;
console.log(`API URL: ${apiUrl}`);
```

### 本番ビルド

```javascript
// webpack.config.js
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  mode: 'production',
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
    splitChunks: {
      chunks: 'all'
    }
  },
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true  // 古いファイル削除
  }
};
```

### TypeScript統合

```bash
npm install --save-dev typescript ts-loader
```

```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js']
  }
};
```

### React統合

```bash
npm install react react-dom
npm install --save-dev @babel/preset-react
```

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react'
            ]
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  }
};
```

### ソースマップ

```javascript
// webpack.config.js
module.exports = {
  devtool: 'source-map',  // 本番
  // devtool: 'eval-source-map',  // 開発
};
```

### エイリアス

```javascript
// webpack.config.js
module.exports = {
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils')
    }
  }
};
```

```javascript
// src/index.js
import Button from '@components/Button';
import { formatDate } from '@utils/date';
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Webpack** | 🟢 無料 | オープンソース、MIT License |

## メリット

1. **無料**: オープンソース
2. **豊富なエコシステム**: プラグイン・ローダー多数
3. **柔軟性**: 高度なカスタマイズ
4. **最適化**: Tree Shaking、コード分割
5. **標準**: React、Vue等で採用

## デメリット

1. **複雑性**: 設定複雑
2. **学習曲線**: steep
3. **ビルド速度**: 大規模で遅い
4. **設定量**: webpack.config.js肥大化

## 公式リンク

- **公式サイト**: [https://webpack.js.org/](https://webpack.js.org/)
- **ドキュメント**: [https://webpack.js.org/concepts/](https://webpack.js.org/concepts/)

## 関連ドキュメント

- [ビルドツール一覧](../ビルドツール/)
- [Babel](../トランスパイラツール/Babel.md)
- [Vite](./Vite.md)

---

**カテゴリ**: ビルドツール
**対象工程**: フロントエンドビルド
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
