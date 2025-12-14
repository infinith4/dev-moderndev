# Catalyst

## 概要

**Catalyst**は、Perl言語のMVCフレームワークです。Ruby on RailsやDjangoに影響を受けた設計、豊富なプラグインエコシステム、CPAN統合により、エンタープライズWebアプリケーション開発を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | オープンソースコミュニティ |
| **種別** | Perl Webフレームワーク（MVC） |
| **ライセンス** | Perl Artistic License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | http://www.catalystframework.org/ |
| **ドキュメント** | https://metacpan.org/pod/Catalyst::Manual |

## 主な特徴

### 1. MVC アーキテクチャ
- **Model**: データベース・ビジネスロジック
- **View**: テンプレートエンジン（TT、Mason等）
- **Controller**: リクエスト処理・ディスパッチ

### 2. プラグインエコシステム
- 認証・認可
- セッション管理
- キャッシュ
- フォーム処理
- REST API

### 3. CPAN統合
- 豊富なPerlモジュール活用
- DBIx::Class（ORM）
- Template Toolkit（テンプレート）
- Moose（OOP）

### 4. デプロイ柔軟性
- FastCGI、mod_perl、PSGI/Plack
- スタンドアロンサーバー
- リバースプロキシ（nginx + Catalyst）

## 使い方

### セットアップ

```bash
# CPANMインストール
curl -L https://cpanmin.us | perl - --sudo App::cpanminus

# Catalystインストール
cpanm Catalyst::Runtime
cpanm Catalyst::Devel

# プロジェクト作成
catalyst.pl MyApp

cd MyApp

# 開発サーバー起動
perl script/myapp_server.pl

# http://localhost:3000 にアクセス
```

### プロジェクト構造

```text
MyApp/
├── lib/
│   └── MyApp/
│       ├── Controller/       # コントローラー
│       │   └── Root.pm
│       ├── Model/            # モデル
│       ├── View/             # ビュー
│       └── MyApp.pm          # アプリケーションクラス
├── root/                     # テンプレート・静的ファイル
│   ├── static/
│   └── src/
├── script/                   # 実行スクリプト
│   ├── myapp_server.pl       # 開発サーバー
│   ├── myapp_test.pl         # テスト
│   └── myapp_create.pl       # コードジェネレーター
├── t/                        # テスト
└── myapp.conf                # 設定ファイル
```

### アプリケーションクラス

```perl
# lib/MyApp.pm
package MyApp;
use Moose;
use namespace::autoclean;

use Catalyst::Runtime 5.80;

use Catalyst qw/
    -Debug
    ConfigLoader
    Static::Simple
    Session
    Session::Store::File
    Session::State::Cookie
    Authentication
    Authorization::Roles
/;

extends 'Catalyst';

our $VERSION = '0.01';

__PACKAGE__->config(
    name => 'MyApp',
    disable_component_resolution_regex_fallback => 1,
    enable_catalyst_header => 1,
);

__PACKAGE__->setup();

1;
```

### コントローラー

```perl
# lib/MyApp/Controller/Root.pm
package MyApp::Controller::Root;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller' }

__PACKAGE__->config(namespace => '');

# デフォルトアクション
sub index :Path :Args(0) {
    my ( $self, $c ) = @_;

    # テンプレート変数
    $c->stash(
        template => 'index.tt',
        message  => 'Welcome to Catalyst!'
    );
}

# 個別ルート
sub hello :Local :Args(0) {
    my ( $self, $c ) = @_;

    $c->response->body('Hello, World!');
}

# パラメータ付きルート
sub user :Local :Args(1) {
    my ( $self, $c, $user_id ) = @_;

    $c->stash(
        template => 'user.tt',
        user_id  => $user_id
    );
}

# RESTful アクション
sub api_users :Path('/api/users') :Args(0) :ActionClass('REST') {
    my ( $self, $c ) = @_;
}

sub api_users_GET {
    my ( $self, $c ) = @_;

    my @users = $c->model('DB::User')->all;

    $c->stash(
        users => \@users,
        current_view => 'JSON'
    );
}

sub api_users_POST {
    my ( $self, $c ) = @_;

    my $user = $c->model('DB::User')->create({
        name  => $c->req->param('name'),
        email => $c->req->param('email'),
    });

    $c->stash(
        user => $user,
        current_view => 'JSON'
    );
}

# エラーハンドリング
sub end : ActionClass('RenderView') {}

__PACKAGE__->meta->make_immutable;

1;
```

