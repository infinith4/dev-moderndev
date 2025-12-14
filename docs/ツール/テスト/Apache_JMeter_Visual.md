# Apache JMeter（GUI版）

## 概要

**Apache JMeter**は、オープンソースの負荷テスト・パフォーマンステストツールです。GUI版は、直感的なテストシナリオ設計と結果の可視化を提供し、Webアプリケーション、API、データベースなど様々なプロトコルの負荷テストに対応します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Apache Software Foundation |
| **種別** | 負荷テスト・パフォーマンステストツール |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://jmeter.apache.org/ |
| **ドキュメント** | https://jmeter.apache.org/usermanual/index.html |

## 主な特徴

### 1. 多様なプロトコルサポート
- HTTP/HTTPS（Web、RESTful API）
- SOAP / XML-RPC
- FTP、JDBC（データベース）
- LDAP、SMTP、POP3、IMAP
- TCP、Java Objects

### 2. GUI ベースのテスト設計
- ドラッグ&ドロップでテストシナリオ作成
- リアルタイムレスポンス確認
- グラフィカルな結果表示（グラフ、テーブル、ツリー）

### 3. 分散負荷テスト
- マスター/スレーブ構成で大規模負荷生成
- 複数マシンからの同時実行

### 4. 拡張性
- プラグインエコシステム（JMeter Plugins）
- カスタムサンプラー・リスナー開発可能

## 使い方

### インストール

```bash
# Java 8以上が必要
java -version

# JMeterダウンロード・解凍（macOS/Linux）
wget https://downloads.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
cd apache-jmeter-5.6.3

# GUI起動
./bin/jmeter

# Windows
# apache-jmeter-5.6.3\bin\jmeter.bat をダブルクリック
```

### 基本的なHTTP負荷テストシナリオ

#### 1. テストプラン作成

**GUIで操作**:

1. **Thread Group追加**
   - Test Plan右クリック → Add → Threads (Users) → Thread Group
   - 設定:
     - Number of Threads: 100（同時ユーザー数）
     - Ramp-Up Period: 10（10秒で100ユーザーに到達）
     - Loop Count: 10（各スレッドが10回実行）

2. **HTTP Request追加**
   - Thread Group右クリック → Add → Sampler → HTTP Request
   - 設定:
     - Server Name: example.com
     - Path: /api/users
     - Method: GET

3. **リスナー追加（結果確認用）**
   - Thread Group右クリック → Add → Listener → View Results Tree
   - Thread Group右クリック → Add → Listener → Summary Report
   - Thread Group右クリック → Add → Listener → Graph Results

4. **実行**
   - メニュー: Run → Start
   - リアルタイムで結果を確認

#### 2. JMXファイル（テストプラン保存形式）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="API Load Test">
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="BASE_URL" elementType="Argument">
            <stringProp name="Argument.name">BASE_URL</stringProp>
            <stringProp name="Argument.value">https://api.example.com</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="User Thread Group">
        <intProp name="ThreadGroup.num_threads">100</intProp>
        <intProp name="ThreadGroup.ramp_time">10</intProp>
        <longProp name="ThreadGroup.duration">60</longProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <intProp name="LoopController.loops">-1</intProp>
        </elementProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="GET /users">
          <stringProp name="HTTPSampler.domain">${BASE_URL}</stringProp>
          <stringProp name="HTTPSampler.path">/api/users</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
        </HTTPSamplerProxy>
        <hashTree>
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP Header Manager">
            <collectionProp name="HeaderManager.headers">
              <elementProp name="" elementType="Header">
                <stringProp name="Header.name">Content-Type</stringProp>
                <stringProp name="Header.value">application/json</stringProp>
              </elementProp>
            </collectionProp>
          </HeaderManager>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### 認証を含むAPIテスト

#### OAuth 2.0 Bearer Token

**GUIで設定**:

1. **HTTP Header Manager追加**
   - HTTP Request右クリック → Add → Config Element → HTTP Header Manager
   - Add:
     - Name: Authorization
     - Value: Bearer ${ACCESS_TOKEN}

2. **User Defined Variables（変数定義）**
   - Test Plan右クリック → Add → Config Element → User Defined Variables
   - Add:
     - Name: ACCESS_TOKEN
     - Value: your_actual_token_here

#### Basic認証

```xml
<!-- HTTP Authorization Manager -->
<AuthManager guiclass="AuthPanel" testclass="AuthManager" testname="HTTP Authorization Manager">
  <collectionProp name="AuthManager.auth_list">
    <elementProp name="" elementType="Authorization">
      <stringProp name="Authorization.url">https://api.example.com</stringProp>
      <stringProp name="Authorization.username">testuser</stringProp>
      <stringProp name="Authorization.password">testpass</stringProp>
      <stringProp name="Authorization.domain"></stringProp>
      <stringProp name="Authorization.realm"></stringProp>
    </elementProp>
  </collectionProp>
</AuthManager>
```

### アサーション（検証）追加

**GUIで設定**:

1. **Response Assertion追加**
   - HTTP Request右クリック → Add → Assertions → Response Assertion
   - 設定:
     - Field to Test: Response Code
     - Pattern Matching Rules: Equals
     - Patterns to Test: 200

