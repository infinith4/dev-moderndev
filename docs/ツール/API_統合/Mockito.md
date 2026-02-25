# Mockito

## 概要

Mockito は、Java/Kotlin 向けのモックフレームワークである。依存コンポーネントをモック化し、ユニットテストでクラス単位の振る舞い検証を行いやすくする。JUnit と組み合わせたテスト自動化で広く利用される。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（MIT License） |
| 商用利用 | ライセンス上利用可能（組織ポリシー確認は必要） |

## 主な特徴

| 項目 | 内容 |
|------|------|
| シンプル API | `mock`、`when`、`verify` を中心に学習しやすい |
| JUnit 連携 | JUnit 5 拡張で初期化と注入を簡略化 |
| アノテーション対応 | `@Mock`、`@Spy`、`@InjectMocks` を利用可能 |
| BDD 記法 | given/when/then スタイルの記述に対応 |
| 引数検証 | `ArgumentCaptor` で引数内容を確認可能 |

## 主な機能

### モック作成機能

| 機能 | 説明 |
|------|------|
| `mock()` | 任意クラス・インターフェースのモック作成 |
| `@Mock` | アノテーションでモックを定義 |
| `@Spy` | 実オブジェクトの一部だけ差し替え |
| `@InjectMocks` | テスト対象へモックを注入 |

### スタブ・振る舞い定義機能

| 機能 | 説明 |
|------|------|
| `when().thenReturn()` | 戻り値の定義 |
| `when().thenThrow()` | 例外発生シナリオの定義 |
| `doReturn()/doThrow()` | void/spy 対象の制御 |
| `Answer` | 動的な返却内容を定義 |

### 検証機能

| 機能 | 説明 |
|------|------|
| `verify()` | 呼び出し有無を検証 |
| `times()/never()` | 呼び出し回数の検証 |
| `ArgumentCaptor` | 呼び出し引数を検証 |
| `InOrder` | 呼び出し順序を検証 |

## インストールとセットアップ

公式URL:
- [Mockito 公式サイト](https://site.mockito.org/)
- [GitHub](https://github.com/mockito/mockito)
- [JavaDoc](https://javadoc.io/doc/org.mockito/mockito-core)

セットアップの要点:
1. `mockito-core` と `mockito-junit-jupiter` をテスト依存に追加する。
2. JUnit 5 で `MockitoExtension` を有効化する。
3. モック対象とテスト対象の責務境界を先に決める。
4. テストデータ準備と検証方針（戻り値優先/呼び出し検証）を統一する。

## 基本的な使い方

1. 依存コンポーネントを `@Mock` で定義する。
2. テスト対象を `@InjectMocks` または手動で生成する。
3. `when(...).thenReturn(...)` で事前条件を設定する。
4. 対象メソッドを実行し、戻り値や状態を確認する。
5. `verify(...)` で副作用や依存呼び出しを検証する。

最小実行例:
- スタブ定義: `when(repo.findById(1L)).thenReturn(user)`
- 検証: `verify(repo, times(1)).findById(1L)`

## メリット

- 依存切り離しによりユニットテストの再現性を高めやすい。
- API が明快で、テストコードの可読性を維持しやすい。
- JUnit 連携で CI 実行まで接続しやすい。

## デメリット

- モック過多になると実装依存の脆いテストになりやすい。
- `verify` 多用で振る舞い変更に弱くなることがある。
- 統合レベルの不整合は別途テストが必要。

## 他ツールとの比較

| ツール | 主な対象 | 特徴 |
|------|------|------|
| Mockito | Java/Kotlin ユニットテスト | 依存モックと振る舞い検証に特化 |
| WireMock | HTTP API モック | 外部 API のスタブサーバー構築に強い |
| MockServer | API 契約テスト | 検証 API と OpenAPI 連携が強い |
| JMockit | Java モック | 高機能だが導入難易度が比較的高い |

## ベストプラクティス

### 1. モック範囲を最小化

- テスト対象の直接依存だけをモック化する。
- DTO や値オブジェクトは実体を使う。

### 2. 検証方針を統一

- 戻り値・状態検証を優先し、`verify` は必要最小限にする。
- 回数検証は業務要件に直結する箇所だけで使う。

### 3. テスト構造を標準化

- given/when/then でテストを構造化する。
- テスト名で期待振る舞いを明示する。

## 公式ドキュメント

- 公式サイト: https://site.mockito.org/
- GitHub: https://github.com/mockito/mockito
- JavaDoc: https://javadoc.io/doc/org.mockito/mockito-core
- Wiki: https://github.com/mockito/mockito/wiki

## まとめ

1. ** 依存分離 ** : Java/Kotlin のユニットテストで依存分離を進めやすい。
2. ** 簡潔記述 ** : シンプルな API で、継続保守しやすいテストを作りやすい。
3. ** 回帰検知 ** : CI 実行に組み込むことで、変更時の回帰検知を早めやすい。
