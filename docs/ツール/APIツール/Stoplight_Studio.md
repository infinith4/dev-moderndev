# Stoplight Studio

## 概要

Stoplight Studioは、API設計とドキュメント作成に特化したビジュアルエディタです。OpenAPI（Swagger）仕様書をGUIまたはコードエディタで編集でき、リアルタイムプレビュー、モックサーバー、バリデーション機能を提供します。デスクトップアプリとWeb版の両方があり、個人開発者からエンタープライズチームまで、API設計を効率化します。

## 主な機能

### 1. ビジュアルAPI設計
- **Form Editor**: GUIでOpenAPI仕様書作成
- **Code Editor**: YAML/JSON直接編集
- **スプリットビュー**: フォーム+コードの同時表示
- **リアルタイムプレビュー**: ドキュメント即座に確認

### 2. OpenAPI 3.xサポート
- **OpenAPI 3.0/3.1**: 最新仕様対応
- **Swagger 2.0**: レガシーサポート
- **自動変換**: Swagger 2.0 → OpenAPI 3.x
- **バリデーション**: 仕様準拠チェック

### 3. モックサーバー
- **即座にモック生成**: API定義から自動モック
- **サンプルレスポンス**: Examplesベースの返却
- **動的レスポンス**: ランダムデータ生成
- **ローカルサーバー**: localhost:4010で起動

### 4. ドキュメント生成
- **美しいドキュメント**: インタラクティブなAPI Docs
- **Try It Out**: ブラウザからAPIテスト
- **認証サポート**: OAuth、API Key、Bearer Token
- **多言語コードサンプル**: cURL、JavaScript、Python等

### 5. バリデーション
- **リアルタイム検証**: 編集中にエラー検出
- **Linting**: スタイルガイド適用
- **ベストプラクティス**: API設計推奨事項

### 6. Git統合
- **ファイルベース**: YAMLファイルで管理
- **GitHub/GitLab連携**: リポジトリと同期
- **バージョン管理**: Git履歴で変更追跡
- **ブランチ切り替え**: ブランチ間の編集

## 利用方法

### インストール

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

### 新規API作成

```
1. Stoplight Studio起動
2. Create New API
3. API名入力: "User API"
4. OpenAPI Version: 3.1

5. 自動生成されたファイル構造:
   user-api/
   ├── reference/
   │   └── user-api.yaml    # OpenAPI仕様書
   └── README.md
```

### フォームエディタでAPI設計

```
1. reference/user-api.yaml を開く

2. Form Editorタブに切り替え

3. Paths → Add Path
   - Path: /users
   - Method: GET
   - Summary: "ユーザー一覧取得"

4. Responses → 200 → Add Response
   - Content Type: application/json
   - Schema: 
     type: array
     items:
       type: object
       properties:
         id:
           type: integer
         name:
           type: string
         email:
           type: string

5. Examples → Add Example
   [
     {"id": 1, "name": "Alice", "email": "alice@example.com"},
     {"id": 2, "name": "Bob", "email": "bob@example.com"}
   ]
```

### コードエディタで編集

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
                    - id: 2
                      name: Bob
                      email: bob@example.com
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
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

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

### モックサーバー起動

```bash
# Stoplight Studio内
1. 左サイドバー → Mock Servers
2. Start Mock Server
3. モックサーバーURL: http://localhost:4010

# cURLでテスト
curl http://localhost:4010/users

# レスポンス（Examplesから返却）
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
```

### ドキュメントプレビュー

```
1. 左サイドバー → Docs
2. リアルタイムでAPI Docsが表示される
3. Try It Out でAPIテスト実行
   - Parameters入力
   - Send Request
   - レスポンス確認
```

### Git連携

```bash
# ローカルGitリポジトリとして管理
cd user-api
git init
git add .
git commit -m "Initial API design"

# GitHub連携
git remote add origin https://github.com/user/user-api.git
git push -u origin main

# Stoplight Studioで編集・コミット
1. File → Open Folder → Gitリポジトリ選択
2. 編集
3. 左サイドバー → Source Control
4. コミットメッセージ入力 → Commit
5. Push
```

### プロジェクト共有

```
# Stoplight Platform（クラウド）連携
1. File → Publish to Stoplight
2. Stoplight Platformアカウント作成
3. Project作成
4. チームメンバー招待
5. https://your-workspace.stoplight.io/docs/user-api
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Studio Desktop** | 🟢 完全無料 | ローカル編集、無制限プロジェクト |
| **Stoplight Platform Starter** | 🟡 $0/月 | 公開プロジェクト無制限、1ユーザー |
| **Stoplight Platform Professional** | 💰 $49/ユーザー/月 | プライベートプロジェクト、チーム協業 |
| **Stoplight Platform Enterprise** | 💰 要問い合わせ | SSO、オンプレミス、専用サポート |

## メリット

### ✅ 主な利点

1. **デスクトップ版無料**: ローカル利用は完全無料
2. **ビジュアル編集**: GUIでOpenAPI作成
3. **即座にモック**: API実装前にテスト可能
4. **リアルタイムプレビュー**: ドキュメント即座確認
5. **Git統合**: ファイルベースでバージョン管理
6. **バリデーション**: OpenAPI仕様準拠チェック
7. **美しいドキュメント**: インタラクティブなAPI Docs
8. **Try It Out**: ブラウザからAPIテスト
9. **コード生成**: クライアントSDK生成
10. **学習容易**: OpenAPI初心者でも使いやすい

## デメリット

### ❌ 制約・課題

1. **チーム協業**: デスクトップ版は単独作業
2. **Platform高価**: チーム利用は有料
3. **オフライン制限**: Web版はインターネット必須
4. **Electronアプリ**: デスクトップ版はリソース消費
5. **機能制限**: Postmanほど高度なテスト機能なし
6. **モック制限**: 複雑なビジネスロジックは未対応
7. **学習曲線**: OpenAPI仕様理解が必要
8. **プラグイン**: 拡張機能が限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Swagger Editor** | OpenAPIエディタ、無料 | Stoplightよりシンプルだが基本機能のみ |
| **Postman** | APIテスト+設計 | Stoplightよりテスト機能強い |
| **Insomnia** | APIテスト+設計 | Stoplightと類似、軽量 |
| **Apicurio Studio** | オープンソースAPI設計 | Stoplightより機能少ない |
| **VS Code + OpenAPI Extension** | コードエディタ統合 | Stoplightより手動作業多い |

## 公式リンク

- **公式サイト**: [https://stoplight.io/studio](https://stoplight.io/studio)
- **ダウンロード**: [https://stoplight.io/studio](https://stoplight.io/studio)
- **ドキュメント**: [https://docs.stoplight.io/](https://docs.stoplight.io/)
- **Stoplight Platform**: [https://stoplight.io/platform](https://stoplight.io/platform)
- **コミュニティ**: [https://community.stoplight.io/](https://community.stoplight.io/)

## 関連ドキュメント

- [APIツール一覧](../APIツール/)
- [Swagger/OpenAPI](./Swagger_OpenAPI.md)
- [Postman](./Postman.md)
- [ReDoc](./ReDoc.md)
- [API設計ベストプラクティス](../../best-practices/api-design.md)

---

**カテゴリ**: APIツール  
**対象工程**: 要件定義、設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
