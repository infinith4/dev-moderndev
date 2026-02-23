# PEP 8

## 概要

PEP 8（Python Enhancement Proposal 8）は、Pythonコードのスタイルガイドです。Guido van Rossumらによって策定され、Pythonコミュニティの標準コーディング規約として広く採用されています。インデント、行の長さ、空白の使い方、命名規則、インポートの書き方等を定義し、Pythonコードの可読性と一貫性を高めます。Ruff、Flake8、Black、autopep8等のツールで自動チェック・自動整形が可能です。

## 主な規則

### 1. インデントと行の長さ

- **インデント**: スペース4つ（タブ不使用）
- **行の長さ**: 最大79文字（docstring/コメントは72文字）
- **継続行**: 括弧内の暗黙的な行連結、またはバックスラッシュ
- **空行**: トップレベル定義間は2行、クラス内メソッド間は1行

### 2. インポート

```python
# 正しいインポート順序（グループ間は空行）
# 1. 標準ライブラリ
import os
import sys
from pathlib import Path

# 2. サードパーティ
import requests
from flask import Flask

# 3. ローカル
from myapp.models import User
from myapp.utils import helper

# NG: ワイルドカードインポート
# from os import *

# NG: 1行に複数インポート
# import os, sys
```

### 3. 空白

```python
# 正しい空白
x = 1
y = x + 1
my_list = [1, 2, 3]
my_dict = {"key": "value"}
func(arg1, arg2)

# NG: 余分な空白
# x = 1          # 代入演算子の周りに余分な空白
# my_list = [ 1, 2, 3 ]  # 括弧内の余分な空白
# func( arg1, arg2 )     # 関数呼び出しの括弧内の空白
# x             = 1      # 位置合わせのための空白
```

### 4. 命名規則

| 対象 | 規則 | 例 |
|------|------|-----|
| モジュール | snake_case | `my_module.py` |
| パッケージ | lowercase | `mypackage` |
| クラス | CapWords（PascalCase） | `MyClass` |
| 関数/メソッド | snake_case | `calculate_total` |
| 変数 | snake_case | `user_name` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| プライベート | 先頭アンダースコア | `_internal_method` |
| マングリング | 先頭ダブルアンダースコア | `__private_attr` |

### 5. 式と文

```python
# 正しい比較
if x is None:
    pass
if isinstance(x, int):
    pass
if not my_list:  # 空リスト判定
    pass

# NG
# if x == None:      # is を使う
# if type(x) is int:  # isinstance を使う
# if len(my_list) == 0:  # 真偽値テストを使う

# 正しい文字列
greeting = f"Hello, {name}!"

# 正しい例外処理
try:
    value = my_dict["key"]
except KeyError:
    value = default_value

# NG: 裸のexcept
# except:
#     pass
```

### 6. docstring（PEP 257）

```python
def calculate_total(items: list[float], tax_rate: float = 0.1) -> float:
    """合計金額を計算する。

    商品リストの合計に税率を適用して税込金額を返す。

    Args:
        items: 商品金額のリスト。
        tax_rate: 税率（デフォルト: 0.1）。

    Returns:
        税込合計金額。

    Raises:
        ValueError: 商品金額に負の値が含まれる場合。
    """
    if any(item < 0 for item in items):
        raise ValueError("商品金額に負の値は指定できません")
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

## 適用ツール

### Ruff（推奨：高速Linter + Formatter）

```bash
# インストール
pip install ruff

# Lintチェック（PEP 8含む）
ruff check .

# 自動修正
ruff check --fix .

# フォーマット（Black互換）
ruff format .
```

```toml
# pyproject.toml
[tool.ruff]
line-length = 79
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I"]  # E/W=pycodestyle, F=pyflakes, I=isort
```

### Black（フォーマッター）

```bash
pip install black

# フォーマット実行
black --line-length 79 .

# チェックのみ（CI用）
black --check --line-length 79 .
```

### Flake8（Linter）

```bash
pip install flake8

# チェック実行
flake8 --max-line-length 79 .
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/lint.yml
name: Python Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install Ruff
        run: pip install ruff
      - name: Lint
        run: ruff check .
      - name: Format Check
        run: ruff format --check .
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **PEP 8** | 無料 | Python公式スタイルガイド |
| **Ruff/Black/Flake8** | 無料 | 各種OSSツール |

## メリット

1. **Python公式**: Pythonコミュニティの公式コーディング規約
2. **可読性重視**: "Readability counts"の哲学に基づいた規則
3. **ツール充実**: Ruff、Black、Flake8、autopep8等で自動適用可能
4. **広く採用**: PyPI上のほとんどのパッケージがPEP 8に準拠
5. **IDE対応**: VS Code、PyCharm等がPEP 8チェックを標準搭載
6. **学習コスト低**: 規則が明確で初学者にも理解しやすい

## デメリット

1. **79文字制限**: モダンなディスプレイでは制約が厳しいと感じる開発者も多い（Black標準は88文字）
2. **一部曖昧**: PEP 8自体が「ガイドライン」であり、厳密なルールではない部分がある
3. **ツール差異**: Black、autopep8、yapf等のフォーマッターで出力が異なる場合がある
4. **既存コード移行**: PEP 8非準拠の既存コードへの一括適用は大きな差分を生む
5. **プロジェクト固有**: PEP 8だけではプロジェクト固有の規約（型ヒント必須等）をカバーしない

## 代替・補完ガイドライン

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Google Python Style Guide** | Google社内規約 | PEP 8ベース + Google独自ルール（docstring形式等） |
| **Black Code Style** | Blackが定義するスタイル | PEP 8準拠、88文字、議論不要のフォーマット |
| **PEP 257** | docstring規約 | PEP 8の補完、docstringの書き方に特化 |
| **PEP 484/526** | 型ヒント | PEP 8と併用、型アノテーションの規約 |

## 公式リンク

- **PEP 8**: [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
- **PEP 257**: [https://peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)
- **Ruff**: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)
- **Black**: [https://black.readthedocs.io/](https://black.readthedocs.io/)
- **Flake8**: [https://flake8.pycqa.org/](https://flake8.pycqa.org/)

## 関連ドキュメント

- [Ruff](../開発ツール/Ruff.md)
- [Black](../開発ツール/Black.md)
- [mypy](../開発ツール/mypy.md)

---

**カテゴリ**: 標準ガイドライン
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
