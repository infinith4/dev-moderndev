# ARM Templates Testing Toolkit (ARM-TTK)

## 概要

**ARM Templates Testing Toolkit（ARM-TTK）**は、Azure Resource Manager（ARM）テンプレートの品質をチェックするMicrosoft公式のテストツールです。ベストプラクティス違反、セキュリティ問題、構文エラーを検出し、IaCコードの品質向上を支援します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Microsoft |
| **種別** | IaCテストツール（ARM Template専用） |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://github.com/Azure/arm-ttk |
| **ドキュメント** | https://learn.microsoft.com/azure/azure-resource-manager/templates/test-toolkit |

## 主な特徴

### 1. ベストプラクティスチェック
- パラメータ命名規則
- 変数の適切な使用
- リソースID参照方法
- ハードコードされた値の検出

### 2. セキュリティチェック
- シークレットの平文記述検出
- 安全でない設定の検出
- アクセス制御の妥当性確認

### 3. 構文チェック
- JSON構文エラー
- ARM テンプレート構文エラー
- 関数の誤用

### 4. CI/CD統合
- PowerShell/Azure CLIでの自動実行
- GitHub Actions / Azure Pipelinesとの統合
- カスタムルール追加可能

## 使い方

### インストール

#### PowerShell（Windows/macOS/Linux）

```powershell
# GitHubからクローン
git clone https://github.com/Azure/arm-ttk.git
cd arm-ttk/arm-ttk

# モジュールインポート
Import-Module .\arm-ttk.psd1

# または、PowerShell Galleryから（推奨）
Install-Module -Name arm-ttk -Scope CurrentUser
```

#### Docker

```bash
# Dockerコンテナで実行
docker pull mcr.microsoft.com/azurerm/arm-ttk:latest

# テスト実行
docker run --rm -v $(pwd):/templates mcr.microsoft.com/azurerm/arm-ttk:latest \
  Test-AzTemplate.sh -TemplatePath /templates/azuredeploy.json
```

### 基本的なテスト実行

```powershell
# ARM テンプレートファイルのテスト
Test-AzTemplate -TemplatePath ./azuredeploy.json

# ディレクトリ全体のテスト
Test-AzTemplate -TemplatePath ./templates/

# 詳細出力
Test-AzTemplate -TemplatePath ./azuredeploy.json -Verbose

# 特定のテストのみ実行
Test-AzTemplate -TemplatePath ./azuredeploy.json -Test "Parameters Must Be Referenced"

# 特定のテストをスキップ
Test-AzTemplate -TemplatePath ./azuredeploy.json -Skip "apiVersions Should Be Recent"
```

### テスト結果の出力

```powershell
# JSON形式で出力
$results = Test-AzTemplate -TemplatePath ./azuredeploy.json
$results | ConvertTo-Json -Depth 10 | Out-File results.json

# CSV形式で出力
$results | Export-Csv -Path results.csv -NoTypeInformation

# 結果のフィルタリング（エラーのみ）
$results | Where-Object { $_.Severity -eq 'Error' }

# 結果のフィルタリング（警告のみ）
$results | Where-Object { $_.Severity -eq 'Warning' }
```

### よくあるテストケース

#### 1. Parameters Must Be Referenced（パラメータ参照チェック）

```json
// ❌ 悪い例: 未使用パラメータ
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "parameters": {
    "unusedParameter": {
      "type": "string"
    }
  },
  "resources": []
}

// ✅ 良い例: パラメータを使用
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "parameters": {
    "vmSize": {
      "type": "string",
      "defaultValue": "Standard_D2s_v3"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Compute/virtualMachines",
      "properties": {
        "hardwareProfile": {
          "vmSize": "[parameters('vmSize')]"
        }
      }
    }
  ]
}
```

#### 2. Secure String Parameters Cannot Have Default（セキュアパラメータのデフォルト値禁止）

