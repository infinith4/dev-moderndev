# Google Java Format

## 概要

Google Java Formatは、JavaソースコードをGoogle Java Style Guideに準拠した形式に自動整形するツールです。Blackと同様に「設定不要」の思想で設計されており、フォーマットオプションを意図的に提供しないことで、スタイル議論を完全に排除します。コマンドライン、Maven/Gradle、IntelliJ/Eclipse/VS Codeなど多様な実行方法をサポートしています。

## 主な機能

### 1. コードフォーマット

- **Google Java Style準拠**: Google Java Style Guideに完全準拠した整形
- **AOSP Style対応**: `--aosp-style` でAndroid Open Source Projectスタイルにも対応
- **部分フォーマット**: 指定行・指定オフセットのみの整形が可能
- **ファイル全体**: ファイル全体の一括フォーマット

### 2. 実行方法

- **コマンドライン**: JARファイルまたはGraalVMネイティブバイナリ
- **Maven/Gradle**: ビルドプロセスに統合
- **IntelliJ IDEA**: 公式プラグイン
- **Eclipse**: ドロップインプラグイン
- **VS Code**: google-java-format-for-vs-code拡張

### 3. 出力オプション

- **標準出力**: デフォルトで標準出力に結果を出力
- **インプレース**: `--replace` でファイルを直接書き換え
- **差分確認**: `--set-exit-if-changed` でCI向けチェック
- **ドライラン**: `--dry-run` で変更があるファイルの一覧表示

## 利用方法

### インストール

```bash
# Homebrew
brew install google-java-format

# JARダウンロード（GitHubリリースページから）
# https://github.com/google/google-java-format/releases
wget https://github.com/google/google-java-format/releases/download/v1.25.2/google-java-format-1.25.2-all-deps.jar

# GraalVMネイティブバイナリ（JVMフラグ不要）
# リリースページからプラットフォーム別バイナリをダウンロード
```

### コマンドライン実行

```bash
# 単一ファイルのフォーマット（標準出力）
java -jar google-java-format-1.25.2-all-deps.jar MyClass.java

# ファイルを直接書き換え
java -jar google-java-format-1.25.2-all-deps.jar --replace MyClass.java

# 複数ファイル
java -jar google-java-format-1.25.2-all-deps.jar --replace src/main/java/**/*.java

# AOSPスタイル
java -jar google-java-format-1.25.2-all-deps.jar --aosp-style --replace MyClass.java

# CIチェック（変更があれば非ゼロ終了）
java -jar google-java-format-1.25.2-all-deps.jar --set-exit-if-changed --dry-run MyClass.java
```

### Maven統合

```xml
<!-- pom.xml -->
<build>
  <plugins>
    <plugin>
      <groupId>com.spotify.fmt</groupId>
      <artifactId>fmt-maven-plugin</artifactId>
      <version>2.25</version>
      <executions>
        <execution>
          <goals>
            <goal>format</goal>
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
    id 'com.github.sherter.google-java-format' version '0.9'
}

googleJavaFormat {
    toolVersion = '1.25.2'
}
```

### CI/CD統合

```yaml
# .github/workflows/format-check.yml
name: Format Check

on: [push, pull_request]

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - uses: axel-op/googlejavaformat-action@v3
        with:
          args: "--set-exit-if-changed"
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Google Java Format** | 無料 | オープンソース、Apache License 2.0 |

## メリット

1. **ゼロコンフィグ**: 設定オプションがないため議論が不要
2. **Google Java Style準拠**: 広く採用されているスタイルガイドに準拠
3. **IDE統合**: IntelliJ、Eclipse、VS Codeをサポート
4. **ネイティブバイナリ**: GraalVMビルドでJVMフラグ不要
5. **部分フォーマット**: 指定行のみの整形が可能
6. **ビルドツール統合**: Maven/Gradleプラグインで自動実行

## デメリット

1. **カスタマイズ不可**: スタイルオプションが一切ない（設計方針）
2. **Google Style限定**: Google Java Style以外のスタイルには非対応（AOSPを除く）
3. **JDK 21必須**: 実行にJDK 21以上が必要
4. **既存コード影響**: 導入時に大量のフォーマット差分が発生
5. **JVMフラグ**: JAR版はJava 16+で`--add-exports`フラグが必要

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Checkstyle** | スタイルチェッカー | フォーマットではなく違反検出 |
| **Eclipse Formatter** | Eclipse内蔵フォーマッター | カスタマイズ性が高い |
| **IntelliJ Formatter** | IntelliJ内蔵フォーマッター | IDE依存だが柔軟 |
| **Spotless** | マルチ言語フォーマッター | google-java-formatをバックエンドとして利用可能 |

## 公式リンク

- **GitHub**: [https://github.com/google/google-java-format](https://github.com/google/google-java-format)
- **リリース**: [https://github.com/google/google-java-format/releases](https://github.com/google/google-java-format/releases)
- **IntelliJプラグイン**: [https://plugins.jetbrains.com/plugin/8527-google-java-format](https://plugins.jetbrains.com/plugin/8527-google-java-format)
- **Google Java Style Guide**: [https://google.github.io/styleguide/javaguide.html](https://google.github.io/styleguide/javaguide.html)

## 関連ドキュメント

- [Checkstyle](./Checkstyle.md)
- [SpotBugs](./SpotBugs.md)
- [ESLint](./ESLint.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
