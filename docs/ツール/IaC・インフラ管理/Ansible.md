# Ansible

## 概要

Ansibleは、Red Hat社が提供するオープンソースの構成管理・自動化ツールです。エージェントレスアーキテクチャにより、SSHベースでサーバーの構成管理、アプリケーションデプロイ、タスク自動化を実現します。YAML形式のPlaybookで人間が読みやすい設定を記述し、冪等性を保証することで、インフラストラクチャの一貫性と再現性を確保します。

## 主な機能

### 1. 構成管理
- サーバー設定の自動化
- パッケージインストール
- ファイル配布・編集
- サービス起動・停止

### 2. アプリケーションデプロイ
- コードデプロイ
- 依存関係インストール
- 設定ファイル配布
- ローリングアップデート

### 3. オーケストレーション
- 複数サーバーの連携
- 順序制御（シーケンシャル/並列）
- 条件分岐・ループ
- エラーハンドリング

### 4. プロビジョニング
- クラウドインスタンス作成
- ネットワーク設定
- セキュリティグループ設定

### 5. エージェントレス
- SSH接続のみ（エージェント不要）
- WinRM（Windows対応）
- 軽量・セットアップ簡単

### 6. 冪等性
- 何度実行しても同じ結果
- 安全な再実行
- 変更がある場合のみ適用

## 利用方法

### インストール

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible

# RHEL/CentOS
sudo yum install ansible

# macOS
brew install ansible

# Python pip
pip install ansible
```

### インベントリファイル作成

```ini
# inventory/hosts
[webservers]
web1.example.com
web2.example.com
web3.example.com

[dbservers]
db1.example.com
db2.example.com

[webservers:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### Playbook作成例（Webサーバーセットアップ）

```yaml
# playbook.yml
---
- name: Webサーバーセットアップ
  hosts: webservers
  become: yes
  
  vars:
    nginx_port: 80
    app_name: myapp
  
  tasks:
    - name: Nginxインストール
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Nginx設定ファイル配布
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
      notify: Nginxリロード
    
    - name: シンボリックリンク作成
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
    
    - name: アプリケーションディレクトリ作成
      file:
        path: /var/www/{{ app_name }}
        state: directory
        owner: www-data
        group: www-data
    
    - name: Nginx起動・有効化
      systemd:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: Nginxリロード
      systemd:
        name: nginx
        state: reloaded
```

### Playbook実行

```bash
# Playbookチェック（dry-run）
ansible-playbook -i inventory/hosts playbook.yml --check

# Playbook実行
ansible-playbook -i inventory/hosts playbook.yml

# 特定のタグのみ実行
ansible-playbook -i inventory/hosts playbook.yml --tags "nginx"

# verboseモード
ansible-playbook -i inventory/hosts playbook.yml -v
```

### Ad-hocコマンド

```bash
# パッケージ更新
ansible webservers -i inventory/hosts -m apt -a "update_cache=yes" -b

# サービス再起動
ansible webservers -i inventory/hosts -m systemd -a "name=nginx state=restarted" -b

# ファイルコピー
ansible webservers -i inventory/hosts -m copy -a "src=app.conf dest=/etc/app.conf"

# コマンド実行
ansible webservers -i inventory/hosts -m command -a "uptime"
```

### Role構造（ベストプラクティス）

```
roles/
  webserver/
    tasks/
      main.yml         # メインタスク
    handlers/
      main.yml         # ハンドラー
    templates/
      nginx.conf.j2    # Jinjaテンプレート
    files/
      index.html       # 静的ファイル
    vars/
      main.yml         # 変数
    defaults/
      main.yml         # デフォルト変数
    meta/
      main.yml         # メタ情報・依存関係
```

### Ansible Vault（機密情報管理）

```bash
# Vaultファイル作成
ansible-vault create secrets.yml

# Vaultファイル編集
ansible-vault edit secrets.yml

# Playbook実行時にVaultパスワード指定
ansible-playbook -i inventory/hosts playbook.yml --ask-vault-pass

# パスワードファイル使用
ansible-playbook -i inventory/hosts playbook.yml --vault-password-file ~/.vault_pass
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Ansible（Community）** | 🟢 完全無料 | オープンソース、CLI |
| **Ansible Automation Platform** | 💰 要問い合わせ | Red Hat商用版、GUI（Automation Controller）、サポート |
| **AWX** | 🟢 完全無料 | Automation Platformのオープンソース版 |

## メリット

### ✅ 主な利点

1. **エージェントレス**: SSHのみ、エージェント不要
2. **YAMLベース**: 人間が読みやすい
3. **冪等性**: 何度実行しても同じ結果
4. **豊富なモジュール**: 3,000以上の組み込みモジュール
5. **マルチプラットフォーム**: Linux、Windows、Mac、クラウド
6. **学習曲線緩やか**: シンプルな構文
7. **無料**: Communityエディション完全無料
8. **Red Hatサポート**: 商用版は24/7サポート
9. **Ansible Galaxy**: コミュニティRole共有
10. **CI/CD統合**: Jenkins、GitLab CI等と統合

## デメリット

### ❌ 制約・課題

1. **SSH接続必須**: ネットワーク接続が前提
2. **パフォーマンス**: 大規模環境ではPuppet/Chefより遅い
3. **状態管理弱い**: Terraformのような状態ファイルなし
4. **Windows対応**: WinRM設定が必要、Linux比で機能劣る
5. **デバッグ困難**: エラーメッセージが不明瞭な場合あり
6. **バージョン管理**: Playbookのバージョン管理はGitに依存
7. **複雑なロジック**: 複雑な条件分岐は記述が煩雑
8. **スケーラビリティ**: 数千台規模ではツール選定検討必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Terraform** | IaC、クラウドプロビジョニング | Ansibleは構成管理、Terraformはプロビジョニング |
| **Chef** | Ruby、エージェントベース | Ansibleよりパフォーマンス高いがエージェント必要 |
| **Puppet** | Ruby、エージェントベース | Ansibleより大規模向け |
| **SaltStack** | Python、エージェント/エージェントレス | Ansibleより高速 |
| **PowerShell DSC** | Windows専用 | Ansibleより Windows対応強い |

## 公式リンク

- **公式サイト**: [https://www.ansible.com/](https://www.ansible.com/)
- **ドキュメント**: [https://docs.ansible.com/](https://docs.ansible.com/)
- **Ansible Galaxy**: [https://galaxy.ansible.com/](https://galaxy.ansible.com/)
- **GitHub**: [https://github.com/ansible/ansible](https://github.com/ansible/ansible)
- **Red Hat Ansible Automation Platform**: [https://www.redhat.com/en/technologies/management/ansible](https://www.redhat.com/en/technologies/management/ansible)

## 関連ドキュメント

- [IaCツール一覧](../IaCツール/)
- [Terraform](./Terraform.md)
- [Chef](./Chef.md)
- [構成管理ベストプラクティス](../../best-practices/configuration-management.md)
- [Ansible Playbook作成ガイド](../../best-practices/ansible-playbook.md)

---

**カテゴリ**: IaCツール  
**対象工程**: インフラ構築、デプロイ、運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
