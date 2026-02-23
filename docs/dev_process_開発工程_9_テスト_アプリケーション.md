# 開発工程_9_テスト（アプリケーション）

- [1. 概要](#1-概要)
  - [1.2. 共通](#12-共通)
- [2. 単体テスト](#2-単体テスト)
  - [2.1 Java](#21-java)
  - [2.2 C#](#22-c)
  - [2.3 Python](#23-python)
  - [2.4 TypeScript](#24-typescript)
  - [2.5 Go](#25-go)
- [3. 結合・APIテスト](#3-結合apiテスト)
- [4. システム・E2Eテスト](#4-システムe2eテスト)
- [5. 非機能テスト](#5-非機能テスト)
- [6. テスト管理・不具合管理](#6-テスト管理不具合管理)
- [7. 回帰テスト・自動実行](#7-回帰テスト自動実行)
- [8. 参考資料](#8-参考資料)

## 1. 概要

テスト（アプリケーション）のタスクと推奨ツール、有用なドキュメントを記載した。

---

### 1.2. 共通

**対応項目**
- テスト計画、テスト設計、テスト実施
- テスト自動化（単体/結合/E2E）
- 不具合記録、トリアージ、再テスト
- テスト結果の可視化と品質判定

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [JSTQB Foundation Level シラバス](https://jstqb.jp/syllabus.html) | テストプロセス、設計技法、品質観点の共通化 |
| [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) | セキュリティテスト観点の整理 |
| [Google Testing Blog](https://testing.googleblog.com/) | 自動テスト運用・改善の実践知見 |

---

## 2. 単体テスト
**成果物**
- 単体テスト仕様書
- テストコード
- カバレッジレポート

### 2.1 Java

| ツール名 | 用途 |
|---------|------|
| [JUnit 5](https://junit.org/junit5/) | Javaの単体テスト実装 |
| [Mockito](https://site.mockito.org/) | Javaのモック作成、依存切り離しテスト |

### 2.2 C#

| ツール名 | 用途 |
|---------|------|
| [xUnit.net](https://xunit.net/) | C#/.NETの単体テスト実装 |
| [Moq](https://github.com/devlooped/moq) | C#のモック作成、依存切り離しテスト |

### 2.3 Python

| ツール名 | 用途 |
|---------|------|
| [pytest](https://docs.pytest.org/) | Pythonの単体テスト実装 |
| [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) | Python標準のモック作成 |

### 2.4 TypeScript

| ツール名 | 用途 |
|---------|------|
| [Jest](https://jestjs.io/) | TypeScriptの単体テスト実装 |
| [ts-jest](https://kulshekhar.github.io/ts-jest/) | TypeScript向けJest実行設定 |

### 2.5 Go

| ツール名 | 用途 |
|---------|------|
| [Go testing](https://pkg.go.dev/testing) | Goの単体テスト実装 |
| [GoMock](https://github.com/uber-go/mock) | Goのモック生成、依存切り離しテスト |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/) | JUnitテスト設計と実装 |
| [pytest Documentation](https://docs.pytest.org/en/stable/) | pytestフィクスチャ、実行方法 |
| [Jest Docs](https://jestjs.io/docs/getting-started) | Jest導入とテスト実装 |
| [xUnit.net Documentation](https://xunit.net/docs/getting-started/v2/getting-started) | xUnit導入とテスト実装 |
| [Go testing package](https://pkg.go.dev/testing) | Go標準テスト実装 |

---

## 3. 結合・APIテスト
**成果物**
- 結合テスト仕様書
- APIテストケース
- テスト実行結果レポート

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Postman](https://www.postman.com/) | APIリクエスト作成・手動/自動テスト | 無料枠あり |
| [Newman](https://github.com/postmanlabs/newman) | PostmanコレクションのCLI実行 | 無料 |
| [REST Assured](https://rest-assured.io/) | JavaでのAPI自動テスト実装 | 無料 |
| [WireMock](https://wiremock.org/) | APIモックサーバによる結合テスト | 無料 |
| [MockServer](https://www.mock-server.com/) | 外部APIモック/期待値検証 | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Postman Learning Center](https://learning.postman.com/) | APIテストケース管理と自動化 |
| [REST Assured Documentation](https://github.com/rest-assured/rest-assured/wiki/Usage) | REST Assured実装パターン |
| [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | API仕様ベースのテスト設計 |

---

## 4. システム・E2Eテスト
**成果物**
- E2Eテストシナリオ
- 自動テストスクリプト
- テスト証跡（動画/スクリーンショット/ログ）

| ツール名 | 用途 |
|---------|------|
| [Playwright](https://playwright.dev/) | クロスブラウザE2Eテスト |
| [Selenium](https://www.selenium.dev/) | ブラウザ自動操作によるE2Eテスト |
| [Appium](https://appium.io/) | モバイルアプリE2Eテスト |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Playwright Docs](https://playwright.dev/docs/intro) | Playwright導入と運用 |
| [Selenium Documentation](https://www.selenium.dev/documentation/) | Selenium実装ガイド |

---

## 5. 非機能テスト
**成果物**
- 性能/負荷テスト仕様書
- セキュリティテスト結果
- ボトルネック分析レポート

| ツール名 | 用途 |
|---------|------|
| [Apache JMeter](https://jmeter.apache.org/) | 負荷・性能テスト実行 |
| [k6](https://k6.io/) | スクリプトベース負荷テスト |
| [Locust](https://locust.io/) | Pythonベース分散負荷テスト |
| [OWASP ZAP](https://www.zaproxy.org/) | Webアプリ脆弱性テスト |
| [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) | 依存ライブラリ脆弱性検査 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html) | JMeterシナリオ作成と結果分析 |
| [k6 Docs](https://grafana.com/docs/k6/latest/) | k6での負荷テスト実装 |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | セキュリティテスト観点の優先度付け |

---

## 6. テスト管理・不具合管理
**成果物**
- テスト進捗レポート
- 不具合管理票
- テストサマリ報告書

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [Xray](https://www.getxray.app/) / [Zephyr](https://smartbear.com/test-management/zephyr/) | Jira連携のテスト管理、テスト実行管理 | 有料 |
| [TestRail](https://www.testrail.com/) | テストケース管理、テスト進捗・品質レポート | 有料 |
| [Allure Report](https://allurereport.org/) | テスト結果可視化レポート | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [Allure Framework Documentation](https://allurereport.org/docs/) | テスト結果の可視化設定 |
| [ISO/IEC/IEEE 29119 overview](https://www.softwaretestingstandards.org/iso-29119/) | テストドキュメント観点の整理 |

---

## 7. 回帰テスト・自動実行
**成果物**
- 回帰テスト実行計画
- 自動実行ジョブ定義
- 品質ゲート判定結果

| ツール名 | 用途 | 料金 |
|---------|------|------|
| [GitHub Actions](https://github.com/features/actions) | プルリク/マージ時の自動テスト実行 | 無料枠あり |
| [GitLab CI/CD](https://about.gitlab.com/solutions/continuous-integration/) | パイプラインでの回帰テスト自動化 | 無料枠あり |
| [Reviewdog](https://reviewdog.github.io/) | テスト/静的解析結果のPRフィードバック | 無料 |

**有用なドキュメント**

| 資料名 | 用途 |
|-------|------|
| [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) | テスト自動実行ジョブ定義 |
| [GitLab CI/CD YAML reference](https://docs.gitlab.com/ee/ci/yaml/) | テストパイプライン定義 |
| [reviewdog Documentation](https://reviewdog.github.io/docs/) | PRコメント連携の設定 |

---

## 8. 参考資料
- IPA 共通フレーム2013（SLCP-JCF: Software Life Cycle Process - Japan Common Frame）
- ISO/IEC/IEEE 12207:2017 / JIS X 0160:2012
