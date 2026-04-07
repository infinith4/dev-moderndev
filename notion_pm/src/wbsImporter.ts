import { Client } from "@notionhq/client";
import type { WBSRow } from "./googleSheetsClient";

/** WBS タスクの階層ノード */
export interface WBSTask {
  level: "大項目" | "中項目" | "小項目";
  name: string;
  details: Record<string, string>;
  notionPageId?: string;
  children: WBSTask[];
}

/** WBS インポート結果 */
export interface ImportResult {
  created: number;
  tasks: WBSTask[];
}

/**
 * WBS 行データを大項目→中項目→小項目の階層ツリーに変換する
 *
 * ルール:
 *   - 大項目が変わったら新しい親タスクを作成（同一大項目はまとめる）
 *   - 中項目が存在する行は大項目の子タスクとして追加（同一中項目はまとめる）
 *   - 小項目が存在する行は中項目の子タスクとして追加（小項目のみの場合は大項目直下）
 */
export function parseWBS(rows: WBSRow[]): WBSTask[] {
  const majorTasks: WBSTask[] = [];
  const majorMap = new Map<string, WBSTask>();
  const mediumMap = new Map<string, WBSTask>();

  for (const row of rows) {
    const { 大項目, 中項目, 小項目, ...rest } = row;

    if (!大項目) continue;

    // 大項目の作成（初出のみ）
    if (!majorMap.has(大項目)) {
      const task: WBSTask = {
        level: "大項目",
        name: 大項目,
        details: {},
        children: [],
      };
      majorTasks.push(task);
      majorMap.set(大項目, task);
    }
    const majorTask = majorMap.get(大項目)!;

    if (!中項目 && !小項目) {
      // 大項目のみの行 → 詳細を大項目に補完
      Object.assign(majorTask.details, rest);
      continue;
    }

    if (中項目) {
      const mediumKey = `${大項目}::${中項目}`;

      // 中項目の作成（初出のみ）
      if (!mediumMap.has(mediumKey)) {
        const task: WBSTask = {
          level: "中項目",
          name: 中項目,
          details: {},
          children: [],
        };
        majorTask.children.push(task);
        mediumMap.set(mediumKey, task);
      }
      const mediumTask = mediumMap.get(mediumKey)!;

      if (小項目) {
        // 小項目を中項目の子として追加
        mediumTask.children.push({
          level: "小項目",
          name: 小項目,
          details: rest,
          children: [],
        });
      } else {
        // 中項目のみ → 詳細を中項目に補完
        Object.assign(mediumTask.details, rest);
      }
    } else if (小項目) {
      // 中項目なし・小項目あり → 大項目の直下に追加
      majorTask.children.push({
        level: "小項目",
        name: 小項目,
        details: rest,
        children: [],
      });
    }
  }

  return majorTasks;
}

/**
 * WBS ツリーを Notion データベースにタスクとして作成する
 *
 * @param client        Notion クライアント
 * @param databaseId    タスクを作成するデータベース ID
 * @param tasks         parseWBS() が返したツリー
 * @param parentProp    親タスクを紐付ける Relation プロパティ名（省略時は無視）
 */
export async function createNotionTasks(
  client: Client,
  databaseId: string,
  tasks: WBSTask[],
  parentProp?: string
): Promise<ImportResult> {
  let created = 0;

  const createRecursive = async (
    task: WBSTask,
    parentPageId: string | null
  ): Promise<void> => {
    const properties = buildProperties(task, parentPageId, parentProp);

    const page = await client.pages.create({
      parent: { database_id: databaseId },
      properties,
    });

    task.notionPageId = page.id;
    created++;

    for (const child of task.children) {
      await createRecursive(child, page.id);
    }
  };

  for (const task of tasks) {
    await createRecursive(task, null);
  }

  return { created, tasks };
}

/**
 * Notion ページのプロパティオブジェクトを組み立てる
 */
function buildProperties(
  task: WBSTask,
  parentPageId: string | null,
  parentProp?: string
): Record<string, unknown> {
  const properties: Record<string, unknown> = {
    // Title プロパティ（Notion データベースの必須プロパティ）
    title: {
      title: [{ text: { content: task.name } }],
    },
  };

  // 親タスク Relation（プロパティ名が指定されかつ親ページが存在する場合のみ）
  if (parentProp && parentPageId) {
    properties[parentProp] = {
      relation: [{ id: parentPageId }],
    };
  }

  return properties;
}
