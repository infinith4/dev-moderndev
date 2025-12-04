# SonarQube

## 概要

SonarQubeは、オープンソースの継続的コード品質管理プラットフォームです。静的コード解析でバグ、脆弱性、コードスメル、重複コード、コードカバレッジを検出し、30+言語（Java、JavaScript、Python、C#、PHP等）をサポートします。SonarCloud（クラウド版）、CI/CD統合、Quality Gate、セキュリティホットスポット検出により、DevSecOpsパイプラインでコード品質を継続的に改善します。

## 主な機能

### 1. コード解析
- **バグ検出**: 潜在的バグ
- **脆弱性**: セキュリティ脆弱性（OWASP Top 10、CWE）
- **コードスメル**: 保守性の問題
- **重複コード**: コピー&ペースト検出
- **カバレッジ**: テストカバレッジ

### 2. Quality Gate
- **品質基準**: 合格/不合格判定
- **カスタム設定**: プロジェクト固有基準
- **CI/CD統合**: パイプライン品質チェック

### 3. 多言語対応
- **30+言語**: Java、JavaScript、TypeScript、Python、C#、Go、Kotlin、PHP等
- **プラグイン**: コミュニティプラグイン

### 4. セキュリティ
- **セキュリティホットスポット**: レビュー必要箇所
- **CWE/OWASP**: 標準脆弱性分類
- **SAST**: Static Application Security Testing

## 利用方法

### インストール（Docker）

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  sonarqube:latest

# アクセス: http://localhost:9000
# デフォルト: admin/admin
```

### プロジェクト解析（Maven）

```xml
<!-- pom.xml -->
<properties>
    <sonar.host.url>http://localhost:9000</sonar.host.url>
</properties>
```

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.login=<token>
```

### プロジェクト解析（Node.js）

```bash
npm install -g sonarqube-scanner

sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<token>
```

### Quality Gate

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  push:
    branches: [main]
  pull_request:

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
      
      - name: Quality Gate
        uses: sonarsource/sonarqube-quality-gate-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Community** | 🟢 無料 | オープンソース、1言語プロジェクト |
| **Developer** | 💰 $150/年 | 複数言語、ブランチ分析 |
| **Enterprise** | 💰 $15,000/年 | ポートフォリオ管理、SAML |
| **SonarCloud** | 💰 $10/月〜 | クラウド版 |

## メリット

1. **継続的品質**: CI/CD統合
2. **多言語**: 30+言語対応
3. **セキュリティ**: OWASP、CWE検出
4. **Quality Gate**: 品質基準
5. **オープンソース**: Community Edition無料

## デメリット

1. **セットアップ**: 初期設定複雑
2. **リソース**: メモリ消費大
3. **誤検出**: False Positive
4. **学習曲線**: 機能多数

## 公式リンク

- **公式サイト**: [https://www.sonarqube.org/](https://www.sonarqube.org/)
- **SonarCloud**: [https://sonarcloud.io/](https://sonarcloud.io/)
- **ドキュメント**: [https://docs.sonarqube.org/](https://docs.sonarqube.org/)

## 関連ドキュメント

- [静的解析ツール一覧](../静的解析ツール/)
- [ESLint](../開発ツール/ESLint.md)

---

**カテゴリ**: 静的解析ツール  
**対象工程**: コード品質管理  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
