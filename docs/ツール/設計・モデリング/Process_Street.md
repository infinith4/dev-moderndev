# Process Street

## 概要

Process Streetは、プロセス管理・ワークフロー自動化ツールで、業務プロセスの標準化、チェックリスト管理、SOP（Standard Operating Procedures：標準作業手順書）管理に特化しています。従来のBPMNツールとは異なり、プロセスの「実行」と「管理」に重点を置いたツールです。

### 主な特徴

- **プロセス実行管理**: 作成したプロセスを実際に実行し、進捗を追跡
- **チェックリスト機能**: タスクごとにチェックリストを作成し、完了状況を管理
- **条件分岐対応**: If/Then条件により、動的なワークフロー作成が可能
- **データ収集**: フォームフィールドでデータを収集し、プロセス内で活用
- **API統合**: Zapier、Slack、Google Workspace等との連携

### 料金プラン

- **Free版**: 基本機能（制限あり、最大5ワークフロー）
- **Pro**: $25/月/ユーザー（無制限ワークフロー、高度な機能）
- **Enterprise**: カスタム価格（大企業向け、専用サポート）

### メリット・デメリット

**メリット**
- プロセスの「実行」と「管理」が一体化されており、実際の業務運用に直結
- チェックリスト機能により、タスクの抜け漏れを防止
- 条件分岐対応により、柔軟なワークフロー設計が可能
- フォームフィールドでデータ収集し、プロセス内で活用可能
- Zapier等のAPI統合により、他システムとの連携が容易

**デメリット**
- 複雑なBPMN図の作成には不向き（図表作成機能が弱い）
- 有料版がやや高額
- 日本語の情報やコミュニティが少ない
- 図表としてのビジュアル表現は他のBPMNツールに劣る

## 利用方法

### 1. アカウント作成

