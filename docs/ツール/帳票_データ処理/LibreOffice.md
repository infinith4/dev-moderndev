# LibreOffice

## 概要

LibreOfficeは、無料のオープンソースオフィススイートで、Writer（ワープロ）、Calc（表計算）、Draw（図形描画）等を備えています。帳票レイアウト設計、帳票テンプレート作成、PDF出力、差し込み印刷、Pythonマクロによる自動化が可能で、Microsoft Officeとの高い互換性を持つクロスプラットフォームツールです。

## 主な特徴

| 項目 | 内容 |
|------|------|
| ライセンス | MPL 2.0（無料で商用利用可能） |
| プラットフォーム | Windows、macOS、Linux |
| Office互換性 | Microsoft Officeとの高い互換性 |
| PDF出力 | PDF/A準拠のPDF出力対応 |
| マクロ | Python/Basicマクロで自動化可能 |
| テンプレート | .ott（Writer）、.ots（Calc）形式 |

## 主な機能

### Writer（ワープロ）

| 機能 | 説明 |
|------|------|
| ページスタイル | 用紙サイズ、余白、ヘッダー/フッター設定 |
| テンプレート | 再利用可能な帳票テンプレートの作成 |
| 差し込み印刷 | データベース/CSVと連携した一括帳票生成 |
| フィールド | 日付、ユーザー定義フィールドの挿入 |

### Calc（表計算）

| 機能 | 説明 |
|------|------|
| 数式・集計 | SUM、VLOOKUPなどの関数利用 |
| セル書式 | 通貨形式（`¥#,##0`）、日付形式 |
| 印刷設定 | 印刷範囲、ページ設定、拡大縮小 |
| テンプレート | 見積書、請求書テンプレート |

### 共通機能

| 機能 | 説明 |
|------|------|
| PDF/Aエクスポート | 長期保存用PDF出力 |
| デジタル署名 | PDF署名の追加 |
| スタイル管理 | 段落・文字スタイルの統一管理 |
| バージョン管理 | 文書内バージョン履歴 |

## インストールとセットアップ