2. **JSON Assertion追加**
   - HTTP Request右クリック → Add → Assertions → JSON Assertion
   - 設定:
     - Assert JSON Path exists: $.data[0].id

### リスナーの種類

| リスナー | 用途 | 表示内容 |
|---------|------|---------|
| **View Results Tree** | 詳細確認 | リクエスト/レスポンスの詳細 |
| **Summary Report** | サマリー確認 | 平均レスポンスタイム、スループット |
| **Aggregate Report** | 集計レポート | パーセンタイル、エラー率 |
| **Graph Results** | グラフ表示 | レスポンスタイムのグラフ |
| **Response Time Graph** | 時系列グラフ | 時系列でのレスポンスタイム推移 |

### 非GUIモード（本番負荷テスト推奨）

```bash
# CLI実行（GUIよりリソース消費が少ない）
jmeter -n -t test_plan.jmx -l results.jtl -e -o ./report

# オプション:
# -n: 非GUIモード
# -t: テストプランファイル
# -l: 結果ファイル
# -e: テスト終了後にHTMLレポート生成
# -o: HTMLレポート出力ディレクトリ
```

### 分散負荷テスト

#### マスターノード設定

```bash
# jmeter.properties編集
remote_hosts=slave1.example.com:1099,slave2.example.com:1099

# マスターから実行
jmeter -n -t test_plan.jmx -R slave1.example.com,slave2.example.com -l results.jtl
```

#### スレーブノード起動

```bash
# 各スレーブマシンで実行
jmeter-server
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **テスト** | 負荷テスト | Webアプリケーション・API性能評価 |
| **テスト** | ストレステスト | システム限界確認 |
| **導入** | 本番前性能検証 | リリース前の最終負荷テスト |

## メリット

- **無料・オープンソース**: ライセンス費用不要
- **GUIで直感的**: プログラミング不要でテスト作成
- **多様なプロトコル対応**: HTTP以外にもFTP、JDBC等サポート
- **拡張性**: プラグインで機能追加可能
- **クロスプラットフォーム**: Windows、macOS、Linux対応
- **分散テスト対応**: 大規模負荷生成可能
- **詳細なレポート**: HTMLレポート自動生成

## デメリット

- **GUI実行時のリソース消費**: 大規模テストには非GUIモード推奨
- **学習曲線**: 高度な機能習得に時間がかかる
- **リアルブラウザ非対応**: JavaScriptレンダリングには制限（Selenium連携で対応可能）
- **設定ファイルの複雑性**: JMXファイルは手動編集が困難
- **同時接続数限界**: 単一マシンでの限界あり（分散テストで対応）

## 類似ツールとの比較

| ツール | 料金 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **Apache JMeter** | 無料 | GUI、多様なプロトコル | 汎用負荷テスト |
| **Gatling** | 無料〜有料 | Scalaベース、コードベース | 開発者向け、CI/CD統合 |
| **k6** | 無料〜有料 | JavaScriptベース、軽量 | 開発者向け、クラウドネイティブ |
| **LoadRunner** | 有料 | エンタープライズ機能 | 大規模エンタープライズ |

## ベストプラクティス

### 1. 本番テストは非GUIモード

```bash
# GUI: テストシナリオ作成・デバッグ用
# 非GUI: 本番負荷テスト用（リソース効率的）
jmeter -n -t production_load_test.jmx -l results.jtl -e -o report/
```

### 2. 段階的負荷増加

```xml
<!-- Ultimate Thread Group使用（プラグイン） -->
<!-- 段階的に負荷を増やして限界点を特定 -->
```

### 3. リスナーの最小化

```xml
<!-- 本番テストではView Results Treeを無効化（リソース削減） -->
<!-- Summary Reportのみ有効化 -->
```

### 4. CI/CDパイプライン統合

```yaml
# .github/workflows/performance-test.yml
name: Performance Test
on: [push]
jobs:
  jmeter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run JMeter
        run: |
          wget https://downloads.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar -xzf apache-jmeter-5.6.3.tgz
          apache-jmeter-5.6.3/bin/jmeter -n -t test_plan.jmx -l results.jtl
      - name: Check Performance
        run: |
          # 平均レスポンスタイムが500ms以下か確認
          avg=$(awk -F',' 'NR>1 {sum+=$2; count++} END {print sum/count}' results.jtl)
          if (( $(echo "$avg > 500" | bc -l) )); then
            echo "Performance degradation detected: ${avg}ms"
            exit 1
          fi
```

## 公式リソース

- **公式サイト**: https://jmeter.apache.org/
- **ユーザーマニュアル**: https://jmeter.apache.org/usermanual/index.html
- **プラグインサイト**: https://jmeter-plugins.org/
- **GitHub**: https://github.com/apache/jmeter
- **チュートリアル**: https://jmeter.apache.org/usermanual/build-web-test-plan.html

## まとめ

Apache JMeterのGUI版は、負荷テストシナリオの設計と結果の可視化に優れたツールです。無料で多機能、プロトコル対応も豊富なため、幅広いプロジェクトで採用されています。GUIで直感的にテストを作成し、本番テストは非GUIモードで実行することで、効率的なパフォーマンステストが実現できます。

---

**最終更新**: 2025-12-06
**対象バージョン**: Apache JMeter 5.6+
