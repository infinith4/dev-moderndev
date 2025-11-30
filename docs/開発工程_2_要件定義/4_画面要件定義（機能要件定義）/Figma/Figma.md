# Figma

## 概要

Figmaは、クラウドベースのUI/UXデザインツールで、画面設計、UIプロトタイプ、デザイン仕様書の作成に特化しています。リアルタイムの共同編集機能とブラウザベースの特性により、チームでの画面要件定義作業を効率化できます。

### 主な特徴

- **ブラウザで完結**: インストール不要で、Webブラウザから利用可能
- **リアルタイム共同編集**: 複数ユーザーが同時に編集可能
- **プロトタイプ作成簡単**: 画面遷移を視覚的に設定可能
- **デベロッパーハンドオフ**: デザインからコードへの引き渡しが容易
- **無料プランあり**: 基本機能は無料で利用可能

### 料金プラン

- **Free版**: 個人利用、3ファイルまで
- **Professional**: $12/月/ユーザー（無制限ファイル、バージョン履歴）
- **Organization**: $45/月/ユーザー（組織管理、デザインシステム）
- **Enterprise**: $75/月/ユーザー（高度なセキュリティ、SSO）

### メリット・デメリット

**メリット**
- ブラウザベースでどこからでもアクセス可能
- リアルタイム協業により、チームでの作業が効率的
- プロトタイプ作成が簡単で、画面遷移を直感的に設定できる
- デベロッパーハンドオフ機能により、開発者への引き渡しが容易
- 無料プランでも基本機能が充実

**デメリット**
- オフラインでは作業不可
- 複雑なダイアグラムや技術図の作成には不向き
- プラグインへの依存が増えがち
- 大規模ファイルは動作が重くなることがある

## 利用方法

### 1. アカウント作成