### モデル（DBIx::Class）

```bash
# DBIx::Class（ORM）インストール
cpanm DBIx::Class
cpanm DBIx::Class::Schema::Loader
cpanm Catalyst::Model::DBIC::Schema

# モデル作成
script/myapp_create.pl model DB DBIC::Schema MyApp::Schema \
  create=static \
  dbi:SQLite:myapp.db
```

```perl
# lib/MyApp/Model/DB.pm（自動生成）
package MyApp::Model::DB;

use strict;
use base 'Catalyst::Model::DBIC::Schema';

__PACKAGE__->config(
    schema_class => 'MyApp::Schema',
    connect_info => {
        dsn => 'dbi:SQLite:myapp.db',
        user => '',
        password => '',
    }
);

1;
```

```perl
# lib/MyApp/Schema/Result/User.pm
package MyApp::Schema::Result::User;
use base qw/DBIx::Class::Core/;

__PACKAGE__->table('users');
__PACKAGE__->add_columns(
    'id' => {
        data_type => 'integer',
        is_auto_increment => 1,
    },
    'email' => {
        data_type => 'varchar',
        size => 255,
    },
    'name' => {
        data_type => 'varchar',
        size => 100,
    },
    'created' => {
        data_type => 'timestamp',
    },
);

__PACKAGE__->set_primary_key('id');
__PACKAGE__->has_many('posts', 'MyApp::Schema::Result::Post', 'user_id');

1;
```

```perl
# コントローラーでモデル使用
sub list :Local :Args(0) {
    my ( $self, $c ) = @_;

    # 全ユーザー取得
    my @users = $c->model('DB::User')->all;

    # 検索
    my @active_users = $c->model('DB::User')->search({
        status => 'active'
    });

    # 関連データ取得
    my $user = $c->model('DB::User')->find(1);
    my @posts = $user->posts;

    $c->stash(
        template => 'user/list.tt',
        users    => \@users
    );
}

sub create :Local :Args(0) {
    my ( $self, $c ) = @_;

    if ( $c->req->method eq 'POST' ) {
        my $user = $c->model('DB::User')->create({
            email => $c->req->param('email'),
            name  => $c->req->param('name'),
        });

        $c->response->redirect($c->uri_for('/user/list'));
    }

    $c->stash( template => 'user/create.tt' );
}
```

### ビュー（Template Toolkit）

```bash
# Template Toolkitインストール
cpanm Template
cpanm Catalyst::View::TT

# ビュー作成
script/myapp_create.pl view TT TT
```

```perl
# lib/MyApp/View/TT.pm
package MyApp::View::TT;

use strict;
use warnings;

use base 'Catalyst::View::TT';

__PACKAGE__->config(
    TEMPLATE_EXTENSION => '.tt',
    WRAPPER            => 'wrapper.tt',
    render_die => 1,
);

1;
```

```html
<!-- root/src/wrapper.tt -->
<!DOCTYPE html>
<html>
<head>
    <title>[% title || 'MyApp' %]</title>
    <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
    <header>
        <h1>MyApp</h1>
    </header>
    <main>
        [% content %]
    </main>
    <footer>
        <p>&copy; 2025 MyApp</p>
    </footer>
</body>
</html>
```

