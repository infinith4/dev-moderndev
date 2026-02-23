# InSpec

## 概要

InSpecは、Chef社（現Progress）が開発したオープンソースのインフラストラクチャテスト・コンプライアンスフレームワークです。人間が読めるRuby DSL（Domain Specific Language）でテストを記述し、サーバー、クラウドリソース、コンテナのセキュリティ・コンプライアンス検証を自動化します。CIS Benchmark、STIG、PCI-DSS等の標準に準拠し、DevSecOpsパイプラインに統合できます。

## 主な機能

### 1. インフラテスト
- **OS設定**: Linux、Windows、macOS
- **パッケージ**: インストール済みパッケージ検証
- **サービス**: systemd、Windows Service
- **ファイル**: パーミッション、所有者、内容
- **ネットワーク**: ポート、ファイアウォール

### 2. クラウドリソース
- **AWS**: EC2、S3、IAM、セキュリティグループ
- **Azure**: VM、Storage、ネットワーク
- **GCP**: Compute Engine、Cloud Storage

### 3. コンプライアンスプロファイル
- **CIS Benchmarks**: Linux、Windows、クラウド
- **STIG**: DoD Security Technical Implementation Guides
- **PCI-DSS**: Payment Card Industry
- **HIPAA**: 医療情報保護
- **カスタムプロファイル**: 組織固有のポリシー

### 4. レポート
- **CLI**: コンソール出力
- **JSON**: 機械可読形式
- **JUnit**: CI/CD統合
- **HTML**: 人間可読レポート

### 5. 統合
- **Chef Automate**: 中央管理ダッシュボード
- **CI/CD**: GitHub Actions、GitLab CI、Jenkins
- **Terraform**: terraform-compliance風の使用
- **Ansible**: Ansibleプレイブック検証

## 利用方法

### インストール

```bash
# Linux/macOS (curl)
curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -P inspec

# Windows (PowerShell)
. { iwr -useb https://omnitruck.chef.io/install.ps1 } | iex; install -project inspec

# Homebrew (macOS)
brew install inspec

# Docker
docker pull chef/inspec

# バージョン確認
inspec version
```

### 基本的な使い方

```bash
# ローカルシステムテスト
inspec exec my_profile

# リモートSSH
inspec exec my_profile -t ssh://user@hostname -i /path/to/key

# Docker コンテナ
inspec exec my_profile -t docker://container_id

# AWS
inspec exec my_profile -t aws://
```

### プロファイル作成

```bash
# プロファイル初期化
inspec init profile my_profile

# ディレクトリ構造
my_profile/
├── README.md
├── inspec.yml
├── controls/
│   └── example.rb
└── libraries/
```

### テストコード例

```ruby
# controls/ssh_config.rb
control 'ssh-01' do
  impact 1.0
  title 'SSH Server Configuration'
  desc 'Ensure SSH is configured securely'
  
  describe sshd_config do
    its('PermitRootLogin') { should eq 'no' }
    its('PasswordAuthentication') { should eq 'no' }
    its('Protocol') { should eq '2' }
  end
end

# controls/firewall.rb
control 'firewall-01' do
  impact 0.8
  title 'Firewall Enabled'
  desc 'Ensure firewall is running'
  
  describe service('firewalld') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
  end
end

# controls/web_server.rb
control 'nginx-01' do
  impact 0.7
  title 'Nginx Configuration'
  desc 'Verify nginx is properly configured'
  
  describe package('nginx') do
    it { should be_installed }
  end
  
  describe service('nginx') do
    it { should be_running }
  end
  
  describe port(80) do
    it { should be_listening }
  end
  
  describe file('/etc/nginx/nginx.conf') do
    it { should exist }
    its('owner') { should eq 'root' }
    its('mode') { should cmp '0644' }
  end
end
```

### AWS リソーステスト

