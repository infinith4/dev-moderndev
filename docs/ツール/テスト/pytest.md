# pytest

## 概要

pytestは、Pythonのための最も人気のある

テストフレームワークです。シンプルで直感的な構文により、小規模なユニットテストから複雑な機能テストまで幅広く対応します。標準ライブラリのunittestよりも柔軟で強力な機能を提供し、プラグインシステムによる拡張性の高さが特徴です。フィクスチャ、パラメータ化テスト、詳細なアサーション表示など、現代的なテスト開発に必要な機能を備えています。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **pytest** |  無料 | オープンソース、無制限利用、MIT License |

**注意**: pytestは無料のオープンソースプロジェクトです。商用利用も制限なく可能です。

## メリット・デメリット

### メリット
-  **シンプルな構文**: `assert`文でテストを記述、学習コスト低い
-  **無料**: オープンソース、商用利用も無料
-  **豊富なプラグイン**: 800以上のプラグインで機能拡張可能
-  **フィクスチャ**: 依存性注入によるテストデータの管理
-  **パラメータ化テスト**: 同じテストを異なる入力で実行
-  **詳細なエラー表示**: アサーション失敗時に詳細な情報を表示
-  **並列実行**: pytest-xdistで高速化
-  **後方互換性**: unittestテストも実行可能

### デメリット
-  **Python専用**: Python専用、他言語では使用不可
-  **暗黙的な動作**: 魔法のような動作（フィクスチャの自動検出等）が初心者には分かりにくい
-  **プラグイン依存**: 高度な機能はプラグインに依存
-  **デバッグ**: 複雑なフィクスチャのデバッグが困難な場合も

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | ユニットテストの作成、TDD開発 | テストコード、テスト結果 |
| **9. テスト（アプリケーション）** | 自動テスト実行、カバレッジ測定 | テストレポート、カバレッジレポート |

## 基本的な利用方法

### 1. インストール

```bash
# pip経由でインストール
pip install pytest

# 推奨プラグインも一緒にインストール
pip install pytest pytest-cov pytest-mock pytest-xdist

# requirements.txtに追加
# pytest==7.4.3
# pytest-cov==4.1.0
# pytest-mock==3.12.0
# pytest-xdist==3.5.0

# バージョン確認
pytest --version
```

### 2. 基本的なテストの記述

```python
# test_calculator.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# テスト関数（test_ で始まる）
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

def test_divide_by_zero():
    # 例外が発生することを検証
    import pytest
    with pytest.raises(ValueError, match="Division by zero"):
        divide(10, 0)
```

### 3. テストの実行

```bash
# 全テストを実行
pytest

# 詳細表示
pytest -v

# 特定のファイルのみ実行
pytest test_calculator.py

# 特定のテスト関数のみ実行
pytest test_calculator.py::test_add

# キーワードマッチでフィルタリング
pytest -k "add or subtract"

# 失敗したテストのみ再実行
pytest --lf

# カバレッジ測定
pytest --cov=myproject --cov-report=html

# 並列実行（4プロセス）
pytest -n 4
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: テスト駆動開発（TDD）、コード品質の維持

**活用方法**:
- Red-Green-Refactorサイクル
- フィクスチャによるテストデータ管理
- モックを使った依存関係の分離
- パラメータ化テストでエッジケースを網羅

**実装例（TDD開発）**:
```python
# test_user_service.py
import pytest
from unittest.mock import Mock
from user_service import UserService, User
from exceptions import InvalidEmailError, DuplicateEmailError

# フィクスチャ: テスト前の準備処理
@pytest.fixture
def user_service():
    """UserServiceのインスタンスを準備"""
    mock_repository = Mock()
    return UserService(mock_repository), mock_repository

def test_register_user_valid_email_success(user_service):
    """新規ユーザー登録: 有効なメールアドレスで成功する"""
    # Arrange
    service, mock_repo = user_service
    email = "test@example.com"
    password = "SecurePass123!"

    mock_repo.find_by_email.return_value = None
    mock_repo.save.return_value = User(email, password)

    # Act
    result = service.register_user(email, password)

    # Assert
    assert result is not None
    assert result.email == email
    mock_repo.save.assert_called_once()

def test_register_user_invalid_email_raises_error(user_service):
    """ユーザー登録: 無効なメールアドレスで失敗する"""
    service, _ = user_service
    invalid_email = "invalid-email"

    with pytest.raises(InvalidEmailError):
        service.register_user(invalid_email, "password")

def test_register_user_duplicate_email_raises_error(user_service):
    """ユーザー登録: 既存メールアドレスで失敗する"""
    service, mock_repo = user_service
    email = "existing@example.com"

    mock_repo.find_by_email.return_value = User(email, "password")

    with pytest.raises(DuplicateEmailError):
        service.register_user(email, "newPassword")

