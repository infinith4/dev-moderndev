import { google } from "googleapis";

export interface WBSRow {
  大項目: string;
  中項目: string;
  小項目: string;
  [key: string]: string;
}

export type GoogleCredentials =
  | { type: "file"; path: string }
  | { type: "json"; key: object };

/**
 * Google Sheets から WBS シートを読み込む
 */
export async function readWBSSheet(
  spreadsheetId: string,
  sheetName: string,
  credentials: GoogleCredentials
): Promise<WBSRow[]> {
  const auth = new google.auth.GoogleAuth({
    ...(credentials.type === "file"
      ? { keyFile: credentials.path }
      : { credentials: credentials.key }),
    scopes: ["https://www.googleapis.com/auth/spreadsheets.readonly"],
  });

  const sheets = google.sheets({ version: "v4", auth });

  const response = await sheets.spreadsheets.values.get({
    spreadsheetId,
    range: sheetName,
  });

  const values = response.data.values;
  if (!values || values.length < 2) {
    return [];
  }

  const headers = values[0].map(String);
  const rows: WBSRow[] = [];

  for (const rawRow of values.slice(1)) {
    const obj: WBSRow = { 大項目: "", 中項目: "", 小項目: "" };
    headers.forEach((header, i) => {
      obj[header] = rawRow[i] != null ? String(rawRow[i]) : "";
    });
    // 大項目・中項目・小項目 が全て空の行はスキップ
    if (obj["大項目"] || obj["中項目"] || obj["小項目"]) {
      rows.push(obj);
    }
  }

  return rows;
}
