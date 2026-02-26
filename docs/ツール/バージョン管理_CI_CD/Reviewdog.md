# Reviewdog

## 概要

Reviewdog は、静的解析ツールの結果を Pull Request コメントとして反映するレビュー支援ツールである。ESLint、golangci-lint、flake8 などの出力を統合し、差分箇所に紐づけて指摘表示できる。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（MIT License） |
| 商用利用 | ライセンス上可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| Lint結果集約 | 複数解析ツール結果を統一処理 |
| PR差分連携 | 差分行へ直接コメント可能 |
| CI連携容易 | GitHub Actions で導入しやすい |
| フィルタ制御 | `added` など差分条件を指定可能 |
| 多言語対応 | 各言語のlint/format結果に対応 |
| ノイズ低減 | 関連行のみ通知して指摘を絞りやすい |

## 主な機能

### 結果取り込み機能

| 機能 | 説明 |
|------|------|
| parser指定 | ツール出力形式に応じて解析 |
| stdin連携 | パイプで結果を受け取り処理 |
| severity反映 | 重要度ごとに通知制御 |
| 複数実行 | ツール別ジョブで並行運用可能 |

### レビュー通知機能

| 機能 | 説明 |
|------|------|
| PRコメント | 差分行にコメント投稿 |
| チェックラン | CIステータスとして結果表示 |
| fail判定 | 一定条件でジョブ失敗可能 |
| ログ出力 | CIログで解析結果を確認可能 |

### 運用機能

| 機能 | 説明 |
|------|------|
| filter-mode | `added`/`nofilter` などを指定 |
| reporter | github-pr-review/github-check 等選択 |
| reviewdog.yml | ルールを設定ファイル化 |
| 再利用性 | 共通設定を複数repoへ展開可能 |

## インストールとセットアップ

公式URL:
- [Reviewdog 公式サイト](https://reviewdog.github.io/)
- [GitHub](https://github.com/reviewdog/reviewdog)
- [GitHub Action](https://github.com/reviewdog/action-reviewdog)

セットアップの要点:
1. CI に reviewdog 実行ステップを追加する。
2. 解析ツールの出力形式と parser を対応付ける。
3. reporter と filter-mode を決定する。
4. 失敗条件（warning以上など）をチームで定義する。

## 基本的な使い方

1. lint ツールを実行して結果を標準出力へ出す。
2. 結果を reviewdog にパイプしてPR連携する。
3. PR上の指摘を確認して修正する。
4. 再実行で指摘解消を確認する。
5. ルール調整でノイズを継続改善する。

最小実行例:
- `eslint . -f stylish | reviewdog -f=eslint -reporter=github-pr-review`
- `golangci-lint run | reviewdog -f=golangci-lint -reporter=github-check`

## メリット

- Lint指摘をPR差分に直接表示しやすい。
- 複数ツールの出力を統一運用しやすい。
- ノイズを抑えた自動レビュー運用を作りやすい。

## デメリット

- parser設定を誤ると指摘反映が不安定になる。
- 解析ツールが多いとCI時間が増えやすい。
- 運用ルール未整備だとコメント過多になりやすい。

## CI/CD での使用

CI で lint 実行後に reviewdog を走らせ、PR差分へ指摘を投稿する運用が一般的である。`filter-mode=added` を使うと既存コード由来のノイズを減らしやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Reviewdog | Lint結果のPR反映 | 差分コメント連携に強い |
| Danger | PR手続きルール | 手順チェック中心 |
| CodeRabbit | AI差分レビュー | 文脈提案に強い |
| SonarQube | 継続品質分析 | 指標管理に強い |

## ベストプラクティス

### 1. parserを厳密に合わせる

- ツールごとに正しい parser を指定する。
- 出力形式変更時は設定を更新する。

### 2. コメント量を制御

- `added` フィルタで差分範囲に限定する。
- severity閾値で重要指摘を優先する。

### 3. 設定を共通化

- `reviewdog.yml` をリポジトリ管理する。
- ルール変更はPRレビューを通して反映する。

## 公式ドキュメント

- 公式サイト: https://reviewdog.github.io/
- GitHub: https://github.com/reviewdog/reviewdog
- GitHub Action: https://github.com/reviewdog/action-reviewdog

## まとめ

1. **即時反映** : Lint結果をPR差分に反映し、修正サイクルを短縮しやすい。
2. **統合運用** : 複数解析ツールを統合して運用標準化しやすい。
3. **精度制御** : フィルタと閾値を設計すると、ノイズを抑えて活用しやすい。
