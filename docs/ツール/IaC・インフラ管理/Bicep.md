# Bicep

## 概要

Bicepは、Microsoft Azure公式のDomain Specific Language（DSL）で、ARM Templates（JSON）の高レベル抽象化言語です。簡潔な宣言的構文でAzureリソース（VM、Storage、ネットワーク等）を定義し、ARM Templatesにトランスパイルしてデプロイします。モジュール化、型安全、IntelliSense、リンターにより、Infrastructure as Code（IaC）の開発体験を向上させ、Azure DevOps、GitHub Actions、VS Code統合で効率的なインフラ管理を実現します。

## 主な機能

### 1. 簡潔な構文
- **宣言的**: リソース定義
- **型安全**: 型チェック
- **シンプル**: JSON比30-50%削減
- **可読性**: 人間が読みやすい

### 2. モジュール化
- **モジュール**: 再利用可能なテンプレート
- **パラメータ**: 動的入力
- **出力**: 値の受け渡し
- **スコープ**: リソースグループ、サブスクリプション、管理グループ

### 3. ツールサポート
- **VS Code拡張**: IntelliSense、補完、エラー検出
- **Bicep CLI**: コマンドライン
- **リンター**: ベストプラクティス警告
- **デコンパイル**: ARM→Bicep変換

### 4. Azure統合
- **Azure CLI**: az deployment group create
- **PowerShell**: New-AzResourceGroupDeployment
- **Azure DevOps**: Bicepタスク
- **GitHub Actions**: Azure/arm-deploy

### 5. 検証
- **What-if**: デプロイ前検証
- **バリデーション**: テンプレート検証
- **ドライラン**: 変更プレビュー

## 利用方法

### インストール

```bash
# Azure CLI（Bicep自動インストール）
az bicep install

# Bicepバージョン確認
az bicep version
```

### 基本例（ストレージアカウント）

```bicep
param storageAccountName string
param location string = resourceGroup().location

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

output storageAccountId string = storageAccount.id
```

### デプロイ

```bash
# リソースグループ作成
az group create --name myResourceGroup --location eastus

# Bicepデプロイ
az deployment group create \
  --resource-group myResourceGroup \
  --template-file storage.bicep \
  --parameters storageAccountName=mystorageacct123
```

### モジュール

```bicep
// main.bicep
param environment string = 'dev'
param location string = resourceGroup().location

module storage './modules/storage.bicep' = {
  name: 'storageDeployment'
  params: {
    storageAccountName: 'mystorage${environment}'
    location: location
  }
}

output storageId string = storage.outputs.storageAccountId
```

### 条件分岐・ループ

```bicep
// 条件デプロイ
param deployStorage bool = true

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = if (deployStorage) {
  name: 'mystorage'
  location: resourceGroup().location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

// ループ
param storageCount int = 3

resource storageAccounts 'Microsoft.Storage/storageAccounts@2021-04-01' = [for i in range(0, storageCount): {
  name: 'mystorage${i}'
  location: resourceGroup().location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}]
```

### GitHub Actions

```yaml
name: Deploy Bicep

on:
  push:
    branches: [main]

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
          parameters: environment=prod
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Bicep** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **完全無料**: オープンソース
2. **シンプル**: JSON比30-50%削減
3. **型安全**: IntelliSense、型チェック
4. **Azure公式**: Microsoft公式サポート
5. **モジュール**: 再利用可能
6. **リンター**: ベストプラクティス警告
7. **デコンパイル**: ARM→Bicep変換
8. **What-if**: デプロイ前検証
9. **VS Code統合**: 快適な開発体験
10. **ARM互換**: 100%ARM Templates互換

## デメリット

### ❌ 制約・課題

1. **Azure専用**: Azureのみ対応
2. **学習曲線**: 新しい構文習得必要
3. **成熟度**: Terraformより新しい
4. **エコシステム**: Terraformよりモジュール少ない
5. **複雑な式**: 複雑なロジックは記述困難
6. **デバッグ**: エラーメッセージが不明確な場合あり
7. **マルチクラウド**: マルチクラウド不可
8. **テスト**: テストツール限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **ARM Templates** | AzureネイティブJSON | Bicepより冗長だがAzure専用 |
| **Terraform** | マルチクラウドIaC | Bicepよりマルチクラウド |
| **Pulumi** | プログラマブルIaC | Bicepより高レベル |
| **Azure CLI** | コマンドラインツール | Bicepより手続き的 |

## 公式リンク

- **公式サイト**: [https://docs.microsoft.com/azure/azure-resource-manager/bicep/](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- **GitHub**: [https://github.com/Azure/bicep](https://github.com/Azure/bicep)
- **VS Code拡張**: [https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)

## 関連ドキュメント

- [IaCツール一覧](../IaCツール/)
- [ARM Templates](./ARM_Templates.md)
- [Terraform](./Terraform.md)
- [Azure CLI](../CLIツール/Azure_CLI.md)

---

**カテゴリ**: IaCツール  
**対象工程**: インフラ構築  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
