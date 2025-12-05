# Python/Pandas（ファイル設計）

## 概要

Python/Pandasは、データ分析・操作ライブラリで、基本設計フェーズではCSV、JSON、XML等のファイルフォーマット設計、ファイルレイアウト定義、データ型定義、サンプルデータ生成に活用します。Pandasのデータ構造を使用して、ファイル仕様書とサンプルファイルを効率的に作成できます。

### 基本設計フェーズでの活用

- **CSVファイル設計**: カラム定義、データ型、区切り文字、文字エンコーディング
- **JSONファイル設計**: スキーマ定義、ネスト構造、配列定義
- **XMLファイル設計**: XSD（XMLスキーマ）定義、要素・属性設計
- **ファイルレイアウト定義**: 固定長ファイルのフィールド位置・桁数
- **サンプルデータ生成**: テスト用のダミーデータ生成

### 料金プラン

- **Python**: 完全無料（PSF Licenseライセンス）
- **Pandas**: 完全無料（BSD 3-Clause Licenseライセンス）

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- CSV、JSON、XML、Excel等の多様なフォーマットに対応
- データ型検証、バリデーションが容易
- サンプルデータを迅速に生成可能
- Jupyter Notebookでインタラクティブに設計可能
- バージョン管理（Git）と相性が良い

**デメリット**
- Pythonの学習コストが必要
- GUIツールではないため、非エンジニアには不向き
- 大規模なXMLスキーマ設計には向いていない

## 利用方法

### 1. 環境構築

#### Pythonのインストール

