# REST Assured

## 概要

REST Assured は Java 向けの API テストライブラリである。HTTP リクエスト実行、レスポンス検証、JSON/XML パース、認証処理を fluent API で記述でき、JUnit/TestNG と組み合わせて自動テストを構築しやすい。バックエンド API の回帰テストで定番の選択肢である。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（Apache License 2.0） |
| 商用利用 | ライセンス上可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Java ネイティブ | JUnit/TestNG と自然に統合 |
| Fluent API | 可読性の高い Given-When-Then スタイル |
| 豊富な検証 | ステータス、ヘッダー、JSONPath/XPath 検証 |
| 認証対応 | Basic/OAuth2/Bearer などに対応 |
| 自動化向き | Maven/Gradle で継続実行しやすい |

## 主な機能

### リクエスト・検証機能

| 機能 | 説明 |
|------|------|
| HTTP メソッド | GET/POST/PUT/PATCH/DELETE を網羅 |
| パラメータ設定 | path/query/header/cookie/body を指定 |
| レスポンス検証 | Hamcrest で柔軟なアサーション |
| JSON/XML 対応 | JSONPath と XPath で値抽出 |

### テスト実装機能

| 機能 | 説明 |
|------|------|
| 共通設定 | `baseURI`、認証、共通ヘッダーを一元管理 |
| リクエスト仕様化 | RequestSpecification で再利用 |
| シリアライズ | POJO と JSON の相互変換 |
| ログ出力 | 失敗時の request/response を可視化 |

### 自動化機能

| 機能 | 説明 |
|------|------|
| Maven/Gradle 実行 | `test` タスクへ組み込み |
| 並列実行 | テストスイート分割で高速化 |
| レポート連携 | Surefire/Allure などと接続 |
| パイプライン連携 | 自動テストの品質ゲート化 |

## インストールとセットアップ

公式URL:
- [REST Assured 公式サイト](https://rest-assured.io/)
- [REST Assured GitHub](https://github.com/rest-assured/rest-assured)
- [Javadoc](https://javadoc.io/doc/io.rest-assured/rest-assured/latest/index.html)

セットアップの要点:
1. `rest-assured` をテスト依存に追加する。
2. `baseURI`、認証、共通ヘッダーを初期化クラスに集約する。
3. 正常系と異常系でテストカテゴリを分けて管理する。

## 基本的な使い方

1. まず `Given-When-Then` 形式で主要エンドポイントの正常系を作成する。
2. ステータスコードと主要レスポンス項目を最低限の必須検証として固定する。
3. 次に認証エラー、入力不正、依存先エラーの異常系を追加する。
4. 失敗時ログを有効化し、デバッグ可能な状態で運用する。

最小コード例:
```java
given().when().get("/health").then().statusCode(200);
```

## メリット

- Java テスト基盤と統合しやすい
- 可読性の高いテストコードを記述できる
- API 回帰テストを段階的に拡張しやすい
- 認証や複雑な検証にも対応可能

## デメリット

- Java 前提のため他言語チームには適合しにくい
- コード管理が増えるため初期整備が必要
- UI チーム主体の簡易検証にはオーバースペックになり得る

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| REST Assured | Java API 自動テスト | コードベースで柔軟な検証 |
| Newman | Postman 資産自動化 | GUI 資産の CLI 実行が簡単 |
| Karate | API + BDD | Gherkin ベースで記述可能 |
| Postman | API 手動/半自動テスト | GUI 中心で導入しやすい |

## ベストプラクティス

### 1. 共通設定を集約

- Base URL、認証、共通ヘッダーを `RequestSpecification` にまとめる
- テストごとの差分だけを記述する

### 2. テストデータを分離

- 固定 JSON を fixture 化して再利用する
- 環境差分は環境変数で注入する

### 3. 失敗解析を簡単にする

- 失敗時ログ出力を標準化する
- 実行結果をアーティファクト保存する

## 公式ドキュメント

- 公式サイト: https://rest-assured.io/
- GitHub: https://github.com/rest-assured/rest-assured
- Javadoc: https://javadoc.io/doc/io.rest-assured/rest-assured/latest/index.html

## まとめ

- Java コードベースで柔軟に API テストを記述でき、バックエンド開発フローに組み込みやすい。
- 共通設定とテストデータ管理を整備すると、保守性の高い回帰テスト基盤を構築できる。
- CI で継続実行することで、API 品質をリリース前に安定して検証できる。
