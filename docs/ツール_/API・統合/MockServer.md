# MockServer

## 概要

MockServerは、HTTP/HTTPSベースのAPIをモック・スタブ化するオープンソースツールです。REST API、SOAP、その他のHTTPサービスをシミュレートし、実際のサービスなしでクライアント開発やテストを可能にします。リクエストマッチング、レスポンステンプレート、プロキシ、検証機能に加え、OpenAPI仕様からのモック自動生成、強力なUIダッシュボード、WebSocketサポートなど、WireMockの機能を拡張した特徴を持ちます。Javaライブラリ、スタンドアロンサーバー、Docker、npm等、多様な環境で動作します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | https://www.mock-server.com/ |
| **料金** | 🟢 無料 |
| **ライセンス** | Apache License 2.0 |
| **対応言語** | Java、JavaScript、言語非依存（HTTPベース） |
| **動作環境** | JVM、Node.js、Docker、スタンドアロンサーバー |
| **開発元** | James D Bloom |
| **初版リリース** | 2012年 |
| **最新バージョン** | 5.x（2024年時点） |

## 主な機能

### 1. リクエストマッチング
- **URLマッチング**: パス、クエリパラメータ、正規表現での柔軟なマッチング
- **ヘッダー・Cookie**: HTTP ヘッダーやCookieの値でリクエストを識別
- **ボディマッチング**: JSON、XML、正規表現、JSONSchema、XPathでマッチ
- **メソッドマッチング**: GET、POST、PUT、DELETE等HTTPメソッド指定

### 2. レスポンス定義
- **テンプレート**: Velocity、JavaScript、Mustacheテンプレートエンジン対応
- **動的レスポンス**: リクエストデータを元に動的にレスポンスを生成
- **ファイル**: 外部ファイルからレスポンスボディを読み込み
- **バイナリ**: 画像、PDFなどバイナリデータの返却

### 3. OpenAPI統合
- **自動生成**: OpenAPI/Swagger仕様からモックを自動生成
- **バリデーション**: リクエストがOpenAPI仕様に準拠しているか検証
- **例の利用**: OpenAPI内のexamplesをレスポンスとして使用
- **スキーマ検証**: JSONSchemaでリクエスト/レスポンスを検証

### 4. プロキシ・録画
- **プロキシモード**: 実際のAPIへのリクエストを中継・変換
- **録画**: 実APIとのやり取りを記録してExpectationを自動生成
- **選択的プロキシ**: 一部のリクエストのみプロキシ、残りはモック
- **リクエスト/レスポンス改変**: プロキシ時にデータを書き換え

### 5. 検証・アサーション
- **リクエスト検証**: 期待したリクエストが送信されたかを確認
- **回数検証**: 特定のエンドポイントが何回呼ばれたかを確認
- **順序検証**: リクエストの順序を検証
- **タイムアウト検証**: 一定時間内にリクエストが来ることを検証

### 6. 動作シミュレーション
- **遅延**: 固定遅延、ランダム遅延でネットワーク遅延を再現
- **エラー**: タイムアウト、接続エラー、不正なレスポンスの生成
- **WebSocket**: WebSocketプロトコルのモック
- **TLS/HTTPS**: HTTPSエンドポイントのモック

### 7. UIダッシュボード
- **Web UI**: ブラウザベースの管理画面
- **ログビューア**: リクエスト/レスポンスの履歴を可視化
- **ライブ編集**: 実行中にExpectationを追加・編集
- **デバッグ**: マッチングの詳細やエラーを確認

## 利用方法

### インストール

#### 1. Javaライブラリとして（Maven）
```xml
<dependency>
    <groupId>org.mock-server</groupId>
    <artifactId>mockserver-netty</artifactId>
    <version>5.15.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mock-server</groupId>
    <artifactId>mockserver-client-java</artifactId>
    <version>5.15.0</version>
    <scope>test</scope>
</dependency>
```

#### 2. Node.jsライブラリとして
```bash
npm install mockserver-client --save-dev
```

#### 3. スタンドアロンサーバー
```bash
# JARファイルをダウンロード
wget https://repo1.maven.org/maven2/org/mock-server/mockserver-netty/5.15.0/mockserver-netty-5.15.0-jar-with-dependencies.jar

# サーバー起動（ポート1080）
java -jar mockserver-netty-5.15.0-jar-with-dependencies.jar -serverPort 1080
```

#### 4. Docker
```bash
# MockServerコンテナ起動
docker run -d -p 1080:1080 mockserver/mockserver

# UI付きで起動
docker run -d -p 1080:1080 -e MOCKSERVER_LOG_LEVEL=INFO mockserver/mockserver
```

