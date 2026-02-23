# Black

## 概要

Blackは、PEP 8準拠の「妥協しない」Pythonコードフォーマッターです。スタイル設定のオプションを意図的に最小限に抑えることで、コードレビュー時のスタイル議論を排除し、チーム全体で一貫したコードスタイルを強制します。フォーマット後のコードが元のコードと意味的に同等であることをAST検証で保証する安全機構を備えています。

## 主な機能

### 1. コードフォーマット
- **PEP 8準拠**: Pythonの標準スタイルガイドに完全準拠
- **AST安全検証**: フォーマット前後でAST（抽象構文木）の等価性を自動チェック
- **決定論的出力**: 同じ入力に対して常に同じ出力を生成
- **文字列正規化**: シングルクォート/ダブルクォートの統一

### 2. 対応ファイル
- **Pythonファイル**: `.py` ファイルのフォーマット
- **Jupyter Notebook**: `.ipynb` のセルフォーマット（`black[jupyter]`）
- **型スタブ**: `.pyi` ファイル対応
- **pyproject.toml**: Pythonコードリテラル

### 3. 設定オプション
- **行長制限**: `--line-length`（デフォルト88文字）
- **ターゲットバージョン**: `--target-version` で対象Pythonバージョン指定
- **文字列正規化スキップ**: `--skip-string-normalization`
- **Magic Trailing Comma**: 末尾カンマの扱い制御

### 4. エディタ統合
- **VS Code**: Black Formatter拡張機能（保存時自動フォーマット）
- **PyCharm/IntelliJ**: External Tools / File Watcher連携
- **Vim/Neovim**: プラグイン統合
- **Sublime Text**: sublack パッケージ

## 利用方法

### インストール

```bash
# pip
pip install black

# Jupyter Notebook対応
pip install "black[jupyter]"

# pipx（グローバルインストール）
pipx install black

# conda
conda install -c conda-forge black
```

### 設定ファイル作成

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.eggs
  | \.git
  | \.mypy_cache
  | \.venv
  | build
  | dist
)/
'''
```

### 実行

```bash
# 単一ファイルのフォーマット
black src/main.py

# ディレクトリ全体
black src/

# ドライラン（変更内容の確認のみ）
black --check src/

# 差分表示
black --diff src/main.py

# Jupyter Notebookのフォーマット
black notebook.ipynb
```

### Pre-commit Hook統合

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black
        language_version: python3.11
      - id: black-jupyter
```

### CI/CD統合

```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  black:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install black
      - run: black --check .
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Black** | 無料 | オープンソース、MIT License |

## メリット

1. **ゼロコンフィグ**: 設定なしですぐに使える
2. **決定論的**: 同じコードに対して常に同じ結果
3. **AST安全検証**: フォーマットによるバグ混入を防止
4. **レビュー効率化**: スタイル議論が不要になる
5. **高速**: 大規模プロジェクトでも高速に動作
6. **Jupyter対応**: Notebookのセルもフォーマット可能
7. **広い採用実績**: Django、pytest、SQLAlchemy等の大規模プロジェクトで採用
8. **Pre-commit統合**: Git hookで自動実行可能

## デメリット

1. **カスタマイズ制限**: スタイル設定オプションが意図的に少ない
2. **88文字制限**: デフォルトの行長がPEP 8の79文字と異なる
3. **既存コード影響**: 導入時に大量の差分が発生する
4. **文字列操作**: 文字列のクォート変更が望まない場合がある
5. **Python 3.10+**: 実行にPython 3.10以上が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Ruff** | Rust製、超高速linter+formatter | Blackより10-100倍高速、Black互換フォーマット |
| **autopep8** | PEP 8準拠フォーマッター | Blackより設定オプションが多い |
| **YAPF** | Google製フォーマッター | Blackよりカスタマイズ性が高い |
| **Blue** | Blackフォーク | Blackよりコミュニティ寄りの設定 |

## 公式リンク

- **公式サイト**: [https://black.readthedocs.io/](https://black.readthedocs.io/)
- **GitHub**: [https://github.com/psf/black](https://github.com/psf/black)
- **PyPI**: [https://pypi.org/project/black/](https://pypi.org/project/black/)
- **Playground**: [https://black.vercel.app/](https://black.vercel.app/)

## 関連ドキュメント

- [Ruff](./Ruff.md)
- [mypy](./mypy.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
