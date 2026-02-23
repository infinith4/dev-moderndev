# Dev Containers

## 概要

Dev Containers（Development Containers）は、Dockerコンテナを利用して再現可能な開発環境を定義・構築するためのオープン仕様です。`devcontainer.json`ファイルにエディタ設定、ツールチェーン、ランタイム、拡張機能などを宣言的に定義し、VS Code、GitHub Codespaces、JetBrains等のIDEからワンクリックで統一された開発環境を起動できます。「自分の環境では動く」問題を根本的に解消します。

## 主な機能

### 1. 環境定義（devcontainer.json）

- **ベースイメージ**: Microsoft公式イメージまたはカスタムDockerfile
- **Features**: 再利用可能なツールインストール単位（Docker-in-Docker、Node.js、Python等）
- **拡張機能**: VS Code拡張を環境に含めて自動インストール
- **設定**: エディタ設定、ポートフォワーディング、環境変数
- **ライフサイクルスクリプト**: postCreateCommand、postStartCommand等

### 2. Features（再利用可能なモジュール）

- **言語ランタイム**: Python、Node.js、Go、Java、.NET等
- **ツール**: Docker-in-Docker、kubectl、Terraform、AWS CLI
- **ユーティリティ**: Git、GitHub CLI、Azure CLI
- **カスタムFeatures**: 独自Featuresの作成・公開が可能

### 3. 構成オプション

- **Dockerfile**: カスタムDockerfileの指定
- **Docker Compose**: マルチサービス構成（DB、Redis等の依存サービス）
- **イメージ直接指定**: `"image": "mcr.microsoft.com/devcontainers/base:ubuntu"`
- **ビルド引数**: build.args でビルド時の変数を指定

### 4. 対応IDE・サービス

- **VS Code**: Dev Containers拡張機能
- **GitHub Codespaces**: クラウドベースの開発環境
- **JetBrains Gateway**: IntelliJ、PyCharm等から接続
- **Dev Container CLI**: コマンドラインでのビルド・実行

## 利用方法

### 基本的なdevcontainer.json

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu-24.04",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.12"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt && npm install",
  "forwardPorts": [3000, 8080],
  "remoteUser": "vscode"
}
```

### Dockerfileを使用した構成

```json
{
  "name": "Custom Environment",
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {
      "VARIANT": "3.12"
    }
  },
  "features": {
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt"
}
```

### Docker Composeを使用した構成

```json
{
  "name": "Full Stack App",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "shutdownAction": "stopCompose"
}
```

### Dev Container CLI

```bash
# CLIのインストール
npm install -g @devcontainers/cli

# コンテナのビルド
devcontainer build --workspace-folder .

# コンテナの起動
devcontainer up --workspace-folder .

# コンテナ内でコマンド実行
devcontainer exec --workspace-folder . npm test
```

### CI/CDでの利用

```yaml
# .github/workflows/ci.yml
name: CI with Dev Container

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: devcontainers/ci@v0.3
        with:
          runCmd: npm test
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Dev Containers仕様** | 無料 | オープン仕様 |
| **VS Code拡張** | 無料 | Microsoft提供 |
| **GitHub Codespaces** | 従量課金 | クラウド実行環境 |

## メリット

1. **環境統一**: チーム全員が同一の開発環境を使用
2. **オンボーディング高速化**: 新メンバーがすぐに開発開始可能
3. **宣言的定義**: 環境をコードとして管理（Infrastructure as Code）
4. **Features**: 再利用可能なモジュールで構成を簡素化
5. **マルチサービス**: Docker Composeで依存サービスも含めた環境構築
6. **Codespaces連携**: クラウドで同じ環境をブラウザから利用可能
7. **CI/CD統合**: 開発環境と同じコンテナでテスト実行

## デメリット

1. **Docker必須**: ローカルにDocker環境が必要
2. **リソース消費**: コンテナ実行にメモリ・CPU・ストレージを消費
3. **イメージサイズ**: 初回ビルドやプルに時間がかかる場合がある
4. **GPU対応制限**: GPU利用は追加設定が必要
5. **パフォーマンス**: ファイルシステムのマウント方式によっては遅延が発生

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Vagrant** | 仮想マシンベースの開発環境 | DevContainerよりリソース消費大 |
| **Nix** | 再現可能なパッケージ管理 | DevContainerよりコンテナ不要 |
| **Docker直接利用** | Dockerfileのみ | DevContainerよりIDE統合が弱い |
| **GitHub Codespaces** | クラウドDevContainer | ローカルDocker不要だが有料 |

## 公式リンク

- **公式サイト**: [https://containers.dev/](https://containers.dev/)
- **仕様**: [https://containers.dev/implementors/spec/](https://containers.dev/implementors/spec/)
- **Features一覧**: [https://containers.dev/features](https://containers.dev/features)
- **VS Code拡張**: [https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **GitHub**: [https://github.com/devcontainers](https://github.com/devcontainers)

## 関連ドキュメント

- [EditorConfig](./EditorConfig.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 環境構築・実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
