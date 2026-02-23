# Pester

## 概要

Pesterは、PowerShell向けのテスティングフレームワークです。BDD（振る舞い駆動開発）スタイルの`Describe`/`It`構文でテストを記述し、PowerShellスクリプト・モジュール・関数の単体テスト、統合テスト、インフラストラクチャテストを実行します。Windows PowerShell 5.1およびPowerShell 7+（クロスプラットフォーム）に対応し、Azure DevOps、GitHub Actionsなどとの統合も容易です。PowerShell 5.1以降にはPester 3.xがプリインストールされています。

## 主な機能

### 1. テスト記述

- **Describe/Context/It**: BDDスタイルのテスト構造化
- **Should**: アサーション（`-Be`、`-BeExactly`、`-Contain`、`-Throw`等）
- **BeforeAll/AfterAll**: テストスイートの前後処理
- **BeforeEach/AfterEach**: 各テストケースの前後処理

### 2. モック

- **Mock**: 関数・コマンドレットのモック化
- **ParameterFilter**: 引数条件付きモック
- **Assert-MockCalled**: モック呼び出し回数の検証
- **Should -Invoke**: Pester 5系のモック検証構文

### 3. テストドライブ

- **TestDrive**: テスト用の一時ファイルシステム（テスト後自動削除）
- **TestRegistry**: テスト用の一時レジストリハイブ（Windows）

### 4. コードカバレッジ

- **-CodeCoverage**: テスト対象スクリプトのカバレッジ測定
- **JaCoCo形式**: カバレッジレポートのXML出力
- **行/関数カバレッジ**: 実行された行と関数の追跡

### 5. 出力・レポート

- **NUnitXml**: NUnit形式のテスト結果出力
- **JUnitXml**: JUnit形式のテスト結果出力
- **CIモード**: CI環境向けの最小出力

## 利用方法

### インストール

```powershell
# PowerShell Gallery からインストール（最新版）
Install-Module -Name Pester -Force -SkipPublisherCheck

# バージョン確認
Get-Module Pester -ListAvailable

# 特定バージョンのインストール
Install-Module -Name Pester -RequiredVersion 5.6.1 -Force
```

### テストの記述

```powershell
# Get-Greeting.Tests.ps1
BeforeAll {
    . $PSScriptRoot/Get-Greeting.ps1
}

Describe 'Get-Greeting' {
    Context 'デフォルト引数の場合' {
        It '既定の挨拶を返す' {
            $result = Get-Greeting
            $result | Should -Be 'Hello, World!'
        }
    }

    Context '名前を指定した場合' {
        It '名前付きの挨拶を返す' {
            $result = Get-Greeting -Name 'Alice'
            $result | Should -Be 'Hello, Alice!'
        }

        It '空文字の場合はエラーをスロー' {
            { Get-Greeting -Name '' } | Should -Throw
        }
    }
}
```

### モックの使用

```powershell
Describe 'Send-Report' {
    It 'メール送信関数を呼び出す' {
        Mock Send-MailMessage {}
        Mock Get-ReportData { return @{ Total = 100 } }

        Send-Report -To 'admin@example.com'

        Should -Invoke Send-MailMessage -Times 1 -Exactly
        Should -Invoke Get-ReportData -Times 1
    }

    It '条件付きモック' {
        Mock Get-Service {
            return @{ Status = 'Running' }
        } -ParameterFilter { $Name -eq 'MyService' }

        Mock Get-Service {
            return @{ Status = 'Stopped' }
        } -ParameterFilter { $Name -eq 'OtherService' }

        (Get-Service -Name 'MyService').Status | Should -Be 'Running'
        (Get-Service -Name 'OtherService').Status | Should -Be 'Stopped'
    }
}
```

### コードカバレッジ

```powershell
# カバレッジ付きテスト実行
$config = New-PesterConfiguration
$config.Run.Path = './tests'
$config.CodeCoverage.Enabled = $true
$config.CodeCoverage.Path = './src/*.ps1'
$config.CodeCoverage.OutputFormat = 'JaCoCo'
$config.CodeCoverage.OutputPath = './coverage.xml'

Invoke-Pester -Configuration $config
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/pester.yml
name: Pester Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Pester Tests
        shell: pwsh
        run: |
          $config = New-PesterConfiguration
          $config.Run.Path = './tests'
          $config.Run.Exit = $true
          $config.TestResult.Enabled = $true
          $config.TestResult.OutputFormat = 'NUnitXml'
          $config.TestResult.OutputPath = './testResults.xml'
          $config.CodeCoverage.Enabled = $true
          $config.CodeCoverage.OutputPath = './coverage.xml'
          Invoke-Pester -Configuration $config
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: |
            testResults.xml
            coverage.xml
```

### Azure DevOps統合

```yaml
# azure-pipelines.yml
steps:
  - task: PowerShell@2
    displayName: 'Run Pester Tests'
    inputs:
      targetType: inline
      pwsh: true
      script: |
        $config = New-PesterConfiguration
        $config.Run.Path = './tests'
        $config.TestResult.Enabled = $true
        $config.TestResult.OutputFormat = 'NUnitXml'
        $config.TestResult.OutputPath = '$(Build.ArtifactStagingDirectory)/testResults.xml'
        Invoke-Pester -Configuration $config
  - task: PublishTestResults@2
    inputs:
      testResultsFormat: NUnit
      testResultsFiles: '**/testResults.xml'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Pester** | 無料 | オープンソース、Apache License 2.0 |

## メリット

1. **PowerShell標準**: PowerShellエコシステムのデファクトテストフレームワーク
2. **BDD構文**: Describe/Context/Itによる読みやすいテスト記述
3. **強力なモック**: 任意のPowerShell関数・コマンドレットをモック可能
4. **TestDrive**: テスト用一時ファイルシステムで副作用を防止
5. **コードカバレッジ**: 組み込みのカバレッジ測定機能
6. **Azure/DevOps親和性**: Azure DevOps、GitHub Actionsとの統合が容易
7. **クロスプラットフォーム**: PowerShell 7+でWindows/macOS/Linuxに対応

## デメリット

1. **PowerShell限定**: PowerShellスクリプト以外のテストには使えない
2. **v4→v5移行**: Pester 4.xから5.xへの破壊的変更が大きい
3. **学習コスト**: BDD構文とPester固有のモック記法の習得が必要
4. **パフォーマンス**: 大量テストの実行時にPowerShellの起動コストが影響
5. **デバッグ**: テスト失敗時のスタックトレースが読みにくい場合がある

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **PSUnit** | PowerShellテスト | Pesterの方が圧倒的にコミュニティが大きい |
| **Selenium + PS** | ブラウザテスト | PowerShellからSeleniumを利用するE2Eテスト |
| **PSScriptAnalyzer** | 静的解析 | テストではなくコード品質チェック（補完的） |

## 公式リンク

- **公式サイト**: [https://pester.dev/](https://pester.dev/)
- **ドキュメント**: [https://pester.dev/docs/quick-start](https://pester.dev/docs/quick-start)
- **GitHub**: [https://github.com/pester/Pester](https://github.com/pester/Pester)
- **PowerShell Gallery**: [https://www.powershellgallery.com/packages/Pester](https://www.powershellgallery.com/packages/Pester)

## 関連ドキュメント

- [xUnit.net](./xUnit_net.md)

---

**カテゴリ**: テスト
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
