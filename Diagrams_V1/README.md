# Diagrams サンプル集

このディレクトリには、Pythonの`diagrams`パッケージを使用したインフラストラクチャ図のサンプルが含まれています。

## セットアップ

### 1. 仮想環境の有効化

```bash
cd /Diagrams_V1
source venv/bin/activate
```

### 2. パッケージのインストール（既にインストール済み）

```bash
pip install diagrams
```

## サンプル図

### 01_simple_web_service.py
AWS 3層Webアプリケーション構成図
- Route53（DNS）
- ELB（ロードバランサー）
- EC2インスタンス（Web層）× 3
- RDS（データベース層）

**実行:**
```bash
python 01_simple_web_service.py
```

**出力:** `01_simple_web_service.png`

### 02_kubernetes_architecture.py
Kubernetesプロダクション環境構成図
- Ingress
- Service
- Pod × 3
- PVC/PV（永続ストレージ）

**実行:**
```bash
python 02_kubernetes_architecture.py
```

**出力:** `02_kubernetes_architecture.png`

### 03_multicloud_architecture.py
マルチクラウド統合アーキテクチャ
- AWS: ELB + EC2 + RDS
- Azure: VM + SQL Database
- GCP: GCE + GCS
- クラウド間連携（API、データ同期）

**実行:**
```bash
python 03_multicloud_architecture.py
```

**出力:** `03_multicloud_architecture.png`

## 全サンプルの一括生成

```bash
for file in *.py; do python "$file"; done
```

## 生成された図の確認

生成されたPNG画像はVSCodeのプレビュー機能で確認できます。

```bash
ls -la *.png
```

## カスタマイズ

各Pythonスクリプトを編集して、以下のカスタマイズが可能です:

- **方向変更**: `direction="LR"` (左→右), `"TB"` (上→下), `"RL"`, `"BT"`
- **出力形式**: `outformat="svg"` または `"pdf"` または `["png", "svg", "pdf"]`
- **コンポーネント追加**: ドキュメントを参照して適切なアイコンをインポート
- **エッジのカスタマイズ**: `Edge(label="...", color="...", style="...")`

## 参考資料

- [Diagrams 公式ドキュメント](https://diagrams.mingrammer.com/)
- [利用可能なノード一覧](https://diagrams.mingrammer.com/docs/nodes/aws)
- [プロジェクトドキュメント](../docs/ツール/プロジェクト管理・ドキュメント/Diagrams.md)

## 依存関係

- Python 3.12+
- diagrams 0.25.1
- Graphviz 2.43.0
