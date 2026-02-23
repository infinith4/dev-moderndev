# xUnit.net

## 概要

xUnit.netは、.NET向けの無料・オープンソースの単体テストフレームワークです。NUnitの作者であるJim Newkirkと、NUnitおよびxUnit.netの設計者であるBrad Wilsonによって開発されました。`[Fact]`属性による基本テスト、`[Theory]`属性によるデータ駆動テストを提供し、テストクラスごとの独立性を重視した設計が特徴です。.NET SDK標準の`dotnet test`コマンドで実行でき、Visual Studio、JetBrains Rider、VS Codeのテストエクスプローラーと統合できます。

## 主な機能

### 1. テスト属性

- **[Fact]**: パラメータなしの基本テストメソッド
- **[Theory]**: データ駆動テスト（パラメータ化テスト）
- **[InlineData]**: Theoryに直接データを渡す
- **[MemberData]**: プロパティやメソッドからデータを供給
- **[ClassData]**: IEnumerable<object[]>を実装するクラスからデータ供給
- **[Trait]**: テストのカテゴリ分類

### 2. アサーション

- **Assert.Equal / Assert.NotEqual**: 値の等価比較
- **Assert.True / Assert.False**: 真偽判定
- **Assert.Null / Assert.NotNull**: null判定
- **Assert.Throws<T>**: 例外発生の検証
- **Assert.ThrowsAsync<T>**: 非同期例外の検証
- **Assert.Contains / Assert.DoesNotContain**: コレクション・文字列の包含チェック
- **Assert.Collection**: コレクション要素の個別検証

### 3. テストライフサイクル

- **コンストラクタ/Dispose**: テストクラスのコンストラクタで初期化、IDisposableで後処理
- **IClassFixture<T>**: テストクラス全体で共有するフィクスチャ
- **ICollectionFixture<T>**: 複数テストクラス間で共有するフィクスチャ
- **IAsyncLifetime**: 非同期の初期化/後処理

### 4. テスト並列実行

- **デフォルト並列**: テストクラス間は並列実行（クラス内は直列）
- **[Collection]**: テストコレクションによる並列制御
- **MaxParallelThreads**: 並列実行スレッド数の制御

## 利用方法

### プロジェクト作成

```bash
# xUnit.netテストプロジェクトの作成
dotnet new xunit -n MyApp.Tests

# 既存プロジェクトにxUnitパッケージを追加
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk

# Moqも一緒に追加（推奨）
dotnet add package Moq
dotnet add package FluentAssertions
```

### 基本テスト（Fact）

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_TwoPositiveNumbers_ReturnsSum()
    {
        // Arrange
        var calculator = new Calculator();

        // Act
        var result = calculator.Add(2, 3);

        // Assert
        Assert.Equal(5, result);
    }

    [Fact]
    public void Divide_ByZero_ThrowsException()
    {
        var calculator = new Calculator();

        Assert.Throws<DivideByZeroException>(
            () => calculator.Divide(10, 0));
    }
}
```

### データ駆動テスト（Theory）

```csharp
public class StringTests
{
    // InlineData: テストメソッドに直接データ指定
    [Theory]
    [InlineData("hello", 5)]
    [InlineData("world", 5)]
    [InlineData("", 0)]
    public void Length_ReturnsCorrectValue(string input, int expected)
    {
        Assert.Equal(expected, input.Length);
    }

    // MemberData: メソッドからデータ供給
    [Theory]
    [MemberData(nameof(GetTestData))]
    public void Contains_ReturnsExpected(string input, string search, bool expected)
    {
        Assert.Equal(expected, input.Contains(search));
    }

    public static IEnumerable<object[]> GetTestData()
    {
        yield return new object[] { "hello world", "hello", true };
        yield return new object[] { "hello world", "xyz", false };
    }
}
```

### フィクスチャ（共有リソース）

```csharp
// テストクラス全体で共有するフィクスチャ
public class DatabaseFixture : IDisposable
{
    public DatabaseFixture()
    {
        Connection = new SqlConnection("Server=localhost;Database=test");
        Connection.Open();
    }

    public SqlConnection Connection { get; }

    public void Dispose()
    {
        Connection.Close();
        Connection.Dispose();
    }
}

