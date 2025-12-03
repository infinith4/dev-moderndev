# ERDPlus

## 概要

ERDPlusは、無料のオンラインER図（Entity-Relationship Diagram）作成ツールです。ブラウザでデータベース設計（概念モデル、論理モデル、物理モデル）、UMLクラス図、リレーショナルスキーマを作成し、PNG、PDF、SQL DDL出力をサポートします。学生、教育機関、小規模プロジェクトに適し、インストール不要、アカウント登録不要で利用できます。

## 主な機能

### 1. ER図モデリング
- **概念モデル**: エンティティ、関係、属性
- **論理モデル**: キー、カーディナリティ
- **物理モデル**: テーブル、カラム、データ型
- **リレーショナルスキーマ**: スキーマ表記

### 2. UML対応
- **クラス図**: クラス、継承、関連
- **シンプル**: 基本的なUMLのみ

### 3. 出力形式
- **PNG**: ラスター画像
- **PDF**: PDF出力
- **SQL DDL**: CREATE TABLE文生成
- **XML**: erdplus形式

### 4. ブラウザベース
- **オンライン**: インストール不要
- **保存**: ローカルストレージ
- **共有**: URLで共有（要アカウント）

### 5. 教育向け
- **シンプル**: 学習向けUI
- **無料**: 完全無料
- **チュートリアル**: 学習リソース

## 利用方法

### ER図作成

```
1. https://erdplus.com/ にアクセス
2. Start Modeling → ER Diagram
3. エンティティ作成:
   - Entity ツール → キャンバスクリック
   - 名前入力: Customer
4. 属性追加:
   - Attribute ツール → エンティティクリック
   - 属性名: CustomerID, Name, Email
5. 関係作成:
   - Relationship ツール
   - Customer ⇔ Order（1:N）
```

### SQL DDL生成

```
1. リレーショナルスキーマ表示
2. Export → SQL DDL
3. データベース選択:
   - MySQL
   - PostgreSQL
   - Oracle
4. ダウンロード: CREATE TABLE文
```

### SQL DDL出力例

```sql
-- ERDPlus生成SQL DDL (MySQL)

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255)
);

CREATE TABLE `Order` (
    OrderID INT PRIMARY KEY,
    OrderDate DATE,
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **ERDPlus** | 🟢 完全無料 | オンライン、無制限 |

## メリット

### ✅ 主な利点

1. **完全無料**: 制限なし
2. **インストール不要**: ブラウザのみ
3. **シンプル**: 初心者向けUI
4. **SQL DDL生成**: MySQL、PostgreSQL等
5. **ER図変換**: 概念→論理→物理
6. **教育向け**: 学習リソース充実
7. **PNG/PDF出力**: ドキュメント化
8. **UML対応**: クラス図作成
9. **軽量**: 高速動作
10. **アカウント不要**: すぐに利用可能

## デメリット

### ❌ 制約・課題

1. **機能限定**: 高度な機能なし
2. **オンライン専用**: オフライン不可
3. **コラボレーション**: リアルタイム共同編集なし
4. **バージョン管理**: Git統合なし
5. **カスタマイズ**: テンプレート少ない
6. **大規模図**: 複雑な図は不向き
7. **エクスポート**: フォーマット限定的
8. **商用**: エンタープライズ機能なし

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Lucidchart** | クラウド作図 | ERDPlusより高機能だが有料 |
| **dbdiagram.io** | オンラインDB設計 | ERDPlusと類似 |
| **MySQL Workbench** | MySQL公式 | ERDPlusより高機能 |
| **pgModeler** | PostgreSQL専用 | ERDPlusより高機能 |
| **draw.io** | 汎用作図 | ERDPlusより柔軟 |

## 公式リンク

- **公式サイト**: [https://erdplus.com/](https://erdplus.com/)
- **チュートリアル**: [https://erdplus.com/#/standalone](https://erdplus.com/#/standalone)

## 関連ドキュメント

- [データベース設計ツール一覧](../データベース設計ツール/)
- [pgModeler](./pgModeler.md)
- [データベース設計ベストプラクティス](../../best-practices/database-design.md)

---

**カテゴリ**: データベース設計ツール  
**対象工程**: 設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
