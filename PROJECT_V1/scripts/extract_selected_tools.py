#!/usr/bin/env python3
"""
選択済みツール抽出スクリプト

Markdownファイルからチェック済み [x] のツールを抽出します。

使い方:
    python extract_selected_tools.py <input_file>
    python extract_selected_tools.py ../プロジェクトツール選択.md
"""

import re
import sys
from pathlib import Path
from typing import List, Dict


def extract_checked_tools(markdown_file: Path) -> List[Dict[str, str]]:
    """
    Markdownファイルからチェック済みツールを抽出

    Args:
        markdown_file: Markdownファイルのパス

    Returns:
        チェック済みツールのリスト
    """
    if not markdown_file.exists():
        print(f"❌ ファイルが見つかりません: {markdown_file}")
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    selected_tools = []
    current_phase = None
    current_category = None

    # 開発工程を抽出
    phase_pattern = r'^## (\d+️⃣|🔟|1️⃣\d+️⃣) (.+)$'
    # カテゴリを抽出
    category_pattern = r'^### (.+)$'
    # チェック済みツールを抽出
    checked_pattern = r'^- \[x\] \*\*(.+?)\*\* - (.+?)$'
    # 料金情報を抽出
    pricing_pattern = r'  - 💰 料金: (🟢|🟡|🔴) (.+)$'
    # 詳細リンクを抽出
    link_pattern = r'  - 📄 詳細: \[.+?\]\((.+?)\)$'
    # 選択理由を抽出
    reason_pattern = r'  - 📝 選択理由: (.+)$'

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # 開発工程の検出
        phase_match = re.match(phase_pattern, line)
        if phase_match:
            current_phase = phase_match.group(2)
            i += 1
            continue

        # カテゴリの検出
        category_match = re.match(category_pattern, line)
        if category_match:
            current_category = category_match.group(1)
            i += 1
            continue

        # チェック済みツールの検出
        checked_match = re.match(checked_pattern, line)
        if checked_match:
            tool_name = checked_match.group(1)
            description = checked_match.group(2)

            # ツール情報を初期化
            tool_info = {
                'name': tool_name,
                'description': description,
                'phase': current_phase,
                'category': current_category,
                'pricing': '',
                'link': '',
                'reason': ''
            }

            # 次の行から詳細情報を抽出
            j = i + 1
            while j < len(lines) and lines[j].startswith('  - '):
                detail_line = lines[j]

                # 料金情報
                pricing_match = re.match(pricing_pattern, detail_line)
                if pricing_match:
                    tool_info['pricing'] = f"{pricing_match.group(1)} {pricing_match.group(2)}"

                # 詳細リンク
                link_match = re.match(link_pattern, detail_line)
                if link_match:
                    tool_info['link'] = link_match.group(1)

                # 選択理由
                reason_match = re.match(reason_pattern, detail_line)
                if reason_match:
                    reason = reason_match.group(1)
                    if reason and reason != '___________':
                        tool_info['reason'] = reason

                j += 1

            selected_tools.append(tool_info)

        i += 1

    return selected_tools


def print_summary(tools: List[Dict[str, str]]):
    """
    選択済みツールのサマリーを表示

    Args:
        tools: ツールのリスト
    """
    print(f"\n{'='*80}")
    print(f"📊 選択済みツール集計")
    print(f"{'='*80}\n")

    print(f"✅ 総ツール数: {len(tools)}\n")

    # 開発工程別集計
    phase_count = {}
    for tool in tools:
        phase = tool['phase']
        if phase:
            phase_count[phase] = phase_count.get(phase, 0) + 1

    print("📋 開発工程別:")
    for phase, count in sorted(phase_count.items()):
        print(f"  - {phase}: {count}ツール")

    # 料金別集計
    pricing_count = {'🟢': 0, '🟡': 0, '🔴': 0}
    for tool in tools:
        if tool['pricing']:
            emoji = tool['pricing'][0]
            if emoji in pricing_count:
                pricing_count[emoji] += 1

    print(f"\n💰 料金別:")
    print(f"  - 🟢 無料: {pricing_count['🟢']}ツール")
    print(f"  - 🟡 一部無料: {pricing_count['🟡']}ツール")
    print(f"  - 🔴 有料: {pricing_count['🔴']}ツール")

    print(f"\n{'='*80}\n")


def print_tool_list(tools: List[Dict[str, str]]):
    """
    選択済みツールのリストを表示

    Args:
        tools: ツールのリスト
    """
    print(f"{'='*80}")
    print(f"📝 選択済みツール一覧")
    print(f"{'='*80}\n")

    current_phase = None

    for tool in tools:
        # 開発工程が変わったら表示
        if tool['phase'] != current_phase:
            current_phase = tool['phase']
            print(f"\n## {current_phase}\n")

        print(f"### {tool['name']}")
        print(f"- **説明**: {tool['description']}")
        print(f"- **カテゴリ**: {tool['category']}")
        if tool['pricing']:
            print(f"- **料金**: {tool['pricing']}")
        if tool['link']:
            print(f"- **詳細**: {tool['link']}")
        if tool['reason']:
            print(f"- **選択理由**: {tool['reason']}")
        print()


def save_to_file(tools: List[Dict[str, str]], output_file: Path):
    """
    選択済みツールをMarkdownファイルに保存

    Args:
        tools: ツールのリスト
        output_file: 出力ファイルのパス
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 選択済みツール一覧\n\n")
        f.write(f"**生成日**: {Path(__file__).stat().st_mtime}\n")
        f.write(f"**総ツール数**: {len(tools)}\n\n")
        f.write("---\n\n")

        current_phase = None

        for tool in tools:
            # 開発工程が変わったら表示
            if tool['phase'] != current_phase:
                current_phase = tool['phase']
                f.write(f"\n## {current_phase}\n\n")

            f.write(f"### {tool['name']}\n\n")
            f.write(f"- **説明**: {tool['description']}\n")
            f.write(f"- **カテゴリ**: {tool['category']}\n")
            if tool['pricing']:
                f.write(f"- **料金**: {tool['pricing']}\n")
            if tool['link']:
                f.write(f"- **詳細**: [{tool['name']}]({tool['link']})\n")
            if tool['reason']:
                f.write(f"- **選択理由**: {tool['reason']}\n")
            f.write("\n")

    print(f"✅ 選択済みツール一覧を保存しました: {output_file}")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使い方: python extract_selected_tools.py <input_file>")
        print("例: python extract_selected_tools.py ../プロジェクトツール選択.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    print(f"🔍 チェック済みツールを抽出中: {input_file}")

    # チェック済みツールを抽出
    tools = extract_checked_tools(input_file)

    if not tools:
        print("⚠️ チェック済み [x] のツールが見つかりませんでした。")
        print("   プロジェクトツール選択.mdでツールを選択してください。")
        sys.exit(0)

    # サマリー表示
    print_summary(tools)

    # ツールリスト表示
    print_tool_list(tools)

    # ファイルに保存
    output_file = input_file.parent / "選択済みツール一覧.md"
    save_to_file(tools, output_file)


if __name__ == "__main__":
    main()
