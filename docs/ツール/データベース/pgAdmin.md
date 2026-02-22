# pgAdmin 4

## 概要

pgAdmin 4は、PostgreSQL公式のオープンソース管理ツールです。Webブラウザベースのインターフェースで、データベースの作成・管理、SQL実行、データのインポート/エクスポート、バックアップ/リストア、クエリビルダー、ER図表示などの包括的な機能を提供します。デスクトップモード（Electron）とサーバーモード（Webアプリ）の両方で動作し、Windows、macOS、Linuxに対応しています。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | https://www.pgadmin.org/ |
| **料金** | 🟢 無料 |
| **ライセンス** | PostgreSQL License（オープンソース） |
| **対応OS** | Windows、macOS、Linux、Docker |
| **動作環境** | Webブラウザ（Chrome、Firefox、Safari、Edge等）またはデスクトップアプリ |
| **開発元** | pgAdmin Development Team |
| **初版リリース** | 1996年（pgAdmin 4は2016年） |
| **最新バージョン** | 8.x（2024年時点） |

## 主な機能

### 1. データベース管理
- **オブジェクト管理**: データベース、スキーマ、テーブル、ビュー、関数、トリガー等をGUIで作成・編集・削除
- **ユーザー/ロール管理**: PostgreSQLユーザー、ロール、権限をグラフィカルに管理
- **データベースダッシュボード**: アクティブセッション、トランザクション、ロック、統計情報をリアルタイム表示

### 2. SQLクエリツール
- **SQLエディタ**: シンタックスハイライト、オートコンプリート、コードフォーマット機能
- **クエリ履歴**: 過去のSQL実行履歴を保存・再実行
- **結果グリッド**: クエリ結果を表形式で表示、フィルタ、ソート、エクスポート
- **実行計画**: EXPLAIN / EXPLAIN ANALYZEの結果をビジュアル表示

### 3. データ操作
- **データビューア**: テーブルデータの閲覧、フィルタ、ソート、編集
- **インポート/エクスポート**: CSV、Excel、JSON形式でのデータ入出力
- **クエリビルダー**: GUIでSELECT文を構築（ビジュアルクエリビルダー）
- **バッチ実行**: SQLスクリプトファイルの実行

### 4. バックアップ/リストア
- **pg_dump統合**: データベース全体または個別オブジェクトをバックアップ
- **pg_restore統合**: バックアップからのリストア
- **カスタム形式**: 圧縮バックアップ、並列リストア対応
- **スケジューリング**: 定期的なバックアップジョブ設定（pgAgent連携）

### 5. モニタリング/診断
- **サーバーアクティビティ**: アクティブセッション、実行中クエリの監視
- **ロック/ブロッキング**: ロック競合、ブロッキングセッションの検出
- **統計情報**: テーブル統計、インデックス使用状況、パフォーマンスメトリクス
- **ログビューア**: PostgreSQLログファイルの閲覧

### 6. スキーマ設計
- **ER図表示**: テーブル関係を自動生成（ERD）
- **DDLビューア**: オブジェクトのCREATE文を表示・コピー
- **リバースエンジニアリング**: 既存DBからスキーマ定義を抽出
- **スキーマ比較**: データベース間の差分検出（プラグイン）

### 7. 開発者向け機能
- **関数/プロシージャエディタ**: PL/pgSQL、PL/Python、PL/Perl等のコード編集・デバッグ
- **トリガー管理**: トリガー作成・編集・テスト
- **拡張機能管理**: PostgreSQL Extensionのインストール・管理
- **パーティション管理**: テーブルパーティション設定

## 利用方法

### インストール

#### 1. デスクトップアプリ（推奨）
```bash
# Windows
# https://www.pgadmin.org/download/pgadmin-4-windows/ からインストーラーダウンロード

# macOS
brew install --cask pgadmin4

# Ubuntu/Debian
sudo apt install pgadmin4-desktop
```

#### 2. Dockerコンテナ
```bash
# pgAdmin 4をDockerで起動
docker run -p 5050:80 \
  -e 'PGADMIN_DEFAULT_EMAIL=admin@example.com' \
  -e 'PGADMIN_DEFAULT_PASSWORD=admin' \
  -d dpage/pgadmin4

# ブラウザで http://localhost:5050 にアクセス
```

#### 3. Python pip（サーバーモード）
```bash
# Python 3.7以上が必要
pip install pgadmin4

# サーバーモードで起動
pgadmin4
# http://127.0.0.1:5050 にアクセス
```

### 基本的な使い方

