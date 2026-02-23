# unittest.mock

## 概要

unittest.mockは、Python標準ライブラリ（`unittest.mock`モジュール）に含まれるモッキングフレームワークです。`Mock`、`MagicMock`、`patch`を中心に、テスト対象の依存関係（外部API呼び出し、データベース接続、ファイルI/O等）を差し替えて単体テストの独立性を確保します。Python 3.3以降で標準搭載され、追加インストール不要で利用できます。pytest、unittestの両方で使用可能です。

## 主な機能

### 1. Mockオブジェクト

- **Mock**: 基本的なモックオブジェクト（任意の属性・メソッドを動的生成）
- **MagicMock**: マジックメソッド（`__len__`、`__iter__`等）もモック化したMock
- **PropertyMock**: プロパティのモック化
- **AsyncMock**: 非同期関数（`async def`）のモック（Python 3.8+）
- **spec**: 実際のクラス/モジュールをスペックとして型安全なモック生成

### 2. patch

- **patch()**: モジュール内のオブジェクトを一時的にモックに差し替え
- **patch.object()**: 特定オブジェクトの属性を差し替え
- **patch.dict()**: 辞書の一時的な書き換え
- **patch.multiple()**: 複数属性の同時差し替え
- **デコレータ/コンテキストマネージャ**: `@patch`または`with patch(...)`で使用

### 3. 検証

- **assert_called()**: 呼び出されたことの確認
- **assert_called_once()**: 1回だけ呼び出されたことの確認
- **assert_called_with()**: 特定の引数で呼び出されたことの確認
- **assert_not_called()**: 呼び出されていないことの確認
- **call_count**: 呼び出し回数の取得
- **call_args_list**: 全呼び出しの引数履歴

### 4. 戻り値・副作用

- **return_value**: モックの戻り値設定
- **side_effect**: 例外送出、複数戻り値のイテレーション、関数による動的戻り値
- **side_effect（リスト）**: 呼び出しごとに異なる値を返す

## 利用方法

### 基本的な使用例

```python
from unittest.mock import Mock, MagicMock

# 基本的なMockオブジェクト
mock = Mock()
mock.some_method.return_value = 42
result = mock.some_method("arg1", key="value")
assert result == 42
mock.some_method.assert_called_once_with("arg1", key="value")

# MagicMock（マジックメソッド対応）
magic = MagicMock()
magic.__len__.return_value = 5
assert len(magic) == 5

# specによる型安全モック
mock_list = MagicMock(spec=list)
mock_list.append(1)       # OK
# mock_list.nonexistent()  # AttributeError
```

### patchの使用

```python
from unittest.mock import patch, MagicMock
import requests

# デコレータとして使用
@patch('mymodule.requests.get')
def test_fetch_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"key": "value"}

    result = fetch_data("https://api.example.com/data")

    assert result == {"key": "value"}
    mock_get.assert_called_once_with("https://api.example.com/data")

# コンテキストマネージャとして使用
def test_fetch_data_context():
    with patch('mymodule.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": [1, 2, 3]}

        result = fetch_data("https://api.example.com/items")
        assert result == {"data": [1, 2, 3]}

# 複数のpatch
@patch('mymodule.db_connection')
@patch('mymodule.cache_client')
def test_with_multiple_mocks(mock_cache, mock_db):
    mock_db.query.return_value = [{"id": 1}]
    mock_cache.get.return_value = None
    # テストロジック
```

### side_effectの活用

```python
from unittest.mock import Mock, patch

# 例外を送出
mock = Mock()
mock.side_effect = ValueError("Invalid input")
# mock()  # raises ValueError

# 呼び出しごとに異なる値を返す
mock = Mock()
mock.side_effect = [1, 2, 3]
assert mock() == 1
assert mock() == 2
assert mock() == 3

# 関数による動的な戻り値
def dynamic_return(arg):
    return arg * 2

mock = Mock(side_effect=dynamic_return)
assert mock(5) == 10
assert mock(3) == 6
```

### AsyncMock（非同期モック）

```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {"status": "ok"}

    result = await mock_client.fetch("/api/health")
    assert result == {"status": "ok"}
    mock_client.fetch.assert_awaited_once_with("/api/health")

@patch('mymodule.aiohttp.ClientSession')
@pytest.mark.asyncio
async def test_async_service(mock_session):
    mock_resp = AsyncMock()
    mock_resp.json.return_value = {"data": "test"}
    mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_resp

    result = await my_async_service()
    assert result == {"data": "test"}
```

### pytestとの組み合わせ

```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_db():
    with patch('mymodule.database') as mock:
        mock.connect.return_value = MagicMock()
        mock.connect.return_value.execute.return_value = [{"id": 1, "name": "Alice"}]
        yield mock

def test_get_users(mock_db):
    users = get_users()
    assert len(users) == 1
    assert users[0]["name"] == "Alice"
    mock_db.connect.assert_called_once()
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **unittest.mock** | 無料 | Python標準ライブラリ（追加インストール不要） |

## メリット

1. **標準ライブラリ**: 追加パッケージ不要でPython環境に組み込み済み
2. **柔軟なpatch**: モジュールレベルの差し替えでテスト環境を制御
3. **AsyncMock対応**: Python 3.8+で非同期関数のモックが容易
4. **spec機能**: 実クラスの構造に基づく型安全なモック生成
5. **pytest互換**: pytest、unittest両方のフレームワークで使用可能
6. **副作用制御**: side_effectで例外送出・動的戻り値・イテレーションを定義

## デメリット

1. **patch対象の理解**: `patch`の対象パス（"モジュールから見た名前"）の指定が直感的でない
2. **過度なモック化**: モックの多用でテストが実装詳細に依存するリスク
3. **デバッグ困難**: モック関連のエラーメッセージが分かりにくい場合がある
4. **型チェック**: mypyとの相性が悪く、型エラーが出ることがある
5. **MagicMock万能性**: 任意の属性を生成するため、typoに気づきにくい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **pytest-mock** | pytestプラグイン | unittest.mockのラッパー、mocker fixtureで使いやすい |
| **responses** | HTTPモック | requests/httpxのモック専用、API呼び出しに特化 |
| **freezegun** | 時刻モック | datetime.now()等の時刻固定に特化 |
| **factory_boy** | テストデータ生成 | モックではなくファクトリパターンによるデータ生成 |

## 公式リンク

- **公式ドキュメント**: [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)
- **Getting Started**: [https://docs.python.org/3/library/unittest.mock-examples.html](https://docs.python.org/3/library/unittest.mock-examples.html)
- **pytest-mock**: [https://github.com/pytest-dev/pytest-mock](https://github.com/pytest-dev/pytest-mock)

## 関連ドキュメント

- [GoMock](./GoMock.md)
- [Moq](./Moq.md)

---

**カテゴリ**: テスト
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
