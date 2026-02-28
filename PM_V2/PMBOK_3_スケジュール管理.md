# PMBOK_3_スケジュール管理

- [1. 概要](#1-概要)
  - [1.1. 共通](#11-共通)
- [2. スケジュールマネジメント計画](#2-スケジュールマネジメント計画)
- [3. アクティビティの定義](#3-アクティビティの定義)
- [4. アクティビティの順序設定](#4-アクティビティの順序設定)
- [5. アクティビティの所要期間見積り](#5-アクティビティの所要期間見積り)
- [6. スケジュールの作成](#6-スケジュールの作成)
- [7. スケジュールのコントロール](#7-スケジュールのコントロール)
- [8. 参考資料](#8-参考資料)

## 1. 概要

スケジュール管理は、プロジェクトの工程を計画し、期限内の完了を確保する領域である。

---

### 1.1. 共通

**対応項目**
- アクティビティ一覧の作成と依存関係の定義
- クリティカルパス分析
- スケジュールベースラインの設定と進捗管理
- アジャイル環境でのイテレーション計画

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [PMBOK Guide 第7版](https://www.pmi.org/pmbok-guide-standards/foundational/pmbok) | スケジュール管理プロセス全般 |
| [IPA ソフトウェア開発見積りガイドブック](https://www.ipa.go.jp/archive/publish/secbooks20060425.html) | 工数・期間見積り手法 |

---

## 2. スケジュールマネジメント計画

**成果物**
- スケジュールマネジメント計画書

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Notion](https://www.notion.so/) | 計画書テンプレート・スケジュール方針記述 | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Notion.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf) | 工程定義の基準 |

---

## 3. アクティビティの定義

**成果物**
- アクティビティリスト
- マイルストーンリスト

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Jira](https://www.atlassian.com/software/jira) | タスク分解・エピック/ストーリー管理 | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Jira.md) |
| [Backlog](https://backlog.com/) | タスク・マイルストーン定義 | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Backlog.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf) | アクティビティの粒度基準 |

---

## 4. アクティビティの順序設定

**成果物**
- プロジェクトスケジュールネットワーク図

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Microsoft Project](https://www.microsoft.com/microsoft-365/project) | 依存関係設定・ネットワーク図 | - |
| [Draw.io](https://www.diagrams.net/) | PERT図・ネットワーク図の作成 | [詳細](../docs/ツール/設計_モデリング/Draw.io.md) |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [PMBOK Guide 第7版](https://www.pmi.org/pmbok-guide-standards/foundational/pmbok) | PDM（プレシデンスダイアグラム法） |

---

## 5. アクティビティの所要期間見積り

**成果物**
- 所要期間見積り
- 見積り根拠

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) | 三点見積り・PERT分析計算 | - |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [IPA ソフトウェア開発見積りガイドブック](https://www.ipa.go.jp/archive/publish/secbooks20060425.html) | 見積り手法（類推、FP、COCOMO等） |
| [IPA ソフトウェア開発分析データ集](https://www.ipa.go.jp/digital/chousa/metrics/index.html) | 業界ベンチマーク、生産性データ |

---

## 6. スケジュールの作成

**成果物**
- プロジェクトスケジュール（ガントチャート）
- スケジュールベースライン

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Microsoft Project](https://www.microsoft.com/microsoft-365/project) | ガントチャート・クリティカルパス分析・リソース平準化 | - |
| [Backlog](https://backlog.com/) | ガントチャート・マイルストーン管理 | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Backlog.md) |
| [Jira](https://www.atlassian.com/software/jira) | スプリント計画・バーンダウンチャート | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Jira.md) |
| [Mermaid](https://mermaid.js.org/) | ガントチャートをコードベースで定義 | - |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [IPA アジャイル開発版モデル取引・契約書](https://www.ipa.go.jp/digital/model/model20200331.html) | アジャイル環境のスケジュール管理方針 |

---

## 7. スケジュールのコントロール

**成果物**
- 作業パフォーマンス情報
- スケジュール予測
- 変更要求

| ツール名 | 用途 | 詳細 |
|---------|------|------|
| [Jira](https://www.atlassian.com/software/jira) | バーンダウン/バーンアップチャート・ベロシティ | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Jira.md) |
| [Backlog](https://backlog.com/) | ガントチャート進捗追跡 | [詳細](../docs/ツール/プロジェクト管理_ドキュメント/Backlog.md) |
| [Microsoft Excel](https://www.microsoft.com/microsoft-365/excel) | EVM分析（SV、SPI） | - |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [PMBOK Guide 第7版](https://www.pmi.org/pmbok-guide-standards/foundational/pmbok) | EVM、進捗管理手法 |

---

## 8. 参考資料

- [PMBOK Guide 第7版](https://www.pmi.org/pmbok-guide-standards/foundational/pmbok)
- [IPA ソフトウェア開発見積りガイドブック](https://www.ipa.go.jp/archive/publish/secbooks20060425.html)
- [IPA ソフトウェア開発分析データ集](https://www.ipa.go.jp/digital/chousa/metrics/index.html)
- [IPA 共通フレーム2013](https://www.ipa.go.jp/archive/files/000027415.pdf)
