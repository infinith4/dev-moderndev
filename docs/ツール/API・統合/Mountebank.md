# Mountebank

## 概要

Mountebankは、複数のネットワークプロトコルに対応したオープンソースのサービス仮想化ツールです。HTTP/HTTPS、TCP、SMTP等、多様なプロトコルをモック・スタブ化でき、マイクロサービスやレガシーシステムの統合テストで威力を発揮します。インポスター（Imposter）と呼ばれる仮想サービスを定義し、スタブ（Stub）でレスポンスを返したり、プロキシ（Proxy）で実サービスと連携したりできます。Node.js製で軽量、言語非依存、シンプルなREST APIとWebUIを提供し、CI/CDパイプラインにも容易に統合できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **公式サイト** | http://www.mbtest.org/ |
| **料金** |  無料 |
| **ライセンス** | MIT License |
| **対応プロトコル** | HTTP、HTTPS、TCP、SMTP |
| **動作環境** | Node.js、Docker、スタンドアロン |
| **開発元** | Brandon Byars |
| **初版リリース** | 2013年 |
| **最新バージョン** | 2.x（2024年時点） |

## 主な機能

### 1. マルチプロトコル対応
- **HTTP/HTTPS**: RESTful API、SOAP、Webhookのモック
- **TCP**: カスタムプロトコル、バイナリ通信のモック
- **SMTP**: メール送信のモック・テスト
- **プロトコル拡張**: カスタムプロトコルの追加可能

### 2. インポスター（仮想サービス）
- **ポート指定**: 任意のポートで仮想サービスを起動
- **複数インポスター**: 異なるプロトコル・ポートで同時に複数実行
- **名前付き**: インポスターに名前を付けて管理
- **ステート管理**: インポスターごとに状態を保持

### 3. スタブ（レスポンス定義）
- **述語（Predicate）**: リクエスト条件のマッチング（equals、contains、regex等）
- **レスポンス（Response）**: 返却するデータの定義
- **優先順位**: スタブの評価順序を制御
- **繰り返し**: 同じリクエストに対して異なるレスポンスを順次返す

### 4. プロキシ
- **リクエスト転送**: 実サービスへのリクエスト中継
- **録画**: 実サービスとの通信を記録してスタブを自動生成
- **predicate generator**: 録画時に適切な述語を自動生成
- **選択的プロキシ**: 一部のリクエストのみプロキシ

### 5. レスポンス変換
- **injectionスクリプト**: JavaScriptでレスポンスを動的生成
- **テンプレート**: リクエストデータをレスポンスに埋め込み
- **装飾（Decoration）**: レスポンスを後処理で加工
- **コピー**: リクエストの一部をレスポンスにコピー

### 6. 動作シミュレーション
- **遅延**: 固定遅延でネットワーク遅延を再現
- **待機動作**: リクエスト受信後に待機してからレスポンス
- **接続エラー**: TCP接続の切断シミュレーション
- **ファイルからの読み込み**: 外部ファイルからレスポンスを取得

### 7. 管理機能
- **REST API**: インポスター、スタブの動的管理
- **Web UI**: ブラウザベースの管理画面（ポート2525）
- **リクエスト履歴**: 受信したリクエストの記録・確認
- **状態リセット**: インポスター、スタブ、履歴のクリア

## 利用方法

### インストール

#### 1. npm（Node.js環境）
```bash
npm install -g mountebank

# サーバー起動
mb
# または特定ポートで起動
mb --port 2525
```

#### 2. Docker
```bash
# Mountebankコンテナ起動
docker run -d -p 2525:2525 -p 4545:4545 --name mountebank bbyars/mountebank

# ログ確認
docker logs -f mountebank
```

#### 3. スタンドアロン（バイナリ）
```bash
# ダウンロード
curl -O https://s3.amazonaws.com/mountebank/v2.9/mountebank-v2.9.0-linux-x64.tar.gz
tar -xzf mountebank-v2.9.0-linux-x64.tar.gz

# 起動
./mountebank/mb
```

### 基本的な使い方

