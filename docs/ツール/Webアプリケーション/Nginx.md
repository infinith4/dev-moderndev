# Nginx

## 概要

Nginxは、高性能なWebサーバー・リバースプロキシです。イベント駆動アーキテクチャ、ロードバランシング、静的コンテンツ配信、HTTPSターミネーション、リバースプロキシにより、高並行処理・低リソース消費を実現します。オープンソース、軽量、API Gateway、Kubernetes Ingressで広く採用されています。

## 主な機能

### 1. Webサーバー
- **静的コンテンツ**: HTML、CSS、JS配信
- **gzip圧縮**: 転送圧縮
- **HTTP/2**: HTTP/2対応
- **HTTPS**: TLS/SSL

### 2. リバースプロキシ
- **プロキシ**: バックエンド転送
- **ロードバランシング**: ラウンドロビン、IP Hash
- **キャッシング**: レスポンスキャッシュ
- **ヘッダー操作**: カスタムヘッダー

### 3. ロードバランサー
- **アルゴリズム**: ラウンドロビン、Least Connections
- **ヘルスチェック**: バックエンド監視
- **セッション維持**: IP Hash

### 4. その他
- **WebSocket**: WebSocketプロキシ
- **FastCGI**: PHP-FPM統合
- **Lua**: Lua スクリプト（OpenResty）

## 利用方法

### インストール（Docker）

```bash
docker run -d --name nginx \
  -p 80:80 \
  -p 443:443 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:latest
```

### 基本設定

```nginx
# nginx.conf
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include mime.types;
    default_type application/octet-stream;

    sendfile on;
    keepalive_timeout 65;

    server {
        listen 80;
        server_name example.com;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
```

### リバースプロキシ

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### ロードバランシング

```nginx
upstream backend {
    least_conn;  # Least Connections

    server backend1:8080 weight=3;
    server backend2:8080 weight=2;
    server backend3:8080 backup;
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
    }
}
```

### HTTPS設定

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
}

# HTTP→HTTPSリダイレクト
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### キャッシング

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    listen 80;

    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_use_stale error timeout updating;

        proxy_pass http://backend;
    }
}
```

### Kubernetes Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Nginx OSS** | 🟢 無料 | オープンソース、BSD License |
| **Nginx Plus** | 💰 $2,500/年〜 | 動的設定、高度ヘルスチェック |

## メリット

1. **無料**: オープンソース
2. **高性能**: 高並行処理
3. **軽量**: 低リソース消費
4. **汎用性**: Webサーバー、プロキシ、LB
5. **HTTP/2**: 最新プロトコル

## デメリット

1. **設定複雑**: 初期設定学習必要
2. **動的設定**: OSS版は再起動必要
3. **Windows**: Windows対応限定的
4. **デバッグ**: エラーデバッグ難しい

## 公式リンク

- **公式サイト**: [https://nginx.org/](https://nginx.org/)
- **ドキュメント**: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)

## 関連ドキュメント

- [Webサーバーツール一覧](../Webサーバーツール/)
- [Apache HTTP Server](./Apache_HTTP_Server.md)
- [HAProxy](../ロードバランサーツール/HAProxy.md)

---

**カテゴリ**: Webサーバーツール
**対象工程**: Webサーバー・リバースプロキシ
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
