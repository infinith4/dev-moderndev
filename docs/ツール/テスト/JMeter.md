# Apache JMeter

## 概要

Apache JMeterは、Webアプリケーション、APIのパフォーマンステスト・負荷テストを実行するオープンソースツールです。Java製のデスクトップアプリケーションとして動作し、HTTP、HTTPS、SOAP、REST、FTP、データベース、JMS、LDAPなど多様なプロトコルに対応します。GUI でテストシナリオを作成し、数千の同時リクエストをシミュレートして、システムの性能限界や応答時間を測定できます。

## 主な機能

### 1. パフォーマンステスト
- 負荷テスト（Load Testing）
- ストレステスト（Stress Testing）
- スパイクテスト（Spike Testing）
- 耐久テスト（Endurance Testing）

### 2. 多様なプロトコル対応
- **HTTP/HTTPS**: Web、REST API
- **SOAP/XML-RPC**: Webサービス
- **FTP**: ファイル転送
- **JDBC**: データベース
- **JMS**: メッセージキュー
- **LDAP**: ディレクトリサービス
- **TCP/UDP**: ネットワークプロトコル

### 3. テストシナリオ作成
- Thread Group（仮想ユーザー）
- Samplers（リクエスト）
- Logic Controllers（条件分岐、ループ）
- Timers（待機時間）
- Assertions（検証）
- Listeners（結果表示）

### 4. 分散テスト
- 複数マシンからの並列実行
- マスター・スレーブ構成
- 大規模負荷生成

### 5. レポート・可視化
- グラフ表示（応答時間、スループット）
- HTML レポート生成
- ログファイル（CSV、XML、JSON）
- リアルタイムモニタリング

### 6. 拡張性
- プラグインエコシステム
- カスタムSamplers作成
- BeanShell/Groovyスクリプト

## 利用方法

### インストール

```bash
# Java 8以上必須
java -version

# JMeterダウンロード（公式サイトから）
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
cd apache-jmeter-5.6.3/bin

# GUI起動
./jmeter

# CLI実行
./jmeter -n -t test.jmx -l results.jtl
```

### 基本テストプラン作成

```
1. Test Plan作成
   右クリック → Add → Threads → Thread Group
   - Number of Threads (users): 100
   - Ramp-Up Period (seconds): 10
   - Loop Count: 10

2. HTTP Request追加
   Thread Group右クリック → Add → Sampler → HTTP Request
   - Server Name: api.example.com
   - Port: 443
   - Protocol: https
   - Path: /api/users
   - Method: GET

3. HTTP Header Manager追加（必要に応じて）
   HTTP Request右クリック → Add → Config Element → HTTP Header Manager
   - Content-Type: application/json
   - Authorization: Bearer <token>

4. Assertion追加（検証）
   HTTP Request右クリック → Add → Assertions → Response Assertion
   - Response Code: 200

5. Listener追加（結果表示）
   Thread Group右クリック → Add → Listener
   - View Results Tree（詳細表示）
   - Summary Report（サマリー）
   - Aggregate Report（集計）
   - Graph Results（グラフ）

6. テスト実行
   上部メニュー → Run → Start
```

### REST APIテスト例

```
Thread Group:
  - 100 threads
  - Ramp-up: 10秒
  - Loop: 10回

HTTP Request Sampler:
  - POST /api/users
  - Body Data:
    {
      "name": "${__RandomString(10)}",
      "email": "${__RandomString(10)}@example.com"
    }

HTTP Header Manager:
  - Content-Type: application/json

JSON Assertion:
  - $.id exists
  - $.name matches pattern

Response Time Assertion:
  - Response time <= 500ms
```

### CSV データ駆動テスト

```
1. CSV Data Set Config追加
   Thread Group右クリック → Add → Config Element → CSV Data Set Config
   - Filename: users.csv
   - Variable Names: username,password

2. HTTP Request で変数使用
   - Path: /login
   - Body:
     {
       "username": "${username}",
       "password": "${password}"
     }

# users.csv
username,password
user1,pass1
user2,pass2
user3,pass3
```

### CLI実行（CI/CD統合）

```bash
# テスト実行
jmeter -n -t test.jmx -l results.jtl -e -o report_folder

# オプション:
# -n: Non-GUI モード
# -t: テストプランファイル
# -l: 結果ファイル
# -e: HTML レポート生成
# -o: レポート出力フォルダ

# プロパティ上書き
jmeter -n -t test.jmx -l results.jtl \
  -Jusers=200 -Jrampup=20 -Jduration=300
```

## CI/CD統合

### GitHub Actions

```yaml
name: Performance Test

on: [push]

jobs:
  performance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          java-version: '11'
      
      - name: Download JMeter
        run: |
          wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar -xzf apache-jmeter-5.6.3.tgz
      
      - name: Run JMeter Test
        run: |
          apache-jmeter-5.6.3/bin/jmeter -n \
            -t tests/performance.jmx \
            -l results/results.jtl \
            -e -o results/report
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: jmeter-report
          path: results/report
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Apache JMeter** | 🟢 無料 | オープンソース、全機能利用可能 |

## メリット

### ✅ 主な利点

1. **無料**: オープンソース、Apache License 2.0
2. **多様なプロトコル**: HTTP、SOAP、FTP、JDBC、JMS等
3. **GUI**: 視覚的なテストシナリオ作成
4. **分散テスト**: 複数マシンからの負荷生成
5. **拡張性**: プラグインエコシステム
6. **クロスプラットフォーム**: Windows、Mac、Linux
7. **CI/CD統合**: CLI モードで自動化可能
8. **レポート**: HTML レポート自動生成
9. **成熟**: 20年以上の開発・利用実績
10. **コミュニティ**: 豊富な情報・プラグイン

## デメリット

### ❌ 制約・課題

1. **UI古い**: Swing ベースの古いインターフェース
2. **学習曲線**: 多機能なため初心者には難しい
3. **リソース消費**: Javaアプリのためメモリ使用量大
4. **モダンプロトコル**: WebSocket、gRPCは標準非対応（プラグイン必要）
5. **リアルユーザー挙動**: ブラウザレンダリング非対応
6. **動的コンテンツ**: JavaScript実行は別ツール必要
7. **設定複雑**: 高度なシナリオは設定が煩雑
8. **デバッグ困難**: エラー特定に時間がかかる

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Gatling** | Scala、DSLベース、モダンレポート | JMeterよりコードベース |
| **k6** | JavaScript、CLI重視、Grafana統合 | JMeterよりモダン、軽量 |
| **Locust** | Python、分散テスト | JMeterより簡単、柔軟 |
| **Artillery** | Node.js、YAML設定 | JMeterよりシンプル |
| **Apache Bench (ab)** | 軽量、CLI | JMeterより機能限定的 |

## 公式リンク

- **公式サイト**: [https://jmeter.apache.org/](https://jmeter.apache.org/)
- **ダウンロード**: [https://jmeter.apache.org/download_jmeter.cgi](https://jmeter.apache.org/download_jmeter.cgi)
- **ドキュメント**: [https://jmeter.apache.org/usermanual/](https://jmeter.apache.org/usermanual/)
- **プラグイン**: [https://jmeter-plugins.org/](https://jmeter-plugins.org/)
- **GitHub**: [https://github.com/apache/jmeter](https://github.com/apache/jmeter)

## 関連ドキュメント

- [テストツール一覧](../テストツール/)
- [Gatling](./Gatling.md)
- [Locust](./Locust.md)
- [k6](./k6.md)
- [パフォーマンステストベストプラクティス](../../best-practices/performance-testing.md)

---

**カテゴリ**: テストツール  
**対象工程**: テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
