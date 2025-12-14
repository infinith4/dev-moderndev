# CentOS

## 概要

**CentOS**（Community Enterprise Operating System）は、Red Hat Enterprise Linux（RHEL）のソースコードから派生したLinuxディストリビューションです。無料でエンタープライズグレードのOS環境を提供し、安定性・長期サポートにより、Webサーバー・開発環境で広く採用されています。

**重要**: CentOS Linuxは2021年12月末で開発終了となり、後継として**CentOS Stream**（RHELの上流版）、または**AlmaLinux**、**Rocky Linux**（CentOSクローン）への移行が推奨されています。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | CentOS Project / Red Hat |
| **種別** | Linuxディストリビューション |
| **ライセンス** | GPL（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://www.centos.org/ |
| **ドキュメント** | https://docs.centos.org/ |

## 主な特徴

### 1. RHEL互換性
- **バイナリ互換**: RHELと互換性のあるパッケージ
- **YUM/DNF**: RHELと同じパッケージ管理
- **SELinux**: エンタープライズセキュリティ
- **長期サポート**: 10年のメンテナンス期間

### 2. 安定性・信頼性
- **保守的リリース**: 枯れた技術の採用
- **徹底テスト**: 本番環境向けの品質保証
- **バックポート**: セキュリティパッチの提供
- **エンタープライズ向け**: 大規模システムでの実績

### 3. 豊富なエコシステム
- **EPEL**: Extra Packages for Enterprise Linux
- **RPMFusion**: マルチメディア・プロプライエタリパッケージ
- **Software Collections**: 新しいバージョンのツール
- **Docker公式対応**: コンテナベースイメージ

### 4. パッケージ管理
- **YUM/DNF**: RPMベースパッケージマネージャー
- **リポジトリ**: 公式・サードパーティリポジトリ
- **自動更新**: yum-cron、dnf-automatic
- **ロールバック**: 依存関係管理

## 使い方

### インストール

```bash
# ISOダウンロード（過去バージョン）
# https://vault.centos.org/

# CentOS 7（最終サポート: 2024-06-30）
# CentOS 8（サポート終了: 2021-12-31）

# 代替OS推奨:
# - CentOS Stream: https://www.centos.org/centos-stream/
# - AlmaLinux: https://almalinux.org/
# - Rocky Linux: https://rockylinux.org/
```

### 基本操作

```bash
# システム情報確認
cat /etc/centos-release
uname -a
hostnamectl

# パッケージ管理（YUM - CentOS 7）
sudo yum update               # 全パッケージ更新
sudo yum install package_name # パッケージインストール
sudo yum remove package_name  # パッケージ削除
sudo yum search keyword       # パッケージ検索
sudo yum info package_name    # パッケージ情報

# パッケージ管理（DNF - CentOS 8+）
sudo dnf update
sudo dnf install package_name
sudo dnf remove package_name
sudo dnf search keyword
sudo dnf info package_name

# インストール済みパッケージ確認
yum list installed
rpm -qa

# リポジトリ確認
yum repolist
```

### EPEL有効化

```bash
# EPEL（Extra Packages for Enterprise Linux）リポジトリ追加
# CentOS 7
sudo yum install epel-release

# CentOS 8
sudo dnf install epel-release

# EPELから追加パッケージインストール
sudo yum install htop
sudo yum install nginx
```

### 開発環境セットアップ

```bash
# 開発ツールインストール
sudo yum groupinstall "Development Tools"

# または個別インストール
sudo yum install gcc gcc-c++ make cmake git

# Python開発環境
sudo yum install python3 python3-devel python3-pip

# Node.js（NodeSource リポジトリ）
curl -sL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install nodejs

# Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
```

### Webサーバーセットアップ（Apache）

```bash
# Apache（httpd）インストール
sudo yum install httpd

# 起動・自動起動設定
sudo systemctl start httpd
sudo systemctl enable httpd

# ファイアウォール設定
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# SELinuxコンテキスト設定
sudo chcon -R -t httpd_sys_content_t /var/www/html/

# 設定ファイル
sudo vi /etc/httpd/conf/httpd.conf

# 再起動
sudo systemctl restart httpd
```

### Webサーバーセットアップ（Nginx）

```bash
# Nginxインストール（EPELリポジトリ）
sudo yum install epel-release
sudo yum install nginx

# 起動・自動起動設定
sudo systemctl start nginx
sudo systemctl enable nginx

# ファイアウォール設定
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 設定ファイル
sudo vi /etc/nginx/nginx.conf

# 再起動
sudo systemctl restart nginx
```

### データベースセットアップ（MySQL/MariaDB）

```bash
# MariaDBインストール（MySQL互換）
sudo yum install mariadb-server mariadb

# 起動・自動起動設定
sudo systemctl start mariadb
sudo systemctl enable mariadb

# 初期セキュリティ設定
sudo mysql_secure_installation

# MySQLログイン
mysql -u root -p

# ユーザー・データベース作成
CREATE DATABASE myapp;
CREATE USER 'myapp_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON myapp.* TO 'myapp_user'@'localhost';
FLUSH PRIVILEGES;
```

### ファイアウォール（firewalld）

```bash
# ファイアウォール状態確認
sudo systemctl status firewalld

# サービス許可
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh

# ポート許可
sudo firewall-cmd --permanent --add-port=8080/tcp

# リロード
sudo firewall-cmd --reload

# ルール確認
sudo firewall-cmd --list-all
```

### SELinuxの管理

