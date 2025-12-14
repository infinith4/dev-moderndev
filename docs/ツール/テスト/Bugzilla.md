# Bugzilla

## 概要

**Bugzilla**は、Mozilla Foundationが開発したオープンソースのバグトラッキングシステムです。1998年の誕生以来、エンタープライズ環境で広く採用され、高度なカスタマイズ性、ワークフロー管理、豊富な検索・レポート機能により、大規模プロジェクトのバグ管理を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Mozilla Foundation / オープンソースコミュニティ |
| **種別** | バグトラッキングシステム |
| **ライセンス** | Mozilla Public License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://www.bugzilla.org/ |
| **ドキュメント** | https://bugzilla.readthedocs.io/ |

## 主な特徴

### 1. バグトラッキング
- **バグライフサイクル**: 新規→確認→担当→修正中→解決→検証→終了
- **優先度・重要度**: 5段階管理
- **製品・コンポーネント**: 階層的分類
- **バージョン・マイルストーン**: リリース管理

### 2. 高度な検索
- **詳細検索**: 複数フィールド組み合わせ
- **保存された検索**: 頻繁に使う検索条件保存
- **Boolean Charts**: 複雑な論理条件
- **全文検索**: コメント・添付ファイル検索

### 3. ワークフロー・カスタマイズ
- **カスタムフィールド**: プロジェクト固有の項目追加
- **ワークフロー設定**: ステータス遷移のカスタマイズ
- **権限管理**: グループベースのアクセス制御
- **カスタムスキン**: UI変更

### 4. 統合・自動化
- **Email通知**: バグ更新時の自動通知
- **REST API**: プログラマティックアクセス
- **WebServices（XML-RPC）**: レガシーAPI
- **外部ツール連携**: Git、Jenkins等

## 使い方

### セットアップ

#### Linux（Ubuntu/Debian）インストール

```bash
# 依存パッケージインストール
sudo apt update
sudo apt install -y \
    apache2 \
    mysql-server \
    perl \
    libcgi-pm-perl \
    libdbd-mysql-perl \
    libdatetime-timezone-perl \
    libtemplate-perl \
    libemail-sender-perl \
    libgd-perl \
    libchart-perl \
    libxml-twig-perl \
    libjson-rpc-perl \
    libtest-taint-perl \
    libhtml-scrubber-perl

# Bugzillaダウンロード
cd /var/www
sudo wget https://ftp.mozilla.org/pub/mozilla.org/webtools/bugzilla-5.0.6.tar.gz
sudo tar -xzf bugzilla-5.0.6.tar.gz
sudo mv bugzilla-5.0.6 bugzilla
cd bugzilla

# Perlモジュール確認・インストール
sudo ./checksetup.pl --check-modules
sudo ./install-module.pl --all

# データベース作成
sudo mysql -u root -p
CREATE DATABASE bugs CHARACTER SET utf8mb4;
GRANT ALL PRIVILEGES ON bugs.* TO 'bugs'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
EXIT;

# Bugzilla設定
sudo vi localconfig
# $db_name = 'bugs';
# $db_user = 'bugs';
# $db_pass = 'your_password';
# $webservergroup = 'www-data';

# セットアップ実行
sudo ./checksetup.pl

# 管理者アカウント作成（対話式）
# Email: admin@example.com
# Real Name: Administrator
# Password: ********

# Apache設定
sudo vi /etc/apache2/sites-available/bugzilla.conf
```

```apache
# /etc/apache2/sites-available/bugzilla.conf
<VirtualHost *:80>
    ServerName bugzilla.example.com
    DocumentRoot /var/www/bugzilla

    <Directory /var/www/bugzilla>
        AddHandler cgi-script .cgi
        Options +ExecCGI +FollowSymLinks
        DirectoryIndex index.cgi index.html
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/bugzilla-error.log
    CustomLog ${APACHE_LOG_DIR}/bugzilla-access.log combined
</VirtualHost>
```

```bash
# Apache設定有効化
sudo a2ensite bugzilla
sudo a2enmod cgi headers expires rewrite
sudo systemctl restart apache2

# ブラウザでアクセス
# http://bugzilla.example.com
```

#### Docker で起動

```yaml
# docker-compose.yml
version: '3.8'

services:
  bugzilla:
    image: bugzilla/bugzilla:latest
    ports:
      - "80:80"
    environment:
      - BUGZILLA_ADMIN_EMAIL=admin@example.com
      - BUGZILLA_ADMIN_PASSWORD=admin123
      - DB_HOST=mysql
      - DB_NAME=bugs
      - DB_USER=bugs
      - DB_PASS=bugs_password
    volumes:
      - bugzilla-data:/var/www/html/bugzilla/data
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=bugs
      - MYSQL_USER=bugs
      - MYSQL_PASSWORD=bugs_password
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  bugzilla-data:
  mysql-data:
```

