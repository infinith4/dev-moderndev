# Atlassian Portfolio (Jira Align)

## 概要

**Atlassian Portfolio**（現在は**Jira Align**として提供）は、エンタープライズレベルのアジャイルポートフォリオ管理ツールです。複数チーム・複数プロジェクトの計画、追跡、依存関係管理を統合的に行い、戦略的目標と開発作業を結びつけます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Atlassian |
| **種別** | アジャイルポートフォリオ管理・プログラム管理ツール |
| **ライセンス** | プロプライエタリ |
| **料金** | 🔴 有料（Jira Align: $39/ユーザー/月〜、Premium: $89/ユーザー/月） |
| **公式サイト** | https://www.atlassian.com/software/jira/align |
| **ドキュメント** | https://support.atlassian.com/jira-align/ |

## 主な特徴

### 1. マルチレベルプランニング
- **ポートフォリオレベル**: 戦略的イニシアティブ
- **プログラムレベル**: エピック・フィーチャー
- **チームレベル**: ストーリー・タスク
- PI（Program Increment）プランニング

### 2. リアルタイム可視化
- ロードマップビュー
- 依存関係マッピング
- キャパシティプランニング
- リスク管理

### 3. SAFe（Scaled Agile Framework）対応
- SAFeフレームワーク準拠
- ART（Agile Release Train）管理
- PI目標設定・追跡
- Value Stream管理

### 4. Jira統合
- Jira Software/Jira Coreとシームレス連携
- 双方向同期
- 自動ロールアップ

## 使い方

### セットアップ

```bash
# Jira Alignへのアクセス
# https://your-org.jiraalign.com

# Jira連携設定
# Settings → Integrations → Jira Software
# 認証情報入力・同期設定
```

### ポートフォリオ階層の設定

```text
戦略レベル:
  └── テーマ (Theme)
        └── イニシアティブ (Initiative)
              └── エピック (Epic)
                    └── フィーチャー (Feature)
                          └── ストーリー (Story)
                                └── タスク (Task)
```

#### テーマの作成（GUI操作）

1. **Themes** セクション → **Create Theme**
2. 設定項目:
   - Name: "デジタル変革"
   - Description: "顧客体験のデジタル化"
   - Strategic Driver: "市場拡大"
   - Timeline: 2025年度
   - Budget: ¥100,000,000

#### イニシアティブの作成

1. **Initiatives** → **Create Initiative**
2. 設定項目:
   - Name: "モバイルアプリ開発"
   - Theme: "デジタル変革"
   - Owner: プロダクトマネージャー
   - Value Stream: カスタマーエクスペリエンス
   - Target Start: 2025-01-01
   - Target End: 2025-06-30

### PI（Program Increment）プランニング

```text
# PI Planning設定
PI 2025.Q1
├── Duration: 12 weeks
├── Start: 2025-01-06
├── End: 2025-03-28
├── Iterations:
│   ├── Sprint 1 (2025-01-06 〜 2025-01-19)
│   ├── Sprint 2 (2025-01-20 〜 2025-02-02)
│   ├── Sprint 3 (2025-02-03 〜 2025-02-16)
│   ├── Sprint 4 (2025-02-17 〜 2025-03-02)
│   ├── Sprint 5 (2025-03-03 〜 2025-03-16)
│   └── Sprint 6 (Innovation & Planning)
└── PI Objectives:
    ├── モバイルアプリβ版リリース
    ├── ユーザー認証機能実装
    └── 決済システム統合
```

### ロードマップの作成

```text
# ロードマップビュー（タイムライン形式）

2025 Q1         Q2          Q3          Q4
─────────────────────────────────────────────
モバイルアプリ   [======開発======][テスト][リリース]
              ↓
Web刷新         [計画][======開発============]
                    ↓
APIマイグレ      [設計][======実装======]
                              ↓
インフラ強化              [計画][======実装======]
```

### 依存関係管理

```text
# Dependency Board

Epic A: ユーザー認証
  ├── Depends on: API設計完了
  └── Blocks: 決済機能開発

Epic B: 決済機能
  ├── Depends on: ユーザー認証完了
  └── Blocks: 注文履歴機能

Epic C: 注文履歴
  └── Depends on: 決済機能完了

# 依存関係アラート
⚠️ Epic A遅延中 → Epic B、Epic Cに影響
```

### キャパシティプランニング

```yaml
# Team Capacity設定
Team: モバイル開発チーム
  - Total Capacity: 80 story points/sprint
  - Available Members: 8人
  - Velocity (平均): 75 points/sprint
  - Planned Work: 78 points (98% キャパシティ)
  - Status: ⚠️ ほぼ満杯

Team: バックエンドチーム
  - Total Capacity: 60 story points/sprint
  - Available Members: 6人
  - Velocity (平均): 55 points/sprint
  - Planned Work: 45 points (75% キャパシティ)
  - Status: ✅ 余裕あり
```

### リスク管理

```text
# Risk Register

Risk ID: R-001
  - Title: サードパーティAPIの仕様変更
  - Impact: High
  - Probability: Medium
  - Mitigation: 代替API調査、影響範囲分析
  - Owner: テックリード
  - Status: Monitoring

Risk ID: R-002
  - Title: キーメンバーの離脱
  - Impact: High
  - Probability: Low
  - Mitigation: ナレッジ共有、クロストレーニング
  - Owner: エンジニアリングマネージャー
  - Status: Open
```