1. [Process Street公式サイト](https://www.process.st/)にアクセス
2. 「Sign Up Free」をクリック
3. メールアドレスまたはGoogle/Microsoftアカウントで登録
4. ワークスペース名を設定
5. チームメンバーを招待（オプション）

### 2. 新規プロセステンプレート作成

1. ダッシュボードから「+ New Template」ボタンをクリック
2. テンプレート名を入力（例: "新規顧客オンボーディング"）
3. 「Create Template」をクリック

### 3. タスク・チェックリストの追加

#### タスクの追加

1. 「+ Add Task」ボタンをクリック
2. タスク名を入力（例: "顧客情報収集"）
3. タスクの説明を追加（オプション）

#### チェックアイテムの追加

1. タスク内で「+ Add Check」をクリック
2. チェック項目を入力（例: "✓ 会社名を確認"）
3. 複数のチェック項目を追加

#### フォームフィールドの追加

1. タスク内で「+ Add Field」をクリック
2. フィールドタイプを選択:
   - **Short Text**: 短いテキスト入力
   - **Long Text**: 長文テキスト入力
   - **Email**: メールアドレス
   - **Number**: 数値
   - **Date**: 日付
   - **Dropdown**: ドロップダウン選択
   - **File Upload**: ファイルアップロード
3. フィールド名を入力（例: "顧客名"）
4. 必須/任意を設定

### 4. 条件分岐の設定

Process Streetの強力な機能の一つが、条件分岐（Conditional Logic）です。

#### Stop Task（条件付きタスク停止）

1. タスクの「⋮」メニューをクリック
2. 「Add Stop Task」を選択
3. 条件を設定:
   - **If**: フィールド名を選択（例: "契約金額"）
   - **Condition**: 条件を選択（例: "より大きい"）
   - **Value**: 値を入力（例: "100000"）
4. 条件が満たされない場合、このタスクはスキップされる

#### Hidden Task（条件付きタスク表示）

1. タスクの「⋮」メニューをクリック
2. 「Add Hidden Task」を選択
3. 条件を設定（Stop Taskと同様）
4. 条件が満たされた場合のみ、タスクが表示される

### 5. プロセス作成の具体例

**例: 新規顧客オンボーディングプロセス**

#### タスク1: 顧客情報収集

- チェック項目:
  - ✓ 会社名を確認
  - ✓ 担当者名を確認
  - ✓ 連絡先を確認
- フォームフィールド:
  - 会社名（Short Text、必須）
  - 担当者名（Short Text、必須）
  - メールアドレス（Email、必須）
  - 契約金額（Number、必須）

#### タスク2: 契約内容確認

- チェック項目:
  - ✓ 契約プランを確認
  - ✓ 契約期間を確認
- フォームフィールド:
  - 契約プラン（Dropdown: Standard/Premium/Enterprise）

#### タスク3: アカウント作成（条件分岐）

- **Stop Task条件**: 契約プラン = "Standard"
- このタスクは、Premium/Enterpriseプランの場合のみ実行
- チェック項目:
  - ✓ 専用アカウントを作成
  - ✓ カスタムドメインを設定

#### タスク4: オンボーディングミーティング設定

- チェック項目:
  - ✓ ミーティング日程を調整
  - ✓ カレンダー招待を送信
- フォームフィールド:
  - ミーティング日時（Date）

#### タスク5: ウェルカムメール送付

- チェック項目:
  - ✓ ウェルカムメールを送信
  - ✓ アカウント情報を共有

### 6. プロセスの実行とモニタリング

#### プロセスの実行（Run）

1. テンプレートページで「Run Workflow」ボタンをクリック
2. 実行名を入力（オプション、例: "ABC株式会社 オンボーディング"）
3. 担当者を割り当て（オプション）
4. 「Run Workflow」をクリック

#### タスクの実行

1. Runページでタスクを順番に実行
2. チェック項目をチェック
3. フォームフィールドに入力
4. 「Complete Task」をクリックして次のタスクへ

#### 進捗モニタリング

1. ダッシュボードから「Workflows」を選択
2. 実行中のワークフローの一覧を確認
3. 各ワークフローの進捗率を確認
4. 担当者、期限、ステータスを確認

### 7. 自動化設定（Zapier連携）

Process Streetは、Zapierを通じて様々なツールと連携できます。

#### 例: Slackへの通知

1. Process Streetテンプレートで「Integrations」タブを選択
2. 「Zapier」を選択
3. Zapierで新規Zapを作成:
   - **Trigger**: Process Street - Workflow Run Completed
   - **Action**: Slack - Send Channel Message
4. メッセージ内容を設定（例: "{{workflow_name}}が完了しました"）

#### 例: Google Sheetsへのデータ保存

1. Zapierで新規Zapを作成:
   - **Trigger**: Process Street - Task Completed
   - **Action**: Google Sheets - Create Spreadsheet Row
2. フィールドマッピングを設定
3. ワークフロー完了時に自動的にGoogle Sheetsに記録

### 8. チーム協業

#### メンバーの招待

1. 左下のワークスペース名をクリック
2. 「Team Members」を選択
3. 「Invite Members」をクリック
4. メールアドレスを入力
5. 役割を選択（Admin/Member）
6. 「Send Invitation」をクリック

#### タスクの割り当て

1. ワークフロー実行時に、各タスクを特定のメンバーに割り当て
2. 割り当てられたメンバーにメール通知が送信される
3. タスク完了時に次の担当者に通知

### 9. レポートと分析

1. 左側メニューから「Reports」を選択
2. 以下のレポートを確認:
   - **Workflow Activity**: ワークフローの実行状況
   - **Task Completion**: タスク完了率
   - **Team Performance**: チームメンバーのパフォーマンス
   - **SLA Compliance**: SLA（サービスレベル契約）遵守率

### 10. テンプレートのエクスポート

1. テンプレートページで「⋮」メニューをクリック
2. 「Export」を選択
3. 形式を選択:
   - **PDF**: ドキュメント形式
   - **CSV**: データ形式
   - **JSON**: API形式

## 公式ドキュメント

- **公式サイト**: [Process Street](https://www.process.st/)
- **ヘルプセンター**: [Process Street Help Center](https://www.process.st/help/)
- **Process Street Academy**: [Learning Resources](https://www.process.st/help/)
- **テンプレートライブラリ**: [Template Library](https://www.process.st/templates/)
- **API Documentation**: [Process Street API](https://www.process.st/help/api-documentation/)

## ユースケース例

### 1. 従業員オンボーディング

- 入社手続きのチェックリスト
- 必要書類の収集
- アカウント作成
- 研修スケジュール管理

### 2. 顧客サポート対応

- 問い合わせ受付
- 問題分類
- エスカレーション判定
- 対応完了・顧客フォローアップ

### 3. 品質管理チェック

- 製品検査チェックリスト
- 不良品発見時のエスカレーション
- 是正措置の記録

### 4. コンテンツ公開ワークフロー

- 執筆
- レビュー・承認
- 編集
- 公開

## 関連リンク

- [Zapier Integration](https://zapier.com/apps/process-street/integrations)
- [Process Street Blog](https://www.process.st/blog/)
- [Process Street YouTube Channel](https://www.youtube.com/c/ProcessStreet)
