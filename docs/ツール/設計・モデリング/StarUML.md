# StarUML

## 概要

StarUMLは、軽量で高速なUMLモデリングツールです。UML 2.0の主要なダイアグラムタイプをサポートし、シンプルで洗練されたUIにより、開発者が素早くUML図を作成できます。オープンソース版から進化した商用ツールで、クロスプラットフォーム対応、拡張機能、コード生成・リバースエンジニアリング機能を提供します。

## 主な機能

### 1. UMLダイアグラム対応
- **クラス図**: クラス構造、継承、関連
- **ユースケース図**: アクター、ユースケース
- **シーケンス図**: オブジェクト間の相互作用
- **ステートマシン図**: 状態遷移
- **アクティビティ図**: ワークフロー
- **コンポーネント図**: コンポーネント構造
- **配置図**: 物理配置
- **パッケージ図**: パッケージ構造

### 2. コード生成
- **Java**: クラス図からJavaコード生成
- **C#**: .NETコード生成
- **C++**: C++コード生成
- **Python**: Pythonコード生成
- **JavaScript**: JSコード生成

### 3. リバースエンジニアリング
- 既存コードからUML図生成
- Javaソースコード解析
- C#ソースコード解析

### 4. 拡張機能
- エクステンションマネージャー
- カスタムステレオタイプ
- プロファイル定義
- テンプレート作成

### 5. エクスポート
- PNG、JPEG、SVG画像出力
- PDF出力
- HTMLドキュメント生成
- MDJファイル（StarUML形式）

### 6. クロスプラットフォーム
- Windows
- macOS
- Linux（Ubuntu、Debian等）

## 利用方法

### インストール

```bash
# 公式サイトからダウンロード
# https://staruml.io/download

# Windows: インストーラー実行
StarUML-Setup-x.x.x.exe

# macOS: DMGファイルマウント
StarUML-x.x.x.dmg

# Linux: DebパッケージまたはAppImage
sudo dpkg -i StarUML_x.x.x_amd64.deb
```

### ライセンス登録

```
1. StarUML起動
2. Help → Enter License Key
3. ライセンスキー入力（購入後に送付）
```

### 基本的なクラス図作成

```
1. 新規プロジェクト作成
   File → New → From Template → UML Minimal

2. クラス追加
   Toolbox → Class → キャンバスにドラッグ
   クラス名をダブルクリックして編集

3. 属性追加
   クラスを右クリック → Add → Attribute
   名前、型、可視性を設定

4. メソッド追加
   クラスを右クリック → Add → Operation
   名前、戻り値、パラメータを設定

5. 関連追加
   Toolbox → Association/Generalization/Dependency
   クラス間をドラッグ
```

### コード生成例

```
1. Javaコード生成設定
   Tools → Preferences → Code Generation → Java
   出力パス設定: ./src/main/java

2. コード生成実行
   Tools → Java → Generate Code
   対象パッケージ選択

3. 生成されたコード例
   // User.java
   public class User {
       private String name;
       private String email;
       
       public String getName() {
           return name;
       }
       
       public void setName(String name) {
           this.name = name;
       }
   }
```

### リバースエンジニアリング

```
1. Javaコードからクラス図生成
   Tools → Java → Reverse Code
   ソースディレクトリ選択

2. 生成されたクラス図を確認
   Model Explorer → Reversed Packages
```

### エクステンション追加

```
1. エクステンションマネージャー起動
   Tools → Extension Manager

2. エクステンション検索・インストール
   - ERD (Entity-Relationship Diagram)
   - DDL Generator
   - Markdown Export

3. エクステンション使用
   インストール後、Toolsメニューに追加される
```

### 図のエクスポート

```
1. PNG/SVG エクスポート
   File → Export Diagram As → PNG/SVG
   解像度、サイズ設定

2. PDFエクスポート
   File → Export Diagram As → PDF
   全ダイアグラムまたは選択ダイアグラム

3. HTMLドキュメント生成
   File → Export → HTML Docs
   プロジェクト全体のドキュメント化
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **StarUML Trial** | 🟡 評価版 | 15日間無料試用、全機能利用可能 |
| **StarUML License** | 💰 $89 USD（買い切り） | 永続ライセンス、1年間アップデート無料 |
| **StarUML Subscription** | 💰 $29 USD/年 | サブスクリプション、継続アップデート |

### ライセンス詳細
- **Personal**: 個人利用
- **Commercial**: 商用利用（企業・組織）
- **Academic**: 教育機関（割引あり）

## メリット

### ✅ 主な利点

1. **軽量・高速**: 起動・動作が速い
2. **シンプルUI**: 直感的で習得容易
3. **クロスプラットフォーム**: Windows、Mac、Linux対応
4. **買い切りライセンス**: サブスク不要の永続ライセンス
5. **コード生成**: Java、C#、Python等に対応
6. **リバースエンジニアリング**: 既存コードからUML生成
7. **拡張機能**: エクステンションで機能追加
8. **SVG/PDFエクスポート**: 高品質な図出力
9. **手頃な価格**: Enterprise Architectより安価
10. **モダンUI**: Electron製のモダンなインターフェース

## デメリット

### ❌ 制約・課題

1. **機能制限**: Enterprise Architectほど高度ではない
2. **チーム協業**: 同時編集機能なし
3. **バージョン管理**: Git統合が弱い
4. **大規模モデル**: 巨大プロジェクトでパフォーマンス低下
5. **プラグイン**: Enterprise Architectほどエコシステム豊富ではない
6. **要件管理**: JIRA等との統合が限定的
7. **ドキュメント生成**: カスタマイズ性が低い
8. **エンタープライズ機能**: リポジトリ、ベースライン管理なし

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Enterprise Architect** | エンタープライズ向け、高機能 | StarUMLより高機能だが高価 |
| **Visual Paradigm** | 多機能、チーム協業 | StarUMLより高機能だが複雑 |
| **PlantUML** | テキストベースUML | StarUMLよりシンプルだが無料 |
| **draw.io (diagrams.net)** | 汎用作図、無料 | StarUMLよりUML専門性低い |
| **Lucidchart** | クラウド、協業重視 | StarUMLよりWeb協業強い |

## 公式リンク

- **公式サイト**: [https://staruml.io/](https://staruml.io/)
- **ダウンロード**: [https://staruml.io/download](https://staruml.io/download)
- **ドキュメント**: [https://docs.staruml.io/](https://docs.staruml.io/)
- **エクステンション**: [http://staruml.io/extensions](http://staruml.io/extensions)
- **GitHub**: [https://github.com/staruml](https://github.com/staruml)

## 関連ドキュメント

- [UMLツール一覧](../UMLツール/)
- [Enterprise Architect](./Enterprise_Architect.md)
- [Visual Paradigm](./Visual_Paradigm.md)
- [PlantUML](./PlantUML.md)
- [UML設計ベストプラクティス](../../best-practices/uml-design.md)

---

**カテゴリ**: UMLツール  
**対象工程**: 要件定義、設計  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
