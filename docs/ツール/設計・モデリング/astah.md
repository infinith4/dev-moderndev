# astah*

## 概要

**astah***（アスター）は、日本のChange Vision社が開発するUML/ER図/DFD/マインドマップ対応のモデリングツールです。日本語に最適化されたUI、軽量動作、直感的な操作性が特徴で、日本国内で広く採用されています。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Change Vision, Inc.（株式会社チェンジビジョン） |
| **種別** | UML/モデリングツール |
| **ライセンス** | プロプライエタリ |
| **料金** | 🟡 一部無料（Community版無料、Professional版有料） |
| **公式サイト** | https://astah.net/ |
| **ドキュメント** | https://astah.net/support/ |

## 主な特徴

### 1. 豊富な図種類
- **UML**: クラス図、シーケンス図、ユースケース図、アクティビティ図、ステートマシン図、コンポーネント図、配置図、オブジェクト図
- **ER図**: エンティティ関連図、論理ER図、物理ER図
- **DFD**: データフロー図
- **フローチャート**: 業務フローチャート
- **マインドマップ**: アイデア整理

### 2. 日本語最適化
- 完全日本語UI
- 日本語フォント最適化
- 日本の開発現場に適した機能

### 3. 軽量・高速
- Javaベース（クロスプラットフォーム）
- 起動・動作が高速
- メモリ消費少ない

### 4. プラグインエコシステム
- Javaで独自プラグイン開発可能
- コード生成（Java、C#、C++等）
- 逆エンジニアリング（コードからUML生成）

## エディション比較

| 機能 | Community | Professional | UML |
|------|-----------|--------------|-----|
| **料金** | 無料 | 約50,000円/年 | 約70,000円/年 |
| **UML図** | ○ | ○ | ○ |
| **ER図** | × | ○ | × |
| **DFD** | × | ○ | × |
| **マインドマップ** | × | ○ | ○ |
| **コード生成** | × | ○ | ○ |
| **逆エンジニアリング** | × | ○ | ○ |
| **商用利用** | × | ○ | ○ |

## 使い方

### インストール

```bash
# 公式サイトからダウンロード
# https://astah.net/download

# Windows: astah-professional-setup.exe
# macOS: astah-professional.dmg
# Linux: astah-professional.sh

# インストール後、ライセンスキー入力（Professional版）
# Community版は無料、ライセンスキー不要
```

### 基本的な使い方

#### 1. クラス図の作成

**GUI操作**:
1. 新規プロジェクト作成
2. 構造ツリーで右クリック → クラス図追加
3. ツールパレットから「クラス」を選択
4. 図上でクリックしてクラス作成
5. クラス名、属性、操作を入力

**例: Javaクラス設計**

```text
┌─────────────────────┐
│   User              │
├─────────────────────┤
│ - id: int           │
│ - name: String      │
│ - email: String     │
│ - createdAt: Date   │
├─────────────────────┤
│ + getId(): int      │
│ + getName(): String │
│ + setName(name: String): void │
│ + validate(): boolean │
└─────────────────────┘
        △
        │ extends
        │
┌─────────────────────┐
│   AdminUser         │
├─────────────────────┤
│ - role: String      │
├─────────────────────┤
│ + getRole(): String │
│ + assignRole(role: String): void │
└─────────────────────┘
```

#### 2. シーケンス図の作成

```text
┌────┐          ┌────────┐        ┌──────────┐       ┌──────────┐
│User│          │Frontend│        │  Backend │       │ Database │
└─┬──┘          └───┬────┘        └────┬─────┘       └────┬─────┘
  │                 │                  │                    │
  │ 1: ログイン要求  │                  │                    │
  ├────────────────>│                  │                    │
  │                 │ 2: POST /auth/login                  │
  │                 ├─────────────────>│                    │
  │                 │                  │ 3: SELECT user     │
  │                 │                  ├───────────────────>│
  │                 │                  │ 4: user data       │
  │                 │                  │<───────────────────┤
  │                 │ 5: JWT token     │                    │
  │                 │<─────────────────┤                    │
  │ 6: トークン返却   │                  │                    │
  │<────────────────┤                  │                    │
```

#### 3. ER図の作成（Professional版）

```text
┌─────────────────┐        ┌─────────────────┐
│  users          │        │  posts          │
├─────────────────┤        ├─────────────────┤
│ PK id           │1      *│ PK id           │
│    name         ├────────┤ FK user_id      │
│    email        │        │    title        │
│    created_at   │        │    content      │
└─────────────────┘        │    created_at   │
                           └─────────────────┘
```

### コード生成

```bash
# Java コード生成（GUI操作）
# ツール → Java → Javaソース生成

# 生成されるJavaコード例
public class User {
    private int id;
    private String name;
    private String email;
    private Date createdAt;

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean validate() {
        // TODO: implement
        return false;
    }
}
```

### 逆エンジニアリング（コードからUML生成）

```bash
# Java コードからクラス図生成（GUI操作）
# ツール → Java → Javaソース読込

# ディレクトリ選択でJavaファイルをスキャン
# クラス図が自動生成される
```

### マインドマップ

