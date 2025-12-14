# WinMerge

## 概要

WinMerge は、Windows 向けのオープンソースファイル比較・マージツールです。テキストファイル、フォルダ、画像などの差分を視覚的に表示し、マージ作業を支援します。シンプルなインターフェースで直感的に操作でき、個人開発者からエンタープライズまで幅広く利用されています。

## 主な特徴

### 1. ファイル比較
- サイドバイサイド表示での差分可視化
- 行単位・文字単位での差分ハイライト
- 3-way マージのサポート
- バイナリファイル比較

### 2. フォルダ比較
- ディレクトリツリー全体の比較
- 再帰的なサブフォルダスキャン
- フィルタリング機能（ファイル名、拡張子）
- 差分のみの表示

### 3. マージ機能
- インタラクティブなマージ操作
- ブロック単位での変更取り込み
- 競合解決の支援
- 編集後の再比較

### 4. 多様な比較オプション
- 空白の無視
- 大文字小文字の区別
- コメント行の無視
- 正規表現フィルター

### 5. プラグインシステム
- カスタムフォーマットのサポート
- 前処理・後処理プラグイン
- ファイルパッカー
- エディタスクリプト

## 主な機能

### ファイル比較機能

| 機能 | 説明 |
|------|------|
| 2-way 比較 | 2つのファイルの差分表示 |
| 3-way 比較 | ベースファイルを含む3つの比較 |
| テーブル比較 | CSV/TSV ファイルの比較 |
| 画像比較 | 画像ファイルの差分表示 |
| バイナリ比較 | バイナリファイルの16進数表示比較 |

### フォルダ比較機能

| 機能 | 説明 |
|------|------|
| ツリー表示 | ディレクトリ構造の可視化 |
| フィルター | ファイル名・拡張子でのフィルタリング |
| 同期機能 | フォルダ間のファイル同期 |
| 統計情報 | 差分ファイル数の集計 |

### 編集機能

| 機能 | 説明 |
|------|------|
| インライン編集 | 差分画面での直接編集 |
| ブロックコピー | 差分ブロックの片方向コピー |
| マージ | 両側の変更をマージ |
| 元に戻す/やり直し | 変更履歴の管理 |

## インストールとセットアップ

### Windows

#### インストーラー版

```powershell
# 公式サイトからダウンロード
# https://winmerge.org/downloads/

# または Chocolatey を使用
choco install winmerge

# または winget を使用
winget install WinMerge.WinMerge
```

#### ポータブル版

```
1. https://winmerge.org/downloads/ からポータブル版をダウンロード
2. 任意のフォルダに解凍
3. WinMergeU.exe を実行
```

### システム要件

- Windows 7 SP1 以降（Windows 10/11 推奨）
- .NET Framework 4.5 以降
- RAM: 512 MB 以上
- ディスク: 50 MB 以上

## 基本的な使い方

### 1. ファイル比較

```
方法1: GUIから
1. WinMerge を起動
2. メニュー: ファイル → 開く (Ctrl+O)
3. 左側と右側のファイルを選択
4. 「OK」をクリック

方法2: コマンドラインから
WinMergeU.exe /e /u "C:\path\to\file1.txt" "C:\path\to\file2.txt"

方法3: エクスプローラーから
2つのファイルを選択 → 右クリック → WinMerge で比較
```

### 2. フォルダ比較

```
方法1: GUIから
1. WinMerge を起動
2. メニュー: ファイル → 開く (Ctrl+O)
3. 左側と右側のフォルダを選択
4. 「サブフォルダを含む」にチェック（必要に応じて）
5. 「OK」をクリック

方法2: コマンドラインから
WinMergeU.exe /r "C:\folder1" "C:\folder2"
```

### 3. 3-way マージ

```
コマンドライン:
WinMergeU.exe /e /u /wl /wr "C:\mine.txt" "C:\base.txt" "C:\theirs.txt"

オプション:
/e : 一つのインスタンスで開く
/u : 最近使ったファイルリストに追加しない
/wl : 左ペインを読み取り専用にする
/wr : 右ペインを読み取り専用にする
```

