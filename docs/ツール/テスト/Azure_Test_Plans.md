# Azure Test Plans

## 概要

Azure Test Plansは、Microsoft Azure DevOps内のテスト管理サービスです。手動テスト、探索的テスト、ユーザー受け入れテストを計画・実行・追跡し、Azure Boards（課題管理）、Azure Pipelines（CI/CD）とシームレスに統合します。テストケース、テスト計画、テスト結果を一元管理し、品質保証プロセスを効率化します。

## 主な機能

### 1. テスト計画
- **Test Plans**: プロジェクト全体のテスト戦略
- **Test Suites**: 機能単位のテストグループ
- **Test Cases**: 詳細なテストケース
- **テストステップ**: 手順・期待結果

### 2. 手動テスト実行
- **Test Runner**: Web、デスクトップアプリ
- **スクリーンショット**: テスト実行中のキャプチャ
- **ビデオ録画**: 操作記録
- **データ収集**: ログ、システム情報

### 3. 探索的テスト
- **Exploratory Testing**: アドホックテスト
- **セッション管理**: テストセッション記録
- **バグ報告**: テスト中にバグ作成
- **Chrome拡張**: ブラウザから実行

### 4. テスト構成
- **Configurations**: OS、ブラウザ、デバイス
- **パラメータ化**: データ駆動テスト
- **共有ステップ**: 再利用可能なステップ

### 5. レポート・分析
- **Test Progress**: テスト進捗
- **Test Results**: 合格/不合格
- **トレーサビリティ**: 要件⇔テスト
- **ダッシュボード**: カスタムダッシュボード

### 6. 統合
- **Azure Boards**: Work Itemリンク
- **Azure Pipelines**: 自動テスト連携
- **Selenium**: 自動化テスト
- **API**: RESTful API

## 利用方法

### テスト計画作成

```
1. Azure DevOps → Test Plans
2. New Test Plan
3. 基本情報:
   - Name: Release 1.0 Test Plan
   - Area Path: MyProject\Web
   - Iteration: Sprint 10

4. Test Suites追加:
   - Suite 1: Login Module
   - Suite 2: User Management
   - Suite 3: Payment Module
```

### テストケース作成

```
1. Test Suite選択 → New Test Case
2. テストケース情報:
   - Title: TC-001: User Login with valid credentials
   - Assigned To: QA Engineer
   - Priority: 1
   - State: Design

3. Steps:
   Step 1:
   - Action: Navigate to login page
   - Expected Result: Login page is displayed
   
   Step 2:
   - Action: Enter username "testuser" and password "Test@123"
   - Expected Result: Credentials are entered
   
   Step 3:
   - Action: Click "Login" button
   - Expected Result: User is redirected to dashboard

4. Save & Close
```

### テスト実行

```
1. Test Suite選択 → Run → Run with options
2. Test Runner起動
3. テスト実行:
   - 各ステップを実行
   - Pass / Fail / Blocked を選択
   - スクリーンショット添付（必要に応じて）
   - コメント追加

4. バグ作成（Failの場合）:
   - Create bug
   - バグ詳細入力
   - スクリーンショット自動添付

5. テスト完了 → Save & Close
```

### 探索的テスト

```
1. Chrome拡張インストール:
   Test & Feedback

2. セッション開始:
   - Start session
   - Work Item: US-101 (User Story)
   - Duration: 30 minutes

3. アプリケーション操作:
   - 自由にアプリ探索
   - バグ発見時: Create bug
   - スクリーンショット、画面録画自動記録

4. セッション終了:
   - End session
   - セッションサマリー保存
```

### テスト構成

```
1. Test Configuration作成:
   - Configuration 1: Windows 10 + Chrome
   - Configuration 2: Windows 10 + Edge
   - Configuration 3: macOS + Safari

2. Test Caseに構成割り当て:
   - TC-001を3つの構成で実行

3. 構成ごとに結果記録
```

### パラメータ化テスト

```
1. Test Case編集 → Parameters
2. パラメータ追加:
   - @username
   - @password
   - @expectedResult

3. Steps更新:
   Step 2: Enter username "@username" and password "@password"
   Step 3: @expectedResult

4. Iteration Data:
   | username  | password  | expectedResult       |
   |-----------|-----------|----------------------|
   | testuser1 | Pass@123  | Login successful     |
   | testuser2 | Pass@456  | Login successful     |
   | invalid   | wrong     | Invalid credentials  |
```

### API統合

```python
# Python API例
import requests

ORGANIZATION = "your-org"
PROJECT = "your-project"
PAT = "YOUR_PERSONAL_ACCESS_TOKEN"

url = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/test/runs?api-version=7.0"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {PAT}"
}

# テスト実行作成
test_run = {
    "name": "Automated Test Run",
    "plan": {"id": "12345"},
    "automated": True
}

response = requests.post(url, headers=headers, json=test_run)
print(response.json())
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** | 🟢 無料 | Basic Plan、ステークホルダー向け |
| **Basic** | 🟢 無料 | 基本機能、コード・作業追跡 |
| **Basic + Test Plans** | 💰 $52/ユーザー/月 | テスト計画・実行、探索的テスト |

## メリット

### ✅ 主な利点

1. **Azure DevOps統合**: Boards、Pipelines連携
2. **手動テスト**: Test Runner
3. **探索的テスト**: Chrome拡張
4. **トレーサビリティ**: 要件⇔テスト⇔バグ
5. **テスト構成**: クロスブラウザ、デバイステスト
6. **スクリーンショット**: 自動キャプチャ
7. **レポート**: 進捗、結果ダッシュボード
8. **API**: RESTful API
9. **エンタープライズ**: AAD、RBAC統合
10. **セキュリティ**: Azure セキュリティ

## デメリット

### ❌ 制約・課題

1. **高価**: $52/ユーザー/月
2. **Azure DevOps依存**: Azure DevOps組織必須
3. **自動化機能**: 自動テスト実行は別途Pipeline必要
4. **UI複雑**: 初心者には難しい
5. **Test Runner**: デスクトップ版がレガシー
6. **モバイルテスト**: モバイルアプリテストは制限的
7. **オフライン**: オフライン実行不可
8. **競合**: TestRailより機能少ない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **TestRail** | 専用テスト管理 | Azure Test Plansより高機能 |
| **Xray for Jira** | Jira統合テスト管理 | Azure Test Plansと類似 |
| **qTest** | エンタープライズテスト管理 | Azure Test Plansより高機能 |
| **Zephyr for Jira** | Jira統合 | Azure Test Plansと類似 |
| **PractiTest** | クラウドテスト管理 | Azure Test Plansと類似 |

## 公式リンク

- **公式サイト**: [https://azure.microsoft.com/services/devops/test-plans/](https://azure.microsoft.com/services/devops/test-plans/)
- **ドキュメント**: [https://docs.microsoft.com/azure/devops/test/](https://docs.microsoft.com/azure/devops/test/)
- **料金**: [https://azure.microsoft.com/pricing/details/devops/azure-devops-services/](https://azure.microsoft.com/pricing/details/devops/azure-devops-services/)
- **API**: [https://docs.microsoft.com/rest/api/azure/devops/test/](https://docs.microsoft.com/rest/api/azure/devops/test/)

## 関連ドキュメント

- [テスト管理ツール一覧](../テスト管理ツール/)
- [Zephyr for Jira](./Zephyr_for_Jira.md)
- [Azure DevOps Pipelines](../CI_CDツール/Azure_DevOps_Pipelines.md)
- [テスト管理ベストプラクティス](../../best-practices/test-management.md)

---

**カテゴリ**: テスト管理ツール  
**対象工程**: テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
