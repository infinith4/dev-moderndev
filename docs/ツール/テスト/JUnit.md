# JUnit

## 概要

JUnitは、Java言語のための最も広く使用されているユニットテストフレームワークです。2000年にKent BeckとErich Gammaによって開発され、テスト駆動開発（TDD）の普及に大きく貢献しました。JUnit 5（Jupiter）は最新版で、モダンなJava（Java 8以降）に対応し、アノテーション駆動のテスト記述、パラメータ化テスト、拡張モデルなど強力な機能を提供します。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **JUnit 5 (Jupiter)** |  無料 | オープンソース、無制限利用、Apache License 2.0 |
| **JUnit 4** |  無料 | レガシー版、引き続きサポート中 |

**注意**: JUnitは無料のオープンソースプロジェクトです。商用利用も制限なく可能です。

## メリット・デメリット

### メリット
-  **業界標準**: Java開発における事実上の標準テストフレームワーク
-  **無料**: オープンソース、商用利用も無料
-  **豊富なエコシステム**: IDEサポート、ビルドツール統合、多数のライブラリ連携
-  **アノテーション駆動**: `@Test`、`@BeforeEach`等でシンプルに記述
-  **パラメータ化テスト**: 同じテストを異なる入力で繰り返し実行
-  **拡張モデル**: カスタム拡張を容易に作成可能
-  **並列実行**: テストの並列実行で高速化
-  **モックライブラリ統合**: Mockito、EasyMockと容易に連携

### デメリット
-  **Java専用**: Java/Kotlin専用、他言語では使用不可
-  **学習曲線**: JUnit 5の高度な機能は習得に時間が必要
-  **JUnit 4からの移行**: レガシーコードの移行には手間がかかる
-  **表現力**: BDD形式（Given-When-Then）のライブラリと比較すると可読性が劣る場合も

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | ユニットテストの作成、TDD開発 | テストコード、テスト結果 |
| **9. テスト（アプリケーション）** | 自動テスト実行、リグレッションテスト | テストレポート、カバレッジレポート |

## 基本的な利用方法

### 1. プロジェクトへの追加

#### Maven (`pom.xml`)
```xml
<dependencies>
    <!-- JUnit 5 (Jupiter) -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.1</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.2</version>
        </plugin>
    </plugins>
</build>
```

#### Gradle (`build.gradle`)
```groovy
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.1'
}

test {
    useJUnitPlatform()
}
```

### 2. 基本的なテストの記述

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private Calculator calculator;

    // 各テストメソッド実行前に呼ばれる
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    // 各テストメソッド実行後に呼ばれる
    @AfterEach
    void tearDown() {
        calculator = null;
    }

    @Test
    @DisplayName("足し算のテスト: 2 + 3 = 5")
    void testAdd() {
        int result = calculator.add(2, 3);
        assertEquals(5, result, "2 + 3 should equal 5");
    }

    @Test
    void testSubtract() {
        assertEquals(1, calculator.subtract(3, 2));
    }

    @Test
    void testDivideByZero() {
        // 例外が発生することを検証
        assertThrows(ArithmeticException.class, () -> {
            calculator.divide(10, 0);
        });
    }

    @Test
    @Disabled("まだ実装されていない機能")
    void testMultiply() {
        // このテストはスキップされる
    }
}
```

### 3. テストの実行

```bash
# Maven
mvn test

# 特定のテストクラスのみ実行
mvn test -Dtest=CalculatorTest

# Gradle
./gradlew test

# 特定のテストのみ実行
./gradlew test --tests CalculatorTest

# IDE (IntelliJ IDEA, Eclipse等)
# テストクラス/メソッドを右クリック → Run 'テスト名'
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: テスト駆動開発（TDD）、コード品質の維持

**活用方法**:
- Red-Green-Refactorサイクル
- ユニットテストの作成
- モックオブジェクトによる依存関係の分離
- テストカバレッジの確保

