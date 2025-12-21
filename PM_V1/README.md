# PM_V1 - Project Management Integration

Google SpreadsheetとNotionを連携して、プロジェクト管理タスクを同期するPythonツール群です。

## 概要

このツールは以下の機能を提供します:

- **双方向同期**: Google SpreadsheetとNotionデータベースを双方向で同期
  - **Spreadsheet → Notion**: SpreadsheetからNotionへタスクを追加・更新
  - **Notion → Spreadsheet**: NotionからSpreadsheetへタスクを追加・更新
- **タイトル接頭辞フィルタ**: `[工程]` などの接頭辞でタスクをフィルタリング
- **Upsert操作**: 既存データは更新、新規データは作成

## ファイル構成

```
PM_V1/
├── README.md                        # このファイル
├── requirements.txt                 # Python依存関係
├── .env.example                     # 環境変数のサンプル
├── .gitignore                       # Git除外設定
├── notion_api.py                    # Notion API クライアント
├── spreadsheet_client.py            # Google Spreadsheet クライアント
├── sync.py                          # 双方向同期メインスクリプト（推奨）
├── sync_spreadsheet_to_notion.py    # Spreadsheet→Notion 同期スクリプト
└── sync_notion_to_spreadsheet.py    # Notion→Spreadsheet 同期スクリプト
```

## セットアップ

### 1. 依存関係のインストール

```bash
cd PM_V1
pip install -r requirements.txt
```

### 2. Notion API の設定