```bash
# SELinux状態確認
getenforce
sestatus

# SELinuxモード変更（一時的）
sudo setenforce 0  # Permissive（警告のみ）
sudo setenforce 1  # Enforcing（強制）

# SELinuxモード変更（永続的）
sudo vi /etc/selinux/config
# SELINUX=enforcing → SELINUX=permissive または disabled

# SELinuxコンテキスト確認
ls -Z /var/www/html/

# SELinuxコンテキスト設定
sudo chcon -R -t httpd_sys_content_t /var/www/html/
sudo restorecon -R /var/www/html/

# SELinuxブール値設定
sudo setsebool -P httpd_can_network_connect on
```

### システムモニタリング

```bash
# システムリソース確認
top
htop  # EPELからインストール必要

# ディスク使用量
df -h
du -sh /var/log/*

# メモリ使用量
free -h

# プロセス確認
ps aux
ps -ef

# サービス状態確認
sudo systemctl status httpd
sudo systemctl status nginx
sudo systemctl status mariadb

# ログ確認
sudo journalctl -u httpd
sudo tail -f /var/log/httpd/access_log
sudo tail -f /var/log/httpd/error_log
```

### 自動更新設定

```bash
# yum-cron インストール（CentOS 7）
sudo yum install yum-cron

# 設定編集
sudo vi /etc/yum/yum-cron.conf
# apply_updates = yes に変更

# 起動・自動起動設定
sudo systemctl start yum-cron
sudo systemctl enable yum-cron

# dnf-automatic インストール（CentOS 8+）
sudo dnf install dnf-automatic

# 設定編集
sudo vi /etc/dnf/automatic.conf
# apply_updates = yes に変更

# 起動・自動起動設定
sudo systemctl enable --now dnf-automatic.timer
```

### Dockerコンテナ

```dockerfile
# Dockerfile（CentOS 7ベース）
FROM centos:7

RUN yum update -y && \
    yum install -y httpd && \
    yum clean all

COPY index.html /var/www/html/

EXPOSE 80

CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
```

```bash
# ビルド・実行
docker build -t myapp-centos .
docker run -d -p 8080:80 myapp-centos
```

### 移行ガイド

#### CentOS → AlmaLinux

```bash
# AlmaLinux移行ツール使用
curl -O https://raw.githubusercontent.com/AlmaLinux/almalinux-deploy/master/almalinux-deploy.sh
sudo bash almalinux-deploy.sh

# 再起動
sudo reboot

# 確認
cat /etc/os-release
```

#### CentOS → Rocky Linux

```bash
# Rocky Linux移行ツール使用
curl -O https://raw.githubusercontent.com/rocky-linux/rocky-tools/main/migrate2rocky/migrate2rocky.sh
sudo bash migrate2rocky.sh -r

# 再起動
sudo reboot

# 確認
cat /etc/os-release
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **環境構築** | 開発環境 | 開発サーバー、テスト環境 |
| **実装** | アプリケーションサーバー | Web・API・バッチサーバー |
| **テスト** | CI/CDランナー | Jenkins、GitLab Runner |
| **導入** | 本番環境 | Webサーバー、DBサーバー |

## メリット

- **無料**: オープンソース、商用利用可能
- **RHEL互換**: エンタープライズグレード
- **安定性**: 長期サポート、枯れた技術
- **豊富なドキュメント**: コミュニティ・企業サポート
- **セキュリティ**: SELinux、定期パッチ
- **パッケージ管理**: YUM/DNF、EPEL
- **実績**: 大規模システムでの採用実績

## デメリット

- **開発終了**: CentOS Linuxは2021年終了
- **古いパッケージ**: 最新版は入手困難
- **移行コスト**: 代替OSへの移行必要
- **学習曲線**: Red Hat系特有の設定
- **SELinux複雑**: 設定・トラブルシューティング
- **デスクトップ非推奨**: サーバー用途向け

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **CentOS Linux** | RHEL互換（開発終了） | 無料 | レガシーシステム |
| **AlmaLinux** | CentOSクローン、活発開発 | 無料 | CentOS後継 |
| **Rocky Linux** | CentOSクローン、活発開発 | 無料 | CentOS後継 |
| **Ubuntu Server** | Debian系、最新パッケージ | 無料 | モダン開発 |

## ベストプラクティス

### 1. セキュリティ更新

```bash
# 定期的なパッケージ更新
sudo yum update -y

# セキュリティパッチのみ適用
sudo yum update --security
```

### 2. ファイアウォール設定

```bash
# 最小限のポート開放
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 3. SELinuxは無効化しない

```bash
# Permissiveモードで動作確認後、Enforcingに戻す
# 無効化（disabled）は非推奨
```

### 4. バックアップ戦略

```bash
# rsync でバックアップ
sudo rsync -avz /var/www/html/ /backup/html/

# tar.gz 圧縮バックアップ
sudo tar -czf /backup/var-www-$(date +%Y%m%d).tar.gz /var/www/
```

## 公式リソース

- **公式サイト**: https://www.centos.org/
- **ドキュメント**: https://docs.centos.org/
- **CentOS Stream**: https://www.centos.org/centos-stream/
- **AlmaLinux**: https://almalinux.org/
- **Rocky Linux**: https://rockylinux.org/
- **EPEL**: https://fedoraproject.org/wiki/EPEL

## まとめ

CentOSは、RHELのソースから派生した無料のLinuxディストリビューションです。エンタープライズグレードの安定性・長期サポートにより、Webサーバー・開発環境で広く採用されていましたが、2021年に開発終了となりました。既存システムはAlmaLinux、Rocky Linux等の代替OSへの移行が推奨されています。

---

**最終更新**: 2025-12-10
**CentOS Linuxサポート**: 終了（2021年12月）
**推奨代替OS**: AlmaLinux、Rocky Linux、CentOS Stream
