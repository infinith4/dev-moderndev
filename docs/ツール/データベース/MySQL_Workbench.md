# MySQL Workbench

## 概要

MySQL Workbenchは、Oracle社が提供するMySQL公式の統合開発環境（IDE）です。データベース設計、SQL開発、サーバー管理を一つのツールで行える包括的なGUIツールで、ER図によるビジュアルデータベース設計、SQLエディタ、データモデリング、リバースエンジニアリング、データベース移行などの機能を提供します。

## 主な機能

### 1. データモデリング・設計
- **ER図作成**: ビジュアルなデータベース設計
- **テーブル設計**: カラム、データ型、制約の定義
- **リレーションシップ**: 外部キー、カーディナリティ設定
- **正規化**: データベース正規化支援
- **DDL生成**: モデルからCREATE文を自動生成

### 2. SQL開発
- **SQLエディタ**: シンタックスハイライト、自動補完
- **クエリ実行**: SQLの実行と結果表示
- **クエリビルダー**: ビジュアルでクエリ作成
- **実行計画**: クエリパフォーマンス分析
- **スニペット**: よく使うSQLの保存・再利用

### 3. データベース管理
- **サーバー管理**: 起動/停止、設定変更
- **ユーザー管理**: ユーザー・権限の管理
- **バックアップ・リストア**: データエクスポート/インポート
- **パフォーマンス監視**: サーバーステータス、クエリ統計

### 4. リバースエンジニアリング
- 既存データベースからER図を自動生成
- スキーマ構造の可視化
- ドキュメント生成

### 5. データベース移行
- Microsoft SQL Server、PostgreSQL、Sybaseからの移行
- スキーマ・データの変換
- 移行スクリプト生成

### 6. フォワードエンジニアリング
- モデルから実際のデータベースを生成
- ALTER文生成（既存DBとの差分）
- 同期機能

## 利用方法

### データベース接続

```
1. Home画面 → MySQL Connections の「+」ボタン
2. 接続情報入力:
   - Connection Name: 接続名（例: Local MySQL）
   - Hostname: localhost
   - Port: 3306
   - Username: root
   - Password: Store in Vault...
3. Test Connection でテスト
4. OK で保存
```

### ER図作成

```
1. メニュー → Database → Reverse Engineer
   または
   File → New Model
   
2. EER Diagram タブで右クリック → Add Diagram

3. テーブル追加:
   - ツールバーから Table アイコンをクリック
   - キャンバスに配置
   
4. テーブル定義:
   - テーブルをダブルクリック
   - Columns タブでカラム追加
     - Column Name, Datatype, PK, NN, UQ, AI 等を設定
   
5. リレーションシップ追加:
   - ツールバーから Relationship アイコン選択
   - 親テーブル → 子テーブルにドラッグ
   - 外部キー制約が自動生成
```

### SQL実行

```
1. 接続を開く（MySQL Connectionsから選択）

2. 新規SQLタブ作成（Ctrl+T）

3. SQLを記述:
   SELECT * FROM users WHERE age > 20;

4. 実行:
   - 全体実行: Ctrl+Shift+Enter
   - 選択部分のみ実行: Ctrl+Enter

5. 結果確認:
   - Result Grid タブに表示
   - Export ボタンで CSV/JSON 出力可能
```

### DDL生成

```
1. モデル（EER Diagram）を開く

2. Database → Forward Engineer

3. オプション選択:
   - Generate DROP statements before each CREATE
   - Generate separate CREATE INDEX statements
   
4. Preview SQL を確認

5. Execute で実行 または Save to File で保存
```

### データエクスポート

```
1. Server → Data Export

2. エクスポート対象選択:
   - スキーマ選択
   - テーブル選択
   
3. Export Options:
   - Export to Dump Project Folder（フォルダ）
   - Export to Self-Contained File（1ファイル）
   
4. Include options:
   - Dump Structure and Data（構造とデータ）
   - Dump Structure Only（構造のみ）
   - Dump Data Only（データのみ）
   
5. Start Export
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Community Edition** |  無料 | 全機能利用可能、オープンソース |
| **Commercial Edition** | MySQL Enterprise同梱 | エンタープライズサポート付き |

※MySQL Workbench Community Editionは無料で、すべての機能を利用できます

## メリット

###  主な利点

1. **無料**: MySQL公式ツールで全機能無料
2. **統合環境**: 設計・開発・管理を1ツールで完結
3. **ビジュアル設計**: ER図でデータベース設計
4. **リバースエンジニアリング**: 既存DBから図を自動生成
5. **DDL自動生成**: モデルからCREATE文を生成
6. **SQLエディタ**: 自動補完、シンタックスハイライト
7. **データベース移行**: SQL ServerやPostgreSQLから移行可能
8. **クロスプラットフォーム**: Windows、Mac、Linux対応
9. **公式ツール**: Oracleによる継続的な開発・サポート
10. **オープンソース**: GPLライセンス

## デメリット

###  制約・課題

1. **MySQL専用**: PostgreSQLやSQL Serverには非対応
2. **動作やや重い**: 大規模DBでは動作が遅い
3. **UI改善余地**: モダンなUIツールと比較すると古い
4. **学習曲線**: 多機能なため初心者には難しい
5. **バグ**: 時々クラッシュやバグが報告される
6. **日本語ドキュメント少ない**: 公式は英語中心
7. **チーム協業弱い**: モデルファイルのバージョン管理が困難
8. **クラウドDB対応限定的**: RDSやAzure DBへの接続は可能だが機能制限

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **DBeaver** | マルチDB対応、無料 | MySQL以外も対応、ER図機能は弱い |
| **phpMyAdmin** | Webベース、MySQL専用 | ブラウザで利用、機能は限定的 |
| **HeidiSQL** | 軽量、Windows専用 | MySQL Workbenchより軽量 |
| **Sequel Pro / Sequel Ace** | Mac専用、シンプル | ER図機能はない |
| **pgAdmin** | PostgreSQL専用 | MySQL非対応 |
| **DataGrip (JetBrains)** | 有料、マルチDB | MySQL Workbenchより高機能だが有料 |

## 公式リンク

- **公式サイト**: [https://www.mysql.com/products/workbench/](https://www.mysql.com/products/workbench/)
- **ダウンロード**: [https://dev.mysql.com/downloads/workbench/](https://dev.mysql.com/downloads/workbench/)
- **ドキュメント**: [https://dev.mysql.com/doc/workbench/en/](https://dev.mysql.com/doc/workbench/en/)
- **チュートリアル**: [https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial.html](https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial.html)

## 関連ドキュメント

- [データベースツール一覧](../データベースツール/)
- [DBeaver](./DBeaver.md)
- [データベース設計ベストプラクティス](../../best-practices/database-design.md)
- [ER図作成ガイド](../../best-practices/er-diagram.md)

---

**カテゴリ**: データベースツール  
**対象工程**: 基本設計、詳細設計、実装  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0

