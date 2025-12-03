# Crystal Reports

## 概要

Crystal Reportsは、SAP社が提供するエンタープライズレポーティングツールです。データベース、Excel、XMLからデータを取得し、ビジュアルなレポート（帳票、グラフ、ダッシュボード）を作成します。30年以上の歴史を持ち、財務レポート、在庫管理、販売分析等のビジネスレポート作成に特化し、.NET、Java、Webアプリケーションに統合できます。

## 主な機能

### 1. レポートデザイン
- **ドラッグ&ドロップ**: GUIレポートデザイナー
- **テンプレート**: 定型レポートテンプレート
- **グラフ**: 棒グラフ、円グラフ、折れ線グラフ
- **クロス集計**: ピボットテーブル風レポート

### 2. データソース
- **RDBMS**: Oracle、SQL Server、MySQL、PostgreSQL
- **ODBC/OLE DB**: 汎用データベース接続
- **Excel/CSV**: ファイルデータ
- **XML**: XML データソース
- **SAP**: SAP ERP連携

### 3. 数式・ロジック
- **Crystal Syntax**: レポート専用言語
- **条件分岐**: If-Then-Else
- **集計関数**: Sum、Avg、Count、Max、Min
- **変数**: グローバル変数、共有変数

### 4. 出力形式
- **PDF**: 標準出力形式
- **Excel**: .xlsx、.xls
- **Word**: .docx
- **HTML**: Webブラウザ表示
- **CSV**: データエクスポート

### 5. パラメータ化
- **動的パラメータ**: ユーザー入力
- **デフォルト値**: 初期値設定
- **カスケード**: 連動パラメータ
- **複数値**: 複数選択

### 6. サブレポート
- **ネストレポート**: レポート内レポート
- **リンク**: メインレポート連携
- **独立データソース**: 別データソース使用

## 利用方法

### 基本レポート作成

```
1. Crystal Reports Designer起動
2. New → Standard Report
3. データソース選択:
   - Database → ODBC → SQL Server
   - 接続情報入力: Server、Database
4. テーブル選択:
   - Orders、Customers テーブル追加
5. フィールド配置:
   - OrderID、CustomerName、OrderDate、Total
6. グループ化:
   - Insert → Group → CustomerName
7. 集計追加:
   - Insert → Summary → Sum(Total)
8. プレビュー: Preview タブで確認
```

### .NET統合

```csharp
// C# レポート統合例
using CrystalDecisions.CrystalReports.Engine;
using CrystalDecisions.Shared;

public void GenerateReport()
{
    ReportDocument reportDocument = new ReportDocument();
    reportDocument.Load(@"C:\Reports\SalesReport.rpt");
    
    // パラメータ設定
    reportDocument.SetParameterValue("StartDate", DateTime.Now.AddDays(-30));
    reportDocument.SetParameterValue("EndDate", DateTime.Now);
    
    // PDF エクスポート
    reportDocument.ExportToDisk(ExportFormatType.PortableDocFormat, @"C:\Output\SalesReport.pdf");
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Crystal Reports for Visual Studio** | 💰 $795 | .NET統合、1開発者ライセンス |
| **SAP Crystal Reports 2020** | 💰 $495 | スタンドアロン版 |
| **Crystal Reports Server** | 💰 要問い合わせ | エンタープライズ配信 |

## メリット

### ✅ 主な利点

1. **成熟**: 30年以上の歴史
2. **豊富なテンプレート**: 帳票テンプレート多数
3. **データソース**: RDBMS、Excel、XML対応
4. **.NET統合**: Visual Studio統合
5. **PDF出力**: 高品質PDF
6. **クロス集計**: ピボットテーブル機能
7. **パラメータ化**: 動的レポート
8. **サブレポート**: 複雑なレポート構造
9. **エンタープライズ**: 大規模配信対応
10. **日本語対応**: 日本語レポート作成可能

## デメリット

### ❌ 制約・課題

1. **高価**: ライセンス費用高額
2. **レガシー**: モダンなUIではない
3. **学習曲線**: Crystal Syntax習得必要
4. **パフォーマンス**: 大量データで遅延
5. **Web統合**: Web統合が複雑
6. **ライセンス**: ランタイムライセンス必要
7. **SAP依存**: SAP製品依存
8. **モダンBI**: Tableau、Power BIより機能少ない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Microsoft Power BI** | モダンBI | Crystal Reportsよりビジュアル |
| **Tableau** | データ可視化 | Crystal Reportsよりインタラクティブ |
| **SSRS** | Microsoft レポーティング | Crystal Reportsと類似、SQL Server統合 |
| **JasperReports** | オープンソース | Crystal Reportsと類似、無料 |

## 公式リンク

- **公式サイト**: [https://www.sap.com/products/technology-platform/crystal-reports.html](https://www.sap.com/products/technology-platform/crystal-reports.html)
- **ドキュメント**: [https://help.sap.com/docs/SAP_CRYSTAL_REPORTS](https://help.sap.com/docs/SAP_CRYSTAL_REPORTS)

## 関連ドキュメント

- [レポーティングツール一覧](../レポーティングツール/)
- [レポーティングベストプラクティス](../../best-practices/reporting.md)

---

**カテゴリ**: レポーティングツール  
**対象工程**: レポート作成、データ分析  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
