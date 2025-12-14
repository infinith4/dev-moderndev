# Vault

## 概要

Vaultは、HashiCorp製のシークレット管理・暗号化ツールです。動的シークレット、暗号化as a Service、アクセス制御（ACL）、監査ログにより、パスワード、APIキー、証明書、暗号化キーを安全に管理します。Kubernetes統合、AWS/Azure統合、Key Rotation、シークレットリース管理で、Zero Trustセキュリティを実現します。

## 主な機能

### 1. シークレット管理
- **Key-Value**: 静的シークレット
- **動的シークレット**: 一時的な認証情報
- **リース**: TTL管理
- **Revocation**: シークレット無効化

### 2. 暗号化
- **Encryption as a Service**: API暗号化
- **Transit Engine**: データ暗号化
- **Key Rotation**: キーローテーション

### 3. 認証
- **Token**: Vaultトークン
- **AppRole**: アプリケーション認証
- **Kubernetes**: K8s ServiceAccount
- **LDAP/OIDC**: 外部認証

### 4. シークレットエンジン
- **Database**: 動的DB認証情報
- **AWS**: 動的IAMクレデンシャル
- **PKI**: 証明書発行

## 利用方法

### インストール（Docker）

```bash
docker run -d --name vault \
  -p 8200:8200 \
  --cap-add=IPC_LOCK \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' \
  -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' \
  vault:latest

# CLI設定
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='myroot'
```

### 基本操作

```bash
# シークレット書き込み
vault kv put secret/myapp/config \
  username=admin \
  password=secret123

# シークレット読み取り
vault kv get secret/myapp/config

# JSON出力
vault kv get -format=json secret/myapp/config

# 削除
vault kv delete secret/myapp/config
```

### 動的シークレット（Database）

```bash
# DatabaseエンジンHCL有効化
vault secrets enable database

# PostgreSQL接続設定
vault write database/config/my-postgresql \
  plugin_name=postgresql-database-plugin \
  allowed_roles="my-role" \
  connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
  username="vault" \
  password="vaultpassword"

# Role作成
vault write database/roles/my-role \
  db_name=my-postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# 動的クレデンシャル生成
vault read database/creds/my-role
```

### AppRole認証

```bash
# AppRole有効化
vault auth enable approle

# Role作成
vault write auth/approle/role/my-app \
  token_policies="my-policy" \
  token_ttl=1h \
  token_max_ttl=4h

# RoleID取得
vault read auth/approle/role/my-app/role-id

# SecretID生成
vault write -f auth/approle/role/my-app/secret-id

# ログイン
vault write auth/approle/login \
  role_id="<role-id>" \
  secret_id="<secret-id>"
```

### Kubernetes統合

```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp

---
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "myapp"
        vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
    spec:
      serviceAccountName: myapp
      containers:
      - name: myapp
        image: myapp:latest
```

### Go SDK

```go
package main

import (
    "fmt"
    vault "github.com/hashicorp/vault/api"
)

func main() {
    config := vault.DefaultConfig()
    config.Address = "http://localhost:8200"

    client, err := vault.NewClient(config)
    if err != nil {
        panic(err)
    }

    client.SetToken("myroot")

    // シークレット読み取り
    secret, err := client.Logical().Read("secret/data/myapp/config")
    if err != nil {
        panic(err)
    }

    data := secret.Data["data"].(map[string]interface{})
    fmt.Println("Username:", data["username"])
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Vault OSS** | 🟢 完全無料 | オープンソース、MPL License |
| **Vault Enterprise** | 💰 要問い合わせ | レプリケーション、HSM、FIPS |
| **HCP Vault** | 💰 従量課金 | マネージドVault |

## メリット

1. **完全無料**: オープンソース
2. **動的シークレット**: 一時認証情報
3. **暗号化**: 暗号化API
4. **統合**: K8s、AWS、Azure
5. **監査**: 詳細ログ

## デメリット

1. **複雑性**: 学習曲線steep
2. **運用**: HA構成複雑
3. **パフォーマンス**: ネットワーク遅延
4. **小規模**: 小規模環境にオーバースペック

## 公式リンク

- **公式サイト**: [https://www.vaultproject.io/](https://www.vaultproject.io/)
- **ドキュメント**: [https://www.vaultproject.io/docs](https://www.vaultproject.io/docs)

## 関連ドキュメント

- [シークレット管理ツール一覧](../シークレット管理ツール/)
- [AWS Secrets Manager](../クラウドツール/AWS_Secrets_Manager.md)
- [Azure Key Vault](../クラウドツール/Azure_Key_Vault.md)

---

**カテゴリ**: シークレット管理ツール
**対象工程**: セキュリティ・認証情報管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
