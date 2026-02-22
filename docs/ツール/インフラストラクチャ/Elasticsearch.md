# Elasticsearch

## 概要

Elasticsearchは、分散型全文検索・分析エンジンです。RESTful API、リアルタイムインデックス、全文検索、集計分析、スケーラビリティにより、ログ分析、アプリケーション検索、セキュリティ分析を実現します。Elastic Stack（Elasticsearch、Kibana、Logstash、Beats）の中核として、大規模データ検索・可視化で広く採用されています。

## 主な機能

### 1. 全文検索
- **インデックス**: 転置インデックス
- **クエリDSL**: JSON検索クエリ
- **アナライザー**: 形態素解析
- **スコアリング**: 関連度スコア

### 2. 分析
- **集計**: Aggregations
- **メトリクス**: 統計計算
- **バケット**: グルーピング
- **パイプライン**: 集計パイプライン

### 3. スケーラビリティ
- **シャーディング**: 水平分割
- **レプリケーション**: 高可用性
- **クラスタリング**: 複数ノード

## 利用方法

### インストール（Docker）

```bash
docker run -d --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  elasticsearch:8.11.0

# 確認
curl http://localhost:9200
```

### インデックス作成

```bash
# インデックス作成
curl -X PUT "localhost:9200/products" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "price": { "type": "integer" },
      "category": { "type": "keyword" }
    }
  }
}
'

# ドキュメント追加
curl -X POST "localhost:9200/products/_doc" -H 'Content-Type: application/json' -d'
{
  "name": "Laptop",
  "price": 80000,
  "category": "electronics"
}
'
```

### 検索クエリ

```bash
# マッチクエリ
curl -X GET "localhost:9200/products/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "name": "laptop"
    }
  }
}
'

# 複合クエリ
curl -X GET "localhost:9200/products/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "category": "electronics" } }
      ],
      "filter": [
        { "range": { "price": { "gte": 50000, "lte": 100000 } } }
      ]
    }
  }
}
'
```

### Node.js（@elastic/elasticsearch）

```javascript
const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: 'http://localhost:9200' });

// 検索
const result = await client.search({
  index: 'products',
  query: {
    match: { name: 'laptop' }
  }
});

console.log(result.hits.hits);

// 集計
const aggResult = await client.search({
  index: 'products',
  size: 0,
  aggs: {
    avg_price: {
      avg: { field: 'price' }
    }
  }
});
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Elasticsearch (OSS)** | 🟢 無料 | オープンソース、SSPL/Elastic License |
| **Elastic Cloud** | 💰 $95/月〜 | マネージドElasticsearch |
| **AWS OpenSearch** | 💰 従量課金 | AWS版Elasticsearch |

## メリット

1. **高速検索**: 全文検索高速
2. **スケーラブル**: 水平スケール
3. **リアルタイム**: 準リアルタイム
4. **REST API**: シンプルAPI
5. **Elastic Stack**: Kibana統合

## デメリット

1. **複雑性**: 学習曲線steep
2. **メモリ**: メモリ消費大
3. **運用**: クラスタ運用複雑
4. **ライセンス**: OSSライセンス変更

## 公式リンク

- **公式サイト**: [https://www.elastic.co/elasticsearch/](https://www.elastic.co/elasticsearch/)
- **ドキュメント**: [https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

## 関連ドキュメント

- [検索ツール一覧](../検索ツール/)
- [Kibana](../可視化ツール/Kibana.md)
- [Logstash](../ログ処理ツール/Logstash.md)

---

**カテゴリ**: 検索ツール
**対象工程**: ログ分析・アプリケーション検索
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
