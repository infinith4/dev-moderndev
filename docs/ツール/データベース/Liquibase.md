# Liquibase

## 概要

Liquibase は、データベース変更を ChangeSet 単位で管理するマイグレーションツールである。XML、YAML、JSON、SQL 形式を選択でき、前提条件やロールバックを含む高度なスキーマ運用を実施しやすい。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（基本機能） |
| Pro / Enterprise | 有料（高度な運用・統制機能を拡張） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| ChangeSet 管理 | 変更単位で履歴を追跡しやすい |
| 複数形式対応 | XML/YAML/JSON/SQL を選択可能 |
| ロールバック支援 | 戻し手順を変更定義に含めやすい |
| 条件分岐 | preconditions や context で環境分岐可能 |
| 差分生成 | 既存DBとの差分比較を実施可能 |
| マルチDB対応 | 主要DBへ横断的に適用しやすい |

## 主な機能

### 変更管理機能

| 機能 | 説明 |
|------|------|
| `update` | 未適用 ChangeSet を適用 |
| `rollback` | 指定地点まで変更を巻き戻し |
| `status` | 適用状況を確認 |
| `tag` | リリース時点をタグ化 |

### 設計支援機能

| 機能 | 説明 |
|------|------|
| `generateChangeLog` | 既存DBから初期ChangeLog生成 |
| `diff` | DB間の差分抽出 |
| preconditions | 実行条件を定義して誤適用を防止 |
| context/label | 環境別適用を制御 |

### 自動化機能

| 機能 | 説明 |
|------|------|
| Maven/Gradle統合 | ビルド時に変更適用を自動化 |
| Spring Boot連携 | 起動時マイグレーション実行 |
| CLI実行 | バッチや運用ジョブに組み込み可能 |
| 監査性 | ChangeLog履歴で追跡しやすい |

## インストールとセットアップ

公式URL:
- [Liquibase 公式サイト](https://www.liquibase.org/)
- [Documentation](https://docs.liquibase.com/)
- [GitHub](https://github.com/liquibase/liquibase)
- [Liquibase Maven Plugin](https://mvnrepository.com/artifact/org.liquibase/liquibase-maven-plugin)

セットアップの要点:
1. CLI かビルドツール連携で導入方式を決める。
2. `liquibase.properties` でDB接続情報を設定する。
3. ChangeLog の構成（master + include）を標準化する。
4. rollback 手順を含めた運用ルールを定義する。

## 基本的な使い方

1. `db.changelog-master` を作成し、変更ファイルを include する。
2. ChangeSet を追加し、ID と author を一意に管理する。
3. `liquibase update` で変更を適用する。
4. `liquibase status` で未適用分を確認する。
5. 必要に応じて `liquibase rollback` で復旧する。

最小実行例:
- 適用: `liquibase update`
- 状況確認: `liquibase status`
- 巻き戻し: `liquibase rollbackCount 1`

## メリット

- 複雑な変更管理を構造化して扱いやすい。
- 形式選択の自由度が高く、チーム方針に合わせやすい。
- 条件分岐やロールバックで本番運用の安全性を高めやすい。

## デメリット

- 初期設計（ChangeLog構成、命名規則）に工数がかかる。
- 高機能ゆえに運用ルール未整備だと複雑化しやすい。
- 学習コストは Flyway より高くなりやすい。

## CI/CD での使用

CI では `validate` と `updateSQL` による事前確認を行い、CD段階で `update` を適用する運用が有効である。リリースタグ運用と組み合わせると、障害時の復旧判断を行いやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Liquibase | 高度なDB変更管理 | 条件分岐・ロールバック設計に強い |
| Flyway | SQL中心の変更管理 | シンプルで導入しやすい |
| Alembic | Python ORM連携 | SQLAlchemy 環境向け |
| Prisma Migrate | Node.js ORM運用 | スキーマ定義から移行しやすい |

## ベストプラクティス

### 1. ChangeSet 一意性を担保

- `id` と `author` の重複を防止する。
- リリース単位でフォルダ整理する。

### 2. rollback を必ず設計

- 重要ChangeSetには rollback を明示する。
- 破壊的変更は復旧手順を別途文書化する。

### 3. 環境分岐を最小化

- context/label の乱用を避ける。
- 共通ChangeSetを基本にして差分を減らす。

## 公式ドキュメント

- 公式サイト: https://www.liquibase.org/
- Documentation: https://docs.liquibase.com/
- GitHub: https://github.com/liquibase/liquibase
- Maven Plugin: https://mvnrepository.com/artifact/org.liquibase/liquibase-maven-plugin

## まとめ

1. **計画運用** : ChangeSet 管理により、複雑なDB変更を計画的に運用しやすい。
2. **安全性** : 条件分岐とロールバックで本番適用リスクを抑えやすい。
3. **安定化** : ルール設計を先に固めることで、継続運用を安定化しやすい。
