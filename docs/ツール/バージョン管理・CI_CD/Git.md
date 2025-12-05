# Git

## 概要

Gitは、分散型バージョン管理システム（DVCS: Distributed Version Control System）です。Linus Torvalds氏によって開発され、ソフトウェア開発におけるソースコードの変更履歴を追跡・管理します。ブランチ・マージ機能により、複数開発者が並行して作業でき、GitHub、GitLab、Bitbucket等のホスティングサービスと組み合わせることで、チーム開発の標準ツールとして世界中で利用されています。

## 主な機能

### 1. 分散型アーキテクチャ
- **ローカルリポジトリ**: 各開発者が完全なコピーを保持
- **リモートリポジトリ**: GitHub、GitLab等での共有
- **オフライン作業**: ネットワーク不要でコミット可能
- **高速**: ローカル操作で高速動作

### 2. ブランチ・マージ
- **ブランチ作成**: 軽量・高速なブランチ作成
- **マージ**: Fast-forward、3-way merge
- **コンフリクト解決**: マージ競合の手動解決
- **Rebase**: コミット履歴の整理

### 3. コミット管理
- **Staging Area**: コミット前の変更選択
- **コミットハッシュ**: SHA-1ハッシュで一意識別
- **コミットメッセージ**: 変更内容の記録
- **Amend**: 直前コミットの修正

### 4. 履歴管理
- **Log**: コミット履歴の表示
- **Diff**: 変更差分の表示
- **Blame**: 行ごとの変更者表示
- **Reset/Revert**: コミットの取り消し

### 5. リモート操作
- **Clone**: リポジトリの複製
- **Pull**: リモート変更の取得
- **Push**: ローカル変更の送信
- **Fetch**: リモート情報の取得（マージなし）

### 6. タグ
- **Lightweight Tag**: 単純なポインタ
- **Annotated Tag**: メッセージ付きタグ
- **リリース管理**: バージョンタグ

## 利用方法

### インストール

```bash
# Windows (Git for Windows)
# https://git-scm.com/download/win
# インストーラーをダウンロード・実行

# macOS (Homebrew)
brew install git

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install git

# CentOS/RHEL
sudo yum install git

# バージョン確認
git --version
```

### 初期設定

```bash
# ユーザー名設定
git config --global user.name "Your Name"

# メールアドレス設定
git config --global user.email "your.email@example.com"

# デフォルトブランチ名（main）
git config --global init.defaultBranch main

# デフォルトエディタ設定
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim

# 改行コード設定（Windows）
git config --global core.autocrlf true

# 改行コード設定（macOS/Linux）
git config --global core.autocrlf input

# 設定確認
git config --list
```

### 基本操作

```bash
# リポジトリ初期化
git init

# ファイル追加（Staging）
git add <file>
git add .                # 全ファイル
git add *.js             # パターンマッチ

# コミット
git commit -m "コミットメッセージ"
git commit -am "Add & Commit"  # addとcommitを同時実行

# 状態確認
git status

# 変更差分表示
git diff                 # ワーキングディレクトリ vs Staging
git diff --staged        # Staging vs HEAD
git diff HEAD            # ワーキングディレクトリ vs HEAD

# コミット履歴
git log
git log --oneline        # 1行表示
git log --graph          # グラフ表示
git log --all --decorate --oneline --graph  # 全ブランチ視覚化
```

### ブランチ操作

```bash
# ブランチ一覧
git branch
git branch -a            # リモート含む全ブランチ

# ブランチ作成
git branch feature/new-feature

# ブランチ切り替え
git checkout feature/new-feature

# ブランチ作成+切り替え
git checkout -b feature/new-feature
git switch -c feature/new-feature  # 新コマンド

# ブランチマージ
git checkout main
git merge feature/new-feature

# ブランチ削除
git branch -d feature/new-feature   # マージ済みブランチ
git branch -D feature/new-feature   # 強制削除
```

### リモート操作

```bash
# リモートリポジトリクローン
git clone https://github.com/user/repo.git

# リモート追加
git remote add origin https://github.com/user/repo.git

# リモート確認
git remote -v

# リモートから取得（マージなし）
git fetch origin

# リモートから取得+マージ
git pull origin main

# リモートへプッシュ
git push origin main

# 新規ブランチをプッシュ（追跡設定）
git push -u origin feature/new-feature
```

### 便利なコマンド

```bash
# 特定ファイルの変更履歴
git log -- <file>

# 特定行の変更者表示
git blame <file>

# コミット取り消し（履歴残す）
git revert <commit-hash>

# コミット取り消し（履歴削除）
git reset --soft HEAD~1   # コミット取り消し、変更は残す
git reset --hard HEAD~1   # コミット+変更を完全削除

# ステージング取り消し
git restore --staged <file>

# ワーキングディレクトリ変更破棄
git restore <file>

# 一時退避
git stash
git stash list
git stash pop
git stash apply stash@{0}

# タグ作成
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"

# タグプッシュ
git push origin v1.0.0
git push origin --tags
```

