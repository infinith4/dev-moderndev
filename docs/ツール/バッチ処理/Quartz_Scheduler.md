# Quartz Scheduler

## 概要

Quartz Scheduler は、Java 向けのジョブスケジューラライブラリである。定期実行、cron 実行、再実行制御、クラスタ運用に対応し、バッチ処理や定時処理をアプリケーション内で安定運用しやすい。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（オープンソース） |
| 商用利用 | ライセンス上利用可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 柔軟なスケジュール | Simple Trigger と Cron Trigger を使い分け可能 |
| Java 統合 | Spring を含む JVM アプリに組み込みやすい |
| 永続化対応 | JDBC JobStore でジョブ状態を DB 保存可能 |
| クラスタ実行 | 複数ノードで冗長化し、可用性を高められる |
| 実行制御 | Misfire、同時実行制御、Listener 連携に対応 |
| 拡張性 | Job/Trigger/Calendar を分離して運用設計しやすい |

## 主な機能

### スケジューリング機能

| 機能 | 説明 |
|------|------|
| Simple Trigger | 固定間隔の繰り返し実行 |
| Cron Trigger | cron 式による詳細な時刻指定 |
| Calendar | 休日・除外日などの実行制御 |
| Misfire ポリシー | 実行遅延時の挙動を明示的に設定 |

### 実行制御機能

| 機能 | 説明 |
|------|------|
| JobDetail | 実行対象ジョブを定義 |
| Trigger 分離 | 実行条件をジョブ本体から分離 |
| JobListener/TriggerListener | 実行前後イベントを監視 |
| 同時実行制御 | 重複起動を防ぐ運用設計に対応 |

### 運用機能

| 機能 | 説明 |
|------|------|
| RAMJobStore | シンプルなメモリ運用 |
| JDBC JobStore | 再起動耐性と永続化を実現 |
| Cluster Mode | ノード障害時の継続運用を支援 |
| 監視連携 | ログ/メトリクス基盤への連携がしやすい |

## インストールとセットアップ

公式URL:
- [Quartz 公式サイト](https://www.quartz-scheduler.org/)
- [Quartz Documentation](https://www.quartz-scheduler.org/documentation/)
- [Quartz Configuration](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/configuration/)
- [GitHub](https://github.com/quartz-scheduler/quartz)

セットアップの要点:
1. `quartz` 依存をプロジェクトへ追加する。
2. RAMJobStore か JDBC JobStore を用途に応じて選択する。
3. Job と Trigger を分離して定義し、責務を明確化する。
4. 本番ではログ、監視、通知を最初から組み込む。

## 基本的な使い方

1. Scheduler を初期化し、最小ジョブを 1 本登録して動作確認する。
2. 固定間隔実行から開始し、必要に応じて Cron Trigger に切り替える。
3. 失敗時の再実行方針（回数、間隔、通知）を決める。
4. 再起動耐性が必要な処理は JDBC JobStore に移行する。
5. 監視基盤で実行回数、失敗率、遅延時間を可視化する。

最小運用例:
- 開始: RAMJobStore + Simple Trigger
- 本番: JDBC JobStore + Cron Trigger + 失敗通知

## メリット

- 定期実行要件を細かく制御できる。
- Java アプリに統合しやすく、実装の一貫性を保ちやすい。
- 永続化とクラスタ構成で可用性を高めやすい。
- バッチ運用ルールを標準化しやすい。

## デメリット

- 設定項目が多く、初期設計に時間がかかる。
- ジョブ設計が粗いと重複実行や運用負荷が増えやすい。
- 小規模・単純用途では過剰になる場合がある。

## クラスタ/永続化での使用

単一ノードの簡易運用では RAMJobStore で開始し、運用段階で JDBC JobStore へ移行する構成が現実的である。可用性要件が高い場合はクラスタ構成を採用し、ロック管理と監視を合わせて整備すると安定運用しやすい。

## 他ツールとの比較

| ツール | 主な用途 | 特徴 |
|------|------|------|
| Quartz Scheduler | Java バッチ/定期実行 | 高機能なスケジュール制御とクラスタ対応 |
| Spring Scheduler | Java 定期実行 | Spring 内で軽量に運用しやすい |
| Cron | OS レベル定期実行 | 単純だがアプリ連携は限定的 |
| Apache Airflow | ワークフロー管理 | DAG ベースで依存ジョブ管理に強い |

## ベストプラクティス

### 1. ジョブ責務を小さく分離

- 1 ジョブ 1 責務を原則にする。
- 長時間処理は分割してタイムアウトを設定する。

### 2. 再実行と重複防止を設計

- リトライ回数、待機時間、通知条件を明確化する。
- 冪等性を担保し、二重処理を防ぐ。

### 3. 監視を運用の前提にする

- 実行時間、失敗率、未実行を継続監視する。
- 障害時の復旧手順を runbook 化する。

## 公式ドキュメント

- 公式サイト: https://www.quartz-scheduler.org/
- Documentation: https://www.quartz-scheduler.org/documentation/
- Configuration: https://www.quartz-scheduler.org/documentation/quartz-2.3.0/configuration/
- GitHub: https://github.com/quartz-scheduler/quartz

## まとめ

1. ** 柔軟制御 ** : Quartz Scheduler は Java バッチ処理の定期実行を柔軟に制御しやすい。
2. ** 安定運用 ** : Job/Trigger 分離と失敗時ポリシー設計が運用安定の鍵になる。
3. ** 高可用性 ** : 永続化とクラスタ運用を組み合わせることで、高可用なバッチ基盤を構築しやすい。
