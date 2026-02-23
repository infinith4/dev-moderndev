# Roslyn Analyzers

## 概要

Roslyn Analyzersは、.NETコンパイラプラットフォーム（Roslyn）に基づくC#/Visual Basicの静的コード解析ツール群です。コードのスタイル、品質、保守性、設計、セキュリティに関する問題をリアルタイムで検出します。.NET 5以降のSDKに標準で含まれており、EditorConfigファイルでルールの重要度やオプションをカスタマイズできます。Visual StudioやVS Codeでの開発中にリアルタイムで警告を表示し、多くの問題は自動修正（Code Fix）にも対応しています。

## 主な機能

### 1. 解析カテゴリ

- **IDExxxx（コードスタイル）**: var使用、式形式メンバー、命名規則など
- **CAxxxx（コード品質）**: パフォーマンス、信頼性、セキュリティ、設計ルール
- **CS/BCxxxx（コンパイラ警告）**: コンパイル時の標準警告

### 2. 主要なルールパッケージ

- **Microsoft.CodeAnalysis.NetAnalyzers**: .NET SDK標準の品質ルール（.NET 5+で自動有効）
- **StyleCop.Analyzers**: 詳細なコードスタイルルール
- **Roslynator**: 500以上の追加アナライザー・リファクタリング
- **SonarAnalyzer.CSharp**: SonarQube互換のルール
- **SecurityCodeScan**: セキュリティ脆弱性検出

### 3. 重要度レベル

- **Error**: ビルドエラーとして扱う
- **Warning**: 警告として表示
- **Suggestion**: 提案として表示（電球アイコン）
- **Silent**: 非表示だが自動修正は利用可能
- **None**: 完全に無効化

### 4. Code Fix（自動修正）

- **リアルタイム修正**: エディタ上で電球アイコンからワンクリック修正
- **一括修正**: ドキュメント/プロジェクト/ソリューション全体に適用
- **dotnet format**: CLI経由での一括自動修正

## 利用方法

### プロジェクトへの導入

```xml
<!-- .csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <!-- コード解析を有効化（.NET 5+ではデフォルトで有効） -->
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <!-- 解析レベル -->
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <!-- 警告をエラーとして扱う -->
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>

  <ItemGroup>
    <!-- 追加アナライザーパッケージ -->
    <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Roslynator.Analyzers" Version="4.12.0">
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
  </ItemGroup>
</Project>
```

### EditorConfigでのルール設定

```ini
# .editorconfig
[*.cs]

# コードスタイル: varの使用
dotnet_style_var_for_built_in_types = true:suggestion
dotnet_style_var_when_type_is_apparent = true:suggestion
dotnet_style_var_elsewhere = true:silent

# コードスタイル: 式形式メンバー
csharp_style_expression_bodied_methods = false:none
csharp_style_expression_bodied_properties = true:suggestion
csharp_style_expression_bodied_constructors = false:none

# コード品質ルールの重要度設定
dotnet_diagnostic.CA1822.severity = warning   # メンバーをstaticにマーク
dotnet_diagnostic.CA2007.severity = warning   # ConfigureAwaitの呼び出し
dotnet_diagnostic.CA1062.severity = error     # パブリックメソッドの引数検証
dotnet_diagnostic.IDE0005.severity = warning  # 不要なusing除去

# 命名規則
dotnet_naming_rule.interface_should_begin_with_i.severity = error
dotnet_naming_rule.interface_should_begin_with_i.symbols = interface
dotnet_naming_rule.interface_should_begin_with_i.style = begins_with_i

dotnet_naming_symbols.interface.applicable_kinds = interface
dotnet_naming_style.begins_with_i.required_prefix = I
dotnet_naming_style.begins_with_i.capitalization = pascal_case
```

### CLIでの実行

```bash
# ビルド時に解析実行（デフォルトで有効）
dotnet build

# コードスタイルの自動修正
dotnet format style

# コード品質の自動修正
dotnet format analyzers

# すべて修正
dotnet format

# ドライラン（確認のみ）
dotnet format --verify-no-changes
```

### CI/CD統合

```yaml
# .github/workflows/analyze.yml
name: Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'
      - run: dotnet restore
      - run: dotnet build --no-restore /p:TreatWarningsAsErrors=true
      - run: dotnet format --verify-no-changes
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **NetAnalyzers** | 無料 | .NET SDK標準搭載 |
| **StyleCop.Analyzers** | 無料 | オープンソース |
| **Roslynator** | 無料 | オープンソース |

## メリット

1. **SDK標準搭載**: .NET 5+で追加インストール不要
2. **リアルタイム解析**: コーディング中にエディタ上で即座にフィードバック
3. **自動修正**: Code Fixで多くの問題をワンクリック修正
4. **EditorConfig統合**: チーム共有可能な設定ファイルでルールを管理
5. **dotnet format**: CLIでの一括修正・CI/CD統合が容易
6. **拡張性**: NuGetパッケージで追加アナライザーを導入可能
7. **カスタムアナライザー**: プロジェクト固有のルールを作成可能

## デメリット

1. **ルール数膨大**: 設定するルール数が多く初期設定に手間がかかる
2. **ビルド時間増加**: アナライザー数が増えるとビルドが遅くなる
3. **偽陽性**: 一部ルールでコンテキストに合わない警告が出る
4. **設定ファイル肥大**: EditorConfigが長くなりやすい
5. **バージョン管理**: アナライザーパッケージのバージョン更新で警告が変化

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **SonarQube** | 統合品質管理プラットフォーム | Roslynより包括的だがサーバ構築が必要 |
| **ReSharper** | JetBrains製コード解析 | Roslynより機能豊富だが有料 |
| **NDepend** | .NET品質・アーキテクチャ解析 | Roslynより高度な依存関係解析 |
| **CodeQL** | GitHub製セキュリティ解析 | セキュリティ特化、CI/CD向け |

## 公式リンク

- **概要**: [https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview)
- **コードスタイルルール**: [https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/)
- **品質ルール**: [https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/)
- **GitHub（roslyn-analyzers）**: [https://github.com/dotnet/roslyn-analyzers](https://github.com/dotnet/roslyn-analyzers)
- **dotnet format**: [https://learn.microsoft.com/dotnet/core/tools/dotnet-format](https://learn.microsoft.com/dotnet/core/tools/dotnet-format)

## 関連ドキュメント

- [.NET Coding Conventions](./DotNET_Coding_Conventions.md)
- [EditorConfig](./EditorConfig.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
