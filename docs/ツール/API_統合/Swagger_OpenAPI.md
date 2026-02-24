# Swagger / OpenAPI

## 概要

Swagger / OpenAPI は、REST API の仕様定義、ドキュメント生成、コード生成を支える標準仕様とツール群である。API ファースト開発の基盤として、多くの言語・フレームワークで採用されている。

## 料金

| プラン | 内容 |
|------|------|
| OpenAPI Specification | 無料（標準仕様） |
| OSS ツール | Swagger UI / Swagger Editor / OpenAPI Generator は無料 |
| 商用製品 | 管理・運用機能を含む有料製品あり |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 業界標準 | API 契約の共通フォーマットとして普及 |
| 仕様駆動 | 実装前に API 契約を明確化しやすい |
| 自動生成 | ドキュメントや SDK を生成可能 |
| 高い互換性 | 多数のツールと連携しやすい |
| CI 運用 | 仕様検証をパイプラインへ組み込み可能 |

## 主な機能

### 仕様定義機能

| 機能 | 説明 |
|------|------|
| OpenAPI 定義 | パス、パラメータ、レスポンスを記述 |
| スキーマ再利用 | `components` で共通モデルを管理 |
| セキュリティ定義 | API Key / OAuth / Bearer を定義 |
| 例データ管理 | 実装・テストに使う examples を保持 |

### ドキュメント機能

| 機能 | 説明 |
|------|------|
| Swagger UI | ブラウザで API を閲覧・試行 |
| Swagger Editor | 仕様編集と妥当性確認 |
| ReDoc 連携 | 可読性重視の公開ドキュメントを生成 |
| 共有運用 | 開発者向け API リファレンスを配布 |

### 生成・連携機能

| 機能 | 説明 |
|------|------|
| SDK 生成 | TypeScript、Python、Java などを生成 |
| サーバースタブ | 実装ひな形を自動生成 |
| 仕様検証 | CI で不整合や互換性を確認 |
| ツール連携 | テスト、モック、ゲートウェイへ接続 |

## インストールとセットアップ

公式URL:
- [OpenAPI Specification](https://spec.openapis.org/)
- [Swagger.io](https://swagger.io/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Swagger Editor](https://editor.swagger.io/)
- [OpenAPI Generator](https://openapi-generator.tech/)

セットアップの要点:
1. OpenAPI ファイル（`openapi.yaml`）をリポジトリに作成する。
2. Swagger Editor で仕様を編集し、妥当性を確認する。
3. Swagger UI または ReDoc でドキュメント公開手段を決める。
4. Generator と CI 検証を追加し、自動運用を整備する。

## 基本的な使い方

1. API のエンドポイント、リクエスト、レスポンスを OpenAPI で定義する。
2. 仕様レビューで命名・エラー形式・認証方式を合意する。
3. Swagger UI で仕様の閲覧・簡易検証を行う。
4. OpenAPI Generator で必要な SDK/スタブを生成する。
5. CI で仕様検証を実行し、変更時の破壊的差分を検知する。

最小実行例:
- 仕様編集: Swagger Editor
- ドキュメント表示: Swagger UI
- 生成: OpenAPI Generator

## メリット

- 仕様を単一ソースとして API 契約を明確化しやすい。
- ドキュメント・SDK 生成により開発効率を上げやすい。
- ツール連携が広く、既存環境へ導入しやすい。

## デメリット

- 仕様更新が滞ると実装との乖離が起きやすい。
- 生成コードはそのままでは要件に合わない場合がある。
- チームでの運用ルールがないと記述品質がばらつきやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Swagger/OpenAPI | API 契約標準 | 仕様定義とエコシステム連携が強い |
| Apidog | 設計〜テスト統合 | 実行・モック・共有まで一体化 |
| Stoplight Studio | 設計中心 | GUI 設計とレビューに強い |
| Postman | 実行検証中心 | API テストとコレクション運用に強い |

## ベストプラクティス

### 1. API 契約を先に定義

- 実装着手前に OpenAPI レビューを完了する。
- 破壊的変更ルールを明文化する。

### 2. 仕様と実装を同時更新

- PR で仕様差分と実装差分を同時に確認する。
- examples とエラー仕様を定期的に更新する。

### 3. 自動検証を標準化

- CI で lint/validation を必須化する。
- 主要 API の互換性チェックを継続実行する。

## 公式ドキュメント

- OpenAPI Specification: https://spec.openapis.org/
- Swagger.io: https://swagger.io/
- Swagger UI: https://swagger.io/tools/swagger-ui/
- Swagger Editor: https://editor.swagger.io/
- OpenAPI Generator: https://openapi-generator.tech/

## まとめ

- API 契約を標準化し、設計段階で合意形成を進めやすい。
- ドキュメントと SDK 生成で、開発・連携コストを下げやすい。
- CI 検証を組み込むことで、仕様と実装の整合を維持しやすい。
