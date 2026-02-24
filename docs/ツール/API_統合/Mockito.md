# Mockito

## 概要

Mockitoは、Java/Kotlin向けオープンソースモックフレームワークです。ユニットテストでモックオブジェクト作成、スタブ化、検証を行い、依存関係を持つクラスのテストを容易にします。アノテーション、BDD（Behavior-Driven Development）スタイル、スパイ、引数キャプチャにより、JUnit、TestNG等のテストフレームワークと統合し、テスト駆動開発（TDD）を支援します。

## 主な特徴

| 項目 | 内容 |
|------|------|
| オープンソース | MIT License、無料で利用可能 |
| シンプルなAPI | 直感的なAPI設計で学習が容易 |
| JUnit統合 | JUnit 5とのシームレスな統合 |
| アノテーション | @Mock、@InjectMocks、@Spyで簡潔に記述 |
| BDDスタイル | given-when-thenパターンをサポート |
| 引数キャプチャ | ArgumentCaptorによる引数検証 |
| Java/Kotlinデファクト | Java/Kotlinモックフレームワークの標準 |

## 主な機能

### モック作成

| 機能 | 説明 |
|------|------|
| @Mock | アノテーションによるモックオブジェクト作成 |
| mock() | プログラマティックなモック生成 |
| @Spy | 実オブジェクトの部分モック（スパイ） |
| @InjectMocks | モックの依存性自動注入 |

### スタブ化

| 機能 | 説明 |
|------|------|
| when().thenReturn() | 戻り値の設定 |
| when().thenThrow() | 例外のスロー |
| doReturn() | voidメソッドへのスタブ設定 |
| Answer | カスタム動作の定義 |

### 検証

| 機能 | 説明 |
|------|------|
| verify() | メソッド呼び出しの検証 |
| times() | 呼び出し回数の指定 |
| never() | 呼び出されていないことの検証 |
| ArgumentCaptor | 引数のキャプチャと検証 |

### Matcher

| 機能 | 説明 |
|------|------|
| any() | 任意の引数にマッチ |
| eq() | 等価性でマッチ |
| argThat() | カスタムマッチャー |
| anyString() | 任意の文字列にマッチ |

## インストールとセットアップ

