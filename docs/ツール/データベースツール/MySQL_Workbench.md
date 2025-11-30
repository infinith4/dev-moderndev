# MySQL Workbench

## 概要

MySQL Workbenchは、MySQL公式の統合開発環境（IDE）で、ER図作成、データベース設計、SQL開発、サーバー管理など、MySQLに関するすべての作業を一元管理できます。概念モデリングから論理設計、物理設計まで、フォワードエンジニアリング（ER図からDDL生成）とリバースエンジニアリング（既存DBからER図生成）の両方に対応しています。

### 主な特徴

- **完全無料**: オープンソースで無料（GPL v2ライセンス）
- **MySQL統合**: MySQLとの完全な統合
- **フォワード/リバースエンジニアリング**: ER図⇔DDLの双方向変換
- **SQL自動生成**: ER図から高品質なDDLを自動生成
- **クロスプラットフォーム**: Windows、macOS、Linux対応
- **詳細設計機能**: データ型、インデックス、外部キー、制約の詳細設定

### 料金プラン

- **完全無料**: オープンソース（GPLライセンス）

### メリット・デメリット

**メリット**
- 完全無料でオープンソース
- MySQLとの完全統合により、シームレスなデータベース開発が可能
- フォワードエンジニアリング（モデル→DB）とリバースエンジニアリング（DB→モデル）
- SQL自動生成が高品質
- クロスプラットフォーム対応
- ER図から直接SQLを生成可能
- データ型、インデックス、外部キーの詳細設定が可能

**デメリット**
- MySQL専用（PostgreSQL、Oracle等には非対応）
- 概念モデリングはやや弱い（物理モデル寄り）
- 複数人での同時編集が困難
- バージョン管理がファイルベースで制限的
- UI改善の余地あり
- 学習曲線がやや急

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| 要件定義/概念モデリング | 概念ER図作成、エンティティ抽出、リレーションシップ定義 | 概念ER図、エンティティ定義書 |
| 基本設計/データベース論理設計 | 論理ER図作成、テーブル定義、カラム定義、正規化、インデックス設計 | 論理ER図、テーブル定義書、DDL |

## 基本的な利用方法

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

### 4. リレーションシップの設定

#### 外部キーの作成

**方法1: 視覚的な接続**
1. 左側ツールバーから「Place a Relationship」アイコンをクリック
2. 関係タイプを選択:
   - **1:n Non-Identifying**: 1対多（非識別関係）
   - **1:1 Non-Identifying**: 1対1（非識別関係）
   - **n:m Identifying**: 多対多（識別関係、中間テーブル自動生成）
3. 親テーブルをクリック
4. 子テーブルをクリック
5. 自動的に外部キーが設定される

**方法2: 手動設定**
1. 子テーブルをダブルクリック
2. 「Foreign Keys」タブを選択
3. 外部キー制約を手動で定義

### 5. SQL生成（フォワードエンジニアリング）

1. 「Database」→「Forward Engineer」を選択
2. 接続先のMySQLサーバーを選択（またはスキップしてSQLファイル出力）
3. 生成オプションを選択:
   - DROP文を含める
   - CREATE TABLE文を生成
   - INSERT文を含める（サンプルデータがあれば）
4. 「Execute」をクリック
5. DDL（CREATE TABLE文）が自動生成される

### 6. リバースエンジニアリング

既存のデータベースからER図を生成:

1. 「Database」→「Reverse Engineer」を選択
2. MySQLサーバーに接続
3. 対象データベースを選択
4. 対象テーブルを選択
5. 「Execute」をクリック
6. ER図が自動生成される

## 工程別の活用方法

### 要件定義/概念モデリングでの活用

概念モデリングフェーズでは、ビジネス要件から主要なエンティティとリレーションシップを抽出します。

#### 概念ER図の作成

**例: ECサイトの概念ER図**

**主要エンティティ:**
- 顧客（Customer）
- 商品（Product）
- 注文（Order）
- カテゴリ（Category）

**リレーションシップ:**
- 顧客 ─ 注文（1:多）
- 注文 ─ 商品（多:多、注文明細で解決）
- カテゴリ ─ 商品（1:多）

**作成手順:**

1. File → New Model → Add Diagram
2. テーブルを配置（上記のエンティティ）
3. 各テーブルの主要属性を定義（詳細は後回し）

**Customer（顧客）エンティティ:**
- customer_id（主キー）
- customer_name
- email
- phone
- address

**Product（商品）エンティティ:**
- product_id（主キー）
- product_name
- category_id（外部キー）
- price
- stock_quantity

**Order（注文）エンティティ:**
- order_id（主キー）
- customer_id（外部キー）
- order_date
- total_amount

**Category（カテゴリ）エンティティ:**
- category_id（主キー）
- category_name

**リレーションシップの作成:**

1. 「Place a Relationship」を選択
2. 1:n Non-Identifyingを選択
3. Customer → Order（顧客は複数の注文を持つ）
4. Category → Product（カテゴリは複数の商品を持つ）

**多対多の解決:**

注文と商品は多対多関係のため、中間テーブル「order_items（注文明細）」を作成:

1. 「Place a Relationship」→「n:m Identifying」を選択
2. Order → Product
3. 自動的に「order_items」中間テーブルが生成される

**カーディナリティの記載:**

各リレーションシップをダブルクリックして、カーディナリティを記載:
- Customer → Order: 1:∞（顧客は0個以上の注文を持つ）
- Category → Product: 1:∞（カテゴリは0個以上の商品を持つ）

### 基本設計/データベース論理設計での活用

