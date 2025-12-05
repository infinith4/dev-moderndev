# Excel / Google Sheets

## 概要

Microsoft ExcelとGoogle Sheetsは、世界で最も広く使用されている表計算ソフトウェアです。データ入力、計算、グラフ作成、ピボットテーブル、マクロ（VBA、Apps Script）で、財務分析、プロジェクト管理、データ分析、レポート作成を支援します。Excelはデスクトップアプリケーション（Microsoft Office）、Google Sheetsはクラウドベース（Google Workspace）で、リアルタイムコラボレーション、データベース連携、BI統合が可能です。

## 主な機能

### 1. データ管理
- **表形式**: 行・列データ
- **フィルター**: データフィルタリング
- **並び替え**: ソート
- **データ検証**: 入力制限

### 2. 数式・関数
- **基本関数**: SUM、AVERAGE、COUNT
- **論理関数**: IF、AND、OR、VLOOKUP、XLOOKUP
- **日付関数**: TODAY、DATE、DATEDIF
- **統計関数**: STDEV、CORREL、FORECAST

### 3. ピボットテーブル
- **集計**: データ集計
- **クロス集計**: 多次元分析
- **グループ化**: カテゴリ別集計
- **計算フィールド**: カスタム計算

### 4. グラフ・可視化
- **グラフ**: 棒グラフ、折れ線グラフ、円グラフ
- **スパークライン**: セル内グラフ
- **条件付き書式**: データバー、カラースケール
- **ダッシュボード**: ビジュアルダッシュボード

### 5. マクロ・自動化
- **Excel VBA**: Visual Basic for Applications
- **Google Apps Script**: JavaScript風スクリプト
- **Power Query**: データ変換（Excel）
- **Power Automate**: ワークフロー自動化（Excel）

### 6. コラボレーション
- **Excel**: OneDrive共有、共同編集
- **Google Sheets**: リアルタイム共同編集、コメント
- **バージョン履歴**: 変更履歴追跡
- **権限管理**: 閲覧・編集権限

## 利用方法

### 基本数式

```excel
// Excel / Google Sheets 数式例

// 合計
=SUM(A1:A10)

// 平均
=AVERAGE(B1:B10)

// 条件付き合計
=SUMIF(C1:C10, ">100")

// VLOOKUP
=VLOOKUP(E2, A1:B10, 2, FALSE)

// XLOOKUP (Excel 365)
=XLOOKUP(E2, A1:A10, B1:B10)

// IF関数
=IF(A1 > 100, "High", "Low")

// ネストIF
=IF(A1 >= 90, "A", IF(A1 >= 80, "B", "C"))
```

### ピボットテーブル（Excel）

```
1. データ範囲選択
2. Insert → PivotTable
3. フィールド設定:
   - Rows: Product Category
   - Columns: Month
   - Values: Sum of Sales
4. 分析:
   - カテゴリ別・月別売上集計
```

### Google Sheets Apps Script

```javascript
// Google Sheets Apps Script例

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('カスタムメニュー')
    .addItem('データ更新', 'updateData')
    .addToUi();
}

function updateData() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Data');
  var lastRow = sheet.getLastRow();
  
  // 最終行にタイムスタンプ
  sheet.getRange(lastRow + 1, 1).setValue(new Date());
  
  // 外部APIからデータ取得
  var response = UrlFetchApp.fetch('https://api.example.com/data');
  var data = JSON.parse(response.getContentText());
  
  // データ書き込み
  sheet.getRange(lastRow + 1, 2).setValue(data.value);
}

// 定期実行トリガー設定
function createTimeDrivenTriggers() {
  ScriptApp.newTrigger('updateData')
    .timeBased()
    .everyHours(1)
    .create();
}
```

### Excel VBA

```vb
' Excel VBA例

Sub UpdateReport()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Data")
    
    ' 最終行取得
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    ' データ更新
    ws.Cells(lastRow + 1, 1).Value = Now()
    ws.Cells(lastRow + 1, 2).Value = "New Data"
    
    ' ピボットテーブル更新
    Dim pt As PivotTable
    For Each pt In ws.PivotTables
        pt.RefreshTable
    Next pt
    
    MsgBox "レポート更新完了"
End Sub
```

### データベース連携（Excel）

