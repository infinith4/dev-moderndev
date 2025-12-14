# Capistrano

## 概要

**Capistrano**は、Rubyベースのリモートサーバー自動化・デプロイツールです。SSH経由での並列実行、ロールベースタスク管理、原子性デプロイにより、Webアプリケーションの安全で効率的なデプロイを実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | オープンソースコミュニティ |
| **種別** | デプロイ・サーバー自動化ツール |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://capistranorb.com/ |
| **ドキュメント** | https://capistranorb.com/ |

## 主な特徴

### 1. SSHベース並列実行
- 複数サーバーへの同時デプロイ
- ロールベースサーバー管理
- エージェント不要（SSHのみ）
- 並列・直列実行制御

### 2. 原子性デプロイ（Atomic Deployment）
- シンボリックリンクによる瞬時切替
- ロールバック機能
- 過去リリース履歴保持
- ダウンタイムゼロ

### 3. フック・プラグイン
- デプロイ前後のカスタムタスク
- プラグインエコシステム
- Rails、Node.js等のプリセット
- Git、SVN統合

### 4. ステージング環境
- 環境別設定（production、staging等）
- 環境固有変数
- ドライラン（--dry-run）

## 使い方

### セットアップ

```bash
# Gemインストール
gem install capistrano

# または、Gemfile に追加
# Gemfile
gem 'capistrano', '~> 3.18'
gem 'capistrano-rails', '~> 1.6'     # Rails用
gem 'capistrano-bundler', '~> 2.1'  # Bundler統合
gem 'capistrano-rbenv', '~> 2.2'    # rbenv統合

bundle install

# Capistranoセットアップ
cap install

# 以下のファイルが生成される
Capfile
config/
├── deploy.rb          # 共通設定
└── deploy/
    ├── production.rb  # 本番環境設定
    └── staging.rb     # ステージング環境設定
lib/capistrano/tasks/ # カスタムタスク
```

### 基本設定

```ruby
# config/deploy.rb
lock '~> 3.18.0'

set :application, 'myapp'
set :repo_url, 'git@github.com:username/myapp.git'

# デプロイ先ディレクトリ
set :deploy_to, '/var/www/myapp'

# Gitブランチ
set :branch, ENV['BRANCH'] || 'main'

# シンボリックリンク
set :linked_files, %w[config/database.yml config/master.key]
set :linked_dirs, %w[log tmp/pids tmp/cache tmp/sockets vendor/bundle public/system public/uploads]

# 保持するリリース数
set :keep_releases, 5

# SSH設定
set :ssh_options, {
  forward_agent: true,
  auth_methods: ['publickey'],
  keys: %w[~/.ssh/id_rsa]
}
```

```ruby
# config/deploy/production.rb
server 'web1.example.com', user: 'deploy', roles: %w[app web db]
server 'web2.example.com', user: 'deploy', roles: %w[app web]
server 'db1.example.com', user: 'deploy', roles: %w[db]

# 環境変数
set :rails_env, 'production'
set :puma_bind, 'unix:///var/www/myapp/shared/tmp/sockets/puma.sock'
```

```ruby
# config/deploy/staging.rb
server 'staging.example.com', user: 'deploy', roles: %w[app web db]

set :rails_env, 'staging'
```

### デプロイディレクトリ構造

```text
/var/www/myapp/
├── current/              # 現在のリリース（シンボリックリンク）
├── releases/             # 過去のリリース
│   ├── 20250106120000/
│   ├── 20250106110000/
│   └── 20250106100000/
├── repo/                 # Gitリポジトリキャッシュ
└── shared/               # 共有ファイル・ディレクトリ
    ├── config/
    │   ├── database.yml
    │   └── master.key
    ├── log/
    ├── tmp/
    ├── vendor/bundle/
    └── public/
        ├── system/
        └── uploads/
```

### デプロイフロー

```bash
# 初回セットアップ
cap production deploy:check

# デプロイ実行
cap production deploy

# デプロイフロー:
# 1. deploy:starting        - デプロイ開始
# 2. deploy:updating        - コード更新（Git pull）
# 3. deploy:publishing      - current シンボリックリンク更新
# 4. deploy:published       - デプロイ完了
# 5. deploy:finishing       - クリーンアップ
# 6. deploy:finished        - 終了

# ロールバック
cap production deploy:rollback

# カスタムタスク実行
cap production app:restart
```

