# Docker Compose

## 概要

Docker Composeは、複数のDockerコンテナを定義・実行するツールです。docker-compose.yml（YAML）でマルチコンテナアプリケーション（Webアプリ+DB+Redis等）を宣言的に定義し、docker-compose upで一括起動します。開発環境、テスト環境、ローカル開発で広く採用され、Docker公式ツールとして統合されています。

## 主な機能

### 1. マルチコンテナ
- **サービス定義**: Web、DB、キャッシュ等
- **ネットワーク**: コンテナ間通信
- **ボリューム**: データ永続化

### 2. 宣言的設定
- **docker-compose.yml**: YAML設定
- **環境変数**: .env ファイル
- **オーバーライド**: docker-compose.override.yml

### 3. ライフサイクル
- **up**: コンテナ起動
- **down**: コンテナ停止・削除
- **restart**: 再起動
- **logs**: ログ確認

## 利用方法

### インストール

```bash
# Docker Desktop（Compose V2統合）
docker compose version

# 独立インストール（レガシー）
pip install docker-compose
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### コマンド

```bash
# コンテナ起動
docker compose up -d

# コンテナ停止
docker compose down

# ログ確認
docker compose logs -f

# サービス一覧
docker compose ps

# サービス再起動
docker compose restart web

# コンテナ削除（ボリューム含む）
docker compose down -v
```

### 開発環境例

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - redis
      - postgres
  
  redis:
    image: redis:7
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Docker Compose** | 🟢 完全無料 | オープンソース、Apache License |

## メリット

1. **完全無料**: オープンソース
2. **シンプル**: YAML設定
3. **マルチコンテナ**: 一括管理
4. **開発環境**: ローカル開発最適
5. **Docker統合**: Docker公式

## デメリット

1. **本番環境**: 本番向きでない（Kubernetes推奨）
2. **スケール**: スケーリング限定的
3. **クラスタ**: 複数ホスト非対応
4. **オーケストレーション**: Kubernetesより機能少ない

## 公式リンク

- **公式ドキュメント**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **GitHub**: [https://github.com/docker/compose](https://github.com/docker/compose)

## 関連ドキュメント

- [コンテナツール一覧](../コンテナツール/)
- [Docker](./Docker.md)
- [Kubernetes](./Kubernetes.md)

---

**カテゴリ**: コンテナツール  
**対象工程**: 開発、テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