1. [Notion Integrations](https://www.notion.so/my-integrations) でインテグレーションを作成
2. APIキーを取得
3. 対象のNotionデータベースをインテグレーションに共有
4. データベースIDを取得（データベースURLの一部）

データベースには以下のプロパティが必要です:
- `Name` (Title): ページタイトル
- `進捗率` (Number): 進捗率（0-100）
- `プロジェクト` (Select): プロジェクト名

### 3. Google Spreadsheet API の設定

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. Google Sheets API と Google Drive API を有効化
3. サービスアカウントを作成
4. サービスアカウントのJSONキーをダウンロードし、`credentials.json` として保存
5. 対象のSpreadsheetをサービスアカウントのメールアドレスに共有

Spreadsheetは以下の形式を想定しています:

| タイトル | 進捗率 | プロジェクト |
|---------|--------|-------------|
| [工程] 要件定義 | 50 | テストプロジェクト |
| [工程] 設計 | 30 | テストプロジェクト |
| [工程] 実装 | 0 | テストプロジェクト |

### 4. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成:

```bash
cp .env.example .env
```

`.env` ファイルを編集して、以下の値を設定:

```env
# Notion API Settings
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Sheets Settings
GOOGLE_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHEET_NAME=Sheet1
```

#### 設定値の取得方法

**NOTION_API_KEY**:
- Notion Integrations ページで作成したインテグレーションの "Internal Integration Token"

**NOTION_DATABASE_ID**:
- NotionのデータベースURLから取得
- 例: `https://www.notion.so/myworkspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...`
- `?` の前の32文字の英数字がデータベースID

**SPREADSHEET_ID**:
- SpreadsheetのURLから取得
- 例: `https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx/edit`
- `/d/` と `/edit` の間の文字列がスプレッドシートID

**SHEET_NAME**:
- Spreadsheet内のシート名（デフォルト: "Sheet1"）

## 使用方法

### 双方向同期スクリプト（推奨）

**sync.py** を使うと、同期方向を簡単に切り替えられます。

#### Spreadsheet → Notion へ同期

```bash
python sync.py --mode sheet-to-notion
```

このコマンドは:

1. Google Spreadsheetから `[工程]` で始まるタスクを読み込み
2. 各タスクについて、Notionデータベース内で同じタイトルのページを検索
3. 存在する場合は進捗率を更新、存在しない場合は新規ページを作成

#### Notion → Spreadsheet へ同期

```bash
python sync.py --mode notion-to-sheet
```

このコマンドは:

1. Notionデータベースから「テストプロジェクト」の `[工程]` で始まるページを取得
2. 各ページのタイトルと進捗率を取得
3. Spreadsheet内で同じタイトルの行を検索
4. 存在する場合は進捗率を更新、存在しない場合は新規行を追加

#### オプション指定

プロジェクト名や接頭辞をカスタマイズできます:

```bash
# カスタムプロジェクトと接頭辞を指定
python sync.py --mode sheet-to-notion --prefix "[フェーズ]" --project "MyProject"

# Notion→Spreadsheet でカスタム設定
python sync.py --mode notion-to-sheet --prefix "[工程]" --project "プロジェクトA"
```

### 個別スクリプト（上級者向け）

各スクリプトを直接実行することもできます:

```bash
# Spreadsheet → Notion
python sync_spreadsheet_to_notion.py

# Notion → Spreadsheet
python sync_notion_to_spreadsheet.py
```

## スクリプト詳細

### notion_api.py

Notion APIを使ってデータベース操作を行うクライアントクラス。

**主要メソッド:**

- `create_page(title, progress, properties)`: 新規ページ作成
- `update_page(page_id, title, progress, properties)`: ページ更新
- `find_page_by_title(title, title_prefix)`: タイトルでページ検索
- `upsert_page(title, progress, project_name, title_prefix)`: ページ作成または更新

### spreadsheet_client.py

Google Spreadsheet APIを使ってデータ読み込みを行うクライアントクラス。

**主要メソッド:**

- `read_tasks(title_prefix)`: タスクデータ読み込み
- `write_task(row, title, progress, project)`: タスク書き込み
- `append_task(title, progress, project)`: タスク追加
- `update_or_append_task(title, progress, project)`: タスク更新または追加

### sync.py

双方向同期のメインスクリプト。コマンドライン引数でモードを切り替え。

**コマンドライン引数:**

- `--mode`: 同期モード（`sheet-to-notion` または `notion-to-sheet`）
- `--prefix`: タイトルの接頭辞（デフォルト: `[工程]`）
- `--project`: プロジェクト名（デフォルト: `テストプロジェクト`）

### sync_spreadsheet_to_notion.py

SpreadsheetからNotionへタスクを同期するスクリプト。

**処理フロー:**

1. 環境変数から設定を読み込み
2. Spreadsheet・Notionクライアントを初期化
3. Spreadsheetから `[工程]` タスクを読み込み
4. 各タスクをNotionへupsert（作成または更新）
5. 結果サマリーを表示

### sync_notion_to_spreadsheet.py

NotionからSpreadsheetへタスクを同期するスクリプト。

**処理フロー:**

1. 環境変数から設定を読み込み
2. Notion・Spreadsheetクライアントを初期化
3. Notionから指定プロジェクトの `[工程]` ページを取得
4. 各ページのタイトルと進捗率を取得
5. Spreadsheetへupsert（更新または追加）
6. 結果サマリーを表示

## トラブルシューティング

### "環境変数が設定されていません" エラー

`.env` ファイルが正しく作成されているか確認してください。

### Google API 認証エラー

1. `credentials.json` ファイルが正しい場所にあるか確認
2. サービスアカウントにSpreadsheetの共有権限があるか確認
3. Google Sheets API と Google Drive API が有効化されているか確認

### Notion API エラー

1. APIキーが正しいか確認
2. データベースがインテグレーションに共有されているか確認
3. データベースに必要なプロパティ（Name, 進捗率, プロジェクト）が存在するか確認

### "タスクが見つからない" 問題

1. Spreadsheetのヘッダー行が以下と一致するか確認:
   - `タイトル`, `進捗率`, `プロジェクト`
2. タスクのタイトルが `[工程]` で始まっているか確認

## ライセンス

MIT License

## 貢献

バグ報告や機能リクエストは、GitHubのIssuesでお願いします。
