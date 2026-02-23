# Visual Studio

## 概要

Visual Studioは、Microsoftが提供する統合開発環境（IDE）です。.NET、C++、Python、Node.js、Unity等の幅広い言語・フレームワークに対応し、IntelliSenseによる高度なコード補完、強力なデバッガ、プロファイラ、Git統合、Azure DevOps連携を備えています。Visual Studio 2022は64ビットアプリケーションとなり、大規模ソリューションの処理能力が大幅に向上しています。

## 主な機能

### 1. コードエディタ

- **IntelliSense**: コード補完、パラメータ情報、クイック情報、メンバー一覧
- **IntelliCode**: AI支援による行全体の自動補完
- **リファクタリング**: 名前変更、メソッド抽出、シグネチャ変更等
- **コードスニペット**: テンプレートコードの挿入
- **CodeLens**: 参照数、テスト状態、変更履歴の表示

### 2. デバッグ・診断

- **ブレークポイント**: 条件付き、ヒットカウント、トレースポイント
- **ホットリロード**: 実行中のアプリにコード変更を反映（.NET/C++）
- **例外設定**: 例外種類別のブレーク制御
- **診断ツール**: CPU使用率、メモリ使用量、イベントのリアルタイム監視
- **パフォーマンスプロファイラ**: CPU、メモリ、データベース、.NET非同期の解析
- **IntelliTrace**: イベントとスナップショットの履歴デバッグ

### 3. テスト

- **テストエクスプローラー**: xUnit、NUnit、MSTestの統合実行
- **Live Unit Testing**: コード変更時のリアルタイムテスト実行
- **コードカバレッジ**: テストカバレッジの可視化
- **IntelliTest**: 自動テストケース生成

### 4. バージョン管理・チーム開発

- **Git統合**: コミット、ブランチ、マージ、PR管理をIDE内で完結
- **GitHub/Azure DevOps連携**: Issue、PR、CI/CDパイプラインとの統合
- **Live Share**: リアルタイム共同編集・デバッグ
- **コードレビュー**: PR差分の表示・コメント

### 5. ワークロード

- **ASP.NET / Web開発**: Webアプリ、API、Blazor
- **デスクトップ開発**: WPF、WinForms、MAUI
- **モバイル開発**: .NET MAUI、Xamarin
- **Azure開発**: Azure Functions、App Service
- **C++開発**: デスクトップ、ゲーム、Linux
- **Unity**: ゲーム開発
- **Python**: Django、Flask、データサイエンス
- **Node.js**: Express、React

## 利用方法

### インストール

```
1. https://visualstudio.microsoft.com/ からインストーラをダウンロード
2. Visual Studio Installer を実行
3. 必要なワークロードを選択（例: ASP.NET and web development）
4. インストール先を選択して「Install」をクリック
```

### 主要なキーボードショートカット

| 操作 | ショートカット |
|------|--------------|
| ビルド | `Ctrl+Shift+B` |
| デバッグ開始 | `F5` |
| デバッグなし実行 | `Ctrl+F5` |
| ステップオーバー | `F10` |
| ステップイン | `F11` |
| すべてのファイルを検索 | `Ctrl+Shift+F` |
| クイック起動 | `Ctrl+Q` |
| リファクタリング | `Ctrl+.` |
| コードフォーマット | `Ctrl+K, Ctrl+D` |
| テストエクスプローラー | `Ctrl+E, T` |

### EditorConfigとの連携

```ini
# .editorconfig（Visual Studioが自動認識）
[*.cs]
indent_style = space
indent_size = 4
dotnet_style_var_for_built_in_types = true:suggestion
csharp_new_line_before_open_brace = all
```

### 拡張機能の管理

```
1. メニュー: Extensions > Manage Extensions
2. Online タブでマーケットプレイスを検索
3. 推奨拡張機能:
   - ReSharper（JetBrains製コード解析）
   - CodeMaid（コード整理）
   - GitHub Copilot（AI補完）
   - SonarLint（品質チェック）
```

### CI/CD統合（Azure DevOps）

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'windows-latest'

steps:
  - task: NuGetToolInstaller@1
  - task: NuGetCommand@2
    inputs:
      restoreSolution: '**/*.sln'
  - task: VSBuild@1
    inputs:
      solution: '**/*.sln'
      msbuildArgs: '/p:Configuration=Release'
  - task: VSTest@2
    inputs:
      testSelector: 'testAssemblies'
      testAssemblyVer2: '**/*Tests.dll'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Community** | 無料 | 個人、学生、OSS開発、5人以下の組織 |
| **Professional** | 有料（月額/年額） | 小〜中規模チーム向け、CodeLens、テストツール |
| **Enterprise** | 有料（月額/年額） | 大規模チーム向け、IntelliTrace、Live Unit Testing、アーキテクチャツール |

## メリット

1. **統合デバッガ**: ブレークポイント、ホットリロード、IntelliTraceなど業界最高クラス
2. **IntelliSense/IntelliCode**: AI支援による高度なコード補完
3. **ワークロード**: 16種類以上のワークロードで幅広い開発に対応
4. **Azure統合**: Azure DevOps、Azure Functions等とのシームレスな連携
5. **Live Share**: リアルタイム共同編集で場所を問わないペアプログラミング
6. **Community版無料**: 個人開発者・OSSプロジェクトは無料で利用可能
7. **テスト統合**: テストエクスプローラーで主要テストフレームワークを統合
8. **64ビット対応**: 大規模ソリューションでもメモリ制限なし

## デメリット

1. **インストールサイズ**: ワークロード次第で数十GBの容量が必要
2. **Windows専用**: macOS版（Visual Studio for Mac）は2024年に廃止
3. **起動時間**: 大規模ソリューションのロードに時間がかかる
4. **リソース消費**: メモリ・CPU消費が大きい
5. **Enterprise高額**: Enterprise版のライセンス費用が高い
6. **アップデート頻度**: 頻繁なアップデートで作業が中断される場合がある

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **VS Code** | 軽量エディタ | Visual Studioより軽量、拡張機能で機能追加 |
| **JetBrains Rider** | .NET向けIDE | Visual Studioよりクロスプラットフォーム対応 |
| **IntelliJ IDEA** | Java向けIDE | Java/Kotlin開発に特化 |
| **Eclipse** | OSS IDE | 無料だがVisual Studioより機能が限定的 |

## 公式リンク

- **公式サイト**: [https://visualstudio.microsoft.com/](https://visualstudio.microsoft.com/)
- **ドキュメント**: [https://learn.microsoft.com/visualstudio/](https://learn.microsoft.com/visualstudio/)
- **リリースノート**: [https://learn.microsoft.com/visualstudio/releases/2022/release-notes](https://learn.microsoft.com/visualstudio/releases/2022/release-notes)
- **マーケットプレイス**: [https://marketplace.visualstudio.com/](https://marketplace.visualstudio.com/)
- **Visual Studio Blog**: [https://devblogs.microsoft.com/visualstudio/](https://devblogs.microsoft.com/visualstudio/)

## 関連ドキュメント

- [Roslyn Analyzers](../開発ツール/Roslyn_Analyzers.md)
- [.NET Coding Conventions](../開発ツール/DotNET_Coding_Conventions.md)
- [EditorConfig](../開発ツール/EditorConfig.md)

---

**カテゴリ**: IDEツール
**対象工程**: 実装・テスト・デバッグ
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
