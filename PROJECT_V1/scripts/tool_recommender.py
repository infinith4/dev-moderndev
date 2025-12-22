#!/usr/bin/env python3
"""
ツール推薦システム

プロジェクト要件チェックリスト.mdで選択された項目に基づいて、
docs/ツール配下から適切なツールを推薦するスクリプト
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Tool:
    """ツール情報"""
    name: str
    category: str
    file_path: str
    description: str = ""
    price: str = ""  # 🟢無料 / 🟡一部無料 / 🔴有料
    platform: str = "All"  # AWS, Azure, GCP, All
    language: str = "All"  # C#, Java, Python, TypeScript, All


@dataclass
class Requirement:
    """要件情報"""
    section: str
    subsection: str
    text: str
    is_checked: bool


@dataclass
class TechStack:
    """技術スタック選択情報"""
    cloud_platforms: Set[str]  # AWS, Azure, GCP
    languages: Set[str]  # C#, Java, Python, TypeScript
    frameworks: Set[str]
    databases: Set[str]
    messaging: Set[str]
    caching: Set[str]
    monitoring: Set[str]
    tools: Set[str]


class ToolRecommender:
    """ツール推薦エンジン"""

    def __init__(self, tools_dir: str = "/src/docs/ツール",
                 checklist_path: str = "/src/PROJECT_V1/プロジェクト要件チェックリスト_template.md"):
        self.tools_dir = Path(tools_dir)
        self.checklist_path = Path(checklist_path)
        self.tools: List[Tool] = []
        self.requirements: List[Requirement] = []
        self.tech_stack: TechStack = TechStack(
            cloud_platforms=set(),
            languages=set(),
            frameworks=set(),
            databases=set(),
            messaging=set(),
            caching=set(),
            monitoring=set(),
            tools=set()
        )

        # キーワードマッピング: 要件キーワード -> ツールカテゴリ/ツール名
        self.keyword_mappings = self._build_keyword_mappings()

        # ツールのプラットフォーム/言語メタデータ
        self.tool_metadata = self._build_tool_metadata()

    def _build_tool_metadata(self) -> Dict[str, Dict[str, str]]:
        """ツール名とプラットフォーム/言語/データベースメタデータのマッピング"""
        return {
            # AWS専用ツール
            "AWS_CloudFormation": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_CloudFormation_Designer": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_CodeDeploy": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_DMS": {"platform": "AWS", "language": "All", "database": "All"},
            "CloudWatch": {"platform": "AWS", "language": "All", "database": "All"},
            "X-Ray": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_Cognito": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_SQS": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_SNS": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_Kinesis": {"platform": "AWS", "language": "All", "database": "All"},
            "AWS_ElastiCache": {"platform": "AWS", "language": "All", "database": "All"},
            "Amazon_CloudFront": {"platform": "AWS", "language": "All", "database": "All"},

            # Azure専用ツール
            "Azure_Bicep": {"platform": "Azure", "language": "All", "database": "All"},
            "Bicep": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_DevOps": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_Pipelines": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_Data_Factory": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_Monitor": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_AD": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_Service_Bus": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_Event_Hubs": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_Cache": {"platform": "Azure", "language": "All", "database": "All"},
            "Azure_CDN": {"platform": "Azure", "language": "All", "database": "All"},
            "Application_Insights": {"platform": "Azure", "language": "All", "database": "All"},

            # GCP専用ツール
            "Google_Cloud": {"platform": "GCP", "language": "All", "database": "All"},
            "Cloud_Functions": {"platform": "GCP", "language": "All", "database": "All"},
            "Pub_Sub": {"platform": "GCP", "language": "All", "database": "All"},

            # クロスプラットフォーム (IaC)
            "Terraform": {"platform": "All", "language": "All", "database": "All"},
            "Pulumi": {"platform": "All", "language": "All", "database": "All"},
            "Ansible": {"platform": "All", "language": "All", "database": "All"},
            "Puppet": {"platform": "All", "language": "All", "database": "All"},
            "Chef": {"platform": "All", "language": "All", "database": "All"},

            # 言語依存ツール - Java
            "JUnit": {"platform": "All", "language": "Java", "database": "All"},
            "Mockito": {"platform": "All", "language": "Java", "database": "All"},
            "JaCoCo": {"platform": "All", "language": "Java", "database": "All"},
            "Maven": {"platform": "All", "language": "Java", "database": "All"},
            "Gradle": {"platform": "All", "language": "Java", "database": "All"},
            "Spring": {"platform": "All", "language": "Java", "database": "All"},
            "Hibernate": {"platform": "All", "language": "Java", "database": "All"},
            "Checkstyle": {"platform": "All", "language": "Java", "database": "All"},
            "REST_Assured": {"platform": "All", "language": "Java", "database": "All"},
            "Gatling": {"platform": "All", "language": "Java", "database": "All"},

            # 言語依存ツール - C#
            "xUnit": {"platform": "All", "language": "C#", "database": "All"},
            "NUnit": {"platform": "All", "language": "C#", "database": "All"},
            "Moq": {"platform": "All", "language": "C#", "database": "All"},
            "Entity_Framework": {"platform": "All", "language": "C#", "database": "All"},
            "StyleCop": {"platform": "All", "language": "C#", "database": "All"},

            # 言語依存ツール - Python
            "pytest": {"platform": "All", "language": "Python", "database": "All"},
            "Coverage.py": {"platform": "All", "language": "Python", "database": "All"},
            "Pylint": {"platform": "All", "language": "Python", "database": "All"},
            "Black": {"platform": "All", "language": "Python", "database": "All"},
            "Alembic": {"platform": "All", "language": "Python", "database": "All"},
            "SQLAlchemy": {"platform": "All", "language": "Python", "database": "All"},
            "Locust": {"platform": "All", "language": "Python", "database": "All"},

            # 言語依存ツール - TypeScript/JavaScript
            "Jest": {"platform": "All", "language": "TypeScript", "database": "All"},
            "Mocha": {"platform": "All", "language": "TypeScript", "database": "All"},
            "ESLint": {"platform": "All", "language": "TypeScript", "database": "All"},
            "Prettier": {"platform": "All", "language": "TypeScript", "database": "All"},
            "Istanbul": {"platform": "All", "language": "TypeScript", "database": "All"},
            "Cypress": {"platform": "All", "language": "TypeScript", "database": "All"},
            "Playwright": {"platform": "All", "language": "TypeScript", "database": "All"},
            "Puppeteer": {"platform": "All", "language": "TypeScript", "database": "All"},

            # データベース固有ツール - MySQL
            "MySQL_Workbench": {"platform": "All", "language": "All", "database": "MySQL"},

            # データベース固有ツール - PostgreSQL
            "pgAdmin": {"platform": "All", "language": "All", "database": "PostgreSQL"},

            # データベース固有ツール - SQL Server
            "SQL_Server_Management_Studio": {"platform": "All", "language": "All", "database": "SQL Server"},
            "SSMS": {"platform": "All", "language": "All", "database": "SQL Server"},

            # データベース固有ツール - Oracle
            "SQL_Developer": {"platform": "All", "language": "All", "database": "Oracle"},

            # データベース固有ツール - MongoDB
            "MongoDB_Compass": {"platform": "All", "language": "All", "database": "MongoDB"},

            # クロスデータベースツール（複数のRDBMSに対応）
            "DBeaver": {"platform": "All", "language": "All", "database": "All"},
            "ERDPlus": {"platform": "All", "language": "All", "database": "All"},
            "Flyway": {"platform": "All", "language": "All", "database": "All"},
            "Liquibase": {"platform": "All", "language": "All", "database": "All"},
        }

    def _build_keyword_mappings(self) -> Dict[str, List[str]]:
        """要件キーワードとツールカテゴリ/ツール名のマッピングを構築"""
        return {
            # 設計・モデリング
            "ビジネスプロセス": ["Draw.io", "Lucidchart", "PlantUML", "Microsoft_Visio"],
            "業務フロー": ["Draw.io", "Lucidchart", "Microsoft_Visio"],
            "ユースケース図": ["PlantUML", "Draw.io", "Lucidchart"],
            "画面遷移図": ["Figma", "Adobe_XD", "Draw.io"],
            "画面レイアウト": ["Figma", "Adobe_XD"],
            "ワイヤーフレーム": ["Figma", "Adobe_XD", "Draw.io"],
            "UI/UXデザイン": ["Figma", "Adobe_XD"],
            "帳票": ["JasperReports", "LibreOffice", "Microsoft_Excel"],
            "概念モデル": ["Draw.io", "ERDPlus", "PlantUML"],
            "ER図": ["ERDPlus", "MySQL_Workbench", "Draw.io"],
            "外部システム": ["Postman", "Swagger", "Apache_Kafka", "RabbitMQ"],
            "システム構成図": ["Draw.io", "Lucidchart", "Microsoft_Visio"],
            "ソフトウェア構成図": ["PlantUML", "Draw.io", "Lucidchart"],

            # アプリケーション設計
            "クラス図": ["PlantUML", "Draw.io", "Lucidchart"],
            "シーケンス図": ["PlantUML", "Draw.io"],
            "状態遷移図": ["PlantUML", "Draw.io"],
            "コンポーネント図": ["PlantUML", "Draw.io"],
            "論理ER図": ["ERDPlus", "MySQL_Workbench", "Draw.io"],
            "テーブル定義": ["ERDPlus", "MySQL_Workbench"],
            "物理ER図": ["MySQL_Workbench", "ERDPlus"],
            "インデックス設計": ["MySQL_Workbench"],

            # データベース
            "データベース": ["MySQL_Workbench", "Flyway", "ERDPlus"],
            "マイグレーション": ["Flyway", "Liquibase", "Alembic"],
            "スキーマ": ["MySQL_Workbench", "Flyway"],

            # API
            "API": ["Postman", "Swagger", "Stoplight_Studio", "Apigee"],
            "REST": ["Postman", "Swagger"],
            "GraphQL": ["Postman"],
            "API仕様": ["Swagger", "Stoplight_Studio", "ReDoc"],
            "APIドキュメント": ["Swagger", "ReDoc", "Postman"],
            "APIテスト": ["Postman", "REST_Assured", "Pact"],

            # バッチ処理
            "バッチ": ["Apache_Airflow"],
            "ワークフロー": ["Apache_Airflow"],
            "スケジューリング": ["Apache_Airflow"],

            # インフラ設計・構築
            "Infrastructure as Code": ["Terraform", "AWS_CloudFormation", "Azure_Bicep", "Pulumi"],
            "IaC": ["Terraform", "AWS_CloudFormation", "Azure_Bicep"],
            "インフラ自動化": ["Terraform", "Ansible", "Puppet", "Chef"],
            "構成管理": ["Ansible", "Puppet", "Chef"],
            "コンテナ": ["Docker", "Kubernetes", "Podman"],
            "オーケストレーション": ["Kubernetes", "Docker_Compose"],
            "Kubernetes": ["Kubernetes", "Helm", "ArgoCD"],

            # CI/CD
            "CI/CD": ["GitHub_Actions", "GitLab_CI_CD", "Jenkins", "Azure_DevOps"],
            "継続的インテグレーション": ["Jenkins", "GitHub_Actions", "GitLab_CI_CD"],
            "自動ビルド": ["GitHub_Actions", "Jenkins", "GitLab_CI_CD"],
            "自動デプロイ": ["GitHub_Actions", "ArgoCD", "Spinnaker"],
            "パイプライン": ["Jenkins", "GitHub_Actions", "GitLab_CI_CD", "Azure_DevOps"],

            # テスト
            "単体テスト": ["Jest", "JUnit", "pytest", "xUnit", "Mocha"],
            "ユニットテスト": ["Jest", "JUnit", "pytest", "xUnit"],
            "結合テスト": ["Postman", "REST_Assured"],
            "統合テスト": ["Selenium", "Cypress", "Playwright"],
            "E2Eテスト": ["Cypress", "Playwright", "Selenium", "Puppeteer"],
            "負荷テスト": ["JMeter", "Gatling", "k6", "Locust"],
            "性能テスト": ["JMeter", "Gatling", "k6"],
            "セキュリティテスト": ["OWASP_ZAP", "Burp_Suite", "Nessus"],
            "テストカバレッジ": ["Jest", "JaCoCo", "Coverage.py", "Istanbul"],
            "モック": ["Mockito", "Moq", "WireMock", "MockServer"],

            # コード品質
            "静的コード解析": ["SonarQube", "SonarCloud", "CodeClimate"],
            "Linter": ["ESLint", "Pylint", "Checkstyle", "StyleCop"],
            "コーディング規約": ["ESLint", "Pylint", "Prettier", "Black"],
            "コードレビュー": ["GitHub", "GitLab", "Azure_DevOps", "Bitbucket"],

            # セキュリティ
            "脆弱性診断": ["OWASP_ZAP", "Snyk", "Trivy", "Checkov"],
            "セキュリティスキャン": ["Snyk", "OWASP_ZAP", "Trivy", "Checkov"],
            "依存関係": ["Snyk", "Dependabot", "OWASP_Dependency_Check"],
            "IaCセキュリティ": ["Checkov", "tfsec", "Terrascan"],

            # 監視・ロギング
            "監視": ["Prometheus", "Grafana", "Datadog", "New_Relic"],
            "ロギング": ["ELK", "Splunk", "Fluentd", "CloudWatch"],
            "メトリクス": ["Prometheus", "Grafana", "CloudWatch", "Azure_Monitor"],
            "トレーシング": ["Jaeger", "Zipkin", "X-Ray", "OpenTelemetry"],
            "APM": ["Application_Insights", "New_Relic", "Datadog", "Dynatrace"],

            # プロジェクト管理
            "プロジェクト管理": ["Jira", "Azure_DevOps_Boards", "GitHub_Projects", "Trello"],
            "課題管理": ["Jira", "GitHub_Issues", "Azure_DevOps_Boards"],
            "タスク管理": ["Jira", "Trello", "Asana"],

            # ドキュメント
            "ドキュメント": ["Confluence", "Notion", "GitHub_Wiki", "ReadTheDocs"],
            "アーキテクチャ図": ["draw.io", "Lucidchart", "PlantUML", "Mermaid"],

            # インフラテスト
            "インフラテスト": ["Terratest", "InSpec", "ServerSpec", "Kitchen"],
            "構成テスト": ["InSpec", "ServerSpec", "Testinfra"],
            "カオスエンジニアリング": ["Chaos_Monkey", "Gremlin", "LitmusChaos"],

            # リリース・導入
            "リリース": ["GitHub_Actions", "GitLab_CI_CD", "Spinnaker", "ArgoCD"],
            "デプロイ": ["Spinnaker", "ArgoCD", "Flux", "AWS_CodeDeploy"],
            "データ移行": ["AWS_DMS", "Azure_Data_Factory", "Flyway", "Liquibase"],
        }

    def load_tools(self) -> None:
        """ツールディレクトリからすべてのツール情報を読み込む"""
        print(f"📚 ツール情報を読み込み中: {self.tools_dir}")

        for md_file in self.tools_dir.rglob("*.md"):
            # 索引ファイルや一覧ファイルは除外
            if md_file.name in ["ツール一覧.md", "ツール索引.md", "カテゴリ統合計画.md", "マイグレーションログ.md"]:
                continue

            tool_name = md_file.stem
            category = md_file.parent.name

            # ツール詳細を読み込み
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 概要セクションを抽出
                    description_match = re.search(r'## 概要\s*\n\s*(.+?)(?:\n##|\Z)', content, re.DOTALL)
                    description = description_match.group(1).strip() if description_match else ""
                    # 最初の段落のみ取得
                    description = description.split('\n\n')[0] if description else ""
            except Exception as e:
                print(f"  ⚠️  {md_file}: 読み込みエラー - {e}")
                description = ""

            tool = Tool(
                name=tool_name,
                category=category,
                file_path=str(md_file.relative_to(Path("/src/docs"))),
                description=description
            )
            self.tools.append(tool)

        print(f"✅ {len(self.tools)} 個のツールを読み込みました\n")

    def load_checklist(self) -> None:
        """プロジェクト要件チェックリストを読み込む"""
        print(f"📋 チェックリストを読み込み中: {self.checklist_path}")

        with open(self.checklist_path, 'r', encoding='utf-8') as f:
            content = f.read()

        current_section = ""
        current_subsection = ""

        for line in content.split('\n'):
            # セクション検出
            section_match = re.match(r'^## (\d+\..+)$', line)
            if section_match:
                current_section = section_match.group(1)
                continue

            # サブセクション検出
            subsection_match = re.match(r'^### (.+)$', line)
            if subsection_match:
                current_subsection = subsection_match.group(1)
                continue

            # チェックボックス検出
            checkbox_match = re.match(r'^- \[([ x])\] (.+)$', line)
            if checkbox_match:
                is_checked = checkbox_match.group(1) == 'x'
                text = checkbox_match.group(2)

                req = Requirement(
                    section=current_section,
                    subsection=current_subsection,
                    text=text,
                    is_checked=is_checked
                )
                self.requirements.append(req)

        checked_count = sum(1 for req in self.requirements if req.is_checked)
        print(f"✅ {len(self.requirements)} 個の要件を読み込みました（チェック済み: {checked_count}）\n")

        # 技術スタック (セクション12) を抽出
        self._parse_tech_stack()

    def _parse_tech_stack(self) -> None:
        """セクション12から技術スタック選択を抽出"""
        print("🔧 技術スタック (セクション12) を解析中...")

        for req in self.requirements:
            if not req.section.startswith("12."):
                continue

            if not req.is_checked:
                continue

            text_lower = req.text.lower()

            # クラウドプラットフォーム検出
            if any(platform in text_lower for platform in ["aws", "amazon"]):
                self.tech_stack.cloud_platforms.add("AWS")
            if "azure" in text_lower:
                self.tech_stack.cloud_platforms.add("Azure")
            if any(platform in text_lower for platform in ["gcp", "google cloud"]):
                self.tech_stack.cloud_platforms.add("GCP")

            # プログラミング言語検出
            if "c#" in text_lower or ".net" in text_lower:
                self.tech_stack.languages.add("C#")
            if "java" in text_lower and "javascript" not in text_lower:
                self.tech_stack.languages.add("Java")
            if "python" in text_lower:
                self.tech_stack.languages.add("Python")
            if "typescript" in text_lower or "javascript" in text_lower:
                self.tech_stack.languages.add("TypeScript")

            # データベース検出 (セクション12.3.5)
            if "postgresql" in text_lower:
                self.tech_stack.databases.add("PostgreSQL")
            if "mysql" in text_lower:
                self.tech_stack.databases.add("MySQL")
            if "sql server" in text_lower:
                self.tech_stack.databases.add("SQL Server")
            if "oracle" in text_lower:
                self.tech_stack.databases.add("Oracle")
            if "mariadb" in text_lower:
                self.tech_stack.databases.add("MariaDB")
            if "mongodb" in text_lower:
                self.tech_stack.databases.add("MongoDB")
            if "redis" in text_lower and "データストア" in req.text:
                self.tech_stack.databases.add("Redis")
            if "dynamodb" in text_lower:
                self.tech_stack.databases.add("DynamoDB")
            if "cosmosdb" in text_lower:
                self.tech_stack.databases.add("CosmosDB")
            if "cassandra" in text_lower:
                self.tech_stack.databases.add("Cassandra")

            # ツール名を技術スタックに追加
            tool_keywords = {
                "Swagger": "Swagger",
                "OpenAPI": "Swagger",
                "Notion": "Notion",
                "Slack": "Slack",
                "GitHub": "GitHub",
                "PlantUML": "PlantUML",
                "Mermaid": "Mermaid",
                "draw.io": "draw.io",
                "Service Bus": "Azure_Service_Bus",
                "RBAC": "RBAC"
            }

            for keyword, tool_name in tool_keywords.items():
                if keyword.lower() in text_lower:
                    self.tech_stack.tools.add(tool_name)

        # 抽出結果を表示
        if self.tech_stack.cloud_platforms:
            print(f"  ☁️  クラウド: {', '.join(sorted(self.tech_stack.cloud_platforms))}")
        if self.tech_stack.languages:
            print(f"  💻 言語: {', '.join(sorted(self.tech_stack.languages))}")
        if self.tech_stack.databases:
            print(f"  🗄️  データベース: {', '.join(sorted(self.tech_stack.databases))}")
        if self.tech_stack.tools:
            print(f"  🔧 ツール: {', '.join(sorted(self.tech_stack.tools))}")
        if not any([self.tech_stack.cloud_platforms, self.tech_stack.languages, self.tech_stack.databases, self.tech_stack.tools]):
            print("  ⚠️  技術スタック選択が検出されませんでした")
        print()

    def recommend_tools(self) -> Dict[str, List[Tuple[Tool, float, str]]]:
        """チェックされた要件に基づいてツールを推薦"""
        print("🔍 ツール推薦を開始...")

        recommendations = defaultdict(list)

        for req in self.requirements:
            if not req.is_checked:
                continue

            # 要件テキストからキーワードを抽出してマッチング
            matched_tools = self._match_tools_for_requirement(req)

            if matched_tools:
                key = f"{req.section} > {req.subsection}"
                for tool, score, reason in matched_tools:
                    # 重複を避けつつ追加
                    if not any(t.name == tool.name for t, _, _ in recommendations[key]):
                        recommendations[key].append((tool, score, reason))

        # スコアでソート
        for key in recommendations:
            recommendations[key].sort(key=lambda x: x[1], reverse=True)

        print(f"✅ 推薦完了\n")
        return dict(recommendations)

    def _match_tools_for_requirement(self, req: Requirement) -> List[Tuple[Tool, float, str]]:
        """個別の要件に対するツールマッチング（技術スタックフィルタリング適用）"""
        matched = []
        req_text = req.text.lower()

        # テストセクション（9, 10）では設計・モデリングツールを除外
        is_test_section = req.section.startswith("9.") or req.section.startswith("10.")
        excluded_design_tools = ["Draw.io", "Lucidchart", "Microsoft_Visio", "PlantUML", "Figma", "Adobe_XD"]

        # キーワードマッピングからマッチング
        for keyword, tool_names in self.keyword_mappings.items():
            if keyword.lower() in req_text:
                # まず、セクション12で選択済みのツールを優先的に推薦
                selected_tools_for_keyword = []
                other_tools_for_keyword = []

                for tool_name in tool_names:
                    # テストセクションで設計ツールを除外
                    if is_test_section and tool_name in excluded_design_tools:
                        continue

                    # ツール名を正規化（アンダースコアをスペースに）
                    normalized_tool_name = tool_name.replace('_', ' ')

                    # マッチするツールを検索
                    for tool in self.tools:
                        normalized_check_name = tool.name.replace('_', ' ')
                        if (tool.name == tool_name or
                            normalized_check_name.lower() == normalized_tool_name.lower() or
                            tool_name.lower() in tool.name.lower()):

                            # 技術スタックとの互換性チェック
                            is_compatible, compatibility_reason = self._is_tool_compatible(tool)
                            if not is_compatible:
                                continue  # 互換性がない場合はスキップ

                            # スコア計算（キーワードの重要度に基づく）
                            score = 1.0
                            if any(kw in req_text for kw in ['必要', '実施', '作成']):
                                score += 0.5

                            # セクション12で選択済みかチェック
                            is_selected = self._is_tool_selected_in_section12(tool)

                            # マッチ理由を技術スタック考慮版に更新
                            reason = f"キーワード '{keyword}' にマッチ"
                            if compatibility_reason:
                                reason += f" + {compatibility_reason}"
                            if is_selected:
                                reason += " + セクション12で選択済み"
                                score += 2.0  # 選択済みツールには高いスコアを付与
                                selected_tools_for_keyword.append((tool, score, reason))
                            else:
                                other_tools_for_keyword.append((tool, score, reason))

                # 選択済みツールがある場合は、それのみを推薦
                # ない場合は、すべてのツールを推薦
                if selected_tools_for_keyword:
                    matched.extend(selected_tools_for_keyword)
                else:
                    matched.extend(other_tools_for_keyword)

        return matched

    def _is_tool_selected_in_section12(self, tool: Tool) -> bool:
        """ツールがセクション12で選択されているかチェック"""
        # ツール名の正規化（異なる表記に対応）
        tool_name_variants = [
            tool.name,
            tool.name.replace('_', ' '),
            tool.name.replace('_', ''),
            tool.name.lower(),
            tool.name.replace('_', ' ').lower(),
        ]

        # tech_stack.tools に含まれているかチェック
        for selected_tool in self.tech_stack.tools:
            selected_variants = [
                selected_tool,
                selected_tool.replace('_', ' '),
                selected_tool.replace('_', ''),
                selected_tool.lower(),
                selected_tool.replace('_', ' ').lower(),
            ]

            # いずれかのバリアントがマッチするかチェック
            for tool_variant in tool_name_variants:
                for selected_variant in selected_variants:
                    if tool_variant.lower() == selected_variant.lower():
                        return True

        return False

    def _is_tool_compatible(self, tool: Tool) -> Tuple[bool, str]:
        """
        ツールが選択された技術スタックと互換性があるかチェック

        Returns:
            (is_compatible, reason): 互換性の有無と理由
        """
        # ツールのメタデータを取得
        metadata = self.tool_metadata.get(tool.name, {"platform": "All", "language": "All", "database": "All"})
        tool_platform = metadata.get("platform", "All")
        tool_language = metadata.get("language", "All")
        tool_database = metadata.get("database", "All")

        reasons = []

        # プラットフォームフィルタリング
        if self.tech_stack.cloud_platforms and tool_platform != "All":
            if tool_platform not in self.tech_stack.cloud_platforms:
                return (False, "")  # 選択されたクラウドプラットフォームと不一致
            else:
                reasons.append(f"{tool_platform}対応")

        # 言語フィルタリング
        if self.tech_stack.languages and tool_language != "All":
            if tool_language not in self.tech_stack.languages:
                return (False, "")  # 選択された言語と不一致
            else:
                reasons.append(f"{tool_language}対応")

        # データベースフィルタリング
        if self.tech_stack.databases and tool_database != "All":
            if tool_database not in self.tech_stack.databases:
                return (False, "")  # 選択されたデータベースと不一致
            else:
                reasons.append(f"{tool_database}対応")

        # 理由をまとめる
        compatibility_reason = " + ".join(reasons) if reasons else ""

        return (True, compatibility_reason)

    def generate_report(self, recommendations: Dict[str, List[Tuple[Tool, float, str]]]) -> str:
        """推薦レポートを生成"""
        # ユニークなツール数を計算
        all_tool_names = set()
        for tools in recommendations.values():
            for tool, _, _ in tools:
                all_tool_names.add(tool.name)

        checked_count = sum(1 for req in self.requirements if req.is_checked)

        report_lines = [
            "# ツール推薦レポート",
            "",
            f"**生成日時**: {self._get_timestamp()}",
            "",
            "## 概要",
            "",
            f"チェックされた要件 **{checked_count}件** に対して、**{len(all_tool_names)}個** のツールを推薦しています。",
            "",
        ]

        # 技術スタック情報を追加
        if any([self.tech_stack.cloud_platforms, self.tech_stack.languages, self.tech_stack.databases, self.tech_stack.tools]):
            report_lines.append("## 選択された技術スタック (セクション12)")
            report_lines.append("")

            if self.tech_stack.cloud_platforms:
                platforms = ", ".join(sorted(self.tech_stack.cloud_platforms))
                report_lines.append(f"- **クラウドプラットフォーム**: {platforms}")

            if self.tech_stack.languages:
                languages = ", ".join(sorted(self.tech_stack.languages))
                report_lines.append(f"- **プログラミング言語**: {languages}")

            if self.tech_stack.databases:
                databases = ", ".join(sorted(self.tech_stack.databases))
                report_lines.append(f"- **データベース**: {databases}")

            if self.tech_stack.tools:
                tools = ", ".join(sorted(self.tech_stack.tools))
                report_lines.append(f"- **選択ツール**: {tools}")

            report_lines.append("")
            report_lines.append("> 💡 **フィルタリングについて**: 以下の推薦ツールは、選択された技術スタックと互換性のあるもののみに絞り込まれています。")
            report_lines.append("")

        report_lines.extend([
            "---",
            "",
        ])

        if not recommendations:
            report_lines.extend([
                "## 結果",
                "",
                "⚠️ チェックされた要件が見つかりませんでした。",
                "プロジェクト要件チェックリスト.md で必要な項目にチェック `[x]` を入れてください。",
                ""
            ])
        else:
            report_lines.append("## 推薦ツール一覧")
            report_lines.append("")

            for section_key, tools in recommendations.items():
                report_lines.append(f"### {section_key}")
                report_lines.append("")

                # 表形式のヘッダー
                report_lines.append("| ツール名 | カテゴリ | スコア | マッチ理由 | 概要 |")
                report_lines.append("|----------|----------|--------|------------|------|")

                for tool, score, reason in tools[:10]:  # 上位10件
                    # 概要を60文字に制限
                    short_desc = ""
                    if tool.description:
                        short_desc = tool.description[:60] + "..." if len(tool.description) > 60 else tool.description
                        # 改行とパイプ文字をエスケープ
                        short_desc = short_desc.replace('\n', ' ').replace('|', '\\|')

                    # マッチ理由内のパイプ文字をエスケープ
                    reason_escaped = reason.replace('|', '\\|')

                    # ツール名をリンク化
                    tool_link = f"[{tool.name}](../{tool.file_path})"

                    report_lines.append(f"| {tool_link} | {tool.category} | {score:.1f} | {reason_escaped} | {short_desc} |")

                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")

        # サマリーセクション
        report_lines.extend([
            "## ツール選択ガイド",
            "",
            "### 次のステップ",
            "",
            "1. **ツール詳細の確認**: 各ツールの詳細ページで機能・料金・メリット/デメリットを確認",
            "2. **技術スタックとの整合性確認**: セクション12の技術スタック選択と照らし合わせ",
            "3. **プロジェクト要件との適合性評価**: プロジェクト固有の要件に合致するか検証",
            "4. **ツール選定会議**: チームで推薦ツールを議論・決定",
            "5. **POC実施**: 候補ツールでProof of Conceptを実施",
            "",
            "### 注意事項",
            "",
            "- このレポートは自動生成された推薦であり、最終的な選定はプロジェクト要件に基づいて判断してください",
            "- 料金・ライセンス条件は必ず公式サイトで最新情報を確認してください",
            "- オープンソースツールでもサポートが必要な場合はエンタープライズ版を検討してください",
            "",
            "---",
            "",
            "**END OF REPORT**",
        ])

        return '\n'.join(report_lines)

    def _get_timestamp(self) -> str:
        """現在のタイムスタンプを取得"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_report(self, report: str, output_path: str = None) -> None:
        """レポートをファイルに保存"""
        if output_path is None:
            output_path = "/src/docs/ツール推薦レポート_自動生成.md"

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📝 レポートを保存しました: {output_file}")


