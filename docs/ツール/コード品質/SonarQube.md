# SonarQube

## 概要

SonarQube は、静的解析を中心にコード品質を継続監視するプラットフォームである。バグ、脆弱性、コードスメル、重複、テストカバレッジを可視化し、Quality Gate でリリース可否を統制できる。

## 料金

| プラン | 内容 |
|------|------|
| Community Edition | 無料（基本的な静的解析） |
| Developer 以上 | 有料（ブランチ/PR 分析などを拡張） |
| Enterprise / Data Center | 有料（大規模組織向け運用機能） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 静的解析 | 多言語ソースコードを継続的に解析 |
| Quality Gate | 品質基準を満たさない変更を検知 |
| PR 連携 | Pull Request 単位で課題を可視化 |
| メトリクス | カバレッジ、複雑度、重複率を集約 |
| IDE 連携 | SonarLint と組み合わせて早期検出 |
| CI/CD 統合 | Jenkins / GitHub Actions などに組み込み可能 |

## 主な機能

### コード品質分析機能

| 機能 | 説明 |
|------|------|
| バグ検出 | 実行時不具合につながる問題を検出 |
| 脆弱性検出 | セキュリティ上のリスクを検出 |
| コードスメル | 保守性低下につながる記述を検出 |
| 重複検出 | コピペコードの割合を可視化 |

### 品質統制機能

| 機能 | 説明 |
|------|------|
| Quality Gate | 閾値ベースで合否判定 |
| Quality Profile | 言語別ルールセットの管理 |
| 課題管理 | 検出結果の担当・優先度管理 |
| 履歴追跡 | 品質トレンドを継続観測 |

### CI/開発連携機能

| 機能 | 説明 |
|------|------|
| Scanner 連携 | Maven/Gradle/CLI で解析実行 |
| PR 装飾 | 差分に対する品質結果を表示 |
| レポート連携 | CI 結果と品質指標を統合 |
| IDE 連携 | SonarLint でローカル解析 |

## インストールとセットアップ

公式URL:
- [SonarQube 公式ページ](https://www.sonarsource.com/products/sonarqube/)
- [SonarQube Docs](https://docs.sonarsource.com/sonarqube/)
- [SonarScanner](https://docs.sonarsource.com/sonarqube/analyzing-source-code/scanners/)
- [SonarLint](https://www.sonarsource.com/products/sonarlint/)

セットアップの要点:
1. Docker などで SonarQube サーバーを起動する。
2. 管理画面でプロジェクトキーとトークンを作成する。
3. ビルドツール（Maven/Gradle/CLI）に Scanner 設定を追加する。
4. CI で解析を実行し、Quality Gate を必須化する。

## 基本的な使い方

1. サーバー起動後、対象プロジェクトを作成する。
2. 解析コマンドを実行して初回レポートを生成する。
3. 検出された課題を重要度順に整理する。
4. Quality Gate 条件（例: カバレッジ、重複率）を設定する。
5. PR 単位で解析し、リリース前に品質を確認する。

最小実行例:
- Maven: `mvn clean verify sonar:sonar`
- Gradle: `./gradlew sonarqube`

## メリット

- 品質課題を定量化し、改善優先度を決めやすい。
- Quality Gate により CI 上で品質を統制しやすい。
- SonarLint 連携でレビュー前に問題を減らしやすい。

## デメリット

- ルール調整をしないと誤検知や過検知が発生しやすい。
- 大規模プロジェクトでは解析時間とサーバー負荷が増える。
- 高度な運用機能は有料エディションが前提になる。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| SonarQube | 継続的コード品質管理 | Quality Gate と多言語解析を統合 |
| ESLint | JavaScript/TypeScript 静的解析 | フロントエンド向けに軽量運用しやすい |
| Semgrep | ルールベース解析 | セキュリティルールの追加が柔軟 |
| Code Climate | クラウド品質管理 | SaaS 中心で導入を簡素化しやすい |

## ベストプラクティス

### 1. Quality Gate を段階導入

- 初期は重要指標（重大バグ、脆弱性、カバレッジ）に絞る。
- 運用が安定したら閾値を段階的に引き上げる。

### 2. ルールセットを標準化

- 言語ごとに Quality Profile を定義する。
- 例外ルールは理由を明記して管理する。

### 3. PR 運用を必須化

- PR ごとに解析を実行して差分品質を確認する。
- 失敗時はログと課題URLをレビューに添付する。

## 公式ドキュメント

- 公式ページ: https://www.sonarsource.com/products/sonarqube/
- SonarQube Docs: https://docs.sonarsource.com/sonarqube/
- SonarScanner: https://docs.sonarsource.com/sonarqube/analyzing-source-code/scanners/
- SonarLint: https://www.sonarsource.com/products/sonarlint/

## まとめ

1. **継続管理** : 静的解析と Quality Gate でコード品質を継続的に管理しやすい。
2. **品質統制** : CI/CD と統合することで、品質基準をリリース前に強制しやすい。
3. **段階導入** : ルール設計と段階導入を行うと、過検知を抑えて運用しやすい。
