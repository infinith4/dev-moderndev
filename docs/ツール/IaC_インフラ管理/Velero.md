# Velero

## 概要

Veleroは、Kubernetesクラスタのバックアップ・リストア・マイグレーションを行うオープンソースツールです。クラスタリソース（Deployment、Service、ConfigMap等）と永続ボリューム（PersistentVolume）を一括でバックアップし、障害時の復旧やクラスタ間のワークロード移行を実現します。AWS S3、Google Cloud Storage、Azure Blob Storage等の主要オブジェクトストレージに対応し、定期スケジュールバックアップやリソースフィルタリングなど、本番環境の運用に必要な機能を備えたKubernetesネイティブのディザスタリカバリソリューションです。

## 主な機能

### 1. バックアップ
- **クラスタリソース**: Deployment、Service、ConfigMap等のバックアップ
- **永続ボリューム**: PersistentVolumeのスナップショット
- **名前空間フィルタ**: 特定Namespaceのバックアップ
- **ラベルフィルタ**: ラベルセレクタによる対象選択

### 2. リストア
- **完全復元**: クラスタ全体の復元
- **部分復元**: 特定リソースのみの復元
- **名前空間マッピング**: 復元先Namespaceの変更
- **リソース競合**: 既存リソースとの競合ポリシー

### 3. スケジュール
- **定期バックアップ**: cron式によるスケジュール設定
- **保持ポリシー**: バックアップの自動削除（TTL）
- **並列実行制御**: 同時バックアップ数の制限

### 4. マイグレーション
- **クラスタ間移行**: 異なるクラスタ間のワークロード移行
- **クラウド間移行**: マルチクラウド間のマイグレーション
- **バージョンアップ**: Kubernetesバージョンアップ時の移行

### 5. ストレージプロバイダー
- **AWS S3**: Amazon S3およびS3互換ストレージ
- **GCS**: Google Cloud Storage
- **Azure Blob**: Azure Blob Storage
- **MinIO**: オンプレミスS3互換ストレージ

## 利用方法

### インストール

```bash
# Velero CLIのインストール（macOS）
brew install velero

# Velero CLIのインストール（Linux）
curl -Lo velero.tar.gz https://github.com/vmware-tanzu/velero/releases/download/v1.13.0/velero-v1.13.0-linux-amd64.tar.gz
tar -xzf velero.tar.gz
sudo mv velero-v1.13.0-linux-amd64/velero /usr/local/bin/

# バージョン確認
velero version
```

### AWS S3でのセットアップ

```bash
# IAMポリシー（velero-policy.json）を作成
cat > velero-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": "arn:aws:s3:::my-velero-bucket/*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::my-velero-bucket"
        }
    ]
}
EOF

# 認証情報ファイルの作成
cat > credentials-velero <<EOF
[default]
aws_access_key_id=<ACCESS_KEY_ID>
aws_secret_access_key=<SECRET_ACCESS_KEY>
EOF

# Veleroのインストール（AWSプラグイン）
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket my-velero-bucket \
  --backup-location-config region=ap-northeast-1 \
  --snapshot-location-config region=ap-northeast-1 \
  --secret-file ./credentials-velero
```

### Azure Blob Storageでのセットアップ

```bash
# Veleroのインストール（Azureプラグイン）
velero install \
  --provider azure \
  --plugins velero/velero-plugin-for-microsoft-azure:v1.9.0 \
  --bucket velero-backups \
  --backup-location-config resourceGroup=myResourceGroup,storageAccount=myStorageAccount \
  --secret-file ./credentials-velero
```

### バックアップ操作

```bash
# クラスタ全体のバックアップ
velero backup create full-backup

# 特定Namespaceのバックアップ
velero backup create app-backup \
  --include-namespaces production,staging

# ラベルセレクタによるバックアップ
velero backup create labeled-backup \
  --selector app=web

# 特定リソースタイプのバックアップ
velero backup create deploy-backup \
  --include-resources deployments,services,configmaps

# TTL（有効期限）付きバックアップ
velero backup create daily-backup --ttl 720h  # 30日間保持

# バックアップの一覧
velero backup get

# バックアップの詳細
velero backup describe full-backup
velero backup describe full-backup --details

# バックアップログの確認
velero backup logs full-backup
```

### リストア操作

