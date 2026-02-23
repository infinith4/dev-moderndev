# Checkstyle

## 概要

Checkstyleは、Javaソースコードがコーディング規約に準拠しているかを自動チェックする静的解析ツールです。Google Java Style GuideやSun Code Conventionsなどのプリセット設定が付属し、高度にカスタマイズ可能なルール設定で、ほぼすべてのコーディング標準に対応できます。Maven、Gradle、ANTとのビルドツール統合やEclipse、IntelliJなどのIDE統合を備え、CI/CDパイプラインでの継続的な品質チェックに活用されます。

## 主な機能

### 1. コーディング規約チェック

- **命名規約**: クラス名、メソッド名、変数名のパターンチェック
- **Javadoc**: Javadocコメントの有無・形式チェック
- **インポート**: 不要インポート、順序、ワイルドカード使用の検出
- **空白・フォーマット**: インデント、空行、波括弧位置のチェック
- **コードサイズ**: メソッド長、ファイル長、パラメータ数の制限

### 2. プリセット設定

- **Google Checks**: `google_checks.xml` - Google Java Style Guide準拠
- **Sun Checks**: `sun_checks.xml` - Sun Code Conventions準拠
- **カスタム設定**: XMLベースで独自ルールセットを定義可能

### 3. 検出レベル

- **error**: ビルド失敗を引き起こすルール違反
- **warning**: 警告として報告されるルール違反
- **info**: 情報レベルの通知
- **抑制**: `@SuppressWarnings` やフィルタによる個別抑制

### 4. レポート出力

- **XML**: 機械処理用レポート
- **HTML**: 人間が読みやすいレポート
- **SARIF**: GitHub Code Scanning連携用
- **コンソール**: CLI実行時の標準出力

## 利用方法

### インストール（コマンドライン）

```bash
# JARファイルをダウンロードして実行
java -jar checkstyle-10.21.4-all.jar -c /google_checks.xml MyClass.java
```

### Maven統合

```xml
<!-- pom.xml -->
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-checkstyle-plugin</artifactId>
      <version>3.6.0</version>
      <configuration>
        <configLocation>google_checks.xml</configLocation>
        <consoleOutput>true</consoleOutput>
        <failsOnError>true</failsOnError>
      </configuration>
      <executions>
        <execution>
          <id>validate</id>
          <phase>validate</phase>
          <goals>
            <goal>check</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

### Gradle統合

```groovy
// build.gradle
plugins {
    id 'checkstyle'
}

checkstyle {
    toolVersion = '10.21.4'
    configFile = file("${rootDir}/config/checkstyle/checkstyle.xml")
    maxWarnings = 0
}
```

### カスタム設定ファイル

```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
  "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
  "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
  <module name="TreeWalker">
    <module name="MethodLength">
      <property name="max" value="50"/>
    </module>
    <module name="ParameterNumber">
      <property name="max" value="5"/>
    </module>
    <module name="JavadocMethod"/>
    <module name="AvoidStarImport"/>
    <module name="UnusedImports"/>
  </module>
</module>
```

### CI/CD統合

```yaml
# .github/workflows/checkstyle.yml
name: Checkstyle

on: [push, pull_request]

jobs:
  checkstyle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - run: mvn checkstyle:check
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Checkstyle** | 無料 | オープンソース、LGPL 2.1 License |

## メリット

1. **高度にカスタマイズ可能**: XMLベースで細かくルールを設定可能
2. **プリセット充実**: Google/Sun規約がすぐに使える
3. **ビルドツール統合**: Maven/Gradle/ANTとのシームレスな統合
4. **IDE統合**: Eclipse、IntelliJ、NetBeansのプラグイン
5. **長い実績**: Java開発で広く採用されている成熟したツール
6. **CI/CD対応**: ビルドパイプラインでの自動チェック
7. **レポート出力**: HTML/XML/SARIF等の多様な出力形式

## デメリット

1. **設定XML複雑**: 初期設定のXMLが長く複雑になりやすい
2. **ルール過多**: デフォルト設定でノイズ（過剰な警告）が発生しやすい
3. **ソースコードのみ**: バイトコード解析は行わない（バグ検出はSpotBugs等）
4. **スタイルチェック中心**: セキュリティ脆弱性の検出には非対応
5. **Java限定**: Java以外の言語には使用不可

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **PMD** | ソースコード解析 | Checkstyleよりバグ検出寄り |
| **SpotBugs** | バイトコード解析 | Checkstyleと補完関係（併用推奨） |
| **SonarQube** | 統合品質管理 | Checkstyleより包括的だがサーバ構築が必要 |
| **Error Prone** | Google製コンパイラプラグイン | コンパイル時にバグパターンを検出 |

## 公式リンク

- **公式サイト**: [https://checkstyle.sourceforge.io/](https://checkstyle.sourceforge.io/)
- **GitHub**: [https://github.com/checkstyle/checkstyle](https://github.com/checkstyle/checkstyle)
- **ルール一覧**: [https://checkstyle.sourceforge.io/checks.html](https://checkstyle.sourceforge.io/checks.html)
- **Gradleプラグイン**: [https://docs.gradle.org/current/userguide/checkstyle_plugin.html](https://docs.gradle.org/current/userguide/checkstyle_plugin.html)

## 関連ドキュメント

- [Google Java Format](./Google_Java_Format.md)
- [SpotBugs](./SpotBugs.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
