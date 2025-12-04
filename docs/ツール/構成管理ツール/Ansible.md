# Ansible

## 概要

Ansibleは、オープンソースの構成管理・自動化ツールです。エージェントレス（SSH）、YAML Playbook、冪等性、モジュール（3000+）により、サーバープロビジョニング、構成管理、アプリケーションデプロイを自動化します。Red Hat開発、シンプルな学習曲線、Ansible Galaxy、Ansible Towerで広く採用されています。

## 主な機能

### 1. 構成管理
- **Playbook**: YAML構成定義
- **モジュール**: パッケージ、サービス、ファイル等
- **Inventory**: ホスト管理
- **冪等性**: 複数回実行安全

### 2. プロビジョニング
- **サーバー**: VM、クラウドインスタンス
- **ネットワーク**: スイッチ、ルーター
- **クラウド**: AWS、Azure、GCP

### 3. オーケストレーション
- **ローリングアップデート**: 順次更新
- **条件分岐**: when句
- **ループ**: with_items

### 4. エージェントレス
- **SSH**: SSH接続
- **Python**: Python実行環境のみ必要
- **WinRM**: Windows対応

## 利用方法

### インストール

```bash
# pipでインストール
pip install ansible

# バージョン確認
ansible --version
```

### Inventory

```ini
# hosts.ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### Playbook（基本）

```yaml
# playbook.yml
---
- name: Setup Web Server
  hosts: webservers
  become: yes

  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start Nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Copy index.html
      copy:
        src: ./index.html
        dest: /var/www/html/index.html
        mode: '0644'
```

### 実行

```bash
# Playbook実行
ansible-playbook -i hosts.ini playbook.yml

# 構文チェック
ansible-playbook playbook.yml --syntax-check

# ドライラン
ansible-playbook playbook.yml --check

# 特定ホスト
ansible-playbook -i hosts.ini playbook.yml --limit web1.example.com
```

### 変数・テンプレート

```yaml
# playbook.yml
---
- name: Deploy App
  hosts: webservers
  vars:
    app_version: "1.2.3"
    app_port: 8080

  tasks:
    - name: Deploy config
      template:
        src: app.conf.j2
        dest: /etc/app/app.conf
```

```jinja2
# app.conf.j2
server {
    listen {{ app_port }};
    version {{ app_version }};
}
```

### Role

```yaml
# site.yml
---
- name: Setup Infrastructure
  hosts: all
  roles:
    - common
    - webserver
    - database
```

```bash
# Role構造
roles/
  webserver/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
    files/
    vars/
    defaults/
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Ansible** | 🟢 完全無料 | オープンソース、GPLv3 License |
| **Ansible Tower** | 💰 商用ライセンス | WebUI、RBAC、スケジューリング |
| **Red Hat Ansible Automation Platform** | 💰 サブスクリプション | エンタープライズサポート |

## メリット

1. **エージェントレス**: SSH接続のみ
2. **シンプル**: YAML、学習容易
3. **冪等性**: 安全な繰り返し実行
4. **完全無料**: オープンソース
5. **豊富なモジュール**: 3000+

## デメリット

1. **パフォーマンス**: SSH遅延
2. **Windows**: WinRM設定必要
3. **複雑な構成**: 大規模で複雑化
4. **デバッグ**: デバッグ難しい

## 公式リンク

- **公式サイト**: [https://www.ansible.com/](https://www.ansible.com/)
- **ドキュメント**: [https://docs.ansible.com/](https://docs.ansible.com/)

## 関連ドキュメント

- [構成管理ツール一覧](../構成管理ツール/)
- [Terraform](../IaCツール/Terraform.md)
- [Chef](./Chef.md)

---

**カテゴリ**: 構成管理ツール
**対象工程**: インフラ自動化
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
