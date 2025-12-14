# Cobertura

## 概要

**Cobertura**は、Javaプログラムのコードカバレッジ測定ツールです。テストスイート実行時のコード実行状況を計測し、HTML・XMLレポートを生成することで、テストの網羅性を可視化します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Mark Doliner / オープンソースコミュニティ |
| **種別** | コードカバレッジ測定ツール（Java） |
| **ライセンス** | GPL v2（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://cobertura.github.io/cobertura/ |
| **ドキュメント** | https://github.com/cobertura/cobertura/wiki |

**注意**: Coberturaのメンテナンスは停滞しており、後継として**JaCoCo**の使用が推奨されています。

## 主な特徴

### 1. コードカバレッジ測定
- **ライン・カバレッジ**: 実行された行の割合
- **ブランチ・カバレッジ**: 分岐条件の網羅性
- **複雑度計算**: Cyclomatic Complexity
- **クラス・メソッド単位**: 詳細な分析

### 2. レポート生成
- **HTMLレポート**: ブラウザで閲覧可能
- **XMLレポート**: CI/CD統合用
- **パッケージ階層**: パッケージ別カバレッジ
- **ソースコード表示**: カバー/未カバー箇所の色分け

### 3. ビルドツール統合
- **Maven**: cobertura-maven-plugin
- **Gradle**: Gradle Cobertura Plugin
- **Ant**: cobertura.jar タスク
- **コマンドライン**: 直接実行

### 4. CI/CD統合
- **Jenkins**: Cobertura Plugin
- **SonarQube**: カバレッジデータ連携
- **GitLab CI/CD**: XMLレポート解析
- **GitHub Actions**: カバレッジバッジ

## 使い方

### Maven統合

```xml
<!-- pom.xml -->
<project>
  <build>
    <plugins>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>cobertura-maven-plugin</artifactId>
        <version>2.7</version>
        <configuration>
          <formats>
            <format>html</format>
            <format>xml</format>
          </formats>
          <check>
            <branchRate>70</branchRate>
            <lineRate>80</lineRate>
            <haltOnFailure>true</haltOnFailure>
          </check>
        </configuration>
        <executions>
          <execution>
            <goals>
              <goal>clean</goal>
              <goal>check</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>

  <reporting>
    <plugins>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>cobertura-maven-plugin</artifactId>
        <version>2.7</version>
        <reportSets>
          <reportSet>
            <reports>
              <report>cobertura</report>
            </reports>
          </reportSet>
        </reportSets>
      </plugin>
    </plugins>
  </reporting>
</project>
```

```bash
# カバレッジ計測・レポート生成
mvn clean cobertura:cobertura

# テスト実行 + カバレッジチェック
mvn clean test cobertura:check

# サイト生成（レポート含む）
mvn site

# レポート閲覧
open target/site/cobertura/index.html
```

### Gradle統合

```groovy
// build.gradle
plugins {
    id 'java'
    id 'cobertura' version '2.5.0'
}

cobertura {
    coverageFormats = ['html', 'xml']
    coverageIgnoreTrivial = true
    coverageExcludes = ['.*Test.*', '.*Mock.*']
    coverageCheckBranchRate = 70
    coverageCheckLineRate = 80
    coverageCheckHaltOnFailure = true
}

test {
    useJUnitPlatform()
}
```

```bash
# カバレッジ計測
./gradlew clean test cobertura

# レポート生成
./gradlew coberturaReport

# カバレッジチェック
./gradlew coberturaCheck

# レポート閲覧
open build/reports/cobertura/index.html
```

### Ant統合

