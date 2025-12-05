#!/usr/bin/env python3
"""
ツールカテゴリ統合マイグレーションスクリプト
78カテゴリ → 16カテゴリへの統合
"""

import os
import shutil
from pathlib import Path

# 移行マッピング定義
MIGRATION_MAP = {
    # 1. 開発ツール
    "開発ツール": "開発ツール",
    "開発環境ツール": "開発ツール",
    "CLIツール": "開発ツール",
    "トランスパイラツール": "開発ツール",
    "ビルドツール": "開発ツール",
    "パッケージ管理ツール": "開発ツール",

    # 2. バージョン管理・CI/CD
    "バージョン管理ツール": "バージョン管理・CI_CD",
    "CI_CDツール": "バージョン管理・CI_CD",
    "自動化ツール": "バージョン管理・CI_CD",

    # 3. コンテナ・オーケストレーション
    "コンテナツール": "コンテナ・オーケストレーション",
    "オーケストレーションツール": "コンテナ・オーケストレーション",
    "サービスディスカバリツール": "コンテナ・オーケストレーション",
    "サービスメッシュツール": "コンテナ・オーケストレーション",

    # 4. IaC・インフラ管理
    "IaCツール": "IaC・インフラ管理",
    "IaCセキュリティツール": "IaC・インフラ管理",
    "インフラ設計ツール": "IaC・インフラ管理",
    "構成管理ツール": "IaC・インフラ管理",
    "シークレット管理ツール": "IaC・インフラ管理",
    "ポリシー管理ツール": "IaC・インフラ管理",

    # 5. テスト
    "テストツール": "テスト",
    "テストフレームワークツール": "テスト",
    "テスト管理ツール": "テスト",
    "E2Eテストツール": "テスト",
    "APIテストツール": "テスト",
    "負荷テストツール": "テスト",
    "インフラテストツール": "テスト",

    # 6. 品質・静的解析
    "静的解析ツール": "品質・静的解析",
    "Lintツール": "品質・静的解析",
    "セキュリティスキャンツール": "品質・静的解析",

    # 7. データベース
    "データベースツール": "データベース",
    "データベース設計ツール": "データベース",
    "NoSQLデータベースツール": "データベース",
    "クエリツール": "データベース",
    "データ移行ツール": "データベース",
    "マイグレーションツール": "データベース",

    # 8. API・統合
    "APIツール": "API・統合",
    "APIドキュメントツール": "API・統合",
    "モックツール": "API・統合",
    "メッセージングツール": "API・統合",

    # 9. Webアプリケーション
    "Webフレームワークツール": "Webアプリケーション",
    "フロントエンドフレームワークツール": "Webアプリケーション",
    "フレームワークツール": "Webアプリケーション",
    "Webサーバーツール": "Webアプリケーション",
    "アプリケーションサーバーツール": "Webアプリケーション",
    "ロードバランサーツール": "Webアプリケーション",

    # 10. 監視・ロギング
    "監視ツール": "監視・ロギング",
    "ログ収集ツール": "監視・ロギング",
    "ログ処理ツール": "監視・ロギング",
    "分散トレーシングツール": "監視・ロギング",
    "可視化ツール": "監視・ロギング",

    # 11. セキュリティ
    "セキュリティツール": "セキュリティ",
    "セキュリティ設計ツール": "セキュリティ",

    # 12. 設計・モデリング
    "設計ツール": "設計・モデリング",
    "UMLツール": "設計・モデリング",
    "UI_UXツール": "設計・モデリング",
    "作図ツール": "設計・モデリング",
    "アーキテクチャツール": "設計・モデリング",
    "プロセスモデリングツール": "設計・モデリング",

    # 13. プロジェクト管理・ドキュメント
    "プロジェクト管理ツール": "プロジェクト管理・ドキュメント",
    "ドキュメント管理ツール": "プロジェクト管理・ドキュメント",
    "ナレッジ管理ツール": "プロジェクト管理・ドキュメント",
    "コラボレーションツール": "プロジェクト管理・ドキュメント",
    "要件管理ツール": "プロジェクト管理・ドキュメント",
    "アイデア整理ツール": "プロジェクト管理・ドキュメント",

    # 14. 帳票・データ処理
    "帳票ツール": "帳票・データ処理",
    "表計算ツール": "帳票・データ処理",
    "データ処理ツール": "帳票・データ処理",
    "バッチ処理ツール": "帳票・データ処理",

    # 15. インフラストラクチャ
    "システム管理ツール": "インフラストラクチャ",
    "ネットワークツール": "インフラストラクチャ",
    "キャッシュツール": "インフラストラクチャ",
    "検索ツール": "インフラストラクチャ",

    # 16. 運用・ITSM
    "ITSMツール": "運用・ITSM",
    "インシデント管理ツール": "運用・ITSM",
    "レポーティングツール": "運用・ITSM",

    # そのまま維持
    "標準・ガイドライン": "標準・ガイドライン",

    # 保留（空カテゴリ）
    "クラウドサービス": "クラウドサービス",
    "AIツール": "AI・先進技術",
}