```bash
docker-compose up -d
# http://localhost にアクセス
```

### バグ登録

```text
# Webインターフェース

1. ログイン
   - Email: user@example.com
   - Password: ********

2. File a Bug（バグ登録）
   - Product: MyWebApp
   - Component: Frontend
   - Version: 1.0
   - Severity: Major（重大）
   - Priority: P2（高）
   - Platform: All
   - OS: All
   - Summary: ログイン画面でパスワードが表示される
   - Description:
     再現手順:
     1. ログイン画面を開く
     2. パスワードを入力
     3. パスワードが平文で表示される

     期待値: パスワードは***で表示されるべき
     実際の結果: 平文で表示される

   - Assigned To: developer@example.com

3. Submit Bug
```

### バグ検索

```text
# 簡易検索
Summary: ログイン
Status: NEW, ASSIGNED, REOPENED
Product: MyWebApp

# 詳細検索（Advanced Search）
- Status: NEW, CONFIRMED
- Priority: P1, P2
- Assigned To: developer@example.com
- Changed: Last 7 days
- Keywords: security

# Boolean Chart（複雑な条件）
(Priority = P1 OR Priority = P2)
AND
(Status = NEW OR Status = CONFIRMED)
AND
Product = MyWebApp

# 検索結果保存
Save Search → Name: "High Priority Bugs"
→ Footer Link（ホーム画面にリンク表示）
```

### ワークフロー

```text
# バグライフサイクル

NEW（新規）
 ↓
CONFIRMED（確認済み）←────┐
 ↓                        │
ASSIGNED（担当割当）       │
 ↓                        │
IN_PROGRESS（作業中）      │
 ↓                        │
RESOLVED（解決）           │
 ├─ FIXED（修正済み）      │
 ├─ INVALID（無効）        │
 ├─ WONTFIX（修正しない）  │
 ├─ DUPLICATE（重複）      │
 └─ WORKSFORME（再現せず） │
  ↓                       │
VERIFIED（検証済み）       │
 ↓                        │
CLOSED（クローズ）         │
                          │
REOPENED（再オープン）─────┘
```

### REST API

#### Python でのバグ操作

```python
# bugzilla_api.py
import requests
from requests.auth import HTTPBasicAuth

BUGZILLA_URL = "https://bugzilla.example.com"
API_KEY = "your-api-key"  # User Preferences → API Keys

def get_bug(bug_id):
    """バグ情報取得"""
    url = f"{BUGZILLA_URL}/rest/bug/{bug_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

def create_bug(product, component, summary, description):
    """バグ作成"""
    url = f"{BUGZILLA_URL}/rest/bug"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "product": product,
        "component": component,
        "summary": summary,
        "description": description,
        "version": "1.0",
        "severity": "normal",
        "priority": "P2"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def update_bug(bug_id, status=None, comment=None):
    """バグ更新"""
    url = f"{BUGZILLA_URL}/rest/bug/{bug_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {}
    if status:
        data["status"] = status
    if comment:
        data["comment"] = {"body": comment}

    response = requests.put(url, headers=headers, json=data)
    return response.json()

def search_bugs(product, status=None):
    """バグ検索"""
    url = f"{BUGZILLA_URL}/rest/bug"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"product": product}
    if status:
        params["status"] = status

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 使用例
bug = get_bug(123)
print(f"Bug #{bug['bugs'][0]['id']}: {bug['bugs'][0]['summary']}")

new_bug = create_bug(
    product="MyWebApp",
    component="Backend",
    summary="API timeout error",
    description="API request times out after 30 seconds"
)
print(f"Created bug #{new_bug['id']}")

update_bug(123, status="RESOLVED", comment="Fixed in commit abc123")

bugs = search_bugs(product="MyWebApp", status=["NEW", "CONFIRMED"])
print(f"Found {len(bugs['bugs'])} open bugs")
```

### CI/CD統合

#### Jenkins連携

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Update Bugzilla') {
            steps {
                script {
                    // コミットメッセージからバグID抽出
                    def commitMsg = sh(
                        returnStdout: true,
                        script: 'git log -1 --pretty=%B'
                    ).trim()

                    def bugId = (commitMsg =~ /Bug (\d+)/)[0][1]

                    // Bugzilla APIでバグ更新
                    sh """
                        curl -X PUT \
                          -H "Authorization: Bearer ${BUGZILLA_API_KEY}" \
                          -H "Content-Type: application/json" \
                          -d '{"comment": {"body": "Fixed in build #${BUILD_NUMBER}"}}' \
                          https://bugzilla.example.com/rest/bug/${bugId}
                    """
                }
            }
        }
    }
}
```

#### Git フック

```bash
# .git/hooks/commit-msg

