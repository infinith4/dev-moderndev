# DevContainer 設定変更手順

このドキュメントでは、DevContainer の名前やサービス名を一括で変更する方法を説明します。

## 概要

以下の設定を環境変数ファイルから一括で変更できます:

- `devcontainer.json` の `name`
- `devcontainer.json` の `service`
- `docker-compose.yml` のサービス名（例: `app`）
- `docker-compose.yml` の `container_name`

## ファイル構成

- `.env.devcontainer` - 環境変数設定ファイル
- `setup-devcontainer.ps1` - 設定を反映する PowerShell スクリプト

## 使用手順

### 1. 環境変数ファイルを編集

`.env.devcontainer` を開いて、任意の値に変更します。

```env
# DevContainer Configuration
# devcontainer.json の name と service、docker-compose.yml の app と container_name に使用されます

DEVCONTAINER_NAME=my-project
SERVICE_NAME=myapp
CONTAINER_NAME=my-project-container
```

#### 環境変数の説明

| 環境変数 | 説明 | 変更対象 |
|---------|------|----------|
| `DEVCONTAINER_NAME` | DevContainer の表示名 | `devcontainer.json` の `name` |
| `SERVICE_NAME` | Docker Compose のサービス名 | `devcontainer.json` の `service`<br>`docker-compose.yml` のサービス名 |
| `CONTAINER_NAME` | Docker コンテナ名 | `docker-compose.yml` の `container_name` |

### 2. PowerShell スクリプトを実行

PowerShell を開いて、プロジェクトのルートディレクトリで以下のコマンドを実行します。

```powershell
./setup-devcontainer.ps1
```

#### 実行例

```
環境変数を読み込んでいます: .env.devcontainer
  DEVCONTAINER_NAME = my-project
  SERVICE_NAME = myapp
  CONTAINER_NAME = my-project-container

devcontainer.json を更新しています...
  name: template-dev-docs -> my-project
  service: app -> myapp
  ✓ 更新完了

docker-compose.yml を更新しています...
  サービス名: app -> myapp
  container_name: template-dev-docs -> my-project-container
  ✓ 更新完了

全ての設定が正常に更新されました!
変更を反映するには、DevContainerを再起動してください。
```

### 3. DevContainer を再起動

VSCode で DevContainer を再起動して変更を反映します。

1. `Ctrl+Shift+P` (または `Cmd+Shift+P`) でコマンドパレットを開く
2. "Dev Containers: Rebuild Container" を選択
3. または "Dev Containers: Reopen in Container" を選択

## オプション

ファイルパスをカスタマイズする場合は、パラメータを指定できます。

```powershell
./setup-devcontainer.ps1 `
    -EnvFile ".env.devcontainer" `
    -DevContainerPath ".devcontainer/devcontainer.json" `
    -DockerComposePath "docker-compose.yml"
```

## トラブルシューティング

### スクリプトが実行できない場合

PowerShell の実行ポリシーでブロックされている場合があります。以下のコマンドで実行ポリシーを確認してください。

```powershell
Get-ExecutionPolicy
```

一時的に実行を許可する場合:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
./setup-devcontainer.ps1
```

### 環境変数が読み込まれない場合

- `.env.devcontainer` ファイルが存在することを確認
- ファイルの文字エンコーディングが UTF-8 であることを確認
- 環境変数の形式が `KEY=VALUE` であることを確認（スペースなし）

### 変更が反映されない場合

- DevContainer を完全に再ビルドしてみてください
  1. コマンドパレットで "Dev Containers: Rebuild Container" を実行
  2. または、既存のコンテナとイメージを削除してから再度開く

## 注意事項

- スクリプト実行前に、変更対象のファイルをバックアップすることを推奨します
- Git で管理している場合は、変更内容を確認してからコミットしてください
- `.env.devcontainer` ファイルは機密情報を含む可能性があるため、必要に応じて `.gitignore` に追加してください

## DevContainer セットアップ内容

`.devcontainer/setup.sh` により、以下のツールが自動的にインストールされます:

1. **Google Chrome** - markdown-preview-enhanced でのPDF生成に使用
2. **日本語フォント** - PDF生成時の日本語表示に必要
3. **PlantUML** - UML図生成ツール
4. **@openai/codex** - OpenAI Codex CLI ツール（グローバルインストール）

## ファイルの変更内容

### devcontainer.json

```json
{
  "name": "my-project",      // ← DEVCONTAINER_NAME
  "dockerComposeFile": "../docker-compose.yml",
  "service": "myapp",         // ← SERVICE_NAME
  // ... その他の設定
}
```

### docker-compose.yml

```yaml
services:
  myapp:                           # ← SERVICE_NAME
    user: vscode
    container_name: my-project-container  # ← CONTAINER_NAME
    build:
      context: .
      dockerfile: Dockerfile
    # ... その他の設定
```
