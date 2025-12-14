# Chef

## 概要

**Chef**は、Rubyベースのインフラ自動化・構成管理ツールです。「Infrastructure as Code」アプローチにより、サーバー設定をコードで記述・バージョン管理し、大規模インフラの一貫した構成を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Progress Software（旧Opscode） |
| **種別** | 構成管理・インフラ自動化ツール |
| **ライセンス** | Apache 2.0 License（オープンソース） |
| **料金** | 🟡 Chef Infra（無料） / Chef Automate（有料） |
| **公式サイト** | https://www.chef.io/ |
| **ドキュメント** | https://docs.chef.io/ |

## 主な特徴

### 1. Infrastructure as Code
- **Ruby DSL**: 直感的なコード記述
- **Cookbook**: 再利用可能な設定レシピ
- **Recipe**: サーバー構成手順
- **バージョン管理**: Git統合

### 2. Pull型アーキテクチャ
- **Chef Server**: 中央管理サーバー
- **Chef Client**: ノード上のエージェント
- **定期実行**: 自動収束（convergence）
- **状態報告**: 変更内容のレポート

### 3. プラットフォーム対応
- **Linux**: RHEL、Ubuntu、CentOS等
- **Windows**: PowerShell統合
- **クラウド**: AWS、Azure、GCP
- **コンテナ**: Docker、Kubernetes

### 4. テスト・CI/CD統合
- **Test Kitchen**: 仮想環境テスト
- **InSpec**: コンプライアンステスト
- **ChefSpec**: ユニットテスト
- **Foodcritic**: コード品質チェック

## 使い方

### セットアップ

```bash
# Chef Workstationインストール（Mac）
brew install --cask chef-workstation

# または、公式インストーラー（Linux/Windows）
# https://downloads.chef.io/tools/workstation

# バージョン確認
chef --version
knife --version
```

### Chef リポジトリ作成

```bash
# Chef リポジトリ初期化
chef generate repo chef-repo
cd chef-repo

# Cookbook作成
chef generate cookbook cookbooks/myapp

# ディレクトリ構造
chef-repo/
├── cookbooks/
│   └── myapp/
│       ├── recipes/
│       │   └── default.rb
│       ├── attributes/
│       ├── files/
│       ├── templates/
│       ├── metadata.rb
│       └── README.md
├── data_bags/
├── environments/
├── roles/
└── .chef/
```

### Recipe（レシピ）作成

```ruby
# cookbooks/myapp/recipes/default.rb

# パッケージインストール
package 'nginx' do
  action :install
end

# サービス起動
service 'nginx' do
  action [:enable, :start]
end

# ファイル作成
file '/var/www/html/index.html' do
  content '<h1>Hello from Chef!</h1>'
  owner 'www-data'
  group 'www-data'
  mode '0644'
end

# テンプレートファイル配置
template '/etc/nginx/sites-available/default' do
  source 'nginx-default.erb'
  variables(
    server_name: 'example.com',
    port: 80
  )
  notifies :reload, 'service[nginx]', :delayed
end

# ディレクトリ作成
directory '/var/www/myapp' do
  owner 'www-data'
  group 'www-data'
  mode '0755'
  action :create
end

# Git リポジトリクローン
git '/var/www/myapp' do
  repository 'https://github.com/username/myapp.git'
  revision 'main'
  action :sync
end

# コマンド実行
execute 'bundle install' do
  cwd '/var/www/myapp'
  command 'bundle install --deployment'
  user 'www-data'
  not_if { ::File.exist?('/var/www/myapp/vendor/bundle') }
end
```

### Template（テンプレート）

```erb
# cookbooks/myapp/templates/nginx-default.erb
server {
    listen <%= @port %>;
    server_name <%= @server_name %>;

    root /var/www/myapp/public;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
    }
}
```

### Attribute（属性）

