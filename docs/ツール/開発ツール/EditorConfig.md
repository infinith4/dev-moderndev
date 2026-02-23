# EditorConfig

## 概要

EditorConfigは、異なるエディタやIDE間で一貫したコーディングスタイルを維持するためのファイルフォーマットおよびプラグインの仕組みです。プロジェクトのルートに`.editorconfig`ファイルを配置するだけで、インデントスタイル、文字コード、改行コードなどの基本的なフォーマット設定をチーム全体で統一できます。言語やエディタに依存しないため、多言語プロジェクトでの標準化に特に有効です。

## 主な機能

### 1. 基本プロパティ

- **indent_style**: `tab` または `space` を指定
- **indent_size**: インデント幅（数値指定）
- **tab_width**: タブ文字の表示幅
- **end_of_line**: 改行コード（`lf`、`cr`、`crlf`）
- **charset**: 文字エンコーディング（`utf-8`、`utf-8-bom`等）
- **trim_trailing_whitespace**: 行末空白の自動除去
- **insert_final_newline**: ファイル末尾の改行有無

### 2. グロブパターン

- **`*`**: 任意のファイル名にマッチ
- **`*.{js,ts}`**: 複数拡張子の指定
- **`[Mm]akefile`**: 文字クラス指定
- **`**`**: ディレクトリの再帰的マッチ

### 3. 階層的設定

- **root = true**: 上位ディレクトリの`.editorconfig`検索を停止
- **セクション優先**: ファイル内で後に定義されたルールが優先
- **ディレクトリ階層**: 対象ファイルに近い`.editorconfig`が優先

### 4. エディタ対応

- **ネイティブ対応**: VS Code、Visual Studio、IntelliJ IDEA、GitHub
- **プラグイン対応**: Vim、Emacs、Sublime Text、Atom、Notepad++
- **CI対応**: editorconfig-checker でCI上での検証

## 利用方法

### セットアップ

プロジェクトルートに `.editorconfig` ファイルを作成するだけで、対応エディタが自動的に設定を読み込みます。

### 設定ファイル例

```ini
# EditorConfig is awesome: https://editorconfig.org

# 最上位の設定ファイル
root = true

# 全ファイル共通設定
[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

# JavaScript/TypeScript
[*.{js,jsx,ts,tsx}]
indent_size = 2

# YAML
[*.{yml,yaml}]
indent_size = 2

# Markdown（末尾空白を保持）
[*.md]
trim_trailing_whitespace = false

# Makefile（タブ必須）
[Makefile]
indent_style = tab

# JSON
[*.json]
indent_size = 2

# C#
[*.cs]
indent_size = 4
dotnet_sort_system_directives_first = true

# Go
[*.go]
indent_style = tab
```

### .NET固有の拡張設定

```ini
# .NET / C# 固有のEditorConfig設定
[*.cs]
# var の使用
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion

# 式形式メンバー
csharp_style_expression_bodied_methods = false:none
csharp_style_expression_bodied_properties = true:suggestion

# 命名規則
dotnet_naming_rule.interface_should_begin_with_i.severity = error
dotnet_naming_rule.interface_should_begin_with_i.symbols = interface
dotnet_naming_rule.interface_should_begin_with_i.style = begins_with_i
```

### CI/CDでの検証

```bash
# editorconfig-checker のインストール
npm install -g editorconfig-checker

# チェック実行
editorconfig-checker

# 特定ディレクトリのチェック
editorconfig-checker src/
```

```yaml
# .github/workflows/editorconfig.yml
name: EditorConfig Check

on: [push, pull_request]

jobs:
  editorconfig:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: editorconfig-checker/action-editorconfig-checker@main
      - run: editorconfig-checker
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **EditorConfig** | 無料 | オープンソース、MIT/BSD License |

## メリット

1. **エディタ非依存**: 主要エディタ・IDEの大半で対応
2. **ゼロコンフィグ**: ファイルを置くだけで動作（プラグイン不要のエディタも多い）
3. **言語非依存**: すべてのプログラミング言語に適用可能
4. **階層的設定**: ディレクトリ単位で異なる設定を適用可能
5. **Git管理**: `.editorconfig`ファイルをリポジトリにコミットしてチーム共有
6. **.NET統合**: C#/VBのコードスタイルルールをEditorConfigで設定可能
7. **CI検証**: editorconfig-checkerでCI上での自動検証が可能

## デメリット

1. **基本設定のみ**: インデントや改行など基本的な設定に限定
2. **高度な整形不可**: コード構造の整形にはフォーマッター（Black、Prettier等）が必要
3. **プラグイン必要**: 古いエディタではプラグインのインストールが必要
4. **上書き問題**: エディタ固有の設定と競合する場合がある

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Prettier** | コードフォーマッター | EditorConfigより高度な整形、Web系言語向け |
| **ESLint** | JavaScript/TypeScript リンター | EditorConfigよりルールが豊富 |
| **IDE固有設定** | 各エディタの設定ファイル | エディタ依存だが詳細な設定が可能 |

## 公式リンク

- **公式サイト**: [https://editorconfig.org/](https://editorconfig.org/)
- **仕様書**: [https://spec.editorconfig.org/](https://spec.editorconfig.org/)
- **プロパティ一覧**: [https://github.com/editorconfig/editorconfig/wiki/EditorConfig-Properties](https://github.com/editorconfig/editorconfig/wiki/EditorConfig-Properties)
- **GitHub**: [https://github.com/editorconfig](https://github.com/editorconfig)

## 関連ドキュメント

- [Prettier](./Prettier.md)
- [ESLint](./ESLint.md)
- [Roslyn Analyzers](./Roslyn_Analyzers.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
