"""
Notion API Client for Project Management

Web API使用方法:
    uvicorn notion_api:app --reload --port 8000

エンドポイント:
    GET /projects/{project_name}/pages - 特定プロジェクトのページを取得
    GET /projects/{project_name}/pages?prefix=[工程] - 接頭辞フィルタ付き
"""
import os
import sys
import io
from typing import List, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from notion_client import Client

# Windows環境でのUnicode出力問題を回避
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class NotionClient:
    """Notion APIを使ってプロジェクト管理データベースを操作するクライアント"""

    def __init__(self, api_key: str, database_id: str):
        """
        Notion クライアントを初期化

        Args:
            api_key: Notion API キー
            database_id: Notion データベース ID
        """
        self.client = Client(auth=api_key, notion_version="2022-06-28")
        # データベースIDはダッシュ付きで保存
        self.database_id = database_id

    def create_page(self, title: str, progress: int = 0, properties: Optional[Dict] = None) -> Dict:
        """
        Notionデータベースに新しいページを作成

        Args:
            title: ページタイトル（例: "[工程] タスク名"）
            progress: 進捗率 (0-100)
            properties: 追加のプロパティ

        Returns:
            作成されたページのレスポンス
        """
        page_properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }

        # 進捗率プロパティが存在する場合
        if properties and "進捗率" in properties:
            page_properties["進捗率"] = {
                "number": progress
            }

        # 追加プロパティをマージ
        if properties:
            for key, value in properties.items():
                if key not in page_properties and key != "進捗率":
                    page_properties[key] = value

        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=page_properties
        )

        return response

    def update_page(self, page_id: str, title: Optional[str] = None,
                   progress: Optional[int] = None, properties: Optional[Dict] = None) -> Dict:
        """
        Notionページを更新

        Args:
            page_id: 更新するページのID
            title: 新しいタイトル（省略可）
            progress: 新しい進捗率（省略可）
            properties: 追加のプロパティ

        Returns:
            更新されたページのレスポンス
        """
        page_properties = {}

        if title:
            page_properties["Name"] = {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }

        if progress is not None:
            page_properties["進捗率"] = {
                "number": progress
            }

        if properties:
            for key, value in properties.items():
                if key not in page_properties:
                    page_properties[key] = value

        response = self.client.pages.update(
            page_id=page_id,
            properties=page_properties
        )

        return response

    def find_page_by_title(self, title: str, title_prefix: str = "[工程]") -> Optional[Dict]:
        """
        タイトルでページを検索

        Args:
            title: 検索するタイトル
            title_prefix: タイトルの接頭辞（デフォルト: "[工程]"）

        Returns:
            見つかったページ、または None
        """
        # データベースをクエリ
        response = self.client.request(
            path=f"databases/{self.database_id}/query",
            method="POST",
            body={
                "filter": {
                    "property": "Name",
                    "title": {
                        "contains": title_prefix
                    }
                }
            }
        )

        # タイトルが完全一致するページを検索
        for page in response["results"]:
            page_title = self._get_page_title(page)
            if page_title == title:
                return page

        return None

    def get_pages_by_project(self, project_name: str, title_prefix: str = "[工程]") -> List[Dict]:
        """
        プロジェクト名でページを取得（SortIdでソート）

        Args:
            project_name: プロジェクト名（例: "テストプロジェクト"）
            title_prefix: タイトルの接頭辞（デフォルト: "[工程]"）

        Returns:
            該当するページのリスト（SortIdでソート済み）
        """
        # データベースをクエリ
        response = self.client.request(
            path=f"databases/{self.database_id}/query",
            method="POST",
            body={
                "filter": {
                    "and": [
                        {
                            "property": "Name",
                            "title": {
                                "contains": title_prefix
                            }
                        },
                        {
                            "property": "プロジェクト",
                            "select": {
                                "equals": project_name
                            }
                        }
                    ]
                }
            }
        )

        # SortIdでソート
        pages = response["results"]
        pages.sort(key=lambda page: self._get_sort_id(page))

        return pages

    def _get_page_title(self, page: Dict) -> str:
        """
        ページからタイトルを取得

        Args:
            page: Notionページオブジェクト

        Returns:
            ページタイトル
        """
        try:
            return page["properties"]["Name"]["title"][0]["text"]["content"]
        except (KeyError, IndexError):
            return ""

    def _get_sort_id(self, page: Dict) -> str:
        """
        ページからSortIdを取得

        Args:
            page: Notionページオブジェクト

        Returns:
            SortId（存在しない場合は空文字列）
        """
        try:
            sort_prop = page["properties"].get("SortId", {})
            if sort_prop.get("rich_text"):
                return sort_prop["rich_text"][0]["text"]["content"]
            return ""
        except (KeyError, IndexError):
            return ""

    def upsert_page(self, title: str, progress: int = 0,
                   project_name: str = "テストプロジェクト",
                   title_prefix: str = "[工程]") -> Dict:
        """
        ページを作成または更新（存在する場合は更新、しない場合は作成）

        Args:
            title: ページタイトル
            progress: 進捗率
            project_name: プロジェクト名
            title_prefix: タイトルの接頭辞

        Returns:
            作成または更新されたページのレスポンス
        """
        existing_page = self.find_page_by_title(title, title_prefix)

        if existing_page:
            # ページが存在する場合は更新
            page_id = existing_page["id"]
            return self.update_page(page_id, progress=progress)
        else:
            # ページが存在しない場合は作成
            properties = {
                "プロジェクト": {
                    "select": {
                        "name": project_name
                    }
                },
                "進捗率": {
                    "number": progress
                }
            }
            return self.create_page(title, progress, properties)


# --- FastAPI Web API ---

load_dotenv()

app = FastAPI(title="Notion Project API", version="1.0.0")


def _get_client() -> NotionClient:
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not api_key or not database_id:
        raise HTTPException(
            status_code=500,
            detail="NOTION_API_KEY and NOTION_DATABASE_ID must be set in .env",
        )
    return NotionClient(api_key=api_key, database_id=database_id)


def _format_page(page: Dict, client: NotionClient) -> Dict:
    """Notionページオブジェクトからレスポンス用の辞書を生成"""
    title = client._get_page_title(page)
    sort_id = client._get_sort_id(page)

    progress = None
    progress_prop = page.get("properties", {}).get("進捗率", {})
    if progress_prop.get("number") is not None:
        progress = progress_prop["number"]

    project = None
    project_prop = page.get("properties", {}).get("プロジェクト", {})
    if project_prop.get("select"):
        project = project_prop["select"].get("name")

    return {
        "id": page["id"],
        "title": title,
        "sort_id": sort_id,
        "progress": progress,
        "project": project,
        "url": page.get("url"),
        "created_time": page.get("created_time"),
        "last_edited_time": page.get("last_edited_time"),
    }


@app.get("/projects/{project_name}/pages")
def get_project_pages(
    project_name: str,
    prefix: str = Query(default="[工程]", description="タイトルの接頭辞フィルタ"),
):
    """特定プロジェクトのページ一覧を取得（SortIdでソート済み）"""
    client = _get_client()
    pages = client.get_pages_by_project(project_name, title_prefix=prefix)
    return {
        "project": project_name,
        "prefix": prefix,
        "count": len(pages),
        "pages": [_format_page(p, client) for p in pages],
    }