#!/bin/bash
# コミットメッセージにバグIDを強制

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Bug #123 形式をチェック
if ! echo "$commit_msg" | grep -qE "^Bug #[0-9]+"; then
    echo "Error: Commit message must start with 'Bug #<id>'"
    echo "Example: Bug #123 Fix login issue"
    exit 1
fi

# Bugzilla APIで存在チェック（オプション）
bug_id=$(echo "$commit_msg" | grep -oE "Bug #[0-9]+" | grep -oE "[0-9]+")
status_code=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $BUGZILLA_API_KEY" \
    "https://bugzilla.example.com/rest/bug/$bug_id")

if [ "$status_code" != "200" ]; then
    echo "Error: Bug #$bug_id does not exist in Bugzilla"
    exit 1
fi
```

### レポート

```text
# レポート機能

1. バグチャート（Graphical Reports）
   - 時系列グラフ
   - 製品別集計
   - ステータス別集計
   - 担当者別集計

2. ピボットテーブル
   - 2次元集計
   - 製品×優先度
   - コンポーネント×重要度

3. カスタムレポート
   - SQL直接実行（管理者のみ）
   - CSV/JSON/XML エクスポート
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | 要望管理 | Severity: Enhancement |
| **設計** | 設計レビュー課題 | 設計変更要求 |
| **実装** | 実装課題 | 実装タスク管理 |
| **テスト** | バグ管理 | 不具合追跡・修正管理 |
| **運用** | 本番障害管理 | 本番環境不具合追跡 |

## メリット

- **オープンソース**: 無料、カスタマイズ可能
- **高機能**: 20年以上の実績、エンタープライズ対応
- **柔軟なワークフロー**: プロジェクトに合わせた設定
- **強力な検索**: Boolean Charts、全文検索
- **REST API**: 自動化・ツール連携
- **セルフホスト**: オンプレミス運用可能

## デメリット

- **UI古い**: モダンなUIではない
- **学習曲線**: 設定項目が多く、初期設定複雑
- **パフォーマンス**: 大規模データで遅延
- **モダンツール比較**: Jira、GitHub Issues等に比べ機能劣る
- **メンテナンスコスト**: サーバー運用・バージョンアップ必要

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Bugzilla** | オープンソース、高機能 | 無料 | オンプレミス、レガシー環境 |
| **Jira** | モダン、Atlassian統合 | 有料 | エンタープライズ、アジャイル |
| **GitHub Issues** | Git統合、シンプル | 無料 | GitHub利用環境 |
| **Redmine** | プロジェクト管理統合 | 無料 | 日本で人気、オンプレミス |

## ベストプラクティス

### 1. 製品・コンポーネント構成

```text
# 階層的製品構成

Product: MyWebApp
├── Component: Frontend
│   ├── Login
│   ├── Dashboard
│   └── Settings
├── Component: Backend
│   ├── API
│   ├── Database
│   └── Authentication
└── Component: Infrastructure
    ├── CI/CD
    ├── Deployment
    └── Monitoring
```

### 2. カスタムフィールド

```text
# プロジェクト固有フィールド追加

- Test Environment（選択式）: Dev, Staging, Production
- Customer Impact（数値）: 1-5
- Root Cause（テキスト）: 分析結果
- Release Note（チェックボックス）: リリースノート記載要否
```

### 3. ワークフロー設定

```text
# カスタムワークフロー

NEW → TRIAGED（トリアージ済み）→ IN_PROGRESS → CODE_REVIEW → RESOLVED
```

### 4. 通知設定

```text
# Email通知最適化

個人設定:
- 自分が担当: すべて通知
- 自分がCC: 重要な変更のみ
- 自分が報告: ステータス変更のみ

グローバル設定:
- P1バグ: 全員に通知
- セキュリティバグ: セキュリティチームに通知
```

## 公式リソース

- **公式サイト**: https://www.bugzilla.org/
- **ドキュメント**: https://bugzilla.readthedocs.io/
- **REST API**: https://bugzilla.readthedocs.io/en/latest/api/
- **インストールガイド**: https://bugzilla.readthedocs.io/en/latest/installing/
- **GitHub**: https://github.com/bugzilla/bugzilla

## まとめ

Bugzillaは、Mozilla Foundationが開発したオープンソースのバグトラッキングシステムです。1998年以来、エンタープライズ環境で広く採用され、高度なカスタマイズ性、ワークフロー管理、豊富な検索・レポート機能により、大規模プロジェクトのバグ管理を実現します。無料でセルフホスト可能なため、オンプレミス環境やレガシーシステムでのバグ管理に最適です。

---

**最終更新**: 2025-12-06
**対象バージョン**: Bugzilla 5.0+
