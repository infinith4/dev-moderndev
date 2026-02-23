# NuGet

## 概要

NuGetは、.NETエコシステムにおける公式パッケージマネージャーです。nuget.orgを中心としたパブリックレジストリから、数十万のライブラリを検索・インストール・更新できます。`dotnet` CLIおよびVisual Studioと密接に統合されており、PackageReference形式による宣言的な依存関係管理、Central Package Management（CPM）によるソリューション全体のバージョン一元管理、Azure ArtifactsやGitHub Packagesなどのプライベートフィードとの連携、脆弱性監査機能など、エンタープライズ開発に必要な機能を備えています。

## 主な機能

### 1. パッケージ管理
- **PackageReference**: csprojファイルでの宣言的な依存関係定義
- **パッケージ復元**: `dotnet restore` による自動復元
- **バージョン管理**: セマンティックバージョニング対応
- **推移的依存関係**: 依存関係の自動解決

### 2. Central Package Management (CPM)
- **Directory.Packages.props**: ソリューション全体のバージョン一元管理
- **バージョン統一**: 複数プロジェクト間でのバージョン一貫性
- **オーバーライド**: プロジェクト単位での例外指定

### 3. プライベートフィード
- **Azure Artifacts**: Azure DevOpsとの統合
- **GitHub Packages**: GitHubリポジトリとの連携
- **NuGet.config**: フィード設定の管理
- **認証**: トークンベースの認証

### 4. セキュリティ
- **脆弱性監査**: `dotnet list package --vulnerable`
- **署名付きパッケージ**: パッケージの改ざん検知
- **ライセンス確認**: 依存パッケージのライセンス確認
- **非推奨パッケージ警告**: 非推奨パッケージの検出

### 5. CI/CD統合
- **GitHub Actions**: ワークフローでのパッケージ復元・公開
- **Azure Pipelines**: パイプラインでの自動化
- **キャッシュ**: パッケージキャッシュによるビルド高速化

## 利用方法

### パッケージのインストール

```bash
# dotnet CLIでパッケージを追加
dotnet add package Newtonsoft.Json

# バージョン指定
dotnet add package Newtonsoft.Json --version 13.0.3

# プレリリース版を含む
dotnet add package Newtonsoft.Json --prerelease

# 特定プロジェクトに追加
dotnet add src/MyApp/MyApp.csproj package Serilog
```

### PackageReference（csproj）

```xml
<!-- MyApp.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Serilog" Version="3.1.1" />
    <PackageReference Include="Serilog.Sinks.Console" Version="5.0.1" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
  </ItemGroup>
</Project>
```

### Central Package Management

```xml
<!-- Directory.Packages.props（ソリューションルートに配置） -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageVersion Include="Serilog" Version="3.1.1" />
    <PackageVersion Include="xunit" Version="2.7.0" />
    <PackageVersion Include="Moq" Version="4.20.70" />
  </ItemGroup>
</Project>
```

```xml
<!-- 各プロジェクトのcsproj（Versionを省略） -->
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" />
    <PackageReference Include="Serilog" />
  </ItemGroup>
</Project>
```

### NuGet.config設定

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <!-- パッケージソースの定義 -->
  <packageSources>
    <clear />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
    <add key="Azure Artifacts" value="https://pkgs.dev.azure.com/myorg/_packaging/myfeed/nuget/v3/index.json" />
    <add key="GitHub Packages" value="https://nuget.pkg.github.com/myorg/index.json" />
  </packageSources>

  <!-- 認証情報 -->
  <packageSourceCredentials>
    <GitHub_Packages>
      <add key="Username" value="USERNAME" />
      <add key="ClearTextPassword" value="%GITHUB_TOKEN%" />
    </GitHub_Packages>
  </packageSourceCredentials>

  <!-- パッケージソースのマッピング -->
  <packageSourceMapping>
    <packageSource key="nuget.org">
      <package pattern="*" />
    </packageSource>
    <packageSource key="Azure Artifacts">
      <package pattern="MyCompany.*" />
    </packageSource>
  </packageSourceMapping>
</configuration>
```

### パッケージの管理コマンド

```bash
# インストール済みパッケージ一覧
dotnet list package

# 更新可能なパッケージ確認
dotnet list package --outdated

# 脆弱性のあるパッケージ確認
dotnet list package --vulnerable

# 非推奨パッケージ確認
dotnet list package --deprecated

# パッケージの更新
dotnet add package Newtonsoft.Json --version 13.0.3

# パッケージの削除
dotnet remove package Newtonsoft.Json

# パッケージの復元
dotnet restore

