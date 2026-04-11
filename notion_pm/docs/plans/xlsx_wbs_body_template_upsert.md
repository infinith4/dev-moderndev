# Plan: テンプレートのセクション単位での上書き・追記制御

## Context

`npm run import-xlsx-wbs` の upsert（更新）時、現在はページボディを一切変更しない。
テンプレート JSON の各見出しセクションごとに `_upsert_mode` を設定し、
更新時に「上書き」「追記」「変更なし（skip）」を制御できるようにする。

**方針:**
- テンプレート JSON を「セクション配列」形式に変更（`_section` / `_upsert_mode` / `blocks` を持つオブジェクト）
- 見出し名でセクションを識別し、Notion API で既存ブロックを操作する
- 新規作成時はすべてのセクションの `blocks` を結合して `children` に渡す（従来通り）
- 更新時は各セクションの `_upsert_mode` に従って処理する

| `_upsert_mode` | 更新時の動作 |
|---|---|
| `"overwrite"` | 既存の見出し配下のコンテンツブロックを削除し、テンプレートのコンテンツブロックを再挿入 |
| `"append"` | 既存セクション末尾にテンプレートのコンテンツブロックを追記 |
| `"skip"` | 何もしない（手動編集を保護） |
| 見出しが存在しない場合 | セクション全体（見出し＋コンテンツ）をページ末尾に追加 |

---

## 変更対象ファイル

| ファイル | 変更種別 |
|---|---|
| `docs/child-template.json` | **変更**（セクション配列形式に再構成） |
| `docs/parent-template.json` | **変更**（セクション配列形式に再構成） |
| `src/importXlsxWbs.ts` | **変更**（型定義・関数追加・upsert ロジック変更） |

---

## テンプレート JSON の新フォーマット

### child-template.json の各セクション設定

| セクション | `_upsert_mode` | 理由 |
|---|---|---|
| タスク着手時 | `overwrite` | 常に最新のチェックリストを表示したい |
| 対応内容 | `skip` | 手動記入内容を保護する |
| 完了条件 | `skip` | 手動記入内容を保護する |
| 成果物 | `skip` | 手動記入内容を保護する |

### parent-template.json の各セクション設定

| セクション | `_upsert_mode` | 理由 |
|---|---|---|
| 目的 | `skip` | 手動記入内容を保護する |
| スコープ | `skip` | 手動記入内容を保護する |
| 完了条件 | `skip` | 手動記入内容を保護する |
| 成果物 | `skip` | 手動記入内容を保護する |
| リスク・課題 | `append` | 行を追記して管理したい |

### フォーマット例（child-template.json 抜粋）

```json
[
  {
    "_section": "タスク着手時",
    "_upsert_mode": "overwrite",
    "blocks": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": { "rich_text": [{ "text": { "content": "タスク着手時" } }] }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": { "rich_text": [{ "text": { "content": "期間に対応を期間を入力してください。(5日を超えるタスクは分割してください)" } }] }
      }
    ]
  },
  {
    "_section": "対応内容",
    "_upsert_mode": "skip",
    "blocks": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": { "rich_text": [{ "text": { "content": "対応内容" } }] }
      },
      {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": { "rich_text": [{ "text": { "content": "" } }] }
      }
    ]
  }
]
```

---

## 実装内容（src/importXlsxWbs.ts）

### 型定義の追加

```typescript
interface TemplateSection {
  _section: string;
  _upsert_mode: "overwrite" | "append" | "skip";
  blocks: unknown[];
}
```

### `loadTemplate` の戻り値型を変更

```typescript
function loadTemplate(filePath: string): TemplateSection[] {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf-8")) as TemplateSection[];
  } catch {
    console.warn(`Template not found or invalid: ${filePath}. Using empty body.`);
    return [];
  }
}
```

### ヘルパー関数の追加

```typescript
/** 既存ページのブロックを全件取得（ページネーション対応） */
async function fetchAllBlocks(client: Client, pageId: string): Promise<BlockObject[]>

/** ブロックが heading_2 かつ指定テキストに一致するか */
function matchesHeading(block: BlockObject, text: string): boolean

/** 見出しブロックか判定（heading_1/2/3） */
function isHeadingBlock(block: BlockObject): boolean

/**
 * upsert 時にテンプレートセクションを適用する。
 * - overwrite: 既存見出し配下のブロックを削除 → テンプレートのコンテンツを挿入
 * - append:    既存セクション末尾にテンプレートのコンテンツを追記
 * - skip:      何もしない
 * - 見出しが見つからない場合: セクション全体をページ末尾に追加
 */
async function applyTemplateSections(
  client: Client,
  pageId: string,
  sections: TemplateSection[],
): Promise<void>
```

### upsert 分岐の変更

```typescript
if (existingPageId) {
  // 更新: プロパティを更新し、テンプレートセクションを適用
  page = await client.pages.update({ ... });
  updated++;
  const template = isParent ? parentTemplate : childTemplate;
  await applyTemplateSections(client, page.id, template);
} else {
  // 新規作成: 全セクションの blocks を結合して children に渡す
  const allBlocks = (isParent ? parentTemplate : childTemplate)
    .flatMap(s => s.blocks);
  page = await client.pages.create({
    ...
    ...(allBlocks.length > 0 && { children: allBlocks as any }),
  });
  created++;
}
```

---

## 動作確認

```bash
cd /src/notion_pm

# 1. Dry run
npm run import-xlsx-wbs -- --dry-run

# 2. 新規作成（全セクションが挿入されることを確認）
npm run import-xlsx-wbs

# 3. 再実行（overwrite / skip / append の動作を確認）
npm run import-xlsx-wbs
```

### Notion で確認するポイント

| シナリオ | 期待動作 |
|---|---|
| 新規作成後 | 子タスクに全4セクションが存在する |
| 「対応内容」に手動入力 → 再実行 | 手動テキストが残っている（skip） |
| 「タスク着手時」を手動変更 → 再実行 | テンプレート内容に戻っている（overwrite） |
| 親タスクの「リスク・課題」テーブルに行追加 → 再実行 | 既存行が残り、テンプレートの行が末尾に追加される（append） |
| 見出しが存在しないページ → 再実行 | セクション全体がページ末尾に追加される |
