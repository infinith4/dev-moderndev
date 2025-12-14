# ArchiMate (Archi)

## 概要

**ArchiMate**は、エンタープライズアーキテクチャをモデリングするためのオープンスタンダード記法です。**Archi**は、ArchiMateをサポートする無料のオープンソースモデリングツールで、ビジネス、アプリケーション、テクノロジーの各層を統合的にモデル化します。

## 基本情報

### ArchiMate（記法）

| 項目 | 内容 |
|------|------|
| **策定団体** | The Open Group |
| **種別** | エンタープライズアーキテクチャモデリング言語 |
| **バージョン** | 3.2（最新） |
| **ライセンス** | オープンスタンダード |
| **料金** | 🟢 無料（仕様自体） |
| **公式サイト** | https://www.opengroup.org/archimate-forum |

### Archi（ツール）

| 項目 | 内容 |
|------|------|
| **開発元** | Phil Beauvoir / Archi Community |
| **種別** | ArchiMateモデリングツール |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://www.archimatetool.com/ |
| **ドキュメント** | https://www.archimatetool.com/user-guide/ |

## 主な特徴

### ArchiMate言語

#### 1. 3層アーキテクチャ
- **Business Layer**: ビジネスプロセス、組織、サービス
- **Application Layer**: アプリケーションコンポーネント、データ
- **Technology Layer**: インフラ、デバイス、ネットワーク

#### 2. アスペクト分類
- **Passive Structure**: データ、オブジェクト（何）
- **Behavior**: プロセス、サービス、機能（何を）
- **Active Structure**: アクター、コンポーネント（誰が）

#### 3. リレーションシップ
- Structural: Composition, Aggregation, Assignment
- Dependency: Serving, Access, Influence
- Dynamic: Flow, Triggering
- Other: Specialization, Realization

### Archiツール

#### 1. モデリング機能
- ドラッグ&ドロップで図を作成
- ArchiMate 3.2完全対応
- Viewpoint（視点）サポート

#### 2. エクスポート機能
- HTML Report生成
- 画像エクスポート（PNG、SVG）
- CSV、Open Exchange Format

#### 3. 拡張性
- jArchi（JavaScriptスクリプティング）
- プラグインエコシステム
- モデルリポジトリ連携

## 使い方

### Archiツールのインストール

```bash
# ダウンロード: https://www.archimatetool.com/download/

# Windows
# archi-windows-x64.zip を解凍して実行

# macOS
# Archi.app を /Applications にコピー

# Linux
wget https://www.archimatetool.com/downloads/archi/Archi-Linux64-5.2.0.tgz
tar -xzf Archi-Linux64-5.2.0.tgz
cd Archi-Linux64
./Archi
```

### 基本的なモデル作成

#### 1. ビジネスレイヤーモデル

**要素**:
- Business Actor（ビジネスアクター）: 顧客、従業員
- Business Role（ビジネスロール）: 営業担当、サポート担当
- Business Process（ビジネスプロセス）: 注文処理、在庫管理
- Business Service（ビジネスサービス）: 注文サービス

**例: ECサイトの注文プロセス**

```text
[顧客] --Serves--> [注文サービス]
        ^
        |
   Realizes
        |
[注文処理プロセス] --Assigned to--> [営業担当]
        |
   Accesses
        |
    [注文データ]
```

#### 2. アプリケーションレイヤーモデル

**要素**:
- Application Component（アプリケーションコンポーネント）: ECサイト、在庫管理システム
- Application Service（アプリケーションサービス）: 注文API
- Data Object（データオブジェクト）: 注文データ、顧客データ

**例: アプリケーション構成**

```text
[Webフロントエンド] --Serves--> [注文API]
                                    ^
                                    |
                               Realizes
                                    |
                        [バックエンドサービス]
                                    |
                               Accesses
                                    |
                              [注文データベース]
```

#### 3. テクノロジーレイヤーモデル

**要素**:
- Node（ノード）: Webサーバー、DBサーバー
- Device（デバイス）: ロードバランサー
- System Software（システムソフトウェア）: OS、DBMS
- Technology Service（テクノロジーサービス）: HTTP、JDBC

**例: インフラ構成**

```text
[ロードバランサー] --Serves--> [Webサーバークラスタ]
                                        |
                                   Accesses
                                        |
                                 [DBサーバー]
                                        |
                                   Realizes
                                        |
                                   [PostgreSQL]
```

### ビューポイント（Viewpoint）

#### Layered Viewpoint（レイヤードビュー）

```text
Business Layer:
  [顧客] -> [注文サービス] -> [注文プロセス]

Application Layer:
  [注文API] -> [バックエンド] -> [データベース]

Technology Layer:
  [Webサーバー] -> [アプリサーバー] -> [DBサーバー]
```

#### Application Usage Viewpoint

```text
# アプリケーション利用視点
[ビジネスプロセス]
    |
  Uses
    |
[アプリケーションサービス]
    |
Realizes
    |
[アプリケーションコンポーネント]
```

### jArchiスクリプト例

