# Visual Paradigm

## 概要

Visual Paradigmは、香港のVisual Paradigm社が開発した包括的なUMLモデリングツールです。UML、BPMN、ERD、DFD、ArchiMate等の多様な記法をサポートし、ソフトウェア設計からビジネスプロセスモデリング、データベース設計まで幅広く対応します。Enterprise Architectと同等の機能を持ちながら、より直感的なUIとリーズナブルな価格設定が特徴です。

## 主な機能

### 1. 多様なダイアグラム対応
- **UML 2.5**: 全14種類のUMLダイアグラム
- **BPMN 2.0**: ビジネスプロセスモデリング
- **ERD**: エンティティ関係図
- **DFD**: データフロー図
- **ArchiMate**: エンタープライズアーキテクチャ
- **SysML**: システムエンジニアリング

### 2. コード生成・リバースエンジニアリング
- **対応言語**: Java、C++、C#、Python、PHP、VB.NET等
- **Round-trip Engineering**: モデル↔コードの双方向同期
- **既存コード分析**: クラス図自動生成

### 3. チームコラボレーション
- TeamworkServer: 共有リポジトリ
- バージョン管理統合（Git、SVN）
- モデルのマージ・差分比較
- コメント・レビュー機能

### 4. ドキュメント生成
- HTML、PDF、Word形式で自動生成
- カスタマイズ可能なテンプレート
- 設計書自動作成

### 5. 要件管理
- 要件の定義・追跡
- ユースケースとの関連付け
- トレーサビリティマトリクス

### 6. アジャイル開発支援
- ユーザーストーリーマップ
- スクラムボード
- スプリントプランニング

## 利用方法

### クラス図作成

```
1. File → New Diagram → Class Diagram

2. ツールパレットから Class をドラッグ

3. クラス名をダブルクリックして編集

4. 属性追加:
   - クラス内で右クリック → Add → Attribute
   - 例: - name: String

5. 操作追加:
   - 右クリック → Add → Operation
   - 例: + getName(): String

6. 関連追加:
   - ツールパレットから Association
   - クラス間をドラッグ&ドロップ
   - 多重度を設定（1, *, 0..1 等）

7. コード生成:
   - Tools → Code → Generate Code
   - 言語選択（Java/C#等）
   - 出力先ディレクトリ指定
```

### シーケンス図作成

```
1. File → New Diagram → Sequence Diagram

2. Lifeline追加:
   - ツールパレットから Lifeline
   - アクター、システムコンポーネント等を配置

3. メッセージ追加:
   - ツールパレットから Message
   - Lifeline間をドラッグ
   - メッセージ名を入力

4. Combined Fragment:
   - alt（条件分岐）、loop（繰り返し）を追加
   - 複雑なインタラクションを表現

5. Activation Box:
   - メッセージをドラッグして自動生成
   - 処理の実行期間を表現
```

### データベース設計（ERD）

```
1. File → New Diagram → Entity Relationship Diagram

2. Entity追加:
   - ツールパレットから Entity
   - エンティティ名入力

3. Attribute追加:
   - Entityをダブルクリック
   - Columns タブで追加
   - Name, Data Type, PK, NN, UQ設定

4. Relationship追加:
   - ツールパレットから Relationship
   - Entity間をドラッグ
   - カーディナリティ設定（1:1, 1:N, N:M）

5. DDL生成:
   - Tools → Database → Generate Database
   - データベース選択（MySQL/PostgreSQL/Oracle等）
   - CREATE文を生成
```

## エディション・料金

| エディション | 価格（目安） | 主な機能 |
|-------------|--------------|----------|
| **Modeler Edition** | $99/永続 | UMLモデリング、コード生成 |
| **Standard Edition** | $349/永続 | + データベース設計、BPMN |
| **Professional Edition** | $789/永続 | + チーム協業、プロジェクト管理 |
| **Enterprise Edition** | $1,899/永続 | 全機能、TeamworkServer |

※サブスクリプションプランもあり（月額/年額）

## メリット

### ✅ 主な利点

1. **Enterprise Architect代替**: 同等機能でより使いやすい
2. **モダンUI**: 直感的で美しいインターフェース
3. **多様な記法**: UML、BPMN、ERD、ArchiMate等
4. **リーズナブル**: Enterprise Architectより低価格
5. **クロスプラットフォーム**: Windows、Mac、Linux対応
6. **コード生成**: 10以上の言語に対応
7. **チーム協業**: 共有リポジトリ、バージョン管理
8. **アジャイル対応**: ユーザーストーリー、スクラムボード
9. **豊富なテンプレート**: 業界別テンプレート多数
10. **継続的更新**: 定期的な機能追加・改善

## デメリット

### ❌ 制約・課題

1. **学習曲線**: 多機能なため習得に時間がかかる
2. **動作やや重い**: 大規模プロジェクトでは遅延
3. **日本語ドキュメント**: 英語中心、日本語情報少ない
4. **TeamworkServer**: セットアップが複雑
5. **Enterprise Architect比**: 一部高度機能は劣る
6. **ライセンス管理**: 複数エディションで混乱しやすい
7. **エクスポート品質**: 一部形式でレイアウト崩れ
8. **プラグイン**: Enterprise Architectほど豊富ではない

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Enterprise Architect** | 老舗、機能豊富 | Visual Paradigmよりエンタープライズ向け |
| **PlantUML** | テキストベース、無料 | Visual Paradigmより軽量だがGUI不要 |
| **astah*** | 日本製、日本語完全対応 | Visual Paradigmより機能やや少ない |
| **StarUML** | モダンUI、低価格 | Visual Paradigmより機能限定的 |
| **Lucidchart** | クラウドベース、協業重視 | UML特化ではない |

## 公式リンク

- **公式サイト**: [https://www.visual-paradigm.com/](https://www.visual-paradigm.com/)
- **ドキュメント**: [https://www.visual-paradigm.com/support/documents/](https://www.visual-paradigm.com/support/documents/)
- **チュートリアル**: [https://www.visual-paradigm.com/tutorials/](https://www.visual-paradigm.com/tutorials/)
- **価格**: [https://www.visual-paradigm.com/purchase/](https://www.visual-paradigm.com/purchase/)
- **無料体験**: [https://www.visual-paradigm.com/download/](https://www.visual-paradigm.com/download/)

## 関連ドキュメント

- [UMLツール一覧](../UMLツール/)
- [Enterprise Architect](./Enterprise_Architect.md)
- [PlantUML](./PlantUML.md)
- [astah*](./astah.md)
- [UML設計ベストプラクティス](../../best-practices/uml-design.md)

---

**カテゴリ**: UMLツール  
**対象工程**: 要件定義、基本設計、詳細設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
