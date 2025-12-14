#!/usr/bin/env python3
"""
ツールリンク検証スクリプト

Markdownファイル内のツール詳細へのリンクが有効かチェックします。

使い方:
    python validate_links.py <input_file>
    python validate_links.py ../ツール選択マスター.md
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


def extract_links(markdown_file: Path) -> List[Dict[str, str]]:
    """
    Markdownファイルからツールリンクを抽出

    Args:
        markdown_file: Markdownファイルのパス

    Returns:
        ツールとリンクのリスト
    """
    if not markdown_file.exists():
        print(f"❌ ファイルが見つかりません: {markdown_file}")
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    tools = []
    current_phase = None

    # 開発工程を抽出
    phase_pattern = r'^## (\d+️⃣|🔟|1️⃣\d+️⃣) (.+)$'
    # ツール名を抽出
    tool_pattern = r'^- \[[ x]\] \*\*(.+?)\*\*'
    # 詳細リンクを抽出
    link_pattern = r'  - 📄 詳細: \[.+?\]\((.+?)\)$'

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

        # ツールの検出
        tool_match = re.match(tool_pattern, line)
        if tool_match:
            tool_name = tool_match.group(1)

            # 次の行から詳細リンクを抽出
            j = i + 1
            while j < len(lines) and lines[j].startswith('  - '):
                detail_line = lines[j]

                link_match = re.match(link_pattern, detail_line)
                if link_match:
                    link = link_match.group(1)
                    tools.append({
                        'name': tool_name,
                        'phase': current_phase,
                        'link': link,
                        'line_number': i + 1
                    })
                    break

                j += 1

        i += 1

    return tools


def validate_link(base_path: Path, link: str) -> Tuple[bool, str]:
    """
    リンクの有効性を検証

    Args:
        base_path: 基準パス（Markdownファイルのディレクトリ）
        link: 検証するリンク

    Returns:
        (有効かどうか, エラーメッセージ)
    """
    # 相対パスを解決
    if link.startswith('http://') or link.startswith('https://'):
        # 外部リンクはスキップ
        return True, ""

    # 相対パスを絶対パスに変換
    link_path = (base_path / link).resolve()

    if not link_path.exists():
        return False, f"ファイルが存在しません: {link}"

    if not link_path.is_file():
        return False, f"ファイルではありません: {link}"

    return True, ""


def validate_all_links(markdown_file: Path, tools: List[Dict[str, str]]) -> Dict[str, List[Dict]]:
    """
    すべてのリンクを検証

    Args:
        markdown_file: Markdownファイルのパス
        tools: ツールのリスト

    Returns:
        検証結果（有効/無効/リンクなし）
    """
    base_path = markdown_file.parent

    results = {
        'valid': [],
        'invalid': [],
        'no_link': []
    }

    for tool in tools:
        if 'link' not in tool or not tool['link']:
            results['no_link'].append(tool)
            continue

        is_valid, error_msg = validate_link(base_path, tool['link'])

        if is_valid:
            results['valid'].append(tool)
        else:
            tool['error'] = error_msg
            results['invalid'].append(tool)

    return results


def print_validation_report(results: Dict[str, List[Dict]]):
    """
    検証結果レポートを表示

    Args:
        results: 検証結果
    """
    total = len(results['valid']) + len(results['invalid']) + len(results['no_link'])

    print(f"\n{'='*80}")
    print(f"🔗 リンク検証レポート")
    print(f"{'='*80}\n")

    print(f"📊 集計:")
    print(f"  - 総ツール数: {total}")
    print(f"  - ✅ 有効なリンク: {len(results['valid'])}")
    print(f"  - ❌ 無効なリンク: {len(results['invalid'])}")
    print(f"  - ⚠️ リンクなし: {len(results['no_link'])}")

    # 無効なリンクの詳細
    if results['invalid']:
        print(f"\n{'='*80}")
        print(f"❌ 無効なリンク ({len(results['invalid'])}件)")
        print(f"{'='*80}\n")

        for tool in results['invalid']:
            print(f"ツール名: {tool['name']}")
            print(f"  開発工程: {tool['phase']}")
            print(f"  リンク: {tool['link']}")
            print(f"  行番号: {tool['line_number']}")
            print(f"  エラー: {tool['error']}")
            print()

    # リンクなしのツール
    if results['no_link']:
        print(f"\n{'='*80}")
        print(f"⚠️ リンクが設定されていないツール ({len(results['no_link'])}件)")
        print(f"{'='*80}\n")

        for tool in results['no_link']:
            print(f"ツール名: {tool['name']}")
            print(f"  開発工程: {tool['phase']}")
            print(f"  行番号: {tool['line_number']}")
            print()

    # 成功メッセージ
    if not results['invalid'] and not results['no_link']:
        print(f"\n✅ すべてのリンクが有効です！")
    elif not results['invalid']:
        print(f"\n✅ すべてのリンクが有効です（リンクなしのツールを除く）")

    print(f"\n{'='*80}\n")


def save_report(results: Dict[str, List[Dict]], output_file: Path):
    """
    検証結果をファイルに保存

    Args:
        results: 検証結果
        output_file: 出力ファイルのパス
    """
    total = len(results['valid']) + len(results['invalid']) + len(results['no_link'])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# リンク検証レポート\n\n")
        f.write(f"**生成日**: {Path(__file__).stat().st_mtime}\n\n")
        f.write("---\n\n")

        f.write("## 📊 集計\n\n")
        f.write(f"- 総ツール数: {total}\n")
        f.write(f"- ✅ 有効なリンク: {len(results['valid'])}\n")
        f.write(f"- ❌ 無効なリンク: {len(results['invalid'])}\n")
        f.write(f"- ⚠️ リンクなし: {len(results['no_link'])}\n\n")

        # 無効なリンク
        if results['invalid']:
            f.write("## ❌ 無効なリンク\n\n")

            for tool in results['invalid']:
                f.write(f"### {tool['name']}\n\n")
                f.write(f"- **開発工程**: {tool['phase']}\n")
                f.write(f"- **リンク**: `{tool['link']}`\n")
                f.write(f"- **行番号**: {tool['line_number']}\n")
                f.write(f"- **エラー**: {tool['error']}\n\n")

        # リンクなし
        if results['no_link']:
            f.write("## ⚠️ リンクが設定されていないツール\n\n")

            for tool in results['no_link']:
                f.write(f"### {tool['name']}\n\n")
                f.write(f"- **開発工程**: {tool['phase']}\n")
                f.write(f"- **行番号**: {tool['line_number']}\n\n")

    print(f"✅ 検証レポートを保存しました: {output_file}")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使い方: python validate_links.py <input_file>")
        print("例: python validate_links.py ../ツール選択マスター.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    print(f"🔍 ツールリンクを抽出中: {input_file}")

    # リンクを抽出
    tools = extract_links(input_file)

    print(f"📝 {len(tools)}個のツールリンクを検出しました")

    # リンクを検証
    print(f"🔗 リンクを検証中...")
    results = validate_all_links(input_file, tools)

    # レポート表示
    print_validation_report(results)

    # レポート保存
    output_file = input_file.parent / "リンク検証レポート.md"
    save_report(results, output_file)

    # エラーがあれば終了コード1
    if results['invalid']:
        sys.exit(1)


if __name__ == "__main__":
    main()