def main():
    """メイン処理"""
    print("=" * 60)
    print("🔧 ツール推薦システム")
    print("=" * 60)
    print()

    # 推薦エンジンを初期化
    recommender = ToolRecommender()

    # ツールとチェックリストを読み込み
    recommender.load_tools()
    recommender.load_checklist()

    # ツールを推薦
    recommendations = recommender.recommend_tools()

    # レポートを生成
    report = recommender.generate_report(recommendations)

    # レポートを保存
    recommender.save_report(report)

    # サマリーを表示
    print()
    print("=" * 60)
    print("📊 サマリー")
    print("=" * 60)
    checked_count = sum(1 for req in recommender.requirements if req.is_checked)
    print(f"チェック済み要件: {checked_count}")
    print(f"推薦カテゴリ: {len(recommendations)}")

    # ユニークなツール数を計算
    unique_tool_names = set()
    for tools in recommendations.values():
        for tool, _, _ in tools:
            unique_tool_names.add(tool.name)

    print(f"推薦ツール総数 (ユニーク): {len(unique_tool_names)}")
    print()

    if recommendations:
        print("トップ推薦ツール:")
        all_tools = []
        for tools in recommendations.values():
            all_tools.extend(tools)

        # スコアでソートして重複を除去してから上位5件を表示
        all_tools.sort(key=lambda x: x[1], reverse=True)

        # ツール名でユニーク化
        seen_tools = set()
        unique_tools = []
        for tool, score, reason in all_tools:
            if tool.name not in seen_tools:
                seen_tools.add(tool.name)
                unique_tools.append((tool, score, reason))

        # 上位5件を表示
        for tool, score, reason in unique_tools[:5]:
            print(f"  • {tool.name} (スコア: {score:.1f}) - {tool.category}")

    print()
    print("✅ 処理完了")


if __name__ == "__main__":
    main()
