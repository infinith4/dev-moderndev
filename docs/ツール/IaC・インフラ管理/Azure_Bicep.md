# Azure Bicep

## 概要

Azure Bicepは、Microsoftが開発したAzure Resource Manager (ARM) テンプレートのための宣言型言語です。JSONベースのARMテンプレートをより簡潔で読みやすい構文で記述できるDSL（ドメイン固有言語）として設計されています。BicepはARMテンプレートにトランスパイルされ、Azureリソースのデプロイに使用されます。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Bicep CLI** |  無料 | オープンソース、ローカル実行 |
| **Azure Resource Manager** |  無料 | デプロイ自体は無料 |
| **デプロイされたリソース** |  従量課金 | 作成されたAzureリソースの料金は別途発生 |

**注意**: Bicep自体とAzure Resource Managerは無料ですが、作成されたAzureリソース（VM、Database等）は通常のAzure料金が発生します。

## メリット・デメリット

### メリット
-  **簡潔な構文**: JSONと比較して50%以上コード量を削減
-  **型安全**: IntelliSense、型チェック、構文検証
-  **モジュール化**: 再利用可能なモジュールで管理を効率化
-  **無料**: オープンソース、Azureネイティブサービス
-  **ARMテンプレート互換**: 既存ARMテンプレートをDecompile可能
-  **VS Code統合**: 拡張機能で強力な開発体験
-  **What-Ifデプロイ**: 変更内容を事前プレビュー可能
-  **自動依存関係管理**: リソース間の依存関係を自動解決

### デメリット
-  **Azure専用**: Azureリソースのみ対応、マルチクラウド不可
-  **比較的新しい**: Terraform等と比較してコミュニティが小さい
-  **学習リソース**: TerraformやCloudFormationと比較して資料が少ない
-  **ARMテンプレートの制約**: 基盤となるARMテンプレートの制限を継承
-  **状態管理なし**: Terraformのような明示的な状態ファイル管理なし

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **6. 詳細設計（インフラ）** | Azureインフラ構成のコード化設計 | Bicepテンプレート設計書、モジュール設計 |
| **8. インフラ構築** | 実際のAzureリソースのプロビジョニング | Bicepテンプレート、デプロイ結果 |
| **10. テスト（インフラ）** | インフラのテスト、変更の検証 | テスト結果、検証レポート |
| **11. 導入** | 本番環境へのインフラデプロイ | デプロイ手順書、本番環境構成 |

## 基本的な利用方法

### 1. Bicep CLIのインストール

```bash
# Windows (Chocolatey)
choco install bicep

# macOS (Homebrew)
brew install bicep

# Linux (Azure CLI経由)
az bicep install

# Azure CLI内蔵版の利用（推奨）
az bicep version

# VS Code拡張機能のインストール
code --install-extension ms-azuretools.vscode-bicep
```

### 2. Azure CLIのインストール

```bash
# macOS (Homebrew)
brew install azure-cli

# Windows (MSI Installer)
# https://aka.ms/installazurecliwindows からダウンロード

# Linux (スクリプト)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Azure へのログイン
az login
```

### 3. 基本的なワークフロー

```bash
# 1. Bicepファイルのビルド（ARMテンプレートへ変換）
az bicep build --file main.bicep

# 2. What-Ifデプロイ（変更内容のプレビュー）
az deployment group what-if \
  --resource-group myResourceGroup \
  --template-file main.bicep

# 3. デプロイ
az deployment group create \
  --resource-group myResourceGroup \
  --template-file main.bicep \
  --parameters parameters.json

# 4. ARMテンプレートをBicepに逆変換（Decompile）
az bicep decompile --file template.json
```

### 4. 基本的なBicepコード例

```bicep
// main.bicep
@description('Azure リージョン')
param location string = resourceGroup().location

@description('環境名')
@allowed([
  'dev'
  'staging'
  'prod'
])
param environment string

@description('VNetのアドレス空間')
param vnetAddressPrefix string = '10.0.0.0/16'

// 仮想ネットワークの作成
resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
  name: 'vnet-${environment}'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        vnetAddressPrefix
      ]
    }
  }
}

// サブネットの作成
resource subnet 'Microsoft.Network/virtualNetworks/subnets@2023-04-01' = {
  parent: vnet
  name: 'subnet-public'
  properties: {
    addressPrefix: '10.0.1.0/24'
  }
}

// 出力
output vnetId string = vnet.id
output subnetId string = subnet.id
```

