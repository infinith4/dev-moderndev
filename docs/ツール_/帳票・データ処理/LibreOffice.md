# LibreOffice（帳票設計）

## 概要

LibreOfficeは、無料のオープンソースオフィススイートで、基本設計フェーズでは帳票レイアウト設計、帳票テンプレート作成、PDF出力仕様の定義に活用します。Writer（ワープロ）、Calc（表計算）、Draw（図形描画）を組み合わせて、印刷帳票やPDF帳票の詳細設計を行います。

### 基本設計フェーズでの活用

- **帳票レイアウト設計**: ビジネス文書、請求書、納品書等のレイアウト
- **帳票テンプレート作成**: 再利用可能な帳票テンプレート（.ott、.ots形式）
- **PDF出力仕様**: PDF/A対応、フォーム機能、デジタル署名
- **差し込み印刷**: データベースと連携した帳票生成
- **マクロによる自動化**: Python、Basic、JavaScriptマクロ

### 料金プラン

- **LibreOffice**: 無料（MPL 2.0ライセンス）
- すべての機能が無料で商用利用可能

### メリット・デメリット

**メリット**
- 無料で商用利用可能
- Microsoft Officeとの高い互換性
- PDF/A準拠のPDF出力
- Python/Basicマクロで自動化可能
- クロスプラットフォーム（Windows、macOS、Linux）
- 軽量で動作が速い

**デメリット**
- Microsoft Officeとの完全互換性はない
- 複雑なマクロはVBA互換性に制限あり
- テンプレートがMicrosoft Officeに比べて少ない

## 利用方法

### 1. LibreOfficeのインストール

