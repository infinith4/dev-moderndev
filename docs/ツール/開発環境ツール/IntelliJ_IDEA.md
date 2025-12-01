# IntelliJ IDEA

## 概要

IntelliJ IDEAは、JetBrainsが開発したJava向けの統合開発環境（IDE）です。強力なコード解析、リファクタリング機能、優れた開発者体験により、Java開発のデファクトスタンダードとなっています。

**主な特徴:**
- 高度なコード補完とインテリジェントな提案
- 強力なリファクタリング機能
- 組み込みデバッガとプロファイラ
- バージョン管理システム（Git、SVN等）の統合
- データベースツール統合
- Spring、Maven、Gradle等の主要フレームワーク対応
- プラグインによる拡張性

## 料金プラン

| プラン | 月額料金 | 年額料金 | 主な機能 |
|--------|----------|----------|----------|
| **Community Edition** | 無料 | 無料 | Java、Kotlin、Groovy、Scala開発、Android開発、Maven/Gradle |
| **Ultimate Edition** | $24.90（初年度） | $249（初年度） | Spring、Jakarta EE、Micronaut、データベース、Web開発、JavaScript/TypeScript |
| **Ultimate Edition** | $19.90（2年目） | $199（2年目） | 同上（継続割引） |
| **Ultimate Edition** | $14.90（3年目以降） | $149（3年目以降） | 同上（継続割引） |
| **All Products Pack** | $77.90（初年度） | $779（初年度） | JetBrains全製品（IntelliJ、PyCharm、WebStorm等） |

※ 学生・教員・オープンソースプロジェクトは無料ライセンスあり

## メリット・デメリット

### メリット

1. **インテリジェントなコード補完**: コンテキストを理解した高精度な補完
2. **強力なリファクタリング**: 安全で広範囲なコード変更が可能
3. **統合開発環境**: ビルド、テスト、デバッグ、デプロイが一つのツールで完結
4. **フレームワーク対応**: Spring、Hibernate、JPA等の主要フレームワークをネイティブサポート
5. **データベース統合**: データベースクライアント機能内蔵
6. **生産性の高さ**: ショートカット、Live Templates、Postfix Completionで高速開発
7. **エンタープライズ対応**: 大規模プロジェクトでも快適に動作
8. **優れたデバッガ**: ブレークポイント、条件付きブレーク、式評価等

### デメリット

1. **高額な料金**: Ultimate Editionは有料（初年度$249）
2. **重い動作**: メモリ消費が大きく、低スペックPCでは動作が遅い
3. **学習曲線**: 多機能ゆえに初心者には複雑
4. **起動時間**: プロジェクトのインデックス作成に時間がかかる
5. **Community版の制限**: Web開発、Spring等はUltimate版のみ

## 利用できる開発工程

| 工程 | 活用度 | 主な用途 |
|------|--------|----------|
| 企画プロセス | ⭐⭐ | プロトタイプ作成 |
| 要件定義 | ⭐⭐ | ドキュメント作成 |
| アーキテクチャ設計 | ⭐⭐⭐⭐ | UML図作成、コード設計 |
| 詳細設計 | ⭐⭐⭐⭐⭐ | インターフェース設計、クラス設計 |
| 開発 | ⭐⭐⭐⭐⭐ | コーディング、リファクタリング |
| テスト | ⭐⭐⭐⭐⭐ | ユニットテスト、統合テスト、カバレッジ分析 |
| リリース | ⭐⭐⭐⭐ | ビルド、パッケージング |
| 運用・保守 | ⭐⭐⭐⭐ | デバッグ、プロファイリング |

## 基本的な利用方法

### 1. インストール

```bash
# JetBrains Toolbox（推奨）
# https://www.jetbrains.com/toolbox-app/ からダウンロード

# Windows (Chocolatey)
choco install intellijidea-ultimate
# または Community Edition
choco install intellijidea-community

# macOS (Homebrew)
brew install --cask intellij-idea
# または Community Edition
brew install --cask intellij-idea-ce

# Linux (Snap)
sudo snap install intellij-idea-ultimate --classic
# または Community Edition
sudo snap install intellij-idea-community --classic
```

