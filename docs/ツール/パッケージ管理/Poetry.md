# Poetry

## 概要

Poetry は Python プロジェクト向けの依存関係管理とパッケージ公開を統合したツールである。`pyproject.toml` と `poetry.lock` を中心に、依存解決、仮想環境管理、ビルド配布を一貫して扱える。

## 料金

| プラン | 内容 |
|------|------|
| Poetry 本体 | 無料（OSS） |
| 公開リポジトリ利用 | PyPI など提供元の条件に依存 |
| 社内リポジトリ運用 | 利用するパッケージ基盤の料金に依存 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 宣言的管理 | `pyproject.toml` で依存とメタ情報を管理 |
| lockfile 運用 | `poetry.lock` で再現性を担保 |
| 仮想環境統合 | 環境作成と実行を Poetry で一元管理 |
| 依存グループ | dev/test/docs など用途別に分離 |
| ビルド/公開統合 | wheel/sdist 作成と公開を同一CLIで実行 |
| Python エコシステム適合 | 近年の標準構成に合わせやすい |

## 主な機能

### 依存関係管理機能

| 機能 | 説明 |
|------|------|
| `poetry add/remove` | 依存パッケージの追加・削除 |
| `poetry update` | lockfile を更新 |
| `poetry lock` | 解決結果を固定 |
| 依存グループ | 開発・テスト依存を分離管理 |

### 環境/実行機能

| 機能 | 説明 |
|------|------|
| `poetry install` | lockfile に基づく依存導入 |
| `poetry run` | 仮想環境内コマンド実行 |
| `poetry env` | Python 実行環境の作成・切替 |
| `poetry show` | 依存関係の可視化 |

### 配布/運用機能

| 機能 | 説明 |
|------|------|
| `poetry build` | sdist/wheel を生成 |
| `poetry publish` | PyPI/社内リポジトリへ公開 |
| source 設定 | 複数インデックスを使い分け |
| version 管理 | `poetry version` で更新 |

## インストールとセットアップ

公式URL:
- [Poetry 公式サイト](https://python-poetry.org/)
- [Poetry Docs](https://python-poetry.org/docs/)
- [Poetry GitHub](https://github.com/python-poetry/poetry)

セットアップの要点:
1. 公式インストーラまたは `pipx` で Poetry を導入する。
2. `poetry init` または `poetry new` でプロジェクトを作成する。
3. `pyproject.toml` に依存と Python バージョンを定義する。
4. `poetry.lock` を必ずコミットし、チームの再現性を確保する。

## 基本的な使い方

1. `poetry add` で依存を追加する。
2. `poetry install` で開発環境を構築する。
3. `poetry run pytest` などでツールを実行する。
4. `poetry build` で配布物を作成する。
5. `poetry publish` でリポジトリへ公開する。

最小運用例:
- 開発依存追加: `poetry add --group dev ruff pytest`
- CI: `poetry install --no-interaction && poetry run pytest`

## メリット

- 依存、環境、配布を単一ツールで扱いやすい。
- lockfile によりビルド再現性を確保しやすい。
- Python プロジェクトの構成を標準化しやすい。
- 開発依存と本番依存を分離しやすい。

## デメリット

- 既存 `pip/requirements.txt` からの移行に手間がかかる。
- 依存解決が重いプロジェクトでは時間がかかる場合がある。
- 複数ツール併用時に設定重複が発生しやすい。

## CI/CD での使用

CI では `poetry install` と `poetry run` を使って、ローカルと同じ依存環境でテストを実行できる。CD では `poetry build` と `poetry publish` を組み合わせ、タグベースで配布自動化する運用が一般的である。

## 他ツールとの比較

| ツール | 強み | 特徴 |
|------|------|------|
| Poetry | 統合管理 | 依存・仮想環境・公開を一体運用 |
| pip + venv | 標準構成 | 軽量だが運用ルールを自作しやすい |
| Pipenv | 依存+環境 | Poetry に近いが採用差がある |
| uv | 速度 | 高速だが運用設計はこれからの領域もある |

## ベストプラクティス

### 1. lockfile を必須運用

- `poetry.lock` を常にコミットする。
- CI で lockfile との差異を検知する。

### 2. 依存グループを整理

- `dev/test/docs` を明確に分ける。
- 本番イメージには不要依存を含めない。

### 3. 配布手順を固定

- `build` と `publish` の手順をリリースフローに組み込む。
- 公開先ごとに認証情報を分離管理する。

## 公式ドキュメント

- 公式サイト: https://python-poetry.org/
- Docs: https://python-poetry.org/docs/
- GitHub: https://github.com/python-poetry/poetry

## まとめ

1. ** 一元化 ** : Poetry は Python 依存管理と配布運用を一元化しやすい。
2. ** 再現性 ** : `pyproject.toml` と `poetry.lock` により再現性を確保しやすい。
3. ** 標準化 ** : CI/CD と連携すると、検証から公開までの手順を標準化しやすい。
