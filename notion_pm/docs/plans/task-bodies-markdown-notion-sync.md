# Plan: task-bodies Markdown生成 & Notion同期の設計

## Context

`notion_pm` の `importXlsxWbs.ts` は `docs/task-bodies/` の Markdown を読み込んで Notion に反映する役割を持たせたい。
不足しているのは以下の2点：
1. **Markdown ファイルを生成するしくみ**（`docs/task-bodies/` の初期生成）
2. **Notion ページボディを `docs/task-bodies/` に書き戻すしくみ**（Markdown を Notion の最新状態に追従させる）

---

## Part 1: Markdown 生成方法

### 推奨: `scripts/generate-task-bodies.sh`（Claude Code CLI による自動生成）

**追加コスト不要。** Claude Code CLI (`claude -p`) を使ってシェルスクリプトから非インタラクティブに一括生成する。

| ツール | コスト | 備考 |
|---|---|---|
| **Claude Code CLI** (`claude -p`) | Pro に含まれる ✅ | `--allowedTools "Write"` でファイル直接生成 |
| Codex CLI (`codex`) | OpenAI API key 別途必要 ❌ | コード生成特化で Markdown 生成には不向き |

**実行方法:**

```bash
cd /src/notion_pm

# 既存ファイルはスキップ（通常実行）
bash scripts/generate-task-bodies.sh

# 強制上書き
bash scripts/generate-task-bodies.sh --force
```

**内部フロー:**

```
① npm run import-xlsx-wbs -- --dry-run
   → タスク一覧テキストを取得

② python3 で child/parent-template.json からセクション名を自動抽出

③ プロンプトを /tmp 一時ファイルに書き込む

④ claude -p --allowedTools "Write" "$(cat prompt)"
   → Claude が Write ツールで docs/task-bodies/**/*.md を一括生成
```

**前提条件:**
```bash
which claude   # PATH に存在するか確認
# なければ: npm install -g @anthropic-ai/claude-code
```

**セクション名の制約（重要）:**
- 子タスク: `タスク着手時` / `対応内容` / `完了条件` / `成果物`（`child-template.json` の `_section` と完全一致）
- 親タスク: `目的` / `スコープ` / `完了条件` / `成果物` / `リスク・課題`（`parent-template.json` と完全一致）
- スクリプトがテンプレート JSON から動的に読み取るため、テンプレート変更にも自動追従する

### 代替案: `scripts/generate-task-bodies-codex.sh`（Codex CLI による自動生成）

Claude Code CLI と同じ 4 ステップを維持しつつ、生成実行だけを `codex exec` に置き換える案。

**実行方法:**

```bash
cd /src/notion_pm

# 既存ファイルはスキップ（通常実行）
bash scripts/generate-task-bodies-codex.sh

# 強制上書き
bash scripts/generate-task-bodies-codex.sh --force
```

**内部フロー:**

```
① npm run import-xlsx-wbs -- --dry-run
   → タスク一覧テキストを取得

② python3 で child/parent-template.json からセクション名を自動抽出

③ プロンプトを /tmp 一時ファイルに書き込む

④ codex exec --full-auto -C "$NOTION_PM_DIR" - < "$PROMPT_FILE"
   → Codex が docs/task-bodies/**/*.md を一括生成
```

**npm script 案:**

```json
"generate-task-bodies:codex": "bash scripts/generate-task-bodies-codex.sh"
```

**前提条件:**

```bash
which codex   # PATH に存在するか確認
codex login   # 未ログインなら先に実施
```

**Codex 用プロンプトで明示する制約:**
- 作業ディレクトリは `notion_pm`
- 変更対象は `docs/task-bodies/**` のみ
- 親タスクは `docs/task-bodies/{タスク名}.md`
- 子タスクは `docs/task-bodies/{親タスク名}/{タスク名}.md`
- `##` 見出し名はテンプレート JSON の `_section` と完全一致させる
- `--force` なしでは既存ファイルを上書きしない
- 余計なファイル作成や他パスの変更は行わない

**コマンド例:**

```bash
codex exec --full-auto -C "$NOTION_PM_DIR" - < "$PROMPT_FILE"
```

### 代替案: Gemini Web App (`https://gemini.google.com/app?hl=ja`) による半手動生成

Gemini Web App でも同様の Markdown 本文生成は可能。ただし CLI のようにローカルの `docs/task-bodies/**` へ直接書き込む手段は前提にしにくいため、**生成は Gemini、保存は手動** の運用とする。

