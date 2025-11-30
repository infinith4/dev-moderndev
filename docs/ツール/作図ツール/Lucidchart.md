# Lucidchart

## 概要

Lucidchartは、クラウドベースの図表作成ツールで、ビジネスプロセス図、フローチャート、組織図、BPMN、ユースケース図、ネットワーク構成図など、様々な図表の作成に対応しています。ブラウザベースでリアルタイムの協業が可能な点が特徴です。

### 主な特徴

- **ブラウザベース**: インストール不要で、ブラウザからアクセス可能
- **リアルタイム協業**: 複数ユーザーが同時に編集可能
- **テンプレート豊富**: 様々な業務に対応したテンプレートを提供
- **BPMN対応**: BPMN 2.0に対応したプロセス図の作成が可能
- **UML対応**: ユースケース図、クラス図、シーケンス図などのUML図作成が可能
- **ネットワーク図対応**: AWS/Azure/GCP公式アイコンライブラリが充実
- **統合機能**: Google Workspace、Microsoft 365、Slack等との連携

### 料金プラン

- **Free版**: 基本機能（制限あり、3つのドキュメント）
- **Individual**: $7.95/月（個人向け）
- **Team**: $9/月/ユーザー（チーム向け）
- **Enterprise**: カスタム価格（大企業向け）

### メリット・デメリット

**メリット**
- ブラウザベースでどこからでもアクセス可能
- リアルタイム協業により、チームでの作業が効率的
- テンプレートが豊富で、すぐに作図を開始できる
- BPMN、UML、ネットワーク図など幅広い図表に対応
- 各種クラウドサービスとの統合機能が充実
- Visioファイルのインポート/エクスポート対応

**デメリット**
- 無料版は機能制限あり（ドキュメント数、図形数など）
- 有料版がやや高額
- オフラインでは利用不可
- 複雑な図を作成すると動作が重くなることがある
- 厳密なUML検証機能がない

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| 企画プロセス | ビジネスモデル可視化、ビジネスプロセス分析 | ビジネスモデルキャンバス、プロセスフロー図 |
| 要件定義/業務分析 | BPMNプロセス図作成、業務フロー可視化 | BPMN図、業務フロー図、組織図 |
| 要件定義/ユースケース分析 | ユースケース図作成、システム機能の可視化 | ユースケース図、システム境界図 |
| 基本設計(インフラ) | ネットワーク構成図、クラウドアーキテクチャ設計 | ネットワークトポロジー図、AWS/Azure構成図 |

## 基本的な利用方法

### 1. アカウント作成

1. [Lucidchart公式サイト](https://www.lucidchart.com/)にアクセス
2. 「Sign up free」をクリック
3. メールアドレスまたはGoogle/Microsoft アカウントで登録
4. アカウントを有効化

### 2. 新規ドキュメント作成

1. ダッシュボードから「+ New」ボタンをクリック
2. テンプレートを選択するか、「Blank Document」を選択
3. ドキュメント名を入力

### 3. 図形ライブラリの利用

1. 左側のパネルで「Shapes」をクリック
2. 必要なライブラリを選択:
   - **BPMN 2.0**: ビジネスプロセスモデリング
   - **UML Use Case**: ユースケース図
   - **Network**: ネットワーク機器全般
   - **AWS Architecture**: AWSサービスアイコン
   - **Azure**: Azure公式アイコン
   - **Google Cloud Platform**: GCPアイコン
   - **Cisco**: Cisco機器専用アイコン
3. 必要に応じて他のライブラリも追加

### 4. 図形の配置とコネクタ接続

1. ライブラリから図形をドラッグ&ドロップでキャンバスに配置
2. 図形をクリックすると、四方に赤い点（コネクションポイント)が表示される
3. 赤い点をクリックして、接続先の図形までドラッグ
4. 自動的にコネクタ（矢印）が作成される

### 5. チーム共有と協業

1. 右上の「Share」ボタンをクリック
2. 共有方法を選択:
   - **メールで招待**: メールアドレスを入力して招待
   - **リンク共有**: 共有リンクを生成（閲覧のみ/編集可能）
3. 権限を設定（View/Edit）
4. 「Send」をクリック

### 6. エクスポート