# キャッシュクリア
dotnet nuget locals all --clear
```

### パッケージの作成と公開

```xml
<!-- ライブラリプロジェクトのcsproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <PackageId>MyCompany.MyLibrary</PackageId>
    <Version>1.0.0</Version>
    <Authors>My Team</Authors>
    <Description>社内共通ライブラリ</Description>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
    <GeneratePackageOnBuild>true</GeneratePackageOnBuild>
  </PropertyGroup>
</Project>
```

```bash
# パッケージの作成
dotnet pack --configuration Release

# nuget.orgへの公開
dotnet nuget push bin/Release/MyCompany.MyLibrary.1.0.0.nupkg \
  --api-key $NUGET_API_KEY \
  --source https://api.nuget.org/v3/index.json

# Azure Artifactsへの公開
dotnet nuget push bin/Release/MyCompany.MyLibrary.1.0.0.nupkg \
  --api-key az \
  --source "Azure Artifacts"
```

### CI/CD統合

```yaml
# .github/workflows/nuget.yml
name: NuGet Package

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Restore packages
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore --configuration Release

      - name: Test
        run: dotnet test --no-build --configuration Release

      - name: Check vulnerabilities
        run: dotnet list package --vulnerable --include-transitive

      - name: Pack
        if: github.ref == 'refs/heads/main'
        run: dotnet pack --no-build --configuration Release

      - name: Push to NuGet
        if: github.ref == 'refs/heads/main'
        run: dotnet nuget push **/*.nupkg --api-key ${{ secrets.NUGET_API_KEY }} --source https://api.nuget.org/v3/index.json
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **NuGet CLI / dotnet CLI** | 無料 | オープンソース、Apache-2.0 License |
| **nuget.org** | 無料 | パブリックパッケージレジストリ |
| **Azure Artifacts** | 2 GiBまで無料 | プライベートフィード、Azure DevOps統合 |
| **GitHub Packages** | 500 MBまで無料 | GitHubリポジトリ統合 |

## メリット

### 主な利点

1. **.NET標準**: .NET SDKに組み込まれた公式パッケージマネージャー
2. **大規模レジストリ**: nuget.orgに40万以上のパッケージ
3. **宣言的管理**: PackageReferenceによる明確な依存関係定義
4. **CPM対応**: ソリューション全体のバージョン一元管理
5. **セキュリティ**: 脆弱性監査・署名・ライセンス確認
6. **Visual Studio統合**: GUIからの直感的なパッケージ管理
7. **プライベートフィード**: 社内パッケージの配布基盤
8. **推移的依存解決**: 依存関係の自動解決
9. **キャッシュ**: グローバルパッケージキャッシュによる高速復元
10. **クロスプラットフォーム**: Windows/macOS/Linux対応

## デメリット

### 制約・課題

1. **.NET限定**: .NETエコシステム以外では利用不可
2. **バージョン競合**: 推移的依存関係でのバージョン競合
3. **packages.config**: レガシー形式からの移行コスト
4. **パッケージサイズ**: 大規模パッケージのダウンロード時間
5. **オフライン対応**: オフライン環境での運用に事前準備が必要
6. **CPM学習**: Central Package Managementの設計理解が必要
7. **フィード管理**: 複数フィード運用時の設定複雑化

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Paket** | 代替.NETパッケージマネージャー | NuGetよりロック管理が厳密 |
| **npm** | Node.jsパッケージマネージャー | JavaScript/TypeScriptエコシステム |
| **pip** | Pythonパッケージマネージャー | Pythonエコシステム |
| **Maven** | Javaビルド・依存管理 | JVMエコシステム |
| **Cargo** | Rustパッケージマネージャー | Rustエコシステム |

## 公式リンク

- **公式ドキュメント**: [https://learn.microsoft.com/nuget/](https://learn.microsoft.com/nuget/)
- **nuget.org**: [https://www.nuget.org/](https://www.nuget.org/)
- **GitHub**: [https://github.com/NuGet/Home](https://github.com/NuGet/Home)
- **NuGet CLI**: [https://learn.microsoft.com/nuget/reference/nuget-exe-cli-reference](https://learn.microsoft.com/nuget/reference/nuget-exe-cli-reference)
- **CPMガイド**: [https://learn.microsoft.com/nuget/consume-packages/central-package-management](https://learn.microsoft.com/nuget/consume-packages/central-package-management)

## 関連ドキュメント

- [パッケージ管理ツール一覧](../パッケージ管理ツール/)
- [Visual Studio](../IDEツール/Visual_Studio.md)
- [Azure Artifacts](../クラウドプラットフォームツール/)

---

**カテゴリ**: パッケージ管理ツール
**対象工程**: 実装・ビルド
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
