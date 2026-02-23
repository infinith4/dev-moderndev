# REST Assured

## 概要

REST Assuredは、JavaでREST APIのテストを容易にするオープンソースライブラリです。流暢なAPI（Fluent API）により、HTTPリクエストの送信とレスポンスの検証をシンプルかつ可読性高く記述できます。JUnit、TestNG等のテストフレームワークと統合し、CI/CDパイプラインでのAPI自動テストに最適です。

## 主な機能

### 1. 流暢なAPI
- **Given-When-Then**: BDD（振る舞い駆動開発）スタイル
- **メソッドチェーン**: 読みやすいテストコード
- **自然言語風**: テストシナリオが理解しやすい

### 2. HTTPメソッド対応
- **GET、POST、PUT、DELETE、PATCH**: 全HTTP動詞サポート
- **HEAD、OPTIONS**: その他のメソッド
- **カスタムヘッダー**: 任意のHTTPヘッダー設定

### 3. リクエスト設定
- **パラメータ**: Query、Path、Form、Multipart
- **Body**: JSON、XML、テキスト
- **ヘッダー**: Content-Type、Authorization等
- **Cookie**: Cookie管理
- **認証**: Basic、OAuth、Bearer Token

### 4. レスポンス検証
- **Status Code**: 200、404、500等
- **Body検証**: JSON Path、XML Path
- **Header検証**: Content-Type等
- **Time検証**: レスポンス時間

### 5. JSON/XMLサポート
- **JSON Path**: JSONレスポンスの要素抽出
- **XML Path**: XMLレスポンスの要素抽出
- **Schema Validation**: JSON Schema検証

### 6. テストフレームワーク統合
- **JUnit 4/5**: Javaの標準テストフレームワーク
- **TestNG**: データ駆動テスト
- **Spock**: Groovyベースのテスト

## 利用方法

### Maven設定

```xml
<!-- pom.xml -->
<dependencies>
  <!-- REST Assured -->
  <dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <version>5.4.0</version>
    <scope>test</scope>
  </dependency>
  
  <!-- JUnit 5 -->
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.1</version>
    <scope>test</scope>
  </dependency>
  
  <!-- JSON Schema Validation -->
  <dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>json-schema-validator</artifactId>
    <version>5.4.0</version>
    <scope>test</scope>
  </dependency>
</dependencies>
```

### Gradle設定

```groovy
// build.gradle
dependencies {
    testImplementation 'io.rest-assured:rest-assured:5.4.0'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.1'
    testImplementation 'io.rest-assured:json-schema-validator:5.4.0'
}
```

### 基本的なGETリクエスト

```java
import io.restassured.RestAssured;
import org.junit.jupiter.api.Test;
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

public class UserApiTest {
    
    @Test
    public void testGetUsers() {
        given()
            .baseUri("https://api.example.com")
        .when()
            .get("/users")
        .then()
            .statusCode(200)
            .body("size()", greaterThan(0));
    }
}
```

### POSTリクエスト（JSON Body）

```java
@Test
public void testCreateUser() {
    String requestBody = "{\"name\":\"John Doe\",\"email\":\"john@example.com\"}";
    
    given()
        .contentType("application/json")
        .body(requestBody)
    .when()
        .post("https://api.example.com/users")
    .then()
        .statusCode(201)
        .body("id", notNullValue())
        .body("name", equalTo("John Doe"))
        .body("email", equalTo("john@example.com"));
}
```

### 認証（Bearer Token）

```java
@Test
public void testGetProfileWithAuth() {
    String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
    
    given()
        .header("Authorization", "Bearer " + token)
    .when()
        .get("https://api.example.com/profile")
    .then()
        .statusCode(200)
        .body("username", notNullValue());
}
```

### クエリパラメータ・パスパラメータ

```java
@Test
public void testGetUserById() {
    given()
        .pathParam("id", 123)
        .queryParam("include", "posts")
    .when()
        .get("https://api.example.com/users/{id}")
    .then()
        .statusCode(200)
        .body("id", equalTo(123))
        .body("posts", notNullValue());
}
```

### JSON Path検証

