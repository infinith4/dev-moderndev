# Mountebank

## 概要

Mountebankは、複数のネットワークプロトコルに対応したオープンソースのサービス仮想化ツールです。HTTP/HTTPS、TCP、SMTP等、多様なプロトコルをモック・スタブ化でき、マイクロサービスやレガシーシステムの統合テストで威力を発揮します。Node.js製で軽量、言語非依存、シンプルなREST APIとWebUIを提供し、CI/CDパイプラインにも容易に統合できます。

## 主な特徴

| 項目 | 内容 |
|------|------|
| マルチプロトコル | HTTP/HTTPS、TCP、SMTPに対応 |
| 軽量・高速 | Node.js製で起動が速く追加依存が少ない |
| 言語非依存 | REST APIで操作するためどの言語からでも利用可能 |
| プロキシ・録画 | 実サービスとの通信を記録してスタブを自動生成 |
| Injection | JavaScriptで動的なレスポンスを生成可能 |
| 状態管理 | インポスターごとに状態を保持し、ステートフルなAPIをシミュレート |
| 無料 | MIT License、オープンソース |

## 主な機能

### インポスター（仮想サービス）

| 機能 | 説明 |
|------|------|
| ポート指定 | 任意のポートで仮想サービスを起動 |
| 複数インポスター | 異なるプロトコル・ポートで同時に複数実行 |
| 名前付き管理 | インポスターに名前を付けて管理 |
| ステート管理 | インポスターごとに状態を保持 |

### スタブ（レスポンス定義）

| 機能 | 説明 |
|------|------|
| 述語（Predicate） | equals、contains、regex等でリクエスト条件をマッチング |
| レスポンス | 返却するデータの定義 |
| 優先順位 | スタブの評価順序を制御 |
| 繰り返し | 同じリクエストに対して異なるレスポンスを順次返す |

### プロキシ・録画

| 機能 | 説明 |
|------|------|
| リクエスト転送 | 実サービスへのリクエスト中継 |
| 録画 | 実サービスとの通信を記録してスタブを自動生成 |
| predicate generator | 録画時に適切な述語を自動生成 |
| 選択的プロキシ | 一部のリクエストのみプロキシ |

### レスポンス変換

| 機能 | 説明 |
|------|------|
| Injection | JavaScriptでレスポンスを動的生成 |
| テンプレート | リクエストデータをレスポンスに埋め込み |
| 装飾（Decoration） | レスポンスを後処理で加工 |
| コピー | リクエストの一部をレスポンスにコピー |

## インストールとセットアップ

