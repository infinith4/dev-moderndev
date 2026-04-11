# Plan: Markdown ファイルからタスクボディを生成してインポート

## Context

各タスクの「対応内容」「完了条件」などのセクションを手動入力するのは工数がかかる。
Claude Code や Gemini などの AI ツールで事前に Markdown ファイルを生成し、
インポート時にそのファイルを読み込んでタスクのページボディとして Notion に登録したい。

**方針:**
- AI ツール（Claude Code / Gemini）は **コードに組み込まない**
- AI が生成した Markdown を `docs/task-bodies/` ディレクトリに保存する
- Markdown をセクション単位（`##` 見出し）に分解し、テンプレートの `_upsert_mode` に従って制御する
- ファイルが存在しないタスクはテンプレート（`child-template.json`）で代替する

---

## 運用フロー

```
① dry-run でタスク一覧出力
       ↓
② Claude Code / Gemini でタスクごとの Markdown を生成
       ↓
③ docs/task-bodies/ に保存
       ↓
④ npm run import-xlsx-wbs でインポート
       ↓
⑤ 新規作成: Markdown の全セクションを挿入
   upsert:   テンプレートの _upsert_mode に従いセクション単位で制御
```

---

## ディレクトリ構造

```
notion_pm/docs/
├── task-bodies/
│   ├── 要件定義.md                            # 親タスク（工程）の Markdown
│   ├── 基本設計.md
│   ├── 要件定義/                              # 親タスク名のフォルダ内に子タスク
│   │   ├── ヒアリング・現状分析-現状ヒアリングMTG設定.md
│   │   ├── 業務フロー作成-業務フロー作成.md
│   │   └── ...
│   ├── 基本設計/
│   │   ├── システム構成設計.md
│   │   └── ...
│   └── ...
├── child-template.json                        # ファイルが存在しない場合のフォールバック
└── parent-template.json
```

**ファイルパス規則:**
- 親タスク: `task-bodies/{parentName}.md`
- 子タスク: `task-bodies/{parentName}/{originalTaskName}.md`
  - `originalTaskName` は wbs シート F列の値（例: `ヒアリング・現状分析-現状ヒアリングMTG設定`）

---

## Markdown ファイルのフォーマット

セクション名（`##` 見出し）は `child-template.json` の `_section` と一致させること。
`_upsert_mode` の制御対象として識別されるため、名前が異なると別セクション扱いになる。

**子タスク用 Markdown:**
```markdown
## タスク着手時

- 期間に対応を期間を入力してください。(5日を超えるタスクは分割してください)
- 見積(人日)に記載がなければ入力してください。
- ステータスを対応中に変更してください。
- 完了条件を満たしたら、ステータスをレビューに変更してください。
- 成果物を記載してください。(例: PR, SpreadsheetのURLなど)

## 対応内容

- ヒアリングシートを作成する
- 関係者にMTGの日程調整メールを送付する
- MTGで現状のワークフローをヒアリングする

## 完了条件

- ヒアリングシートが完成している
- MTGが実施され、議事録が作成されている

## 成果物

- ヒアリングシート（Spreadsheet URL）
- MTG議事録（Notion URL）
```

---

## セクション単位の更新制御

Markdown ファイルが存在する場合も、`_upsert_mode` による制御を維持する。
Markdown のセクションはテンプレートの「コンテンツブロック」として扱い、
`_upsert_mode` は引き続きテンプレート JSON で管理する。

### 新規作成時（pages.create）

Markdown ファイルの全セクションを結合して `children` に渡す。
ファイルなし → テンプレートの全セクションを結合して使用（従来通り）。

### upsert（更新）時

Markdown ファイルのセクションをテンプレートのコンテンツブロックと同等に扱い、
`_upsert_mode` に従って Notion の既存ボディに適用する。

| 条件 | `_upsert_mode` | 更新時の動作 |
|---|---|---|
| Markdown あり | `overwrite` | Notion の既存コンテンツを削除し、Markdown の該当セクションで置き換え |
| Markdown あり | `append` | Markdown の該当セクションを既存末尾に追記 |
| Markdown あり | `skip` | 何もしない（手動編集を保護） |
| Markdown なし | `overwrite` | テンプレートのブロックで置き換え（従来通り） |
| Markdown なし | `append` | テンプレートのブロックを追記（従来通り） |
| Markdown なし | `skip` | 何もしない（従来通り） |
| 見出しが Notion に存在しない | いずれも | セクション全体をページ末尾に追加 |

