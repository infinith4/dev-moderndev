# WireMock

## 概要

WireMockは、HTTP APIのモック・スタブ化を行うオープンソースツールです。REST APIやSOAPサービスの動作をシミュレートし、実際のサービスなしでAPIクライアントの開発・テストを可能にします。Javaライブラリとして、またスタンドアロンサーバーとして動作し、言語非依存でHTTPレベルでのモックを提供します。リクエストマッチング、レスポンステンプレート、遅延シミュレーション、プロキシ/録画機能など、APIテストに必要な包括的な機能を備えています。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | https://wiremock.org/ |
| **料金** | 🟢 無料（オープンソース）、🔴 WireMock Cloud（有料SaaS版あり） |
| **ライセンス** | Apache License 2.0 |
| **対応言語** | Java、言語非依存（HTTPベース） |
| **動作環境** | JVM、Docker、スタンドアロンサーバー |
| **開発元** | Tom Akehurst（現在はコミュニティ開発） |
| **初版リリース** | 2011年 |
| **最新バージョン** | 3.x（2024年時点） |

## 主な機能

### 1. リクエストマッチング
- **URLマッチング**: パス、クエリパラメータの柔軟なマッチング
- **ヘッダーマッチング**: HTTPヘッダーの値でリクエストを識別
- **ボディマッチング**: JSON、XML、正規表現でリクエストボディをマッチ
- **優先度制御**: 複数のスタブが一致する場合の優先順位設定

### 2. レスポンス定義
- **ステータスコード**: 任意のHTTPステータスコードを返却
- **ヘッダー**: カスタムレスポンスヘッダーの設定
- **ボディ**: JSON、XML、HTML、バイナリなど任意のコンテンツ
- **テンプレート**: Handlebarsテンプレートでリクエストデータを参照

### 3. 動作シミュレーション
- **遅延**: 固定遅延、ランダム遅延でネットワーク遅延を再現
- **障害**: タイムアウト、接続リセット、不正なレスポンスの生成
- **確率的障害**: 指定確率で障害を発生させる
- **チャンキング**: レスポンスを分割送信してストリーミングを再現

### 4. プロキシ・録画
- **プロキシモード**: 実際のAPIへのリクエストを中継
- **録画**: 実APIとのやり取りを記録してスタブを自動生成
- **再生**: 録画したスタブを再利用
- **選択的プロキシ**: 一部のリクエストのみプロキシ、残りはモック

### 5. 検証
- **リクエスト検証**: 期待したリクエストが送信されたかを確認
- **呼び出し回数**: 特定のエンドポイントが何回呼ばれたかを検証
- **順序検証**: リクエストの順序を検証
- **タイムアウト**: 一定時間内にリクエストが来ることを検証

### 6. 管理API
- **REST API**: モック設定をHTTP APIで動的に管理
- **スタブの追加/削除**: 実行時にスタブを追加・削除
- **リセット**: すべてのスタブやリクエスト履歴をクリア
- **シナリオ**: 状態遷移を持つ複雑な動作のモック

### 7. 拡張性
- **カスタムマッチャー**: 独自のマッチングロジックを実装
- **カスタムトランスフォーマー**: レスポンス生成ロジックをカスタマイズ
- **拡張機能**: Webhook、状態管理、外部データソース連携

## 利用方法

### インストール

#### 1. Javaライブラリとして（Maven）
```xml
<dependency>
    <groupId>org.wiremock</groupId>
    <artifactId>wiremock</artifactId>
    <version>3.3.1</version>
    <scope>test</scope>
</dependency>
```

#### 2. Javaライブラリとして（Gradle）
```gradle
testImplementation 'org.wiremock:wiremock:3.3.1'
```

#### 3. スタンドアロンサーバー
```bash
# JARファイルをダウンロード
curl -o wiremock-standalone.jar https://repo1.maven.org/maven2/org/wiremock/wiremock-standalone/3.3.1/wiremock-standalone-3.3.1.jar

# サーバー起動（ポート8080）
java -jar wiremock-standalone.jar --port 8080
```

#### 4. Docker
```bash
# WireMockコンテナ起動
docker run -d -p 8080:8080 --name wiremock wiremock/wiremock

# カスタムポートで起動
docker run -d -p 9090:8080 --name wiremock wiremock/wiremock
```

### 基本的な使い方

