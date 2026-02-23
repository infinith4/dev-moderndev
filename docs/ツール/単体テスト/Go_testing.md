# Go testing

## 概要

Go testingは、Go言語に標準搭載されているテスティングパッケージ（`testing`）および`go test`コマンドである。外部ライブラリのインストールなしで、単体テスト、ベンチマーク、ファジングテスト、サンプルテスト（Example）を実行できる。テーブル駆動テスト（Table-Driven Tests）パターンやサブテスト（`t.Run`）による構造化、カバレッジ計測、競合状態検出（Race Detector）など、Go言語の哲学であるシンプルさと実用性を体現したテスト基盤である。`go test`コマンドはCI/CDパイプラインに容易に統合でき、Go言語プロジェクトのテスト標準として広く利用されている。

## 主な機能

### 1. 単体テスト（Test関数）
- **Test関数**: `func TestXxx(t *testing.T)` 形式のテスト関数
- **t.Error/t.Errorf**: テスト失敗の報告（実行は継続）
- **t.Fatal/t.Fatalf**: テスト失敗の報告（即座に中断）
- **t.Log/t.Logf**: テストログの出力
- **t.Skip**: テストのスキップ

### 2. サブテスト
- **t.Run**: ネストされたサブテストの実行
- **名前付きテスト**: サブテスト名による特定テストの実行
- **並列実行**: `t.Parallel()` によるサブテストの並列化
- **フィルタリング**: `-run` フラグでサブテスト名によるフィルタ

### 3. テーブル駆動テスト
- **構造体スライス**: テストケースを構造体のスライスで定義
- **パラメータ化**: 入力値と期待値のペアを網羅的に定義
- **ループ実行**: `for range` でテストケースを反復実行
- **サブテスト連携**: `t.Run` と組み合わせて個別テスト名を付与

### 4. ベンチマーク
- **Benchmark関数**: `func BenchmarkXxx(b *testing.B)` 形式
- **b.N**: フレームワークが決定する反復回数
- **b.ResetTimer**: タイマーリセットによるセットアップ除外
- **b.ReportAllocs**: メモリアロケーション統計の出力
- **サブベンチマーク**: `b.Run` によるネスト

### 5. ファジングテスト
- **Fuzz関数**: `func FuzzXxx(f *testing.F)` 形式（Go 1.18以降）
- **f.Add**: シードコーパスの追加
- **f.Fuzz**: ファジング対象関数の定義
- **自動入力生成**: ランダムな入力値による境界値テスト

### 6. Exampleテスト
- **Example関数**: `func ExampleXxx()` 形式
- **Output コメント**: `// Output:` による期待出力の定義
- **ドキュメント連携**: `go doc` でドキュメントとして表示

### 7. テストユーティリティ
- **TestMain**: テスト全体の前処理・後処理
- **t.Cleanup**: テスト終了時のクリーンアップ登録
- **t.TempDir**: テスト用一時ディレクトリの自動作成・削除
- **t.Helper**: ヘルパー関数のスタックトレース調整
- **t.Setenv**: テスト用環境変数の一時設定（Go 1.17以降）

### 8. カバレッジ・競合検出
- **-cover**: コードカバレッジの計測
- **-coverprofile**: カバレッジプロファイルの出力
- **-race**: 競合状態検出（Race Detector）
- **go tool cover**: カバレッジレポートの可視化

## 利用方法

### 基本的なテスト

```go
// math.go
package math

func Add(a, b int) int {
    return a + b
}

func Divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}
```

```go
// math_test.go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

func TestDivide(t *testing.T) {
    result, err := Divide(10, 2)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result != 5.0 {
        t.Errorf("Divide(10, 2) = %f; want 5.0", result)
    }
}

func TestDivideByZero(t *testing.T) {
    _, err := Divide(10, 0)
    if err == nil {
        t.Fatal("expected error for division by zero")
    }
}
```

### テーブル駆動テスト

