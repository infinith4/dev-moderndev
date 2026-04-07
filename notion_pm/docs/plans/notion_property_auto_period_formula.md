# 期間(自動)プロパティの数式設定

## Context

Notionのタスクデータベースでは、親タスクの「期間(自動)」プロパティを
**すべての子タスクの開始日の最小値 〜 終了日の最大値** で自動算出したい。

手動入力では更新漏れが発生するため、子タスクの期間Propertyをロールアップで集計し、
数式Propertyで表示する構成を採用する。

---

## 前提条件

| 項目 | 内容 |
|------|------|
| 親子関係 | 親タスクと子タスクが **Relation Property** で紐づいていること |
| 子側のRelation名 | `親タスク`（親→子 の逆リレーション名：`子タスク`） |
| 期間Property名 | `期間`（Date型、開始日・終了日あり） |
| 対象データベース | WBSタスク管理データベース |

---

## 実装内容

### Step 1: Rollupプロパティの作成（2つ）

Notionデータベースの設定から以下の **Rollup** Propertyを追加する。

#### 1-1. 子タスク_最早開始日

| 設定項目 | 値 |
|----------|-----|
| Property名 | `子タスク_最早開始日` |
| Type | Rollup |
| Relation | `子タスク`（親→子の Relation Property） |
| Property | `期間` |
| Calculate | **Earliest date** |

> ※ Notionの "Earliest date" は、Date Propertyの **start** を対象とする。

#### 1-2. 子タスク_最遅終了日

| 設定項目 | 値 |
|----------|-----|
| Property名 | `子タスク_最遅終了日` |
| Type | Rollup |
| Relation | `子タスク`（親→子の Relation Property） |
| Property | `期間` |
| Calculate | **Latest date** |

> ※ Notionの "Latest date" は、Date Propertyの **end** を対象とする（endがない場合はstartを使用）。

---

### Step 2: 数式プロパティの設定

#### 2-1. 期間(自動) Propertyの作成

| 設定項目 | 値 |
|----------|-----|
| Property名 | `期間(自動)` |
| Type | Formula |

#### 2-2. 数式（Notion Formula 2.0 形式）

```notion-formula
let(
  startDate, prop("子タスク_最早開始日"),
  endDate, prop("子タスク_最遅終了日"),
  if(
    empty(startDate) or empty(endDate),
    "未設定",
    formatDate(startDate, "YYYY-MM-DD") + " 〜 " + formatDate(endDate, "YYYY-MM-DD")
  )
)
```

#### 2-3. 数式の解説

| 部分 | 説明 |
|------|------|
| `prop("子タスク_最早開始日")` | Step 1で作成したRollup（子タスク全体の最早開始日） |
| `prop("子タスク_最遅終了日")` | Step 1で作成したRollup（子タスク全体の最遅終了日） |
| `empty(...) or empty(...)` | 子タスクが存在しない場合のガード |
| `formatDate(..., "YYYY-MM-DD")` | 日付を `2025-04-01` 形式の文字列に変換 |
| `+ " 〜 " +` | 開始〜終了を連結して `2025-04-01 〜 2025-06-30` 形式に整形 |

---

### Step 3: 表示確認用フォーマット例

子タスクに以下のような期間が設定されている場合：

| 子タスク名 | 開始日 | 終了日 |
|-----------|--------|--------|
| タスクA | 2025-04-01 | 2025-04-30 |
| タスクB | 2025-03-15 | 2025-05-10 |
| タスクC | 2025-05-01 | 2025-06-30 |

**期間(自動) の出力結果：**

```
2025-03-15 〜 2025-06-30
```

---

## 注意事項

### Rollup の "Latest date" の動作仕様

Notionの `Latest date` ロールアップは、Date Propertyの **end** が設定されている場合はそれを使用し、
設定がない場合は **start** を使用する。
そのため、子タスクの `期間` Propertyに必ず **終了日(end)** を設定することを推奨する。

### 数式プロパティの制約

| 制約 | 内容 |
|------|------|
| 出力型 | テキスト（`YYYY-MM-DD 〜 YYYY-MM-DD` 形式の文字列） |
| Date型への変換不可 | FormulaプロパティはDate型のstart/endを直接返せない |
| 代替案 | 実際のDateプロパティとして管理する場合はAPI経由で更新が必要 |

### API経由でDate型として設定する場合（拡張オプション）

FormulaではなくDate型の `期間(自動)` PropertyをAPIで更新したい場合は、
`importXlsxWbs.ts` に以下のような処理を追加することで対応可能：

```typescript
// 親タスクの期間を子タスクから自動計算して更新する
async function updateParentPeriodFromChildren(
  client: Client,
  parentPageId: string,
  childPages: PageObjectResponse[]
): Promise<void> {
  const dates = childPages
    .map(page => {
      const dateProp = page.properties["期間"] as DatePropertyItemObjectResponse;
      return dateProp?.date ?? null;
    })
    .filter((d): d is { start: string; end: string | null } => d !== null);

  if (dates.length === 0) return;

  const startDate = dates
    .map(d => d.start)
    .sort()[0]; // 最早開始日

  const endDate = dates
    .map(d => d.end ?? d.start)
    .sort()
    .reverse()[0]; // 最遅終了日

  await client.pages.update({
    page_id: parentPageId,
    properties: {
      "期間(自動)": {
        date: { start: startDate, end: endDate },
      },
    } as any,
  });
}
```

---

## 変更対象ファイル（Notion UI設定のみの場合）

| 対象 | 変更種別 | 内容 |
|------|----------|------|
| Notionデータベース | 設定変更 | Rollupプロパティ2つを追加 |
| Notionデータベース | 設定変更 | Formulaプロパティ「期間(自動)」を追加・数式を設定 |

---

## 動作確認

### 確認手順

1. 親タスクのページを開く
2. 子タスクが複数存在し、それぞれに`期間`（開始日・終了日）が設定されていることを確認
3. `子タスク_最早開始日` Rollupに最も早い開始日が表示されることを確認
4. `子タスク_最遅終了日` Rollupに最も遅い終了日が表示されることを確認
5. `期間(自動)` Formulaに `YYYY-MM-DD 〜 YYYY-MM-DD` 形式で結果が表示されることを確認

### エッジケースの確認

| ケース | 期待動作 |
|--------|----------|
| 子タスクが0件 | `未設定` と表示される |
| 子タスクが1件（終了日なし） | `2025-04-01 〜 2025-04-01`（開始日を終了日として使用） |
| 子タスクが1件（終了日あり） | `2025-04-01 〜 2025-04-30` と表示される |
| 子タスクが複数件 | 全子タスクを包含する最広の期間が表示される |
