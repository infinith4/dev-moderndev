# AWS Database Migration Service (DMS)

## 概要

AWS Database Migration Service（DMS）は、Amazon Web Services公式のデータベースマイグレーションサービスです。オンプレミス、AWS、他クラウド間でデータベース（Oracle、SQL Server、MySQL、PostgreSQL、MongoDB等）を最小ダウンタイムで移行し、同種・異種データベース間の移行、継続的データレプリケーション、データウェアハウス統合をサポートします。Schema Conversion Tool（SCT）と組み合わせ、データベース現代化を実現します。

## 主な機能

### 1. データベースマイグレーション
- **同種移行**: Oracle→Oracle、MySQL→MySQL
- **異種移行**: Oracle→PostgreSQL、SQL Server→Aurora
- **クラウド移行**: オンプレミス→AWS RDS/Aurora
- **ダウンタイム最小化**: 継続的レプリケーション

### 2. サポートデータベース
- **ソース**: Oracle、SQL Server、MySQL、PostgreSQL、MongoDB、SAP ASE、IBM Db2
- **ターゲット**: RDS、Aurora、Redshift、S3、DynamoDB、Kinesis Data Streams
- **NoSQL**: MongoDB、DocumentDB、Cassandra

### 3. 継続的レプリケーション（CDC）
- **Change Data Capture**: リアルタイム変更取り込み
- **低レイテンシ**: 秒単位の遅延
- **データ同期**: ソース・ターゲット同期
- **検証**: データ整合性チェック

### 4. Schema Conversion Tool（SCT）
- **スキーマ変換**: DDL自動変換
- **コード変換**: ストアドプロシージャ、関数
- **評価レポート**: 移行複雑度評価
- **推奨事項**: 最適化提案

### 5. タスク管理
- **フルロード**: 全データ初期コピー
- **CDC**: 継続的変更同期
- **フルロード+CDC**: 初期コピー後CDC
- **タスク再開**: 障害時自動再開

### 6. データ変換
- **列フィルタ**: 特定列のみ移行
- **行フィルタ**: WHERE条件
- **テーブルマッピング**: テーブル名変換
- **データ型変換**: 自動型変換

## 利用方法

### レプリケーションインスタンス作成

```bash
# AWS CLI
aws dms create-replication-instance \
  --replication-instance-identifier dms-instance-1 \
  --replication-instance-class dms.c5.large \
  --allocated-storage 100 \
  --vpc-security-group-ids sg-12345678 \
  --multi-az
```

### ソースエンドポイント作成

```bash
# オンプレミスMySQL
aws dms create-endpoint \
  --endpoint-identifier source-mysql \
  --endpoint-type source \
  --engine-name mysql \
  --server-name onprem-mysql.example.com \
  --port 3306 \
  --username admin \
  --password "MyPassword123"
```

### ターゲットエンドポイント作成

```bash
# AWS Aurora PostgreSQL
aws dms create-endpoint \
  --endpoint-identifier target-aurora \
  --endpoint-type target \
  --engine-name aurora-postgresql \
  --server-name myaurora.cluster-xxxxx.us-east-1.rds.amazonaws.com \
  --port 5432 \
  --username postgres \
  --password "MyPassword123" \
  --database-name mydb
```

### マイグレーションタスク作成

```bash
# フルロード + CDC
aws dms create-replication-task \
  --replication-task-identifier migration-task-1 \
  --source-endpoint-arn arn:aws:dms:us-east-1:123456789012:endpoint:source-mysql \
  --target-endpoint-arn arn:aws:dms:us-east-1:123456789012:endpoint:target-aurora \
  --replication-instance-arn arn:aws:dms:us-east-1:123456789012:rep:dms-instance-1 \
  --migration-type full-load-and-cdc \
  --table-mappings file://table-mappings.json
```

### テーブルマッピング設定

```json
{
  "rules": [
    {
      "rule-type": "selection",
      "rule-id": "1",
      "rule-name": "include-all-tables",
      "object-locator": {
        "schema-name": "public",
        "table-name": "%"
      },
      "rule-action": "include"
    },
    {
      "rule-type": "transformation",
      "rule-id": "2",
      "rule-name": "rename-schema",
      "rule-target": "schema",
      "object-locator": {
        "schema-name": "public"
      },
      "value": "prod"
    },
    {
      "rule-type": "transformation",
      "rule-id": "3",
      "rule-name": "add-prefix",
      "rule-target": "table",
      "object-locator": {
        "schema-name": "public",
        "table-name": "%"
      },
      "value": "migrated_",
      "rule-action": "add-prefix"
    }
  ]
}
```

### フィルタリング