```go
// math_test.go
func TestAddTableDriven(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -2, -3},
        {"zero", 0, 0, 0},
        {"mixed signs", -1, 5, 4},
        {"large numbers", 1000000, 2000000, 3000000},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

func TestDivideTableDriven(t *testing.T) {
    tests := []struct {
        name      string
        a, b      float64
        expected  float64
        expectErr bool
    }{
        {"normal division", 10, 2, 5.0, false},
        {"decimal result", 7, 2, 3.5, false},
        {"divide by zero", 10, 0, 0, true},
        {"negative division", -10, 2, -5.0, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Divide(tt.a, tt.b)
            if tt.expectErr {
                if err == nil {
                    t.Fatal("expected error but got nil")
                }
                return
            }
            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if result != tt.expected {
                t.Errorf("Divide(%f, %f) = %f; want %f",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### 並列テスト

```go
func TestAddParallel(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"case1", 1, 2, 3},
        {"case2", 10, 20, 30},
        {"case3", -5, 5, 0},
    }

    for _, tt := range tests {
        tt := tt // ループ変数のキャプチャ（Go 1.22未満で必要）
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### ベンチマーク

```go
// math_bench_test.go
package math

import "testing"

func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(100, 200)
    }
}

func BenchmarkDivide(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Divide(100, 3)
    }
}

func BenchmarkAddWithAllocs(b *testing.B) {
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        Add(100, 200)
    }
}
```

### ファジングテスト

```go
// math_fuzz_test.go
package math

import "testing"

func FuzzDivide(f *testing.F) {
    // シードコーパス
    f.Add(10.0, 2.0)
    f.Add(0.0, 1.0)
    f.Add(-5.0, 3.0)

    f.Fuzz(func(t *testing.T, a, b float64) {
        result, err := Divide(a, b)
        if b == 0 {
            if err == nil {
                t.Error("expected error for zero divisor")
            }
            return
        }
        if err != nil {
            t.Errorf("unexpected error: %v", err)
        }
        // 逆算による検証
        if b != 0 && result*b != a {
            // 浮動小数点の精度を考慮
        }
    })
}
```

### TestMainとヘルパー

```go
// setup_test.go
package math

import (
    "os"
    "testing"
)

func TestMain(m *testing.M) {
    // テスト全体の前処理
    setup()

    // テスト実行
    code := m.Run()

    // テスト全体の後処理
    teardown()

    os.Exit(code)
}

func setup() {
    // データベース接続、テストデータ投入等
}

func teardown() {
    // リソース解放、テストデータ削除等
}

// ヘルパー関数
func assertEqual(t *testing.T, got, want int) {
    t.Helper() // テスト失敗時に呼び出し元の行番号を表示
    if got != want {
        t.Errorf("got %d; want %d", got, want)
    }
}
```

### テスト実行コマンド

```bash
# 基本実行
go test ./...

# 詳細出力
go test -v ./...

# 特定テストのみ実行
go test -run TestAdd ./...
go test -run TestAdd/positive ./...

# カバレッジ計測
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html

# 競合状態検出
go test -race ./...

# ベンチマーク実行
go test -bench=. ./...
go test -bench=BenchmarkAdd -benchmem ./...

# ファジングテスト
go test -fuzz=FuzzDivide -fuzztime=30s ./...

# タイムアウト設定
go test -timeout 60s ./...

# キャッシュ無効化
go test -count=1 ./...

# ショートモード
go test -short ./...
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/go-test.yml
name: Go Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.23'
      - name: Run tests
        run: go test -v -race -coverprofile=coverage.out ./...
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.out
      - name: Run benchmarks
        run: go test -bench=. -benchmem ./... | tee bench.txt
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Go testing** | 無料 | Go標準ライブラリ、BSD License |

## メリット

1. **標準搭載**: 外部依存なしでテスト・ベンチマーク・ファジングが実行可能
2. **シンプルな規約**: `_test.go`ファイルと`Test`プレフィックスのみの明快な規約
3. **テーブル駆動テスト**: 構造体スライスによる網羅的なテストケース管理パターン
4. **並列テスト**: `t.Parallel()`で容易にテストの並列実行が可能
5. **競合検出**: `-race`フラグで並行処理の競合状態を自動検出
6. **カバレッジ内蔵**: 追加ツール不要でコードカバレッジを計測・可視化
7. **ファジング内蔵**: Go 1.18以降、標準でファジングテストが可能
8. **高速実行**: コンパイル言語の利点を活かした高速なテスト実行
9. **go testコマンド**: 統一されたCLIでテスト・ベンチマーク・カバレッジを一元管理
10. **ドキュメント連携**: Example関数が`go doc`のドキュメントとして自動反映

## デメリット

1. **アサーション不足**: 標準ライブラリにassert/expect関数がなく、if文での記述が冗長
2. **モック非標準**: モック機能は標準搭載されておらず、外部ライブラリ（gomock等）が必要
3. **テストスイート非対応**: xUnit形式のテストスイート・セットアップ/ティアダウンが標準にない
4. **エラーメッセージ**: テスト失敗時のメッセージを手動で記述する必要がある
5. **テストデータ管理**: フィクスチャやテストデータの管理機構が限定的
6. **BDD非対応**: Given/When/Then形式のBDDテストは外部ライブラリが必要
7. **パラメータ化制限**: テーブル駆動テストは強力だが、型安全なパラメータ化は制限的
8. **統合テスト分離**: ユニットテストと統合テストの分離にビルドタグ等の工夫が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **testify** | assert/suite/mock拡張 | 標準testingより表現力豊かだが外部依存 |
| **gomock** | インターフェースモック生成 | 標準testingにモック機能を追加 |
| **goconvey** | BDD風テストFW | 標準testingよりBDD寄りだがオーバーヘッド |
| **ginkgo** | BDDテストFW（Describe/It） | 標準testingよりRSpec風だが学習コスト高い |
| **go-cmp** | 構造体比較ライブラリ | 標準reflect.DeepEqualより柔軟な比較 |

## 公式リンク

- **公式ドキュメント**: [https://pkg.go.dev/testing](https://pkg.go.dev/testing)
- **テストチュートリアル**: [https://go.dev/doc/tutorial/add-a-test](https://go.dev/doc/tutorial/add-a-test)
- **テーブル駆動テスト**: [https://go.dev/wiki/TableDrivenTests](https://go.dev/wiki/TableDrivenTests)
- **ファジング**: [https://go.dev/doc/tutorial/fuzz](https://go.dev/doc/tutorial/fuzz)
- **カバレッジ**: [https://go.dev/blog/cover](https://go.dev/blog/cover)

## 関連ドキュメント

- [テストツール一覧](../テスト/)
- [GoMock](./GoMock.md)
- [Allure Report](./Allure_Report.md)
- [Go言語](../プログラミング言語/Go.md)
- [テストベストプラクティス](../../best-practices/testing.md)

---

**カテゴリ**: テスト
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
