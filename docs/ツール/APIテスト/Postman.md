# Postman

## 概要

Postman は API の設計・テスト・ドキュメント共有を行える統合ツールである。リクエスト実行、テスト、環境変数管理、モック、チーム共有を一つのプラットフォームで扱えるため、API 開発の標準ツールとして広く利用されている。

## 料金

| プラン | 内容 |
|------|------|
| Free | 個人・小規模向けの基本機能 |
| Basic / Professional / Enterprise | コラボレーション、ガバナンス、監査機能を拡張 |
| 補足 | 最新料金は公式 pricing を参照 |

## 主な特徴

| 項目 | 内容 |
|------|------|
| API クライアント | REST/GraphQL/gRPC/WebSocket リクエストを実行 |
| Collection 管理 | テストケースをコレクション単位で再利用 |
| チーム共有 | ワークスペースで履歴・レビュー・共同編集 |
| 自動化連携 | Newman/Postman CLI で自動実行へ展開 |
| ドキュメント化 | Collection からドキュメントを公開可能 |

## 主な機能

### API テスト機能

| 機能 | 説明 |
|------|------|
| リクエスト作成 | メソッド、パラメータ、ヘッダー、Body を設定 |
| テストスクリプト | JavaScript でアサーションを記述 |
| 環境変数 | 環境ごとの URL やトークンを切替 |
| コレクション実行 | 一括実行で回帰テストを実施 |

### 設計・共有機能

| 機能 | 説明 |
|------|------|
| API ドキュメント | Collection から自動生成 |
| Mock Server | API 実装前に疑似レスポンスを提供 |
| バージョン管理 | 履歴差分を確認して変更を追跡 |
| ワークスペース | チーム単位で API 資産を管理 |

### 自動化機能

| 機能 | 説明 |
|------|------|
| Newman / Postman CLI | CLI でコレクションを実行 |
| レポート出力 | JSON/JUnit 等で結果を保存 |
| モニター | 定期実行で API ヘルスチェック |
| Secrets 連携 | 環境情報を安全に切り替え可能 |

## インストールとセットアップ

公式URL:
- [Postman 公式サイト](https://www.postman.com/)
- [Download](https://www.postman.com/downloads/)
- [Postman Learning Center](https://learning.postman.com/)
- [Postman API Platform Docs](https://learning.postman.com/docs/)

セットアップの要点:
1. Postman をインストールし、Workspace を作成する。
2. Environment を `dev/stg/prod` で分けて作成する。
3. Collection をドメイン単位で分割して登録する。

## 基本的な使い方

1. リクエストを作成し、まず手動で API 応答を確認する。
2. 主要 API に対してテストスクリプトを追加し、期待値を固定する。
3. Collection Runner で一括実行し、回帰確認を行う。
4. 自動化が必要な場合は Newman へ接続して CLI 実行に移行する。

最小スクリプト例:
```javascript
pm.test('status is 200', () => pm.response.to.have.status(200))
```

## メリット

- GUI 操作で API テストを始めやすい
- チーム共有とレビューがしやすい
- Collection をそのまま自動化に展開できる
- ドキュメントとテスト資産を統合管理できる

## デメリット

- 運用規模が大きいと資産整理ルールが必須
- 高度なガバナンス機能は有料プラン依存
- GUI 主体で始めると CLI 運用の整備が後回しになりやすい

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Postman | API 開発全般 | GUI 中心で設計・テスト・共有を統合 |
| Apidog | 設計主導の API 開発 | OpenAPI と統合管理に強い |
| Insomnia | API クライアント | 軽量でローカル運用しやすい |
| Bruno | Git 管理重視 | ローカルファーストで差分管理しやすい |

## ベストプラクティス

### 1. Collection 設計を標準化

- ドメイン単位にフォルダ分割する
- 命名規則を統一して検索しやすくする

### 2. 環境変数を厳格管理

- シークレットは共有 Environment に直書きしない
- 自動実行時は CI secrets から注入する

### 3. 自動化前提で資産化

- 手動確認用リクエストと回帰テストを分離する
- 重要 API は必ずアサーションを実装する

## 公式ドキュメント

- 公式サイト: https://www.postman.com/
- ドキュメント: https://learning.postman.com/docs/
- ダウンロード: https://www.postman.com/downloads/
- Pricing: https://www.postman.com/pricing/

## まとめ

1. **統合管理** : API リクエスト作成、テスト、ドキュメント共有を1つのワークスペースで管理できる。
2. **手順標準** : Collection と Environment を整備することで、チーム内の検証手順を標準化しやすい。
3. **段階拡張** : Newman などと連携すると、手動確認から CI 自動実行へ段階的に拡張できる。