---

## 変更対象ファイル

| ファイル | 変更種別 |
|---|---|
| `docs/task-bodies/` | **新規作成**（ディレクトリ + Markdown ファイル群） |
| `src/importXlsxWbs.ts` | **変更**（Markdown 読み込み・セクション分解・upsert 統合） |
| `package.json` | **変更**（`@tryfabric/martian` パッケージ追加） |
| `.env.example` | **変更**（`TASK_BODIES_DIR` 変数追加） |

---

## 実装内容（src/importXlsxWbs.ts）

### 使用ライブラリ

```bash
npm install @tryfabric/martian
```

`@tryfabric/martian`: Markdown テキスト → Notion ブロック配列に変換するライブラリ。

### 追加するインポートと定数

```typescript
import { markdownToBlocks } from "@tryfabric/martian";

const TASK_BODIES_DIR = process.env.TASK_BODIES_DIR
  ?? path.resolve(__dirname, "../docs/task-bodies");
```

### Markdown ファイル読み込み・セクション分解関数

```typescript
/**
 * Markdown テキストを ## 見出しでセクションに分解し、
 * セクション名 → Notion ブロック配列 のマップを返す。
 * 見出しより前のブロックは "_preamble" キーに格納する。
 */
function parseMarkdownSections(markdown: string): Map<string, unknown[]> {
  const allBlocks = markdownToBlocks(markdown) as any[];
  const sections = new Map<string, unknown[]>();
  let currentSection = "_preamble";
  let currentBlocks: unknown[] = [];

  for (const block of allBlocks) {
    if (block.type === "heading_2") {
      sections.set(currentSection, currentBlocks);
      currentSection = block.heading_2.rich_text.map((r: any) => r.text?.content ?? "").join("");
      currentBlocks = []; // 見出しブロック自体はコンテンツとして含めない
    } else {
      currentBlocks.push(block);
    }
  }
  sections.set(currentSection, currentBlocks);
  return sections;
}

/**
 * 親タスクの Markdown を読み込み、セクションマップを返す。
 * パス: task-bodies/{parentName}.md
 */
function loadParentMarkdownSections(parentName: string): Map<string, unknown[]> | null {
  const filePath = path.join(TASK_BODIES_DIR, `${parentName}.md`);
  if (!fs.existsSync(filePath)) return null;
  return parseMarkdownSections(fs.readFileSync(filePath, "utf-8"));
}

/**
 * 子タスクの Markdown を読み込み、セクションマップを返す。
 * パス: task-bodies/{parentName}/{originalTaskName}.md
 */
function loadChildMarkdownSections(parentName: string, originalTaskName: string): Map<string, unknown[]> | null {
  const filePath = path.join(TASK_BODIES_DIR, parentName, `${originalTaskName}.md`);
  if (!fs.existsSync(filePath)) return null;
  return parseMarkdownSections(fs.readFileSync(filePath, "utf-8"));
}
```

### `applyTemplateSections` の拡張

既存の `applyTemplateSections` に `markdownSections` を追加引数として渡す。
`_upsert_mode` はテンプレート JSON で管理したまま、コンテンツブロックだけを
Markdown セクションで上書きする。

```typescript
async function applyTemplateSections(
  client: Client,
  pageId: string,
  sections: TemplateSection[],
  taskName: string,
  markdownSections: Map<string, unknown[]> | null,  // 追加
): Promise<void> {
  for (const section of sections) {
    if (section._upsert_mode === "skip") continue;

    // Markdown セクションがあればそのコンテンツを優先、なければテンプレートを使用
    const contentBlocks = markdownSections?.get(section._section) ?? section.blocks.slice(1);
    // ... 以降は既存の overwrite / append ロジックで contentBlocks を使う
  }
}
```

### 新規作成時の適用

