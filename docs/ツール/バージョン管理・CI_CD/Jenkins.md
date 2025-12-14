# Jenkins

## 概要

Jenkinsは、オープンソースの自動化サーバーで、CI/CD（継続的インテグレーション/継続的デリバリー）のデファクトスタンダードとして長年利用されています。Java製で、プラグインアーキテクチャにより高い拡張性を持ち、ほぼ全ての開発ツールやプラットフォームと統合可能です。Jenkinsfileによるパイプライン as Codeをサポートし、複雑なビルド・テスト・デプロイワークフローを自動化できます。

## 料金プラン

| プラン | 料金 | 特徴 |
|-------|------|------|
| **Jenkins (OSS)** | 🟢 完全無料 | オープンソース、無制限利用、コミュニティサポート |
| **CloudBees CI (SaaS)** | 💰 見積もり必要 | マネージドサービス、エンタープライズサポート |
| **CloudBees CI (Traditional)** | 💰 見積もり必要 | オンプレミス版、商用サポート、高度な機能 |
| **セルフホスト費用** | 💰 インフラ次第 | サーバー、メンテナンス、運用コスト |

**注意**: Jenkins本体は無料ですが、セルフホスト環境の運用コスト（サーバー、保守）が発生します。エンタープライズ機能が必要な場合はCloudBees製品を検討。

## メリット・デメリット

### メリット
- ✅ **完全無料**: オープンソース、無制限利用可能
- ✅ **豊富なプラグイン**: 1,800以上のプラグインで拡張可能
- ✅ **高い柔軟性**: あらゆるツール、プラットフォームと統合可能
- ✅ **成熟したエコシステム**: 長年の実績、大規模コミュニティ
- ✅ **Pipeline as Code**: Jenkinsfileでパイプラインをバージョン管理
- ✅ **分散ビルド**: マスター/エージェント構成で大規模ビルドに対応
- ✅ **プラットフォーム非依存**: Git、GitHub、GitLab、Bitbucket等全て対応
- ✅ **Blue Ocean UI**: モダンなUIで可視化

### デメリット
- ❌ **保守負担**: セルフホスト環境の運用・保守が必要
- ❌ **初期設定の複雑さ**: セットアップ、プラグイン選定に時間がかかる
- ❌ **古いUI**: デフォルトUIが旧式（Blue Oceanで改善）
- ❌ **セキュリティリスク**: 定期的なアップデート、プラグイン管理が必要
- ❌ **リソース消費**: Javaベースで比較的重い
- ❌ **プラグイン依存**: プラグイン間の競合や非互換の可能性

## 利用できる開発工程

| 開発工程 | 活用シーン | 主な成果物 |
|---------|----------|-----------|
| **7. 実装（アプリケーション）** | コミット時の自動ビルド、コード品質チェック | Jenkinsfile、ビルド結果 |
| **8-1. CI/CD** | 自動ビルド、テスト、デプロイパイプライン構築 | CI/CDパイプライン、デプロイ履歴 |
| **9. テスト（アプリケーション）** | 自動テスト実行、カバレッジレポート | テスト結果、品質メトリクス |
| **10. テスト（インフラ）** | インフラコードの検証、セキュリティスキャン | インフラテスト結果 |
| **11. 導入** | 本番環境への自動デプロイ、ロールバック | デプロイログ、リリース管理 |

## 基本的な利用方法

### 1. Jenkinsのインストール

```bash
# Docker版（最も簡単）
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins \
  jenkins/jenkins:lts

# 初期管理者パスワードの確認
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Linux (Ubuntu/Debian)
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

# サービス起動
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Windows
# https://www.jenkins.io/download/ からMSIインストーラーをダウンロード

# macOS (Homebrew)
brew install jenkins-lts
brew services start jenkins-lts

# アクセス
# http://localhost:8080
```

### 2. 初期セットアップ

1. ブラウザで `http://localhost:8080` にアクセス
2. 初期管理者パスワードを入力
3. "Install suggested plugins" を選択（推奨プラグインを一括インストール）
4. 管理者ユーザーを作成
5. Jenkins URLを確認・設定

### 3. Jenkinsfile（宣言型パイプライン）の例

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    // 環境変数
    environment {
        NODE_VERSION = '20'
        APP_NAME = 'myapp'
    }

    // ビルドトリガー
    triggers {
        // 5分ごとにSCMをポーリング
        pollSCM('H/5 * * * *')
    }

    // ステージ定義
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/user/repo.git'
            }
        }

        stage('Build') {
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Lint') {
                    steps {
                        sh 'npm run lint'
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }

    // ビルド後の処理
    post {
        always {
            // テスト結果の収集
            junit 'test-results/**/*.xml'
            // ワークスペースのクリーンアップ
            cleanWs()
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
            // 通知（Slack、メール等）
        }
    }
}
```

### 4. 基本的な操作

```bash
# Jenkins CLI のダウンロード
wget http://localhost:8080/jnlpJars/jenkins-cli.jar

