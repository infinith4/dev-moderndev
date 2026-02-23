# mypy

## 概要

mypyは、Python用のオプショナル静的型チェッカーです。PEP 484に基づく型ヒントを活用し、コードを実行せずに型の不整合やバグを検出します。動的型付けと静的型付けを自由に混在させる「段階的型付け（Gradual Typing）」をサポートしており、既存プロジェクトへの段階的な導入が可能です。デーモンモードによる高速なインクリメンタルチェックにも対応しています。

## 主な機能

### 1. 型チェック
- **型推論**: 明示的な型注釈がなくても基本的な型を推論
- **段階的型付け**: 型注釈のあるコードとないコードを混在可能
- **ジェネリクス**: `List[int]`、`Dict[str, Any]` 等のジェネリック型
- **ユニオン型**: `Union[int, str]`、`Optional[int]` 対応
- **Protocol**: 構造的部分型付け（ダックタイピングの形式化）

### 2. 解析モード
- **strict モード**: すべてのチェックを有効化（`--strict`）
- **段階的導入**: `--ignore-missing-imports` で未型付けライブラリを許容
- **デーモンモード**: `dmypy` による高速インクリメンタルチェック（サブ秒更新）
- **型カバレッジ**: 型注釈のカバレッジレポート

### 3. 型システム機能
- **TypedDict**: 辞書の型定義
- **Literal型**: リテラル値の型指定
- **Final**: 定数宣言
- **TypeGuard**: 型ガード関数
- **ParamSpec**: パラメータ仕様変数
- **Callable型**: 関数型の定義

### 4. エディタ統合
- **VS Code**: Pylance / mypy拡張機能
- **PyCharm**: 内蔵型チェック + mypy plugin
- **Vim/Neovim**: ALE / LSP経由
- **Emacs**: flycheck-mypy

## 利用方法

### インストール

```bash
# pip
pip install mypy

# pipx
pipx install mypy

# conda
conda install -c conda-forge mypy
```

### 設定ファイル作成

```ini
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
check_untyped_defs = True
no_implicit_optional = True
strict_equality = True

# サードパーティライブラリの設定
[mypy-requests.*]
ignore_missing_imports = True

[mypy-pandas.*]
ignore_missing_imports = True
```

```toml
# pyproject.toml での設定
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true

[[tool.mypy.overrides]]
module = "requests.*"
ignore_missing_imports = true
```

### 実行

```bash
# 単一ファイルのチェック
mypy src/main.py

# ディレクトリ全体
mypy src/

# strictモード
mypy --strict src/

# 型カバレッジレポート
mypy --html-report report/ src/

# デーモンモード（高速インクリメンタル）
dmypy start
dmypy check src/
dmypy stop
```

### 型注釈の例

```python
from typing import Optional, Union

def greet(name: str) -> str:
    return f"Hello, {name}"

def find_user(user_id: int) -> Optional[dict]:
    """ユーザーが見つからない場合はNoneを返す"""
    ...

def process(data: Union[str, bytes]) -> list[str]:
    if isinstance(data, bytes):
        data = data.decode()
    return data.split(",")
```

### Pre-commit Hook統合

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### CI/CD統合

```yaml
# .github/workflows/typecheck.yml
name: Type Check

on: [push, pull_request]

jobs:
  mypy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install mypy
      - run: mypy src/
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **mypy** | 無料 | オープンソース、MIT License |

## メリット

1. **実行前バグ検出**: コードを実行せずに型の不整合を発見
2. **段階的導入**: 既存コードベースに少しずつ型注釈を追加可能
3. **IDE連携**: エディタでリアルタイムにエラー表示
4. **デーモンモード**: 大規模プロジェクトでもサブ秒でチェック
5. **Protocol対応**: ダックタイピングを型安全に表現
6. **リファクタリング支援**: 型情報に基づいた安全なリファクタリング
7. **ドキュメント効果**: 型注釈がコードのドキュメントとして機能
8. **Python標準**: PEP 484準拠の標準的な型チェッカー

## デメリット

1. **型注釈コスト**: 既存コードへの型注釈追加は手間がかかる
2. **サードパーティ対応**: 型スタブのないライブラリは`ignore_missing_imports`が必要
3. **学習コスト**: 高度な型システム（Protocol、TypeVar等）の理解が必要
4. **偽陽性**: 動的なPythonコードで誤検出が発生する場合がある
5. **設定複雑化**: プロジェクト規模が大きくなると設定が複雑になる

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Pyright** | Microsoft製、高速 | mypyより高速、VS Code統合が強い |
| **Pylance** | Pyrightベース、VS Code専用 | エディタ体験に特化 |
| **Pyre** | Meta製型チェッカー | mypyより高速、大規模コード向け |
| **pytype** | Google製型チェッカー | 型推論が強力、注釈なしでも解析可能 |

## 公式リンク

- **公式サイト**: [https://mypy-lang.org/](https://mypy-lang.org/)
- **ドキュメント**: [https://mypy.readthedocs.io/](https://mypy.readthedocs.io/)
- **GitHub**: [https://github.com/python/mypy](https://github.com/python/mypy)
- **PyPI**: [https://pypi.org/project/mypy/](https://pypi.org/project/mypy/)

## 関連ドキュメント

- [Black](./Black.md)
- [Ruff](./Ruff.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
