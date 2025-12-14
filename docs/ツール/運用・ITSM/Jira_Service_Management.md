# Jira Service Management

## 概要

Jira Service Management（旧Jira Service Desk）は、Atlassian社が提供するITサービスマネジメント（ITSM）ツールです。ITILベストプラクティスに準拠し、インシデント管理、問題管理、変更管理、資産管理をサポートします。Jiraプロジェクト管理と統合され、開発チームとIT運用チームのコラボレーションを促進し、DevOps文化を実現します。

## 主な機能

### 1. サービスデスク
- **セルフサービスポータル**: ユーザー向けヘルプセンター
- **ナレッジベース**: FAQドキュメント
- **リクエストフォーム**: カスタムリクエストタイプ
- **SLA管理**: サービスレベル目標

### 2. インシデント管理
- **チケット起票**: メール、ポータル、API
- **優先度設定**: Critical、High、Medium、Low
- **自動割り当て**: ルールベース割り当て
- **エスカレーション**: SLA違反時の自動エスカレーション

### 3. 問題管理
- **根本原因分析**: インシデントから問題へ昇格
- **既知の問題**: ナレッジ登録
- **変更要求**: 問題解決のための変更

### 4. 変更管理
- **変更承認**: 承認ワークフロー
- **リスク評価**: 変更のリスクアセスメント
- **変更スケジュール**: 変更カレンダー
- **ロールバック**: 変更失敗時の対応

### 5. 資産管理
- **CMDB**: 構成管理データベース
- **資産追跡**: ハードウェア、ソフトウェア
- **依存関係**: サービス間の関連
- **資産ライフサイクル**: 購入から廃棄

### 6. オンコール管理
- **アラート**: モニタリングツール統合
- **ローテーション**: オンコールスケジュール
- **通知**: SMS、電話、Slack
- **インシデント対応**: PagerDuty風機能

### 7. Jira統合
- **開発連携**: Jira SoftwareJira Work Management統合
- **双方向リンク**: インシデント ⇔ Jira課題
- **バージョン追跡**: リリースとインシデント関連付け

## 利用方法

### プロジェクト作成

```
1. Jira管理画面 → Projects → Create project
2. テンプレート選択: IT Service Management
3. プロジェクト名: "IT Support"
4. プロジェクトキー: ITS
```

### リクエストタイプ設定

```
1. Project settings → Request types
2. 追加:
   - インシデント報告
   - サービスリクエスト
   - 変更要求
   - アクセス権限リクエスト

3. フィールド設定:
   - 優先度
   - 影響範囲
   - 緊急度
   - カテゴリ
```

### SLA設定

```
1. Project settings → SLAs
2. 新規SLA作成:
   - Name: "Critical Incident Response"
   - Time to first response: 15 minutes
   - Time to resolution: 4 hours
   - Conditions: Priority = Critical

3. カレンダー設定:
   - 営業時間: 9:00-18:00 (月-金)
   - 休日除外
```

### 自動化ルール

```
# インシデント自動割り当て
1. Automation → Create rule
2. Trigger: Issue created
3. Condition: Request type = Incident
4. Action: 
   - If Priority = Critical → Assign to Senior Support
   - Else → Assign to Support Queue

# SLA違反時エスカレーション
1. Trigger: SLA breached
2. Action:
   - Send email to manager
   - Add comment to issue
   - Change priority to High
```

### ナレッジベース

```
1. Knowledge base → Create article
2. タイトル: "パスワードリセット手順"
3. カテゴリ: アカウント管理
4. 内容:
   手順1: ログイン画面の「パスワードを忘れた」をクリック
   手順2: メールアドレス入力
   手順3: 届いたメールのリンクをクリック
5. Publish
```

### 資産管理

```
1. Assets → Create object type
2. オブジェクトタイプ: "Laptop"
3. 属性:
   - Serial Number
   - Model
   - Purchase Date
   - Assigned User
   - Status (In Use, Available, Retired)

4. オブジェクト作成:
   - Serial: ABC123456
   - Model: MacBook Pro 16"
   - Assigned User: user@example.com
```

### Opsgenie統合（オンコール）

```
1. Apps → Find new apps → Opsgenie
2. インストール
3. 設定:
   - Alert routing: Critical incidents → On-call team
   - Escalation policy: 5分後にチームリーダーへ
   - Notification channels: SMS、Slack
```

### Confluence統合

```
1. ナレッジベース記事作成時
2. Link to Confluence page
3. 双方向同期設定
```

## エディション・料金

| エディション | 価格（月額） | 特徴 |
|-------------|-------------|------|
| **Free** | 🟢 無料 | 3エージェント、基本ITSM |
| **Standard** | 💰 $20/エージェント | SLA、オンコール、資産管理 |
| **Premium** | 💰 $47/エージェント | 高度な自動化、サンドボックス、24/7サポート |
| **Enterprise** | 💰 要問い合わせ | 無制限ストレージ、99.9% SLA、専用サポート |

## メリット

### ✅ 主な利点

1. **ITIL準拠**: 業界標準ITSMプロセス
2. **Jira統合**: 開発とIT運用の連携
3. **無料プラン**: 3エージェントまで無料
4. **柔軟なワークフロー**: カスタマイズ可能
5. **SLA管理**: サービスレベル自動追跡
6. **オンコール**: Opsgenie統合
7. **資産管理**: CMDB機能
8. **自動化**: ルールエンジン
9. **セルフサービス**: ユーザーポータル
10. **エコシステム**: Atlassianツール統合

## デメリット

### ❌ 制約・課題

1. **コスト**: エージェント数増加で高額
2. **学習曲線**: 高度な設定は習得に時間
3. **複雑性**: 多機能のため設定煩雑
4. **パフォーマンス**: 大規模環境で遅延
5. **カスタマイズ制限**: 一部機能は制限的
6. **オンプレミス**: クラウド推奨（オンプレは高価）
7. **Atlassian依存**: エコシステムに依存
8. **UI**: Jiraユーザー向け（非技術者には難しい）

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **ServiceNow** | エンタープライズITSM | Jira SMより高機能だが高価 |
| **Zendesk** | カスタマーサポート特化 | Jira SMよりシンプル |
| **Freshservice** | クラウドITSM | Jira SMと類似、料金体系異なる |
| **ManageEngine ServiceDesk Plus** | コスト効率的ITSM | Jira SMより安価 |
| **BMC Helix ITSM** | エンタープライズITSM | Jira SMより高機能だが複雑 |

## 公式リンク

- **公式サイト**: [https://www.atlassian.com/software/jira/service-management](https://www.atlassian.com/software/jira/service-management)
- **ドキュメント**: [https://support.atlassian.com/jira-service-management-cloud/](https://support.atlassian.com/jira-service-management-cloud/)
- **コミュニティ**: [https://community.atlassian.com/t5/Jira-Service-Management/ct-p/jira-service-desk](https://community.atlassian.com/t5/Jira-Service-Management/ct-p/jira-service-desk)
- **Marketplace**: [https://marketplace.atlassian.com/addons/app/jira-service-management](https://marketplace.atlassian.com/addons/app/jira-service-management)

## 関連ドキュメント

- [ITSMツール一覧](../ITSMツール/)
- [JIRA](../プロジェクト管理ツール/JIRA.md)
- [Confluence](../ドキュメント管理ツール/Confluence.md)
- [PagerDuty](../監視ツール/PagerDuty.md)
- [ITSMベストプラクティス](../../best-practices/itsm.md)

---

**カテゴリ**: ITSMツール  
**対象工程**: 運用、サポート  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
