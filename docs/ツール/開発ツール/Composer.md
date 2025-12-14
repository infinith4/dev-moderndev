# Composer

## 概要

**Composer**は、PHP向けの依存関係管理ツールです。`composer.json`によるパッケージ定義、Packagistレジストリからの自動インストール、オートローディング機能により、PHPプロジェクトの依存関係を効率的に管理します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Nils Adermann / Jordi Boggiano |
| **種別** | PHP依存関係管理ツール |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://getcomposer.org/ |
| **ドキュメント** | https://getcomposer.org/doc/ |

## 主な特徴

### 1. 依存関係管理
- **composer.json**: パッケージ定義
- **composer.lock**: バージョン固定
- **バージョン制約**: セマンティックバージョニング
- **依存解決**: 競合自動解決

### 2. Packagist連携
- **パッケージレジストリ**: 40万以上のパッケージ
- **自動ダウンロード**: `composer require`
- **プライベートリポジトリ**: Git、Satis
- **VCSサポート**: GitHub、GitLab、Bitbucket

### 3. オートローディング
- **PSR-4**: 名前空間ベース
- **PSR-0**: クラス名ベース（非推奨）
- **Classmap**: ディレクトリスキャン
- **Files**: 手動指定ファイル

### 4. スクリプト機能
- **フック**: インストール前後の処理
- **カスタムコマンド**: 独自スクリプト定義
- **イベント**: pre-install、post-updateなど
- **環境変数**: プラットフォーム要件

## 使い方

### インストール

```bash
# ローカルインストール
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"

# グローバルインストール（Unix/Mac）
sudo mv composer.phar /usr/local/bin/composer

# グローバルインストール（Windows）
# https://getcomposer.org/Composer-Setup.exe

# バージョン確認
composer --version
```

### プロジェクト初期化

```bash
# composer.json 作成
composer init

# 対話式で以下を設定:
# - Package name: vendor/project
# - Description
# - Author
# - Minimum Stability
# - License
# - Dependencies
```

```json
// composer.json（生成例）
{
    "name": "mycompany/myproject",
    "description": "My awesome project",
    "type": "project",
    "license": "MIT",
    "authors": [
        {
            "name": "John Doe",
            "email": "john@example.com"
        }
    ],
    "require": {
        "php": "^8.1"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

### パッケージインストール

```bash
# パッケージ追加
composer require guzzlehttp/guzzle

# 開発用パッケージ追加
composer require --dev phpunit/phpunit

# 特定バージョン指定
composer require monolog/monolog:^2.0

# 複数パッケージ同時インストール
composer require symfony/http-foundation symfony/routing

# パッケージ削除
composer remove guzzlehttp/guzzle

# 全パッケージインストール（composer.lock基準）
composer install

# パッケージ更新
composer update

# 特定パッケージのみ更新
composer update monolog/monolog
```

### バージョン制約

```json
// composer.json
{
    "require": {
        "vendor/package": "1.0.0",        // 厳密に1.0.0
        "vendor/package": "^1.2.3",       // >=1.2.3 <2.0.0
        "vendor/package": "~1.2.3",       // >=1.2.3 <1.3.0
        "vendor/package": ">=1.2.3",      // 1.2.3以上
        "vendor/package": ">=1.2.3 <2.0", // 1.2.3以上2.0未満
        "vendor/package": "1.2.*",        // >=1.2.0 <1.3.0
        "vendor/package": "dev-master"    // masterブランチ最新
    }
}
```

### オートローディング

```json
// composer.json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/",
            "Database\\": "database/"
        },
        "psr-0": {
            "": "src/"
        },
        "classmap": [
            "app/Models",
            "app/Controllers"
        ],
        "files": [
            "app/helpers.php"
        ]
    }
}
```

```bash
# オートローダー再生成
composer dump-autoload

# 最適化されたオートローダー生成（本番環境）
composer dump-autoload --optimize
```

```php
// index.php
<?php
require __DIR__ . '/vendor/autoload.php';

use App\Services\UserService;
use GuzzleHttp\Client;

$userService = new UserService();
$client = new Client();
```

### スクリプト定義

```json
// composer.json
{
    "scripts": {
        "test": "phpunit",
        "lint": "phpcs --standard=PSR12 src/",
        "fix": "phpcbf --standard=PSR12 src/",
        "post-install-cmd": [
            "@php artisan key:generate --ansi"
        ],
        "post-update-cmd": [
            "@php artisan optimize"
        ],
        "dev": [
            "Composer\\Config::disableProcessTimeout",
            "php -S localhost:8000 -t public"
        ]
    }
}
```

```bash
# スクリプト実行
composer test
composer lint
composer fix
composer dev
```

### プラットフォーム要件

```json
// composer.json
{
    "require": {
        "php": "^8.1",
        "ext-mbstring": "*",
        "ext-pdo": "*",
        "ext-gd": "*"
    },
    "config": {
        "platform": {
            "php": "8.1.0"
        }
    }
}
```

### プライベートリポジトリ

```json
// composer.json
{
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/mycompany/private-package"
        },
        {
            "type": "composer",
            "url": "https://repo.packagist.com/mycompany/"
        }
    ],
    "require": {
        "mycompany/private-package": "^1.0"
    }
}
```

```bash
# GitHub Personal Access Token設定
composer config --global github-oauth.github.com <token>

