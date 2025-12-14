# ApacheBench (ab)

## 概要

**ApacheBench（ab）**は、Apache HTTP Serverに同梱されるコマンドラインベースの負荷テストツールです。シンプルなHTTP/HTTPS負荷テストを素早く実行でき、Webサーバーのパフォーマンス測定に広く使用されています。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Apache Software Foundation |
| **種別** | HTTPベンチマークツール |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://httpd.apache.org/docs/current/programs/ab.html |
| **ドキュメント** | https://httpd.apache.org/docs/current/programs/ab.html |

## 主な特徴

### 1. シンプル・軽量
- 1コマンドで負荷テスト実行
- インストール不要（多くのLinuxディストリビューションに標準搭載）
- GUI不要、CLI完結

### 2. 基本的な負荷テスト機能
- 同時接続数指定
- リクエスト総数指定
- Keep-Alive対応
- POST/PUT/DELETEリクエスト対応

### 3. 即座に結果表示
- レスポンスタイム統計
- リクエスト/秒（RPS）
- 転送速度
- パーセンタイル分析

## 使い方

### インストール

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install apache2-utils

# CentOS/RHEL
sudo yum install httpd-tools

# macOS（Homebrewの場合）
# 標準でインストール済みの場合が多い
which ab  # /usr/sbin/ab

# Homebrewでインストール（必要な場合）
brew install httpd
```

### 基本的な使い方

#### シンプルな負荷テスト

```bash
# 100リクエスト、同時接続10
ab -n 100 -c 10 http://example.com/

# オプション:
# -n: リクエスト総数
# -c: 同時接続数
```

**出力例**:

```text
This is ApacheBench, Version 2.3
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking example.com (be patient).....done

Server Software:        nginx/1.18.0
Server Hostname:        example.com
Server Port:            80

Document Path:          /
Document Length:        1256 bytes

