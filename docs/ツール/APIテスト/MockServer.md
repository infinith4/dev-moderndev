# MockServer

## 概要

MockServer は、HTTP/HTTPS API をモック・スタブ化できるオープンソースツールである。API 実体が未完成でも期待するリクエストとレスポンスを定義して、フロントエンド開発や自動テストを先行できる。OpenAPI 連携、プロキシ/録画、検証 API を備え、契約テストにも使いやすい。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（Apache License 2.0） |
| 商用利用 | ライセンス上可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 柔軟なマッチング | パス、クエリ、ヘッダー、Cookie、Body を条件指定 |
| 動的レスポンス | テンプレートやスクリプトで可変レスポンスを返却 |
| OpenAPI 連携 | 仕様からモック生成、契約ベースの検証 |
| 検証機能 | 呼び出し有無、回数、順序の検証が可能 |
| プロキシ/録画 | 実 API を中継しながら Expectation を生成 |
| 実行形態 | Java ライブラリ、スタンドアロン、Docker で利用可能 |

## 主な機能

### モック定義機能

| 機能 | 説明 |
|------|------|
| Expectation | リクエスト条件とレスポンスをペアで定義 |
| レスポンス制御 | ステータス、ヘッダー、Body、遅延、エラーを設定 |
| テンプレート | リクエスト内容に応じた動的レスポンス |
| 優先度/TTL | 使い捨てモックや期限付きモックを管理 |

### OpenAPI/契約テスト機能

| 機能 | 説明 |
|------|------|
| 仕様ベース起動 | OpenAPI URL/ファイルからモックを生成 |
| スキーマ検証 | 仕様に沿ったリクエスト/レスポンス検査 |
| 例データ利用 | examples をレスポンスに利用しやすい |
| 仕様追従 | API 変更時の差分検証に使える |

### テスト支援機能

| 機能 | 説明 |
|------|------|
| Verify API | 期待したリクエスト到達を検証 |
| Proxy/Record | 実通信から初期スタブを生成 |
| ログ | マッチしない原因の解析に有効 |
| HTTPS 対応 | TLS を含む API のテストに対応 |

## インストールとセットアップ

公式URL:
- [MockServer 公式サイト](https://www.mock-server.com/)
- [Getting Started](https://www.mock-server.com/mock_server/getting_started.html)
- [OpenAPI 連携](https://www.mock-server.com/mock_server/openapi.html)
- [Docker Hub](https://hub.docker.com/r/mockserver/mockserver)

セットアップの要点:
1. Docker か Java 実行のどちらで動かすかを決める。
2. テスト環境では Docker 起動を標準化すると再現性が高い。
3. Java で組み込む場合は `mockserver-netty` と `mockserver-client-java` をテスト依存に追加する。

## 基本的な使い方

1. MockServer を起動し、待受ポート（一般的には `1080`）を確認する。
2. テスト対象 API ごとに Expectation（リクエスト条件とレスポンス）を登録する。
3. アプリケーション側の接続先を MockServer に向け、通常どおり API を呼び出す。
4. テスト終了時に Verify API で期待した呼び出しが実行されたか確認する。
5. OpenAPI を使う場合は、仕様からモックを自動生成し、仕様との差分検知に活用する。

最小実行例:
- モック登録先: `PUT http://localhost:1080/mockserver/expectation`
- 呼び出し確認: `GET http://localhost:1080/status`

## メリット

- API 実装前でもフロントエンドとテストを先行できる
- OpenAPI ベースの契約テストに組み込みやすい
- リクエスト検証とプロキシ機能で不具合解析がしやすい
- Docker で簡単に CI 環境へ組み込める

## デメリット

- JVM ベースのため軽量ツールより起動コストが高い
- 高機能な分、初学者には設定項目が多い
- 複雑なテンプレート運用では保守ルールが必要

## Docker での使用

`docker-compose` では `1080` を公開し、必要に応じて初期 Expectation ファイルをマウントする。チーム開発では compose を共有して起動手順を統一すると運用しやすい。

## 他ツールとの比較

| ツール | OpenAPI 連携 | 特徴 |
|------|------|------|
| MockServer | 強い | 検証 API、Proxy/Record、高い拡張性 |
| WireMock | 中程度 | 採用実績が多く学習情報が豊富 |
| Prism | 強い | OpenAPI 準拠の軽量モック |
| MSW | 限定的 | フロントエンド向け、ブラウザ統合に強い |

## ベストプラクティス

### 1. Expectation を用途別に分離

- 正常系、異常系、パフォーマンス系で設定ファイルを分ける
- テストごとに必要最小限のモックだけ読み込む

### 2. OpenAPI を単一ソースにする

- 仕様変更時は OpenAPI と Expectation を同時更新する
- CI で仕様差分チェックを行う

### 3. ログと検証を必ず残す

- Verify API をテストの完了条件に含める
- 失敗時にマッチングログをアーティファクト保存する

## 公式ドキュメント

- 公式サイト: https://www.mock-server.com/
- Getting Started: https://www.mock-server.com/mock_server/getting_started.html
- Java API: https://www.mock-server.com/mock_server/creating_expectations_java.html
- REST API: https://www.mock-server.com/mock_server/creating_expectations.html
- GitHub: https://github.com/mock-server/mockserver

## まとめ

- API 実装前でも、Expectation を使ってフロントエンド開発と自動テストを先行できる。
- OpenAPI 連携により、契約ベースでモック生成と仕様差分検知を進めやすい。
- Verify API と Proxy/Record を組み合わせることで、品質確認と不具合解析を効率化できる。