```javascript
// create_components.ajs
// Archi内でJavaScriptスクリプト実行

// モデル取得
var model = $("model");

// ビジネスプロセス作成
var process = model.createElement("business-process", "注文処理");

// アプリケーションコンポーネント作成
var app = model.createElement("application-component", "ECサイト");

// リレーションシップ作成
process.createRelationship("realization-relationship", app, "realizes");

console.log("コンポーネント作成完了");
```

### HTMLレポート生成

```bash
# Archi GUI操作
File → Export → HTML Report

# 設定:
- Include Views: すべてのビューを含める
- Include Model Elements: 要素リスト生成
- Style: デフォルトテンプレート
```

**生成されるHTML構造**:

```text
report/
├── index.html          # トップページ
├── css/
│   └── style.css
├── js/
│   └── scripts.js
├── images/
│   ├── view1.png
│   └── view2.png
└── model/
    ├── elements.html   # 要素一覧
    └── relations.html  # リレーション一覧
```

### CSV エクスポート/インポート

```bash
# CSV Export（Archi GUI）
File → Export → Model to CSV

# 生成されるCSV
elements.csv        # 要素一覧
properties.csv      # プロパティ
relationships.csv   # リレーション
```

```csv
# elements.csv例
"ID","Type","Name","Documentation"
"id-1","BusinessActor","顧客","ECサイト利用者"
"id-2","BusinessProcess","注文処理","顧客からの注文を処理"
"id-3","ApplicationComponent","ECサイト","Webベースの注文システム"

# relationships.csv例
"ID","Type","Source","Target"
"rel-1","Serving","id-2","id-1"
"rel-2","Realization","id-3","id-2"
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **企画** | ビジネスアーキテクチャ設計 | ビジネスプロセス・組織モデリング |
| **要件定義** | システム全体像設計 | ビジネス要求とシステムのマッピング |
| **基本設計** | アプリケーション/インフラ設計 | 3層モデルでの全体設計 |
| **実装** | アーキテクチャドキュメント | 実装時の参照アーキテクチャ |

## メリット

- **無料・オープンソース**: ツールもライセンスも無料
- **標準化**: The Open Group標準のモデリング言語
- **3層統合モデル**: ビジネス・アプリ・テクノロジーを統合的にモデル化
- **ビューポイント**: 目的別に異なる視点でモデル表示
- **HTMLレポート生成**: ドキュメント自動生成
- **スクリプティング**: jArchiでモデル操作自動化

## デメリット

- **学習曲線**: ArchiMate記法の習得が必要
- **複雑性**: 小規模プロジェクトにはオーバースペック
- **日本語情報少ない**: 日本語ドキュメント・コミュニティが少ない
- **リアルタイムコラボ不可**: ファイルベースで同時編集困難
- **プレゼン機能弱い**: PowerPointのようなプレゼン機能なし

## 類似ツールとの比較

| ツール | 記法 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Archi (ArchiMate)** | ArchiMate | 無料 | エンタープライズアーキテクチャ全体 |
| **Enterprise Architect** | UML, BPMN, ArchiMate | 有料 | エンタープライズモデリング |
| **Sparx EA** | UML, SysML, ArchiMate | 有料 | 大規模エンタープライズ |
| **Draw.io** | 自由形式 | 無料 | 汎用作図ツール |

## ベストプラクティス

### 1. レイヤーの分離

```text
# 良い例: レイヤーを明確に分離
Business Layer:
  - ビジネスプロセス
  - ビジネスサービス

Application Layer:
  - アプリケーションコンポーネント
  - アプリケーションサービス

Technology Layer:
  - サーバー
  - ネットワーク

# 悪い例: レイヤーが混在
すべての要素を1つのビューに配置
```

### 2. Viewpointの活用

```text
# 目的別にViewpointを使い分け
- Stakeholder Viewpoint: ステークホルダー向け全体像
- Application Structure: 開発者向けアプリ構成
- Technology Usage: インフラ担当向け技術スタック
```

### 3. プロパティの活用

```text
# 各要素にプロパティを追加
Business Process "注文処理":
  - Owner: 営業部
  - SLA: 24時間以内
  - Status: 稼働中

Application Component "ECサイト":
  - Version: 2.1.0
  - Technology: React + Node.js
  - Repository: https://github.com/...
```

### 4. バージョン管理

```bash
# Git でモデルファイルを管理
git add model.archimate
git commit -m "Add order processing architecture"

# Collaboration Plugin使用（有料）
# チーム全員でモデル共有
```

## 公式リソース

### ArchiMate
- **公式サイト**: https://www.opengroup.org/archimate-forum
- **仕様書**: https://pubs.opengroup.org/architecture/archimate3-doc/

### Archi
- **公式サイト**: https://www.archimatetool.com/
- **ユーザーガイド**: https://www.archimatetool.com/user-guide/
- **GitHub**: https://github.com/archimatetool/archi
- **フォーラム**: https://forum.archimatetool.com/

## まとめ

ArchiMateは、エンタープライズアーキテクチャを統合的にモデリングするための標準言語です。Archiツールを使用することで、無料でArchiMateモデリングが可能となり、ビジネス・アプリケーション・テクノロジーの3層を一貫したモデルで表現できます。大規模システムのアーキテクチャ設計やエンタープライズアーキテクチャ管理に最適です。

---

**最終更新**: 2025-12-06
**対象バージョン**: ArchiMate 3.2 / Archi 5.2+
