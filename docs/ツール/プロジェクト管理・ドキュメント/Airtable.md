# Airtable

## 概要

**Airtable**は、スプレッドシートのシンプルさとデータベースの強力さを組み合わせたクラウドベースのコラボレーションプラットフォームです。ノーコード/ローコードでワークフロー・プロジェクト管理・タスク管理を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Airtable, Inc. |
| **種別** | クラウドデータベース・プロジェクト管理ツール |
| **ライセンス** | プロプライエタリ |
| **料金** | 🟡 一部無料（Free: 無料、Plus: $10/月、Pro: $20/月、Enterprise: 要問合せ） |
| **公式サイト** | https://airtable.com/ |
| **ドキュメント** | https://support.airtable.com/ |

## 主な特徴

### 1. スプレッドシート + データベース
- スプレッドシートのような直感的UI
- リレーショナルデータベース機能（テーブル間リンク）
- 複数ビュー（Grid、Kanban、Calendar、Gallery、Form）

### 2. 豊富なフィールドタイプ
- テキスト、数値、日付
- 添付ファイル、チェックボックス、ドロップダウン
- リンク（他テーブルへの参照）
- ロールアップ（集計）、ルックアップ（参照）
- フォーミュラ（計算式）

### 3. 自動化（Automation）
- トリガー: レコード作成/更新、条件一致
- アクション: メール送信、Slack通知、レコード作成
- スケジュール実行

### 4. API・統合
- RESTful API
- Zapier、Make（Integromat）統合
- JavaScript拡張（Scripting Extensions）

## 使い方

### 基本的なプロジェクト管理ベース作成

#### 1. ベース作成（GUI操作）

**テーブル構成例（タスク管理）**:

| フィールド名 | タイプ | 説明 |
|-------------|--------|------|
| Task Name | Single line text | タスク名 |
| Assignee | Linked to Users | 担当者（Usersテーブルへのリンク） |
| Status | Single select | 未着手/進行中/完了 |
| Priority | Single select | 高/中/低 |
| Due Date | Date | 期日 |
| Attachments | Attachments | ファイル添付 |
| Notes | Long text | 詳細メモ |

**Usersテーブル**:

| フィールド名 | タイプ | 説明 |
|-------------|--------|------|
| Name | Single line text | ユーザー名 |
| Email | Email | メールアドレス |
| Tasks | Linked from Tasks | タスク一覧（逆リンク） |

#### 2. ビュー設定

**Kanbanビュー**:
- Group by: Status
- カード表示: Task Name, Assignee, Due Date

**Calendarビュー**:
- 日付フィールド: Due Date
- カード表示: Task Name, Assignee

**Galleryビュー**:
- カード表示: Attachments（サムネイル）

### フォーミュラの活用

```javascript
// 期日が過ぎているかチェック
IF(
  AND(
    {Due Date},
    IS_BEFORE({Due Date}, TODAY()),
    {Status} != "完了"
  ),
  "⚠️ 遅延",
  "✅ OK"
)

// タスク優先度に基づくスコア計算
SWITCH(
  {Priority},
  "高", 3,
  "中", 2,
  "低", 1,
  0
)

// 担当者名の表示（リンクフィールドから）
{Assignee} & ""  # 配列を文字列に変換
```

### Automation設定

#### 例1: タスク完了時にSlack通知

```yaml
# Automation設定（GUI操作）
Trigger:
  Type: When record matches conditions
  Conditions:
    - Field: Status
    - Condition: is
    - Value: 完了

Actions:
  - Type: Send Slack message
    Channel: #project-updates
    Message: |
      ✅ タスクが完了しました！
      タスク名: {Task Name}
      担当者: {Assignee}
```

#### 例2: 期日前日にメールリマインダー

```yaml
Trigger:
  Type: At scheduled time
  Time: Daily at 9:00 AM

Actions:
  - Type: Find records
    Conditions:
      - {Due Date} = DATEADD(TODAY(), 1, 'days')
      - {Status} != "完了"

  - Type: Send email
    To: {Assignee.Email}
    Subject: タスク期日リマインダー
    Message: |
      明日が期日のタスクがあります:
      - {Task Name}
      期日: {Due Date}
```

### API操作

#### Node.js でのAPI使用

```javascript
// airtable-example.js
const Airtable = require('airtable');

// 認証設定
const base = new Airtable({apiKey: 'YOUR_API_KEY'}).base('YOUR_BASE_ID');

// レコード一覧取得
base('Tasks').select({
    maxRecords: 10,
    view: "Grid view",
    filterByFormula: "{Status} = '進行中'"
}).eachPage(function page(records, fetchNextPage) {
    records.forEach(function(record) {
        console.log('Retrieved', record.get('Task Name'));
    });
    fetchNextPage();
}, function done(err) {
    if (err) { console.error(err); return; }
});

// レコード作成
base('Tasks').create([
  {
    "fields": {
      "Task Name": "新しいタスク",
      "Status": "未着手",
      "Priority": "中",
      "Due Date": "2025-12-31"
    }
  }
], function(err, records) {
  if (err) {
    console.error(err);
    return;
  }
  records.forEach(function (record) {
    console.log(record.getId());
  });
});

// レコード更新
base('Tasks').update([
  {
    "id": "recXXXXXXXXXXXXXX",
    "fields": {
      "Status": "完了"
    }
  }
], function(err, records) {
  if (err) {
    console.error(err);
    return;
  }
  records.forEach(function(record) {
    console.log(record.get('Task Name'));
  });
});
```

