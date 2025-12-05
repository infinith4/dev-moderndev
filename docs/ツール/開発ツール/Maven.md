# Maven

## 概要

Mavenは、Java向けプロジェクト管理・ビルド自動化ツールです。pom.xml（Project Object Model）で依存関係、ビルド、テスト、パッケージング、デプロイを宣言的に定義し、Maven Central Repositoryから依存ライブラリを自動ダウンロードします。標準ディレクトリ構造、プラグインアーキテクチャ、マルチモジュールプロジェクトにより、Javaエコシステムの標準ビルドツールとして広く採用されています。

## 主な機能

### 1. 依存関係管理
- **Maven Central**: 中央リポジトリ
- **pom.xml**: 依存関係宣言
- **トランジティブ依存**: 推移的依存解決

### 2. ビルドライフサイクル
- **clean**: クリーンアップ
- **compile**: コンパイル
- **test**: テスト実行
- **package**: JAR/WAR作成
- **install**: ローカルリポジトリ
- **deploy**: リモートリポジトリ

### 3. プラグイン
- **compiler**: Javaコンパイル
- **surefire**: ユニットテスト
- **jar**: JAR作成

### 4. マルチモジュール
- **親POM**: 共通設定
- **子モジュール**: サブプロジェクト

## 利用方法

### インストール

```bash
# macOS (Homebrew)
brew install maven

# バージョン確認
mvn -version
```

### pom.xml

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

### ビルド実行

```bash
# ビルド
mvn clean package

# テスト
mvn test

# インストール
mvn install

# 依存関係ツリー
mvn dependency:tree
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Maven** | 🟢 完全無料 | オープンソース、Apache License |

## メリット

1. **完全無料**: オープンソース
2. **標準**: Java標準ビルドツール
3. **Maven Central**: 豊富なライブラリ
4. **宣言的**: pom.xml宣言的設定
5. **IDE統合**: IntelliJ、Eclipse統合

## デメリット

1. **XML冗長**: pom.xml冗長
2. **柔軟性**: Gradleより柔軟性低い
3. **ビルド時間**: 大規模で遅い
4. **依存競合**: 依存競合解決難しい

## 公式リンク

- **公式サイト**: [https://maven.apache.org/](https://maven.apache.org/)
- **Maven Central**: [https://search.maven.org/](https://search.maven.org/)

## 関連ドキュメント

- [ビルドツール一覧](../ビルドツール/)
- [Gradle](./Gradle.md)

---

**カテゴリ**: ビルドツール  
**対象工程**: ビルド  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
