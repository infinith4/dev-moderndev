# ARM Templates

## 概要

ARM Templates（Azure Resource Manager Templates）は、Microsoft Azure公式のInfrastructure as Code（IaC）ソリューションです。JSON形式でAzureリソース（VM、Storage、ネットワーク等）を宣言的に定義し、一貫性のあるデプロイを実現します。バージョン管理、テンプレート再利用、パラメータ化により、インフラのコード管理、CI/CD統合、エンタープライズガバナンスを支援します。

## 主な機能

### 1. 宣言的構文
- **JSON形式**: Azure リソース定義
- **リソース**: VM、VNet、Storage、App Service等
- **依存関係**: dependsOn自動管理
- **出力**: デプロイ結果取得

### 2. パラメータ化
- **パラメータ**: デプロイ時入力
- **変数**: テンプレート内再利用
- **関数**: concat、uniqueString等
- **条件分岐**: if条件

### 3. モジュール化
- **Linked Templates**: 外部テンプレート参照
- **Nested Templates**: ネストテンプレート
- **Template Specs**: テンプレート共有
- **Bicep**: ARMの高レベル言語

### 4. デプロイモード
- **Incremental**: 増分デプロイ（既存保持）
- **Complete**: 完全デプロイ（既存削除）
- **What-if**: デプロイ前検証
- **Rollback**: 前回成功デプロイへロールバック

### 5. ガバナンス
- **Azure Policy**: ポリシー適用
- **RBAC**: ロールベースアクセス
- **Tags**: リソースタグ
- **Locks**: リソースロック

### 6. 統合
- **Azure DevOps**: CI/CDパイプライン
- **GitHub Actions**: GitHub統合
- **Azure CLI**: コマンドライン
- **PowerShell**: PowerShell Az モジュール

## 利用方法

### 基本テンプレート

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "storageAccountName": {
      "type": "string",
      "metadata": {
        "description": "Storage Account Name"
      }
    }
  },
  "variables": {
    "location": "[resourceGroup().location]"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-04-01",
      "name": "[parameters('storageAccountName')]",
      "location": "[variables('location')]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2"
    }
  ],
  "outputs": {
    "storageAccountId": {
      "type": "string",
      "value": "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageAccountName'))]"
    }
  }
}
```

### 仮想マシンテンプレート

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "vmName": {
      "type": "string"
    },
    "adminUsername": {
      "type": "string"
    },
    "adminPassword": {
      "type": "securestring"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Compute/virtualMachines",
      "apiVersion": "2021-03-01",
      "name": "[parameters('vmName')]",
      "location": "[resourceGroup().location]",
      "properties": {
        "hardwareProfile": {
          "vmSize": "Standard_B2s"
        },
        "osProfile": {
          "computerName": "[parameters('vmName')]",
          "adminUsername": "[parameters('adminUsername')]",
          "adminPassword": "[parameters('adminPassword')]"
        },
        "storageProfile": {
          "imageReference": {
            "publisher": "Canonical",
            "offer": "UbuntuServer",
            "sku": "18.04-LTS",
            "version": "latest"
          }
        }
      }
    }
  ]
}
```

### パラメータファイル

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "vmName": {
      "value": "myVM"
    },
    "adminUsername": {
      "value": "azureuser"
    },
    "adminPassword": {
      "reference": {
        "keyVault": {
          "id": "/subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.KeyVault/vaults/{vault-name}"
        },
        "secretName": "vmPassword"
      }
    }
  }
}
```

### デプロイ（Azure CLI）

```bash
# リソースグループ作成
az group create \
  --name myResourceGroup \
  --location eastus

# テンプレートデプロイ
az deployment group create \
  --resource-group myResourceGroup \
  --template-file azuredeploy.json \
  --parameters azuredeploy.parameters.json

# What-if検証
az deployment group what-if \
  --resource-group myResourceGroup \
  --template-file azuredeploy.json \
  --parameters azuredeploy.parameters.json

# デプロイ状態確認
az deployment group show \
  --resource-group myResourceGroup \
  --name azuredeploy
