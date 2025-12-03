# Mockito

## 概要

Mockitoは、Java/Kotlin向けオープンソースモックフレームワークです。ユニットテストでモックオブジェクト作成、スタブ化、検証を行い、依存関係を持つクラスのテストを容易にします。アノテーション、BDD（Behavior-Driven Development）スタイル、スパイ、引数キャプチャにより、JUnit、TestNG等のテストフレームワークと統合し、テスト駆動開発（TDD）を支援します。

## 主な機能

### 1. モック作成
- **@Mock**: モックオブジェクト作成
- **mock()**: プログラマティックモック
- **@Spy**: スパイオブジェクト
- **@InjectMocks**: 依存性注入

### 2. スタブ化
- **when().thenReturn()**: 戻り値設定
- **when().thenThrow()**: 例外スロー
- **doReturn()**: void メソッド
- **Answer**: カスタム動作

### 3. 検証
- **verify()**: メソッド呼び出し検証
- **times()**: 呼び出し回数
- **never()**: 呼び出されていない
- **ArgumentCaptor**: 引数キャプチャ

### 4. Matcher
- **any()**: 任意の引数
- **eq()**: 等価性
- **argThat()**: カスタムマッチャー
- **anyString()**: 任意の文字列

### 5. BDDスタイル
- **given().willReturn()**: BDD given-when-then
- **then().should()**: BDD検証

## 利用方法

### インストール（Maven）

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

### 基本例

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

### スタブ化

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

### 検証

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

### 引数キャプチャ

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

### BDDスタイル

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

### スパイ

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

### Answer

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

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Mockito** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **完全無料**: オープンソース
2. **シンプル**: 学習容易
3. **JUnit統合**: JUnit 5連携
4. **アノテーション**: @Mock、@InjectMocks
5. **BDD**: given-when-then
6. **スパイ**: 実オブジェクト部分モック
7. **引数キャプチャ**: 引数検証
8. **Matcher**: 柔軟なマッチング
9. **活発な開発**: 継続的改善
10. **標準**: Java/Kotlinデファクトスタンダード

## デメリット

### ❌ 制約・課題

1. **Java専用**: Java/Kotlinのみ
2. **final制限**: finalクラス・メソッドモック困難（mockito-inline使用で可能）
3. **staticメソッド**: 標準ではモック不可（mockito-inline必要）
4. **複雑な検証**: 複雑な検証は冗長
5. **学習曲線**: 初心者には難しい
6. **パフォーマンス**: 大量モック生成で遅延
7. **エラーメッセージ**: わかりにくい場合あり
8. **過剰モック**: テストが脆くなりがち

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **JMockit** | Javaモックライブラリ | Mockitoより高機能だが複雑 |
| **PowerMock** | static、finalモック | Mockitoより強力だが非推奨 |
| **EasyMock** | Javaモックライブラリ | Mockitoと類似 |
| **WireMock** | HTTPモック | MockitoよりHTTP特化 |
| **Testcontainers** | 統合テスト | Mockitoより実環境テスト |

## 公式リンク

- **公式サイト**: [https://site.mockito.org/](https://site.mockito.org/)
- **GitHub**: [https://github.com/mockito/mockito](https://github.com/mockito/mockito)
- **JavaDoc**: [https://javadoc.io/doc/org.mockito/mockito-core](https://javadoc.io/doc/org.mockito/mockito-core)

## 関連ドキュメント

- [モックツール一覧](../モックツール/)
- [JUnit](../テストツール/JUnit.md)
- [テストベストプラクティス](../../best-practices/testing.md)

---

**カテゴリ**: モックツール  
**対象工程**: ユニットテスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
