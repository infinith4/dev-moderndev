# Diagrams (Python)

## 概要

Diagramsは、Pythonコードでクラウドシステムアーキテクチャ図を作成できるオープンソースツールです。AWS、Azure、GCP、Kubernetes、オンプレミス等の公式アイコンを使用し、コードベースで図を生成することで、バージョン管理、自動化、一貫性の保持が可能です。PlantUMLやVisioを使わずに、Pythonの直感的な記述でインフラ構成図、ネットワーク図、システム設計図を作成できます。

## 主な機能

### 1. 主要クラウドプロバイダ対応
- **AWS**: EC2、S3、RDS、Lambda、ECS等200+サービス
- **Azure**: VM、Storage、Functions、AKS等100+サービス
- **GCP**: Compute、Storage、BigQuery、GKE等100+サービス
- **Kubernetes**: Pod、Service、Deployment、Ingress等
- **オンプレミス**: Server、Database、Network等

### 2. Pythonコードベース
- **直感的記述**: Pythonの構文でノード・エッジ定義
- **プログラマブル**: ループ、条件分岐で動的生成
- **バージョン管理**: Gitで図の履歴管理
- **自動生成**: CI/CDで図を自動更新

### 3. 出力形式
- **PNG**: デフォルト出力形式
- **SVG**: スケーラブルベクター形式
- **PDF**: ドキュメント統合用
- **DOT**: Graphviz形式

### 4. カスタマイズ
- **グラフ属性**: サイズ、方向、ランク指定
- **エッジ**: ラベル、色、スタイル
- **クラスタ**: グループ化・整理
- **カスタムアイコン**: 独自画像追加

## 利用方法

### インストール

```bash
# pip インストール
pip install diagrams

# 依存関係（Graphviz）インストール
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows
# https://graphviz.org/download/ からインストーラダウンロード
```

### 基本的な図作成（AWS）

```python
# simple_web_service.py
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Web Service", show=False):
    ELB("lb") >> EC2("web") >> RDS("database")
```

```bash
# 実行（simple_web_service.pngが生成される）
python simple_web_service.py
```

### クラスタ（グループ化）

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53

with Diagram("Clustered Web Services", show=False):
    dns = Route53("dns")
    lb = ELB("lb")

    with Cluster("Web Tier"):
        web_servers = [EC2("web1"),
                       EC2("web2"),
                       EC2("web3")]

    with Cluster("DB Tier"):
        db_master = RDS("master")
        db_master - [RDS("slave1"),
                     RDS("slave2")]

    dns >> lb >> web_servers >> db_master
```

### エッジのカスタマイズ

```python
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("Edge Customization", show=False):
    web = EC2("web")
    db = RDS("db")

    # ラベル付きエッジ
    web >> Edge(label="query") >> db

    # 色付きエッジ
    web >> Edge(color="red", style="dashed") >> db

    # 双方向エッジ
    web - Edge(color="blue") - db
```

### 複数ノードへの接続

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Multiple Connections", show=False):
    lb = ELB("lb")

    # リストで複数EC2作成
    web_servers = [EC2("web1"), EC2("web2"), EC2("web3")]

    # ELBから全webサーバへ
    lb >> web_servers

    # 全webサーバから単一DBへ
    web_servers >> RDS("database")
```

### Kubernetes構成図

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.storage import PV, PVC

with Diagram("Kubernetes Architecture", show=False):
    ingress = Ingress("ingress")

    with Cluster("Namespace: Production"):
        svc = Service("service")

        with Cluster("Deployment"):
            pods = [Pod("pod1"),
                    Pod("pod2"),
                    Pod("pod3")]

        with Cluster("Storage"):
            pvc = PVC("pvc")
            pv = PV("pv")
            pvc - pv

    ingress >> svc >> pods
    pods >> pvc
```

### マルチクラウド構成図

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.azure.compute import VM
from diagrams.gcp.compute import GCE

with Diagram("Multi-Cloud Architecture", show=False):
    with Cluster("AWS"):
        aws_lb = ELB("AWS LB")
        aws_web = EC2("AWS Web")
        aws_lb >> aws_web

    with Cluster("Azure"):
        azure_vm = VM("Azure VM")

    with Cluster("GCP"):
        gcp_compute = GCE("GCP Compute")

    aws_web >> azure_vm
    azure_vm >> gcp_compute
```

