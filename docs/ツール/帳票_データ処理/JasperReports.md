# JasperReports

## 概要

JasperReportsは、オープンソースのJava帳票ライブラリで、XMLベースの帳票テンプレート（JRXML）を使用してPDF、Excel、HTML等の多様な形式でレポートを生成します。Jaspersoft Studioによるビジュアルな帳票設計が可能で、サブレポート、クロス集計、チャート等の高度な機能を備えたJava環境のデファクトスタンダードです。

## 主な特徴

| 項目 | 内容 |
|------|------|
| ライセンス | LGPL v3.0（無料で商用利用可能） |
| 言語 | Java |
| テンプレート形式 | JRXML（XML） |
| デザインツール | Jaspersoft Studio（無料） |
| 出力形式 | PDF、Excel、Word、HTML、CSV等 |
| サーバー | JasperReports Server（Community Edition無料、Commercial版有料） |
| フレームワーク連携 | Spring Bootとの統合が容易 |

## 主な機能

### 帳票レイアウト

| 機能 | 説明 |
|------|------|
| バンド構成 | Title、Page Header、Detail、Page Footer、Summary等 |
| サブレポート | 再利用可能な帳票コンポーネント |
| グループ化 | カテゴリ別グループとブレイク集計 |
| チャート | 棒グラフ、円グラフ、折れ線グラフ等 |

### データ連携

| 機能 | 説明 |
|------|------|
| JDBC接続 | MySQL、PostgreSQL等のデータベース接続 |
| SQLクエリ | レポート内でSQLクエリを定義 |
| パラメータ | 外部から値を渡すパラメータ定義 |
| 変数 | Sum、Count等の集計変数 |

### 出力制御

| 機能 | 説明 |
|------|------|
| PDF出力 | A4サイズ、余白、フォント設定 |
| Excel出力 | シート名、列幅、改ページ制御 |
| 条件付き書式 | データ値に応じた表示制御 |
| 多形式対応 | 1つのテンプレートから複数形式に出力 |

## インストールとセットアップ

