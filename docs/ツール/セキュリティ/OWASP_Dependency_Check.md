# OWASP Dependency-Check

## 概要

OWASP Dependency-Checkは、プロジェクトの依存ライブラリに含まれる既知の脆弱性を検出するソフトウェアコンポジション分析（SCA）ツールである。依存関係からベンダー・製品・バージョン情報を収集し、NIST National Vulnerability Database（NVD）のCVEデータと照合して脆弱性を特定する。エビデンスベースの分析エンジンにより、信頼度付きのCPEマッチングを行い偽陽性を低減する。

## 主な特徴

| 項目 | 内容 |
|------|------|
| オープンソース | OWASP公式プロジェクト、Apache License 2.0 |
| NVD直接照合 | 公式脆弱性データベースとの直接連携 |
| エビデンスベース | 信頼度付きのCPEマッチングで偽陽性を低減 |
| 多言語対応 | Java、.NET、Node.js、Python、Ruby、Go、Rust等 |
| ビルドツール統合 | Maven、Gradle、ANTプラグイン提供 |
| サプレッション機能 | 誤検知の管理と監査証跡 |
| CVSSフィルタ | 重要度閾値でビルド失敗を制御 |

## 主な機能

### 脆弱性検出機能

| 機能 | 説明 |
|------|------|
| CVEデータベース照合 | NVDとの自動照合 |
| CPEマッチング | エビデンスベースのCommon Platform Enumeration識別 |
| CVSSスコア | 脆弱性の深刻度スコア表示（CVSS v2/v3） |
| 信頼度レベル | 各検出結果にConfidence（High/Medium/Low）を付与 |

### レポート機能

| 機能 | 説明 |
|------|------|
| HTML | 詳細な脆弱性レポート |
| JSON | 機械処理用レポート |
| SARIF | GitHub Code Scanning連携 |
| JUnit XML | CI/CDテスト結果連携 |

### サプレッション機能

| 機能 | 説明 |
|------|------|
| XMLフィルタ | 誤検知をsuppression.xmlで管理 |
| 監査証跡 | 抑制理由の記録 |
| CVE単位除外 | 特定CVEの除外 |
| ライブラリ単位除外 | 特定依存関係の除外 |

## インストールとセットアップ

