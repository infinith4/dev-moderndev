# Poetry

## 概要

Poetryは、Pythonプロジェクトの依存関係管理とパッケージビルドを一元的に行うツールです。`pyproject.toml` による宣言的な設定と `poetry.lock` による厳密な依存解決により、開発環境の再現性を保証します。仮想環境の自動管理、依存グループ（dev/test）の分離、PyPIへのパッケージ公開、CI/CDパイプラインとの統合など、Pythonプロジェクトのライフサイクル全体をカバーする包括的なツールです。

## 主な機能

### 1. 依存関係管理
- **pyproject.toml**: PEP 621準拠の宣言的設定ファイル
- **poetry.lock**: 厳密なバージョンロックによる再現性確保
- **依存解決**: SATソルバーによる高精度な依存解決
- **推移的依存**: 間接依存の自動管理

### 2. 仮想環境管理
- **自動作成**: プロジェクトごとの仮想環境を自動生成
- **分離**: システムPythonとの完全な分離
- **Pythonバージョン指定**: 対応バージョンの宣言
- **環境切替**: `poetry env use` による環境切替

### 3. 依存グループ
- **開発依存**: `[tool.poetry.group.dev.dependencies]`
- **テスト依存**: `[tool.poetry.group.test.dependencies]`
- **オプショナル**: `optional = true` で任意グループ化
- **グループ除外**: インストール時にグループを除外可能

### 4. パッケージビルド・公開
- **ビルド**: sdistおよびwheel形式の自動生成
- **PyPI公開**: `poetry publish` でワンコマンド公開
- **プライベートリポジトリ**: 社内PyPIへの公開対応
- **バージョニング**: `poetry version` によるバージョン管理

### 5. スクリプト・プラグイン
- **スクリプト定義**: `[tool.poetry.scripts]` でCLIエントリポイント
- **プラグインシステム**: 機能拡張プラグイン対応
- **カスタムソース**: プライベートリポジトリの設定

## 利用方法

### インストール

```bash
# 公式インストーラ（推奨）
curl -sSL https://install.python-poetry.org | python3 -

# pipx経由
pipx install poetry

# バージョン確認
poetry --version

# シェル補完（bash）
poetry completions bash >> ~/.bash_completion
```

### プロジェクト初期化

```bash
# 新規プロジェクト作成
poetry new my-project
# 生成されるディレクトリ構造:
# my-project/
#   pyproject.toml
#   README.md
#   my_project/__init__.py
#   tests/__init__.py

# 既存プロジェクトにPoetryを導入
cd existing-project
poetry init
```

### pyproject.toml設定

```toml
[tool.poetry]
name = "my-project"
version = "1.0.0"
description = "プロジェクトの説明"
authors = ["Developer <dev@example.com>"]
readme = "README.md"
license = "MIT"
packages = [{include = "my_project"}]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.104.0"
sqlalchemy = "^2.0.0"
pydantic = "^2.5.0"
httpx = "^0.25.0"

[tool.poetry.group.dev.dependencies]
black = "^23.0.0"
ruff = "^0.1.0"
mypy = "^1.7.0"
pre-commit = "^3.6.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
pytest-asyncio = "^0.23.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.5.0"
mkdocs-material = "^9.4.0"

[tool.poetry.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 依存関係の追加・管理

```bash
# パッケージの追加
poetry add requests
poetry add "fastapi>=0.104.0,<1.0.0"

# 開発依存に追加
poetry add --group dev pytest black ruff

# テストグループに追加
poetry add --group test pytest-cov

# パッケージの削除
poetry remove requests

# 依存関係の更新
poetry update
poetry update requests  # 特定パッケージのみ

# lockファイルの更新（インストールなし）
poetry lock

# インストール済みパッケージの一覧
poetry show
poetry show --tree  # ツリー表示
poetry show --outdated  # 更新可能なパッケージ
```

### 仮想環境の操作

```bash
# 依存関係のインストール
poetry install

# 開発依存を除外してインストール
poetry install --without dev,test

# オプショナルグループを含めてインストール
poetry install --with docs

# 仮想環境内でコマンド実行
poetry run python main.py
poetry run pytest

