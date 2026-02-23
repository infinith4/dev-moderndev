# OWASP ZAP (Zed Attack Proxy)

## 概要

OWASP ZAP（Zed Attack Proxy）は、OWASP（Open Web Application Security Project）が開発した、世界で最も広く使われているオープンソースのWebアプリケーション脆弱性スキャナーです。ペネトレーションテスト（侵入テスト）とセキュリティテストを自動化し、SQL Injection、XSS、CSRF等の一般的な脆弱性を検出します。初心者からセキュリティ専門家まで、幅広いユーザーに対応したGUIとCLIを提供し、CI/CDパイプラインへの統合も容易です。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **OWASP ZAP** | 🟢 無料 | オープンソース、無制限利用、Apache License 2.0 |

**注意**: OWASP ZAPは無料のオープンソースプロジェクトです。商用利用も制限なく可能です。

## メリット・デメリット

### メリット
- ✅ **無料**: オープンソース、商用利用も無料
- ✅ **OWASP Top 10対応**: 主要な脆弱性を包括的にスキャン
- ✅ **自動・手動両対応**: 自動スキャンと手動テストの両方が可能
- ✅ **使いやすいGUI**: 初心者でも使いやすいデスクトップアプリ
- ✅ **CI/CD統合**: コマンドライン/API経由でパイプライン統合可能
- ✅ **アクティブ/パッシブスキャン**: 両方のスキャンモードをサポート
- ✅ **プラグイン拡張**: 豊富なアドオンで機能拡張
- ✅ **レポート生成**: HTML/JSON/XML形式でレポート出力

### デメリット
- ❌ **誤検知**: 自動スキャンでfalse positiveが発生する場合がある
- ❌ **学習曲線**: 高度な機能を使いこなすには習熟が必要
- ❌ **パフォーマンス**: 大規模サイトのスキャンには時間がかかる
- ❌ **ネットワーク負荷**: スキャン中に対象システムに高負荷
- ❌ **複雑な認証**: 複雑な認証フローの設定が難しい場合も

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **9. テスト（アプリケーション）** | セキュリティテスト、脆弱性診断 | 脆弱性レポート、修正提案 |
| **10. テスト（インフラ）** | Webサーバー・APIのセキュリティ検証 | セキュリティ診断結果 |
| **11. 導入** | 本番環境のセキュリティチェック | セキュリティ監査レポート |

## 基本的な利用方法

### 1. インストール

```bash
# Docker版（最も簡単）
docker run -u zap -p 8080:8080 -p 8090:8090 \
  -i ghcr.io/zaproxy/zaproxy:stable zap-webswing.sh

# ブラウザでアクセス
# http://localhost:8080/zap

# Linux (Debian/Ubuntu)
wget https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0_Linux.tar.gz
tar -xvf ZAP_2.14.0_Linux.tar.gz
cd ZAP_2.14.0
./zap.sh

# macOS (Homebrew)
brew install --cask zap

# Windows
# https://www.zaproxy.org/download/ からインストーラーをダウンロード

# バージョン確認
zap.sh -version
```

### 2. 基本的な使い方（GUIモード）

#### 自動スキャン
1. ZAPを起動
2. "Automated Scan"タブを選択
3. 対象URLを入力（例: `http://localhost:3000`）
4. "Attack"ボタンをクリック
5. スキャン完了後、"Alerts"タブで脆弱性を確認

#### 手動スキャン
1. ZAPをプロキシとして設定（デフォルト: localhost:8080）
2. ブラウザのプロキシ設定をZAPに変更
3. ブラウザで対象サイトを操作
4. ZAPの"Sites"タブでサイト構造を確認
5. "Active Scan"を実行
6. 検出された脆弱性を"Alerts"タブで確認

### 3. コマンドライン（CLIモード）

```bash
# クイックスキャン
zap.sh -quickurl http://localhost:3000 -quickprogress

# ベースラインスキャン（受動的スキャン）
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://localhost:3000 -r baseline-report.html

# フルスキャン（能動的スキャン）
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t http://localhost:3000 -r full-scan-report.html

# APIスキャン
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t http://localhost:3000/openapi.json -f openapi -r api-report.html
```

## 工程別の活用方法

### 9. テスト（アプリケーション）での活用

**目的**: アプリケーションの脆弱性を検出、OWASP Top 10への対応確認

**活用方法**:
- 自動脆弱性スキャン
- 認証機能のセキュリティテスト
- セッション管理の検証
- 入力バリデーションのテスト

**実装例（認証付きサイトのスキャン）**:

