# Microsoft Visio

## 概要

Microsoft Visioは、プロフェッショナル向けの図表作成ツールで、業務フロー、組織図、BPMN、プロセスマッピングなど、様々な図表作成に対応しています。Microsoft 365エコシステムとの統合により、エンタープライズ環境で広く利用されています。

### 主な特徴

- **Microsoft 365統合**: SharePoint、Teams、Excel等との連携が可能
- **図形ライブラリ豊富**: 業種別・用途別の豊富なステンシル（図形セット）
- **エンタープライズ標準**: 多くの企業で標準的に採用されている
- **データ連携機能**: Excelやデータベースとのリンクが可能
- **BPMN対応**: BPMN 2.0に対応したプロセス図の作成が可能

### 料金プラン

- **Visio Plan 1**: $5/月/ユーザー（Web版のみ）
- **Visio Plan 2**: $15/月/ユーザー（デスクトップ版 + Web版、高度な機能）
- **買い切り版**: Visio Standard 2021、Visio Professional 2021（約3万円〜6万円）

### メリット・デメリット

**メリット**
- Microsoft 365との統合により、SharePoint、Teams等での図表共有が容易
- 業種・用途別の図形ライブラリが非常に豊富
- エンタープライズ環境での採用実績が多く、信頼性が高い
- Excelやデータベースとのデータリンク機能により、動的な図表作成が可能
- BPMN対応で標準的なプロセス図の作成が可能

**デメリット**
- 料金が高額（特にデスクトップ版）
- Windows/Web中心で、Macネイティブ版がない
- 学習コストがあり、初心者には操作が難しい場合がある
- モダンなツールに比べると動作が重い場合がある

## 利用方法

### 1. Visioの起動

#### デスクトップ版（Visio Plan 2またはスタンドアロン版）

1. Windows スタートメニューから「Visio」を検索
2. Visioアプリケーションを起動
3. Microsoftアカウントでサインイン

#### Web版（Visio Plan 1/2）

1. [Office.com](https://www.office.com/)にアクセス
2. Microsoftアカウントでサインイン
3. アプリランチャーから「Visio」を選択

### 2. テンプレート選択

1. Visio起動後、テンプレートギャラリーが表示される
2. カテゴリから選択:
   - **Business Process**: ビジネスプロセス図、BPMN
   - **Flowchart**: フローチャート
   - **Organization Chart**: 組織図
   - **Cross-Functional Flowchart**: スイムレーン図
3. または「Blank Drawing」で白紙から開始

#### BPMNテンプレートの選択

1. 「Business Process」カテゴリを選択
2. 「BPMN Diagram」テンプレートをクリック
3. 「Create」ボタンをクリック

### 3. ステンシル（図形ライブラリ）の利用

1. 左側のパネルに「Shapes」ウィンドウが表示される
2. BPMN図の場合、以下のステンシルが自動的に読み込まれる:
   - **BPMN Basic Shapes**: 基本図形（タスク、イベント、ゲートウェイ）
   - **BPMN Expanded Shapes**: 拡張図形

#### ステンシルの追加

1. 「More Shapes」をクリック
2. カテゴリから追加のステンシルを選択
   - 例: Flowchart、Cross-Functional Flowchart

### 4. 図形の配置

1. ステンシルから図形をドラッグ&ドロップでキャンバスに配置
2. 主要なBPMN図形:
   - **Start Event**: 開始イベント（緑の円）
   - **Task**: タスク（四角形）
   - **Exclusive Gateway**: 排他ゲートウェイ（菱形、×マーク）
   - **Parallel Gateway**: 並列ゲートウェイ（菱形、+マーク）
   - **End Event**: 終了イベント（赤の円）

### 5. コネクタで接続

#### 自動接続

1. 図形をキャンバスに配置すると、四方に青い矢印が表示される
2. 青い矢印をクリックすると、自動的に次の図形が配置され接続される

#### 手動接続

1. 「Connector」ツールを選択（または「Ctrl + クリック」）
2. 接続元の図形をクリック
3. 接続先の図形をクリック
4. 自動的にシーケンスフローが作成される

### 6. プロセスフロー作成の具体例

**例: クレーム処理プロセス**

```
[開始] → [クレーム受付] → [内容確認] → <重大度判定>
                                        ├─ 高 → [即時対応] → [顧客連絡] → [終了]
                                        ├─ 中 → [調査・分析] → [対応策決定] → [顧客連絡] → [終了]
                                        └─ 低 → [定期対応リスト追加] → [終了]
```

#### 作成手順

1. **Start Event**をキャンバスに配置
2. **Task**「クレーム受付」を配置し、Start Eventから接続
3. **Task**「内容確認」を配置
4. **Exclusive Gateway**「重大度判定」を配置
5. 3つの経路を作成:
   - **高**: Task「即時対応」→「顧客連絡」→End Event
   - **中**: Task「調査・分析」→「対応策決定」→「顧客連絡」→End Event
   - **低**: Task「定期対応リスト追加」→End Event
6. 各コネクタに条件ラベルを追加（高/中/低）

### 7. データリンク機能

Visioの強力な機能の一つが、Excelやデータベースとのデータリンクです。

#### Excelデータとのリンク

1. 「Data」タブ→「Link Data to Shapes」を選択
2. Excelファイルを選択
3. データ範囲を指定
4. 図形とデータ行を紐付け
5. データが更新されると、図形も自動更新される

### 8. レイヤーとコンテナの利用

#### コンテナ（プール/レーン）

1. 「Insert」タブ→「Container」を選択
2. BPMNの場合、「Pool」と「Lane」を配置
3. プール内にレーンを追加して、役割や部署ごとにタスクを分類

### 9. エクスポートと共有

#### ファイル保存

1. 「File」→「Save As」を選択
2. 保存先を選択（OneDrive、SharePoint、ローカル）
3. ファイル名を入力して保存

#### PDF/画像エクスポート

1. 「File」→「Export」を選択
2. 形式を選択:
   - **PDF**
   - **PNG**
   - **SVG**
   - **JPEG**
3. オプションを設定して「Export」をクリック

#### SharePointで共有

1. 「File」→「Share」を選択
2. SharePointサイトを選択
3. 共同編集者を招待

### 10. SharePoint/Teamsでの閲覧

1. VisioファイルをSharePointまたはTeamsにアップロード
2. ブラウザで直接開いて閲覧・編集が可能
3. コメント機能でフィードバックを受け取る

## 公式ドキュメント

- **公式サイト**: [Microsoft Visio](https://www.microsoft.com/microsoft-365/visio/)
- **Visioヘルプとラーニング**: [Visio Help & Learning](https://support.microsoft.com/visio)
- **Visio基本トレーニング**: [Visio Training](https://support.microsoft.com/office/visio-training-e058bcfa-1d90-4653-afc6-e84d54cf94a6)
- **BPMN図の作成**: [Create a BPMN diagram](https://support.microsoft.com/office/create-a-bpmn-diagram-0e34db42-1f0a-4a8d-9f46-1b8f8b7e8d4f)
- **データリンク機能**: [Link data to shapes](https://support.microsoft.com/office/link-data-to-shapes-in-your-drawing-f8c0e3e0-9c0e-4e0e-9c0e-0e0e0e0e0e0e)

## 関連リンク

- [BPMN 2.0 仕様書（OMG公式）](https://www.omg.org/spec/BPMN/)
- [Visioテンプレートとサンプル](https://templates.office.com/visio)
- [Microsoft 365管理センター](https://admin.microsoft.com/)
