import { Client } from "@notionhq/client";
import type { PageObjectResponse } from "@notionhq/client/build/src/api-endpoints/common";
import type { QueryDataSourceResponse } from "@notionhq/client/build/src/api-endpoints/data-sources";

export interface PageEntry {
  pageId: string;
  title: string;
}

export interface PaginatedResult {
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  pages: PageEntry[];
}

export function createNotionClient(apiKey: string): Client {
  return new Client({ auth: apiKey });
}

function extractTitleAndPrefix(page: PageObjectResponse): PageEntry {
  const titleProp = Object.values(page.properties).find(
    (prop) => prop.type === "title"
  );

  let title = "";
  if (titleProp && titleProp.type === "title") {
    title = titleProp.title.map((t) => t.plain_text).join("");
  }

  const match = title.match(/^(\[?[A-Za-z0-9_-]+[\]:]?\s*)/);

  return {
    pageId: page.id,
    title,
  };
}

async function getDataSourceId(
  client: Client,
  databaseId: string
): Promise<string> {
  const db = await client.databases.retrieve({ database_id: databaseId });
  if (!("data_sources" in db) || !db.data_sources?.length) {
    throw new Error(`No data sources found for database: ${databaseId}`);
  }
  return db.data_sources[0].id;
}

export async function getPagesByDatabaseId(
  client: Client,
  databaseId: string
): Promise<PageEntry[]> {
  const dataSourceId = await getDataSourceId(client, databaseId);
  const pages: PageEntry[] = [];
  let cursor: string | undefined = undefined;

  do {
    const response: QueryDataSourceResponse = await client.dataSources.query({
      data_source_id: dataSourceId,
      start_cursor: cursor,
      page_size: 100,
    });

    for (const page of response.results) {
      if ("properties" in page) {
        pages.push(extractTitleAndPrefix(page as PageObjectResponse));
      }
    }

    cursor = response.has_more ? (response.next_cursor ?? undefined) : undefined;
  } while (cursor);

  return pages;
}
