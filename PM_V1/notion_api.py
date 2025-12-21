"""
Notion API Client for Project Management
"""
import os
from typing import List, Dict, Optional
from notion_client import Client


class NotionClient:
    """Notion APIを使ってプロジェクト管理データベースを操作するクライアント"""

    def __init__(self, api_key: str, database_id: str):
        """
        Notion クライアントを初期化

        Args:
            api_key: Notion API キー
            database_id: Notion データベース ID
        """
        self.client = Client(auth=api_key)
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
        response = self.client.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Name",
                "title": {
                    "contains": title_prefix
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
        プロジェクト名でページを取得

        Args:
            project_name: プロジェクト名（例: "テストプロジェクト"）
            title_prefix: タイトルの接頭辞（デフォルト: "[工程]"）

        Returns:
            該当するページのリスト
        """
        # データベースをクエリ
        response = self.client.databases.query(
            database_id=self.database_id,
            filter={
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
        )

        return response["results"]

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
