# Apigee

## 概要

**Apigee**は、Google Cloud が提供するフルマネージドAPIマネジメントプラットフォームです。API設計、セキュリティ、分析、開発者ポータル機能を統合し、エンタープライズレベルのAPI戦略を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Google Cloud（元Apigee Corporation） |
| **種別** | APIマネジメント・APIゲートウェイ |
| **ライセンス** | プロプライエタリ |
| **料金** | 🔴 有料（従量課金、月額固定プランあり） |
| **公式サイト** | https://cloud.google.com/apigee |
| **ドキュメント** | https://cloud.google.com/apigee/docs |

## 主な特徴

### 1. フルライフサイクルAPIマネジメント
- API設計・開発
- セキュリティ（OAuth 2.0、JWT、APIキー）
- レート制限・クォータ管理
- 分析・モニタリング
- 開発者ポータル

### 2. ハイブリッド・マルチクラウド対応
- **Apigee X**: Google Cloud完全マネージド
- **Apigee Hybrid**: オンプレミス + クラウド
- AWS、Azure上のバックエンドAPIもサポート

### 3. 高度なトラフィック管理
- レート制限（Spike Arrest）
- クォータ管理
- ルーティング・負荷分散
- キャッシング

### 4. 開発者エクスペリエンス
- APIドキュメント自動生成
- インタラクティブAPI Explorer
- 開発者登録・APIキー発行

## 使い方

### Apigee X（Google Cloud）でのAPI作成

#### 1. APIプロキシ作成（GUIまたはCLI）

**GUI操作**:
1. Google Cloud Console → Apigee
2. API Proxies → Create Proxy
3. Reverse Proxy選択
4. 設定:
   - Proxy Name: `users-api`
   - Base Path: `/v1/users`
   - Target URL: `https://backend.example.com/users`

**CLI操作（apigeetool）**:

```bash
# apigeetoolインストール
npm install -g apigeetool

# APIプロキシ作成
apigeetool createproxy \
  -o your-org \
  -e test \
  -n users-api \
  -d /v1/users \
  -u https://backend.example.com/users
```

#### 2. APIプロキシ定義（XML）

```xml
<!-- apiproxy/users-api.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<APIProxy revision="1" name="users-api">
  <ConfigurationVersion majorVersion="4" minorVersion="0"/>
  <CreatedAt>1701878400000</CreatedAt>
  <CreatedBy>admin@example.com</CreatedBy>
  <DisplayName>Users API</DisplayName>
  <LastModifiedAt>1701878400000</LastModifiedAt>
  <LastModifiedBy>admin@example.com</LastModifiedBy>
  <BasePaths>/v1/users</BasePaths>
  <Policies>
    <Policy>Verify-API-Key</Policy>
    <Policy>Quota</Policy>
    <Policy>Spike-Arrest</Policy>
  </Policies>
  <ProxyEndpoints>
    <ProxyEndpoint>default</ProxyEndpoint>
  </ProxyEndpoints>
  <TargetEndpoints>
    <TargetEndpoint>default</TargetEndpoint>
  </TargetEndpoints>
</APIProxy>
```

#### 3. ポリシー設定

**APIキー検証（Verify-API-Key.xml）**:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VerifyAPIKey async="false" continueOnError="false" enabled="true" name="Verify-API-Key">
  <DisplayName>Verify API Key</DisplayName>
  <APIKey ref="request.header.x-api-key"/>
</VerifyAPIKey>
```

**レート制限（Spike-Arrest.xml）**:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<SpikeArrest async="false" continueOnError="false" enabled="true" name="Spike-Arrest">
  <DisplayName>Spike Arrest</DisplayName>
  <Rate>100pm</Rate>  <!-- 100 requests per minute -->
</SpikeArrest>
```

**クォータ（Quota.xml）**:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Quota async="false" continueOnError="false" enabled="true" name="Quota">
  <DisplayName>Quota</DisplayName>
  <Allow count="10000" countRef="verifyapikey.Verify-API-Key.apiproduct.developer.quota.limit"/>
  <Interval ref="verifyapikey.Verify-API-Key.apiproduct.developer.quota.interval">1</Interval>
  <TimeUnit ref="verifyapikey.Verify-API-Key.apiproduct.developer.quota.timeunit">month</TimeUnit>
