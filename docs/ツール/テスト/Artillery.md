# Artillery

## 概要

**Artillery**は、モダンなクラウドネイティブアプリケーション向けの負荷テスト・パフォーマンステストツールです。YAML形式のシナリオ定義で、HTTP/WebSocket/Socket.io/gRPCなど多様なプロトコルに対応し、CI/CD統合に最適化されています。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Artillery Software Ltd. |
| **種別** | 負荷テスト・パフォーマンステストツール |
| **ライセンス** | MPL 2.0（オープンソース） |
| **料金** | 🟡 一部無料（OSS版無料、Pro版有料） |
| **公式サイト** | https://www.artillery.io/ |
| **ドキュメント** | https://www.artillery.io/docs |

## 主な特徴

### 1. モダンなプロトコルサポート
- HTTP/HTTPS
- WebSocket
- Socket.io
- gRPC
- Kinesis（AWS）
- Lambda（AWS）

### 2. YAML形式のシナリオ定義
- コードとしてのテスト（Test as Code）
- バージョン管理容易
- 可読性高い

### 3. 分散負荷テスト（Pro版）
- AWS Fargateで大規模負荷生成
- 自動スケーリング
- グローバル分散テスト

### 4. リアルタイムメトリクス
- レスポンスタイム統計
- エラー率
- リクエスト/秒（RPS）
- カスタムメトリクス

## 使い方

### インストール

```bash
# npm経由でインストール
npm install -g artillery

# バージョン確認
artillery version

# または、npx で実行（インストール不要）
npx artillery quick --count 10 --num 3 https://example.com
```

### クイックテスト

```bash
# シンプルな負荷テスト（10ユーザー、3回リクエスト）
artillery quick --count 10 --num 3 https://example.com

# 出力例:
# Summary report @ 10:30:00(+0900)
#   Scenarios launched:  10
#   Scenarios completed: 10
#   Requests completed:  30
#   Mean response/sec: 15.2
#   Response time (msec):
#     min: 45
#     max: 120
#     median: 67
#     p95: 105
#     p99: 115
```

### YAML シナリオファイル

#### 基本的なHTTP負荷テスト

```yaml
# load-test.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60       # 60秒間実行
      arrivalRate: 10    # 1秒あたり10ユーザー到着
      name: "Warm up"
    - duration: 120
      arrivalRate: 50    # 1秒あたり50ユーザー
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100   # 1秒あたり100ユーザー
      name: "Peak load"

scenarios:
  - name: "Get users"
    flow:
      - get:
          url: "/users"
      - think: 2           # 2秒待機
      - get:
          url: "/users/{{ $randomNumber(1, 100) }}"
```

```bash
# テスト実行
artillery run load-test.yml

# JSON形式でレポート出力
artillery run --output report.json load-test.yml

# HTML レポート生成
artillery report report.json
```

#### 認証付きリクエスト

```yaml
# auth-test.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 20
  defaults:
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"

scenarios:
  - name: "Authenticated requests"
    flow:
      - get:
          url: "/protected/resource"
          headers:
            X-Custom-Header: "CustomValue"
```

#### POSTリクエスト・JSONボディ

```yaml
# post-test.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 30
      arrivalRate: 10

scenarios:
  - name: "Create user"
    flow:
      - post:
          url: "/users"
          json:
            name: "Test User {{ $randomString(5) }}"
            email: "user{{ $randomNumber(1, 10000) }}@example.com"
            age: "{{ $randomNumber(18, 65) }}"
      - think: 1
      - get:
          url: "/users"
```

#### 変数・カスタムロジック

```yaml
# variables-test.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 20
  variables:
    apiVersion: "v1"
  processor: "./helpers.js"  # カスタムロジック

scenarios:
  - name: "Complex scenario"
    flow:
      # ログイン
      - post:
          url: "/{{ apiVersion }}/auth/login"
          json:
            email: "test@example.com"
            password: "password"
          capture:
            - json: "$.token"
              as: "authToken"

      # 認証トークンを使用
      - get:
          url: "/{{ apiVersion }}/profile"
          headers:
            Authorization: "Bearer {{ authToken }}"

      # カスタム関数呼び出し
      - function: "logResponse"
```

```javascript
// helpers.js
module.exports = {
  logResponse: function(context, events, done) {
    console.log('Response captured:', context.vars.authToken);
    return done();
  }
};
```

### WebSocketテスト

```yaml
# websocket-test.yml
config:
  target: "wss://echo.websocket.org"
  phases:
    - duration: 30
      arrivalRate: 5

engines:
  ws:
    timeout: 30000

scenarios:
  - engine: ws
    flow:
      - send: "Hello from Artillery"
      - think: 1
      - send:
          payload: '{"action": "ping"}'
      - think: 2
```

### Socket.ioテスト

```yaml
# socketio-test.yml
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 10

engines:
  socketio:
    transports: ["websocket"]

scenarios:
  - engine: socketio
    flow:
      - emit:
          channel: "join"
          data: "room123"
      - think: 1
      - emit:
          channel: "message"
          data:
            text: "Hello {{ $randomString(10) }}"
            timestamp: "{{ $timestamp() }}"
```

### カスタムメトリクス

```yaml
# metrics-test.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 20
  processor: "./metrics-processor.js"

scenarios:
  - name: "Track custom metrics"
    flow:
      - get:
          url: "/products"
          capture:
            - json: "$.length"
              as: "productCount"
      - function: "recordProductCount"
```

