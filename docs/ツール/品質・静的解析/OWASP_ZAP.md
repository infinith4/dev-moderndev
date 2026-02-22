# OWASP ZAP

## 概要

OWASP ZAP（Zed Attack Proxy）は、オープンソースのWebアプリケーション脆弱性スキャナーです。SQLインジェクション、XSS、CSRF等のOWASP Top 10脆弱性を自動検出し、動的アプリケーションセキュリティテスト（DAST）、ペネトレーションテスト、CI/CD統合により、セキュリティテスト自動化を支援します。

## 主な機能

### 1. 脆弱性スキャン
- **自動スキャン**: クローリング+スキャン
- **手動テスト**: プロキシモード
- **OWASP Top 10**: SQLi、XSS、CSRF等

### 2. プロキシ
- **インターセプト**: HTTP/HTTPS通信
- **リクエスト改変**: 手動テスト
- **履歴**: 全リクエスト記録

### 3. 自動化
- **API**: RESTful API
- **CLI**: コマンドライン
- **CI/CD**: Jenkins、GitHub Actions統合

## 利用方法

### インストール

```bash
# Docker
docker run -u zap -p 8080:8080 zaproxy/zap-stable zap-webswing.sh

# ダウンロード
# https://www.zaproxy.org/download/
```

### GUI使用

```
1. ZAP起動
2. Quick Start → Automated Scan
3. URL入力: https://example.com
4. Attack → スキャン開始
5. Alerts → 脆弱性確認
```

### CLI使用

```bash
# クイックスキャン
docker run -t zaproxy/zap-stable zap-baseline.py -t https://example.com

# フルスキャン
docker run -t zaproxy/zap-stable zap-full-scan.py -t https://example.com -r report.html
```

### CI/CD統合

```yaml
# .github/workflows/zap.yml
name: OWASP ZAP Scan

on: [push]

jobs:
  zap_scan:
    runs-on: ubuntu-latest
    steps:
      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'https://example.com'
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **OWASP ZAP** | 🟢 無料 | オープンソース、Apache License |

## メリット

1. **無料**: オープンソース
2. **OWASP公式**: 信頼性高い
3. **自動化**: CI/CD統合
4. **DAST**: 動的テスト
5. **GUI/CLI**: 両対応

## デメリット

1. **誤検出**: False Positive多い
2. **パフォーマンス**: スキャン遅い
3. **学習曲線**: 機能多数
4. **本番環境**: 本番スキャン注意

## 公式リンク

- **公式サイト**: [https://www.zaproxy.org/](https://www.zaproxy.org/)
- **ドキュメント**: [https://www.zaproxy.org/docs/](https://www.zaproxy.org/docs/)

## 関連ドキュメント

- [セキュリティスキャンツール一覧](../セキュリティスキャンツール/)
- [Burp Suite](./Burp_Suite.md)

---

**カテゴリ**: セキュリティスキャンツール  
**対象工程**: セキュリティテスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
