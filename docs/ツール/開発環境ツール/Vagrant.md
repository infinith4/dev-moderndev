# Vagrant

## 概要

Vagrantは、HashiCorp社が開発した仮想開発環境の構築・管理ツールです。VagrantfileというテキストファイルでVM設定を定義し、`vagrant up`コマンドで即座に開発環境を立ち上げられます。VirtualBox、VMware、Docker等の仮想化プラットフォームを統一的なインターフェースで操作でき、チーム全体で一貫した開発環境を共有できます。

## 主な機能

### 1. 仮想環境管理
- **Vagrantfile**: コードで環境定義
- **Box**: 事前構築済みVMイメージ
- **プロビジョニング**: Shell、Ansible、Chef、Puppet
- **ネットワーク設定**: ポートフォワーディング、プライベートネットワーク

### 2. マルチプロバイダー対応
- **VirtualBox**: デフォルト、無料
- **VMware**: Workstation、Fusion（有料プラグイン）
- **Hyper-V**: Windows標準
- **Docker**: コンテナプロバイダー
- **AWS、Azure**: クラウドプロバイダー

### 3. プロビジョニング
- **Shell Script**: シンプルなbashスクリプト
- **Ansible**: YAMLでプレイブック記述
- **Chef**: Rubyベースのレシピ
- **Puppet**: 宣言的なマニフェスト
- **Docker**: Dockerコンテナ起動

### 4. ネットワーク
- **Port Forwarding**: ホスト⇔ゲスト間のポート転送
- **Private Network**: ホストオンリーネットワーク
- **Public Network**: ブリッジネットワーク
- **固定IP**: 静的IPアドレス割り当て

### 5. 共有フォルダ
- **デフォルト同期**: プロジェクトディレクトリを/vagrantにマウント
- **NFS**: 高速ファイル共有
- **rsync**: 一方向同期

### 6. スナップショット
- **環境保存**: 現在の状態を保存
- **復元**: 保存した状態に戻す
- **複数スナップショット**: 複数ポイント管理

## 利用方法

### インストール

```bash
# 公式サイトからダウンロード
# https://www.vagrantup.com/downloads

# Windows: インストーラー実行
vagrant_x.x.x_windows_amd64.msi

# macOS: DMGまたはHomebrew
brew install --cask vagrant

# Linux (Ubuntu/Debian)
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant

# バージョン確認
vagrant --version

# VirtualBoxインストール（プロバイダー）
# https://www.virtualbox.org/wiki/Downloads
```

### 基本的な使い方

```bash
# プロジェクトディレクトリ作成
mkdir my-vagrant-project
cd my-vagrant-project

# Vagrantfile初期化（Ubuntu 22.04）
vagrant init ubuntu/jammy64

# VM起動
vagrant up

# SSH接続
vagrant ssh

# VM停止
vagrant halt

# VM削除
vagrant destroy

# VM状態確認
vagrant status
```

### Vagrantfile基本例

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  # ベースBox指定
  config.vm.box = "ubuntu/jammy64"
  
  # ホスト名設定
  config.vm.hostname = "dev-server"
  
  # ポートフォワーディング
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 3000, host: 3000
  
  # プライベートネットワーク（固定IP）
  config.vm.network "private_network", ip: "192.168.33.10"
  
  # 共有フォルダ
  config.vm.synced_folder "./data", "/vagrant_data"
  
  # VMスペック設定
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
    vb.name = "my-dev-vm"
  end
  
  # プロビジョニング（Shell）
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y nginx nodejs npm
  SHELL
end
```

### プロビジョニング（Ansible）

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end
end
```

```yaml
# playbook.yml
---
- hosts: all
  become: yes
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
    
    - name: Install packages
      apt:
        name:
          - nginx
          - nodejs
          - npm
        state: present
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

### マルチマシン構成

```ruby
# Vagrantfile
Vagrant.configure("2") do |config|
  # Webサーバー
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/jammy64"
    web.vm.hostname = "web-server"
    web.vm.network "private_network", ip: "192.168.33.10"
    web.vm.provision "shell", inline: "apt-get update && apt-get install -y nginx"
  end
  
  # DBサーバー
  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/jammy64"
    db.vm.hostname = "db-server"
    db.vm.network "private_network", ip: "192.168.33.11"
    db.vm.provision "shell", inline: "apt-get update && apt-get install -y postgresql"
  end