1. 「File」→「Download As」を選択
2. 形式を選択:
   - **PDF**: プレゼンテーション用
   - **PNG**: 画像形式
   - **JPEG**: 画像形式
   - **SVG**: ベクター形式
   - **Visio (VDX/VSDX)**: Visioとの互換性
3. オプションを設定（ページ範囲、品質など）
4. 「Download」をクリック

## 工程別の活用方法

### 要件定義/業務分析での活用

#### BPMNプロセス図の作成

**1. BPMNテンプレートの利用**

1. 「+ New」→「Templates」を選択
2. 検索バーに「BPMN」と入力
3. 適切なBPMNテンプレートを選択（例: "BPMN Process Map"）
4. 「Use Template」をクリック

**2. 主要なBPMN要素**

- **開始イベント**: 左パネルから「Start Event」（緑の円）をドラッグ&ドロップ
- **タスク**: 「Task」（四角形）を配置
- **排他ゲートウェイ**: 「Gateway」（菱形、×マーク）を配置
- **並列ゲートウェイ**: 「Gateway」（菱形、+マーク）を配置
- **終了イベント**: 「End Event」（赤の円）を配置

**3. プロセスフロー作成例: 購買承認プロセス**

```
[開始] → [購買申請] → [上司承認] → <承認？>
                                    ├─ Yes → [発注処理] → [納品確認] → [支払処理] → [終了]
                                    └─ No → [申請者へ差戻し] → [購買申請] (ループ)
```

### 要件定義/ユースケース分析での活用

#### UMLユースケース図の作成

**1. UMLテンプレートの選択**

1. 「+ New」→「UML Use Case」テンプレートを検索
2. 「Blank UML Use Case Diagram」を選択
3. ドキュメント名を入力（例: "予約システム ユースケース図"）

**2. 主要なUML要素**

- **Actor**: アクター（人型アイコン）
- **Use Case**: ユースケース（楕円形）
- **System Boundary**: システム境界（矩形）
- **Association**: 関連線（実線）
- **Include/Extend**: インクルード/エクステンド（破線矢印、«include»/«extend»ステレオタイプ）
- **Generalization**: 汎化（白抜き三角矢印）

**3. ユースケース図作成例: 病院予約システム**

**アクター:**
- 患者、医師、受付担当者、システム管理者

**ユースケース（患者向け）:**
- 予約する
  - «include» ログイン
  - «include» 空き枠確認
  - «extend» リマインダー設定
- 予約をキャンセルする
- 診察履歴を閲覧する

**作成手順:**
1. 左側にアクターを縦に配置
2. 中央にシステム境界「病院予約システム」を配置
3. システム境界内にユースケース（楕円形）を配置
4. アクターとユースケースを関連線で接続
5. Include/Extend関係を破線矢印で表現

### 基本設計(インフラ)/ネットワーク構成図での活用

#### AWS VPCネットワーク構成図の作成

**1. シェイプライブラリの有効化**

1. 左サイドバーの「More Shapes」をクリック
2. 以下のライブラリを有効化:
   - **Network**: ネットワーク機器全般
   - **AWS Architecture**: AWSサービスアイコン
   - **Azure**: Azure公式アイコン
   - **Google Cloud Platform**: GCPアイコン
   - **Cisco**: Cisco機器専用アイコン

**2. AWS 3層Webアプリケーション構成例**

**構成:**
- VPC: 10.0.0.0/16
- Public Subnet（ALB、NAT Gateway）
- Private Subnet（EC2、アプリサーバー）
- Database Subnet（RDS）
- Multi-AZ構成

**作成手順:**

**VPCコンテナの作成:**
1. 「Rectangle」で大きな枠を作成
2. 塗りつぶし: 薄い青（#E3F2FD）
3. 枠線: 青（#2196F3）
4. ラベル: "VPC: production-vpc (10.0.0.0/16)"

**Availability Zoneの配置:**
1. VPC内に2つのRectangleを配置
2. ラベル: "Availability Zone ap-northeast-1a"、"Availability Zone ap-northeast-1c"
3. 塗りつぶし: 薄いグレー

**サブネットの配置（AZ-a）:**

**Public Subnet:**
- Rectangle作成、塗りつぶし: 薄い緑（#E8F5E9）
- ラベル: "Public Subnet (10.0.1.0/24)"
- 内部に配置: Application Load Balancer、NAT Gateway