### 2. プロジェクトの作成

```
新規プロジェクト:
1. File → New → Project
2. プロジェクトタイプを選択:
   - Java
   - Spring Boot
   - Maven
   - Gradle
   - Jakarta EE
3. SDK（JDK）を選択
4. プロジェクト名、場所を指定
5. Create

既存プロジェクトを開く:
1. File → Open
2. プロジェクトのルートディレクトリ（pom.xml、build.gradle等がある場所）を選択
3. IntelliJ IDEAがプロジェクト構造を自動検出
```

### 3. 基本操作

```
コード編集:
- Ctrl + Space: 基本補完
- Ctrl + Shift + Space: スマート補完
- Alt + Enter: クイックフィックス、インテンション
- Ctrl + Alt + L: コードフォーマット
- Ctrl + Alt + O: import文の最適化

ナビゲーション:
- Ctrl + N: クラスに移動
- Ctrl + Shift + N: ファイルに移動
- Ctrl + B: 定義へジャンプ
- Ctrl + Alt + B: 実装へジャンプ
- Ctrl + Shift + A: アクションを検索

リファクタリング:
- Shift + F6: 名前変更
- Ctrl + Alt + M: メソッドの抽出
- Ctrl + Alt + V: 変数の抽出
- Ctrl + Alt + C: 定数の抽出
- F6: 移動
```

### 4. Live Templates

```java
// 「psvm」と入力してTab
public static void main(String[] args) {

}

// 「sout」と入力してTab
System.out.println();

// 「fori」と入力してTab
for (int i = 0; i < ; i++) {

}

// 「iter」と入力してTab
for (String arg : args) {

}

// カスタムLive Templateの作成
Settings → Editor → Live Templates → 「+」
```

## 工程別の活用方法

### アーキテクチャ設計での活用

**UML図の作成:**
```
Ultimate Editionの機能:
1. クラスを右クリック → Diagrams → Show Diagram
2. UMLクラス図が自動生成
3. 依存関係、継承関係が可視化

図の種類:
- Class Diagram（クラス図）
- Package Dependencies（パッケージ依存関係）
- Module Dependencies（モジュール依存関係）

操作:
- 図から直接クラス作成
- リファクタリングが図に反映
- 画像としてエクスポート
```

**プロジェクト構造の設計:**
```
File → Project Structure (Ctrl + Alt + Shift + S)

設定項目:
- Modules: モジュール構成
- Libraries: 依存ライブラリ
- Facets: フレームワーク設定（Spring、JPA等）
- Artifacts: ビルド成果物
- SDKs: 使用するJDK
```

### 詳細設計での活用

**インターフェース駆動開発:**
```java
// インターフェース定義
public interface UserService {
    User findById(Long id);
    List<User> findAll();
    User save(User user);
    void delete(Long id);
}

// Alt + Enter → Implement interface
public class UserServiceImpl implements UserService {
    // メソッドスタブが自動生成
    @Override
    public User findById(Long id) {
        return null; // TODO: implement
    }
    // ...
}
```

**テストファーストアプローチ:**
```java
// テストクラスを先に作成
public class UserServiceTest {
    @Test
    void findById_shouldReturnUser() {
        // Alt + Enter → Create class 'UserService'
        UserService service = new UserService();
        // Alt + Enter → Create method 'findById'
        User user = service.findById(1L);
        assertNotNull(user);
    }
}
```

### 開発での活用

**Spring Boot開発:**
```java
// Spring Boot プロジェクトの作成
File → New → Project → Spring Initializr

依存関係の管理:
- pom.xmlまたはbuild.gradleを編集
- Alt + Insert → Dependency
- 自動補完で依存関係を追加

Spring機能:
- @Autowired の依存関係チェック
- Spring Bean の可視化
- application.properties/yml の補完
- REST API エンドポイントの一覧表示
```

