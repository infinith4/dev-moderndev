import dotenv from "dotenv";
import express from "express";
import { createNotionClient, getPagesByDatabaseId, type PaginatedResult } from "./notionClient";

dotenv.config();

const app = express();
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

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log(
    `GET /api/databases/:databaseId/pages - Fetch pages by database ID`
  );
});