# ジョブのビルド実行
java -jar jenkins-cli.jar -s http://localhost:8080/ build JOB_NAME

# ジョブ一覧の取得
java -jar jenkins-cli.jar -s http://localhost:8080/ list-jobs

# プラグインのインストール
java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin PLUGIN_NAME

# Jenkinsの再起動
java -jar jenkins-cli.jar -s http://localhost:8080/ safe-restart
```

## 工程別の活用方法

### 7. 実装（アプリケーション）での活用

**目的**: 継続的インテグレーション、コード品質の維持

**活用方法**:
- プルリクエストビルド
- コードフォーマットチェック
- 静的解析（SonarQube統合）
- 依存関係の脆弱性スキャン

**実装例（Multibranch Pipeline）**:
```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }

    options {
        // タイムアウト設定
        timeout(time: 30, unit: 'MINUTES')
        // 同時実行を防止
        disableConcurrentBuilds()
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install flake8 black mypy pytest
                '''
            }
        }

        stage('Code Quality') {
            parallel {
                stage('Format Check') {
                    steps {
                        sh 'black --check .'
                    }
                }
                stage('Linting') {
                    steps {
                        sh 'flake8 . --max-line-length=88'
                    }
                }
                stage('Type Check') {
                    steps {
                        sh 'mypy . --strict'
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest tests/unit/ --junitxml=test-results/unit.xml --cov=src --cov-report=xml'
            }
            post {
                always {
                    junit 'test-results/unit.xml'
                    publishCoverage adapters: [
                        coberturaAdapter('coverage.xml')
                    ]
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Check console output at ${env.BUILD_URL}",
                to: '${DEFAULT_RECIPIENTS}'
            )
        }
    }
}
```

---

### 8-1. CI/CDでの活用

**目的**: エンド・ツー・エンドの自動化パイプライン

**活用方法**:
- マルチステージパイプライン
- 環境別デプロイ（dev/staging/prod）
- 承認ゲート
- アーティファクト管理

**実装例（完全なCI/CDパイプライン）**:
```groovy
// Jenkinsfile
@Library('shared-pipeline-library') _

pipeline {
    agent none

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Deployment environment')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests')
    }

    environment {
        DOCKER_REGISTRY = 'docker.io/mycompany'
        APP_NAME = 'myapp'
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Build') {
            agent {
                docker {
                    image 'maven:3.9-openjdk-21'
                    args '-v $HOME/.m2:/root/.m2'
                }
            }
            steps {
                sh 'mvn clean package -DskipTests'
                archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            }
        }

        stage('Test') {
            when {
                expression { !params.SKIP_TESTS }
            }
            parallel {
                stage('Unit Tests') {
                    agent {
                        docker 'maven:3.9-openjdk-21'
                    }
                    steps {
                        sh 'mvn test'
                    }
                    post {
                        always {
                            junit 'target/surefire-reports/*.xml'
                        }
                    }
                }
                stage('Integration Tests') {
                    agent {
                        docker 'maven:3.9-openjdk-21'
                    }
                    steps {
                        sh 'mvn verify -DskipUnitTests'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                script {
                    docker.withRegistry('', 'docker-hub-credentials') {
                        def customImage = docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG}")
                        customImage.push()
                        customImage.push('latest')
                    }
                }
            }
        }

        stage('Security Scan') {
            agent any
            steps {
                script {
                    sh """
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image ${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy to Dev') {
            when {
                expression { params.ENVIRONMENT == 'dev' }
            }
            agent any
            steps {
                sh """
                    kubectl set image deployment/${APP_NAME} \
                    ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG} \
                    --namespace=dev
                """
            }
        }

        stage('Deploy to Staging') {
            when {
                expression { params.ENVIRONMENT == 'staging' }
            }
            agent any
            steps {
                sh """
                    kubectl set image deployment/${APP_NAME} \
                    ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG} \
                    --namespace=staging
                """
            }
        }

        stage('Approval for Production') {
            when {
                expression { params.ENVIRONMENT == 'production' }
            }
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'
            }
        }

        stage('Deploy to Production') {
            when {
                expression { params.ENVIRONMENT == 'production' }
            }
            agent any
            steps {
                sh """
                    kubectl set image deployment/${APP_NAME} \
                    ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG} \
                    --namespace=production
                """
            }
        }

        stage('Post-Deployment Tests') {
            agent any
            steps {
                sh 'npm run test:smoke'
            }
        }
    }

    post {
        success {
            slackSend(
                channel: '#deployments',
                color: 'good',
                message: "Deployment successful: ${env.JOB_NAME} #${env.BUILD_NUMBER} to ${params.ENVIRONMENT}"
            )
        }
        failure {
            slackSend(
                channel: '#deployments',
                color: 'danger',
                message: "Deployment failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

---

### 9. テスト（アプリケーション）での活用

**目的**: 包括的なテストの自動実行、品質メトリクスの収集

**活用方法**:
- 並列テスト実行
- テストレポート統合
- パフォーマンステスト
- E2Eテスト

**実装例（テストパイプライン）**:
```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Parallel Tests') {
            parallel {
                stage('Unit Tests - Backend') {
                    agent {
                        docker 'maven:3.9-openjdk-21'
                    }
                    steps {
                        sh 'mvn test'
                        junit 'target/surefire-reports/*.xml'
                    }
                }

                stage('Unit Tests - Frontend') {
                    agent {
                        docker 'node:20'
                    }
                    steps {
                        sh 'npm ci'
                        sh 'npm test -- --coverage'
                        junit 'test-results/junit.xml'
                        publishHTML([
                            reportDir: 'coverage',
                            reportFiles: 'index.html',
                            reportName: 'Coverage Report'
                        ])
                    }
                }

                stage('Integration Tests') {
                    agent any
                    steps {
                        sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit'
                    }
                }
            }
        }

        stage('E2E Tests') {
            agent {
                docker {
                    image 'cypress/browsers:latest'
                    args '-v $PWD:/e2e -w /e2e'
                }
            }
            steps {
                sh 'npm ci'
                sh 'npm run cypress:run'
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'cypress/reports',
                        reportFiles: 'index.html',
                        reportName: 'Cypress Report'
                    ])
                }
            }
        }

        stage('Performance Tests') {
            agent {
                docker 'grafana/k6:latest'
            }
            steps {
                sh 'k6 run --out json=performance.json performance-test.js'
            }
            post {
                always {
                    perfReport sourceDataFiles: 'performance.json'
                }
            }
        }

        stage('Test Report') {
            steps {
                script {
                    def testResults = [
                        unit: currentBuild.getBuildCauses('hudson.model.Cause$UserIdCause').isEmpty(),
                        integration: true,
                        e2e: true,
                        performance: true
                    ]
                    echo "Test Results: ${testResults}"
                }
            }
        }
    }
}
```

---

### 10. テスト（インフラ）での活用

**目的**: Infrastructure as Codeの検証

**活用方法**:
- Terraformのvalidateとplan
- Ansibleの構文チェック
- インフラセキュリティスキャン

**実装例（Terraformパイプライン）**:
```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'hashicorp/terraform:1.6'
        }
    }

    environment {
        TF_VAR_environment = "${params.ENVIRONMENT}"
        AWS_DEFAULT_REGION = 'ap-northeast-1'
    }

    stages {
        stage('Terraform Init') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                sh 'terraform fmt -check -recursive'
                sh 'terraform validate'
            }
        }

        stage('Terraform Plan') {
            steps {
                sh 'terraform plan -out=tfplan'
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm -v $(pwd):/tf bridgecrew/checkov \
                    -d /tf --framework terraform --output junitxml > checkov-report.xml
                '''
            }
            post {
                always {
                    junit 'checkov-report.xml'
                }
            }
        }

        stage('Approval') {
            when {
                expression { params.ENVIRONMENT == 'production' }
            }
            steps {
                input message: 'Apply Terraform plan?', ok: 'Apply'
            }
        }

        stage('Terraform Apply') {
            steps {
                sh 'terraform apply tfplan'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'tfplan', allowEmptyArchive: true
        }
    }
}
```

---

### 11. 導入での活用

**目的**: 本番環境への信頼性の高いデプロイ

**活用方法**:
- ブルー/グリーンデプロイメント
- ロールバック機能
- デプロイ承認フロー

**実装例（本番デプロイ）**:
```groovy
// Jenkinsfile
pipeline {
    agent any

    parameters {
        string(name: 'VERSION', description: 'Version to deploy')
        choice(name: 'DEPLOYMENT_STRATEGY', choices: ['blue-green', 'rolling', 'canary'])
    }

    stages {
        stage('Pre-Deployment Checks') {
            steps {
                sh 'npm run test:smoke'
                sh './scripts/verify-environment.sh production'
            }
        }

        stage('Backup Current State') {
            steps {
                sh '''
                    kubectl get deployment myapp -n production -o yaml > backup-deployment.yaml
                    aws s3 cp backup-deployment.yaml s3://backups/$(date +%Y%m%d-%H%M%S)/
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (params.DEPLOYMENT_STRATEGY == 'blue-green') {
                        sh './scripts/blue-green-deploy.sh ${params.VERSION}'
                    } else if (params.DEPLOYMENT_STRATEGY == 'rolling') {
                        sh 'kubectl set image deployment/myapp myapp=myapp:${params.VERSION} --record'
                    } else if (params.DEPLOYMENT_STRATEGY == 'canary') {
                        sh './scripts/canary-deploy.sh ${params.VERSION}'
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                retry(5) {
                    sh 'curl -f https://app.example.com/health'
                    sleep 10
                }
            }
        }

        stage('Rollback Decision') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input message: 'Keep deployment or rollback?',
                          ok: 'Keep',
                          submitter: 'admin,devops'
                }
            }
        }
    }

    post {
        failure {
            sh '''
                echo "Deployment failed, initiating rollback"
                kubectl apply -f backup-deployment.yaml
            '''
        }
        success {
            sh 'rm -f backup-deployment.yaml'
        }
    }
}
```

## 公式ドキュメント

- [Jenkins 公式サイト](https://www.jenkins.io/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Plugin Index](https://plugins.jenkins.io/)
- [Jenkins User Handbook](https://www.jenkins.io/doc/book/)
- [Blue Ocean Documentation](https://www.jenkins.io/doc/book/blueocean/)

## 学習リソース

### チュートリアル
- [Jenkins Getting Started](https://www.jenkins.io/doc/pipeline/tour/getting-started/)
- [Pipeline Tutorial](https://www.jenkins.io/doc/book/pipeline/getting-started/)
- [Jenkins by Example](https://www.jenkins.io/doc/pipeline/examples/)

### 書籍・コース
- "Jenkins 2: Up and Running" by Brent Laster (O'Reilly)
- "Learning Continuous Integration with Jenkins" by Nikhil Pathania
- LinkedIn Learning - Learning Jenkins
- Udemy - Jenkins From Zero To Hero

### 動画
- [Jenkins Tutorial for Beginners](https://www.youtube.com/results?search_query=jenkins+tutorial)
- [CloudBeesTV](https://www.youtube.com/@cloudbees) - 公式YouTubeチャンネル
- [DevOps Directive - Jenkins](https://www.youtube.com/watch?v=6YZvp2GwT0A)

### コミュニティ
- [Jenkins Community](https://www.jenkins.io/participate/)
- [Jenkins User Mailing List](https://www.jenkins.io/mailing-lists/)
- [r/jenkinsci (Reddit)](https://www.reddit.com/r/jenkinsci/)
- [Stack Overflow - Jenkins](https://stackoverflow.com/questions/tagged/jenkins)

## 関連リンク

### 必須プラグイン
- [Pipeline Plugin](https://plugins.jenkins.io/workflow-aggregator/) - パイプライン機能の基盤
- [Git Plugin](https://plugins.jenkins.io/git/) - Gitリポジトリ統合
- [Docker Pipeline Plugin](https://plugins.jenkins.io/docker-workflow/) - Dockerコンテナでビルド実行
- [Blue Ocean](https://plugins.jenkins.io/blueocean/) - モダンなUI
- [Credentials Plugin](https://plugins.jenkins.io/credentials/) - 認証情報管理
- [Email Extension Plugin](https://plugins.jenkins.io/email-ext/) - メール通知

### 便利なプラグイン
- [Slack Notification Plugin](https://plugins.jenkins.io/slack/) - Slack通知
- [SonarQube Scanner](https://plugins.jenkins.io/sonar/) - コード品質分析
- [Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/) - Kubernetes統合
- [Config File Provider](https://plugins.jenkins.io/config-file-provider/) - 設定ファイル管理
- [Job DSL Plugin](https://plugins.jenkins.io/job-dsl/) - ジョブ定義をコード化

### ベストプラクティス
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Scaling Jenkins](https://www.jenkins.io/doc/book/scaling/)
- [Securing Jenkins](https://www.jenkins.io/doc/book/security/)
- [Awesome Jenkins](https://github.com/sahilsk/awesome-jenkins) - リソース集

---

**最終更新日**: 2025年11月30日
**バージョン**: 1.0