**リファクタリング:**
```
メソッドの抽出:
1. コードブロックを選択
2. Ctrl + Alt + M
3. メソッド名を入力
4. パラメータ、戻り値が自動推論

変数のインライン化:
1. 変数にカーソル
2. Ctrl + Alt + N
3. 変数が使用箇所で展開される

クラスの移動:
1. クラスにカーソル
2. F6
3. 移動先パッケージを選択
4. import文が自動更新
```

**コード生成:**
```java
public class User {
    private Long id;
    private String name;
    private String email;

    // Alt + Insert → Constructor
    // Alt + Insert → Getter and Setter
    // Alt + Insert → equals() and hashCode()
    // Alt + Insert → toString()
}

// Lombokプラグインを使用
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private String email;
}
```

### テストでの活用

**JUnitテスト:**
```java
// テストクラスの自動生成
// クラス上で Ctrl + Shift + T → Create New Test

@Test
void testUserCreation() {
    User user = new User("John", "john@example.com");
    assertEquals("John", user.getName());
}

// テスト実行:
// メソッド横の緑アイコンをクリック
// または Ctrl + Shift + F10

// カバレッジ測定:
// Run → Run 'Tests' with Coverage
```

**モックとスタブ:**
```java
// Mockitoを使用
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    void findById_shouldReturnUser() {
        // Given
        User mockUser = new User(1L, "John");
        when(userRepository.findById(1L))
            .thenReturn(Optional.of(mockUser));

        // When
        User user = userService.findById(1L);

        // Then
        assertNotNull(user);
        assertEquals("John", user.getName());
        verify(userRepository).findById(1L);
    }
}
```

**テストデータの生成:**
```
プラグイン:
- JUnit Generator
- TestMe
- Squaretest

機能:
- テストメソッドの自動生成
- テストデータのファクトリー作成
- パラメータ化テストのサポート
```

### データベース開発での活用

**データベースツール（Ultimate版）:**
```
Database Tool Window:
1. View → Tool Windows → Database
2. 「+」→ Data Source → PostgreSQL/MySQL/Oracle等
3. 接続情報を入力
4. Test Connection → OK

機能:
- SQLコンソール（Ctrl + Shift + F10で実行）
- テーブルデータの閲覧・編集
- ER図の自動生成
- SQLコード補完
- クエリ履歴
```

**JPA/Hibernateサポート:**
```java
// エンティティクラス
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    // IntelliJの機能:
    // - JPQLの補完
    // - エンティティとテーブルの対応確認
    // - N+1問題の検出
    // - データベーススキーマとの同期チェック
}
```

### デバッグとプロファイリング

**デバッガ:**
```
ブレークポイント:
- 行番号をクリック（または Ctrl + F8）
- 条件付きブレークポイント（右クリック → Condition）
- ログポイント（メッセージを出力するだけ）

デバッグ実行:
- Shift + F9: デバッグモードで実行
- F8: ステップオーバー
- F7: ステップイン
- Shift + F8: ステップアウト
- F9: 次のブレークポイントまで実行

評価:
- Alt + F8: 式を評価
- ウォッチ式を追加
- 変数の値を変更
```

**プロファイラ（Ultimate版）:**
```
機能:
- CPU プロファイリング
- メモリプロファイリング
- メソッド呼び出しトレース

使い方:
1. Run → Profile...
2. プロファイリング結果を分析
3. ホットスポット（重い処理）を特定
4. メモリリーク検出
```

## 公式ドキュメント

- **公式サイト**: https://www.jetbrains.com/idea/
- **ドキュメント**: https://www.jetbrains.com/help/idea/
- **チュートリアル**: https://www.jetbrains.com/idea/learn/
- **プラグインマーケットプレイス**: https://plugins.jetbrains.com/
- **ブログ**: https://blog.jetbrains.com/idea/

## 学習リソース

### 公式リソース

1. **IntelliJ IDEA Documentation**
   - URL: https://www.jetbrains.com/help/idea/
   - 包括的なドキュメント、チュートリアル

