# Apache HTTP Server

## 概要

Apache HTTP Serverは、オープンソースのWebサーバーです。モジュールアーキテクチャ、バーチャルホスト、.htaccess、CGI/FastCGI、リバースプロキシにより、静的コンテンツ配信、PHPアプリケーション、SSLターミネーションを実現します。Apache Software Foundation開発、LAMPスタック、長年の実績で広く採用されています。

## 主な機能

### 1. Webサーバー
- **静的コンテンツ**: HTML、CSS、JS配信
- **動的コンテンツ**: PHP、CGI
- **HTTPS**: SSL/TLS
- **HTTP/2**: HTTP/2対応

### 2. モジュール
- **mod_rewrite**: URLリライト
- **mod_proxy**: リバースプロキシ
- **mod_ssl**: SSL/TLS
- **mod_php**: PHPモジュール

### 3. バーチャルホスト
- **名前ベース**: ドメイン別
- **IPベース**: IP別
- **ポートベース**: ポート別

### 4. アクセス制御
- **.htaccess**: ディレクトリ設定
- **認証**: Basic、Digest認証
- **IP制限**: アクセス制限

## 利用方法

### インストール（Docker）

```bash
docker run -d --name apache \
  -p 80:80 \
  -p 443:443 \
  -v $(pwd)/htdocs:/usr/local/apache2/htdocs \
  -v $(pwd)/httpd.conf:/usr/local/apache2/conf/httpd.conf \
  httpd:2.4
```

### 基本設定

```apache
# httpd.conf
ServerRoot "/usr/local/apache2"
Listen 80

LoadModule rewrite_module modules/mod_rewrite.so
LoadModule ssl_module modules/mod_ssl.so
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so

DocumentRoot "/usr/local/apache2/htdocs"

<Directory "/usr/local/apache2/htdocs">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

ErrorLog logs/error.log
CustomLog logs/access.log combined
```

### バーチャルホスト

```apache
# httpd-vhosts.conf
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot "/var/www/example"

    <Directory "/var/www/example">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog logs/example-error.log
    CustomLog logs/example-access.log combined
</VirtualHost>

<VirtualHost *:80>
    ServerName test.example.com
    DocumentRoot "/var/www/test"

    <Directory "/var/www/test">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

### SSL/TLS設定

```apache
Listen 443

<VirtualHost *:443>
    ServerName example.com
    DocumentRoot "/var/www/example"

    SSLEngine on
    SSLCertificateFile "/etc/ssl/certs/server.crt"
    SSLCertificateKeyFile "/etc/ssl/private/server.key"
    SSLCertificateChainFile "/etc/ssl/certs/chain.crt"

    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite HIGH:!aNULL:!MD5

    <Directory "/var/www/example">
        Require all granted
    </Directory>
</VirtualHost>

# HTTP→HTTPSリダイレクト
<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>
```

### リバースプロキシ

```apache
<VirtualHost *:80>
    ServerName api.example.com

    ProxyPreserveHost On
    ProxyPass / http://backend:8080/
    ProxyPassReverse / http://backend:8080/

    <Proxy *>
        Require all granted
    </Proxy>
</VirtualHost>
```

### .htaccess（URLリライト）

```apache
# .htaccess
RewriteEngine On

# HTTPSリダイレクト
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

# SPAルーティング
RewriteBase /
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

# 静的ファイル圧縮
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>
```

### Basic認証

```apache
# httpd.conf
<Directory "/var/www/admin">
    AuthType Basic
    AuthName "Admin Area"
    AuthUserFile /etc/apache2/.htpasswd
    Require valid-user
</Directory>
```

```bash
# パスワードファイル作成
htpasswd -c /etc/apache2/.htpasswd admin
```

### PHPサポート

```apache
LoadModule php_module modules/libphp.so

<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

DirectoryIndex index.php index.html
```

### ロードバランシング

```apache
<Proxy balancer://mycluster>
    BalancerMember http://backend1:8080
    BalancerMember http://backend2:8080
    BalancerMember http://backend3:8080
    ProxySet lbmethod=byrequests
</Proxy>

<VirtualHost *:80>
    ServerName example.com
    ProxyPass / balancer://mycluster/
    ProxyPassReverse / balancer://mycluster/
</VirtualHost>
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Apache HTTP Server** | 🟢 無料 | オープンソース、Apache License |

## メリット

1. **無料**: オープンソース
2. **成熟**: 長年の実績
3. **柔軟性**: モジュール豊富
4. **LAMPスタック**: PHP標準
5. **.htaccess**: ディレクトリ設定

## デメリット

1. **パフォーマンス**: Nginxより遅い
2. **メモリ**: メモリ消費大
3. **設定複雑**: 初期設定複雑
4. **プロセスモデル**: スレッド/プロセス

## 公式リンク

- **公式サイト**: [https://httpd.apache.org/](https://httpd.apache.org/)
- **ドキュメント**: [https://httpd.apache.org/docs/](https://httpd.apache.org/docs/)

## 関連ドキュメント

- [Webサーバーツール一覧](../Webサーバーツール/)
- [Nginx](./Nginx.md)
- [Apache Tomcat](../アプリケーションサーバーツール/Apache_Tomcat.md)

---

**カテゴリ**: Webサーバーツール
**対象工程**: Webサーバー
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