### Rails アプリケーション

```ruby
# Capfile
require 'capistrano/rails'
require 'capistrano/bundler'
require 'capistrano/rbenv'
require 'capistrano/puma'

# config/deploy.rb
set :application, 'myapp'
set :repo_url, 'git@github.com:username/myapp.git'
set :deploy_to, '/var/www/myapp'

# rbenv
set :rbenv_type, :user
set :rbenv_ruby, File.read('.ruby-version').strip

# Bundler
set :bundle_flags, '--deployment'
set :bundle_without, 'development test'

# Puma
set :puma_threads, [4, 16]
set :puma_workers, 2
set :puma_bind, 'unix:///var/www/myapp/shared/tmp/sockets/puma.sock'
set :puma_preload_app, true
```

### Node.js アプリケーション

```ruby
# Capfile
require 'capistrano/npm'

# config/deploy.rb
set :application, 'myapp'
set :repo_url, 'git@github.com:username/myapp.git'
set :deploy_to, '/var/www/myapp'

# npm
set :npm_flags, '--production --silent --no-progress'

# PM2
namespace :pm2 do
  task :start do
    on roles(:app) do
      within current_path do
        execute :pm2, :start, 'ecosystem.config.js', '--env', fetch(:stage)
      end
    end
  end

  task :restart do
    on roles(:app) do
      within current_path do
        execute :pm2, :reload, 'ecosystem.config.js', '--env', fetch(:stage)
      end
    end
  end

  task :stop do
    on roles(:app) do
      within current_path do
        execute :pm2, :stop, 'all'
      end
    end
  end
end

after 'deploy:published', 'pm2:restart'
```

### カスタムタスク

```ruby
# lib/capistrano/tasks/app.rake
namespace :app do
  desc 'アプリケーション再起動'
  task :restart do
    on roles(:app) do
      within current_path do
        execute :touch, 'tmp/restart.txt'
      end
    end
  end

  desc 'データベースマイグレーション'
  task :migrate do
    on roles(:db) do
      within release_path do
        with rails_env: fetch(:rails_env) do
          execute :rake, 'db:migrate'
        end
      end
    end
  end

  desc 'アセットプリコンパイル'
  task :precompile do
    on roles(:web) do
      within release_path do
        with rails_env: fetch(:rails_env) do
          execute :rake, 'assets:precompile'
        end
      end
    end
  end

  desc 'キャッシュクリア'
  task :clear_cache do
    on roles(:app) do
      within current_path do
        execute :rake, 'cache:clear'
      end
    end
  end
end

# フック
after 'deploy:updated', 'app:migrate'
after 'deploy:updated', 'app:precompile'
after 'deploy:published', 'app:restart'
```

### ロール・フィルタ

```ruby
# ロール別実行
task :task_name do
  on roles(:app) do
    # appロールのサーバーでのみ実行
  end

  on roles(:db), in: :sequence do
    # dbロールのサーバーで直列実行
  end

  on roles(:web), in: :parallel do
    # webロールのサーバーで並列実行
  end
end

# フィルタ
set :filter, roles: :app, host: 'web1.example.com'
```

### 環境変数・シークレット

```ruby
# config/deploy.rb
set :default_env, {
  'NODE_ENV' => 'production',
  'RAILS_ENV' => 'production'
}

# dotenv統合
require 'capistrano/dotenv'
set :dotenv_file, '.env.production'

# またはサーバー側で管理
# ~/.bashrc または /etc/environment
```

### デプロイ通知（Slack）

```ruby
# Gemfile
gem 'capistrano-slackify', require: false

# Capfile
require 'capistrano/slackify'

# config/deploy.rb
set :slack_webhook_url, ENV['SLACK_WEBHOOK_URL']
set :slack_channel, '#deployments'
set :slack_username, 'Capistrano'
set :slack_emoji, ':rocket:'

# デプロイ開始通知
before 'deploy:starting', 'slack:notify_starting'

# デプロイ完了通知
after 'deploy:finished', 'slack:notify_finished'

# デプロイ失敗通知
after 'deploy:failed', 'slack:notify_failed'
```

### ドライラン

```bash
# ドライラン（実際には実行しない）
cap production deploy --dry-run

# トレースモード
cap production deploy --trace

# デバッグモード
set :log_level, :debug
```

### CI/CD統合

#### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Setup SSH
        uses: webfactory/ssh-agent@v0.8.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Deploy to Production
        env:
          BRANCH: main
        run: |
          bundle exec cap production deploy
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:production:
  stage: deploy
  image: ruby:3.2
  before_script:
    - 'which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )'
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
    - bundle install
  script:
    - bundle exec cap production deploy
  only:
    - main
  environment:
    name: production
    url: https://example.com
```

### ロールバック戦略

```bash
# 直前のリリースにロールバック
cap production deploy:rollback

# 特定のリリースにロールバック
cap production deploy:rollback ROLLBACK_RELEASE=20250106100000

# ロールバック後の再起動
cap production app:restart
```

### トラブルシューティング

```bash
# デプロイ確認（サーバー接続テスト）
cap production deploy:check

# SSHログイン
cap production ssh

# リモートコマンド実行
cap production invoke COMMAND="ls -la /var/www/myapp"

# ログ確認
cap production logs:tail
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | 開発環境デプロイ | 開発サーバーへの自動デプロイ |
| **テスト** | ステージング環境デプロイ | テスト環境への定期デプロイ |
| **導入** | 本番環境デプロイ | 本番リリース自動化 |
| **運用** | ホットフィックス | 緊急修正の迅速デプロイ |

## メリット

- **原子性デプロイ**: ダウンタイムゼロ、瞬時切替
- **ロールバック**: 過去バージョンへ即座に戻せる
- **並列実行**: 複数サーバーへ同時デプロイ
- **エージェント不要**: SSHのみで動作
- **Ruby DSL**: 柔軟なタスク定義
- **プラグイン豊富**: Rails、Node.js等のプリセット
- **無料**: オープンソース

## デメリット

- **Ruby必須**: Ruby環境が必要
- **学習曲線**: DSL・概念の習得が必要
- **SSH依存**: SSH接続必須、コンテナ環境では工夫必要
- **モダンツール比較**: Kubernetes、Ansibleに比べ古い
- **スケーラビリティ**: 大規模（数百台）では非効率

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Capistrano** | Ruby、SSH、原子性 | 無料 | Railsアプリ、VPSデプロイ |
| **Ansible** | エージェント不要、YAML | 無料 | 汎用サーバー管理 |
| **Kubernetes** | コンテナオーケストレーション | 無料 | クラウドネイティブ |
| **Fabric** | Python、SSH | 無料 | Python環境 |

## ベストプラクティス

### 1. 共有ファイルの分離

```ruby
# 環境ごとに異なる設定ファイルは shared/ に配置
set :linked_files, %w[
  config/database.yml
  config/master.key
  .env.production
]

# 永続化ディレクトリ
set :linked_dirs, %w[
  log
  tmp/pids
  tmp/cache
  tmp/sockets
  vendor/bundle
  public/uploads
]
```

### 2. ゼロダウンタイムデプロイ

```ruby
# Pumaのphased restart
set :puma_preload_app, true
set :puma_phased_restart, true

# データベースマイグレーション
# 後方互換性を保つ（カラム削除は次回デプロイで）
```

### 3. ヘルスチェック

```ruby
namespace :app do
  task :health_check do
    on roles(:web) do
      within current_path do
        execute :curl, '-f', 'http://localhost/health', '||', 'exit 1'
      end
    end
  end
end

after 'deploy:published', 'app:health_check'
```

### 4. ロールバック戦略

```ruby
# デプロイ失敗時の自動ロールバック
after 'deploy:failed', :rollback do
  invoke 'deploy:rollback'
  invoke 'app:restart'
end
```

## 公式リソース

- **公式サイト**: https://capistranorb.com/
- **GitHub**: https://github.com/capistrano/capistrano
- **ドキュメント**: https://capistranorb.com/documentation/getting-started/
- **プラグイン**: https://github.com/capistrano/
- **コミュニティ**: https://groups.google.com/group/capistrano

## まとめ

Capistranoは、Rubyベースのリモートサーバー自動化・デプロイツールです。SSH経由での並列実行、シンボリックリンクによる原子性デプロイ、豊富なプラグインにより、Webアプリケーションの安全で効率的なデプロイを実現します。特にRailsアプリケーションのデプロイでは、長年の実績とベストプラクティスが蓄積されています。

---

**最終更新**: 2025-12-06
**対象バージョン**: Capistrano 3.18+
