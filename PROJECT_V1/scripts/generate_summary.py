#!/usr/bin/env python3
"""
選択済みツール要約生成スクリプト

選択済みツールから簡潔な要約を生成します。

使い方:
    python generate_summary.py <input_file> [output_file]
    python generate_summary.py ../プロジェクトツール選択.md
    python generate_summary.py ../プロジェクトツール選択.md ../要約.md
"""

import re
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def extract_project_info(content: str) -> Dict[str, str]:
    """
    プロジェクト情報を抽出

    Args:
        content: Markdownファイルの内容

    Returns:
        プロジェクト情報
    """
    info = {
        'project_name': '',
        'created_date': '',
        'updated_date': '',
        'author': ''
    }

    # プロジェクト名
    project_pattern = r'\*\*プロジェクト名\*\*: (.+)'
    match = re.search(project_pattern, content)
    if match:
        info['project_name'] = match.group(1).strip('_').strip()

    # 作成日
    created_pattern = r'\*\*作成日\*\*: (.+)'
    match = re.search(created_pattern, content)
    if match:
        info['created_date'] = match.group(1)

    # 最終更新
    updated_pattern = r'\*\*最終更新\*\*: (.+)'
    match = re.search(updated_pattern, content)
    if match:
        info['updated_date'] = match.group(1).strip('_').strip()

    # 作成者
    author_pattern = r'\*\*作成者\*\*: (.+)'
    match = re.search(author_pattern, content)
    if match:
        info['author'] = match.group(1).strip('_').strip()

    return info


def extract_selected_tools(markdown_file: Path) -> List[Dict[str, str]]:
    """
    選択済みツールを抽出

    Args:
        markdown_file: Markdownファイルのパス

    Returns:
        選択済みツールのリスト
    """
    if not markdown_file.exists():
        print(f"❌ ファイルが見つかりません: {markdown_file}")
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    selected_tools = []
    current_phase = None
    current_category = None

    # チェック済みツールを抽出
    checked_pattern = r'^- \[x\] \*\*(.+?)\*\* - (.+?)$'
    pricing_pattern = r'  - 💰 料金: (🟢|🟡|🔴) (.+)$'
    reason_pattern = r'  - 📝 選択理由: (.+)$'

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # 開発工程の検出
        if line.startswith('## '):
            current_phase = re.sub(r'^## (\d+️⃣|🔟|1️⃣\d+️⃣) ', '', line)
            i += 1
            continue

        # カテゴリの検出
        if line.startswith('### '):
            current_category = line.replace('### ', '')
            i += 1
            continue

        # チェック済みツールの検出
        checked_match = re.match(checked_pattern, line)
        if checked_match:
            tool_name = checked_match.group(1)
            description = checked_match.group(2)

            tool_info = {
                'name': tool_name,
                'description': description,
                'phase': current_phase,
                'category': current_category,
                'pricing': '',
                'reason': ''
            }

            # 詳細情報を抽出
            j = i + 1
            while j < len(lines) and lines[j].startswith('  - '):
                detail_line = lines[j]

                pricing_match = re.match(pricing_pattern, detail_line)
                if pricing_match:
                    tool_info['pricing'] = f"{pricing_match.group(1)} {pricing_match.group(2)}"

                reason_match = re.match(reason_pattern, detail_line)
                if reason_match:
                    reason = reason_match.group(1)
                    if reason and reason != '___________':
                        tool_info['reason'] = reason

                j += 1

            selected_tools.append(tool_info)

        i += 1

    return selected_tools