公式URL:
- [Mountebank 公式サイト](http://www.mbtest.org/)
- [GitHub リポジトリ](https://github.com/bbyars/mountebank)
- [Docker Hub](https://hub.docker.com/r/bbyars/mountebank)

## 基本的な使い方

### 1. インストールと起動

```bash
# npm（Node.js環境）
npm install -g mountebank
mb --port 2525

# Docker
docker run -d -p 2525:2525 -p 4545:4545 --name mountebank bbyars/mountebank

# スタンドアロン（バイナリ）
curl -O https://s3.amazonaws.com/mountebank/v2.9/mountebank-v2.9.0-linux-x64.tar.gz
tar -xzf mountebank-v2.9.0-linux-x64.tar.gz
./mountebank/mb
```

### 2. HTTPインポスターの作成

```bash
# POST /imposters でインポスターを作成
curl -X POST http://localhost:2525/imposters \
  -H "Content-Type: application/json" \
  -d '{
    "port": 4545,
    "protocol": "http",
    "stubs": [
      {
        "predicates": [
          {
            "equals": {
              "method": "GET",
              "path": "/users/1"
            }
          }
        ],
        "responses": [
          {
            "is": {
              "statusCode": 200,
              "headers": {
                "Content-Type": "application/json"
              },
              "body": "{\"id\":1,\"name\":\"Alice\"}"
            }
          }
        ]
      }
    ]
  }'

# テスト
curl http://localhost:4545/users/1
# レスポンス: {"id":1,"name":"Alice"}
```

### 3. 述語（Predicate）のパターン

```json
{
  "predicates": [
    {"equals": {"method": "POST", "path": "/login"}},
    {"contains": {"body": "username"}},
    {"matches": {"path": "^/users/[0-9]+$"}},
    {"exists": {"headers": {"Authorization": true}}},
    {"jsonpath": {"selector": "$.user.name"}}
  ]
}
```

### 4. プロキシと録画

```json
{
  "port": 4545,
  "protocol": "http",
  "stubs": [
    {
      "responses": [
        {
          "proxy": {
            "to": "https://api.github.com",
            "mode": "proxyAlways",
            "predicateGenerators": [
              {"matches": {"method": true, "path": true}}
            ]
          }
        }
      ]
    }
  ]
}
```

```bash
# プロキシ経由でアクセス
curl http://localhost:4545/users/octocat

# 録画されたスタブを確認
curl http://localhost:2525/imposters/4545

# 録画を保存してproxyモードを終了
curl -X POST http://localhost:2525/imposters/4545 \
  -d '{"removeProxies": true}'
```

### 5. Injection（動的レスポンス）

```json
{
  "stubs": [
    {
      "responses": [
        {
          "inject": "function (request, state, logger) { return { statusCode: 200, body: 'Hello ' + request.query.name }; }"
        }
      ]
    }
  ]
}
```

### 6. 遅延のシミュレーション

```json
{
  "responses": [
    {
      "is": {
        "statusCode": 200,
        "body": "Slow response"
      },
      "_behaviors": {
        "wait": 3000
      }
    }
  ]
}
```

## CI/CD 統合

### GitHub Actions

```yaml
name: Integration Tests

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mountebank:
        image: bbyars/mountebank:latest
        ports:
          - 2525:2525
          - 4545:4545
    steps:
      - uses: actions/checkout@v3
      - name: Setup imposters
        run: curl -X POST http://localhost:2525/imposters -d @imposters.json
      - name: Run tests
        run: npm test
```

### GitLab CI

```yaml
integration_test:
  stage: test
  services:
    - bbyars/mountebank:latest
  before_script:
    - curl -X POST http://mountebank:2525/imposters -d @imposters.json
  script:
    - npm test
```

## Docker での使用

### Dockerfile 例

```dockerfile
FROM node:24-alpine
RUN npm install -g mountebank
EXPOSE 2525 4545
CMD ["mb", "--port", "2525"]
```

### docker-compose.yml 例

```yaml
version: '3.8'
services:
  mountebank:
    image: bbyars/mountebank
    ports:
      - "2525:2525"
      - "4545:4545"
    volumes:
      - ./imposters:/imposters
    command: mb --configfile /imposters/imposters.ejs --allowInjection
```

## 他ツールとの比較

### Mountebank vs WireMock

| 機能 | Mountebank | WireMock |
|------|------------|----------|
| プロトコル | HTTP/TCP/SMTP | HTTP/HTTPS |
| 言語 | Node.js | Java |
| UIダッシュボード | 簡易 | なし |
| コミュニティ | 中規模 | 大規模 |
| OpenAPI統合 | なし | 限定的 |

### Mountebank vs MockServer

| 機能 | Mountebank | MockServer |
|------|------------|------------|
| プロトコル | HTTP/TCP/SMTP | HTTP/HTTPS/WS |
| OpenAPI統合 | なし | 強力 |
| UI | 簡易 | 強力 |
| 学習曲線 | 低い | 中程度 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| マルチプロトコルテスト | HTTP以外も含むシステムのテスト | TCP、SMTPを組み合わせたモック |
| サービス仮想化 | 外部依存の排除 | マイクロサービス間の依存をモック化 |
| メール送信テスト | SMTP経由のメール検証 | SMTPインポスターでメール内容を検証 |
| レガシーシステム統合 | 古いプロトコルのモック | TCPベースシステムのモック化 |
| CI/CDパイプライン | 外部依存のない自動テスト | Docker対応で軽量なテスト環境構築 |

## ベストプラクティス

### 1. インポスター定義の管理

- JSON定義ファイルとして保存し、バージョン管理する
- `mb --configfile` で定義ファイルから起動する
- 環境別の定義ファイルを用意する

### 2. 述語の優先順位

- より詳細な述語を先に定義する
- デフォルトのフォールバックスタブを最後に配置する
- 正規表現マッチは完全一致より後に配置する

### 3. Injectionのセキュリティ

- `--allowInjection` は開発・テスト環境のみで有効化する
- 本番環境では無効化を推奨する
- Injection内のコードは最小限に保つ

### 4. ログ管理

- 開発時は `--loglevel debug` で詳細ログを取得する
- CI/CD環境では `--loglevel error` でノイズを削減する

## トラブルシューティング

### よくある問題と解決策

#### 1. インポスターのポートが使用済み

```
原因: 指定したポートが既に使用されている
解決策:
- 別のポートを指定する
- 既存のプロセスを終了してから起動する
```

#### 2. 述語がマッチしない

```
原因: 述語の条件が正しくない、または複数のスタブが競合
解決策:
- リクエスト履歴を確認する（GET /imposters/{port}）
- 述語の順序を見直す（詳細な条件を先に配置）
- --loglevel debug でマッチングの詳細を確認する
```

#### 3. Injectionが動作しない

```
原因: --allowInjection オプションが未指定
解決策:
- mb --allowInjection で起動する
- Docker使用時はcommandに --allowInjection を追加する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: http://www.mbtest.org/
- ドキュメント: http://www.mbtest.org/docs/api/overview

### コミュニティ
- GitHub: https://github.com/bbyars/mountebank
- Google Group: https://groups.google.com/g/mountebank-discuss

### チュートリアル
- Getting Started: http://www.mbtest.org/docs/gettingStarted

## まとめ

Mountebankは、以下の場面で特に有用です:

1. **マルチプロトコルテスト** - HTTP以外のTCP、SMTPを含むシステムのモック化
2. **レガシーシステム統合** - 古いプロトコルのモックとプロキシ録画による段階的移行
3. **CI/CDパイプライン** - 軽量でDocker対応のため、外部依存のない自動テスト環境を構築

Node.js製で軽量・シンプルながら高度な機能を備え、マルチプロトコル対応が必要な統合テストにおいて強力な選択肢となる。
