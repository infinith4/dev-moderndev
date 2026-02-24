# Stoplight Studio

## 概要

Stoplight Studioは、API設計とドキュメント作成に特化したビジュアルエディタです。OpenAPI（Swagger）仕様書をGUIまたはコードエディタで編集でき、リアルタイムプレビュー、モックサーバー、バリデーション機能を提供します。デスクトップアプリとWeb版の両方があり、個人開発者からエンタープライズチームまで、API設計を効率化します。

## 主な特徴

| 項目 | 内容 |
|------|------|
| デスクトップ版無料 | ローカル利用は完全無料で無制限 |
| ビジュアルAPI設計 | GUIでOpenAPI仕様書をフォーム編集 |
| リアルタイムプレビュー | ドキュメントを即座に確認可能 |
| モックサーバー | API定義から自動モック生成 |
| Git統合 | ファイルベースでバージョン管理 |
| バリデーション | OpenAPI仕様準拠のリアルタイム検証 |
| OpenAPI 3.x対応 | 最新のOpenAPI 3.0/3.1をサポート |

## 主な機能

### ビジュアルAPI設計

| 機能 | 説明 |
|------|------|
| Form Editor | GUIでOpenAPI仕様書を作成 |
| Code Editor | YAML/JSON直接編集 |
| スプリットビュー | フォーム+コードの同時表示 |
| リアルタイムプレビュー | ドキュメントを即座に確認 |

### モックサーバー

| 機能 | 説明 |
|------|------|
| 即座にモック生成 | API定義から自動モック |
| サンプルレスポンス | Examplesベースの返却 |
| 動的レスポンス | ランダムデータ生成 |
| ローカルサーバー | localhost:4010で起動 |

### バリデーション・Linting

| 機能 | 説明 |
|------|------|
| リアルタイム検証 | 編集中にエラー検出 |
| Linting | スタイルガイド適用 |
| ベストプラクティス | API設計推奨事項の提示 |
| 自動変換 | Swagger 2.0からOpenAPI 3.xへの変換 |

## インストールとセットアップ

公式URL:
- [Stoplight Studio ダウンロード](https://stoplight.io/studio)
- [ドキュメント](https://docs.stoplight.io/)
- [Stoplight Platform](https://stoplight.io/platform)
- [コミュニティ](https://community.stoplight.io/)

## 基本的な使い方

### 1. インストール

```bash
# デスクトップ版ダウンロード
# https://stoplight.io/studio

# Windows: インストーラー実行
Stoplight-Studio-Setup-x.x.x.exe

# macOS: DMGマウント
Stoplight-Studio-x.x.x.dmg

# Linux: AppImage
chmod +x Stoplight-Studio-x.x.x.AppImage
./Stoplight-Studio-x.x.x.AppImage

# Web版（ブラウザ）
# https://stoplight.io/studio-app
```

### 2. フォームエディタでAPI設計

```
1. reference/user-api.yaml を開く
2. Form Editorタブに切り替え
3. Paths → Add Path
   - Path: /users
   - Method: GET
   - Summary: "ユーザー一覧取得"
4. Responses → 200 → Add Response
   - Content Type: application/json
   - Schema定義
5. Examples → Add Example
```

### 3. コードエディタで編集

```yaml
# reference/user-api.yaml
openapi: 3.1.0
info:
  title: User API
  version: 1.0.0
  description: ユーザー管理API
servers:
  - url: https://api.example.com/v1
paths:
  /users:
    get:
      summary: ユーザー一覧取得
      operationId: getUsers
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
              examples:
                default:
                  value:
                    - id: 1
                      name: Alice
                      email: alice@example.com
    post:
      summary: ユーザー作成
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserInput'
      responses:
        '201':
          description: 作成成功

components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        email:
          type: string
          format: email

    UserInput:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email
```

### 4. モックサーバー起動

```bash
# Stoplight Studio内
# 左サイドバー → Mock Servers → Start Mock Server
# モックサーバーURL: http://localhost:4010

# cURLでテスト
curl http://localhost:4010/users
# レスポンス（Examplesから返却）
# [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
```

### 5. Git連携

```bash
# ローカルGitリポジトリとして管理
cd user-api
git init
git add .
git commit -m "Initial API design"
git remote add origin https://github.com/user/user-api.git
git push -u origin main
```

## 他ツールとの比較

### Stoplight Studio vs Swagger Editor

| 機能 | Stoplight Studio | Swagger Editor |
|------|-----------------|----------------|
| エディタ | GUI + コード | コードのみ |
| モック | 内蔵モックサーバー | なし |
| バリデーション | リアルタイム | リアルタイム |
| オフライン | デスクトップ版対応 | Web版のみ |
| 価格 | デスクトップ無料 | 無料 |

### Stoplight Studio vs Postman

| 機能 | Stoplight Studio | Postman |
|------|-----------------|---------|
| API設計 | ビジュアル設計が得意 | テストが得意 |
| テスト機能 | 限定的 | 強力 |
| モック | API定義から自動生成 | 基本的 |
| Git統合 | ファイルベース | 独自形式 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| APIファースト設計 | 実装前にAPI仕様を定義 | ビジュアルエディタでOpenAPI仕様を設計 |
| フロントエンド並行開発 | バックエンド未完成でもUI開発 | モックサーバーでフロントエンド開発を進行 |
| API仕様レビュー | チームでの仕様合意 | Git連携でPull Requestベースのレビュー |
| OpenAPI学習 | OpenAPI仕様の習得 | GUIで直感的にOpenAPIの構造を理解 |

## ベストプラクティス

### 1. API設計ワークフロー

- 最初にForm Editorでエンドポイントとスキーマの全体構造を設計する
- 詳細な設定はCode Editorに切り替えて調整する
- Examplesを充実させてモックの品質を上げる

### 2. Git管理

- OpenAPI定義ファイルをGitリポジトリで管理する
- ブランチを使ってAPI仕様の変更を管理する
- Pull Requestでチームレビューを行う

### 3. モックの活用

- API設計完了後すぐにモックサーバーを起動する
- フロントエンド開発チームにモックURLを共有する
- Examplesを複数用意してエラーケースもカバーする

## トラブルシューティング

### よくある問題と解決策

#### 1. モックサーバーが起動しない

```
原因: ポート4010が既に使用されている
解決策:
- 既存のプロセスを終了する
- 設定でポート番号を変更する
```

#### 2. OpenAPIバリデーションエラー

```
原因: OpenAPI仕様に違反する記述
解決策:
- エラーパネルの詳細メッセージを確認する
- $refの参照先が存在するか確認する
- required配列にpropertiesに存在しないキーがないか確認する
```

#### 3. Electronアプリが重い

```
原因: 大きなOpenAPIファイルを編集している
解決策:
- ファイルを分割して$refで参照する
- 不要な拡張機能を無効化する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://stoplight.io/studio
- ドキュメント: https://docs.stoplight.io/

### コミュニティ
- コミュニティフォーラム: https://community.stoplight.io/

### チュートリアル
- Getting Started: https://docs.stoplight.io/docs/studio/

## まとめ

Stoplight Studioは、以下の場面で特に有用です:

1. **APIファースト設計** - ビジュアルエディタで直感的にOpenAPI仕様を設計
2. **フロントエンド並行開発** - 内蔵モックサーバーでバックエンド未完成でもUI開発を進行
3. **OpenAPI初心者** - GUIでOpenAPIの構造を学びながらAPI設計ができる

デスクトップ版は完全無料で、個人開発からチーム開発まで幅広くAPI設計を効率化するツールである。