公式URL:
- [OWASP Dependency-Check 公式サイト](https://owasp.org/www-project-dependency-check/)
- [GitHub](https://github.com/dependency-check/DependencyCheck)
- [ドキュメント](https://jeremylong.github.io/DependencyCheck/)
- [Mavenプラグイン](https://mvnrepository.com/artifact/org.owasp/dependency-check-maven)

## 基本的な使い方

### 1. CLIでのスキャン

```bash
# ダウンロード: https://github.com/dependency-check/DependencyCheck/releases

# プロジェクトスキャン
dependency-check --project "MyApp" --scan ./src --out ./reports

# 重要度閾値でビルド失敗
dependency-check --project "MyApp" --scan . --failOnCVSS 7

# NVDデータベースの更新のみ
dependency-check --updateonly

# サプレッションファイル指定
dependency-check --project "MyApp" --scan . --suppression suppression.xml
```

### 2. Maven統合

```xml
<!-- pom.xml -->
<build>
  <plugins>
    <plugin>
      <groupId>org.owasp</groupId>
      <artifactId>dependency-check-maven</artifactId>
      <version>11.1.1</version>
      <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
        <suppressionFile>suppression.xml</suppressionFile>
        <formats>
          <format>HTML</format>
          <format>JSON</format>
        </formats>
      </configuration>
      <executions>
        <execution>
          <goals><goal>check</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

```bash
mvn dependency-check:check
```

### 3. Gradle統合

```groovy
plugins {
    id 'org.owasp.dependencycheck' version '11.1.1'
}

dependencyCheck {
    failBuildOnCVSS = 7.0f
    suppressionFile = 'suppression.xml'
    formats = ['HTML', 'JSON']
}
```

```bash
./gradlew dependencyCheckAnalyze
```

### 4. サプレッションファイル

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <suppress>
    <notes><![CDATA[
      False positive - the vulnerable component is not used in our code path.
    ]]></notes>
    <cve>CVE-2023-12345</cve>
  </suppress>

  <suppress>
    <notes><![CDATA[Mitigated by WAF configuration]]></notes>
    <gav regex="true">^org\.example:mylib:.*$</gav>
    <cve>CVE-2024-56789</cve>
  </suppress>
</suppressions>
```

## CI/CD 統合

### GitHub Actions

```yaml
name: Dependency Check

on: [push, pull_request]

jobs:
  depcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - name: Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'MyApp'
          path: '.'
          format: 'HTML'
          args: '--failOnCVSS 7'
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: dependency-check-report
          path: reports/
```

### GitLab CI

```yaml
dependency-check:
  stage: security
  image: owasp/dependency-check:latest
  script:
    - /usr/share/dependency-check/bin/dependency-check.sh
      --project "MyApp"
      --scan .
      --format JSON
      --format HTML
      --out reports/
      --failOnCVSS 7
  artifacts:
    paths:
      - reports/
    when: always
```

## 他ツールとの比較

### Dependency-Check vs Trivy

| 機能 | OWASP Dependency-Check | Trivy |
|------|----------------------|-------|
| 対象 | 依存ライブラリの脆弱性 | コンテナ、IaC、シークレットも対応 |
| データソース | NVD | 複数DB（NVD、GitHub Advisory等） |
| 速度 | 初回遅い（NVDダウンロード） | 高速 |
| ビルドツール統合 | Maven/Gradle/ANTプラグイン | CLI中心 |
| コンテナ対応 | なし | あり |

### Dependency-Check vs Snyk

| 機能 | OWASP Dependency-Check | Snyk |
|------|----------------------|------|
| 価格 | 無料 | 無料枠あり、高機能は有料 |
| 修正提案 | なし | PR自動生成 |
| 精度 | エビデンスベース | キュレーションDB |
| IDE統合 | なし | あり |

## ユースケース

| ユースケース | 目的 | 活用内容 |
|-------------|------|----------|
| 依存ライブラリの脆弱性検出 | 既知CVEの早期発見 | NVDとの照合で脆弱性を特定 |
| CI/CDセキュリティゲート | ビルドパイプラインでの脆弱性チェック | CVSSスコア閾値でビルド制御 |
| コンプライアンス対応 | セキュリティ監査への対応 | HTML/JSONレポートによる証跡管理 |
| 誤検知管理 | 効率的な脆弱性トリアージ | サプレッションファイルによる管理 |

## ベストプラクティス

### 1. NVD APIキーの取得

- NVD APIのレート制限対策にAPIキーの取得を推奨
- https://nvd.nist.gov/developers/request-an-api-key から取得
- CI/CDシークレットとして管理

### 2. サプレッションファイルの管理

- suppression.xmlをGit管理に含める
- 除外理由を必ず記載する
- 定期的に除外内容を見直す

### 3. CI/CDパイプラインへの統合

- CVSS閾値を段階的に引き上げる（まず9.0から開始）
- PRマージ前にスキャンを実行
- NVDデータベースのキャッシュで実行時間を短縮

## トラブルシューティング

### よくある問題と解決策

#### 1. 初回スキャンが非常に遅い

```
原因: NVDデータベースの初回ダウンロードに時間がかかる
解決策:
- NVD APIキーを設定してダウンロード速度を向上
- CI/CDではNVDデータベースをキャッシュ
- --updateonly で事前にDB更新
```

#### 2. 偽陽性が多い

```
原因: CPEマッチングの精度による誤検知
解決策:
- suppression.xmlで誤検知を管理
- 信頼度レベル（Confidence）を確認
- GAV（groupId:artifactId:version）での精密な除外設定
```

#### 3. NVD API接続エラー

```
原因: NVD APIのレート制限またはネットワーク問題
解決策:
- NVD APIキーを設定
- プロキシ設定を確認
- オフラインDBの利用を検討
```

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://owasp.org/www-project-dependency-check/
- GitHub: https://github.com/dependency-check/DependencyCheck
- ドキュメント: https://jeremylong.github.io/DependencyCheck/

### コミュニティ
- GitHub Issues: https://github.com/dependency-check/DependencyCheck/issues
- OWASP Slack: https://owasp.org/slack/invite

### チュートリアル
- Getting Started: https://jeremylong.github.io/DependencyCheck/
- Maven Plugin: https://jeremylong.github.io/DependencyCheck/dependency-check-maven/

## まとめ

OWASP Dependency-Checkは、依存ライブラリの脆弱性検出のためのOSS SCAツールとして、以下の場面で特に有用である:

1. **依存ライブラリのセキュリティ検証** - NVDとの直接照合で既知CVEを検出
2. **CI/CDセキュリティゲート** - CVSSスコア閾値によるビルドパイプライン制御
3. **コンプライアンス対応** - 詳細なレポート生成による監査証跡の管理
4. **Javaエコシステムとの統合** - Maven/Gradleプラグインによるシームレスな統合

OWASP公式プロジェクトとして信頼性が高く、無料で利用できるため、あらゆるプロジェクトのSCA導入に適している。
