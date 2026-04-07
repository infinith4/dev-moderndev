import dotenv from "dotenv";
import express from "express";
import { createNotionClient, getPagesByDatabaseId, type PaginatedResult } from "./notionClient";
import { readWBSSheet, type GoogleCredentials } from "./googleSheetsClient";
import { parseWBS, createNotionTasks } from "./wbsImporter";

dotenv.config();

const app = express();
app.use(express.json());
const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;

const apiKey = process.env.NOTION_API_KEY;
if (!apiKey) {
  console.error("NOTION_API_KEY is not set in environment variables");
  process.exit(1);
}

const notion = createNotionClient(apiKey);

app.get("/api/databases/:databaseId/pages", async (req, res) => {
  try {
    const { databaseId } = req.params;
    const prefix = req.query.prefix as string | undefined;
    const page = Math.max(1, parseInt(req.query.page as string, 10) || 1);
    const pageSize = Math.max(1, Math.min(100, parseInt(req.query.pageSize as string, 10) || 20));

    let allPages = await getPagesByDatabaseId(notion, databaseId);
    if (prefix) {
      allPages = allPages.filter((p) => p.title.startsWith(prefix));
    }

    const total = allPages.length;
    const totalPages = Math.ceil(total / pageSize);
    const start = (page - 1) * pageSize;
    const paginated = allPages.slice(start, start + pageSize);

    const result: PaginatedResult = {
      total,
      page,
      pageSize,
      totalPages,
      pages: paginated,
    };
    res.json({ databaseId, ...result });
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : "Unknown error occurred";
    console.error("Error fetching pages:", message);
    res.status(500).json({ error: message });
  }
});

/**
 * WBS スプレッドシートからタスクを一括作成する
 *
 * POST /api/tasks/import-wbs
 * Body (JSON):
 *   spreadsheetId       - Google Spreadsheet ID（省略時: env SPREADSHEET_ID）
 *   sheetName           - シート名（省略時: "wbs"）
 *   databaseId          - Notion データベース ID（省略時: env NOTION_DATABASE_ID）
 *   parentRelationProp  - 親タスク Relation プロパティ名（省略時: "親タスク"）
 *   dryRun              - true の場合タスクを作成せず解析結果のみ返す（デフォルト: false）
 */
app.post("/api/tasks/import-wbs", async (req, res) => {
  try {
    const {
      spreadsheetId = process.env.SPREADSHEET_ID,
      sheetName = "wbs",
      databaseId = process.env.NOTION_DATABASE_ID,
      parentRelationProp = "親タスク",
      dryRun = false,
    } = req.body as {
      spreadsheetId?: string;
      sheetName?: string;
      databaseId?: string;
      parentRelationProp?: string;
      dryRun?: boolean;
    };

    if (!spreadsheetId) {
      res.status(400).json({ error: "spreadsheetId is required (or set SPREADSHEET_ID env)" });
      return;
    }
    if (!databaseId) {
      res.status(400).json({ error: "databaseId is required (or set NOTION_DATABASE_ID env)" });
      return;
    }

    // Google 認証情報の解決
    const credentials = resolveGoogleCredentials();

    // 1. スプレッドシートから WBS データを読み込む
    const rows = await readWBSSheet(spreadsheetId, sheetName, credentials);

    // 2. 大項目→中項目→小項目 の階層ツリーに変換
    const tasks = parseWBS(rows);

    if (dryRun) {
      res.json({
        dryRun: true,
        spreadsheetId,
        sheetName,
        rowCount: rows.length,
        tasks,
      });
      return;
    }

    // 3. Notion にタスクを作成
    const result = await createNotionTasks(notion, databaseId, tasks, parentRelationProp);

    res.json({
      spreadsheetId,
      sheetName,
      databaseId,
      created: result.created,
      tasks: result.tasks,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Unknown error occurred";
    console.error("Error importing WBS:", message);
    res.status(500).json({ error: message });
  }
});

/** Google 認証情報を環境変数から解決する */
function resolveGoogleCredentials(): GoogleCredentials {
  const keyFile = process.env.GOOGLE_SERVICE_ACCOUNT_KEY_FILE;
  if (keyFile) {
    return { type: "file", path: keyFile };
  }

  const keyJson = process.env.GOOGLE_SERVICE_ACCOUNT_KEY;
  if (keyJson) {
    return { type: "json", key: JSON.parse(keyJson) };
  }

  throw new Error(
    "Google credentials not configured. Set GOOGLE_SERVICE_ACCOUNT_KEY_FILE or GOOGLE_SERVICE_ACCOUNT_KEY env variable."
  );
}

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log(
    `GET /api/databases/:databaseId/pages - Fetch pages by database ID`
  );
});