```ruby
# controls/aws_s3.rb
control 'aws-s3-01' do
  impact 1.0
  title 'S3 Bucket Encryption'
  desc 'All S3 buckets should have encryption enabled'
  
  aws_s3_buckets.bucket_names.each do |bucket_name|
    describe aws_s3_bucket(bucket_name) do
      it { should have_default_encryption_enabled }
    end
  end
end

# controls/aws_ec2.rb
control 'aws-ec2-01' do
  impact 0.8
  title 'EC2 Instances Not Public'
  desc 'EC2 instances should not have public IP addresses'
  
  aws_ec2_instances.instance_ids.each do |instance_id|
    describe aws_ec2_instance(instance_id) do
      it { should_not have_public_ip_address }
    end
  end
end
```

### CI/CD統合

```yaml
# .github/workflows/inspec.yml
name: InSpec Tests

on: [push, pull_request]

jobs:
  inspec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup InSpec
        run: |
          curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -P inspec
      
      - name: Run InSpec tests
        run: |
          inspec exec my_profile --reporter cli json:results.json
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: inspec-results
          path: results.json
```

### CIS Benchmark使用

```bash
# CIS Docker Benchmark
inspec supermarket exec dev-sec/cis-docker-benchmark

# CIS Kubernetes Benchmark
inspec supermarket exec dev-sec/cis-kubernetes-benchmark

# カスタムプロファイル
inspec exec https://github.com/dev-sec/linux-baseline
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **InSpec (OSS)** |  無料 | オープンソース、Apache License 2.0 |
| **Chef Automate** |  商用 | 中央管理、ダッシュボード、レポート |

## メリット

###  主な利点

1. **無料**: オープンソース、Apache License
2. **人間が読める**: Ruby DSL、明確なテスト
3. **マルチプラットフォーム**: Linux、Windows、macOS、クラウド
4. **コンプライアンス**: CIS、STIG、PCI-DSS対応
5. **リモート実行**: SSH、WinRM、Docker
6. **豊富なリソース**: 100+の組み込みリソース
7. **CI/CD統合**: GitHub Actions、GitLab CI
8. **コミュニティ**: dev-sec等の共有プロファイル
9. **拡張可能**: カスタムリソース作成
10. **Chef統合**: Chef Automate連携

## デメリット

###  制約・課題

1. **Ruby必須**: Ruby DSL習得必要
2. **学習曲線**: 初心者には難しい
3. **パフォーマンス**: 大規模環境で遅延
4. **GUI不在**: コマンドライン中心（Chef Automate除く）
5. **ドキュメント**: 一部不十分
6. **エラーメッセージ**: 分かりにくい場合あり
7. **Windows**: Linux より機能少ない
8. **リモート実行**: ネットワーク設定が煩雑

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Serverspec** | RSpec風、インフラテスト | InSpecと類似だがコンプライアンス弱い |
| **Terratest** | Go製、Terraform テスト | InSpecより Terraform特化 |
| **Ansible Molecule** | Ansible ロール テスト | InSpecより Ansible特化 |
| **Open Policy Agent** | ポリシーエンジン | InSpecよりRegoベース |
| **Chef Compliance** | 商用 | InSpec + 管理UI |

## 公式リンク

- **公式サイト**: [https://www.inspec.io/](https://www.inspec.io/)
- **ドキュメント**: [https://docs.chef.io/inspec/](https://docs.chef.io/inspec/)
- **GitHub**: [https://github.com/inspec/inspec](https://github.com/inspec/inspec)
- **Supermarket**: [https://supermarket.chef.io/tools?type=compliance_profile](https://supermarket.chef.io/tools?type=compliance_profile)
- **Dev-Sec**: [https://dev-sec.io/](https://dev-sec.io/)

## 関連ドキュメント

- [インフラテストツール一覧](../インフラテストツール/)
- [Terratest](./Terratest.md)
- [OPA](../ポリシー管理ツール/OPA.md)
- [Ansible](../IaCツール/Ansible.md)
- [インフラテストベストプラクティス](../../best-practices/infrastructure-testing.md)

---

**カテゴリ**: インフラテストツール  
**対象工程**: インフラ構築、テスト  
**最終更新**: 2025年12月  
**ドキュメントバージョン**: 1.0