### 4. 差分のナビゲーション

```
キーボードショートカット:
Alt + ↓     : 次の差分へ移動
Alt + ↑     : 前の差分へ移動
Ctrl + Alt + ←/→ : 差分ブロックをコピー
Ctrl + Alt + L/R : 現在の差分を左/右から取得
F5           : 再比較
Ctrl + S     : 保存
```

## コマンドラインオプション

### 基本オプション

```bash
# ファイル比較
WinMergeU.exe "file1.txt" "file2.txt"

# フォルダ比較（再帰的）
WinMergeU.exe /r "folder1" "folder2"

# 読み取り専用で開く
WinMergeU.exe /r /wl /wr "file1.txt" "file2.txt"

# 比較結果を出力
WinMergeU.exe /r /u /minimize "folder1" "folder2" /or "result.html"

# 3-way マージ
WinMergeU.exe "left.txt" "base.txt" "right.txt"
```

### オプション一覧

| オプション | 説明 |
|-----------|------|
| `/r` | フォルダを再帰的に比較 |
| `/e` | 一つのインスタンスで開く（ESCで閉じる） |
| `/s` | 単一インスタンスモード |
| `/u` | 最近使ったファイルリストに追加しない |
| `/wl` | 左ペインを読み取り専用 |
| `/wr` | 右ペインを読み取り専用 |
| `/ul` | 左ペインのラベルを指定 |
| `/ur` | 右ペインのラベルを指定 |
| `/um` | 中央ペインのラベルを指定（3-way） |
| `/minimize` | 最小化状態で起動 |
| `/maximize` | 最大化状態で起動 |
| `/fl` | 左ファイルへの自動フォーカス |
| `/fm` | 中央ファイルへの自動フォーカス |
| `/fr` | 右ファイルへの自動フォーカス |
| `/dl` | 左側の説明テキスト |
| `/dr` | 右側の説明テキスト |
| `/or` | レポートファイル出力 |

### レポート出力

```bash
# HTML レポート
WinMergeU.exe /r "folder1" "folder2" /or "report.html"

# シンプルリスト
WinMergeU.exe /r "folder1" "folder2" /or "report.txt"

# CSV 形式
WinMergeU.exe /r "folder1" "folder2" /or "report.csv"
```

## 高度な機能

### プラグインの使用

#### 組み込みプラグイン

```
1. プラグイン → プラグインの自動展開
2. プラグイン → プラグインの設定

主なプラグイン:
- CompareMSExcelFiles.sct : Excel ファイル比較
- CompareMSWordFiles.sct : Word ファイル比較
- CompareMSPowerPointFiles.sct : PowerPoint ファイル比較
- IgnoreColumns.dll : CSV の特定列を無視
- IgnoreCommentsC.dll : C/C++ コメント無視
```

#### カスタムプラグインの作成

```vbscript
' MyPlugin.sct
<?xml version="1.0"?>
<scriptlet>
<implements type="Automation">
  <property name="PluginEvent">
    <get/>
  </property>
  <method name="PluginFileFilter"/>
  <method name="PluginFileProcess"/>
</implements>

<script language="VBScript">
Option Explicit

Function get_PluginEvent()
  get_PluginEvent = "FILE_PREDIFF"
End Function

Function PluginFileFilter(sText, bstrFilepath)
  PluginFileFilter = True
End Function

Function PluginFileProcess(sText, bstrFilepath)
  ' カスタム処理
  PluginFileProcess = sText
End Function
</script>
</scriptlet>
```

### フィルターの設定

#### ファイルフィルター

```
設定 → フィルター → ファイルフィルター

例:
*.exe;*.dll;*.obj     # 実行ファイル除外
bin\;obj\;.git\       # 特定フォルダ除外
test_*.txt            # パターンマッチ
```

#### 行フィルター

```
設定 → フィルター → 行フィルター

正規表現の例:
^#.*$                 # コメント行を無視
^\s*$                 # 空行を無視
^import\s+.*          # import文を無視
^\d{4}-\d{2}-\d{2}    # 日付形式を無視
```

