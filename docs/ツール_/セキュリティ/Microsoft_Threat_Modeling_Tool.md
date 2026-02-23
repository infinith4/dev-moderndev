# Microsoft Threat Modeling Tool

## 概要

Microsoft Threat Modeling Tool（TMT）は、ソフトウェア設計段階でセキュリティ脅威を特定・分析するための無料ツールです。STRIDE（Spoofing、Tampering、Repudiation、Information Disclosure、Denial of Service、Elevation of Privilege）フレームワークに基づき、システムアーキテクチャ図からセキュリティ脅威を自動検出します。設計段階での脅威分析により、実装後の脆弱性修正コストを大幅に削減します。

## 主な機能

### 1. データフロー図（DFD）作成
- **プロセス**: アプリケーション、サービス
- **データストア**: データベース、ファイル
- **外部エンティティ**: ユーザー、外部システム
- **データフロー**: プロセス間のデータ移動
- **トラストバウンダリ**: 信頼境界

### 2. STRIDE脅威分析
- **Spoofing（なりすまし）**: 認証の脅威
- **Tampering（改ざん）**: データ整合性の脅威
- **Repudiation（否認）**: 監査の脅威
- **Information Disclosure（情報漏洩）**: 機密性の脅威
- **Denial of Service（サービス拒否）**: 可用性の脅威
- **Elevation of Privilege（権限昇格）**: 認可の脅威

### 3. 自動脅威検出
- **ルールベース**: 要素タイプに基づく脅威生成
- **脅威リスト**: 検出された脅威一覧
- **優先度**: High、Medium、Low

### 4. 対策提案
- **緩和策**: 各脅威への対策
- **検証**: 対策の実装状況
- **ステータス**: Not Started、Mitigation Implemented等

### 5. レポート
- **HTMLレポート**: 脅威一覧、対策レポート
- **Excel**: 脅威管理表
- **テンプレート**: カスタムレポート

## 利用方法

### インストール

```
1. 公式サイトにアクセス
   https://aka.ms/threatmodelingtool

2. ダウンロード（Windows専用）
   Threat Modeling Tool 2016.exe

3. インストーラー実行
   .NET Framework 4.5以上必須

4. 起動
   Threat Modeling Tool 2016
```

### 基本的なモデル作成

```
1. 新規モデル作成
   File → New

2. 要素追加（左ペイン）
   - External Entity: User
   - Process: Web Application
   - Data Store: Database
   - Data Flow: User → Web App → Database

3. トラストバウンダリ追加
   Web Applicationを囲む境界を追加

4. 脅威分析実行
   View → Analysis View
   自動的に脅威が検出される
```

### Webアプリケーション例

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

### 脅威分析結果

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

4. Elevation of Privilege
   - Category: Elevation of Privilege
   - Priority: Medium
   - Mitigation: Implement principle of least privilege
```

### 対策記録

```
1. 脅威選択
   Analysis View → 脅威をクリック

2. 対策入力
   State: Mitigation Implemented
   Justification: "Implemented TLS 1.2 encryption"
   Priority: (変更可能)

3. ステータス管理
   - Not Started
   - Needs Investigation
   - Mitigation Implemented
   - Not Applicable
```

### レポート生成

```
1. HTMLレポート
   Reports → Create Full Report
   → HTML形式で脅威一覧・対策レポート生成

2. Excelレポート
   Reports → Create Excel Report
   → 脅威管理表をExcel出力
```

### テンプレート活用

```
1. Azure用テンプレート
   File → New → Azure Template
   - Azure Web App
   - Azure SQL Database
   - Azure Storage

2. AWS用テンプレート（カスタム作成）
   - カスタムステンシル追加
   - 組織固有のテンプレート作成
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Threat Modeling Tool** | 🟢 無料 | Windows専用、無料ダウンロード |

## メリット

### ✅ 主な利点

1. **無料**: Microsoft提供、無料
2. **STRIDE**: 業界標準フレームワーク
3. **自動脅威検出**: DFDから自動生成
4. **設計段階**: 早期の脅威特定
5. **対策提案**: 緩和策の提案
6. **レポート**: HTMLEXcel出力
7. **テンプレート**: Azure統合テンプレート
8. **学習容易**: シンプルなUI
9. **Microsoft支援**: 公式ドキュメント充実
10. **SDL統合**: Microsoft SDL準拠

## デメリット

### ❌ 制約・課題

1. **Windows専用**: macOS、Linux非対応
2. **更新頻度**: 更新が遅い
3. **UI古い**: モダンなUIではない
4. **チーム協業**: 同時編集不可
5. **クラウド非対応**: ローカルファイルのみ
6. **自動化**: CI/CD統合困難
7. **カスタマイズ**: ルール追加が複雑
8. **大規模モデル**: パフォーマンス低下

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **OWASP Threat Dragon** | オープンソース、クロスプラットフォーム | TMTよりモダンだがSTRIDEに特化 |
| **IriusRisk** | 商用、自動化対応 | TMTより高機能だが有料 |
| **ThreatModeler** | クラウド、チーム協業 | TMTよりエンタープライズ向け |
| **Cairis** | オープンソース、セキュリティ要件管理 | TMTより高度だが複雑 |
| **draw.io** | 汎用作図 | TMTより柔軟だが脅威自動検出なし |

## 公式リンク

- **ダウンロード**: [https://aka.ms/threatmodelingtool](https://aka.ms/threatmodelingtool)
- **ドキュメント**: [https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
- **GitHub**: [https://github.com/microsoft/threat-modeling-tool](https://github.com/microsoft/threat-modeling-tool)
- **SDL**: [https://www.microsoft.com/en-us/securityengineering/sdl](https://www.microsoft.com/en-us/securityengineering/sdl)

## 関連ドキュメント

- [セキュリティ設計ツール一覧](../セキュリティ設計ツール/)
- [OWASP ZAP](../セキュリティツール/OWASP_ZAP.md)
- [Snyk](../セキュリティツール/Snyk.md)
- [脅威モデリングベストプラクティス](../../best-practices/threat-modeling.md)

---

**カテゴリ**: セキュリティ設計ツール  
**対象工程**: 設計、セキュリティ  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