```typescript
} else {
  // 新規作成
  const originalTaskName = task.details["_originalTaskName"] ?? task.name;
  let mdSections: Map<string, unknown[]> | null = null;

  if (isParent) {
    mdSections = loadParentMarkdownSections(task.name);
    if (mdSections) console.log(`  [body] Loaded: ${task.name}.md`);
  } else if (parentName) {
    mdSections = loadChildMarkdownSections(parentName, originalTaskName);
    if (mdSections) console.log(`  [body] Loaded: ${parentName}/${originalTaskName}.md`);
  }

  // 各セクションのコンテンツを Markdown または テンプレートから取得して結合
  const bodyBlocks = template.flatMap((s) => {
    const content = mdSections?.get(s._section) ?? s.blocks.slice(1);
    const heading = s.blocks[0]; // 見出しブロック
    return heading ? [heading, ...content] : content;
  });

  page = await client.pages.create({
    parent: { database_id: databaseId },
    properties: properties as any,
    ...(isParent && { icon: PARENT_ICON }),
    ...(bodyBlocks.length > 0 && { children: bodyBlocks as any }),
  });
  created++;
}

// 子タスクの再帰呼び出しに parentName を渡す
for (const child of task.children) {
  await upsertRecursive(child, page.id, isParent ? task.name : parentName);
}
```

### upsert 時の適用

```typescript
if (existingPageId) {
  page = await client.pages.update({ ... });
  updated++;

  // Markdown セクションを読み込み（あれば）
  let mdSections: Map<string, unknown[]> | null = null;
  if (isParent) {
    mdSections = loadParentMarkdownSections(task.name);
  } else if (parentName) {
    const originalTaskName = task.details["_originalTaskName"] ?? task.name;
    mdSections = loadChildMarkdownSections(parentName, originalTaskName);
  }

  await applyTemplateSections(client, page.id, template, task.name, mdSections);
}
```

### `upsertRecursive` のシグネチャ変更

```typescript
const upsertRecursive = async (
  task: WBSTask,
  parentPageId: string | null,
  parentName: string | null,  // 追加
): Promise<void>
```

### `.env.example` への追記

```env
TASK_BODIES_DIR=docs/task-bodies
```

---

## AI コンテンツ生成手順（運用）

### 1. タスク一覧を確認する

```bash
cd /src/notion_pm
npm run import-xlsx-wbs -- --dry-run
```

### 2. Claude Code にプロンプトを渡して一括生成する

**親タスク（工程）:**
```
以下の工程タスクについて「目的」「スコープ」「完了条件」「成果物」を
Markdown 形式（## 見出し区切り）で生成し、
notion_pm/docs/task-bodies/{工程名}.md として保存してください。

工程一覧: 要件定義, 基本設計, 詳細設計, 実装, 単体テスト, 結合テスト実施, リリース, 納品
```

**子タスク（作業タスク）:**
```
以下のタスク一覧に対して、「タスク着手時」「対応内容」「完了条件」「成果物」の
セクションを Markdown 形式（## 見出し区切り）で生成し、
notion_pm/docs/task-bodies/{親タスク名}/{タスク名}.md として保存してください。

タスク一覧:
- 要件定義/ヒアリング・現状分析-現状ヒアリングMTG設定（工数: 4日）
- 要件定義/業務フロー作成-業務フロー作成（工数: 2日）
- 基本設計/システム構成設計（工数: 3.5日）
...
```

### 3. インポート実行

```bash
npm run import-xlsx-wbs
```

---

## 動作確認

```bash
# 1. Dry run
npm run import-xlsx-wbs -- --dry-run

# 2. 実登録
npm run import-xlsx-wbs
# ログに "[body] Loaded: {パス}" が出ればファイルから読み込まれている

# 3. Notion で確認するポイント
```

| シナリオ | 期待動作 |
|---|---|
| Markdown あり・新規作成 | Markdown の各セクションが見出し付きで挿入される |
| Markdown あり・upsert・overwrite | Notion の「タスク着手時」がMarkdown内容で置き換わる |
| Markdown あり・upsert・skip | Notion の「対応内容」など手動編集が保護される |
| Markdown なし・新規作成 | テンプレートの全セクションが挿入される（従来通り） |
| Markdown なし・upsert | テンプレートの `_upsert_mode` に従い制御（従来通り） |
