# DBML (Database Markup Language)

## 概要

DBML は、データベーススキーマをコードライクなテキストで記述するためのオープンソースのDSL（ドメイン固有言語）である。Git管理が容易で、可読性の高い記法によりER図の自動生成やSQL DDLへの変換が可能なため、チーム開発でのスキーマ設計・レビューに適している。

## 料金

| プラン | 内容 |
|------|------|
| DBML CLI / dbml-core | 無料（OSS、MIT License） |
| [dbdiagram.io](https://dbdiagram.io/) | 無料プランあり（有料プランで共同編集・エクスポート拡張） |
| [dbdocs.io](https://dbdocs.io/) | 無料プランあり（ドキュメント公開・共有） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| コードベース定義 | テキストでスキーマを記述し、Git管理が可能 |
| 可読性 | シンプルな記法で業務担当者にも読みやすい |
| ER図自動生成 | dbdiagram.io と連携し、記述からER図を自動描画 |
| SQL変換 | DBML → SQL DDL、SQL DDL → DBML の双方向変換に対応 |
| マルチDB対応 | PostgreSQL、MySQL、SQL Server、SQLite 向けのSQL出力が可能 |

## 主な機能

### モデリング機能

| 機能 | 説明 |
|------|------|
| テーブル定義 | カラム名、型、制約（PK、NOT NULL、UNIQUE等）を記述 |
| リレーション定義 | `>` `<` `-` 記法で1:1、1:N、N:Mを表現 |
| Enum定義 | 列挙型をスキーマ内で定義 |
| テーブルグループ | 関連テーブルをグルーピングして整理 |
| ノート・コメント | テーブル・カラムに説明文を付与 |
| インデックス定義 | 複合インデックス、ユニークインデックスを定義 |

### 変換・出力機能

| 機能 | 説明 |
|------|------|
| DBML → SQL | CREATE TABLE文を生成（PostgreSQL / MySQL / SQL Server / SQLite） |
| SQL → DBML | 既存DDLからDBMLへ逆変換 |
| DBML → ER図 | dbdiagram.io で可視化 |
| ドキュメント生成 | dbdocs.io でスキーマドキュメントを公開 |

### 設計支援機能

| 機能 | 説明 |
|------|------|
| 差分レビュー | Gitでスキーマ変更のdiffが取れる |
| CI連携 | CLIツールでCI/CDパイプラインに組み込み可能 |
| チーム共有 | dbdiagram.io / dbdocs.io でブラウザ上から共有 |
| 既存DB取込 | SQL DDLからの逆変換で既存スキーマをDBML化 |

## インストールとセットアップ

公式URL:
- [DBML 公式サイト](https://dbml.dbdiagram.io/)
- [dbml-core (npm)](https://www.npmjs.com/package/@dbml/core)
- [dbdiagram.io](https://dbdiagram.io/)

セットアップの要点:
1. Node.js 環境で `@dbml/cli` をインストールする。
2. `.dbml` ファイルにスキーマを記述する。
3. CLIでSQL変換またはdbdiagram.ioで可視化する。
4. Gitリポジトリでスキーマファイルをバージョン管理する。

```bash
# CLIインストール
npm install -g @dbml/cli

# DBML → SQL変換
dbml2sql schema.dbml --mysql -o output.sql

# SQL → DBML変換
sql2dbml input.sql --mysql -o schema.dbml
```

## 基本的な使い方

```dbml
// テーブル定義
Table users {
  id integer [pk, increment]
  username varchar [not null, unique]
  email varchar [not null]
  created_at timestamp [default: `now()`]
}

Table orders {
  id integer [pk, increment]
  user_id integer [not null]
  total decimal
  status order_status
  created_at timestamp [default: `now()`]
}

// Enum定義
Enum order_status {
  pending
  processing
  completed
  cancelled
}

// リレーション定義
Ref: orders.user_id > users.id
```

最小実行例:
- 入力: 上記の `.dbml` ファイル
- 出力: ER図（dbdiagram.io）+ SQL DDL（CLI変換）

## メリット

- テキストベースでGit管理が容易であり、スキーマ変更のレビューがしやすい。
- シンプルな記法で学習コストが低く、業務担当者にも理解しやすい。
- SQL DDLとの双方向変換により、既存DBからの取込も容易である。
- dbdiagram.io / dbdocs.io との連携でER図やドキュメントを自動生成できる。

## デメリット

- ストアドプロシージャやビューなど、DDL以外のDB機能は記述できない。
- dbdiagram.io の高度な機能（共同編集、PDF出力等）は有料プランが必要。
- 物理設計の詳細（パーティション、テーブルスペース等）は表現範囲外である。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| DBML | コードベースDB設計 | テキスト記述、Git管理、SQL双方向変換 |
| ERDPlus | 学習/小規模ER設計 | 無料でシンプル、ブラウザ完結 |
| MySQL Workbench | MySQL設計/運用 | GUI中心、設計から管理まで統合 |
| PlantUML (ER) | テキストベースUML | 汎用UML、DB特化機能は限定的 |
| tbls | 既存DBドキュメント化 | 稼働中DBからドキュメント自動生成 |

## ベストプラクティス

### 1. スキーマファイルを分割管理する

- ドメイン単位やテーブルグループ単位で `.dbml` ファイルを分割する。
- 大規模スキーマの見通しを維持しやすい。

### 2. Git管理でレビュープロセスに組み込む

- スキーマ変更をPRベースでレビューする。
- `dbml2sql` の出力をCIで検証し、構文エラーを早期検出する。

### 3. 既存DBからの逆変換を活用する

- `sql2dbml` で既存スキーマをDBML化し、現状把握に活用する。
- 移行プロジェクトで新旧スキーマの比較に使いやすい。

## 公式ドキュメント

- DBML公式: https://dbml.dbdiagram.io/
- DBML仕様: https://dbml.dbdiagram.io/docs/
- GitHub: https://github.com/holistics/dbml

## まとめ

1. **設計可視** : テキストベースのスキーマ定義により、ER図やドキュメントを自動生成できる。
2. **効率化** : Git管理・SQL双方向変換により、設計レビューと実装の橋渡しを効率化できる。
3. **品質安定** : コードとしてスキーマを管理することで、変更履歴の追跡と品質維持がしやすい。
