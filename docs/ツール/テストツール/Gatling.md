# Gatling

## 概要

Gatlingは、高性能な負荷テスト・パフォーマンステストツールです。Scala/JavaのDSLでテストシナリオを記述し、非同期アーキテクチャにより少ないリソースで大量の同時ユーザーをシミュレートできます。美しく詳細なHTMLレポートを自動生成し、CI/CDパイプラインとのシームレスな統合により、継続的なパフォーマンステストを実現します。

## 主な機能

### 1. 高性能
- 非同期I/O（Akka、Netty）
- 少ないリソースで大量負荷生成
- 効率的なメモリ使用

### 2. DSLベースシナリオ
- Scala DSL（読みやすい）
- Java DSL（Javaユーザー向け）
- レコーダー（ブラウザ操作記録）

### 3. プロトコル対応
- HTTP/HTTPS
- WebSocket
- Server-Sent Events (SSE)
- JMS
- MQTT（プラグイン）

### 4. 美しいレポート
- インタラクティブHTMLレポート
- 応答時間グラフ
- パーセンタイル分布
- リクエスト統計

### 5. CI/CD統合
- Maven/Gradleプラグイン
- Jenkins統合
- GitLab CI/GitHub Actions対応

### 6. リアルタイムモニタリング
- Grafana/InfluxDB統合
- リアルタイムメトリクス
- カスタムダッシュボード

## 利用方法

### セットアップ（Maven）

```xml
<!-- pom.xml -->
<dependencies>
  <dependency>
    <groupId>io.gatling.highcharts</groupId>
    <artifactId>gatling-charts-highcharts</artifactId>
    <version>3.10.3</version>
    <scope>test</scope>
  </dependency>
</dependencies>

<plugin>
  <groupId>io.gatling</groupId>
  <artifactId>gatling-maven-plugin</artifactId>
  <version>4.7.0</version>
</plugin>
```

### 基本シナリオ（Scala DSL）

```scala
// src/test/scala/simulations/BasicSimulation.scala
package simulations

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class BasicSimulation extends Simulation {
  
  // HTTPプロトコル設定
  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
    .header("User-Agent", "Gatling")
  
  // シナリオ定義
  val scn = scenario("Basic Load Test")
    .exec(
      http("Get Users")
        .get("/api/users")
        .check(status.is(200))
    )
    .pause(1)
    .exec(
      http("Get User Details")
        .get("/api/users/1")
        .check(status.is(200))
        .check(jsonPath("$.name").exists)
    )
  
  // 負荷設定
  setUp(
    scn.inject(
      atOnceUsers(10),              // 10ユーザーを即座に
      rampUsers(100).during(60.seconds)  // 100ユーザーを60秒かけて
    )
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.max.lt(2000),  // 最大応答時間2秒以下
     global.successfulRequests.percent.gt(95)  // 成功率95%以上
   )
}
```

### 認証・セッション管理

```scala
val scn = scenario("Authenticated API Test")
  .exec(
    http("Login")
      .post("/auth/login")
      .body(StringBody("""{"username":"user","password":"pass"}"""))
      .asJson
      .check(status.is(200))
      .check(jsonPath("$.token").saveAs("authToken"))
  )
  .exec(
    http("Get Protected Resource")
      .get("/api/protected")
      .header("Authorization", "Bearer ${authToken}")
      .check(status.is(200))
  )
```

### フィーダー（データ駆動テスト）

```scala
// users.csv
// username,password
// user1,pass1
// user2,pass2

val feeder = csv("users.csv").random

val scn = scenario("Data Driven Test")
  .feed(feeder)
  .exec(
    http("Login with CSV Data")
      .post("/login")
      .body(StringBody("""{"username":"${username}","password":"${password}"}"""))
      .asJson
  )
```

### 複雑な負荷パターン