#### 1. HTTPインポスターの作成
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
```

```bash
# テスト: GET http://localhost:4545/users/1
curl http://localhost:4545/users/1
# レスポンス: {"id":1,"name":"Alice"}
```

#### 2. 述語（Predicate）のパターン
```json
{
  "predicates": [
    // 完全一致
    {
      "equals": {
        "method": "POST",
        "path": "/login"
      }
    },

    // 部分一致（contains）
    {
      "contains": {
        "body": "username"
      }
    },

    // 正規表現
    {
      "matches": {
        "path": "^/users/[0-9]+$"
      }
    },

    // 存在確認
    {
      "exists": {
        "headers": {
          "Authorization": true
        }
      }
    },

    // JSONPath
    {
      "jsonpath": {
        "selector": "$.user.name"
      }
    }
  ]
}
```

#### 3. 複数レスポンスの定義（繰り返し）
```json
{
  "stubs": [
    {
      "predicates": [{"equals": {"path": "/counter"}}],
      "responses": [
        {"is": {"body": "First call"}},
        {"is": {"body": "Second call"}},
        {"is": {"body": "Third call"}},
        {"is": {"body": "All subsequent calls"}}
      ]
    }
  ]
}
```

```bash
# 1回目
curl http://localhost:4545/counter  # → First call
# 2回目
curl http://localhost:4545/counter  # → Second call
# 3回目
curl http://localhost:4545/counter  # → Third call
# 4回目以降
curl http://localhost:4545/counter  # → All subsequent calls
```

#### 4. プロキシと録画
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
# プロキシ経由でGitHub APIにアクセス
curl http://localhost:4545/users/octocat

# 録画されたスタブを確認
curl http://localhost:2525/imposters/4545

# 録画を保存してproxyモードを終了
curl -X POST http://localhost:2525/imposters/4545 \
  -d '{"removeProxies": true}'
```

#### 5. Injection（JavaScriptでの動的レスポンス）
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

```bash
curl "http://localhost:4545/greet?name=Alice"
# レスポンス: Hello Alice
```

#### 6. TCPインポスター
```json
{
  "port": 3000,
  "protocol": "tcp",
  "mode": "text",
  "stubs": [
    {
      "predicates": [
        {"contains": {"data": "PING"}}
      ],
      "responses": [
        {"is": {"data": "PONG\n"}}
      ]
    }
  ]
}
```

```bash
# TCPクライアントでテスト
echo "PING" | nc localhost 3000
# レスポンス: PONG
```

#### 7. SMTPインポスター
```json
{
  "port": 2525,
  "protocol": "smtp",
  "stubs": [
    {
      "responses": [
        {
          "is": {}
        }
      ]
    }
  ]
}
```

```bash
# メール送信テスト（telnet）
telnet localhost 2525
EHLO localhost
MAIL FROM:<sender@example.com>
RCPT TO:<recipient@example.com>
DATA
Subject: Test
Test email
.
QUIT

# 受信したメールを確認
curl http://localhost:2525/imposters/2525
```

#### 8. 遅延のシミュレーション
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

#### 9. ファイルからのレスポンス
```json
{
  "responses": [
    {
      "is": {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "_behaviors": {
          "copy": [{
            "from": "path",
            "into": "TOKEN",
            "using": {"method": "regex", "selector": "/users/(.+)"}
          }],
          "lookup": [{
            "key": {
              "from": "TOKEN",
              "index": 1
            },
            "datasource": {
              "csv": {
                "path": "users.csv",
                "keyColumn": "id"
              }
            },
            "into": "${row}"
          }]
        },
        "body": "${row}"
      }
    }
  ]
}
```

#### 10. Web UIの利用
```bash
# ブラウザでアクセス
# http://localhost:2525

# UIで以下が可能:
# - インポスター一覧の表示
# - リクエスト履歴の確認
# - スタブの可視化
# - インポスターの作成・削除（GUIなし、JSONビューのみ）
```

## メリット

### 1. マルチプロトコル対応
 HTTP以外のTCP、SMTPもサポート
 レガシーシステムやカスタムプロトコルのテストに対応
 プロトコル拡張で任意のプロトコルを追加可能

### 2. 軽量・シンプル
 Node.js製で起動が速い
 設定がJSON形式でシンプル
 追加の依存関係が少ない

### 3. プロキシと録画機能
 実サービスとの通信を記録してスタブを自動生成
 predicate generatorで適切なマッチング条件を自動設定
 レガシーシステムのモック化が容易

### 4. 言語非依存
 REST APIで操作するためどの言語からでも利用可能
 Java、Python、Ruby、.NET等あらゆる言語に対応
 CI/CDパイプラインに容易に統合

### 5. Injection機能
 JavaScriptで複雑なロジックを実装可能
 動的なレスポンス生成が柔軟
 外部データソース（CSV、JSON）との連携

### 6. 状態管理
 インポスターごとに状態を保持
 繰り返しレスポンスで異なる応答を返せる
 ステートフルなAPIのシミュレーションが可能

## デメリット

### 1. Web UIの限界
 UIは主に閲覧用で編集機能が限定的
 GUIでのスタブ作成ができない
 デバッグ機能が弱い

### 2. ドキュメント
 公式ドキュメントがやや古い
 複雑なユースケースの例が少ない
 日本語情報がほとんどない

### 3. OpenAPI統合
 OpenAPI仕様からの自動生成機能がない
 スキーマバリデーションが弱い
 手動でスタブを定義する必要がある

### 4. エラーハンドリング
 スタブ定義のエラーメッセージが分かりにくい
 述語のマッチング失敗時のデバッグが難しい
 Injection内のエラーが見つけにくい

### 5. コミュニティ
 WireMockやMockServerに比べてコミュニティが小さい
 サードパーティプラグインがほとんどない
 StackOverflowでの質問数が少ない

## ユースケース