# 仮想環境のシェルに入る
poetry shell

# 仮想環境の情報表示
poetry env info

# Pythonバージョンの切替
poetry env use python3.11

# 仮想環境の削除
poetry env remove python3.11
```

### プライベートリポジトリの設定

```bash
# プライベートリポジトリの追加
poetry source add private https://pypi.example.com/simple/

# 認証情報の設定
poetry config http-basic.private username password
```

```toml
# pyproject.toml にソースを定義
[[tool.poetry.source]]
name = "private"
url = "https://pypi.example.com/simple/"
priority = "supplemental"
```

### パッケージのビルドと公開

```bash
# パッケージのビルド
poetry build
# dist/my_project-1.0.0.tar.gz
# dist/my_project-1.0.0-py3-none-any.whl

# PyPIへの公開
poetry publish

# ビルドと公開を同時に実行
poetry publish --build

# プライベートリポジトリへの公開
poetry publish -r private

# バージョン更新
poetry version patch   # 1.0.0 -> 1.0.1
poetry version minor   # 1.0.0 -> 1.1.0
poetry version major   # 1.0.0 -> 2.0.0
```

### CI/CD統合

```yaml
# .github/workflows/python.yml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: 1.7.1
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        run: poetry install --no-interaction

      - name: Lint
        run: |
          poetry run ruff check .
          poetry run mypy .

      - name: Test
        run: poetry run pytest --cov=my_project --cov-report=xml

      - name: Build
        run: poetry build
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Poetry** | 無料 | オープンソース、MIT License |

## メリット

### 主な利点

1. **統合管理**: 依存関係・仮想環境・ビルド・公開を一元化
2. **再現性**: poetry.lockによる厳密な依存ロック
3. **宣言的設定**: pyproject.tomlによる標準準拠の設定
4. **高精度な依存解決**: SATソルバーによる確実な依存解決
5. **グループ管理**: dev/test/docsなどの依存グループ分離
6. **仮想環境自動管理**: 手動のvenv作成が不要
7. **CI/CD親和性**: lockファイルによる再現可能なビルド
8. **PEP準拠**: pyproject.toml（PEP 621）に対応
9. **ワンコマンド公開**: PyPIへの簡単なパッケージ公開
10. **アクティブ開発**: 活発なコミュニティと継続的改善

## デメリット

### 制約・課題

1. **pip移行コスト**: 既存requirements.txtからの移行作業が必要
2. **依存解決速度**: 大規模プロジェクトで依存解決が遅い場合がある
3. **学習曲線**: pip/venvに慣れたユーザーには新たな学習が必要
4. **プラグイン互換**: 一部プラグインの互換性問題
5. **Conda非互換**: Condaエコシステムとの併用が困難
6. **モノレポ**: 複数パッケージのモノレポ対応が限定的
7. **C拡張**: システムライブラリに依存するパッケージのビルド
8. **setuptools機能**: 一部のsetuptools固有機能が未対応

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **pip + venv** | Python標準ツール | Poetryより軽量だがロック管理が弱い |
| **Pipenv** | pip + virtualenv統合 | Poetryと同目的だがビルド機能なし |
| **uv** | Rust製高速パッケージマネージャー | Poetryより高速だが新しい |
| **Hatch** | PEP準拠ビルドツール | Poetryよりビルド機能が豊富 |
| **PDM** | PEP 582対応パッケージマネージャー | Poetryと類似だがPEP 582対応 |

## 公式リンク

- **公式サイト**: [https://python-poetry.org/](https://python-poetry.org/)
- **ドキュメント**: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
- **GitHub**: [https://github.com/python-poetry/poetry](https://github.com/python-poetry/poetry)
- **PyPI**: [https://pypi.org/project/poetry/](https://pypi.org/project/poetry/)

## 関連ドキュメント

- [パッケージ管理ツール一覧](../パッケージ管理ツール/)
- [Black](../開発ツール/Black.md)
- [Ruff](../開発ツール/Ruff.md)
- [mypy](../開発ツール/mypy.md)

---

**カテゴリ**: パッケージ管理ツール
**対象工程**: 実装・ビルド
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
