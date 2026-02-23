# Terratest

## 概要

Terratestは、Gruntwork社が開発したGo言語ベースのインフラストラクチャコードのテスティングフレームワークです。Terraform、Packer、Docker、Kubernetesなどのインフラ自動化ツールに対して自動テストを作成し、実際のクラウド環境でコードを検証できます。Infrastructure as Code (IaC) の品質を保証し、本番環境へのデプロイ前に問題を早期発見することを目的としています。

## 主な機能

### 1. 多様なインフラツール対応
- **Terraform**: モジュール、リソース、出力のテスト
- **Packer**: AMI/VM イメージのビルド検証
- **Docker**: コンテナイメージのテスト
- **Kubernetes**: Pod、Service、Deploymentの検証
- **AWS、Azure、GCP**: クラウドリソースの統合テスト

### 2. 実環境でのテスト
- 実際のクラウド環境にリソースをデプロイ
- エンドツーエンドの統合テスト
- テスト後の自動クリーンアップ

### 3. 並列実行
- 複数テストの並行実行
- テスト時間の短縮
- CIパイプラインでの高速フィードバック

### 4. リトライ・タイムアウト機能
- リソース作成待機のリトライロジック
- タイムアウト設定による無限待機回避
- 非同期リソースの確実な検証

### 5. SSH・HTTPヘルパー
- SSH接続によるサーバー状態確認
- HTTPエンドポイントのヘルスチェック
- ログ取得・コマンド実行

## 利用方法

### セットアップ

```bash
# Goのインストール（前提条件）
# https://golang.org/doc/install

# Terratestをプロジェクトに追加
go get github.com/gruntwork-io/terratest/modules/terraform
go get github.com/gruntwork-io/terratest/modules/aws
go get github.com/gruntwork-io/terratest/modules/http-helper
```

### 基本的なTerraformテスト例

```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestTerraformBasicExample(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        // Terraformコードのパス
        TerraformDir: "../examples/terraform-basic-example",

        // 変数を渡す
        Vars: map[string]interface{}{
            "instance_type": "t2.micro",
        },
    }

    // テスト終了時にリソースを削除
    defer terraform.Destroy(t, terraformOptions)

    // Terraform initとapplyを実行
    terraform.InitAndApply(t, terraformOptions)

    // 出力値を取得
    instanceID := terraform.Output(t, terraformOptions, "instance_id")
    
    // アサーション
    assert.NotEmpty(t, instanceID)
}
```

### AWSリソースの検証例

```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestEC2Instance(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../",
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // EC2インスタンスIDを取得
    instanceID := terraform.Output(t, terraformOptions, "instance_id")
    region := "us-east-1"

    // インスタンスが実行中であることを確認
    instanceStatus := aws.GetEc2InstanceState(t, instanceID, region)
    assert.Equal(t, "running", instanceStatus)

    // タグの検証
    tags := aws.GetEc2InstanceTags(t, instanceID, region)
    assert.Equal(t, "test-instance", tags["Name"])
}
```

### HTTPエンドポイントのテスト例

```go
package test

import (
    "testing"
    "time"
    http_helper "github.com/gruntwork-io/terratest/modules/http-helper"
    "github.com/gruntwork-io/terratest/modules/terraform"
)

func TestWebServer(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../",
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // ALBのDNS名を取得
    albDNS := terraform.Output(t, terraformOptions, "alb_dns_name")
    url := "http://" + albDNS

    // HTTPエンドポイントが200を返すまでリトライ
    maxRetries := 30
    timeBetweenRetries := 5 * time.Second
    expectedStatus := 200
    expectedBody := "Hello, World!"

    http_helper.HttpGetWithRetry(
        t,
        url,
        nil,
        expectedStatus,
        expectedBody,
        maxRetries,
        timeBetweenRetries,
    )
}
```

### テスト実行

```bash
# 単一テスト実行
go test -v -timeout 30m

# 特定のテストのみ実行
go test -v -run TestTerraformBasicExample -timeout 30m

# 並列実行（デフォルトで並列）
go test -v -parallel 10 -timeout 60m
```

## CI/CD統合

### GitHub Actions例

```yaml
name: Terratest

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Go
        uses: actions/setup-go@v2
        with:
          go-version: 1.21
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0
      
      - name: Run Terratest
        run: |
          cd test
          go test -v -timeout 60m
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## メリット

###  主な利点

1. **実環境テスト**: 本物のクラウド環境で検証
2. **早期バグ発見**: 本番デプロイ前に問題を検出
3. **Go言語**: 高速、並列実行、クロスプラットフォーム
4. **多様なツール対応**: Terraform、Packer、Docker、K8s
5. **リトライロジック**: 非同期リソースの確実な検証
6. **自動クリーンアップ**: defer文でリソース削除を保証
7. **CI/CD統合**: GitHub Actions、GitLab CI等と統合可能
8. **オープンソース**: MIT

ライセンス、無料
9. **豊富なヘルパー**: AWS、Azure、GCP、SSHヘルパー充実
10. **コミュニティ活発**: Gruntwork社の継続的な開発

## デメリット

###  制約・課題

1. **実環境コスト**: 実際のクラウドリソースを作成するため課金発生
2. **テスト時間長い**: リソース作成・削除に時間がかかる
3. **Go言語必須**: Goの学習コストが必要
4. **並列実行の制約**: クラウドAPIレート制限に注意
5. **デバッグ困難**: 失敗時のトラブルシューティングが難しい
6. **クリーンアップ失敗**: ネットワークエラー時にリソースが残る可能性
7. **認証情報管理**: AWSクレデンシャルのセキュアな管理が必要
8. **ステートファイル競合**: 並列実行時のTerraformステート管理に注意

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Kitchen-Terraform** | Ruby、Test Kitchenベース | Terratestより柔軟性低い |
| **Terraform Validate** | 構文チェックのみ | 実環境テストは不可 |
| **Checkov** | 静的解析、ポリシーチェック | 実環境テストは不可 |
| **tfsec** | セキュリティ静的解析 | 実環境テストは不可 |
| **InSpec** | インフラテスト（Terraform以外も対応） | Terratestより汎用的 |
| **Pulumi Testing** | Pulumi専用テストフレームワーク | Terraform非対応 |

## 公式リンク

- **GitHubリポジトリ**: [https://github.com/gruntwork-io/terratest](https://github.com/gruntwork-io/terratest)
- **ドキュメント**: [https://terratest.gruntwork.io/](https://terratest.gruntwork.io/)
- **サンプル**: [https://github.com/gruntwork-io/terratest/tree/master/examples](https://github.com/gruntwork-io/terratest/tree/master/examples)
- **Gruntwork Blog**: [https://blog.gruntwork.io/](https://blog.gruntwork.io/)

## 関連ドキュメント

- [インフラテストツール一覧](../インフラテストツール/)
- [Terraform](../IaCツール/Terraform.md)
- [Checkov](../セキュリティツール/Checkov.md)
- [InfrastructureTest Best Practices](../../best-practices/infrastructure-testing.md)

---

**カテゴリ**: インフラテストツール  
**対象工程**: インフラ構築、インフラテスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0