```html
<!-- root/src/index.tt -->
<h2>[% message %]</h2>
<p>Welcome to Catalyst Framework!</p>

<ul>
    <li><a href="/hello">Hello</a></li>
    <li><a href="/user/123">User Profile</a></li>
    <li><a href="/user/list">User List</a></li>
</ul>
```

```html
<!-- root/src/user/list.tt -->
<h2>User List</h2>

<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
        </tr>
    </thead>
    <tbody>
        [% FOREACH user IN users %]
        <tr>
            <td>[% user.id %]</td>
            <td>[% user.name %]</td>
            <td>[% user.email %]</td>
        </tr>
        [% END %]
    </tbody>
</table>
```

### 認証・認可

```bash
# 認証プラグインインストール
cpanm Catalyst::Plugin::Authentication
cpanm Catalyst::Plugin::Authorization::Roles
cpanm Catalyst::Authentication::Store::DBIx::Class
```

```perl
# lib/MyApp.pm（認証設定）
__PACKAGE__->config(
    'Plugin::Authentication' => {
        default => {
            credential => {
                class          => 'Password',
                password_field => 'password',
                password_type  => 'self_check',
            },
            store => {
                class      => 'DBIx::Class',
                user_model => 'DB::User',
                role_relation => 'roles',
                role_field => 'role',
            }
        }
    }
);
```

```perl
# lib/MyApp/Controller/Auth.pm
package MyApp::Controller::Auth;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller' }

sub login :Local :Args(0) {
    my ( $self, $c ) = @_;

    if ( $c->req->method eq 'POST' ) {
        my $email = $c->req->param('email');
        my $password = $c->req->param('password');

        if ( $c->authenticate({ email => $email, password => $password }) ) {
            $c->response->redirect($c->uri_for('/dashboard'));
        } else {
            $c->stash( error_msg => 'Invalid email or password' );
        }
    }

    $c->stash( template => 'auth/login.tt' );
}

sub logout :Local :Args(0) {
    my ( $self, $c ) = @_;

    $c->logout;
    $c->response->redirect($c->uri_for('/'));
}

# 認可チェック
sub admin :Local :Args(0) :Does(NeedsLogin) :Does(ACL) :RequiresRole(admin) {
    my ( $self, $c ) = @_;

    $c->stash( template => 'admin/dashboard.tt' );
}

__PACKAGE__->meta->make_immutable;

1;
```

### フォーム処理（HTML::FormHandler）

```bash
cpanm HTML::FormHandler
cpanm HTML::FormHandler::Model::DBIC
```

```perl
# lib/MyApp/Form/User.pm
package MyApp::Form::User;
use HTML::FormHandler::Moose;
extends 'HTML::FormHandler::Model::DBIC';

has_field 'email' => (
    type     => 'Email',
    required => 1,
);

has_field 'name' => (
    type     => 'Text',
    required => 1,
);

has_field 'password' => (
    type     => 'Password',
    required => 1,
);

has_field 'submit' => ( type => 'Submit' );

1;
```

```perl
# コントローラーでフォーム使用
sub create :Local :Args(0) {
    my ( $self, $c ) = @_;

    my $form = MyApp::Form::User->new(
        item_class => 'DB::User',
    );

    $form->process(
        item   => $c->model('DB::User')->new_result({}),
        params => $c->req->params,
    );

    if ( $form->validated ) {
        $c->response->redirect($c->uri_for('/user/list'));
    }

    $c->stash(
        template => 'user/create.tt',
        form     => $form,
    );
}
```

### デプロイ

#### PSGI/Plack

```perl
# myapp.psgi
use strict;
use warnings;

use MyApp;

my $app = MyApp->apply_default_middlewares(MyApp->psgi_app);
$app;
```

```bash
# Plackインストール
cpanm Plack
cpanm Starman  # 本番サーバー

# 開発環境
plackup myapp.psgi

# 本番環境
starman --workers 10 --listen :5000 myapp.psgi
```

#### nginx + Plack

