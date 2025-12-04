# pip

## 概要

pipは、Python公式のパッケージ管理ツールです。PyPI（Python Package Index）から30万以上のPythonパッケージをインストール、依存関係管理、仮想環境統合を行います。requirements.txt、pip install、pip freezeにより、Pythonエコシステムの標準ツールとして広く採用されています。

## 主な機能

### 1. パッケージ管理
- **インストール**: pip install
- **依存関係**: 自動解決
- **バージョン指定**: ==、>=、<=

### 2. PyPI
- **公開リポジトリ**: 30万+パッケージ
- **検索**: pip search（非推奨）

### 3. 仮想環境
- **venv統合**: Python仮想環境
- **requirements.txt**: 依存関係ファイル

## 利用方法

### インストール

```bash
# Python 3にバンドル
python -m pip --version
```

### パッケージ管理

```bash
# パッケージインストール
pip install requests

# バージョン指定
pip install Django==4.2.0

# requirements.txtからインストール
pip install -r requirements.txt

# パッケージ一覧
pip list

# インストール済み出力
pip freeze > requirements.txt

# パッケージアップグレード
pip install --upgrade requests

# パッケージアンインストール
pip uninstall requests
```

### requirements.txt

```text
Django==4.2.0
requests>=2.28.0
pytest>=7.0.0
```

### 仮想環境

```bash
# 仮想環境作成
python -m venv venv

# 有効化（Linux/macOS）
source venv/bin/activate

# 有効化（Windows）
venv\Scripts\activate

# パッケージインストール
pip install -r requirements.txt
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **pip** | 🟢 完全無料 | オープンソース |

## メリット

1. **完全無料**: オープンソース
2. **標準**: Python標準
3. **PyPI**: 豊富なパッケージ
4. **シンプル**: 使いやすい
5. **venv統合**: 仮想環境対応

## デメリット

1. **依存競合**: 依存解決弱い
2. **ロックファイル**: pip-toolsやPoetry推奨
3. **パフォーマンス**: 遅い場合あり
4. **セキュリティ**: 脆弱性チェック弱い

## 公式リンク

- **公式サイト**: [https://pip.pypa.io/](https://pip.pypa.io/)
- **PyPI**: [https://pypi.org/](https://pypi.org/)

## 関連ドキュメント

- [パッケージ管理ツール一覧](../パッケージ管理ツール/)
- [Poetry](./Poetry.md)

---

**カテゴリ**: パッケージ管理ツール  
**対象工程**: 開発  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