論理設計フェーズでは、概念ER図を詳細化し、テーブル定義、カラム定義、制約、インデックスを設計します。

#### 論理ER図の作成

**例: ECサイトのデータベース論理設計**

**1. customersテーブルの作成**

テーブルをダブルクリックして詳細設定:

**カラム定義:**

| カラム名 | データ型 | 桁数 | NULL許可 | デフォルト | 制約 | 備考 |
|---------|---------|------|---------|----------|------|------|
| customer_id | INT | - | NO | AUTO_INCREMENT | PK | 主キー |
| email | VARCHAR | 100 | NO | - | UNIQUE | メールアドレス |
| password_hash | VARCHAR | 255 | NO | - | - | パスワードハッシュ |
| first_name | VARCHAR | 50 | NO | - | - | 名 |
| last_name | VARCHAR | 50 | NO | - | - | 姓 |
| phone | VARCHAR | 20 | YES | NULL | - | 電話番号 |
| address | VARCHAR | 200 | YES | NULL | - | 住所 |
| city | VARCHAR | 50 | YES | NULL | - | 市区町村 |
| postal_code | VARCHAR | 10 | YES | NULL | - | 郵便番号 |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | 作成日時 |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP ON UPDATE | - | 更新日時 |

**設定手順:**

1. 「Columns」タブで各カラムを追加
2. PK（主キー）にチェック: `customer_id`
3. NN（NOT NULL）にチェック: 必須項目
4. UQ（UNIQUE）にチェック: `email`
5. AI（AUTO_INCREMENT）にチェック: `customer_id`
6. Default値を設定: `created_at`, `updated_at`

**2. インデックスの設計**

1. テーブルをダブルクリック
2. 「Indexes」タブを選択
3. 「Add」をクリックしてインデックスを追加

**customersテーブルのインデックス:**

| インデックス名 | カラム | タイプ | 目的 |
|-------------|-------|-------|------|
| idx_email | email | UNIQUE | メールアドレスでの検索高速化 |
| idx_name | last_name, first_name | INDEX | 氏名での検索高速化 |
| idx_created_at | created_at | INDEX | 登録日時での絞り込み |

**3. 外部キー制約の詳細設定**

1. 子テーブル（例: orders）をダブルクリック
2. 「Foreign Keys」タブを選択
3. 外部キー名を入力: `fk_orders_customer_id`
4. Referenced Table: `customers`
5. カラムマッピング:
   - orders.customer_id → customers.customer_id
6. 参照整合性アクション:
   - **ON UPDATE**: CASCADE（親の更新を反映）
   - **ON DELETE**: RESTRICT（子が存在する場合は削除不可）

**4. 正規化の実施**

**第1正規形（1NF）:**
- 繰り返し項目を排除
- 各カラムは原子値（atomic value）

**第2正規形（2NF）:**
- 部分関数従属を排除
- 主キー全体に従属

**第3正規形（3NF）:**
- 推移的関数従属を排除
- 非キー属性は主キーのみに従属

**例: 住所の正規化**

顧客テーブルに住所フィールドがある場合、都道府県、市区町村、番地に分割:

Before:
```
customers
- address: "東京都渋谷区道玄坂1-2-3"
```

After (3NF):
```
customers
- prefecture_id (FK)
- city
- address_line

prefectures
- prefecture_id (PK)
- prefecture_name
```

**5. テーブル定義書の出力**

1. File → Export → Forward Engineer SQL CREATE Script
2. 出力先を選択
3. DDLが生成される

**生成されるDDL例:**

```sql
CREATE TABLE customers (
  customer_id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  address VARCHAR(200),
  city VARCHAR(50),
  postal_code VARCHAR(10),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (customer_id),
  UNIQUE KEY idx_email (email),
  KEY idx_name (last_name, first_name),
  KEY idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE orders (
  order_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(10,2) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  PRIMARY KEY (order_id),
  KEY idx_customer_id (customer_id),
  KEY idx_order_date (order_date),
  CONSTRAINT fk_orders_customer_id FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### ER図のエクスポート

1. File → Export → Export as PNG（画像形式）
2. File → Export → Export as SQL CREATE Script（DDL）
3. File → Export → Export as PDF（ドキュメント形式）

## 公式ドキュメント

- **公式サイト**: [MySQL Workbench](https://www.mysql.com/products/workbench/)
- **ダウンロード**: [MySQL Workbench Downloads](https://dev.mysql.com/downloads/workbench/)
- **公式マニュアル**: [MySQL Workbench Manual](https://dev.mysql.com/doc/workbench/en/)
- **データモデリングガイド**: [Data Modeling](https://dev.mysql.com/doc/workbench/en/wb-data-modeling.html)
- **フォワードエンジニアリング**: [Forward Engineering](https://dev.mysql.com/doc/workbench/en/wb-forward-engineering.html)
- **リバースエンジニアリング**: [Reverse Engineering](https://dev.mysql.com/doc/workbench/en/wb-reverse-engineering.html)

## 学習リソース

- **MySQL Workbench Tutorial**: [Official Tutorial](https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial.html)
- **ER図作成ガイド**: [Creating an EER Diagram](https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial-creating-a-model.html)

## 関連リンク

- [MySQL公式サイト](https://www.mysql.com/)
- [phpMyAdmin](https://www.phpmyadmin.net/)（Webベースの管理ツール）
- [DBeaver](https://dbeaver.io/)（汎用DBツール）
- [ERDPlus](https://erdplus.com/)（オンラインER図ツール）
- [dbdiagram.io](https://dbdiagram.io/)（シンプルなER図ツール）
