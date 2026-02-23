# ServiceNow

## 概要

ServiceNowは、エンタープライズ向けのクラウドベースITサービスマネジメント（ITSM）プラットフォームです。インシデント管理、変更管理、問題管理、CMDB（構成管理データベース）、サービスカタログなどのITILプロセスを統合的に提供し、IT運用の標準化と自動化を実現します。Flow Designerによるノーコード/ローコードのワークフロー自動化、Integration Hubによる外部システム連携、AIを活用した予測分析など、IT運用のデジタルトランスフォーメーションを推進する包括的なプラットフォームです。

## 主な機能

### 1. インシデント管理
- **チケット管理**: インシデントの登録・分類・追跡
- **優先度設定**: 影響度と緊急度に基づく自動分類
- **エスカレーション**: 自動エスカレーションルール
- **SLA管理**: SLA目標の追跡と通知

### 2. 変更管理
- **変更要求**: 標準変更・通常変更・緊急変更の管理
- **CAB**: 変更諮問委員会のワークフロー
- **影響分析**: CMDBとの連携による影響範囲分析
- **承認プロセス**: 多段階承認ワークフロー

### 3. 問題管理
- **根本原因分析**: インシデントの根本原因特定
- **既知のエラー**: 既知のエラーデータベース管理
- **ナレッジ連携**: 解決策のナレッジベース登録
- **傾向分析**: 問題発生の傾向分析

### 4. CMDB（構成管理データベース）
- **CI管理**: 構成アイテムの登録・管理
- **リレーションシップ**: CI間の依存関係マッピング
- **ディスカバリ**: 自動検出によるCI情報の収集
- **サービスマッピング**: ビジネスサービスの依存関係可視化

### 5. サービスカタログ
- **リクエスト管理**: サービスリクエストのセルフサービス
- **カタログ定義**: サービスメニューの定義
- **フルフィルメント**: 自動プロビジョニング
- **承認ワークフロー**: リクエスト承認の自動化

### 6. Flow Designer / Integration Hub
- **ノーコード自動化**: GUIベースのワークフロー設計
- **外部連携**: REST API、Webhook等による外部システム統合
- **スポーク**: Slack、Jira、Azure DevOps等の連携コネクタ
- **スケジュール実行**: 定期実行ワークフロー

## 利用方法

### インスタンスのセットアップ

```
セットアップ手順:
  1. ServiceNowのインスタンスを契約・プロビジョニング
  2. 管理者アカウントでログイン
  3. プラグインの有効化（ITSM、CMDB等）
  4. 組織構造の設定（部門、グループ、ユーザー）
  5. SLAポリシーの設定
  6. 通知ルールの設定
  7. サービスカタログの定義
```

### インシデント管理の設定

```javascript
// Business Rule: インシデント作成時の自動分類
(function executeRule(current, previous) {
    // カテゴリに基づく優先度の自動設定
    if (current.category == 'network') {
        current.impact = 1;  // High
        current.urgency = 1; // High
    }

    // 割り当てグループの自動設定
    if (current.category == 'hardware') {
        current.assignment_group.setDisplayValue('Hardware Support');
    } else if (current.category == 'software') {
        current.assignment_group.setDisplayValue('Software Support');
    }

    // VIPユーザーの優先対応
    var user = new GlideRecord('sys_user');
    user.get(current.caller_id);
    if (user.vip == true) {
        current.priority = 1; // Critical
    }
})(current, previous);
```

### REST APIによるインシデント操作

```bash
# インシデントの作成
curl -X POST "https://instance.service-now.com/api/now/table/incident" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -u "admin:password" \
  -d '{
    "short_description": "メールサーバー障害",
    "description": "メール送受信が不能になっている",
    "category": "network",
    "impact": "1",
    "urgency": "1",
    "assignment_group": "Network Support",
    "caller_id": "user@example.com"
  }'

# インシデントの一覧取得
curl -X GET "https://instance.service-now.com/api/now/table/incident?sysparm_limit=10&sysparm_query=state=1" \
  -H "Accept: application/json" \
  -u "admin:password"

# インシデントの更新
curl -X PATCH "https://instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -u "admin:password" \
  -d '{
    "state": "2",
    "work_notes": "調査開始。ネットワーク機器のログを確認中。"
  }'

# インシデントのクローズ
curl -X PATCH "https://instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -u "admin:password" \
  -d '{
    "state": "7",
    "close_code": "Solved (Permanently)",
    "close_notes": "ネットワーク機器のファームウェア更新により解決"
  }'
```

### 変更管理のワークフロー

