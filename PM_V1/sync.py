#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion と Spreadsheet を双方向同期するメインスクリプト

使用方法:
    # Spreadsheet → Notion へ同期
    python sync.py --mode sheet-to-notion

    # Notion → Spreadsheet へ同期
    python sync.py --mode notion-to-sheet

    # オプション指定
    python sync.py --mode sheet-to-notion --prefix "[工程]" --project "テストプロジェクト"
"""
import argparse
import sys
import io

# Windows環境でのUnicode出力問題を回避
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sync_spreadsheet_to_notion import sync_tasks as sync_sheet_to_notion, load_config
from sync_notion_to_spreadsheet import sync_tasks as sync_notion_to_sheet


def parse_args():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(
        description="Notion と Spreadsheet を双方向同期",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # Spreadsheet → Notion
  python sync.py --mode sheet-to-notion

  # Notion → Spreadsheet
  python sync.py --mode notion-to-sheet

  # プロジェクト名と接頭辞を指定
  python sync.py --mode sheet-to-notion --prefix "[工程]" --project "MyProject"
        """
    )

    parser.add_argument(
        "--mode",
        choices=["sheet-to-notion", "notion-to-sheet"],
        required=True,
        help="同期モード: sheet-to-notion (Spreadsheet→Notion) または notion-to-sheet (Notion→Spreadsheet)"
    )

    parser.add_argument(
        "--prefix",
        default="[工程]",
        help="タイトルの接頭辞 (デフォルト: [工程])"
    )

    parser.add_argument(
        "--project",
        default="テストプロジェクト",
        help="プロジェクト名 (デフォルト: テストプロジェクト)"
    )

    return parser.parse_args()


def main():
    """メイン関数"""
    args = parse_args()

    # 設定を読み込む
    config = load_config()

    # モードに応じて同期を実行
    if args.mode == "sheet-to-notion":
        print(f"モード: Spreadsheet → Notion")
        print(f"接頭辞: {args.prefix}")
        print(f"プロジェクト: {args.project}\n")
        sync_sheet_to_notion(
            config,
            title_prefix=args.prefix,
            project_name=args.project
        )
    elif args.mode == "notion-to-sheet":
        print(f"モード: Notion → Spreadsheet")
        print(f"接頭辞: {args.prefix}")
        print(f"プロジェクト: {args.project}\n")
        sync_notion_to_sheet(
            config,
            title_prefix=args.prefix,
            project_name=args.project
        )
    else:
        print(f"エラー: 不正なモード '{args.mode}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
