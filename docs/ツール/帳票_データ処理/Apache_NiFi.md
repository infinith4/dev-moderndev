# Apache NiFi

## 概要

Apache NiFiは、オープンソースのデータフロー自動化ツールです。Webベースのビジュアルエディタで、複雑なデータパイプラインを設計・管理し、様々なデータソース間でのデータルーティング、変換、システム統合を実現します。元々はNSAで開発され、現在はApache Software Foundationが管理しています。

## 主な特徴

| 項目 | 内容 |
|------|------|
| 開発元 | Apache Software Foundation（元NSA開発） |
| ライセンス | Apache License 2.0（無料） |
| 設計方式 | ビジュアル（ドラッグ&ドロップ）でデータフロー構築 |
| プロセッサー | 300以上のビルトインプロセッサー |
| データ来歴 | FlowFileの完全な履歴追跡（データプロビナンス） |
| スケーラビリティ | クラスタ構成でスケールアウト対応 |
| バックプレッシャー | フロー制御による安定動作 |

## 主な機能

### データ取り込み・送信

| 機能 | 説明 |
|------|------|
| HTTP/FTP/SFTP | Webやファイルサーバーからのデータ取得・送信 |
| Kafka連携 | ConsumeKafka/PublishKafkaプロセッサー |
| AWS S3 | PutS3Object/FetchS3Objectプロセッサー |
| データベース | JDBC経由のデータ読み書き（PutSQL/ExecuteSQL） |

### データ変換

| 機能 | 説明 |
|------|------|
| ConvertRecord | JSON/CSV/Avro等の形式間変換 |
| EvaluateJsonPath | JSONフィールドの抽出 |
| RouteOnAttribute | 属性値による条件分岐 |
| 式言語 | FlowFile属性の参照・操作 |

### 管理・監視

| 機能 | 説明 |
|------|------|
| プロセスグループ | 論理的なフローのグループ化 |
| パラメーターコンテキスト | 環境別の設定外部化 |
| REST API | プログラマティックなフロー操作 |
| NiFi Registry | フローのバージョン管理 |

## インストールとセットアップ

公式URL:
- [Apache NiFi 公式サイト](https://nifi.apache.org/)
- [NiFi ドキュメント](https://nifi.apache.org/docs.html)

### Docker でのインストール

```bash
# Docker Composeで起動
docker-compose up -d

# ブラウザでアクセス
# https://localhost:8443/nifi/
# ユーザー: admin
# パスワード: adminadminadmin
```

### スタンドアロンインストール

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
```

## 基本的な使い方

### 1. データフローの作成（HTTP to S3）

**GUI操作手順**:

1. ツールバーからProcessorアイコンをドラッグし、GetHTTPを追加
   - URL: `https://api.example.com/data`
   - Filename: `data.json`
2. PutS3Objectプロセッサーを追加
   - Bucket: `my-data-bucket`
   - Region: `us-east-1`
3. GetHTTPの"success"リレーションシップをPutS3Objectに接続
4. 各プロセッサーを右クリック → Start

### 2. データ変換（JSON to CSV）

プロセッサー構成:

1. **GetFile**: ローカルファイル読み込み
2. **ConvertRecord**: JSON → CSV変換
   - Record Reader: JsonTreeReader
   - Record Writer: CSVRecordSetWriter
3. **PutFile**: CSV出力

### 3. 式言語（Expression Language）

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
${fileSize:gt(1000000)}
${mime.type:equals('application/json')}
```

### 4. REST API操作

```bash
# プロセッサーグループ一覧取得
curl -k -u admin:adminadminadmin \
  https://localhost:8443/nifi-api/flow/process-groups/root

# プロセッサー起動
curl -k -u admin:adminadminadmin -X PUT \
  -H "Content-Type: application/json" \
  -d '{"revision":{"version":0},"state":"RUNNING"}' \
  https://localhost:8443/nifi-api/processors/{processor-id}/run-status
```

## Docker での使用

### docker-compose.yml 例

```yaml
version: '3.8'
services:
  nifi:
    image: apache/nifi:latest
    ports:
      - "8443:8443"
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

## 他ツールとの比較

### Apache NiFi vs Apache Airflow

| 機能 | Apache NiFi | Apache Airflow |
|------|-------------|----------------|
| 設計方式 | ビジュアル（GUI） | コードベース（Python） |
| 処理方式 | リアルタイム＋バッチ | バッチ処理中心 |
| データ来歴 | ネイティブ対応 | 限定的 |
| コードレビュー | 困難（XML定義） | 容易（Pythonコード） |
| 適用場面 | データフロー・ETL | スケジュール管理 |

### Apache NiFi vs Airbyte

| 機能 | Apache NiFi | Airbyte |
|------|-------------|---------|
| 用途 | 汎用データフロー | ELT特化 |
| コネクタ | 300+プロセッサー | 350+コネクタ |
| 設定 | GUI中心 | GUI + YAML |
| コスト | 無料 | 無料〜有料 |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| ETLパイプライン | 複雑なデータ統合 | 300+プロセッサーで多様なデータソースを接続 |
| データ移行 | システム間データ転送 | ビジュアル設計で移行フローを構築 |
| リアルタイム処理 | ストリーミングデータ処理 | Kafka連携によるイベント処理 |
| 監査対応 | データ系譜の追跡 | データプロビナンスで完全な来歴を記録 |

## ベストプラクティス

### 1. プロセスグループの活用

- 論理的な単位（取り込み、変換、出力）でグループ化
- フローの可読性と管理性を向上

### 2. パラメーターコンテキスト

- 環境変数的に設定を外部化（開発/本番の切り替え）
- 接続先、バケット名等を環境別に管理

### 3. NiFi Registry統合

- フロー定義をバージョン管理
- Git連携で変更履歴を追跡

### 4. モニタリング

- Prometheusメトリクスを公開しGrafanaで可視化
- バックプレッシャー設定でフロー制御を最適化

## トラブルシューティング

### よくある問題と解決策

#### 1. メモリ不足でNiFiが停止する

```
原因: Java VMのヒープメモリ設定が小さい
解決策: bootstrap.conf で java.arg.Xmx を増やす（例: -Xmx4g）
```

#### 2. プロセッサーが動作しない

```
原因: リレーションシップが未接続または自動終了設定が不足
解決策: すべてのリレーションシップ（success/failure）を接続または自動終了に設定する
```

#### 3. データプロビナンスのディスク消費

```
原因: プロビナンスリポジトリのサイズ上限が大きい
解決策: nifi.propertiesでnifi.provenance.repository.max.storage.sizeを調整する
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: [https://nifi.apache.org/](https://nifi.apache.org/)
- ドキュメント: [https://nifi.apache.org/docs.html](https://nifi.apache.org/docs.html)
- ユーザーガイド: [https://nifi.apache.org/docs/nifi-docs/html/user-guide.html](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html)

### コミュニティ
- GitHub: [https://github.com/apache/nifi](https://github.com/apache/nifi)
- NiFi Registry: [https://nifi.apache.org/registry.html](https://nifi.apache.org/registry.html)

## まとめ

Apache NiFiは、以下の場面で特に有用です:

1. **複雑なデータフロー** - ビジュアルなGUIで直感的にデータパイプラインを設計・管理
2. **データ監査・コンプライアンス** - データプロビナンスにより完全なデータ系譜追跡が可能
3. **リアルタイムデータ統合** - Kafka等と連携し、ストリーミングデータ処理にも対応

無料でありながらエンタープライズレベルのデータ来歴追跡・監査機能を提供し、導入フェーズのデータ移行や継続的なデータパイプライン運用に最適です。
