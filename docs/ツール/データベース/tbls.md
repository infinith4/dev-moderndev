# tbls

## 概要

**tbls**（テーブルス）は、既存のデータベーススキーマから自動的にドキュメント・ER図を生成するオープンソースのCLIツールです。実際のデータベース構造を解析し、Markdown形式のドキュメント、PNG/SVG形式のER図、PlantUML/Mermaid形式の図を自動生成します。リバースエンジニアリングにより、コードとドキュメントの乖離を防ぎ、データベース設計書のメンテナンスを自動化します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | [https://github.com/k1LoW/tbls](https://github.com/k1LoW/tbls) |
| **GitHub** | [https://github.com/k1LoW/tbls](https://github.com/k1LoW/tbls) |
| **開発言語** | Go |
| **ライセンス** | MIT License |
| **開発者** | k1LoW (日本) |
| **対応DB** | PostgreSQL / MySQL / MariaDB / SQLite / BigQuery / Redshift / Snowflake / MongoDB / DynamoDB 等 |
| **料金** | 🟢 無料・オープンソース |

## 主な機能

### 1. データベーススキーマドキュメント自動生成
- データベース接続してスキーマ解析
- Markdown形式ドキュメント自動生成
- テーブル定義・カラム定義・インデックス・制約を抽出
- テーブル間のリレーション自動検出

### 2. ER図自動生成
- PNG/SVG形式のER図生成
- PlantUML形式出力
- Mermaid形式出力
- DOT形式（Graphviz）出力

### 3. 多様なデータベース対応
- **RDBMS**: PostgreSQL, MySQL, MariaDB, SQLite, SQL Server
- **クラウドDB**: BigQuery, Redshift, Snowflake, Spanner
- **NoSQL**: MongoDB, DynamoDB
- **データウェアハウス**: BigQuery, Redshift, Snowflake

### 4. CI/CD統合
- スキーマ差分検出
- ドキュメント更新自動化
- GitHub Actions統合
- Git管理されたドキュメント

### 5. カスタマイズ可能
- 設定ファイル（.tbls.yml）
- テーブル・カラムコメント追加
- ドキュメントテンプレートカスタマイズ
- 除外テーブル指定

## メリット・デメリット

### メリット ✅

- **無料・オープンソース** - ライセンス費用不要
- **リバースエンジニアリング** - 既存DBから自動生成
- **多様なDB対応** - 主要DBほぼすべて対応
- **ER図自動生成** - PNG/SVG/PlantUML/Mermaid出力
- **CI/CD統合容易** - 自動ドキュメント更新
- **軽量・高速** - Go製でパフォーマンス優秀
- **日本製** - 日本人開発者によるツール

### デメリット ❌

- **CLIツール** - GUI非対応（コマンドライン操作必須）
- **リバースエンジニアリング専用** - DB設計ツールではない
- **インタラクティブ編集不可** - ER図をGUIで編集できない
- **学習コスト** - CLI操作・設定ファイル理解必要

## インストール・セットアップ

### Homebrewでインストール（macOS/Linux）

```bash
# Homebrew
brew install k1LoW/tap/tbls
```

### バイナリダウンロード

```bash
# GitHub Releasesから最新版ダウンロード
# https://github.com/k1LoW/tbls/releases

# Linux (amd64)
curl -L https://github.com/k1LoW/tbls/releases/latest/download/tbls_linux_amd64.tar.gz | tar xz
sudo mv tbls /usr/local/bin/

# macOS (arm64)
curl -L https://github.com/k1LoW/tbls/releases/latest/download/tbls_darwin_arm64.zip -o tbls.zip
unzip tbls.zip
sudo mv tbls /usr/local/bin/
```

### Goでインストール

```bash
go install github.com/k1LoW/tbls@latest
```

### Dockerで使用

```bash
docker pull ghcr.io/k1low/tbls:latest
```

## 基本的な使用方法

### データベーススキーマドキュメント生成

```bash
# PostgreSQL
tbls doc postgres://user:password@localhost:5432/dbname dbdoc/

# MySQL
tbls doc mysql://user:password@localhost:3306/dbname dbdoc/

# SQLite
tbls doc sqlite:///path/to/database.db dbdoc/

# BigQuery
tbls doc bigquery://project-id/dataset-name dbdoc/
```

実行すると、`dbdoc/` ディレクトリに以下が生成されます:
- `README.md` - データベース全体概要
- `schema.md` - スキーマ詳細
- `テーブル名.md` - 各テーブル詳細
- `schema.svg` - ER図（SVG形式）

### ER図のみ生成

```bash
# PNG形式
tbls out -t png postgres://user:password@localhost:5432/dbname > schema.png

# SVG形式
tbls out -t svg postgres://user:password@localhost:5432/dbname > schema.svg

# PlantUML形式
tbls out -t plantuml postgres://user:password@localhost:5432/dbname > schema.puml

# Mermaid形式
tbls out -t mermaid postgres://user:password@localhost:5432/dbname > schema.mmd

# DOT形式（Graphviz）
tbls out -t dot postgres://user:password@localhost:5432/dbname > schema.dot
```

### 設定ファイル使用

```yaml
# .tbls.yml
# データソース定義
dsn: postgres://user:password@localhost:5432/dbname

# ドキュメント出力先
docPath: dbdoc

# コメント追加
comments:
  - table: users
    tableComment: ユーザー情報を管理するテーブル
    columnComments:
      id: ユーザーID（主キー）
      name: ユーザー名
      email: メールアドレス（ユニーク）
      created_at: 作成日時

# 除外テーブル
exclude:
  - schema_migrations
  - ar_internal_metadata

# ER図設定
er:
  format: svg
  distance: 1  # 関連テーブルの距離（1=直接関連のみ）
```

```bash
# 設定ファイルを使用
tbls doc
```

## 実践例

### PostgreSQLスキーマドキュメント生成

```bash
# 1. データベース接続設定
export DATABASE_URL="postgres://postgres:password@localhost:5432/myapp_production"

# 2. ドキュメント生成
tbls doc $DATABASE_URL docs/db/

# 3. 生成されたファイル確認
ls -la docs/db/
# README.md
# schema.md
# users.md
# posts.md
# comments.md
# schema.svg
```

### 設定ファイル例（.tbls.yml）

```yaml
# データソース
dsn: postgres://postgres:password@localhost:5432/myapp_production

# ドキュメント出力先
docPath: docs/db

# ER図フォーマット
er:
  format: svg
  distance: 2
  showColumnTypes: true

# 除外テーブル
exclude:
  - schema_migrations
  - ar_internal_metadata
  - spatial_ref_sys

# テーブル・カラムコメント
comments:
  - table: users
    tableComment: ユーザーアカウント管理テーブル
    columnComments:
      id: ユーザーID（UUID）
      email: メールアドレス（ログインID）
      encrypted_password: 暗号化パスワード（bcrypt）
      created_at: アカウント作成日時
      updated_at: 最終更新日時

  - table: posts
    tableComment: 投稿記事管理テーブル
    columnComments:
      id: 投稿ID
      user_id: 投稿者ID（users.idへの外部キー）
      title: 投稿タイトル
      body: 投稿本文（Markdown形式）
      published: 公開フラグ
      published_at: 公開日時
```

### GitHub Actionsで自動更新

```yaml
# .github/workflows/update-db-docs.yml
name: Update Database Documentation

on:
  push:
    branches:
      - main
    paths:
      - 'db/migrate/**'
  workflow_dispatch:

jobs:
  update-docs:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Database
        run: |
          PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE DATABASE myapp_test;"
          # マイグレーション実行（例: Rails）
          bundle install
          bundle exec rails db:migrate RAILS_ENV=test

      - name: Install tbls
        run: |
          curl -L https://github.com/k1LoW/tbls/releases/latest/download/tbls_linux_amd64.tar.gz | tar xz
          sudo mv tbls /usr/local/bin/

      - name: Generate Database Documentation
        run: |
          tbls doc postgres://postgres:postgres@localhost:5432/myapp_test docs/db/

      - name: Commit and Push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add docs/db/
          git diff --quiet && git diff --staged --quiet || \
            (git commit -m "Update database documentation [skip ci]" && git push)
```

### スキーマ差分検出

```bash
# 現在のDBスキーマとドキュメントの差分を検出
tbls diff postgres://user:password@localhost:5432/dbname docs/db/

# 差分があれば exit 1 が返される（CI/CDで利用可能）
```

### Docker Composeで使用

```yaml
# docker-compose.yml
services:
  tbls:
    image: ghcr.io/k1low/tbls:latest
    volumes:
      - .:/work
    working_dir: /work
    command: doc postgres://postgres:password@db:5432/myapp docs/db/
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
```

```bash
docker-compose run --rm tbls
```

## ER図出力フォーマット比較

| フォーマット | 用途 | メリット | デメリット |
|------------|------|---------|-----------|
| **PNG** | 画像埋め込み、プレゼン | 互換性高い | 編集不可、拡大でボケる |
| **SVG** | Web表示、高品質 | ベクター、拡大しても鮮明 | ブラウザ依存 |
| **PlantUML** | コードベースER図 | テキストで管理、差分確認容易 | レンダリング必要 |
| **Mermaid** | Markdown埋め込み | GitHub/GitLab対応 | レンダリング必要 |
| **DOT** | Graphviz連携 | カスタマイズ柔軟 | Graphviz必要 |

## CI/CD統合パターン

### パターン1: マイグレーション後に自動更新

```yaml
# マイグレーション実行 → tbls doc → コミット
on:
  push:
    paths:
      - 'db/migrate/**'
```

### パターン2: Pull Requestで差分チェック

```yaml
# tbls diff で差分検出 → コメント投稿
on:
  pull_request:
    paths:
      - 'db/migrate/**'
```

### パターン3: 定期的にドキュメント更新

```yaml
# スケジュール実行（毎日午前0時）
on:
  schedule:
    - cron: '0 0 * * *'
```

## 関連ツール・連携

| ツール | 用途 | 連携方法 |
|--------|------|---------|
| **PlantUML** | ER図レンダリング | PlantUML形式出力 |
| **Mermaid** | Markdown埋め込みER図 | Mermaid形式出力 |
| **GitHub Actions** | CI/CD自動化 | ワークフロー統合 |
| **Flyway** | DBマイグレーション | マイグレーション後にドキュメント生成 |
| **Liquibase** | DBマイグレーション | マイグレーション後にドキュメント生成 |
| **Graphviz** | DOT形式レンダリング | DOT形式出力 |

## 他ツールとの比較

| 機能 | tbls | SchemaSpy | ERDPlus | MySQL Workbench | dbdocs.io |
|------|------|-----------|---------|-----------------|-----------|
| リバースエンジニアリング | ✅ | ✅ | ❌ | ✅ | ✅ |
| ER図自動生成 | ✅ | ✅ | ⚠️ 手動 | ✅ | ✅ |
| Markdown出力 | ✅ | ❌ | ❌ | ❌ | ✅ |
| CLI対応 | ✅ | ✅ | ❌ | ⚠️ 限定的 | ✅ |
| CI/CD統合 | ✅ 優秀 | ⚠️ 可能 | ❌ | ❌ | ✅ |
| GUI | ❌ | ✅ HTML | ✅ | ✅ | ✅ Web |
| 無料 | ✅ | ✅ | ✅ | ⚠️ 一部 | ⚠️ 制限あり |

## 推奨用途

### 最適なケース

- 既存データベースのドキュメント化
- CI/CDでのスキーマドキュメント自動更新
- Git管理されたデータベース設計書
- リバースエンジニアリング
- マイグレーション後のドキュメント自動生成
- 複数データベースの統一ドキュメント

### 不向きなケース

- 新規データベース設計（フォワードエンジニアリング）
- GUIでのER図編集が必要
- インタラクティブな設計作業
- ビジュアル重視のプレゼンテーション

## ベストプラクティス

### 設定ファイルの管理

```bash
# プロジェクトルートに .tbls.yml を配置
# Git管理に含める
git add .tbls.yml
```

### コメントの充実

```yaml
# .tbls.yml
comments:
  - table: users
    tableComment: |
      ユーザーアカウント管理テーブル

      アプリケーションにログインするユーザーの情報を管理します。
      認証はdevise gemを使用しています。
    columnComments:
      id: ユーザーID（UUID、主キー）
      email: メールアドレス（ログインID、ユニーク制約）
```

### 環境変数でDB接続情報管理

```bash
# .env
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# .tbls.yml
dsn: ${DATABASE_URL}
```

### マイグレーションフックに組み込み

```ruby
# Rails: db/migrate/20250101000000_update_db_docs.rb
class UpdateDbDocs < ActiveRecord::Migration[7.0]
  def up
    system('tbls doc')
  end
end
```

## トラブルシューティング

### よくある問題

**問題**: データベース接続エラー

```bash
# 解決方法: 接続文字列確認
tbls doc --debug postgres://user:password@localhost:5432/dbname docs/
```

**問題**: ER図が大きすぎて読めない

```yaml
# 解決方法: distance設定で関連範囲制限
er:
  distance: 1  # 直接関連のみ
```

**問題**: 一部のテーブルが表示されない

```yaml
# 解決方法: exclude設定確認
exclude:
  - schema_migrations  # 除外リスト確認
```

## 学習リソース

| リソース | URL |
|---------|-----|
| **公式GitHub** | [https://github.com/k1LoW/tbls](https://github.com/k1LoW/tbls) |
| **ドキュメント** | [https://github.com/k1LoW/tbls/blob/main/README.md](https://github.com/k1LoW/tbls/blob/main/README.md) |
| **使用例** | [https://github.com/k1LoW/tbls/tree/main/sample](https://github.com/k1LoW/tbls/tree/main/sample) |

## 関連ドキュメント

- [Flyway](./Flyway.md) - DBマイグレーションツール
- [Liquibase](./Liquibase.md) - DBマイグレーションツール
- [DBML](./DBML.md) - データベース定義言語
- [ERDPlus](./ERDPlus.md) - オンラインER図作成ツール
- [MySQL Workbench](./MySQL_Workbench.md) - MySQL公式GUIツール
- [pgModeler](./pgModeler.md) - PostgreSQLモデリングツール

---

**カテゴリ**: データベース設計・ドキュメント
**対象工程**: 詳細設計・実装・保守
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