# GitLab Private Token設定
composer config --global gitlab-oauth.gitlab.com <token>
```

### Laravel プロジェクト

```bash
# Laravel新規プロジェクト作成
composer create-project laravel/laravel myproject

# パッケージ追加
cd myproject
composer require laravel/sanctum
composer require --dev laravel/pint

# 依存関係インストール
composer install

# オートローダー最適化
composer dump-autoload --optimize
```

### Symfony プロジェクト

```bash
# Symfony新規プロジェクト作成
composer create-project symfony/skeleton myproject
cd myproject

# Webアプリケーション用パッケージ追加
composer require webapp

# デバッグ用パッケージ追加
composer require --dev symfony/debug-bundle
composer require --dev symfony/maker-bundle
```

### Docker統合

```dockerfile
# Dockerfile
FROM php:8.1-fpm

# Composerインストール
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 依存関係インストール
WORKDIR /var/www/html
COPY composer.json composer.lock ./
RUN composer install --no-dev --optimize-autoloader --no-interaction

COPY . .

CMD ["php-fpm"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/var/www/html
    environment:
      - COMPOSER_MEMORY_LIMIT=-1

  composer:
    image: composer:latest
    volumes:
      - .:/app
    command: install
```

### CI/CD統合

#### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.1'
          extensions: mbstring, pdo, gd
          coverage: xdebug

      - name: Validate composer.json
        run: composer validate --strict

      - name: Cache Composer dependencies
        uses: actions/cache@v3
        with:
          path: vendor
          key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
          restore-keys: ${{ runner.os }}-composer-

      - name: Install dependencies
        run: composer install --prefer-dist --no-progress

      - name: Run tests
        run: composer test
```

#### GitLab CI/CD

```yaml
# .gitlab-ci.yml
image: php:8.1

cache:
  paths:
    - vendor/

before_script:
  - apt-get update -yqq
  - apt-get install -yqq git unzip
  - curl -sS https://getcomposer.org/installer | php
  - php composer.phar install

test:
  stage: test
  script:
    - php composer.phar test
```

### キャッシュ・パフォーマンス

```bash
# キャッシュクリア
composer clear-cache

# 並列ダウンロード（Prestissimo - Composer 1.x）
composer global require hirak/prestissimo

# Composer 2.x（デフォルトで並列）
# 設定不要

# メモリ制限解除
COMPOSER_MEMORY_LIMIT=-1 composer install

# パフォーマンス最適化
composer install --no-dev --optimize-autoloader --classmap-authoritative
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **環境構築** | 依存関係インストール | プロジェクトセットアップ |
| **実装** | ライブラリ追加 | 新機能開発時のパッケージ追加 |
| **テスト** | テストツール管理 | PHPUnit、Codeception等 |
| **導入** | 本番デプロイ | 最適化されたオートローダー生成 |

## メリット

- **依存関係管理**: 自動インストール・更新
- **Packagist**: 40万以上のパッケージ
- **バージョン固定**: composer.lockで再現性保証
- **オートローディング**: PSR-4、クラスマップ
- **スクリプト機能**: タスク自動化
- **無料**: オープンソース
- **標準ツール**: PHP開発で事実上の標準

## デメリット

- **ディスク容量**: vendor/ディレクトリ肥大化
- **インストール時間**: 大量パッケージで時間がかかる
- **メモリ使用**: 依存解決で大量メモリ消費
- **バージョン競合**: 複雑な依存関係で解決困難
- **セキュリティ**: パッケージの脆弱性リスク
- **PHP専用**: 他言語非対応

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Composer** | PHP標準、Packagist | 無料 | PHP開発 |
| **npm** | Node.js、npm registry | 無料 | JavaScript開発 |
| **pip** | Python、PyPI | 無料 | Python開発 |
| **Bundler** | Ruby、RubyGems | 無料 | Ruby開発 |

## ベストプラクティス

### 1. composer.lockをコミット

```bash
# 再現性のため必ずコミット
git add composer.lock
git commit -m "Update dependencies"
```

### 2. 本番環境で最適化

```bash
composer install --no-dev --optimize-autoloader --classmap-authoritative
```

### 3. セマンティックバージョニング

```json
{
    "require": {
        "vendor/package": "^2.0"  // >=2.0.0 <3.0.0
    }
}
```

### 4. セキュリティ監査

```bash
# Composer Audit（Composer 2.4+）
composer audit

# または、Roaveを使用
composer global require roave/security-advisories:dev-latest
```

## 公式リソース

- **公式サイト**: https://getcomposer.org/
- **ドキュメント**: https://getcomposer.org/doc/
- **Packagist**: https://packagist.org/
- **GitHub**: https://github.com/composer/composer
- **Satis（プライベートレジストリ）**: https://github.com/composer/satis

## まとめ

Composerは、PHP向けの依存関係管理ツールです。`composer.json`によるパッケージ定義、Packagistレジストリからの自動インストール、PSR-4オートローディングにより、PHPプロジェクトの依存関係を効率的に管理します。Laravel、SymfonyなどモダンなPHPフレームワークでは標準的に使用され、PHP開発の事実上の標準ツールとなっています。

---

**最終更新**: 2025-12-10
**対象バージョン**: Composer 2.6+
