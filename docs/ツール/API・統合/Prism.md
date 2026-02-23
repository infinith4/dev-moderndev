# Prism

## 概要

Prismは、OpenAPI仕様（Swagger）をベースにしたHTTP APIモックサーバーです。OpenAPI/Swagger定義ファイルから自動的にモックサーバーを生成し、リクエストのバリデーション、レスポンスの自動生成、エラーケースのシミュレーションを提供します。スキーマ駆動開発（Schema-Driven Development）を強力にサポートし、API仕様書とモックの乖離を防ぎます。軽量でNode.js製、コマンドラインツールとして使いやすく、Docker対応でCI/CDにも容易に統合できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | https://stoplight.io/open-source/prism |
| **料金** |  無料 |
| **ライセンス** | Apache License 2.0 |
| **対応仕様** | OpenAPI 2.0 (Swagger)、OpenAPI 3.x |
| **動作環境** | Node.js、Docker、スタンドアロンバイナリ |
| **開発元** | Stoplight |
| **初版リリース** | 2017年 |
| **最新バージョン** | 5.x（2024年時点） |

## 主な機能

### 1. OpenAPI仕様ベースのモック
- **自動モック生成**: OpenAPI定義から即座にモックサーバーを起動
- **Examples利用**: OpenAPI内のexamplesをレスポンスとして返却
- **動的生成**: スキーマからランダムなダミーデータを自動生成
- **複数レスポンス**: 複数のexampleを切り替えて返却

### 2. リクエストバリデーション
- **スキーマ検証**: リクエストがOpenAPI仕様に準拠しているか検証
- **パラメータチェック**: パス、クエリ、ヘッダーパラメータの検証
- **ボディ検証**: JSON Schemaに基づくリクエストボディの検証
- **エラーレスポンス**: バリデーション失敗時に詳細なエラーメッセージを返却

### 3. レスポンスモード
- **Static Mode**: examplesを固定で返す
- **Dynamic Mode**: スキーマからランダムにデータを生成
- **Example Selection**: 複数のexampleから選択して返却（prefer指定）
- **Status Code Selection**: 任意のステータスコードのレスポンスを選択

### 4. エラーシミュレーション
- **400番台エラー**: バリデーションエラー、認証エラー
- **500番台エラー**: サーバーエラーのシミュレーション
- **任意のステータスコード**: OpenAPIで定義された任意のレスポンスを返却
- **エラーケーステスト**: クライアントのエラーハンドリングを検証

### 5. プロキシモード
- **リクエスト転送**: 実APIへのリクエストを中継
- **フォールバック**: モックにないエンドポイントは実APIへ
- **ヘッダー転送**: 認証情報などのヘッダーを実APIに転送
- **ローカル開発**: 一部のエンドポイントのみモック、残りは実API

### 6. コンテンツネゴシエーション
- **Accept対応**: Acceptヘッダーに応じたレスポンス形式（JSON、XML等）
- **複数形式**: OpenAPIで定義された複数のcontent typeに対応
- **優先度**: クライアントの要求に応じた最適な形式を返却

### 7. CORS対応
- **自動設定**: CORS ヘッダーを自動的に追加
- **クロスオリジン**: フロントエンド開発でのクロスオリジン問題を解決
- **カスタマイズ**: CORS設定のカスタマイズが可能

## 利用方法

### インストール

#### 1. npm/yarn（Node.js環境）
```bash
# npmでグローバルインストール
npm install -g @stoplight/prism-cli

# yarnの場合
yarn global add @stoplight/prism-cli
```

#### 2. Docker
```bash
# Dockerコンテナで起動
docker run --rm -it -p 4010:4010 \
  -v $(pwd)/openapi.yaml:/tmp/openapi.yaml \
  stoplight/prism:latest mock /tmp/openapi.yaml
```

#### 3. スタンドアロンバイナリ
```bash
# GitHubからバイナリをダウンロード
# https://github.com/stoplightio/prism/releases
curl -L https://github.com/stoplightio/prism/releases/download/v5.x.x/prism-cli-linux -o prism
chmod +x prism

# 実行
./prism mock openapi.yaml
```

### 基本的な使い方

#### 1. OpenAPI定義ファイルの準備
```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: Sample API
  version: 1.0.0
paths:
  /users/{userId}:
    get:
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: ユーザー情報
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
              examples:
                alice:
                  value:
                    id: 1
                    name: Alice
                    email: alice@example.com
                bob:
                  value:
                    id: 2
                    name: Bob
                    email: bob@example.com
        '404':
          description: ユーザーが見つからない
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
```

#### 2. モックサーバーの起動
```bash
# 基本的な起動（デフォルトポート4010）
prism mock openapi.yaml

# ポート指定
prism mock -p 8080 openapi.yaml

# ダイナミックモード（スキーマからランダム生成）
prism mock --dynamic openapi.yaml

# URLから直接起動
prism mock https://api.example.com/openapi.json
```

#### 3. リクエストの実行
```bash
# GET /users/1
curl http://localhost:4010/users/1

# レスポンス（aliceのexample）
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

#### 4. Example選択
```bash
# Prefer ヘッダーでexampleを指定
curl -H "Prefer: example=bob" http://localhost:4010/users/2