**実装例（TDD開発）**:
```java
// 1. テストを先に書く（Red）
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {

    private UserService userService;
    private UserRepository mockRepository;

    @BeforeEach
    void setUp() {
        mockRepository = mock(UserRepository.class);
        userService = new UserService(mockRepository);
    }

    @Test
    @DisplayName("新規ユーザー登録: 有効なメールアドレスで成功する")
    void testRegisterUser_ValidEmail_Success() {
        // Arrange
        String email = "test@example.com";
        String password = "SecurePass123!";
        User expectedUser = new User(email, password);

        when(mockRepository.findByEmail(email)).thenReturn(Optional.empty());
        when(mockRepository.save(any(User.class))).thenReturn(expectedUser);

        // Act
        User result = userService.registerUser(email, password);

        // Assert
        assertNotNull(result);
        assertEquals(email, result.getEmail());
        verify(mockRepository).save(any(User.class));
    }

    @Test
    @DisplayName("ユーザー登録: 無効なメールアドレスで失敗する")
    void testRegisterUser_InvalidEmail_ThrowsException() {
        // Arrange
        String invalidEmail = "invalid-email";
        String password = "SecurePass123!";

        // Act & Assert
        assertThrows(InvalidEmailException.class, () -> {
            userService.registerUser(invalidEmail, password);
        });
    }

    @Test
    @DisplayName("ユーザー登録: 既存メールアドレスで失敗する")
    void testRegisterUser_DuplicateEmail_ThrowsException() {
        // Arrange
        String email = "existing@example.com";
        User existingUser = new User(email, "password");

        when(mockRepository.findByEmail(email)).thenReturn(Optional.of(existingUser));

        // Act & Assert
        assertThrows(DuplicateEmailException.class, () -> {
            userService.registerUser(email, "newPassword");
        });
    }
}

// 2. 実装を書く（Green）
class UserService {
    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public User registerUser(String email, String password) {
        if (!isValidEmail(email)) {
            throw new InvalidEmailException("Invalid email format");
        }

        if (repository.findByEmail(email).isPresent()) {
            throw new DuplicateEmailException("Email already exists");
        }

        User user = new User(email, password);
        return repository.save(user);
    }

    private boolean isValidEmail(String email) {
        return email != null && email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }
}

// 3. リファクタリング（Refactor）
```

**パラメータ化テスト**:
```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

class PasswordValidatorTest {

    @ParameterizedTest
    @ValueSource(strings = {
        "Pass123!",
        "SecureP@ssw0rd",
        "MyP@ssw0rd123"
    })
    @DisplayName("有効なパスワード")
    void testValidPasswords(String password) {
        assertTrue(PasswordValidator.isValid(password));
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "short",           // 短すぎる
        "nouppercase123!", // 大文字なし
        "NOLOWERCASE123!", // 小文字なし
        "NoSpecialChar123", // 特殊文字なし
        "NoNumbers!@#"     // 数字なし
    })
    @DisplayName("無効なパスワード")
    void testInvalidPasswords(String password) {
        assertFalse(PasswordValidator.isValid(password));
    }

    @ParameterizedTest
    @CsvSource({
        "admin, admin@example.com, true",
        "user, user@example.com, false",
        "guest, , false"
    })
    void testUserCreation(String username, String email, boolean expectedValid) {
        User user = new User(username, email);
        assertEquals(expectedValid, user.isValid());
    }
}
```

**ネストされたテスト**:
```java
import org.junit.jupiter.api.Nested;

class ShoppingCartTest {

    @Nested
    @DisplayName("空のカートの場合")
    class WhenEmpty {

        private ShoppingCart cart;

        @BeforeEach
        void setUp() {
            cart = new ShoppingCart();
        }

        @Test
        @DisplayName("合計金額は0円")
        void totalShouldBeZero() {
            assertEquals(0, cart.getTotal());
        }

        @Test
        @DisplayName("アイテム追加後は空でない")
        void shouldNotBeEmptyAfterAddingItem() {
            cart.addItem(new Item("Product", 1000));
            assertFalse(cart.isEmpty());
        }
    }

    @Nested
    @DisplayName("アイテムが含まれる場合")
    class WhenHasItems {

        private ShoppingCart cart;

        @BeforeEach
        void setUp() {
            cart = new ShoppingCart();
            cart.addItem(new Item("Product A", 1000));
            cart.addItem(new Item("Product B", 2000));
        }

        @Test
        @DisplayName("合計金額が正しい")
        void totalShouldBeCorrect() {
            assertEquals(3000, cart.getTotal());
        }

        @Test
        @DisplayName("アイテム削除後、合計が更新される")
        void totalShouldUpdateAfterRemoval() {
            cart.removeItem("Product A");
            assertEquals(2000, cart.getTotal());
        }
    }
}
```

---

### 9. テスト（アプリケーション）での活用

**目的**: 包括的なテストスイートの実行、品質保証

**活用方法**:
- CI/CDパイプラインでの自動実行
- コードカバレッジ測定
- リグレッションテスト
- テストレポート生成

**実装例（CI/CD統合）**:

**Maven Surefireプラグイン設定**:
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.2</version>
            <configuration>
                <!-- 並列実行 -->
                <parallel>methods</parallel>
                <threadCount>4</threadCount>

                <!-- テストレポート出力 -->
                <reportsDirectory>${project.build.directory}/surefire-reports</reportsDirectory>

                <!-- タグによるフィルタリング -->
                <groups>unit, integration</groups>
                <excludedGroups>slow</excludedGroups>
            </configuration>
        </plugin>

        <!-- JaCoCo: コードカバレッジ測定 -->
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.11</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
                <execution>
                    <id>jacoco-check</id>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <configuration>
                        <rules>
                            <rule>
                                <element>PACKAGE</element>
                                <limits>
                                    <limit>
                                        <counter>LINE</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.80</minimum>
                                    </limit>
                                </limits>
                            </rule>
                        </rules>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**タグによるテスト分類**:
