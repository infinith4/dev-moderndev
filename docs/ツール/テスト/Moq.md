# Moq

## 概要

Moqは、.NET向けの最も広く使われているモッキングライブラリです。LINQ式とラムダ式を活用した直感的なAPIで、インターフェースや仮想メソッドのモックオブジェクトを作成し、単体テストでの依存関係の分離を実現します。Castle DynamicProxyを基盤としたプロキシ生成により、テスト対象のクラスを外部依存から切り離して検証できます。xUnit.net、NUnit、MSTestなど主要なテストフレームワークと組み合わせて使用します。

## 主な機能

### 1. モック作成

- **インターフェースモック**: `Mock<IService>`でインターフェースのモック生成
- **クラスモック**: 仮想メソッドを持つクラスのモック（sealedクラスは不可）
- **Strict/Looseモード**: 未設定メソッド呼び出し時の動作制御
- **コンストラクタ引数**: モック対象クラスへのコンストラクタ引数受け渡し

### 2. セットアップ（振る舞い定義）

- **Setup**: メソッド呼び出し時の戻り値定義
- **SetupSequence**: 呼び出し回数に応じた異なる戻り値
- **SetupProperty**: プロパティのget/set動作定義
- **Callback**: メソッド呼び出し時のコールバック処理
- **Throws**: 例外をスローする設定
- **ReturnsAsync**: 非同期メソッドの戻り値設定

### 3. 検証（Verify）

- **Verify**: メソッドが呼び出されたことの検証
- **VerifyNoOtherCalls**: 想定外の呼び出しがないことの確認
- **Times**: 呼び出し回数の検証（Exactly、AtLeast、AtMost、Never）
- **VerifyAll**: 全Setupが呼び出されたことの確認

### 4. 引数マッチング

- **It.IsAny<T>()**: 任意の引数にマッチ
- **It.Is<T>(predicate)**: 条件に合う引数にマッチ
- **It.IsIn()**: 指定リスト内の値にマッチ
- **It.IsRegex()**: 正規表現パターンにマッチ

## 利用方法

### インストール

```bash
# NuGetパッケージの追加
dotnet add package Moq

# テストプロジェクトへの追加（xUnit.netと併用）
dotnet add package xunit
dotnet add package Moq
```

### 基本的な使用例

```csharp
using Moq;
using Xunit;

public interface IUserRepository
{
    User GetById(int id);
    Task<User> GetByIdAsync(int id);
    void Save(User user);
}

public class UserServiceTests
{
    [Fact]
    public void GetUser_ReturnsUser_WhenExists()
    {
        // Arrange
        var mockRepo = new Mock<IUserRepository>();
        mockRepo.Setup(r => r.GetById(1))
                .Returns(new User { Id = 1, Name = "Alice" });

        var service = new UserService(mockRepo.Object);

        // Act
        var user = service.GetUser(1);

        // Assert
        Assert.Equal("Alice", user.Name);
        mockRepo.Verify(r => r.GetById(1), Times.Once);
    }

    [Fact]
    public async Task GetUserAsync_ReturnsUser()
    {
        var mockRepo = new Mock<IUserRepository>();
        mockRepo.Setup(r => r.GetByIdAsync(It.IsAny<int>()))
                .ReturnsAsync(new User { Id = 1, Name = "Bob" });

        var service = new UserService(mockRepo.Object);
        var user = await service.GetUserAsync(1);

        Assert.Equal("Bob", user.Name);
    }
}
```

### 高度な使用例

```csharp
// シーケンス（呼び出し回数で戻り値を変える）
mockRepo.SetupSequence(r => r.GetById(It.IsAny<int>()))
        .Returns(new User { Name = "First" })
        .Returns(new User { Name = "Second" })
        .Throws(new InvalidOperationException());

// コールバック
var savedUsers = new List<User>();
mockRepo.Setup(r => r.Save(It.IsAny<User>()))
        .Callback<User>(u => savedUsers.Add(u));

// プロパティ
var mockConfig = new Mock<IConfiguration>();
mockConfig.SetupGet(c => c.ConnectionString)
          .Returns("Server=localhost;Database=test");

// 条件付きマッチング
mockRepo.Setup(r => r.GetById(It.Is<int>(id => id > 0)))
        .Returns<int>(id => new User { Id = id });

// Strict モード（未設定メソッド呼び出しで例外）
var strictMock = new Mock<IUserRepository>(MockBehavior.Strict);
```

### protected/internal メンバーのモック

```csharp
// protected メンバー
var mock = new Mock<MyAbstractClass>();
mock.Protected()
    .Setup<int>("ProtectedMethod", ItExpr.IsAny<string>())
    .Returns(42);
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Moq** | 無料 | オープンソース、BSD 3-Clause License |

## メリット

1. **直感的なAPI**: LINQ/ラムダ式による型安全なセットアップ
2. **IDE補完**: Visual Studio/RiderのIntelliSenseで設定ミスを防止
3. **柔軟な検証**: 呼び出し回数、引数パターン、順序の検証が可能
4. **非同期対応**: `ReturnsAsync`/`ThrowsAsync`で非同期メソッドを簡単にモック
5. **軽量**: 追加の依存関係が少なく導入が容易
6. **.NET標準**: .NET開発のデファクトスタンダードモックライブラリ

## デメリット

1. **sealedクラス不可**: sealedクラスや静的メソッドのモックは非対応
2. **プロキシベース**: Castle DynamicProxyに依存し、具象クラスの非仮想メソッドはモック不可
3. **過度なモック**: モックの多用でテストが実装詳細に密結合するリスク
4. **SponsorLink問題**: v4.20でSponsorLink（テレメトリ）が導入され議論に（v4.20.2で削除済み）
5. **パフォーマンス**: 大量のモック生成時にプロキシ生成コストが発生

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **NSubstitute** | 自然言語に近いAPI | Moqより記述がシンプル、機能は同等 |
| **FakeItEasy** | 流暢なAPI | Moqと同等機能、AAA（Arrange-Act-Assert）パターン重視 |
| **Microsoft Fakes** | VS Enterprise機能 | Shimによるstaticメソッドモック可能だが高額 |
| **Bogus** | テストデータ生成 | モックではなくフェイクデータ生成に特化 |

## 公式リンク

- **GitHub**: [https://github.com/devlooped/moq](https://github.com/devlooped/moq)
- **NuGet**: [https://www.nuget.org/packages/Moq](https://www.nuget.org/packages/Moq)
- **ドキュメント**: [https://github.com/devlooped/moq/wiki/Quickstart](https://github.com/devlooped/moq/wiki/Quickstart)

## 関連ドキュメント

- [xUnit.net](./xUnit_net.md)
- [GoMock](./GoMock.md)
- [unittest.mock](./unittest_mock.md)

---

**カテゴリ**: テスト
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