### 1. マルチプロトコルテスト
- HTTP、TCP、SMTPを組み合わせたシステムのテスト
- レガシープロトコルのモック
- IoTデバイス通信のシミュレーション

### 2. サービス仮想化
- 複数のマイクロサービスをモック化
- 外部APIに依存しない統合テスト
- 並行開発の促進

### 3. メール送信テスト
- SMTP経由のメール送信をモック
- メール内容の検証
- メール送信エラーのシミュレーション

### 4. レガシーシステム統合
- 古いTCPベースシステムのモック
- プロキシモードで実システムと並行稼働
- 段階的な移行のサポート

### 5. CI/CDパイプライン
- 外部依存を排除した自動テスト
- 軽量で起動が速い
- Docker対応でコンテナ化が容易

## 類似ツールとの比較

| ツール | 料金 | プロトコル | UI | 特徴 |
|--------|------|-----------|----|----|
| **Mountebank** |  無料 | HTTP/TCP/SMTP |  簡易 | マルチプロトコル、軽量 |
| WireMock |  無料 | HTTP/HTTPS |  なし | HTTP特化、成熟 |
| MockServer |  無料 | HTTP/HTTPS/WS |  強力 | OpenAPI統合、UI充実 |
| MSW |  無料 | HTTP |  なし | JavaScript特化、ブラウザ |
| Hoverfly |  無料 | HTTP |  あり | サービス仮想化、Go製 |

### Mountebankを選ぶべきケース
- HTTP以外のプロトコル（TCP、SMTP）のモックが必要
- 軽量でシンプルなツールが欲しい
- レガシーシステムのモック化
- 言語非依存のツールが必要

### 他ツールを検討すべきケース
- HTTP APIのみで充分 → **WireMock**
- OpenAPI統合が必要 → **MockServer**
- JavaScript/TypeScript開発 → **MSW**
- Go言語環境 → **Hoverfly**

## ベストプラクティス

### 1. インポスター定義の管理
```bash
# JSON定義ファイルとして保存
# imposters/users-api.json
{
  "port": 4545,
  "protocol": "http",
  "stubs": [...]
}

# ファイルから起動
mb --configfile imposters/users-api.json
```

### 2. CI/CD統合
```yaml
# .gitlab-ci.yml
test:
  services:
    - bbyars/mountebank:latest
  before_script:
    - curl -X POST http://mountebank:2525/imposters -d @imposters.json
  script:
    - npm test
```

### 3. Dockerでの利用
```yaml
# docker-compose.yml
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

### 4. 述語の優先順位
```json
// より詳細な述語を先に定義
{
  "stubs": [
    {
      "predicates": [
        {"equals": {"path": "/users/1"}},
        {"equals": {"method": "DELETE"}}
      ],
      "responses": [{"is": {"statusCode": 403}}]
    },
    {
      "predicates": [{"equals": {"path": "/users/1"}}],
      "responses": [{"is": {"statusCode": 200, "body": "..."}}]
    }
  ]
}
```

### 5. Injectionのセキュリティ
```bash
# Injection機能を有効化（デフォルトは無効）
mb --allowInjection

# 本番環境では無効化を推奨
mb --allowInjection false
```

### 6. リクエスト履歴の管理
```bash
# インポスターのリクエスト履歴を取得
curl http://localhost:2525/imposters/4545

# 履歴をクリア
curl -X DELETE http://localhost:2525/imposters/4545/requests
```

### 7. ログレベル調整
```bash
# デバッグログ
mb --loglevel debug

# 本番: 最小ログ
mb --loglevel error
```

## 公式リンク

- **公式サイト**: http://www.mbtest.org/
- **ドキュメント**: http://www.mbtest.org/docs/api/overview
- **GitHub**: https://github.com/bbyars/mountebank
- **Docker Hub**: https://hub.docker.com/r/bbyars/mountebank
- **Google Group**: https://groups.google.com/g/mountebank-discuss

## 関連ツール

- [WireMock](./WireMock.md) - HTTP APIモックの定番
- [MockServer](./MockServer.md) - OpenAPI統合モックサーバー
- [MSW](./MSW.md) - JavaScript/TypeScript向けモック
- [Mockito](./Mockito.md) - Javaメソッドレベルモック
- [Postman](./Postman.md) - API開発・テストツール

## まとめ

Mountebankは、HTTP/HTTPS、TCP、SMTPなど複数のプロトコルに対応したサービス仮想化ツールです。Node.js製で軽量・シンプルながら、プロキシ/録画機能、Injection機能、状態管理など、高度な機能を備えています。

特にHTTP以外のプロトコルをモック化する必要がある場合や、レガシーシステムとの統合テストにおいて、Mountebankは他のツールにはない強力な選択肢となります。言語非依存でREST APIベースの操作により、どの開発環境でも容易に統合できます。

Web UIやドキュメントにやや課題はあるものの、マルチプロトコル対応と柔軟なモック機能により、複雑なシステム環境のテストに最適なツールです。

