# MySQL Workbench（データベース論理設計）

## 概要

MySQL Workbenchは、MySQL公式のデータベース設計ツールで、基本設計フェーズではER図の詳細化、テーブル定義、カラム定義、インデックス設計、外部キー制約の設計に活用します。論理ERDから物理ERDへの変換、正規化、DDL自動生成が可能です。

### 基本設計フェーズでの活用

- **論理ER図の作成**: エンティティとリレーションシップの詳細設計
- **テーブル定義**: テーブル名、カラム名、データ型、桁数の定義
- **制約定義**: PRIMARY KEY、UNIQUE、NOT NULL、CHECK制約
- **インデックス設計**: 検索性能向上のためのインデックス設計
- **外部キー制約**: テーブル間の参照整合性定義
- **正規化**: 第1正規形〜第3正規形への正規化
- **DDL自動生成**: CREATE TABLE文の自動生成

### 料金プラン

- **MySQL Workbench**: 完全無料（GPL v2ライセンス）

### メリット・デメリット

**メリット**
- 完全無料でMySQL公式ツール
- ER図から直接SQLを生成可能
- リバースエンジニアリングで既存DBからER図を生成
- フォワードエンジニアリングでER図からDBを構築
- データ型、インデックス、外部キーの詳細設定が可能
- MySQLとの完全互換性

**デメリット**
- MySQL専用（PostgreSQL、Oracle等には非対応）
- 複数人での同時編集が困難
- バージョン管理がファイルベースで制限的

## 利用方法

### 1. MySQL Workbenchのインストール

