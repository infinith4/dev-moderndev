# C4 Model

## 概要

C4 Modelは、Simon Brown氏が提唱したソフトウェアアーキテクチャ図作成フレームワークです。4つの抽象度レベル（Context、Container、Component、Code）で段階的にシステムを可視化し、ステークホルダーごとに適切な詳細度でアーキテクチャを説明します。PlantUML、Structurizr、diagrams.net等のツールで図を作成し、ドキュメント化、コミュニケーション、設計レビューを支援します。

## 主な機能

### 1. 4つの抽象度レベル
- **Level 1: System Context**: システム全体と外部依存関係
- **Level 2: Container**: システム内のコンテナ（アプリ、DB等）
- **Level 3: Component**: コンテナ内のコンポーネント
- **Level 4: Code**: クラス図、UML（オプション）

### 2. 対象者別
- **Context**: 経営層、プロジェクトマネージャー
- **Container**: アーキテクト、運用チーム
- **Component**: 開発者、アーキテクト
- **Code**: 開発者

### 3. 要素
- **Person**: ユーザー、外部システムの人
- **Software System**: ソフトウェアシステム
- **Container**: 実行可能単位（Webアプリ、DB、モバイルアプリ等）
- **Component**: コードのグループ（サービス、リポジトリ等）

### 4. ツール統合
- **PlantUML**: C4-PlantUML
- **Structurizr**: 公式ツール
- **diagrams.net (draw.io)**: C4テンプレート
- **Mermaid**: C4図対応

## 利用方法

### Level 1: System Context図

```
[概要]
システム全体とユーザー、外部システムとの関係を表示

[例: ECサイト]
- Person: Customer
- Software System: E-commerce System
- External System: Payment Gateway, Email Service
```

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(customer, "Customer", "オンラインショッピングユーザー")
System(ecommerce, "E-commerce System", "商品閲覧・購入")
System_Ext(payment, "Payment Gateway", "決済処理")
System_Ext(email, "Email Service", "メール送信")

Rel(customer, ecommerce, "商品閲覧・購入", "HTTPS")
Rel(ecommerce, payment, "決済処理", "API")
Rel(ecommerce, email, "注文確認メール", "SMTP")

@enduml
```

### Level 2: Container図

```
[概要]
システム内のコンテナ（実行単位）とその関係を表示

[例: ECサイトのコンテナ]
- Web Application (React)
- Mobile App (React Native)
- API Application (Node.js)
- Database (PostgreSQL)
- Cache (Redis)
```

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(customer, "Customer")

System_Boundary(ecommerce, "E-commerce System") {
    Container(web, "Web Application", "React", "顧客向けWebアプリ")
    Container(mobile, "Mobile App", "React Native", "顧客向けモバイルアプリ")
    Container(api, "API Application", "Node.js", "ビジネスロジック、REST API")
    ContainerDb(db, "Database", "PostgreSQL", "商品、注文、顧客情報")
    ContainerDb(cache, "Cache", "Redis", "セッション、キャッシュ")
}

System_Ext(payment, "Payment Gateway")

Rel(customer, web, "使用", "HTTPS")
Rel(customer, mobile, "使用", "HTTPS")
Rel(web, api, "API呼び出し", "JSON/HTTPS")
Rel(mobile, api, "API呼び出し", "JSON/HTTPS")
Rel(api, db, "読み書き", "SQL/TCP")
Rel(api, cache, "読み書き", "Redis Protocol")
Rel(api, payment, "決済処理", "HTTPS")

@enduml
```

### Level 3: Component図

```
[概要]
コンテナ内のコンポーネント（コードのグループ）とその関係を表示

[例: API Applicationのコンポーネント]
- Product Controller
- Order Controller
- Product Service
- Order Service
- Product Repository
- Order Repository
```

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

Container(web, "Web Application", "React")
ContainerDb(db, "Database", "PostgreSQL")

Container_Boundary(api, "API Application") {
    Component(productCtrl, "Product Controller", "Express Router", "商品API")
    Component(orderCtrl, "Order Controller", "Express Router", "注文API")
    Component(productSvc, "Product Service", "Service", "商品ビジネスロジック")
    Component(orderSvc, "Order Service", "Service", "注文ビジネスロジック")
    Component(productRepo, "Product Repository", "Repository", "商品データアクセス")
    Component(orderRepo, "Order Repository", "Repository", "注文データアクセス")
}