```xml
<!-- build.xml -->
<project name="myproject" default="coverage-report">
  <property name="cobertura.dir" value="${basedir}/lib/cobertura" />

  <path id="cobertura.classpath">
    <fileset dir="${cobertura.dir}">
      <include name="cobertura-*.jar" />
      <include name="lib/**/*.jar" />
    </fileset>
  </path>

  <taskdef classpathref="cobertura.classpath" resource="tasks.properties" />

  <target name="init">
    <mkdir dir="${build.dir}" />
    <mkdir dir="${instrumented.dir}" />
    <mkdir dir="${reports.dir}" />
  </target>

  <target name="compile" depends="init">
    <javac srcdir="${src.dir}" destdir="${build.dir}" />
  </target>

  <target name="instrument" depends="compile">
    <cobertura-instrument todir="${instrumented.dir}">
      <fileset dir="${build.dir}">
        <include name="**/*.class" />
        <exclude name="**/*Test*.class" />
      </fileset>
    </cobertura-instrument>
  </target>

  <target name="test" depends="instrument">
    <junit fork="yes">
      <classpath location="${instrumented.dir}" />
      <classpath location="${build.dir}" />
      <classpath refid="cobertura.classpath" />

      <formatter type="xml" />

      <batchtest todir="${reports.dir}">
        <fileset dir="${test.dir}">
          <include name="**/*Test.java" />
        </fileset>
      </batchtest>
    </junit>
  </target>

  <target name="coverage-report" depends="test">
    <cobertura-report format="html" destdir="${reports.dir}/cobertura">
      <fileset dir="${src.dir}">
        <include name="**/*.java" />
      </fileset>
    </cobertura-report>
  </target>

  <target name="coverage-check">
    <cobertura-check branchrate="70" linerate="80" />
  </target>
</project>
```

### コマンドライン実行

```bash
# Coberturaダウンロード
wget https://github.com/cobertura/cobertura/releases/download/cobertura-2.1.1/cobertura-2.1.1-bin.tar.gz
tar -xzf cobertura-2.1.1-bin.tar.gz

# クラスファイルをインストルメント
java -cp cobertura-2.1.1.jar net.sourceforge.cobertura.instrument.Main \
  --destination instrumented-classes \
  classes/*.class

# テスト実行（インストルメント版使用）
java -cp instrumented-classes:cobertura-2.1.1.jar:junit.jar \
  org.junit.runner.JUnitCore com.example.MyTest

# HTMLレポート生成
java -cp cobertura-2.1.1.jar net.sourceforge.cobertura.reporting.Main \
  --format html \
  --destination coverage-report \
  --datafile cobertura.ser \
  src/**/*.java

# XMLレポート生成
java -cp cobertura-2.1.1.jar net.sourceforge.cobertura.reporting.Main \
  --format xml \
  --destination coverage-report \
  --datafile cobertura.ser \
  src/**/*.java
```

### カバレッジ除外設定

```xml
<!-- pom.xml -->
<configuration>
  <instrumentation>
    <ignores>
      <ignore>com.example.generated.*</ignore>
    </ignores>
    <excludes>
      <exclude>**/*Test.class</exclude>
      <exclude>**/*Mock.class</exclude>
      <exclude>**/dto/*.class</exclude>
    </excludes>
  </instrumentation>
</configuration>
```

```groovy
// build.gradle
cobertura {
    coverageExcludes = [
        '.*Test.*',
        '.*Mock.*',
        '.*\\.dto\\..*'
    ]
    coverageIgnores = [
        'com.example.generated.*'
    ]
}
```

### カバレッジ閾値設定

```xml
<!-- pom.xml -->
<configuration>
  <check>
    <branchRate>70</branchRate>
    <lineRate>80</lineRate>
    <haltOnFailure>true</haltOnFailure>
    <totalBranchRate>70</totalBranchRate>
    <totalLineRate>80</totalLineRate>
    <packageLineRate>75</packageLineRate>
    <packageBranchRate>65</packageBranchRate>
    <regexes>
      <regex>
        <pattern>com.example.critical.*</pattern>
        <branchRate>90</branchRate>
        <lineRate>95</lineRate>
      </regex>
    </regexes>
  </check>
</configuration>
```

### Jenkins統合

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Test & Coverage') {
            steps {
                sh 'mvn test cobertura:cobertura'
            }
        }

        stage('Publish Coverage') {
            steps {
                // Cobertura Plugin
                cobertura coberturaReportFile: 'target/site/cobertura/coverage.xml',
                         failNoReports: true,
                         onlyStable: false,
                         sourceEncoding: 'UTF-8',
                         zoomCoverageChart: false
            }
        }
    }
}
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
test:
  stage: test
  script:
    - mvn clean test cobertura:cobertura
  artifacts:
    reports:
      cobertura: target/site/cobertura/coverage.xml
    paths:
      - target/site/cobertura/
  coverage: '/Total.*?([0-9]{1,3})%/'