public class UserRepositoryTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public UserRepositoryTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void GetUser_ReturnsUser()
    {
        // _fixture.Connection を使用
    }
}

// 非同期フィクスチャ
public class WebAppFixture : IAsyncLifetime
{
    public HttpClient Client { get; private set; }

    public async Task InitializeAsync()
    {
        // WebApplicationFactoryの起動等
        Client = new HttpClient();
    }

    public async Task DisposeAsync()
    {
        Client.Dispose();
    }
}
```

### 設定ファイル

```json
// xunit.runner.json
{
  "$schema": "https://xunit.net/schema/current/xunit.runner.schema.json",
  "maxParallelThreads": 4,
  "diagnosticMessages": true,
  "methodDisplay": "classAndMethod",
  "parallelizeTestCollections": true
}
```

### テスト実行

```bash
# 全テスト実行
dotnet test

# 特定プロジェクトのテスト実行
dotnet test MyApp.Tests/MyApp.Tests.csproj

# フィルタ指定
dotnet test --filter "FullyQualifiedName~UserTests"
dotnet test --filter "Category=Integration"

# 詳細ログ出力
dotnet test --logger "console;verbosity=detailed"

# カバレッジ測定（coverlet）
dotnet test --collect:"XPlat Code Coverage"

# JUnit形式の結果出力
dotnet test --logger "junit;LogFilePath=results.xml"
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/dotnet-test.yml
name: .NET Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'
      - name: Restore
        run: dotnet restore
      - name: Build
        run: dotnet build --no-restore
      - name: Test
        run: dotnet test --no-build --logger "trx" --collect:"XPlat Code Coverage"
      - name: Upload Coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: '**/coverage.cobertura.xml'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **xUnit.net** | 無料 | オープンソース、Apache License 2.0 |

## メリット

1. **.NET標準**: `dotnet new xunit`でプロジェクトテンプレートが標準提供
2. **コンストラクタ/Dispose**: テストごとの初期化/後処理がC#の標準パターンで記述可能
3. **並列実行**: テストクラス間のデフォルト並列実行で高速
4. **Theory**: InlineData/MemberData/ClassDataによる柔軟なデータ駆動テスト
5. **拡張性**: カスタム属性、カスタムアサーションの作成が容易
6. **IDE統合**: Visual Studio/Rider/VS Codeのテストエクスプローラーで実行・デバッグ
7. **コミュニティ**: .NETエコシステムで最もアクティブなテストフレームワーク

## デメリット

1. **[SetUp]/[TearDown]なし**: NUnitの`[SetUp]`に相当する属性がなく、コンストラクタで代替
2. **Assert限定的**: NUnit/FluentAssertionsと比べるとアサーションの種類が少ない
3. **NUnitからの移行**: NUnit経験者は属性名の違いに注意が必要
4. **コレクション共有**: ICollectionFixtureの設定がやや複雑
5. **出力キャプチャ**: `Console.WriteLine`ではなく`ITestOutputHelper`が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **NUnit** | .NETテストフレームワーク | xUnit.netより属性が豊富（SetUp/TearDown等） |
| **MSTest** | Microsoft公式テスト | Visual Studio統合が最も強い |
| **FluentAssertions** | アサーションライブラリ | xUnit.netと併用、可読性の高いアサーション |
| **Shouldly** | アサーションライブラリ | xUnit.netと併用、エラーメッセージが優秀 |

## 公式リンク

- **公式サイト**: [https://xunit.net/](https://xunit.net/)
- **ドキュメント**: [https://xunit.net/docs/getting-started/netcore/cmdline](https://xunit.net/docs/getting-started/netcore/cmdline)
- **GitHub**: [https://github.com/xunit/xunit](https://github.com/xunit/xunit)
- **NuGet**: [https://www.nuget.org/packages/xunit](https://www.nuget.org/packages/xunit)
- **Visual Studio Runner**: [https://www.nuget.org/packages/xunit.runner.visualstudio](https://www.nuget.org/packages/xunit.runner.visualstudio)

## 関連ドキュメント

- [Moq](./Moq.md)
- [Allure Report](./Allure_Report.md)

---

**カテゴリ**: テスト
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
