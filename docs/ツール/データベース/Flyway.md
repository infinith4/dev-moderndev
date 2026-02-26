# Flyway

## 概要

Flyway は、データベーススキーマの変更履歴をバージョン管理するマイグレーションツールである。SQL ベースで変更を管理し、開発・検証・本番のスキーマ差分を抑えて運用しやすくする。

## 料金

| プラン | 内容 |
|------|------|
| Community | 無料（基本的なマイグレーション機能） |
| Teams / Enterprise | 有料（高度な運用機能やサポートを拡張） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| SQL ベース運用 | 既存SQL資産を活かして導入しやすい |
| バージョン管理 | `V__` 形式で変更履歴を追跡 |
| 差分防止 | 環境間で同一順序の適用を担保しやすい |
| マルチDB対応 | 主要RDBMSで利用可能 |
| CI/CD 統合 | Maven/Gradle/CLI で自動実行可能 |
| 学習容易 | シンプルな運用モデルで理解しやすい |

## 主な機能

### マイグレーション管理機能

| 機能 | 説明 |
|------|------|
| `migrate` | 未適用マイグレーションを順次適用 |
| `info` | 適用済み/未適用状況を確認 |
| `validate` | スクリプト整合性を検証 |
| `repair` | 履歴テーブルの不整合を修復 |

### スクリプト運用機能

| 機能 | 説明 |
|------|------|
| バージョン付きSQL | `V1__init.sql` 形式で履歴管理 |
| リピータブルSQL | `R__view.sql` で再適用対象を管理 |
| ベースライン | 既存DB導入時の起点を設定 |
| 複数スキーマ対応 | 対象スキーマを指定して運用可能 |

### 自動化機能

| 機能 | 説明 |
|------|------|
| Maven/Gradle統合 | ビルド時に自動適用可能 |
| CLI 実行 | バッチ・ジョブから実行可能 |
| Docker 実行 | 実行環境差分を減らして運用可能 |
| 失敗検知 | 適用失敗をCIで即時検知しやすい |

## インストールとセットアップ

公式URL:
- [Flyway 公式サイト](https://flywaydb.org/)
- [Documentation](https://documentation.red-gate.com/flyway)
- [GitHub](https://github.com/flyway/flyway)
- [Maven Plugin](https://mvnrepository.com/artifact/org.flywaydb/flyway-maven-plugin)

セットアップの要点:
1. CLI、Maven、Gradle のいずれか導入方式を決める。
2. `flyway.conf` で接続先とマイグレーション場所を設定する。
3. バージョン命名規則（`V__`, `R__`）をチームで統一する。
4. CI で `validate` と `migrate` の実行順を標準化する。

## 基本的な使い方

1. `db/migration` に SQL マイグレーションファイルを配置する。
2. `flyway info` で適用状況を確認する。
3. `flyway migrate` で未適用変更を反映する。
4. 失敗時は原因修正後に `flyway repair` を検討する。
5. 本番適用前に同条件で検証環境を通す。

最小実行例:
- 情報確認: `flyway info`
- 適用: `flyway migrate`
- 検証: `flyway validate`

## メリット

- SQL 中心の運用で導入ハードルが低い。
- 履歴管理により環境差分を抑えやすい。
- CI 組み込みでスキーマ変更の品質を担保しやすい。

## デメリット

- 複雑なデータ移行は追加スクリプト設計が必要。
- 競合マイグレーションの解決ルールが必要。
- 高度機能は有料プラン前提になる場合がある。

## CI/CD での使用

CI では `validate` を先行実行し、問題がない場合のみ `migrate` を実行する運用が一般的である。PR時点で検証環境へ適用し、競合や破壊的変更を早期に検出すると安全性を高めやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Flyway | SQLベースのスキーマ管理 | シンプルで導入しやすい |
| Liquibase | 高度な変更管理 | XML/YAML/JSON対応で柔軟性が高い |
| Alembic | Python系マイグレーション | SQLAlchemyとの親和性が高い |
| Prisma Migrate | Node.js ORM運用 | スキーマ駆動で扱いやすい |

## ベストプラクティス

### 1. 命名規則を固定

- `V{version}__{description}.sql` を統一する。
- ファイル名だけで意図が読めるようにする。

### 2. 変更粒度を小さく保つ

- 1変更1ファイルでレビューしやすくする。
- 大規模変更は段階分割して適用する。

### 3. 本番前検証を必須化

- 本番相当データで適用テストを行う。
- ロールバック方針（手順書）を事前に定義する。

## 公式ドキュメント

- 公式サイト: https://flywaydb.org/
- Documentation: https://documentation.red-gate.com/flyway
- GitHub: https://github.com/flyway/flyway
- Maven Plugin: https://mvnrepository.com/artifact/org.flywaydb/flyway-maven-plugin

## まとめ

1. **履歴管理** : SQLベースでスキーマ変更履歴を一貫管理しやすい。
2. **差分抑制** : 環境差分を減らし、デプロイ時の変更リスクを抑えやすい。
3. **安定運用** : CI で検証手順を固定すると、継続運用の安定性を高めやすい。