#### 1. サーバー接続設定
```
1. pgAdmin 4を起動
2. 左パネルで「Servers」を右クリック → Create → Server
3. General タブ:
   - Name: ローカルPostgreSQL（任意の名前）
4. Connection タブ:
   - Host: localhost
   - Port: 5432
   - Database: postgres
   - Username: postgres
   - Password: [パスワード]
5. Save をクリック
```

#### 2. データベース作成
```
1. サーバーを展開 → Databases を右クリック → Create → Database
2. General タブ:
   - Database: my_database
   - Owner: postgres
3. Save をクリック
```

#### 3. テーブル作成（GUIで）
```
1. Databases → my_database → Schemas → public → Tables を右クリック → Create → Table
2. General タブ:
   - Name: users
3. Columns タブ → + ボタンで列追加:
   - Name: id, Data type: integer, Primary key: チェック
   - Name: name, Data type: character varying(100)
   - Name: email, Data type: character varying(255)
4. Save をクリック
```

#### 4. SQLクエリ実行
```sql
-- Tools → Query Tool でSQLエディタを開く

-- データ挿入
INSERT INTO users (id, name, email) VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com');

-- データ検索
SELECT * FROM users WHERE name LIKE 'A%';

-- F5キーまたは実行ボタンでクエリ実行
```

#### 5. データのインポート/エクスポート
```
【エクスポート】
1. テーブルを右クリック → Import/Export Data
2. Export タブ選択
3. Format: csv
4. Filename: /path/to/users.csv
5. Columns to export: 全選択
6. OK をクリック

【インポート】
1. テーブルを右クリック → Import/Export Data
2. Import タブ選択
3. Format: csv
4. Filename: /path/to/import.csv
5. Header: Yes（CSVにヘッダー行がある場合）
6. OK をクリック
```

#### 6. バックアップ/リストア
```
【バックアップ】
1. データベースを右クリック → Backup
2. Filename: /path/to/backup.dump
3. Format: Custom（圧縮形式）
4. Backup をクリック

【リストア】
1. データベースを右クリック → Restore
2. Filename: /path/to/backup.dump
3. Format: Custom
4. Restore をクリック
```

### 実行計画の確認
```sql
-- Query Tool で EXPLAIN を実行
EXPLAIN ANALYZE
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;

-- Explain タブに実行計画がグラフィカル表示される
-- - Seq Scan（全表スキャン）
-- - Index Scan（インデックス使用）
-- - Hash Join（結合方法）
-- 各ノードのコスト、実行時間、行数が視覚化
```

## メリット

### 1. PostgreSQL公式ツール
✅ PostgreSQL開発チームが公式サポート
✅ 最新のPostgreSQL機能に対応（パーティション、JSON、FDW等）
✅ PostgreSQL全バージョンに対応（9.x〜16.x）

### 2. 無料・オープンソース
✅ ライセンス費用ゼロ
✅ ソースコード公開、カスタマイズ可能
✅ 商用利用も無料

### 3. クロスプラットフォーム
✅ Windows、macOS、Linux対応
✅ Webブラウザベース（どこからでもアクセス）
✅ Dockerコンテナ対応

### 4. 包括的な機能
✅ 管理・開発・運用の全機能を統合
✅ GUI操作とSQL両方サポート
✅ バックアップ/リストアの自動化

### 5. 可視化・モニタリング
✅ ER図自動生成
✅ 実行計画のグラフィカル表示
✅ サーバーアクティビティのリアルタイム監視

### 6. マルチデータベース管理
✅ 複数のPostgreSQLサーバーを一元管理
✅ データベース間のスキーマ比較
✅ リモートサーバー管理

## デメリット

### 1. UIの複雑さ
❌ 機能が多く、初心者には習得に時間がかかる
❌ 画面構成が複雑で直感的でない部分あり
❌ メニュー階層が深い

### 2. パフォーマンス
❌ 大規模データベースでは動作が重い
❌ Webベースのため、ネイティブアプリより遅延
❌ クエリ結果の大量表示で固まることがある

### 3. PostgreSQL専用
❌ MySQL、SQL Server等には使用不可
❌ PostgreSQL以外のDBを管理する場合は別ツールが必要

### 4. ER図機能の制限
❌ ER図は閲覧のみで編集不可
❌ ER図から直接テーブル作成できない
❌ データモデリングツールとしては不十分

### 5. バグ・安定性
❌ バージョンアップで新機能追加と同時にバグ混入
❌ Webブラウザ依存のため、ブラウザ互換性問題
❌ セッションタイムアウトで作業が失われることがある

## ユースケース

### 1. PostgreSQL管理者
- データベースの日常管理（ユーザー、権限、パフォーマンス監視）
- バックアップ/リストアの実行・スケジューリング
- トラブルシューティング（ロック、ブロッキング検出）

