# Zammad

## 概要

Zammadは、オープンソースのWebベースヘルプデスク・チケット管理システムです。メール、チャット、電話、SNS（Twitter/Facebook）などマルチチャネルからの問い合わせを統合管理し、チケットベースのワークフローで効率的なカスタマーサポートを実現します。ナレッジベース、SLA管理、REST API、LDAP/Active Directory連携など、エンタープライズ運用に必要な機能を備えつつ、Docker Composeによる簡単なセルフホスト展開が可能です。Ruby on Rails製でモダンなUIを提供し、中小規模から大規模組織まで幅広く対応します。

## 主な機能

### 1. チケット管理
- **チケットライフサイクル**: 作成・分類・割り当て・解決・クローズ
- **自動分類**: トリガーによる自動タグ付け・優先度設定
- **マージ**: 重複チケットの統合
- **テンプレート**: 定型回答テンプレート

### 2. マルチチャネル対応
- **メール**: IMAP/POP3によるメール取り込み
- **Webチャット**: リアルタイムチャットサポート
- **電話**: CTI連携による通話管理
- **SNS**: Twitter、Facebook連携
- **Webフォーム**: 問い合わせフォームの埋め込み

### 3. ナレッジベース
- **記事管理**: FAQ・ナレッジ記事の作成
- **カテゴリ**: 階層的なカテゴリ分類
- **検索**: 全文検索によるナレッジ検索
- **公開設定**: 内部/外部公開の制御

### 4. SLA管理
- **SLAポリシー**: 応答時間・解決時間の目標設定
- **エスカレーション**: SLA違反時の自動エスカレーション
- **カレンダー**: 営業時間カレンダーの設定
- **レポート**: SLA達成率のダッシュボード

### 5. 自動化・連携
- **トリガー**: 条件に基づく自動アクション
- **マクロ**: 複数操作のバッチ実行
- **Webhook**: 外部システムへの通知
- **REST API**: プログラムからの操作

### 6. ユーザー管理
- **組織管理**: 顧客組織の管理
- **ロール**: 権限ベースのアクセス制御
- **LDAP/AD**: Active Directory連携
- **SSO**: SAML/OAuth2によるシングルサインオン

## 利用方法

### Docker Composeによるインストール

```yaml
# docker-compose.yml
version: '3.8'

services:
  zammad-railsserver:
    image: ghcr.io/zammad/zammad:6.2.0
    restart: always
    depends_on:
      - zammad-memcached
      - zammad-postgresql
      - zammad-redis
    environment:
      - MEMCACHE_SERVERS=zammad-memcached:11211
      - POSTGRESQL_HOST=zammad-postgresql
      - POSTGRESQL_USER=zammad
      - POSTGRESQL_PASS=zammad
      - REDIS_URL=redis://zammad-redis:6379
    volumes:
      - zammad-storage:/opt/zammad/storage

  zammad-nginx:
    image: ghcr.io/zammad/zammad:6.2.0
    command: ["zammad-nginx"]
    restart: always
    depends_on:
      - zammad-railsserver
    ports:
      - "8080:8080"
    volumes:
      - zammad-storage:/opt/zammad/storage

  zammad-scheduler:
    image: ghcr.io/zammad/zammad:6.2.0
    command: ["zammad-scheduler"]
    restart: always
    depends_on:
      - zammad-memcached
      - zammad-railsserver
      - zammad-redis

  zammad-websocket:
    image: ghcr.io/zammad/zammad:6.2.0
    command: ["zammad-websocket"]
    restart: always
    depends_on:
      - zammad-memcached
      - zammad-railsserver
      - zammad-redis

  zammad-postgresql:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_USER=zammad
      - POSTGRES_PASSWORD=zammad
    volumes:
      - postgresql-data:/var/lib/postgresql/data

  zammad-memcached:
    image: memcached:1.6-alpine
    restart: always
    command: memcached -m 256

  zammad-redis:
    image: redis:7-alpine
    restart: always

volumes:
  zammad-storage:
  postgresql-data:
```

```bash
# 起動
docker compose up -d

# 初期セットアップ
# ブラウザで http://localhost:8080 にアクセス
# 管理者アカウントを作成
```

### REST APIによるチケット操作

```bash
# チケットの作成
curl -X POST "http://localhost:8080/api/v1/tickets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token token=YOUR_API_TOKEN" \
  -d '{
    "title": "ログインできない",
    "group": "Users",
    "customer": "customer@example.com",
    "article": {
      "subject": "ログインエラー",
      "body": "ログインページで認証エラーが発生します。",
      "type": "note",
      "internal": false
    },
    "priority_id": 2,
    "state_id": 1
  }'

# チケットの検索
curl -X GET "http://localhost:8080/api/v1/tickets/search?query=ログイン&limit=10" \
  -H "Authorization: Token token=YOUR_API_TOKEN"

# チケットの更新
curl -X PUT "http://localhost:8080/api/v1/tickets/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token token=YOUR_API_TOKEN" \
  -d '{
    "state_id": 2,
    "priority_id": 3
  }'

# チケットに記事を追加（返信）
curl -X POST "http://localhost:8080/api/v1/ticket_articles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token token=YOUR_API_TOKEN" \
  -d '{
    "ticket_id": 1,
    "subject": "Re: ログインエラー",
    "body": "調査した結果、パスワードリセットが必要です。",
    "type": "email",
    "internal": false
  }'

# ユーザーの一覧取得
curl -X GET "http://localhost:8080/api/v1/users?limit=20" \
  -H "Authorization: Token token=YOUR_API_TOKEN"
```