公式URL:
- [LibreOffice 公式サイト](https://www.libreoffice.org/)
- [LibreOffice ドキュメント](https://documentation.libreoffice.org/)

1. [LibreOffice公式サイト](https://www.libreoffice.org/)にアクセス
2. 「ダウンロード」をクリックし、OS別のインストーラーをダウンロード
3. インストーラーを実行
4. 日本語言語パックをインストール（必要に応じて）

## 基本的な使い方

### 1. Writer で請求書テンプレートを作成

**ページ設定:**
1. 書式 → ページスタイル
2. 用紙サイズ: A4 (210 x 297 mm)、余白: 上下左右 20mm
3. ヘッダー/フッターを有効化

**請求先情報の配置:**
```
請求先:
株式会社サンプル
〒100-0001
東京都千代田区千代田1-1-1
ご担当者: 山田 太郎 様
```

表（2列 x 4行）を挿入し、ラベルとデータフィールドを配置

**請求明細テーブル:**
表（5列 x 10行）を挿入し、「No.」「商品名」「数量」「単価」「小計」の見出しを設定

### 2. Calc で見積書テンプレートを作成

**数式の設定:**

```
小計セル（E7）: =C7*D7
合計セル（E21）: =SUM(E7:E20)
消費税セル（E22）: =E21*0.1
合計金額セル（E23）: =E21+E22
```

**セル書式:** 単価・小計列の書式コードを `¥#,##0` に設定

### 3. テンプレートとして保存

1. ファイル → テンプレートとして保存
2. テンプレート名を入力（例: "請求書テンプレート"）
3. カテゴリ: "ビジネス" を選択

### 4. 差し込み印刷

**CSVファイル例:**
```csv
customer_name,address,invoice_number,subtotal,tax,total
株式会社A,東京都千代田区1-1-1,INV-001,100000,10000,110000
株式会社B,大阪府大阪市2-2-2,INV-002,200000,20000,220000
```

1. ツール → 差し込み印刷ウィザード
2. CSVファイルをデータソースとして選択
3. フィールドを挿入
4. すべてのレコードに対して帳票を生成

### 5. Pythonマクロによる自動化

```python
import uno
from com.sun.star.beans import PropertyValue

def generate_invoice_pdf():
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
    doc = desktop.loadComponentFromURL(
        "file:///path/to/invoice_template.odt", "_blank", 0, ()
    )

    # PDFエクスポート
    pdf_url = "file:///path/to/output/invoice.pdf"
    filter_data = (
        PropertyValue("FilterName", 0, "writer_pdf_Export", 0),
    )
    doc.storeToURL(pdf_url, filter_data)
    doc.close(True)
```

### 6. PDF出力仕様

1. ファイル → PDFとしてエクスポート
2. 一般タブ: 範囲、画像圧縮を設定
3. PDF/A-1bにチェック（長期保存用）
4. デジタル署名タブで証明書を選択（必要に応じて）

## 他ツールとの比較

### LibreOffice vs Microsoft Office

| 機能 | LibreOffice | Microsoft Office |
|------|-------------|-----------------|
| 料金 | 無料 | 有料（サブスクリプション or 買い切り） |
| 互換性 | Microsoft形式に高い互換性 | ネイティブ |
| マクロ | Python/Basic | VBA |
| プラットフォーム | Windows/macOS/Linux | Windows/macOS |
| テンプレート | 少なめ | 豊富 |

### LibreOffice vs ONLYOFFICE

| 機能 | LibreOffice | ONLYOFFICE |
|------|-------------|-----------|
| デスクトップ | 強力 | 対応 |
| クラウド連携 | 限定的 | ネイティブ |
| 共同編集 | 限定的 | 対応 |
| Office互換性 | 高い | 高い |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| 帳票テンプレート作成 | 定型帳票の設計 | Writer/Calcで請求書・見積書テンプレートを作成 |
| PDF帳票出力 | PDF/A準拠の帳票生成 | PDF/A形式でのエクスポートと長期保存 |
| 差し込み印刷 | 一括帳票生成 | CSVデータと連携して複数の帳票を一括生成 |
| マクロ自動化 | 帳票生成の自動化 | Pythonマクロでテンプレートの値設定とPDF出力を自動化 |

## ベストプラクティス

### 1. スタイルの統一

- 段落スタイル、文字スタイルを定義して統一
- テンプレート全体で一貫したフォント・サイズ・色を使用

### 2. テンプレート管理

- テンプレートファイル（.ott/.ots）として保存
- バージョン管理にはGit LFSの活用を検討

### 3. 帳票項目定義

- 帳票項目定義表を作成し、データ型・桁数・書式・DB項目名を文書化

## トラブルシューティング

### よくある問題と解決策

#### 1. Microsoft Officeとのレイアウト崩れ

```
原因: フォントや書式設定の互換性差異
解決策: 標準フォント（Noto Sans等）を使用し、PDF形式で配布する
```

#### 2. 差し込み印刷でCSVの文字化け

```
原因: CSVファイルのエンコーディングが不一致
解決策: UTF-8（BOMあり）でCSVを保存し、LibreOfficeのインポート時にエンコーディングを指定する
```

#### 3. Pythonマクロが動作しない

```
原因: LibreOfficeのリスナーが起動していない
解決策: `soffice --accept="socket,host=localhost,port=2002;urp;"` で起動する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: [https://www.libreoffice.org/](https://www.libreoffice.org/)
- ユーザーガイド: [https://documentation.libreoffice.org/](https://documentation.libreoffice.org/)
- API Documentation: [https://api.libreoffice.org/](https://api.libreoffice.org/)

### コミュニティ
- Ask LibreOffice: [https://ask.libreoffice.org/](https://ask.libreoffice.org/)
- マクロガイド: [https://wiki.documentfoundation.org/Macros](https://wiki.documentfoundation.org/Macros)

## まとめ

LibreOfficeは、以下の場面で特に有用です:

1. **無料での帳票テンプレート作成** - コストをかけずに請求書・見積書等の帳票テンプレートを設計
2. **PDF/A準拠の帳票出力** - 長期保存要件に対応したPDF出力とデジタル署名
3. **マクロによる帳票自動化** - Pythonマクロでテンプレートへのデータ設定とPDF出力を自動化

Microsoft Officeとの高い互換性を持ちながら、無料で商用利用可能なオフィススイートとして活用できます。
