# JFrog Artifactory OSS

## 概要

JFrog Artifactory OSS は、ビルド成果物や依存パッケージを一元管理するアーティファクトリポジトリである。CI/CD パイプラインで生成された成果物を保存・配布し、再現可能なビルドとデプロイを支援する。

## 料金

| プラン | 内容 |
|------|------|
| OSS 版 | 無料（オープンソース版） |
| 商用版 | 上位機能を含む有償エディションあり |

## 主な特徴

| 項目 | 内容 |
|------|------|
| 成果物の一元管理 | ビルド成果物と依存パッケージを集中管理 |
| 複数フォーマット対応 | Maven、npm、Docker などを扱える |
| プロキシ機能 | 外部レジストリのキャッシュで安定供給 |
| 仮想リポジトリ | 複数リポジトリを単一エンドポイントで提供 |
| 権限制御 | チーム/プロジェクト単位でアクセス制御 |
| CI/CD連携 | Jenkins、GitHub Actions、GitLab CI/CD と連携しやすい |

## 主な機能

### リポジトリ管理機能

| 機能 | 説明 |
|------|------|
| Local Repository | 自組織成果物の保管 |
| Remote Repository | 外部レジストリのプロキシ・キャッシュ |
| Virtual Repository | 複数レポジトリを統合公開 |
| Repository Layout | 命名規則と保存構造を標準化 |

### 配布/運用機能

| 機能 | 説明 |
|------|------|
| Artifact Search | バージョンや属性で成果物を検索 |
| Metadata 管理 | ビルド情報や属性情報を保持 |
| Access Control | ユーザー/グループ別に権限設定 |
| Cleanup Policy | 古い成果物の整理運用を実施 |

### CI/CD連携機能

| 機能 | 説明 |
|------|------|
| Build Integration | ビルドから publish を自動化 |
| Docker Registry | コンテナイメージの保管・配布 |
| Dependency Resolution | 依存解決先を社内標準に統一 |
| Traceability | どのビルドがどの成果物か追跡可能 |

## インストールとセットアップ

公式URL:
- [JFrog Open Source](https://jfrog.com/open-source/)
- [Artifactory Documentation](https://jfrog.com/help/r/jfrog-artifactory-documentation)
- [Docker Distribution with Artifactory](https://jfrog.com/help/r/jfrog-artifactory-documentation/docker-registry)

セットアップの要点:
1. Docker かサーバーインストールで Artifactory を起動する。
2. Local/Remote/Virtual リポジトリを用途別に作成する。
3. CI/CD から publish / pull する認証情報を設定する。
4. 保持期間と削除ルール（cleanup）を定義する。

## 基本的な使い方

1. プロジェクトごとにリポジトリを作成する。
2. CI でビルド成果物を Artifactory へ publish する。
3. デプロイ工程で同じ成果物を pull して使用する。
4. 依存取得先を Remote/Virtual に集約する。
5. 不要成果物を定期削除してストレージを管理する。

最小運用例:
- Build: `artifactA:1.0.0` を publish
- Deploy: 同じ `artifactA:1.0.0` を参照して再現性を担保

## メリット

- 成果物管理を中央集約し、再現性を高めやすい。
- 外部依存のキャッシュによりビルド安定性を上げやすい。
- バージョン追跡と権限制御で監査性を確保しやすい。

## デメリット

- 初期設計（命名、権限、保持方針）が不十分だと運用が崩れやすい。
- ストレージとバックアップの運用設計が必要。
- OSS 版では一部の高度機能に制限がある。

## CI/CD での使用

CI ではビルド完了後に成果物を Artifactory へ公開し、CD では同一バージョンを取得してデプロイする構成が基本である。これにより「ビルド時成果物」と「配布成果物」を一致させ、環境差分による不具合を減らしやすい。

## 他ツールとの比較

| ツール | 強み | 特徴 |
|------|------|------|
| Artifactory OSS | 汎用性 | 複数パッケージ形式の一元管理 |
| Sonatype Nexus OSS | OSS導入 | Maven 系中心で導入しやすい |
| GitHub Packages | GitHub連携 | GitHub 利用組織で運用しやすい |
| GitLab Package Registry | GitLab連携 | GitLab パイプラインと統合しやすい |

## ベストプラクティス

### 1. リポジトリ設計を先に決める

- Local/Remote/Virtual の役割を固定する。
- プロジェクト単位で命名規則を統一する。

### 2. 成果物の不変性を守る

- リリース済みバージョンの上書きを禁止する。
- タグやビルド番号と成果物を紐づける。

### 3. 運用ルールを自動化

- 古いスナップショット削除を定期実行する。
- アクセス権とトークンを定期棚卸しする。

## 公式ドキュメント

- 公式サイト: https://jfrog.com/open-source/
- Artifactory Documentation: https://jfrog.com/help/r/jfrog-artifactory-documentation
- Docker Registry: https://jfrog.com/help/r/jfrog-artifactory-documentation/docker-registry

## まとめ

- Artifactory OSS は成果物を一元管理し、再現可能な CI/CD 運用を実現しやすい。
- リポジトリ設計と権限制御を先に固めることで、運用の安定性を高められる。
- 成果物の不変性と cleanup 自動化を徹底すると、長期運用しやすくなる。
