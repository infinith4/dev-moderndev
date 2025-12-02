# Axure RP

## 概要

Axure RPは、高度なインタラクティブプロトタイプ作成に特化したUX設計ツールです。ワイヤーフレームからハイファイプロトタイプまで、コードを書かずに動的なWebアプリケーションやモバイルアプリのプロトタイプを作成できます。条件分岐、変数、関数を用いた複雑なインタラクションにより、実際のアプリケーションに近い動作を再現し、ユーザビリティテストや開発仕様書としても活用されます。

## 主な機能

### 1. 高度なプロトタイプ
- **動的コンテンツ**: 変数、関数、条件分岐
- **インタラクション**: クリック、ホバー、スワイプ
- **アニメーション**: トランジション、フェード
- **データ駆動**: リピーター、マスター

### 2. ワイヤーフレーム
- **豊富なウィジェット**: フォーム、ナビゲーション、メディア
- **マスター**: 再利用可能なコンポーネント
- **ダイナミックパネル**: タブ、カルーセル、モーダル
- **適応ビュー**: レスポンシブデザイン

### 3. ドキュメント生成
- **仕様書**: HTML形式で自動生成
- **注釈**: ページノート、ウィジェットノート
- **フローダイアグラム**: 画面遷移図
- **スタイルガイド**: デザインシステム

### 4. コラボレーション
- **チーム共有**: Axure Cloudで共有
- **レビュー**: コメント、フィードバック
- **バージョン管理**: SVN、Git統合
- **インスペクトモード**: 開発者向けCSS情報

### 5. HTML出力
- **パブリッシュ**: HTML/CSS/JSとして出力
- **ホスティング**: Axure Cloudでホスト
- **モバイル対応**: タッチジェスチャー対応
- **パスワード保護**: プロトタイプ保護

## 利用方法

### インストール

```
1. 公式サイトからダウンロード
   https://www.axure.com/download

2. インストーラー実行
   - Windows: Axure-RP-Setup.exe
   - macOS: Axure-RP.dmg

3. ライセンス認証
   - 30日間無料トライアル
   - ライセンスキー入力
```

### 基本操作

```
1. 新規プロジェクト作成
   File → New

2. ページ追加
   Pages パネル → + Add Page

3. ウィジェット追加
   Widgets パネル → ドラッグ&ドロップ
   - Rectangle, Text, Button, Text Field等

4. インタラクション追加
   ウィジェット選択 → Interactions パネル
   - OnClick → Open Link in Current Window → ページ選択
```

### ログイン画面プロトタイプ

```
1. ウィジェット配置
   - Text Field: Email
   - Text Field (Type: Password): Password
   - Button: Login

2. インタラクション設定
   Button選択 → Interactions
   - OnClick → Open Link → Dashboard Page
   - Condition: [[LVAR1.length > 0 && LVAR2.length > 0]]
     (両方のフィールドが入力されている場合のみ遷移)

3. エラーメッセージ
   - Text: "Please enter email and password"
   - Hidden by default
   - OnClick (Button) → Show → Error Text (if condition false)
```

### データリピーター

```
1. Repeater追加
   Widgets → Repeater → ドラッグ

2. データセット設定
   Repeater ダブルクリック
   - Column 1: Name
   - Column 2: Email
   - Row 1: John Doe, john@example.com
   - Row 2: Jane Smith, jane@example.com

3. アイテム設計
   Repeater内にウィジェット配置
   - Text: [[Item.Name]]
   - Text: [[Item.Email]]

4. フィルタ・ソート
   - OnClick → Add Filter
   - OnClick → Sort
```

### レスポンシブデザイン

```
1. 適応ビュー追加
   Pages → Adaptive Views → Add View
   - Mobile: 320px
   - Tablet: 768px
   - Desktop: 1024px

2. ビュー切り替え
   上部ツールバー → View選択

3. ビュー固有の配置
   各ビューでウィジェット位置・サイズ調整
```

### HTML出力

```
1. Publish
   Publish → Generate HTML Files

2. 設定
   - Output folder選択
   - Include page notes
   - Password protection

3. プレビュー
   出力フォルダ → index.html をブラウザで開く

4. Axure Cloudにアップロード
   Publish → Publish to Axure Cloud
   - Project name入力
   - Share link生成
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Pro** | 💰 $29/月 または $495（買い切り） | 全機能、単独使用 |
| **Team** | 💰 $49/ユーザー/月 | チーム共有、プラグイン |
| **Enterprise** | 💰 要問い合わせ | オンプレミス、SSO、専用サポート |
| **30日間無料トライアル** | 🟡 無料 | 全機能利用可能 |

## メリット

### ✅ 主な利点

1. **高度なインタラクション**: 変数、条件分岐、関数
2. **リアルな動作**: アプリに近いプロトタイプ
3. **データ駆動**: リピーター、動的コンテンツ
4. **ドキュメント生成**: 仕様書自動生成
5. **レスポンシブ**: 適応ビュー対応
6. **開発者ハンドオフ**: CSS情報出力
7. **バージョン管理**: SVN、Git統合
8. **オフライン**: デスクトップアプリ
9. **買い切りオプション**: 永続ライセンス
10. **エンタープライズ**: 大企業で広く採用

## デメリット

### ❌ 制約・課題

1. **学習曲線**: 習得に時間がかかる
2. **高価**: Figmaより高額
3. **UI古い**: モダンなUIではない
4. **パフォーマンス**: 大規模プロトタイプで遅延
5. **デザインツールではない**: ビジュアルデザイン機能弱い
6. **リアルタイム協業**: Figmaほど強力ではない
7. **モバイルアプリ**: アプリ版なし
8. **クラウド制限**: Axure Cloud容量制限

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Figma** | モダン、協業、デザイン | Axureよりデザイン強い |
| **Adobe XD** | Adobe統合、軽量 | Axureよりシンプル |
| **Sketch** | macOS、プラグイン豊富 | Axureよりデザイン重視 |
| **Balsamiq** | ローファイ、ラピッド | Axureよりシンプル |
| **Framer** | コードベース、高度 | Axureよりモダン |

## 公式リンク

- **公式サイト**: [https://www.axure.com/](https://www.axure.com/)
- **ダウンロード**: [https://www.axure.com/download](https://www.axure.com/download)
- **ドキュメント**: [https://docs.axure.com/](https://docs.axure.com/)
- **チュートリアル**: [https://www.axure.com/learn](https://www.axure.com/learn)
- **フォーラム**: [https://forum.axure.com/](https://forum.axure.com/)

## 関連ドキュメント

- [UI/UXツール一覧](../UI_UXツール/)
- [Figma](./Figma.md)
- [Balsamiq](./Balsamiq.md)
- [Adobe XD](./Adobe_XD.md)
- [プロトタイピングベストプラクティス](../../best-practices/prototyping.md)

---

**カテゴリ**: UI/UXツール  
**対象工程**: 要件定義、設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
