# Visual Studio Code (VS Code)

## 概要

Visual Studio Code（VS Code）は、Microsoft製の無料オープンソースコードエディタです。軽量、高速、拡張機能（Extension）、IntelliSense、統合ターミナル、Git統合、デバッガー、リモート開発により、多言語開発環境を提供します。Electron（Web技術）、クロスプラットフォーム、世界シェア1位のエディタです。

## 主な機能

### 1. コーディング
- **IntelliSense**: 自動補完
- **シンタックスハイライト**: 構文強調
- **コード整形**: Prettier、ESLint統合
- **スニペット**: コードスニペット

### 2. デバッグ
- **統合デバッガー**: ブレークポイント
- **変数ウォッチ**: 変数監視
- **コールスタック**: スタック表示
- **多言語対応**: Node.js、Python、Java等

### 3. Git統合
- **Source Control**: Git UI
- **コミット**: コミット・プッシュ
- **差分表示**: diff ビュー
- **ブランチ管理**: ブランチ切り替え

### 4. 拡張機能
- **Marketplace**: 豊富な拡張機能
- **言語サポート**: 多言語対応
- **テーマ**: カラーテーマ
- **アイコン**: ファイルアイコン

## 利用方法

### インストール

```bash
# macOS
brew install --cask visual-studio-code

# Windows
# https://code.visualstudio.com/Download

# Linux (Debian/Ubuntu)
sudo apt install code
```

### 基本操作

```
# コマンドパレット
Cmd/Ctrl + Shift + P

# ファイル検索
Cmd/Ctrl + P

# 複数カーソル
Alt + Click

# 行複製
Shift + Alt + Down/Up

# コメント
Cmd/Ctrl + /

# フォーマット
Shift + Alt + F
```

### 人気拡張機能

```
必須拡張機能:
- Prettier - Code formatter
- ESLint
- GitLens
- Path Intellisense
- Auto Rename Tag
- Bracket Pair Colorizer

言語別:
- Python (Microsoft)
- Java Extension Pack
- C/C++ (Microsoft)
- Go
- Rust Analyzer

フロントエンド:
- ES7+ React/Redux/React-Native snippets
- Vetur (Vue.js)
- Angular Language Service

その他:
- Live Server
- Docker
- Remote - SSH
- REST Client
```

### settings.json

```json
// settings.json
{
  "editor.fontSize": 14,
  "editor.tabSize": 2,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "terminal.integrated.fontSize": 13,
  "git.autofetch": true,
  "git.confirmSync": false,
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  }
}
```

### tasks.json（タスク自動化）

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "npm install",
      "type": "shell",
      "command": "npm install",
      "group": "build"
    },
    {
      "label": "npm run dev",
      "type": "shell",
      "command": "npm run dev",
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "npm test",
      "type": "shell",
      "command": "npm test",
      "group": "test"
    }
  ]
}
```

### launch.json（デバッグ設定）

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Node.js",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/index.js"
    },
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/src"
    },
    {
      "type": "python",
      "request": "launch",
      "name": "Python: Current File",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

### スニペット

```json
// .vscode/snippets.code-snippets
{
  "React Component": {
    "prefix": "rfc",
    "body": [
      "import React from 'react'",
      "",
      "function ${1:ComponentName}() {",
      "  return (",
      "    <div>",
      "      $0",
      "    </div>",
      "  )",
      "}",
      "",
      "export default ${1:ComponentName}"
    ],
    "description": "React Functional Component"
  }
}
```

### ワークスペース

```json
// project.code-workspace
{
  "folders": [
    {
      "path": "frontend"
    },
    {
      "path": "backend"
    }
  ],
  "settings": {
    "editor.formatOnSave": true
  }
}
```

### リモート開発

```bash
# Remote - SSH拡張機能インストール

# SSH接続
Cmd/Ctrl + Shift + P > "Remote-SSH: Connect to Host..."

# または .ssh/config設定
Host myserver
  HostName example.com
  User username
  IdentityFile ~/.ssh/id_rsa
```

### Dev Containers

```json
// .devcontainer/devcontainer.json
{
  "name": "Node.js",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  },
  "forwardPorts": [3000],
  "postCreateCommand": "npm install"
}
```

### GitHub Copilot

```bash
# GitHub Copilot拡張機能インストール

# 使用方法
1. コメントで機能説明を書く
2. Tabキーで提案受け入れ
3. Alt+[ / Alt+] で次の提案

# 例
// Create a function that calculates fibonacci number
function fibonacci(n) {
  // Copilotが自動補完
}
```

### マルチカーソル

```
# 複数選択
Alt + Click

# 次の一致を選択
Cmd/Ctrl + D

# すべての一致を選択
Cmd/Ctrl + Shift + L

# カーソル追加（上）
Cmd/Ctrl + Alt + Up

# カーソル追加（下）
Cmd/Ctrl + Alt + Down
```

### キーボードショートカット

```
# ファイル
Cmd/Ctrl + N: 新規ファイル
Cmd/Ctrl + S: 保存
Cmd/Ctrl + W: 閉じる

# 編集
Cmd/Ctrl + X: カット
Cmd/Ctrl + C: コピー
Cmd/Ctrl + V: ペースト
Cmd/Ctrl + Z: 元に戻す
Cmd/Ctrl + Shift + Z: やり直し

# 検索
Cmd/Ctrl + F: 検索
Cmd/Ctrl + H: 置換
Cmd/Ctrl + Shift + F: ワークスペース検索

# ナビゲーション
Cmd/Ctrl + P: ファイル移動
Cmd/Ctrl + Shift + O: シンボル移動
Cmd/Ctrl + G: 行移動

# ターミナル
Ctrl + `: ターミナル表示/非表示
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **VS Code** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **軽量**: 高速起動
3. **拡張機能**: 豊富な拡張機能
4. **クロスプラットフォーム**: Windows、macOS、Linux
5. **IntelliSense**: 強力な補完

## デメリット

1. **メモリ**: 拡張機能で重くなる
2. **設定**: 初期設定必要
3. **Electron**: Electronベース
4. **IDE機能**: フルIDE比較で機能少ない

## 公式リンク

- **公式サイト**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **ドキュメント**: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)

## 関連ドキュメント

- [エディタツール一覧](../エディタツール/)
- [IntelliJ IDEA](./IntelliJ_IDEA.md)
- [Sublime Text](./Sublime_Text.md)

---

**カテゴリ**: エディタツール
**対象工程**: コーディング・開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