```scala
setUp(
  scn.inject(
    nothingFor(5.seconds),                    // 5秒待機
    atOnceUsers(10),                          // 10ユーザー即座
    rampUsers(50).during(30.seconds),         // 50ユーザーを30秒
    constantUsersPerSec(20).during(60.seconds), // 20users/秒を60秒
    rampUsersPerSec(10).to(50).during(2.minutes) // 10→50users/秒に増加
  ).protocols(httpProtocol)
)
```

### 実行

```bash
# Mavenで実行
mvn gatling:test

# 特定シミュレーション実行
mvn gatling:test -Dgatling.simulationClass=simulations.BasicSimulation

# Gradleで実行
gradle gatlingRun

# スタンドアロン実行
./bin/gatling.sh
```

## CI/CD統合

### GitHub Actions

```yaml
name: Performance Test

on: [push]

jobs:
  gatling-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          java-version: '17'
      
      - name: Run Gatling Tests
        run: mvn gatling:test
      
      - name: Upload Gatling Report
        uses: actions/upload-artifact@v3
        with:
          name: gatling-report
          path: target/gatling/*
```

### Grafana統合

```scala
// build.sbt
libraryDependencies += "io.gatling" % "gatling-graphite" % "3.10.3"

// application.conf
gatling {
  data {
    writers = [console, file, graphite]
    graphite {
      host = "localhost"
      port = 2003
    }
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Gatling Open Source** | 🟢 完全無料 | オープンソース、Apache License 2.0 |
| **Gatling Enterprise** | 💰 要問い合わせ | クラウド実行、チーム協業、高度な分析 |

## メリット

### ✅ 主な利点

1. **高性能**: 非同期I/Oで少ないリソースで大量負荷
2. **美しいレポート**: インタラクティブHTMLレポート
3. **DSL**: 読みやすいScala/Java DSL
4. **無料**: オープンソース、Apache License
5. **CI/CD統合**: Maven/Gradleプラグイン
6. **Grafana統合**: リアルタイムモニタリング
7. **レコーダー**: ブラウザ操作を自動記録
8. **アサーション**: 成功条件を明確に定義
9. **詳細メトリクス**: パーセンタイル、応答時間分布
10. **アクティブ開発**: 継続的な改善

## デメリット

### ❌ 制約・課題

1. **Scala/Java必須**: DSL学習コスト
2. **プロトコル制限**: HTTP中心（JDBC、FTP等は非対応）
3. **分散テスト**: Enterprise版または手動設定必要
4. **GUI**: レコーダー以外はコードベース
5. **デバッグ**: エラー特定に時間がかかる
6. **Windows**: 一部機能でパス問題
7. **メモリ**: 大規模テストではJVMチューニング必要
8. **コミュニティ**: JMeterほど情報豊富ではない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **JMeter** | GUI、多様なプロトコル | Gatlingよりプロトコル対応広い |
| **Locust** | Python、分散テスト | GatlingよりPython開発者向け |
| **k6** | JavaScript、CLI重視 | Gatlingより軽量 |
| **Artillery** | Node.js、YAML設定 | Gatlingよりシンプル |
| **wrk** | C言語、超軽量 | Gatlingより機能限定的 |

## 公式リンク

- **公式サイト**: [https://gatling.io/](https://gatling.io/)
- **ドキュメント**: [https://docs.gatling.io/](https://docs.gatling.io/)
- **GitHub**: [https://github.com/gatling/gatling](https://github.com/gatling/gatling)
- **Community**: [https://community.gatling.io/](https://community.gatling.io/)
- **Gatling Enterprise**: [https://gatling.io/enterprise/](https://gatling.io/enterprise/)

## 関連ドキュメント

- [テストツール一覧](../テストツール/)
- [JMeter](./JMeter.md)
- [Locust](./Locust.md)
- [k6](./k6.md)
- [パフォーマンステストベストプラクティス](../../best-practices/performance-testing.md)

---

**カテゴリ**: テストツール  
**対象工程**: テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
