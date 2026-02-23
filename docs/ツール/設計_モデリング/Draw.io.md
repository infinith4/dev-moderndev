# Draw.io (diagrams.net)

## 概要

Draw.io（現在はdiagrams.netとしても知られる）は、無料のオープンソース図作成ツールです。ビジネスプロセス図、UML図、ER図、ワイヤーフレーム、ネットワーク図など、様々な図表の作成に対応しています。ブラウザ版とデスクトップ版の両方が利用可能です。

### 主な特徴

- **無料**: すべての機能が無料で利用可能
- **オープンソース**: ソースコードが公開されており、カスタマイズ可能
- **ブラウザ/デスクトップ両対応**: Web版とデスクトップアプリの両方が利用可能
- **クラウドストレージ統合**: Google Drive、OneDrive、Dropboxとの連携
- **豊富なシェイプライブラリ**: BPMN、UML、ER図、AWS/Azure/GCPアイコン、ネットワーク機器等
- **オフライン利用可能**: デスクトップ版でインターネット接続なしで作図可能

### 料金プラン

- **無料**: すべての機能が無料（オープンソース）

### メリット・デメリット

**メリット**
- 無料で広告なし
- オープンソースで透明性が高く、セキュリティ面でも安心
- ブラウザ版とデスクトップ版の両方が利用可能
- Google Drive、OneDrive等との統合により、ファイル管理が容易
- BPMN、UML、ER図など標準記法に対応
- AWS/Azure/GCP等のクラウドアイコンライブラリが充実
- オフラインでも利用可能（デスクトップ版）
- Git統合でバージョン管理可能

**デメリット**
- リアルタイム協業機能が弱い（同時編集は不可）
- テンプレートが他の有料ツールに比べて少ない
- UIがやや古めのデザイン
- 高度な機能（シミュレーション、コード生成、トレーサビリティ管理等）は限定的

## 利用できる開発工程

Draw.ioは以下の開発工程で活用できます：

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| 要件定義/業務分析 | BPMNプロセス図作成 | 業務フロー図、BPMNプロセス図 |
| 要件定義/ユースケース分析 | ユースケース図作成 | ユースケース図、アクター関連図 |
| 要件定義/システム方針検討 | システム構成図作成 | システムアーキテクチャ図、C4モデル図 |
| 基本設計（アプリケーション）/画面設計 | ワイヤーフレーム、画面遷移図 | 画面遷移図、画面フロー図、ワイヤーフレーム |
| 基本設計（アプリケーション）/データベース論理設計 | ER図、テーブル関連図 | 論理ER図、テーブル関連図、正規化図 |
| 基本設計（アプリケーション）/バッチ設計 | バッチ処理フロー図 | バッチフロー図、ジョブネットワーク図、データフロー図 |
| 基本設計（インフラ）/ネットワーク構成図 | ネットワーク構成図、VLAN設計 | ネットワーク構成図、VLANセグメント図、AWS/Azure/GCPネットワーク図 |

## 基本的な利用方法

### 1. アクセス方法

#### Web版（ブラウザ）

