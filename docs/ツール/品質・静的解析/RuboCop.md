# RuboCop

## 概要

RuboCopは、Ruby公式の静的コード解析ツールです。Rubyスタイルガイド準拠、コードスメル、セキュリティ問題、パフォーマンス問題を検出し、自動修正（--auto-correct）をサポートします。Rails専用ルール、カスタムCop、VS Code統合により、Rubyコード品質を向上させます。

## 主な機能

### 1. コード解析
- **スタイル**: Rubyスタイルガイド
- **Lint**: 構文エラー、バグ
- **セキュリティ**: セキュリティ問題
- **パフォーマンス**: パフォーマンス改善

### 2. 自動修正
- **Auto-correct**: 自動コード修正
- **セーフモード**: 安全な修正のみ

### 3. Rails対応
- **RuboCop Rails**: Rails専用ルール
- **RuboCop RSpec**: RSpec専用ルール

## 利用方法

### インストール

```bash
gem install rubocop
```

### 基本実行

```bash
# ファイル解析
rubocop myfile.rb

# ディレクトリ解析
rubocop app/

# 自動修正
rubocop --auto-correct
```

### 設定ファイル

```yaml
# .rubocop.yml
AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable

Style/StringLiterals:
  EnforcedStyle: double_quotes

Metrics/MethodLength:
  Max: 20
```

### CI/CD統合

```yaml
# .github/workflows/rubocop.yml
name: RuboCop

on: [push]

jobs:
  rubocop:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
      - run: gem install rubocop
      - run: rubocop
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **RuboCop** | 🟢 完全無料 | オープンソース、MIT License |

## メリット

1. **完全無料**: オープンソース
2. **自動修正**: コード自動修正
3. **Rails**: Rails専用ルール
4. **カスタマイズ**: 柔軟な設定
5. **活発**: 継続的開発

## デメリット

1. **厳格**: デフォルト設定が厳しい
2. **パフォーマンス**: 大規模で遅い
3. **誤検出**: False Positive
4. **設定**: 初期設定煩雑

## 公式リンク

- **公式サイト**: [https://rubocop.org/](https://rubocop.org/)
- **GitHub**: [https://github.com/rubocop/rubocop](https://github.com/rubocop/rubocop)

## 関連ドキュメント

- [Lintツール一覧](../Lintツール/)
- [Pylint](./Pylint.md)

---

**カテゴリ**: Lintツール  
**対象工程**: コード品質管理  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
