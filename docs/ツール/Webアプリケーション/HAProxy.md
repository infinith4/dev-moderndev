# HAProxy

## 概要

HAProxyは、高性能TCP/HTTPロードバランサー・プロキシです。Layer 4/7ロードバランシング、SSL/TLSターミネーション、ヘルスチェック、スティッキーセッション、ACL（アクセス制御）により、Webサーバー、APIサーバー、データベースの負荷分散・高可用性を実現します。オープンソース、低レイテンシ、高スループットで広く採用されています。

## 主な機能

### 1. ロードバランシング
- **Layer 4**: TCP（L4）
- **Layer 7**: HTTP（L7）
- **アルゴリズム**: ラウンドロビン、Least Connections
- **重み付け**: サーバー重み

### 2. ヘルスチェック
- **HTTP**: HTTPリクエスト
- **TCP**: TCP接続
- **カスタム**: カスタムチェック
- **自動フェイルオーバー**: 障害検出

### 3. SSL/TLS
- **ターミネーション**: SSL終端
- **パススルー**: SSL透過
- **証明書**: SNI対応
- **HTTPS**: HTTP/2

### 4. セッション維持
- **スティッキーセッション**: Cookie、IP Hash
- **セッションテーブル**: セッション管理

## 利用方法

### インストール（Docker）

```bash
docker run -d --name haproxy \
  -p 80:80 \
  -p 443:443 \
  -p 8404:8404 \
  -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  haproxy:latest

# Stats UI: http://localhost:8404/stats
```

### 基本設定

```cfg
# haproxy.cfg
global
    log stdout format raw local0
    maxconn 4096
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server server1 192.168.1.10:8080 check
    server server2 192.168.1.11:8080 check
    server server3 192.168.1.12:8080 check
```

### HTTPSターミネーション

```cfg
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/server.pem
    default_backend https_back

backend https_back
    balance roundrobin
    option httpchk GET /health
    server server1 192.168.1.10:8080 check
    server server2 192.168.1.11:8080 check
```

### ロードバランシングアルゴリズム

```cfg
backend http_back
    # ラウンドロビン
    balance roundrobin

    # Least Connections
    # balance leastconn

    # Source IP Hash
    # balance source

    # URI Hash
    # balance uri

    server server1 192.168.1.10:8080 check weight 1
    server server2 192.168.1.11:8080 check weight 2
    server server3 192.168.1.12:8080 check backup
```

### ヘルスチェック

```cfg
backend http_back
    balance roundrobin

    # HTTPヘルスチェック
    option httpchk GET /health HTTP/1.1\r\nHost:\ example.com

    server server1 192.168.1.10:8080 check inter 2s rise 2 fall 3
    server server2 192.168.1.11:8080 check inter 2s rise 2 fall 3

    # inter: チェック間隔
    # rise: 正常判定回数
    # fall: 異常判定回数
```

### スティッキーセッション

```cfg
backend http_back
    balance roundrobin

    # Cookieベース
    cookie SERVERID insert indirect nocache

    server server1 192.168.1.10:8080 check cookie s1
    server server2 192.168.1.11:8080 check cookie s2
```

### ACL（アクセス制御）

```cfg
frontend http_front
    bind *:80

    # ACL定義
    acl is_api path_beg /api
    acl is_static path_beg /static

    # バックエンド選択
    use_backend api_back if is_api
    use_backend static_back if is_static
    default_backend web_back

backend api_back
    server api1 192.168.1.20:8080 check

backend static_back
    server static1 192.168.1.30:8080 check

backend web_back
    server web1 192.168.1.10:8080 check
```

### Stats ページ

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats auth admin:password
```

### TCP ロードバランシング

```cfg
frontend mysql_front
    bind *:3306
    mode tcp
    default_backend mysql_back

backend mysql_back
    mode tcp
    balance leastconn
    option tcp-check

    server mysql1 192.168.1.40:3306 check
    server mysql2 192.168.1.41:3306 check backup
```

### Docker Compose

```yaml
version: '3.8'
services:
  haproxy:
    image: haproxy:latest
    ports:
      - "80:80"
      - "443:443"
      - "8404:8404"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./certs:/etc/haproxy/certs:ro

  web1:
    image: nginx:latest
    environment:
      - SERVER_NAME=web1

  web2:
    image: nginx:latest
    environment:
      - SERVER_NAME=web2
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **HAProxy Community** | 🟢 完全無料 | オープンソース、GPLv2 License |
| **HAProxy Enterprise** | 💰 商用ライセンス | サポート、高度機能 |

## メリット

1. **完全無料**: オープンソース
2. **高性能**: 低レイテンシ、高スループット
3. **Layer 4/7**: TCP、HTTP対応
4. **SSL/TLS**: SSL終端
5. **柔軟性**: ACL、ヘルスチェック

## デメリット

1. **設定複雑**: 初期設定学習必要
2. **動的設定**: 再起動必要
3. **GUI**: Web UI限定的
4. **学習曲線**: 高度機能複雑

## 公式リンク

- **公式サイト**: [https://www.haproxy.org/](https://www.haproxy.org/)
- **ドキュメント**: [https://www.haproxy.org/#docs](https://www.haproxy.org/#docs)

## 関連ドキュメント

- [ロードバランサーツール一覧](../ロードバランサーツール/)
- [Nginx](../Webサーバーツール/Nginx.md)
- [Traefik](./Traefik.md)

---

**カテゴリ**: ロードバランサーツール
**対象工程**: 負荷分散・高可用性
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
