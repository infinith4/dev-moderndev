# CSV Spec Validator

## 概要

CSV Spec Validatorは、CSVファイルがRFC 4180（Common Format and MIME Type for Comma-Separated Values）およびプロジェクト固有の仕様に準拠しているかを検証するためのツール・アプローチの総称です。カラム数、データ型、文字エンコーディング、区切り文字、引用符の使用、必須フィールドの存在等をチェックし、データインターフェースの品質を事前に確保します。Python（csvkit、pandas、Great Expectations）、Java、.NET等の各言語でバリデーション実装が可能です。

## 主な機能

### 1. RFC 4180準拠チェック

- **区切り文字**: カンマ（`,`）区切りの検証
- **引用符**: ダブルクォート（`"`）によるフィールド囲みの正当性
- **改行**: CRLF改行コードの検証
- **ヘッダー行**: 先頭行のヘッダー有無の判定
- **エスケープ**: フィールド内のダブルクォートエスケープ（`""`）

### 2. スキーマバリデーション

- **カラム数**: 期待するカラム数との一致検証
- **カラム名**: ヘッダー名の正当性チェック
- **データ型**: 整数、浮動小数点、日付、メール等の型チェック
- **必須チェック**: NULL/空文字の検出
- **値の範囲**: 最小値・最大値・許容値リストの検証
- **正規表現**: パターンマッチによるフォーマット検証

### 3. エンコーディング・形式チェック

- **文字エンコーディング**: UTF-8、Shift_JIS、EUC-JP等の検証
- **BOM**: UTF-8 BOMの有無チェック
- **行末文字**: LF/CRLF/CRの統一性検証
- **ファイルサイズ**: 最大行数・最大ファイルサイズのチェック

## 利用方法

### csvkit（Python CLIツール）

```bash
# インストール
pip install csvkit

# CSVの統計情報表示
csvstat data.csv

# CSVの整合性チェック
csvclean data.csv

# エンコーディング変換
iconv -f SHIFT_JIS -t UTF-8 input.csv > output.csv
```

### Python（pandas + カスタムバリデーション）

```python
import pandas as pd
from pathlib import Path

def validate_csv(filepath: str, schema: dict) -> list[str]:
    """CSVファイルをスキーマに基づいて検証する"""
    errors = []

    # エンコーディング・読み込みチェック
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
for e in errors:
    print(f"ERROR: {e}")
```

### Great Expectations（データバリデーションフレームワーク）

```python
import great_expectations as gx

context = gx.get_context()

# データソース設定
datasource = context.sources.add_pandas("my_datasource")
asset = datasource.add_csv_asset("orders", filepath_or_buffer="orders.csv")

# Expectation定義
batch = asset.get_batch()
batch.expect_column_to_exist("order_id")
batch.expect_column_values_to_not_be_null("order_id")
batch.expect_column_values_to_be_of_type("order_id", "int64")
batch.expect_column_values_to_be_unique("order_id")
batch.expect_column_values_to_match_regex("email", r"^[\w.-]+@[\w.-]+\.\w+$")
batch.expect_column_values_to_be_between("amount", min_value=0, max_value=1000000)

# バリデーション実行
result = batch.validate()
print(f"Success: {result.success}")
```

### CI/CD統合（GitHub Actions）

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

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **csvkit** | 無料 | MIT License、CLI向け |
| **Great Expectations** | 無料（OSS） / 有料（Cloud） | Apache 2.0、エンタープライズ機能は有料 |
| **pandas** | 無料 | BSD License、汎用データ処理 |

## メリット

1. **データ品質保証**: インターフェースのCSVファイルを受入時に自動検証
2. **早期エラー検出**: データ連携前に形式不整合やエンコーディング問題を発見
3. **自動化可能**: CI/CDパイプラインに組み込んで継続的に検証
4. **柔軟なスキーマ定義**: プロジェクト固有の検証ルールをコードで定義可能
5. **多言語対応**: Python、Java、.NET等で実装可能

## デメリット

1. **標準ツールなし**: 統一的なCSVバリデーションツールが存在せず、自作が必要な場合がある
2. **スキーマ管理**: バリデーションルールの保守・更新が必要
3. **大容量対応**: 大容量CSVファイルの検証にはメモリ・パフォーマンスの考慮が必要
4. **エンコーディング**: Shift_JIS等のレガシーエンコーディングの自動判定が困難
5. **RFC 4180限界**: 実務のCSVはRFC 4180に完全準拠しないケースが多い

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Great Expectations** | データバリデーションFW | CSV以外も対応、エンタープライズ向け |
| **csvkit** | CSV専用CLI | 軽量、コマンドラインで即利用可能 |
| **Cerberus** | Pythonバリデーション | スキーマ定義によるデータ検証ライブラリ |
| **JSON Schema** | JSONバリデーション | CSV→JSON変換後にスキーマ検証する方法 |

## 公式リンク

- **RFC 4180**: [https://datatracker.ietf.org/doc/html/rfc4180](https://datatracker.ietf.org/doc/html/rfc4180)
- **csvkit**: [https://csvkit.readthedocs.io/](https://csvkit.readthedocs.io/)
- **Great Expectations**: [https://greatexpectations.io/](https://greatexpectations.io/)
- **pandas**: [https://pandas.pydata.org/](https://pandas.pydata.org/)

## 関連ドキュメント

- [PEP 8](./PEP_8.md)

---

**カテゴリ**: 標準ガイドライン
**対象工程**: 設計・実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
