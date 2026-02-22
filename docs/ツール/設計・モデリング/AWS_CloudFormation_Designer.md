# AWS CloudFormation Designer

## 概要

AWS CloudFormation Designerは、Amazon Web Services公式のビジュアルテンプレートデザイナーです。ドラッグ&ドロップでCloudFormationテンプレート（JSON/YAML）を作成・編集し、AWSリソース（EC2、VPC、RDS、Lambda等）の関係を視覚的に設計します。既存テンプレートのインポート、リアルタイムプレビュー、テンプレートバリデーションにより、Infrastructure as Code（IaC）の理解とデバッグを支援します。

## 主な機能

### 1. ビジュアルデザイン
- **ドラッグ&ドロップ**: AWSリソース配置
- **自動レイアウト**: リソース関係の自動整列
- **コネクション**: リソース間の依存関係表示
- **リアルタイム同期**: GUI⇔コード双方向同期

### 2. テンプレート編集
- **JSON/YAML**: 両フォーマット対応
- **構文ハイライト**: コードエディター
- **自動補完**: リソースタイプ補完
- **バリデーション**: テンプレート検証

### 3. リソース管理
- **リソースタイプ**: 200+のAWSリソース
- **プロパティ編集**: リソースプロパティ設定
- **パラメータ**: 動的パラメータ定義
- **出力**: テンプレート出力値

### 4. インポート・エクスポート
- **テンプレートインポート**: 既存テンプレート読み込み
- **S3連携**: S3からテンプレート取得
- **ローカル保存**: JSONファイル保存
- **スタック作成**: Designerから直接デプロイ

### 5. コスト見積もり
- **AWS Cost Calculator**: リソースコスト試算
- **月額見積もり**: 予想コスト表示

## 利用方法

### Designer起動

```
1. AWS Management Console → CloudFormation
2. Design template → Create template in Designer
3. Designerキャンバス表示
```

### リソース追加

```
1. 左パネル: Resource types
2. リソース選択: EC2 → Instance
3. ドラッグ&ドロップ: キャンバスへ配置
4. プロパティ編集: 右パネルでプロパティ設定
   - InstanceType: t3.micro
   - ImageId: ami-12345678
   - KeyName: my-keypair
```

### VPC + EC2例

```
1. リソース追加:
   - VPC
   - Subnet (VPC内に配置)
   - InternetGateway
   - RouteTable
   - EC2 Instance (Subnet内に配置)

2. 接続:
   - VPC → Subnet（自動接続）
   - VPC → InternetGateway（ドラッグで接続）
   - Subnet → EC2 Instance（自動接続）

3. コード確認（YAML）:
   - 下部コードエディタで自動生成YAML確認
```

### テンプレート例（自動生成）

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: VPC with EC2 Instance

Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: MyVPC

  MySubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: us-east-1a
      MapPublicIpOnLaunch: true

  MyInternetGateway:
    Type: AWS::EC2::InternetGateway

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MyVPC
      InternetGatewayId: !Ref MyInternetGateway

  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-12345678
      SubnetId: !Ref MySubnet
      Tags:
        - Key: Name
          Value: MyEC2Instance
```

### 既存テンプレートインポート

```
1. Designer画面 → Open → Local file
2. テンプレートファイル選択（JSON/YAML）
3. ビジュアル表示
4. 編集・修正
5. Save → Download
```

### パラメータ追加

```yaml
# Designerでパラメータ追加
Parameters:
  InstanceTypeParameter:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
    Description: Enter instance type

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceTypeParameter
```

### バリデーション

```
1. テンプレート作成・編集
2. Validate template → 検証実行
3. エラー確認:
   - 構文エラー
   - リソース依存関係エラー
   - プロパティ不足
4. 修正
```

### スタック作成

```
1. Designer → Create stack
2. パラメータ入力:
   - Stack name: my-vpc-stack
   - Parameters: InstanceType = t3.micro
3. Review and create
4. デプロイ実行
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **CloudFormation Designer** | 🟢 無料 | AWS Console標準機能 |

## メリット

### ✅ 主な利点

1. **無料**: AWS標準機能
2. **ビジュアル**: GUI設計
3. **学習向け**: IaC理解促進
4. **リアルタイム同期**: GUI⇔コード双方向
5. **既存テンプレート**: インポート・可視化
6. **バリデーション**: テンプレート検証
7. **AWS公式**: 最新リソースタイプ対応
8. **デバッグ**: 依存関係確認
9. **スタック作成**: Designer直接デプロイ
10. **ブラウザベース**: インストール不要

## デメリット

### ❌ 制約・課題

1. **大規模テンプレート**: 複雑な図は見づらい
2. **レイアウト**: 自動配置が最適でない
3. **詳細編集**: コード直接編集が速い
4. **Git統合**: バージョン管理は別途必要
5. **複雑な依存関係**: 手動接続が煩雑
6. **ネストスタック**: サポート限定的
7. **エクスポート**: PNG等画像出力なし
8. **モダンUI**: UIが古い

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Terraform Visual** | Terraformビジュアル化 | Designer類似、Terraform向け |
| **Lucidchart** | クラウド作図 | Designerより柔軟だがCloudFormation非対応 |
| **draw.io** | 汎用作図 | Designerよりビジュアルだがコード生成なし |
| **Diagrams (Python)** | コードから図生成 | Designerと逆方向（コード→図） |
| **VS Code拡張** | CloudFormation Linter | Designerよりコード編集特化 |

## 公式リンク

- **公式ドキュメント**: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/working-with-templates-cfn-designer.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/working-with-templates-cfn-designer.html)
- **CloudFormation**: [https://aws.amazon.com/cloudformation/](https://aws.amazon.com/cloudformation/)
- **テンプレートリファレンス**: [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html)

## 関連ドキュメント

- [設計ツール一覧](../設計ツール/)
- [AWS CloudFormation](../IaCツール/AWS_CloudFormation.md)
- [Terraform](../IaCツール/Terraform.md)
- [Diagrams](../作図ツール/Diagrams.md)

---

**カテゴリ**: 設計ツール  
**対象工程**: インフラ設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
