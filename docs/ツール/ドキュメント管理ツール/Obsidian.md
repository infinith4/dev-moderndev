# Obsidian

## 概要

Obsidian は、Markdown ベースのナレッジベース・ノート管理アプリケーションです。ローカルファイルを基盤とし、双方向リンクによるネットワーク状のノート構造を構築できます。「Second Brain（第二の脳）」として、個人的な知識管理からチームのドキュメント管理まで幅広く活用できます。

## 主な特徴

### 1. ローカルファイル優先
- Markdown ファイルをローカルに保存
- プレーンテキストで可搬性が高い
- オフラインで完全動作
- 自分でバックアップとバージョン管理が可能

### 2. 双方向リンク
- `[[ノート名]]` で簡単にリンク作成
- バックリンクの自動追跡
- グラフビューでノート間の関係を可視化
- リンクされたメンション

### 3. プラグインエコシステム
- コアプラグイン（標準機能）
- コミュニティプラグイン（1000以上）
- カスタムCSS/テーマ
- Dataview などの強力なプラグイン

### 4. 拡張性
- API を使った独自プラグイン開発
- CSS によるカスタマイズ
- テンプレート機能
- ホットキーのカスタマイズ

### 5. グラフビュー
- ノート間の関係を視覚化
- インタラクティブな探索
- フィルタリングとグループ化
- ローカルグラフとグローバルグラフ

## 主な機能

### 基本機能

| 機能 | 説明 |
|------|------|
| Markdown エディタ | リアルタイムプレビュー付きエディタ |
| ファイルエクスプローラー | フォルダ・ファイルのツリー表示 |
| クイック検索 | ノート名・内容の全文検索 |
| タグ | `#tag` によるノート分類 |
| バックリンク | 被リンクの自動表示 |

### コアプラグイン

| プラグイン | 説明 |
|-----------|------|
| Daily Notes | 日次ノートの自動作成 |
| Templates | テンプレート挿入 |
| Backlinks | バックリンクパネル |
| Graph View | ノート関係の視覚化 |
| Outgoing Links | 外部リンク表示 |
| File Recovery | 自動バックアップ |
| Workspaces | ワークスペースの保存 |
| Slides | プレゼンテーションモード |

### 人気のコミュニティプラグイン

| プラグイン | 説明 |
|-----------|------|
| Dataview | ノートをデータベースとしてクエリ |
| Templater | 高度なテンプレート機能 |
| Calendar | カレンダービューでデイリーノート管理 |
| Kanban | かんばんボード |
| Excalidraw | 手書き図表作成 |
| Advanced Tables | テーブル編集の強化 |
| Tasks | タスク管理 |

## インストールとセットアップ

### デスクトップアプリ

#### Windows

```powershell
# 公式サイトからダウンロード
# https://obsidian.md/download

# または winget を使用
winget install Obsidian.Obsidian

# または Chocolatey を使用
choco install obsidian
```

#### macOS

```bash
# 公式サイトからダウンロード
# https://obsidian.md/download

# または Homebrew を使用
brew install --cask obsidian
```

#### Linux

```bash
# AppImage（推奨）
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v1.5.3/Obsidian-1.5.3.AppImage
chmod +x Obsidian-1.5.3.AppImage
./Obsidian-1.5.3.AppImage

# Snap
sudo snap install obsidian --classic

# Flatpak
flatpak install flathub md.obsidian.Obsidian
```

### モバイルアプリ

- iOS: App Store からダウンロード
- Android: Google Play ストアからダウンロード

### 初期セットアップ

```
1. Obsidian を起動
2. 「Create new vault」または「Open folder as vault」を選択
3. Vault 名とロケーションを設定
4. 「Create」をクリック
```

## 基本的な使い方

### 1. ノートの作成

```markdown
# 方法1: 新規ノートボタン
左サイドバーの「New note」ボタンをクリック

# 方法2: ショートカット
Ctrl + N（Windows/Linux）
Cmd + N（macOS）

# 方法3: リンクから作成
[[新しいノート名]]  ← リンクをクリックして作成
```

### 2. リンクの作成

```markdown
# 内部リンク
[[ノート名]]
[[ノート名|表示テキスト]]
[[ノート名#見出し]]
[[ノート名#見出し|表示テキスト]]

# ブロックリンク
[[ノート名#^block-id]]

# 外部リンク
[表示テキスト](https://example.com)

# 画像埋め込み
![[画像.png]]
![[画像.png|300]]  # サイズ指定

# ノート埋め込み
![[ノート名]]
```

### 3. タグの使用

```markdown
# ハッシュタグ
#プロジェクト
#プロジェクト/サブタグ
#進行中

# フロントマターでのタグ
---
tags:
  - プロジェクト
  - 重要
  - 2024
---
```

