# Jama Connect

## 概要

Jama Connectは、複雑な製品開発における要件管理・トレーサビリティプラットフォームです。システム要件、ソフトウェア要件、テストケースを一元管理し、要件から設計、実装、テストまでの双方向トレーサビリティを実現します。医療機器、自動車、航空宇宙等の規制産業で広く採用され、ISO 26262、IEC 62304、DO-178C等のコンプライアンスを支援します。

## 主な機能

### 1. 要件管理
- **階層構造**: システム要件 → サブシステム要件 → コンポーネント要件
- **カスタムフィールド**: 優先度、リスク、検証方法
- **ベースライン**: 要件のスナップショット
- **バージョン管理**: 変更履歴追跡

### 2. トレーサビリティ
- **関係管理**: 要件間、要件⇔テストケース、要件⇔リスク
- **トレーサビリティマトリクス**: カバレッジ分析
- **影響分析**: 変更影響範囲の特定
- **双方向リンク**: 上流⇔下流の追跡

### 3. レビュー・承認
- **フォーマルレビュー**: 承認ワークフロー
- **コメント**: レビューコメント
- **電子署名**: 21 CFR Part 11準拠
- **監査ログ**: 全変更履歴

### 4. 変更管理
- **変更リクエスト**: 要件変更管理
- **影響分析**: 自動影響範囲計算
- **承認フロー**: 多段階承認
- **通知**: 関係者への自動通知

### 5. コラボレーション
- **リアルタイム編集**: 同時編集
- **コメント**: ディスカッション
- **@メンション**: ユーザー通知
- **ダッシュボード**: プロジェクト概要

### 6. 統合
- **Jira**: 開発チケット連携
- **ALM tools**: qTest、TestRail等
- **Git**: コード連携
- **API**: RESTful API

## 利用方法

### 要件作成

```
1. Project → Create Item → Requirement
2. 基本情報入力:
   - ID: REQ-001
   - Name: User Authentication
   - Description: The system shall authenticate users via email and password
   - Priority: High
   - Status: Draft

3. カスタムフィールド:
   - Risk Level: Medium
   - Verification Method: Test
   - Assigned To: Development Team
```

### 階層構造

```
System Requirements
├── REQ-001: User Management
│   ├── REQ-001-01: User Registration
│   ├── REQ-001-02: User Login
│   └── REQ-001-03: Password Reset
├── REQ-002: Data Management
│   ├── REQ-002-01: Data Storage
│   └── REQ-002-02: Data Encryption
```

### トレーサビリティリンク

```
1. 要件選択: REQ-001-02 (User Login)
2. Create Relationship → "is verified by" → Test Case
3. テストケース選択: TC-101 (Login Success Test)
4. リンク作成

結果:
REQ-001-02 ⇔ TC-101
└─ Coverage: 100%
```

### レビュー設定

```
1. 要件選択 → Create Review
2. レビュー設定:
   - Review Name: Authentication Requirements Review
   - Reviewers: Architect, Security Lead, QA Lead
   - Due Date: 2024-01-15
   - Approval Type: Unanimous

3. レビュー実行:
   - Reviewers: コメント追加、Approve/Reject
   - Author: コメント対応、要件更新
   - Moderator: レビュー完了判定
```

### トレーサビリティマトリクス

```
1. Reports → Traceability Matrix
2. 設定:
   - Source: System Requirements
   - Target: Test Cases
   - Relationship Type: "is verified by"

3. レポート生成:
   
   Requirements | Test Cases | Coverage
   -------------|------------|----------
   REQ-001      | TC-101     | 100%
   REQ-002      | TC-102     | 100%
   REQ-003      | -          | 0% ⚠️
```

### ベースライン作成

```
1. Project → Baselines → Create Baseline
2. 設定:
   - Name: Release 1.0 Baseline
   - Description: Requirements for Release 1.0
   - Include: All approved requirements

3. ベースライン比較:
   - Compare Baseline 1.0 vs Current
   - 変更内容表示: Added, Modified, Deleted
```

### API統合

```python
# Python API例
import requests

API_URL = "https://your-instance.jamacloud.com/rest/v1"
API_TOKEN = "YOUR_API_TOKEN"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# 要件取得
response = requests.get(
    f"{API_URL}/items/REQ-001",
    headers=headers
)
requirement = response.json()

# 要件作成
new_req = {
    "project": 12345,
    "itemType": 10,
    "fields": {
        "name": "New Security Requirement",
        "description": "The system shall encrypt all data at rest"
    }
}
response = requests.post(
    f"{API_URL}/items",
    headers=headers,
    json=new_req
)
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Standard** | 💰 要問い合わせ | 基本要件管理、トレーサビリティ |
| **Professional** | 💰 要問い合わせ | レビュー、ベースライン、API |
| **Enterprise** | 💰 要問い合わせ | 高度な統合、専用サポート、SSO |

## メリット

### ✅ 主な利点

1. **トレーサビリティ**: 要件⇔テスト完全追跡
2. **規制対応**: ISO 26262、IEC 62304準拠
3. **変更管理**: 影響分析、承認フロー
4. **レビュー**: フォーマルレビュー対応
5. **ベースライン**: 要件凍結・比較
6. **電子署名**: 21 CFR Part 11対応
7. **監査ログ**: 全変更履歴
8. **統合**: Jira、ALM tools連携
9. **カスタマイズ**: 業界特化カスタマイズ
10. **エンタープライズ**: 大規模プロジェクト対応

## デメリット

### ❌ 制約・課題

1. **高価**: エンタープライズ向け価格
2. **学習曲線**: 習得に時間がかかる
3. **複雑性**: 小規模プロジェクトには過剰
4. **UI**: モダンなUIではない
5. **パフォーマンス**: 大規模データで遅延
6. **オンプレミス**: クラウド推奨だがオンプレ高価
7. **ライセンス**: 同時ユーザー数制限
8. **カスタマイズコスト**: 高度なカスタマイズは高額

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Polarion** | ALM、要件管理 | Jama Connectと類似 |
| **DOORS (IBM)** | エンタープライズ要件管理 | Jama Connectより高機能だが複雑 |
| **Helix RM (Perforce)** | 要件管理 | Jama Connectと類似 |
| **Jira + Confluence** | アジャイル開発 | Jama Connectよりシンプル |
| **Azure DevOps** | DevOps統合 | Jama Connectより開発特化 |

## 公式リンク

- **公式サイト**: [https://www.jamasoftware.com/](https://www.jamasoftware.com/)
- **ドキュメント**: [https://help.jamasoftware.com/](https://help.jamasoftware.com/)
- **コミュニティ**: [https://community.jamasoftware.com/](https://community.jamasoftware.com/)
- **API**: [https://dev.jamasoftware.com/](https://dev.jamasoftware.com/)

## 関連ドキュメント

- [要件管理ツール一覧](../要件管理ツール/)
- [JIRA](../プロジェクト管理ツール/JIRA.md)
- [Azure DevOps](../CI_CDツール/Azure_DevOps_Pipelines.md)
- [要件管理ベストプラクティス](../../best-practices/requirements-management.md)

---

**カテゴリ**: 要件管理ツール  
**対象工程**: 要件定義、設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
