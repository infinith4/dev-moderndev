# MockServer

## 概要

MockServerは、HTTPモックサーバとプロキシサーバの機能を提供するオープンソースツールです。Java、Node.js、Dockerで動作し、REST API、WebSocket、HTTPSのモックとプロキシをサポートします。期待値検証、リクエスト記録、動的レスポンス生成、UI管理画面など、包括的なAPIテスト機能を提供します。

## 主な機能

### 1. モックサーバ
- **HTTPモック**: REST API、SOAP、WebSocket
- **HTTPS対応**: SSL/TLS証明書自動生成
- **動的レスポンス**: JavaScript/Velocityテンプレート
- **条件分岐**: リクエスト内容による分岐

### 2. プロキシモード
- **HTTPプロキシ**: 実サーバへのプロキシ
- **レコーディング**: リクエスト/レスポンス記録
- **書き換え**: リクエスト/レスポンス変換
- **検証**: プロキシ通過リクエスト検証

### 3. 検証機能
- **期待値検証**: リクエスト回数、内容確認
- **リクエスト履歴**: 全リクエスト記録
- **アサーション**: テストフレームワーク統合
- **ログ出力**: 詳細ログ

### 4. UI管理画面
- **ダッシュボード**: リクエスト履歴表示
- **期待値設定**: GUI操作
- **リアルタイム監視**: リクエスト/レスポンス確認
- **ログビューア**: ログ表示

## 利用方法

### Javaライブラリとして使用

```java
// Maven依存関係
// <dependency>
//   <groupId>org.mock-server</groupId>
//   <artifactId>mockserver-netty</artifactId>
//   <version>5.15.0</version>
//   <scope>test</scope>
// </dependency>

import org.mockserver.integration.ClientAndServer;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

public class MockServerTest {

    private ClientAndServer mockServer;

    @BeforeEach
    public void startServer() {
        mockServer = ClientAndServer.startClientAndServer(1080);
    }

    @AfterEach
    public void stopServer() {
        mockServer.stop();
    }

    @Test
    public void testMockApi() {
        // モック設定
        mockServer
            .when(
                request()
                    .withMethod("GET")
                    .withPath("/api/users/1")
            )
            .respond(
                response()
                    .withStatusCode(200)
                    .withHeader("Content-Type", "application/json")
                    .withBody("{\"id\":1,\"name\":\"John Doe\"}")
            );

        // APIテスト実行
        // ... your test code

        // 検証
        mockServer.verify(
            request()
                .withMethod("GET")
                .withPath("/api/users/1")
        );
    }
}
```

### Node.jsクライアント

```javascript
const mockServer = require('mockserver-client');
const mockServerClient = mockServer.mockServerClient;

// モック設定
await mockServerClient("localhost", 1080).mockAnyResponse({
    "httpRequest": {
        "method": "GET",
        "path": "/api/users/1"
    },
    "httpResponse": {
        "statusCode": 200,
        "headers": {
            "Content-Type": ["application/json"]
        },
        "body": JSON.stringify({
            id: 1,
            name: "John Doe"
        })
    }
});

// 検証
await mockServerClient("localhost", 1080).verify({
    "method": "GET",
    "path": "/api/users/1"
}, 1, 1); // 最小1回、最大1回
```

### Docker使用

```bash
# Dockerコンテナ起動
docker run -d --rm \
  -p 1080:1080 \
  -e MOCKSERVER_LOG_LEVEL=INFO \
  mockserver/mockserver:5.15.0

# UI管理画面アクセス
# http://localhost:1080/mockserver/dashboard

# ヘルスチェック
curl http://localhost:1080/mockserver/status
```

### スタンドアロンJAR

```bash
# JARダウンロード
wget https://repo1.maven.org/maven2/org/mock-server/mockserver-netty/5.15.0/mockserver-netty-5.15.0-jar-with-dependencies.jar

# サーバ起動
java -jar mockserver-netty-5.15.0-jar-with-dependencies.jar -serverPort 1080

# ログレベル指定
java -Dmockserver.logLevel=DEBUG -jar mockserver-netty-5.15.0-jar-with-dependencies.jar
```

### REST API経由での設定

```bash
# モック設定
curl -X PUT http://localhost:1080/mockserver/expectation \
  -H 'Content-Type: application/json' \
  -d '{
    "httpRequest": {
      "method": "GET",
      "path": "/api/users/1"
    },
    "httpResponse": {
      "statusCode": 200,
      "body": "{\"id\":1,\"name\":\"John Doe\"}"
    }
  }'

# リクエスト検証
curl -X PUT http://localhost:1080/mockserver/verify \
  -H 'Content-Type: application/json' \
  -d '{
    "httpRequest": {
      "method": "GET",
      "path": "/api/users/1"
    },
    "times": {
      "atLeast": 1
    }
  }'

# 全モックリセット
curl -X PUT http://localhost:1080/mockserver/reset
```

### 動的レスポンス（JavaScript）

```javascript
// モック設定（動的レスポンス）
mockServer
    .when(
        request()
            .withMethod("POST")
            .withPath("/api/users")
    )
    .respond(
        httpRequest -> {
            String body = httpRequest.getBodyAsString();
            // 動的にレスポンス生成
            return response()
                .withStatusCode(201)
                .withBody("{\"id\":100,\"created\":true}")
                .withHeader("Location", "/api/users/100");
        }
    );
```

### プロキシモード

```java
// プロキシとして動作
mockServer
    .when(
        request()
            .withPath("/api/.*")
    )
    .forward(
        forward()
            .withHost("api.example.com")
            .withPort(443)
            .withScheme(HttpForward.Scheme.HTTPS)
    );
```

### JUnit 5統合

```java
import org.mockserver.client.MockServerClient;
import org.mockserver.junit.jupiter.MockServerExtension;
import org.mockserver.junit.jupiter.MockServerSettings;

@ExtendWith(MockServerExtension.class)
@MockServerSettings(ports = {1080})
class ApiTest {

    private MockServerClient client;

    @BeforeEach
    void setUp(MockServerClient client) {
        this.client = client;
    }

    @Test
    void testApi() {
        client
            .when(request().withPath("/api/test"))
            .respond(response().withBody("test response"));

        // テスト実行
    }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **MockServer Open Source** | 🟢 無料 | オープンソース、フル機能 |

## メリット

1. **無料**: オープンソースでフル機能
2. **Java/Node.js/Docker対応**: 柔軟な環境
3. **プロキシモード**: 実サーバ連携可能
4. **UI付属**: ダッシュボードで管理容易
5. **期待値検証機能**: テスト検証充実

## デメリット

1. **セットアップやや複雑**: 初期設定に時間
2. **ドキュメント整理不十分**: 情報探しにくい場合あり
3. **パフォーマンス課題**: 大量リクエストで遅延
4. **学習コスト中程度**: 概念理解に時間

## 公式リンク

- **公式サイト**: [https://www.mock-server.com/](https://www.mock-server.com/)
- **ドキュメント**: [https://www.mock-server.com/mock_server/getting_started.html](https://www.mock-server.com/mock_server/getting_started.html)
- **GitHub**: [https://github.com/mock-server/mockserver](https://github.com/mock-server/mockserver)

## 関連ドキュメント

- [モックサーバツール一覧](../../dev_process_開発工程_9_テスト_アプリケーション.md#922-apiテスト用モックサーバツールtop-6)
- [WireMock](./WireMock.md)
- [Postman](./Postman.md)

---

**カテゴリ**: モックサーバ・APIテスト
**対象工程**: 結合テスト・APIテスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
