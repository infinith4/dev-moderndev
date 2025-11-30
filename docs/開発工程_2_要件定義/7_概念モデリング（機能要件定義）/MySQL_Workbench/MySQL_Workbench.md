# MySQL Workbench

## 概要

MySQL Workbenchは、MySQL公式の統合開発環境（IDE）で、ER図作成、データベース設計、SQL開発、サーバー管理など、MySQLに関するすべての作業を一元管理できます。フォワードエンジニアリング（ER図からDDL生成）とリバースエンジニアリング（既存DBからER図生成）の両方に対応しています。

### 主な特徴

- **完全無料**: オープンソースで無料
- **MySQL統合**: MySQLとの完全な統合
- **フォワード/リバースエンジニアリング**: ER図⇔DDLの双方向変換
- **SQL自動生成**: ER図から高品質なDDLを自動生成
- **クロスプラットフォーム**: Windows、macOS、Linux対応

### 料金プラン

- **完全無料**: オープンソース（GPLライセンス）

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- MySQLとの完全統合により、シームレスなデータベース開発が可能
- フォワードエンジニアリング（モデル→DB）とリバースエンジニアリング（DB→モデル）
- SQL自動生成が高品質
- クロスプラットフォーム対応

**デメリット**
- MySQL特化（PostgreSQL、Oracle等には非対応）
- 概念モデリングはやや弱い（物理モデル寄り）
- UI改善の余地あり
- 学習曲線がやや急

## 利用方法

### 1. インストール

1. [MySQL Workbench公式サイト](https://www.mysql.com/products/workbench/)からダウンロード
2. OSに応じたインストーラーを選択（Windows、macOS、Linux）
3. インストーラーを実行してセットアップ
4. MySQL Workbenchを起動

### 2. 新規EERダイアグラムの作成

EER（Extended Entity-Relationship）ダイアグラムは、ER図の拡張版です。

1. MySQL Workbenchを起動
2. 「File」→「New Model」を選択
3. モデル名を入力（例: "ECサイトDB"）
4. 「Add Diagram」ボタンをクリック
5. EERダイアグラムのキャンバスが表示される

### 3. テーブルの追加

#### テーブルの配置

1. 左側のツールバーから「Place a New Table」アイコンをクリック
2. キャンバス上でクリックして配置
3. テーブル名を入力（例: "customer"、"order"、"product"）

#### カラムの定義

1. テーブルをダブルクリック
2. 「Columns」タブでカラムを定義:
   - **Column Name**: カラム名
   - **Datatype**: データ型（INT、VARCHAR、DATE等）
   - **PK**: 主キー（チェックボックス）
   - **NN**: NOT NULL（チェックボックス）
   - **UQ**: UNIQUE（チェックボックス）
   - **AI**: AUTO_INCREMENT（チェックボックス）
   - **Default**: デフォルト値

#### 例: customerテーブル

| Column Name | Datatype | PK | NN | AI | Default |
|-------------|----------|----|----|----|----|
| customer_id | INT | ✓ | ✓ | ✓ | |
| customer_name | VARCHAR(100) | | ✓ | | |
| email | VARCHAR(100) | | | | |
| phone | VARCHAR(20) | | | | |
| address | VARCHAR(200) | | | | |
| created_at | TIMESTAMP | | ✓ | | CURRENT_TIMESTAMP |

### 4. リレーションシップの設定

#### 外部キーの作成

方法1: 視覚的な接続
1. 左側ツールバーから「Place a Relationship」アイコンをクリック
2. 関係タイプを選択:
   - **1:n Non-Identifying**: 1対多（非識別関係）
   - **1:1 Non-Identifying**: 1対1（非識別関係）
   - **n:m Identifying**: 多対多（識別関係、中間テーブル自動生成）
3. 親テーブルをクリック
4. 子テーブルをクリック
5. 自動的に外部キーが設定される

方法2: 手動設定
1. 子テーブルをダブルクリック
2. 「Foreign Keys」タブを選択
3. 「Add」ボタンをクリック
4. 外部キー名を入力
5. 「Referenced Table」で親テーブルを選択
6. カラムのマッピングを設定

### 5. ER図の具体例

**例: 図書館管理システム**

#### テーブル定義

**bookテーブル（書籍）**
- book_id (PK, INT, AI)
- title (VARCHAR(200), NN)
- author (VARCHAR(100))
- isbn (VARCHAR(20), UQ)
- publication_year (INT)
- category (VARCHAR(50))

**memberテーブル（会員）**
- member_id (PK, INT, AI)
- member_name (VARCHAR(100), NN)
- email (VARCHAR(100), UQ)
- phone (VARCHAR(20))
- membership_date (DATE, NN)

**loanテーブル（貸出）**
- loan_id (PK, INT, AI)
- book_id (FK → book.book_id, NN)
- member_id (FK → member.member_id, NN)
- loan_date (DATE, NN)
- due_date (DATE, NN)
- return_date (DATE)
- status (ENUM('貸出中', '返却済み'), NN)

#### リレーションシップ

1. **member** 1:n **loan**: 1人の会員が複数の貸出レコードを持つ
2. **book** 1:n **loan**: 1冊の本が複数の貸出レコードを持つ

### 6. インデックスの設定

1. テーブルをダブルクリック
2. 「Indexes」タブを選択
3. 「Add」ボタンをクリック
4. インデックス名を入力
5. インデックスに含めるカラムを選択
6. インデックスタイプを選択（INDEX、UNIQUE等）

### 7. SQL自動生成（フォワードエンジニアリング）

#### DDLの生成

1. 「Database」→「Forward Engineer...」を選択
2. 接続先MySQLサーバーを選択（またはローカル）
3. 「Next」をクリック
4. 生成オプションを設定:
   - **DROP objects before creation**: 既存オブジェクトを削除
   - **Generate INSERT statements**: サンプルデータのINSERT文生成
5. 「Next」をクリック
6. 生成されるSQLを確認
7. 「Execute」でデータベースに適用、または「Export SQL Script」でファイル保存

#### 生成されるSQL例

```sql
CREATE TABLE `book` (
  `book_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  `author` VARCHAR(100) NULL,
  `isbn` VARCHAR(20) NULL,
  `publication_year` INT NULL,
  `category` VARCHAR(50) NULL,
  PRIMARY KEY (`book_id`),
  UNIQUE INDEX `isbn_UNIQUE` (`isbn` ASC)
);

