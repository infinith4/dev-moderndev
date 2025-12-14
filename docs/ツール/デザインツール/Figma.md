# Figma

## 概要

Figmaは、クラウドベースのUI/UXデザインツールです。リアルタイムコラボレーション、コンポーネント、Auto Layout、プロトタイピング、デザインシステム、デベロッパーハンドオフにより、Webサイト・モバイルアプリのデザインを効率化します。Adobe買収予定、ブラウザベース、Sketch代替で急速に普及しています。

## 主な機能

### 1. デザイン
- **ベクター編集**: Pen Tool、図形
- **コンポーネント**: 再利用可能コンポーネント
- **Auto Layout**: レスポンシブ
- **スタイル**: カラー、テキストスタイル

### 2. プロトタイプ
- **インタラクション**: クリック、ホバー
- **トランジション**: アニメーション
- **オーバーレイ**: モーダル
- **プレビュー**: リアルタイムプレビュー

### 3. コラボレーション
- **リアルタイム**: 同時編集
- **コメント**: フィードバック
- **バージョン履歴**: 履歴管理
- **共有**: リンク共有

### 4. ハンドオフ
- **Inspect**: CSS・コード出力
- **エクスポート**: PNG、SVG、PDF
- **デザイントークン**: 変数
- **プラグイン**: 拡張機能

## 利用方法

### アカウント作成

```
https://www.figma.com/

Sign up:
- Email
- Google
- GitHub

Create team / Join team
```

### 基本操作

```
# ツール
V: 選択ツール
F: フレームツール
R: 長方形
O: 円
T: テキスト
P: ペンツール

# ショートカット
Cmd/Ctrl + D: 複製
Cmd/Ctrl + G: グループ化
Cmd/Ctrl + /: 検索
Cmd/Ctrl + .: コメント
Shift + 1: ズームフィット
Shift + 2: 選択範囲ズーム

# レイヤー
Cmd/Ctrl + ]: 前面へ
Cmd/Ctrl + [: 背面へ
```

### フレーム作成

```
1. Frame Tool (F)
2. サイズ選択:
   - Desktop: 1440x1024
   - iPhone 14 Pro: 393x852
   - iPad Pro: 1024x1366

または
プリセット: Desktop / iPhone / Android
```

### コンポーネント

```
# コンポーネント作成
1. ボタンデザイン作成
2. 右クリック > Create Component (Cmd/Ctrl + Alt + K)

# バリアント作成
1. コンポーネント選択
2. 右パネル > Add variant
3. プロパティ設定:
   - State: Default, Hover, Active
   - Size: Small, Medium, Large
   - Type: Primary, Secondary

# インスタンス使用
1. Assets パネル > Component
2. ドラッグ&ドロップ
3. プロパティ変更
```

### Auto Layout

```
1. フレーム選択
2. Shift + A (Auto Layout)

設定:
- Direction: Horizontal / Vertical
- Spacing: 16px
- Padding: 20px
- Resizing: Hug / Fill

用途:
- ボタン（テキスト長に応じて幅自動調整）
- カード（コンテンツに応じて高さ自動調整）
- ナビゲーション（アイテム数に応じて配置）
```

### スタイル

```
# カラースタイル
1. オブジェクト選択
2. Fill color 選択
3. Style icon (四角4つ) > +
4. Name: Primary/500

# テキストスタイル
1. テキスト選択
2. Text properties
3. Style icon > +
4. Name: Heading/H1
   - Font: Inter
   - Size: 32px
   - Weight: Bold
   - Line height: 120%
```

### プロトタイプ

```
# インタラクション設定
1. Prototype タブ
2. オブジェクト選択（例: ボタン）
3. + をドラッグ → 遷移先フレーム
4. 設定:
   - On click
   - Navigate to
   - Instant / Dissolve / Smart Animate
   - 300ms

# プレビュー
右上 Play icon > プレビュー表示
```

### デザインシステム

