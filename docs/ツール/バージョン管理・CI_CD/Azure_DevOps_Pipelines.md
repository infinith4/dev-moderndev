# Azure DevOps Pipelines

## 概要

Azure DevOps Pipelinesは、Microsoft Azure DevOps内のCI/CDサービスです。YAML定義またはクラシックUIでビルド・デプロイパイプラインを作成し、マルチプラットフォーム（Windows、Linux、macOS）、マルチ言語（.NET、Java、Python、Node.js等）、マルチクラウド（Azure、AWS、GCP）に対応します。GitHub、GitLab等のリポジトリと統合し、エンタープライズグレードのCI/CDを実現します。

## 主な機能

### 1. CI/CD パイプライン
- **YAML定義**: コードでパイプライン管理
- **クラシックエディタ**: GUIベース設定
- **マルチステージ**: ビルド、テスト、デプロイ
- **承認ゲート**: 本番デプロイ前の承認

### 2. マルチプラットフォーム
- **Microsoft-hosted agents**: Windows、Linux、macOS
- **Self-hosted agents**: オンプレミス、カスタムエージェント
- **コンテナジョブ**: Docker、Kubernetes
- **並列実行**: 複数ジョブ同時実行

### 3. 統合
- **Azure統合**: Azure App Service、AKS、Functions
- **GitHub**: GitHub Actions風の統合
- **他クラウド**: AWS、GCP、Heroku
- **成果物管理**: Azure Artifacts

### 4. テスト
- **自動テスト**: JUnit、NUnit、pytest、Jest
- **カバレッジ**: コードカバレッジレポート
- **テスト結果**: ダッシュボード表示

### 5. リリース管理
- **リリースパイプライン**: 環境別デプロイ
- **ブルーグリーン**: ゼロダウンタイムデプロイ
- **カナリアリリース**: 段階的リリース
- **ロールバック**: 失敗時の自動ロールバック

## 利用方法

### YAMLパイプライン基本例

```
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: 18.x
  
  - script: npm install
    displayName: Install dependencies
  
  - script: npm test
    displayName: Run tests
```

### Docker ビルド

```
steps:
  - task: Docker@2
    inputs:
      command: buildAndPush
      repository: myapp
      dockerfile: Dockerfile
      tags: latest
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** | 🟢 無料 | 1,800分/月、並列1ジョブ |
| **Microsoft-hosted** | 💰 $40/並列ジョブ/月 | 追加並列ジョブ |
| **Self-hosted** | 💰 $15/並列ジョブ/月 | 自前エージェント |

## メリット

### ✅ 主な利点

1. **無料枠**: 1,800分/月無料
2. **YAML**: Infrastructure as Code
3. **マルチプラットフォーム**: Windows、Linux、macOS
4. **マルチクラウド**: Azure、AWS、GCP対応
5. **Azure統合**: シームレスなAzure連携
6. **GitHub統合**: GitHub Actionsと類似
7. **承認ゲート**: 本番デプロイ承認
8. **エンタープライズ**: AAD、RBAC統合
9. **並列実行**: 複数ジョブ同時実行
10. **テンプレート**: 再利用可能な定義

## デメリット

### ❌ 制約・課題

1. **Azure DevOps依存**: Azure DevOps組織必須
2. **学習曲線**: YAML構文習得必要
3. **無料枠制限**: 1,800分/月まで
4. **Microsoft-hosted制約**: ネットワーク制限
5. **UI複雑**: 初心者には難しい
6. **ドキュメント**: GitHub Actionsより情報少ない
7. **エージェントプール**: Self-hosted設定が煩雑
8. **ログ保持**: 30日間のみ

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **GitHub Actions** | GitHub統合、YAML | Azure Pipelinesと類似 |
| **GitLab CI/CD** | GitLab統合、YAML | Azure Pipelinesと類似 |
| **Jenkins** | オープンソース、プラグイン豊富 | Azure Pipelinesより柔軟 |
| **CircleCI** | SaaS、高速 | Azure Pipelinesより使いやすい |
| **AWS CodePipeline** | AWS統合 | Azure PipelinesのAWS版 |

## 公式リンク

- **公式サイト**: [https://azure.microsoft.com/services/devops/pipelines/](https://azure.microsoft.com/services/devops/pipelines/)
- **ドキュメント**: [https://docs.microsoft.com/azure/devops/pipelines/](https://docs.microsoft.com/azure/devops/pipelines/)
- **料金**: [https://azure.microsoft.com/pricing/details/devops/azure-devops-services/](https://azure.microsoft.com/pricing/details/devops/azure-devops-services/)

## 関連ドキュメント

- [CI/CDツール一覧](../CI_CDツール/)
- [GitHub Actions](./GitHub_Actions.md)
- [GitLab CI/CD](./GitLab_CI_CD.md)
- [Jenkins](./Jenkins.md)
- [CI/CDベストプラクティス](../../best-practices/cicd.md)

---

**カテゴリ**: CI/CDツール  
**対象工程**: 実装、テスト、デプロイ  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0
