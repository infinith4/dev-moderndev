# Gradle

## 概要

Gradleは、Java/Kotlin/Android向けビルド自動化ツールです。Groovy/Kotlin DSLでビルドスクリプトを記述し、依存関係管理、マルチプロジェクトビルド、増分ビルド、ビルドキャッシュにより、高速かつ柔軟なビルドを実現します。Android公式ビルドツール、Spring Boot対応、CI/CD統合で広く採用されています。

## 主な機能

### 1. ビルド自動化
- **タスク**: compile、test、build
- **依存関係**: Maven Central、JCenter
- **マルチプロジェクト**: サブプロジェクト管理

### 2. 高性能
- **増分ビルド**: 変更ファイルのみ
- **ビルドキャッシュ**: ビルド結果再利用
- **並列実行**: タスク並列化

### 3. DSL
- **Groovy DSL**: build.gradle
- **Kotlin DSL**: build.gradle.kts

### 4. プラグイン
- **Java Plugin**: Java ビルド
- **Android Plugin**: Android アプリ
- **Spring Boot Plugin**: Spring Boot

## 利用方法

### インストール

```bash
# macOS (Homebrew)
brew install gradle

# Gradle Wrapper
./gradlew
```

### build.gradle

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

test {
    useJUnitPlatform()
}
```

### ビルド実行

```bash
# ビルド
./gradlew build

# テスト
./gradlew test

# クリーン
./gradlew clean

# 依存関係表示
./gradlew dependencies
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Gradle** | 🟢 無料 | オープンソース、Apache License |
| **Gradle Enterprise** | 💰 商用 | ビルド高速化、分析 |

## メリット

1. **無料**: オープンソース
2. **高速**: 増分ビルド、キャッシュ
3. **柔軟**: DSL、プラグイン
4. **Android**: Android公式
5. **Maven互換**: Maven依存関係

## デメリット

1. **学習曲線**: DSL習得必要
2. **ビルド時間**: 初回ビルド遅い
3. **デバッグ**: エラー解析難しい
4. **メモリ**: メモリ消費大

## 公式リンク

- **公式サイト**: [https://gradle.org/](https://gradle.org/)
- **ドキュメント**: [https://docs.gradle.org/](https://docs.gradle.org/)

## 関連ドキュメント

- [ビルドツール一覧](../ビルドツール/)
- [Maven](./Maven.md)

---

**カテゴリ**: ビルドツール  
**対象工程**: ビルド  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