CREATE TABLE `member` (
  `member_id` INT NOT NULL AUTO_INCREMENT,
  `member_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NULL,
  `phone` VARCHAR(20) NULL,
  `membership_date` DATE NOT NULL,
  PRIMARY KEY (`member_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC)
);

CREATE TABLE `loan` (
  `loan_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `member_id` INT NOT NULL,
  `loan_date` DATE NOT NULL,
  `due_date` DATE NOT NULL,
  `return_date` DATE NULL,
  `status` ENUM('貸出中', '返却済み') NOT NULL,
  PRIMARY KEY (`loan_id`),
  INDEX `fk_loan_book_idx` (`book_id` ASC),
  INDEX `fk_loan_member_idx` (`member_id` ASC),
  CONSTRAINT `fk_loan_book`
    FOREIGN KEY (`book_id`)
    REFERENCES `book` (`book_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_loan_member`
    FOREIGN KEY (`member_id`)
    REFERENCES `member` (`member_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
```

### 8. リバースエンジニアリング（既存DBからER図生成）

既存のMySQLデータベースからER図を自動生成できます。

1. 「Database」→「Reverse Engineer...」を選択
2. MySQL接続を選択
3. 「Continue」をクリック
4. スキーマを選択
5. インポートするテーブルを選択
6. 「Execute」をクリック
7. ER図が自動生成される

### 9. 用語集（データディクショナリ）の作成

MySQL Workbenchでは、各テーブル・カラムにコメントを追加できます。

1. テーブルをダブルクリック
2. 「Columns」タブで、各カラムの「Comment」欄に説明を入力
3. 「Table」タブで、テーブル全体のコメントを入力

これらのコメントは、DDL生成時に `COMMENT` 句として出力されます。

```sql
CREATE TABLE `book` (
  `book_id` INT NOT NULL AUTO_INCREMENT COMMENT '書籍ID',
  `title` VARCHAR(200) NOT NULL COMMENT '書籍タイトル',
  PRIMARY KEY (`book_id`)
) COMMENT = '書籍マスタテーブル';
```

### 10. モデルの保存とエクスポート

#### モデルの保存

1. 「File」→「Save Model」を選択
2. ファイル名を入力（例: "図書館管理システム.mwb"）
3. 保存

#### PNG/PDF/SVGエクスポート

1. 「File」→「Export」→「Export as PNG/PDF/SVG」
2. ファイル名を入力
3. 「Save」をクリック

#### SQL DDLエクスポート

1. 「File」→「Export」→「Forward Engineer SQL CREATE Script...」
2. ファイル名を入力（例: "create_library_db.sql"）
3. 「Save」をクリック

## 公式ドキュメント

- **公式サイト**: [MySQL Workbench](https://www.mysql.com/products/workbench/)
- **公式マニュアル**: [MySQL Workbench Manual](https://dev.mysql.com/doc/workbench/en/)
- **データモデリング**: [Data Modeling with MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-data-modeling.html)
- **フォワードエンジニアリング**: [Forward Engineering](https://dev.mysql.com/doc/workbench/en/wb-forward-engineering-live-server.html)
- **リバースエンジニアリング**: [Reverse Engineering](https://dev.mysql.com/doc/workbench/en/wb-reverse-engineering.html)

## 学習リソース

- **MySQL Workbench Tutorial**: [Tutorial Video](https://www.youtube.com/results?search_query=mysql+workbench+tutorial)
- **ER図作成ガイド**: [Creating EER Diagrams](https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial-creating-a-model.html)

## 関連リンク

- [MySQL公式サイト](https://www.mysql.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [データベース正規化理論](https://en.wikipedia.org/wiki/Database_normalization)
