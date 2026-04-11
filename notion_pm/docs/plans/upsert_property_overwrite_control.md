# Plan: upsert 時のプロパティ上書き制御フラグ

## Context

`npm run import-xlsx-wbs` を2回以上実行すると、既存ページのプロパティが
Excel / term シートの値で常に上書きされる。
Notion で手動変更した期間・工数・Relation を保護したいケースがある。

`.env` のフラグで各プロパティの upsert 時上書きを制御できるようにする。

---

## 変更対象ファイル

| ファイル | 変更種別 |
|---|---|
| `src/importXlsxWbs.ts` | **変更**（定数追加・properties 構築ロジック変更） |
| `.env.example` | **変更**（フラグ変数を追加） |

---

## 追加する環境変数

`.env.example` に以下を追記:

```env
# upsert（更新）時の上書き制御（true=上書きする / false=上書きしない、デフォルト: true）
OVERWRITE_PERIOD=true
OVERWRITE_EFFORT=true
OVERWRITE_PARENT_RELATION=true
OVERWRITE_CHILDREN_RELATION=true
```

| 変数名 | 対象プロパティ | デフォルト | 説明 |
|---|---|---|---|
| `OVERWRITE_PERIOD` | 期間（Date） | `true` | false にすると upsert 時に期間を変更しない |
| `OVERWRITE_EFFORT` | 見積(人日)（Number） | `true` | false にすると upsert 時に工数を変更しない |
| `OVERWRITE_PARENT_RELATION` | 親タスク（Relation） | `true` | false にすると upsert 時に親タスク Relation を変更しない |
| `OVERWRITE_CHILDREN_RELATION` | サブタスク（Relation） | `true` | false にすると upsert 時に子タスク Relation を変更しない |

> タイトルは常に Excel の値で同期する（変更不可）。

---

## 実装内容（src/importXlsxWbs.ts）

### 定数に追加

```typescript
const OVERWRITE_PERIOD            = process.env.OVERWRITE_PERIOD            !== "false";
const OVERWRITE_EFFORT            = process.env.OVERWRITE_EFFORT            !== "false";
const OVERWRITE_PARENT_RELATION   = process.env.OVERWRITE_PARENT_RELATION   !== "false";
const OVERWRITE_CHILDREN_RELATION = process.env.OVERWRITE_CHILDREN_RELATION !== "false";
```

デフォルト `true`（`"false"` と明示した場合のみ無効化）。

### `upsertRecursive` の properties 構築ロジック変更

現在はすべて無条件に `properties` に設定しているが、
`existingPageId` がある場合（upsert）は各フラグを参照して条件付きで設定する。

```typescript
const isUpsert = !!existingPageId;

const properties: Record<string, unknown> = {
  title: { title: [{ text: { content: task.name } }] }, // 常に更新
};

// 親タスク Relation
if (PARENT_PROP) {
  if (!isUpsert || OVERWRITE_PARENT_RELATION) {
    properties[PARENT_PROP] = parentPageId
      ? { relation: [{ id: parentPageId }] }
      : { relation: [] };
  }
}

// 期間・工数（子タスクのみ）
const originalName = task.details["_originalTaskName"];
if (originalName) {
  const term = termMap.get(originalName);
  if (term) {
    if (term.startDate && (!isUpsert || OVERWRITE_PERIOD)) {
      properties[PERIOD_PROP] = {
        date: { start: term.startDate, end: term.endDate || null },
      };
    }
    if (term.effort > 0 && (!isUpsert || OVERWRITE_EFFORT)) {
      properties[EFFORT_PROP] = { number: term.effort };
    }
  }
}
```

### サブタスク Relation の更新制御

子タスクの Relation を親ページに書き戻す処理にもフラグを適用する:

```typescript
// 子タスクが存在する場合、親タスクに子タスク Relation を明示セット
if (CHILDREN_PROP && task.children.length > 0) {
  if (!isUpsert || OVERWRITE_CHILDREN_RELATION) {
    const childIds = task.children
      .map((c) => c.notionPageId)
      .filter((id): id is string => !!id);
    if (childIds.length > 0) {
      await client.pages.update({ ... });
    }
  }
}
```

---

## dry-run 出力への反映

フラグ状態を dry-run 時にも表示する:

```
OVERWRITE flags: PERIOD=true EFFORT=true PARENT_RELATION=true CHILDREN_RELATION=true
```

---

## 動作確認

```bash
# 1. デフォルト（全て上書き）
npm run import-xlsx-wbs

# 2. 期間・工数を保護して実行
OVERWRITE_PERIOD=false OVERWRITE_EFFORT=false npm run import-xlsx-wbs

# 3. Relation を保護して実行
OVERWRITE_PARENT_RELATION=false OVERWRITE_CHILDREN_RELATION=false npm run import-xlsx-wbs
```

Notion で確認するポイント:
- `OVERWRITE_PERIOD=false` で実行後、手動変更した期間が残っている
- `OVERWRITE_EFFORT=false` で実行後、手動変更した工数が残っている
- `OVERWRITE_PARENT_RELATION=false` で実行後、親タスク Relation が変わっていない
- `OVERWRITE_CHILDREN_RELATION=false` で実行後、サブタスク Relation が変わっていない
