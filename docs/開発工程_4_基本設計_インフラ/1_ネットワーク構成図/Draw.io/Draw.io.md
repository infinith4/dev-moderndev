# Draw.io（ネットワーク構成図）

## 概要

Draw.io（diagrams.net）は、完全無料のオンライン図作成ツールで、基本設計（インフラ）フェーズではネットワーク構成図、VLANセグメント図、ファイアウォール設定図、データセンターレイアウトの作成に活用します。AWS/Azure/GCPのネットワークアイコンが充実しており、オンプレミス・クラウド両方のネットワーク設計に対応します。

### 基本設計（インフラ）フェーズでの活用

- **ネットワーク構成図**: 物理・論理ネットワークトポロジーの設計
- **VLANセグメント図**: VLAN分割、IPアドレス設計、サブネット設計
- **ファイアウォール設定図**: セキュリティグループ、ACL、ファイアウォールルールの可視化
- **クラウドネットワーク図**: VPC、サブネット、ルーティングテーブルの設計
- **データセンターレイアウト**: ラック配置、配線図、電源系統図

### メリット・デメリット

**メリット**
- 完全無料で広告なし
- AWS、Azure、GCP、Cisco、ネットワーク機器のアイコンが豊富
- Google Drive、OneDrive統合でバージョン管理が容易
- オフライン利用可能（デスクトップ版）
- SVG/PNG/PDFエクスポート対応

**デメリット**
- リアルタイムコスト見積不可
- 実ネットワーク連携機能なし
- リアルタイム協業機能が弱い
- 自動レイアウト機能が限定的

## 利用方法

### 1. Draw.ioへのアクセスとネットワーク図作成