#### 5. Homebrew（macOS）
```bash
brew install mockserver
mockserver -serverPort 1080
```

### 基本的な使い方

#### 1. Javaでのモック定義（JUnit）
```java
import org.mockserver.integration.ClientAndServer;
import org.mockserver.model.HttpRequest;
import org.mockserver.model.HttpResponse;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

class ApiTest {
    private ClientAndServer mockServer;

    @BeforeEach
    void startServer() {
        mockServer = ClientAndServer.startClientAndServer(1080);
    }

    @Test
    void testGetUser() {
        // Expectation定義: GET /users/1 → 200 OK
        mockServer
            .when(
                request()
                    .withMethod("GET")
                    .withPath("/users/1")
            )
            .respond(
                response()
                    .withStatusCode(200)
                    .withHeader("Content-Type", "application/json")
                    .withBody("{\"id\":1,\"name\":\"Alice\"}")
            );

        // テスト実行
        RestClient client = new RestClient("http://localhost:1080");
        User user = client.getUser(1);

        assertEquals("Alice", user.getName());
    }

    @AfterEach
    void stopServer() {
        mockServer.stop();
    }
}
```

#### 2. Node.jsでのモック定義
```javascript
const mockServerClient = require('mockserver-client').mockServerClient;

// MockServerに接続
const client = mockServerClient("localhost", 1080);

// Expectation作成
client.mockAnyResponse({
  httpRequest: {
    method: 'POST',
    path: '/users',
    body: {
      type: 'JSON',
      json: JSON.stringify({ name: 'Bob' })
    }
  },
  httpResponse: {
    statusCode: 201,
    headers: {
      'Content-Type': ['application/json']
    },
    body: JSON.stringify({ id: 2, name: 'Bob' })
  }
}).then(
  () => console.log("Expectation created"),
  (error) => console.log(error)
);
```

#### 3. REST APIでのモック登録
```bash
# Expectationを動的に追加
curl -X PUT http://localhost:1080/mockserver/expectation \
  -H "Content-Type: application/json" \
  -d '{
    "httpRequest": {
      "method": "GET",
      "path": "/api/products"
    },
    "httpResponse": {
      "statusCode": 200,
      "headers": {
        "Content-Type": ["application/json"]
      },
      "body": "{\"products\":[{\"id\":1,\"name\":\"Widget\"}]}"
    }
  }'
```

#### 4. OpenAPI仕様からのモック生成
```java
// OpenAPI/Swagger仕様を読み込んでモックを自動生成
mockServer
    .when(
        request()
            .withSpecUrlOrPayload("https://api.example.com/openapi.json")
    )
    .respond(
        response()
            .withStatusCode(200)
    );
```

```bash
# CLIでOpenAPI仕様からモック起動
java -jar mockserver-netty-jar-with-dependencies.jar \
  -serverPort 1080 \
  -specUrlOrPayload https://petstore.swagger.io/v2/swagger.json
```

#### 5. リクエストマッチング（高度な例）
```java
// クエリパラメータとヘッダーでマッチ
mockServer
    .when(
        request()
            .withMethod("GET")
            .withPath("/search")
            .withQueryStringParameter("category", "electronics")
            .withHeader("Authorization", "Bearer .*")
    )
    .respond(
        response()
            .withStatusCode(200)
            .withBody("{\"results\":[]}")
    );

// JSONボディのスキーマでマッチ
mockServer
    .when(
        request()
            .withMethod("POST")
            .withPath("/orders")
            .withBody(
                jsonSchema("{"
                    + "\"type\": \"object\","
                    + "\"properties\": {"
                    + "  \"items\": {\"type\": \"array\"}"
                    + "},"
                    + "\"required\": [\"items\"]"
                    + "}")
            )
    )
    .respond(response().withStatusCode(201));
```

#### 6. 動的レスポンス（テンプレート）
```java
// Velocityテンプレートでリクエストデータを参照
mockServer
    .when(
        request()
            .withPath("/echo")
    )
    .respond(
        response()
            .withBody("You requested: $!request.path")
            .withBody(template(TemplateType.VELOCITY))
    );

// JavaScriptでカスタムロジック実行
mockServer
    .when(request().withPath("/calculate"))
    .respond(
        response()
            .withBody("function(request) { return { result: 2 + 2 }; }")
            .withBody(template(TemplateType.JAVASCRIPT))
    );
```

#### 7. 遅延とエラーのシミュレーション
```java
// 固定遅延（2秒）
mockServer
    .when(request().withPath("/slow"))
    .respond(
        response()
            .withStatusCode(200)
            .withDelay(TimeUnit.SECONDS, 2)
    );

// 接続エラー
mockServer
    .when(request().withPath("/broken"))
    .error(
        error()
            .withDropConnection(true)
    );

// ランダム遅延
mockServer
    .when(request().withPath("/variable"))
    .respond(
        response()
            .withStatusCode(200)
            .withDelay(delay()
                .withTimeUnit(TimeUnit.MILLISECONDS)
                .withMin(100)
                .withMax(1000)
            )
    );
```

