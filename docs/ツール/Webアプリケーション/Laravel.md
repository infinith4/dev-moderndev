# Laravel

## 概要

Laravelは、PHP製のフルスタックWebアプリケーションフレームワークです。Eloquent ORM、Blade（テンプレート）、Artisan（CLI）、マイグレーション、認証、キュー、リアルタイム（Broadcasting）により、エレガントな構文で高速開発を実現します。Taylor Otwell開発、PHPデファクトスタンダード、豊富なエコシステムで広く採用されています。

## 主な機能

### 1. Eloquent ORM
- **ORM**: オブジェクトリレーショナルマッピング
- **モデル**: データモデル
- **リレーション**: belongsTo、hasMany等
- **クエリビルダ**: 流れるようなAPI

### 2. Blade テンプレート
- **テンプレートエンジン**: Blade
- **レイアウト**: 継承
- **コンポーネント**: 再利用可能
- **ディレクティブ**: @if、@foreach

### 3. Artisan CLI
- **コマンド**: カスタムコマンド
- **マイグレーション**: スキーマ管理
- **シーディング**: テストデータ
- **キュー**: バックグラウンドジョブ

### 4. 認証・認可
- **認証**: Laravel Breeze、Jetstream
- **認可**: ポリシー、Gate
- **API**: Sanctum（トークン）、Passport（OAuth2）

## 利用方法

### インストール

```bash
# Composerインストール
composer global require laravel/installer

# プロジェクト作成
laravel new my-app
cd my-app

# 開発サーバー起動
php artisan serve
# http://127.0.0.1:8000/
```

### ルーティング

```php
// routes/web.php
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/users', function () {
    return ['users' => ['Alice', 'Bob', 'Charlie']];
});

Route::get('/users/{id}', function ($id) {
    return ['id' => $id, 'name' => 'Alice'];
});
```

### コントローラー

```bash
php artisan make:controller UserController
```

```php
// app/Http/Controllers/UserController.php
namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        return ['users' => ['Alice', 'Bob']];
    }

    public function show($id)
    {
        return ['id' => $id, 'name' => 'Alice'];
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'email' => 'required|email'
        ]);

        // ユーザー作成処理
        return response()->json($validated, 201);
    }
}

// routes/web.php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
Route::get('/users/{id}', [UserController::class, 'show']);
Route::post('/users', [UserController::class, 'store']);
```

### Eloquent モデル

```bash
php artisan make:model User -m
```

```php
// app/Models/User.php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected $fillable = ['name', 'email'];

    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}

// database/migrations/xxxx_create_users_table.php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('users');
    }
};

// マイグレーション実行
// php artisan migrate
```

### Eloquent CRUD

```php
use App\Models\User;

// 全件取得
$users = User::all();

// 条件付き取得
$users = User::where('name', 'Alice')->get();

// 1件取得
$user = User::find(1);
$user = User::where('email', 'alice@example.com')->first();

// 作成
$user = User::create([
    'name' => 'Alice',
    'email' => 'alice@example.com'
]);

// 更新
$user = User::find(1);
$user->name = 'Alice Smith';
$user->save();

// または
User::where('id', 1)->update(['name' => 'Alice Smith']);

// 削除
$user = User::find(1);
$user->delete();

// または
User::destroy(1);
```

### REST API コントローラー

```bash
php artisan make:controller Api/UserController --api
```

```php
// app/Http/Controllers/Api/UserController.php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        return User::all();
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'email' => 'required|email|unique:users'
        ]);

        $user = User::create($validated);
        return response()->json($user, 201);
    }

    public function show($id)
    {
        $user = User::findOrFail($id);
        return $user;
    }

    public function update(Request $request, $id)
    {
        $user = User::findOrFail($id);

        $validated = $request->validate([
            'name' => 'sometimes|required|max:255',
            'email' => 'sometimes|required|email|unique:users,email,'.$id
        ]);

        $user->update($validated);
        return $user;
    }

    public function destroy($id)
    {
        User::findOrFail($id)->delete();
        return response()->noContent();
    }
}

// routes/api.php
use App\Http\Controllers\Api\UserController;

Route::apiResource('users', UserController::class);
```

### Blade テンプレート

```php
<!-- resources/views/layout.blade.php -->
<!DOCTYPE html>
<html>
<head>
    <title>@yield('title')</title>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
    </nav>

    <div class="container">
        @yield('content')
    </div>
</body>
</html>

<!-- resources/views/users/index.blade.php -->
@extends('layout')

@section('title', 'Users')

@section('content')
    <h1>Users</h1>
    <ul>
        @foreach($users as $user)
            <li>{{ $user->name }} - {{ $user->email }}</li>
        @endforeach
    </ul>

    @if(count($users) === 0)
        <p>No users found.</p>
    @endif
@endsection

// Controller
public function index()
{
    $users = User::all();
    return view('users.index', ['users' => $users]);
}
```

### バリデーション

```php
// app/Http/Requests/StoreUserRequest.php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreUserRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed'
        ];
    }

    public function messages()
    {
        return [
            'name.required' => 'Name is required',
            'email.required' => 'Email is required',
            'email.email' => 'Email must be valid'
        ];
    }
}

// Controller
use App\Http\Requests\StoreUserRequest;

public function store(StoreUserRequest $request)
{
    $user = User::create($request->validated());
    return response()->json($user, 201);
}
```

### リレーション

```php
// app/Models/User.php
class User extends Model
{
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}

// app/Models/Post.php
class Post extends Model
{
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}

// 使用例
$user = User::find(1);
$posts = $user->posts;  // hasMany

$post = Post::find(1);
$user = $post->user;  // belongsTo

// Eager Loading
$users = User::with('posts')->get();
```

### 認証（Laravel Breeze）

```bash
composer require laravel/breeze --dev
php artisan breeze:install
npm install && npm run dev
php artisan migrate
```

### データベース設定

```env
# .env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=my_database
DB_USERNAME=root
DB_PASSWORD=secret
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Laravel** | 🟢 完全無料 | オープンソース、MIT License |
| **Laravel Forge** | 💰 $12/月〜 | サーバー管理 |
| **Laravel Vapor** | 💰 $39/月〜 | サーバーレスデプロイ |

## メリット

1. **完全無料**: オープンソース
2. **エレガント**: 美しい構文
3. **フルスタック**: 機能豊富
4. **Eloquent**: 強力なORM
5. **エコシステム**: 豊富なパッケージ

## デメリット

1. **パフォーマンス**: 他PHP比較で遅い
2. **学習曲線**: 学習曲線steep
3. **PHP**: PHP依存
4. **メモリ**: メモリ消費大

## 公式リンク

- **公式サイト**: [https://laravel.com/](https://laravel.com/)
- **ドキュメント**: [https://laravel.com/docs](https://laravel.com/docs)

## 関連ドキュメント

- [Webフレームワークツール一覧](../Webフレームワークツール/)
- [Symfony](./Symfony.md)
- [CodeIgniter](./CodeIgniter.md)

---

**カテゴリ**: Webフレームワークツール
**対象工程**: バックエンド開発・PHP
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