```json
// ❌ 悪い例: secureStringにデフォルト値
{
  "parameters": {
    "adminPassword": {
      "type": "secureString",
      "defaultValue": "P@ssw0rd123"  // セキュリティリスク
    }
  }
}

// ✅ 良い例: デフォルト値なし
{
  "parameters": {
    "adminPassword": {
      "type": "secureString",
      "metadata": {
        "description": "Administrator password"
      }
    }
  }
}
```

#### 3. Location Should Not Be Hardcoded（ロケーションのハードコード禁止）

```json
// ❌ 悪い例: ロケーションをハードコード
{
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "location": "eastus",  // ハードコード
      "name": "mystorageaccount"
    }
  ]
}

// ✅ 良い例: resourceGroup().locationを使用
{
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "location": "[resourceGroup().location]",
      "name": "[parameters('storageAccountName')]"
    }
  ]
}
```

#### 4. ResourceIds Should Not Contain（リソースID構築ルール）

```json
// ❌ 悪い例: 文字列連結でリソースID構築
{
  "variables": {
    "vnetId": "[concat('/subscriptions/', subscription().subscriptionId, '/resourceGroups/', resourceGroup().name, '/providers/Microsoft.Network/virtualNetworks/', parameters('vnetName'))]"
  }
}

// ✅ 良い例: resourceId関数を使用
{
  "variables": {
    "vnetId": "[resourceId('Microsoft.Network/virtualNetworks', parameters('vnetName'))]"
  }
}
```

### CI/CD パイプライン統合

#### GitHub Actions

```yaml
# .github/workflows/arm-ttk.yml
name: ARM Template Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run ARM-TTK
        uses: docker://mcr.microsoft.com/azurerm/arm-ttk:latest
        with:
          args: Test-AzTemplate.sh -TemplatePath /github/workspace/templates/

      - name: Check results
        run: |
          if [ $? -ne 0 ]; then
            echo "ARM-TTK validation failed"
            exit 1
          fi
```

#### Azure Pipelines

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'windows-latest'

steps:
  - task: PowerShell@2
    displayName: 'Install ARM-TTK'
    inputs:
      targetType: 'inline'
      script: |
        Install-Module -Name arm-ttk -Force -Scope CurrentUser

  - task: PowerShell@2
    displayName: 'Run ARM-TTK Tests'
    inputs:
      targetType: 'inline'
      script: |
        Import-Module arm-ttk
        $results = Test-AzTemplate -TemplatePath ./templates/azuredeploy.json
        $errors = $results | Where-Object { $_.Severity -eq 'Error' }
        if ($errors) {
          Write-Error "ARM-TTK validation failed with $($errors.Count) errors"
          exit 1
        }
```

### カスタムテストルール作成

```powershell
# custom-tests/Storage-Account-Should-Use-HTTPS.test.ps1
<#
.Synopsis
    Ensures storage accounts enforce HTTPS only
.Description
    This test checks that all storage accounts have supportsHttpsTrafficOnly set to true
#>
param(
    [Parameter(Mandatory=$true)]
    [PSObject]
    $TemplateObject
)

$storageAccounts = $TemplateObject.resources | Where-Object {
    $_.type -eq 'Microsoft.Storage/storageAccounts'
}

foreach ($sa in $storageAccounts) {
    if (-not $sa.properties.supportsHttpsTrafficOnly) {
        Write-Error "Storage account $($sa.name) should enforce HTTPS only" -TargetObject $sa
    }
}
```

```powershell
# カスタムテストを実行
Test-AzTemplate -TemplatePath ./azuredeploy.json -TestFolder ./custom-tests/
```

### Bicep ファイルのテスト

```powershell
# Bicep を ARM テンプレートに変換してテスト
az bicep build --file main.bicep

# 生成された ARM テンプレートをテスト
Test-AzTemplate -TemplatePath ./main.json
```

### パラメータファイルのテスト

```powershell
# パラメータファイルも同時にテスト
Test-AzTemplate `
  -TemplatePath ./azuredeploy.json `
  -TemplateParameterPath ./azuredeploy.parameters.json
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **詳細設計（インフラ）** | テンプレート品質チェック | ARM テンプレート設計時の検証 |
| **実装（インフラ）** | IaCコード品質保証 | コーディング中のリアルタイムチェック |
| **CI/CD構築** | 自動品質チェック | パイプラインでの自動検証 |
| **テスト（インフラ）** | デプロイ前検証 | 本番デプロイ前の最終確認 |