#### 1. Javaでのスタブ定義（JUnit 5）
```java
import com.github.tomakehurst.wiremock.junit5.WireMockTest;
import static com.github.tomakehurst.wiremock.client.WireMock.*;

@WireMockTest(httpPort = 8080)
class ApiTest {

    @Test
    void testGetUser() {
        // スタブ定義: GET /users/1 → 200 OK
        stubFor(get(urlEqualTo("/users/1"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("{\"id\":1,\"name\":\"Alice\"}")));

        // テスト実行
        RestClient client = new RestClient("http://localhost:8080");
        User user = client.getUser(1);

        assertEquals("Alice", user.getName());
    }
}
```

#### 2. JSONファイルによるスタブ定義
```json
// mappings/get-user.json
{
  "request": {
    "method": "GET",
    "urlPattern": "/users/[0-9]+"
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "jsonBody": {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com"
    }
  }
}
```

#### 3. REST APIでのスタブ登録
```bash
# スタブを動的に追加
curl -X POST http://localhost:8080/__admin/mappings \
  -H "Content-Type: application/json" \
  -d '{
    "request": {
      "method": "POST",
      "url": "/users",
      "bodyPatterns": [
        {"matchesJsonPath": "$.name"}
      ]
    },
    "response": {
      "status": 201,
      "headers": {"Content-Type": "application/json"},
      "jsonBody": {"id": 99, "name": "{{jsonPath request.body \"$.name\"}}"}
    }
  }'
```

#### 4. リクエストマッチング（高度な例）
```java
// クエリパラメータでマッチ
stubFor(get(urlPathEqualTo("/search"))
    .withQueryParam("q", equalTo("wiremock"))
    .willReturn(aResponse()
        .withStatus(200)
        .withBody("{\"results\":[]}")));

// JSONボディのパスでマッチ
stubFor(post(urlEqualTo("/orders"))
    .withRequestBody(matchingJsonPath("$.items[?(@.price > 100)]"))
    .willReturn(aResponse().withStatus(400)));

// ヘッダーでマッチ
stubFor(get(urlEqualTo("/api/data"))
    .withHeader("Authorization", matching("Bearer .*"))
    .willReturn(aResponse().withStatus(200)));
```

#### 5. 遅延とエラーのシミュレーション
```java
// 固定遅延（3秒）
stubFor(get(urlEqualTo("/slow-api"))
    .willReturn(aResponse()
        .withStatus(200)
        .withFixedDelay(3000)));

// ランダム遅延（1-5秒）
stubFor(get(urlEqualTo("/variable-api"))
    .willReturn(aResponse()
        .withStatus(200)
        .withUniformRandomDelay(1000, 5000)));

// 接続エラー
stubFor(get(urlEqualTo("/broken-api"))
    .willReturn(aResponse().withFault(Fault.CONNECTION_RESET_BY_PEER)));

// 確率的障害（30%の確率で500エラー）
stubFor(get(urlEqualTo("/flaky-api"))
    .willReturn(aResponse()
        .withStatus(200)
        .withTransformers("response-template")
        .withTransformerParameter("probability", 0.3)));
```

#### 6. プロキシと録画
```java
// プロキシモード設定
stubFor(get(urlMatching("/api/.*"))
    .willReturn(aResponse().proxiedFrom("https://real-api.example.com")));

// 録画の開始
snapshotRecord(recordSpec()
    .forTarget("https://real-api.example.com")
    .extractTextBodiesOver(1024)
    .makeStubsPersistent(false));

// CLIでの録画
// java -jar wiremock-standalone.jar --proxy-all="https://real-api.example.com" --record-mappings
```

#### 7. シナリオ（状態遷移）
```java
// シナリオ: ログイン状態の管理
stubFor(post(urlEqualTo("/login"))
    .inScenario("Auth")
    .whenScenarioStateIs(STARTED)
    .willReturn(aResponse().withStatus(200).withBody("{\"token\":\"abc123\"}"))
    .willSetStateTo("Logged In"));

stubFor(get(urlEqualTo("/profile"))
    .inScenario("Auth")
    .whenScenarioStateIs("Logged In")
    .willReturn(aResponse().withStatus(200).withBody("{\"name\":\"Alice\"}")));

stubFor(post(urlEqualTo("/logout"))
    .inScenario("Auth")
    .whenScenarioStateIs("Logged In")
    .willReturn(aResponse().withStatus(200))
    .willSetStateTo(STARTED));
```