### 4. フロントマター

```markdown
---
title: ドキュメント名
author: 山田太郎
date: 2024-01-15
tags:
  - プロジェクト
  - 技術文書
status: 進行中
---

# ドキュメント本文
```

### 5. テンプレートの使用

```markdown
# テンプレートファイル: templates/meeting-note.md
---
type: meeting
date: {{date}}
participants: []
---

# {{title}}

## アジェンダ
-

## 議事録
-

## アクションアイテム
- [ ]

---
使い方:
1. 設定 → コアプラグイン → Templates を有効化
2. Templates folder を設定
3. Ctrl/Cmd + T でテンプレート挿入
```

## 高度な機能

### Dataview プラグイン

```markdown
# タスクリストのクエリ
```dataview
TASK
WHERE !completed
GROUP BY file.folder
```

# テーブル表示
```dataview
TABLE
  author,
  date,
  status
FROM #プロジェクト
WHERE status = "進行中"
SORT date DESC
```

# リスト表示
```dataview
LIST
FROM #重要
WHERE date >= date(today) - dur(7 days)
```

# カレンダー表示
```dataview
CALENDAR date
FROM #デイリーノート
```
```

### Templater プラグイン

```markdown
# 高度なテンプレート
---
created: <% tp.file.creation_date() %>
modified: <% tp.file.last_modified_date() %>
---

# <% tp.file.title %>

<% tp.system.prompt("概要を入力してください") %>

## 関連ノート
<% tp.file.cursor(1) %>

---
作成者: <% tp.user.name() %>
```

### Kanban ボード

```markdown
---

kanban-plugin: basic

---

## To Do

- [ ] タスク1 #重要
- [ ] タスク2 @担当者A


## In Progress

- [ ] タスク3


## Done

- [x] タスク4 ✅ 2024-01-15

```

### Excalidraw 統合

```
1. Excalidraw プラグインをインストール
2. 新規 Excalidraw 図を作成
3. 手書き図表を作成
4. ノートに埋め込み: ![[drawing.excalidraw]]
```

## Git によるバージョン管理

### Obsidian Git プラグイン

```
1. コミュニティプラグインから「Obsidian Git」をインストール
2. Vault を Git リポジトリとして初期化
3. 自動コミット・プッシュの設定

設定例:
- 自動コミット間隔: 10分
- 自動プッシュ間隔: 30分
- コミットメッセージ: "vault backup: {{date}}"
```

### .gitignore 例

```gitignore
# Obsidian の設定ファイル（プライベート設定）
.obsidian/workspace.json
.obsidian/workspace-mobile.json

# キャッシュ
.obsidian/cache

# プラグイン（含めない場合）
.obsidian/plugins/*

# 作業中ファイル
.trash/
.DS_Store
```

## チーム利用

### Obsidian Sync（公式サービス）

```
特徴:
- エンドツーエンド暗号化
- デバイス間の自動同期
- バージョン履歴
- 月額 $8（年間 $96）

設定:
1. 設定 → Sync を有効化
2. Obsidian アカウントでサインイン
3. 同期設定を選択
4. 他のデバイスで同期開始
```

### サードパーティ同期

#### Git + GitHub/GitLab

```bash
# リポジトリの初期化
cd /path/to/vault
git init
git remote add origin https://github.com/username/vault.git

# Obsidian Git プラグインで自動化
# または手動コミット
git add .
git commit -m "Update notes"
git push origin main
```

#### クラウドストレージ

```
対応サービス:
- Google Drive
- Dropbox
- OneDrive
- iCloud Drive

注意点:
- 競合解決の管理が必要
- 同期タイミングに注意
- .obsidian フォルダの扱い
```

## プラグイン開発

### 基本的なプラグイン構造

```typescript
// main.ts
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
    async onload() {
        console.log('Loading plugin');

        // コマンドの追加
        this.addCommand({
            id: 'my-command',
            name: 'My Command',
            callback: () => {
                console.log('Command executed');
            }
        });

        // リボンアイコンの追加
        this.addRibbonIcon('dice', 'My Plugin', () => {
            console.log('Ribbon icon clicked');
        });

        // ステータスバーアイテムの追加
        const statusBarItem = this.addStatusBarItem();
        statusBarItem.setText('My Plugin Status');
    }

    async onunload() {
        console.log('Unloading plugin');
    }
}
```

### マニフェストファイル

```json
{
    "id": "my-plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "minAppVersion": "0.15.0",
    "description": "My custom Obsidian plugin",
    "author": "Your Name",
    "authorUrl": "https://example.com",
    "isDesktopOnly": false
}
```

### ビルドとテスト

```bash
# 依存関係のインストール
npm install

# 開発ビルド
npm run dev

# 本番ビルド
npm run build

# プラグインフォルダにコピー
cp main.js manifest.json /path/to/vault/.obsidian/plugins/my-plugin/
```

