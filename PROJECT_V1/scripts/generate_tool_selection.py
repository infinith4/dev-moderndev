#!/usr/bin/env python3
"""
ツール選択マスター生成スクリプト

開発工程ドキュメントから自動的にツール情報を抽出し、
ツール選択マスターを生成します。

使い方:
    python generate_tool_selection.py [output_file]
    python generate_tool_selection.py ../ツール選択マスター_再生成.md
"""

import re
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def find_process_documents(base_dir: Path) -> List[Path]:
    """
    開発工程ドキュメントを検索

    Args:
        base_dir: 検索開始ディレクトリ

    Returns:
        開発工程ドキュメントのパスリスト
    """
    docs_dir = base_dir / "docs"
    if not docs_dir.exists():
        print(f"❌ docsディレクトリが見つかりません: {docs_dir}")
        return []

    # dev_process_開発工程_*.md ファイルを検索
    pattern = "dev_process_開発工程_*.md"
    files = sorted(docs_dir.glob(pattern))

    # .bakファイルを除外
    files = [f for f in files if not f.name.endswith('.bak')]

    return files


def extract_tools_from_table(content: str) -> List[Dict[str, str]]:
    """
    テーブル形式のツール情報を抽出

    Args:
        content: ドキュメントの内容

    Returns:
        ツール情報のリスト
    """
    tools = []

    # テーブルヘッダーを検出
    table_header_pattern = r'\| # \| ツール名 \| 概要 \| 用途 \|'

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # テーブルヘッダーを検出
        if re.search(table_header_pattern, line):
            # 次の行はセパレータなのでスキップ
            i += 2

            # テーブルの行を抽出
            while i < len(lines):
                line = lines[i].strip()

                # テーブル終了
                if not line.startswith('|') or line.startswith('| 資料名'):
                    break

                # テーブル行をパース
                cells = [cell.strip() for cell in line.split('|')]

                if len(cells) >= 8:
                    # cells[0]は空、cells[1]は番号
                    tool_info = {
                        'name': cells[2].strip('[]()').split('](')[0].replace('**', ''),
                        'description': cells[3],
                        'usage': cells[4],
                        'pricing': cells[5],
                        'merits': cells[6],
                        'demerits': cells[7]
                    }

                    tools.append(tool_info)

                i += 1

        i += 1

    return tools


def extract_tools_from_document(doc_path: Path) -> Dict[str, any]:
    """
    開発工程ドキュメントからツール情報を抽出

    Args:
        doc_path: ドキュメントのパス

    Returns:
        工程名とツール情報
    """
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 工程名を抽出
    phase_match = re.search(r'# 開発工程_(\d+)_(.+)', content)
    if phase_match:
        phase_number = phase_match.group(1)
        phase_name = phase_match.group(2)
    else:
        phase_number = ""
        phase_name = doc_path.stem.replace('dev_process_開発工程_', '')

    # ツール情報を抽出
    tools = extract_tools_from_table(content)

    return {
        'number': phase_number,
        'name': phase_name,
        'tools': tools,
        'path': doc_path
    }


def convert_pricing_to_emoji(pricing: str) -> str:
    """
    料金情報を絵文字形式に変換

    Args:
        pricing: 料金情報

    Returns:
        絵文字付き料金情報
    """
    if '無料' in pricing or '無料' in pricing:
        return '🟢 無料'
    elif '有料' in pricing and '無料' in pricing:
        return '🟡 一部無料'
    elif '有料' in pricing:
        return '🔴 有料'
    else:
        return pricing


def generate_master_markdown(phases: List[Dict]) -> str:
    """
    ツール選択マスターMarkdownを生成

    Args:
        phases: 開発工程情報のリスト

    Returns:
        Markdown文字列
    """
    md = []

    # ヘッダー
    md.append("# ツール選択マスター（自動生成版）\n\n")
    md.append(f"**生成日**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append("**バージョン**: 1.0（自動生成）\n")
    md.append("**対象**: IPA共通フレーム2013 全開発工程\n\n")
    md.append("---\n\n")

    # 使い方
    md.append("## 📋 使い方\n\n")
    md.append("1. **各開発工程で使用するツールにチェック ☑ を入れてください**\n")
    md.append("2. **チェックしたツールの詳細は各リンクから確認できます**\n")
    md.append("3. **このファイルをGitで管理して、チーム全体で共有してください**\n\n")
    md.append("---\n\n")

    # 工程ごとにツールを出力
    for phase in phases:
        # 工程ヘッダー
        md.append(f"## {phase['number']}️⃣ {phase['name']}\n\n")

        if not phase['tools']:
            md.append("（ツール情報なし）\n\n")
            continue

        # ツールリスト
        for tool in phase['tools']:
            md.append(f"- [ ] **{tool['name']}** - {tool['description']}\n")

            # 料金
            pricing = convert_pricing_to_emoji(tool['pricing'])
            md.append(f"  - 💰 料金: {pricing}\n")

            # 用途
            if tool['usage']:
                md.append(f"  - 📝 用途: {tool['usage']}\n")

            # メリット（簡潔化）
            if tool['merits']:
                merits = tool['merits'].replace('✅ ', '').split('<br>')
                if len(merits) > 3:
                    merits = merits[:3]
                md.append(f"  - ✅ メリット: {', '.join([m.strip() for m in merits if m.strip()])}\n")

            # デメリット（簡潔化）
            if tool['demerits']:
                demerits = tool['demerits'].replace('❌ ', '').split('<br>')
                if len(demerits) > 2:
                    demerits = demerits[:2]
                md.append(f"  - ⚠️ デメリット: {', '.join([d.strip() for d in demerits if d.strip()])}\n")

            md.append("\n")

        md.append("---\n\n")

    # フッター
    md.append("**END OF DOCUMENT**\n")

    return ''.join(md)


def main():
    """メイン関数"""
    # 出力ファイル名
    if len(sys.argv) >= 2:
        output_file = Path(sys.argv[1])
    else:
        script_dir = Path(__file__).parent
        output_file = script_dir.parent / "ツール選択マスター_自動生成.md"

    # プロジェクトルートを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    print(f"🔍 開発工程ドキュメントを検索中: {project_root / 'docs'}")

    # 開発工程ドキュメントを検索
    doc_files = find_process_documents(project_root)

    if not doc_files:
        print("❌ 開発工程ドキュメントが見つかりませんでした")
        sys.exit(1)

    print(f"📝 {len(doc_files)}個の開発工程ドキュメントを検出しました")

    # 各ドキュメントからツール情報を抽出
    phases = []
    for doc_file in doc_files:
        print(f"  - 処理中: {doc_file.name}")
        phase_info = extract_tools_from_document(doc_file)
        if phase_info['tools']:
            phases.append(phase_info)
            print(f"    ✅ {len(phase_info['tools'])}個のツールを抽出")
        else:
            print(f"    ⚠️ ツール情報なし")

    if not phases:
        print("❌ ツール情報を抽出できませんでした")
        sys.exit(1)

    # ツール選択マスターを生成
    print(f"\n📝 ツール選択マスターを生成中...")
    master_md = generate_master_markdown(phases)

    # ファイルに保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(master_md)

    print(f"✅ ツール選択マスターを保存しました: {output_file}")

    # サマリー表示
    total_tools = sum(len(p['tools']) for p in phases)
    print(f"\n{'='*80}")
    print(f"📊 生成サマリー")
    print(f"{'='*80}\n")
    print(f"開発工程数: {len(phases)}")
    print(f"総ツール数: {total_tools}")
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
