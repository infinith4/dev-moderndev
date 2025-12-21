"""
Google Spreadsheet Client for Project Management
"""
import os
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials


class SpreadsheetClient:
    """Google Spreadsheetからプロジェクト管理データを読み込むクライアント"""

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self, credentials_file: str, spreadsheet_id: str, sheet_name: str = "Sheet1"):
        """
        Spreadsheetクライアントを初期化

        Args:
            credentials_file: Google Cloud サービスアカウントの認証情報ファイルパス
            spreadsheet_id: SpreadsheetのID
            sheet_name: シート名（デフォルト: "Sheet1"）
        """
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.client = self._authenticate()

    def _authenticate(self) -> gspread.Client:
        """
        Google Spreadsheet APIに認証

        Returns:
            認証済みのgspreadクライアント
        """
        creds = Credentials.from_service_account_file(
            self.credentials_file,
            scopes=self.SCOPES
        )
        return gspread.authorize(creds)

    def get_worksheet(self) -> gspread.Worksheet:
        """
        ワークシートを取得

        Returns:
            gspread Worksheetオブジェクト
        """
        spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        return spreadsheet.worksheet(self.sheet_name)

    def read_tasks(self, title_prefix: str = "[工程]") -> List[Dict[str, any]]:
        """
        Spreadsheetからタスクデータを読み込む

        想定フォーマット:
        | タイトル | 進捗率 | プロジェクト | ... |
        | [工程] タスク1 | 50 | テストプロジェクト | ... |

        Args:
            title_prefix: タイトルの接頭辞でフィルタ（デフォルト: "[工程]"）

        Returns:
            タスクデータのリスト
        """
        worksheet = self.get_worksheet()
        records = worksheet.get_all_records()

        tasks = []
        for record in records:
            # タイトルが接頭辞で始まるものだけを抽出
            title = record.get("タイトル", "")
            if title.startswith(title_prefix):
                task = {
                    "title": title,
                    "progress": self._parse_progress(record.get("進捗率", 0)),
                    "project": record.get("プロジェクト", "テストプロジェクト")
                }
                tasks.append(task)

        return tasks

    def _parse_progress(self, progress_value: any) -> int:
        """
        進捗率を整数にパース

        Args:
            progress_value: 進捗率の値（文字列または数値）

        Returns:
            0-100の整数値
        """
        try:
            if isinstance(progress_value, str):
                # "%"記号を削除して数値に変換
                progress_value = progress_value.replace("%", "").strip()
            progress = int(float(progress_value))
            # 0-100の範囲に制限
            return max(0, min(100, progress))
        except (ValueError, TypeError):
            return 0

    def write_task(self, row: int, title: str, progress: int, project: str = "テストプロジェクト"):
        """
        Spreadsheetにタスクデータを書き込む

        Args:
            row: 書き込む行番号（1から開始、ヘッダー行を含む）
            title: タイトル
            progress: 進捗率
            project: プロジェクト名
        """
        worksheet = self.get_worksheet()
        worksheet.update(f"A{row}", [[title, progress, project]])

    def append_task(self, title: str, progress: int = 0, project: str = "テストプロジェクト"):
        """
        Spreadsheetの末尾にタスクを追加

        Args:
            title: タイトル
            progress: 進捗率
            project: プロジェクト名
        """
        worksheet = self.get_worksheet()
        worksheet.append_row([title, progress, project])

    def find_row_by_title(self, title: str) -> Optional[int]:
        """
        タイトルで行を検索

        Args:
            title: 検索するタイトル

        Returns:
            見つかった行番号（1から開始）、またはNone
        """
        worksheet = self.get_worksheet()
        try:
            cell = worksheet.find(title)
            return cell.row if cell else None
        except gspread.exceptions.CellNotFound:
            return None

    def update_or_append_task(self, title: str, progress: int, project: str = "テストプロジェクト"):
        """
        タスクを更新または追加（存在する場合は更新、しない場合は追加）

        Args:
            title: タイトル
            progress: 進捗率
            project: プロジェクト名
        """
        row = self.find_row_by_title(title)
        if row:
            # 既存の行を更新
            self.write_task(row, title, progress, project)
        else:
            # 新しい行を追加
            self.append_task(title, progress, project)
