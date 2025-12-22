# draw.io CLI ガイド

このガイドでは、公式の draw.io Desktop を使用してコマンドラインから UML 図を作成・エクスポートする方法を説明します。

## 目次

- [インストール](#インストール)
- [基本的な使い方](#基本的な使い方)
- [UML図の作成](#uml図の作成)
- [コマンドラインでのエクスポート](#コマンドラインでのエクスポート)
- [サンプル図](#サンプル図)

## インストール

### Ubuntu/Debian へのインストール

公式の draw.io Desktop は GitHub リリースページから .deb パッケージをダウンロードしてインストールできます。

#### 1. 最新バージョンの確認

```bash
curl -s https://api.github.com/repos/jgraph/drawio-desktop/releases/latest | grep '"tag_name"'
```

#### 2. .deb パッケージのダウンロード

```bash
# 最新版（例: v29.0.3）をダウンロード
wget https://github.com/jgraph/drawio-desktop/releases/download/v29.0.3/drawio-amd64-29.0.3.deb
```

または、自動的に最新版を取得:

```bash
curl -s https://api.github.com/repos/jgraph/drawio-desktop/releases/latest | \
  grep "browser_download_url.*amd64.*\.deb" | \
  cut -d '"' -f 4 | \
  wget -i -
```

#### 3. インストール

```bash
sudo dpkg -i drawio-amd64-*.deb

# 依存関係のエラーが出た場合
sudo apt-get install -f
```

#### 4. インストール確認

```bash
drawio --version
```

### その他のインストール方法

#### Snap を使用（推奨・最も簡単）

```bash
sudo snap install drawio
```

#### AppImage を使用

```bash
# AppImage をダウンロード
wget https://github.com/jgraph/drawio-desktop/releases/download/v29.0.3/drawio-x86_64-29.0.3.AppImage

# 実行権限を付与
chmod +x drawio-x86_64-*.AppImage

# 実行
./drawio-x86_64-*.AppImage
```

## 基本的な使い方

### GUI モードでの起動

```bash
drawio
```

### 既存ファイルを開く

```bash
drawio diagram.drawio
```

### 新規ファイルを作成

```bash
drawio --create new_diagram.drawio
```

## UML図の作成

### GUI での UML 図作成手順

1. **draw.io を起動**
   ```bash
   drawio
   ```

2. **新規図の作成**
   - File → New を選択
   - または既存ファイルを開く

3. **UML 図形の選択**
   - 左側のパネルで「More Shapes...」をクリック
   - 「Software」カテゴリから「UML」を選択してチェック
   - 「Apply」をクリック

4. **UML 要素の配置**
   - **クラス図**: Class、Interface、Abstract Class などを配置
   - **シーケンス図**: Lifeline、Activation、Message などを配置
   - **ユースケース図**: Actor、Use Case、System Boundary などを配置
   - **アクティビティ図**: Action、Decision、Fork/Join などを配置

5. **保存**
   - File → Save As
   - `.drawio` 形式で保存

### UML 図の種類と使用例

#### クラス図 (Class Diagram)

クラスの構造と関係を表現します。

**主要な要素:**
- クラスボックス（属性とメソッドを含む）
- 継承関係（実線矢印）
- 実装関係（点線矢印）
- 関連・集約・コンポジション

**サンプル:** [diagrams/class_diagram.drawio](diagrams/class_diagram.drawio)

#### シーケンス図 (Sequence Diagram)

オブジェクト間のメッセージのやり取りを時系列で表現します。

**主要な要素:**
- ライフライン（オブジェクトの存在期間）
- アクティベーション（処理の実行期間）
- メッセージ（同期・非同期）
- 戻り値

**サンプル:** [diagrams/sequence_diagram.drawio](diagrams/sequence_diagram.drawio)

#### ユースケース図 (Use Case Diagram)

システムの機能とアクターの関係を表現します。

**主要な要素:**
- アクター（スティックフィギュア）
- ユースケース（楕円形）
- システム境界（矩形）
- 関連（実線）
- 包含（<<include>>）
- 拡張（<<extend>>）

**サンプル:** [diagrams/usecase_diagram.drawio](diagrams/usecase_diagram.drawio)

#### アクティビティ図 / フローチャート

処理の流れを表現します。

**主要な要素:**
- 開始/終了（角丸矩形）
- アクション/処理（矩形）
- 判断（菱形）
- 分岐/合流

**サンプル:** [diagrams/flowchart.drawio](diagrams/flowchart.drawio)

## コマンドラインでのエクスポート

draw.io Desktop には強力なコマンドライン機能が組み込まれており、GUI を使わずに図をエクスポートできます。

### 基本構文

```bash
drawio -x -f <format> -o <output> <input>
```

### エクスポートオプション

#### 主要オプション

| オプション | 説明 | 例 |
|-----------|------|-----|
| `-x, --export` | エクスポートモード | `-x` |
| `-f, --format <format>` | 出力形式（pdf, png, jpg, svg, xml, vsdx） | `-f pdf` |
| `-o, --output <file>` | 出力ファイルパス | `-o output.pdf` |
| `-t, --transparent` | PNG 背景を透過 | `-t` |
| `-b, --border <width>` | 図の周囲の余白（ピクセル） | `-b 10` |
| `-s, --scale <scale>` | 拡大縮小率 | `-s 2` |
| `--width <pixels>` | 幅指定（アスペクト比維持） | `--width 1920` |
| `--height <pixels>` | 高さ指定（アスペクト比維持） | `--height 1080` |
| `--crop` | PDF の余白を削除 | `--crop` |
| `-a, --all-pages` | 全ページをエクスポート（PDF のみ） | `-a` |
| `-p, --page-index <n>` | 特定ページを指定（1 始まり） | `-p 2` |
| `-e, --embed-diagram` | 図データを埋め込み（PNG, SVG, PDF） | `-e` |
| `-q, --quality <quality>` | JPEG 品質（0-100） | `-q 90` |

### エクスポート例

#### PDF 形式でエクスポート

```bash
# 基本的な PDF エクスポート
drawio -x -f pdf -o class_diagram.pdf class_diagram.drawio

# 余白を削除して PDF エクスポート
drawio -x -f pdf --crop -o class_diagram.pdf class_diagram.drawio

# 全ページを PDF にエクスポート
drawio -x -f pdf -a --crop -o document.pdf multi_page.drawio
```

#### PNG 形式でエクスポート

```bash
# 基本的な PNG エクスポート
drawio -x -f png -o diagram.png diagram.drawio

# 背景透過 PNG
drawio -x -f png -t -o diagram.png diagram.drawio

# 高品質 PNG（2倍スケール、余白 10px）
drawio -x -f png -t -s 2 -b 10 -o diagram_hq.png diagram.drawio

# サイズ指定 PNG
drawio -x -f png --width 1920 --height 1080 -o diagram_fullhd.png diagram.drawio
```

#### SVG 形式でエクスポート

```bash
# SVG エクスポート
drawio -x -f svg -o diagram.svg diagram.drawio

# 図データを埋め込んだ SVG
drawio -x -f svg -e -o diagram.svg diagram.drawio
```

#### JPEG 形式でエクスポート

```bash
# JPEG エクスポート（品質 90）
drawio -x -f jpg -q 90 -o diagram.jpg diagram.drawio
```

### 一括エクスポート

#### フォルダ内の全ファイルをエクスポート

```bash
# 再帰的に全 .drawio ファイルを PDF に変換
drawio -x -r -f pdf -o output_folder/ input_folder/

# 現在のディレクトリの全 .drawio ファイルを PNG に変換
for file in *.drawio; do
  drawio -x -f png -t -o "${file%.drawio}.png" "$file"
done
```

### シェルスクリプト例

```bash
#!/bin/bash
# export_diagrams.sh - 全ての drawio ファイルを PDF と PNG にエクスポート

DIAGRAMS_DIR="./diagrams"
OUTPUT_DIR="./output"

mkdir -p "$OUTPUT_DIR"

for file in "$DIAGRAMS_DIR"/*.drawio; do
  filename=$(basename "$file" .drawio)

  # PDF エクスポート
  drawio -x -f pdf --crop -o "$OUTPUT_DIR/${filename}.pdf" "$file"

  # PNG エクスポート（透過、2倍スケール）
  drawio -x -f png -t -s 2 -b 10 -o "$OUTPUT_DIR/${filename}.png" "$file"

  echo "Exported: $filename"
done

echo "All diagrams exported successfully!"
```

実行方法:

```bash
chmod +x export_diagrams.sh
./export_diagrams.sh
```

## サンプル図

このリポジトリには以下のサンプル UML 図が含まれています:

### 1. クラス図 (Class Diagram)

EC サイトのクラス構造を示した例です。

- **ファイル:** [diagrams/class_diagram.drawio](diagrams/class_diagram.drawio)
- **PDF:** [diagrams/class_diagram.pdf](diagrams/class_diagram.pdf)
- **PNG:** [diagrams/class_diagram.png](diagrams/class_diagram.png)

**含まれる要素:**
- User クラス
- Product クラス
- Order クラス
- クラス間の関連（集約、関連）

### 2. シーケンス図 (Sequence Diagram)

ユーザー認証のシーケンスを示した例です。

- **ファイル:** [diagrams/sequence_diagram.drawio](diagrams/sequence_diagram.drawio)
- **PDF:** [diagrams/sequence_diagram.pdf](diagrams/sequence_diagram.pdf)
- **PNG:** [diagrams/sequence_diagram.png](diagrams/sequence_diagram.png)

**処理フロー:**
1. ユーザーがログイン要求
2. Web サーバーが認証サービスに問い合わせ
3. 認証サービスがデータベースからユーザー情報を取得
4. 認証結果を返却
5. セッショントークン生成
6. ログイン成功

### 3. ユースケース図 (Use Case Diagram)

EC サイトシステムのユースケースを示した例です。

- **ファイル:** [diagrams/usecase_diagram.drawio](diagrams/usecase_diagram.drawio)
- **PDF:** [diagrams/usecase_diagram.pdf](diagrams/usecase_diagram.pdf)
- **PNG:** [diagrams/usecase_diagram.png](diagrams/usecase_diagram.png)

**アクター:**
- 顧客
- 管理者
- 決済システム

**主なユースケース:**
- ユーザー登録、ログイン
- 商品検索、カートに追加
- 注文確定、支払い処理
- 商品管理、注文履歴閲覧

### 4. フローチャート (Flowchart)

ログイン処理のフローを示した例です。

- **ファイル:** [diagrams/flowchart.drawio](diagrams/flowchart.drawio)
- **PDF:** [diagrams/flowchart.pdf](diagrams/flowchart.pdf)
- **PNG:** [diagrams/flowchart.png](diagrams/flowchart.png)

**処理フロー:**
- ユーザー入力
- 入力バリデーション
- データベース認証
- セッション作成
- エラーハンドリングとリトライ

### サンプル図のエクスポート方法

各サンプル図を再エクスポートする場合:

```bash
cd PROJECT_V1

# PDF エクスポート
drawio -x -f pdf --crop -o diagrams/class_diagram.pdf diagrams/class_diagram.drawio
drawio -x -f pdf --crop -o diagrams/sequence_diagram.pdf diagrams/sequence_diagram.drawio
drawio -x -f pdf --crop -o diagrams/usecase_diagram.pdf diagrams/usecase_diagram.drawio
drawio -x -f pdf --crop -o diagrams/flowchart.pdf diagrams/flowchart.drawio

# PNG エクスポート（透過背景、2倍スケール）
drawio -x -f png -t -s 2 -b 10 -o diagrams/class_diagram.png diagrams/class_diagram.drawio
drawio -x -f png -t -s 2 -b 10 -o diagrams/sequence_diagram.png diagrams/sequence_diagram.drawio
drawio -x -f png -t -s 2 -b 10 -o diagrams/usecase_diagram.png diagrams/usecase_diagram.drawio
drawio -x -f png -t -s 2 -b 10 -o diagrams/flowchart.png diagrams/flowchart.drawio
```

## トラブルシューティング

### drawio コマンドが見つからない

**症状:** `drawio: command not found`

**解決方法:**

1. インストールの確認:
   ```bash
   which drawio
   dpkg -l | grep drawio
   ```

2. Snap でインストールした場合:
   ```bash
   /snap/bin/drawio --version
   ```

3. PATH に追加:
   ```bash
   export PATH=$PATH:/snap/bin
   ```

### X サーバーエラー

**症状:** `Error: Cannot open display`

**解決方法:**

ヘッドレス環境（SSH 接続など）では、Xvfb を使用します:

```bash
# Xvfb のインストール
sudo apt-get install xvfb

# Xvfb 経由で実行
xvfb-run -a drawio -x -f pdf -o output.pdf input.drawio
```

### フォントの問題

**症状:** 日本語フォントが正しく表示されない

**解決方法:**

日本語フォントをインストール:

```bash
sudo apt-get install fonts-ipafont fonts-noto-cjk
fc-cache -fv
```

## 参考リンク

- [draw.io Desktop GitHub リポジトリ](https://github.com/jgraph/drawio-desktop)
- [draw.io 公式サイト](https://www.drawio.com/)
- [draw.io ドキュメント](https://www.diagrams.net/doc/)

## チェックリスト

- [x] draw.io CLI のインストール（公式 draw.io desktop の利用）
- [x] draw.io CLI で UML 作成（サンプル含む）

---

**作成日:** 2025-12-19
**バージョン:** draw.io Desktop v29.0.3