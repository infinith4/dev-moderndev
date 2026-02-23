# SpotBugs

## 概要

SpotBugsは、Javaのコンパイル済みバイトコード（.classファイル）を解析してバグパターンを検出する静的解析ツールです。FindBugsの後継として開発され、400以上のバグパターンを検出します。NullPointerDereference、無限ループ、リソースリーク、スレッド安全性の問題などを、コードを実行せずに発見できます。Find Security Bugsプラグインを追加することで、OWASP Top 10に対応したセキュリティ脆弱性の検出も可能です。

## 主な機能

### 1. バグパターン検出（400+パターン）

- **Correctness**: NullPointerDereference、無限ループ、型キャストエラー
- **Bad Practice**: equals/hashCodeの不整合、例外処理の問題、リソース未クローズ
- **Performance**: 不要なオブジェクト生成、非効率なString操作
- **Multithreaded**: デッドロック、競合状態、不正な同期処理
- **Malicious Code**: 可変オブジェクトの公開、防御的コピーの欠如

### 2. セキュリティ検出（Find Security Bugs）

- **SQLインジェクション**: 動的クエリ構築の検出
- **XSS**: クロスサイトスクリプティングの脆弱性
- **パストラバーサル**: ファイルパス操作の脆弱性
- **暗号化**: 弱い暗号アルゴリズムの使用
- **デシリアライゼーション**: 安全でないデシリアライゼーション
- **144脆弱性タイプ**: 826以上のAPIシグネチャを認識

### 3. レポート出力

- **HTML**: ナビゲーション可能な概要レポート
- **XML**: 機械処理用の詳細レポート
- **SARIF**: GitHub Code Scanning連携
- **Eclipse GUI**: SpotBugs Eclipse Pluginでの対話的表示

### 4. フィルタリング

- **XMLフィルタ**: 特定のバグパターン、クラス、メソッドの除外
- **アノテーション**: `@SuppressFBWarnings` による個別抑制
- **優先度フィルタ**: High/Medium/Low優先度でのフィルタリング

## 利用方法

### Maven統合

```xml
<!-- pom.xml -->
<build>
  <plugins>
    <plugin>
      <groupId>com.github.spotbugs</groupId>
      <artifactId>spotbugs-maven-plugin</artifactId>
      <version>4.9.0</version>
      <configuration>
        <effort>Max</effort>
        <threshold>Low</threshold>
        <xmlOutput>true</xmlOutput>
        <plugins>
          <plugin>
            <groupId>com.h3xstream.findsecbugs</groupId>
            <artifactId>findsecbugs-plugin</artifactId>
            <version>1.13.0</version>
          </plugin>
        </plugins>
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
mvn spotbugs:check

# レポート生成
mvn spotbugs:spotbugs
```

### Gradle統合

```groovy
// build.gradle
plugins {
    id 'com.github.spotbugs' version '6.1.2'
}

spotbugs {
    effort = com.github.spotbugs.snom.Effort.MAX
    reportLevel = com.github.spotbugs.snom.Confidence.LOW
}

dependencies {
    spotbugsPlugins 'com.h3xstream.findsecbugs:findsecbugs-plugin:1.13.0'
}

spotbugsMain {
    reports {
        html { required = true }
        xml { required = false }
    }
}
```

```bash
# Gradle実行
./gradlew spotbugsMain
```

### フィルタ設定

```xml
<!-- spotbugs-exclude.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<FindBugsFilter>
  <!-- 生成コードを除外 -->
  <Match>
    <Package name="~.*\.generated\..*"/>
  </Match>
  <!-- 特定バグパターンを除外 -->
  <Match>
    <Bug pattern="DM_DEFAULT_ENCODING"/>
  </Match>
  <!-- テストコードの一部ルールを除外 -->
  <Match>
    <Class name="~.*Test"/>
    <Bug category="PERFORMANCE"/>
  </Match>
</FindBugsFilter>
```

### CI/CD統合

```yaml
# .github/workflows/spotbugs.yml
name: SpotBugs

on: [push, pull_request]

jobs:
  spotbugs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - run: mvn compile spotbugs:check
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **SpotBugs** | 無料 | オープンソース、LGPL License |
| **Find Security Bugs** | 無料 | オープンソース、セキュリティ検出プラグイン |

## メリット

1. **バイトコード解析**: ソースコードなしでもJARから解析可能
2. **400+バグパターン**: 幅広いバグカテゴリをカバー
3. **セキュリティ検出**: Find Security Bugsで脆弱性スキャン
4. **ビルドツール統合**: Maven/Gradle/ANT/SBTとの統合
5. **IDE統合**: Eclipse、IntelliJプラグイン
6. **SARIF出力**: GitHub Code Scanningとの直接連携
7. **FindBugs互換**: FindBugsからの移行が容易

## デメリット

1. **偽陽性**: 一部のバグパターンで誤検出が発生
2. **バイトコード必要**: コンパイル後でないと解析できない
3. **実行速度**: 大規模プロジェクトでは解析に時間がかかる
4. **設定複雑**: フィルタ設定のXMLが煩雑
5. **JDK 11+**: 実行にJDK 11以上が必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Checkstyle** | ソースコードスタイルチェック | SpotBugsと補完関係（併用推奨） |
| **PMD** | ソースコード解析 | SpotBugsよりソースレベルの問題に強い |
| **Error Prone** | コンパイラプラグイン | コンパイル時に検出、SpotBugsより高速 |
| **SonarQube** | 統合品質管理 | SpotBugsより包括的だがサーバ構築が必要 |
| **Semgrep** | パターンマッチ解析 | 多言語対応、カスタムルール作成が容易 |

## 公式リンク

- **公式サイト**: [https://spotbugs.github.io/](https://spotbugs.github.io/)
- **GitHub**: [https://github.com/spotbugs/spotbugs](https://github.com/spotbugs/spotbugs)
- **Mavenプラグイン**: [https://spotbugs.github.io/spotbugs-maven-plugin/](https://spotbugs.github.io/spotbugs-maven-plugin/)
- **Find Security Bugs**: [https://find-sec-bugs.github.io/](https://find-sec-bugs.github.io/)
- **バグ解説**: [https://spotbugs.readthedocs.io/](https://spotbugs.readthedocs.io/)

## 関連ドキュメント

- [Checkstyle](./Checkstyle.md)
- [Google Java Format](./Google_Java_Format.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