#### Python でのAPI使用

```python
# airtable_example.py
from pyairtable import Api

api = Api('YOUR_API_KEY')
table = api.table('YOUR_BASE_ID', 'Tasks')

# レコード一覧取得
records = table.all(formula="{Status} = '進行中'")
for record in records:
    print(record['fields']['Task Name'])

# レコード作成
new_record = table.create({
    'Task Name': '新しいタスク',
    'Status': '未着手',
    'Priority': '中'
})
print(f"Created: {new_record['id']}")

# レコード更新
table.update('recXXXXXXXXXXXXXX', {
    'Status': '完了'
})
```

### フォーム機能

```markdown
# Airtable Form（GUI操作）

1. ビューで「Form」を選択
2. フォームフィールドを設定:
   - Task Name（必須）
   - Assignee
   - Priority
   - Due Date
   - Notes
3. 公開設定:
   - 共有リンク生成
   - Webサイトに埋め込み可能

# フォーム送信後の動作設定
- 送信完了メッセージのカスタマイズ
- 自動返信メール送信（Automation連携）
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **企画** | アイデア管理 | 機能要件・ユーザーストーリー管理 |
| **要件定義** | 要件管理 | 要件トラッキング、優先度付け |
| **実装** | タスク管理 | スプリント管理、バグトラッキング |
| **テスト** | テスト管理 | テストケース管理、結果記録 |
| **導入** | リリース管理 | デプロイチェックリスト管理 |

## メリット

- **直感的UI**: スプレッドシートライクで学習コストが低い
- **柔軟性**: データベース構造を自由に設計可能
- **リッチなフィールドタイプ**: 添付ファイル、リンク、計算式など豊富
- **複数ビュー**: Grid、Kanban、Calendar、Galleryで多角的に表示
- **自動化**: ノーコードでワークフロー自動化
- **API完備**: 外部システムとの統合が容易
- **コラボレーション**: リアルタイム共同編集

## デメリット

- **有料プラン必要**: 本格利用にはPlus以上が必要
- **パフォーマンス**: 大量データ（50,000レコード超）では遅延
- **複雑なクエリ制限**: SQLのような複雑なクエリは困難
- **オフライン非対応**: インターネット必須
- **ベンダーロックイン**: データエクスポートは可能だがプラットフォーム依存
- **レコード制限**: Freeプランは1,200レコード/ベースまで

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Airtable** | データベース+スプレッドシート、ノーコード | 無料〜$20/月 | 柔軟なデータ管理・プロジェクト管理 |
| **Notion** | ドキュメント+データベース、All-in-One | 無料〜$10/月 | ナレッジベース・プロジェクト管理 |
| **Monday.com** | ワークマネジメント、ビジュアル | $8/月〜 | プロジェクト管理・タスク管理 |
| **Asana** | タスク管理特化 | 無料〜$24.99/月 | タスク・プロジェクト管理 |

## ベストプラクティス

### 1. テーブル設計の正規化

```text
# 良い設計例
Tasks Table:
  - Task Name
  - Assignee (Link to Users)
  - Project (Link to Projects)
  - Status

Users Table:
  - Name
  - Email
  - Tasks (Link from Tasks)

Projects Table:
  - Project Name
  - Tasks (Link from Tasks)

# 悪い設計例（非正規化）
Tasks Table:
  - Task Name
  - Assignee Name（テキスト）  # 更新時に全レコード変更必要
  - Assignee Email（テキスト）
  - Project Name（テキスト）
```

### 2. ビューの活用

```text
# 複数ビューで異なる視点を提供
- Grid View: 全データ一覧
- Kanban View (Status別): タスク進捗管理
- Calendar View (Due Date): スケジュール確認
- Gallery View (Assignee別): 担当者別タスク
- Form View: 外部からのタスク登録
```

### 3. フィルタ・ソートのプリセット

```text
# よく使うフィルタを保存
- "私のタスク": Assignee = Current User
- "今週期限": Due Date is within 1 week from now
- "遅延タスク": Due Date < Today AND Status != 完了
```

### 4. Zapier連携

```yaml
# Zapier Zap例: GitHub Issue → Airtable
Trigger:
  App: GitHub
  Event: New Issue

Action:
  App: Airtable
  Action: Create Record
  Table: Tasks
  Fields:
    Task Name: {issue.title}
    Notes: {issue.body}
    Status: 未着手
    Priority: 中
```

## 公式リソース

- **公式サイト**: https://airtable.com/
- **ヘルプセンター**: https://support.airtable.com/
- **テンプレート**: https://airtable.com/templates
- **API ドキュメント**: https://airtable.com/developers/web/api/introduction
- **コミュニティ**: https://community.airtable.com/

## まとめ

Airtableは、スプレッドシートの直感性とデータベースの強力さを兼ね備えたプラットフォームです。ノーコード/ローコードで柔軟なデータ管理・プロジェクト管理が可能で、API統合により外部システムとの連携も容易です。中小規模のプロジェクト管理やデータ管理に最適で、複数ビューによる多角的なデータ可視化が魅力です。

---

**最終更新**: 2025-12-06
**対象プラン**: Free / Plus / Pro / Enterprise
