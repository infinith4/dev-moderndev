# Newman

## 概要

Newman は Postman Collection を CLI で実行するための公式ツールである。ローカル検証だけでなく、CI/CD で API テストを自動実行し、レポート出力や失敗判定まで一貫して扱える。GUI に依存しない再現性の高い運用に向いている。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（Apache License 2.0） |
| 商用利用 | ライセンス上可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Postman 互換 | Collection / Environment をそのまま実行 |
| CLI 実行 | ローカル・CI で同一コマンド運用 |
| レポート出力 | CLI、JSON、JUnit、HTML などに対応 |
| 自動化向き | exit code により失敗を明確に判定 |
| 軽量導入 | Node.js 環境があれば即利用可能 |

## 主な機能

### 実行機能

| 機能 | 説明 |
|------|------|
| Collection 実行 | 1コマンドで API テストを連続実行 |
| Environment 切替 | dev/stg/prod など環境差分を吸収 |
| データ駆動テスト | CSV/JSON を読み込んだ反復実行 |
| 実行制御 | フォルダ指定、反復回数、タイムアウト設定 |

### レポート機能

| 機能 | 説明 |
|------|------|
| CLI レポーター | コンソールで結果を即確認 |
| JSON/JUnit | CI 連携に使いやすい形式で出力 |
| HTML 拡張 | `newman-reporter-htmlextra` などに対応 |
| 成果物保存 | パイプラインのアーティファクトとして保管 |

### 自動化機能

| 機能 | 説明 |
|------|------|
| 失敗時終了コード | CI でビルド失敗を明確化 |
| シークレット注入 | 環境変数や CI secrets と連携 |
| 並列ジョブ運用 | 環境別・サービス別の分割実行 |
| スケジュール実行 | cron や CI スケジュール実行に対応 |

## インストールとセットアップ

公式URL:
- [Newman 公式](https://www.npmjs.com/package/newman)
- [Postman Docs](https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/)
- [Newman GitHub](https://github.com/postmanlabs/newman)

セットアップの要点:
1. `newman` をグローバルインストールする。
2. 実行対象の Collection と Environment をリポジトリに配置する。
3. 必要に応じて HTML など追加レポーターを導入する。

## 基本的な使い方

1. まず Collection 単体を実行し、ローカルで成功することを確認する。
2. 次に Environment を指定して環境差分（URL、認証情報）を切り替える。
3. データ駆動テストが必要な API は CSV/JSON を追加する。
4. CI 用には JSON/JUnit レポートを出力し、失敗時にジョブを落とす。

最小コマンド:
- 単体実行: `newman run ./postman/MyCollection.json`
- 環境指定: `newman run ./postman/MyCollection.json -e ./postman/dev.environment.json`

## メリット

- Postman 資産をそのまま CI に載せられる
- GUI 非依存のため再現性が高い
- レポート形式が豊富で運用へ組み込みやすい
- 導入コストが低く小規模案件でも使いやすい

## デメリット

- 大規模 Collection では実行時間が長くなりやすい
- スクリプト依存が増えると保守負荷が上がる
- API 仕様管理自体は別ツールで補完が必要

## Docker での使用

`postman/newman` イメージを使うと、ローカル Node 環境に依存せず実行環境を統一できる。Collection とレポート出力先をボリュームマウントして使うと運用しやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Newman | Postman Collection 自動実行 | CLI 中心、CI 連携が容易 |
| Postman CLI | Postman ワークスペース連携 | Postman 機能との統合が強い |
| REST Assured | Java テストコード | コードベースで柔軟に記述 |
| k6 | 負荷・性能試験 | パフォーマンステストに強い |

## ベストプラクティス

### 1. Collection を責務分割

- 認証、ユーザー、決済などドメインごとに分離する
- 実行時間短縮のためジョブを分割する

### 2. 環境変数を厳格管理

- API キーは CI secrets から注入する
- 固定値は Environment に直書きしない

### 3. レポートを標準化

- JUnit を共通形式として保存する
- 失敗ログと合わせて追跡できるようにする

## 公式ドキュメント

- npm: https://www.npmjs.com/package/newman
- ドキュメント: https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/
- GitHub: https://github.com/postmanlabs/newman

## まとめ

1. ** 自動移行 ** : Postman Collection を CLI 実行できるため、既存の手動テスト資産を自動化へ移行しやすい。
2. ** 継続実行 ** : CI/CD と組み合わせることで、API 回帰テストを継続的に実行できる。
3. ** 品質管理 ** : Environment とレポート運用を標準化すると、失敗分析と品質ゲート管理を効率化できる。