```
# ローカルライブラリ
1. File > Publish library
2. Component / Style を公開

# 使用
1. 別ファイルで Assets > Team library
2. ライブラリ有効化
3. Component使用

# 更新
1. ライブラリファイルでComponent更新
2. Publish changes
3. 使用側ファイルで Update available > Review
```

### プラグイン

```
人気プラグイン:

デザイン:
- Iconify: アイコン検索・挿入
- Unsplash: 画像挿入
- Lorem Ipsum: ダミーテキスト
- Remove BG: 背景削除

ハンドオフ:
- Figma to Code: HTML/CSS生成
- Anima: React/Vue コード生成

ユーティリティ:
- Autoflow: フローチャート
- Chart: グラフ作成
- Table Generator: テーブル生成
```

### デベロッパーハンドオフ

```
# Inspect モード
1. Share > Copy link
2. 開発者に共有
3. Inspect パネル:
   - CSS プロパティ
   - iOS / Android コード
   - エクスポート

# コードコピー
.button {
  width: 120px;
  height: 40px;
  background: #0066FF;
  border-radius: 8px;
  font-family: Inter;
  font-size: 14px;
  color: #FFFFFF;
}
```

### エクスポート

```
# 設定
1. オブジェクト選択
2. Export section > +
3. 設定:
   - Format: PNG / SVG / PDF
   - Scale: 1x / 2x / 3x (@2x, @3x)
   - Suffix: @2x

# 一括エクスポート
File > Export > Export [object name]
```

### バージョン履歴

```
File > Show version history

- すべての編集履歴表示
- 任意のバージョンにロールバック可能
- バージョン名付け
- バージョン比較
```

### Figma API

```javascript
// Figma API（Node.js）
const axios = require('axios')

const FIGMA_TOKEN = 'your-token'
const FILE_KEY = 'file-key'

// ファイル取得
async function getFile() {
  const response = await axios.get(
    `https://api.figma.com/v1/files/${FILE_KEY}`,
    {
      headers: { 'X-Figma-Token': FIGMA_TOKEN }
    }
  )
  return response.data
}

// 画像エクスポート
async function exportImage(nodeId) {
  const response = await axios.get(
    `https://api.figma.com/v1/images/${FILE_KEY}?ids=${nodeId}&format=png&scale=2`,
    {
      headers: { 'X-Figma-Token': FIGMA_TOKEN }
    }
  )
  return response.data.images[nodeId]
}
```

### Figma Embed

```html
<!-- Webサイト埋め込み -->
<iframe
  style="border: 1px solid rgba(0, 0, 0, 0.1);"
  width="800"
  height="450"
  src="https://www.figma.com/embed?embed_host=share&url=https://www.figma.com/file/..."
  allowfullscreen
></iframe>
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Starter** | 🟢 無料 | 3ファイル、無制限閲覧者 |
| **Professional** | 💰 $12/エディター/月 | 無制限ファイル、バージョン履歴 |
| **Organization** | 💰 $45/エディター/月 | デザインシステム、高度権限 |
| **Enterprise** | 💰 $75/エディター/月 | SSO、専用サポート |

## メリット

1. **無料枠**: 個人利用無料
2. **ブラウザベース**: インストール不要
3. **コラボレーション**: リアルタイム共同編集
4. **クロスプラットフォーム**: Windows、macOS
5. **プラグイン**: 豊富な拡張機能

## デメリット

1. **オフライン**: ネット接続必要
2. **パフォーマンス**: 大規模ファイルで遅延
3. **学習曲線**: 高度機能複雑
4. **有料機能**: デザインシステム有料

## 公式リンク

- **公式サイト**: [https://www.figma.com/](https://www.figma.com/)
- **ドキュメント**: [https://help.figma.com/](https://help.figma.com/)

## 関連ドキュメント

- [デザインツール一覧](../デザインツール/)
- [Sketch](./Sketch.md)
- [Adobe XD](./Adobe_XD.md)

---

**カテゴリ**: デザインツール
**対象工程**: UI/UXデザイン
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
