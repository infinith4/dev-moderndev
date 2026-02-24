# CSV Spec Validator

## 概要

CSV Spec Validatorは、CSVファイルがRFC 4180およびプロジェクト固有の仕様に準拠しているかを検証するためのツール・アプローチの総称です。カラム数、データ型、文字エンコーディング、区切り文字、引用符の使用、必須フィールドの存在等をチェックし、データインターフェースの品質を事前に確保します。Python（csvkit、pandas、Great Expectations）、Java、.NET等の各言語で実装が可能です。

## 主な特徴

| 項目 | 内容 |
|------|------|
| 対象 | CSVファイルの形式・内容の検証 |
| 基準 | RFC 4180（Common Format and MIME Type for CSV） |
| 主なツール | csvkit（無料）、pandas（無料）、Great Expectations（無料/有料） |
| 自動化 | CI/CDパイプラインに組み込んで継続的に検証可能 |
| 多言語対応 | Python、Java、.NET等で実装可能 |
| スキーマ定義 | プロジェクト固有の検証ルールをコードで定義 |

## 主な機能

### RFC 4180準拠チェック

| 機能 | 説明 |
|------|------|
| 区切り文字 | カンマ（`,`）区切りの検証 |
| 引用符 | ダブルクォート（`"`）によるフィールド囲みの正当性 |
| 改行 | CRLF改行コードの検証 |
| ヘッダー行 | 先頭行のヘッダー有無の判定 |
| エスケープ | フィールド内のダブルクォートエスケープ（`""`） |

### スキーマバリデーション

| 機能 | 説明 |
|------|------|
| カラム数・名チェック | 期待するカラム数・名との一致検証 |
| データ型チェック | 整数、浮動小数点、日付、メール等の型チェック |
| 必須チェック | NULL/空文字の検出 |
| 値の範囲 | 最小値・最大値・許容値リストの検証 |
| 正規表現 | パターンマッチによるフォーマット検証 |

### エンコーディング・形式チェック

| 機能 | 説明 |
|------|------|
| 文字エンコーディング | UTF-8、Shift_JIS、EUC-JP等の検証 |
| BOM | UTF-8 BOMの有無チェック |
| 行末文字 | LF/CRLF/CRの統一性検証 |
| ファイルサイズ | 最大行数・最大ファイルサイズのチェック |

## インストールとセットアップ

