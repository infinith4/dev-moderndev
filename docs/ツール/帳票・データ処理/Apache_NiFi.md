# Apache NiFi

## 概要

**Apache NiFi**は、オープンソースのデータフロー自動化ツールです。Webベースのビジュアルエディタで、複雑なデータパイプラインを設計・管理し、様々なデータソース間でのデータルーティング、変換、システム統合を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Apache Software Foundation（元々はNSA開発） |
| **種別** | データフロー自動化・ETL |
| **ライセンス** | Apache License 2.0（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://nifi.apache.org/ |
| **ドキュメント** | https://nifi.apache.org/docs.html |

## 主な特徴

### 1. ビジュアルデータフロー設計
- ドラッグ&ドロップでデータパイプライン構築
- リアルタイムでフロー実行・監視
- プロセッサー間のデータ移動を可視化

### 2. 豊富なプロセッサーライブラリ
- **300以上のビルトインプロセッサー**
  - HTTP、FTP、SFTP
  - Kafka、RabbitMQ、MQTT
  - Hadoop、Hive、HBase
  - AWS S3、Azure Blob、GCS
  - データベース（JDBC）
  - JSON、XML、CSV変換

### 3. データプロビナンス（来歴追跡）
- 各FlowFileの完全な履歴追跡
- データ系譜（Lineage）の可視化
- 監査・コンプライアンス対応

### 4. スケーラビリティ
- クラスタ構成でスケールアウト
- バックプレッシャー・優先度制御
- 分散処理対応

## 使い方

### インストール（Docker）

```bash
# Docker Composeで起動（最も簡単）
version: '3.8'
services:
  nifi:
    image: apache/nifi:latest
    ports:
      - "8443:8443"  # HTTPS UI
    environment:
      - SINGLE_USER_CREDENTIALS_USERNAME=admin
      - SINGLE_USER_CREDENTIALS_PASSWORD=adminadminadmin
    volumes:
      - nifi-conf:/opt/nifi/nifi-current/conf
      - nifi-database_repository:/opt/nifi/nifi-current/database_repository
      - nifi-flowfile_repository:/opt/nifi/nifi-current/flowfile_repository
      - nifi-content_repository:/opt/nifi/nifi-current/content_repository
      - nifi-provenance_repository:/opt/nifi/nifi-current/provenance_repository
      - nifi-state:/opt/nifi/nifi-current/state
      - nifi-logs:/opt/nifi/nifi-current/logs

volumes:
  nifi-conf:
  nifi-database_repository:
  nifi-flowfile_repository:
  nifi-content_repository:
  nifi-provenance_repository:
  nifi-state:
  nifi-logs:
```

```bash
# 起動
docker-compose up -d

# ブラウザでアクセス
# https://localhost:8443/nifi/
# ユーザー: admin
# パスワード: adminadminadmin
```

### インストール（スタンドアロン）

```bash
# Java 11以上が必要
java -version

# NiFiダウンロード・解凍
wget https://downloads.apache.org/nifi/1.24.0/nifi-1.24.0-bin.tar.gz
tar -xzf nifi-1.24.0-bin.tar.gz
cd nifi-1.24.0

# シングルユーザー認証設定
./bin/nifi.sh set-single-user-credentials admin adminadminadmin

# 起動
./bin/nifi.sh start

# ログ確認
tail -f logs/nifi-app.log

# ブラウザでアクセス
# https://localhost:8443/nifi/
```

### 基本的なデータフローの作成

#### シナリオ: HTTPでJSONデータを取得してS3に保存

**GUI操作手順**:

1. **GetHTTPプロセッサー追加**
   - ツールバーからProcessorアイコンをドラッグ
   - 検索: "GetHTTP"
   - 設定:
     - URL: `https://api.example.com/data`
     - Filename: `data.json`

2. **PutS3Objectプロセッサー追加**
   - 同様にPutS3Objectを追加
   - 設定:
     - Bucket: `my-data-bucket`
     - Access Key ID: `${AWS_ACCESS_KEY}`
     - Secret Access Key: `${AWS_SECRET_KEY}`
     - Region: `us-east-1`