#### 8. プロキシと録画
```java
// プロキシモード設定
mockServer
    .when(
        request().withPath("/api/.*")
    )
    .forward(
        forward()
            .withHost("real-api.example.com")
            .withPort(443)
            .withScheme(HttpForward.Scheme.HTTPS)
    );

// リクエスト/レスポンス改変
mockServer
    .when(request().withPath("/transform"))
    .forward(
        forward()
            .withHost("example.com")
            .withPort(80)
            .withResponseModifier(
                responseModifier()
                    .withHeader("X-Custom-Header", "Modified")
            )
    );
```

#### 9. リクエスト検証
```java
// リクエストが送信されたことを検証
mockServer.verify(
    request()
        .withMethod("POST")
        .withPath("/users")
        .withBody(json("{\"name\": \"Alice\"}"))
);

// 呼び出し回数の検証
mockServer.verify(
    request()
        .withPath("/items"),
    VerificationTimes.exactly(3)
);

// 呼び出されていないことを検証
mockServer.verify(
    request()
        .withPath("/admin"),
    VerificationTimes.exactly(0)
);
```

#### 10. UIダッシュボードの利用
```bash
# サーバー起動後、ブラウザでアクセス
# http://localhost:1080/mockserver/dashboard

# ダッシュボードで以下が可能:
# - リクエスト/レスポンスの履歴表示
# - Expectationのライブ追加・編集
# - ログのフィルタリング・検索
# - 統計情報の確認
```

## メリット

### 1. OpenAPI統合
✅ OpenAPI/Swagger仕様から自動でモック生成
✅ スキーマバリデーションによる契約テスト
✅ API仕様変更への追従が容易
✅ 仕様駆動開発（Spec-Driven Development）を促進

### 2. 豊富なテンプレート機能
✅ Velocity、JavaScript、Mustacheをサポート
✅ リクエストデータを使った動的レスポンス生成
✅ 複雑なビジネスロジックのシミュレーションが可能
✅ 条件分岐やループを含むレスポンス作成

### 3. 強力なUIダッシュボード
✅ ブラウザベースの直感的な管理画面
✅ リアルタイムでリクエスト/レスポンスを確認
✅ 実行中にExpectationを編集可能
✅ デバッグ効率の向上

### 4. 多言語サポート
✅ Java、JavaScript/TypeScript、Pythonなど多数のクライアント
✅ 言語非依存のHTTPベース動作
✅ チーム全体で利用しやすい

### 5. WebSocketサポート
✅ WebSocketプロトコルのモックが可能
✅ リアルタイム通信のテストに対応
✅ 双方向通信のシミュレーション

### 6. 詳細なログ・デバッグ
✅ リクエストマッチングの詳細ログ
✅ なぜマッチしなかったかの診断情報
✅ JSON形式でのログ出力

## デメリット

### 1. 複雑さ
❌ WireMockよりも機能が多く学習コストが高い
❌ 設定項目が多岐にわたり初心者には難しい
❌ テンプレート構文の習得が必要

### 2. リソース消費
❌ JVM環境が必要（Dockerで回避可能だが追加の複雑さ）
❌ UIダッシュボード起動時のメモリ使用量が多い
❌ 大量のExpectationで性能低下の可能性

### 3. ドキュメント
❌ 公式ドキュメントが網羅的だが冗長
❌ 日本語情報が少ない
❌ サンプルコードが分散している

### 4. コミュニティ
❌ WireMockに比べるとコミュニティが小さい
❌ StackOverflowでの質問数が少ない
❌ サードパーティプラグインが少ない

### 5. 後方互換性
❌ メジャーバージョンアップ時のAPI変更
❌ 一部のテンプレート構文が非推奨化
❌ 移行コストが発生することがある

## ユースケース

### 1. OpenAPIベース開発
- API仕様ファイルからモックを自動生成
- フロントエンドとバックエンドの並行開発
- 契約テスト（Contract Testing）の実施

### 2. マイクロサービステスト
- サービス間の依存関係をモック化
- 統合テストの高速化・安定化
- サービス障害のシミュレーション

### 3. WebSocketアプリケーション
- リアルタイムチャットのテスト
- 株価・為替の更新通知モック
- IoTデバイス通信のシミュレーション

### 4. デバッグ・トラブルシューティング
- UIダッシュボードでリクエスト/レスポンスを確認
- プロキシモードで実通信をキャプチャ
- エラーケースの再現

