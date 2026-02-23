# OWASP Dependency-Check

## 概要

OWASP Dependency-Checkは、プロジェクトの依存ライブラリに含まれる既知の脆弱性を検出するソフトウェアコンポジション分析（SCA）ツールです。依存関係からベンダー・製品・バージョン情報を収集し、NIST National Vulnerability Database（NVD）のCVEデータと照合して脆弱性を特定します。単純なハッシュマッチングではなく、エビデンスベースの分析エンジンにより、信頼度付きのCPEマッチングを行い偽陽性を低減します。

## 主な機能

### 1. 脆弱性検出

- **CVEデータベース照合**: NVD（National Vulnerability Database）との自動照合
- **CPEマッチング**: エビデンスベースのCommon Platform Enumeration識別
- **CVSSスコア**: 脆弱性の深刻度スコア表示（CVSS v2/v3）
- **信頼度レベル**: 各検出結果にConfidence（High/Medium/Low）を付与

### 2. 対応言語・エコシステム

- **Java**: Maven、Gradle、JAR/WAR/EAR
- **.NET**: NuGet、.NET assemblies
- **Node.js**: npm、yarn
- **Python**: pip（requirements.txt）、Poetry
- **Ruby**: Bundler（Gemfile.lock）
- **Go**: Go modules
- **Rust**: Cargo
- **C/C++**: CMake（実験的）

### 3. レポート

- **HTML**: 詳細な脆弱性レポート（CVE詳細、CVSSスコア、影響範囲）
- **JSON**: 機械処理用レポート
- **XML**: 他ツールとの統合用
- **SARIF**: GitHub Code Scanning連携
- **JUnit XML**: CI/CDテスト結果連携

### 4. サプレッション（誤検知管理）

- **XMLフィルタ**: 誤検知をsuppression.xmlで管理
- **監査証跡**: 抑制理由の記録
- **CVE単位**: 特定CVEの除外
- **ライブラリ単位**: 特定依存関係の除外

## 利用方法

### CLI実行

```bash
# ダウンロード
# https://github.com/dependency-check/DependencyCheck/releases からZIPを取得

# プロジェクトスキャン
dependency-check --project "MyApp" --scan ./src --out ./reports

# 重要度閾値でビルド失敗
dependency-check --project "MyApp" --scan . --failOnCVSS 7

# NVDデータベースの更新のみ
dependency-check --updateonly

# サプレッションファイル指定
dependency-check --project "MyApp" --scan . --suppression suppression.xml
```

### Maven統合

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
          <goals>
            <goal>check</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

```bash
# Maven実行
mvn dependency-check:check

# レポート生成のみ
mvn dependency-check:aggregate
```

### Gradle統合

```groovy
// build.gradle
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
# Gradle実行
./gradlew dependencyCheckAnalyze
```

### サプレッションファイル

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <!-- 特定CVEの除外（理由付き） -->
  <suppress>
    <notes><![CDATA[
      This is a false positive - the vulnerable component is not used in our code path.
    ]]></notes>
    <cve>CVE-2023-12345</cve>
  </suppress>

  <!-- 特定ライブラリのCVE除外 -->
  <suppress>
    <notes><![CDATA[Mitigated by WAF configuration]]></notes>
    <gav regex="true">^org\.example:mylib:.*$</gav>
    <cve>CVE-2024-56789</cve>
  </suppress>
</suppressions>
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/dependency-check.yml
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

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **OWASP Dependency-Check** | 無料 | オープンソース、Apache License 2.0 |

## メリット

1. **無料・OSS**: OWASP公式プロジェクトとして無料で利用可能
2. **NVD直接照合**: 公式脆弱性データベースとの直接連携
3. **エビデンスベース**: 信頼度付きのCPEマッチングで偽陽性を低減
4. **多言語対応**: Java、.NET、Node.js、Python、Ruby、Go等
5. **ビルドツール統合**: Maven、Gradle、ANTプラグイン
6. **サプレッション機能**: 誤検知の管理と監査証跡
7. **CVSSフィルタ**: 重要度閾値でビルド失敗を制御

## デメリット

1. **NVD APIキー**: NVD APIのレート制限対策にAPIキーの取得が推奨
2. **初回スキャン遅い**: 初回はNVDデータベースのダウンロードに時間がかかる
3. **偽陽性**: CPEマッチングの精度によっては誤検知が発生
4. **DB更新必要**: 定期的なNVDデータベースの更新が必要
5. **コンテナ非対応**: コンテナイメージのスキャンには非対応（Trivyが代替）

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Trivy** | オールインワンスキャナー | コンテナ・IaC対応、Dependency-Checkより高速 |
| **Snyk** | 商用SCAツール | 修正提案が充実だが有料 |
| **GitHub Dependabot** | GitHub統合SCA | GitHub専用、PRで自動修正提案 |
| **Renovate** | 依存関係更新自動化 | SCAではなく更新管理に特化 |

## 公式リンク

- **公式サイト**: [https://owasp.org/www-project-dependency-check/](https://owasp.org/www-project-dependency-check/)
- **GitHub**: [https://github.com/dependency-check/DependencyCheck](https://github.com/dependency-check/DependencyCheck)
- **ドキュメント**: [https://jeremylong.github.io/DependencyCheck/](https://jeremylong.github.io/DependencyCheck/)
- **Mavenプラグイン**: [https://mvnrepository.com/artifact/org.owasp/dependency-check-maven](https://mvnrepository.com/artifact/org.owasp/dependency-check-maven)

## 関連ドキュメント

- [Trivy](./Trivy.md)
- [SpotBugs](../開発ツール/SpotBugs.md)

---

**カテゴリ**: セキュリティ
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
