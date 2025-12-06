# Jira

## 概要

Jiraは、Atlassian製のプロジェクト管理・課題追跡ツールです。Issue管理、スクラムボード、カンバンボード、ロードマップ、レポート、カスタムワークフローにより、アジャイル開発・プロジェクト管理を支援します。エンタープライズ採用、Confluence・Bitbucket統合で広く使用されています。

## 主な機能

### 1. Issue管理
- **Issue タイプ**: Story、Bug、Task、Epic
- **カスタムフィールド**: フィールド追加
- **優先度**: Highest、High、Medium、Low
- **ステータス**: To Do、In Progress、Done

### 2. アジャイルボード
- **スクラムボード**: スプリント管理
- **カンバンボード**: フロー管理
- **バックログ**: バックログ管理
- **バーンダウン**: バーンダウンチャート

### 3. ワークフロー
- **カスタムワークフロー**: ステータス遷移
- **自動化**: トリガー・アクション
- **通知**: Email・Slack通知
- **SLA**: サービスレベル

### 4. レポート
- **ベロシティ**: ベロシティチャート
- **バーンダウン**: バーンダウンチャート
- **累積フロー**: CFD
- **カスタムレポート**: ダッシュボード

## 利用方法

### プロジェクト作成

```
Jira > Projects > Create project

Template:
- Scrum: スクラム開発
- Kanban: カンバン
- Bug tracking: バグ管理

Project name: My Project
Project key: MP

Create
```

### Issue作成

```
Create > Issue

Project: My Project
Issue Type: Story / Bug / Task
Summary: ユーザーログイン機能実装
Description:
- ログインフォーム作成
- 認証API実装
- セッション管理

Assignee: @user
Priority: High
Labels: frontend, authentication
Sprint: Sprint 1

Create
```

### スクラムボード

```
Boards > My Project Board

Backlog:
- Issue をドラッグ&ドロップでスプリントに追加

Sprint:
1. Start Sprint
2. Sprint期間: 2 weeks
3. Sprint goal: ユーザー認証機能完成

Board:
- To Do: 未着手
- In Progress: 作業中
- In Review: レビュー中
- Done: 完了

Complete Sprint:
- 完了Issueをクローズ
- 未完了Issueを次スプリントに移動
```

### カンバンボード

```
Boards > Kanban Board

Columns:
- To Do
- In Progress
- In Review
- Done

WIP Limits:
- In Progress: Max 5
- In Review: Max 3

Issue移動:
ドラッグ&ドロップでステータス変更
```

### JQL（Jira Query Language）

```
# 自分にアサインされた未完了Issue
assignee = currentUser() AND status != Done

# 優先度Highの未完了Bug
type = Bug AND priority = High AND status != Done

# 今週更新されたIssue
updated >= startOfWeek()

# 特定Sprintの全Issue
sprint = "Sprint 1"

# 複合条件
project = MP AND assignee = currentUser() AND status IN ("To Do", "In Progress") ORDER BY priority DESC

# ラベル検索
labels = "frontend" AND sprint in openSprints()
```

### カスタムフィールド

```
Settings > Issues > Custom fields

Add custom field:
- Field type: Text Field / Number / Date / Select List
- Name: Story Points
- Description: Estimated effort
- Context: All projects

Configure:
- Add to screens
- Set default value
```

### ワークフロー

```
Settings > Issues > Workflows

Create workflow:
1. Statuses:
   - To Do
   - In Progress
   - In Review
   - Done
   - Blocked

2. Transitions:
   - To Do → In Progress (Start Progress)
   - In Progress → In Review (Submit for Review)
   - In Review → In Progress (Request Changes)
   - In Review → Done (Approve)
   - Any → Blocked

3. Conditions:
   - Only assignee can transition

4. Validators:
   - Required fields

5. Post Functions:
   - Assign to reviewer
   - Send notification
```

### Automation

```
Settings > System > Automation

Create rule:

Trigger:
- Issue created
- Status changed
- Field value changed

Conditions:
- Issue type = Bug
- Priority = High

Actions:
- Assign to @lead
- Send Slack notification
- Add comment
```

### Jira API（REST）