# レスポンス（bobのexample）
{
  "id": 2,
  "name": "Bob",
  "email": "bob@example.com"
}
```

#### 5. エラーレスポンスの取得
```bash
# Preferヘッダーでステータスコードを指定
curl -H "Prefer: code=404" http://localhost:4010/users/999

# レスポンス（404エラー）
{
  "error": "ユーザーが見つからない"
}
```

#### 6. リクエストバリデーション
```bash
# バリデーションを有効化してサーバー起動
prism mock --validate openapi.yaml

# 不正なリクエスト（userIdが数値でない）
curl http://localhost:4010/users/abc

# レスポンス（400エラー）
{
  "type": "https://stoplight.io/prism/errors#UNPROCESSABLE_ENTITY",
  "title": "Invalid request",
  "status": 422,
  "detail": "The request doesn't match the schema"
}
```

#### 7. プロキシモード
```bash
# 実APIへのプロキシとして動作
prism proxy openapi.yaml https://api.example.com

# エラー発生時にモックを返す
prism proxy --errors openapi.yaml https://api.example.com
```

#### 8. ダイナミックモード
```bash
# スキーマからランダムにデータを生成
prism mock --dynamic openapi.yaml

# リクエスト
curl http://localhost:4010/users/1

# レスポンス（ランダム生成されたダミーデータ）
{
  "id": 72548392,
  "name": "consectetur dolor",
  "email": "laborum@example.com"
}
```

#### 9. CORS設定
```bash
# CORS を有効化（デフォルトで有効）
prism mock openapi.yaml

# CORSを無効化
prism mock --cors=false openapi.yaml
```

#### 10. Docker Composeでの利用
```yaml
# docker-compose.yml
version: '3.8'
services:
  prism:
    image: stoplight/prism:latest
    command: mock -h 0.0.0.0 /tmp/openapi.yaml
    ports:
      - "4010:4010"
    volumes:
      - ./openapi.yaml:/tmp/openapi.yaml
```

```bash
docker-compose up
```

#### 11. CI/CDでの利用
```yaml
# .github/workflows/test.yml
name: API Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      prism:
        image: stoplight/prism:latest
        ports:
          - 4010:4010
        options: >-
          --entrypoint prism
          mock -h 0.0.0.0 /openapi.yaml
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
        env:
          API_BASE_URL: http://localhost:4010
```

## メリット

### 1. OpenAPI仕様ベース
 API仕様書がそのままモックになる
 ドキュメントとモックの乖離がない
 スキーマ駆動開発（Schema-Driven Development）を促進

### 2. 強力なバリデーション
 リクエストがOpenAPI仕様に準拠しているか自動検証
 開発中にAPI仕様違反を早期発見
 クライアント・サーバー間の契約を保証

### 3. 軽量・高速
 Node.js製で起動が速い
 メモリ消費が少ない
 追加の設定やコードが不要

### 4. 柔軟なレスポンスモード
 Static/Dynamicモードの切り替え
 複数のexampleを使い分け
 エラーケースのシミュレーション

### 5. プロキシモード
 実APIとモックを併用可能
 段階的な開発をサポート
 未実装エンドポイントのみモック

### 6. CI/CD統合
 Dockerコンテナで簡単に起動
 GitHub Actions、GitLab CI等で利用しやすい
 自動テストに組み込みやすい

### 7. 豊富なツールチェーン
 Stoplight Studioと統合
 OpenAPIエコシステムの一部
 他のOpenAPIツールと連携

## デメリット

### 1. OpenAPI依存
 OpenAPI仕様ファイルが必須
 OpenAPIがない場合は使えない
 仕様作成の手間が先行

### 2. 複雑なロジック
 動的なレスポンス生成に限界
 状態管理やビジネスロジックは実装できない
 データベースとの連携はない

### 3. WebSocket/gRPC非対応
 HTTP/REST APIに特化
 WebSocketやgRPCは未サポート
 双方向通信のモックには不向き

### 4. 録画機能なし
 実APIとの通信を記録してモック化する機能がない
 既存APIのモック化には手動でOpenAPI定義が必要
 WireMockやMountebankより自動化度が低い

### 5. UIなし
 管理画面やダッシュボードがない
 リクエスト履歴の確認はログのみ
 デバッグがコマンドライン依存

## ユースケース

### 1. スキーマ駆動開発
- API仕様書を先に定義
- フロントエンドとバックエンドを並行開発
- 仕様をベースにしたコミュニケーション

### 2. フロントエンド開発
- バックエンドAPIの開発を待たずにUI実装
- エラーケースのテスト
- デモ環境の構築

### 3. 契約テスト（Contract Testing）
- クライアントがAPI仕様を守っているか検証
- リクエストバリデーション
- 統合テストの信頼性向上

### 4. CI/CDパイプライン
- 外部APIに依存しない自動テスト
- OpenAPI仕様のバリデーション
- テスト環境の簡素化

### 5. APIドキュメント作成
- OpenAPI定義の動作確認
- 仕様書のサンプルレスポンス生成
- クライアント向けのデモAPI

## 類似ツールとの比較

| ツール | 料金 | OpenAPI対応 | バリデーション | 特徴 |
|--------|------|------------|--------------|------|
| **Prism** |  無料 |  専用 |  強力 | OpenAPI特化、軽量、バリデーション |
| MockServer |  無料 |  強力 |  あり | OpenAPI統合、UI、WebSocket |
| WireMock |  無料 |  限定的 |  なし | 成熟、柔軟なマッチング |
| MSW |  無料 |  手動 |  なし | JavaScript特化、Service Worker |
| Mountebank |  無料 |  なし |  なし | マルチプロトコル |
| Stoplight Studio |  一部有料 |  専用 |  あり | OpenAPI編集、Prism統合、GUI |

### Prismを選ぶべきケース
- OpenAPI仕様ベースの開発
- リクエストバリデーションが必要
- 軽量でシンプルなモックツールが欲しい
- スキーマ駆動開発を実践したい

### 他ツールを検討すべきケース
- 複雑なロジックや状態管理が必要 → **WireMock**、**MockServer**
- JavaScript/TypeScript中心の開発 → **MSW**
- HTTP以外のプロトコルも必要 → **Mountebank**
- GUI環境でOpenAPI編集も行いたい → **Stoplight Studio**

## ベストプラクティス

### 1. OpenAPI定義の充実
```yaml
# examplesを複数定義
responses:
  '200':
    content:
      application/json:
        examples:
          success:
            value: {id: 1, name: "Alice"}
          empty:
            value: {id: 0, name: ""}
          largeData:
            value: {id: 9999, name: "Very long name..."}
