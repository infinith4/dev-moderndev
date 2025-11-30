# Draw.io（データベース論理設計）

## 概要

Draw.io（diagrams.net）は、完全無料のオンライン図作成ツールで、基本設計フェーズではデータベース論理ER図、テーブル関連図、データモデル図の作成に活用します。Entity-Relationshipモデルの視覚化、カーディナリティ表現、正規化の可視化が可能です。

### 基本設計フェーズでの活用

- **論理ER図**: エンティティ、属性、リレーションシップの詳細設計
- **テーブル関連図**: テーブル間の外部キー関係の可視化
- **カーディナリティ表現**: 1対1、1対多、多対多の関係表現
- **正規化の可視化**: 正規化前後のデータモデル比較
- **データディクショナリ**: テーブル・カラム定義表

### メリット・デメリット

**メリット**
- 完全無料で広告なし
- ER図専用のシェイプライブラリが充実
- Crow's Foot記法、IE記法、Chen記法に対応
- SVG/PNG/PDFエクスポート対応
- Google Drive統合でバージョン管理が容易

**デメリット**
- DDL自動生成機能がない
- リバースエンジニアリング非対応
- 大規模なER図の管理が困難

## 利用方法

### 1. Draw.ioへのアクセスとER図作成

1. [diagrams.net](https://www.diagrams.net/)にアクセス
2. 保存先を選択（Device、Google Drive、OneDrive等）
3. 「Create New Diagram」をクリック
4. テンプレートから「Software」→「Entity Relation」を選択

### 2. ERモデリングライブラリの有効化

1. 左パネルで「More Shapes...」をクリック
2. 以下のライブラリにチェック:
   - **Entity Relation**: ER図専用シェイプ
   - **Software / ER**: エンティティとリレーション
3. 「Apply」をクリック

### 3. 論理ER図の作成

#### 例: ECサイトのデータベース論理設計

**対象エンティティ:**
- Customer（顧客）
- Product（商品）
- Order（注文）
- OrderItem（注文明細）
- Category（カテゴリ）

#### Crow's Foot記法でのER図作成

**1. Customerエンティティの作成**

1. 左パネルの「Entity Relation」から「Entity」をキャンバスに配置
2. エンティティ名を入力: `Customer`
3. 属性を追加:

```
Customer
─────────────────
PK customer_id: INT
   email: VARCHAR(100)
   password_hash: VARCHAR(255)
   first_name: VARCHAR(50)
   last_name: VARCHAR(50)
   phone: VARCHAR(20)
   address: VARCHAR(200)
   created_at: TIMESTAMP
```

**属性の表記:**
- **PK**: Primary Key（主キー）
- **FK**: Foreign Key（外部キー）
- **データ型**: VARCHAR、INT、DECIMAL、TIMESTAMP等

**2. Productエンティティの作成**

```
Product
─────────────────
PK product_id: INT
FK category_id: INT
   product_name: VARCHAR(200)
   description: TEXT
   price: DECIMAL(10,2)
   stock_quantity: INT
   is_active: TINYINT(1)
   created_at: TIMESTAMP
```

**3. Orderエンティティの作成**

```
Order
─────────────────
PK order_id: INT
FK customer_id: INT
   order_date: TIMESTAMP
   status: ENUM
   total_amount: DECIMAL(10,2)
   shipping_address: VARCHAR(200)
   created_at: TIMESTAMP
```

**4. OrderItemエンティティの作成**

```
OrderItem
─────────────────
PK order_item_id: INT
FK order_id: INT
FK product_id: INT
   quantity: INT
   unit_price: DECIMAL(10,2)
   subtotal: DECIMAL(10,2)
```

**5. Categoryエンティティの作成**

```
Category
─────────────────
PK category_id: INT
FK parent_category_id: INT
   category_name: VARCHAR(100)
   description: TEXT
```

### 4. リレーションシップの設定

#### Crow's Foot記法での関連付け

**1対多リレーション（Customer - Order）**

1. 「Entity Relation」から「Many to One」アイコンを選択
2. `Order` エンティティをクリック（Many側）
3. `Customer` エンティティをクリック（One側）
4. リレーションシップが接続される

**カーディナリティの表記:**
- **1 (One)**: 単一線
- **多 (Many)**: Crow's Foot（カラスの足）記号

**関連付け一覧:**

| 多側（子） | 1側（親） | リレーション名 |
|-----------|----------|--------------|
| Order | Customer | Customer_places_Order |
| OrderItem | Order | Order_contains_OrderItem |
| OrderItem | Product | Product_ordered_in_OrderItem |
| Product | Category | Category_contains_Product |
| Category | Category（自己参照） | parent_child_category |

**リレーションシップのラベル追加:**

1. リレーションシップの線をダブルクリック
2. ラベルを追加（例: "places"、"contains"）
3. カーディナリティを表示（例: "1", "0..N"）

### 5. カーディナリティの詳細設定

#### 最小・最大カーディナリティの表記

**例: Customer - Order（1対多、オプショナル）**

```
Customer (1,1) ─────< (0,N) Order
```

- Customer: 必ず1件存在（1,1）
- Order: 0件以上存在可能（0,N）

**Draw.ioでの設定:**

1. リレーションシップの線を選択
2. 右パネルの「Style」で線のスタイルを調整
3. テキストボックスを追加してカーディナリティを表記

### 6. 属性の詳細定義

#### テーブル形式での属性定義

**Productエンティティの属性詳細:**

| 属性名 | データ型 | 桁数 | NULL許可 | デフォルト | 制約 | 備考 |
|--------|---------|------|---------|----------|------|------|
| product_id | INT | - | NO | AUTO_INCREMENT | PK | 主キー |
| category_id | INT | - | YES | NULL | FK | 外部キー→Category |
| product_name | VARCHAR | 200 | NO | - | NOT NULL | - |
| price | DECIMAL | 10,2 | NO | - | CHECK >= 0 | 価格 |
| stock_quantity | INT | - | NO | 0 | CHECK >= 0 | 在庫数 |

**Draw.ioでのテーブル作成:**

1. 「General」から「Table」を選択
2. 行・列数を設定（7行 x 7列）
3. 上記の属性詳細を入力
4. エンティティの横に配置

### 7. 正規化の可視化

#### 非正規形から第3正規形への変換

**非正規形（注文データ）**

```
Order (非正規形)
─────────────────
order_id
customer_name
customer_email
products: [
  {product_name, quantity, unit_price},
  {product_name, quantity, unit_price}
]
```

**第1正規形（繰り返しグループを排除）**

```
Order               OrderProduct
─────────────       ─────────────────
order_id            order_id
customer_name       product_name
customer_email      quantity
                    unit_price
```

**第2正規形（部分関数従属を排除）**

```
Order               Customer           OrderProduct
─────────────       ─────────────      ─────────────────
order_id            customer_id        order_id
customer_id         customer_name      product_name
                    customer_email     quantity
                                       unit_price
```

**第3正規形（推移的関数従属を排除）**

```
Order               Customer           OrderProduct         Product
─────────────       ─────────────      ─────────────────    ─────────────
order_id            customer_id        order_id             product_id
customer_id         customer_name      product_id           product_name
                    customer_email     quantity             unit_price
                                       unit_price
```

**Draw.ioでの表現:**

1. 各正規形のエンティティを横に並べて配置
2. 矢印で変換フローを示す
3. 削除された属性を赤字で表示
4. 追加された外部キーを緑字で表示

### 8. 多対多リレーションの解消

#### 中間テーブルの作成

**多対多リレーション:**

```
Student ←────→ Course
```

**中間テーブル（Enrollment）を使用:**

```
Student (1) ─────< (N) Enrollment (N) >───── (1) Course
```

**Enrollmentテーブル:**

```
Enrollment
─────────────────
PK enrollment_id: INT
FK student_id: INT
FK course_id: INT
   enrolled_date: DATE
   grade: VARCHAR(2)
```

### 9. 自己参照リレーションシップ

#### 例: Categoryテーブルの階層構造

```
Category
─────────────────
PK category_id: INT
FK parent_category_id: INT
   category_name: VARCHAR(100)
```

**Draw.ioでの表現:**

1. `Category` エンティティを配置
2. `parent_category_id` から `category_id` へリレーションシップを作成
3. ループバック（自己参照）の矢印を描画
4. ラベル: "parent-child"

### 10. インデックス設計の可視化

#### インデックス定義の表

**Orderテーブルのインデックス:**

| インデックス名 | カラム | タイプ | カーディナリティ | 目的 |
|--------------|--------|--------|----------------|------|
| PRIMARY | order_id | PRIMARY KEY | Unique | 主キー |
| idx_customer_id | customer_id | INDEX | Non-unique | 顧客別検索 |
| idx_order_date | order_date | INDEX | Non-unique | 日付検索 |
| idx_status | status | INDEX | Non-unique | ステータス検索 |

**Draw.ioでのテーブル配置:**

エンティティの下にインデックス定義表を配置

### 11. 制約定義の可視化

#### CHECK制約、UNIQUE制約の表示

**Productエンティティの制約:**

```
Product
─────────────────
PK product_id: INT
   product_name: VARCHAR(200) UNIQUE
   price: DECIMAL(10,2) CHECK >= 0
   stock_quantity: INT CHECK >= 0
```

**テキストボックスで制約を追加:**

1. エンティティの横にテキストボックスを配置
2. 制約内容を記載:

```
【制約】
- UNIQUE: product_name
- CHECK: price >= 0
- CHECK: stock_quantity >= 0
```

### 12. データディクショナリの作成

#### テーブル定義一覧

**全テーブルのサマリー:**

| No. | テーブル名 | 論理名 | 主キー | 外部キー | 説明 |
|-----|-----------|--------|--------|---------|------|
| 1 | Customer | 顧客 | customer_id | - | 顧客マスタ |
| 2 | Product | 商品 | product_id | category_id | 商品マスタ |
| 3 | Order | 注文 | order_id | customer_id | 注文ヘッダー |
| 4 | OrderItem | 注文明細 | order_item_id | order_id, product_id | 注文明細 |
| 5 | Category | カテゴリ | category_id | parent_category_id | 商品カテゴリ |

**Draw.ioでのテーブル作成:**

ER図とは別のページにデータディクショナリを作成

### 13. ER図のレイアウト

#### 読みやすい配置

**レイアウトのベストプラクティス:**

1. **階層配置**: 親テーブルを上、子テーブルを下に配置
2. **左から右**: データフローに沿って配置
3. **グループ化**: 関連するテーブルをグループ化
4. **色分け**: マスタテーブル（青）、トランザクションテーブル（緑）

**例: ECサイトER図の配置**

```
┌─────────────┐         ┌─────────────┐
│  Customer   │         │  Category   │
└─────────────┘         └─────────────┘
       │                       │
       │                       │
       ↓                       ↓
┌─────────────┐         ┌─────────────┐
│    Order    │         │   Product   │
└─────────────┘         └─────────────┘
       │                       │
       │                       │
       └───────┬───────────────┘
               ↓
       ┌─────────────┐
       │  OrderItem  │
       └─────────────┘
```

### 14. IE記法（Information Engineering）での表現

#### IE記法の特徴

- **実線**: 必須リレーション
- **破線**: オプショナルリレーション
- **●**: 多（Many）
- **│**: 1（One）

**例: Customer - Order（IE記法）**

```
Customer ─────●< Order
（1側）        （多側）
```

**Draw.ioでのIE記法:**

1. リレーションシップの線種を変更
2. 「Entity Relation」ライブラリから「IE Relation」を使用

### 15. エクスポートとドキュメント化

#### PNG/PDF/SVGエクスポート

1. File → Export as → 形式を選択
2. **PNG**: ドキュメント添付用（300dpi推奨）
3. **PDF**: 設計書統合用
4. **SVG**: 拡大縮小可能なベクター形式

#### Git統合

```bash
git add ec_site_db_erd.drawio
git commit -m "Add Order and OrderItem entities with foreign keys"
git push
```

### 16. データベース設計書への統合

#### 設計書の構成

**1. 論理ER図（Draw.io）**

- ER図をPNG/PDFでエクスポート
- 設計書に添付

**2. テーブル定義一覧**

- データディクショナリをExcelまたはMarkdownで作成

**3. カラム定義（各テーブル）**

- 属性詳細表を設計書に記載

**4. リレーションシップ一覧**

| 子テーブル | 子カラム | 親テーブル | 親カラム | カーディナリティ | ON DELETE | ON UPDATE |
|-----------|---------|-----------|---------|----------------|-----------|-----------|
| Order | customer_id | Customer | customer_id | 1:N | RESTRICT | CASCADE |
| OrderItem | order_id | Order | order_id | 1:N | CASCADE | CASCADE |

### 17. ER図のバージョン管理

#### バージョン履歴の管理

1. Google Driveに保存
2. ファイル名に日付を含める（例: `ec_site_db_erd_20250115.drawio`）
3. 変更履歴をコメントに記載
4. 主要なバージョンをタグ付け

## 公式ドキュメント

- **公式サイト**: [diagrams.net](https://www.diagrams.net/)
- **ER図ガイド**: [Entity Relationship Diagrams](https://www.drawio.com/blog/entity-relationship-diagrams)
- **データベース設計**: [Database Design with draw.io](https://www.drawio.com/blog/database-design)

## 学習リソース

- **ER図チュートリアル**: [ER Diagram Tutorial](https://www.youtube.com/results?search_query=drawio+er+diagram)
- **Crow's Foot記法**: [Crow's Foot Notation](https://vertabelo.com/blog/crow-s-foot-notation/)
- **正規化理論**: [Database Normalization](https://www.studytonight.com/dbms/database-normalization.php)

## 関連リンク

- [MySQL Workbench](https://www.mysql.com/products/workbench/)（MySQL公式モデリングツール）
- [ERDPlus](https://erdplus.com/)（オンラインER図ツール）
- [dbdiagram.io](https://dbdiagram.io/)（コードベースER図ツール）

## 関連ドキュメント

このツールは他の開発工程でも使用されます：

- [要件定義/業務分析でのDraw.io](../../../開発工程_2_要件定義/2_業務分析/Draw.io/Draw.io.md) - BPMNプロセス図作成
- [要件定義/ユースケース分析でのDraw.io](../../../開発工程_2_要件定義/3_ユースケース分析（機能要件定義）/Draw.io/Draw.io.md) - ユースケース図作成
- [要件定義/システム方針検討でのDraw.io](../../../開発工程_2_要件定義/10_システム方針検討（機能要件定義）/Draw.io/Draw.io.md) - システム構成図作成
- [基本設計（アプリケーション）/画面設計でのDraw.io](../2_画面設計/Draw.io/Draw.io.md) - ワイヤーフレーム、画面遷移図
- [基本設計（アプリケーション）/バッチ設計でのDraw.io](../7_バッチ設計/Draw.io/Draw.io.md) - バッチ処理フロー図
- [基本設計（インフラ）/ネットワーク構成図でのDraw.io](../../../開発工程_4_基本設計_インフラ/1_ネットワーク構成図/Draw.io/Draw.io.md) - ネットワーク構成図、VLAN設計

全ツールの一覧については[ツール索引](../../../ツール索引.md)を参照してください。
