# JasperReports（帳票設計）

## 概要

JasperReportsは、オープンソースのJava帳票ツールで、基本設計フェーズでは帳票レイアウト設計、帳票項目定義、帳票出力仕様の作成に活用します。XMLベースの帳票テンプレート(JRXML)を設計し、PDF、Excel、HTML等の多様な形式での出力仕様を定義できます。

### 基本設計フェーズでの活用

- **帳票レイアウト設計**: ヘッダー、詳細、フッター等の配置設計
- **帳票項目定義**: データソースと帳票項目のマッピング
- **帳票出力仕様**: PDF/Excel/HTML等の出力形式仕様
- **集計・グループ化仕様**: サブレポート、グループ集計の設計
- **テンプレート作成**: 再利用可能な帳票テンプレートの設計

### 料金プラン

- **JasperReports Library**: 完全無料（LGPL v3.0ライセンス）
- **Jaspersoft Studio**: 完全無料（帳票デザインツール）
- **JasperReports Server**: Community Edition無料、Commercial版有料

### メリット・デメリット

**メリット**
- 完全無料で商用利用可能
- Java環境でのデファクトスタンダード
- PDF、Excel、Word、HTML等の多様な出力形式に対応
- Jaspersoft Studioでビジュアル設計が可能
- サブレポート、クロス集計、チャート等の高度な機能
- Spring Bootとの統合が容易

**デメリット**
- Java環境が必須
- 学習コストが高い
- 複雑なレイアウトの設計が難しい
- JRXMLファイルの手動編集が必要な場合がある

## 利用方法

### 1. Jaspersoft Studioのインストール

