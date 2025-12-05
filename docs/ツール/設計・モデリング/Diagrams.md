# Diagrams (Python)

## 概要

Diagramsは、Pythonコードでクラウドアーキテクチャ図を作成するオープンソースライブラリです。AWS、Azure、GCP、Kubernetes、オンプレミス等のアイコンを使用し、コードでインフラ構成を表現します。「Diagram as Code」として、バージョン管理可能、自動生成可能な図を作成でき、ドキュメントとコードの一貫性を保ちます。

## 主な機能

### 1. マルチクラウド対応
- **AWS**: EC2、S3、RDS、Lambda等 200+サービス
- **Azure**: VM、Storage、Functions等
- **GCP**: Compute Engine、Cloud Storage等
- **Kubernetes**: Pod、Service、Deployment等
- **オンプレミス**: Nginx、PostgreSQL、Redis等

### 2. コードで図作成
- **Pythonコード**: クラスとコンテキストマネージャー
- **自動レイアウト**: Graphviz自動配置
- **エッジ**: ノード間の接続
- **クラスタ**: グループ化

### 3. 出力形式
- **PNG**: ラスター画像
- **SVG**: ベクター画像
- **PDF**: PDF出力
- **DOT**: Graphvizソースコード

### 4. バージョン管理
- **Git管理**: Pythonファイルとして管理
- **差分比較**: コード差分で変更確認
- **CI/CD**: 自動図生成

## 利用方法

### インストール

```bash
# pip
pip install diagrams

# Graphvizインストール（必須）
# Ubuntu/Debian
sudo apt install graphviz

# macOS
brew install graphviz

# Windows
# https://graphviz.org/download/ からインストール
```

### 基本例

```python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Simple Web Service", show=False):
    ELB("lb") >> EC2("web") >> RDS("db")
```

### AWS 3-Tier Architecture

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.storage import S3

with Diagram("AWS 3-Tier Architecture", show=False, direction="TB"):
    dns = Route53("dns")
    lb = ELB("load balancer")
    
    with Cluster("Web Tier"):
        web_group = [EC2("web1"),
                     EC2("web2"),
                     EC2("web3")]
    
    with Cluster("Application Tier"):
        app_group = [EC2("app1"),
                     EC2("app2")]
    
    with Cluster("Database Tier"):
        db_primary = RDS("primary")
        db_standby = RDS("standby")
    
    storage = S3("storage")
    
    dns >> lb >> web_group >> app_group >> db_primary
    db_primary - db_standby
    app_group >> storage
```

### Kubernetes Deployment

```python
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

with Diagram("Kubernetes Architecture", show=False):
    ingress = Ingress("my-app.com")
    
    with Cluster("Namespace: default"):
        svc = Service("web-service")
        
        with Cluster("Deployment"):
            pods = [Pod("pod1"),
                    Pod("pod2"),
                    Pod("pod3")]
    
    ingress >> svc >> pods
```

### Microservices

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka

with Diagram("Microservices Architecture", show=False):
    users = Users("users")
    
    with Cluster("Load Balancer"):
        lb = Nginx("nginx")
    
    with Cluster("Services"):
        svc1 = Docker("auth-service")
        svc2 = Docker("user-service")
        svc3 = Docker("order-service")
    
    with Cluster("Data Layer"):
        db1 = PostgreSQL("users-db")
        db2 = MongoDB("orders-db")
        cache = Redis("cache")
    
    queue = Kafka("event-bus")
    
    users >> lb >> [svc1, svc2, svc3]
    svc1 >> db1
    svc2 >> db1
    svc2 >> cache
    svc3 >> db2
    [svc1, svc2, svc3] >> Edge(color="firebrick") >> queue
```

### カスタムスタイル

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2

with Diagram("Custom Style", show=False, graph_attr={"fontsize": "20"}):
    with Cluster("Cluster 1", graph_attr={"bgcolor": "lightblue"}):
        ec2_1 = EC2("ec2-1")
    
    with Cluster("Cluster 2"):
        ec2_2 = EC2("ec2-2")
    
    ec2_1 >> Edge(color="red", style="dashed") >> ec2_2
```

### CI/CD統合

```yaml
# .github/workflows/diagrams.yml
name: Generate Architecture Diagrams

on:
  push:
    paths:
      - 'diagrams/*.py'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          sudo apt-get install -y graphviz
          pip install diagrams
      
      - name: Generate diagrams
        run: |
          python diagrams/architecture.py
      
      - name: Commit diagrams
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add *.png
          git commit -m "Update architecture diagrams"
          git push
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Diagrams** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

### ✅ 主な利点

1. **完全無料**: オープンソース、MIT License
2. **コードで管理**: Pythonコードでバージョン管理
3. **自動生成**: CI/CDで自動更新
4. **マルチクラウド**: AWS、Azure、GCP対応
5. **豊富なアイコン**: 公式アイコン使用
6. **Git統合**: 差分比較、レビュー可能
7. **プログラマブル**: ループ、条件分岐可能
8. **軽量**: Pythonスクリプトのみ
9. **自動レイアウト**: Graphviz自動配置
10. **ドキュメントとコードの一貫性**: コードから図生成

## デメリット

### ❌ 制約・課題

1. **Python必須**: Python習得必要
2. **レイアウト制御**: 手動配置困難
3. **インタラクティブ不可**: 静的画像のみ
4. **細かい調整**: GUI図より調整難しい
5. **Graphviz依存**: Graphvizインストール必要
6. **学習曲線**: API習得必要
7. **プレビュー**: 実行しないと図が見えない
8. **複雑な図**: 大規模図は見づらい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **CloudCraft** | AWS GUI図作成 | Diagramsよりビジュアル |
| **Lucidchart** | クラウド作図 | Diagramsより柔軟だがコード非対応 |
| **draw.io** | 汎用作図 | Diagramsより柔軟だがコード非対応 |
| **Mermaid** | テキストベース図 | Diagramsと類似、マークダウン統合 |
| **PlantUML** | テキストベースUML | Diagramsと類似、UML特化 |

## 公式リンク

- **GitHub**: [https://github.com/mingrammer/diagrams](https://github.com/mingrammer/diagrams)
- **ドキュメント**: [https://diagrams.mingrammer.com/](https://diagrams.mingrammer.com/)
- **アイコン一覧**: [https://diagrams.mingrammer.com/docs/nodes/aws](https://diagrams.mingrammer.com/docs/nodes/aws)

## 関連ドキュメント

- [作図ツール一覧](../作図ツール/)
- [Mermaid](./Mermaid.md)
- [PlantUML](./PlantUML.md)
- [Lucidchart](./Lucidchart.md)
- [アーキテクチャ図作成ベストプラクティス](../../best-practices/architecture-diagrams.md)

---

**カテゴリ**: 作図ツール  
**対象工程**: 設計、ドキュメント作成  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
