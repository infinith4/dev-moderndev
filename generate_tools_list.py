#!/usr/bin/env python3
"""
ツール一覧生成スクリプト

docs/ツール フォルダ配下のすべてのツールを走査し、
カテゴリ別の一覧をMarkdownファイルとして生成します。
"""

import os
from pathlib import Path
from typing import Dict, List
import re


def extract_title_from_markdown(file_path: Path) -> str:
    """
    Markdownファイルから最初のH1見出しを抽出する

    Args:
        file_path: Markdownファイルのパス

    Returns:
        抽出したタイトル、見つからない場合はファイル名（拡張子なし）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # H1見出し（# で始まる行）を探す
                if line.startswith('# '):
                    return line[2:].strip()
        # 見出しが見つからない場合はファイル名を使用
        return file_path.stem
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return file_path.stem


def extract_overview_from_markdown(file_path: Path) -> str:
    """
    Markdownファイルから概要セクションを抽出する

    Args:
        file_path: Markdownファイルのパス

    Returns:
        概要テキスト、見つからない場合は空文字列
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_overview = False
        overview_lines = []

        for line in lines:
            stripped = line.strip()

            # 概要セクションの開始
            if stripped in ['## 概要', '## Overview']:
                in_overview = True
                continue

            # 次のセクションに到達したら終了
            if in_overview and stripped.startswith('## '):
                break

            # 概要セクション内のテキストを収集
            if in_overview and stripped:
                overview_lines.append(stripped)

        # 最初の段落のみを返す（最大2文）
        if overview_lines:
            text = ' '.join(overview_lines)
            # 最大200文字に制限
            if len(text) > 200:
                text = text[:200] + '...'
            return text

        return ""
    except Exception as e:
        print(f"Warning: Could not extract overview from {file_path}: {e}")
        return ""


def scan_tools_directory(base_path: Path) -> Dict[str, List[Dict[str, str]]]:
    """
    ツールディレクトリを走査し、カテゴリ別にツールを収集する

    Args:
        base_path: docs/ツール ディレクトリのパス

    Returns:
        カテゴリ名をキーとし、ツール情報のリストを値とする辞書
    """
    tools_by_category = {}

    # ツールディレクトリ内のすべてのサブディレクトリを走査
    for category_dir in sorted(base_path.iterdir()):
        if not category_dir.is_dir():
            continue

        category_name = category_dir.name
        tools = []

        # カテゴリディレクトリ内のMarkdownファイルを収集
        md_files = sorted(category_dir.glob('*.md'))

        for md_file in md_files:
            title = extract_title_from_markdown(md_file)
            overview = extract_overview_from_markdown(md_file)
            relative_path = md_file.relative_to(base_path)

            tools.append({
                'title': title,
                'overview': overview,
                'file': md_file.name,
                'path': str(relative_path)
            })

        if tools:
            tools_by_category[category_name] = tools

    return tools_by_category


def generate_markdown(tools_by_category: Dict[str, List[Dict[str, str]]]) -> str:
    """
    ツール一覧のMarkdownを生成する

    Args:
        tools_by_category: カテゴリ別のツール情報

    Returns:
        生成されたMarkdown文字列
    """
    lines = []

    # ヘッダー
    lines.append('# ツール一覧')
    lines.append('')
    lines.append('このドキュメントは、docs/ツール フォルダ配下に存在するすべてのツールの一覧です。')
    lines.append('')

    # 統計情報
    total_categories = len(tools_by_category)
    total_tools = sum(len(tools) for tools in tools_by_category.values())
    lines.append('## 統計')
    lines.append('')
    lines.append(f'- **カテゴリ数**: {total_categories}')
    lines.append(f'- **ツール総数**: {total_tools}')
    lines.append('')

    # 目次
    lines.append('## 目次')
    lines.append('')
    for category_name in sorted(tools_by_category.keys()):
        tool_count = len(tools_by_category[category_name])
        # カテゴリ名をアンカーリンク用に変換
        anchor = category_name.lower().replace(' ', '-').replace('_', '-')
        lines.append(f'- [{category_name}](#{anchor}) ({tool_count}ツール)')
    lines.append('')

    # カテゴリ別のツール一覧
    for category_name in sorted(tools_by_category.keys()):
        tools = tools_by_category[category_name]

        lines.append(f'## {category_name}')
        lines.append('')
        lines.append(f'**ツール数**: {len(tools)}')
        lines.append('')

        # テーブル形式で出力
        lines.append('| ツール名 | 概要 | ファイル |')
        lines.append('|----------|------|----------|')

        for tool in tools:
            title = tool['title']
            overview = tool['overview'] if tool['overview'] else '(概要なし)'
            file_link = f"[{tool['file']}]({tool['path']})"

            # テーブル内の特殊文字をエスケープ
            overview = overview.replace('|', '\\|').replace('\n', ' ')

            lines.append(f'| {title} | {overview} | {file_link} |')

        lines.append('')

    # フッター
    lines.append('---')
    lines.append('')
    lines.append('> このドキュメントは自動生成されています。')
    lines.append('> 再生成するには、`python3 generate_tools_list.py` を実行してください。')
    lines.append('')

    return '\n'.join(lines)


def main():
    """
    メイン処理
    """
    # ベースパスの設定
    script_dir = Path(__file__).parent
    tools_dir = script_dir / 'docs' / 'ツール'
    output_file = tools_dir / 'ツール一覧.md'

    # ツールディレクトリの存在確認
    if not tools_dir.exists():
        print(f"Error: Tools directory not found: {tools_dir}")
        return 1

    print(f"Scanning tools directory: {tools_dir}")

    # ツールの収集
    tools_by_category = scan_tools_directory(tools_dir)

    if not tools_by_category:
        print("Warning: No tools found")
        return 1

    print(f"Found {len(tools_by_category)} categories")

    # Markdownの生成
    markdown_content = generate_markdown(tools_by_category)

    # ファイルへの書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Generated: {output_file}")
    print(f"Total categories: {len(tools_by_category)}")
    print(f"Total tools: {sum(len(tools) for tools in tools_by_category.values())}")

    return 0


if __name__ == '__main__':
    exit(main())