```

### 2. バリデーションの活用
```bash
# 開発中は常にバリデーションを有効化
prism mock --validate openapi.yaml

# クライアント開発でAPI仕様違反を早期発見
```

### 3. プロキシモードでの段階的開発
```bash
# 実装済みエンドポイントは実API、未実装はモック
prism proxy openapi.yaml https://staging-api.example.com
```

### 4. CI/CDでの契約テスト
```yaml
# package.json
{
  "scripts": {
    "mock": "prism mock --validate openapi.yaml",
    "test": "jest --testEnvironment=node"
  }
}
```

```javascript
// test/contract.test.js
const axios = require('axios');

test('GET /users/:id returns valid response', async () => {
  const response = await axios.get('http://localhost:4010/users/1');
  expect(response.status).toBe(200);
  expect(response.data).toHaveProperty('id');
  expect(response.data).toHaveProperty('name');
});
```

### 5. エラーケーステスト
```bash
# 各ステータスコードのレスポンスをテスト
curl -H "Prefer: code=400" http://localhost:4010/users
curl -H "Prefer: code=401" http://localhost:4010/users
curl -H "Prefer: code=403" http://localhost:4010/users
curl -H "Prefer: code=404" http://localhost:4010/users/999
curl -H "Prefer: code=500" http://localhost:4010/users
```

### 6. Docker Composeでの統合
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    environment:
      API_URL: http://prism:4010
    depends_on:
      - prism

  prism:
    image: stoplight/prism:latest
    command: mock -h 0.0.0.0 /tmp/openapi.yaml
    volumes:
      - ./openapi.yaml:/tmp/openapi.yaml
```

### 7. OpenAPI定義のバージョン管理
```
 OpenAPI定義をGitで管理
 変更履歴を追跡
 Pull Requestでの仕様レビュー
 タグでバージョン管理
```

## 公式リンク

- **公式サイト**: https://stoplight.io/open-source/prism
- **ドキュメント**: https://meta.stoplight.io/docs/prism/
- **GitHub**: https://github.com/stoplightio/prism
- **NPM**: https://www.npmjs.com/package/@stoplight/prism-cli
- **Stoplight Studio**: https://stoplight.io/studio (OpenAPI編集ツール)

## 関連ツール

- [Swagger (OpenAPI)](./Swagger.md) - OpenAPI仕様・ドキュメント生成
- [MockServer](./MockServer.md) - OpenAPI統合モックサーバー
- [WireMock](./WireMock.md) - HTTP APIモックの定番
- [MSW](./MSW.md) - JavaScript/TypeScript向けモック
- [Postman](./Postman.md) - API開発・テストツール
- [Stoplight Studio](https://stoplight.io/studio) - OpenAPI編集ツール

## まとめ

Prismは、OpenAPI仕様をベースにしたHTTP APIモックサーバーの決定版です。API仕様書から即座にモックを生成し、リクエストバリデーション、複数レスポンスモード、エラーシミュレーション、プロキシ機能を提供します。

スキーマ駆動開発（Schema-Driven Development）を実践するプロジェクトにおいて、Prismは仕様とモックの乖離を防ぎ、クライアント・サーバー間の契約を保証する強力なツールです。軽量で起動が速く、CI/CDパイプラインにも容易に統合できます。

OpenAPI仕様が整備されているプロジェクトにおいて、Prismは第一選択となるモックツールです。フロントエンド・バックエンドの並行開発や契約テストの実施において、高い価値を提供します。