**向いているケース:**
- ローカル CLI のセットアップなしで試したい
- プロンプトを対話的に微調整しながら文章品質を上げたい
- まず数ファイルだけ試作したい

**制約:**
- `claude` / `codex` のようにローカルファイルへ直接保存する自動化には向かない
- Gemini Web App 上で生成した内容を、`docs/task-bodies/**/*.md` へ手動で保存する必要がある
- タスク数が多い場合は手作業が増えるため、バッチ生成は CLI 案の方が現実的

**実行方法:**

```text
1. /src/notion_pm で npm run import-xlsx-wbs -- --dry-run を実行
2. Gemini Web App を開く
   https://gemini.google.com/app?hl=ja
3. dry-run 出力、parent-template.json、child-template.json を Gemini に渡す
4. Gemini に Markdown を生成させる
5. 生成結果を docs/task-bodies/{親}.md / docs/task-bodies/{親}/{子}.md として保存する
```

**推奨フロー:**

```
① npm run import-xlsx-wbs -- --dry-run
   → タスク一覧を取得

② Gemini Web App に以下を貼り付け or アップロード
   - dry-run 出力
   - docs/parent-template.json
   - docs/child-template.json

③ 生成単位を分ける
   - 親タスクごとに生成
   - あるいは 1 ファイルずつ生成

④ Gemini の回答を Markdown コードブロックで出させる
   → 各ファイルを docs/task-bodies/** に保存
```

**Gemini に渡すプロンプトの要点:**
- 出力対象は `docs/task-bodies/**` の Markdown 本文のみ
- 親タスクは `docs/task-bodies/{タスク名}.md`
- 子タスクは `docs/task-bodies/{親タスク名}/{タスク名}.md`
- `##` 見出し名はテンプレート JSON の `_section` と完全一致
- 1 回の回答では 1 ファイルずつ出力させるか、複数ファイルなら `path:` 見出し付きで分離させる
- 回答は必ず Markdown コードブロックで出力させる
- `リスク・課題` は空テーブル
- `タスク着手時` は既定チェックリストをそのまま使用

**Gemini 用プロンプト例:**

```text
以下の WBS タスクに対して、Markdown ファイル本文を生成してください。

制約:
- 出力は Markdown コードブロックのみ
- 見出しは ## から始める
- 親タスクは docs/task-bodies/{タスク名}.md
- 子タスクは docs/task-bodies/{親タスク名}/{タスク名}.md
- セクション名は parent-template.json / child-template.json の _section と完全一致
- 今回は 1 ファイルずつ出力する
- 「タスク着手時」は既定チェックリストをそのまま使う
- 「リスク・課題」は空テーブル（ヘッダーのみ）

対象タスク:
{ここに dry-run 出力から対象タスクを貼る}
```

**Gemini Web App を使う理由:**
- Google 公式ヘルプ上、Gemini Web App はファイルやコードフォルダのアップロードに対応している
- 生成結果は Google Docs などへ export できるため、下書き作成には使いやすい
- 一方で、ローカルの `docs/task-bodies/**` への直接保存は公式ヘルプ上の標準フローではないため、保存は手動運用にするのが安全

**補足:**
- dry-run 出力をそのまま貼るだけでも使えるが、`parent-template.json` / `child-template.json` も併せて渡した方が見出し名の揺れを防ぎやすい
- ファイル数が多い場合は、Gemini で草案を作り、最終的な一括生成は `generate-task-bodies-codex.sh` または Claude 案へ寄せた方が管理しやすい

---

## Part 2: Notion 同期方法

### 推奨: `src/syncTaskBodies.ts`（Notion → Markdown の独立同期スクリプト）

Excel に依存せず、Notion ページボディを `docs/task-bodies/` の Markdown ファイル群へ単独同期するスクリプト。

**なぜ独立スクリプトが必要か:**
- `importXlsxWbs.ts` は Markdown → Notion のインポート専用に寄せたい
- Notion 上で更新した本文をローカル Markdown に取り込みたい
- Excel が手元になくても Notion の現状を `docs/task-bodies/` に反映できる
- 将来的な定期同期や watch の起点にしやすい

**実装概要:**

```
Notion データベースを走査
  → タイトル / 親子Relation / キャッシュから task-bodies 上の出力先を決定
  → ページブロックを全件取得
  → heading_2 単位でテンプレート対象セクションを抽出
  → Notion ブロックを Markdown に変換
  → docs/task-bodies/{親}.md / docs/task-bodies/{親}/{子}.md に書き出し
  → .sync-state.json に task key → page ID を保存
```

