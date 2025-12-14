# ASP.NET Core

## 概要

**ASP.NET Core**は、Microsoftが開発するオープンソースのクロスプラットフォームWebフレームワークです。高性能でモジュラー設計を採用し、Windows、macOS、Linuxで動作するモダンなWebアプリケーション、API、マイクロサービスを構築できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Microsoft |
| **種別** | Webアプリケーションフレームワーク |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://dotnet.microsoft.com/apps/aspnet |
| **ドキュメント** | https://learn.microsoft.com/aspnet/core/ |

## 主な特徴

### 1. クロスプラットフォーム
- Windows、macOS、Linux対応
- Dockerコンテナ対応
- クラウドネイティブ（Azure、AWS、GCP）

### 2. 高性能
- 非同期I/O（async/await）
- Kestrel Webサーバー（高速）
- メモリ効率的

### 3. モジュラー設計
- 必要なパッケージのみ追加
- 軽量なランタイム
- Minimal APIs（.NET 6+）

### 4. 統合開発体験
- Visual Studio / VS Code統合
- ホットリロード
- Entity Framework Core（ORM）
- Razor Pages / MVC / Blazor

## 使い方

### インストール

```bash
# .NET SDK インストール（Windows/macOS/Linux）
# https://dotnet.microsoft.com/download

# バージョン確認
dotnet --version

# .NET 8 SDK（最新LTS）
# 8.0.x
```

### プロジェクト作成

#### Web API プロジェクト

```bash
# Web API プロジェクト作成
dotnet new webapi -n MyWebApi
cd MyWebApi

# プロジェクト実行
dotnet run

# ブラウザでアクセス
# https://localhost:7000/swagger
```

#### Minimal API（.NET 6+）

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// サービス追加
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// ミドルウェア設定
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// エンドポイント定義
app.MapGet("/api/users", () =>
{
    return Results.Ok(new[]
    {
        new { Id = 1, Name = "John Doe" },
        new { Id = 2, Name = "Jane Smith" }
    });
});

app.MapGet("/api/users/{id:int}", (int id) =>
{
    if (id <= 0)
        return Results.BadRequest("Invalid user ID");

    return Results.Ok(new { Id = id, Name = $"User {id}" });
});

app.MapPost("/api/users", (User user) =>
{
    // ユーザー作成ロジック
    return Results.Created($"/api/users/{user.Id}", user);
});

app.Run();

record User(int Id, string Name, string Email);
```

#### MVC アプリケーション

```bash
# MVC プロジェクト作成
dotnet new mvc -n MyMvcApp
cd MyMvcApp
dotnet run
```

```csharp
// Controllers/HomeController.cs
using Microsoft.AspNetCore.Mvc;

namespace MyMvcApp.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public IActionResult Index()
    {
        _logger.LogInformation("Index page accessed");
        return View();
    }

    [HttpGet]
    public IActionResult About()
    {
        ViewData["Message"] = "About our application";
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Contact(ContactForm form)
    {
        if (!ModelState.IsValid)
            return View(form);

        // フォーム処理ロジック
        await SendEmailAsync(form);

        return RedirectToAction("ThankYou");
    }

    private async Task SendEmailAsync(ContactForm form)
    {
        // メール送信ロジック
        await Task.CompletedTask;
    }
}

public class ContactForm
{
    [Required]
    public string Name { get; set; }

    [Required]
    [EmailAddress]
    public string Email { get; set; }

    public string Message { get; set; }
}
```

### Entity Framework Core（ORM）

```bash
# EF Core パッケージ追加
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design

# マイグレーションツール（グローバル）
dotnet tool install --global dotnet-ef
```

```csharp
// Data/ApplicationDbContext.cs
using Microsoft.EntityFrameworkCore;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<User> Users { get; set; }
    public DbSet<Post> Posts { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>()
            .HasMany(u => u.Posts)
            .WithOne(p => p.Author)
            .HasForeignKey(p => p.AuthorId);

        modelBuilder.Entity<User>()
            .HasIndex(u => u.Email)
            .IsUnique();
    }
}

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public DateTime CreatedAt { get; set; }
    public ICollection<Post> Posts { get; set; }
}

public class Post
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }
    public int AuthorId { get; set; }
    public User Author { get; set; }
}
```

```csharp
// Program.cs
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
```

```bash
# マイグレーション作成・適用
dotnet ef migrations add InitialCreate
dotnet ef database update
```

### 依存性注入（DI）

```csharp
// Services/IUserService.cs
public interface IUserService
{
    Task<User> GetUserByIdAsync(int id);
    Task<IEnumerable<User>> GetAllUsersAsync();
    Task<User> CreateUserAsync(User user);
}

// Services/UserService.cs
public class UserService : IUserService
{
    private readonly ApplicationDbContext _context;
    private readonly ILogger<UserService> _logger;

    public UserService(ApplicationDbContext context, ILogger<UserService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<User> GetUserByIdAsync(int id)
    {
        _logger.LogInformation("Fetching user {UserId}", id);
        return await _context.Users
            .Include(u => u.Posts)
            .FirstOrDefaultAsync(u => u.Id == id);
    }

    public async Task<IEnumerable<User>> GetAllUsersAsync()
    {
        return await _context.Users.ToListAsync();
    }

    public async Task<User> CreateUserAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user;
    }
}