### カラースキームのカスタマイズ

```
設定 → 色 → シンタックスカラー

カスタマイズ可能な要素:
- 差分背景色
- 追加行/削除行/変更行
- 現在の差分ハイライト
- 移動ブロック
- SNP（空白・改行・パラグラフ）表示
```

## バージョン管理システムとの統合

### Git との統合

#### difftool として設定

```bash
# Git 設定
git config --global diff.tool winmerge
git config --global difftool.winmerge.cmd '"C:/Program Files/WinMerge/WinMergeU.exe" -e -u "$LOCAL" "$REMOTE"'
git config --global difftool.prompt false

# 使用
git difftool HEAD~1 HEAD
```

#### mergetool として設定

```bash
# Git 設定
git config --global merge.tool winmerge
git config --global mergetool.winmerge.cmd '"C:/Program Files/WinMerge/WinMergeU.exe" -e -u -wl -wr "$LOCAL" "$BASE" "$REMOTE" -o "$MERGED"'
git config --global mergetool.winmerge.trustExitCode false

# 使用
git mergetool
```

### TortoiseSVN との統合

```
1. TortoiseSVN の設定を開く
2. 「外部プログラム」→「Diff Viewer」を選択
3. 外部 Diff プログラム:
   C:\Program Files\WinMerge\WinMergeU.exe -e -u -wl -wr %base %mine

4. 「マージツール」を選択
5. 外部マージツール:
   C:\Program Files\WinMerge\WinMergeU.exe -e -u %merged %theirs %mine
```

### TortoiseGit との統合

```
設定 → Diff Viewer:
C:\Program Files\WinMerge\WinMergeU.exe -e -u %base %mine

設定 → Merge Tool:
C:\Program Files\WinMerge\WinMergeU.exe -e -u %base %theirs %mine -o %merged
```

## スクリプトでの自動化

### PowerShell スクリプト例

```powershell
# 複数フォルダの比較レポート生成
$WinMerge = "C:\Program Files\WinMerge\WinMergeU.exe"
$BaseDir = "C:\baseline"
$CompareDir = "C:\current"
$ReportDir = "C:\reports"

$folders = Get-ChildItem $CompareDir -Directory

foreach ($folder in $folders) {
    $base = Join-Path $BaseDir $folder.Name
    $compare = $folder.FullName
    $report = Join-Path $ReportDir "$($folder.Name)_diff.html"

    if (Test-Path $base) {
        & $WinMerge /r /u /minimize $base $compare /or $report
        Write-Host "Generated report: $report"
    }
}
```

### バッチスクリプト例

```batch
@echo off
setlocal

set WINMERGE="C:\Program Files\WinMerge\WinMergeU.exe"
set LEFT=C:\project\version1
set RIGHT=C:\project\version2
set REPORT=C:\reports\comparison.html

REM フォルダ比較してレポート生成
%WINMERGE% /r /u /minimize "%LEFT%" "%RIGHT%" /or "%REPORT%"

REM レポートをブラウザで開く
start "" "%REPORT%"

endlocal
```

## CI/CD での使用

### Jenkins パイプライン

```groovy
pipeline {
    agent any

    stages {
        stage('Compare') {
            steps {
                script {
                    def winmerge = 'C:\\Program Files\\WinMerge\\WinMergeU.exe'
                    def baseline = 'C:\\baseline'
                    def current = 'C:\\workspace\\output'
                    def report = 'C:\\reports\\diff.html'

                    bat """
                        "${winmerge}" /r /u /minimize "${baseline}" "${current}" /or "${report}"
                    """

                    publishHTML([
                        reportDir: 'C:\\reports',
                        reportFiles: 'diff.html',
                        reportName: 'WinMerge Comparison Report'
                    ])
                }
            }
        }
    }
}
```

## 設定ファイル

### WinMerge.ini の場所

```
ユーザー設定:
%APPDATA%\WinMerge\WinMerge.ini

インストールフォルダ（管理者設定）:
C:\Program Files\WinMerge\WinMerge.ini
```

