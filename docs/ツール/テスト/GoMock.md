# GoMock

## 概要

GoMockは、Go言語のインターフェースベースのモック生成フレームワークである。元々はGoogle社が開発し（`github.com/golang/mock`）、現在はUber社がフォーク・メンテナンスしている（`go.uber.org/mock`）。`mockgen`コマンドでインターフェースからモックコードを自動生成し、`gomock.Controller`を使って期待値（Expectation）の設定と検証を行う。Go標準の`testing`パッケージと組み合わせて使用し、依存関係を切り離した単体テストを効率的に記述できる。

## 主な機能

### 1. モックコード自動生成（mockgen）

- インターフェース定義からモック実装を自動生成
- ソースモード（`-source`）とリフレクトモード（パッケージ指定）の2つの生成方式
- `go:generate`ディレクティブとの統合で生成を自動化
- 生成先パッケージ名やモック名のカスタマイズ

### 2. 期待値設定（EXPECT）

- `EXPECT()`メソッドで呼び出し期待を定義
- `Return()`で戻り値を指定
- `DoAndReturn()`で任意のロジックを戻り値として実行
- `Do()`で副作用のあるアクションを設定
- `SetArg()`で引数のポインタ経由の値設定

### 3. 呼び出し回数制御

- `Times(n)` - 正確にn回呼ばれることを期待
- `AnyTimes()` - 何回呼ばれてもよい
- `MaxTimes(n)` - 最大n回まで許容
- `MinTimes(n)` - 最低n回は呼ばれることを期待

### 4. 引数マッチャー

- `gomock.Any()` - 任意の値にマッチ
- `gomock.Eq(value)` - 等値マッチ
- `gomock.Nil()` - nil値にマッチ
- `gomock.Not(matcher)` - マッチャーの否定
- カスタムマッチャーの実装（`gomock.Matcher`インターフェース）

### 5. 呼び出し順序制御

- `gomock.InOrder()` - 複数の期待に対して呼び出し順序を強制
- `After()` - 特定の呼び出しの後に実行されることを期待

## 利用方法

### インストール

```bash
# mockgenコマンドのインストール
go install go.uber.org/mock/mockgen@latest

# プロジェクトへの依存追加
go get go.uber.org/mock/gomock
```

### mockgenによるモック生成

```bash
# リフレクトモード（パッケージとインターフェース名を指定）
mockgen -destination=mocks/mock_repository.go -package=mocks myapp/repository UserRepository

# ソースモード（ソースファイルを指定）
mockgen -source=repository/user_repository.go -destination=mocks/mock_repository.go -package=mocks
```

### go:generateディレクティブの活用

```go
// repository/user_repository.go
package repository

//go:generate mockgen -destination=../mocks/mock_user_repository.go -package=mocks . UserRepository

type UserRepository interface {
    FindByID(id string) (*User, error)
    Save(user *User) error
    Delete(id string) error
}
```

```bash
# プロジェクト全体のモックを一括生成
go generate ./...
```

### テストコードの記述

```go
package service_test

import (
    "testing"

    "go.uber.org/mock/gomock"
    "myapp/mocks"
    "myapp/service"
)

func TestUserService_GetUser(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockUserRepository(ctrl)

    // 期待値の設定
    mockRepo.EXPECT().
        FindByID("user-123").
        Return(&repository.User{ID: "user-123", Name: "Taro"}, nil).
        Times(1)

    svc := service.NewUserService(mockRepo)
    user, err := svc.GetUser("user-123")

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "Taro" {
        t.Errorf("expected name Taro, got %s", user.Name)
    }
}

func TestUserService_CreateUser_WithOrder(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockUserRepository(ctrl)

    // 呼び出し順序の制御
    gomock.InOrder(
        mockRepo.EXPECT().FindByID("user-123").Return(nil, nil),
        mockRepo.EXPECT().Save(gomock.Any()).Return(nil),
    )

    svc := service.NewUserService(mockRepo)
    err := svc.CreateUserIfNotExists("user-123", "Taro")

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func TestUserService_DoAndReturn(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockUserRepository(ctrl)

    // DoAndReturnで動的な戻り値を生成
    mockRepo.EXPECT().
        Save(gomock.Any()).
        DoAndReturn(func(user *repository.User) error {
            if user.Name == "" {
                return fmt.Errorf("name is required")
            }
            return nil
        }).
        AnyTimes()

    svc := service.NewUserService(mockRepo)
    err := svc.CreateUser(&repository.User{Name: ""})

    if err == nil {
        t.Fatal("expected error but got nil")
    }
}
```

### CI/CD統合（GitHub Actions）

```yaml
name: Go Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Install mockgen
        run: go install go.uber.org/mock/mockgen@latest
      - name: Generate mocks
        run: go generate ./...
      - name: Run tests
        run: go test -v -cover ./...
```

## エディション・料金

| プラン | 料金 | 内容 |
|--------|------|------|
| オープンソース | 無料 | 全機能利用可能、Apache 2.0ライセンス |

## メリット

1. インターフェースからモックを自動生成するため、手動実装の手間を大幅に削減できる
2. `EXPECT()`による宣言的な期待値設定で、テストの意図が明確になる
3. `go:generate`との統合によりモック生成をビルドプロセスに組み込める
4. `InOrder()`や`Times()`による呼び出し順序・回数の厳密な制御が可能
5. Go標準の`testing`パッケージとシームレスに連携する
6. Uber社による積極的なメンテナンスが継続されている

## デメリット

1. インターフェース定義変更時にモックの再生成が必要であり、更新漏れが発生しやすい
2. 具象型やエクスポートされていないインターフェースにはモックを生成できない
3. 過度なモック利用はテストの保守コストを増大させる可能性がある
4. 旧リポジトリ（golang/mock）からの移行が必要な既存プロジェクトがある
5. 生成コードがリポジトリに含まれる場合、差分管理の煩雑さがある

## 代替ツール

| ツール名 | 特徴 | 比較 |
|----------|------|------|
| testify/mock | アサーション付きモックライブラリ | 構造体ベース、手動実装が必要だがアサーションが豊富 |
| counterfeiter | インターフェースからモック生成 | Cloud Foundry由来、シンプルなAPI |
| mockery | testify/mock向けのコード生成ツール | testifyエコシステムとの統合に優れる |
| moq (Go) | 型安全なモック生成 | 関数フィールドベース、軽量 |

## 公式リンク

- [GoMock GitHub（uber-go/mock）](https://github.com/uber-go/mock)
- [GoMock pkg.go.dev](https://pkg.go.dev/go.uber.org/mock/gomock)
- [mockgen ドキュメント](https://pkg.go.dev/go.uber.org/mock/mockgen)
- [旧リポジトリ（golang/mock）](https://github.com/golang/mock)

## 関連ドキュメント

- [Go testing 標準パッケージ](https://pkg.go.dev/testing)
- [Go generate コマンド](https://go.dev/blog/generate)
- [Effective Go - Testing](https://go.dev/doc/effective_go)

---

カテゴリ: テスト
対象工程: 単体テスト、結合テスト
最終更新: 2025年12月
ドキュメントバージョン: 1.0