def migrate_files(base_dir: Path, dry_run: bool = False):
    """
    ファイルを旧カテゴリから新カテゴリに移動

    Args:
        base_dir: ツールディレクトリのベースパス
        dry_run: Trueの場合、実際の移動は行わずログのみ出力
    """
    moved_count = 0
    skipped_count = 0

    for old_category, new_category in MIGRATION_MAP.items():
        old_dir = base_dir / old_category
        new_dir = base_dir / new_category

        if not old_dir.exists():
            print(f"⚠️  旧カテゴリが存在しません: {old_category}")
            continue

        if old_category == new_category:
            print(f"✓ そのまま維持: {old_category}")
            continue

        # ディレクトリ内のMarkdownファイルを取得
        md_files = list(old_dir.glob("*.md"))

        if not md_files:
            print(f"📂 空カテゴリ: {old_category} (ファイル数: 0)")
            skipped_count += 1
            continue

        print(f"\n📦 {old_category} → {new_category} (ファイル数: {len(md_files)})")

        for md_file in md_files:
            dest_file = new_dir / md_file.name

            if dest_file.exists():
                print(f"  ⚠️  既に存在: {md_file.name} (スキップ)")
                skipped_count += 1
                continue

            if dry_run:
                print(f"  [DRY-RUN] {md_file.name} → {new_category}/")
            else:
                shutil.move(str(md_file), str(dest_file))
                print(f"  ✓ {md_file.name}")
                moved_count += 1

    return moved_count, skipped_count

def remove_empty_directories(base_dir: Path, dry_run: bool = False):
    """
    空ディレクトリを削除

    Args:
        base_dir: ツールディレクトリのベースパス
        dry_run: Trueの場合、実際の削除は行わずログのみ出力
    """
    removed_count = 0

    print("\n\n🗑️  空ディレクトリの削除")
    print("=" * 60)

    for item in base_dir.iterdir():
        if item.is_dir() and item.name not in ["標準・ガイドライン", "クラウドサービス", "AI・先進技術",
                                                 "開発ツール", "バージョン管理・CI_CD", "コンテナ・オーケストレーション",
                                                 "IaC・インフラ管理", "テスト", "品質・静的解析", "データベース",
                                                 "API・統合", "Webアプリケーション", "監視・ロギング", "セキュリティ",
                                                 "設計・モデリング", "プロジェクト管理・ドキュメント", "帳票・データ処理",
                                                 "インフラストラクチャ", "運用・ITSM"]:
            md_files = list(item.glob("*.md"))
            if not md_files:
                if dry_run:
                    print(f"  [DRY-RUN] 削除予定: {item.name}")
                else:
                    try:
                        shutil.rmtree(item)
                        print(f"  ✓ 削除: {item.name}")
                        removed_count += 1
                    except Exception as e:
                        print(f"  ❌ 削除失敗: {item.name} ({e})")

    return removed_count

def main():
    """メイン処理"""
    base_dir = Path("/src/docs/ツール")

    print("=" * 60)
    print("ツールカテゴリ統合マイグレーション")
    print("78カテゴリ → 16カテゴリへの統合")
    print("=" * 60)
    print()

    # ドライラン
    print("📋 ドライラン（実際の移動は行いません）")
    print("=" * 60)
    moved, skipped = migrate_files(base_dir, dry_run=True)
    print(f"\n移動予定: {moved}ファイル, スキップ: {skipped}件")

    # 確認
    print("\n\n" + "=" * 60)
    response = input("実際に移動を実行しますか？ (yes/no): ")

    if response.lower() != "yes":
        print("❌ キャンセルしました")
        return

    # 実際の移動
    print("\n\n🚀 ファイル移動を実行します...")
    print("=" * 60)
    moved, skipped = migrate_files(base_dir, dry_run=False)
    print(f"\n✅ 移動完了: {moved}ファイル, スキップ: {skipped}件")

    # 空ディレクトリの削除
    removed = remove_empty_directories(base_dir, dry_run=False)
    print(f"\n✅ 削除完了: {removed}ディレクトリ")

    print("\n" + "=" * 60)
    print("✅ マイグレーション完了！")
    print("=" * 60)

if __name__ == "__main__":
    main()