### .gitignore設定

```bash
# .gitignore ファイル作成
cat > .gitignore << 'EOF'
# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Node.js
node_modules/
npm-debug.log

# Python
__pycache__/
*.pyc
.env

# Build
dist/
build/
*.log
EOF

# 反映
git add .gitignore
git commit -m "Add .gitignore"
```

## チーム開発ワークフロー

### Git Flow

```bash
# mainブランチ: 本番環境
# developブランチ: 開発統合

# 新機能開発
git checkout develop
git checkout -b feature/login-page
# 開発作業
git add .
git commit -m "Add login page"
git checkout develop
git merge feature/login-page
git branch -d feature/login-page

# リリース準備
git checkout -b release/v1.0.0 develop
# バグ修正、バージョン番号更新
git checkout main
git merge release/v1.0.0
git tag v1.0.0
git checkout develop
git merge release/v1.0.0
git branch -d release/v1.0.0

# ホットフィックス
git checkout -b hotfix/critical-bug main
# バグ修正
git checkout main
git merge hotfix/critical-bug
git tag v1.0.1
git checkout develop
git merge hotfix/critical-bug
git branch -d hotfix/critical-bug
```

### GitHub Flow（シンプル）

```bash
# mainブランチから機能ブランチ作成
git checkout main
git pull origin main
git checkout -b feature/new-feature

# 開発・コミット
git add .
git commit -m "Implement new feature"

# リモートへプッシュ
git push -u origin feature/new-feature

# GitHub でPull Request作成
# レビュー・承認後、main へマージ
# ブランチ削除
git checkout main
git pull origin main
git branch -d feature/new-feature
```

## 料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Git** | 🟢 完全無料 | オープンソース、GPL v2 License |

## メリット

### ✅ 主な利点

1. **分散型**: 各開発者がフル履歴を保持
2. **高速**: ローカル操作で即座に反応
3. **ブランチ軽量**: ブランチ作成・切り替えが高速
4. **オフライン作業**: ネットワーク不要でコミット可能
5. **無料**: 完全無料、オープンソース
6. **業界標準**: 世界中で最も利用されるVCS
7. **豊富なツール**: GUI、IDE統合、ホスティング多数
8. **柔軟なワークフロー**: Git Flow、GitHub Flow等
9. **強力な履歴管理**: Rebase、Cherry-pick等
10. **大規模対応**: Linuxカーネル等の巨大プロジェクトに対応

## デメリット

### ❌ 制約・課題

1. **学習曲線**: コマンド多数、概念理解が必要
2. **バイナリファイル**: 大きなバイナリには不向き
3. **複雑な履歴**: Merge/Rebaseで履歴が複雑化
4. **権限管理**: Git単体では細かい権限設定不可
5. **初心者には難解**: コンフリクト解決等で挫折しやすい
6. **リポジトリ肥大化**: 履歴が増えるとクローン遅延
7. **GUIツール依存**: CLI習得には時間かかる
8. **誤操作リスク**: Reset --hardで変更消失の危険

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Subversion (SVN)** | 集中型VCS | Gitより単純だが分散型ではない |
| **Mercurial** | 分散型VCS | Gitと類似だが採用率低い |
| **Perforce** | エンタープライズVCS | Gitより大規模バイナリに強い |
| **Fossil** | 分散型VCS+Wiki+Bug tracker | Gitよりオールインワン |
| **Bazaar** | 分散型VCS | Gitより使いやすいが開発停滞 |

## 公式リンク

- **公式サイト**: [https://git-scm.com/](https://git-scm.com/)
- **ドキュメント**: [https://git-scm.com/doc](https://git-scm.com/doc)
- **Pro Git Book**: [https://git-scm.com/book/ja/v2](https://git-scm.com/book/ja/v2)
- **GitHub**: [https://github.com/](https://github.com/)
- **GitLab**: [https://gitlab.com/](https://gitlab.com/)
- **Bitbucket**: [https://bitbucket.org/](https://bitbucket.org/)

## 関連ドキュメント

- [バージョン管理ツール一覧](../バージョン管理ツール/)
- [GitHub](./GitHub.md)
- [GitLab](./GitLab.md)
- [GitHub Actions](../CI_CDツール/GitHub_Actions.md)
- [Gitワークフローベストプラクティス](../../best-practices/git-workflow.md)

---

**カテゴリ**: バージョン管理ツール  
**対象工程**: 全工程  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
