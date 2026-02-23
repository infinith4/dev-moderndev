# OWASP Top 10

## 概要

OWASP Top 10は、OWASPが発行するWebアプリケーションにおける最も重大なセキュリティリスクのランキングです。数百の組織からのデータと業界調査に基づき、約3〜4年ごとに更新されます。最新版（2021年版）では、アクセス制御の不備、暗号化の失敗、インジェクション等の10カテゴリを定義し、各リスクの概要、脆弱性の例、対策方法を解説しています。セキュリティ教育、設計レビュー、テスト計画の観点定義に広く活用されます。

## OWASP Top 10 2021

| 順位 | カテゴリ | 概要 |
|------|----------|------|
| **A01** | Broken Access Control | アクセス制御の不備（権限昇格、IDOR等） |
| **A02** | Cryptographic Failures | 暗号化の失敗（平文保存、弱い暗号等） |
| **A03** | Injection | インジェクション（SQL、NoSQL、OS、LDAP等） |
| **A04** | Insecure Design | セキュアでない設計（脅威モデリング不足等） |
| **A05** | Security Misconfiguration | セキュリティ設定ミス（デフォルト設定、不要機能有効等） |
| **A06** | Vulnerable and Outdated Components | 脆弱・古いコンポーネントの使用 |
| **A07** | Identification and Authentication Failures | 認証の不備（弱いパスワード、セッション管理等） |
| **A08** | Software and Data Integrity Failures | ソフトウェアとデータの整合性の不備（CI/CDパイプライン攻撃等） |
| **A09** | Security Logging and Monitoring Failures | セキュリティログと監視の不備 |
| **A10** | Server-Side Request Forgery (SSRF) | サーバーサイドリクエストフォージェリ |

## 各リスクの詳細と対策

### A01: Broken Access Control（アクセス制御の不備）

```
脆弱性例:
- URLパラメータ変更で他ユーザーのデータにアクセス（IDOR）
- 管理者APIに一般ユーザーがアクセス可能
- JWTトークンの改ざんによる権限昇格

対策:
- デフォルトで全アクセスを拒否（deny by default）
- サーバーサイドでアクセス制御を実装
- CORSの適切な設定
- ディレクトリリスティングの無効化
- レート制限の実装
```

### A03: Injection（インジェクション）

```
脆弱性例:
- SQLインジェクション: SELECT * FROM users WHERE id = '1' OR '1'='1'
- XSS: <script>document.cookie</script>
- OSコマンドインジェクション: ; rm -rf /

対策:
- パラメータ化クエリ（Prepared Statement）の使用
- ORM（Object-Relational Mapping）の使用
- 入力値のサーバーサイドバリデーション
- 出力のコンテキスト別エスケープ（HTML/URL/JS/CSS）
- Content Security Policy（CSP）ヘッダーの設定
```

### A06: Vulnerable and Outdated Components

```
脆弱性例:
- 既知のCVEが存在するライブラリの使用
- サポート終了（EOL）のフレームワーク使用
- パッチ未適用のOSやミドルウェア

対策:
- OWASP Dependency-Check / Trivyによる自動スキャン
- Dependabot / Renovateによる依存関係の自動更新
- SBOMの生成と管理
- 定期的なパッチ適用プロセスの確立
```

## 活用方法

### セキュリティ教育

```
1. 開発者向けセキュリティトレーニングの基本教材として使用
2. 各カテゴリの脆弱性デモ環境（OWASP WebGoat、Juice Shop）で実習
3. コードレビューのセキュリティ観点チェックリストとして活用
4. 新規メンバーのオンボーディング教材に組み込み
```

### 設計レビュー

```
1. 脅威モデリング時にOWASP Top 10の各カテゴリを確認
2. アーキテクチャ設計書にセキュリティ対策のマッピングを記載
3. API設計時にA01（アクセス制御）、A03（インジェクション）を重点チェック
4. 認証・認可フロー設計時にA07を参照
```

### テスト計画

```
1. セキュリティテスト計画にOWASP Top 10の各カテゴリを観点として組み込み
2. OWASP ZAPやBurp SuiteでA03（Injection）、A05（Misconfiguration）を自動テスト
3. ペネトレーションテストのスコープにA01（Access Control）を必須項目として含める
4. CI/CDパイプラインにSAST/DASTを組み込みA06（Vulnerable Components）を継続チェック
```

### 実習環境

| ツール | 用途 |
|--------|------|
| **OWASP WebGoat** | Webセキュリティの学習用脆弱アプリ |
| **OWASP Juice Shop** | モダンなWebアプリの脆弱性実習環境 |
| **DVWA** | PHP製の脆弱性実習環境 |
| **HackTheBox** | CTF形式のセキュリティ学習プラットフォーム |

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **OWASP Top 10** | 無料 | CC BY-SA 4.0 License |

## メリット

1. **簡潔**: 10項目に絞ることで最重要リスクを効率的に把握可能
2. **データ駆動**: 実際のインシデントデータに基づいたランキング
3. **国際認知**: セキュリティ業界のデファクト参照標準
4. **教育効果**: 開発者のセキュリティ意識向上に最適な教材
5. **実習環境**: WebGoat/Juice Shopで実践的に学習可能
6. **ツール連携**: SAST/DASTツールの検出ルールがTop 10に対応

## デメリット

1. **網羅性不足**: 10項目のみのため、すべてのセキュリティリスクをカバーしない
2. **更新間隔**: 3〜4年ごとの更新のため、新しい脅威の反映が遅れる
3. **抽象的**: 各カテゴリが広範で、具体的な実装ガイダンスはASVSが必要
4. **ランキングの議論**: 順位付けの方法論に対する業界内の議論がある
5. **Webアプリ限定**: モバイルアプリ、API、IoT等は別のTop 10が存在

## 代替・補完リソース

| ツール | 特徴 | 比較 |
|--------|------|------|
| **OWASP ASVS** | セキュリティ検証標準 | Top 10より詳細、286項目以上の検証要件 |
| **OWASP API Security Top 10** | API特化 | REST/GraphQL APIのセキュリティリスク |
| **OWASP Mobile Top 10** | モバイル特化 | iOS/Androidアプリのセキュリティリスク |
| **CWE/SANS Top 25** | ソフトウェア脆弱性 | Top 10よりコード寄りの脆弱性リスト |

## 公式リンク

- **公式サイト**: [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
- **OWASP Top 10 2021**: [https://owasp.org/Top10/](https://owasp.org/Top10/)
- **GitHub**: [https://github.com/OWASP/Top10](https://github.com/OWASP/Top10)
- **日本語版**: [https://owasp.org/Top10/ja/](https://owasp.org/Top10/ja/)
- **WebGoat**: [https://owasp.org/www-project-webgoat/](https://owasp.org/www-project-webgoat/)
- **Juice Shop**: [https://owasp.org/www-project-juice-shop/](https://owasp.org/www-project-juice-shop/)

## 関連ドキュメント

- [OWASP ASVS](./OWASP_ASVS.md)
- [OWASP Dependency-Check](../セキュリティ/OWASP_Dependency_Check.md)
- [Trivy](../セキュリティ/Trivy.md)

---

**カテゴリ**: 標準ガイドライン
**対象工程**: 要件定義・設計・実装・テスト
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