### 出力形式指定

```python
from diagrams import Diagram

# PNG出力（デフォルト）
with Diagram("Output PNG", show=False):
    # ...

# SVG出力
with Diagram("Output SVG", show=False, outformat="svg"):
    # ...

# PDF出力
with Diagram("Output PDF", show=False, outformat="pdf"):
    # ...

# 複数形式出力
with Diagram("Multi Format", show=False, outformat=["png", "svg", "pdf"]):
    # ...
```

### グラフ属性カスタマイズ

```python
from diagrams import Diagram

graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "pad": "1.0",
    "ranksep": "1.0",  # ノード間距離
    "nodesep": "0.5"   # 同ランク内ノード間距離
}

with Diagram("Custom Graph", show=False, graph_attr=graph_attr, direction="LR"):
    # direction: TB（上下）, BT（下上）, LR（左右）, RL（右左）
    # ...
```

### プログラマティックな図生成

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB

# 環境変数やループで動的生成
num_servers = 5

with Diagram("Dynamic Generation", show=False):
    lb = ELB("lb")
    web_servers = [EC2(f"web{i}") for i in range(1, num_servers + 1)]
    lb >> web_servers
```

### カスタムアイコン使用

```python
from diagrams import Diagram, Cluster
from diagrams.custom import Custom

with Diagram("Custom Icon", show=False):
    # カスタムアイコン（ローカル画像ファイル）
    custom_service = Custom("My Service", "./icons/my_icon.png")
```

### CI/CD統合（GitHub Actions）

```yaml
name: Generate Diagrams

on:
  push:
    paths:
      - 'diagrams/*.py'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y graphviz
          pip install diagrams

      - name: Generate diagrams
        run: |
          cd diagrams
          for file in *.py; do
            python "$file"
          done

      - name: Commit diagrams
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add diagrams/*.png
          git commit -m "Auto-generate diagrams" || echo "No changes"
          git push
```

### 実用例：3層Webアプリケーション

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB, Route53, CloudFront
from diagrams.aws.storage import S3

with Diagram("3-Tier Web Application", show=False, direction="TB"):
    dns = Route53("DNS")
    cdn = CloudFront("CDN")

    with Cluster("Public Subnet"):
        lb = ELB("Load Balancer")

    with Cluster("Application Tier"):
        with Cluster("Auto Scaling Group"):
            app_servers = [EC2("App 1"),
                          EC2("App 2"),
                          EC2("App 3")]

    with Cluster("Cache Layer"):
        cache = ElastiCache("Redis")

    with Cluster("Database Tier"):
        db_master = RDS("Master")
        db_slaves = [RDS("Slave 1"),
                    RDS("Slave 2")]

    static_assets = S3("Static Assets")

    dns >> cdn >> lb >> app_servers
    app_servers >> cache >> db_master
    db_master >> db_slaves
    cdn >> static_assets
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Diagrams** |  無料 | オープンソース、MIT ライセンス |

## メリット

1. **無料**: MIT ライセンスのオープンソース
2. **コードベース**: Pythonで記述、バージョン管理可能
3. **豊富なアイコン**: AWS/Azure/GCP等400+公式アイコン
4. **自動化**: CI/CDで図を自動生成・更新
5. **プログラマブル**: ループ・条件分岐で動的生成

## デメリット

1. **Graphviz依存**: 別途インストール必要
2. **GUI なし**: コードのみ（ビジュアルエディタなし）
3. **レイアウト制御限定的**: Graphvizの自動レイアウトに依存
4. **学習コスト**: Python・Graphviz知識必要

## 公式リンク

- **公式サイト**: [https://diagrams.mingrammer.com/](https://diagrams.mingrammer.com/)
- **ドキュメント**: [https://diagrams.mingrammer.com/docs/getting-started/installation](https://diagrams.mingrammer.com/docs/getting-started/installation)
- **GitHub**: [https://github.com/mingrammer/diagrams](https://github.com/mingrammer/diagrams)
- **PyPI**: [https://pypi.org/project/diagrams/](https://pypi.org/project/diagrams/)

## 関連ドキュメント

- [PlantUML](../デザインツール/PlantUML.md)
- [Miro](./Miro.md)
- [Confluence](./Confluence.md)

---

**カテゴリ**: ドキュメント・図作成ツール
**対象工程**: システム設計・ドキュメント作成
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0

