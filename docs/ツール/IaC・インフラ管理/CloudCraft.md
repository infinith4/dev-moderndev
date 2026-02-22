# CloudCraft

## 概要

CloudCraftは、AWSインフラストラクチャをビジュアルに設計・文書化できるクラウドアーキテクチャ図作成ツールです。ドラッグ&ドロップで直感的にAWSリソースを配置し、美しい3Dまたは2Dのシステム構成図を作成できます。既存のAWSアカウントと連携して現在のインフラを自動的にスキャンし、ドキュメント化することも可能です。コスト見積もり機能により、設計段階でインフラコストを把握できます。

## 主な機能

### 1. ビジュアルアーキテクチャ設計
- **AWSアイコン**: 公式アイコンでリソース表示
- **3D/2Dビュー**: 立体的または平面的な図表
- **ドラッグ&ドロップ**: 直感的な操作
- **スナップグリッド**: 整列された配置

### 2. ライブAWSスキャン
- 既存AWSアカウントからリソースを自動取得
- VPC、EC2、RDS、S3、Lambda等を自動配置
- リアルタイムインフラの可視化
- インベントリ管理

### 3. コスト見積もり
- リソースごとの月額コスト計算
- インスタンスタイプ変更による比較
- TCO（総所有コスト）分析
- リージョン別料金対応

### 4. チームコラボレーション
- 図表の共有・編集
- コメント・フィードバック
- バージョン履歴
- 権限管理

### 5. エクスポート
- PNG、SVG、PDF形式
- 高解像度出力
- プレゼンテーション資料作成

### 6. Terraformエクスポート（Pro版）
- 設計図からTerraformコード生成
- Infrastructure as Code化
- Git管理との統合

## 利用方法

### 基本的な使い方

```
1. アカウント作成
   https://www.cloudcraft.co/ でサインアップ
   
2. 新規図表作成
   Dashboard → Create a new blueprint
   
3. AWSリソース配置
   - 左サイドバーから EC2、RDS 等をドラッグ
   - キャンバスに配置
   - プロパティパネルでインスタンスタイプ等を設定
   
4. VPC・サブネット構成
   - VPC コンポーネントをドラッグ
   - Availability Zone を配置
   - Public/Private Subnet を定義
   - リソースをサブネット内に配置
   
5. 接続線の追加
   - リソース間をドラッグして接続
   - セキュリティグループの視覚化
   
6. コスト確認
   - 右上の Budget タブでコスト表示
   - リソースごとの料金内訳確認
```

### AWSアカウント連携

```
1. Settings → AWS Account

2. Add AWS Account

3. 認証方法選択:
   - CloudFormation Stack（推奨）
   - IAM Role
   
4. CloudFormation Stackの場合:
   - Launch Stack in AWS
   - AWS Management Consoleで実行
   - 必要な権限を付与（ReadOnly推奨）
   
5. Scan AWS Account
   - リージョン選択
   - Scan実行
   - 既存リソースが自動配置される
```

### システム構成図作成例

```
典型的な3層Webアプリケーション:

1. VPCを配置
2. 2つのAvailability Zoneを追加
3. 各AZに以下を配置:
   - Public Subnet: ALB、NAT Gateway
   - Private Subnet (App): EC2 Auto Scaling Group
   - Private Subnet (DB): RDS Multi-AZ
4. 外部からの接続:
   - Internet Gateway → ALB
5. 内部接続:
   - ALB → EC2
   - EC2 → RDS
   - EC2 → Internet (NAT経由)
6. コスト確認:
   - Budget タブで月額料金表示
   - インスタンスサイズ調整でコスト最適化
```

## 料金プラン

| プラン | 価格 | 主な機能 |
|--------|------|----------|
| **Free** | 無料 | 1ユーザー、無制限図表（要透かし） |
| **Pro** | $49/月 | 無制限ユーザー、AWSスキャン、Terraformエクスポート |
| **Enterprise** | $149/月～ | SSO、高度なセキュリティ、専用サポート |

※価格は2025年時点

## メリット

### ✅ 主な利点

1. **美しいビジュアル**: 3D表示でプレゼンに最適
2. **AWSスキャン**: 既存インフラを自動取得
3. **コスト見積もり**: 設計段階でコスト把握
4. **直感的操作**: ドラッグ&ドロップで簡単
5. **公式アイコン**: AWSの最新アイコン対応
6. **Terraformエクスポート**: IaC化が容易（Pro版）
7. **リアルタイム協業**: チームで同時編集可能
8. **エクスポート**: PNG、SVG、PDF出力
9. **無料プラン**: 基本機能は無料で利用可能
10. **クロスプラットフォーム**: ブラウザで動作

## デメリット

### ❌ 制約・課題

1. **AWS専用**: Azure、GCPには非対応
2. **Pro版必要**: AWSスキャンはPro版のみ
3. **Terraformエクスポート制限**: Pro版のみ、完全性は保証されない
4. **オフライン不可**: インターネット接続必須
5. **日本語非対応**: UIは英語のみ
6. **無料版制限**: 透かしが入る、AWSスキャン不可
7. **詳細設定困難**: 複雑なネットワーク設定は表現しづらい
8. **料金変動**: AWSの料金変更に追随しない場合あり

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Lucidchart** | マルチクラウド対応、AWS/Azure/GCP | CloudCraftよりコスト見積もり弱い |
| **Draw.io (diagrams.net)** | 無料、AWSアイコンあり | CloudCraftより機能限定的だが無料 |
| **Cacoo** | 日本製、AWSアイコン対応 | CloudCraftより3D表示なし |
| **AWS Application Composer** | AWS公式、無料 | CloudCraftよりビジュアルは劣る |
| **Cloudockit** | AWS/Azure自動ドキュメント化 | CloudCraftよりドキュメント重視 |
| **Hava.io** | マルチクラウド自動図表化 | CloudCraftより高額 |

## 公式リンク

- **公式サイト**: [https://www.cloudcraft.co/](https://www.cloudcraft.co/)
- **ドキュメント**: [https://docs.cloudcraft.co/](https://docs.cloudcraft.co/)
- **サンプル図表**: [https://www.cloudcraft.co/examples](https://www.cloudcraft.co/examples)
- **価格**: [https://www.cloudcraft.co/pricing](https://www.cloudcraft.co/pricing)
- **ブログ**: [https://www.cloudcraft.co/blog](https://www.cloudcraft.co/blog)

## 関連ドキュメント

- [インフラ設計ツール一覧](../インフラ設計ツール/)
- [作図ツール一覧](../作図ツール/)
- [Lucidchart](../作図ツール/Lucidchart.md)
- [Terraform](../IaCツール/Terraform.md)
- [AWS設計ベストプラクティス](../../best-practices/aws-architecture.md)

---

**カテゴリ**: インフラ設計ツール  
**対象工程**: 基本設計、詳細設計、インフラ設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