1. [MySQL公式サイト](https://dev.mysql.com/downloads/workbench/)にアクセス
2. OS別のインストーラーをダウンロード
3. インストーラーを実行
4. MySQLサーバーへの接続情報を設定（オプション）

### 2. 新規ERモデルの作成

1. MySQL Workbenchを起動
2. File → New Model
3. モデル名を入力（例: "ECサイトDB論理設計"）

### 3. 論理ER図の作成

#### 例: ECサイトのデータベース論理設計

**対象テーブル:**
- customers（顧客）
- products（商品）
- orders（注文）
- order_items（注文明細）
- categories（カテゴリ）

#### テーブル設計

**1. customersテーブルの作成**

1. 左側の「Add Diagram」をクリックして新規EER Diagramを作成
2. 左ツールバーから「Place a New Table」アイコンを選択
3. キャンバスをクリックしてテーブルを配置
4. テーブル名を入力: `customers`
5. テーブルをダブルクリックして詳細設定を開く

**カラム定義:**

| カラム名 | データ型 | 桁数 | NULL許可 | デフォルト | 備考 |
|---------|---------|------|---------|----------|------|
| customer_id | INT | - | NO | AUTO_INCREMENT | 主キー |
| email | VARCHAR | 100 | NO | - | UNIQUE制約 |
| password_hash | VARCHAR | 255 | NO | - | - |
| first_name | VARCHAR | 50 | NO | - | - |
| last_name | VARCHAR | 50 | NO | - | - |
| phone | VARCHAR | 20 | YES | NULL | - |
| address | VARCHAR | 200 | YES | NULL | - |
| city | VARCHAR | 50 | YES | NULL | - |
| postal_code | VARCHAR | 10 | YES | NULL | - |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP ON UPDATE | - |

**設定手順:**

1. 「Columns」タブで各カラムを追加
2. カラム名を入力
3. Datatype列でデータ型を選択
4. PK（主キー）にチェック: `customer_id`
5. NN（NOT NULL）にチェック: 必須項目
6. UQ（UNIQUE）にチェック: `email`
7. AI（AUTO_INCREMENT）にチェック: `customer_id`

**2. productsテーブルの作成**

同様に `products` テーブルを作成:

| カラム名 | データ型 | 桁数 | NULL許可 | デフォルト | 備考 |
|---------|---------|------|---------|----------|------|
| product_id | INT | - | NO | AUTO_INCREMENT | 主キー |
| category_id | INT | - | YES | NULL | 外部キー→categories |
| product_name | VARCHAR | 200 | NO | - | - |
| description | TEXT | - | YES | NULL | - |
| price | DECIMAL | 10,2 | NO | - | - |
| stock_quantity | INT | - | NO | 0 | - |
| is_active | TINYINT | 1 | NO | 1 | 0=無効、1=有効 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP ON UPDATE | - |

**3. ordersテーブルの作成**

| カラム名 | データ型 | 桁数 | NULL許可 | デフォルト | 備考 |
|---------|---------|------|---------|----------|------|
| order_id | INT | - | NO | AUTO_INCREMENT | 主キー |
| customer_id | INT | - | NO | - | 外部キー→customers |
| order_date | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - |
| status | ENUM | - | NO | 'pending' | 'pending','shipped','delivered','cancelled' |
| total_amount | DECIMAL | 10,2 | NO | - | - |
| shipping_address | VARCHAR | 200 | NO | - | - |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP ON UPDATE | - |

**ENUM型の設定:**

1. Datatype列に `ENUM('pending','shipped','delivered','cancelled')` を入力

**4. order_itemsテーブルの作成**

| カラム名 | データ型 | 桁数 | NULL許可 | デフォルト | 備考 |
|---------|---------|------|---------|----------|------|
| order_item_id | INT | - | NO | AUTO_INCREMENT | 主キー |
| order_id | INT | - | NO | - | 外部キー→orders |
| product_id | INT | - | NO | - | 外部キー→products |
| quantity | INT | - | NO | - | CHECK (quantity > 0) |
| unit_price | DECIMAL | 10,2 | NO | - | - |
| subtotal | DECIMAL | 10,2 | NO | - | 計算カラム（quantity * unit_price） |

**5. categoriesテーブルの作成**

| カラム名 | データ型 | 桁数 | NULL許可 | デフォルト | 備考 |
|---------|---------|------|---------|----------|------|
| category_id | INT | - | NO | AUTO_INCREMENT | 主キー |
| category_name | VARCHAR | 100 | NO | - | UNIQUE制約 |
| parent_category_id | INT | - | YES | NULL | 自己参照外部キー |
| description | TEXT | - | YES | NULL | - |

### 4. 外部キー制約の設定

#### 1対多リレーションシップの作成

**ordersテーブル → customersテーブル（多対1）**

1. 左ツールバーから「Place a Relationship Using Existing Columns」を選択
2. `orders` テーブルをクリック
3. `customers` テーブルをクリック
4. リレーションシップが作成される
5. リレーションシップをダブルクリックして詳細設定
6. Foreign Key設定:
   - **Foreign Key Name**: `fk_orders_customer_id`
   - **Referenced Table**: `customers`
   - **Column Mapping**: `customer_id` → `customer_id`
   - **On Update**: CASCADE
   - **On Delete**: RESTRICT

**設定の意味:**
- `ON UPDATE CASCADE`: 親テーブルのIDが更新されたら子テーブルも更新
- `ON DELETE RESTRICT`: 親テーブルのレコードが削除できない（子レコードが存在する場合）

**同様に以下のリレーションシップを作成:**

- `orders.customer_id` → `customers.customer_id`
- `order_items.order_id` → `orders.order_id` (ON DELETE CASCADE)
- `order_items.product_id` → `products.product_id` (ON DELETE RESTRICT)
- `products.category_id` → `categories.category_id`
- `categories.parent_category_id` → `categories.category_id` (自己参照)

### 5. インデックス設計

検索性能向上のためにインデックスを設計します。

#### インデックスの追加

1. テーブルをダブルクリック
2. 「Indexes」タブを選択
3. 「+」ボタンをクリック
4. インデックス名を入力
5. 対象カラムを選択

**例: customersテーブルのインデックス**

| インデックス名 | カラム | タイプ | 用途 |
|--------------|--------|--------|------|
| PRIMARY | customer_id | PRIMARY KEY | 主キー |
| idx_email | email | UNIQUE | メールアドレス検索 |
| idx_created_at | created_at | INDEX | 登録日検索 |

**例: ordersテーブルのインデックス**

| インデックス名 | カラム | タイプ | 用途 |
|--------------|--------|--------|------|
| PRIMARY | order_id | PRIMARY KEY | 主キー |
| idx_customer_id | customer_id | INDEX | 顧客別注文検索 |
| idx_order_date | order_date | INDEX | 注文日検索 |
| idx_status | status | INDEX | ステータス検索 |

**複合インデックスの作成:**

1. Indexesタブで新規インデックスを作成
2. 名前: `idx_customer_order_date`
3. カラムを追加: `customer_id`, `order_date`
4. これにより顧客別・日付順検索が高速化

### 6. CHECK制約の設定

データ整合性を保つための制約を設定します。

#### CHECK制約の例

**productsテーブルのCHECK制約:**

1. テーブルをダブルクリック
2. 「Check」タブを選択（MySQL 8.0.16以降）
3. 「+」ボタンをクリック
4. 制約名: `chk_price_positive`
5. Expression: `price >= 0`

**他のCHECK制約例:**

- `chk_stock_quantity_positive`: `stock_quantity >= 0`
- `chk_quantity_positive` (order_items): `quantity > 0`

### 7. 正規化の実施

#### 正規化のチェック

**第1正規形（1NF）:**
- すべての属性が原子値（分割不可能な値）
- 例: `address` を `prefecture`, `city`, `street` に分割

**第2正規形（2NF）:**
- 1NFを満たす
- 部分関数従属を排除
- 例: `order_items.product_name` を削除（`products.product_name` から取得）

**第3正規形（3NF）:**
- 2NFを満たす
- 推移的関数従属を排除
- 例: `orders.customer_name` を削除（`customers` から取得）

### 8. DDL（CREATE TABLE文）の生成

設計したER図からSQL文を自動生成します。

1. メニューバー → Database → Forward Engineer
2. 接続先を選択（または「Export SQL Script」でファイル出力）
3. オプションを選択:
   - **Generate DROP Statements**: DROP TABLE文を含める
   - **Generate INSERT Statements**: サンプルデータを含める
4. 「Continue」をクリック
5. 生成されたSQLをプレビュー
6. 「Execute」または「Save to File」

**生成されるSQL例:**

```sql
-- customers テーブル
CREATE TABLE `customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `phone` VARCHAR(20) NULL,
  `address` VARCHAR(200) NULL,
  `city` VARCHAR(50) NULL,
  `postal_code` VARCHAR(10) NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `idx_email` (`email` ASC),
  INDEX `idx_created_at` (`created_at` ASC)
) ENGINE = InnoDB;