### 主な設定項目

```ini
[Settings]
# 外観
ViewLineNumbers=1
ViewWhitespace=1

# 比較オプション
IgnoreCase=0
IgnoreEol=0
IgnoreBlankLines=0

# エディタ
TabSize=4
InsertTabs=0
WordWrap=1

# パフォーマンス
FileSize=128
QuickCompareLimit=4194304

# 自動保存
AutomaticRescan=1
```

## ユースケース

### 1. コードレビュー

```
シナリオ: プルリクエストのコード差分確認

手順:
1. ブランチをチェックアウト
   git checkout main
   git pull origin main

2. 比較対象ブランチをチェックアウト
   git checkout feature-branch

3. WinMerge で比較
   git difftool main feature-branch

利点:
- サイドバイサイドでの詳細確認
- インライン編集による即座の修正
- 複数ファイルの同時比較
```

### 2. リリース検証

```
シナリオ: 本番環境とステージング環境の設定ファイル比較

手順:
1. 設定ファイルのダウンロード
2. WinMerge でフォルダ比較
3. 差分レポートの生成
4. レビューと承認

コマンド:
WinMergeU.exe /r "staging-config" "production-config" /or "release-diff.html"
```

### 3. データ移行

```
シナリオ: CSV データの移行前後の検証

手順:
1. 移行前後のCSVファイルを準備
2. WinMerge でテーブル比較モードを使用
3. データの整合性確認
4. 差分の記録
```

## トラブルシューティング

### よくある問題と解決策

#### 1. 日本語が文字化けする

```
原因: 文字エンコーディングの不一致
解決策:
1. 表示 → 文字コードページ → UTF-8 / Shift-JIS を選択
2. 設定 → エディタ → デフォルト文字コードページを設定
```

#### 2. 大きなファイルで動作が遅い

```
原因: ファイルサイズが大きすぎる
解決策:
1. 設定 → 比較 → クイック比較限界を調整
2. バイナリ比較モードを使用
3. ファイルを分割して比較
```

#### 3. フォルダ比較で特定のファイルが表示されない

```
原因: ファイルフィルターが適用されている
解決策:
1. 表示 → フィルター → すべて表示
2. 設定 → フィルター → ファイルフィルターを確認
```

## 代替ツールとの比較

| 機能 | WinMerge | Beyond Compare | Meld | KDiff3 |
|------|----------|----------------|------|--------|
| ライセンス | オープンソース（無料） | 商用（有料） | オープンソース（無料） | オープンソース（無料） |
| プラットフォーム | Windows | Win/Mac/Linux | Win/Mac/Linux | Win/Mac/Linux |
| 3-way マージ | ○ | ○ | ○ | ○ |
| 画像比較 | ○ | ○ | × | × |
| プラグイン | ○ | ○ | × | × |
| Office ファイル | プラグイン | ネイティブ | × | × |
| 日本語 | ○ | △ | ○ | ○ |

## 参考リソース

### 公式ドキュメント
- 公式サイト: https://winmerge.org/
- ドキュメント: https://manual.winmerge.org/
- GitHub: https://github.com/WinMerge/winmerge

### コミュニティ
- フォーラム: https://forums.winmerge.org/
- バグトラッカー: https://github.com/WinMerge/winmerge/issues
- 翻訳: https://translations.winmerge.org/

### チュートリアル
- Getting Started: https://manual.winmerge.org/Quick_start.html
- Command Line: https://manual.winmerge.org/Command_line.html
- Plugins: https://manual.winmerge.org/Plugins.html

## まとめ

WinMerge は、以下の場面で特に有用です:

1. **コードレビュー** - ブランチ間の差分確認とインライン修正
2. **リリース管理** - 環境間の設定ファイル比較
3. **データ検証** - CSV/テキストファイルの整合性確認
4. **マージ作業** - 競合解決とマージ操作

無料でありながら強力な機能を持ち、Windows 環境での差分比較・マージ作業の定番ツールとして広く使用されています。