```excel
1. Data → Get Data → From Database → SQL Server
2. 接続情報入力:
   - Server: localhost
   - Database: SalesDB
3. テーブル選択: Orders
4. Load → データインポート
5. Refresh: データ更新
```

### Google Sheets API統合

```javascript
// Google Sheets API (Node.js)
const { google } = require('googleapis');
const sheets = google.sheets('v4');

async function appendData(auth) {
  const spreadsheetId = 'YOUR_SPREADSHEET_ID';
  const range = 'Sheet1!A1';
  const values = [
    ['Date', 'Sales', 'Region'],
    ['2024-01-01', 1000, 'East'],
  ];
  
  await sheets.spreadsheets.values.append({
    auth,
    spreadsheetId,
    range,
    valueInputOption: 'USER_ENTERED',
    resource: { values },
  });
}
```

### 条件付き書式

```
Excel / Google Sheets:

1. 範囲選択: A1:A10
2. Home → Conditional Formatting → Data Bars
3. ルール設定:
   - Minimum: 0
   - Maximum: 1000
   - Color: Blue
4. 結果: 値に応じてデータバー表示
```

## エディション・料金

| ツール | エディション | 価格 | 特徴 |
|--------|-------------|------|------|
| **Microsoft Excel** | Microsoft 365 Personal | 💰 ¥1,490/月 | 1ユーザー、1TB OneDrive |
| | Microsoft 365 Business | 💰 ¥900/ユーザー/月 | ビジネス向け |
| | Excel 2021 | 💰 ¥19,800（買い切り） | 永続ライセンス |
| **Google Sheets** | 個人（無料） | 🟢 無料 | 15GB Googleドライブ |
| | Google Workspace Business | 💰 $12/ユーザー/月 | 2TB、ビジネス機能 |

## メリット

### ✅ 主な利点

1. **普及率**: 世界標準ツール
2. **多機能**: 計算、グラフ、マクロ
3. **ピボットテーブル**: 高度な集計
4. **マクロ**: VBA、Apps Script自動化
5. **データベース連携**: SQL Server、MySQL等
6. **テンプレート**: 豊富なテンプレート
7. **コラボレーション**: 共同編集（Google Sheets特に優れる）
8. **モバイル対応**: iOS、Android
9. **Power BI連携**: Excel→Power BI（Excel）
10. **API**: Google Sheets API（Google Sheets）

## デメリット

### ❌ 制約・課題

1. **大規模データ**: 100万行制限（Excel）、500万セル（Google Sheets）
2. **パフォーマンス**: 大量データで遅延
3. **バージョン管理**: Git非対応
4. **複雑な計算**: 専用BIツールより劣る
5. **セキュリティ**: マクロウイルスリスク（Excel VBA）
6. **コスト**: Microsoft 365サブスクリプション（Excel）
7. **オフライン**: Google Sheetsはオフライン制限的
8. **スキーマレス**: データベースより構造化弱い

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **LibreOffice Calc** | オープンソース表計算 | Excel互換、無料 |
| **Airtable** | クラウドデータベース | Excelより構造化 |
| **Notion** | オールインワン | Excelよりコラボレーション強化 |
| **Power BI** | BI専用ツール | Excelより高度な分析 |
| **Tableau** | データ可視化 | Excelより可視化特化 |

## 公式リンク

### Microsoft Excel
- **公式サイト**: [https://www.microsoft.com/microsoft-365/excel](https://www.microsoft.com/microsoft-365/excel)
- **ドキュメント**: [https://support.microsoft.com/excel](https://support.microsoft.com/excel)
- **VBA リファレンス**: [https://docs.microsoft.com/office/vba/api/overview/excel](https://docs.microsoft.com/office/vba/api/overview/excel)

### Google Sheets
- **公式サイト**: [https://www.google.com/sheets/about/](https://www.google.com/sheets/about/)
- **ドキュメント**: [https://support.google.com/docs/topic/9054603](https://support.google.com/docs/topic/9054603)
- **Apps Script**: [https://developers.google.com/apps-script](https://developers.google.com/apps-script)

## 関連ドキュメント

- [表計算ツール一覧](../表計算ツール/)
- [Power BI](../BIツール/Power_BI.md)
- [Airtable](../データベースツール/Airtable.md)
- [表計算ベストプラクティス](../../best-practices/spreadsheets.md)

---

**カテゴリ**: 表計算ツール  
**対象工程**: データ分析、レポート作成、プロジェクト管理  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
