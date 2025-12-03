# Azure Resource Graph

## 概要

Azure Resource Graphは、Microsoft Azure公式の大規模リソースクエリサービスです。KQL（Kusto Query Language）でAzureリソースをサブスクリプション横断で高速検索・分析し、リソース管理、コスト最適化、コンプライアンス監査を支援します。Azure Portal、Azure CLI、PowerShell、REST APIから利用でき、Azure Policy、Azure Monitorと統合します。

## 主な機能

### 1. 大規模クエリ
- **スケール**: 数千サブスクリプション対応
- **高速**: 数秒で大量リソース検索
- **複雑クエリ**: join、集計、フィルタリング
- **ページネーション**: 大量結果の分割取得

### 2. KQL構文
- **Kusto Query Language**: Azure Data Explorer構文
- **演算子**: where、project、summarize、join
- **関数**: count、max、min、avg
- **正規表現**: regex検索

### 3. リソースタイプ
- **全Azureリソース**: VM、Storage、ネットワーク等
- **リソースグループ**: 組織単位
- **タグ**: リソースタグ検索
- **プロパティ**: 詳細プロパティ

### 4. 統合
- **Azure Portal**: Resource Graph Explorer
- **Azure CLI**: az graph query
- **PowerShell**: Search-AzGraph
- **REST API**: RESTful API
- **Azure Policy**: ポリシー評価

## 利用方法

### 基本クエリ

```kusto
// すべてのリソース一覧
Resources

// 仮想マシンのみ
Resources
| where type == "microsoft.compute/virtualmachines"

// 特定リージョンのVM
Resources
| where type == "microsoft.compute/virtualmachines"
| where location == "eastus"
| project name, location, resourceGroup
```

### タグ検索

```kusto
// 環境タグが "production" のリソース
Resources
| where tags.Environment == "production"
| project name, type, resourceGroup, tags

// タグがないリソース
Resources
| where isnull(tags) or array_length(todynamic(tags)) == 0
| project name, type, resourceGroup
```

### 集計クエリ

```kusto
// リソースタイプ別カウント
Resources
| summarize count() by type
| order by count_ desc

// リージョン別VMサイズ集計
Resources
| where type == "microsoft.compute/virtualmachines"
| extend vmSize = properties.hardwareProfile.vmSize
| summarize count() by location, tostring(vmSize)
| order by location, count_ desc
```

### Azure CLI実行

```bash
# 基本クエリ
az graph query -q "Resources | where type == 'microsoft.compute/virtualmachines' | count"

# 複数サブスクリプション
az graph query \
  -q "Resources | summarize count() by subscriptionId" \
  --subscriptions sub1 sub2 sub3

# 結果をJSON出力
az graph query \
  -q "Resources | where type == 'microsoft.compute/virtualmachines' | project name, location" \
  --output json
```

### PowerShell実行

```powershell
# PowerShellでクエリ
Search-AzGraph -Query "Resources | where type == 'microsoft.compute/virtualmachines' | count"

# 複数サブスクリプション
$subscriptions = @("sub1", "sub2", "sub3")
Search-AzGraph -Query "Resources | summarize count() by resourceGroup" -Subscription $subscriptions

# ページネーション
$query = "Resources"
$result = Search-AzGraph -Query $query -First 1000
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Azure Resource Graph** | 🟢 完全無料 | Azure標準機能 |

## メリット

### ✅ 主な利点

1. **完全無料**: Azure標準機能
2. **高速**: 大規模クエリを数秒で実行
3. **スケーラブル**: 数千サブスクリプション対応
4. **KQL**: 強力なクエリ言語
5. **サブスクリプション横断**: 複数サブスクリプション一括検索
6. **リアルタイム**: 最新リソース状態
7. **統合**: Portal、CLI、PowerShell、API
8. **コンプライアンス**: ポリシー評価支援
9. **コスト分析**: リソース使用状況分析
10. **監査**: リソース変更追跡

## デメリット

### ❌ 制約・課題

1. **Azure専用**: Azureのみ対応
2. **学習曲線**: KQL習得必要
3. **制限**: 1クエリ15秒、5000件制限
4. **遅延**: リソース作成後数秒遅延
5. **一部プロパティ**: すべてのプロパティが取得できない
6. **履歴**: 過去データ保持期間限定
7. **複雑クエリ**: 高度なjoinは難しい
8. **ドキュメント**: KQL例が少ない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Azure CLI** | コマンドラインツール | Resource Graphよりスクリプト的 |
| **PowerShell Az** | PowerShellモジュール | Resource Graphよりスクリプト的 |
| **Azure Cost Management** | コスト分析 | Resource Graphよりコスト特化 |
| **Azure Monitor** | 監視 | Resource Graphよりメトリクス特化 |

## 公式リンク

- **公式ドキュメント**: [https://docs.microsoft.com/azure/governance/resource-graph/](https://docs.microsoft.com/azure/governance/resource-graph/)
- **KQLリファレンス**: [https://docs.microsoft.com/azure/data-explorer/kusto/query/](https://docs.microsoft.com/azure/data-explorer/kusto/query/)
- **REST API**: [https://docs.microsoft.com/rest/api/azureresourcegraph/](https://docs.microsoft.com/rest/api/azureresourcegraph/)

## 関連ドキュメント

- [クエリツール一覧](../クエリツール/)
- [Azure CLI](../CLIツール/Azure_CLI.md)
- [Azure Monitor](../監視ツール/Azure_Monitor.md)

---

**カテゴリ**: クエリツール  
**対象工程**: 運用、監査  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
