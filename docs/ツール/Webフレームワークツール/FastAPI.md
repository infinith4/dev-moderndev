# FastAPI

## 概要

FastAPIは、Python製の高速APIフレームワークです。ASGI、型ヒント、自動ドキュメント（OpenAPI/Swagger）、Pydantic（バリデーション）、async/await、高速により、REST API・マイクロサービスを構築します。Flask/Django比較で高速、型安全、モダンPython対応で急速に採用拡大中です。

## 主な機能

### 1. 高速
- **ASGI**: 非同期サーバー
- **Starlette**: ASGIフレームワーク
- **Uvicorn**: ASGIサーバー
- **パフォーマンス**: Node.js/Go級

### 2. 型ヒント
- **Python型**: 型安全
- **Pydantic**: バリデーション
- **自動補完**: IDE補完
- **型チェック**: mypy

### 3. 自動ドキュメント
- **OpenAPI**: OpenAPI 3.0
- **Swagger UI**: /docs
- **ReDoc**: /redoc
- **自動生成**: コードから自動

### 4. 非同期
- **async/await**: 非同期処理
- **WebSocket**: WebSocket対応
- **バックグラウンドタスク**: 非同期タスク

## 利用方法

### インストール

```bash
pip install fastapi uvicorn[standard]
```

### 基本アプリケーション

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

# 起動
# uvicorn main:app --reload
# http://127.0.0.1:8000/
# Swagger UI: http://127.0.0.1:8000/docs
# ReDoc: http://127.0.0.1:8000/redoc
```

### Pydanticモデル

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    age: Optional[int] = None

users = []

@app.get("/api/users", response_model=list[User])
def get_users():
    return users

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/users", response_model=User, status_code=201)
def create_user(user: User):
    user.id = len(users) + 1
    users.append(user)
    return user

@app.put("/api/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    existing_user = next((u for u in users if u.id == user_id), None)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.age = user.age
    return existing_user

@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    global users
    users = [u for u in users if u.id != user_id]
    return None
```

### パスパラメータ・クエリパラメータ

```python
from fastapi import FastAPI, Query

app = FastAPI()

# パスパラメータ
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# クエリパラメータ
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}

# クエリパラメータバリデーション
@app.get("/items")
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    q: Optional[str] = Query(None, min_length=3)
):
    return {"skip": skip, "limit": limit, "query": q}
```

### リクエストボディ

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.post("/items")
def create_item(item: Item):
    return {"item": item, "total": item.price * 1.1}

# 複数ボディパラメータ
@app.post("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    user_id: int = Body(...)
):
    return {"item_id": item_id, "item": item, "user_id": user_id}
```

### 依存性注入

```python
from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

def get_token(authorization: str = Header(...)):
    if authorization != "Bearer secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return authorization

@app.get("/protected")
def protected_route(token: str = Depends(get_token)):
    return {"message": "Protected resource", "token": token}
```

### データベース（SQLAlchemy）

```bash
pip install sqlalchemy databases asyncpg
```

```python
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### 非同期処理

```python
from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

@app.get("/slow")
async def slow_operation():
    await asyncio.sleep(2)
    return {"message": "Done after 2 seconds"}

@app.get("/fetch")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### バックグラウンドタスク

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str, message: str):
    print(f"Sending email to {email}: {message}")
    # メール送信処理

@app.post("/send-email")
async def trigger_send_email(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Email will be sent in background"}
```

### CORS

```bash
pip install fastapi[all]
```

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/data")
def get_data():
    return {"message": "CORS enabled"}
```

### エラーハンドリング

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomException)
def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )

@app.get("/error")
def trigger_error():
    raise CustomException("Something went wrong!")
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **FastAPI** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **高速**: 最速クラス
3. **型安全**: 型ヒント・Pydantic
4. **自動ドキュメント**: OpenAPI自動生成
5. **非同期**: async/await対応

## デメリット

1. **新しい**: 比較的新しい
2. **エコシステム**: Django比較で小規模
3. **学習曲線**: 型ヒント・Pydantic学習
4. **テンプレート**: テンプレート機能弱い

## 公式リンク

- **公式サイト**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **ドキュメント**: [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/)

## 関連ドキュメント

- [Webフレームワークツール一覧](../Webフレームワークツール/)
- [Flask](./Flask.md)
- [Django](./Django.md)

---

**カテゴリ**: Webフレームワークツール
**対象工程**: バックエンド開発・Python
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
