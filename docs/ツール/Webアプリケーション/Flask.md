# Flask

## 概要

Flaskは、Pythonマイクロウェブフレームワークです。ミニマルコア、拡張可能、Jinja2テンプレート、Werkzeug（WSGI）、軽量により、REST API、Webアプリケーション、マイクロサービスを迅速に構築します。シンプル、柔軟、学習容易で広く採用されています。

## 主な機能

### 1. ルーティング
- **デコレータ**: @app.route()
- **HTTPメソッド**: GET、POST、PUT、DELETE
- **URLパラメータ**: <int:id>
- **クエリパラメータ**: request.args

### 2. テンプレート
- **Jinja2**: テンプレートエンジン
- **render_template**: レンダリング
- **変数**: {{ variable }}
- **制御構文**: {% if %}, {% for %}

### 3. リクエスト・レスポンス
- **request**: リクエストオブジェクト
- **jsonify**: JSON レスポンス
- **redirect**: リダイレクト
- **abort**: エラーレスポンス

### 4. 拡張
- **Flask-SQLAlchemy**: ORM
- **Flask-Migrate**: マイグレーション
- **Flask-Login**: 認証
- **Flask-CORS**: CORS

## 利用方法

### インストール

```bash
pip install flask

# プロジェクト作成
mkdir my-app
cd my-app
```

### 基本アプリケーション

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/users')
def users():
    return {'users': ['Alice', 'Bob', 'Charlie']}

if __name__ == '__main__':
    app.run(debug=True)
```

```bash
python app.py
# http://127.0.0.1:5000/
```

### ルーティング

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
]

# GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

# POST create user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

# PUT update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return jsonify(user)

# DELETE user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
```

### テンプレート

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Home', users=['Alice', 'Bob'])

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>Welcome to Flask!</h1>
    <ul>
        {% for user in users %}
            <li>{{ user }}</li>
        {% endfor %}
    </ul>
</body>
</html>

<!-- templates/user.html -->
<!DOCTYPE html>
<html>
<head>
    <title>User: {{ name }}</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    <a href="{{ url_for('index') }}">Back to Home</a>
</body>
</html>
```

### フォーム

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        print(f'Name: {name}, Email: {email}')
        return redirect(url_for('index'))

    return render_template('form.html')
```

```html
<!-- templates/form.html -->
<form method="POST">
    <input type="text" name="name" placeholder="Name" required />
    <input type="email" name="email" placeholder="Email" required />
    <button type="submit">Submit</button>
</form>
```

### Flask-SQLAlchemy

```bash
pip install flask-sqlalchemy
```

```python
# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
```

### Blueprint（モジュール化）

```python
# api/users.py
from flask import Blueprint, jsonify, request

users_bp = Blueprint('users', __name__)

users = []

@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify(users)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user)

# app.py
from flask import Flask
from api.users import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True)
```

### エラーハンドリング

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/error')
def trigger_error():
    raise Exception('Something went wrong!')

if __name__ == '__main__':
    app.run(debug=True)
```

### Flask-CORS

```bash
pip install flask-cors
```

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # すべてのオリジン許可

# または特定オリジンのみ
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/data')
def get_data():
    return {'message': 'CORS enabled'}

if __name__ == '__main__':
    app.run(debug=True)
```

### 設定管理

```python
# config.py
class Config:
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# app.py
from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Flask** | 🟢 無料 | オープンソース、BSD License |

## メリット

1. **無料**: オープンソース
2. **シンプル**: ミニマル設計
3. **柔軟**: 高い自由度
4. **軽量**: 小さいフットプリント
5. **学習容易**: 学習曲線緩やか

## デメリット

1. **機能不足**: Djangoより機能少ない
2. **構造化**: 構造化不十分
3. **非同期**: 非同期サポート弱い
4. **拡張選択**: 拡張選択必要

## 公式リンク

- **公式サイト**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **ドキュメント**: [https://flask.palletsprojects.com/en/latest/](https://flask.palletsprojects.com/en/latest/)

## 関連ドキュメント

- [Webフレームワークツール一覧](../Webフレームワークツール/)
- [Django](./Django.md)
- [FastAPI](./FastAPI.md)

---

**カテゴリ**: Webフレームワークツール
**対象工程**: バックエンド開発・Python
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
