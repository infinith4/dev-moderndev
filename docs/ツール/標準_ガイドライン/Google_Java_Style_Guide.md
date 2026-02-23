# Google Java Style Guide

## 概要

Google Java Style Guideは、Googleが公開しているJavaソースコードのコーディング標準です。ソースファイルの構造、命名規則、フォーマット（インデント、改行、空白）、Javadocコメントの書き方を包括的に定義しています。Google Java Formatツールで自動整形でき、CheckstyleのGoogle設定でルール準拠を自動チェックできます。Javaプロジェクトのコーディング規約として広く参照されています。

## 主な規則

### 1. ソースファイル構造

- **ファイル名**: トップレベルクラス名と同一（`MyClass.java`）
- **ファイルエンコーディング**: UTF-8
- **構成順序**: ライセンスヘッダー → パッケージ宣言 → インポート → クラス定義
- **インポート**: ワイルドカード（`*`）不使用、静的インポートとそれ以外を分離

### 2. フォーマット

- **インデント**: スペース2つ（タブ不使用）
- **列制限**: 100文字（Javadocの`@`句は除外可能）
- **ブレース**: K&Rスタイル（開き波括弧は同一行）
- **空行**: パッケージ宣言後、インポート後、クラスメンバー間
- **空白**: 制御構文のキーワード後、カンマ後、コロン前後等

### 3. 命名規則

| 対象 | 規則 | 例 |
|------|------|-----|
| パッケージ | 小文字のみ | `com.google.common` |
| クラス/インターフェース | UpperCamelCase | `ImmutableList` |
| メソッド | lowerCamelCase | `sendMessage` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| パラメータ/変数 | lowerCamelCase | `userName` |
| 型変数 | 単一大文字または大文字+数字 | `T`, `E`, `T2` |

### 4. プログラミング慣行

- **`@Override`**: 常に付与
- **例外キャッチ**: 空のcatchブロック禁止（最低でもコメント記載）
- **static メンバー**: クラス名で参照（インスタンス経由で参照しない）
- **finalizers**: 使用禁止

### 5. Javadoc

- **必須対象**: public/protectedなクラス・メソッド・フィールド
- **フォーマット**: 概要行 → 空行 → `@param`/`@return`/`@throws`
- **単一行Javadoc**: 短い場合は`/** Returns the count. */`形式可

## 適用方法

### Google Java Format（自動整形）

```bash
# ダウンロード
wget https://github.com/google/google-java-format/releases/download/v1.24.0/google-java-format-1.24.0-all-deps.jar

# 単一ファイルの整形
java -jar google-java-format-1.24.0-all-deps.jar --replace MyClass.java

# ディレクトリ配下を一括整形
find src -name "*.java" | xargs java -jar google-java-format-1.24.0-all-deps.jar --replace

# 差分確認（ドライラン）
java -jar google-java-format-1.24.0-all-deps.jar MyClass.java | diff - MyClass.java
```

### Checkstyle（ルール準拠チェック）

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.5.0</version>
    <configuration>
        <!-- Google Java Style準拠の設定 -->
        <configLocation>google_checks.xml</configLocation>
        <violationSeverity>warning</violationSeverity>
        <failOnViolation>true</failOnViolation>
    </configuration>
</plugin>
```

```bash
# Checkstyle実行
mvn checkstyle:check
```

### IDE設定

```
# IntelliJ IDEA
1. Settings > Editor > Code Style > Java
2. Scheme: Import Scheme > IntelliJ IDEA code style XML
3. https://raw.githubusercontent.com/google/styleguide/gh-pages/intellij-java-google-style.xml をインポート

# Eclipse
1. Preferences > Java > Code Style > Formatter
2. Import: https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml

# VS Code
1. Extension: "Checkstyle for Java" をインストール
2. settings.json: "java.checkstyle.configuration": "google_checks.xml"
```

### CI/CD統合（GitHub Actions）

```yaml
# .github/workflows/style-check.yml
name: Java Style Check

on: [pull_request]

jobs:
  style:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - name: Google Java Format Check
        uses: axel-op/googlejavaformat-action@v3
        with:
          args: "--dry-run --set-exit-if-changed"
```

## コード例

```java
// Google Java Style Guide準拠のコード例
package com.example.myapp.service;

import com.example.myapp.model.User;
import com.example.myapp.repository.UserRepository;
import java.util.List;
import java.util.Optional;

/** ユーザー管理サービス。ユーザーのCRUD操作を提供する。 */
public class UserService {

  private static final int MAX_RETRY_COUNT = 3;

  private final UserRepository userRepository;

  public UserService(UserRepository userRepository) {
    this.userRepository = userRepository;
  }

  /**
   * 指定されたIDのユーザーを取得する。
   *
   * @param userId ユーザーID
   * @return ユーザー情報（存在しない場合はempty）
   * @throws IllegalArgumentException userIdがnullの場合
   */
  public Optional<User> findById(String userId) {
    if (userId == null) {
      throw new IllegalArgumentException("userId must not be null");
    }
    return userRepository.findById(userId);
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Google Java Style Guide** | 無料 | CC-By 3.0 License |
| **Google Java Format** | 無料 | Apache License 2.0 |
| **Checkstyle** | 無料 | LGPL 2.1 |

## メリット

1. **業界標準**: Google発の広く認知されたJavaスタイルガイド
2. **ツール連携**: Google Java Format + Checkstyleで自動適用・検証
3. **IDE統合**: IntelliJ IDEA/Eclipse用の設定ファイルが公式提供
4. **包括的**: ファイル構造、フォーマット、命名、Javadocを網羅
5. **一貫性**: チーム内のコードスタイルを統一し、レビューコストを削減

## デメリット

1. **インデント2スペース**: Java標準の4スペースと異なり、既存プロジェクトとの差分が大きい
2. **列制限100文字**: 長い型名やメソッドチェーンで改行が頻発
3. **Google固有**: Googleの文化に基づくルールが全プロジェクトに適するとは限らない
4. **カスタマイズ困難**: Google Java Formatはゼロコンフィグ設計でルール変更不可

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Oracle Java Code Conventions** | Oracle公式 | より古典的なJavaスタイル |
| **Spring Framework Code Style** | Spring公式 | Spring開発に特化、4スペースインデント |
| **Alibaba Java Coding Guidelines** | Alibaba規約 | 中国発、p3c pluginで自動チェック |

## 公式リンク

- **スタイルガイド**: [https://google.github.io/styleguide/javaguide.html](https://google.github.io/styleguide/javaguide.html)
- **Google Java Format**: [https://github.com/google/google-java-format](https://github.com/google/google-java-format)
- **IDE設定ファイル**: [https://github.com/google/styleguide](https://github.com/google/styleguide)
- **Checkstyle google_checks.xml**: [https://github.com/checkstyle/checkstyle/blob/master/src/main/resources/google_checks.xml](https://github.com/checkstyle/checkstyle/blob/master/src/main/resources/google_checks.xml)

## 関連ドキュメント

- [Checkstyle](../開発ツール/Checkstyle.md)
- [Google Java Format](../開発ツール/Google_Java_Format.md)

---

**カテゴリ**: 標準ガイドライン
**対象工程**: 設計・実装
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