```java
@Test
public void testJsonPath() {
    given()
        .baseUri("https://api.example.com")
    .when()
        .get("/users/1")
    .then()
        .statusCode(200)
        .body("id", equalTo(1))
        .body("name", equalTo("Alice"))
        .body("address.city", equalTo("Tokyo"))
        .body("posts[0].title", containsString("Hello"))
        .body("posts.size()", greaterThan(0));
}
```

### JSON Schema検証

```java
import static io.restassured.module.jsv.JsonSchemaValidator.*;

@Test
public void testJsonSchema() {
    given()
        .baseUri("https://api.example.com")
    .when()
        .get("/users")
    .then()
        .statusCode(200)
        .body(matchesJsonSchemaInClasspath("schemas/users-schema.json"));
}
```

### レスポンス時間検証

```java
@Test
public void testResponseTime() {
    given()
        .baseUri("https://api.example.com")
    .when()
        .get("/users")
    .then()
        .statusCode(200)
        .time(lessThan(2000L)); // 2秒以内
}
```

### レスポンス抽出・再利用

```java
@Test
public void testExtractResponse() {
    // レスポンスから値抽出
    int userId = 
        given()
            .contentType("application/json")
            .body("{\"name\":\"Alice\",\"email\":\"alice@example.com\"}")
        .when()
            .post("https://api.example.com/users")
        .then()
            .statusCode(201)
        .extract()
            .path("id");
    
    // 抽出した値を次のリクエストで使用
    given()
        .pathParam("id", userId)
    .when()
        .get("https://api.example.com/users/{id}")
    .then()
        .statusCode(200)
        .body("id", equalTo(userId));
}
```

## CI/CD統合

### GitHub Actions

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Run API Tests
        run: mvn test
```

## 料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **REST Assured** |  無料 | オープンソース、Apache License 2.0 |

## メリット

###  主な利点

1. **流暢なAPI**: Given-When-Thenで可読性高い
2. **Java標準**: Java開発者にとって習得容易
3. **無料**: オープンソース、Apache License
4. **JUnit/TestNG統合**: 既存テストフレームワークと統合
5. **JSON/XML対応**: JSON Path、XML Path
6. **Schema検証**: JSON Schema Validation
7. **認証サポート**: Basic、OAuth、Bearer
8. **CI/CD統合**: Maven/Gradleで自動化
9. **豊富なドキュメント**: 公式Wikiが充実
10. **アクティブ開発**: 継続的な改善

## デメリット

###  制約・課題

1. **Java必須**: Java/Groovy専用
2. **学習曲線**: Hamcrestマッチャー理解必要
3. **非同期制限**: WebSocket、SSEは限定的
4. **GUI不在**: Postmanのようなグラフィカルツールなし
5. **大規模テスト**: 負荷テストには不向き
6. **JavaScript非対応**: Node.js環境では使えない
7. **エラーメッセージ**: 複雑な検証でエラー解析困難
8. **パフォーマンス**: 大量リクエストでオーバーヘッド

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Postman / Newman** | GUI、CLI、Node.js | REST Assuredよりグラフィカル |
| **Karate** | Java、BDD、Cucumber | REST Assuredより高機能 |
| **WireMock** | モックサーバー | REST Assuredと補完関係 |
| **Pact** | Contract Testing | REST Assuredよりマイクロサービス向け |
| **JMeter** | 負荷テスト | REST Assuredよりパフォーマンステスト向け |

## 公式リンク

- **公式サイト**: [https://rest-assured.io/](https://rest-assured.io/)
- **GitHub**: [https://github.com/rest-assured/rest-assured](https://github.com/rest-assured/rest-assured)
- **Wiki**: [https://github.com/rest-assured/rest-assured/wiki/Usage](https://github.com/rest-assured/rest-assured/wiki/Usage)
- **Javadoc**: [https://javadoc.io/doc/io.rest-assured/rest-assured/](https://javadoc.io/doc/io.rest-assured/rest-assured/)

## 関連ドキュメント

- [テストツール一覧](../テストツール/)
- [JUnit](./JUnit.md)
- [Postman](../APIツール/Postman.md)
- [JMeter](./JMeter.md)
- [APIテストベストプラクティス](../../best-practices/api-testing.md)

---

**カテゴリ**: テストツール  
**対象工程**: テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0