```

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run tests with coverage
        run: mvn clean test cobertura:cobertura

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./target/site/cobertura/coverage.xml
          flags: unittests
          name: codecov-umbrella

      - name: Publish coverage report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: target/site/cobertura/
```

### SonarQube統合

```xml
<!-- pom.xml -->
<properties>
  <sonar.java.coveragePlugin>cobertura</sonar.java.coveragePlugin>
  <sonar.cobertura.reportPath>target/site/cobertura/coverage.xml</sonar.cobertura.reportPath>
</properties>
```

```bash
# カバレッジ計測
mvn clean test cobertura:cobertura

# SonarQubeにアップロード
mvn sonar:sonar \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | ユニットテスト検証 | テストの網羅性確認 |
| **テスト** | カバレッジ測定 | コードカバレッジ計測 |
| **テスト** | 品質ゲート | 閾値チェック |
| **CI/CD** | 継続的品質監視 | ビルドパイプラインでカバレッジ確認 |

## メリット

- **網羅性可視化**: テスト未実行コードの特定
- **HTMLレポート**: 視覚的なカバレッジ確認
- **ビルドツール統合**: Maven、Gradle対応
- **CI/CD統合**: Jenkins、GitLabプラグイン
- **閾値チェック**: ビルド失敗機能
- **無料**: オープンソース

## デメリット

- **メンテナンス停滞**: 2015年以降更新少
- **Java限定**: 他言語非対応
- **パフォーマンス**: 大規模プロジェクトで遅延
- **モダンツール**: JaCoCo推奨
- **Java 9+制約**: 新バージョンで問題
- **代替推奨**: JaCoCo、Clover

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Cobertura** | HTMLレポート、Maven統合 | 無料 | レガシープロジェクト |
| **JaCoCo** | モダン、Java 17対応、軽量 | 無料 | 新規Java開発 |
| **Clover** | 高機能、詳細分析 | 有料 | エンタープライズ |
| **Emma** | シンプル、軽量（非推奨） | 無料 | 古いプロジェクト |

## ベストプラクティス

### 1. 閾値設定

```xml
<!-- 80%以上のカバレッジを強制 -->
<check>
  <branchRate>70</branchRate>
  <lineRate>80</lineRate>
  <haltOnFailure>true</haltOnFailure>
</check>
```

### 2. 除外パターン設定

```xml
<!-- 自動生成・DTOを除外 -->
<excludes>
  <exclude>**/*Test.class</exclude>
  <exclude>**/generated/**/*.class</exclude>
  <exclude>**/dto/*.class</exclude>
</excludes>
```

### 3. CI/CDでの活用

```groovy
// ビルド失敗させる
cobertura {
  coverageCheckHaltOnFailure = true
}
```

### 4. JaCoCoへの移行検討

```xml
<!-- JaCoCo推奨（pom.xml） -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.10</version>
  <executions>
    <execution>
      <goals>
        <goal>prepare-agent</goal>
        <goal>report</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

## 公式リソース

- **公式サイト**: https://cobertura.github.io/cobertura/
- **GitHub**: https://github.com/cobertura/cobertura
- **Maven Plugin**: https://www.mojohaus.org/cobertura-maven-plugin/
- **Wiki**: https://github.com/cobertura/cobertura/wiki

## まとめ

Coberturaは、Javaプログラムのコードカバレッジ測定ツールです。Maven・Gradle統合、HTMLレポート生成により、テストの網羅性を可視化します。ただし、メンテナンスが停滞しており、新規プロジェクトではより活発に開発されているJaCoCoの使用が推奨されています。

---

**最終更新**: 2025-12-10
**メンテナンス状況**: 停滞（2015年以降更新少）
**推奨代替ツール**: JaCoCo
