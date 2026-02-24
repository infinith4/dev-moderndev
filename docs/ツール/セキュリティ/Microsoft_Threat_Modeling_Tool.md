# Microsoft Threat Modeling Tool

## 概要

Microsoft Threat Modeling Tool（TMT）は、ソフトウェア設計段階でセキュリティ脅威を特定・分析するための無料ツールである。STRIDE（Spoofing、Tampering、Repudiation、Information Disclosure、Denial of Service、Elevation of Privilege）フレームワークに基づき、システムアーキテクチャ図からセキュリティ脅威を自動検出する。設計段階での脅威分析により、実装後の脆弱性修正コストを大幅に削減できる。

## 主な特徴

| 項目 | 内容 |
|------|------|
| 無料提供 | Microsoft提供、Windows専用の無料ツール |
| STRIDEフレームワーク | 業界標準の脅威分類モデルを採用 |
| 自動脅威検出 | データフロー図（DFD）から脅威を自動生成 |
| 対策提案 | 各脅威に対する緩和策を提案 |
| レポート生成 | HTML・Excel形式でレポート出力 |
| Azureテンプレート | Azure向けの統合テンプレートを提供 |
| SDL統合 | Microsoft Security Development Lifecycle準拠 |

## 主な機能

### データフロー図（DFD）作成

| 機能 | 説明 |
|------|------|
| プロセス | アプリケーション、サービスの配置 |
| データストア | データベース、ファイルの配置 |
| 外部エンティティ | ユーザー、外部システムの配置 |
| データフロー | プロセス間のデータ移動定義 |
| トラストバウンダリ | 信頼境界の設定 |

### STRIDE脅威分析

| 機能 | 説明 |
|------|------|
| Spoofing | なりすまし・認証の脅威検出 |
| Tampering | データ改ざん・整合性の脅威検出 |
| Repudiation | 否認・監査の脅威検出 |
| Information Disclosure | 情報漏洩・機密性の脅威検出 |
| Denial of Service | サービス拒否・可用性の脅威検出 |
| Elevation of Privilege | 権限昇格・認可の脅威検出 |

### 対策管理

| 機能 | 説明 |
|------|------|
| 緩和策提案 | 各脅威への対策を自動提案 |
| ステータス管理 | Not Started、Needs Investigation、Mitigation Implemented、Not Applicable |
| 優先度設定 | High、Medium、Lowの優先度管理 |
| 対策記録 | 実施内容の記録と監査証跡 |

## インストールとセットアップ

