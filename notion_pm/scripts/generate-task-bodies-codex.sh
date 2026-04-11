#!/bin/bash
# notion_pm/scripts/generate-task-bodies-codex.sh
#
# Codex CLI を使ってタスクボディ Markdown を一括生成する。
#
# Usage:
#   bash scripts/generate-task-bodies-codex.sh            # 既存ファイルはスキップ
#   bash scripts/generate-task-bodies-codex.sh --force    # 既存ファイルも上書き
#
# 前提:
#   - `codex` コマンドが PATH に存在すること
#   - `codex login` 済みであること
#   - python3 が利用可能であること
#   - notion_pm/ ディレクトリで実行 OR スクリプト直接呼び出し、どちらでも動作

set -euo pipefail

NOTION_PM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_BODIES_DIR="$NOTION_PM_DIR/docs/task-bodies"
CHILD_TEMPLATE="$NOTION_PM_DIR/docs/child-template.json"
PARENT_TEMPLATE="$NOTION_PM_DIR/docs/parent-template.json"
FORCE="${1:-}"
PROMPT_FILE=$(mktemp /tmp/codex-gen-XXXXX.txt)

trap "rm -f '$PROMPT_FILE'" EXIT

# ---------------------------------------------------------------------------
# 前提チェック
# ---------------------------------------------------------------------------
if ! command -v codex &>/dev/null; then
  echo "ERROR: 'codex' command not found."
  echo "  Install Codex CLI and ensure it is on PATH."
  exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 not found."
  exit 1
fi

if [ ! -f "$CHILD_TEMPLATE" ] || [ ! -f "$PARENT_TEMPLATE" ]; then
  echo "ERROR: Template files not found in $NOTION_PM_DIR/docs/"
  exit 1
fi

mkdir -p "$TASK_BODIES_DIR"

# ---------------------------------------------------------------------------
# 1. dry-run でタスク一覧を取得
# ---------------------------------------------------------------------------
echo "[1/4] Getting task list (dry-run)..."
TASK_LIST=$(cd "$NOTION_PM_DIR" && npm run --silent import-xlsx-wbs -- --dry-run 2>&1)
echo "$TASK_LIST"

# ---------------------------------------------------------------------------
# 2. テンプレートからセクション名を抽出
# ---------------------------------------------------------------------------
echo ""
echo "[2/4] Reading template section names..."
CHILD_SECTIONS=$(python3 - "$CHILD_TEMPLATE" << 'PYEOF'
import json, sys
data = json.load(open(sys.argv[1]))
print(", ".join(f'"{s["_section"]}"' for s in data))
PYEOF
)
PARENT_SECTIONS=$(python3 - "$PARENT_TEMPLATE" << 'PYEOF'
import json, sys
data = json.load(open(sys.argv[1]))
print(", ".join(f'"{s["_section"]}"' for s in data))
PYEOF
)
echo "  Child sections : $CHILD_SECTIONS"
echo "  Parent sections: $PARENT_SECTIONS"

# ---------------------------------------------------------------------------
# 3. プロンプトを一時ファイルに書き込む
# ---------------------------------------------------------------------------
echo ""
echo "[3/4] Building prompt..."

if [ "$FORCE" = "--force" ]; then
  SKIP_INSTRUCTION="すでにファイルが存在する場合も上書きしてください。"
else
  SKIP_INSTRUCTION="すでにファイルが存在する場合はスキップしてください（上書きしない）。"
fi

cat > "$PROMPT_FILE" << EOF
以下の WBS タスク一覧に対して、Markdown ファイルを生成してください。

【作業ディレクトリ】
$NOTION_PM_DIR

【変更対象】
- docs/task-bodies/** のみ変更してよい
- それ以外のファイルは作成・編集しないこと

【ファイルパス規則（$NOTION_PM_DIR からの相対パス）】
- 親タスク: docs/task-bodies/{タスク名}.md
- 子タスク: docs/task-bodies/{親タスク名}/{タスク名}.md
  ※ dry-run 出力の "[子] タスク名 [期間:...] [工数:...]" の「タスク名」部分をファイル名にする
  ※ 親タスク名は直前の "[親]" 行のタスク名

【セクション名（## 見出し、名前は完全一致させること）】
- 親タスク のセクション: $PARENT_SECTIONS
- 子タスク のセクション: $CHILD_SECTIONS

【各セクションの内容ガイドライン】
- 「対応内容」: タスク名から推測した具体的な作業ステップをリスト形式で記述
- 「完了条件」: 測定可能な完了基準をリスト形式で記述
- 「成果物」: 具体的な成果物名（ドキュメント、URL 等）をリスト形式で記述
- 「タスク着手時」: 以下のチェックリストをそのまま使用すること
  - 期間に対応を期間を入力してください。(5日を超えるタスクは分割してください)
  - 見積(人日)に記載がなければ入力してください。
  - ステータスを対応中に変更してください。
  - 完了条件を満たしたら、ステータスをレビューに変更してください。
  - 成果物を記載してください。(例: PR, SpreadsheetのURLなど)
- 「目的」「スコープ」: 工程名から適切な内容を推測して記述
- 「リスク・課題」: 空のテーブル（ヘッダーのみ）でよい
- ${SKIP_INSTRUCTION}

【出力ルール】
- Markdown のみを作成する
- 各ファイルの見出しは ## から開始する
- 箇条書きは "-" を使う
- 余計な説明ファイルやログファイルは作らない

【WBS タスク一覧（dry-run 出力）】
${TASK_LIST}
EOF

echo "  Prompt written to: $PROMPT_FILE"

# ---------------------------------------------------------------------------
# 4. Codex CLI でファイル生成
# ---------------------------------------------------------------------------
echo ""
echo "[4/4] Generating Markdown files with Codex CLI..."
echo "      (This may take a moment...)"
echo ""

codex exec --full-auto -C "$NOTION_PM_DIR" - < "$PROMPT_FILE"

# ---------------------------------------------------------------------------
# 完了報告
# ---------------------------------------------------------------------------
echo ""
echo "Done. Files in: $TASK_BODIES_DIR"
echo ""
if command -v tree &>/dev/null; then
  tree "$TASK_BODIES_DIR" --noreport 2>/dev/null || ls -R "$TASK_BODIES_DIR"
else
  ls -R "$TASK_BODIES_DIR"
fi
