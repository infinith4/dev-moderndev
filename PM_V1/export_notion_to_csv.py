#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion からデータをCSV（タブ区切り）形式で出力するスクリプト

使用方法:
    python export_notion_to_csv.py
    python export_notion_to_csv.py --output custom_output.tsv
    python export_notion_to_csv.py --project "別のプロジェクト"
"""
import os
import sys
import csv
import argparse
from dotenv import load_dotenv
from notion_api import NotionClient


def export_to_csv(output_file: str = "notion_export.tsv",
                  title_prefix: str = "[工程]",
                  project_name: str = "テストプロジェクト"):
    """
    NotionデータをCSV（タブ区切り）形式で出力

    Args:
        output_file: 出力ファイル名
        title_prefix: タイトルの接頭辞でフィルタ
        project_name: プロジェクト名でフィルタ
    """
    # 設定を読み込む
    load_dotenv()

    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_database_id = os.getenv("NOTION_DATABASE_ID")

    if not notion_api_key or not notion_database_id:
        print("エラー: NOTION_API_KEY と NOTION_DATABASE_ID を .env ファイルに設定してください")
        sys.exit(1)

    # Notionクライアントを初期化
    notion_client = NotionClient(notion_api_key, notion_database_id)

    # Notionからタスクを取得
    print(f"Notionからデータを取得中...")
    print(f"  プロジェクト: {project_name}")
    print(f"  接頭辞: {title_prefix}")

    pages = notion_client.get_pages_by_project(project_name, title_prefix)
    print(f"\n✓ {len(pages)} 件のページを取得しました\n")

    if not pages:
        print("出力するデータがありません")
        return

    # CSVファイルに出力（タブ区切り）
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')

        # ヘッダー行
        writer.writerow(['SortId', 'タイトル', '進捗率', 'プロジェクト'])

        # データ行
        for page in pages:
            title = notion_client._get_page_title(page)
            sort_id = notion_client._get_sort_id(page)

            # 進捗率を取得
            progress = 0
            if "進捗率" in page["properties"]:
                progress_prop = page["properties"]["進捗率"]
                if progress_prop["type"] == "number" and progress_prop["number"] is not None:
                    progress = int(progress_prop["number"])

            # プロジェクト名を取得
            project = project_name
            if "プロジェクト" in page["properties"]:
                project_prop = page["properties"]["プロジェクト"]
                if project_prop["type"] == "select" and project_prop["select"]:
                    project = project_prop["select"]["name"]

            writer.writerow([sort_id, title, progress, project])
            print(f"  [{sort_id}] {title} (進捗: {progress}%, プロジェクト: {project})")

    print(f"\n✓ {output_file} に出力しました")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="NotionデータをCSV（タブ区切り）形式で出力"
    )
    parser.add_argument(
        "--output", "-o",
        default="notion_export.tsv",
        help="出力ファイル名（デフォルト: notion_export.tsv）"
    )
    parser.add_argument(
        "--prefix",
        default="[工程]",
        help="タイトルの接頭辞でフィルタ（デフォルト: [工程]）"
    )
    parser.add_argument(
        "--project",
        default="テストプロジェクト",
        help="プロジェクト名でフィルタ（デフォルト: テストプロジェクト）"
    )

    args = parser.parse_args()

    export_to_csv(
        output_file=args.output,
        title_prefix=args.prefix,
        project_name=args.project
    )


if __name__ == "__main__":
    main()