## メリット

- **Microsoft公式**: Azure ベストプラクティスに準拠
- **無料・オープンソース**: ライセンス費用不要
- **CI/CD統合容易**: PowerShell/Docker対応
- **カスタマイズ可能**: 独自テストルール追加可能
- **詳細なエラーメッセージ**: 問題箇所と修正方法を明示
- **Bicep対応**: Bicepファイルも間接的にテスト可能

## デメリット

- **ARM Template専用**: Terraform、Pulumi等には非対応
- **実行環境必要**: PowerShell環境またはDocker必要
- **テスト実行時間**: 大規模テンプレートでは時間がかかる
- **誤検知の可能性**: 一部のテストで正当なコードが警告される場合あり
- **日本語ドキュメント少ない**: 英語ドキュメントが主

## 類似ツールとの比較

| ツール | 対象IaC | 特徴 | 適用場面 |
|--------|---------|------|----------|
| **ARM-TTK** | ARM Template | Microsoft公式、ベストプラクティス | Azureインフラ（ARM） |
| **Checkov** | Terraform, ARM, CFN | マルチクラウド、セキュリティ重視 | セキュリティ重視IaC |
| **tflint** | Terraform | Terraform専用、プラグイン豊富 | Terraform品質チェック |
| **cfn-lint** | CloudFormation | AWS公式、CloudFormation専用 | AWS CloudFormation |

## ベストプラクティス

### 1. Pre-commit Hook統合

```bash
# .git/hooks/pre-commit
#!/bin/bash

pwsh -Command "
Import-Module arm-ttk
\$results = Test-AzTemplate -TemplatePath ./templates/
\$errors = \$results | Where-Object { \$_.Severity -eq 'Error' }
if (\$errors) {
    Write-Error 'ARM-TTK validation failed'
    exit 1
}
"
```

### 2. 段階的な導入

```powershell
# フェーズ1: 警告を無視してエラーのみチェック
$results = Test-AzTemplate -TemplatePath ./templates/
$errors = $results | Where-Object { $_.Severity -eq 'Error' }

# フェーズ2: 特定の警告を段階的に修正
$criticalWarnings = $results | Where-Object {
    $_.Severity -eq 'Warning' -and
    $_.Name -in @('Secure String Parameters Cannot Have Default', 'Location Should Not Be Hardcoded')
}
```

### 3. 結果の可視化

```powershell
# HTML レポート生成
$results = Test-AzTemplate -TemplatePath ./templates/
$html = $results | ConvertTo-Html -Property Name, Severity, Message
$html | Out-File report.html
```

### 4. 継続的な改善

```yaml
# Azure Pipelines でトレンド追跡
- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'NUnit'
    testResultsFiles: '**/arm-ttk-results.xml'
    testRunTitle: 'ARM Template Validation'
```

## 公式リソース

- **GitHub**: https://github.com/Azure/arm-ttk
- **ドキュメント**: https://learn.microsoft.com/azure/azure-resource-manager/templates/test-toolkit
- **テストリスト**: https://github.com/Azure/arm-ttk/tree/master/arm-ttk/testcases/deploymentTemplate
- **Azure Docs**: https://learn.microsoft.com/azure/azure-resource-manager/templates/

## まとめ

ARM Templates Testing Toolkit（ARM-TTK）は、Azure Resource Manager テンプレートの品質を保証するMicrosoft公式ツールです。ベストプラクティス、セキュリティ、構文をチェックし、IaCコードの品質向上を支援します。無料でCI/CD統合も容易なため、Azureインフラ開発において必須のツールとして広く採用されています。

---

**最終更新**: 2025-12-06
**対象バージョン**: ARM-TTK v0.18+
