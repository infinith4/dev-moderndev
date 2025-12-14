# CakePHP

## 概要

**CakePHP**は、PHPのMVCフレームワークです。Ruby on Railsに影響を受けた設定より規約（Convention over Configuration）の思想、スキャフォールディング、ORMによる高速開発により、Webアプリケーション開発を効率化します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Cake Software Foundation |
| **種別** | PHPフレームワーク（MVC） |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://cakephp.org/ |
| **ドキュメント** | https://book.cakephp.org/ |

## 主な特徴

### 1. MVC アーキテクチャ
- **Model**: データベースとビジネスロジック
- **View**: 表示層（テンプレート）
- **Controller**: リクエスト処理・制御

### 2. ORM（Object-Relational Mapping）
- クエリビルダー
- アソシエーション（関連）
- バリデーション
- コールバック

### 3. 規約（Convention）
- ファイル・クラス命名規則
- データベーステーブル命名規則
- 自動ルーティング
- スキャフォールディング

### 4. ビルトイン機能
- 認証・認可
- セッション管理
- キャッシュ
- 国際化（i18n）
- フォームヘルパー
- バリデーション

## 使い方

### セットアップ

```bash
# Composerでインストール（推奨）
composer create-project --prefer-dist cakephp/app:~5.0 myapp

cd myapp

# データベース設定
cp config/app_local.example.php config/app_local.php
vi config/app_local.php

# 'Datasources' => [
#     'default' => [
#         'host' => 'localhost',
#         'username' => 'my_app',
#         'password' => 'secret',
#         'database' => 'my_app',
#     ],
# ],

# 開発サーバー起動
bin/cake server

# http://localhost:8765 にアクセス
```

### プロジェクト構造

```text
myapp/
├── bin/                   # 実行スクリプト
│   └── cake              # CLIツール
├── config/               # 設定ファイル
│   ├── app.php           # アプリケーション設定
│   ├── app_local.php     # ローカル設定（DB等）
│   └── routes.php        # ルーティング
├── src/                  # アプリケーションコード
│   ├── Controller/       # コントローラー
│   ├── Model/            # モデル
│   │   ├── Entity/       # エンティティ
│   │   └── Table/        # テーブルクラス
│   ├── View/             # ビュー（テンプレート）
│   └── Application.php   # アプリケーションブートストラップ
├── templates/            # テンプレートファイル
│   ├── layout/           # レイアウト
│   └── Users/            # Users Controller用テンプレート
├── webroot/              # 公開ディレクトリ
│   ├── css/
│   ├── js/
│   └── index.php         # エントリーポイント
└── tests/                # テスト
```

### データベース・マイグレーション

```bash
# マイグレーション作成
bin/cake bake migration CreateUsers

# マイグレーションファイル編集
vi config/Migrations/20250106120000_CreateUsers.php
```

```php
<?php
// config/Migrations/20250106120000_CreateUsers.php
use Migrations\AbstractMigration;

class CreateUsers extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('users');
        $table->addColumn('email', 'string', [
            'limit' => 255,
            'null' => false,
        ]);
        $table->addColumn('password', 'string', [
            'limit' => 255,
            'null' => false,
        ]);
        $table->addColumn('name', 'string', [
            'limit' => 100,
            'null' => false,
        ]);
        $table->addColumn('created', 'datetime', [
            'default' => null,
            'null' => false,
        ]);
        $table->addColumn('modified', 'datetime', [
            'default' => null,
            'null' => false,
        ]);
        $table->create();
    }
}
```

```bash
# マイグレーション実行
bin/cake migrations migrate

# ロールバック
bin/cake migrations rollback
```

### モデル（Model）