# パラメータ化テスト
@pytest.mark.parametrize("password,expected", [
    ("Pass123!", True),
    ("SecureP@ssw0rd", True),
    ("MyP@ssw0rd123", True),
    ("short", False),           # 短すぎる
    ("nouppercase123!", False),  # 大文字なし
    ("NOLOWERCASE123!", False),  # 小文字なし
    ("NoSpecialChar123", False), # 特殊文字なし
    ("NoNumbers!@#", False),     # 数字なし
])
def test_password_validation(password, expected):
    """パスワードバリデーションのテスト"""
    from password_validator import PasswordValidator
    assert PasswordValidator.is_valid(password) == expected

# 複数パラメータのテスト
@pytest.mark.parametrize("email,password,should_succeed", [
    ("valid@example.com", "ValidPass123!", True),
    ("invalid-email", "ValidPass123!", False),
    ("valid@example.com", "weak", False),
])
def test_user_registration_scenarios(user_service, email, password, should_succeed):
    """ユーザー登録の各種シナリオ"""
    service, mock_repo = user_service
    mock_repo.find_by_email.return_value = None

    if should_succeed:
        mock_repo.save.return_value = User(email, password)
        result = service.register_user(email, password)
        assert result is not None
    else:
        with pytest.raises(Exception):
            service.register_user(email, password)