```javascript
// metrics-processor.js
module.exports = {
  recordProductCount: function(context, events, done) {
    events.emit('counter', 'products.fetched', context.vars.productCount);
    events.emit('histogram', 'products.count', context.vars.productCount);
    return done();
  }
};
```

### CI/CD パイプライン統合

#### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Load Test
on:
  push:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Artillery
        run: npm install -g artillery

      - name: Run load test
        run: artillery run --output report.json load-test.yml

      - name: Generate HTML report
        run: artillery report report.json

      - name: Check performance threshold
        run: |
          # p95 レスポンスタイムが500ms以下を期待
          p95=$(jq '.aggregate.summaries["http.response_time"].p95' report.json)
          if (( $(echo "$p95 > 500" | bc -l) )); then
            echo "Performance degradation: p95=${p95}ms"
            exit 1
          fi

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: load-test-report
          path: report.json.html
```

### Artillery Pro（分散負荷テスト）

```bash
# Artillery Pro インストール
npm install -g artillery-pro

# AWS認証情報設定（~/.aws/credentials）
artillery-pro configure

# 分散負荷テスト実行（AWS Fargate）
artillery-pro run-fargate \
  --region us-east-1 \
  --count 10 \          # 10台のFargateタスク
  load-test.yml

# リアルタイムダッシュボード
artillery-pro dashboard
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **テスト** | 負荷テスト | API・Webアプリケーション性能評価 |
| **テスト** | ストレステスト | システム限界確認 |
| **CI/CD** | 継続的パフォーマンステスト | 毎リリース前の性能チェック |
| **導入** | 本番前性能検証 | 本番リリース前の最終負荷テスト |

## メリット

- **YAML形式**: 可読性高く、バージョン管理容易
- **多様なプロトコル**: HTTP, WebSocket, Socket.io, gRPC対応
- **CI/CD統合容易**: npm packageでシンプルに導入
- **リアルタイムメトリクス**: 即座にパフォーマンス確認
- **カスタマイズ性**: JavaScript関数でカスタムロジック追加
- **無料版充実**: オープンソース版で基本機能利用可能
- **分散負荷テスト**: Pro版でAWS Fargate利用の大規模テスト

## デメリット

- **Node.js必須**: Node.js環境が必要
- **GUIなし**: コマンドライン/YAML主体（JMeterのようなGUIなし）
- **学習曲線**: YAML記法、カスタム関数の習得が必要
- **Pro版の高コスト**: 分散テストには有料版が必要
- **ブラウザレンダリング非対応**: JavaScript実行は限定的（Playwright連携で対応可能）

## 類似ツールとの比較

| ツール | 記法 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Artillery** | YAML | 無料〜有料 | モダンAPI、CI/CD統合 |
| **k6** | JavaScript | 無料〜有料 | 開発者向け、クラウドネイティブ |
| **Gatling** | Scala | 無料〜有料 | 高負荷、Javaエコシステム |
| **JMeter** | GUI/XML | 無料 | 汎用負荷テスト、GUI重視 |

## ベストプラクティス

### 1. 段階的負荷増加

```yaml
config:
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Ramp up"
    - duration: 120
      arrivalRate: 50
      rampTo: 100      # 50→100に段階的に増加
      name: "Sustained load"
    - duration: 60
      arrivalRate: 10
      name: "Cool down"
```

### 2. シナリオの重み付け

```yaml
scenarios:
  - name: "Read operations"
    weight: 80         # 80%のユーザー
    flow:
      - get:
          url: "/products"

  - name: "Write operations"
    weight: 20         # 20%のユーザー
    flow:
      - post:
          url: "/products"
```

### 3. パフォーマンス閾値設定

```yaml
config:
  ensure:
    maxErrorRate: 1              # エラー率1%以下
    p99: 300                     # p99 < 300ms
    median: 100                  # median < 100ms

  # 閾値超過時は終了コード1で終了
```

### 4. 環境変数の活用

```yaml
config:
  target: "{{ $processEnvironment.API_URL }}"
  phases:
    - duration: "{{ $processEnvironment.TEST_DURATION }}"
      arrivalRate: "{{ $processEnvironment.ARRIVAL_RATE }}"
```

```bash
# 環境変数で設定
export API_URL="https://api.production.example.com"
export TEST_DURATION=300
export ARRIVAL_RATE=100

artillery run load-test.yml
```

## 公式リソース

- **公式サイト**: https://www.artillery.io/
- **ドキュメント**: https://www.artillery.io/docs
- **GitHub**: https://github.com/artilleryio/artillery
- **Examples**: https://github.com/artilleryio/artillery/tree/main/examples
- **コミュニティ**: https://github.com/artilleryio/artillery/discussions

## まとめ

Artilleryは、モダンなクラウドネイティブアプリケーション向けの負荷テストツールです。YAML形式のシナリオ定義で可読性が高く、CI/CD統合が容易です。HTTP、WebSocket、gRPCなど多様なプロトコルに対応し、無料版でも充実した機能を提供します。Pro版では AWS Fargate を利用した分散負荷テストも可能で、エンタープライズレベルのパフォーマンステストに対応できます。

---

**最終更新**: 2025-12-06
**対象バージョン**: Artillery v2.0+