```json
{
  "rules": [
    {
      "rule-type": "selection",
      "rule-id": "1",
      "rule-name": "filter-customers",
      "object-locator": {
        "schema-name": "public",
        "table-name": "customers"
      },
      "rule-action": "include",
      "filters": [
        {
          "filter-type": "source",
          "column-name": "country",
          "filter-conditions": [
            {
              "filter-operator": "eq",
              "value": "USA"
            }
          ]
        }
      ]
    }
  ]
}
```

### タスク開始・監視

```bash
# タスク開始
aws dms start-replication-task \
  --replication-task-arn arn:aws:dms:us-east-1:123456789012:task:migration-task-1 \
  --start-replication-task-type start-replication

# タスク状態確認
aws dms describe-replication-tasks \
  --filters "Name=replication-task-arn,Values=arn:aws:dms:us-east-1:123456789012:task:migration-task-1"

# テーブル統計
aws dms describe-table-statistics \
  --replication-task-arn arn:aws:dms:us-east-1:123456789012:task:migration-task-1
```

### Schema Conversion Tool（SCT）

```
1. SCTダウンロード・インストール
2. 新規プロジェクト作成
3. ソースDB接続: Oracle 12c
4. ターゲットDB接続: Aurora PostgreSQL
5. Assessment Report生成:
   - 自動変換率: 85%
   - 手動対応必要: 15%
6. スキーマ変換実行
7. 変換後SQLレビュー
8. ターゲットDBへ適用
```

### CloudWatch監視

```bash
# CloudWatch Logs確認
aws logs tail /aws/dms/tasks/migration-task-1 --follow

# メトリクス確認
aws cloudwatch get-metric-statistics \
  --namespace AWS/DMS \
  --metric-name FullLoadThroughputRowsSource \
  --dimensions Name=ReplicationTaskIdentifier,Value=migration-task-1 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

## エディション・料金

| タイプ | 価格 | 特徴 |
|--------|------|------|
| **T3.micro** | 💰 $0.036/時間 | 開発・テスト |
| **C5.large** | 💰 $0.154/時間 | 本番環境（2 vCPU、4GB RAM） |
| **C5.4xlarge** | 💰 $1.235/時間 | 大規模移行（16 vCPU、32GB RAM） |
| **R5.4xlarge** | 💰 $1.344/時間 | メモリ最適化（16 vCPU、128GB RAM） |
| **データ転送** | 🟢 無料 | AWS内転送無料（インターネット転送は有料） |

## メリット

### ✅ 主な利点

1. **マネージド**: サーバー管理不要
2. **最小ダウンタイム**: CDC継続的レプリケーション
3. **異種DB移行**: Oracle→PostgreSQL等
4. **SCT統合**: スキーマ自動変換
5. **サポート範囲**: 主要DB全対応
6. **データ検証**: 整合性チェック
7. **自動再開**: 障害時自動リトライ
8. **CloudWatch統合**: 監視・ログ
9. **セキュリティ**: VPC、SSL、KMS暗号化
10. **スケーラブル**: インスタンスサイズ選択

## デメリット

### ❌ 制約・課題

1. **コスト**: インスタンス時間課金
2. **学習曲線**: 設定複雑
3. **SCT制限**: 100%自動変換不可
4. **LOB制限**: Large Object処理遅い
5. **DDL変更**: CDC中のDDL変更制限
6. **パフォーマンス**: 大規模移行で調整必要
7. **ネットワーク**: オンプレミス接続が煩雑
8. **トラブルシューティング**: エラー解析難しい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Azure Database Migration Service** | Azure DMS | AWS DMSと類似（Azure版） |
| **Google Database Migration Service** | Google Cloud DMS | AWS DMSと類似（GCP版） |
| **Oracle GoldenGate** | エンタープライズレプリケーション | AWS DMSより高機能だが高額 |
| **AWS Glue** | ETL | AWS DMSよりデータ変換特化 |
| **Attunity Replicate** | データレプリケーション | AWS DMSと類似 |

## 公式リンク

- **公式サイト**: [https://aws.amazon.com/dms/](https://aws.amazon.com/dms/)
- **ドキュメント**: [https://docs.aws.amazon.com/dms/](https://docs.aws.amazon.com/dms/)
- **料金**: [https://aws.amazon.com/dms/pricing/](https://aws.amazon.com/dms/pricing/)
- **SCT**: [https://docs.aws.amazon.com/SchemaConversionTool/](https://docs.aws.amazon.com/SchemaConversionTool/)

## 関連ドキュメント

- [マイグレーションツール一覧](../マイグレーションツール/)
- [AWS CLI](../CLIツール/AWS_CLI.md)
- [Amazon RDS](../データベースツール/Amazon_RDS.md)
- [データベースマイグレーションベストプラクティス](../../best-practices/database-migration.md)

---

**カテゴリ**: マイグレーションツール  
**対象工程**: マイグレーション、データ統合  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