1. [Figma公式サイト](https://www.figma.com/)にアクセス
2. 「Get started for free」をクリック
3. メールアドレスまたはGoogle/Appleアカウントで登録
4. アカウントを有効化

### 2. 新規デザインファイルの作成

1. Figmaダッシュボードにログイン
2. 「+ New」ボタンをクリック→「Design file」を選択
3. ファイル名を入力（例: "ECサイト画面設計"）
4. 空のキャンバスが表示される

### 3. フレームの配置

フレームは、各画面を表す基本単位です。

#### デスクトップ画面の作成

1. 左側ツールバーから「Frame」ツール（F）を選択
2. 右側パネルから「Desktop」カテゴリを選択
3. プリセットサイズを選択（例: Desktop - 1440 x 1024）
4. または、キャンバス上でドラッグしてカスタムサイズのフレームを作成

#### モバイル画面の作成

1. 「Frame」ツールを選択
2. 右側パネルから「Phone」カテゴリを選択
3. プリセットサイズを選択（例: iPhone 14 Pro - 393 x 852）

### 4. UI要素の配置

#### テキストの追加

1. 左側ツールバーから「Text」ツール（T）を選択
2. フレーム内でクリック
3. テキストを入力（例: "ログイン画面"、"商品一覧"）
4. 右側パネルでフォント、サイズ、色を設定

#### 図形の追加

1. 左側ツールバーから図形ツールを選択
   - **Rectangle** (R): 四角形（ボタン、入力フィールド等）
   - **Ellipse** (O): 円形（アイコン等）
   - **Line** (L): 線
2. フレーム内でドラッグして配置
3. 右側パネルで塗りつぶし色、線の色・太さを設定

#### コンポーネントの利用

Figmaでは、再利用可能なUI要素を「コンポーネント」として定義できます。

1. UI要素（例: ボタン）を作成
2. 要素を選択して、右クリック→「Create component」
3. コンポーネント名を入力（例: "Primary Button"）
4. 「Assets」パネルからコンポーネントをドラッグ&ドロップで再利用

### 5. 画面設計の具体例

**例: ECサイトのログイン画面**

#### 1. フレームの作成

- Frame名: "ログイン画面"
- サイズ: Desktop - 1440 x 1024

#### 2. ヘッダーの作成

1. Rectangle (R) を作成
   - サイズ: 1440 x 80
   - 位置: 上部に配置
   - 背景色: #2C3E50
2. Textで「ECサイト」ロゴを追加
   - フォント: Bold、24px
   - 色: #FFFFFF

#### 3. ログインフォームの作成

1. 中央にログインコンテナを配置
   - Rectangle: 400 x 500
   - 背景色: #FFFFFF
   - Border radius: 8px
   - Shadow: Drop shadow設定

2. タイトルを追加
   - Text: "ログイン"
   - フォント: Bold、32px
   - 色: #2C3E50

3. メールアドレス入力フィールド
   - Text: "メールアドレス"（ラベル）
   - Rectangle: 360 x 48（入力フィールド）
   - Border: 1px、色 #D0D5DD
   - Border radius: 4px

4. パスワード入力フィールド
   - Text: "パスワード"（ラベル）
   - Rectangle: 360 x 48（入力フィールド）
   - Border: 1px、色 #D0D5DD
   - Border radius: 4px

5. ログインボタン
   - Rectangle: 360 x 48
   - 背景色: #3498DB
   - Border radius: 4px
   - Text: "ログイン"
   - フォント: Bold、16px、色 #FFFFFF

6. リンク
   - Text: "パスワードを忘れた方はこちら"
   - フォント: 14px、色 #3498DB
   - Underline

#### 4. フッターの作成

1. Rectangle: 1440 x 60
2. Text: "© 2025 ECサイト. All rights reserved."
3. 背景色: #ECF0F1

### 6. プロトタイプモードで画面遷移設定

Figmaのプロトタイプ機能により、画面遷移を定義できます。

#### 画面遷移の設定

1. 画面上部で「Prototype」タブを選択
2. 遷移元の要素（例: ログインボタン）を選択
3. 要素の右端に表示される「+」アイコンをクリック
4. 遷移先のフレーム（例: "商品一覧画面"）までドラッグ
5. 右側パネルで遷移設定を調整:
   - **Interaction**: On click、On hover等
   - **Animation**: Instant、Dissolve、Slide等
   - **Easing**: Linear、Ease in、Ease out等
   - **Duration**: アニメーション時間（ms）

#### プロトタイプのプレビュー

1. 右上の「Play」ボタン（▶）をクリック
2. 新しいウィンドウでプロトタイプが表示される
3. インタラクションをクリックして画面遷移を確認

### 7. コンポーネントとバリアント

#### コンポーネントの作成

複数の画面で共通して使うUI要素（ボタン、ヘッダー等）をコンポーネント化します。

1. UI要素を作成（例: プライマリボタン）
2. 要素を選択→上部ツールバーの「Create component」アイコンをクリック
3. コンポーネント名を入力

#### バリアントの作成

ボタンの状態（Default、Hover、Disabled）をバリアントとして管理します。

1. 複数のコンポーネント（例: Button Default、Button Hover）を選択
2. 右クリック→「Combine as variants」
3. バリアントプロパティを設定（例: State = Default/Hover/Disabled）

### 8. 画面一覧と画面遷移図の作成

#### 画面一覧

1. 新しいページを作成（左側パネルの「Pages」→「+」）
2. ページ名を「画面一覧」に変更
3. Tableプラグインをインストール（Plugins → Browse plugins → Table）
4. テーブルを作成し、以下の列を定義:
   - 画面ID
   - 画面名
   - 概要
   - URL
   - アクセス権限

#### 画面遷移図

1. 新しいページ「画面遷移図」を作成
2. 各画面のフレームのサムネイルを配置
3. 「Arrow」ツールで画面間の遷移を矢印で接続
4. 矢印にラベルを追加（例: "ログインボタンクリック"）

### 9. デベロッパーハンドオフ

Figmaは、デザインから開発への引き渡し（ハンドオフ）機能が充実しています。

#### 開発者へのアクセス共有

1. 右上の「Share」ボタンをクリック
2. 開発者のメールアドレスを入力
3. 権限を「Can view」に設定（編集不可、閲覧のみ）
4. 「Send」をクリック

#### Inspect モード

開発者は、Inspectモードで以下の情報を確認できます:
- CSS: 要素のスタイル（色、フォント、サイズ等）
- コード: CSS、iOS、Android用のコードスニペット
- Assets: 画像やアイコンのエクスポート

1. 要素を選択
2. 右側パネルで「Code」タブを選択
3. CSS、iOS、Androidのコードを確認
4. 「Copy」ボタンでコードをコピー

### 10. 画面仕様書の自動生成

FigmaからHTML/PDF形式で画面仕様書を生成できます。

#### プラグインの利用

1. 「Plugins」→「Browse plugins」→「Design Docs」をインストール
2. ファイルを開いて「Plugins」→「Design Docs」を実行
3. 仕様書に含める情報を選択
   - 画面キャプチャ
   - コンポーネント一覧
   - スタイルガイド
4. 「Export」ボタンでPDF/HTML出力

### 11. バージョン履歴

Figmaは自動的にバージョン履歴を保存します。

1. 左上のファイル名をクリック→「Show version history」
2. 過去のバージョンを確認
3. 復元したいバージョンを選択→「Restore this version」

### 12. チーム協業のベストプラクティス

#### コメント機能

1. 左側ツールバーの「Comment」ツール（C）を選択
2. コメントを追加したい場所をクリック
3. コメント内容を入力
4. チームメンバーが返信可能

#### リアルタイム編集

- 複数ユーザーが同時に編集可能
- 各ユーザーのカーソルが色分けされて表示
- 編集内容はリアルタイムで同期

## 公式ドキュメント

- **公式サイト**: [Figma](https://www.figma.com/)
- **入門ガイド**: [Get Started with Figma](https://help.figma.com/hc/en-us/categories/360002051613-Get-started)
- **デザインチュートリアル**: [Figma Design Tutorials](https://www.figma.com/resources/learn-design/)
- **プロトタイプガイド**: [Prototype Tutorial](https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma)
- **コンポーネント**: [Create Components](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma)
- **デベロッパーハンドオフ**: [Inspect Mode](https://help.figma.com/hc/en-us/articles/360055203533-Use-Inspect-panel)

## 学習リソース

- **Figma YouTube チャンネル**: [Figma YouTube](https://www.youtube.com/c/Figmadesign)
- **Figma Community**: [Community Files](https://www.figma.com/community)（無料テンプレート、UIキット）
- **Config（年次カンファレンス）**: [Config Recordings](https://config.figma.com/)

## 関連リンク

- [Material Design 3 Figma Kit](https://www.figma.com/community/file/1035203688168086460)
- [iOS 17 UI Kit](https://www.figma.com/community/)
- [Figma Plugins](https://www.figma.com/community/plugins)
- [FigJam](https://www.figma.com/figjam/)（Figmaのホワイトボードツール）
