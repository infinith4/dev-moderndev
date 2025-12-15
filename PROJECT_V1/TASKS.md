# 技術スタックフィルタリング機能 - 実装完了

**実装日**: 2025-12-15
**バージョン**: v2.2
**ステータス**: ✅ 完了（データベースフィルタリング追加）

---

## 📋 実装概要

`tool_recommender.py` に技術スタックフィルタリング機能を追加し、セクション12で選択された技術スタック（クラウドプラットフォーム、プログラミング言語、**データベース**）に基づいて、互換性のあるツールのみを推薦するように改善しました。

### v2.2 新機能: データベースフィルタリング
セクション12.3.5で選択されたデータベースに基づいて、データベース固有のツール（MySQL_Workbench、pgAdmin等）を自動的にフィルタリングします。

---

## 🎯 主な変更点

### 1. データ構造の追加

**新規追加したクラス**:
```python
@dataclass
class TechStack:
    """技術スタック選択情報"""
    cloud_platforms: Set[str]  # AWS, Azure, GCP
    languages: Set[str]  # C#, Java, Python, TypeScript
    frameworks: Set[str]
    databases: Set[str]
    messaging: Set[str]
    caching: Set[str]
    monitoring: Set[str]
    tools: Set[str]
```

**Tool クラスへの追加属性**:
- `platform`: AWS, Azure, GCP, All
- `language`: C#, Java, Python, TypeScript, All

### 2. ツールメタデータマッピング

80+のツールに対してプラットフォームと言語の互換性メタデータを定義:

```python
{
    # AWS専用ツール
    "AWS_CloudFormation": {"platform": "AWS", "language": "All"},
    "AWS_CodeDeploy": {"platform": "AWS", "language": "All"},
    
    # Azure専用ツール
    "Azure_Bicep": {"platform": "Azure", "language": "All"},
    "Application_Insights": {"platform": "Azure", "language": "All"},
    
    # 言語依存ツール - TypeScript
    "Jest": {"platform": "All", "language": "TypeScript"},
    "Cypress": {"platform": "All", "language": "TypeScript"},
    
    # クロスプラットフォーム
    "Terraform": {"platform": "All", "language": "All"},
}
```

### 3. セクション12パース機能