```nginx
# /etc/nginx/sites-available/myapp
upstream myapp {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name myapp.example.com;

    location / {
        proxy_pass http://myapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/myapp/root/static/;
        expires 30d;
    }
}
```

### テスト

```perl
# t/controller_Root.t
use strict;
use warnings;
use Test::More;

BEGIN { use_ok 'Catalyst::Test', 'MyApp' }

ok( request('/')->is_success, 'Request should succeed' );
ok( request('/hello')->is_success, 'Hello should succeed' );

my $response = request('/');
like( $response->content, qr/Welcome/, 'Content should contain Welcome' );

done_testing();
```

```bash
# テスト実行
prove -lv t/
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | プロトタイピング | 高速試作 |
| **設計** | アーキテクチャ設計 | MVC設計 |
| **実装** | Webアプリ開発 | CRUD実装 |
| **テスト** | ユニット・統合テスト | Test::More統合 |

## メリット

- **成熟**: 2005年から、長期実績
- **柔軟**: プラグインで機能拡張
- **CPAN統合**: 豊富なPerlモジュール活用
- **Moose**: モダンPerlのOOP
- **DBIx::Class**: 強力なORM
- **コミュニティ**: 長年のコミュニティサポート

## デメリット

- **Perl依存**: Perl環境必須
- **学習曲線**: Moose、Perlの理解必要
- **人気低下**: 近年の新規採用は少ない
- **モダン度**: Laravel、Rails等に比べ古い設計
- **ドキュメント**: 英語のみ、日本語情報少ない
- **パフォーマンス**: 起動時間、メモリ消費

## 類似ツールとの比較

| ツール | 言語 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **Catalyst** | Perl | MVC、CPAN統合 | Perl環境、レガシー |
| **Mojolicious** | Perl | モダン、軽量 | モダンPerl開発 |
| **Ruby on Rails** | Ruby | 規約、高速開発 | Ruby環境 |
| **Django** | Python | バッテリー同梱 | Python環境 |

## ベストプラクティス

### 1. Chained アクション

```perl
# 段階的ディスパッチ
sub base :Chained('/') :PathPart('user') :CaptureArgs(0) {
    my ( $self, $c ) = @_;
    # 共通処理
}

sub view :Chained('base') :PathPart('view') :Args(1) {
    my ( $self, $c, $user_id ) = @_;
    # /user/view/123
}

sub edit :Chained('base') :PathPart('edit') :Args(1) {
    my ( $self, $c, $user_id ) = @_;
    # /user/edit/123
}
```

### 2. フォーム検証

```perl
# HTML::FormHandler で検証
has_field 'email' => (
    type     => 'Email',
    required => 1,
    unique   => 1,
);
```

### 3. テンプレート分割

```text
root/src/
├── wrapper.tt         # 共通レイアウト
├── header.tt          # ヘッダー
├── footer.tt          # フッター
├── index.tt
└── user/
    ├── list.tt
    └── view.tt
```

## 公式リソース

- **公式サイト**: http://www.catalystframework.org/
- **ドキュメント**: https://metacpan.org/pod/Catalyst::Manual
- **GitHub**: https://github.com/perl-catalyst/catalyst-runtime
- **チュートリアル**: https://metacpan.org/pod/Catalyst::Manual::Tutorial
- **CPAN**: https://metacpan.org/

## まとめ

Catalystは、Perl言語のMVCフレームワークです。豊富なプラグインエコシステム、CPAN統合、DBIx::Class（ORM）により、エンタープライズWebアプリケーション開発を実現します。2005年から長年の実績があり、Perl環境での堅牢なWebアプリ開発に適しています。ただし、近年の新規採用は少なく、モダンなフレームワークへの移行が進んでいます。

---

**最終更新**: 2025-12-06
**対象バージョン**: Catalyst 5.90+
**注**: 新規プロジェクトではMojolicious等のモダンフレームワーク検討を推奨
