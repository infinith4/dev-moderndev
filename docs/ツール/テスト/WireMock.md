# WireMock

## 概要

WireMockは、Java製のHTTPモックサーバライブラリです。スタンドアロンサーバとしても、Javaライブラリとしても動作し、REST APIのモックやスタブを簡単に作成できます。リクエストマッチング、レスポンステンプレート、遅延シミュレーション、リクエスト検証など、APIテストに必要な機能を網羅しています。

## 主な機能

### 1. リクエストマッチング
- **URLパターン**: 正規表現、パス完全一致
- **HTTPメソッド**: GET、POST、PUT、DELETE等
- **ヘッダーマッチング**: カスタムヘッダー検証
- **ボディマッチング**: JSON、XML、テキスト

### 2. レスポンス生成
- **ステータスコード**: 任意のHTTPステータス
- **レスポンスボディ**: JSON、XML、HTML
- **ヘッダー**: カスタムレスポンスヘッダー
- **テンプレート**: Handlebarsテンプレート

### 3. 動作制御
- **遅延シミュレーション**: 固定遅延、ランダム遅延
- **障害シミュレーション**: 接続エラー、タイムアウト
- **プロキシモード**: 実サーバへのプロキシ
- **レコーディング**: 実リクエスト記録

### 4. 検証機能
- **リクエスト検証**: 呼び出し回数確認
- **リクエスト履歴**: 全リクエスト記録
- **アサーション**: JUnit統合

## 利用方法

### スタンドアロンサーバ起動

```bash
# JARダウンロード
wget https://repo1.maven.org/maven2/org/wiremock/wiremock-standalone/3.3.1/wiremock-standalone-3.3.1.jar

# サーバ起動（デフォルト: ポート8080）
java -jar wiremock-standalone-3.3.1.jar

# カスタムポート指定
java -jar wiremock-standalone-3.3.1.jar --port 9090

# ルートディレクトリ指定
java -jar wiremock-standalone-3.3.1.jar --root-dir /path/to/wiremock
```

### スタブ定義（JSON）

```json
// mappings/user-api.json
{
  "request": {
    "method": "GET",
    "urlPattern": "/api/users/([0-9]+)"
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "jsonBody": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

### Javaライブラリとして使用

```java
// Maven依存関係
// <dependency>
//   <groupId>org.wiremock</groupId>
//   <artifactId>wiremock</artifactId>
//   <version>3.3.1</version>
//   <scope>test</scope>
// </dependency>

import com.github.tomakehurst.wiremock.WireMockServer;
import static com.github.tomakehurst.wiremock.client.WireMock.*;

public class ApiTest {

    @Test
    public void testUserApi() {
        // WireMockサーバ起動
        WireMockServer wireMockServer = new WireMockServer(8080);
        wireMockServer.start();

        // スタブ設定
        stubFor(get(urlEqualTo("/api/users/1"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("{\"id\":1,\"name\":\"John Doe\"}")));

        // APIテスト実行
        // ... your test code

        // 検証
        verify(getRequestedFor(urlEqualTo("/api/users/1")));

        // サーバ停止
        wireMockServer.stop();
    }
}
```

### JUnit 5統合

```java
import org.wiremock.integrations.testcontainers.WireMockContainer;
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@Testcontainers
class WireMockTest {

    @Container
    WireMockContainer wiremock = new WireMockContainer("wiremock/wiremock:3.3.1")
        .withMapping("user", WireMockTest.class, "user-stub.json");

    @Test
    void testApi() {
        String baseUrl = wiremock.getBaseUrl();
        // テスト実行
    }
}
```

### レスポンステンプレート

```json
{
  "request": {
    "method": "GET",
    "urlPathPattern": "/api/users/([0-9]+)"
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "jsonBody": {
      "id": "{{request.path.[2]}}",
      "timestamp": "{{now format='yyyy-MM-dd HH:mm:ss'}}",
      "requestId": "{{randomValue type='UUID'}}"
    },
    "transformers": ["response-template"]
  }
}
```

### 遅延シミュレーション

```json
{
  "request": {
    "method": "GET",
    "url": "/api/slow-endpoint"
  },
  "response": {
    "status": 200,
    "fixedDelayMilliseconds": 3000,
    "body": "Delayed response"
  }
}
```

### プロキシモード

```bash
# 実サーバへのプロキシとして動作
java -jar wiremock-standalone-3.3.1.jar --proxy-all="https://api.example.com"

# レコーディングモード（実リクエストを記録）
java -jar wiremock-standalone-3.3.1.jar --record-mappings --proxy-all="https://api.example.com"
```

### Docker使用

```bash
# Docker起動
docker run -it --rm \
  -p 8080:8080 \
  -v $(pwd)/wiremock:/home/wiremock \
  wiremock/wiremock:3.3.1

# スタブファイル配置
# ./wiremock/mappings/*.json
# ./wiremock/__files/*.json
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **WireMock Open Source** | 🟢 完全無料 | オープンソース、フル機能 |
| **WireMock Cloud** | 💰 $99/月〜 | クラウドホスティング、GUI管理 |
| **WireMock Studio** | 💰 $25/月〜 | デスクトップGUI、スタブ管理 |

## メリット

1. **完全無料**: オープンソースでフル機能利用可能
2. **スタンドアロン・ライブラリ両対応**: 柔軟な使い方
3. **強力なマッチング**: 正規表現、JSONパス対応
4. **CI/CD統合容易**: Javaベースで自動化簡単
5. **レスポンス遅延シミュレーション**: 性能テスト対応

## デメリット

1. **Java環境必要**: JVMインストール必須
2. **GUI基本なし**: JSON手動編集（Studio版は有料）
3. **設定ファイル複雑化**: 大規模スタブで管理困難
4. **GraphQL対応限定的**: REST API特化

## 公式リンク

- **公式サイト**: [https://wiremock.org/](https://wiremock.org/)
- **ドキュメント**: [https://wiremock.org/docs/](https://wiremock.org/docs/)
- **GitHub**: [https://github.com/wiremock/wiremock](https://github.com/wiremock/wiremock)

## 関連ドキュメント

- [モックサーバツール一覧](../../dev_process_開発工程_9_テスト_アプリケーション.md#922-apiテスト用モックサーバツールtop-6)
- [MockServer](./MockServer.md)
- [Postman](./Postman.md)

---

**カテゴリ**: モックサーバ・APIテスト
**対象工程**: 結合テスト・APIテスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