### トリガー（自動化ルール）の設定

```
トリガー例1: 高優先度チケットの自動通知
  条件:
    - チケット作成時
    - 優先度 = "高" または "緊急"
  アクション:
    - メール送信: サポートマネージャーに通知
    - タグ追加: "high-priority"
    - グループ割り当て: "Senior Support"

トリガー例2: 未回答チケットのエスカレーション
  条件:
    - チケット更新時
    - 状態 = "新規" かつ 作成から24時間経過
  アクション:
    - 優先度を1段階引き上げ
    - メール送信: チームリーダーに通知
    - 内部メモ追加: "24時間未対応のためエスカレーション"

トリガー例3: 自動クローズ
  条件:
    - チケット更新時
    - 状態 = "保留中" かつ 最終更新から7日経過
  アクション:
    - 状態変更: "クローズ"
    - メール送信: 顧客にクローズ通知
```

### SLA設定例

```
SLAポリシー: 標準サポート
  対象条件:
    - プラン: Standard
  応答時間:
    - 緊急: 1時間以内
    - 高:   4時間以内
    - 通常: 8時間以内
    - 低:   24時間以内
  解決時間:
    - 緊急: 4時間以内
    - 高:   8時間以内
    - 通常: 3営業日以内
    - 低:   5営業日以内
  営業時間:
    - 月〜金: 09:00-18:00（JST）
    - 祝日: 対象外
```

### メールチャネルの設定

```
メール設定手順:
  1. 管理画面 > チャネル > メール
  2. 受信設定（IMAP）
     - ホスト: imap.example.com
     - ポート: 993
     - SSL: 有効
     - ユーザー: support@example.com
     - パスワード: xxxxxxxx
  3. 送信設定（SMTP）
     - ホスト: smtp.example.com
     - ポート: 587
     - STARTTLS: 有効
     - ユーザー: support@example.com
  4. グループ割り当て: "1st Level Support"
  5. テスト送受信の確認
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Community（セルフホスト）** | 無料 | オープンソース、AGPL-3.0 License |
| **Hosted Starter** | EUR 5/エージェント/月 | クラウドホスティング |
| **Hosted Professional** | EUR 15/エージェント/月 | SSO、カスタムドメイン |
| **Hosted Plus** | EUR 24/エージェント/月 | LDAP、大容量ストレージ |

## メリット

### 主な利点

1. **オープンソース**: セルフホスト版が無料で利用可能
2. **マルチチャネル**: メール・チャット・電話・SNSの統合管理
3. **モダンUI**: 直感的で使いやすいWebインターフェース
4. **Docker対応**: Docker Composeによる簡単なデプロイ
5. **REST API**: プログラムからの完全な操作が可能
6. **ナレッジベース**: 組み込みのFAQ・ナレッジ管理
7. **SLA管理**: 応答時間・解決時間の自動追跡
8. **LDAP/SSO**: エンタープライズ認証との統合
9. **全文検索**: Elasticsearchベースの高速検索
10. **多言語対応**: 日本語を含む30以上の言語に対応

## デメリット

### 制約・課題

1. **大規模運用**: 数千エージェント規模では設計が必要
2. **プラグイン**: ServiceNow等と比較してエコシステムが小さい
3. **ITIL対応**: 変更管理・問題管理はITSM専用ツールが優れる
4. **カスタマイズ**: 高度なカスタマイズにはRuby on Rails知識が必要
5. **レポーティング**: 高度な分析にはBI連携が必要
6. **運用負荷**: セルフホスト版はインフラ管理が必要
7. **ドキュメント**: 日本語ドキュメントが限定的
8. **バージョンアップ**: メジャーアップデート時の移行作業

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **ServiceNow** | エンタープライズITSM | Zammadより高機能だが高コスト |
| **Jira Service Management** | Atlassian製ITSM | DevOps連携が強い |
| **Freshdesk** | クラウドヘルプデスク | Zammadより導入が容易 |
| **osTicket** | オープンソースチケットシステム | Zammadよりシンプル |
| **OTRS** | エンタープライズチケットシステム | Zammadより歴史が長い |
| **Zendesk** | クラウドカスタマーサービス | Zammadより機能豊富だが有償 |

## 公式リンク

- **公式サイト**: [https://zammad.com/](https://zammad.com/)
- **ドキュメント**: [https://docs.zammad.org/](https://docs.zammad.org/)
- **GitHub**: [https://github.com/zammad/zammad](https://github.com/zammad/zammad)
- **API ドキュメント**: [https://docs.zammad.org/en/latest/api/intro.html](https://docs.zammad.org/en/latest/api/intro.html)
- **Docker**: [https://docs.zammad.org/en/latest/install/docker-compose.html](https://docs.zammad.org/en/latest/install/docker-compose.html)

## 関連ドキュメント

- [運用ITSM一覧](../運用ITSM/)
- [ServiceNow](./ServiceNow.md)

---

**カテゴリ**: 運用ITSM
**対象工程**: 運用・保守
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