def generate_summary_markdown(
    project_info: Dict[str, str],
    tools: List[Dict[str, str]]
) -> str:
    """
    要約Markdownを生成

    Args:
        project_info: プロジェクト情報
        tools: ツールのリスト

    Returns:
        Markdown形式の要約
    """
    md = []

    # ヘッダー
    md.append("# プロジェクトツール選択 要約\n")
    md.append(f"**プロジェクト名**: {project_info.get('project_name', '未設定')}\n")
    md.append(f"**作成日**: {project_info.get('created_date', '未設定')}\n")
    md.append(f"**最終更新**: {project_info.get('updated_date', datetime.now().strftime('%Y-%m-%d')}}\n")
    if project_info.get('author'):
        md.append(f"**作成者**: {project_info['author']}\n")
    md.append("\n---\n\n")

    # サマリー
    md.append("## 📊 選択ツールサマリー\n\n")
    md.append(f"**総ツール数**: {len(tools)}\n\n")

    # 料金別集計
    pricing_count = {'🟢': 0, '🟡': 0, '🔴': 0}
    for tool in tools:
        if tool['pricing']:
            emoji = tool['pricing'][0]
            if emoji in pricing_count:
                pricing_count[emoji] += 1

    md.append("### 💰 料金別内訳\n\n")
    md.append(f"- 🟢 無料: {pricing_count['🟢']}ツール\n")
    md.append(f"- 🟡 一部無料: {pricing_count['🟡']}ツール\n")
    md.append(f"- 🔴 有料: {pricing_count['🔴']}ツール\n\n")

    # 開発工程別集計
    phase_count = {}
    for tool in tools:
        phase = tool['phase']
        if phase:
            phase_count[phase] = phase_count.get(phase, 0) + 1

    md.append("### 📋 開発工程別内訳\n\n")
    for phase, count in sorted(phase_count.items()):
        md.append(f"- {phase}: {count}ツール\n")
    md.append("\n")

    # 選択ツール一覧（工程別）
    md.append("---\n\n")
    md.append("## 📝 選択ツール一覧\n\n")

    current_phase = None
    for tool in tools:
        # 工程が変わったらヘッダー表示
        if tool['phase'] != current_phase:
            current_phase = tool['phase']
            md.append(f"\n### {current_phase}\n\n")

        # ツール情報
        md.append(f"#### {tool['name']}\n\n")
        md.append(f"- **カテゴリ**: {tool['category']}\n")
        if tool['pricing']:
            md.append(f"- **料金**: {tool['pricing']}\n")
        if tool['reason']:
            md.append(f"- **選択理由**: {tool['reason']}\n")
        md.append("\n")

    # テーブル形式の一覧
    md.append("---\n\n")
    md.append("## 📋 選択ツール一覧表\n\n")
    md.append("| # | ツール名 | カテゴリ | 開発工程 | 料金 |\n")
    md.append("|---|---------|---------|---------|------|\n")

    for i, tool in enumerate(tools, 1):
        pricing = tool['pricing'].replace('🟢 ', '🟢').replace('🟡 ', '🟡').replace('🔴 ', '🔴')
        md.append(f"| {i} | {tool['name']} | {tool['category']} | {tool['phase']} | {pricing} |\n")

    md.append("\n")

    # フッター
    md.append("---\n\n")
    md.append("**生成日**: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")

    return ''.join(md)


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使い方: python generate_summary.py <input_file> [output_file]")
        print("例: python generate_summary.py ../プロジェクトツール選択.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    # 出力ファイル名（指定がなければ自動生成）
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.parent / f"{input_file.stem}_要約.md"

    print(f"🔍 選択済みツールを抽出中: {input_file}")

    # ファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # プロジェクト情報を抽出
    project_info = extract_project_info(content)

    # 選択済みツールを抽出
    tools = extract_selected_tools(input_file)

    if not tools:
        print("⚠️ チェック済み [x] のツールが見つかりませんでした。")
        print("   プロジェクトツール選択.mdでツールを選択してください。")
        sys.exit(0)

    print(f"✅ {len(tools)}個のツールが選択されています")

    # 要約を生成
    print(f"📝 要約を生成中...")
    summary = generate_summary_markdown(project_info, tools)

    # ファイルに保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"✅ 要約を保存しました: {output_file}")

    # サマリーを表示
    print(f"\n{'='*80}")
    print(f"📊 要約サマリー")
    print(f"{'='*80}\n")
    print(f"プロジェクト名: {project_info.get('project_name', '未設定')}")
    print(f"総ツール数: {len(tools)}")

    pricing_count = {'🟢': 0, '🟡': 0, '🔴': 0}
    for tool in tools:
        if tool['pricing']:
            emoji = tool['pricing'][0]
            if emoji in pricing_count:
                pricing_count[emoji] += 1

    print(f"料金別: 🟢{pricing_count['🟢']} / 🟡{pricing_count['🟡']} / 🔴{pricing_count['🔴']}")
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
