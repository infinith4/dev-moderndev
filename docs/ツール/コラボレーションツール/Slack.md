# Slack

## 概要

Slackは、ビジネスコミュニケーションプラットフォームです。チャンネルベース、ダイレクトメッセージ、ファイル共有、検索、2000+統合（GitHub、JIRA、Google Drive）、Slack App、Workflowにより、チームコラボレーション・リモートワークを効率化します。Salesforce買収、エンタープライズ採用で広く使用されています。

## 主な機能

### 1. チャンネル
- **パブリックチャンネル**: オープンチャンネル
- **プライベートチャンネル**: 限定メンバー
- **スレッド**: 返信スレッド
- **検索**: 全文検索

### 2. メッセージ
- **ダイレクトメッセージ**: DM
- **メンション**: @user、@channel
- **リアクション**: 絵文字リアクション
- **リマインダー**: /remind

### 3. ファイル共有
- **アップロード**: ファイル・画像
- **プレビュー**: ファイルプレビュー
- **共有**: チャンネル・DM

### 4. 統合
- **2000+アプリ**: GitHub、JIRA等
- **Webhook**: カスタム通知
- **Slack App**: カスタムアプリ
- **Workflow**: 自動化

## 利用方法

### 基本操作

```
# チャンネル作成
+ > Create a channel
Channel name: project-alpha
Description: Project Alpha discussions

# ユーザー招待
@username を入力

# メンション
@user: 特定ユーザー
@channel: チャンネル全員
@here: オンライン全員

# リマインダー
/remind me to check email at 3pm
/remind @user about meeting tomorrow
```

### Slash Commands

```
# メッセージ
/msg @user Hello!
/dm @user Private message

# ステータス
/status :house: Working from home

# リマインダー
/remind me to send report in 2 hours
/remind list

# その他
/away: 離席設定
/dnd: 通知オフ
/search: 検索
```

### Workflow Builder

```
ワークフロー例:

1. 新メンバーオンボーディング
   - トリガー: 新メンバー追加
   - アクション: ウェルカムメッセージ送信
   - アクション: オンボーディングチャンネルに招待

2. 定期アンケート
   - トリガー: スケジュール（毎週金曜）
   - アクション: チームにアンケート送信
   - アクション: 回答を集計チャンネルに投稿

3. GitHub通知
   - トリガー: Webhook
   - アクション: PRレビュー依頼をチャンネルに投稿
```

### GitHub統合

```
# GitHub App インストール
Slack > Apps > GitHub

# リポジトリ連携
/github subscribe owner/repo

# 通知設定
/github subscribe owner/repo reviews comments

# PR通知
/github subscribe owner/repo pulls

# Issue通知
/github subscribe owner/repo issues
```

### JIRA統合

```
# JIRA Cloud App インストール
Slack > Apps > Jira Cloud

# 接続
/jira connect

# Issue作成
/jira create

# 通知設定
/jira subscribe PROJECT-KEY
```

### Google Drive統合

```
# Google Drive App インストール
Slack > Apps > Google Drive

# ファイル共有
Google Driveファイルリンクを貼り付け
→ プレビュー表示

# 検索
/gdrive search [keyword]
```

### カスタムWebhook

```bash
# Incoming Webhook URL取得
Slack > Apps > Incoming Webhooks
Add to Slack

# cURLで送信
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "Hello from webhook!",
    "channel": "#general",
    "username": "Bot",
    "icon_emoji": ":robot_face:"
  }'
```

### Slack API（Python）

```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="xoxb-your-token")

try:
    # メッセージ送信
    response = client.chat_postMessage(
        channel="#general",
        text="Hello from Python!"
    )
    print(f"Message sent: {response['ts']}")

    # ファイルアップロード
    response = client.files_upload(
        channels="#general",
        file="./report.pdf",
        title="Monthly Report"
    )

    # チャンネル一覧
    response = client.conversations_list()
    channels = response['channels']
    for channel in channels:
        print(f"{channel['name']}: {channel['id']}")

except SlackApiError as e:
    print(f"Error: {e.response['error']}")
```