### 5. CI/CDパイプライン
- 外部APIに依存しない自動テスト
- 環境構築の簡素化
- テスト実行速度の向上

## 類似ツールとの比較

| ツール | 料金 | OpenAPI対応 | UI | 特徴 |
|--------|------|------------|----|----|
| **MockServer** | 🟢 無料 | ✅ 強力 | ✅ あり | OpenAPI統合、強力なUI、WebSocket対応 |
| WireMock | 🟢 無料 | ⚠️ 限定的 | ❌ なし | 成熟したツール、豊富な事例 |
| Prism | 🟢 無料 | ✅ 専用 | ❌ なし | OpenAPI特化、軽量、バリデーション強い |
| MSW | 🟢 無料 | ⚠️ 手動 | ❌ なし | JavaScript特化、ブラウザ/Node.js |
| Mountebank | 🟢 無料 | ❌ なし | ✅ あり | 複数プロトコル対応 |

### MockServerを選ぶべきケース
- OpenAPI/Swagger仕様ベースの開発
- UIダッシュボードでリアルタイムにデバッグしたい
- WebSocketのモックが必要
- 動的レスポンス生成の複雑なロジックが必要

### 他ツールを検討すべきケース
- シンプルなHTTP APIモック → **WireMock**
- OpenAPIバリデーション特化 → **Prism**
- JavaScript/TypeScript中心 → **MSW**
- HTTP以外のプロトコルも必要 → **Mountebank**

## ベストプラクティス

### 1. OpenAPI仕様の活用
```java
// OpenAPI仕様をベースにモックを構築
mockServer.retrieveOpenApiExpectations(
    openAPI()
        .withSpecUrlOrPayload("https://api.example.com/openapi.json")
        .withOperationsAndResponses(Map.of(
            "listPets", "200",
            "createPet", "201"
        ))
);
```

### 2. Expectationの整理
```
✅ initializerクラスで初期Expectationをセットアップ
✅ テストケースごとに必要なExpectationのみ追加
✅ @AfterEachでExpectationをリセット
✅ 共通のExpectationはベースクラスで定義
```

### 3. ログレベルの調整
```bash
# 開発時: 詳細ログ
java -jar mockserver.jar -logLevel DEBUG

# CI/CD: 必要最小限
java -jar mockserver.jar -logLevel WARN
```

### 4. Docker Composeでの統合
```yaml
version: '3.8'
services:
  mockserver:
    image: mockserver/mockserver:latest
    ports:
      - "1080:1080"
    environment:
      MOCKSERVER_INITIALIZATION_JSON_PATH: /config/expectations.json
    volumes:
      - ./mockserver-config:/config
```

### 5. パフォーマンスチューニング
```java
// メモリ使用量の削減
ConfigurationProperties.maxExpectations(100);
ConfigurationProperties.maxWebSocketExpectations(50);

// リクエスト履歴の制限
mockServer.clear(request());
```

### 6. セキュリティ
```
✅ ダッシュボードへのアクセス制限（認証設定）
✅ 本番データをモックに含めない
✅ HTTPSエンドポイントの証明書管理
✅ ポート公開範囲の最小化
```

## 公式リンク

- **公式サイト**: https://www.mock-server.com/
- **ドキュメント**: https://www.mock-server.com/mock_server/getting_started.html
- **GitHub**: https://github.com/mock-server/mockserver
- **Docker Hub**: https://hub.docker.com/r/mockserver/mockserver
- **Slack**: https://join.slack.com/t/mock-server/shared_invite/...

## 関連ツール

- [WireMock](./WireMock.md) - HTTP APIモックの定番
- [Mockito](./Mockito.md) - Javaメソッドレベルモック
- [Prism](./Prism.md) - OpenAPI特化モック
- [MSW](./MSW.md) - JavaScript/TypeScript向けモック
- [Postman](./Postman.md) - API開発・テストツール
- [Swagger](./Swagger.md) - OpenAPI仕様・ドキュメント

## まとめ

MockServerは、HTTP/HTTPSベースのAPIモックにおいて、OpenAPI統合、UIダッシュボード、WebSocketサポートなど、WireMockを超える先進的な機能を提供するツールです。

特にOpenAPI/Swagger仕様ベースの開発において、仕様からのモック自動生成やバリデーション機能が強力で、契約テスト（Contract Testing）やスキーマ駆動開発を実践する上で理想的です。UIダッシュボードによるリアルタイムデバッグ機能も開発効率を大きく向上させます。

学習コストやリソース消費はWireMockよりやや高いものの、OpenAPIベースの開発やWebSocketを含む高度なモック要求がある場合、MockServerの採用は非常に有効です。