1. [Jaspersoft Community](https://community.jaspersoft.com/project/jaspersoft-studio/releases)にアクセス
2. OS別のインストーラーをダウンロード:
   - Windows: `TIB_js-studiocomm_x.x.x_windows_x86_64.exe`
   - macOS: `TIB_js-studiocomm_x.x.x_macos_x86_64.dmg`
   - Linux: `TIB_js-studiocomm_x.x.x_linux_x86_64.tgz`
3. インストーラーを実行
4. JDK 11以上が必要（事前にインストール）

### 2. 新規レポートプロジェクトの作成

1. Jaspersoft Studioを起動
2. File → New → Jasper Report
3. テンプレートを選択:
   - **Blank A4**: 白紙のA4縦
   - **Blank A4 Landscape**: A4横
   - **Table**: 表形式
   - **Invoice**: 請求書テンプレート
4. レポート名を入力（例: `Invoice_Report`）
5. 保存先フォルダを選択
6. "Finish"をクリック

### 3. 帳票レイアウトの設計

#### 帳票の構成要素

JasperReportsの帳票は以下のバンド（帯）で構成されます:

- **Title**: タイトル（1回のみ表示）
- **Page Header**: ページヘッダー（各ページ上部）
- **Column Header**: 列ヘッダー（表の見出し）
- **Detail**: 詳細（データ行ごとに繰り返し）
- **Column Footer**: 列フッター
- **Page Footer**: ページフッター（各ページ下部）
- **Summary**: サマリー（最終ページのみ）

#### 例: 請求書の帳票設計

**1. タイトルバンドの設計**

1. Titleバンドをクリック
2. 高さを100pxに設定
3. Paletteから「Static Text」を追加
4. テキスト: "請求書"
5. フォント: ゴシック、24px、太字

**2. ページヘッダーの設計**

```
┌─────────────────────────────────┐
│ 請求書番号: INV-2025-001         │
│ 請求日: 2025年1月15日           │
│ 顧客名: 株式会社サンプル         │
│ 宛先: 〒100-0001 東京都...      │
└─────────────────────────────────┘
```

1. Page Headerバンドに「Static Text」を追加: "請求書番号:"
2. 「Text Field」を追加して、フィールド式: `$F{invoice_number}`
3. 同様に、請求日、顧客名、宛先を配置

**3. 列ヘッダーの設計**

| 商品コード | 商品名 | 数量 | 単価 | 小計 |
|-----------|--------|------|------|------|

1. Column Headerバンドに「Static Text」を5つ配置
2. テキスト: "商品コード", "商品名", "数量", "単価", "小計"
3. 背景色: #E0E0E0
4. 枠線: 上下左右すべて表示

**4. 詳細バンドの設計**

1. Detailバンドに「Text Field」を5つ配置
2. 式を設定:
   - `$F{product_code}`
   - `$F{product_name}`
   - `$F{quantity}`
   - `$F{unit_price}`
   - `$F{subtotal}`
3. 数値フィールドの書式設定:
   - 単価・小計: パターン `#,##0`

**5. サマリーバンドの設計**

```
合計金額: ¥100,000
消費税(10%): ¥10,000
─────────────────────
請求金額: ¥110,000
```

1. Summaryバンドに「Static Text」を追加: "合計金額:"
2. 「Text Field」を追加:
   - 式: `new java.text.DecimalFormat("#,##0").format($V{total_amount})`
3. 同様に消費税、請求金額を配置

### 4. データソースの定義

#### データベース接続の設定

1. 右側の「Repository Explorer」で右クリック
2. "Create Data Adapter" → "Database JDBC Connection"
3. 接続情報を入力:
   - **Name**: MySQL_Production
   - **JDBC Driver**: `com.mysql.cj.jdbc.Driver`
   - **JDBC URL**: `jdbc:mysql://localhost:3306/sales_db`
   - **Username**: root
   - **Password**: ********
4. "Test"をクリックして接続確認
5. "Finish"をクリック

#### SQLクエリの定義

1. レポートデザイナーで右クリック → "Dataset and Query"
2. クエリ言語: SQL
3. SQLを入力:

```sql
SELECT
    i.invoice_number,
    i.invoice_date,
    c.customer_name,
    c.address,
    il.product_code,
    p.product_name,
    il.quantity,
    il.unit_price,
    il.quantity * il.unit_price AS subtotal
FROM
    invoices i
    INNER JOIN customers c ON i.customer_id = c.customer_id
    INNER JOIN invoice_lines il ON i.invoice_id = il.invoice_id
    INNER JOIN products p ON il.product_id = p.product_id
WHERE
    i.invoice_id = $P{invoiceId}
ORDER BY
    il.line_number
```

4. "Read Fields"をクリックしてフィールドを自動取得
5. "OK"をクリック

### 5. パラメータの定義

レポートに外部から値を渡すパラメータを定義します。

1. 左側の「Outline」で「Parameters」を右クリック
2. "Create Parameter"
3. パラメータ設定:
   - **Name**: `invoiceId`
   - **Class**: `java.lang.Long`
   - **Description**: "請求書ID"
4. デフォルト値式: `1L`

### 6. 変数（集計）の定義

#### 合計金額の計算

1. 「Outline」で「Variables」を右クリック
2. "Create Variable"
3. 変数設定:
   - **Name**: `total_amount`
   - **Class**: `java.math.BigDecimal`
   - **Calculation**: Sum
   - **Expression**: `$F{subtotal}`
   - **Initial Value**: `new java.math.BigDecimal(0)`

#### 消費税の計算

1. 別の変数を作成:
   - **Name**: `tax_amount`
   - **Class**: `java.math.BigDecimal`
   - **Calculation**: System
   - **Expression**: `$V{total_amount}.multiply(new java.math.BigDecimal("0.10"))`

### 7. サブレポートの作成

複雑な帳票では、サブレポートを使用して再利用性を高めます。

#### 例: 商品明細サブレポート

1. 新しいレポート `Invoice_Detail_Subreport.jrxml` を作成
2. 詳細バンドに商品明細のレイアウトを設計
3. メインレポートに戻る
4. Detailバンドに「Subreport」を追加
5. サブレポート式: `"Invoice_Detail_Subreport.jasper"`
6. Connection Expression: `$P{REPORT_CONNECTION}`

### 8. グループ化とブレイク

#### カテゴリ別グループ化

1. 「Outline」で「Report」を右クリック
2. "Create Group"
3. グループ名: `CategoryGroup`
4. Group Expression: `$F{category_name}`
5. "Group Header"と"Group Footer"が追加される
6. Group Headerにカテゴリ名を表示
7. Group Footerにカテゴリ別小計を表示

### 9. チャートの追加

#### 売上推移の棒グラフ

1. Paletteから「Chart」→「Bar Chart」を選択
2. Summaryバンドに配置
3. Chart Dataを設定:
   - **Dataset**: クエリを実行して月別売上データを取得
   - **Category Expression**: `$F{month}`
   - **Value Expression**: `$F{sales_amount}`
4. Chart Propertiesでスタイル調整

### 10. 条件付き書式

#### 在庫切れ商品の赤字表示

1. 商品名の「Text Field」を選択
2. Propertiesパネルで「Print When Expression」を設定:

```java
$F{stock_quantity} == 0
```

3. Forecolorを赤に設定: `#FF0000`

### 11. 帳票出力仕様の定義

#### PDF出力設定

1. レポートのプロパティを開く
2. 「Export」セクションで設定:
   - **Page Width**: 595 (A4幅)
   - **Page Height**: 842 (A4高さ)
   - **Orientation**: Portrait
   - **Margin**: Top 20, Bottom 20, Left 20, Right 20

#### Excel出力設定

1. 「Properties」→「Export」→「XLS Metadata」
2. 設定:
   - **Sheet Name**: "請求書"
   - **Column Width**: Auto-fit
   - **Ignore Pagination**: true（改ページを無視）

### 12. プレビューとテスト

1. 上部メニューの「Preview」をクリック
2. パラメータ入力画面で `invoiceId` を入力（例: 1）
3. プレビュー表示で帳票を確認
4. 出力形式を切り替え:
   - PDF: PDFアイコンをクリック
   - Excel: Excelアイコンをクリック
   - HTML: HTMLアイコンをクリック

### 13. JRXMLファイルの構造

設計した帳票は、XML形式のJRXMLファイルとして保存されます。

#### JRXMLの主要要素

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports"
              name="Invoice_Report"
              pageWidth="595"
              pageHeight="842">

    <!-- パラメータ定義 -->
    <parameter name="invoiceId" class="java.lang.Long"/>

    <!-- クエリ定義 -->
    <queryString>
        <![CDATA[
            SELECT * FROM invoices WHERE invoice_id = $P{invoiceId}
        ]]>
    </queryString>

    <!-- フィールド定義 -->
    <field name="invoice_number" class="java.lang.String"/>
    <field name="customer_name" class="java.lang.String"/>

    <!-- 変数定義 -->
    <variable name="total_amount" class="java.math.BigDecimal" calculation="Sum">
        <variableExpression><![CDATA[$F{subtotal}]]></variableExpression>
    </variable>

    <!-- タイトルバンド -->
    <title>
        <band height="100">
            <staticText>
                <reportElement x="0" y="0" width="555" height="50"/>
                <textElement textAlignment="Center">
                    <font size="24" isBold="true"/>
                </textElement>
                <text><![CDATA[請求書]]></text>
            </staticText>
        </band>
    </title>

    <!-- 詳細バンド -->
    <detail>
        <band height="30">
            <textField>
                <reportElement x="0" y="0" width="100" height="30"/>
                <textFieldExpression><![CDATA[$F{product_code}]]></textFieldExpression>
            </textField>
        </band>
    </detail>
</jasperReport>
```

### 14. Spring Bootとの統合

#### Maven依存関係

```xml
<dependency>
    <groupId>net.sf.jasperreports</groupId>
    <artifactId>jasperreports</artifactId>
    <version>6.20.6</version>
</dependency>
```

#### Javaコード例

```java
import net.sf.jasperreports.engine.*;
import java.util.HashMap;
import java.util.Map;

public class ReportService {

    public byte[] generateInvoicePdf(Long invoiceId) throws JRException {
        // JRXMLをコンパイル
        JasperReport jasperReport = JasperCompileManager.compileReport(
            "reports/Invoice_Report.jrxml"
        );

        // パラメータ設定
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("invoiceId", invoiceId);

        // レポート実行
        JasperPrint jasperPrint = JasperFillManager.fillReport(
            jasperReport,
            parameters,
            dataSource.getConnection()
        );

        // PDF出力
        return JasperExportManager.exportReportToPdf(jasperPrint);
    }
}
```

### 15. 帳票設計書の作成

基本設計では、帳票設計書にJasperReportsのレイアウトと仕様を記載します。

#### 帳票設計書の構成

1. **帳票ID・帳票名**: INV-001 / 請求書
2. **出力形式**: PDF、Excel
3. **用紙サイズ**: A4縦
4. **データソース**: `invoices`テーブル、`invoice_lines`テーブル
5. **レイアウト図**: Jaspersoft Studioのプレビュー画像を添付
6. **帳票項目一覧**:

| 項目名 | データ型 | フィールド名 | 書式 | 備考 |
|--------|---------|-------------|------|------|
| 請求書番号 | String | invoice_number | - | - |
| 請求日 | Date | invoice_date | yyyy年MM月dd日 | - |
| 商品コード | String | product_code | - | - |
| 数量 | Integer | quantity | #,##0 | 3桁区切り |
| 単価 | BigDecimal | unit_price | ¥#,##0 | 通貨形式 |

7. **集計仕様**: 合計金額、消費税、請求金額の計算式
8. **出力条件**: `invoiceId`パラメータで請求書を指定

## 公式ドキュメント

- **公式サイト**: [JasperReports](https://community.jaspersoft.com/project/jasperreports-library)
- **Jaspersoft Studio**: [Download](https://community.jaspersoft.com/project/jaspersoft-studio/releases)
- **ユーザーガイド**: [JasperReports Ultimate Guide](https://jasperreports.sourceforge.net/JasperReports-Ultimate-Guide-3.pdf)
- **サンプルレポート**: [Sample Reports](https://jasperreports.sourceforge.net/sample.reference.html)
- **APIドキュメント**: [JavaDoc](http://jasperreports.sourceforge.net/api/)

## 学習リソース

- **チュートリアル**: [JasperReports Tutorial](https://www.tutorialspoint.com/jasper_reports/index.htm)
- **YouTube**: [Jaspersoft Studio Tutorial](https://www.youtube.com/results?search_query=jaspersoft+studio+tutorial)
- **Baeldung**: [Introduction to JasperReports](https://www.baeldung.com/java-jasper-reports)

## 関連リンク

- [Apache POI](https://poi.apache.org/)（Excel操作ライブラリ）
- [iText](https://itextpdf.com/)（PDF生成ライブラリ）
- [BIRT Project](https://www.eclipse.org/birt/)（Eclipse帳票ツール）