公式URL:
- [Mockito 公式サイト](https://site.mockito.org/)
- [GitHub リポジトリ](https://github.com/mockito/mockito)
- [JavaDoc](https://javadoc.io/doc/org.mockito/mockito-core)

### Maven

```xml
<dependencies>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.8.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <version>5.8.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## 基本的な使い方

### 1. 基本的なモックとスタブ

```java
// テスト対象クラス
public class UserService {
    private UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUserById(Long id) {
        return userRepository.findById(id);
    }
}

// リポジトリインターフェース
public interface UserRepository {
    User findById(Long id);
}

// テストクラス
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void testGetUserById() {
        // モック設定
        User mockUser = new User(1L, "John Doe");
        when(userRepository.findById(1L)).thenReturn(mockUser);

        // テスト実行
        User result = userService.getUserById(1L);

        // 検証
        assertEquals("John Doe", result.getName());
        verify(userRepository).findById(1L);
    }
}
```

### 2. スタブ化

```java
@Test
void testStubbing() {
    List<String> mockList = mock(List.class);

    // 戻り値設定
    when(mockList.get(0)).thenReturn("first");
    when(mockList.get(1)).thenReturn("second");

    assertEquals("first", mockList.get(0));
    assertEquals("second", mockList.get(1));
    assertNull(mockList.get(999)); // スタブされていない

    // 例外スロー
    when(mockList.get(anyInt())).thenThrow(new RuntimeException());
    assertThrows(RuntimeException.class, () -> mockList.get(0));
}
```

### 3. 検証

```java
@Test
void testVerification() {
    List<String> mockList = mock(List.class);

    mockList.add("one");
    mockList.add("two");
    mockList.add("two");

    // 呼び出し検証
    verify(mockList).add("one");
    verify(mockList, times(2)).add("two");
    verify(mockList, never()).add("three");
    verify(mockList, atLeast(1)).add("one");
    verify(mockList, atMost(3)).add(anyString());
}
```

### 4. 引数キャプチャ

```java
@Test
void testArgumentCaptor() {
    UserRepository mockRepo = mock(UserRepository.class);
    UserService service = new UserService(mockRepo);

    User newUser = new User(1L, "Alice");
    service.saveUser(newUser);

    // 引数キャプチャ
    ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);
    verify(mockRepo).save(userCaptor.capture());

    User capturedUser = userCaptor.getValue();
    assertEquals("Alice", capturedUser.getName());
}
```

### 5. BDDスタイル

```java
import static org.mockito.BDDMockito.*;

@Test
void testBDDStyle() {
    // Given
    UserRepository mockRepo = mock(UserRepository.class);
    User mockUser = new User(1L, "Bob");
    given(mockRepo.findById(1L)).willReturn(mockUser);

    UserService service = new UserService(mockRepo);

    // When
    User result = service.getUserById(1L);

    // Then
    then(mockRepo).should().findById(1L);
    assertEquals("Bob", result.getName());
}
```

### 6. スパイ

```java
@Test
void testSpy() {
    List<String> list = new ArrayList<>();
    List<String> spyList = spy(list);

    // 実際のメソッド呼び出し
    spyList.add("one");
    spyList.add("two");

    assertEquals(2, spyList.size());
    assertEquals("one", spyList.get(0));

    // スタブ化も可能
    when(spyList.size()).thenReturn(100);
    assertEquals(100, spyList.size());

    verify(spyList).add("one");
}
```

### 7. Answer

```java
@Test
void testAnswer() {
    UserRepository mockRepo = mock(UserRepository.class);

    when(mockRepo.findById(anyLong())).thenAnswer(invocation -> {
        Long id = invocation.getArgument(0);
        return new User(id, "User" + id);
    });

    User user = mockRepo.findById(5L);
    assertEquals("User5", user.getName());
}
```

## CI/CD 統合

### GitHub Actions

```yaml
name: Unit Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

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
      - name: Run Tests
        run: mvn test
```

### GitLab CI

```yaml
unit_test:
  stage: test
  image: maven:3.9-eclipse-temurin-17
  script:
    - mvn test
  artifacts:
    reports:
      junit: target/surefire-reports/*.xml
    when: always
```

## 他ツールとの比較

### Mockito vs JMockit

| 機能 | Mockito | JMockit |
|------|---------|---------|
| API | シンプル・直感的 | 高機能だが複雑 |
| finalクラス | mockito-inlineで対応 | 標準対応 |
| staticメソッド | mockito-inline必要 | 標準対応 |
| コミュニティ | 非常に活発 | 小規模 |
| 学習曲線 | 低い | 高い |

### Mockito vs PowerMock

| 機能 | Mockito | PowerMock |
|------|---------|-----------|
| finalモック | mockito-inline | 標準対応 |
| staticモック | mockito-inline | 標準対応 |
| メンテナンス | 活発 | 非推奨傾向 |
| JUnit 5 | 完全対応 | 限定的 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| ユニットテスト | 依存関係を分離したテスト | モックオブジェクトで外部依存を置換 |
| TDD | テスト駆動開発の実践 | モックで未実装の依存をスタブ化 |
| リポジトリ層テスト | DB接続なしでサービス層テスト | リポジトリをモック化してビジネスロジック検証 |
| 外部API統合テスト | 外部サービス呼び出しのテスト | HTTPクライアントをモック化 |

## ベストプラクティス

### 1. 適切なモック範囲

- テスト対象クラスの直接的な依存のみモック化する
- 過剰なモックはテストの信頼性を下げる
- 値オブジェクトやDTOはモックせず実オブジェクトを使用する

### 2. 検証の適切な利用

- 振る舞い（メソッド呼び出し）の検証は必要最小限にする
- 戻り値の検証を優先し、verifyは副作用の確認に限定する
- times()の過度な使用は脆いテストの原因になる

### 3. テストの可読性

- BDDスタイル（given-when-then）で構造化する
- テストメソッド名は振る舞いを明確に記述する
- Arrangeブロックを小さく保つ

## トラブルシューティング

### よくある問題と解決策

#### 1. finalクラス/メソッドのモックが失敗する

```
原因: Mockitoのデフォルトではfinalクラス/メソッドをモックできない
解決策:
- mockito-inlineをdependencyに追加する
- またはMockito 5以降を使用する（デフォルトでinline有効）
```

#### 2. @InjectMocksで依存が注入されない

```
原因: コンストラクタやフィールドの型が一致しない
解決策:
- テスト対象クラスのコンストラクタ引数の型を確認する
- @Mockフィールドの型が正しいか確認する
- @ExtendWith(MockitoExtension.class)が付与されているか確認する
```

#### 3. UnnecessaryStubbingException

```
原因: 定義したスタブがテスト中に使用されていない
解決策:
- 不要なスタブ定義を削除する
- lenient()を使用して厳密な検証を緩和する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://site.mockito.org/
- ドキュメント: https://javadoc.io/doc/org.mockito/mockito-core

### コミュニティ
- GitHub: https://github.com/mockito/mockito

### チュートリアル
- Getting Started: https://site.mockito.org/#how
- Mockito Wiki: https://github.com/mockito/mockito/wiki

## まとめ

Mockitoは、以下の場面で特に有用です:

1. **Javaユニットテスト** - 依存関係を分離してクラス単体のテストを実現
2. **テスト駆動開発（TDD）** - 未実装の依存をモックで置換し開発を進行
3. **CI/CDパイプライン** - JUnit統合により自動テストに組み込み品質を維持

Java/Kotlinでのユニットテストにおけるデファクトスタンダードとして、シンプルなAPIと豊富な機能により生産性の高いテスト開発を実現する。