#### GUIでの認証設定
```
1. ZAPを起動
2. ツールバー → Tools → Options → Authentication
3. 認証方法を選択:
   - Form-Based Authentication
   - Script-Based Authentication
   - JSON-Based Authentication
   - HTTP Authentication

4. フォームベース認証の設定例:
   - Login URL: http://localhost:3000/login
   - Login form parameters: username={%username%}&password={%password%}
   - Logged in indicator: <a href="/logout">Logout</a>
   - Logged out indicator: <form id="login">

5. ユーザー認証情報を追加:
   - Context → Users → Add
   - Username: testuser
   - Password: TestPass123!

6. 認証後にスキャンを実行
```

#### スクリプトでの自動化
```python
#!/usr/bin/env python
# zap_authenticated_scan.py

from zapv2 import ZAPv2
import time

# ZAP APIに接続
zap = ZAPv2(apikey='your-api-key', proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

target = 'http://localhost:3000'
login_url = f'{target}/login'
username = 'testuser'
password = 'TestPass123!'

# 1. 新しいセッションを開始
print('Creating new session...')
zap.core.new_session(name='authenticated_scan', overwrite=True)

# 2. 対象URLにアクセス
print(f'Accessing target {target}')
zap.urlopen(target)
time.sleep(2)

# 3. ログイン処理
print('Logging in...')
zap.urlopen(login_url)
time.sleep(2)

# POSTデータでログイン
login_data = f'username={username}&password={password}'
zap.core.send_request(
    url=login_url,
    method='POST',
    postdata=login_data
)
time.sleep(2)

# 4. スパイダー（クローリング）
print('Spidering target...')
scan_id = zap.spider.scan(target)
while int(zap.spider.status(scan_id)) < 100:
    print(f'Spider progress: {zap.spider.status(scan_id)}%')
    time.sleep(5)
print('Spider completed')

# 5. パッシブスキャン完了を待機
print('Waiting for passive scan...')
while int(zap.pscan.records_to_scan) > 0:
    print(f'Records to scan: {zap.pscan.records_to_scan}')
    time.sleep(5)
print('Passive scan completed')

# 6. アクティブスキャン
print('Active scanning target...')
scan_id = zap.ascan.scan(target)
while int(zap.ascan.status(scan_id)) < 100:
    print(f'Active scan progress: {zap.ascan.status(scan_id)}%')
    time.sleep(10)
print('Active scan completed')

# 7. アラート（脆弱性）を取得
print('\n--- Vulnerabilities Found ---')
alerts = zap.core.alerts(baseurl=target)

for alert in alerts:
    print(f"[{alert['risk']}] {alert['alert']}")
    print(f"  URL: {alert['url']}")
    print(f"  Description: {alert['description'][:100]}...")
    print()

# 8. HTMLレポート生成
print('Generating report...')
with open('zap-report.html', 'w') as f:
    f.write(zap.core.htmlreport())

print('Scan completed! Report saved to zap-report.html')
```

**CI/CD統合（GitHub Actions）**:
```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  zap_scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build application
        run: |
          npm ci
          npm run build

      - name: Start application
        run: |
          npm start &
          sleep 10

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.10.0
        with:
          target: 'http://localhost:3000'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: Upload ZAP Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: zap-scan-report
          path: report_html.html
```

**ZAPルール設定ファイル（.zap/rules.tsv）**:
```tsv
10202	IGNORE	(X-Frame-Options Header Not Set)
10021	WARN	(X-Content-Type-Options Header Missing)
10098	FAIL	(Cross-Domain Misconfiguration)
90022	FAIL	(Application Error Disclosure)
```

---

### 10. テスト（インフラ）での活用

**目的**: WebサーバーやAPIのセキュリティ設定検証

**活用方法**:
- HTTPヘッダーセキュリティチェック
- TLS/SSL設定の検証
- APIエンドポイントの脆弱性スキャン

**実装例（APIスキャン）**:
```bash
# OpenAPI仕様からAPIスキャン
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://api.example.com/openapi.json \
  -f openapi \
  -r api-security-report.html \
  -w api-security-report.md

# GraphQL APIスキャン
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://api.example.com/graphql \
  -f graphql \
  -r graphql-report.html
```