// Program.cs
builder.Services.AddScoped<IUserService, UserService>();
```

### ミドルウェア

```csharp
// Middleware/RequestLoggingMiddleware.cs
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var startTime = DateTime.UtcNow;

        _logger.LogInformation("Incoming request: {Method} {Path}",
            context.Request.Method,
            context.Request.Path);

        await _next(context);

        var duration = DateTime.UtcNow - startTime;
        _logger.LogInformation("Request completed: {StatusCode} in {Duration}ms",
            context.Response.StatusCode,
            duration.TotalMilliseconds);
    }
}

// Program.cs
app.UseMiddleware<RequestLoggingMiddleware>();
```

### 認証・認可（JWT）

```bash
# JWT パッケージ追加
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

```csharp
// Program.cs
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
        };
    });

builder.Services.AddAuthorization();

app.UseAuthentication();
app.UseAuthorization();

// コントローラーで使用
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class SecureController : ControllerBase
{
    [HttpGet]
    public IActionResult GetSecureData()
    {
        var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        return Ok(new { Message = "Secure data", UserId = userId });
    }

    [Authorize(Roles = "Admin")]
    [HttpDelete("{id}")]
    public IActionResult DeleteUser(int id)
    {
        // 管理者のみ実行可能
        return NoContent();
    }
}
```

### 設定管理

```json
// appsettings.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyAppDb;Trusted_Connection=True;"
  },
  "Jwt": {
    "Key": "YourSuperSecretKeyHere",
    "Issuer": "https://yourdomain.com",
    "Audience": "https://yourdomain.com"
  },
  "AllowedHosts": "*"
}
```

```csharp
// Program.cs
var jwtKey = builder.Configuration["Jwt:Key"];
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
```

### ヘルスチェック

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>();

app.MapHealthChecks("/health");
```

### Docker対応

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MyWebApi/MyWebApi.csproj", "MyWebApi/"]
RUN dotnet restore "MyWebApi/MyWebApi.csproj"
COPY . .
WORKDIR "/src/MyWebApi"
RUN dotnet build "MyWebApi.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "MyWebApi.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyWebApi.dll"]
```

```bash
# Dockerイメージビルド・実行
docker build -t mywebapi .
docker run -p 8080:80 mywebapi
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | Webアプリケーション開発 | API、MVC、Blazor実装 |
| **実装** | マイクロサービス開発 | .NET分散アプリケーション |
| **テスト** | 統合テスト | xUnit/NUnitでのテスト |
| **導入** | 本番デプロイ | Azure App Service、Docker、Kubernetes |

## メリット

- **高性能**: 非同期I/O、Kestrel Webサーバー
- **クロスプラットフォーム**: Windows、macOS、Linux対応
- **無料・オープンソース**: MITライセンス、活発なコミュニティ
- **統合開発環境**: Visual Studio、VS Code統合
- **豊富なライブラリ**: NuGetパッケージエコシステム
- **モジュラー設計**: 必要な機能のみ追加可能
- **クラウドネイティブ**: Azure、AWS、GCP対応
- **Entity Framework Core**: 強力なORM

## デメリット

- **.NET依存**: .NET ランタイム必須
- **Windows歴史的優位**: Windows外でのツール・ライブラリが少ない場合あり
- **学習曲線**: C#言語、.NETエコシステムの習得が必要
- **メモリ消費**: Node.js等に比べてメモリ消費が大きい
- **リリースサイクル**: LTS（Long-Term Support）とSTSの違いに注意

## 類似ツールとの比較

| フレームワーク | 言語 | 特徴 | 適用場面 |
|---------------|------|------|----------|
| **ASP.NET Core** | C# | 高性能、エンタープライズ | .NETエコシステム、エンタープライズ |
| **Spring Boot** | Java | Javaエコシステム、成熟 | Javaエンタープライズ |
| **Express.js** | JavaScript | 軽量、シンプル | Node.js、マイクロサービス |
| **Django** | Python | バッテリー同梱、ORM | Python Webアプリ |

## ベストプラクティス

### 1. 非同期プログラミング

```csharp
// ✅ 良い例: async/await
public async Task<IActionResult> GetUsersAsync()
{
    var users = await _userService.GetAllUsersAsync();
    return Ok(users);
}

// ❌ 悪い例: 同期呼び出し
public IActionResult GetUsers()
{
    var users = _userService.GetAllUsersAsync().Result;  // デッドロックリスク
    return Ok(users);
}
```

### 2. 環境別設定

```json
// appsettings.Development.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  }
}

// appsettings.Production.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning"
    }
  }
}
```

### 3. エラーハンドリング

```csharp
// Program.cs
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}
```

### 4. CORS設定

```csharp
// Program.cs
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp",
        policy => policy.WithOrigins("http://localhost:3000")
                        .AllowAnyHeader()
                        .AllowAnyMethod());
});

app.UseCors("AllowReactApp");
```

## 公式リソース

- **公式サイト**: https://dotnet.microsoft.com/apps/aspnet
- **ドキュメント**: https://learn.microsoft.com/aspnet/core/
- **GitHub**: https://github.com/dotnet/aspnetcore
- **チュートリアル**: https://learn.microsoft.com/aspnet/core/tutorials/
- **.NET Blog**: https://devblogs.microsoft.com/dotnet/

## まとめ

ASP.NET Coreは、高性能でクロスプラットフォーム対応のモダンWebフレームワークです。無料・オープンソースでありながら、エンタープライズレベルの機能を提供し、.NETエコシステムの強力なツール・ライブラリと統合されています。Web API、MVC、Blazorなど多様なアプリケーションタイプに対応し、クラウドネイティブ開発に最適です。

---

**最終更新**: 2025-12-06
**対象バージョン**: ASP.NET Core 8.0 (.NET 8 LTS)
