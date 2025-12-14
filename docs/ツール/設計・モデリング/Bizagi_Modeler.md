# Bizagi Modeler

## 概要

Bizagi Modelerは、ビジネスプロセスモデリングツールで、BPMN 2.0（Business Process Model and Notation）に完全準拠しています。ビジネスプロセス図作成、BPMN図、業務フロー可視化に特化しており、完全無料で利用できます。

### 主な特徴

- **完全無料**: デスクトップ版は無料で利用可能
- **BPMN 2.0準拠**: 国際標準のビジネスプロセスモデリング表記法に対応
- **プロセスシミュレーション**: 作成したプロセスのシミュレーション実行が可能
- **Word/PDF出力**: 作成したプロセス図をドキュメント形式で出力
- **日本語対応**: UIが日本語に対応している

### メリット・デメリット

**メリット**
- 完全無料で高機能
- BPMN2.0準拠のため、標準的な記法で業務プロセスを記述可能
- プロセスシミュレーション機能により、業務フローの検証が可能
- Word/PDF出力により、ドキュメント作成が容易
- 日本語対応

**デメリット**
- オンライン協業機能が弱い（デスクトップアプリケーションのため）
- クラウド版は有料
- UIがやや古めのデザイン
- 学習曲線があり、初心者には習得に時間がかかる

## 利用方法

### 1. インストール

1. [Bizagi公式サイト](https://www.bizagi.com/en/products/bpm-suite/modeler)からBizagi Modelerをダウンロード
2. インストーラーを実行してセットアップ
3. アプリケーションを起動

### 2. 新規プロセス作成

1. Bizagi Modelerを起動
2. 「New Process」をクリックして新規プロセスを作成
3. プロセス名を入力（例: 「受注プロセス」）

### 3. BPMN要素の配置

#### 主要なBPMN要素

- **タスク（Task）**: 業務活動を表す四角形
- **開始イベント（Start Event）**: プロセスの開始を表す細線の円
- **終了イベント（End Event）**: プロセスの終了を表す太線の円
- **ゲートウェイ（Gateway）**: 分岐・合流を表す菱形
  - 排他ゲートウェイ（XOR）: 条件によって1つの経路を選択
  - 並列ゲートウェイ（AND）: 複数の経路を同時実行
- **シーケンスフロー（Sequence Flow）**: タスク間の流れを表す矢印

#### 配置手順

1. 左側のパレットから「Start Event」をキャンバスにドラッグ&ドロップ
2. 「Task」を配置（例: 「受注確認」）
3. 「Gateway」を配置（必要に応じて分岐処理を追加）
4. 「End Event」を配置
5. 各要素を「Sequence Flow」（矢印）で接続

### 4. プロセスフロー作成の具体例

**例: 受注処理プロセス**

```
[開始] → [受注受付] → [在庫確認] → <在庫あり？>
                                    ├─ Yes → [出荷手配] → [請求書発行] → [終了]
                                    └─ No → [発注手配] → [入荷待ち] → [出荷手配] → [請求書発行] → [終了]
```

1. 開始イベントを配置
2. タスク「受注受付」を配置
3. タスク「在庫確認」を配置
4. 排他ゲートウェイ「在庫あり？」を配置
5. Yes経路: タスク「出荷手配」→「請求書発行」→終了イベント
6. No経路: タスク「発注手配」→「入荷待ち」→「出荷手配」→「請求書発行」→終了イベント
7. 各要素をシーケンスフローで接続

### 5. プロパティ設定

1. 各タスクやゲートウェイをダブルクリック
2. プロパティパネルで詳細情報を入力
   - タスク名
   - 説明
   - 担当者（ロール）
   - 条件（ゲートウェイの場合）

### 6. シミュレーション実行

1. 上部メニューから「Simulation」を選択
2. 「Run Simulation」をクリック
3. プロセスがシミュレーション実行され、各タスクの実行時間やボトルネックを確認

### 7. Word/PDF出力

1. 「Publish」メニューを選択
2. 出力形式を選択（Word、PDF、SharePoint等）
3. 出力テンプレートを選択（またはカスタマイズ）
4. 「Publish」ボタンをクリックして出力

## 公式ドキュメント

- **公式サイト**: [Bizagi BPM Suite - Modeler](https://www.bizagi.com/en/products/bpm-suite/modeler)
- **公式ドキュメント**: [Bizagi Documentation](https://help.bizagi.com/bpm-suite/en/)
- **チュートリアル**: [Bizagi Modeler Tutorial](https://help.bizagi.com/bpm-suite/en/index.html?process_modeler.htm)
- **BPMN 2.0 リファレンス**: [BPMN Elements](https://help.bizagi.com/bpm-suite/en/index.html?bpmn_2_0_elements.htm)

## 関連リンク

- [BPMN 2.0 仕様書（OMG公式）](https://www.omg.org/spec/BPMN/)
- [ユーザのための要件定義ガイド - IPA](https://www.ipa.go.jp/archive/digital/iot-en-ci/jyouryuu/youkenteigi20190912.html)