```php
<?php
// src/Model/Table/UsersTable.php
namespace App\Model\Table;

use Cake\ORM\Table;
use Cake\Validation\Validator;

class UsersTable extends Table
{
    public function initialize(array $config): void
    {
        parent::initialize($config);

        $this->setTable('users');
        $this->setDisplayField('name');
        $this->setPrimaryKey('id');

        $this->addBehavior('Timestamp');

        // アソシエーション
        $this->hasMany('Articles', [
            'foreignKey' => 'user_id'
        ]);
    }

    public function validationDefault(Validator $validator): Validator
    {
        $validator
            ->notEmptyString('email')
            ->email('email')
            ->requirePresence('email', 'create')
            ->maxLength('email', 255);

        $validator
            ->notEmptyString('password')
            ->minLength('password', 8)
            ->requirePresence('password', 'create');

        $validator
            ->notEmptyString('name')
            ->maxLength('name', 100);

        return $validator;
    }
}
```

```php
<?php
// src/Model/Entity/User.php
namespace App\Model\Entity;

use Cake\ORM\Entity;
use Authentication\PasswordHasher\DefaultPasswordHasher;

class User extends Entity
{
    protected array $_accessible = [
        'email' => true,
        'password' => true,
        'name' => true,
        'created' => true,
        'modified' => true,
    ];

    protected array $_hidden = [
        'password',
    ];

    protected function _setPassword(string $password): ?string
    {
        if (strlen($password) > 0) {
            return (new DefaultPasswordHasher())->hash($password);
        }
        return null;
    }
}
```

### コントローラー（Controller）

```php
<?php
// src/Controller/UsersController.php
namespace App\Controller;

use App\Controller\AppController;

class UsersController extends AppController
{
    public function index()
    {
        $users = $this->paginate($this->Users);

        $this->set(compact('users'));
    }

    public function view($id = null)
    {
        $user = $this->Users->get($id, [
            'contain' => ['Articles'],
        ]);

        $this->set(compact('user'));
    }

    public function add()
    {
        $user = $this->Users->newEmptyEntity();

        if ($this->request->is('post')) {
            $user = $this->Users->patchEntity($user, $this->request->getData());

            if ($this->Users->save($user)) {
                $this->Flash->success(__('The user has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The user could not be saved. Please, try again.'));
        }

        $this->set(compact('user'));
    }

    public function edit($id = null)
    {
        $user = $this->Users->get($id);

        if ($this->request->is(['patch', 'post', 'put'])) {
            $user = $this->Users->patchEntity($user, $this->request->getData());

            if ($this->Users->save($user)) {
                $this->Flash->success(__('The user has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The user could not be saved. Please, try again.'));
        }

        $this->set(compact('user'));
    }

    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $user = $this->Users->get($id);

        if ($this->Users->delete($user)) {
            $this->Flash->success(__('The user has been deleted.'));
        } else {
            $this->Flash->error(__('The user could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }
}
```

### ビュー（View/Template）

```php
<?php
// templates/Users/index.php
?>
<div class="users index content">
    <h3><?= __('Users') ?></h3>
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th><?= $this->Paginator->sort('id') ?></th>
                    <th><?= $this->Paginator->sort('email') ?></th>
                    <th><?= $this->Paginator->sort('name') ?></th>
                    <th><?= $this->Paginator->sort('created') ?></th>
                    <th class="actions"><?= __('Actions') ?></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($users as $user): ?>
                <tr>
                    <td><?= $this->Number->format($user->id) ?></td>
                    <td><?= h($user->email) ?></td>
                    <td><?= h($user->name) ?></td>
                    <td><?= h($user->created) ?></td>
                    <td class="actions">
                        <?= $this->Html->link(__('View'), ['action' => 'view', $user->id]) ?>
                        <?= $this->Html->link(__('Edit'), ['action' => 'edit', $user->id]) ?>
                        <?= $this->Form->postLink(__('Delete'), ['action' => 'delete', $user->id], ['confirm' => __('Are you sure you want to delete # {0}?', $user->id)]) ?>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <div class="paginator">
        <?= $this->Paginator->prev('< ' . __('previous')) ?>
        <?= $this->Paginator->numbers() ?>
        <?= $this->Paginator->next(__('next') . ' >') ?>
    </div>
</div>
```

