# Azure CLI

## 概要

Azure CLI（Command-Line Interface）は、Microsoft Azure公式のコマンドラインツールです。ブラウザのAzure Portalを使わず、ターミナルからAzureリソース（VM、Storage、App Service等）を作成・管理・削除できます。クロスプラットフォーム（Windows、macOS、Linux）対応で、シェルスクリプト、CI/CDパイプライン、自動化タスクに統合し、Infrastructure as Codeを実現します。

## 主な機能

### 1. リソース管理
- **VM**: 仮想マシン作成・管理
- **Storage**: Blob、File、Queue
- **App Service**: Webアプリデプロイ
- **AKS**: Kubernetesクラスター管理
- **Database**: SQL Database、Cosmos DB

### 2. スクリプト対応
- **Bash**: シェルスクリプト
- **PowerShell**: PowerShellスクリプト
- **Python**: Azure SDK連携
- **JSON出力**: jqでパース

### 3. 認証
- **Azure AD**: ユーザー認証
- **Service Principal**: 自動化用
- **Managed Identity**: VM内認証
- **Cloud Shell**: ブラウザ内CLI

### 4. 対話モード
- **Interactive mode**: 自動補完
- **コマンドヘルプ**: --help
- **エラーメッセージ**: 詳細エラー表示

## 利用方法

### インストール

```bash
# Windows (MSI)
# https://aka.ms/installazurecliwindows からダウンロード

# macOS (Homebrew)
brew update && brew install azure-cli

# Linux (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Docker
docker run -it mcr.microsoft.com/azure-cli

# バージョン確認
az --version
```

### ログイン

```bash
# ブラウザ認証
az login

# Service Principal
az login --service-principal \
  --username <app-id> \
  --password <password> \
  --tenant <tenant-id>

# サブスクリプション選択
az account set --subscription "My Subscription"

# 現在のアカウント確認
az account show
```

### リソースグループ

```bash
# 作成
az group create \
  --name myResourceGroup \
  --location eastus

# 一覧
az group list --output table

# 削除
az group delete --name myResourceGroup --yes --no-wait
```

### 仮想マシン

```bash
# VM作成
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys

# VM一覧
az vm list --output table

# VM起動・停止
az vm start --resource-group myResourceGroup --name myVM
az vm stop --resource-group myResourceGroup --name myVM

# VM削除
az vm delete --resource-group myResourceGroup --name myVM --yes
```

### App Service

```bash
# App Service Plan作成
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux

# Web App作成
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name myUniqueAppName \
  --runtime "NODE:18-lts"

# デプロイ
az webapp deployment source config \
  --name myUniqueAppName \
  --resource-group myResourceGroup \
  --repo-url https://github.com/user/repo \
  --branch main \
  --manual-integration

# ログストリーミング
az webapp log tail --name myUniqueAppName --resource-group myResourceGroup
```

### ストレージ

```bash
# Storage Account作成
az storage account create \
  --name mystorageaccount \
  --resource-group myResourceGroup \
  --location eastus \
  --sku Standard_LRS

# Blob Container作成
az storage container create \
  --account-name mystorageaccount \
  --name mycontainer

# ファイルアップロード
az storage blob upload \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myblob.txt \
  --file ./local-file.txt
```

### AKS (Kubernetes)

```bash
# AKSクラスター作成
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --enable-managed-identity \
  --generate-ssh-keys

# kubectl認証情報取得
az aks get-credentials \
  --resource-group myResourceGroup \
  --name myAKSCluster

# ノードプール追加
az aks nodepool add \
  --resource-group myResourceGroup \
  --cluster-name myAKSCluster \
  --name mynodepool \
  --node-count 2
```

### JSON出力とjq

```bash
# JSON形式で出力
az vm list --output json

# jqでフィルタ
az vm list --output json | jq '.[].name'

# 特定フィールド抽出
az vm show \
  --resource-group myResourceGroup \
  --name myVM \
  --query "provisioningState" \
  --output tsv
```

### スクリプト例

```bash
#!/bin/bash
# VM一括作成スクリプト

RESOURCE_GROUP="myResourceGroup"
LOCATION="eastus"

# リソースグループ作成
az group create --name $RESOURCE_GROUP --location $LOCATION

# VM 3台作成
for i in {1..3}; do
  az vm create \
    --resource-group $RESOURCE_GROUP \
    --name "myVM$i" \
    --image Ubuntu2204 \
    --size Standard_B2s \
    --admin-username azureuser \
    --generate-ssh-keys \
    --no-wait
done

echo "VM creation initiated"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Azure CLI** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **完全無料**: オープンソース、MIT License
2. **クロスプラットフォーム**: Windows、macOS、Linux
3. **公式ツール**: Microsoft公式サポート
4. **スクリプト対応**: 自動化・CI/CD統合
5. **JSON出力**: jq等でパース可能
6. **対話モード**: 自動補完
7. **Cloud Shell**: ブラウザから利用
8. **包括的**: 全Azureサービス対応
9. **活発な開発**: 継続的な改善
10. **ドキュメント充実**: 豊富な公式ドキュメント

## デメリット

### ❌ 制約・課題

1. **Azure専用**: Azureのみ対応
2. **学習曲線**: コマンド多数
3. **バージョン**: 頻繁な更新で互換性注意
4. **エラーメッセージ**: わかりにくい場合あり
5. **パフォーマンス**: 大量リソース操作で遅延
6. **GUI不在**: GUIツールではない
7. **認証**: 初期設定が煩雑
8. **ドキュメント**: 一部古い情報あり

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Azure PowerShell** | PowerShellモジュール | Azure CLIと類似、PowerShell向け |
| **Terraform** | IaC、マルチクラウド | Azure CLIよりインフラ管理特化 |
| **Pulumi** | プログラマブルIaC | Azure CLIより高レベル |
| **Azure Portal** | WebベースGUI | Azure CLIよりビジュアル |
| **ARM Templates** | 宣言的IaC | Azure CLIより宣言的 |

## 公式リンク

- **公式サイト**: [https://docs.microsoft.com/cli/azure/](https://docs.microsoft.com/cli/azure/)
- **インストール**: [https://docs.microsoft.com/cli/azure/install-azure-cli](https://docs.microsoft.com/cli/azure/install-azure-cli)
- **GitHub**: [https://github.com/Azure/azure-cli](https://github.com/Azure/azure-cli)
- **リファレンス**: [https://docs.microsoft.com/cli/azure/reference-index](https://docs.microsoft.com/cli/azure/reference-index)

## 関連ドキュメント

- [CLIツール一覧](../CLIツール/)
- [AWS CLI](./AWS_CLI.md)
- [Azure DevOps Pipelines](../CI_CDツール/Azure_DevOps_Pipelines.md)
- [Terraform](../IaCツール/Terraform.md)
- [Azure自動化ベストプラクティス](../../best-practices/azure-automation.md)

---

**カテゴリ**: CLIツール  
**対象工程**: インフラ構築、運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
