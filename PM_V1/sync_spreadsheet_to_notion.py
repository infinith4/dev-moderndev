#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spreadsheet から Notion へタスクデータを同期するスクリプト

使用方法:
    python sync_spreadsheet_to_notion.py
"""
import os
import sys
import io
from dotenv import load_dotenv
from notion_api import NotionClient
from spreadsheet_client import SpreadsheetClient

# Windows環境でのUnicode出力問題を回避
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def load_config():
    """環境変数から設定を読み込む"""
    load_dotenv()

    config = {
        "notion_api_key": os.getenv("NOTION_API_KEY"),
        "notion_database_id": os.getenv("NOTION_DATABASE_ID"),
        "google_credentials_file": os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json"),
        "spreadsheet_id": os.getenv("SPREADSHEET_ID"),
        "sheet_name": os.getenv("SHEET_NAME", "Sheet1"),
    }

    # 必須設定の確認
    required_keys = ["notion_api_key", "notion_database_id", "spreadsheet_id"]
    missing_keys = [key for key in required_keys if not config[key]]

    if missing_keys:
        print(f"エラー: 以下の環境変数が設定されていません: {', '.join(missing_keys)}")
        print("\n.env ファイルを作成し、以下の環境変数を設定してください:")
        print("  NOTION_API_KEY=your_notion_api_key")
        print("  NOTION_DATABASE_ID=your_database_id")
        print("  SPREADSHEET_ID=your_spreadsheet_id")
        print("  GOOGLE_CREDENTIALS_FILE=credentials.json (オプション)")
        print("  SHEET_NAME=Sheet1 (オプション)")
        sys.exit(1)

    return config


def sync_tasks(config: dict, title_prefix: str = "[工程]", project_name: str = "テストプロジェクト"):
    """
    SpreadsheetからNotionへタスクを同期

    Args:
        config: 設定辞書
        title_prefix: タイトルの接頭辞
        project_name: プロジェクト名
    """
    print("=== Spreadsheet から Notion へタスクを同期 ===\n")

    # クライアントを初期化
    print("1. クライアントを初期化中...")
    try:
        spreadsheet_client = SpreadsheetClient(
            config["google_credentials_file"],
            config["spreadsheet_id"],
            config["sheet_name"]
        )
        print("   ✓ Spreadsheet クライアント初期化完了")

        notion_client = NotionClient(
            config["notion_api_key"],
            config["notion_database_id"]
        )
        print("   ✓ Notion クライアント初期化完了\n")
    except Exception as e:
        print(f"   ✗ エラー: クライアント初期化に失敗しました: {e}")
        sys.exit(1)

    # Spreadsheetからタスクを読み込む
    print("2. Spreadsheet からタスクを読み込み中...")
    try:
        tasks = spreadsheet_client.read_tasks(title_prefix)
        print(f"   ✓ {len(tasks)} 件のタスクを読み込みました\n")

        if not tasks:
            print("同期するタスクがありません。")
            return

        # タスクの一覧を表示
        print("読み込んだタスク:")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task['title']} (進捗: {task['progress']}%, プロジェクト: {task['project']})")
        print()

    except Exception as e:
        print(f"   ✗ エラー: タスク読み込みに失敗しました: {e}")
        sys.exit(1)

    # Notionへタスクを同期
    print("3. Notion へタスクを同期中...")
    success_count = 0
    error_count = 0

    for task in tasks:
        try:
            response = notion_client.upsert_page(
                title=task["title"],
                progress=task["progress"],
                project_name=task.get("project", project_name),
                title_prefix=title_prefix
            )

            page_id = response["id"]
            print(f"   ✓ {task['title']} (Page ID: {page_id[:8]}...)")
            success_count += 1

        except Exception as e:
            print(f"   ✗ {task['title']} - エラー: {e}")
            error_count += 1

    # 結果サマリー
    print(f"\n=== 同期完了 ===")
    print(f"成功: {success_count} 件")
    if error_count > 0:
        print(f"失敗: {error_count} 件")


def main():
    """メイン関数"""
    # 設定を読み込む
    config = load_config()

    # タスクを同期
    sync_tasks(config)


if __name__ == "__main__":
    main()