## 工程別の活用方法

### 6. 詳細設計（インフラ）での活用

**目的**: Azureインフラ構成をBicepコードとして設計

**活用方法**:
- リソースの依存関係を明確化
- モジュール構造の設計
- パラメータと出力の定義
- デプロイスコープの設計（サブスクリプション/リソースグループ）

**モジュール設計例**:
```bicep
// modules/vnet.bicep
@description('VNet名')
param vnetName string

@description('ロケーション')
param location string

resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
  }
}

output vnetId string = vnet.id
```

```bicep
// main.bicep（モジュールを使用）
module vnetModule './modules/vnet.bicep' = {
  name: 'vnetDeployment'
  params: {
    vnetName: 'my-vnet'
    location: location
  }
}

output vnetId string = vnetModule.outputs.vnetId
```

**パラメータファイル（parameters.json）**:
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": {
      "value": "dev"
    },
    "location": {
      "value": "japaneast"
    }
  }
}
```

---

### 8. インフラ構築での活用

**目的**: 設計したAzureインフラを実際にプロビジョニング

**活用方法**:
- 環境別のデプロイ
- サブスクリプションレベルのデプロイ
- デプロイスタックの管理
- CI/CDパイプラインとの統合

**環境別デプロイ例**:
```bash
# 開発環境
az deployment group create \
  --resource-group rg-myapp-dev \
  --template-file main.bicep \
  --parameters parameters.dev.json

# 本番環境
az deployment group create \
  --resource-group rg-myapp-prod \
  --template-file main.bicep \
  --parameters parameters.prod.json
```

**サブスクリプションレベルのデプロイ**:
```bicep
// subscription.bicep
targetScope = 'subscription'

@description('リソースグループ名')
param rgName string

@description('ロケーション')
param location string

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: rgName
  location: location
}

module vnetModule './modules/vnet.bicep' = {
  scope: rg
  name: 'vnetDeployment'
  params: {
    vnetName: 'my-vnet'
    location: location
  }
}
```

```bash
# サブスクリプションレベルでデプロイ
az deployment sub create \
  --location japaneast \
  --template-file subscription.bicep
```

**ディレクトリ構造例**:
```
bicep/
├── modules/
│   ├── vnet.bicep
│   ├── vm.bicep
│   └── database.bicep
├── environments/
│   ├── dev/
│   │   ├── main.bicep
│   │   └── parameters.json
│   ├── staging/
│   └── prod/
└── main.bicep
```

---

### 10. テスト（インフラ）での活用

**目的**: Bicepコードの品質保証とインフラの検証

**活用方法**:
- `az bicep build`: 構文チェック
- `az deployment what-if`: 変更内容の確認
- ARM Template Test Toolkit (arm-ttk)
- Pesterによる自動テスト

**テストコマンド例**:
```bash
# 構文チェック
az bicep build --file main.bicep

# Linter実行（Bicep設定で有効化）
# bicepconfig.json で設定

# What-Ifデプロイ
az deployment group what-if \
  --resource-group myResourceGroup \
  --template-file main.bicep

# ARM TTK によるテスト
Test-AzTemplate -TemplatePath ./main.bicep

