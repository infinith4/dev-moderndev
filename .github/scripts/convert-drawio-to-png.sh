#!/bin/bash
set -e

# drawio コマンドの存在確認
if ! command -v drawio &> /dev/null; then
  echo "Error: drawio CLI is not installed."
  exit 1
fi

for drawio in "$@"; do
  png="${drawio}.png"
  drawio -x -f png -s 2 -t -o "$png" "$drawio" 2>/dev/null
  git add "$png"
done