</Quota>
```

**レスポンスキャッシュ（Response-Cache.xml）**:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ResponseCache async="false" continueOnError="false" enabled="true" name="Response-Cache">
  <DisplayName>Response Cache</DisplayName>
  <CacheKey>
    <Prefix/>
    <KeyFragment ref="request.uri"/>
  </CacheKey>
  <ExpirySettings>
    <TimeoutInSec>3600</TimeoutInSec>  <!-- 1 hour -->
  </ExpirySettings>
</ResponseCache>
```

#### 4. プロキシエンドポイント（ProxyEndpoint）

```xml
<!-- apiproxy/proxies/default.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ProxyEndpoint name="default">
  <Description/>
  <FaultRules/>
  <PreFlow name="PreFlow">
    <Request>
      <Step>
        <Name>Verify-API-Key</Name>
      </Step>
      <Step>
        <Name>Spike-Arrest</Name>
      </Step>
      <Step>
        <Name>Quota</Name>
      </Step>
    </Request>
    <Response>
      <Step>
        <Name>Response-Cache</Name>
      </Step>
    </Response>
  </PreFlow>
  <HTTPProxyConnection>
    <BasePath>/v1/users</BasePath>
    <VirtualHost>secure</VirtualHost>
  </HTTPProxyConnection>
  <RouteRule name="default">
    <TargetEndpoint>default</TargetEndpoint>
  </RouteRule>
</ProxyEndpoint>
```

#### 5. ターゲットエンドポイント（TargetEndpoint）

```xml
<!-- apiproxy/targets/default.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<TargetEndpoint name="default">
  <Description/>
  <FaultRules/>
  <PreFlow name="PreFlow">
    <Request/>
    <Response/>
  </PreFlow>
  <HTTPTargetConnection>
    <URL>https://backend.example.com/users</URL>
  </HTTPTargetConnection>
</TargetEndpoint>
```

### OAuth 2.0実装

```xml
<!-- OAuthV2-GenerateAccessToken.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<OAuthV2 async="false" continueOnError="false" enabled="true" name="OAuthV2-GenerateAccessToken">
  <DisplayName>OAuth 2.0 Generate Access Token</DisplayName>
  <Operation>GenerateAccessToken</Operation>
  <ExpiresIn>3600000</ExpiresIn>  <!-- 1 hour in ms -->
  <SupportedGrantTypes>
    <GrantType>client_credentials</GrantType>
    <GrantType>password</GrantType>
  </SupportedGrantTypes>
  <GenerateResponse enabled="true"/>
</OAuthV2>
```

### Node.js スクリプトポリシー

```xml
<!-- AssignMessage-AddCustomHeader.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Javascript async="false" continueOnError="false" enabled="true" timeLimit="200" name="JS-ProcessRequest">
  <DisplayName>JavaScript - Process Request</DisplayName>
  <ResourceURL>jsc://process-request.js</ResourceURL>
</Javascript>
```

```javascript
// resources/jsc/process-request.js
// カスタムヘッダー追加
context.setVariable("request.header.X-Custom-Header", "CustomValue");

// リクエストボディの変換
var requestBody = context.getVariable("request.content");
var jsonBody = JSON.parse(requestBody);

jsonBody.timestamp = new Date().toISOString();
jsonBody.apiVersion = "v1";

context.setVariable("request.content", JSON.stringify(jsonBody));
```

### API Management CLI（apigee-cli）

