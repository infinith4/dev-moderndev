# Webpack

## 概要

Webpackは、JavaScriptアプリケーション向けモジュールバンドラーです。JavaScript、CSS、画像等のアセットを依存関係グラフで解析し、最適化されたバンドルを生成します。Code Splitting、Tree Shaking、Hot Module Replacement（HMR）、Loader、Pluginにより、モダンWebアプリケーション開発を支援します。

## 主な機能

### 1. バンドリング
- **モジュール統合**: ES6 Modules、CommonJS
- **依存関係解析**: エントリーポイントから自動解析
- **出力最適化**: Minify、圧縮

### 2. Code Splitting
- **動的インポート**: import()
- **複数エントリー**: マルチページアプリ
- **共通チャンク**: vendor分離

### 3. Loader
- **babel-loader**: ES6→ES5変換
- **css-loader**: CSS処理
- **file-loader**: 画像、フォント

### 4. Plugin
- **HtmlWebpackPlugin**: HTML自動生成
- **MiniCssExtractPlugin**: CSS分離
- **CleanWebpackPlugin**: ビルドクリーンアップ

### 5. 開発サーバー
- **webpack-dev-server**: ライブリロード
- **HMR**: Hot Module Replacement

## 利用方法

### インストール

```bash
npm install --save-dev webpack webpack-cli
```

### 設定ファイル

```javascript
// webpack.config.js
const path = require('path');

module.exports = {
  mode: 'production',
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  }
};
```

### ビルド実行

```bash
# 本番ビルド
npx webpack --mode production

# 開発ビルド
npx webpack --mode development

# Watch モード
npx webpack --watch
```

### 開発サーバー

```bash
npm install --save-dev webpack-dev-server

# 起動
npx webpack serve --open
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Webpack** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **高性能**: 最適化バンドル
3. **柔軟**: Loader、Plugin拡張
4. **Code Splitting**: 遅延ロード
5. **HMR**: 高速開発

## デメリット

1. **学習曲線**: 設定複雑
2. **ビルド時間**: 大規模で遅い
3. **設定**: webpack.config.js煩雑
4. **エラー**: エラーメッセージわかりにくい

## 公式リンク

- **公式サイト**: [https://webpack.js.org/](https://webpack.js.org/)
- **ドキュメント**: [https://webpack.js.org/concepts/](https://webpack.js.org/concepts/)

## 関連ドキュメント

- [ビルドツール一覧](../ビルドツール/)
- [Vite](./Vite.md)

---

**カテゴリ**: ビルドツール  
**対象工程**: ビルド  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