```bash
# バックアップからの完全リストア
velero restore create --from-backup full-backup

# 特定Namespaceのリストア
velero restore create --from-backup full-backup \
  --include-namespaces production

# Namespaceマッピング付きリストア
velero restore create --from-backup full-backup \
  --namespace-mappings production:staging

# 特定リソースタイプのみリストア
velero restore create --from-backup full-backup \
  --include-resources deployments,services

# リストアの一覧
velero restore get

# リストアの詳細
velero restore describe <restore-name>
```

### スケジュールバックアップ

```bash
# 毎日AM3時にバックアップ（UTC）
velero schedule create daily-backup \
  --schedule="0 3 * * *" \
  --ttl 720h

# 毎週日曜日のバックアップ
velero schedule create weekly-backup \
  --schedule="0 0 * * 0" \
  --include-namespaces production \
  --ttl 2160h  # 90日間保持

# 6時間ごとのバックアップ
velero schedule create frequent-backup \
  --schedule="0 */6 * * *" \
  --include-namespaces critical-apps \
  --ttl 168h  # 7日間保持

# スケジュールの一覧
velero schedule get

# スケジュールの詳細
velero schedule describe daily-backup

# スケジュールの削除
velero schedule delete daily-backup
```

### ディザスタリカバリの手順

```bash
# 1. 新しいクラスタでVeleroをインストール（同じストレージ設定）
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket my-velero-bucket \
  --backup-location-config region=ap-northeast-1 \
  --snapshot-location-config region=ap-northeast-1 \
  --secret-file ./credentials-velero

# 2. 利用可能なバックアップを確認
velero backup get

# 3. 最新のバックアップからリストア
velero restore create disaster-recovery \
  --from-backup daily-backup-20240101030000

# 4. リストアの状態確認
velero restore describe disaster-recovery
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Velero** | 無料 | オープンソース、Apache-2.0 License |

## メリット

### 主な利点

1. **Kubernetesネイティブ**: CRDとコントローラーによるK8s統合
2. **マルチクラウド**: AWS、GCP、Azureの主要クラウドに対応
3. **スケジュール**: cron式による定期自動バックアップ
4. **選択的バックアップ**: Namespace、ラベル、リソース単位のフィルタリング
5. **マイグレーション**: クラスタ間・クラウド間のワークロード移行
6. **プラグイン**: ストレージプロバイダーのプラグイン拡張
7. **CLI操作**: 直感的なコマンドラインインターフェース
8. **CNCF準拠**: CNCF Sandboxプロジェクト
9. **PV対応**: 永続ボリュームのスナップショット
10. **オンプレ対応**: MinIO等のS3互換ストレージ利用可能

## デメリット

### 制約・課題

1. **ストレージコスト**: バックアップデータのストレージ費用
2. **リストア時間**: 大規模クラスタのリストアに時間がかかる
3. **PV制約**: CSIドライバー対応が必要な場合がある
4. **設定複雑**: IAMポリシーやストレージ設定が煩雑
5. **アプリ整合性**: アプリケーションレベルの一貫性保証は別途必要
6. **監視**: バックアップ失敗の監視体制構築が必要
7. **暗号化**: バックアップデータの暗号化は別途設定が必要
8. **バージョン互換**: Kubernetes/Veleroバージョン間の互換性確認

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Kasten K10** | エンタープライズK8sバックアップ | Veleroより高機能だが有償 |
| **Stash** | Kubernetesバックアップ | Veleroと類似だがHelm中心 |
| **Longhorn** | 分散ブロックストレージ | ストレージレベルのバックアップ |
| **etcd snapshot** | etcdのスナップショット | クラスタ状態のみ（PV非対応） |
| **Restic** | ファイルバックアップ | Veleroのバックエンドとしても利用 |

## 公式リンク

- **公式サイト**: [https://velero.io/](https://velero.io/)
- **ドキュメント**: [https://velero.io/docs/](https://velero.io/docs/)
- **GitHub**: [https://github.com/vmware-tanzu/velero](https://github.com/vmware-tanzu/velero)
- **プラグイン一覧**: [https://velero.io/plugins/](https://velero.io/plugins/)

## 関連ドキュメント

- [IaCインフラ管理一覧](../IaCインフラ管理/)
- [tflint](./tflint.md)
- [CloudFormation Guard](./CloudFormation_Guard.md)

---

**カテゴリ**: IaCインフラ管理
**対象工程**: 運用・保守
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