### 2. アプリケーション開発者
- データベーススキーマ設計・作成
- SQLクエリの開発・テスト・デバッグ
- 関数/ストアドプロシージャの開発

### 3. データアナリスト
- アドホッククエリの実行
- データのエクスポート（CSV、Excel）
- 集計・分析用のデータ抽出

### 4. DevOps/SREエンジニア
- データベースのヘルスチェック
- パフォーマンスメトリクスの確認
- スキーマ変更の適用

## 類似ツールとの比較

| ツール | 料金 | PostgreSQL対応 | 特徴 |
|--------|------|---------------|------|
| **pgAdmin 4** | 🟢 無料 | ✅ 公式 | PostgreSQL公式、全機能網羅 |
| DBeaver | 🟢 無料 | ✅ 対応 | マルチDB対応、SQL開発に強い |
| DataGrip | 🔴 有料 | ✅ 対応 | JetBrains製、高機能IDE |
| Adminer | 🟢 無料 | ✅ 対応 | 軽量、PHPベース、シンプル |
| TablePlus | 🟡 一部無料 | ✅ 対応 | macOS/iOS向け、モダンUI |

### pgAdmin 4を選ぶべきケース
- PostgreSQL専用の管理ツールが欲しい
- 無料でフル機能を使いたい
- バックアップ/リストアを含む総合管理が必要
- リモートサーバーをWebから管理したい

### 他ツールを検討すべきケース
- MySQL、SQL Server等も管理したい → **DBeaver**
- より洗練されたUIが欲しい → **DataGrip**、**TablePlus**
- 軽量でシンプルなツールが欲しい → **Adminer**

## ベストプラクティス

### 1. 接続設定の管理
```
✅ サーバーごとにグループ化（開発、ステージング、本番）
✅ 読み取り専用ユーザーで接続（本番環境）
✅ SSHトンネリング経由で安全に接続
✅ 接続パスワードはマスターパスワードで暗号化
```

### 2. クエリパフォーマンス最適化
```sql
-- 常にEXPLAIN ANALYZEで実行計画を確認
EXPLAIN ANALYZE
SELECT * FROM large_table WHERE id > 1000;

-- Seq Scanが発生している場合はインデックス追加
CREATE INDEX idx_id ON large_table(id);

-- 再度実行計画を確認
EXPLAIN ANALYZE
SELECT * FROM large_table WHERE id > 1000;
-- Index Scan に変わったことを確認
```

### 3. バックアップの自動化
```
1. pgAgent拡張機能をインストール
   CREATE EXTENSION pgagent;

2. pgAdmin 4でスケジュールジョブ作成:
   - Tools → pgAgent Jobs → Create Job
   - Name: Daily Backup
   - Schedule: 毎日 2:00 AM
   - Steps: pg_dump コマンド実行

3. 定期的にバックアップファイルの確認・テストリストア実施
```

### 4. クエリ履歴の活用
```
✅ Query History（Ctrl+Shift+H）で過去のクエリを再利用
✅ 頻繁に使うクエリはスニペットとして保存
✅ クエリエディタの履歴をエクスポートして共有
```

### 5. セキュリティ
```
✅ 本番環境では読み取り専用ロールで接続
✅ DELETE/TRUNCATE実行前に必ずトランザクション確認
✅ master passwordでpgAdmin設定を暗号化
✅ Webサーバーモードでは認証を必須化
```

## 公式リンク

- **公式サイト**: https://www.pgadmin.org/
- **ダウンロード**: https://www.pgadmin.org/download/
- **ドキュメント**: https://www.pgadmin.org/docs/
- **GitHub**: https://github.com/pgadmin-org/pgadmin4
- **コミュニティ**: https://www.postgresql.org/list/pgadmin-support/

## 関連ツール

- [PostgreSQL](./PostgreSQL.md) - pgAdmin 4が管理対象とするデータベース
- [MySQL Workbench](./MySQL_Workbench.md) - MySQL版の公式管理ツール
- [ERDPlus](./ERDPlus.md) - ER図作成専用ツール
- [Flyway](./Flyway.md) - データベースマイグレーションツール
- [DBeaver](https://dbeaver.io/) - マルチデータベース対応の無料ツール

## まとめ

pgAdmin 4は、PostgreSQL公式の包括的な管理ツールとして、データベース管理者から開発者まで幅広く利用されています。無料でありながら、GUI操作、SQL開発、バックアップ/リストア、モニタリング、ER図表示など、PostgreSQL運用に必要な全機能を提供します。

UI/UXは若干複雑ですが、PostgreSQL専用ツールとして最も信頼性が高く、継続的にアップデートされています。PostgreSQLを使用するプロジェクトにおいて、標準的な管理ツールとして採用する価値があります。