end
```

```bash
# 特定マシンのみ起動
vagrant up web
vagrant ssh web

# 全マシン起動
vagrant up
```

### Boxの管理

```bash
# Box検索（Vagrant Cloud）
# https://app.vagrantup.com/boxes/search

# Box追加
vagrant box add ubuntu/jammy64

# Box一覧
vagrant box list

# Box削除
vagrant box remove ubuntu/jammy64

# Box更新
vagrant box update
```

### スナップショット

```bash
# スナップショット作成
vagrant snapshot save clean-state

# スナップショット一覧
vagrant snapshot list

# スナップショット復元
vagrant snapshot restore clean-state

# スナップショット削除
vagrant snapshot delete clean-state
```

### プラグイン

```bash
# プラグイン一覧
vagrant plugin list

# 便利なプラグインインストール
vagrant plugin install vagrant-vbguest      # VirtualBox Guest Additions自動更新
vagrant plugin install vagrant-hostmanager  # /etc/hosts自動更新
vagrant plugin install vagrant-disksize     # ディスクサイズ変更
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Vagrant** | 🟢 完全無料 | オープンソース、MIT License |
| **Vagrant VMware Plugin** | 💰 $79 USD（買い切り） | VMware Workstation/Fusion対応 |

## メリット

### ✅ 主な利点

1. **環境再現性**: Vagrantfileで環境をコード化
2. **チーム共有**: 全員が同じ環境を利用
3. **クロスプラットフォーム**: Windows、Mac、Linux対応
4. **無料**: オープンソース、MIT License
5. **マルチプロバイダー**: VirtualBox、VMware、Docker対応
6. **プロビジョニング統合**: Ansible、Chef、Puppet対応
7. **スナップショット**: 環境の保存・復元
8. **豊富なBox**: Vagrant Cloudで公開Box多数
9. **軽量**: Dockerより重いがVM管理が簡単
10. **学習容易**: シンプルなコマンド体系

## デメリット

### ❌ 制約・課題

1. **リソース消費**: VM起動でメモリ・CPU使用量大
2. **起動時間**: Dockerより起動遅い
3. **ディスク使用量**: VMイメージで数GB消費
4. **パフォーマンス**: ホストOSより遅い
5. **Dockerとの比較**: コンテナより重い
6. **Windows制約**: Hyper-VとVirtualBoxの共存不可
7. **共有フォルダ遅い**: NFS設定が必要
8. **メンテナンス**: Box更新が手動
9. **ネットワーク複雑**: マルチマシン構成で設定煩雑
10. **モダン開発**: DevContainerやDockerに移行傾向

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Docker / Docker Compose** | コンテナ、軽量 | Vagrantより高速・軽量 |
| **DevContainer (VS Code)** | VSCode統合開発環境 | Vagrantよりモダン |
| **VirtualBox** | VM管理 | Vagrantより低レベル |
| **Multipass** | Ubuntu VM管理 | VagrantよりシンプルだがUbuntuのみ |
| **Lima** | macOS用Linux VM | Vagrantより軽量だがmacOSのみ |

## 公式リンク

- **公式サイト**: [https://www.vagrantup.com/](https://www.vagrantup.com/)
- **ドキュメント**: [https://developer.hashicorp.com/vagrant/docs](https://developer.hashicorp.com/vagrant/docs)
- **Vagrant Cloud**: [https://app.vagrantup.com/boxes/search](https://app.vagrantup.com/boxes/search)
- **GitHub**: [https://github.com/hashicorp/vagrant](https://github.com/hashicorp/vagrant)
- **プラグイン**: [https://github.com/hashicorp/vagrant/wiki/Available-Vagrant-Plugins](https://github.com/hashicorp/vagrant/wiki/Available-Vagrant-Plugins)

## 関連ドキュメント

- [開発環境ツール一覧](../開発環境ツール/)
- [Docker](../コンテナツール/Docker.md)
- [VirtualBox](./VirtualBox.md)
- [Ansible](../IaCツール/Ansible.md)
- [開発環境セットアップベストプラクティス](../../best-practices/dev-environment-setup.md)

---

**カテゴリ**: 開発環境ツール  
**対象工程**: 実装、テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