Rel(web, productCtrl, "商品取得", "JSON/HTTPS")
Rel(web, orderCtrl, "注文作成", "JSON/HTTPS")
Rel(productCtrl, productSvc, "使用")
Rel(orderCtrl, orderSvc, "使用")
Rel(productSvc, productRepo, "使用")
Rel(orderSvc, orderRepo, "使用")
Rel(productRepo, db, "読み書き", "SQL")
Rel(orderRepo, db, "読み書き", "SQL")

@enduml
```

### Structurizr DSL

```
workspace {
    model {
        customer = person "Customer" "オンラインショッピングユーザー"
        
        ecommerce = softwareSystem "E-commerce System" {
            web = container "Web Application" "React" "顧客向けWebアプリ"
            api = container "API Application" "Node.js" {
                productCtrl = component "Product Controller"
                productSvc = component "Product Service"
                productRepo = component "Product Repository"
            }
            db = container "Database" "PostgreSQL"
        }
        
        payment = softwareSystem "Payment Gateway" "External"
        
        customer -> web "使用"
        web -> api "API呼び出し"
        api -> db "読み書き"
        api -> payment "決済処理"
        
        productCtrl -> productSvc "使用"
        productSvc -> productRepo "使用"
    }
    
    views {
        systemContext ecommerce {
            include *
            autolayout lr
        }
        
        container ecommerce {
            include *
            autolayout lr
        }
        
        component api {
            include *
            autolayout lr
        }
    }
}
```

### diagrams.net (draw.io)

```
1. diagrams.net にアクセス
2. File → Open Library → URL
3. C4テンプレート:
   https://github.com/plantuml-stdlib/C4-PlantUML/raw/master/samples/C4_Context%20Diagram%20Sample%20-%20bigbankplc.puml
4. Context図作成:
   - Person (顧客)
   - System (ECサイト)
   - External System (決済、メール)
5. 関係線追加
6. Export → PNG/PDF
```

## エディション・料金

| ツール | 価格 | 特徴 |
|--------|------|------|
| **C4 Model (フレームワーク)** | 🟢 完全無料 | コンセプト、無料 |
| **PlantUML + C4-PlantUML** | 🟢 完全無料 | オープンソース |
| **Structurizr Lite** | 🟢 無料 | ローカル実行 |
| **Structurizr Cloud** | 💰 $7.50/月 | クラウド版 |
| **diagrams.net** | 🟢 完全無料 | オンライン、無料 |

## メリット

### ✅ 主な利点

1. **段階的詳細化**: 4レベルで適切な粒度
2. **対象者別**: ステークホルダーごとに最適な図
3. **シンプル**: 覚えやすいコンセプト
4. **ツール豊富**: PlantUML、Structurizr、draw.io対応
5. **コミュニケーション**: 技術・非技術者間
6. **標準化**: チーム内統一表記
7. **スケーラブル**: 小規模～大規模システム対応
8. **バージョン管理**: テキストベースで Git管理可能
9. **ドキュメント**: アーキテクチャドキュメント化
10. **無料**: フレームワーク自体無料

## デメリット

### ❌ 制約・課題

1. **学習曲線**: コンセプト理解必要
2. **ツール**: PlantUML等の習得必要
3. **大規模システム**: Component図が複雑化
4. **動的側面**: シーケンス図は別途必要
5. **標準外**: UML等の既存標準ではない
6. **ツールバラバラ**: 統一ツールなし
7. **保守**: 図の更新が煩雑
8. **自動化**: コードから自動生成が限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **UML** | 標準モデリング言語 | C4 Modelよりコミュニケーション弱い |
| **ArchiMate** | エンタープライズアーキテクチャ | C4 Modelより複雑 |
| **4+1 View** | ソフトウェアアーキテクチャビュー | C4 Modelと類似 |
| **Arc42** | アーキテクチャドキュメント | C4 Modelより包括的 |
| **Lucidchart** | 汎用作図 | C4 Modelよりビジュアル |

## 公式リンク

- **公式サイト**: [https://c4model.com/](https://c4model.com/)
- **C4-PlantUML**: [https://github.com/plantuml-stdlib/C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML)
- **Structurizr**: [https://structurizr.com/](https://structurizr.com/)
- **書籍**: [https://leanpub.com/visualising-software-architecture](https://leanpub.com/visualising-software-architecture)

## 関連ドキュメント

- [アーキテクチャツール一覧](../アーキテクチャツール/)
- [PlantUML](../作図ツール/PlantUML.md)
- [Mermaid](../作図ツール/Mermaid.md)
- [アーキテクチャ設計ベストプラクティス](../../best-practices/architecture-design.md)

---

**カテゴリ**: アーキテクチャツール  
**対象工程**: 設計、ドキュメント作成  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