2. **JetBrains Academy**
   - URL: https://www.jetbrains.com/academy/
   - 無料のプログラミング学習プラットフォーム

3. **JetBrains YouTube チャンネル**
   - URL: https://www.youtube.com/@intellijidea
   - Tips、チュートリアル、ウェビナー

### 外部リソース

1. **Udemy - IntelliJ IDEA コース**
   - 「IntelliJ IDEA Tricks to Boost Productivity」
   - 生産性向上のテクニック

2. **書籍**
   - 「IntelliJ IDEA 実践ガイド」（日本語）
   - 実践的な使い方を学べる

3. **Qiita/Zenn**
   - IntelliJ IDEA Tips記事多数

## 関連リンク

### 推奨プラグイン

**必須:**
- **Lombok**: Lombokサポート
- **SonarLint**: コード品質チェック
- **CheckStyle-IDEA**: コードスタイルチェック
- **Google Java Format**: Googleスタイルフォーマット

**生産性向上:**
- **Key Promoter X**: ショートカットの学習支援
- **String Manipulation**: 文字列操作ユーティリティ
- **Rainbow Brackets**: 括弧の色分け
- **GitToolBox**: Git拡張機能

**フレームワーク:**
- **Spring Assistant**: Spring開発支援
- **MyBatisX**: MyBatis統合
- **JPA Buddy**: JPA/Hibernate開発支援

**その他:**
- **Docker**: Docker統合
- **.ignore**: .gitignore サポート
- **Kubernetes**: Kubernetes マニフェスト編集

### JetBrains製品ファミリー

- **PyCharm**: Python開発IDE
- **WebStorm**: JavaScript/TypeScript開発IDE
- **GoLand**: Go開発IDE
- **Rider**: .NET開発IDE
- **CLion**: C/C++開発IDE
- **RubyMine**: Ruby開発IDE
- **PhpStorm**: PHP開発IDE
- **DataGrip**: データベースIDE

### コミュニティ

- **JetBrains Community**: https://www.jetbrains.com/community/
- **Stack Overflow**: タグ「intellij-idea」
- **Reddit**: r/IntelliJIDEA

## ベストプラクティス

### パフォーマンスチューニング

```
メモリ設定:
Help → Edit Custom VM Options

推奨設定（16GB RAM搭載マシン）:
-Xms2g
-Xmx4g
-XX:ReservedCodeCacheSize=512m
-XX:+UseG1GC

インデックス最適化:
- File → Invalidate Caches / Restart（定期的に実行）
- 不要なプラグインを無効化
- 大規模プロジェクトでは不要なモジュールを除外
```

### ショートカットマスター

```
最重要ショートカット:
- Ctrl + Shift + A: Find Action（すべての機能を検索）
- Alt + Enter: Show Intention Actions（クイックフィックス）
- Ctrl + W: 選択範囲を拡大
- Ctrl + /: 行コメント
- Ctrl + Shift + /: ブロックコメント
- Ctrl + D: 行を複製
- Ctrl + Y: 行を削除
- Shift × 2: Search Everywhere

カスタマイズ:
Settings → Keymap
- プリセット: Windows、macOS、Eclipse、Visual Studio等
```

### コードスタイル設定

```java
// Settings → Editor → Code Style → Java

推奨設定:
- Indent: 4 spaces
- Continuation indent: 8 spaces
- Tab size: 4
- Use tab character: ✗（スペースを使用）

.editorconfig を使用:
root = true

[*.java]
indent_style = space
indent_size = 4
trim_trailing_whitespace = true
insert_final_newline = true
```

### プロジェクト構成のベストプラクティス

```
推奨ディレクトリ構造:
project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       └── model/
│   │   └── resources/
│   │       ├── application.yml
│   │       └── static/
│   └── test/
│       ├── java/
│       └── resources/
├── .idea/                  # IntelliJ設定（.gitignoreに追加推奨）
├── pom.xml または build.gradle
└── README.md
```
