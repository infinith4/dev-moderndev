# Python

## 概要

Pythonは、汎用高水準プログラミング言語です。シンプルな構文、豊富なライブラリ、pip（パッケージ管理）、多様な用途（Web、データサイエンス、機械学習、自動化）により、初学者からプロまで幅広く使用されます。Guido van Rossum開発、インタープリタ言語、クロスプラットフォームで世界的に人気です。

## 主な機能

### 1. シンプルな構文
- **可読性**: 英語に近い構文
- **インデント**: ブロック構造
- **動的型付け**: 型宣言不要
- **REPL**: 対話型シェル

### 2. 豊富なライブラリ
- **標準ライブラリ**: "Batteries included"
- **pip**: パッケージ管理
- **PyPI**: 40万+パッケージ
- **フレームワーク**: Django、Flask、FastAPI

### 3. 多様な用途
- **Web開発**: Django、Flask
- **データサイエンス**: NumPy、Pandas
- **機械学習**: TensorFlow、PyTorch
- **自動化**: スクリプト、CLI

### 4. クロスプラットフォーム
- **Windows/macOS/Linux**: 全対応
- **仮想環境**: venv、virtualenv
- **パッケージ管理**: pip、conda

## 利用方法

### インストール

```bash
# macOS (Homebrew)
brew install python

# Windows
# https://www.python.org/downloads/

# Linux (Ubuntu/Debian)
sudo apt install python3 python3-pip

# バージョン確認
python3 --version
pip3 --version
```

### 基本プログラム

```python
# hello.py
print("Hello, Python!")

# 実行
# python3 hello.py
```

### 変数・データ型

```python
# 変数
name = "Alice"
age = 30
height = 165.5
is_student = False

# リスト
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print(fruits[0])  # apple

# タプル
coordinates = (10, 20)

# 辞書
user = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}
print(user["name"])  # Alice

# セット
unique_numbers = {1, 2, 3, 3, 4}
print(unique_numbers)  # {1, 2, 3, 4}
```

### 制御構文

```python
# if文
age = 20
if age >= 20:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# for文
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# while文
count = 0
while count < 5:
    print(count)
    count += 1

# リスト内包表記
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 関数

```python
# 関数定義
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Hello, Alice!

# デフォルト引数
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Bob"))  # Hello, Bob!
print(greet("Bob", "Hi"))  # Hi, Bob!

# 可変長引数
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3, 4, 5))  # 15

# キーワード引数
def create_user(**kwargs):
    return kwargs

user = create_user(name="Alice", age=30, email="alice@example.com")
print(user)  # {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
```

### クラス

```python
# クラス定義
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}, {self.age} years old."

    def __str__(self):
        return f"User(name={self.name}, age={self.age})"

# インスタンス作成
user = User("Alice", 30)
print(user.greet())  # Hello, I'm Alice, 30 years old.
print(user)  # User(name=Alice, age=30)

# 継承
class Student(User):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def greet(self):
        return f"Hello, I'm {self.name}, student ID: {self.student_id}"

student = Student("Bob", 20, "S12345")
print(student.greet())  # Hello, I'm Bob, student ID: S12345
```

### ファイル操作

```python
# ファイル読み込み
with open('file.txt', 'r') as f:
    content = f.read()
    print(content)

# 行ごと読み込み
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())

# ファイル書き込み
with open('output.txt', 'w') as f:
    f.write("Hello, Python!\n")
    f.write("Second line\n")

# JSON
import json

data = {"name": "Alice", "age": 30}

# JSON書き込み
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

# JSON読み込み
with open('data.json', 'r') as f:
    data = json.load(f)
    print(data)
```

### パッケージ管理

```bash
# パッケージインストール
pip install requests
pip install numpy pandas

# requirements.txt
pip freeze > requirements.txt
pip install -r requirements.txt

# 仮想環境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# パッケージ一覧
pip list
pip show requests
```

### 外部ライブラリ

```python
# requests（HTTP）
import requests

response = requests.get('https://api.example.com/users')
data = response.json()
print(data)

# POST
response = requests.post('https://api.example.com/users', json={
    "name": "Alice",
    "email": "alice@example.com"
})

# NumPy（数値計算）
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)  # [2, 4, 6, 8, 10]
print(arr.mean())  # 3.0

# Pandas（データ分析）
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [30, 25, 35],
    'city': ['Tokyo', 'Osaka', 'Kyoto']
})

print(df)
print(df[df['age'] > 26])
```

### 例外処理

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print("Success")
finally:
    print("Cleanup")

# カスタム例外
class CustomError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise CustomError("Age cannot be negative")
    return age

try:
    validate_age(-5)
except CustomError as e:
    print(e)
```

### デコレータ

```python
# デコレータ定義
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

result = add(5, 3)
# Output:
# Calling add
# Finished add
```

### 型ヒント（Type Hints）

```python
from typing import List, Dict, Optional

def greet(name: str) -> str:
    return f"Hello, {name}!"

def process_numbers(numbers: List[int]) -> int:
    return sum(numbers)

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    if user_id == 1:
        return {"name": "Alice", "email": "alice@example.com"}
    return None

# mypy型チェック
# pip install mypy
# mypy script.py
```

### async/await（非同期処理）

```python
import asyncio

async def fetch_data(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(2)  # シミュレート
    return f"Data from {url}"

async def main():
    tasks = [
        fetch_data("https://api1.example.com"),
        fetch_data("https://api2.example.com"),
        fetch_data("https://api3.example.com")
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### CLI作成

```python
# argparse
import argparse

parser = argparse.ArgumentParser(description='My CLI tool')
parser.add_argument('name', help='Your name')
parser.add_argument('--age', type=int, help='Your age')
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')

args = parser.parse_args()

print(f"Hello, {args.name}!")
if args.age:
    print(f"You are {args.age} years old.")
if args.verbose:
    print("Verbose mode enabled")

# 実行
# python script.py Alice --age 30 -v
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Python** | 🟢 無料 | オープンソース、PSF License |
| **Anaconda** | 🟢 無料/💰 | データサイエンス向けディストリビューション |

## メリット

1. **無料**: オープンソース
2. **学習容易**: シンプルな構文
3. **汎用性**: Web、AI、自動化
4. **豊富なライブラリ**: 40万+パッケージ
5. **コミュニティ**: 大規模コミュニティ

## デメリット

1. **速度**: C/C++比較で遅い
2. **GIL**: マルチスレッド制約
3. **モバイル**: モバイルアプリ開発弱い
4. **型**: 動的型付け

## 公式リンク

- **公式サイト**: [https://www.python.org/](https://www.python.org/)
- **ドキュメント**: [https://docs.python.org/](https://docs.python.org/)

## 関連ドキュメント

- [ランタイムツール一覧](../ランタイムツール/)
- [Django](../Webフレームワークツール/Django.md)
- [Flask](../Webフレームワークツール/Flask.md)

---

**カテゴリ**: ランタイムツール
**対象工程**: Python開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