1. [diagrams.net](https://www.diagrams.net/)にアクセス
2. ブラウザで直接利用可能（アカウント登録不要）

#### デスクトップ版

1. [Draw.io Desktop](https://github.com/jgraph/drawio-desktop/releases)からダウンロード
2. インストーラーを実行してセットアップ
3. アプリケーションを起動

### 2. 保存先の選択

Draw.ioを開くと、最初に保存先を選択する画面が表示されます。

1. **Device**: ローカルストレージ（ブラウザ版ではダウンロードフォルダ）
2. **Google Drive**: Googleドライブに保存
3. **OneDrive**: OneDriveに保存
4. **Dropbox**: Dropboxに保存
5. **GitHub**: GitHubリポジトリに保存

推奨: チームでの共有が必要な場合は「Google Drive」や「OneDrive」を選択

### 3. 新規図の作成

1. 保存先を選択後、「Create New Diagram」をクリック
2. テンプレートを選択するか、「Blank Diagram」を選択
3. ファイル名を入力（例: "受注処理フロー"）
4. 「Create」ボタンをクリック

### 4. ライブラリの選択

1. 左側のパネルで「More Shapes...」をクリック
2. 必要なライブラリにチェックを入れる:
   - **General**: 基本図形
   - **Flowchart**: フローチャート図形
   - **BPMN 2.0**: ビジネスプロセスモデリング
   - **UML 2.5**: UML図（ユースケース、シーケンス等）
   - **Entity Relation**: ER図専用シェイプ
   - **Network**: ネットワーク機器
   - **Cisco**: Cisco機器アイコン
   - **AWS19**: AWSアーキテクチャアイコン
   - **Azure**: Microsoft Azureアイコン
   - **GCP**: Google Cloud Platformアイコン
   - **Mockups**: UIモックアップ
3. 「Apply」をクリック

### 5. 図形の配置

1. 左側のパネルから図形をドラッグ&ドロップでキャンバスに配置
2. 図形をダブルクリックしてテキストを編集
3. 図形をクリックして選択し、右側のパネルでスタイルを設定

### 6. コネクタの利用

#### 方法1: ドラッグ接続

1. 図形をクリックすると、四方に青い矢印アイコンが表示される
2. 青い矢印をクリックして、接続先の図形までドラッグ
3. 自動的にコネクタ（矢印）が作成される

#### 方法2: Waypoint接続

1. 図形の端にマウスを持っていくと、緑の×印が表示される
2. 緑の×印をクリックして、接続先の図形の緑の×印までドラッグ
3. コネクタが作成される

### 7. エクスポート

1. 「File」→「Export as」を選択
2. 形式を選択:
   - **PNG**: 画像形式
   - **JPEG**: 画像形式（圧縮率高）
   - **SVG**: ベクター形式（拡大縮小しても劣化しない）
   - **PDF**: ドキュメント形式
   - **HTML**: 埋め込み可能なHTML
   - **XML**: Draw.io形式（再編集可能）
3. オプションを設定:
   - ズームレベル
   - 背景色
   - 透明背景（PNG/SVGの場合）
4. 「Export」をクリック

## 工程別の活用方法

### 要件定義/業務分析での活用

**主な用途**: BPMNプロセス図、業務フロー図の作成

#### BPMN 2.0プロセス図の作成

**例: 顧客問い合わせ対応プロセス**

1. **BPMNライブラリの有効化**
   - 「More Shapes...」→「Business」→「BPMN 2.0」にチェック

2. **主要なBPMN図形**
   - **Event**: イベント（円）
     - Start Event: 開始イベント（細い線の円）
     - End Event: 終了イベント（太い線の円）
   - **Task**: タスク（四角形）
   - **Gateway**: ゲートウェイ（菱形）
     - Exclusive (XOR): 排他ゲートウェイ
     - Parallel (AND): 並列ゲートウェイ
   - **Sequence Flow**: シーケンスフロー（矢印）

3. **プロセスフロー作成の手順**
   - Start Eventを配置
   - Task「問い合わせ受付」を配置し、Start Eventから接続
   - Task「内容分類」を配置
   - Exclusive Gateway「分類」を配置
   - 分岐経路を作成（技術/営業/その他）
   - 各経路の処理タスクを配置
   - End Eventで終了

4. **スタイル設定とエクスポート**
   - 図形の色分け（例: 正常フロー=青、エラーフロー=赤）
   - PDF/PNG形式でエクスポート

### 要件定義/ユースケース分析での活用

**主な用途**: ユースケース図、アクター関連図の作成

#### ユースケース図の作成

**例: DVDレンタルシステムのユースケース図**

1. **UMLライブラリの有効化**
   - 「More Shapes...」→「Software」→「UML 2.5」にチェック

2. **アクターとユースケースの配置**
   - **Actor**（人型アイコン）を配置: 会員、スタッフ、システム管理者
   - **Use Case**（楕円形）を配置: DVDを借りる、DVDを返却する、等
   - **Subsystem**（システム境界）でユースケースを囲む

3. **関連付け**
   - アクター → ユースケース: 実線で接続（関連）
   - ユースケース → ユースケース:
     - «include» 関係: 破線矢印（必須の呼び出し）
     - «extend» 関係: 破線矢印（条件付き拡張）

4. **ユースケース詳細の記述**
   - ノートを使用してユースケース詳細を追加
   - または、「Edit Data」でメタデータを追加

### 要件定義/システム方針検討での活用

**主な用途**: システムアーキテクチャ図、クラウド構成図の作成

#### AWSシステム構成図の作成

**例: 3層Webアプリケーション**

1. **AWS19ライブラリの有効化**
   - 「More Shapes...」→「AWS19」にチェック

2. **VPCとサブネットの配置**
   - VPCアイコンを配置
   - Public Subnet、Private Subnet、Database Subnetを配置（色分け）

3. **AWSリソースの配置**
   - CloudFront + S3（フロントエンド）
   - ALB（ロードバランサー）
   - EC2 + Auto Scaling（アプリケーション層）
   - RDS（データベース層）

4. **セキュリティグループの記載**
   - 各リソースの近くにテキストボックスでSG設定を記載

### 基本設計（アプリケーション）/画面設計での活用

**主な用途**: ワイヤーフレーム、画面遷移図、画面フロー図の作成

#### ワイヤーフレームの作成

**例: ログイン画面のワイヤーフレーム**

1. **Mockupsライブラリの有効化**
   - 「More Shapes...」→「Mockups」カテゴリをすべて有効化

2. **レイアウトの作成**
   - Browser Windowを配置
   - ヘッダー、フッターをRectangleで配置
   - ログインフォームコンテナを配置

3. **フォーム要素の配置**
   - Text Input（メールアドレス、パスワード）
   - Button（ログインボタン）
   - ラベルとプレースホルダーを追加

4. **画面遷移図の作成**
   - 各画面をRectangleで表現
   - Arrowで遷移を接続
   - 遷移条件をラベルに追加

### 基本設計（アプリケーション）/データベース論理設計での活用

**主な用途**: 論理ER図、テーブル関連図、正規化図の作成

#### Crow's Foot記法でのER図作成

**例: ECサイトのデータベース設計**

1. **Entity Relationライブラリの有効化**
   - 「More Shapes...」→「Entity Relation」にチェック

2. **エンティティの作成**
   - Entityシェイプを配置
   - エンティティ名と属性を記載:
     ```
     Customer
     ─────────────────
     PK customer_id: INT
        email: VARCHAR(100)
        password_hash: VARCHAR(255)
        first_name: VARCHAR(50)
        last_name: VARCHAR(50)
        created_at: TIMESTAMP
     ```

3. **リレーションシップの設定**
   - Many to One アイコンを使用
   - Order（Many側） → Customer（One側）
   - OrderItem → Order
   - OrderItem → Product

4. **カーディナリティの表記**
   - リレーションシップ線をダブルクリックしてラベルを追加
   - 例: "1", "0..N", "(1,1)", "(0,N)"

### 基本設計（アプリケーション）/バッチ設計での活用

**主な用途**: バッチ処理フロー図、ジョブネットワーク図、データフロー図の作成

#### バッチ処理フロー図の作成

**例: 日次売上集計バッチ**

1. **Flowchartライブラリの有効化**
   - 「More Shapes...」→「Flowchart」にチェック

2. **フローチャート要素**
   - Terminator（楕円）: 開始/終了
   - Process（四角形）: 処理
   - Decision（菱形）: 判定
   - Data（平行四辺形）: 入出力データ

3. **バッチフロー作成の手順**
   - 開始ノード（毎日2:00 AM）
   - データ抽出処理
   - 件数チェック（判定）
   - データ変換・集計処理
   - レポート生成
   - S3へ保存
   - メール送信
   - 終了

4. **エラーハンドリングフローの追加**
   - 失敗時のリトライ処理
   - 3回失敗時のアラート送信
   - 処理中断

### 基本設計（インフラ）/ネットワーク構成図での活用

**主な用途**: ネットワーク構成図、VLANセグメント図、クラウドネットワーク設計

#### 物理ネットワーク構成図の作成

**例: 3層ネットワークアーキテクチャ**

1. **NetworkライブラリとCiscoライブラリの有効化**
   - 「More Shapes...」→「Network」「Cisco」にチェック

2. **ネットワーク機器の配置**
   - Firewall（インターネット境界）
   - Core Switch 1, 2（冗長化）
   - Distribution Switch 1, 2
   - Access Switch 1〜4

3. **接続線の配置**
   - 実線: アクティブリンク
   - 破線: スタンバイリンク
   - ラベルに回線速度を記載（10Gbps、1Gbps等）

4. **VLANセグメント図の作成**
   - Rectangleで各VLANセグメントを表現
   - 色分け（VLAN 10=緑、VLAN 20=青、VLAN 30=黄、VLAN 100=赤）
   - VLAN情報を記載（ネットワークアドレス、ゲートウェイ、DHCP範囲）

## 公式ドキュメント

- **公式サイト**: [diagrams.net](https://www.diagrams.net/)
- **ユーザーマニュアル**: [Draw.io User Manual](https://www.drawio.com/doc/)
- **FAQ**: [Draw.io FAQ](https://www.drawio.com/doc/faq/)
- **チュートリアル**: [Getting Started with draw.io](https://www.drawio.com/blog/getting-started-with-drawio)
- **BPMN Tutorial**: [BPMN Diagrams in draw.io](https://www.drawio.com/blog/bpmn-2-0)
- **UMLユースケース図チュートリアル**: [UML Use Case Diagrams in draw.io](https://www.drawio.com/blog/uml-use-case-diagrams)
- **ER図ガイド**: [Entity Relationship Diagrams](https://www.drawio.com/blog/entity-relationship-diagrams)
- **ネットワーク図ガイド**: [Network Diagrams](https://www.drawio.com/blog/network-diagrams)
- **AWS Architecture Icons**: [AWS Icons for draw.io](https://www.drawio.com/blog/aws-diagrams)
- **Azure Icons**: [Azure Diagrams](https://www.drawio.com/blog/azure-diagrams)

## 学習リソース

- **YouTube公式チャンネル**: [diagrams.net YouTube Channel](https://www.youtube.com/c/drawio)
- **Grafana Play**: [Demo Site](https://play.grafana.org/)（デモサイトで試せる）
- **テンプレート集**: [Diagram Templates](https://www.diagrams.net/example-diagrams)

## 関連リンク

- [Draw.io GitHub Repository](https://github.com/jgraph/drawio)
- [Draw.io Desktop Releases](https://github.com/jgraph/drawio-desktop/releases)
- [BPMN 2.0 仕様書（OMG公式）](https://www.omg.org/spec/BPMN/)
- [UML 2.5 仕様書（OMG公式）](https://www.omg.org/spec/UML/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
- [C4 Model](https://c4model.com/)（ソフトウェアアーキテクチャ可視化手法）
- [Crow's Foot記法](https://vertabelo.com/blog/crow-s-foot-notation/)
- [正規化理論](https://www.studytonight.com/dbms/database-normalization.php)