公式URL:
- [Microsoft Threat Modeling Tool ダウンロード](https://aka.ms/threatmodelingtool)
- [公式ドキュメント](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
- [GitHub](https://github.com/microsoft/threat-modeling-tool)
- [Microsoft SDL](https://www.microsoft.com/en-us/securityengineering/sdl)

## 基本的な使い方

### 1. インストール

```
1. 公式サイトにアクセス: https://aka.ms/threatmodelingtool
2. ダウンロード（Windows専用）
3. インストーラー実行（.NET Framework 4.5以上必須）
4. Threat Modeling Toolを起動
```

### 2. 新規モデル作成

```
1. File → New でモデル作成
2. 要素追加（左ペイン）:
   - External Entity: ユーザー
   - Process: Webアプリケーション
   - Data Store: データベース
   - Data Flow: ユーザー → Web App → Database
3. トラストバウンダリを追加
4. View → Analysis View で脅威分析実行
```

### 3. Webアプリケーション例

```
要素配置:
1. External Entity: "User" (インターネット)
2. Trust Boundary: "HTTPS Boundary"
3. Process: "Web Server"
4. Trust Boundary: "Internal Network"
5. Process: "API Server"
6. Data Store: "Database"

データフロー:
User → Web Server (HTTPS)
Web Server → API Server (Internal)
API Server → Database (SQL)
```

### 4. 脅威分析結果の確認

```
検出される脅威例:

1. Spoofing the Web Server Process
   - Category: Spoofing
   - Priority: High
   - Mitigation: Use HTTPS with valid certificate

2. Tampering with Data Flow
   - Category: Tampering
   - Priority: High
   - Mitigation: Use TLS 1.2+, validate SSL certificates

3. Information Disclosure of Database
   - Category: Information Disclosure
   - Priority: High
   - Mitigation: Encrypt data at rest, use encrypted connections
```

### 5. 対策記録とレポート生成

```
対策記録:
1. Analysis View → 脅威をクリック
2. State: Mitigation Implemented
3. Justification: "Implemented TLS 1.2 encryption"

レポート生成:
1. Reports → Create Full Report（HTML形式）
2. Reports → Create Excel Report（Excel形式）
```

## テンプレート活用

```
Azure用テンプレート:
- File → New → Azure Template
  - Azure Web App
  - Azure SQL Database
  - Azure Storage

カスタムテンプレート:
- カスタムステンシル追加
- 組織固有のテンプレート作成
```

## 他ツールとの比較

### TMT vs OWASP Threat Dragon

| 機能 | Microsoft TMT | OWASP Threat Dragon |
|------|---------------|---------------------|
| プラットフォーム | Windows専用 | クロスプラットフォーム |
| 価格 | 無料 | 無料（OSS） |
| 脅威フレームワーク | STRIDE | STRIDE |
| 自動脅威検出 | あり | 限定的 |
| UI | デスクトップアプリ | Web/デスクトップ |
| チーム協業 | ファイル共有 | Git連携可能 |
| Azureテンプレート | あり | なし |

### TMT vs IriusRisk

| 機能 | Microsoft TMT | IriusRisk |
|------|---------------|-----------|
| 価格 | 無料 | 有料 |
| 自動化 | 限定的 | CI/CD統合対応 |
| チーム協業 | 非対応 | クラウド対応 |
| レポート | 基本的 | 高度 |
| カスタマイズ | 限定的 | 柔軟 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| システム設計レビュー | 設計段階での脅威特定 | DFD作成、STRIDE分析、緩和策計画 |
| セキュリティ監査 | コンプライアンス対応 | 脅威レポート生成、対策状況の追跡 |
| Azure設計検証 | クラウドアーキテクチャのセキュリティ | Azureテンプレートによる脅威分析 |
| SDL準拠 | Microsoft SDL準拠の開発 | 設計フェーズでの必須脅威分析 |

## ベストプラクティス

### 1. モデル作成時の注意点

- トラストバウンダリを適切に設定し、信頼境界を明確にする
- すべてのデータフローにプロトコルを記載する
- 外部エンティティと内部プロセスを明確に区別する

### 2. 脅威分析の進め方

- 検出された脅威を優先度順に評価する
- 各脅威に対して緩和策を具体的に記録する
- Not Applicableの場合も理由を記録する

### 3. レポートの管理

- 定期的にレポートを生成して変更を追跡する
- Excelレポートを使って進捗管理する
- 脅威モデルファイルをバージョン管理に含める

## トラブルシューティング

### よくある問題と解決策

#### 1. インストールできない

```
原因: .NET Framework 4.5以上が未インストール
解決策:
- .NET Frameworkの最新版をインストール
- Windows Updateを実行
```

#### 2. 大規模モデルでパフォーマンスが低下

```
原因: 要素数が多すぎる
解決策:
- モデルをサブシステム単位に分割
- 重要なコンポーネントに焦点を絞る
```

#### 3. カスタムテンプレートが認識されない

```
原因: テンプレートファイルの配置場所が不正
解決策:
- 公式ドキュメントでテンプレートの配置パスを確認
- XMLスキーマを検証
```

## 参考リソース

### 公式ドキュメント
- ダウンロード: https://aka.ms/threatmodelingtool
- ドキュメント: https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool
- SDL: https://www.microsoft.com/en-us/securityengineering/sdl

### コミュニティ
- GitHub: https://github.com/microsoft/threat-modeling-tool

### チュートリアル
- Getting Started with TMT: https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started
- STRIDE Overview: https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats

## まとめ

Microsoft Threat Modeling Toolは、設計段階でのセキュリティ脅威分析に特化した無料ツールとして、以下の場面で特に有用である:

1. **設計段階の脅威分析** - STRIDEフレームワークによる体系的な脅威特定
2. **Azure環境のセキュリティ設計** - Azure統合テンプレートによる効率的な分析
3. **SDL準拠の開発** - Microsoft Security Development Lifecycle準拠のプロセス
4. **セキュリティ教育** - シンプルなUIで脅威モデリングの学習に最適

Windows専用という制約はあるが、無料で利用でき、自動脅威検出と対策提案機能により、セキュリティ設計の品質向上に貢献する。