```text
                    プロジェクト計画
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
      要件定義          設計              実装
        │                 │                 │
  ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
機能要件  非機能要件  基本設計  詳細設計  フロント  バック
```

### プラグイン開発

```java
// MyAstahPlugin.java
import com.change_vision.jude.api.inf.AstahAPI;
import com.change_vision.jude.api.inf.project.ProjectAccessor;
import com.change_vision.jude.api.inf.ui.IPluginActionDelegate;
import com.change_vision.jude.api.inf.ui.IWindow;

public class MyAstahPlugin implements IPluginActionDelegate {

    @Override
    public Object run(IWindow window) throws UnExpectedException {
        try {
            AstahAPI api = AstahAPI.getAstahAPI();
            ProjectAccessor projectAccessor = api.getProjectAccessor();

            // プロジェクト情報取得
            String projectName = projectAccessor.getProject().getName();

            // カスタム処理
            window.showMessageDialog("Project: " + projectName);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}
```

### ファイル形式

```text
# astah* プロジェクトファイル
*.asta      # 標準形式
*.jude      # 旧JUDE形式（互換性）

# エクスポート形式
*.png       # 画像エクスポート
*.jpg       # 画像エクスポート
*.svg       # ベクター画像
*.xmi       # XMI (UML交換形式)
```

### バージョン管理

```bash
# Git で astah* ファイルを管理
git add design.asta
git commit -m "Add user class diagram"

# 差分確認（テキストベースではないため困難）
# → 画像エクスポート + Gitでの管理推奨

# PNG エクスポート自動化（プラグイン利用）
# または、Git LFS利用
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **要件定義** | ユースケース図 | ユーザー要求の可視化 |
| **基本設計** | クラス図・ER図 | システム構造設計 |
| **基本設計** | シーケンス図 | 処理フロー設計 |
| **詳細設計** | 詳細クラス図 | 実装レベルの設計 |
| **実装** | コード生成 | UMLからコード自動生成 |

## メリット

- **日本語最適化**: 完全日本語UI、日本の開発現場に適合
- **軽量・高速**: 起動・動作が軽快
- **豊富な図種類**: UML、ER図、DFD、マインドマップ対応
- **コード生成**: Java、C#、C++等のコード自動生成
- **逆エンジニアリング**: コードからUML生成
- **Community版無料**: 学習・非商用利用は無料
- **プラグインエコシステム**: カスタマイズ可能

## デメリット

- **有料ライセンス**: 商用利用にはProfessional版が必要（約5万円/年）
- **ファイル形式独自**: .asta形式、他ツールとの互換性限定的
- **バージョン管理困難**: バイナリ形式でGit差分確認が困難
- **リアルタイムコラボ不可**: ファイルベース、同時編集不可
- **クラウド非対応**: ローカルインストール必須

## 類似ツールとの比較

| ツール | 料金 | 特徴 | 適用場面 |
|--------|------|------|----------|
| **astah*** | 無料〜5万円/年 | 日本語、軽量、ER図対応 | 日本の開発現場 |
| **Enterprise Architect** | 約6万円〜 | エンタープライズ機能豊富 | 大規模プロジェクト |
| **Visual Paradigm** | 無料〜有料 | 多機能、コラボレーション | チーム開発 |
| **PlantUML** | 無料 | テキストベースUML | コード管理・自動化 |
| **Draw.io** | 無料 | 汎用作図、クラウド対応 | シンプルな図作成 |

## ベストプラクティス

### 1. 図の階層化

```text
# パッケージ構造で整理
プロジェクト
├── domain (ドメインモデル)
│   ├── User.class
│   └── Post.class
├── application (アプリケーション層)
│   └── UserService.class
└── infrastructure (インフラ層)
    └── UserRepository.class
```

### 2. ステレオタイプの活用

```text
<<interface>>
IUserRepository
├────────────
+ findById(id: int): User
+ save(user: User): void

<<entity>>
User
├────────────
- id: int
- name: String
```

### 3. 図の定期的なエクスポート

```bash
# PNGエクスポート → Git管理
design/
├── class-diagram.asta      # 元ファイル
├── class-diagram.png       # エクスポート画像（Git管理）
└── sequence-diagram.png    # エクスポート画像（Git管理）
```

### 4. ドキュメント生成

```bash
# 図 + 説明をドキュメント化
# ツール → HTML出力
# → 設計ドキュメント自動生成
```

## 公式リソース

- **公式サイト**: https://astah.net/
- **ダウンロード**: https://astah.net/download
- **ユーザーズガイド**: https://astah.net/support/astah-professional/user-guide/
- **プラグイン**: https://astah.net/product/plugin
- **コミュニティ**: https://members.change-vision.com/

## まとめ

astah*は、日本製の軽量・高速なUML/モデリングツールです。完全日本語対応、直感的なUI、豊富な図種類（UML、ER図、DFD、マインドマップ）を提供し、日本の開発現場で広く採用されています。Community版は無料で学習・非商用利用が可能で、Professional版では商用利用、コード生成、逆エンジニアリング等の高度な機能が利用できます。

---

**最終更新**: 2025-12-06
**対象バージョン**: astah* professional 9.0+
