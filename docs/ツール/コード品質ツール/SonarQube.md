# SonarQube

## 概要

SonarQubeは、ソースコード品質管理プラットフォームです。静的コード解析、バグ検出、脆弱性スキャン、コードスメル検出、技術的負債測定により、コード品質を継続的に改善します。30+言語対応、CI/CD統合、オープンソースで広く使用されています。

## 主な機能

### 1. コード品質分析
- **バグ検出**: 潜在的バグ
- **脆弱性**: セキュリティ問題
- **コードスメル**: 保守性問題
- **重複コード**: コピペ検出

### 2. メトリクス
- **カバレッジ**: テストカバレッジ
- **複雑度**: サイクロマティック複雑度
- **技術的負債**: 修正工数
- **信頼性**: A-E評価

### 3. Quality Gate
- **合否判定**: 品質基準
- **カスタムルール**: プロジェクト別
- **CI/CD統合**: ビルド失敗
- **レポート**: ダッシュボード

### 4. 多言語対応
- **Java/C#/JavaScript**: サポート
- **Python/Go/PHP**: サポート
- **TypeScript/Ruby**: サポート
- **30+言語**: 対応

## 利用方法

### インストール（Docker）

```bash
# SonarQube起動
docker run -d --name sonarqube \
  -p 9000:9000 \
  sonarqube:latest

# アクセス
http://localhost:9000

# デフォルト認証
ユーザー: admin
パスワード: admin
```

### プロジェクト設定

```
SonarQube > Create new project

Project key: my-project
Display name: My Project

Generate token:
Token: squ_abc123xyz...

Choose analysis method:
- Maven
- Gradle
- .NET
- Other
```

### Maven統合

```xml
<!-- pom.xml -->
<properties>
  <sonar.host.url>http://localhost:9000</sonar.host.url>
  <sonar.login>squ_abc123xyz...</sonar.login>
</properties>

<build>
  <plugins>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>3.10.0.2594</version>
    </plugin>
  </plugins>
</build>
```

```bash
# スキャン実行
mvn clean verify sonar:sonar
```

### Gradle統合

```groovy
// build.gradle
plugins {
    id "org.sonarqube" version "4.4.1.3373"
}

sonarqube {
    properties {
        property "sonar.host.url", "http://localhost:9000"
        property "sonar.login", "squ_abc123xyz..."
        property "sonar.projectKey", "my-project"
        property "sonar.projectName", "My Project"
    }
}
```

```bash
# スキャン実行
./gradlew sonarqube
```

### SonarScanner CLI

```bash
# インストール
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
export PATH=$PATH:/path/to/sonar-scanner/bin

# 設定ファイル
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0
sonar.sources=src
sonar.host.url=http://localhost:9000
sonar.login=squ_abc123xyz...

# スキャン実行
sonar-scanner
```

### JavaScript/TypeScript

```bash
# 依存関係インストール
npm install --save-dev sonarqube-scanner

# package.json
{
  "scripts": {
    "sonar": "sonar-scanner"
  }
}
```

```javascript
// sonar-project.js
const scanner = require('sonarqube-scanner');

scanner({
  serverUrl: 'http://localhost:9000',
  token: 'squ_abc123xyz...',
  options: {
    'sonar.projectKey': 'my-project',
    'sonar.projectName': 'My Project',
    'sonar.sources': 'src',
    'sonar.tests': 'tests',
    'sonar.javascript.lcov.reportPaths': 'coverage/lcov.info'
  }
}, () => process.exit());
```

```bash
# スキャン実行
npm run sonar
```

### GitHub Actions統合

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: 17
          distribution: 'temurin'

      - name: Cache SonarQube packages
        uses: actions/cache@v3
        with:
          path: ~/.sonar/cache
          key: ${{ runner.os }}-sonar

      - name: SonarQube Scan
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: |
          mvn clean verify sonar:sonar \
            -Dsonar.projectKey=my-project \
            -Dsonar.host.url=$SONAR_HOST_URL \
            -Dsonar.login=$SONAR_TOKEN
```

### Quality Gate

```
SonarQube > Quality Gates > Create

Conditions:
- Coverage < 80%: FAILED
- Duplicated Lines > 3%: FAILED
- Maintainability Rating worse than A: FAILED
- Reliability Rating worse than A: FAILED
- Security Rating worse than A: FAILED

適用:
Project Settings > Quality Gate > Select gate
```

### カスタムルール

```
SonarQube > Rules > Create

Language: Java
Type: Code Smell
Severity: Major

Rule:
メソッド長は50行以内にすべき

Activate:
Quality Profiles > Java > Activate rule
```

### Pull Request分析

```yaml
# GitHub Actions
- name: SonarQube PR Analysis
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    mvn sonar:sonar \
      -Dsonar.pullrequest.key=${{ github.event.pull_request.number }} \
      -Dsonar.pullrequest.branch=${{ github.head_ref }} \
      -Dsonar.pullrequest.base=${{ github.base_ref }}
```

### Webhook通知

```
SonarQube > Administration > Webhooks > Create

Name: Slack Notification
URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL

Trigger:
- Quality Gate status changes

Slack通知:
Quality Gate FAILED on my-project
Coverage: 75% (< 80%)
```

### SonarLint（IDE統合）

```
VSCode:
Extensions > SonarLint

IntelliJ IDEA:
Preferences > Plugins > SonarLint

設定:
- SonarQube Server: http://localhost:9000
- Token: squ_abc123xyz...
- Project binding: my-project

リアルタイム:
コード入力中にリアルタイムでバグ・脆弱性検出
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Community** |  無料 | オープンソース、個人・小規模 |
| **Developer** |  $150/年 | ブランチ分析、PR装飾 |
| **Enterprise** |  $12,000/年 | ポートフォリオ、セキュリティレポート |
| **Data Center** |  $120,000/年 | 高可用性、スケーラビリティ |

## メリット

1. **無料枠**: Community版無料
2. **多言語**: 30+言語対応
3. **CI/CD統合**: Jenkins、GitHub Actions等
4. **継続的改善**: トレンド可視化
5. **IDE統合**: SonarLint

## デメリット

1. **リソース**: 大規模で重い
2. **誤検知**: ルール調整必要
3. **有料機能**: ブランチ分析有料
4. **学習曲線**: ルール理解必要

## 公式リンク

- **公式サイト**: [https://www.sonarsource.com/products/sonarqube/](https://www.sonarsource.com/products/sonarqube/)
- **ドキュメント**: [https://docs.sonarsource.com/sonarqube/](https://docs.sonarsource.com/sonarqube/)

## 関連ドキュメント

- [コード品質ツール一覧](../コード品質ツール/)
- [Jenkins](../CI_CDツール/Jenkins.md)
- [GitHub Actions](../CI_CDツール/GitHub_Actions.md)

---

**カテゴリ**: コード品質ツール
**対象工程**: コード品質管理
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0