3. **プロセッサー接続**
   - GetHTTPの"success"リレーションシップをPutS3Objectに接続
   - GetHTTPの"failure"を自動終了（Auto-terminate）に設定

4. **実行**
   - 各プロセッサーを右クリック → Start

### テンプレート（XML形式）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<template encoding-version="1.3">
    <description>HTTP to S3 Data Pipeline</description>
    <groupId>root</groupId>
    <name>HTTP-to-S3-Pipeline</name>
    <snippet>
        <processors>
            <id>GetHTTP-001</id>
            <parentGroupId>root</parentGroupId>
            <position>
                <x>100.0</x>
                <y>100.0</y>
            </position>
            <bundle>
                <artifact>nifi-standard-nar</artifact>
                <group>org.apache.nifi</group>
                <version>1.24.0</version>
            </bundle>
            <config>
                <bulletinLevel>WARN</bulletinLevel>
                <comments></comments>
                <concurrentlySchedulableTaskCount>1</concurrentlySchedulableTaskCount>
                <descriptors>
                    <entry>
                        <key>URL</key>
                        <value>
                            <name>URL</name>
                        </value>
                    </entry>
                </descriptors>
                <executionNode>ALL</executionNode>
                <lossTolerant>false</lossTolerant>
                <penaltyDuration>30 sec</penaltyDuration>
                <properties>
                    <entry>
                        <key>URL</key>
                        <value>https://api.example.com/data</value>
                    </entry>
                    <entry>
                        <key>Filename</key>
                        <value>data.json</value>
                    </entry>
                </properties>
                <runDurationMillis>0</runDurationMillis>
                <schedulingPeriod>60 sec</schedulingPeriod>
                <schedulingStrategy>TIMER_DRIVEN</schedulingStrategy>
                <yieldDuration>1 sec</yieldDuration>
            </config>
            <name>GetHTTP</name>
            <relationships>
                <autoTerminate>false</autoTerminate>
                <name>success</name>
            </relationships>
            <state>STOPPED</state>
            <type>org.apache.nifi.processors.standard.GetHTTP</type>
        </processors>
    </snippet>
    <timestamp>12/06/2025 00:00:00 UTC</timestamp>
</template>
```

### データ変換フロー例

#### JSON to CSV変換

**プロセッサー構成**:

1. **GetFile**: ローカルファイル読み込み
2. **ConvertRecord**: JSON → CSV変換
   - Record Reader: JsonTreeReader
   - Record Writer: CSVRecordSetWriter
3. **PutFile**: CSV出力

```properties
# ConvertRecord設定
Record Reader: JsonTreeReader
  - Schema Access Strategy: Infer Schema

Record Writer: CSVRecordSetWriter
  - Schema Write Strategy: Do Not Write Schema
  - Include Header Line: true
  - Value Separator: ","
```

### 式言語（Expression Language）

```nifi
# FlowFile属性を参照
${filename}
${absolute.path}

# 文字列操作
${filename:toUpper()}
${filename:substring(0, 5)}

# 日付フォーマット
${now():format('yyyy-MM-dd')}

# 条件分岐（RouteOnAttributeプロセッサーで使用）
${fileSize:gt(1000000)}  # ファイルサイズが1MB超
${mime.type:equals('application/json')}  # MIMEタイプがJSON
```

### REST API操作

```bash
# プロセッサーグループ一覧取得
curl -k -u admin:adminadminadmin \
  https://localhost:8443/nifi-api/flow/process-groups/root

# プロセッサー起動
curl -k -u admin:adminadminadmin -X PUT \
  -H "Content-Type: application/json" \
  -d '{"revision":{"version":0},"state":"RUNNING"}' \
  https://localhost:8443/nifi-api/processors/{processor-id}/run-status

# データプロビナンス検索
curl -k -u admin:adminadminadmin \
  https://localhost:8443/nifi-api/provenance
