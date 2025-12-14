# Amazon CodeWhisperer

## 概要

**Amazon CodeWhisperer**は、AWS が提供するAI駆動のコード補完ツールです。機械学習モデルを使用して、コンテキストに基づいたコード提案をリアルタイムで提供し、開発者の生産性を向上させます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | AIコード補完・生成ツール |
| **ライセンス** | プロプライエタリ |
| **料金** | 🟡 一部無料（Individual Tier無料、Professional Tier有料）|
| **公式サイト** | https://aws.amazon.com/codewhisperer/ |
| **ドキュメント** | https://docs.aws.amazon.com/codewhisperer/ |

## 主な特徴

### 1. リアルタイムコード提案
- コンテキスト認識型のコード補完
- コメントや関数名から複数行のコード生成
- 自然言語コメントからのコード生成

### 2. セキュリティスキャン
- コード内の脆弱性を自動検出
- OWASP Top 10などのセキュリティベストプラクティスに基づくスキャン
- 修正案の提示

### 3. リファレンストラッキング
- 提案コードのオープンソース類似コードを検出
- ライセンス情報の表示
- コンプライアンスリスク軽減

### 4. 多言語・多IDEサポート
- **対応言語**: Python, Java, JavaScript, TypeScript, C#, Go, Rust, PHP, Ruby, Kotlin, C, C++, Shell scripting, SQL, Scala
- **対応IDE**: VS Code, IntelliJ IDEA, PyCharm, WebStorm, Rider, CLion, GoLand, Visual Studio, AWS Cloud9, JupyterLab

## 料金プラン

| プラン | 料金 | 機能 |
|--------|------|------|
| **Individual Tier** | 無料 | コード提案、セキュリティスキャン（月50スキャン） |
| **Professional Tier** | $19/ユーザー/月 | Individual機能 + 管理機能、SSO、無制限セキュリティスキャン |

## 使い方

### VS Codeへのインストール

```bash
# 1. VS Code拡張機能からインストール
# Marketplace: "AWS Toolkit" で検索してインストール

# 2. AWS認証情報の設定（AWS Builder IDまたはIAM Identity Center）
# VS Codeコマンドパレット (Ctrl+Shift+P / Cmd+Shift+P)
# > AWS: Sign in with AWS Builder ID

# 3. CodeWhispererを有効化
# Settings > Extensions > AWS Toolkit > CodeWhisperer: Enable
```

### 基本的な使い方

#### 1. 自動補完

```python
# コメントからコード生成
# Calculate the fibonacci sequence up to n

# Tab キーを押すと以下のようなコードが提案される:
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
```

#### 2. 関数名から実装生成

```java
// メソッド名を入力すると実装が提案される
public List<User> filterActiveUsers(List<User> users) {
    // Tab を押すと以下が提案される:
    return users.stream()
        .filter(user -> user.isActive())
        .collect(Collectors.toList());
}
```

#### 3. AWS SDK利用コード生成

```python
# AWS S3からファイルをダウンロードする関数
def download_from_s3(bucket_name, key, local_path):
    # CodeWhispererがAWS SDK使用例を提案
    import boto3
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, key, local_path)
```

### セキュリティスキャン

```bash
# VS Codeコマンドパレット
> CodeWhisperer: Run Security Scan

# スキャン結果が表示される:
# - High: SQL Injection vulnerability detected
# - Medium: Hardcoded credentials found
# - Low: Insecure random number generation
```

#### スキャン結果例

```python
# 脆弱性のあるコード
import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # CodeWhispererが警告: SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# CodeWhispererの修正提案
def get_user_safe(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # パラメータ化クエリを使用
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

### リファレンストラッキング

```json
// settings.json
{
    "aws.codeWhisperer.includeSuggestionsWithCodeReferences": true
}
```

```python
# 提案コードにオープンソース類似コードがある場合
# CodeWhispererが表示:
# Reference: MIT License - https://github.com/example/repo
def merge_sort(arr):
    # MIT License code here...
```

### エンタープライズ設定（Professional Tier）

```yaml
# AWS IAM Identity Center統合
# AWS Organizations経由で一元管理