### Slack Bot（Node.js）

```javascript
const { App } = require('@slack/bolt')

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET
})

// メッセージリスニング
app.message('hello', async ({ message, say }) => {
  await say(`Hey there <@${message.user}>!`)
})

// Slash Command
app.command('/greet', async ({ command, ack, say }) => {
  await ack()
  await say(`Hello, <@${command.user_id}>!`)
})

// ボタンクリック
app.action('approve_button', async ({ ack, say }) => {
  await ack()
  await say('Request approved!')
})

// イベントリスニング
app.event('app_mention', async ({ event, say }) => {
  await say(`Thanks for mentioning me, <@${event.user}>!`)
})

;(async () => {
  await app.start(process.env.PORT || 3000)
  console.log('⚡️ Bolt app is running!')
})()
```

### Interactive Messages

```javascript
// ボタン付きメッセージ
const { WebClient } = require('@slack/web-api')

const client = new WebClient(process.env.SLACK_BOT_TOKEN)

await client.chat.postMessage({
  channel: '#general',
  text: 'Approval required',
  blocks: [
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: '*Deployment Request*\nDeploy version 1.2.3 to production?'
      }
    },
    {
      type: 'actions',
      elements: [
        {
          type: 'button',
          text: {
            type: 'plain_text',
            text: 'Approve'
          },
          style: 'primary',
          value: 'approve',
          action_id: 'approve_button'
        },
        {
          type: 'button',
          text: {
            type: 'plain_text',
            text: 'Reject'
          },
          style: 'danger',
          value: 'reject',
          action_id: 'reject_button'
        }
      ]
    }
  ]
})
```

### CI/CD通知（GitHub Actions）

```yaml
# .github/workflows/notify-slack.yml
name: Slack Notification

on:
  push:
    branches: [ main ]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Slack Notification
        uses: rtCamp/action-slack-notify@v2
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          SLACK_CHANNEL: '#deployments'
          SLACK_COLOR: ${{ job.status }}
          SLACK_MESSAGE: 'Deployed to production'
          SLACK_TITLE: 'Deployment Success'
          SLACK_USERNAME: 'GitHub Actions'
```

### Block Kit

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Deployment Status"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Environment:*\nProduction"
        },
        {
          "type": "mrkdwn",
          "text": "*Status:*\n:white_check_mark: Success"
        }
      ]
    },
    {
      "type": "divider"
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Deployed by: @user | Time: 2025-12-06 10:00"
        }
      ]
    }
  ]
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** | 🟢 無料 | 90日履歴、10統合 |
| **Pro** | 💰 $7.25/月 | 無制限履歴、無制限統合 |
| **Business+** | 💰 $12.50/月 | SAML SSO、24/7サポート |
| **Enterprise Grid** | 💰 要問い合わせ | 無制限ワークスペース |

## メリット

1. **無料枠**: 小規模チーム無料
2. **統合**: 2000+アプリ統合
3. **検索**: 強力な検索機能
4. **リモートワーク**: 非同期コミュニケーション
5. **カスタマイズ**: Bot・Workflow

## デメリット

1. **通知過多**: 通知管理難しい
2. **有料機能**: 履歴・統合制限
3. **学習曲線**: 多機能で複雑
4. **依存**: Slack依存リスク

## 公式リンク

- **公式サイト**: [https://slack.com/](https://slack.com/)
- **API ドキュメント**: [https://api.slack.com/](https://api.slack.com/)

## 関連ドキュメント

- [コラボレーションツール一覧](../コラボレーションツール/)
- [Microsoft Teams](./Microsoft_Teams.md)
- [Discord](./Discord.md)

---

**カテゴリ**: コラボレーションツール
**対象工程**: チームコミュニケーション
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