1. [Python公式サイト](https://www.python.org/)にアクセス
2. Python 3.10以上をダウンロード
3. インストーラーを実行
4. 「Add Python to PATH」にチェック

#### Pandasのインストール

```bash
pip install pandas openpyxl lxml faker jsonschema
```

- `pandas`: データ操作ライブラリ
- `openpyxl`: Excelファイル読み書き
- `lxml`: XML処理
- `faker`: ダミーデータ生成
- `jsonschema`: JSONスキーマ検証

### 2. CSVファイル設計

#### 例: 顧客マスタCSVファイル

**1. ファイル仕様の定義**

| カラム名 | データ型 | 桁数 | 必須 | 説明 | サンプル値 |
|---------|---------|------|------|------|----------|
| customer_id | Integer | 10 | ○ | 顧客ID | 1001 |
| customer_name | String | 100 | ○ | 顧客名 | 株式会社サンプル |
| email | String | 100 | ○ | メールアドレス | sample@example.com |
| phone | String | 15 | - | 電話番号 | 03-1234-5678 |
| created_at | DateTime | - | ○ | 登録日時 | 2025-01-15 10:30:00 |

**2. Pandasでサンプルデータ生成**

```python
import pandas as pd
from faker import Faker
import random

fake = Faker('ja_JP')  # 日本語ロケール

# サンプルデータ生成
data = {
    'customer_id': range(1001, 1051),  # 50件
    'customer_name': [fake.company() for _ in range(50)],
    'email': [fake.email() for _ in range(50)],
    'phone': [fake.phone_number() for _ in range(50)],
    'created_at': [fake.date_time_this_year() for _ in range(50)]
}

# DataFrameを作成
df = pd.DataFrame(data)

# CSV出力
df.to_csv('customer_master.csv', index=False, encoding='utf-8-sig')
print("CSVファイルを生成しました: customer_master.csv")
```

**3. CSV出力オプションの設定**

```python
# 区切り文字をタブに変更
df.to_csv('customer_master.tsv', index=False, sep='\t', encoding='utf-8-sig')

# ヘッダーなしで出力
df.to_csv('customer_master_no_header.csv', index=False, header=False)

# ダブルクォートで囲む
df.to_csv('customer_master_quoted.csv', index=False, quoting=1)
```

**4. データ型検証**

```python
# データ型定義
dtypes = {
    'customer_id': 'int64',
    'customer_name': 'object',  # String
    'email': 'object',
    'phone': 'object',
    'created_at': 'datetime64[ns]'
}

# 型変換とバリデーション
df = df.astype(dtypes)

# 必須チェック
assert df['customer_id'].notna().all(), "customer_idにNULLがあります"
assert df['customer_name'].notna().all(), "customer_nameにNULLがあります"

# 桁数チェック
assert df['customer_name'].str.len().max() <= 100, "customer_nameが100文字を超えています"

print("バリデーション成功")
```

### 3. JSONファイル設計

#### 例: 注文データJSONファイル

**1. JSONスキーマの定義**

```python
import json

# JSONスキーマ定義
order_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "order_id": {"type": "integer"},
        "customer_id": {"type": "integer"},
        "order_date": {"type": "string", "format": "date-time"},
        "total_amount": {"type": "number", "minimum": 0},
        "status": {"type": "string", "enum": ["pending", "shipped", "delivered", "cancelled"]},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "product_name": {"type": "string", "maxLength": 200},
                    "quantity": {"type": "integer", "minimum": 1},
                    "unit_price": {"type": "number", "minimum": 0}
                },
                "required": ["product_id", "product_name", "quantity", "unit_price"]
            }
        }
    },
    "required": ["order_id", "customer_id", "order_date", "total_amount", "status", "items"]
}

# スキーマをファイルに保存
with open('order_schema.json', 'w', encoding='utf-8') as f:
    json.dump(order_schema, f, indent=2, ensure_ascii=False)

print("JSONスキーマを生成しました: order_schema.json")
```

**2. サンプルJSONデータの生成**

```python
from datetime import datetime

# サンプルデータ
orders = []

for order_id in range(1, 11):  # 10件の注文
    order = {
        "order_id": order_id,
        "customer_id": 1000 + order_id,
        "order_date": datetime.now().isoformat(),
        "total_amount": random.randint(1000, 50000),
        "status": random.choice(["pending", "shipped", "delivered"]),
        "items": [
            {
                "product_id": random.randint(1, 100),
                "product_name": fake.word(),
                "quantity": random.randint(1, 10),
                "unit_price": random.randint(100, 5000)
            }
            for _ in range(random.randint(1, 5))  # 1-5個の商品
        ]
    }
    orders.append(order)

# JSON出力
with open('orders.json', 'w', encoding='utf-8') as f:
    json.dump(orders, f, indent=2, ensure_ascii=False)

print("サンプルJSONファイルを生成しました: orders.json")
```

**3. JSONスキーマ検証**

```python
from jsonschema import validate, ValidationError

# スキーマ読み込み
with open('order_schema.json', 'r', encoding='utf-8') as f:
    schema = json.load(f)

# データ読み込み
with open('orders.json', 'r', encoding='utf-8') as f:
    orders = json.load(f)

# 各注文を検証
for order in orders:
    try:
        validate(instance=order, schema=schema)
        print(f"注文ID {order['order_id']}: バリデーション成功")
    except ValidationError as e:
        print(f"注文ID {order['order_id']}: バリデーションエラー - {e.message}")
```

### 4. XMLファイル設計

#### 例: 商品カタログXMLファイル

**1. XSDスキーマの定義**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="catalog">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="product" maxOccurs="unbounded">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="product_id" type="xs:integer"/>
                            <xs:element name="product_name" type="xs:string"/>
                            <xs:element name="category" type="xs:string"/>
                            <xs:element name="price" type="xs:decimal"/>
                            <xs:element name="stock_quantity" type="xs:integer"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
```

**2. Pandasでサンプルデータ生成**

```python
import lxml.etree as ET

# サンプルデータ
products_data = {
    'product_id': range(1, 21),
    'product_name': [fake.word() for _ in range(20)],
    'category': [random.choice(['Electronics', 'Books', 'Clothing']) for _ in range(20)],
    'price': [random.randint(100, 10000) for _ in range(20)],
    'stock_quantity': [random.randint(0, 100) for _ in range(20)]
}

df_products = pd.DataFrame(products_data)

# XML生成
root = ET.Element("catalog")

for _, row in df_products.iterrows():
    product = ET.SubElement(root, "product")
    ET.SubElement(product, "product_id").text = str(row['product_id'])
    ET.SubElement(product, "product_name").text = row['product_name']
    ET.SubElement(product, "category").text = row['category']
    ET.SubElement(product, "price").text = str(row['price'])
    ET.SubElement(product, "stock_quantity").text = str(row['stock_quantity'])

# XML出力
tree = ET.ElementTree(root)
tree.write('products.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')

print("サンプルXMLファイルを生成しました: products.xml")
```

### 5. 固定長ファイル設計

#### 例: 銀行振込データ（全銀協フォーマット風）

**1. ファイルレイアウト定義**

| フィールド名 | 開始位置 | 桁数 | データ型 | 説明 |
|------------|---------|------|---------|------|
| レコード区分 | 1 | 1 | String | "1"=ヘッダー、"2"=データ、"9"=トレーラー |
| 依頼日 | 2 | 8 | String | YYYYMMDD |
| 振込先銀行コード | 10 | 4 | String | 銀行コード |
| 振込先支店コード | 14 | 3 | String | 支店コード |
| 口座種別 | 17 | 1 | String | "1"=普通、"2"=当座 |
| 口座番号 | 18 | 7 | String | 7桁、左詰めゼロパディング |
| 受取人名 | 25 | 30 | String | 全角カナ |
| 振込金額 | 55 | 10 | Integer | 右詰めゼロパディング |

**2. Pandasでサンプルデータ生成**

```python
# 固定長フォーマット定義
fixed_length_spec = {
    'record_type': (0, 1),
    'transfer_date': (1, 9),
    'bank_code': (9, 13),
    'branch_code': (13, 16),
    'account_type': (16, 17),
    'account_number': (17, 24),
    'recipient_name': (24, 54),
    'amount': (54, 64)
}

# サンプルデータ
data = {
    'record_type': ['2'] * 10,  # データレコード
    'transfer_date': ['20250115'] * 10,
    'bank_code': [f"{random.randint(1, 9999):04d}" for _ in range(10)],
    'branch_code': [f"{random.randint(1, 999):03d}" for _ in range(10)],
    'account_type': ['1'] * 10,  # 普通預金
    'account_number': [f"{random.randint(1, 9999999):07d}" for _ in range(10)],
    'recipient_name': ['サンプル　タロウ'.ljust(30) for _ in range(10)],
    'amount': [f"{random.randint(1000, 1000000):010d}" for _ in range(10)]
}

df_transfer = pd.DataFrame(data)

# 固定長ファイル出力
with open('transfer_data.txt', 'w', encoding='shift_jis') as f:
    for _, row in df_transfer.iterrows():
        line = (
            row['record_type'] +
            row['transfer_date'] +
            row['bank_code'] +
            row['branch_code'] +
            row['account_type'] +
            row['account_number'] +
            row['recipient_name'] +
            row['amount']
        )
        f.write(line + '\n')

print("固定長ファイルを生成しました: transfer_data.txt")
```

### 6. ファイル仕様書の自動生成

#### Markdown形式のファイル仕様書

```python
def generate_file_spec_markdown(df, filename, file_type='CSV'):
    """
    DataFrameからファイル仕様書（Markdown）を生成
    """
    spec_md = f"# {filename} ファイル仕様書\n\n"
    spec_md += f"## ファイル形式\n\n{file_type}\n\n"
    spec_md += "## カラム定義\n\n"
    spec_md += "| No. | カラム名 | データ型 | 必須 | 説明 | サンプル値 |\n"
    spec_md += "|-----|---------|---------|------|------|----------|\n"

    for i, col in enumerate(df.columns, start=1):
        dtype = str(df[col].dtype)
        sample_value = str(df[col].iloc[0]) if len(df) > 0 else ""
        spec_md += f"| {i} | {col} | {dtype} | ○ | - | {sample_value} |\n"

    spec_md += f"\n## サンプルデータ件数\n\n{len(df)}件\n"

    # ファイルに保存
    with open(f'{filename}_spec.md', 'w', encoding='utf-8') as f:
        f.write(spec_md)

    print(f"ファイル仕様書を生成しました: {filename}_spec.md")

# 使用例
generate_file_spec_markdown(df, 'customer_master', 'CSV')
```

### 7. データバリデーション関数

#### 包括的なバリデーション

```python
def validate_csv_file(df, spec):
    """
    CSVファイルのバリデーション

    Args:
        df: DataFrame
        spec: 仕様辞書
            {
                'column_name': {
                    'dtype': 'int64',
                    'required': True,
                    'max_length': 100,
                    'min_value': 0,
                    'max_value': 9999
                }
            }
    """
    errors = []

    for col, rules in spec.items():
        if col not in df.columns:
            errors.append(f"カラム '{col}' が存在しません")
            continue

        # 必須チェック
        if rules.get('required', False):
            if df[col].isna().any():
                errors.append(f"カラム '{col}' にNULL値があります")

        # データ型チェック
        if 'dtype' in rules:
            try:
                df[col].astype(rules['dtype'])
            except Exception as e:
                errors.append(f"カラム '{col}' のデータ型が不正です: {e}")

        # 桁数チェック
        if 'max_length' in rules and df[col].dtype == 'object':
            max_len = df[col].str.len().max()
            if max_len > rules['max_length']:
                errors.append(f"カラム '{col}' の最大桁数 {max_len} が制限 {rules['max_length']} を超えています")

        # 値の範囲チェック
        if 'min_value' in rules:
            if df[col].min() < rules['min_value']:
                errors.append(f"カラム '{col}' に最小値 {rules['min_value']} 未満の値があります")

        if 'max_value' in rules:
            if df[col].max() > rules['max_value']:
                errors.append(f"カラム '{col}' に最大値 {rules['max_value']} を超える値があります")

    return errors

# 使用例
spec = {
    'customer_id': {'dtype': 'int64', 'required': True, 'min_value': 1},
    'customer_name': {'dtype': 'object', 'required': True, 'max_length': 100},
    'email': {'dtype': 'object', 'required': True, 'max_length': 100}
}

errors = validate_csv_file(df, spec)
if errors:
    for error in errors:
        print(f"❌ {error}")
else:
    print("✅ バリデーション成功")
```

### 8. Excelファイル設計

#### 複数シートのExcelファイル生成

```python
# ExcelWriterで複数シートを作成
with pd.ExcelWriter('database_design.xlsx', engine='openpyxl') as writer:
    # 顧客マスタ
    df_customers.to_excel(writer, sheet_name='顧客マスタ', index=False)

    # 商品マスタ
    df_products.to_excel(writer, sheet_name='商品マスタ', index=False)

    # 注文データ
    df_orders.to_excel(writer, sheet_name='注文データ', index=False)

print("Excelファイルを生成しました: database_design.xlsx")
```

### 9. Jupyter Notebookでの設計ドキュメント作成

#### ファイル設計ノートブック

```python
# ファイル設計ノートブック例（.ipynb）

# ## 1. ファイル概要
# - ファイル名: customer_master.csv
# - ファイル形式: CSV（UTF-8、カンマ区切り）
# - 用途: 顧客マスタデータのエクスポート/インポート

# ## 2. カラム定義
display(df.head())
display(df.dtypes)

# ## 3. サンプルデータ
display(df.describe())

# ## 4. バリデーション結果
errors = validate_csv_file(df, spec)
print(f"バリデーション結果: {len(errors)}件のエラー")
```

## 公式ドキュメント

- **Python公式サイト**: [Python.org](https://www.python.org/)
- **Pandas公式ドキュメント**: [Pandas Documentation](https://pandas.pydata.org/docs/)
- **Pandas IO Tools**: [IO Tools (CSV, JSON, Excel)](https://pandas.pydata.org/docs/user_guide/io.html)
- **Faker Documentation**: [Faker](https://faker.readthedocs.io/)
- **JSONSchema**: [JSON Schema](https://json-schema.org/)

## 学習リソース

- **Pandas Tutorial**: [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- **Real Python**: [Pandas Tutorials](https://realpython.com/learning-paths/pandas-data-science/)
- **Kaggle**: [Pandas Course](https://www.kaggle.com/learn/pandas)

## 関連リンク

- [NumPy](https://numpy.org/)（数値計算ライブラリ）
- [Apache Parquet](https://parquet.apache.org/)（列指向ファイルフォーマット）
- [CSV RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180)（CSV標準仕様）
