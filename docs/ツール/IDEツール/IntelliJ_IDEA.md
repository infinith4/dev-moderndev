# IntelliJ IDEA

## 概要

IntelliJ IDEAは、JetBrains製のJava統合開発環境（IDE）です。インテリジェントコード補完、リファクタリング、デバッガー、ビルドツール統合（Maven、Gradle）、バージョン管理、Spring・Hibernate統合により、Java/Kotlin/Scala開発を支援します。Community Edition（無料）、Ultimate Edition（有料）、Android Studio（Google版）で広く採用されています。

## 主な機能

### 1. インテリジェント補完
- **スマート補完**: コンテキスト認識
- **リファクタリング**: 安全なリファクタリング
- **コード生成**: Getter/Setter自動生成
- **クイックフィックス**: エラー自動修正

### 2. デバッガー
- **ブレークポイント**: 条件付きブレークポイント
- **ステップ実行**: ステップイン/アウト
- **変数ウォッチ**: 変数監視
- **式評価**: 式評価

### 3. ビルドツール
- **Maven**: Maven統合
- **Gradle**: Gradle統合
- **依存関係**: 依存関係管理
- **タスク実行**: ビルドタスク

### 4. フレームワーク
- **Spring**: Spring Framework
- **Hibernate**: JPA/Hibernate
- **Java EE**: Jakarta EE
- **Kotlin**: Kotlinサポート

## 利用方法

### インストール

```bash
# macOS (Homebrew)
brew install --cask intellij-idea-ce  # Community Edition
brew install --cask intellij-idea     # Ultimate Edition

# Windows/Linux
# https://www.jetbrains.com/idea/download/
```

### プロジェクト作成

```
File > New > Project

- Java
  - SDK: Java 17
  - Build System: Maven/Gradle

- Spring Initializr
  - Dependencies: Spring Web, Spring Data JPA

- Kotlin
  - SDK: Kotlin 1.9

Create
```

### ショートカット

```
# 基本
Cmd/Ctrl + N: クラス検索
Cmd/Ctrl + Shift + N: ファイル検索
Cmd/Ctrl + E: 最近のファイル
Cmd/Ctrl + Shift + A: アクション検索

# 編集
Cmd/Ctrl + D: 行複製
Cmd/Ctrl + Y: 行削除
Cmd/Ctrl + /: コメント
Alt + Enter: クイックフィックス

# ナビゲーション
Cmd/Ctrl + B: 定義へジャンプ
Cmd/Ctrl + Alt + B: 実装へジャンプ
Cmd/Ctrl + U: スーパークラスへ
Alt + F7: 使用箇所検索

# リファクタリング
Shift + F6: リネーム
Cmd/Ctrl + Alt + M: メソッド抽出
Cmd/Ctrl + Alt + V: 変数抽出
Cmd/Ctrl + Alt + C: 定数抽出

# デバッグ
F8: ステップオーバー
F7: ステップイン
Shift + F8: ステップアウト
F9: 再開
```

### Live Templates

```java
// psvm + Tab
public static void main(String[] args) {

}

// sout + Tab
System.out.println();

// fori + Tab
for (int i = 0; i < ; i++) {

}

// カスタムテンプレート
Settings > Editor > Live Templates > + > Template Group
```

### コード生成

```java
// Alt + Insert

public class User {
    private String name;
    private String email;

    // Generate > Constructor
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    // Generate > Getter and Setter
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    // Generate > equals() and hashCode()
    @Override
    public boolean equals(Object o) { ... }

    @Override
    public int hashCode() { ... }

    // Generate > toString()
    @Override
    public String toString() {
        return "User{name='" + name + "', email='" + email + "'}";
    }
}
```

### リファクタリング

```java
// Before
public class Calculator {
    public int calculate(int a, int b) {
        return a + b + a * b + a / b;
    }
}

// Shift + F6: Rename
// Cmd/Ctrl + Alt + M: Extract Method

// After
public class Calculator {
    public int calculate(int a, int b) {
        return sum(a, b) + multiply(a, b) + divide(a, b);
    }

    private int sum(int a, int b) {
        return a + b;
    }

    private int multiply(int a, int b) {
        return a * b;
    }

    private int divide(int a, int b) {
        return a / b;
    }
}
```

### デバッグ設定

```
Run > Edit Configurations

+ > Application
  Name: Main
  Main class: com.example.Main
  VM options: -Xmx1024m
  Program arguments: --debug

+ > JUnit
  Name: UserTest
  Test kind: Class
  Class: com.example.UserTest
```

### Mavenプロジェクト

```xml
<!-- pom.xml -->
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.1.0</version>
        </dependency>
    </dependencies>
</project>
```

```
# Maven Tool Window
View > Tool Windows > Maven

- Lifecycle
  - clean
  - compile
  - test
  - package
  - install

- Plugins
```

### Gradleプロジェクト

```groovy
// build.gradle
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.1.0'
}

group = 'com.example'
version = '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'junit:junit:4.13.2'
}
```

### Spring Framework統合

```java
// Spring Bootアプリケーション
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// IntelliJ機能
- Spring Bean自動補完
- @Autowired インジェクション
- application.propertiesサポート
- HTTPクライアント（.http ファイル）
```

### データベースツール

```
View > Tool Windows > Database

+ > Data Source > MySQL/PostgreSQL

Host: localhost
Port: 3306/5432
Database: mydb
User: root

# SQL実行
Right-click database > New > Query Console
SELECT * FROM users;
```

### プラグイン

```
Settings > Plugins

人気プラグイン:
- Lombok
- Docker
- .ignore
- Rainbow Brackets
- Key Promoter X
- String Manipulation
- SonarLint
- CheckStyle-IDEA
```

### バージョン管理

```
VCS > Enable Version Control Integration > Git

# Git機能
- Commit: Cmd/Ctrl + K
- Push: Cmd/Ctrl + Shift + K
- Pull: Cmd/Ctrl + T
- Branches: 右下ブランチ名クリック
- Diff: Cmd/Ctrl + D
```

### HTTPクライアント

```http
### GET Request
GET https://api.example.com/users
Accept: application/json

### POST Request
POST https://api.example.com/users
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}

### With Variables
@host = https://api.example.com
@token = your-token

GET {{host}}/users
Authorization: Bearer {{token}}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Community Edition** | 🟢 完全無料 | Java、Kotlin、Groovy、Scala |
| **Ultimate Edition** | 💰 $149/年 | Spring、Java EE、データベース、Web開発 |
| **学生版** | 🟢 無料 | Ultimate Edition無料 |

## メリット

1. **インテリジェント**: 強力な補完
2. **リファクタリング**: 安全なリファクタリング
3. **フレームワーク**: Spring等統合
4. **Community Edition**: Java開発無料
5. **デバッガー**: 高機能デバッガー

## デメリット

1. **重い**: メモリ消費大
2. **起動遅い**: 起動時間長い
3. **Ultimate有料**: 高度機能有料
4. **学習曲線**: 機能多く複雑

## 公式リンク

- **公式サイト**: [https://www.jetbrains.com/idea/](https://www.jetbrains.com/idea/)
- **ドキュメント**: [https://www.jetbrains.com/help/idea/](https://www.jetbrains.com/help/idea/)

## 関連ドキュメント

- [IDEツール一覧](../IDEツール/)
- [Eclipse](./Eclipse.md)
- [VS Code](../エディタツール/VS_Code.md)

---

**カテゴリ**: IDEツール
**対象工程**: Java開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
