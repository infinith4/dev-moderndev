# Mountebank

## 概要

Mountebank は、HTTP/HTTPS、TCP、SMTP など複数プロトコルをモック化できるサービス仮想化ツールである。外部依存先の代替を作り、統合テストや段階移行を進めやすくする。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（MIT License） |
| 商用利用 | ライセンス上利用可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| マルチプロトコル | HTTP/HTTPS、TCP、SMTP に対応 |
| REST 操作 | API 経由でインポスターを管理 |
| Proxy/Record | 実通信を中継しスタブ生成に活用可能 |
| Injection | 動的レスポンス生成に対応 |
| Docker 運用 | CI 環境へ組み込みやすい |

## 主な機能

### インポスター管理機能

| 機能 | 説明 |
|------|------|
| インポスター作成 | ポート単位で仮想サービスを作成 |
| 複数同時起動 | プロトコル別に複数サービスを運用 |
| 状態保持 | テスト中の状態を保持した応答制御 |
| API 管理 | 追加・更新・削除を REST API で実行 |

### スタブ・マッチング機能

| 機能 | 説明 |
|------|------|
| Predicate | メソッド、パス、本文などで条件指定 |
| レスポンス定義 | ステータス、ヘッダー、本文、遅延を設定 |
| 順序制御 | スタブの評価順を制御 |
| 繰り返し応答 | シーケンス応答を設定可能 |

### プロキシ・録画機能

| 機能 | 説明 |
|------|------|
| Proxy | 実サービスへ転送しながら応答 |
| Record | 実通信からスタブを生成 |
| Predicate 生成 | 録画データから条件を自動作成 |
| 段階移行 | 一部だけ実サービス利用に切り替え可能 |

## インストールとセットアップ

公式URL:
- [Mountebank 公式サイト](http://www.mbtest.org/)
- [GitHub](https://github.com/bbyars/mountebank)
- [Getting Started](http://www.mbtest.org/docs/gettingStarted)
- [Docker Hub](https://hub.docker.com/r/bbyars/mountebank)

セットアップの要点:
1. npm または Docker で Mountebank を起動する。
2. 管理ポート（通常 `2525`）を確認する。
3. テスト対象ごとにインポスターとスタブを作成する。
4. 必要に応じて Proxy/Record で初期スタブを作成する。

## 基本的な使い方

1. `POST /imposters` で仮想サービスを起動する。
2. Predicate とレスポンスを定義してスタブを登録する。
3. アプリケーションの接続先をインポスターへ変更する。
4. 統合テストを実行し、期待レスポンスを確認する。
5. 必要に応じてスタブを更新し、シナリオ別に管理する。

最小実行例:
- インポスター作成: `POST http://localhost:2525/imposters`
- 内容確認: `GET http://localhost:2525/imposters/{port}`

## メリット

- HTTP 以外も含む統合テスト環境を1ツールで構築しやすい。
- Proxy/Record により既存APIからスタブを作りやすい。
- Docker で再現性の高いテスト環境を作りやすい。

## デメリット

- 高度機能（Injection 等）は運用ルールがないと複雑化しやすい。
- 設定が増えるとスタブ保守コストが上がる。
- UI 主体ツールに比べると学習はややCLI/API寄りになる。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Mountebank | マルチプロトコル統合テスト | HTTP/TCP/SMTP を横断してモック可能 |
| WireMock | HTTP モック | HTTP 前提の運用と資産が豊富 |
| MockServer | 契約テスト/モック | OpenAPI 連携と検証 API が強い |
| Prism | OpenAPI モック | 仕様準拠モックを軽量に実行 |

## ベストプラクティス

### 1. スタブを用途別に分離

- 正常系、異常系、遅延系を分けて管理する。
- 1テストで必要なスタブだけを読み込む。

### 2. Proxy/Record は初期作成に限定

- 録画後は不要スタブを整理して固定化する。
- 本番依存を残さないようスタブを明示管理する。

### 3. 検証ログを残す

- 不一致時のリクエスト履歴を必ず確認する。
- CI 失敗時にログをアーティファクト保存する。

## 公式ドキュメント

- 公式サイト: http://www.mbtest.org/
- API Docs: http://www.mbtest.org/docs/api/overview
- Getting Started: http://www.mbtest.org/docs/gettingStarted
- GitHub: https://github.com/bbyars/mountebank

## まとめ

1. **多種対応** : 複数プロトコルを扱う統合テストで依存先を置き換えやすい。
2. **録画活用** : Proxy/Record を使って既存連携先からスタブ化を進めやすい。
3. **再現性確保** : Docker と組み合わせると再現性の高い CI テスト基盤を作りやすい。
