# Draw.io（システム構成図作成）

## 概要

Draw.io（diagrams.net）は、完全無料のオンライン図作成ツールで、システム構成図、ネットワーク図、アーキテクチャ図の作成に対応しています。AWS、Azure、GCPのアイコンライブラリが充実しており、クラウドアーキテクチャの設計に最適です。

### 主な特徴

- **完全無料**: すべての機能が無料
- **オープンソース**: ソースコードが公開
- **AWS/Azureアイコン**: クラウドサービスの公式アイコンを標準装備
- **Google Drive統合**: ファイル管理が容易
- **軽量**: ブラウザで軽快に動作

### メリット・デメリット

**メリット**
- 完全無料で広告なし
- AWS、Azure、GCPの公式アイコンライブラリが充実
- Google Drive、OneDriveとの統合でファイル管理が容易
- オフライン利用も可能（デスクトップ版）
- 軽量で動作が速い

**デメリット**
- リアルタイム協業機能が弱い
- テンプレートが他のツールに比べて少ない
- UIがやや古め

## 利用方法

### 1. アクセスと保存先選択

1. [diagrams.net](https://www.diagrams.net/)にアクセス
2. 保存先を選択:
   - **Device**: ローカルストレージ
   - **Google Drive**: Googleドライブ
   - **OneDrive**: OneDrive

### 2. クラウドアイコンライブラリの有効化

1. 左側パネルで「More Shapes...」をクリック
2. 以下のライブラリを有効化:
   - **AWS19**: AWSアーキテクチャアイコン
   - **Azure**: Microsoft Azureアイコン
   - **GCP**: Google Cloud Platformアイコン
   - **Network**: ネットワーク機器アイコン
3. 「Apply」をクリック

### 3. システム構成図の作成

#### 例: AWSを使用した3層Webアプリケーション

**アーキテクチャ構成**
- フロントエンド: CloudFront + S3
- アプリケーション層: ALB + EC2 (Auto Scaling)
- データベース層: RDS (Multi-AZ)

#### 作成手順

**1. VPCの配置**

1. 左パネルの「AWS19」ライブラリから「VPC」を検索
2. 「VPC」アイコンをキャンバスにドラッグ
3. サイズを調整して、内部にリソースを配置できるようにする
4. VPC名をラベルに追加（例: "production-vpc"）

**2. パブリックサブネットとプライベートサブネットの配置**

1. VPC内に矩形を2つ配置（「General」ライブラリから「Rectangle」）
2. 1つ目: パブリックサブネット（背景色: 薄い緑）
3. 2つ目: プライベートサブネット（背景色: 薄い青）
4. ラベルを追加:
   - "Public Subnet (10.0.1.0/24)"
   - "Private Subnet (10.0.2.0/24)"

**3. CloudFrontとS3の配置**

1. VPCの外側（インターネット側）にCloudFrontアイコンを配置
2. S3アイコンを配置
3. CloudFront → S3へ矢印で接続
4. ラベル: "Static Content Delivery"

**4. ALB（Application Load Balancer）の配置**

1. パブリックサブネット内にALBアイコンを配置
2. CloudFront → ALBへ矢印で接続

**5. EC2インスタンス（Auto Scaling）の配置**

1. プライベートサブネット内にEC2アイコンを配置
2. EC2アイコンを複数配置（または1つのアイコンに「×3」などのラベル）
3. Auto Scalingアイコンも配置
4. ALB → EC2へ矢印で接続

**6. RDS（データベース）の配置**

1. 別のプライベートサブネットにRDSアイコンを配置
2. Multi-AZを示すために、破線で囲む
3. EC2 → RDSへ矢印で接続
4. ラベル: "MySQL 8.0 (Multi-AZ)"

**7. セキュリティグループとNATゲートウェイ**

1. セキュリティグループを示す破線の枠を各リソースに追加
2. パブリックサブネットにNAT Gatewayアイコンを配置
3. EC2 → NAT Gateway → Internet Gatewayへの経路を矢印で示す

**8. 補足情報の追加**

1. 「Note」図形を配置して、構成の説明を追加:
   - "Auto Scaling: Min 2, Max 10"
   - "RDS: db.t3.medium, 100GB SSD"
   - "Backup: Daily at 03:00 JST"

### 4. ネットワーク図の作成

#### 例: オンプレミスとクラウドのハイブリッド構成

1. 左側に「オンプレミス」エリアを配置（矩形）
2. 右側に「AWS」エリアを配置（VPCアイコン）
3. オンプレミス側にサーバー、ファイアウォール、スイッチを配置
4. AWS側にVPC、Subnet、EC2を配置
5. オンプレミスとAWSを「Site-to-Site VPN」または「Direct Connect」で接続
6. 矢印にラベルを追加（例: "VPN 10.0.0.0/16 ⇔ 192.168.0.0/16"）

### 5. ソフトウェア構成図（C4モデル風）

Draw.ioでC4モデル（Context、Container、Component、Code）風の図も作成できます。

#### System Context Diagram（システムコンテキスト図）

1. 中央に「System」（矩形、背景色: 青）を配置
2. 周囲に「User」（人型アイコン）、「External System」（矩形）を配置
3. 矢印で関係を接続
4. ラベル: "Uses", "Sends data to"

#### Container Diagram（コンテナ図）

1. システム内部を展開
2. 「Web Application」「API Server」「Database」を配置
3. 技術スタックをラベルに追加（例: "React.js", "Node.js", "PostgreSQL"）

### 6. レイヤー分け

複雑なシステム構成図では、レイヤーごとに色分けします。

#### レイヤー例

- **プレゼンテーション層**: 薄い黄色
- **アプリケーション層**: 薄い緑
- **データ層**: 薄い青
- **インフラ層**: 薄い灰色

### 7. エクスポート

#### PNG/SVG/PDF出力

1. 「File」→「Export as」を選択
2. 形式を選択:
   - **PNG**: プレゼンテーション用
   - **SVG**: ベクター形式（拡大縮小しても劣化しない）
   - **PDF**: ドキュメント用
3. オプションを設定:
   - **Zoom**: 100%〜400%
   - **Border Width**: 余白
   - **Transparent Background**: 透明背景（PNG/SVG）
4. 「Export」をクリック

### 8. テンプレートの活用

Draw.ioには、システム構成図のテンプレートがあります。

1. 新規作成時に「Create New Diagram」画面で「Template」を選択
2. カテゴリから「Cloud」または「Network」を選択
3. テンプレートを選択（例: "AWS Architecture"、"Azure Architecture"）
4. 「Create」をクリック

### 9. アイコンのカスタマイズ

#### アイコンの色変更

1. アイコンを選択
2. 右側パネルの「Style」タブで色を変更
3. 「Fill」で塗りつぶし色、「Line」で線の色を設定

#### アイコンのグループ化

1. 複数のアイコンを選択（Ctrl + クリック）
2. 右クリック→「Group」
3. グループ化されたアイコンを移動・コピーできる

### 10. ベストプラクティス

#### 命名規則

- **リソース名**: わかりやすい名前を使用（例: "web-server-01", "db-master"）
- **CIDR**: IPアドレス範囲を明記（例: "10.0.1.0/24"）
- **ポート番号**: 通信ポートを明記（例: "HTTPS:443"）

#### 図の整理

- レイヤーごとに色分け
- データフローを矢印で明示
- 重要なリソースを中央に配置
- ラベルを適切に配置（読みやすさを優先）

#### バージョン管理

- ファイル名にバージョン番号を含める（例: "system-architecture-v1.0.drawio"）
- Google Drive/OneDriveでバージョン履歴を管理

## 公式ドキュメント

- **公式サイト**: [diagrams.net](https://www.diagrams.net/)
- **ユーザーマニュアル**: [Draw.io User Manual](https://www.drawio.com/doc/)
- **AWS Architecture Icons**: [AWS Icons for draw.io](https://www.drawio.com/blog/aws-diagrams)
- **Azure Icons**: [Azure Diagrams](https://www.drawio.com/blog/azure-diagrams)

## 学習リソース

- **システム構成図チュートリアル**: [Network Diagrams with draw.io](https://www.youtube.com/results?search_query=drawio+network+diagram)
- **AWSアーキテクチャ図**: [AWS Architecture Diagrams](https://aws.amazon.com/architecture/)

## 関連リンク

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
- [C4 Model](https://c4model.com/)（ソフトウェアアーキテクチャ可視化手法）

## 関連ドキュメント

このツールは他の開発工程でも使用されます：

- [要件定義/業務分析でのDraw.io](../../2_業務分析/Draw.io/Draw.io.md) - BPMNプロセス図作成
- [要件定義/ユースケース分析でのDraw.io](../../3_ユースケース分析（機能要件定義）/Draw.io/Draw.io.md) - ユースケース図作成
- [基本設計（アプリケーション）/画面設計でのDraw.io](../../../開発工程_3_基本設計_アプリケーション/2_画面設計/Draw.io/Draw.io.md) - ワイヤーフレーム、画面遷移図
- [基本設計（アプリケーション）/データベース論理設計でのDraw.io](../../../開発工程_3_基本設計_アプリケーション/5_データベース論理設計/Draw.io/Draw.io.md) - ER図、テーブル関連図
- [基本設計（アプリケーション）/バッチ設計でのDraw.io](../../../開発工程_3_基本設計_アプリケーション/7_バッチ設計/Draw.io/Draw.io.md) - バッチ処理フロー図
- [基本設計（インフラ）/ネットワーク構成図でのDraw.io](../../../開発工程_4_基本設計_インフラ/1_ネットワーク構成図/Draw.io/Draw.io.md) - ネットワーク構成図、VLAN設計

全ツールの一覧については[ツール索引](../../../ツール索引.md)を参照してください。