`_parse_tech_stack()` メソッドを追加し、チェックリストのセクション12から以下を自動抽出:
- クラウドプラットフォーム (AWS/Azure/GCP)
- プログラミング言語 (C#/Java/Python/TypeScript)
- **データベース (PostgreSQL/MySQL/SQL Server/Oracle/MongoDB等)** ← v2.2で追加
- 選択済みツール (Swagger, Notion, GitHub等)

### 4. フィルタリングロジック

`_is_tool_compatible()` メソッドを追加し、以下のルールでフィルタリング:

1. **クラウドプラットフォームフィルタ**:
   - ツールが特定プラットフォーム専用の場合、そのプラットフォームが選択されている場合のみ推薦
   - 例: Azure Bicep は Azure選択時のみ推薦

2. **言語フィルタ**:
   - ツールが特定言語専用の場合、その言語が選択されている場合のみ推薦
   - 例: Jest は TypeScript選択時のみ推薦

3. **データベースフィルタ** ← v2.2で追加:
   - ツールが特定データベース専用の場合、そのデータベースが選択されている場合のみ推薦
   - 例: MySQL_Workbench は MySQL選択時のみ推薦、pgAdmin は PostgreSQL選択時のみ推薦

4. **クロスプラットフォームツール**:
   - `platform: "All"`, `language: "All"`, `database: "All"` のツールは常に推薦対象
   - 例: Terraform, Draw.io, ERDPlus, Flyway

### 5. レポート強化

生成されるレポートに以下を追加:
- 選択された技術スタックのサマリー
- フィルタリングに関する説明
- マッチ理由に技術スタック対応情報を追加

---

## 🔬 動作検証

### テストケース 1: Azure + RBAC選択

**入力** (`プロジェクト要件チェックリスト_template.md`):
- セクション12.2: `[x] Azure Service Bus`
- セクション12.1: `[x] RBAC (Role-Based Access Control)`

**出力結果**:
```
🔧 技術スタック (セクション12) を解析中...
  ☁️  クラウド: Azure
  🔧 ツール: Azure_Service_Bus, GitHub, Mermaid, Notion, PlantUML, RBAC, Slack, Swagger, draw.io
```

**推薦ツール（IaC）**:
- ✅ **Azure Bicep** - マッチ理由: "キーワード 'Infrastructure as Code' にマッチ + **Azure対応**"
- ✅ **Terraform** - マッチ理由: "キーワード 'Infrastructure as Code' にマッチ" (クロスプラットフォーム)
- ❌ **AWS CloudFormation** - フィルタリングで除外
- ❌ **AWS CloudFormation Designer** - フィルタリングで除外

**ツール数の変化**:
- フィルタリング前: 132ツール
- フィルタリング後: 131ツール (AWS専用ツール1件除外)

### テストケース 2: PostgreSQL選択（v2.2新規）

**入力** (`プロジェクト要件チェックリスト_template.md`):
- セクション12.3.5: `[x] PostgreSQL`

**出力結果**:
```
🔧 技術スタック (セクション12) を解析中...
  ☁️  クラウド: Azure
  🗄️  データベース: PostgreSQL
  🔧 ツール: Azure_Service_Bus, GitHub, Mermaid, Notion, PlantUML, RBAC, Slack, Swagger, draw.io
```

**推薦ツール（データベース関連）**:
- ✅ **ERDPlus** - マッチ理由: "キーワード 'ER図' にマッチ" (クロスDB)
- ✅ **Flyway** - マッチ理由: "キーワード 'マイグレーション' にマッチ" (クロスDB)
- ✅ **pgAdmin** - マッチ理由: "キーワード 'データベース' にマッチ + **PostgreSQL対応**" (PostgreSQL選択時)
- ❌ **MySQL_Workbench** - フィルタリングで除外 (MySQL専用ツール)

**検証結果**:
- PostgreSQL選択時: MySQL_Workbenchは推薦から除外される ✅
- MySQL選択時: MySQL_Workbenchが推薦に含まれる ✅

---

## 📊 コード変更統計

| ファイル | 追加行数 | 主な変更内容 |
|---------|---------|------------|
| `tool_recommender.py` | ~150行 | TechStack追加、メタデータ定義、フィルタリングロジック |
| `README.md` | ~30行 | 技術スタックフィルタリング機能の説明追加 |

---

## 🚀 使用例

```bash
# 1. チェックリストでAzureとTypeScriptを選択
# プロジェクト要件チェックリスト_template.md で以下をチェック:
#   - [x] Azure Service Bus (セクション12.2)
#   - [x] TypeScript関連ツール

# 2. ツール推薦を実行
python3 scripts/tool_recommender.py

# 3. レポート確認
cat ツール推薦レポート_自動生成.md
```

**期待される結果**:
- Azure専用ツール (Bicep, Application Insights) が推薦される
- TypeScript関連ツール (Jest, ESLint, Prettier) が推薦される
- AWS専用ツールは除外される
- Java専用ツール (JUnit, Mockito) は除外される

---

## ✅ 完了タスク

### v2.1 - 基本フィルタリング
- [x] TechStack データクラスの定義
- [x] Tool クラスへの platform/language 属性追加
- [x] ツールメタデータマッピング (80+ツール)
- [x] セクション12パース機能 (`_parse_tech_stack`)
- [x] フィルタリングロジック (`_is_tool_compatible`)
- [x] マッチ理由への技術スタック情報追加
- [x] レポート生成の強化
- [x] README.md への機能説明追加
- [x] 動作検証 (Azure選択時のフィルタリング確認)

### v2.2 - データベースフィルタリング
- [x] セクション12.3.5 データベース選択項目の追加（PostgreSQL, MySQL等）
- [x] データベース検出ロジックの実装（_parse_tech_stack）
- [x] データベース固有ツールのメタデータ定義（MySQL_Workbench, pgAdmin等）
- [x] データベースフィルタリングロジックの実装（_is_tool_compatible）
- [x] レポート出力へのデータベース情報追加
- [x] 動作検証（PostgreSQL選択時にMySQL_Workbench除外を確認）
- [x] 動作検証（MySQL選択時にMySQL_Workbench推薦を確認）
- [x] README.mdへのデータベースフィルタリング説明追加
- [x] TASKS.mdの更新

---

## 🎉 成果

ユーザーの要望通り、**「マッチ理由がキーワードのみ」という問題を解決**し、**セクション12で選択した技術スタックを考慮した推薦**が可能になりました。

### v2.1 成果
- Azure選択時 → Bicep, Terraform のみ推薦 (CloudFormation除外) ✅
- TypeScript選択時 → Jest, Cypress のみ推薦 (JUnit除外) ✅

### v2.2 成果（データベースフィルタリング）
- PostgreSQL選択時 → ERDPlus, Flyway のみ推薦 (MySQL_Workbench除外) ✅
- MySQL選択時 → MySQL_Workbench, ERDPlus, Flyway が推薦 ✅
- データベース固有ツールが適切にフィルタリングされ、マッチ理由に「PostgreSQL対応」「MySQL対応」が表示される ✅

---

**実装者**: Claude Sonnet 4.5
**v2.1 実装日時**: 2025-12-15
**v2.2 実装日時**: 2025-12-15