### レポーティング

```text
# Portfolio Health Report

全体進捗: 68% 完了
  ├── On Track: 12イニシアティブ (60%)
  ├── At Risk: 5イニシアティブ (25%)
  └── Off Track: 3イニシアティブ (15%)

予算使用率: 45% / ¥45M使用

リソース稼働率:
  ├── 開発: 92%
  ├── QA: 78%
  └── DevOps: 85%

主要リスク: 3件（High）
```

### Jira連携の設定

```yaml
# Jira Sync設定

Sync Rules:
  - Jira Epic → Jira Align Feature
    Mapping:
      - Summary → Name
      - Description → Description
      - Story Points → Points
      - Status → State

  - Jira Story → Jira Align Story
    Mapping:
      - Summary → Title
      - Assignee → Owner
      - Sprint → Iteration

Sync Frequency: Every 15 minutes
Auto-create: Enabled
Bi-directional: Enabled
```

### APIでの操作

```python
# jira_align_api.py
import requests

BASE_URL = "https://your-org.jiraalign.com/api/v1"
API_TOKEN = "your_api_token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# イニシアティブ作成
def create_initiative(name, description, theme_id):
    url = f"{BASE_URL}/initiatives"
    payload = {
        "name": name,
        "description": description,
        "themeId": theme_id,
        "targetStartDate": "2025-01-01",
        "targetEndDate": "2025-06-30"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# ポートフォリオ進捗取得
def get_portfolio_progress():
    url = f"{BASE_URL}/reports/portfolio-health"
    response = requests.get(url, headers=headers)
    return response.json()

# PI情報取得
def get_pi_objectives(pi_id):
    url = f"{BASE_URL}/program-increments/{pi_id}/objectives"
    response = requests.get(url, headers=headers)
    return response.json()
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **企画** | ポートフォリオ計画 | 戦略的イニシアティブ管理 |
| **要件定義** | エピック・フィーチャー管理 | 複数チーム間の調整 |
| **実装** | PIプランニング | スプリント計画・依存関係管理 |
| **全工程** | 進捗追跡 | リアルタイムダッシュボード |

## メリット

- **エンタープライズスケール**: 複数チーム・プロジェクトの統合管理
- **SAFe準拠**: Scaled Agile Framework対応
- **リアルタイム可視化**: ポートフォリオ全体の健全性をリアルタイム把握
- **Jira統合**: Jira Softwareとシームレス連携
- **依存関係管理**: チーム間依存関係の可視化・管理
- **リソース最適化**: キャパシティプランニング
- **リスク管理**: 統合的なリスク追跡

## デメリット

- **高コスト**: $39〜$89/ユーザー/月、大規模組織向け
- **複雑性**: 小規模チームにはオーバースペック
- **学習曲線**: SAFe、Jira Alignの習得が必要
- **Atlassian依存**: Jiraエコシステムへのロックイン
- **カスタマイズ制限**: オンプレミス版なし、SaaS版のみ

## 類似ツールとの比較

| ツール | 料金 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **Jira Align** | $39〜/月 | SAFe準拠、Jira統合 | エンタープライズアジャイル |
| **Azure DevOps** | $6〜/月 | Microsoft統合、柔軟 | Microsoftエコシステム |
| **Rally (Broadcom)** | 要問合せ | アジャイル管理特化 | 大規模アジャイル |
| **Monday.com** | $8〜/月 | 汎用PM、視覚的 | 中小規模プロジェクト |

## ベストプラクティス

### 1. 段階的導入

```text
Phase 1: パイロットチーム（1-2チーム）
  - 基本機能習得
  - Jira連携設定
  - フィードバック収集

Phase 2: 部門展開（5-10チーム）
  - ポートフォリオ階層確立
  - PI Planning開始
  - ロードマップ共有

Phase 3: 全社展開
  - 全チーム統合
  - エグゼクティブダッシュボード
  - 継続的改善
```

### 2. 役割の明確化

```text
Portfolio Manager:
  - テーマ・イニシアティブ管理
  - 予算配分
  - リスク管理

Product Owner:
  - エピック・フィーチャー優先順位付け
  - バックログ管理

Scrum Master / RTE:
  - PI Planning進行
  - 依存関係解消
  - チーム間調整
```

### 3. 定期的なレビュー

```text
Daily: チーム内スタンドアップ
Weekly: ポートフォリオステータスレビュー
Bi-weekly: リスク・依存関係レビュー
Quarterly: PI Planning & Retrospective
```

### 4. メトリクスの活用

```text
追跡すべきKPI:
  - Velocity Trend
  - PI達成率
  - リードタイム
  - リスク発生率
  - 予算消化率
```

## 公式リソース

- **公式サイト**: https://www.atlassian.com/software/jira/align
- **ドキュメント**: https://support.atlassian.com/jira-align/
- **SAFe Guide**: https://www.scaledagileframework.com/
- **コミュニティ**: https://community.atlassian.com/

## まとめ

Jira Align（旧Atlassian Portfolio）は、エンタープライズレベルのアジャイルポートフォリオ管理ツールです。SAFe準拠、Jira統合、リアルタイム可視化により、複数チーム・プロジェクトの戦略的管理を実現します。高コストですが、大規模組織のアジャイル変革には強力なツールです。

---

**最終更新**: 2025-12-06
**対象バージョン**: Jira Align 2024+