Concurrency Level:      10
Time taken for tests:   2.145 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      142400 bytes
HTML transferred:       125600 bytes
Requests per second:    46.62 [#/sec] (mean)
Time per request:       214.508 [ms] (mean)
Time per request:       21.451 [ms] (mean, across all concurrent requests)
Transfer rate:          64.82 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        5   10   3.2      9      18
Processing:    89  198  52.1    185     356
Waiting:       85  190  50.3    178     348
Total:         98  208  52.8    196     365

Percentage of the requests served within a certain time (ms)
  50%    196
  66%    215
  75%    235
  80%    251
  90%    289
  95%    325
  98%    356
  99%    365
 100%    365 (longest request)
```

### よく使うオプション

#### タイムアウト設定

```bash
# タイムアウト30秒
ab -n 100 -c 10 -s 30 http://example.com/
```

#### Keep-Alive有効化

```bash
# Keep-Aliveで接続再利用
ab -n 100 -c 10 -k http://example.com/
```

#### カスタムヘッダー

```bash
# Authorization ヘッダー追加
ab -n 100 -c 10 \
   -H "Authorization: Bearer YOUR_TOKEN" \
   http://example.com/api/users
```

#### POSTリクエスト

```bash
# JSON POSTリクエスト
ab -n 100 -c 10 \
   -p post_data.json \
   -T "application/json" \
   http://example.com/api/users

# post_data.json
{
  "name": "Test User",
  "email": "test@example.com"
}
```

#### 結果をファイルに保存

```bash
# TSV形式で保存
ab -n 100 -c 10 -g results.tsv http://example.com/

# GnuPlotでグラフ化可能
gnuplot
> plot "results.tsv" using 9 with lines title "Response Time"
```

### より高度な使い方

#### 複数パターンのテスト

```bash
#!/bin/bash
# load_test.sh

URL="http://example.com/"
REQUESTS=1000

# 同時接続数を変えてテスト
for CONCURRENCY in 10 50 100 200; do
    echo "Testing with concurrency: $CONCURRENCY"
    ab -n $REQUESTS -c $CONCURRENCY -k $URL > "result_c${CONCURRENCY}.txt"
    echo "---"
done

# 結果サマリー抽出
for file in result_c*.txt; do
    echo "=== $file ==="
    grep "Requests per second" $file
    grep "Time per request" $file | head -1
    grep "Failed requests" $file
    echo ""
done
```

#### ベンチマークスクリプト

```bash
#!/bin/bash
# benchmark.sh

# 設定
TARGET_URL="http://localhost:8080/api/health"
DURATION=60  # 60秒間テスト
CONCURRENCY=50

# 計算（60秒で継続的にリクエスト）
# 仮に1リクエスト=100msとすると、1秒で500リクエスト必要
TOTAL_REQUESTS=$((DURATION * 500))

echo "Starting benchmark..."
echo "URL: $TARGET_URL"
echo "Duration: ${DURATION}s"
echo "Concurrency: $CONCURRENCY"
echo "Total Requests: $TOTAL_REQUESTS"
echo ""

ab -n $TOTAL_REQUESTS \
   -c $CONCURRENCY \
   -k \
   -g benchmark_results.tsv \
   $TARGET_URL

# 結果分析
echo ""
echo "=== Benchmark Results ==="
grep "Requests per second" benchmark_results.txt
grep "50%" benchmark_results.txt
grep "95%" benchmark_results.txt
grep "99%" benchmark_results.txt
grep "Failed requests" benchmark_results.txt
```

### 認証付きリクエスト

#### Basic認証

```bash
ab -n 100 -c 10 \
   -A username:password \
   http://example.com/protected/
```

#### Cookie認証

```bash
ab -n 100 -c 10 \
   -C "session_id=abc123; user_token=xyz789" \
   http://example.com/dashboard/
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **テスト** | 負荷テスト | Webサーバー・APIパフォーマンス測定 |
| **テスト** | ベンチマーク | 設定変更前後の性能比較 |
| **導入** | 本番前性能検証 | リリース前の簡易負荷テスト |

## メリット

- **シンプル**: 1コマンドで即座にテスト実行
- **軽量**: リソース消費が少ない
- **標準搭載**: 多くのLinux環境で追加インストール不要
- **無料**: ライセンス費用不要
- **スクリプト化容易**: シェルスクリプトで自動化可能
- **結果の即時確認**: リアルタイムでパフォーマンス把握

## デメリット

- **機能制限**: 複雑なシナリオには不向き
- **単一URL**: 1回のテストで1URLのみ
- **JavaScript非対応**: ブラウザレンダリングなし
- **詳細分析機能なし**: JMeterやGatlingに比べて分析機能が貧弱
- **並列テストなし**: 複数エンドポイントの同時テストは別プロセス起動が必要
- **グラフ表示なし**: 結果はテキストのみ（GnuPlot等で別途可視化）

## 類似ツールとの比較

| ツール | 特徴 | コスト | 適用場面 |
|--------|------|--------|----------|
| **ApacheBench (ab)** | シンプル、1コマンド | 無料 | 簡易負荷テスト、CI/CD統合 |
| **Apache JMeter** | GUI、複雑シナリオ | 無料 | 詳細な負荷テストシナリオ |
| **wrk** | マルチスレッド、Luaスクリプト | 無料 | 高負荷生成、カスタマイズ |
| **k6** | JavaScript、開発者向け | 無料〜有料 | CI/CD統合、クラウド連携 |

## ベストプラクティス

### 1. CI/CDパイプライン統合

```yaml
# .github/workflows/performance.yml
name: Performance Test
on: [push]
jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Start application
        run: docker-compose up -d

      - name: Wait for app
        run: sleep 10

      - name: Run ApacheBench
        run: |
          ab -n 1000 -c 50 http://localhost:8080/ > ab_result.txt

      - name: Check performance
        run: |
          # 平均レスポンスタイムが200ms以下を期待
          AVG_TIME=$(grep "Time per request" ab_result.txt | head -1 | awk '{print $4}')
          if (( $(echo "$AVG_TIME > 200" | bc -l) )); then
            echo "Performance degradation: ${AVG_TIME}ms"
            exit 1
          fi
```

### 2. 段階的負荷増加テスト

```bash
#!/bin/bash
# ramp_up_test.sh

URL="http://localhost:8080/api/users"

for c in 1 5 10 25 50 100; do
    echo "=== Concurrency: $c ==="
    ab -n 500 -c $c -k $URL | grep -E "(Requests per second|Time per request|Failed)"
    echo ""
    sleep 5  # 次のテストまで待機
done
```

### 3. 結果の比較分析

```bash
#!/bin/bash
# compare_results.sh

# 設定変更前
echo "Before optimization:"
ab -n 1000 -c 50 http://localhost:8080/ > before.txt

# 設定変更（例: Nginxチューニング）
# ...

# 設定変更後
echo "After optimization:"
ab -n 1000 -c 50 http://localhost:8080/ > after.txt

# 比較
echo "=== Comparison ==="
echo "Before:"
grep "Requests per second" before.txt
echo "After:"
grep "Requests per second" after.txt
```

### 4. ウォームアップ実行

```bash
# ウォームアップ（キャッシュ準備）
ab -n 10 -c 1 http://localhost:8080/

# 本番テスト
ab -n 1000 -c 50 -k http://localhost:8080/
```

## 公式リソース

- **公式ドキュメント**: https://httpd.apache.org/docs/current/programs/ab.html
- **Apache HTTP Server**: https://httpd.apache.org/
- **マニュアルページ**: `man ab`

## まとめ

ApacheBench（ab）は、シンプルで軽量なHTTP負荷テストツールです。複雑なシナリオには不向きですが、Webサーバーの基本性能測定やCI/CDパイプラインでの性能チェックには最適です。1コマンドで即座にテスト実行でき、スクリプト化も容易なため、開発者が日常的に使用する負荷テストツールとして広く採用されています。

---

**最終更新**: 2025-12-06
**対象バージョン**: ApacheBench 2.3+
