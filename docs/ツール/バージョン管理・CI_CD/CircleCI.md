# CircleCI

## 概要

CircleCIは、クラウドベースCI/CDプラットフォームです。config.yml、ワークフロー、Orbs（再利用可能コンポーネント）、Docker/Kubernetes統合により、ビルド、テスト、デプロイを自動化します。高速並列実行、GitHubGitLab統合、豊富な無料枠で広く採用されています。

## 主な機能

### 1. パイプライン
- **ワークフロー**: 複数ジョブ
- **並列実行**: マトリックスビルド
- **条件分岐**: ブランチ、タグ
- **スケジュール**: cron実行

### 2. Docker統合
- **Docker Executor**: コンテナビルド
- **Remote Docker**: DinD
- **イメージキャッシュ**: レイヤーキャッシュ

### 3. Orbs
- **再利用**: 共有コンポーネント
- **公式Orbs**: AWS、GCP、Kubernetes
- **カスタムOrbs**: 独自Orbs

### 4. キャッシュ
- **依存関係**: npm、Maven等
- **Docker層**: レイヤーキャッシュ
- **ワークスペース**: ジョブ間共有

## 利用方法

### 基本設定

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: npm install
      - run:
          name: Run tests
          command: npm test

workflows:
  version: 2
  build-and-test:
    jobs:
      - build
```

### 複数ジョブ・ワークフロー

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run: npm install
      - run: npm run build
      - persist_to_workspace:
          root: .
          paths:
            - dist

  test:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run: npm install
      - run: npm test

  deploy:
    docker:
      - image: cimg/node:18.0
    steps:
      - attach_workspace:
          at: .
      - run: ./deploy.sh

workflows:
  build-test-deploy:
    jobs:
      - build
      - test:
          requires:
            - build
      - deploy:
          requires:
            - test
          filters:
            branches:
              only: main
```

### Docker Build

```yaml
version: 2.1

jobs:
  build-docker:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.14
      - run:
          name: Build Docker image
          command: |
            docker build -t myapp:$CIRCLE_SHA1 .
            docker tag myapp:$CIRCLE_SHA1 myapp:latest
      - run:
          name: Push to Docker Hub
          command: |
            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
            docker push myapp:latest

workflows:
  docker-build:
    jobs:
      - build-docker
```

### キャッシュ

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout

      # 依存関係キャッシュ復元
      - restore_cache:
          keys:
            - v1-dependencies-{{ checksum "package-lock.json" }}
            - v1-dependencies-

      - run: npm install

      # 依存関係キャッシュ保存
      - save_cache:
          paths:
            - node_modules
          key: v1-dependencies-{{ checksum "package-lock.json" }}

      - run: npm test
```

### Orbs使用

```yaml
version: 2.1

orbs:
  aws-cli: circleci/aws-cli@3.1
  kubernetes: circleci/kubernetes@1.3

jobs:
  deploy-to-eks:
    executor: aws-cli/default
    steps:
      - checkout
      - aws-cli/setup
      - kubernetes/install-kubectl
      - run:
          name: Deploy to EKS
          command: |
            aws eks update-kubeconfig --name my-cluster
            kubectl apply -f k8s/

workflows:
  deploy:
    jobs:
      - deploy-to-eks
```

### 並列実行

```yaml
version: 2.1

jobs:
  test:
    docker:
      - image: cimg/node:18.0
    parallelism: 4
    steps:
      - checkout
      - run: npm install
      - run:
          name: Run tests
          command: |
            TEST_FILES=$(circleci tests glob "test/**/*.test.js" | circleci tests split --split-by=timings)
            npm test -- $TEST_FILES

workflows:
  test-parallel:
    jobs:
      - test
```

### 環境変数

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/node:18.0
    environment:
      NODE_ENV: production
      API_URL: https://api.example.com
    steps:
      - checkout
      - run: echo "API URL is $API_URL"
      - run: npm run build

# CircleCI Web UI > Project Settings > Environment Variables
# API_KEY=secret123
```

### スケジュール実行

```yaml
version: 2.1

workflows:
  nightly:
    triggers:
      - schedule:
          cron: "0 0 * * *"
          filters:
            branches:
              only: main
    jobs:
      - build
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Free** | 🟢 無料 | 6,000分/月、1並列 |
| **Performance** | 💰 $15/月 | 25,000分/月、5並列 |
| **Scale** | 💰 $2,000/月 | 200,000分/月、カスタム |
| **Server** | 💰 要問い合わせ | Self-Hosted |

## メリット

1. **無料枠**: 6,000分/月無料
2. **並列実行**: 高速ビルド
3. **Docker統合**: Dockerネイティブ
4. **Orbs**: 再利用可能コンポーネント
5. **GitHub統合**: シームレス統合

## デメリット

1. **分数制限**: 無料枠6,000分
2. **YAML複雑**: 設定学習必要
3. **デバッグ**: ローカルデバッグ難しい
4. **コスト**: 大規模で高額

## 公式リンク

- **公式サイト**: [https://circleci.com/](https://circleci.com/)
- **ドキュメント**: [https://circleci.com/docs/](https://circleci.com/docs/)

## 関連ドキュメント

- [CI/CDツール一覧](../CI_CDツール/)
- [GitHub Actions](./GitHub_Actions.md)
- [GitLab CI](./GitLab_CI.md)

---

**カテゴリ**: CI/CDツール
**対象工程**: 継続的インテグレーション・デプロイ
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