```bash
# Issue取得
curl -u user@example.com:api_token \
  -X GET \
  "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123"

# Issue作成
curl -u user@example.com:api_token \
  -X POST \
  -H "Content-Type: application/json" \
  "https://your-domain.atlassian.net/rest/api/3/issue" \
  -d '{
    "fields": {
      "project": {"key": "MP"},
      "summary": "New bug found",
      "description": "Bug description",
      "issuetype": {"name": "Bug"}
    }
  }'

# Issue更新
curl -u user@example.com:api_token \
  -X PUT \
  -H "Content-Type: application/json" \
  "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123" \
  -d '{
    "fields": {
      "summary": "Updated summary"
    }
  }'
```

### Python統合

```python
from jira import JIRA

# 接続
jira = JIRA(
    server='https://your-domain.atlassian.net',
    basic_auth=('user@example.com', 'api_token')
)

# Issue検索
issues = jira.search_issues('assignee = currentUser() AND status != Done')
for issue in issues:
    print(f"{issue.key}: {issue.fields.summary}")

# Issue作成
new_issue = jira.create_issue(
    project='MP',
    summary='New feature request',
    description='Feature description',
    issuetype={'name': 'Story'}
)

# Issue更新
issue = jira.issue('MP-123')
issue.update(summary='Updated summary', assignee={'name': 'user'})

# コメント追加
jira.add_comment(issue, 'This is a comment')

# トランジション
jira.transition_issue(issue, 'In Progress')
```

### GitHub統合

```
Jira > Apps > GitHub for Jira

Connect GitHub:
1. Install GitHub App
2. Select repositories
3. Authorize

Commit message:
git commit -m "MP-123 Fix login bug"

Pull Request:
Title: MP-123 Implement user authentication
→ Jira Issue に自動リンク

Smart Commits:
git commit -m "MP-123 #comment Fixed the bug #time 2h #close"
```

### Confluence統合

```
Jira Issue > More > Link Confluence page

Create Confluence page:
- Requirements: MP-123
- Design Doc: MP-123
- Meeting Notes: Sprint Planning

Jira Issue に Confluence リンク表示
```

### Slack統合

```
Slack > Apps > Jira Cloud

/jira connect

/jira create
→ Jiraモーダルで Issue作成

/jira subscribe MP
→ チャンネルにプロジェクト通知

Issue更新通知:
#channel に自動投稿
```

### ダッシュボード

```
Dashboards > Create dashboard

Gadgets:
- Filter Results: JQL クエリ結果
- Sprint Burndown: バーンダウンチャート
- Velocity Chart: ベロシティ
- Pie Chart: Issue統計
- Activity Stream: 最近のアクティビティ

配置:
ドラッグ&ドロップで配置

共有:
Share > Team/Public
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** | 🟢 無料 | 10ユーザーまで |
| **Standard** | 💰 $7.75/ユーザー/月 | 250GBストレージ、サポート |
| **Premium** | 💰 $15.25/ユーザー/月 | 無制限ストレージ、高度機能 |
| **Enterprise** | 💰 要問い合わせ | 無制限インスタンス、24/7サポート |

## メリット

1. **無料枠**: 10ユーザーまで無料
2. **アジャイル**: スクラム・カンバン対応
3. **カスタマイズ**: 高度なカスタマイズ
4. **統合**: GitHub、Slack、Confluence
5. **エンタープライズ**: 大規模対応

## デメリット

1. **複雑性**: 学習曲線steep
2. **重い**: UIパフォーマンス
3. **高コスト**: 大規模で高額
4. **カスタマイズ**: 過度なカスタマイズで複雑化

## 公式リンク

- **公式サイト**: [https://www.atlassian.com/software/jira](https://www.atlassian.com/software/jira)
- **ドキュメント**: [https://support.atlassian.com/jira/](https://support.atlassian.com/jira/)

## 関連ドキュメント

- [プロジェクト管理ツール一覧](../プロジェクト管理ツール/)
- [Confluence](../ドキュメントツール/Confluence.md)
- [Trello](./Trello.md)

---

**カテゴリ**: プロジェクト管理ツール
**対象工程**: プロジェクト管理・Issue管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