```
変更管理プロセス:
  1. 変更要求（RFC）の登録
     - 変更の種類: Standard / Normal / Emergency
     - 影響範囲の記述
     - リスクアセスメント

  2. 影響分析
     - CMDBからの依存関係確認
     - 影響を受けるCI（構成アイテム）の特定
     - サービス影響の評価

  3. 承認プロセス
     - 技術レビュー
     - CAB（変更諮問委員会）レビュー
     - マネージャー承認

  4. 実装
     - 実装計画の実行
     - バックアウトプランの準備
     - 変更の実施

  5. レビュー
     - PIR（実施後レビュー）
     - 成功/失敗の記録
     - 教訓の文書化
```

### Flow Designer による自動化例

```
フロー名: インシデント自動エスカレーション

トリガー:
  - テーブル: Incident
  - 条件: Priority = 1 (Critical) AND State = New
  - 30分以上未対応

アクション:
  1. Slackで通知
     - チャンネル: #incident-critical
     - メッセージ: "重大インシデント未対応: {incident.number}"

  2. メール送信
     - 宛先: ITマネージャー
     - 件名: "[緊急] 重大インシデント: {incident.short_description}"

  3. インシデント更新
     - エスカレーション: Level 2
     - 割り当てグループ: Senior Engineers

  4. PagerDutyでオンコール通知
     - サービス: Critical Infrastructure
```

### CMDB構成例

```
CI（構成アイテム）の階層構造:
  ビジネスサービス
    └── Webアプリケーション
        ├── Webサーバー (nginx)
        │   ├── サーバー: web-prod-01
        │   └── サーバー: web-prod-02
        ├── アプリケーションサーバー
        │   ├── サーバー: app-prod-01
        │   └── サーバー: app-prod-02
        ├── データベース (PostgreSQL)
        │   ├── サーバー: db-prod-01 (Primary)
        │   └── サーバー: db-prod-02 (Replica)
        └── ロードバランサー
            └── Azure Load Balancer
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **ITSM Standard** | 要問合せ | インシデント・問題・変更管理 |
| **ITSM Professional** | 要問合せ | Standard + パフォーマンス分析 |
| **ITSM Enterprise** | 要問合せ | Professional + AI/ML機能 |
| **Developer Instance** | 無料 | 個人学習・開発用 |

## メリット

### 主な利点

1. **ITIL準拠**: ITILフレームワークに完全対応
2. **統合プラットフォーム**: インシデント・変更・問題管理を一元化
3. **CMDB**: 構成管理データベースによるIT資産の可視化
4. **ワークフロー自動化**: Flow Designerによるノーコード自動化
5. **外部連携**: Integration Hubによる幅広いシステム連携
6. **スケーラビリティ**: エンタープライズ規模に対応
7. **SLA管理**: SLA目標の自動追跡と通知
8. **レポーティング**: ダッシュボードとレポート機能
9. **セルフサービス**: サービスカタログによるユーザー自律
10. **AI/ML**: 予測分析とインテリジェントな推奨

## デメリット

### 制約・課題

1. **高コスト**: エンタープライズ向けの高額ライセンス
2. **導入期間**: 初期導入に数ヶ月を要する場合がある
3. **学習曲線**: プラットフォームの習熟に時間が必要
4. **カスタマイズ複雑**: 高度なカスタマイズにはスクリプト知識が必要
5. **運用定着**: プロセス定着までに組織的な取り組みが必要
6. **過剰機能**: 小規模組織には機能過多
7. **ベンダーロックイン**: プラットフォーム固有の設定が多い
8. **パフォーマンス**: 大量データ時のレスポンス低下

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Jira Service Management** | Atlassian製ITSM | ServiceNowより軽量で安価 |
| **Zammad** | オープンソースヘルプデスク | 無料だが機能は限定的 |
| **Freshservice** | クラウドITSM | ServiceNowより安価で導入が容易 |
| **BMC Helix ITSM** | エンタープライズITSM | ServiceNowと同等の機能 |
| **ManageEngine** | IT管理プラットフォーム | 中小企業向けに強い |

## 公式リンク

- **公式サイト**: [https://www.servicenow.com/](https://www.servicenow.com/)
- **ドキュメント**: [https://docs.servicenow.com/](https://docs.servicenow.com/)
- **Developer**: [https://developer.servicenow.com/](https://developer.servicenow.com/)
- **コミュニティ**: [https://www.servicenow.com/community/](https://www.servicenow.com/community/)
- **Training**: [https://nowlearning.servicenow.com/](https://nowlearning.servicenow.com/)

## 関連ドキュメント

- [運用ITSM一覧](../運用ITSM/)
- [Zammad](./Zammad.md)
- [監視ロギング](../監視ロギング/)

---

**カテゴリ**: 運用ITSM
**対象工程**: 運用・保守
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