```ruby
# cookbooks/myapp/attributes/default.rb

# デフォルト属性
default['myapp']['version'] = '1.0.0'
default['myapp']['port'] = 8080
default['myapp']['user'] = 'appuser'

# 環境別属性
default['myapp']['database']['host'] = 'localhost'
default['myapp']['database']['port'] = 5432

# 配列・ハッシュ
default['myapp']['packages'] = ['git', 'curl', 'vim']
default['myapp']['config'] = {
  'debug' => false,
  'log_level' => 'info'
}
```

```ruby
# recipes/default.rb で属性使用
package node['myapp']['packages']

file "/etc/myapp/config.yml" do
  content node['myapp']['config'].to_yaml
end
```

### Chef Solo（単体実行）

```bash
# Chef Solo設定
cat > solo.rb <<EOF
file_cache_path "/tmp/chef-solo"
cookbook_path "/path/to/chef-repo/cookbooks"
EOF

# Chef Solo実行
sudo chef-solo -c solo.rb -o 'recipe[myapp::default]'

# JSON形式で属性上書き
cat > node.json <<EOF
{
  "myapp": {
    "port": 9000
  },
  "run_list": ["recipe[myapp::default]"]
}
EOF

sudo chef-solo -c solo.rb -j node.json
```

### Test Kitchen（テスト環境）

```yaml
# .kitchen.yml
driver:
  name: vagrant

provisioner:
  name: chef_zero

platforms:
  - name: ubuntu-22.04
  - name: centos-8

suites:
  - name: default
    run_list:
      - recipe[myapp::default]
    attributes:
      myapp:
        port: 8080
```

```bash
# Test Kitchen コマンド
kitchen list              # インスタンス一覧
kitchen create            # インスタンス作成
kitchen converge          # レシピ適用
kitchen verify            # InSpecテスト実行
kitchen test              # 全テスト（create → converge → verify → destroy）
kitchen destroy           # インスタンス削除

# 特定インスタンスのみ
kitchen test default-ubuntu-2204
```

### InSpec（コンプライアンステスト）

```ruby
# test/integration/default/default_test.rb

describe package('nginx') do
  it { should be_installed }
end

describe service('nginx') do
  it { should be_enabled }
  it { should be_running }
end

describe file('/var/www/html/index.html') do
  it { should exist }
  its('content') { should match /Hello from Chef/ }
  its('owner') { should eq 'www-data' }
  its('mode') { should cmp '0644' }
end

describe port(80) do
  it { should be_listening }
end

describe command('nginx -v') do
  its('stderr') { should match /nginx/ }
end
```

### ChefSpec（ユニットテスト）

```ruby
# spec/unit/recipes/default_spec.rb
require 'chefspec'

describe 'myapp::default' do
  let(:chef_run) { ChefSpec::SoloRunner.new.converge(described_recipe) }

  it 'installs nginx' do
    expect(chef_run).to install_package('nginx')
  end

  it 'enables and starts nginx service' do
    expect(chef_run).to enable_service('nginx')
    expect(chef_run).to start_service('nginx')
  end

  it 'creates index.html' do
    expect(chef_run).to create_file('/var/www/html/index.html')
      .with_content('Hello from Chef!')
      .with_owner('www-data')
      .with_mode('0644')
  end
end
```

```bash
# ChefSpec実行
rspec
```

### Knife（Chef管理ツール）

```bash
# Knife設定
knife configure

# Cookbook アップロード
knife cookbook upload myapp

# ノード一覧
knife node list

# ノード情報
knife node show node1.example.com

# レシピ実行
knife ssh 'name:node1*' 'sudo chef-client' -x ubuntu -i ~/.ssh/id_rsa

# Bootstrap（新規ノード登録）
knife bootstrap 192.168.1.10 \
  --ssh-user ubuntu \
  --sudo \
  --identity-file ~/.ssh/id_rsa \
  --node-name web1 \
  --run-list 'recipe[myapp::default]'
```

### Role（ロール）

```ruby
# roles/webserver.rb
name 'webserver'
description 'Web Server Role'

run_list(
  'recipe[myapp::default]',
  'recipe[myapp::nginx]'
)

default_attributes(
  'myapp' => {
    'port' => 80
  }
)
```

```bash
# Role アップロード
knife role from file roles/webserver.rb

# ノードに Role 割り当て
knife node run_list add web1 'role[webserver]'
```

