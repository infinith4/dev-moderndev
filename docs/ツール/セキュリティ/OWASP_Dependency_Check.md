# OWASP Dependency-Check

## 概要

OWASP Dependency-Check は、依存ライブラリの既知脆弱性を検出する Software Composition Analysis（SCA）ツールである。依存関係の情報を収集し、NVD などの脆弱性情報と照合して CVE を特定できる。ビルド工程に組み込み、脆弱な依存を早期に検知しやすい。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（Apache License 2.0） |
| 商用利用 | ライセンス上可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 依存脆弱性検査 | 依存ライブラリの CVE を検出 |
| NVD 連携 | 公開脆弱性情報を基に照合 |
| 多言語対応 | Java、.NET、Node.js など複数エコシステム対応 |
| ビルド統合 | Maven/Gradle/CLI で実行可能 |
| サプレッション管理 | 誤検知や例外を理由付きで管理可能 |
| レポート出力 | HTML、JSON、SARIF、JUnit 形式を出力可能 |

## 主な機能

### 脆弱性検出機能

| 機能 | 説明 |
|------|------|
| CVE 照合 | 依存ライブラリを脆弱性DBと照合 |
| CPE 推定 | ライブラリ識別を行い検出精度を向上 |
| CVSS 評価 | 深刻度で優先度付け |
| 信頼度表示 | 検出結果の確度を確認可能 |

### レポート・管理機能

| 機能 | 説明 |
|------|------|
| HTML レポート | 人間向けの詳細レポート |
| JSON/SARIF | CI・セキュリティ基盤連携向け出力 |
| JUnit 出力 | テストレポートとして扱える |
| サプレッション | 例外管理を監査可能に記録 |

### 運用統制機能

| 機能 | 説明 |
|------|------|
| CVSS 閾値制御 | 閾値超過時にビルド失敗 |
| 依存更新判断 | 修正優先度の判定に活用 |
| 監査証跡 | スキャン結果を履歴として保存 |
| 例外期限管理 | 一時除外の恒久化を防止 |

## インストールとセットアップ

公式URL:
- [OWASP Dependency-Check 公式ページ](https://owasp.org/www-project-dependency-check/)
- [GitHub](https://github.com/dependency-check/DependencyCheck)
- [ドキュメント](https://jeremylong.github.io/DependencyCheck/)
- [Maven Plugin](https://mvnrepository.com/artifact/org.owasp/dependency-check-maven)

セットアップの要点:
1. CLI またはビルドプラグインで導入方法を決める。
2. スキャン対象（依存定義ファイル、ソースツリー）を指定する。
3. CVSS 閾値とサプレッション方針を定義する。
4. CI で定期実行し、レポート保存を標準化する。

## 基本的な使い方

1. プロジェクト全体をスキャンし、脆弱依存の一覧を取得する。
2. CVSS と影響範囲で修正優先度を決める。
3. 誤検知は suppression ファイルで理由付き管理する。
4. `failOnCVSS` でビルドゲートを設定する。
5. 修正後に再スキャンして改善を確認する。

最小実行例:
- CLI: `dependency-check --project "MyApp" --scan . --out reports`
- Maven: `mvn dependency-check:check`
- Gradle: `./gradlew dependencyCheckAnalyze`

## メリット

- 依存ライブラリ由来の既知脆弱性を早期に把握しやすい。
- ビルド統合で継続的なセキュリティチェックを実装しやすい。
- レポートとサプレッション管理で監査対応しやすい。

## デメリット

- 初回DB更新に時間がかかる場合がある。
- 誤検知対策として例外管理ルールが必要。
- コンテナやIaC検査は別ツール併用が前提になる。

## CI/CD での使用

CI/CD では `failOnCVSS` を用いて重大脆弱性をマージ/リリース前にブロックする運用が有効である。NVD キャッシュを利用すると実行時間を抑えやすい。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| OWASP Dependency-Check | 依存ライブラリ脆弱性 | OSS でビルド統合しやすい |
| Trivy | イメージ/依存/IaC | 対象が広く運用を一本化しやすい |
| Snyk | SCA + 修正支援 | 修正提案やPR連携が強い（有料機能あり） |
| Grype | SBOM/イメージ脆弱性 | 軽量スキャンに強い |

## ベストプラクティス

### 1. 閾値を段階導入

- 初期は Critical/High をゲート対象にする。
- 運用定着後に Medium へ拡張する。

### 2. サプレッションを監査可能に管理

- 除外理由と期限を必ず記録する。
- 定期見直しで恒久除外を避ける。

### 3. スキャン結果を継続可視化

- レポートをアーティファクト保存する。
- 脆弱性残件の推移を追跡する。

## 公式ドキュメント

- 公式ページ: https://owasp.org/www-project-dependency-check/
- ドキュメント: https://jeremylong.github.io/DependencyCheck/
- GitHub: https://github.com/dependency-check/DependencyCheck
- NVD: https://nvd.nist.gov/

## まとめ

1. ** 早期検出 ** : 依存ライブラリの既知脆弱性をビルド段階で検出しやすい。
2. ** 品質統制 ** : 閾値ベースのゲート設定で、リリース品質を統制しやすい。
3. ** 監査対応 ** : サプレッション運用を整えることで、誤検知と監査対応を両立しやすい。
