# .NET Coding Conventions

## 概要

.NET Coding Conventionsは、Microsoftが提供するC#/.NETの公式コーディング規約です。命名規則、レイアウト規則、コメント規則、言語ガイドラインを包括的に定義しており、EditorConfigファイルとRoslyn Analyzersを組み合わせることで、規約の自動適用・検証が可能です。チーム全体でコードの一貫性と可読性を維持するための標準として広く採用されています。

## 主な規約

### 1. 命名規則

- **PascalCase**: クラス、メソッド、プロパティ、パブリックフィールド
- **camelCase**: ローカル変数、パラメータ
- **_camelCase**: プライベートフィールド（アンダースコアプレフィックス）
- **IPascalCase**: インターフェース（`I`プレフィックス）
- **TPascalCase**: 型パラメータ（`T`プレフィックス）
- **UPPER_CASE**: 定数（`const`）

### 2. レイアウト規則

- **インデント**: スペース4つ
- **波括弧**: Allmanスタイル（新しい行に配置）
- **1行1ステートメント**: 1行に複数の文を書かない
- **1行1宣言**: 1行に複数の変数宣言を書かない
- **空行**: メソッド間、論理ブロック間に空行を挿入
- **行長**: 65文字を超える場合は適切に改行

### 3. 言語ガイドライン

- **var使用**: 型が明らかな場合に`var`を使用
- **string vs String**: 組み込み型エイリアス（`string`、`int`等）を使用
- **式形式メンバー**: 単一式のプロパティ・メソッドで活用
- **パターンマッチング**: `is`/`switch`式の積極的活用
- **null条件演算子**: `?.`、`??`の活用
- **LINQ**: クエリ構文よりメソッド構文を推奨

### 4. コメント規則

- **XMLドキュメント**: パブリックAPI（`///`）
- **行コメント**: `//` を使用（`/* */`は避ける）
- **TODO/HACK**: 一時的な注記にはプレフィックスを付ける

## 利用方法

### EditorConfigでの設定

```ini
# .editorconfig
[*.cs]

# 命名規則: インターフェースはIで始まる
dotnet_naming_rule.interface_should_begin_with_i.severity = error
dotnet_naming_rule.interface_should_begin_with_i.symbols = interface
dotnet_naming_rule.interface_should_begin_with_i.style = begins_with_i

dotnet_naming_symbols.interface.applicable_kinds = interface
dotnet_naming_style.begins_with_i.required_prefix = I
dotnet_naming_style.begins_with_i.capitalization = pascal_case

# 命名規則: プライベートフィールドは_camelCase
dotnet_naming_rule.private_field_should_be_camel_case.severity = warning
dotnet_naming_rule.private_field_should_be_camel_case.symbols = private_field
dotnet_naming_rule.private_field_should_be_camel_case.style = camel_case_with_underscore

dotnet_naming_symbols.private_field.applicable_kinds = field
dotnet_naming_symbols.private_field.applicable_accessibilities = private
dotnet_naming_style.camel_case_with_underscore.required_prefix = _
dotnet_naming_style.camel_case_with_underscore.capitalization = camel_case

# 言語ルール: var の使用
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = true:silent

# 言語ルール: 式形式メンバー
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_properties = true:suggestion
csharp_style_expression_bodied_accessors = true:suggestion

# 言語ルール: パターンマッチング
csharp_style_pattern_matching_over_is_with_cast_check = true:suggestion
csharp_style_pattern_matching_over_as_with_null_check = true:suggestion

# フォーマット: 波括弧
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true

# 組み込み型エイリアスの使用
dotnet_style_predefined_type_for_locals_parameters_members = true:warning
dotnet_style_predefined_type_for_member_access = true:warning

# usingの整理
dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = false
```

### コード例

```csharp
// .NET Coding Conventions に準拠したコード例
using System;
using System.Collections.Generic;
using System.Linq;

namespace MyProject.Services
{
    /// <summary>
    /// ユーザー管理サービス
    /// </summary>
    public class UserService : IUserService
    {
        private readonly IUserRepository _userRepository;
        private readonly ILogger<UserService> _logger;

        public UserService(
            IUserRepository userRepository,
            ILogger<UserService> logger)
        {
            _userRepository = userRepository;
            _logger = logger;
        }

        // 式形式プロパティ
        public int UserCount => _userRepository.Count;

        public async Task<User?> GetUserAsync(int id)
        {
            var user = await _userRepository.FindByIdAsync(id);

            if (user is null)
            {
                _logger.LogWarning("User {Id} not found", id);
                return null;
            }

            return user;
        }

        public IReadOnlyList<User> GetActiveUsers()
        {
            return _userRepository
                .GetAll()
                .Where(u => u.IsActive)
                .OrderBy(u => u.Name)
                .ToList();
        }
    }
}
```

### dotnet formatでの自動適用

```bash
# コードスタイルの自動修正
dotnet format style

# すべてのルールを適用
dotnet format

# ドライラン（変更有無の確認のみ）
dotnet format --verify-no-changes
```

### CI/CD統合

```yaml
# .github/workflows/style.yml
name: Code Style

on: [push, pull_request]

jobs:
  format-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'
      - run: dotnet restore
      - run: dotnet format --verify-no-changes
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **.NET Coding Conventions** | 無料 | Microsoft公式ガイドライン |
| **EditorConfig + Analyzers** | 無料 | .NET SDK標準搭載の自動検証 |

## メリット

1. **Microsoft公式**: .NET開発の標準的なコーディング規約
2. **自動適用**: EditorConfig + Roslyn Analyzersで規約を自動検証
3. **dotnet format**: CLIで一括修正が可能
4. **IDE統合**: Visual Studio / VS Codeでリアルタイム警告
5. **命名規則強制**: EditorConfigで命名規則をエラーとして検出
6. **チーム標準化**: .editorconfigをリポジトリに含めてチーム共有

## デメリット

1. **初期設定コスト**: EditorConfigの設定項目が多い
2. **既存コード適用**: 既存プロジェクトへの適用で大量の変更が発生
3. **チーム合意**: 細かい規約（var使用範囲等）でチーム内議論が必要
4. **完全自動化不可**: 一部の規約（コメント内容等）は手動レビューが必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **StyleCop** | 詳細なスタイルルール | .NET Conventionsより細かいルール |
| **ReSharper** | JetBrains製コード解析 | より包括的だが有料 |
| **SonarQube** | 統合品質管理 | 規約以外にバグ・脆弱性も検出 |

## 公式リンク

- **コーディング規約**: [https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- **コードスタイルルール**: [https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/)
- **命名規則**: [https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/naming-rules](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/naming-rules)
- **dotnet/runtime コーディングスタイル**: [https://github.com/dotnet/runtime/blob/main/docs/coding-guidelines/coding-style.md](https://github.com/dotnet/runtime/blob/main/docs/coding-guidelines/coding-style.md)

## 関連ドキュメント

- [Roslyn Analyzers](./Roslyn_Analyzers.md)
- [EditorConfig](./EditorConfig.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