```bash
# Google Cloud SDKでApigee認証
gcloud auth login

# APIプロキシデプロイ
gcloud apigee apis deploy \
  --api=users-api \
  --env=test \
  --org=your-org

# APIプロダクト作成
gcloud apigee products create \
  --display-name="Users API Product" \
  --apis=users-api \
  --environments=test \
  --approval-type=auto

# 開発者作成
gcloud apigee developers create \
  --email=developer@example.com \
  --first-name=John \
  --last-name=Doe

# アプリ登録
gcloud apigee apps create \
  --developer=developer@example.com \
  --display-name="My App" \
  --api-products="Users API Product"
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **基本設計** | API設計 | APIゲートウェイアーキテクチャ設計 |
| **実装** | APIゲートウェイ実装 | セキュリティポリシー・ルーティング実装 |
| **テスト** | API統合テスト | セキュリティ・レート制限テスト |
| **導入** | API公開・運用 | 開発者ポータル公開、モニタリング |

## メリット

- **フルマネージド**: インフラ管理不要（Apigee X）
- **エンタープライズ機能**: OAuth、JWT、mTLS、SAML対応
- **高度な分析**: APIトラフィック分析、エラー分析、開発者分析
- **開発者ポータル**: ドキュメント自動生成、API Explorer
- **ハイブリッド対応**: オンプレミスとクラウドのハイブリッド構成可能
- **スケーラビリティ**: Google Cloudインフラで自動スケール
- **多様なポリシー**: 300以上のビルトインポリシー

## デメリット

- **高コスト**: 小規模プロジェクトには高額（月額数十万〜数百万円）
- **ベンダーロックイン**: Google Cloud依存
- **学習曲線**: ポリシー設定・XML構成の習得が必要
- **複雑性**: シンプルなAPI管理には過剰な機能
- **設定の煩雑さ**: GUI/CLI/XMLでの設定管理が複雑

## 類似ツールとの比較

| ツール | 料金 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **Apigee** | 有料 | エンタープライズ機能、開発者ポータル | 大規模API戦略 |
| **AWS API Gateway** | 従量課金 | AWS統合、低コスト | AWSエコシステム |
| **Azure API Management** | 従量課金 | Azure統合、Power Platform連携 | Azureエコシステム |
| **Kong** | 無料〜有料 | オープンソース、プラグインエコシステム | カスタマイズ重視 |

## ベストプラクティス

### 1. ポリシーの再利用

```xml
<!-- Shared Flows: 複数APIで共通のポリシー -->
<SharedFlow name="common-security">
  <Step>
    <Name>Verify-API-Key</Name>
  </Step>
  <Step>
    <Name>Spike-Arrest</Name>
  </Step>
</SharedFlow>
```

### 2. 環境変数の活用

```xml
<!-- KeyValueMap: 環境ごとの設定を外部化 -->
<KeyValueMapOperations name="Get-Config">
  <Get assignTo="backend.url">
    <Key>
      <Parameter>backend_url</Parameter>
    </Key>
  </Get>
</KeyValueMapOperations>
```

### 3. エラーハンドリング

```xml
<!-- FaultRules: 統一されたエラーレスポンス -->
<FaultRules>
  <FaultRule name="invalid_api_key">
    <Step>
      <Name>AM-InvalidAPIKeyResponse</Name>
    </Step>
    <Condition>(fault.name = "InvalidApiKey")</Condition>
  </FaultRule>
</FaultRules>
```

### 4. CI/CDパイプライン統合

```yaml
# .github/workflows/apigee-deploy.yml
name: Deploy to Apigee
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy API Proxy
        run: |
          gcloud apigee apis deploy \
            --api=users-api \
            --env=production \
            --org=${{ secrets.APIGEE_ORG }}
```

## 公式リソース

- **公式サイト**: https://cloud.google.com/apigee
- **ドキュメント**: https://cloud.google.com/apigee/docs
- **チュートリアル**: https://cloud.google.com/apigee/docs/api-platform/get-started/overview
- **コミュニティ**: https://www.googlecloudcommunity.com/gc/Apigee/bd-p/cloud-apigee

## まとめ

Apigeeは、エンタープライズレベルのAPIマネジメントに必要な機能を網羅したプラットフォームです。高コストですが、セキュリティ、分析、開発者エクスペリエンス、ハイブリッド対応など、大規模API戦略に求められる要件を満たします。Google Cloudとの統合により、スケーラブルで信頼性の高いAPIゲートウェイを構築できます。

---

**最終更新**: 2025-12-06
**対象バージョン**: Apigee X / Apigee Hybrid
