# Lucidchart（ネットワーク構成図）

## 概要

Lucidchartは、クラウドベースの図作成ツールで、基本設計（インフラ）フェーズではネットワーク構成図、クラウドアーキテクチャ図、インフラ設計図の作成に活用します。リアルタイム協業機能が強力で、AWS/Azure/GCPの公式アイコンライブラリが充実しており、チームでのインフラ設計に最適です。

### 基本設計（インフラ）フェーズでの活用

- **ネットワークトポロジー図**: 物理・論理ネットワーク構成の設計
- **クラウドアーキテクチャ図**: AWS/Azure/GCPのネットワーク設計
- **VLANセグメント図**: VLAN分割、IPアドレス設計
- **ファイアウォール構成図**: セキュリティグループ、ACLの設計
- **ラック配置図**: データセンターレイアウト

### 料金プラン

- **無料プラン**: 3つのドキュメント、基本図形
- **Individual**: $7.95/月（年払い $95/年）
- **Team**: $9/月/ユーザー（年払い、最小3ユーザー）
- **Enterprise**: カスタム価格

### メリット・デメリット

**メリット**
- リアルタイム協業機能が強力（複数人同時編集）
- AWS/Azure/GCPの公式アイコンライブラリが豊富
- Visioファイルのインポート/エクスポート対応
- テンプレートが充実（ネットワーク図、クラウド図等）
- 自動レイアウト機能
- Confluence、Slack、Google Workspace統合

**デメリット**
- 有料プランが高額（Team: $480/年）
- オフライン利用不可
- 大規模な図の作成は動作が重い
- Infrastructure as Code（IaC）生成機能なし

## 利用方法

### 1. Lucidchartアカウントの作成