公式URL:
- [JasperReports Community](https://community.jaspersoft.com/project/jasperreports-library)
- [Jaspersoft Studio](https://community.jaspersoft.com/project/jaspersoft-studio/releases)

### Jaspersoft Studioのインストール

1. [Jaspersoft Community](https://community.jaspersoft.com/project/jaspersoft-studio/releases)にアクセス
2. OS別のインストーラーをダウンロード
3. インストーラーを実行（JDK 11以上が必要）

### Maven依存関係

```xml
<dependency>
    <groupId>net.sf.jasperreports</groupId>
    <artifactId>jasperreports</artifactId>
    <version>6.20.6</version>
</dependency>
```

## 基本的な使い方

### 1. 新規レポートの作成

1. Jaspersoft Studioを起動
2. File → New → Jasper Report
3. テンプレートを選択（Blank A4、Table、Invoice等）
4. レポート名を入力し、保存先を選択

### 2. 帳票レイアウトの設計

帳票は以下のバンド（帯）で構成されます:

- **Title**: タイトル（1回のみ表示）
- **Page Header**: ページヘッダー（各ページ上部）
- **Column Header**: 列ヘッダー（表の見出し）
- **Detail**: 詳細（データ行ごとに繰り返し）
- **Column Footer**: 列フッター
- **Page Footer**: ページフッター（各ページ下部）
- **Summary**: サマリー（最終ページのみ）

### 3. データソースの定義

```sql
SELECT
    i.invoice_number,
    i.invoice_date,
    c.customer_name,
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

### 4. JRXMLファイルの構造

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports"
              name="Invoice_Report"
              pageWidth="595"
              pageHeight="842">

    <parameter name="invoiceId" class="java.lang.Long"/>

    <queryString>
        <![CDATA[SELECT * FROM invoices WHERE invoice_id = $P{invoiceId}]]>
    </queryString>

    <field name="invoice_number" class="java.lang.String"/>
    <field name="customer_name" class="java.lang.String"/>

    <variable name="total_amount" class="java.math.BigDecimal" calculation="Sum">
        <variableExpression><![CDATA[$F{subtotal}]]></variableExpression>
    </variable>

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

### 5. Spring Bootとの統合

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
            jasperReport, parameters, dataSource.getConnection()
        );

        // PDF出力
        return JasperExportManager.exportReportToPdf(jasperPrint);
    }
}
```

## 他ツールとの比較

### JasperReports vs Apache POI

| 機能 | JasperReports | Apache POI |
|------|--------------|------------|
| 用途 | 帳票レイアウト+出力 | Excel/Wordファイル操作 |
| デザイナー | Jaspersoft Studio（GUI） | なし（コードのみ） |
| 出力形式 | PDF/Excel/HTML等 | Excel/Word |
| 複雑な帳票 | 得意 | 困難 |

### JasperReports vs iText

| 機能 | JasperReports | iText |
|------|--------------|-------|
| 用途 | 帳票テンプレート+データ連携 | PDF生成・操作 |
| テンプレート | JRXML（XML） | コードでレイアウト定義 |
| ライセンス | LGPL v3.0 | AGPL（商用は有料） |
| 適用場面 | 定型帳票 | 動的PDF生成 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| 請求書・納品書 | 定型帳票の自動生成 | JRXMLテンプレートとデータベース連携でPDF出力 |
| 売上レポート | 集計・グラフ付きレポート | グループ集計とチャート機能で可視化 |
| 帳票設計書 | 帳票仕様の定義 | Jaspersoft Studioで帳票レイアウトと項目定義を設計 |
| バッチ帳票出力 | 大量帳票の一括生成 | Spring Boot統合でバッチ処理と連携 |

## ベストプラクティス

### 1. テンプレート設計

- バンド構成を明確にし、各バンドの役割を統一
- 再利用可能な部分はサブレポートに分離
- 数値フィールドには書式パターン（`#,##0`等）を必ず設定

### 2. パフォーマンス

- 大量データの帳票ではページネーションを適切に設定
- JRXMLのコンパイル結果（.jasper）をキャッシュ
- データソースのSQLクエリを最適化

### 3. 運用

- JRXMLファイルはGitでバージョン管理
- 帳票項目定義表を作成し、フィールド名・データ型・書式を文書化
- テスト環境でプレビュー確認後に本番デプロイ

## トラブルシューティング

### よくある問題と解決策

#### 1. 日本語が文字化けする

```
原因: フォント設定が不足している
解決策: IPAフォント等の日本語フォントをクラスパスに追加し、JRXMLでフォント名を指定する
```

#### 2. PDFで改ページが意図しない位置で発生する

```
原因: バンドの高さがページに収まっていない
解決策: 各バンドの高さを確認し、ページサイズと余白を考慮して調整する
```

#### 3. サブレポートにデータが表示されない

```
原因: サブレポートへのパラメータ渡しやConnection設定が不足
解決策: Connection Expression に $P{REPORT_CONNECTION} を設定し、パラメータマッピングを確認する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: [https://community.jaspersoft.com/project/jasperreports-library](https://community.jaspersoft.com/project/jasperreports-library)
- ユーザーガイド: [https://jasperreports.sourceforge.net/JasperReports-Ultimate-Guide-3.pdf](https://jasperreports.sourceforge.net/JasperReports-Ultimate-Guide-3.pdf)
- APIドキュメント: [http://jasperreports.sourceforge.net/api/](http://jasperreports.sourceforge.net/api/)

### コミュニティ
- Jaspersoft Studio: [https://community.jaspersoft.com/project/jaspersoft-studio/releases](https://community.jaspersoft.com/project/jaspersoft-studio/releases)
- Baeldung: [https://www.baeldung.com/java-jasper-reports](https://www.baeldung.com/java-jasper-reports)

## まとめ

JasperReportsは、以下の場面で特に有用です:

1. **Java環境での帳票出力** - Java/Spring Bootアプリケーションに帳票機能を統合
2. **定型帳票のテンプレート管理** - Jaspersoft StudioでGUI設計し、JRXMLでテンプレートを管理
3. **多形式出力** - 1つのテンプレートからPDF、Excel、HTML等の複数形式に対応

Java環境の帳票ツールとして広く採用されており、無料で商用利用可能なデファクトスタンダードです。