```

**フィクスチャの高度な使い方**:
```python
# conftest.py (プロジェクト全体で共有されるフィクスチャ)
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def db_engine():
    """データベースエンジン（セッション全体で1回だけ作成）"""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    """データベースセッション（各テスト関数ごと）"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def sample_user(db_session):
    """サンプルユーザーデータ"""
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    return user

# テストでの使用
def test_user_creation(db_session, sample_user):
    """ユーザーが正しく作成される"""
    user = db_session.query(User).filter_by(email="test@example.com").first()
    assert user is not None
    assert user.name == "Test User"

# フィクスチャのパラメータ化
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db_type(request):
    """複数のデータベースタイプでテスト"""
    return request.param

def test_database_compatibility(db_type):
    """各種データベースでの互換性テスト"""
    # db_typeが "sqlite", "postgresql", "mysql" で3回実行される
    pass
```

**モックとパッチ**:
```python
import pytest
from unittest.mock import Mock, patch, MagicMock

def test_api_call_with_mock():
    """APIコールをモック化"""
    # Mockオブジェクトの作成
    mock_api = Mock()
    mock_api.get_user.return_value = {"id": 1, "name": "John"}

    # テスト
    result = mock_api.get_user(user_id=1)
    assert result["name"] == "John"
    mock_api.get_user.assert_called_once_with(user_id=1)

@patch('requests.get')
def test_fetch_data_from_api(mock_get):
    """外部APIコールをパッチ"""
    # モックのレスポンスを設定
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # テスト対象の関数
    from my_module import fetch_data
    result = fetch_data("https://api.example.com/data")

    assert result["status"] == "success"
    mock_get.assert_called_once()

# pytest-mockプラグインの使用
def test_with_pytest_mock(mocker):
    """pytest-mockでモック化"""
    mock_func = mocker.patch('my_module.expensive_function')
    mock_func.return_value = 42

    from my_module import calculate
    result = calculate()

    assert result == 42
    mock_func.assert_called()
```

---

### 9. テスト（アプリケーション）での活用

**目的**: 包括的なテストスイートの実行、品質保証

**活用方法**:
- CI/CDパイプラインでの自動実行
- コードカバレッジ測定
- テストレポート生成
- 並列実行による高速化

**実装例（CI/CD統合）**:

**pytest.ini設定ファイル**:
```ini
# pytest.ini
[pytest]
minversion = 7.0
addopts =
    -ra
    -q
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: 時間のかかるテスト
    integration: 統合テスト
    unit: ユニットテスト
    smoke: スモークテスト
```

**マーカーによるテスト分類**:
```python
import pytest

@pytest.mark.unit
def test_fast_unit():
    """高速なユニットテスト"""
    assert 1 + 1 == 2

@pytest.mark.integration
@pytest.mark.slow
def test_database_integration():
    """時間のかかるDB統合テスト"""
    # データベーステスト
    pass

@pytest.mark.skip(reason="まだ実装されていない機能")
def test_future_feature():
    """将来実装予定の機能"""
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Windowsではスキップ")
def test_linux_only():
    """Linux専用テスト"""
    pass

@pytest.mark.xfail(reason="既知のバグ")
def test_known_bug():
    """修正中のバグ"""
    assert False

# マーカーでフィルタリングして実行
# pytest -m unit          # ユニットテストのみ
# pytest -m "not slow"    # slowマーカー以外
# pytest -m "unit and not slow"  # 高速なユニットテストのみ
```

**カバレッジレポート**:
```bash
# HTMLレポート生成
pytest --cov=src --cov-report=html

# ターミナルに詳細表示
pytest --cov=src --cov-report=term-missing

# XMLレポート（CI/CD向け）
pytest --cov=src --cov-report=xml

# カバレッジ80%未満で失敗
pytest --cov=src --cov-fail-under=80

# .coveragercファイルで設定
# [run]
# source = src
# omit = */tests/*
#
# [report]
# precision = 2
# show_missing = True
# skip_covered = False
#
# [html]
# directory = htmlcov
```

**並列実行（pytest-xdist）**:
```bash
# 4プロセスで並列実行
pytest -n 4

# 自動でCPUコア数を検出
pytest -n auto

# 失敗したテストを即座に表示
pytest -n 4 -v

# ロードバランシング
pytest -n 4 --dist=loadscope
```

**テストレポート生成（pytest-html）**:
```bash
# HTMLレポート生成
pip install pytest-html
pytest --html=report.html --self-contained-html

# JUnit XML（CI/CDツールで使用）
pytest --junitxml=junit.xml
```

**GitHub Actionsでの実行例**:
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist

      - name: Run tests
        run: |
          pytest -n auto --cov=src --cov-report=xml --junitxml=junit.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

      - name: Publish test results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: junit.xml
```

**高度なフィクスチャパターン**:
```python
import pytest

# スコープ別フィクスチャ
@pytest.fixture(scope="session")
def browser():
    """ブラウザ（セッション全体で1回）"""
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def api_client():
    """APIクライアント（モジュールごと）"""
    client = APIClient()
    yield client
    client.close()

@pytest.fixture(scope="class")
def database():
    """データベース（クラスごと）"""
    db = Database()
    yield db
    db.cleanup()

@pytest.fixture(scope="function")  # デフォルト
def temp_file(tmp_path):
    """一時ファイル（各テスト関数ごと）"""
    file = tmp_path / "test.txt"
    file.write_text("test data")
    yield file
    # 自動的にクリーンアップされる

# Autouseフィクスチャ（自動適用）
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """全テストで自動実行"""
    print("\nSetup")
    yield
    print("\nTeardown")
```

## 公式ドキュメント

- [pytest 公式サイト](https://pytest.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest API Reference](https://docs.pytest.org/en/stable/reference/)
- [pytest GitHub Repository](https://github.com/pytest-dev/pytest)
- [pytest Plugins](https://docs.pytest.org/en/latest/reference/plugin_list.html)

## 学習リソース

### チュートリアル
- [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)
- [Real Python - pytest Guide](https://realpython.com/pytest-python-testing/)
- [pytest Tutorial](https://www.tutorialspoint.com/pytest/index.htm)

### 書籍
- "Python Testing with pytest" by Brian Okken (O'Reilly)
- "Test-Driven Development with Python" by Harry Percival (O'Reilly)
- "Effective Python Testing with Pytest" by Bruno Oliveira

### 動画・コース
- [pytest Tutorial for Beginners](https://www.youtube.com/results?search_query=pytest+tutorial)
- [Talk Python Training - pytest Course](https://training.talkpython.fm/courses/explore_pytest/testing-python-applications-with-pytest)
- [Pluralsight - Unit Testing with pytest](https://www.pluralsight.com/courses/unit-testing-python)

### コミュニティ
- [pytest Discord](https://discord.com/invite/pytest-dev)
- [Stack Overflow - pytest](https://stackoverflow.com/questions/tagged/pytest)
- [pytest GitHub Discussions](https://github.com/pytest-dev/pytest/discussions)

## 関連リンク

### 必須プラグイン
- [pytest-cov](https://pytest-cov.readthedocs.io/) - コードカバレッジ測定
- [pytest-mock](https://pytest-mock.readthedocs.io/) - モック拡張
- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - 並列実行
- [pytest-html](https://pytest-html.readthedocs.io/) - HTMLレポート生成

### 便利なプラグイン
- [pytest-django](https://pytest-django.readthedocs.io/) - Django統合
- [pytest-flask](https://pytest-flask.readthedocs.io/) - Flask統合
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - 非同期テスト
- [pytest-bdd](https://pytest-bdd.readthedocs.io/) - BDDスタイルテスト
- [pytest-selenium](https://pytest-selenium.readthedocs.io/) - Selenium統合
- [pytest-benchmark](https://pytest-benchmark.readthedocs.io/) - パフォーマンステスト

### ベストプラクティス
- [pytest Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [pytest Best Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