#### 8. リクエスト検証
```java
// リクエストが送信されたことを検証
verify(postRequestedFor(urlEqualTo("/users"))
    .withRequestBody(matchingJsonPath("$.name"))
    .withHeader("Content-Type", equalTo("application/json")));

// 呼び出し回数の検証
verify(exactly(3), getRequestedFor(urlEqualTo("/items")));

// 呼び出されていないことを検証
verify(0, deleteRequestedFor(urlMatching("/users/.*")));
```

## メリット

### 1. 言語非依存
✅ HTTPレベルで動作するため、どの言語・フレームワークからでも利用可能
✅ Java以外（Python、JavaScript、Go等）でも使える
✅ マイクロサービス間のモックに最適

### 2. 柔軟なマッチング
✅ URL、ヘッダー、ボディ、クエリパラメータの組み合わせで詳細にマッチ
✅ 正規表現、JSONPath、XPathをサポート
✅ カスタムマッチャーで独自ロジックを実装可能

### 3. 現実的なシミュレーション
✅ 遅延、タイムアウト、エラーなど実環境の問題を再現
✅ 確率的障害でフレイキーなAPIをテスト
✅ シナリオ機能で状態遷移を持つ複雑なAPIをモック

### 4. プロキシ・録画機能
✅ 実APIとの通信を記録してスタブを自動生成
✅ レガシーAPIのモック化が容易
✅ 本番環境のトラフィックを再現したテストが可能

### 5. スタンドアロン動作
✅ コード不要でJSON定義だけでモックを構築
✅ チーム全体で共有しやすい
✅ CI/CDパイプラインに統合しやすい

### 6. 活発なコミュニティ
✅ 10年以上の歴史、成熟したプロジェクト
✅ 豊富なドキュメントと事例
✅ 多数の拡張機能が利用可能

## デメリット

### 1. Java依存
❌ JVM環境が必要（Dockerで回避可能だが追加の複雑さ）
❌ Javaに不慣れなチームには学習コスト
❌ 軽量な環境では少しオーバーヘッド

### 2. 複雑なシナリオの設定
❌ 状態遷移が多いシナリオはJSON定義が煩雑
❌ デバッグが難しい場合がある
❌ テンプレート構文の習得が必要

### 3. パフォーマンス
❌ 大量のスタブやリクエストで性能低下の可能性
❌ 複雑なマッチング条件は処理時間が増加
❌ メモリ使用量が多い場合がある

### 4. WebSocket/gRPCサポート
❌ HTTP/HTTPSに特化、WebSocketやgRPCは限定的
❌ 双方向通信のモックには不向き
❌ 別ツールとの組み合わせが必要な場合あり

### 5. ドキュメント生成機能
❌ API仕様書の自動生成機能はない
❌ OpenAPIとの統合は手動またはプラグインが必要
❌ スタブからのドキュメント逆生成は困難

## ユースケース

### 1. マイクロサービステスト
- サービス間の依存関係をモック化
- 他チームのAPIが未完成でも開発を進行
- 統合テストの高速化・安定化

### 2. フロントエンド開発
- バックエンドAPIの開発を待たずにUI実装
- エラーケースや境界値のテストデータを簡単に用意
- デモ環境の構築

### 3. パフォーマンステスト
- 遅いAPIや不安定なAPIをシミュレート
- 負荷テスト時の外部依存の排除
- タイムアウト処理の検証

### 4. CI/CDパイプライン
- 外部APIに依存しない自動テスト
- テスト環境の構築コスト削減
- テスト実行速度の向上

### 5. レガシーシステム移行
- 既存APIの動作を記録して新システムで再現
- 段階的な移行時のフォールバック
- 互換性テスト

## 類似ツールとの比較

| ツール | 料金 | 言語 | 特徴 |
|--------|------|------|------|
| **WireMock** | 🟢 無料 | Java/言語非依存 | HTTP APIモックの定番、柔軟なマッチング |
| Mockito | 🟢 無料 | Java/Kotlin | メソッドレベルモック、単体テスト向け |
| MockServer | 🟢 無料 | Java/言語非依存 | WireMock類似、OpenAPI対応 |
| MSW | 🟢 無料 | JavaScript/TypeScript | ブラウザ/Node.js特化、Service Worker利用 |
| Mountebank | 🟢 無料 | 言語非依存 | 複数プロトコル対応（HTTP、TCP、SMTP等） |
| Prism | 🟢 無料 | 言語非依存 | OpenAPI仕様ベース、バリデーション強い |

