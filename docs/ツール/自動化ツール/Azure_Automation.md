# Azure Automation

## 概要

Azure Automationは、Microsoft Azure公式のクラウドベース自動化・構成管理サービスです。Runbook（PowerShell、Python）でクラウド・オンプレミス環境のタスクを自動化し、更新プログラム管理、構成管理（DSC）、プロセスオーケストレーションを提供します。スケジュール実行、Webhook、イベント駆動で業務プロセスを効率化し、Azure Monitor、Azure Logic Appsと統合します。

## 主な機能

### 1. Runbook自動化
- **PowerShell Runbook**: Windows自動化
- **Python Runbook**: Linux、クロスプラットフォーム
- **Graphical Runbook**: GUIワークフロー
- **PowerShell Workflow**: 並列実行、チェックポイント

### 2. 更新プログラム管理
- **Update Management**: Windows、Linux パッチ管理
- **スケジュール**: 定期パッチ適用
- **コンプライアンスレポート**: パッチ状況確認
- **ハイブリッド対応**: Azure、オンプレミス、他クラウド

### 3. 構成管理（DSC）
- **Desired State Configuration**: 構成ドリフト検出
- **ノード管理**: サーバー構成一元管理
- **構成コンパイル**: MOFファイル生成
- **レポート**: 構成状態レポート

### 4. スケジュール・トリガー
- **スケジュール実行**: 時刻ベース
- **Webhook**: HTTP POST トリガー
- **Azure Alert**: アラート連携
- **Logic Apps**: ワークフロー統合

### 5. 資格情報・変数管理
- **資格情報**: 暗号化保存
- **変数**: グローバル変数
- **証明書**: SSL/TLS証明書
- **接続**: Azure、AWS、GCP接続情報

### 6. ハイブリッドWorker
- **Hybrid Runbook Worker**: オンプレミス実行
- **Hybrid Worker Group**: グループ管理
- **ネットワークアクセス**: オンプレミスリソース接続

## 利用方法

### Automationアカウント作成

```bash
# Azure CLI
az automation account create \
  --resource-group myResourceGroup \
  --name myAutomationAccount \
  --location eastus
```

### PowerShell Runbook作成

```powershell
# PowerShell Runbook例: VM自動起動
Param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$VMName
)

# Azure接続（Managed Identity使用）
Connect-AzAccount -Identity

# VM起動
Write-Output "Starting VM: $VMName"
Start-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName

# 状態確認
$vm = Get-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName -Status
Write-Output "VM Status: $($vm.Statuses[1].DisplayStatus)"
```

### Python Runbook作成

```python
# Python Runbook例: ストレージBlobクリーンアップ
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta

# 環境変数から接続情報取得
storage_account_name = os.environ.get("STORAGE_ACCOUNT")
container_name = os.environ.get("CONTAINER_NAME")

# 認証
credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)

# 30日以前のBlob削除
container_client = blob_service_client.get_container_client(container_name)
cutoff_date = datetime.now() - timedelta(days=30)

for blob in container_client.list_blobs():
    if blob.last_modified < cutoff_date:
        print(f"Deleting blob: {blob.name}")
        container_client.delete_blob(blob.name)
```

### 更新プログラム管理

```bash
# Update Managementソリューション有効化
az vm extension set \
  --resource-group myResourceGroup \
  --vm-name myVM \
  --name MicrosoftMonitoringAgent \
  --publisher Microsoft.EnterpriseCloud.Monitoring
```

### DSC構成

```powershell
# DSC構成例: IISインストール
Configuration IISInstall {
    Node "WebServer" {
        WindowsFeature IIS {
            Ensure = "Present"
            Name = "Web-Server"
        }
        
        WindowsFeature ASP {
            Ensure = "Present"
            Name = "Web-Asp-Net45"
        }
    }
}
```

### Webhook統合

```bash
# Webhook呼び出し（curl）
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"ResourceGroupName": "myRG", "VMName": "myVM"}' \
  https://s1events.azure-automation.net/webhooks?token=XXXX
```

### スケジュール設定

```powershell
# PowerShellでスケジュール作成
$automationAccount = "myAutomationAccount"
$resourceGroup = "myResourceGroup"

# 毎日午前2時に実行
New-AzAutomationSchedule `
  -Name "DailyBackup" `
  -ResourceGroupName $resourceGroup `
  -AutomationAccountName $automationAccount `
  -StartTime "2024-01-01T02:00:00" `
  -DayInterval 1

# RunbookとSchedule紐付け
Register-AzAutomationScheduledRunbook `
  -Name "BackupRunbook" `
  -ScheduleName "DailyBackup" `
  -ResourceGroupName $resourceGroup `
  -AutomationAccountName $automationAccount
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Process Automation** | 💰 $0.002/分 | Runbook実行時間課金 |
| **Update Management** | 🟢 無料 | Azure VM無料、非AzureはLog Analytics課金 |
| **State Configuration (DSC)** | 💰 $6/ノード/月 | ノード数課金 |
| **無料枠** | 🟢 500分/月 | Runbook実行時間無料枠 |

## メリット

### ✅ 主な利点

1. **完全マネージド**: サーバーレス自動化
2. **ハイブリッド**: Azure、オンプレミス、他クラウド
3. **PowerShell/Python**: 豊富なエコシステム
4. **更新プログラム管理**: パッチ自動化
5. **DSC統合**: 構成管理
6. **Azure統合**: Logic Apps、Monitor連携
7. **Managed Identity**: 安全な認証
8. **スケジュール**: 柔軟な実行タイミング
9. **Webhook**: イベント駆動
10. **監査ログ**: 実行履歴追跡

## デメリット

### ❌ 制約・課題

1. **Azure中心**: Azure環境での利用が前提
2. **コスト**: 実行時間課金で高額化リスク
3. **学習曲線**: PowerShell、Python習得必要
4. **デバッグ**: ローカルデバッグ困難
5. **実行時間制限**: 3時間制限（Hybrid Worker除く）
6. **ログ遅延**: 実行ログ反映に遅延
7. **バージョン管理**: Runbookバージョン管理が弱い
8. **エラーハンドリング**: 複雑なエラー処理が難しい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **AWS Systems Manager Automation** | AWS自動化 | Azure Automationと類似 |
| **Ansible** | オープンソースIaC | Azure Automationよりマルチクラウド |
| **Jenkins** | CI/CD自動化 | Azure Automationより開発特化 |
| **Azure Logic Apps** | ローコード自動化 | Azure Automationよりビジュアル |
| **Terraform** | IaC | Azure Automationより宣言的 |

## 公式リンク

- **公式サイト**: [https://azure.microsoft.com/services/automation/](https://azure.microsoft.com/services/automation/)
- **ドキュメント**: [https://docs.microsoft.com/azure/automation/](https://docs.microsoft.com/azure/automation/)
- **料金**: [https://azure.microsoft.com/pricing/details/automation/](https://azure.microsoft.com/pricing/details/automation/)
- **PowerShell Gallery**: [https://www.powershellgallery.com/](https://www.powershellgallery.com/)

## 関連ドキュメント

- [自動化ツール一覧](../自動化ツール/)
- [Azure CLI](../CLIツール/Azure_CLI.md)
- [Ansible](../IaCツール/Ansible.md)
- [Azure自動化ベストプラクティス](../../best-practices/azure-automation.md)

---

**カテゴリ**: 自動化ツール  
**対象工程**: 運用、インフラ構築  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
