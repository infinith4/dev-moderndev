# pgModeler

## 概要

pgModelerは、PostgreSQL専用のオープンソースデータベースモデリングツールです。ER図（Entity-Relationship Diagram）を視覚的に設計し、DDL（Data Definition Language）を自動生成できます。既存データベースからのリバースエンジニアリング、差分比較、バージョン管理対応により、データベース設計からスキーマ管理までを効率化します。

## 主な機能

### 1. ER図設計
- **テーブル**: カラム、制約、インデックス定義
- **リレーションシップ**: 外部キー、1対多、多対多
- **ビュー**: SQLビュー定義
- **関数・トリガー**: PostgreSQL拡張機能
- **スキーマ**: 名前空間管理

### 2. DDL生成
- **CREATE文**: テーブル、インデックス、制約
- **ALTER文**: スキーマ変更
- **DROP文**: オブジェクト削除
- **PostgreSQL固有構文**: ARRAY、JSON、HStore等

### 3. リバースエンジニアリング
- **既存DB取り込み**: 接続してスキーマ取得
- **ER図自動生成**: データベースからモデル生成
- **差分比較**: モデルとDBの差分検出

### 4. バージョン管理
- **XML形式**: モデルをXMLで保存
- **Git統合**: バージョン管理システムで管理
- **変更履歴**: モデル変更の追跡

### 5. エクスポート
- **SQL**: DDLスクリプト出力
- **PNG/SVG**: ER図画像出力
- **PDF**: ドキュメント出力

## 利用方法

### インストール

```bash
# Windows: インストーラーダウンロード
# https://pgmodeler.io/download

# macOS (Homebrew)
brew install --cask pgmodeler

# Linux (Ubuntu/Debian)
sudo apt install pgmodeler

# ソースからビルド
git clone https://github.com/pgmodeler/pgmodeler.git
cd pgmodeler
qmake pgmodeler.pro
make
sudo make install
```

### 基本的な使い方

```
1. 新規モデル作成
   File → New Model

2. テーブル追加
   Database → Add → Table
   - テーブル名入力
   - カラム追加: name (VARCHAR), email (VARCHAR), created_at (TIMESTAMP)
   - Primary Key設定

3. リレーションシップ追加
   Database → Add → Relationship
   - ソーステーブル選択
   - ターゲットテーブル選択
   - 外部キー設定

4. DDL生成
   Export → SQL Code
   - PostgreSQL バージョン選択
   - エクスポート
```

### リバースエンジニアリング

```
1. データベース接続
   Database → Import → Database

2. 接続情報入力
   - Host: localhost
   - Port: 5432
   - Database: mydb
   - User: postgres
   - Password: ****

3. インポートオプション
   - Import all objects
   - Select specific schemas

4. ER図自動生成
   完了後、モデルが自動生成される
```

### DDLエクスポート

```sql
-- 生成されるDDL例
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
```

### 差分比較

```
1. モデルとDBの差分
   Database → Diff → Compare with Database

2. 接続情報入力

3. 差分レポート表示
   - 追加されたテーブル
   - 削除されたテーブル
   - 変更されたカラム

4. 差分SQL生成
   Generate ALTER statements
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **pgModeler (OSS)** | 🟢 無料 | オープンソース、GPLv3 License |
| **pgModeler Premium** | 💰 $30 USD（買い切り） | サポート、優先バグ修正 |

## メリット

### ✅ 主な利点

1. **PostgreSQL専用**: PostgreSQL固有機能完全サポート
2. **無料**: オープンソース、GPLv3
3. **視覚的設計**: ER図でデータベース設計
4. **DDL自動生成**: 手書きSQL不要
5. **リバースエンジニアリング**: 既存DBからモデル生成
6. **差分比較**: モデルとDBの同期確認
7. **バージョン管理**: XML形式でGit管理
8. **クロスプラットフォーム**: Windows、Mac、Linux対応
9. **拡張機能**: PostgreSQL拡張機能対応
10. **軽量**: 単独アプリケーション

## デメリット

### ❌ 制約・課題

1. **PostgreSQL専用**: MySQL、Oracle等は非対応
2. **学習曲線**: UI習得に時間
3. **大規模DB**: 巨大スキーマでパフォーマンス低下
4. **チーム協業**: 同時編集機能なし
5. **クラウドDB**: RDS、Cloud SQL直接接続に制約
6. **ドキュメント**: 日本語ドキュメント少ない
7. **プラグイン**: 拡張性が限定的
8. **GUI依存**: CLIツールなし

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **MySQL Workbench** | MySQL専用、無料 | pgModelerと類似だがMySQL向け |
| **DBeaver** | マルチDB、オープンソース | pgModelerより多DB対応だがER図機能弱い |
| **dbdiagram.io** | Web、Markdown風 | pgModelerよりシンプル、Web版 |
| **Lucidchart** | 汎用作図、協業 | pgModelerより協業強い |
| **ERBuilder** | 商用、多DB対応 | pgModelerより高機能だが有料 |

## 公式リンク

- **公式サイト**: [https://pgmodeler.io/](https://pgmodeler.io/)
- **ダウンロード**: [https://pgmodeler.io/download](https://pgmodeler.io/download)
- **GitHub**: [https://github.com/pgmodeler/pgmodeler](https://github.com/pgmodeler/pgmodeler)
- **ドキュメント**: [https://pgmodeler.io/support/documentation](https://pgmodeler.io/support/documentation)

## 関連ドキュメント

- [データベースツール一覧](../データベースツール/)
- [PostgreSQL](./PostgreSQL.md)
- [MySQL Workbench](./MySQL_Workbench.md)
- [DBeaver](./DBeaver.md)
- [データベース設計ベストプラクティス](../../best-practices/database-design.md)

---

**カテゴリ**: データベースツール  
**対象工程**: 設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