# 管理者設定
codewhisperer:
  organization_id: "o-1234567890"
  sso_configuration:
    identity_source: "AWS IAM Identity Center"
  policies:
    - block_public_code_references: true
    - require_security_scan: true
  usage_analytics:
    enabled: true
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | コード生成・補完 | 開発速度向上、ボイラープレートコード生成 |
| **実装** | セキュリティ対策 | コーディング中の脆弱性検出 |
| **テスト** | テストコード生成 | ユニットテスト・統合テストのスケルトン生成 |

## メリット

- **生産性向上**: 繰り返し作業の自動化、ボイラープレートコード生成
- **無料枠が充実**: Individual Tierで基本機能を無料利用可能
- **セキュリティ統合**: コーディング中に脆弱性を検出・修正
- **AWS統合**: AWS SDKのベストプラクティスコードを提案
- **リファレンストラッキング**: ライセンスリスク管理
- **多言語対応**: 15以上のプログラミング言語をサポート
- **多IDE対応**: JetBrains全製品、VS Code、Visual Studioに対応

## デメリット

- **精度のばらつき**: 複雑なビジネスロジックでは提案精度が低い場合がある
- **AWS依存**: AWSアカウント・認証が必要
- **インターネット必須**: クラウドベースのため、オフライン動作不可
- **学習曲線**: 効果的な使用にはプロンプトエンジニアリング的な工夫が必要
- **コード品質の責任**: 生成コードのレビューは開発者の責任
- **プライバシー**: コードがAWSに送信される（Professional Tierで制御可能）

## 類似ツールとの比較

| ツール | 開発元 | 料金 | 特徴 |
|--------|--------|------|------|
| **Amazon CodeWhisperer** | AWS | 無料〜$19/月 | AWSサービス統合、セキュリティスキャン |
| **GitHub Copilot** | GitHub/Microsoft | $10/月 | 広範なトレーニングデータ、高精度 |
| **Cursor** | Cursor Inc. | 無料〜$20/月 | IDE統合型、チャット機能 |
| **Tabnine** | Tabnine | 無料〜$12/月 | オンプレミス対応、プライバシー重視 |

## ベストプラクティス

### 1. コメント駆動開発

```python
# Good: 詳細なコメントでより正確なコード生成
# Function to calculate compound interest
# Parameters: principal (float), rate (float), time (int), compounds_per_year (int)
# Returns: final amount (float)
def calculate_compound_interest(principal, rate, time, compounds_per_year):
    # CodeWhispererが完全な実装を提案
```

### 2. セキュリティスキャンの定期実行

```bash
# CI/CDパイプラインに組み込む
# .github/workflows/security-scan.yml
name: CodeWhisperer Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run CodeWhisperer Scan
        run: |
          # AWS CLIを使用してセキュリティスキャン実行
          aws codewhisperer start-code-analysis --source-code-path .
```

### 3. 提案コードのレビュー

```python
# 必ず生成コードをレビュー
def process_data(data):
    # CodeWhispererの提案を受け入れる前に:
    # 1. ロジックが正しいか確認
    # 2. エッジケースを考慮しているか確認
    # 3. パフォーマンスへの影響を確認
    # 4. セキュリティ問題がないか確認
```

### 4. チーム標準との整合性

```json
// .vscode/settings.json
{
    "aws.codeWhisperer.shareContentWithAWS": false,  // Professional Tierのみ
    "aws.codeWhisperer.includeSuggestionsWithCodeReferences": true,
    "aws.codeWhisperer.importRecommendation": {
        "enabled": true
    }
}
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/codewhisperer/
- **ドキュメント**: https://docs.aws.amazon.com/codewhisperer/
- **FAQ**: https://aws.amazon.com/codewhisperer/faqs/
- **ユーザーガイド**: https://docs.aws.amazon.com/codewhisperer/latest/userguide/
- **AWS Toolkit for VS Code**: https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-toolkit-vscode

## まとめ

Amazon CodeWhispererは、無料でも充実した機能を提供するAIコード補完ツールです。セキュリティスキャン、リファレンストラッキング、AWS統合などの独自機能により、開発生産性とコード品質の両面で貢献します。特にAWS環境での開発では、SDKのベストプラクティスコードを提案してくれるため、非常に有用です。

---

**最終更新**: 2025-12-06
**対象バージョン**: CodeWhisperer 2024