## ユースケース

### 1. 個人のナレッジベース

```
構造例:
vault/
├── Daily Notes/        # デイリーノート
├── Projects/           # プロジェクト別ノート
├── Areas/              # 責任領域
├── Resources/          # 参考資料
├── Archives/           # アーカイブ
└── Templates/          # テンプレート

ワークフロー:
1. デイリーノートで毎日の記録
2. プロジェクトノートで詳細管理
3. リソースノートで知識蓄積
4. グラフビューで関連発見
```

### 2. 技術ドキュメント管理

```
構造例:
docs/
├── Architecture/       # アーキテクチャ設計
├── API/                # API ドキュメント
├── Guides/             # 開発ガイド
├── Troubleshooting/    # トラブルシューティング
└── ADR/                # アーキテクチャ決定記録

Dataview クエリ例:
```dataview
TABLE
  status,
  author,
  date
FROM "Architecture"
WHERE status = "approved"
SORT date DESC
```
```

### 3. プロジェクト管理

```
Kanban ボード + Dataview の組み合わせ:

# プロジェクトダッシュボード
```dataview
TASK
WHERE !completed AND contains(tags, "current-sprint")
GROUP BY project
```

# 進捗レポート
```dataview
TABLE
  length(filter(file.tasks, (t) => t.completed)) as "完了",
  length(file.tasks) as "総数"
FROM #プロジェクト
```
```

## ベストプラクティス

### 1. フォルダ構造

```
# PARA メソッド
vault/
├── Projects/       # 進行中のプロジェクト
├── Areas/          # 継続的な責任領域
├── Resources/      # 参考資料・知識
└── Archives/       # 完了・保管

# Zettelkasten メソッド
vault/
├── Inbox/          # 未処理ノート
├── Permanent/      # 恒久的ノート
├── Literature/     # 文献ノート
└── Fleeting/       # 一時的メモ
```

### 2. ノートの命名規則

```
# タイムスタンプ方式
202401151430 - ミーティングノート.md

# トピック方式
プロジェクトA - 要件定義.md
技術メモ - Docker コンテナ最適化.md

# 階層方式
プロジェクト/プロジェクトA/要件定義.md
```

### 3. リンク戦略

```markdown
# ハブノート（MOC: Map of Content）
# プロジェクトA

## 概要
[[プロジェクトA - 概要]]

## ドキュメント
- [[要件定義]]
- [[設計書]]
- [[テスト計画]]

## ミーティング
- [[2024-01-15 - キックオフ]]
- [[2024-01-22 - 進捗確認]]

## 参考資料
- [[技術選定]]
- [[ベストプラクティス]]
```

## トラブルシューティング

### よくある問題と解決策

#### 1. 同期の競合

```
原因: 複数デバイスでの同時編集
解決策:
- Obsidian Sync を使用
- Git で競合を管理
- クラウドストレージの同期タイミングを調整
```

#### 2. パフォーマンスの低下

```
原因: Vault のサイズが大きい、プラグインが多い
解決策:
- インデックスの再構築
- 不要なプラグインを無効化
- 画像ファイルの最適化
- Vault の分割
```

#### 3. リンク切れ

```
原因: ファイル名変更、移動
解決策:
- 「Core Plugins → File Recovery」を有効化
- リンクの自動更新を有効化
- Dataview で壊れたリンクを検出:
  ```dataview
  LIST
  WHERE length(file.outlinks) > 0 AND !all(file.outlinks, (l) => exists(l))
  ```
```

## 参考リソース

### 公式リソース
- 公式サイト: https://obsidian.md/
- ドキュメント: https://help.obsidian.md/
- フォーラム: https://forum.obsidian.md/
- Discord: https://discord.gg/obsidianmd

### コミュニティ
- Reddit: https://www.reddit.com/r/ObsidianMD/
- GitHub: https://github.com/obsidianmd
- プラグイン一覧: https://obsidian.md/plugins

### チュートリアル
- Getting Started: https://help.obsidian.md/Getting+started/
- Linking Notes: https://help.obsidian.md/Linking+notes+and+files/
- Community Talks: https://obsidian.md/community

## まとめ

Obsidian は、以下の場面で特に有用です:

1. **個人のナレッジ管理** - 双方向リンクによる知識のネットワーク化
2. **技術ドキュメント** - Markdown + Git によるバージョン管理
3. **プロジェクト管理** - Dataview + Kanban によるタスク・進捗管理
4. **チーム共有** - Git または Obsidian Sync による協調作業

ローカルファイル優先の設計により、データの完全なコントロールと可搬性を確保しながら、強力なプラグインエコシステムで拡張可能な柔軟性を提供します。