**状態ファイル:** `docs/task-bodies/.sync-state.json`
```json
{
  "要件定義": "notion-page-id-xxx",
  "要件定義/ヒアリング・現状分析-現状ヒアリングMTG設定": "notion-page-id-yyy"
}
```
PM_V2 の `.wbs_sync_state.json` と同様のパターン。

**npm スクリプト:**
```json
"import-notion-markdown": "ts-node src/syncTaskBodies.ts"
```

**参照・再利用する既存コード:**
- `src/notionClient.ts` の `createNotionClient()` / `getPagesByDatabaseId()` → そのまま使用
- `src/importXlsxWbs.ts` の Markdown セクション構造とテンプレート JSON → 見出し名の基準として流用
- `src/notionBodyUtils.ts` に `fetchAllBlocks()` / heading 判定 / テンプレート section 抽出ロジックを集約

**共通化の方針:** `fetchAllBlocks`, `matchesHeading`, `isHeadingBlock`, `extractTemplateSectionsFromBlocks`, `serializeBlocksToMarkdown` などを `src/notionBodyUtils.ts` にまとめ、`importXlsxWbs.ts` と `syncTaskBodies.ts` で共有する。

**Markdown 変換方針:**
- 親タスク: `docs/task-bodies/{parentName}.md`
- 子タスク: `docs/task-bodies/{parentName}/{originalTaskName}.md`
- 出力順はテンプレート JSON の `_section` 順を優先する
- 各セクションは `## セクション名` で出力する
- テンプレートに存在しない Notion 見出しは、原則として同期対象外にする
- `skip` セクションも Notion → Markdown では書き出す。`skip` は Markdown → Notion 時の上書き制御にだけ使う

**ページ解決方針:**
- まず `.sync-state.json` の page ID を信頼する
- キャッシュがない場合はデータベース全件取得結果からタイトル一致で解決する
- 子タスクのファイルパスは Notion の親 Relation から `{parentName}/{childName}` を復元する
- タイトル重複時は自動確定しない。警告してスキップし、state 修正または手動対応を促す

---

## 全体ワークフロー（完成後）

```
① bash scripts/generate-task-bodies.sh
   dry-run → Claude Code CLI → docs/task-bodies/**/*.md を一括生成

② (内容確認・手動編集)
   docs/task-bodies/**/*.md をエディタで確認・修正

③ npm run import-xlsx-wbs
   Excel + docs/task-bodies/*.md → Notion (プロパティ + ボディを反映)

④ (Notion 側の編集を取り込みたい場合) npm run import-notion-markdown
   Notion → docs/task-bodies/**/*.md を再同期
```

---

## 変更対象ファイル

| ファイル | 変更種別 | 内容 |
|---|---|---|
| `scripts/generate-task-bodies.sh` | **新規** | Claude Code CLI による Markdown 一括生成スクリプト |
| `src/notionBodyUtils.ts` | **新規** | Notion ブロック取得、セクション抽出、Markdown 変換の共通ヘルパー |
| `src/syncTaskBodies.ts` | **新規** | Notion → Markdown のボディ同期スクリプト |
| `src/importXlsxWbs.ts` | **変更** | Markdown → Notion 専用の役割に整理し、共通ヘルパーを利用 |
| `package.json` | **変更** | npm scripts 追加（`import-notion-markdown`） |
| `docs/task-bodies/.sync-state.json` | **新規（自動生成）** | page ID キャッシュ |

---

## 検証手順

```bash
# 1. Markdown 一括生成（既存スキップ）
bash scripts/generate-task-bodies.sh

# 1b. 強制上書き
bash scripts/generate-task-bodies.sh --force

# 2. docs/task-bodies/ の内容を確認
ls docs/task-bodies/
ls docs/task-bodies/要件定義/   # 子タスク確認

# 3. Notion へインポート
npm run import-xlsx-wbs -- --dry-run
npm run import-xlsx-wbs

# 4. Notion から Markdown へ同期
npm run import-notion-markdown

# 確認ポイント:
# - import-xlsx-wbs で Markdown 内容が Notion ページに反映される
# - import-notion-markdown で Notion の各セクションが docs/task-bodies に書き戻される
# - 親タスク/子タスクの保存先パスが崩れない
# - セクション見出しがテンプレート順で出力される
# - .sync-state.json に page ID が記録されている
```