1. [Lucidchart公式サイト](https://www.lucidchart.com/)にアクセス
2. 「Sign up free」をクリック
3. Google、Microsoft、またはメールアドレスでアカウント作成
4. 無料プランで開始

### 2. 新規ドキュメントの作成

1. ダッシュボードで「+ New」をクリック
2. 「Blank Document」を選択
3. または、テンプレートから「Network Diagram」を選択

### 3. ネットワーク図作成の基本

#### シェイプライブラリの有効化

1. 左サイドバーの「More Shapes」をクリック
2. 以下のライブラリを有効化:
   - **Network**: ネットワーク機器全般
   - **Cisco**: Cisco機器専用アイコン
   - **AWS Architecture**: AWSサービスアイコン
   - **Azure**: Azure公式アイコン
   - **Google Cloud Platform**: GCPアイコン
3. 「Use Selected Shapes」をクリック

### 4. 企業ネットワーク構成図の作成

#### 例: 中規模企業のネットワーク設計

**ネットワーク構成:**
- インターネット接続（ISP冗長化）
- ファイアウォール（HA構成）
- コアスイッチ（冗長化）
- ディストリビューションスイッチ
- アクセススイッチ
- Wi-Fiアクセスポイント

**作成手順:**

**1. インターネット接続の配置**

1. 「Network」ライブラリから「Cloud」アイコンを配置
2. ラベル: "Internet"
3. 配置: 図の最上部中央

**2. ISP冗長化の表現**

1. 「Network」から「Router」を2つ配置
2. ラベル: "ISP Router 1 (主系)"、"ISP Router 2 (副系)"
3. Internetから両方のルーターへ線を引く

**3. ファイアウォール（HA）の配置**

1. 「Network」から「Firewall」を2つ配置
2. ラベル: "Firewall 1 (Active)"、"Firewall 2 (Standby)"
3. ISPルーターからファイアウォールへ接続
4. 2つのファイアウォール間に「HA Sync」とラベルを付けた線を追加

**4. コアスイッチの配置**

1. 「Cisco」から「Multilayer Switch」を2つ配置
2. ラベル: "Core Switch 1"、"Core Switch 2"
3. ファイアウォールからコアスイッチへ接続
4. 2つのコアスイッチ間を線で接続（LACP、スタッキング等）

**5. VLAN情報の追加**

各スイッチの近くにテキストボックスを追加:

```
【VLANトランク】
- VLAN 10: 管理 (192.168.10.0/24)
- VLAN 20: サーバー (192.168.20.0/24)
- VLAN 30: クライアント (192.168.30.0/24)
- VLAN 40: ゲスト (192.168.40.0/24)
```

### 5. AWS VPCネットワーク構成図

#### 例: 3層Webアプリケーション on AWS

**構成:**
- VPC: 10.0.0.0/16
- Public Subnet（ALB、NAT Gateway）
- Private Subnet（EC2、アプリサーバー）
- Database Subnet（RDS）
- Multi-AZ構成

**作成手順:**

**1. VPCコンテナの作成**

1. 「Rectangle」で大きな枠を作成
2. 塗りつぶし: 薄い青（#E3F2FD）
3. 枠線: 青（#2196F3）
4. ラベル: "VPC: production-vpc (10.0.0.0/16)"

**2. Availability Zoneの配置**

VPC内に2つのRectangleを配置:
- ラベル: "Availability Zone ap-northeast-1a"、"Availability Zone ap-northeast-1c"
- 塗りつぶし: 薄いグレー

**3. サブネットの配置（AZ-a）**

AZ-a内に以下のサブネットを配置:

**Public Subnet:**
1. Rectangle作成
2. 塗りつぶし: 薄い緑（#E8F5E9）
3. ラベル: "Public Subnet (10.0.1.0/24)"
4. 内部に以下を配置:
   - 「AWS Architecture」から「Application Load Balancer」
   - 「AWS Architecture」から「NAT Gateway」

**Private Subnet:**
1. Rectangle作成
2. 塗りつぶし: 薄いオレンジ（#FFF3E0）
3. ラベル: "Private Subnet (10.0.2.0/24)"
4. 内部に以下を配置:
   - 「AWS Architecture」から「EC2」アイコンを3つ（または1つに「×3」ラベル）
   - 「AWS Architecture」から「Auto Scaling」

**Database Subnet:**
1. Rectangle作成
2. 塗りつぶし: 薄い赤（#FFEBEE）
3. ラベル: "Database Subnet (10.0.3.0/24)"
4. 内部に以下を配置:
   - 「AWS Architecture」から「RDS」

**4. AWSリソースの追加**

1. VPCの外側に「Internet Gateway」を配置
2. Security Groupを破線のRectangleで表現

**5. データフローの表現**

矢印で通信フローを追加:

```
Internet → Internet Gateway → ALB → EC2 → RDS
                                ↓
                           NAT Gateway → Internet
```

各矢印にラベルを追加:
- "HTTPS (443)"
- "HTTP (80)"
- "MySQL (3306)"

### 6. セキュリティグループの詳細設計

#### Security Group可視化

**方法1: テーブル形式**

1. 「Insert」→「Table」でテーブルを挿入
2. Security Groupルールを記載:

| Security Group | Inbound Rules | Source | Protocol | Port | 説明 |
|---------------|---------------|--------|----------|------|------|
| alb-sg | Allow | 0.0.0.0/0 | HTTPS | 443 | インターネットからのHTTPS |
| alb-sg | Allow | 0.0.0.0/0 | HTTP | 80 | インターネットからのHTTP |
| ec2-sg | Allow | alb-sg | HTTP | 8080 | ALBからのトラフィック |
| rds-sg | Allow | ec2-sg | MySQL | 3306 | EC2からのDB接続 |

**方法2: 図形で表現**

1. 各リソースを破線のRectangleで囲む
2. Rectangleのラベル: "Security Group: alb-sg"
3. テキストボックスでルールを記載

### 7. ネットワークACL（NACL）設計

#### NACLルールの可視化

**サブネット単位のNACL:**

1. サブネットを選択
2. 右側にテキストボックスを配置
3. NACLルールを記載:

```
【Network ACL: public-nacl】
Inbound Rules:
100: Allow HTTP (80) from 0.0.0.0/0
110: Allow HTTPS (443) from 0.0.0.0/0
120: Allow Ephemeral ports (1024-65535) from 0.0.0.0/0
*: Deny all

Outbound Rules:
100: Allow HTTP (80) to 0.0.0.0/0
110: Allow HTTPS (443) to 0.0.0.0/0
120: Allow Ephemeral ports (1024-65535) to 0.0.0.0/0
*: Deny all
```

### 8. ルートテーブル設計

#### Route Table可視化

1. サブネットの横に「Route Table」アイコンを配置（または専用アイコンがない場合はテキストボックス）
2. ルーティングテーブルの内容を記載:

```
【Route Table: public-rtb】
Destination      Target               Status
10.0.0.0/16      local                Active
0.0.0.0/0        igw-xxxxxxxxx        Active
```

```
【Route Table: private-rtb】
Destination      Target               Status
10.0.0.0/16      local                Active
0.0.0.0/0        nat-xxxxxxxxx        Active
```

### 9. ハイブリッドクラウド構成図

#### オンプレミスとAWSの接続

**構成:**
- オンプレミスデータセンター
- AWS Direct Connect
- VPN接続（バックアップ）

**作成手順:**

**1. オンプレミス側の配置**

1. 左側に「Rectangle」を配置
2. ラベル: "オンプレミスデータセンター"
3. 内部に以下を配置:
   - 「Cisco」から「Router」
   - 「Cisco」から「Firewall」
   - 「Network」から「Server」

**2. AWS側の配置**

1. 右側に「VPC」を配置（前述の手順）

**3. 接続の表現**

1. オンプレミスとAWSを接続:
   - 「AWS Architecture」から「Direct Connect」アイコンを配置
   - 「AWS Architecture」から「VPN Connection」アイコンを配置（破線で表現）
2. ラベル:
   - Direct Connect: "1Gbps専用線"
   - VPN: "IPsec VPN（バックアップ）"

**4. ネットワーク情報の追加**

```
【オンプレミス】
ネットワーク: 192.168.0.0/16

【AWS VPC】
ネットワーク: 10.0.0.0/16

【Direct Connect】
BGP ASN（オンプレ）: 65001
BGP ASN（AWS）: 7224
VLAN: 100
```

### 10. テンプレートの活用

#### Lucidchart標準テンプレート

1. 「Templates」→「Network Diagrams」を選択
2. 以下のテンプレートが利用可能:
   - **Basic Network Diagram**: 基本的なネットワーク図
   - **AWS Architecture**: AWS構成図テンプレート
   - **Cisco Network Diagram**: Ciscoネットワーク図
   - **Data Center Layout**: データセンターラック配置

### 11. リアルタイム協業

#### チームでの共同編集

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
3. コメントを入力（例: "このサブネットのCIDRブロック要確認"）

### 12. バージョン管理

#### リビジョン履歴

1. 「File」→「Revision History」
2. 過去のバージョンを確認・復元
3. 変更内容の比較表示

### 13. エクスポート機能

#### 複数形式でのエクスポート

1. 「File」→「Download As」
2. 形式を選択:
   - **PDF**: プレゼンテーション用
   - **PNG**: 設計書添付用（解像度選択可能）
   - **JPEG**: 画像形式
   - **SVG**: ベクター形式
   - **Visio (VSDX)**: Visioとの互換性

### 14. 統合機能

#### Confluence統合

1. Lucidchartドキュメントを選択
2. 「Publish」→「Confluence」
3. Confluenceページに埋め込み

#### Slack統合

1. Slack Appをインストール
2. `/lucidchart` コマンドで図を共有

### 15. ネットワーク設計書への統合

#### 設計書の構成

**1. ネットワーク概要図**

Lucidchartで作成した全体構成図をPDFでエクスポートして添付

**2. 詳細設計図**

- VLANセグメント図
- IPアドレス設計図
- ルーティング設計図
- セキュリティグループ設計図

**3. 設計仕様表**

Lucidchart内でテーブルを作成、またはExcelと連携

## 公式ドキュメント

- **公式サイト**: [Lucidchart](https://www.lucidchart.com/)
- **ヘルプセンター**: [Lucidchart Help Center](https://lucidchart.zendesk.com/)
- **ネットワーク図ガイド**: [Network Diagram Guide](https://www.lucidchart.com/pages/network-diagram)
- **AWS Architecture**: [AWS Diagram Tutorial](https://www.lucidchart.com/pages/tutorials/aws-architecture-diagram)
- **チュートリアル動画**: [Lucidchart YouTube](https://www.youtube.com/c/Lucidchart)

## 学習リソース

- **ネットワーク図作成ガイド**: [How to Create Network Diagrams](https://www.lucidchart.com/blog/how-to-make-a-network-diagram)
- **AWS Architecture Best Practices**: [AWS Architecture with Lucidchart](https://www.lucidchart.com/pages/solutions/aws)
- **Cisco Network Design**: [Cisco Network Diagrams](https://www.lucidchart.com/pages/templates/network-diagram/cisco-network-diagram)

## 関連リンク

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)（AWS設計ベストプラクティス）
- [Microsoft Visio](https://www.microsoft.com/microsoft-365/visio/)（代替ツール）
- [Draw.io](https://www.diagrams.net/)（無料代替ツール）
- [Cacoo](https://cacoo.com/)（日本製図作成ツール）

## 関連ドキュメント

このツールは他の開発工程でも使用されます：

- [要件定義/業務分析でのLucidchart](../../../開発工程_2_要件定義/2_業務分析/Lucidchart/Lucidchart.md) - BPMNプロセス図作成、チーム協業
- [要件定義/ユースケース分析でのLucidchart](../../../開発工程_2_要件定義/3_ユースケース分析（機能要件定義）/Lucidchart/Lucidchart.md) - ユースケース図作成、リアルタイム協業

全ツールの一覧については[ツール索引](../../../ツール索引.md)を参照してください。