```php
<?php
// templates/Users/add.php
?>
<div class="users form content">
    <?= $this->Form->create($user) ?>
    <fieldset>
        <legend><?= __('Add User') ?></legend>
        <?php
            echo $this->Form->control('email');
            echo $this->Form->control('password');
            echo $this->Form->control('name');
        ?>
    </fieldset>
    <?= $this->Form->button(__('Submit')) ?>
    <?= $this->Form->end() ?>
</div>
```

### スキャフォールディング（Bake）

```bash
# モデル・コントローラー・ビュー一括生成
bin/cake bake all Users

# 個別生成
bin/cake bake model Users
bin/cake bake controller Users
bin/cake bake template Users

# 既存テーブルから全モデル生成
bin/cake bake model --all
```

### ルーティング

```php
<?php
// config/routes.php
use Cake\Routing\RouteBuilder;
use Cake\Routing\Router;

Router::defaultRouteClass('DashedRoute');

Router::scope('/', function (RouteBuilder $routes) {
    // デフォルトルート
    $routes->connect('/', ['controller' => 'Pages', 'action' => 'display', 'home']);

    // CRUD ルート（規約）
    // /users → UsersController::index()
    // /users/add → UsersController::add()
    // /users/view/1 → UsersController::view(1)

    // カスタムルート
    $routes->connect('/login', ['controller' => 'Users', 'action' => 'login']);
    $routes->connect('/logout', ['controller' => 'Users', 'action' => 'logout']);

    // RESTful ルート
    $routes->resources('Articles');

    $routes->fallbacks('DashedRoute');
});
```

### 認証（Authentication）

```bash
# 認証プラグインインストール
composer require cakephp/authentication:^3.0
```

```php
<?php
// src/Application.php
use Authentication\AuthenticationService;
use Authentication\Middleware\AuthenticationMiddleware;
use Psr\Http\Message\ServerRequestInterface;

class Application extends BaseApplication
{
    public function bootstrap(): void
    {
        parent::bootstrap();

        $this->addPlugin('Authentication');
    }

    public function middleware(MiddlewareQueue $middlewareQueue): MiddlewareQueue
    {
        $middlewareQueue
            ->add(new ErrorHandlerMiddleware(Configure::read('Error')))
            ->add(new AssetMiddleware([
                'cacheTime' => Configure::read('Asset.cacheTime'),
            ]))
            ->add(new RoutingMiddleware($this))
            ->add(new AuthenticationMiddleware($this));

        return $middlewareQueue;
    }

    public function getAuthenticationService(ServerRequestInterface $request): AuthenticationService
    {
        $service = new AuthenticationService();

        $service->setConfig([
            'unauthenticatedRedirect' => '/users/login',
            'queryParam' => 'redirect',
        ]);

        $fields = [
            'username' => 'email',
            'password' => 'password'
        ];

        $service->loadAuthenticator('Authentication.Session');
        $service->loadAuthenticator('Authentication.Form', [
            'fields' => $fields,
            'loginUrl' => '/users/login',
        ]);

        $service->loadIdentifier('Authentication.Password', compact('fields'));

        return $service;
    }
}
```

```php
<?php
// src/Controller/UsersController.php
public function login()
{
    $result = $this->Authentication->getResult();

    if ($result->isValid()) {
        $target = $this->Authentication->getLoginRedirect() ?? '/articles';
        return $this->redirect($target);
    }

    if ($this->request->is('post') && !$result->isValid()) {
        $this->Flash->error('Invalid username or password');
    }
}

public function logout()
{
    $this->Authentication->logout();
    return $this->redirect(['controller' => 'Users', 'action' => 'login']);
}
```

### API開発

```php
<?php
// src/Controller/Api/ArticlesController.php
namespace App\Controller\Api;

use Cake\Controller\Controller;

class ArticlesController extends Controller
{
    public function initialize(): void
    {
        parent::initialize();

        $this->loadComponent('RequestHandler');
        $this->RequestHandler->renderAs($this, 'json');
    }

    public function index()
    {
        $articles = $this->Articles->find('all');

        $this->set([
            'articles' => $articles,
            '_serialize' => ['articles']
        ]);
    }

    public function view($id)
    {
        $article = $this->Articles->get($id);

        $this->set([
            'article' => $article,
            '_serialize' => ['article']
        ]);
    }

    public function add()
    {
        $this->request->allowMethod(['post']);

        $article = $this->Articles->newEmptyEntity();
        $article = $this->Articles->patchEntity($article, $this->request->getData());

        if ($this->Articles->save($article)) {
            $message = 'Created';
        } else {
            $message = 'Error';
        }

        $this->set([
            'message' => $message,
            'article' => $article,
            '_serialize' => ['message', 'article']
        ]);
    }
}
```