### WireMockを選ぶべきケース
- HTTPベースのREST APIモックが必要
- プロキシ/録画機能で実APIから学習したい
- Javaプロジェクトで統合しやすいツールが欲しい
- 複雑なシナリオや状態管理が必要

### 他ツールを検討すべきケース
- JavaScript/TypeScript中心の開発 → **MSW**
- OpenAPI仕様ありきの開発 → **Prism**
- HTTP以外のプロトコルも必要 → **Mountebank**
- Javaのメソッドレベルモック → **Mockito**

## ベストプラクティス

### 1. スタブの整理
```
✅ mappingsディレクトリに機能別にスタブをファイル分割
✅ 命名規則を統一（例: method-endpoint.json）
✅ 共通のレスポンスは__filesディレクトリで管理
✅ 優先度を適切に設定してスタブの衝突を回避
```

### 2. リアルなデータ
```
✅ 実際のAPIから録画したデータを使用
✅ エッジケース（エラー、空配列、大量データ）も用意
✅ レスポンステンプレートでリクエストデータを反映
✅ ランダム遅延で実環境の揺らぎを再現
```

### 3. CI/CD統合
```bash
# Dockerでテスト環境にWireMockを起動
version: '3.8'
services:
  wiremock:
    image: wiremock/wiremock
    ports:
      - "8080:8080"
    volumes:
      - ./wiremock:/home/wiremock
    command: ["--global-response-templating"]

# テスト実行前にスタブをセットアップ
curl -X POST http://wiremock:8080/__admin/mappings/reset
curl -X POST http://wiremock:8080/__admin/mappings/import \
  -d @./wiremock/mappings/
```

### 4. バージョン管理
```
✅ スタブファイル（mappings/*.json）をGitで管理
✅ テストコード内のスタブ定義は最小限に
✅ 環境別のスタブセットを用意
✅ スタブの変更履歴をコミットメッセージに記録
```

### 5. パフォーマンス最適化
```java
// 必要最小限のマッチング条件
stubFor(get(urlEqualTo("/users")).willReturn(...)); // Good
stubFor(get(urlMatching("/.*")).willReturn(...));   // Bad: すべてにマッチ

// リクエスト履歴のクリア
wireMockServer.resetRequests();

// 不要なスタブの削除
wireMockServer.removeStub(stubMapping);
```

### 6. セキュリティ
```
✅ 本番のAPIキーや認証情報をスタブに含めない
✅ 管理API（__admin）への外部アクセスを制限
✅ Dockerの場合は必要なポートのみ公開
✅ センシティブなデータはマスキング
```

## 公式リンク

- **公式サイト**: https://wiremock.org/
- **ドキュメント**: https://wiremock.org/docs/
- **GitHub**: https://github.com/wiremock/wiremock
- **WireMock Cloud**: https://www.wiremock.io/ (有料SaaS版)
- **コミュニティ**: https://slack.wiremock.org/

## 関連ツール

- [Mockito](./Mockito.md) - Javaメソッドレベルモック
- [Postman](./Postman.md) - API開発・テストツール
- [MockServer](./MockServer.md) - WireMock類似ツール
- [MSW](./MSW.md) - JavaScript/TypeScript向けモック
- [Prism](./Prism.md) - OpenAPIベースモック
- [Swagger](./Swagger.md) - API仕様・ドキュメント

## まとめ

WireMockは、HTTP APIのモック・スタブ化において最も成熟したオープンソースツールの一つです。言語非依存でHTTPレベルで動作するため、マイクロサービスアーキテクチャやポリグロット環境で特に有用です。

リクエストマッチング、遅延・障害シミュレーション、プロキシ/録画機能など、APIテストに必要な包括的な機能を提供します。スタンドアロンサーバーとしてもJavaライブラリとしても使えるため、開発からテスト、CI/CDまで幅広いシーンで活用できます。

Java依存や複雑なシナリオ設定の学習コストはありますが、それを補って余りある柔軟性と信頼性を持っており、API開発プロジェクトにおいて標準的なモックツールとして採用する価値があります。
