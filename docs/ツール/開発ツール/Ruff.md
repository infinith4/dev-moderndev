# Ruff

## 概要

Ruffは、Rust製の超高速Pythonリンター兼コードフォーマッターです。Flake8（およびその数十のプラグイン）、Black、isort、pydocstyle、pyupgrade、autoflakeなどの複数ツールを単一のバイナリで置き換えることができ、従来のツールの10〜100倍の速度で動作します。800以上の組み込みルールを搭載し、モノレポにも対応した階層的な設定システムを備えています。

## 主な機能

### 1. リンター（`ruff check`）
- **800+ルール**: Flake8、Pyflakes、pycodestyle、isort等のルールを内蔵
- **自動修正**: `--fix` による安全な自動修正
- **カテゴリ別ルール**: E（pycodestyle）、F（Pyflakes）、I（isort）、B（flake8-bugbear）、UP（pyupgrade）等
- **カスタムルール選択**: ルール単位での有効/無効切り替え

### 2. フォーマッター（`ruff format`）
- **Black互換**: Blackと同等のフォーマット出力
- **高速実行**: Blackの10〜100倍の速度
- **isort統合**: インポート整理も同時実行
- **差分表示**: `--diff` でフォーマット差分確認

### 3. パフォーマンス
- **Rust製**: ネイティブバイナリで超高速実行
- **並列処理**: マルチコア活用による高速化
- **キャッシュ**: 変更ファイルのみ再チェック
- **大規模対応**: モノレポ・大規模プロジェクトでもストレスなく動作

### 4. エディタ統合
- **VS Code**: 公式Ruff拡張機能（保存時自動チェック/フォーマット）
- **Neovim**: LSP経由での統合
- **PyCharm**: プラグイン対応
- **Language Server**: ruff-lsp によるLSP統合

## 利用方法

### インストール

```bash
# pip
pip install ruff

# pipx
pipx install ruff

# Homebrew
brew install ruff

# conda
conda install -c conda-forge ruff
```

### 設定ファイル作成

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
    "SIM", # flake8-simplify
    "RUF", # Ruff固有ルール
]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 実行

```bash
# リンター実行
ruff check .

# 自動修正付きリンター
ruff check --fix .

# フォーマッター実行
ruff format .

# ドライラン（確認のみ）
ruff check --diff .
ruff format --check .

# 特定ファイル
ruff check src/main.py
ruff format src/main.py
```

### Pre-commit Hook統合

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### CI/CD統合

```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/ruff-action@v3
        with:
          args: "check"
      - uses: astral-sh/ruff-action@v3
        with:
          args: "format --check"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Ruff** | 無料 | オープンソース、MIT License |

## メリット

1. **超高速**: Rust製で従来ツールの10〜100倍高速
2. **オールインワン**: linter + formatter + isort を1ツールに統合
3. **Black互換**: 既存のBlack設定からスムーズに移行可能
4. **800+ルール**: 多数のFlake8プラグインを内蔵
5. **ゼロコンフィグ**: デフォルト設定で即座に利用可能
6. **モノレポ対応**: 階層的な設定ファイルをサポート
7. **自動修正**: 安全な自動修正機能
8. **公式GitHub Action**: CI/CD統合が容易

## デメリット

1. **比較的新しい**: 2022年登場で、一部ルールは開発中
2. **カスタムプラグイン不可**: Flake8のようなサードパーティプラグイン機構がない
3. **Rust依存**: プラットフォーム固有のバイナリが必要
4. **一部ルール未対応**: Flake8プラグインの完全互換ではない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Flake8** | Python製リンター | Ruffより遅いが成熟したプラグインエコシステム |
| **Black** | Pythonフォーマッター | Ruffより遅いが安定した実績 |
| **Pylint** | 包括的リンター | Ruffより遅いがより深い解析 |
| **isort** | インポート整理 | Ruffに機能が内蔵済み |

## 公式リンク

- **公式サイト**: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)
- **GitHub**: [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff)
- **PyPI**: [https://pypi.org/project/ruff/](https://pypi.org/project/ruff/)
- **VS Code拡張**: [Ruff - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- **Playground**: [https://play.ruff.rs/](https://play.ruff.rs/)

## 関連ドキュメント

- [Black](./Black.md)
- [mypy](./mypy.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