```

### デプロイ（PowerShell）

```powershell
# リソースグループ作成
New-AzResourceGroup `
  -Name myResourceGroup `
  -Location eastus

# テンプレートデプロイ
New-AzResourceGroupDeployment `
  -ResourceGroupName myResourceGroup `
  -TemplateFile .\azuredeploy.json `
  -TemplateParameterFile .\azuredeploy.parameters.json

# What-if検証
New-AzResourceGroupDeployment `
  -ResourceGroupName myResourceGroup `
  -TemplateFile .\azuredeploy.json `
  -WhatIf
```

### Linked Templates

```json
{
  "resources": [
    {
      "type": "Microsoft.Resources/deployments",
      "apiVersion": "2021-04-01",
      "name": "linkedTemplate",
      "properties": {
        "mode": "Incremental",
        "templateLink": {
          "uri": "https://mystorageaccount.blob.core.windows.net/templates/storage.json"
        },
        "parameters": {
          "storageAccountName": {
            "value": "[parameters('storageAccountName')]"
          }
        }
      }
    }
  ]
}
```

### Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: AzureResourceManagerTemplateDeployment@3
    inputs:
      deploymentScope: 'Resource Group'
      azureResourceManagerConnection: 'Azure-Subscription'
      subscriptionId: '$(subscriptionId)'
      resourceGroupName: 'myResourceGroup'
      location: 'East US'
      templateLocation: 'Linked artifact'
      csmFile: 'azuredeploy.json'
      csmParametersFile: 'azuredeploy.parameters.json'
      deploymentMode: 'Incremental'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **ARM Templates** | 🟢 完全無料 | Azure標準機能 |
| **Template Specs** | 🟢 無料 | テンプレート共有 |

## メリット

### ✅ 主な利点

1. **完全無料**: Azure標準機能
2. **宣言的**: JSON宣言的構文
3. **Azure公式**: Microsoft公式IaC
4. **バージョン管理**: Git管理
5. **再利用**: パラメータ化、モジュール化
6. **What-if**: デプロイ前検証
7. **ロールバック**: 前回成功デプロイへ復帰
8. **CI/CD統合**: Azure DevOps、GitHub Actions
9. **依存関係**: 自動依存解決
10. **エンタープライズ**: Azure Policy、RBAC統合

## デメリット

### ❌ 制約・課題

1. **JSON冗長**: JSON記述が冗長
2. **学習曲線**: 関数、構文習得必要
3. **Azure専用**: Azureのみ対応
4. **エラーメッセージ**: わかりにくい
5. **ループ**: copy構文が複雑
6. **テスト**: テスト環境が限定的
7. **ドキュメント**: 一部不十分
8. **IDE**: JSON編集サポート限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Bicep** | ARM高レベル言語 | ARM TemplatesよりシンプルだがAzure専用 |
| **Terraform** | マルチクラウドIaC | ARM Templatesよりマルチクラウド |
| **Pulumi** | プログラマブルIaC | ARM Templatesより高レベル |
| **Azure CLI** | コマンドラインツール | ARM Templatesより手続き的 |
| **PowerShell Az** | PowerShellモジュール | ARM Templatesと併用 |

## 公式リンク

- **公式ドキュメント**: [https://docs.microsoft.com/azure/azure-resource-manager/templates/](https://docs.microsoft.com/azure/azure-resource-manager/templates/)
- **テンプレートリファレンス**: [https://docs.microsoft.com/azure/templates/](https://docs.microsoft.com/azure/templates/)
- **クイックスタート**: [https://github.com/Azure/azure-quickstart-templates](https://github.com/Azure/azure-quickstart-templates)
- **Bicep**: [https://docs.microsoft.com/azure/azure-resource-manager/bicep/](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)

## 関連ドキュメント

- [IaCツール一覧](../IaCツール/)
- [Bicep](./Bicep.md)
- [Terraform](./Terraform.md)
- [Azure CLI](../CLIツール/Azure_CLI.md)
- [Azure DevOps Pipelines](../CI_CDツール/Azure_DevOps_Pipelines.md)

---

**カテゴリ**: IaCツール  
**対象工程**: インフラ構築  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