公式URL:
- [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180)
- [csvkit](https://csvkit.readthedocs.io/)
- [Great Expectations](https://greatexpectations.io/)

```bash
# csvkit インストール
pip install csvkit

# pandas インストール
pip install pandas

# Great Expectations インストール
pip install great-expectations
```

## 基本的な使い方

### 1. csvkit（CLIツール）

```bash
# CSVの統計情報表示
csvstat data.csv

# CSVの整合性チェック
csvclean data.csv

# エンコーディング変換
iconv -f SHIFT_JIS -t UTF-8 input.csv > output.csv
```

### 2. Python（pandas + カスタムバリデーション）

```python
import pandas as pd

def validate_csv(filepath: str, schema: dict) -> list[str]:
    """CSVファイルをスキーマに基づいて検証する"""
    errors = []

    try:
        df = pd.read_csv(filepath, encoding=schema.get("encoding", "utf-8"))
    except UnicodeDecodeError:
        return [f"エンコーディングエラー: {schema.get('encoding', 'utf-8')}で読み込めません"]
    except pd.errors.ParserError as e:
        return [f"CSV解析エラー: {e}"]

    # カラム数チェック
    expected_cols = schema.get("columns", [])
    if expected_cols and list(df.columns) != expected_cols:
        errors.append(f"カラム不一致: 期待={expected_cols}, 実際={list(df.columns)}")

    # 必須フィールドチェック
    for col in schema.get("required", []):
        if col in df.columns and df[col].isnull().any():
            null_rows = df[df[col].isnull()].index.tolist()
            errors.append(f"必須フィールド '{col}' にNULLあり: 行 {null_rows}")

    # データ型チェック
    for col, dtype in schema.get("types", {}).items():
        if col in df.columns:
            if dtype == "integer":
                invalid = df[~df[col].apply(lambda x: str(x).isdigit())]
                if not invalid.empty:
                    errors.append(f"'{col}' に整数以外の値: 行 {invalid.index.tolist()}")

    return errors

# 使用例
schema = {
    "encoding": "utf-8",
    "columns": ["id", "name", "email", "amount"],
    "required": ["id", "name", "email"],
    "types": {"id": "integer", "amount": "integer"}
}
errors = validate_csv("data.csv", schema)
```

### 3. Great Expectations

```python
import great_expectations as gx

context = gx.get_context()

datasource = context.sources.add_pandas("my_datasource")
asset = datasource.add_csv_asset("orders", filepath_or_buffer="orders.csv")

batch = asset.get_batch()
batch.expect_column_to_exist("order_id")
batch.expect_column_values_to_not_be_null("order_id")
batch.expect_column_values_to_be_of_type("order_id", "int64")
batch.expect_column_values_to_be_unique("order_id")
batch.expect_column_values_to_match_regex("email", r"^[\w.-]+@[\w.-]+\.\w+$")
batch.expect_column_values_to_be_between("amount", min_value=0, max_value=1000000)

result = batch.validate()
print(f"Success: {result.success}")
```

## CI/CD 統合

### GitHub Actions

```yaml
# .github/workflows/csv-validate.yml
name: CSV Validation

on:
  pull_request:
    paths:
      - 'data/**/*.csv'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install pandas csvkit
      - name: Validate CSV files
        run: |
          for f in data/*.csv; do
            echo "Validating $f..."
            csvclean "$f" || exit 1
            python scripts/validate_csv.py "$f" || exit 1
          done
```

## 他ツールとの比較

### csvkit vs Great Expectations

| 機能 | csvkit | Great Expectations |
|------|--------|-------------------|
| 用途 | CSV専用CLI | 汎用データバリデーションFW |
| 学習コスト | 低い | 中程度 |
| スキーマ定義 | 限定的 | 柔軟なExpectation定義 |
| CI/CD連携 | コマンドラインで簡単 | Checkpoint機能で統合 |
| 対象形式 | CSVのみ | CSV、DB、Spark等 |

### pandas vs Cerberus

| 機能 | pandas | Cerberus |
|------|--------|----------|
| 用途 | データ処理+検証 | スキーマバリデーション専用 |
| 柔軟性 | 自由度が高い | スキーマ定義ベース |
| パフォーマンス | 大容量対応 | 軽量 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| データ受入検証 | インターフェースCSVの品質検証 | スキーマに基づく自動バリデーションで不正データを早期検出 |
| CI/CDパイプライン | データ連携の継続的検証 | PRマージ前にCSVファイルの形式チェックを自動実行 |
| エンコーディング検証 | 文字コードの統一 | UTF-8/Shift_JIS等のエンコーディング整合性チェック |
| データ移行前検証 | 移行データの事前確認 | 移行元CSVデータの型・必須チェックで移行エラーを防止 |

## ベストプラクティス

### 1. スキーマ定義の管理

- バリデーションルール（スキーマ）をコードで定義しGitで管理
- カラム名、データ型、必須/任意、値の範囲を明文化

### 2. エンコーディング統一

- プロジェクト全体でCSVエンコーディングをUTF-8に統一
- Shift_JIS等のレガシーエンコーディングは変換スクリプトを用意

### 3. CI/CD統合

- CSVファイルの変更をトリガーにバリデーションを自動実行
- エラー時はPRのマージをブロック

## トラブルシューティング

### よくある問題と解決策

#### 1. Shift_JISファイルの読み込みエラー

```
原因: UTF-8として読み込もうとしてUnicodeDecodeErrorが発生
解決策: encoding='shift_jis' または encoding='cp932' を指定する
```

#### 2. カラム数が行によって異なる

```
原因: フィールド内にエスケープされていない区切り文字やダブルクォートが含まれている
解決策: csvcleanで問題行を特定し、RFC 4180に準拠するようデータを修正する
```

#### 3. 大容量CSVでメモリ不足

```
原因: pandasが全データをメモリに読み込む
解決策: chunksize パラメータでチャンク分割読み込みを行う
```

## 参考リソース

### 公式ドキュメント
- RFC 4180: [https://datatracker.ietf.org/doc/html/rfc4180](https://datatracker.ietf.org/doc/html/rfc4180)
- csvkit: [https://csvkit.readthedocs.io/](https://csvkit.readthedocs.io/)
- pandas: [https://pandas.pydata.org/](https://pandas.pydata.org/)

### コミュニティ
- Great Expectations: [https://greatexpectations.io/](https://greatexpectations.io/)

## まとめ

CSV Spec Validatorは、以下の場面で特に有用です:

1. **データインターフェースの品質保証** - CSVファイルの受入時に形式・内容を自動検証し、データ連携の信頼性を確保
2. **CI/CDパイプラインでの継続的検証** - PRやデータ更新のタイミングでバリデーションを自動実行
3. **エンコーディング・形式の標準化** - プロジェクト全体のCSV仕様を統一し、文字化けやパースエラーを防止

csvkit、pandas、Great Expectations等のツールを組み合わせることで、柔軟なCSVバリデーション体制を構築できます。