```java
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class IntegrationTest {

    @Test
    @Tag("unit")
    @Tag("fast")
    void fastUnitTest() {
        // 高速なユニットテスト
    }

    @Test
    @Tag("integration")
    @Tag("slow")
    void slowIntegrationTest() {
        // 時間のかかる統合テスト
    }

    @Test
    @Tag("database")
    void databaseTest() {
        // データベースアクセスが必要なテスト
    }
}
```

**条件付きテスト実行**:
```java
import org.junit.jupiter.api.condition.*;

class ConditionalTest {

    @Test
    @EnabledOnOs(OS.LINUX)
    void testOnLinuxOnly() {
        // Linux環境でのみ実行
    }

    @Test
    @EnabledOnJre(JRE.JAVA_17)
    void testOnJava17Only() {
        // Java 17でのみ実行
    }

    @Test
    @EnabledIfSystemProperty(named = "env", matches = "production")
    void testOnProductionOnly() {
        // システムプロパティ env=production の場合のみ実行
    }

    @Test
    @EnabledIfEnvironmentVariable(named = "CI", matches = "true")
    void testOnCIOnly() {
        // CI環境でのみ実行
    }
}
```

**テストライフサイクル**:
```java
import org.junit.jupiter.api.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class LifecycleTest {

    // クラス全体で1回だけ実行
    @BeforeAll
    static void initAll() {
        System.out.println("Before all tests");
    }

    // 各テストメソッドの前に実行
    @BeforeEach
    void init() {
        System.out.println("Before each test");
    }

    @Test
    void test1() {
        System.out.println("Test 1");
    }

    @Test
    void test2() {
        System.out.println("Test 2");
    }

    // 各テストメソッドの後に実行
    @AfterEach
    void tearDown() {
        System.out.println("After each test");
    }

    // クラス全体で1回だけ実行
    @AfterAll
    static void tearDownAll() {
        System.out.println("After all tests");
    }
}
```

## 公式ドキュメント

- [JUnit 5 公式サイト](https://junit.org/junit5/)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [JUnit 5 API Documentation](https://junit.org/junit5/docs/current/api/)
- [JUnit 5 GitHub Repository](https://github.com/junit-team/junit5)
- [JUnit 4 Documentation](https://junit.org/junit4/)

## 学習リソース

### チュートリアル
- [JUnit 5 Quickstart](https://junit.org/junit5/docs/current/user-guide/#overview-getting-started)
- [Baeldung - JUnit 5 Guide](https://www.baeldung.com/junit-5)
- [Vogella - JUnit Tutorial](https://www.vogella.com/tutorials/JUnit/article.html)

### 書籍
- "JUnit in Action, Third Edition" by Catalin Tudose (Manning)
- "Pragmatic Unit Testing in Java 8 with JUnit" by Jeff Langr
- "Test Driven Development: By Example" by Kent Beck

### 動画・コース
- [JUnit Tutorial for Beginners](https://www.youtube.com/results?search_query=junit+tutorial)
- [Udemy - JUnit & Mockito Crash Course](https://www.udemy.com/topic/junit/)
- [Pluralsight - JUnit 5 Fundamentals](https://www.pluralsight.com/courses/junit-5-fundamentals)

### コミュニティ
- [JUnit 5 Gitter Chat](https://gitter.im/junit-team/junit5)
- [Stack Overflow - JUnit](https://stackoverflow.com/questions/tagged/junit)
- [Stack Overflow - JUnit5](https://stackoverflow.com/questions/tagged/junit5)

## 関連リンク

### 関連ツール
- [Mockito](https://site.mockito.org/) - モックライブラリ（最もよく使われる）
- [JaCoCo](https://www.jacoco.org/) - コードカバレッジ測定ツール
- [AssertJ](https://assertj.github.io/doc/) - 流れるようなアサーション（Fluent Assertions）
- [Hamcrest](http://hamcrest.org/) - マッチャーライブラリ
- [TestContainers](https://www.testcontainers.org/) - Docker統合テスト
- [ArchUnit](https://www.archunit.org/) - アーキテクチャテスト

### JUnit 5拡張
- [JUnit Pioneer](https://junit-pioneer.org/) - JUnit 5の拡張機能集
- [JUnit Params](https://github.com/Pragmatists/JUnitParams) - パラメータ化テスト拡張
- [Spring Test](https://docs.spring.io/spring-framework/docs/current/reference/html/testing.html) - Spring統合

### ベストプラクティス
- [JUnit 5 Best Practices](https://phauer.com/2019/modern-best-practices-testing-java/)
- [Effective Unit Testing](https://www.baeldung.com/java-unit-testing-best-practices)
- [Test Naming Conventions](https://dzone.com/articles/7-popular-unit-test-naming)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