```

### Kafka統合例

**フロー構成**:

1. **ConsumeKafka_2_6**
   - Topic: `user-events`
   - Bootstrap Servers: `kafka:9092`
   - Group ID: `nifi-consumers`

2. **EvaluateJsonPath**: JSON解析
   - `$.userId` → `user.id` 属性に抽出
   - `$.eventType` → `event.type` 属性に抽出

3. **RouteOnAttribute**: イベントタイプで分岐
   - Route 1: `${event.type:equals('purchase')}` → データベースに保存
   - Route 2: `${event.type:equals('pageview')}` → ログファイルに保存

4. **PutSQL / PutFile**: 保存先

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | データ統合実装 | ETLパイプライン実装 |
| **テスト** | データフローテスト | データ変換ロジック検証 |
| **導入** | データ移行 | システム間データ転送・移行 |

## メリット

- **ビジュアル設計**: プログラミング不要でデータフロー構築
- **リアルタイム処理**: ストリーミングデータ処理対応
- **データプロビナンス**: 完全なデータ系譜追跡
- **豊富なプロセッサー**: 300以上のビルトインコンポーネント
- **バックプレッシャー対応**: フロー制御で安定動作
- **スケーラビリティ**: クラスタ構成でスケールアウト
- **式言語**: 柔軟なデータ操作
- **監視・アラート**: リアルタイムモニタリング

## デメリット

- **リソース消費**: Java VMで動作、メモリ・CPU消費が大きい
- **学習曲線**: プロセッサー種類が多く、初期学習コストあり
- **複雑な変換には不向き**: 複雑なビジネスロジックはカスタムプロセッサー開発が必要
- **バージョン管理の難しさ**: フロー定義がXMLで管理が煩雑
- **GUIベース**: コードレビュー・差分管理がしにくい

## 類似ツールとの比較

| ツール | 特徴 | コスト | 適用場面 |
|--------|------|--------|----------|
| **Apache NiFi** | ビジュアル設計、データプロビナンス | 無料 | 複雑なデータフロー、監査要件 |
| **Apache Airflow** | コードベース（Python）、ワークフロー管理 | 無料 | バッチ処理、スケジュール管理 |
| **Airbyte** | ELT特化、コネクタ豊富 | 無料〜有料 | SaaS間データ統合 |
| **StreamSets** | NiFi類似、エンタープライズ機能 | 有料 | エンタープライズETL |

## ベストプラクティス

### 1. プロセスグループの活用

```text
# 論理的なグループ化で管理性向上
Root Process Group
├── Ingestion (データ取り込み)
│   ├── HTTP Sources
│   └── Kafka Sources
├── Transformation (変換)
│   ├── JSON Processing
│   └── CSV Processing
└── Export (エクスポート)
    ├── S3 Export
    └── Database Export
```

### 2. パラメーターコンテキスト

```properties
# 環境変数的に設定を外部化
[Development]
kafka.bootstrap.servers = localhost:9092
s3.bucket = dev-bucket

[Production]
kafka.bootstrap.servers = kafka-prod:9092
s3.bucket = prod-bucket
```

### 3. モニタリング

```bash
# Prometheusメトリクス公開
# nifi.properties
nifi.metrics.reporting.task.PrometheusReportingTask.enabled=true
nifi.metrics.reporting.task.PrometheusReportingTask.port=9092

# Grafanaで可視化
```

### 4. バージョン管理（NiFi Registry統合）

```bash
# NiFi Registryでフローをバージョン管理
# Git連携で変更履歴追跡

# フローをRegistryにコミット
# GUI: Process Group右クリック → Version → Start version control
```

## 公式リソース

- **公式サイト**: https://nifi.apache.org/
- **ドキュメント**: https://nifi.apache.org/docs.html
- **ユーザーガイド**: https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
- **GitHub**: https://github.com/apache/nifi
- **NiFi Registry**: https://nifi.apache.org/registry.html

## まとめ

Apache NiFiは、ビジュアルなデータフロー設計と強力なデータプロビナンスにより、複雑なデータ統合・ETL処理を直感的に実装できるツールです。無料でありながら、エンタープライズレベルのデータ系譜追跡・監査機能を提供します。導入フェーズのデータ移行や、継続的なデータパイプライン運用に最適です。

---

**最終更新**: 2025-12-06
**対象バージョン**: Apache NiFi 1.24+