**セキュリティヘッダーチェックスクリプト**:
```python
#!/usr/bin/env python
# check_security_headers.py

from zapv2 import ZAPv2

zap = ZAPv2(apikey='your-api-key')

target = 'https://app.example.com'

# 対象URLにアクセス
zap.urlopen(target)

# セキュリティヘッダーのチェック
required_headers = {
    'X-Frame-Options': 'DENY or SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Strict-Transport-Security': 'max-age=31536000',
    'Content-Security-Policy': 'Required',
    'X-XSS-Protection': '1; mode=block',
}

print("Security Headers Check:")
print("-" * 60)

messages = zap.core.messages(baseurl=target)
if messages:
    headers = messages[0]['responseHeader']

    for header, expected in required_headers.items():
        if header.lower() in headers.lower():
            print(f"✓ {header}: Present")
        else:
            print(f"✗ {header}: Missing (Expected: {expected})")
```

---

### 11. 導入での活用

**目的**: 本番環境デプロイ前のセキュリティ検証

**活用方法**:
- 本番環境のセキュリティ監査
- デプロイ前のセキュリティチェック
- 定期的なセキュリティスキャン

**実装例（本番環境スキャン）**:
```bash
# ベースラインスキャン（低リスク）
docker run -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://app.example.com \
  -r production-baseline-report.html \
  -l PASS

# 定期スキャン（cron設定）
# 毎日午前3時に実行
0 3 * * * docker run -v /var/zap/reports:/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://app.example.com \
  -r daily-scan-$(date +\%Y\%m\%d).html
```

**Terraform統合（AWS Lambda でスケジュール実行）**:
```hcl
# lambda_zap_scan.tf
resource "aws_lambda_function" "zap_scan" {
  filename      = "zap_scan.zip"
  function_name = "zap-security-scan"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 900

  environment {
    variables = {
      TARGET_URL = "https://app.example.com"
      S3_BUCKET  = aws_s3_bucket.reports.id
    }
  }
}

# 毎日午前3時（UTC）に実行
resource "aws_cloudwatch_event_rule" "daily_scan" {
  name                = "daily-zap-scan"
  description         = "Trigger ZAP scan daily"
  schedule_expression = "cron(0 3 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.daily_scan.name
  target_id = "ZapScanLambda"
  arn       = aws_lambda_function.zap_scan.arn
}
```

## 公式ドキュメント

- [OWASP ZAP 公式サイト](https://www.zaproxy.org/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [ZAP API Documentation](https://www.zaproxy.org/docs/api/)
- [ZAP Docker Images](https://www.zaproxy.org/docs/docker/)
- [OWASP ZAP GitHub Repository](https://github.com/zaproxy/zaproxy)
- [ZAP Add-ons Marketplace](https://www.zaproxy.org/addons/)

## 学習リソース

### チュートリアル
- [Getting Started with ZAP](https://www.zaproxy.org/getting-started/)
- [ZAP Automation Framework](https://www.zaproxy.org/docs/automate/)
- [ZAP in Ten](https://www.alldaydevops.com/zap-in-ten) - 10分で学ぶZAP

### 書籍
- "OWASP ZAP Cookbook" by Simon Bennetts
- "Web Application Security Testing with ZAP" (OWASP)

### 動画・コース
- [OWASP ZAP Tutorial](https://www.youtube.com/results?search_query=owasp+zap+tutorial)
- [ZAP by Example](https://www.youtube.com/playlist?list=PLq9Ra239pNZaFZzqWyKuKRdH3P4aD9pzd)
- [Web Security Testing with OWASP ZAP](https://www.udemy.com/topic/owasp/)

### コミュニティ
- [OWASP ZAP User Group](https://groups.google.com/g/zaproxy-users)
- [OWASP ZAP GitHub Discussions](https://github.com/zaproxy/zaproxy/discussions)
- [Stack Overflow - OWASP ZAP](https://stackoverflow.com/questions/tagged/zap)

## 関連リンク

### 関連ツール
- [ZAP Python API Client](https://pypi.org/project/python-owasp-zap-v2.4/) - Python APIクライアント
- [ZAP Jenkins Plugin](https://plugins.jenkins.io/zap/) - Jenkins統合
- [ZAP GitHub Action](https://github.com/zaproxy/action-baseline) - GitHub Actions統合
- [ZAP Extensions](https://www.zaproxy.org/addons/) - アドオン一覧

### 他のセキュリティツール
- [Burp Suite](https://portswigger.net/burp) - 商用脆弱性スキャナー
- [Nikto](https://github.com/sullo/nikto) - Webサーバースキャナー
- [Arachni](https://www.arachni-scanner.com/) - Webアプリスキャナー
- [w3af](http://w3af.org/) - Web攻撃・監査フレームワーク

### ベストプラクティス
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Webアプリケーション脆弱性トップ10
- [ZAP Scanning Best Practices](https://www.zaproxy.org/docs/guides/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