**Private Subnet:**
- Rectangle作成、塗りつぶし: 薄いオレンジ（#FFF3E0）
- ラベル: "Private Subnet (10.0.2.0/24)"
- 内部に配置: EC2アイコン×3、Auto Scaling

**Database Subnet:**
- Rectangle作成、塗りつぶし: 薄い赤（#FFEBEE）
- ラベル: "Database Subnet (10.0.3.0/24)"
- 内部に配置: RDS

**AWSリソースの追加:**
1. VPCの外側に「Internet Gateway」を配置
2. Security Groupを破線のRectangleで表現

**データフローの表現:**
矢印で通信フローを追加し、各矢印にラベルを追加（HTTPS (443)、HTTP (80)、MySQL (3306)等）

#### 企業ネットワーク構成図の作成

**例: 中規模企業のネットワーク設計**

**ネットワーク構成:**
- インターネット接続（ISP冗長化）
- ファイアウォール（HA構成）
- コアスイッチ（冗長化）
- ディストリビューションスイッチ
- アクセススイッチ
- Wi-Fiアクセスポイント

**VLAN情報の追加:**
各スイッチの近くにテキストボックスを追加:

```
【VLANトランク】
- VLAN 10: 管理 (192.168.10.0/24)
- VLAN 20: サーバー (192.168.20.0/24)
- VLAN 30: クライアント (192.168.30.0/24)
- VLAN 40: ゲスト (192.168.40.0/24)
```

### リアルタイム協業機能

**1. 共有設定**
1. 右上の「Share」ボタンをクリック
2. チームメンバーのメールアドレスを入力
3. 権限を選択:
   - **Can edit**: 編集可能
   - **Can comment**: コメントのみ
   - **Can view**: 閲覧のみ

**2. リアルタイム編集**
- 複数人が同時に編集可能
- カーソル位置が色分けされて表示
- チャット機能でコミュニケーション

**3. コメント機能**
1. オブジェクトを右クリック
2. 「Add Comment」を選択
3. コメントを入力

### バージョン管理

1. 「File」→「Revision History」
2. 過去のバージョンを確認・復元
3. 変更内容の比較表示

### 統合機能

**Confluence統合:**
1. Lucidchartドキュメントを選択
2. 「Publish」→「Confluence」
3. Confluenceページに埋め込み

**Slack統合:**
1. Slack Appをインストール
2. `/lucidchart` コマンドで図を共有

## 公式ドキュメント

- **公式サイト**: [Lucidchart](https://www.lucidchart.com/)
- **公式チュートリアル**: [Lucidchart Tutorials](https://www.lucidchart.com/pages/tutorial)
- **ヘルプセンター**: [Lucidchart Help Center](https://lucidchart.zendesk.com/hc/en-us)
- **BPMNガイド**: [BPMN Guide](https://www.lucidchart.com/pages/bpmn)
- **ネットワーク図ガイド**: [Network Diagram Guide](https://www.lucidchart.com/pages/network-diagram)
- **AWS Architecture**: [AWS Diagram Tutorial](https://www.lucidchart.com/pages/tutorials/aws-architecture-diagram)
- **動画チュートリアル**: [Lucidchart YouTube Channel](https://www.youtube.com/c/lucidchart)

## 学習リソース

- **ネットワーク図作成ガイド**: [How to Create Network Diagrams](https://www.lucidchart.com/blog/how-to-make-a-network-diagram)
- **AWS Architecture Best Practices**: [AWS Architecture with Lucidchart](https://www.lucidchart.com/pages/solutions/aws)
- **Cisco Network Design**: [Cisco Network Diagrams](https://www.lucidchart.com/pages/templates/network-diagram/cisco-network-diagram)

## 関連リンク

- [BPMN 2.0 仕様書（OMG公式）](https://www.omg.org/spec/BPMN/)
- [Lucidchart テンプレートギャラリー](https://www.lucidchart.com/pages/templates)
- [統合機能一覧](https://www.lucidchart.com/pages/integrations)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Microsoft Visio](https://www.microsoft.com/microsoft-365/visio/)（代替ツール）
- [Draw.io](https://www.diagrams.net/)（無料代替ツール）
