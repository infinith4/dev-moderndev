# OPA (Open Policy Agent)

## 概要

OPA（Open Policy Agent）は、CNCF（Cloud Native Computing Foundation）のGraduatedプロジェクトである汎用ポリシーエンジンです。Rego言語でポリシーをコード化し、マイクロサービス、Kubernetes、CI/CD、API Gateway等のあらゆるレイヤーで統一的なポリシー管理を実現します。宣言的なポリシー定義により、認可、アドミッション制御、データフィルタリング、コンプライアンスチェックを自動化します。

## 主な機能

### 1. 汎用ポリシーエンジン
- **統一的なポリシー管理**: アプリケーション、インフラ、データ
- **Rego言語**: 宣言的ポリシー記述言語
- **JSON/YAMLサポート**: 構造化データの評価
- **APIベース**: RESTful APIでポリシー評価

### 2. Kubernetes統合
- **Admission Control**: Pod、Service等の作成制御
- **Gatekeeper**: Kubernetes用OPAフレームワーク
- **カスタムリソース**: CRDでポリシー管理
- **監査モード**: 違反検出のみ（enforcement無効）

### 3. マイクロサービス認可
- **API認可**: HTTP APIアクセス制御
- **サービスメッシュ**: Istio、Envoy統合
- **動的ポリシー**: リアルタイムポリシー更新
- **コンテキスト評価**: リクエストコンテキストベースの判断

### 4. CI/CD統合
- **IaC検証**: Terraform、CloudFormation検証
- **コンテナイメージ**: Dockerイメージポリシー
- **パイプラインゲート**: デプロイ前検証

### 5. データフィルタリング
- **JSONフィルタ**: データマスキング
- **RBAC**: ロールベースアクセス制御
- **動的クエリ**: ユーザーコンテキストベースのデータ取得

### 6. パフォーマンス
- **高速**: メモリ内評価
- **スケーラブル**: 分散デプロイ対応
- **キャッシング**: ポリシー評価結果キャッシュ

## 利用方法

### インストール

```bash
# バイナリダウンロード（Linux/macOS）
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
chmod +x opa
sudo mv opa /usr/local/bin/

# Homebrew (macOS)
brew install opa

# Docker
docker pull openpolicyagent/opa

# バージョン確認
opa version
```

### 基本的な使い方

```bash
# OPAサーバー起動
opa run --server

# ポリシーロード
opa run --server policy.rego

# ポリシー評価（CLI）
opa eval -d policy.rego -i input.json "data.authz.allow"
```

### Regoポリシー例

#### 1. 基本的な認可ポリシー

```rego
# policy.rego
package authz

# デフォルトは拒否
default allow = false

# 管理者は全許可
allow {
    input.user.role == "admin"
}

# 自分自身のデータのみ許可
allow {
    input.user.id == input.resource.owner_id
}
```

```json
# input.json
{
  "user": {
    "id": "user123",
    "role": "user"
  },
  "resource": {
    "owner_id": "user123"
  }
}
```

```bash
# 評価
opa eval -d policy.rego -i input.json "data.authz.allow"
# 結果: true
```

#### 2. Kubernetes Admission Control

```rego
# k8s_admission.rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    image := input.request.object.spec.containers[_].image
    not startswith(image, "myregistry.com/")
    msg := sprintf("Image '%v' is not from trusted registry", [image])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.securityContext.runAsNonRoot
    msg := "Pods must run as non-root user"
}
```

#### 3. Terraform検証

```rego
# terraform.rego
package terraform

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    not resource.change.after.server_side_encryption_configuration
    msg := sprintf("S3 bucket '%v' must have encryption enabled", [resource.name])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port == 22
    msg := "Security group allows SSH from internet"
}
```

### REST API使用

```bash
# ポリシーアップロード
curl -X PUT http://localhost:8181/v1/policies/authz \
  --data-binary @policy.rego

# ポリシー評価
curl -X POST http://localhost:8181/v1/data/authz/allow \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "user": {"id": "user123", "role": "user"},
      "resource": {"owner_id": "user123"}
    }
  }'

# レスポンス
{
  "result": true
}
```

### Kubernetes Gatekeeper

```yaml
# constraint-template.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8strustedimages
spec:
  crd:
    spec:
      names:
        kind: K8sTrustedImages
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8strustedimages
        
        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not startswith(container.image, "myregistry.com/")
          msg := sprintf("Image '%v' is not from trusted registry", [container.image])
        }
```

```yaml
# constraint.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sTrustedImages
metadata:
  name: trusted-images
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **OPA (OSS)** |  無料 | オープンソース、Apache License 2.0 |
| **Styra DAS** |  商用 | エンタープライズ版、UIダッシュボード、サポート |

## メリット

###  主な利点

1. **汎用性**: あらゆるレイヤーでポリシー管理
2. **無料**: オープンソース、Apache License
3. **CNCF Graduated**: 成熟した安定プロジェクト
4. **Kubernetes統合**: Gatekeeper標準化
5. **宣言的**: Regoで明確なポリシー記述
6. **パフォーマンス**: 高速評価
7. **テスト可能**: ユニットテスト記述可能
8. **動的更新**: リアルタイムポリシー変更
9. **エコシステム**: Istio、Envoy、Terraform統合
10. **スケーラブル**: 大規模環境対応

## デメリット

###  制約・課題

1. **学習曲線**: Rego言語の習得必要
2. **デバッグ困難**: ポリシーデバッグに時間
3. **ドキュメント**: 日本語情報少ない
4. **GUI不在**: コマンドライン中心（Styra DAS除く）
5. **複雑なポリシー**: 大規模ポリシー管理が煩雑
6. **パフォーマンス**: 超複雑ポリシーで遅延
7. **エラーメッセージ**: 分かりにくい場合あり
8. **ツール不足**: IDE統合が限定的

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Kyverno** | Kubernetes専用、YAML | OPAよりKubernetes特化、学習容易 |
| **HashiCorp Sentinel** | Terraform専用 | OPAよりTerraform特化 |
| **Casbin** | 認可ライブラリ | OPAよりシンプルだが汎用性低い |
| **AWS IAM** | AWS専用 | OPAより管理容易だがAWS限定 |
| **Istio AuthorizationPolicy** | Service Mesh専用 | OPAよりIstio特化 |

## 公式リンク

- **公式サイト**: [https://www.openpolicyagent.org/](https://www.openpolicyagent.org/)
- **ドキュメント**: [https://www.openpolicyagent.org/docs/](https://www.openpolicyagent.org/docs/)
- **GitHub**: [https://github.com/open-policy-agent/opa](https://github.com/open-policy-agent/opa)
- **Gatekeeper**: [https://open-policy-agent.github.io/gatekeeper/](https://open-policy-agent.github.io/gatekeeper/)
- **Playground**: [https://play.openpolicyagent.org/](https://play.openpolicyagent.org/)

## 関連ドキュメント

- [ポリシー管理ツール一覧](../ポリシー管理ツール/)
- [Kubernetes](../コンテナオーケストレーション/Kubernetes.md)
- [Terraform](../IaCツール/Terraform.md)
- [Istio](../サービスメッシュ/Istio.md)
- [ポリシー管理ベストプラクティス](../../best-practices/policy-management.md)

---

**カテゴリ**: ポリシー管理ツール  
**対象工程**: セキュリティ、インフラ構築、運用  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0