-- products テーブル
CREATE TABLE `products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NULL,
  `product_name` VARCHAR(200) NOT NULL,
  `description` TEXT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `stock_quantity` INT NOT NULL DEFAULT 0,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`),
  INDEX `fk_products_category_idx` (`category_id` ASC),
  CONSTRAINT `fk_products_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `categories` (`category_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `chk_price_positive` CHECK (`price` >= 0),
  CONSTRAINT `chk_stock_quantity_positive` CHECK (`stock_quantity` >= 0)
) ENGINE = InnoDB;

-- orders テーブル
CREATE TABLE `orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `order_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('pending', 'shipped', 'delivered', 'cancelled') NOT NULL DEFAULT 'pending',
  `total_amount` DECIMAL(10,2) NOT NULL,
  `shipping_address` VARCHAR(200) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  INDEX `fk_orders_customer_idx` (`customer_id` ASC),
  INDEX `idx_order_date` (`order_date` ASC),
  INDEX `idx_status` (`status` ASC),
  CONSTRAINT `fk_orders_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `customers` (`customer_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- order_items テーブル
CREATE TABLE `order_items` (
  `order_item_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `unit_price` DECIMAL(10,2) NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  INDEX `fk_order_items_order_idx` (`order_id` ASC),
  INDEX `fk_order_items_product_idx` (`product_id` ASC),
  CONSTRAINT `fk_order_items_order`
    FOREIGN KEY (`order_id`)
    REFERENCES `orders` (`order_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_order_items_product`
    FOREIGN KEY (`product_id`)
    REFERENCES `products` (`product_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `chk_quantity_positive` CHECK (`quantity` > 0)
) ENGINE = InnoDB;
```

### 9. リバースエンジニアリング

既存のデータベースからER図を生成します。

1. Database → Reverse Engineer
2. 接続先を選択
3. スキーマを選択
4. テーブルを選択
5. ER図が自動生成される

### 10. テーブル定義書の出力

#### DBDoc Pluginのインストール

1. Scripting → Install Plugin/Module
2. DBDocプラグインをインストール
3. Plugins → DBDoc → Export Documentation
4. HTML/PDF形式でテーブル定義書を出力

### 11. データモデルのバージョン管理

#### MWBファイルのGit管理

1. .mwbファイルをGitリポジトリに追加
2. コミットメッセージ例: "Add orders table and foreign keys"

```bash
git add ec_site_db.mwb
git commit -m "Add orders table with customer foreign key"
git push
```

### 12. データベース設計書の作成

基本設計では、MySQL Workbenchで作成したER図を元に、詳細なテーブル定義書を作成します。

#### テーブル定義書の構成

**1. テーブル一覧**

| No. | テーブル名 | 論理名 | 説明 |
|-----|-----------|--------|------|
| 1 | customers | 顧客 | 顧客マスタ |
| 2 | products | 商品 | 商品マスタ |
| 3 | orders | 注文 | 注文ヘッダー |
| 4 | order_items | 注文明細 | 注文明細 |
| 5 | categories | カテゴリ | 商品カテゴリ |

**2. カラム定義（customersテーブル例）**

上記のカラム定義表を記載

**3. インデックス一覧**

上記のインデックス定義表を記載

**4. 外部キー制約一覧**

| 制約名 | テーブル | カラム | 参照テーブル | 参照カラム | ON DELETE | ON UPDATE |
|--------|---------|--------|------------|----------|-----------|-----------|
| fk_orders_customer | orders | customer_id | customers | customer_id | RESTRICT | CASCADE |

**5. ER図**

MySQL WorkbenchのER図を画像として添付

## 公式ドキュメント

- **公式サイト**: [MySQL Workbench](https://www.mysql.com/products/workbench/)
- **ユーザーマニュアル**: [MySQL Workbench Manual](https://dev.mysql.com/doc/workbench/en/)
- **データモデリング**: [Database Design and Modeling](https://dev.mysql.com/doc/workbench/en/wb-data-modeling.html)
- **Forward Engineering**: [Forward Engineering SQL Scripts](https://dev.mysql.com/doc/workbench/en/wb-forward-engineering-sql-scripts.html)

## 学習リソース

- **チュートリアル**: [MySQL Workbench Tutorial](https://www.mysqltutorial.org/mysql-workbench-tutorial/)
- **YouTube**: [MySQL Workbench Data Modeling](https://www.youtube.com/results?search_query=mysql+workbench+data+modeling)

## 関連リンク

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [正規化理論](https://ja.wikipedia.org/wiki/データベース正規化)
- [インデックス設計ベストプラクティス](https://dev.mysql.com/doc/refman/8.0/en/optimization-indexes.html)