### Environment（環境）

```ruby
# environments/production.rb
name 'production'
description 'Production Environment'

cookbook 'myapp', '= 1.2.0'

default_attributes(
  'myapp' => {
    'database' => {
      'host' => 'db.production.example.com'
    }
  }
)

override_attributes(
  'myapp' => {
    'debug' => false
  }
)
```

```bash
# Environment アップロード
knife environment from file environments/production.rb

# ノードに Environment 割り当て
knife node environment set web1 production
```

### Docker統合

```ruby
# cookbooks/myapp/recipes/docker.rb

# Dockerインストール
docker_installation 'default' do
  action :create
end

# Dockerサービス起動
docker_service 'default' do
  action [:create, :start]
end

# Dockerイメージプル
docker_image 'nginx' do
  tag 'latest'
  action :pull
end

# Dockerコンテナ起動
docker_container 'myapp' do
  image 'nginx:latest'
  port '80:80'
  volumes ['/var/www/html:/usr/share/nginx/html']
  action :run
end
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **環境構築** | インフラ構築 | サーバー初期設定、ミドルウェア導入 |
| **実装** | 開発環境統一 | 開発者間での環境一致 |
| **テスト** | テスト環境構築 | Test Kitchen、InSpec |
| **導入** | 本番デプロイ | 一貫した構成管理 |

## メリット

- **Infrastructure as Code**: 設定のコード化・バージョン管理
- **再利用性**: Cookbook・Recipeの共有
- **冪等性**: 何度実行しても同じ結果
- **プラットフォーム対応**: Linux、Windows、クラウド
- **テスト充実**: Test Kitchen、InSpec、ChefSpec
- **コミュニティ**: Supermarket（Cookbook共有）
- **エンタープライズ対応**: Chef Automate

## デメリット

- **学習曲線**: Ruby DSL、概念の習得
- **インフラ複雑化**: Chef Server必須（Chef Solo以外）
- **エージェント必須**: Chef Client常駐
- **実行速度**: Pull型のため遅延
- **デバッグ困難**: エラー原因の特定
- **有料機能**: Chef Automateは商用
- **代替ツール**: Ansible、Terraform優勢

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Chef** | Ruby、Pull型、Cookbook | 無料/有料 | エンタープライズ、複雑な構成 |
| **Ansible** | YAML、Push型、エージェント不要 | 無料/有料 | シンプル、汎用 |
| **Puppet** | Ruby、Pull型、モジュール | 無料/有料 | 大規模、レガシー |
| **Terraform** | HCL、宣言型、クラウドIaaS | 無料/有料 | クラウドインフラ |

## ベストプラクティス

### 1. Cookbookの分割

```ruby
# 小さな責務ごとにRecipe分割
# recipes/default.rb - メインレシピ
# recipes/nginx.rb - Nginx設定
# recipes/database.rb - データベース設定
```

### 2. Attributeの活用

```ruby
# 環境依存値はAttributeで管理
default['myapp']['database']['host'] = 'localhost'
```

### 3. Test Kitchenでテスト

```bash
# 本番適用前に必ずテスト
kitchen test
```

### 4. InSpecでコンプライアンス

```ruby
# セキュリティ要件を InSpec で検証
describe file('/etc/ssh/sshd_config') do
  its('content') { should match /PasswordAuthentication no/ }
end
```

## 公式リソース

- **公式サイト**: https://www.chef.io/
- **ドキュメント**: https://docs.chef.io/
- **Supermarket**: https://supermarket.chef.io/
- **Learn Chef**: https://learn.chef.io/
- **GitHub**: https://github.com/chef/chef

## まとめ

Chefは、Rubyベースのインフラ自動化・構成管理ツールです。Infrastructure as Codeアプローチにより、サーバー設定をコードで記述・バージョン管理し、大規模インフラの一貫した構成を実現します。Test Kitchen、InSpec等の充実したテストツールにより、信頼性の高いインフラ運用を支援します。

---

**最終更新**: 2025-12-10
**対象バージョン**: Chef Infra 18+