1. [LibreOffice公式サイト](https://www.libreoffice.org/)にアクセス
2. 「ダウンロード」をクリック
3. OS別のインストーラーをダウンロード:
   - Windows: `LibreOffice_x.x.x_Win_x64.msi`
   - macOS: `LibreOffice_x.x.x_MacOS_x86-64.dmg`
   - Linux: `LibreOffice_x.x.x_Linux_x86-64_deb.tar.gz`
4. インストーラーを実行
5. 日本語言語パックをインストール（必要に応じて）

### 2. Writer（ワープロ）での帳票設計

#### 例: 請求書テンプレートの作成

**1. 新規文書の作成**

1. LibreOffice Writerを起動
2. ファイル → 新規作成 → 文書テンプレート
3. 用紙サイズをA4に設定（デフォルト）

**2. ページ設定**

1. 書式 → ページスタイル
2. 「ページ」タブで設定:
   - **用紙サイズ**: A4 (210 x 297 mm)
   - **向き**: 縦
   - **余白**: 上下左右 20mm
3. 「ヘッダー」タブ:
   - 「ヘッダーを付ける」にチェック
   - 高さ: 30mm
4. 「フッター」タブ:
   - 「フッターを付ける」にチェック
   - 高さ: 20mm

**3. ヘッダーの設計**

```
┌───────────────────────────────────┐
│ 【会社ロゴ】    請求書              │
│                                   │
│ 発行日: 2025年1月15日              │
└───────────────────────────────────┘
```

1. ヘッダーエリアをダブルクリック
2. 挿入 → 画像で会社ロゴを挿入（左上）
3. テキストボックスを挿入: "請求書"（右上、24pt、太字）
4. テキストボックスを挿入: "発行日: [日付フィールド]"

**4. 請求先情報の配置**

```
請求先:
株式会社サンプル
〒100-0001
東京都千代田区千代田1-1-1
ご担当者: 山田 太郎 様
```

1. 表 → 挿入 → 表（2列 x 4行）
2. 1列目: ラベル（"請求先:"、"住所:"、"ご担当者:"）
3. 2列目: データフィールド（後でデータを差し込む）
4. 枠線を非表示または薄いグレーに設定

**5. 請求明細テーブルの作成**

| No. | 商品名 | 数量 | 単価 | 小計 |
|-----|--------|------|------|------|
| 1   |        |      |      |      |
| 2   |        |      |      |      |
| ... |        |      |      |      |

1. 表 → 挿入 → 表（5列 x 10行）
2. 1行目: ヘッダー行
   - 背景色: #E0E0E0
   - テキスト: "No."、"商品名"、"数量"、"単価"、"小計"
   - 中央揃え、太字
3. 2行目以降: データ行
4. 列幅の調整:
   - No.: 10mm
   - 商品名: 80mm
   - 数量: 20mm
   - 単価: 30mm
   - 小計: 30mm

**6. 合計金額の配置**

```
                        小計: ¥100,000
                    消費税(10%): ¥10,000
                    ──────────────────
                    合計金額: ¥110,000
```

1. テーブルの下に右寄せテキストを配置
2. フィールドを挿入:
   - `小計: [subtotal]`
   - `消費税(10%): [tax]`
   - `合計金額: [total]`

**7. フッターの設計**

```
お支払期限: 2025年1月31日
振込先: ○○銀行 △△支店 普通 1234567
────────────────────────────────
株式会社ABC  〒100-0001 東京都...
Tel: 03-1234-5678  Email: info@example.com
```

1. フッターエリアをダブルクリック
2. お支払い条件、振込先情報を配置
3. 会社情報を配置

### 3. フィールドの定義

LibreOfficeでは、動的なデータを挿入するためにフィールドを使用します。

#### 日付フィールド

1. 挿入 → フィールド → 日付
2. 書式を選択: "YYYY年MM月DD日"

#### ユーザー定義フィールド

1. 挿入 → フィールド → その他のフィールド
2. 「変数」タブを選択
3. 種類: "ユーザー定義フィールド"
4. 名前: `customer_name`
5. 値: （空白のまま）
6. 挿入をクリック

同様に以下のフィールドを定義:
- `customer_address`
- `invoice_number`
- `subtotal`
- `tax`
- `total`

### 4. Calc（表計算）での帳票設計

#### 例: 見積書テンプレート

**1. 新規スプレッドシートの作成**

1. LibreOffice Calcを起動
2. ファイル → 新規作成 → 表計算ドキュメント

**2. ヘッダーの設計**

セルA1-F1を結合して "見積書" を中央揃えで配置（24pt、太字）

**3. 見積先情報の配置**

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 見積日 | 2025-01-15 | | | 見積番号 | EST-2025-001 |
| お客様名 | 株式会社サンプル | | | 有効期限 | 2025-01-31 |

**4. 見積明細テーブルの設計**

| No. | 商品名 | 数量 | 単価 | 小計 |
|-----|--------|------|------|------|
| 1   | 商品A  | 10   | 1,000 | 10,000 |
| 2   | 商品B  | 5    | 2,000 | 10,000 |

セル範囲: A6-E20

**5. 数式の設定**

小計セル（E7）:
```
=C7*D7
```

合計セル（E21）:
```
=SUM(E7:E20)
```

消費税セル（E22）:
```
=E21*0.1
```

合計金額セル（E23）:
```
=E21+E22
```

**6. セルの書式設定**

1. 単価・小計列を選択
2. 書式 → セル
3. 「数値」カテゴリを選択
4. 書式コード: `¥#,##0`

### 5. テンプレートとして保存

#### Writerテンプレートの保存

1. ファイル → テンプレートとして保存
2. 新規テンプレート名: "請求書テンプレート"
3. カテゴリ: "ビジネス"
4. 保存をクリック

保存先: `~/.config/libreoffice/4/user/template/`（Linux）

#### Calcテンプレートの保存

1. ファイル → テンプレートとして保存
2. 新規テンプレート名: "見積書テンプレート"
3. カテゴリ: "ビジネス"
4. 保存をクリック

### 6. 差し込み印刷（Mail Merge）

データベースと連携して、複数の請求書を一括生成します。

#### データソースの準備

**CSVファイル例（`customers.csv`）:**

```csv
customer_name,address,invoice_number,subtotal,tax,total
株式会社A,東京都千代田区1-1-1,INV-001,100000,10000,110000
株式会社B,大阪府大阪市2-2-2,INV-002,200000,20000,220000
```

#### 差し込み印刷の実行

1. ツール → 差し込み印刷ウィザード
2. 「文書の種類」: 手紙を選択
3. 「差し込み印刷の開始」: 現在の文書を使用
4. 「宛先の選択」: 既存のアドレス帳を使用 → その他のアドレス帳
5. CSVファイルを選択
6. 「フィールドの挿入」: customer_name、address等を挿入
7. 「差し込み印刷の完了」: 個々のドキュメントの編集
8. すべてのレコードに対して請求書が生成される

### 7. PDF出力仕様の定義

#### PDF/A形式でのエクスポート

1. ファイル → PDFとしてエクスポート
2. 「一般」タブ:
   - **範囲**: すべて
   - **画像**: ロスレス圧縮
3. 「初期表示」タブ:
   - **ページ**: 1ページ目
   - **ズーム**: ページ全体
4. 「ユーザーインターフェイス」タブ:
   - **ウィンドウオプション**: タイトルを表示
5. 「リンク」タブ:
   - ブックマークをPDFに変換
6. **PDF/A-1b**にチェック（長期保存用）
7. エクスポートをクリック

### 8. Pythonマクロによる自動化

LibreOfficeでは、Pythonマクロで帳票生成を自動化できます。

#### 例: 請求書PDF自動生成マクロ

```python
import uno
from com.sun.star.beans import PropertyValue

def generate_invoice_pdf():
    # LibreOffice接続
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

    # テンプレートを開く
    doc_url = "file:///path/to/invoice_template.odt"
    doc = desktop.loadComponentFromURL(doc_url, "_blank", 0, ())

    # フィールドに値を設定
    text_fields = doc.getTextFields()
    enum = text_fields.createEnumeration()

    while enum.hasMoreElements():
        field = enum.nextElement()
        if field.supportsService("com.sun.star.text.TextField.User"):
            field_name = field.getPropertyValue("Content")
            if field_name == "customer_name":
                field.setPropertyValue("Content", "株式会社サンプル")
            elif field_name == "invoice_number":
                field.setPropertyValue("Content", "INV-2025-001")

    # PDFエクスポート
    pdf_url = "file:///path/to/output/invoice.pdf"
    filter_data = (
        PropertyValue("FilterName", 0, "writer_pdf_Export", 0),
    )
    doc.storeToURL(pdf_url, filter_data)
    doc.close(True)

# マクロ実行
generate_invoice_pdf()
```

#### マクロの登録

1. ツール → マクロ → マクロの管理 → Python
2. 「作成」をクリック
3. 上記コードを貼り付け
4. 保存してマクロを実行

### 9. 帳票項目定義表の作成

基本設計では、帳票項目の詳細仕様を表で定義します。

#### 帳票項目定義表（Calc）

| 項目名 | データ型 | 桁数 | 必須 | デフォルト | 書式 | DB項目名 | 備考 |
|--------|---------|------|------|----------|------|---------|------|
| 請求書番号 | String | 20 | ○ | - | INV-YYYY-nnn | invoice_number | 年度+連番 |
| 請求日 | Date | - | ○ | 当日 | YYYY年MM月DD日 | invoice_date | - |
| 顧客名 | String | 100 | ○ | - | - | customer_name | - |
| 商品コード | String | 20 | ○ | - | - | product_code | - |
| 数量 | Integer | 10 | ○ | 1 | #,##0 | quantity | 3桁区切り |
| 単価 | Decimal | 10,2 | ○ | - | ¥#,##0 | unit_price | 通貨形式 |
| 小計 | Decimal | 10,2 | - | - | ¥#,##0 | subtotal | 数量×単価 |
| 合計金額 | Decimal | 10,2 | - | - | ¥#,##0 | total_amount | SUM(小計) |
| 消費税 | Decimal | 10,2 | - | - | ¥#,##0 | tax_amount | 合計×10% |

### 10. 多言語対応帳票の設計

#### 日本語・英語対応請求書

1. Writer文書で2つのセクションを作成
2. セクション1: 日本語版
3. セクション2: 英語版
4. 条件付き表示を設定（言語パラメータで切り替え）

### 11. デジタル署名の追加

#### PDF署名の設定

1. ファイル → PDFとしてエクスポート
2. 「デジタル署名」タブ
3. 証明書を選択
4. 署名理由を入力
5. エクスポートをクリック

### 12. ベストプラクティス

#### スタイルの統一

1. 書式 → スタイル → スタイルの管理
2. 段落スタイル、文字スタイルを定義:
   - "見出し1": 24pt、太字
   - "本文": 11pt、標準
   - "表ヘッダー": 12pt、太字、背景色グレー
3. テンプレート全体で統一したスタイルを使用

#### バージョン管理

1. ファイル → バージョン
2. 「新しいバージョンを保存」
3. コメントを入力（例: "消費税率を8%から10%に変更"）

## 公式ドキュメント

- **公式サイト**: [LibreOffice](https://www.libreoffice.org/)
- **ユーザーガイド**: [Getting Started Guide](https://documentation.libreoffice.org/)
- **Writer Guide**: [Writer Guide (PDF)](https://documentation.libreoffice.org/en/english-documentation/writer/)
- **Calc Guide**: [Calc Guide (PDF)](https://documentation.libreoffice.org/en/english-documentation/calc/)
- **マクロガイド**: [Macros Guide](https://wiki.documentfoundation.org/Macros)
- **API Documentation**: [LibreOffice API](https://api.libreoffice.org/)

## 学習リソース

- **チュートリアル**: [LibreOffice Tutorials](https://www.tutorialspoint.com/libreoffice/index.htm)
- **YouTube**: [LibreOffice Tutorial](https://www.youtube.com/results?search_query=libreoffice+tutorial)
- **コミュニティ**: [Ask LibreOffice](https://ask.libreoffice.org/)

## 関連リンク

- [Apache OpenOffice](https://www.openoffice.org/)（類似オフィススイート）
- [ONLYOFFICE](https://www.onlyoffice.com/)（クラウド対応オフィス）
- [PDF/A標準](https://www.pdfa.org/)（長期保存用PDF規格）