# Pesterによるテスト
Invoke-Pester -Path ./tests/
```

**bicepconfig.json（Linter設定）**:
```json
{
  "analyzers": {
    "core": {
      "enabled": true,
      "verbose": true,
      "rules": {
        "no-unused-params": {
          "level": "warning"
        },
        "no-hardcoded-env-urls": {
          "level": "error"
        }
      }
    }
  }
}
```

---

### 11. 導入での活用

**目的**: 本番環境への安全なデプロイ

**活用方法**:
- Azure Pipelinesとの統合
- GitHub Actionsとの統合
- デプロイゲートの実装
- ロールバック手順の準備

**Azure Pipelines統合例**:
```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: AzureCLI@2
    displayName: 'Bicep Build'
    inputs:
      azureSubscription: 'MyAzureSubscription'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az bicep build --file main.bicep

  - task: AzureCLI@2
    displayName: 'What-If Deployment'
    inputs:
      azureSubscription: 'MyAzureSubscription'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        az deployment group what-if \
          --resource-group $(resourceGroup) \
          --template-file main.bicep \
          --parameters parameters.prod.json

  - task: AzureResourceManagerTemplateDeployment@3
    displayName: 'Deploy Bicep'
    inputs:
      deploymentScope: 'Resource Group'
      azureResourceManagerConnection: 'MyAzureSubscription'
      subscriptionId: '$(subscriptionId)'
      action: 'Create Or Update Resource Group'
      resourceGroupName: '$(resourceGroup)'
      location: 'Japan East'
      templateLocation: 'Linked artifact'
      csmFile: 'main.bicep'
      csmParametersFile: 'parameters.prod.json'
      deploymentMode: 'Incremental'
```

**GitHub Actions統合例**:
```yaml
# .github/workflows/deploy.yml
name: Deploy Bicep

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy Bicep
        uses: azure/arm-deploy@v1
        with:
          subscriptionId: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          resourceGroupName: myResourceGroup
          template: ./main.bicep
          parameters: ./parameters.prod.json
```

## 公式ドキュメント

- [Azure Bicep 公式サイト](https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/bicep/)
- [Bicep ドキュメント](https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/bicep/overview)
- [Bicep GitHub Repository](https://github.com/Azure/bicep)
- [Bicep Playground](https://aka.ms/bicepdemo) - ブラウザ上でBicepを試せる
- [Bicep リファレンス](https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/bicep/bicep-functions)
- [VS Code Bicep Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)

## 学習リソース

### チュートリアル
- [Bicep Quickstart](https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/bicep/quickstart-create-bicep-use-visual-studio-code)
- [Microsoft Learn - Bicep Learning Path](https://learn.microsoft.com/ja-jp/training/paths/bicep-deploy/)
- [Bicep Modules](https://github.com/Azure/bicep-registry-modules)

### 書籍・コース
- Microsoft Learn - Deploy and manage resources in Azure by using Bicep
- Pluralsight - Getting Started with Azure Bicep
- LinkedIn Learning - Azure Bicep Essential Training

### 動画
- [John Savill's Technical Training - Bicep](https://www.youtube.com/watch?v=_yvb6NVx61Y)
- [Microsoft Azure - Bicep Tutorial](https://www.youtube.com/results?search_query=azure+bicep+tutorial)

### コミュニティ
- [Bicep GitHub Discussions](https://github.com/Azure/bicep/discussions)
- [Azure Bicep Community](https://techcommunity.microsoft.com/t5/azure/ct-p/Azure)
- [Stack Overflow - Azure Bicep](https://stackoverflow.com/questions/tagged/azure-bicep)

## 関連リンク

### 関連ツール
- [ARM Template Test Toolkit (arm-ttk)](https://github.com/Azure/arm-ttk) - ARMテンプレート/Bicepのテストツール
- [Bicep Linter](https://learn.microsoft.com/azure/azure-resource-manager/bicep/linter) - Bicep組み込みリンター
- [Pester](https://pester.dev/) - PowerShellテストフレームワーク（Bicepテストに活用）
- [Checkov](https://www.checkov.io/) - IaCセキュリティスキャナー（Bicep対応）
- [Azure Resource Manager (ARM)](https://learn.microsoft.com/azure/azure-resource-manager/management/overview) - Bicepの基盤技術

### Bicepモジュールライブラリ
- [Bicep Registry](https://github.com/Azure/bicep-registry-modules) - 公式モジュールレジストリ
- [Common Azure Resource Modules Library (CARML)](https://github.com/Azure/ResourceModules) - 再利用可能なBicepモジュール集
- [Bicep Community Modules](https://github.com/topics/bicep-modules)

### ベストプラクティス
- [Bicep Best Practices](https://learn.microsoft.com/azure/azure-resource-manager/bicep/best-practices)
- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/architecture/framework/)
- [ARM Template Best Practices](https://learn.microsoft.com/azure/azure-resource-manager/templates/best-practices)

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0