1. [diagrams.net](https://www.diagrams.net/)にアクセス
2. 保存先を選択（Device、Google Drive、OneDrive等）
3. 「Create New Diagram」をクリック
4. テンプレートから「Network」を選択

### 2. ネットワークアイコンライブラリの有効化

1. 左パネルで「More Shapes...」をクリック
2. 以下のライブラリにチェック:
   - **Network**: ネットワーク機器全般
   - **Cisco**: Cisco機器アイコン
   - **AWS19**: AWSネットワークサービス
   - **Azure**: Microsoft Azureネットワーク
   - **GCP**: Google Cloud Platformネットワーク
3. 「Apply」をクリック

### 3. 物理ネットワーク構成図の作成

#### 例: 3層ネットワークアーキテクチャ（オンプレミス）

**ネットワーク構成:**
- コアスイッチ層（Core Layer）
- ディストリビューション層（Distribution Layer）
- アクセス層（Access Layer）

**作成手順:**

**1. コアスイッチの配置**

1. 左パネルの「Cisco」から「Router」または「Multilayer Switch」を配置
2. ラベル: "Core Switch 1"、"Core Switch 2"（冗長化）
3. 配置: 図の最上部

**2. ディストリビューションスイッチの配置**

1. 「Cisco」から「Multilayer Switch」を配置
2. ラベル: "Distribution Switch 1"、"Distribution Switch 2"
3. 配置: コアスイッチの下

**3. アクセススイッチの配置**

1. 「Cisco」から「Switch」を配置
2. ラベル: "Access Switch 1"〜"Access Switch 4"
3. 配置: ディストリビューションスイッチの下

**4. ファイアウォールの配置**

1. 「Network」から「Firewall」を配置
2. ラベル: "Firewall（ASA 5545-X）"
3. 配置: コアスイッチとインターネット間

**5. 接続線の配置**

1. 「Line」ツールで各機器を接続
2. 線の種類:
   - **実線**: アクティブリンク
   - **破線**: スタンバイリンク（冗長化）
3. ラベル: 回線速度、VLAN ID等を追加
   - 例: "10Gbps"、"VLAN 100"

**完成イメージ:**

```
┌──────────────┐
│ Internet     │
└───────┬──────┘
        ↓
┌──────────────┐
│ Firewall     │
│ (ASA 5545-X) │
└───────┬──────┘
        ↓
┌────────────────────────┐
│ Core Switch 1          │ ←→ Core Switch 2
│ (10Gbps)               │
└────────┬───────────────┘
         ↓
┌─────────────────────────────────┐
│ Distribution Switch 1 ←→ Distribution Switch 2 │
│ (VLAN 10, 20, 30)                               │
└────────┬────────────────────────┘
         ↓
┌────────────────────────────────────────┐
│ Access Switch 1 │ Access Switch 2 │ ... │
│ (VLAN 10)       │ (VLAN 20)       │     │
└─────────────────────────────────────────┘
```

### 4. 論理ネットワーク構成図（VLANセグメント図）

#### 例: VLANセグメント設計

**VLAN構成:**
- VLAN 10: 管理ネットワーク（192.168.10.0/24）
- VLAN 20: サーバーネットワーク（192.168.20.0/24）
- VLAN 30: クライアントネットワーク（192.168.30.0/24）
- VLAN 100: DMZ（192.168.100.0/24）

**作成手順:**

**1. VLANセグメントの表現**

1. 「General」から「Rectangle」を配置
2. 各VLANを色分け:
   - VLAN 10: 薄い緑（#E8F5E9）
   - VLAN 20: 薄い青（#E3F2FD）
   - VLAN 30: 薄い黄（#FFF9C4）
   - VLAN 100: 薄い赤（#FFEBEE）

**2. VLAN情報の記載**

各Rectangleに以下を記載:

```
VLAN 10: 管理ネットワーク
─────────────────────
ネットワークアドレス: 192.168.10.0/24
ゲートウェイ: 192.168.10.1
DHCP範囲: 192.168.10.100-200
用途: サーバー管理、監視ツール
```

**3. ルーティングの表現**

1. 各VLANセグメントの上に「Router」または「Layer 3 Switch」を配置
2. 矢印でルーティング関係を表現
3. ラベル: "L3 Routing"

### 5. クラウドネットワーク構成図（AWS VPC）

#### 例: AWS 3層Webアプリケーションのネットワーク設計

**構成:**
- VPC: 10.0.0.0/16
- Public Subnet（AZ-a）: 10.0.1.0/24
- Private Subnet（AZ-a）: 10.0.2.0/24
- Database Subnet（AZ-a）: 10.0.3.0/24
- Multi-AZ構成（AZ-b）も同様に構成

**作成手順:**

**1. VPCの配置**

1. 「AWS19」ライブラリから「VPC」アイコンを配置
2. サイズを大きめに調整（内部にサブネットを配置）
3. ラベル: "production-vpc (10.0.0.0/16)"

**2. Availability Zoneの表現**

1. VPC内に「Rectangle」を2つ配置
2. ラベル: "Availability Zone A"、"Availability Zone B"
3. 背景色: 薄いグレー

**3. サブネットの配置**

AZ-A内に以下のサブネットを配置（Rectangleで表現）:

- **Public Subnet**: 背景色 薄い緑
  ```
  Public Subnet (10.0.1.0/24)
  ・ALB
  ・NAT Gateway
  ```

- **Private Subnet**: 背景色 薄い青
  ```
  Private Subnet (10.0.2.0/24)
  ・EC2インスタンス（Webサーバー）
  ・Auto Scaling Group
  ```

- **Database Subnet**: 背景色 薄い赤
  ```
  Database Subnet (10.0.3.0/24)
  ・RDS (Multi-AZ)
  ```

**4. AWSリソースの配置**

1. 「AWS19」から以下のアイコンを配置:
   - **Internet Gateway**: VPCの外側（上部）
   - **Application Load Balancer**: Public Subnet内
   - **NAT Gateway**: Public Subnet内
   - **EC2**: Private Subnet内（複数配置、または「×3」などのラベル）
   - **RDS**: Database Subnet内
   - **Security Group**: 各リソースの枠として破線で表現

**5. ルーティングの表現**

1. 矢印で通信フローを表現:
   - Internet → Internet Gateway → ALB
   - ALB → EC2
   - EC2 → RDS
   - EC2 → NAT Gateway → Internet（外部API呼び出し用）

**6. セキュリティグループの記載**

各リソースの近くにテキストボックスを配置:

```
【Security Group: alb-sg】
Inbound:
- HTTP (80) from 0.0.0.0/0
- HTTPS (443) from 0.0.0.0/0
Outbound:
- All traffic to private-subnet-sg
```

### 6. ファイアウォール設定図

#### ファイアウォールルールの可視化

**例: DMZのファイアウォール設定**

**ゾーン構成:**
- Internet Zone
- DMZ Zone
- Internal Zone

**作成手順:**

**1. ゾーンの配置**

1. 「Rectangle」で3つのゾーンを表現
2. 配置: 左から右へ「Internet」→「DMZ」→「Internal」

**2. ファイアウォールの配置**

1. 各ゾーン間に「Firewall」アイコンを配置
2. ラベル: "FW1: Internet-DMZ"、"FW2: DMZ-Internal"

**3. 通信フローとルールの記載**

矢印とラベルで通信を表現:

```
Internet → DMZ
─────────────
・HTTP (80) → Webサーバー
・HTTPS (443) → Webサーバー

DMZ → Internal
─────────────
・MySQL (3306) → DBサーバー
・LDAP (389) → 認証サーバー

Internal → DMZ
─────────────
・SSH (22) → 管理アクセス（特定IPのみ）
```

**4. ルールテーブルの作成**

ファイアウォール近くにテーブルを配置:

| No. | Source | Destination | Protocol | Port | Action | 備考 |
|-----|--------|-------------|----------|------|--------|------|
| 1 | 0.0.0.0/0 | Web Server | TCP | 80 | Allow | HTTP |
| 2 | 0.0.0.0/0 | Web Server | TCP | 443 | Allow | HTTPS |
| 3 | Web Server | DB Server | TCP | 3306 | Allow | MySQL |
| 4 | 管理PC | DMZ | TCP | 22 | Allow | SSH管理 |
| 5 | Any | Any | Any | Any | Deny | デフォルト拒否 |

### 7. IPアドレス設計表の作成

#### IPアドレス割り当て一覧

**方法1: Draw.io内でテーブル作成**

1. 「Insert」→「Table」でテーブルを作成
2. 行・列数を設定（例: 20行 x 7列）

| ネットワーク | VLAN ID | IPアドレス範囲 | サブネットマスク | ゲートウェイ | DHCP範囲 | 用途 |
|------------|---------|--------------|--------------|------------|---------|------|
| 管理NW | 10 | 192.168.10.0/24 | 255.255.255.0 | 192.168.10.1 | 192.168.10.100-200 | サーバー管理 |
| サーバーNW | 20 | 192.168.20.0/24 | 255.255.255.0 | 192.168.20.1 | - | 固定IP |
| クライアントNW | 30 | 192.168.30.0/24 | 255.255.255.0 | 192.168.30.1 | 192.168.30.50-250 | 業務PC |
| DMZ | 100 | 192.168.100.0/24 | 255.255.255.0 | 192.168.100.1 | - | 公開サーバー |

### 8. ラック配置図（データセンターレイアウト）

#### 42Uラックのサーバー配置

**作成手順:**

**1. ラックの作成**

1. 「Rectangle」で縦長の四角形を作成
2. サイズ: 幅150px、高さ800px
3. ラベル: "Rack 1 (42U)"

**2. Uユニットの表示**

1. ラック内に細い横線を引いて、Uユニットを表現
2. または、テーブルを使用してUユニットを表現

**3. 機器の配置**

各機器を配置し、Uユニット数を記載:

```
[Rack 1: 42U]
─────────────
U42-40: ブランク (3U)
U39-37: スイッチ (3U) - Cisco Catalyst 9500
U36-32: サーバー1 (5U) - Dell PowerEdge R750
U31-27: サーバー2 (5U) - Dell PowerEdge R750
U26-22: ストレージ (5U) - NetApp FAS8300
U21-20: UPS (2U)
U19-15: ブランク (5U)
U14-10: サーバー3 (5U) - Dell PowerEdge R750
U9-5: ブランク (5U)
U4-1: PDU・配線整理 (4U)
```

### 9. ネットワーク設計書の作成

#### 設計書の構成

**1. ネットワーク概要図**

Draw.ioで作成した全体ネットワーク構成図をPNG/PDFでエクスポートして添付

**2. VLANセグメント一覧**

| VLAN ID | VLAN名 | IPアドレス範囲 | 用途 | 備考 |
|---------|--------|--------------|------|------|
| 10 | Management | 192.168.10.0/24 | サーバー管理 | 管理者のみアクセス可 |
| 20 | Server | 192.168.20.0/24 | アプリサーバー | 固定IP割り当て |
| 30 | Client | 192.168.30.0/24 | 業務PC | DHCP |
| 100 | DMZ | 192.168.100.0/24 | 公開Webサーバー | - |

**3. ルーティングテーブル**

| Destination | Next Hop | Interface | Metric | 備考 |
|-------------|----------|-----------|--------|------|
| 0.0.0.0/0 | 192.168.1.1 | GigabitEthernet0/0 | 1 | デフォルトゲートウェイ |
| 192.168.10.0/24 | - | VLAN10 | 0 | 直接接続 |
| 192.168.20.0/24 | - | VLAN20 | 0 | 直接接続 |

**4. ファイアウォールルール一覧**

上記のファイアウォール設定表を記載

### 10. ネットワーク冗長性設計の可視化

#### HSRP/VRRPによるゲートウェイ冗長化

**構成:**
- Router 1（Active）
- Router 2（Standby）
- 仮想IP: 192.168.10.1

**作成手順:**

1. 「Cisco」から「Router」を2つ配置
2. ラベル: "Router 1 (Active)"、"Router 2 (Standby)"
3. 仮想IPを示すテキストボックス: "Virtual IP: 192.168.10.1 (HSRP)"
4. ハートビート通信を破線で表現
5. アクティブ経路を太線、スタンバイ経路を細線で表現

### 11. レイヤー構成の色分け

#### レイヤーごとの色分け例

- **Layer 1（物理層）**: 灰色
- **Layer 2（データリンク層）**: 緑色
- **Layer 3（ネットワーク層）**: 青色
- **Layer 4-7（上位層）**: 黄色

各機器に色を設定して、どのレイヤーで動作するかを視覚化

### 12. アイコンのカスタマイズ

#### ベンダー固有アイコンの追加

**Cisco機器の詳細アイコン:**

1. 「Cisco」ライブラリから選択:
   - Cisco Router
   - Cisco Switch
   - Cisco ASA Firewall
   - Cisco Wireless Controller

**クラウドサービスアイコン:**

1. 「AWS19」「Azure」「GCP」から選択:
   - VPC、VNet、VPC
   - Subnet
   - Route Table
   - Internet Gateway
   - NAT Gateway
   - Load Balancer

### 13. エクスポートとバージョン管理

#### PNG/PDF/SVGエクスポート

1. File → Export as → 形式を選択
2. **PNG**: 設計書添付用（300dpi推奨）
3. **PDF**: プレゼンテーション用
4. **SVG**: 拡大縮小可能なベクター形式

#### Git管理

```bash
git add network_design_production.drawio
git commit -m "Add VPC network design with 3-tier architecture"
git push
```

### 14. ベストプラクティス

#### 命名規則

- **ネットワーク名**: わかりやすい名前（例: "production-vpc"、"dmz-network"）
- **CIDR表記**: 必ずCIDR記法を使用（例: "10.0.1.0/24"）
- **機器名**: ホスト名、IPアドレスを明記（例: "core-sw-01 (192.168.10.254)"）

#### 図の整理

- レイヤーごとに上から下へ配置（Internet → Firewall → Core → Distribution → Access）
- データフローを左から右、または上から下へ表現
- 冗長構成は左右対称に配置
- ラベルを適切に配置（読みやすさを優先）

#### バージョン管理

- ファイル名にバージョン番号を含める（例: "network_design_v1.2.drawio"）
- Google Drive/OneDriveでバージョン履歴を管理
- 主要な変更点をコメントに記載

## 公式ドキュメント

- **公式サイト**: [diagrams.net](https://www.diagrams.net/)
- **ユーザーマニュアル**: [Draw.io User Manual](https://www.drawio.com/doc/)
- **ネットワーク図ガイド**: [Network Diagrams](https://www.drawio.com/blog/network-diagrams)
- **AWS Architecture Icons**: [AWS Icons for draw.io](https://www.drawio.com/blog/aws-diagrams)
- **Azure Icons**: [Azure Diagrams](https://www.drawio.com/blog/azure-diagrams)

## 学習リソース

- **ネットワーク図チュートリアル**: [Network Diagrams with draw.io](https://www.youtube.com/results?search_query=drawio+network+diagram)
- **AWS Architecture Diagrams**: [AWS Architecture](https://aws.amazon.com/architecture/)
- **Cisco Design Zone**: [Cisco Network Design](https://www.cisco.com/c/en/us/solutions/design-zone.html)

## 関連リンク

- [Lucidchart](https://www.lucidchart.com/)（商用ネットワーク図ツール）
- [Microsoft Visio](https://www.microsoft.com/microsoft-365/visio/)（エンタープライズ図作成ツール）
- [Cacoo](https://cacoo.com/)（日本製図作成ツール）
- [RFC 3021 - VLAN設計](https://www.ietf.org/rfc/rfc3021.txt)（VLAN標準仕様）

## 関連ドキュメント

このツールは他の開発工程でも使用されます：

- [要件定義/業務分析でのDraw.io](../../../開発工程_2_要件定義/2_業務分析/Draw.io/Draw.io.md) - BPMNプロセス図作成
- [要件定義/ユースケース分析でのDraw.io](../../../開発工程_2_要件定義/3_ユースケース分析（機能要件定義）/Draw.io/Draw.io.md) - ユースケース図作成
- [要件定義/システム方針検討でのDraw.io](../../../開発工程_2_要件定義/10_システム方針検討（機能要件定義）/Draw.io/Draw.io.md) - システム構成図作成
- [基本設計（アプリケーション）/画面設計でのDraw.io](../../../開発工程_3_基本設計_アプリケーション/2_画面設計/Draw.io/Draw.io.md) - ワイヤーフレーム、画面遷移図
- [基本設計（アプリケーション）/データベース論理設計でのDraw.io](../../../開発工程_3_基本設計_アプリケーション/5_データベース論理設計/Draw.io/Draw.io.md) - ER図、テーブル関連図
- [基本設計（アプリケーション）/バッチ設計でのDraw.io](../../../開発工程_3_基本設計_アプリケーション/7_バッチ設計/Draw.io/Draw.io.md) - バッチ処理フロー図

全ツールの一覧については[ツール索引](../../../ツール索引.md)を参照してください。