```php
<?php
// config/routes.php
Router::prefix('api', function (RouteBuilder $routes) {
    $routes->setExtensions(['json']);
    $routes->resources('Articles');
});

// GET  /api/articles.json
// GET  /api/articles/1.json
// POST /api/articles.json
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | プロトタイピング | スキャフォールディングで高速試作 |
| **設計** | データモデル設計 | マイグレーション、ORM |
| **実装** | Webアプリ開発 | MVC、CRUD実装 |
| **テスト** | ユニット・統合テスト | PHPUnit統合 |

## メリット

- **高速開発**: 規約、スキャフォールディング
- **ORM**: データベース操作簡単
- **ビルトイン機能**: 認証、バリデーション、キャッシュ
- **セキュリティ**: CSRF、XSS、SQLインジェクション対策
- **コミュニティ**: 長い歴史、豊富なドキュメント
- **柔軟性**: プラグインシステム

## デメリット

- **学習曲線**: 規約の習得が必要
- **パフォーマンス**: ORMオーバーヘッド
- **モダン度**: Laravel等に比べ古い設計
- **コミュニティ縮小**: Laravel人気により縮小傾向
- **大規模開発困難**: マイクロサービスには不向き

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **CakePHP** | 規約重視、高速開発 | 無料 | 中小規模Web  アプリ |
| **Laravel** | モダン、人気No.1 | 無料 | モダンPHP開発全般 |
| **Symfony** | エンタープライズ | 無料 | 大規模・複雑なアプリ |
| **CodeIgniter** | 軽量、シンプル | 無料 | 小規模、レガシー環境 |

## ベストプラクティス

### 1. 命名規約

```text
# テーブル: 複数形、小文字、アンダースコア
users, blog_posts, user_profiles

# モデル: 単数形、Pascal Case
User, BlogPost, UserProfile

# コントローラー: 複数形、Pascal Case + Controller
UsersController, BlogPostsController

# ビュー: 小文字、アンダースコア
index.php, add.php, edit.php
```

### 2. ファット・モデル、スリム・コントローラー

```php
<?php
// ビジネスロジックはモデルに
// src/Model/Table/UsersTable.php
public function findActive($query)
{
    return $query->where(['Users.active' => true]);
}

// コントローラーはシンプルに
// src/Controller/UsersController.php
public function index()
{
    $users = $this->Users->find('active');
    $this->set(compact('users'));
}
```

### 3. バリデーション・ルール

```php
<?php
// src/Model/Table/UsersTable.php
public function validationDefault(Validator $validator): Validator
{
    $validator
        ->email('email')
        ->requirePresence('email', 'create')
        ->notEmptyString('email')
        ->add('email', 'unique', [
            'rule' => 'validateUnique',
            'provider' => 'table'
        ]);

    return $validator;
}
```

## 公式リソース

- **公式サイト**: https://cakephp.org/
- **ドキュメント**: https://book.cakephp.org/5/
- **GitHub**: https://github.com/cakephp/cakephp
- **チュートリアル**: https://book.cakephp.org/5/en/tutorials-and-examples.html
- **プラグイン**: https://plugins.cakephp.org/

## まとめ

CakePHPは、規約より設定の思想に基づいたPHP MVCフレームワークです。スキャフォールディング、ORM、ビルトイン機能により、高速なWebアプリケーション開発を実現します。長い歴史と豊富なドキュメントを持ち、中小規模のWebアプリ開発に最適なフレームワークです。

---

**最終更新**: 2025-12-06
**対象バージョン**: CakePHP 5.0+
