# 開発工程別ツールマップ（Mermaid）

各 `docs/dev_process_開発工程_xx_*.md` の `##` セクションをレイヤーとして可視化したマップです。  
工程内で複数セクションに登場するツールは、最上部の「Common tools」レイヤーにまとめ、各セクション側では重複を除外しています。

各工程を個別のMermaidブロックに分割し、レンダラーでのエラーを避けています。

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P1[1_企画プロセス]
        direction TB
        P1_common["Common tools<br/>ClickUp"]
        subgraph P1s1[1.1 システム化構想の立案プロセス]
            direction TB
            P1s1_t["Miro<br/>FigJam<br/>Mural<br/>Whimsical<br/>MindMeister<br/>Notion<br/>Confluence<br/>Google Workspace<br/>Microsoft 365<br/>Microsoft Visio<br/>Lucidchart<br/>Draw.io (diagrams.net)<br/>Creately<br/>JIRA<br/>Trello<br/>Asana<br/>monday.com<br/>Basecamp"]
        end
        subgraph P1s2[1.2 システム化計画の立案プロセス]
            direction TB
            P1s2_t["Microsoft Project<br/>Wrike<br/>Planview<br/>Smartsheet<br/>Redmine<br/>OpenProject<br/>GanttProject<br/>Backlog<br/>Lychee Redmine<br/>Teamwork<br/>ProofHub<br/>Monday.com<br/>Airtable<br/>Atlassian Portfolio (Jira Align)"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P2[2_要件定義]
        direction TB
        P2_common["Common tools<br/>Confluence<br/>Figma<br/>Adobe XD<br/>Sketch<br/>Balsamiq<br/>Axure RP<br/>Jama Connect<br/>Lucidchart<br/>Microsoft Visio<br/>Draw.io (diagrams.net)<br/>Enterprise Architect<br/>Microsoft Excel<br/>Notion"]
        subgraph P2s1[1. 概要]
            direction TB
            P2s1_t["ONES Wiki<br/>GEAR.indigo<br/>VISLITE"]
        end
        subgraph P2s2[2. 業務分析]
            direction TB
            P2s2_t["Bizagi Modeler<br/>Process Street"]
        end
        subgraph P2s3[3. ユースケース分析（機能要件定義）]
            direction TB
            P2s3_t["Visual Paradigm<br/>PlantUML"]
        end
        subgraph P2s4[5. 帳票要件定義（機能要件定義）]
            direction TB
            P2s4_t["Crystal Reports<br/>Jaspersoft Studio<br/>BIRT (Business Intelligence and Reporting Tools)<br/>LibreOffice Calc"]
        end
        subgraph P2s5[6. ファイル要件定義（機能要件定義）]
            direction TB
            P2s5_t["CSV Spec Validator"]
        end
        subgraph P2s6[7. 概念モデリング（機能要件定義）]
            direction TB
            P2s6_t["ERDPlus<br/>MySQL Workbench<br/>pgModeler"]
        end
        subgraph P2s7[8. 外部システム連携要件定義（機能要件定義）]
            direction TB
            P2s7_t["Postman<br/>Swagger/OpenAPI"]
        end
        subgraph P2s8[9. バッチ処理要件定義（機能要件定義）]
            direction TB
            P2s8_t["JP1/AJS (Hitachi)"]
        end
        subgraph P2s9[10. システム方針検討（機能要件定義）]
            direction TB
            P2s9_t["C4 Model + PlantUML"]
        end
        subgraph P2s10[11. 非機能要件定義]
            direction TB
            P2s10_t["IPA 非機能要求グレード利用ガイド（Excel版）<br/>Microsoft Excel / Google Sheets"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P3[3_基本設計（アプリケーション）]
        direction TB
        P3_common["Common tools<br/>draw.io<br/>Lucidchart"]
        subgraph P3s1[1. 概要]
            direction TB
            P3s1_t["Next Design<br/>astah*<br/>Enterprise Architect<br/>draw.io (diagrams.net)<br/>PlantUML<br/>StarUML<br/>Visual Paradigm<br/>Cacoo<br/>Structurizr<br/>ArchiMate (Archi)"]
        end
        subgraph P3s2[2. 画面設計]
            direction TB
            P3s2_t["Figma<br/>Adobe XD<br/>MockFlow<br/>Sketch"]
        end
        subgraph P3s3[3. 帳票設計]
            direction TB
            P3s3_t["JasperReports<br/>Crystal Reports<br/>Apache POI<br/>BIRT<br/>LibreOffice"]
        end
        subgraph P3s4[4. ファイル設計]
            direction TB
            P3s4_t["VSCode<br/>Python/Pandas"]
        end
        subgraph P3s5[5. データベース論理設計]
            direction TB
            P3s5_t["MySQL Workbench<br/>ERDPlus<br/>pgAdmin<br/>Power Designer<br/>Dataedo"]
        end
        subgraph P3s6[6. 外部システムI/F設計]
            direction TB
            P3s6_t["Postman<br/>Swagger / OpenAPI<br/>Insomnia<br/>ReDoc<br/>API Blueprint"]
        end
        subgraph P3s7[7. バッチ設計]
            direction TB
            P3s7_t["Apache Airflow<br/>Spring Batch<br/>Quartz Scheduler<br/>Kubernetes CronJob<br/>GitHub Actions"]
        end
        subgraph P3s8[8. セキュリティ設計]
            direction TB
            P3s8_t["Microsoft Threat Modeling Tool<br/>OWASP Top 10<br/>JWT.io"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P4[3_基本設計（インフラ）]
        direction TB
        P4_common["Common tools<br/>Lucidchart<br/>Microsoft Visio<br/>draw.io<br/>Cacoo<br/>PlantUML<br/>CloudCraft<br/>AWS CloudFormation Designer<br/>Diagrams (Python)<br/>Excel / Google Sheets"]
        subgraph P4s1[成果物と有用なツール・ドキュメント]
            direction TB
            P4s1_t["Microsoft Threat Modeling Tool<br/>Miro<br/>Grafana<br/>Prometheus<br/>Datadog<br/>ELK Stack (Elasticsearch, Logstash, Kibana)<br/>CloudWatch（AWS）"]
        end
        subgraph P4s2[総合推奨ツール（生産性が高いもの Top 10）]
            direction TB
            P4s2_t["Hava.io<br/>Cloudockit"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P5[4_詳細設計（アプリケーション）]
        direction TB
        P5_common["Common tools<br/>Enterprise Architect<br/>PlantUML<br/>draw.io<br/>Swagger/OpenAPI<br/>Postman<br/>MySQL Workbench<br/>dbdiagram.io<br/>Docker<br/>VS Code"]
        subgraph P5s1[2. プログラム設計]
            direction TB
            P5s1_t["Mermaid<br/>Visual Paradigm<br/>StarUML"]
        end
        subgraph P5s2[3. API詳細設計]
            direction TB
            P5s2_t["Stoplight Studio<br/>ReDoc<br/>Insomnia"]
        end
        subgraph P5s3[4. 実装方針策定]
            direction TB
            P5s3_t["ESLint<br/>Prettier<br/>SonarQube<br/>Google Style Guides<br/>Markdown"]
        end
        subgraph P5s4[5. データベース物理設計]
            direction TB
            P5s4_t["DBeaver<br/>pgModeler"]
        end
        subgraph P5s5[6. 開発環境構築]
            direction TB
            P5s5_t["Vagrant<br/>JetBrains IDEs<br/>Git<br/>GitHub / GitLab"]
        end
        subgraph P5s6[総合推奨ツール（詳細設計 Top 10）]
            direction TB
            P5s6_t["Git / GitHub"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P6[6_詳細設計_インフラ]
        direction TB
        P6_common["Common tools<br/>AWS CloudFormation<br/>Azure Bicep"]
        subgraph P6s1[2. インフラ詳細設計]
            direction TB
            P6s1_t["Terraform<br/>Ansible<br/>Lucidchart<br/>Microsoft Visio<br/>Palo Alto Expedition<br/>AWS Well-Architected Tool<br/>Checkov<br/>Infracost"]
        end
        subgraph P6s2[3. Azure専用インフラ詳細設計ツール]
            direction TB
            P6s2_t["ARM Templates<br/>Azure Policy<br/>Azure Blueprints<br/>Azure DevOps<br/>Azure CLI<br/>Azure PowerShell<br/>Azure Resource Graph<br/>Azure Automation<br/>Azure Arc"]
        end
        subgraph P6s3[4. AWS専用インフラ詳細設計ツール]
            direction TB
            P6s3_t["AWS CDK<br/>AWS CLI<br/>AWS Service Catalog<br/>AWS Config<br/>AWS Systems Manager<br/>AWS Control Tower<br/>CloudFormation Designer<br/>AWS Application Composer<br/>AWS OpsWorks"]
        end
        subgraph P6s4[5. バージョン管理（全言語共通）]
            direction TB
            P6s4_t["Git<br/>GitHub<br/>GitLab"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P7[7_実装（アプリケーション）]
        direction TB
        subgraph P7s1[2. プログラミング]
            direction TB
            P7s1_t["IntelliJ IDEA<br/>Eclipse<br/>Maven<br/>Gradle<br/>Spring Boot<br/>JUnit 5<br/>Mockito<br/>SonarQube<br/>Checkstyle<br/>Google Java Format<br/>Visual Studio<br/>Rider<br/>MSBuild<br/>NuGet<br/>ASP.NET Core<br/>xUnit<br/>NUnit<br/>Moq<br/>ReSharper<br/>EditorConfig<br/>PyCharm<br/>VS Code + Python拡張<br/>pip<br/>Poetry<br/>pytest<br/>Black<br/>Ruff<br/>mypy<br/>Django<br/>pylint<br/>FastAPI<br/>VS Code<br/>WebStorm<br/>Node.js<br/>npm<br/>pnpm<br/>Yarn<br/>Vite<br/>Webpack<br/>React<br/>Next.js<br/>Vue.js<br/>Vitest<br/>Jest<br/>Playwright<br/>ESLint<br/>Prettier<br/>TypeScript"]
        end
        subgraph P7s2[5.1. AI コード補完（全言語共通）]
            direction TB
            P7s2_t["GitHub Copilot<br/>Cursor<br/>Amazon CodeWhisperer"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P8[8_インフラ構築]
        direction TB
        P8_common["Common tools<br/>Checkov<br/>OPA (Open Policy Agent)<br/>Terratest<br/>tfsec<br/>Terraform Validate<br/>Terraform Compliance<br/>Infracost"]
        subgraph P8s1[2. インフラ構築]
            direction TB
            P8s1_t["Terraform<br/>Ansible<br/>Pulumi<br/>Packer<br/>Terragrunt<br/>Crossplane<br/>Chef<br/>Puppet<br/>SaltStack<br/>Vagrant"]
        end
        subgraph P8s2[3. Azure専用インフラ構築ツール]
            direction TB
            P8s2_t["Azure Bicep<br/>ARM Templates<br/>Azure DevOps Pipelines<br/>Azure CLI<br/>Azure Automation<br/>Azure Resource Graph"]
        end
        subgraph P8s3[4. AWS専用インフラ構築ツール]
            direction TB
            P8s3_t["AWS CloudFormation<br/>AWS CDK<br/>AWS CodePipeline<br/>AWS CodeBuild<br/>AWS Systems Manager"]
        end
        subgraph P8s4[6. IaCコード検証・テスト（事前チェック）]
            direction TB
            P8s4_t["Azure Bicep Linter<br/>Azure Resource Manager Testing Toolkit (ARM-TTK)<br/>CDK-nag<br/>CloudFormation Guard<br/>AWS CDK Assertions"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P9[8-1_CI/CD構築]
        direction TB
        subgraph P9s1[4. 推奨ツール（マルチクラウド対応 CI/CD - Top 10）]
            direction TB
            P9s1_t["GitHub Actions<br/>GitLab CI/CD<br/>Jenkins<br/>CircleCI<br/>ArgoCD<br/>Tekton<br/>Travis CI<br/>Drone<br/>TeamCity<br/>Bamboo"]
        end
        subgraph P9s2[5. Azure専用CI/CDツール]
            direction TB
            P9s2_t["Azure DevOps Pipelines<br/>Azure Container Registry Tasks (ACR Tasks)<br/>Azure Release Pipelines"]
        end
        subgraph P9s3[6. AWS専用CI/CDツール]
            direction TB
            P9s3_t["AWS CodePipeline<br/>AWS CodeBuild<br/>AWS CodeDeploy<br/>AWS Amplify Hosting"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P10[9_テスト（アプリケーション）]
        direction TB
        subgraph P10s1[9.1 単体テスト（ユニットテスト）]
            direction TB
            P10s1_t["JUnit 5 / TestNG<br/>pytest<br/>Jest<br/>xUnit.net<br/>Go testing (標準)<br/>PHPUnit<br/>Vitest<br/>Mocha + Chai<br/>JaCoCo<br/>Coverage.py<br/>Istanbul / nyc<br/>OpenCover<br/>Codecov"]
        end
        subgraph P10s2[9.2 結合テスト（統合テスト）]
            direction TB
            P10s2_t["Postman<br/>REST Assured<br/>Insomnia<br/>SoapUI / ReadyAPI<br/>Katalon Studio<br/>Swagger / OpenAPI<br/>pyresttest<br/>Apigee<br/>Playwright<br/>Cypress<br/>Selenium<br/>TestCafe<br/>Puppeteer<br/>WebdriverIO"]
        end
        subgraph P10s3[9.4 非機能テスト（性能・セキュリティテスト）]
            direction TB
            P10s3_t["JMeter<br/>Gatling<br/>k6<br/>Locust<br/>Artillery<br/>LoadRunner / Unified Functional Testing<br/>Apache JMeter Visual<br/>ApacheBench (ab)<br/>OWASP ZAP<br/>Burp Suite Community<br/>Snyk<br/>Checkmarx / CxAST<br/>SonarQube / SonarCloud<br/>OWASP Dependency-Check"]
        end
        subgraph P10s4[9.5 テスト管理・レポーティングツール]
            direction TB
            P10s4_t["TestRail<br/>Zephyr for Jira<br/>HP ALM / Micro Focus ALM<br/>PractiTest<br/>Azure Test Plans<br/>qTest<br/>Tautoko<br/>DBmaestro<br/>DATADOPE"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P11[10_テスト（インフラ）]
        direction TB
        P11_common["Common tools<br/>Terratest<br/>InSpec<br/>Azure CLI / AWS CLI<br/>k6"]
        subgraph P11s1[10.1 インフラ単体テスト]
            direction TB
            P11s1_t["Serverspec<br/>Azure Resource Manager Testing Toolkit<br/>AWS CDK Assertions<br/>Kitchen-Terraform<br/>Pester<br/>Goss<br/>Pulumi Testing"]
        end
        subgraph P11s2[10.2 インフラ結合テスト]
            direction TB
            P11s2_t["Azure Network Watcher<br/>AWS VPC Reachability Analyzer<br/>curl / wget<br/>nc (netcat)<br/>Postman / Newman<br/>Pytest + Requests"]
        end
        subgraph P11s3[10.3 インフラ総合テスト]
            direction TB
            P11s3_t["Azure Load Testing<br/>AWS Fault Injection Simulator (FIS)<br/>Chaos Mesh<br/>JMeter<br/>Locust<br/>Gatling<br/>Microsoft Defender for Cloud<br/>Prowler<br/>Azure Monitor / CloudWatch"]
        end
        subgraph P11s4[参考: IaC開発・コンテナ・監視・セキュリティツール]
            direction TB
            P11s4_t["Terraform<br/>Azure Bicep<br/>AWS CDK<br/>Pulumi<br/>Ansible<br/>Docker<br/>Kubernetes<br/>Helm<br/>Amazon EKS<br/>Azure AKS<br/>Azure Monitor<br/>Amazon CloudWatch<br/>Prometheus + Grafana<br/>Datadog<br/>ELK Stack<br/>Snyk<br/>Trivy<br/>Checkov<br/>SonarQube"]
        end
    end
```

```mermaid
%%{init: {'flowchart': {'htmlLabels': true}}}%%
flowchart TB
    subgraph P12[11_導入（アプリケーション・インフラ）]
        direction TB
        P12_common["Common tools<br/>Flyway<br/>AWS Database Migration Service<br/>GitHub Actions<br/>Docker<br/>Kubernetes<br/>Datadog<br/>Prometheus + Grafana<br/>CloudWatch<br/>Jira Service Management"]
        subgraph P12s1[2. データ移行]
            direction TB
            P12s1_t["Liquibase<br/>Talend<br/>Apache NiFi<br/>Informatica<br/>Airbyte<br/>dbt (data build tool)<br/>Fivetran"]
        end
        subgraph P12s2[3. デプロイメント・リリース]
            direction TB
            P12s2_t["GitLab CI/CD<br/>AWS CodePipeline<br/>Jenkins<br/>Argo CD<br/>HashiCorp Terraform"]
        end
        subgraph P12s3[3.1. 受入テスト]
            direction TB
            P12s3_t["TestRail<br/>Xray (Jira Plugin)<br/>Cucumber<br/>SpecFlow<br/>Selenium<br/>Playwright<br/>Cypress<br/>Postman<br/>Robot Framework<br/>Azure Test Plans"]
        end
        subgraph P12s4[4. 運用監視・ログ管理]
            direction TB
            P12s4_t["ELK Stack<br/>New Relic<br/>Sentry<br/>Azure Monitor<br/>Splunk<br/>Zabbix<br/>ServiceNow<br/>PagerDuty<br/>Freshservice<br/>OpsGenie<br/>BMC Remedy<br/>ManageEngine ServiceDesk Plus<br/>Zendesk"]
        end
        subgraph P12s5[5. 導入フェーズ 総合推奨ツール（Top 10）]
            direction TB
            P12s5_t["Terraform"]
        end
    end
```

> 図は既存ドキュメントをスキャンして自動生成しています。セクションやツールを追加・変更した場合は、このファイルを再生成してください（現状スクリプトはリポジトリ未同梱）。
