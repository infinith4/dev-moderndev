# Django

## 概要

Djangoは、Python製のフルスタックWebフレームワークです。MTV（Model-Template-View）、ORM、管理画面、認証、セキュリティ（CSRF、XSS対応）により、高速な開発・保守性の高いWebアプリケーションを実現します。"Batteries included"哲学、Instagram・Pinterest採用、Django REST Frameworkで広く採用されています。

## 主な機能

### 1. MTV アーキテクチャ
- **Model**: データモデル（ORM）
- **Template**: テンプレートエンジン
- **View**: ビジネスロジック
- **URL Dispatcher**: ルーティング

### 2. ORM
- **モデル定義**: Pythonクラス
- **マイグレーション**: スキーマ管理
- **クエリセット**: 遅延評価
- **リレーション**: 外部キー、多対多

### 3. 管理画面
- **Admin**: 自動生成管理画面
- **カスタマイズ**: 管理画面カスタマイズ
- **認証**: ユーザー管理

### 4. セキュリティ
- **CSRF**: CSRF対策
- **XSS**: XSS対策
- **SQL Injection**: ORM自動エスケープ
- **認証**: 認証・認可

## 利用方法

### インストール

```bash
pip install django

# プロジェクト作成
django-admin startproject myproject
cd myproject

# 開発サーバー起動
python manage.py runserver
# http://127.0.0.1:8000/
```

### アプリケーション作成

```bash
python manage.py startapp blog
```

```python
# myproject/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # 追加
]
```

### モデル定義

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

```bash
# マイグレーション作成
python manage.py makemigrations

# マイグレーション適用
python manage.py migrate
```

### ビュー

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post

# 関数ベースビュー
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# クラスベースビュー
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
```

### URL設定

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]

# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

### テンプレート

```html
<!-- blog/templates/blog/post_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Blog Posts</title>
</head>
<body>
    <h1>Blog Posts</h1>
    <ul>
        {% for post in posts %}
            <li>
                <a href="{% url 'blog:post_detail' post.pk %}">
                    {{ post.title }}
                </a>
                - {{ post.created_at|date:"Y-m-d" }}
            </li>
        {% endfor %}
    </ul>
</body>
</html>

<!-- blog/templates/blog/post_detail.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p>By {{ post.author.username }} on {{ post.created_at|date:"Y-m-d" }}</p>
    <div>{{ post.content|linebreaks }}</div>
    <a href="{% url 'blog:post_list' %}">Back to list</a>
</body>
</html>
```

### フォーム

```python
# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

# blog/views.py
from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})
```

### 管理画面

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
```

```bash
# スーパーユーザー作成
python manage.py createsuperuser

# 管理画面: http://127.0.0.1:8000/admin/
```

### REST API（Django REST Framework）

```bash
pip install djangorestframework
```

```python
# myproject/settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'blog',
]

# blog/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']

# blog/views.py
from rest_framework import viewsets
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# blog/urls.py
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
```

### 認証

```python
# blog/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def protected_view(request):
    return HttpResponse('Protected content')

class ProtectedView(LoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'
```

### データベース設定

```python
# myproject/settings.py
# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Django** | 🟢 無料 | オープンソース、BSD License |

## メリット

1. **無料**: オープンソース
2. **Batteries included**: 機能豊富
3. **ORM**: 強力なORM
4. **管理画面**: 自動生成管理画面
5. **セキュリティ**: セキュリティ対策万全

## デメリット

1. **モノリシック**: フルスタックフレームワーク
2. **学習曲線**: 学習曲線steep
3. **柔軟性**: 規約強い
4. **パフォーマンス**: Flask比較で遅い

## 公式リンク

- **公式サイト**: [https://www.djangoproject.com/](https://www.djangoproject.com/)
- **ドキュメント**: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

## 関連ドキュメント

- [Webフレームワークツール一覧](../Webフレームワークツール/)
- [Flask](./Flask.md)
- [Django REST Framework](./Django_REST_Framework.md)

---

**カテゴリ**: Webフレームワークツール
**対象工程**: バックエンド開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
