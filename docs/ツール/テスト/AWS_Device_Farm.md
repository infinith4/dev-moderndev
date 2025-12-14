# AWS Device Farm

## 概要

**AWS Device Farm**は、実機デバイスを使用したモバイルアプリケーション（iOS/Android）・Webアプリケーションのテストを自動化するクラウドベーステストサービスです。数百台の実デバイスで並列テストを実行し、互換性問題を早期検出、品質向上を実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Amazon Web Services (AWS) |
| **種別** | モバイル・Webアプリケーションテストサービス |
| **ライセンス** | プロプライエタリ（AWS提供） |
| **料金** | 🟡 従量課金（デバイス分×時間） |
| **公式サイト** | https://aws.amazon.com/device-farm/ |
| **ドキュメント** | https://docs.aws.amazon.com/devicefarm/ |

## 主な特徴

### 1. 実機デバイステスト
- **iOS**: iPhone、iPad（最新〜過去数世代）
- **Android**: Samsung、Google Pixel、Huawei等
- **実機**: シミュレーターではなく実デバイス
- **デバイスプール**: カスタムデバイスセット作成

### 2. テストフレームワーク対応
- **Android**: Espresso、UI Automator 2.0、Appium、Calabash、Robotium
- **iOS**: XCTest、XCUITest、Appium、Calabash、UI Automation
- **Web**: Selenium WebDriver
- **組み込みExplorer**: コード不要の自動探索テスト

### 3. 並列実行
- 数百台のデバイスで同時テスト
- テスト時間大幅短縮
- デバイスプール単位で並列度調整

### 4. レポート・デバッグ
- スクリーンショット・動画
- デバイスログ
- パフォーマンスデータ（CPU、メモリ、ネットワーク）
- クラッシュレポート

## 使い方

### セットアップ

#### AWS CLI インストール

```bash
# AWS CLI インストール済み前提
aws devicefarm list-projects

# Device Farm サービスエンドポイントは us-west-2 固定
export AWS_DEFAULT_REGION=us-west-2
```

### プロジェクト作成

```bash
# プロジェクト作成
aws devicefarm create-project \
  --name "MyMobileApp" \
  --default-job-timeout-minutes 60

# プロジェクトID取得
PROJECT_ARN=$(aws devicefarm list-projects \
  --query 'projects[?name==`MyMobileApp`].arn' \
  --output text)

echo $PROJECT_ARN
```

### Android アプリテスト

#### Espresso テスト

```bash
# 1. APKビルド
cd android-app
./gradlew assembleDebug
./gradlew assembleDebugAndroidTest

# 2. APKアップロード
APP_UPLOAD=$(aws devicefarm create-upload \
  --project-arn $PROJECT_ARN \
  --name app-debug.apk \
  --type ANDROID_APP)

APP_UPLOAD_ARN=$(echo $APP_UPLOAD | jq -r '.upload.arn')
APP_UPLOAD_URL=$(echo $APP_UPLOAD | jq -r '.upload.url')

# S3に直接アップロード
curl -T app/build/outputs/apk/debug/app-debug.apk "$APP_UPLOAD_URL"

# テストAPKアップロード
TEST_UPLOAD=$(aws devicefarm create-upload \
  --project-arn $PROJECT_ARN \
  --name app-debug-androidTest.apk \
  --type INSTRUMENTATION_TEST_PACKAGE)

TEST_UPLOAD_ARN=$(echo $TEST_UPLOAD | jq -r '.upload.arn')
TEST_UPLOAD_URL=$(echo $TEST_UPLOAD | jq -r '.upload.url')

curl -T app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk "$TEST_UPLOAD_URL"

# 3. デバイスプール選択（トップデバイス）
DEVICE_POOL_ARN=$(aws devicefarm list-device-pools \
  --arn $PROJECT_ARN \
  --query 'devicePools[?name==`Top Devices`].arn' \
  --output text)

# 4. テスト実行をスケジュール
RUN=$(aws devicefarm schedule-run \
  --project-arn $PROJECT_ARN \
  --app-arn $APP_UPLOAD_ARN \
  --device-pool-arn $DEVICE_POOL_ARN \
  --name "Espresso Test Run" \
  --test '{
    "type": "INSTRUMENTATION",
    "testPackageArn": "'$TEST_UPLOAD_ARN'"
  }')

RUN_ARN=$(echo $RUN | jq -r '.run.arn')

# 5. テスト結果確認
aws devicefarm get-run --arn $RUN_ARN

# ステータス: PENDING → RUNNING → COMPLETED
```

#### Appium テスト（Python）

```python
# test_appium.py
from appium import webdriver
import unittest

class AppiumTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '13',
            'deviceName': 'Android Device',
            'app': '/path/to/app-debug.apk',
            'automationName': 'UiAutomator2',
            'appPackage': 'com.example.myapp',
            'appActivity': '.MainActivity'
        }

        # AWS Device Farmでは環境変数から取得
        # self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver = webdriver.Remote(
            command_executor='http://0.0.0.0:4723/wd/hub',
            desired_capabilities=desired_caps
        )

    def test_login(self):
        # ログインテスト
        username_field = self.driver.find_element_by_id('com.example.myapp:id/username')
        password_field = self.driver.find_element_by_id('com.example.myapp:id/password')
        login_button = self.driver.find_element_by_id('com.example.myapp:id/login')

        username_field.send_keys('testuser')
        password_field.send_keys('password123')
        login_button.click()

        # 検証
        welcome_text = self.driver.find_element_by_id('com.example.myapp:id/welcome')
        self.assertEqual(welcome_text.text, 'Welcome, testuser!')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
```

```bash
# Appium テストをDevice Farmで実行
# requirements.txt
cat > requirements.txt <<EOF
Appium-Python-Client==2.9.0
pytest==7.4.0
EOF

# テストパッケージ作成
zip -r appium-tests.zip test_appium.py requirements.txt

# アップロード
TEST_SPEC_UPLOAD=$(aws devicefarm create-upload \
  --project-arn $PROJECT_ARN \
  --name appium-tests.zip \
  --type APPIUM_PYTHON_TEST_PACKAGE)

# ... （APP_UPLOAD同様にアップロード）

# テスト実行
aws devicefarm schedule-run \
  --project-arn $PROJECT_ARN \
  --app-arn $APP_UPLOAD_ARN \
  --device-pool-arn $DEVICE_POOL_ARN \
  --name "Appium Test Run" \
  --test '{
    "type": "APPIUM_PYTHON",
    "testPackageArn": "'$TEST_SPEC_UPLOAD_ARN'"
  }'
```

### iOS アプリテスト

#### XCUITest

```bash
# 1. Xcodeでテストビルド
cd ios-app
xcodebuild \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphoneos \
  -configuration Debug \
  -derivedDataPath build \
  build-for-testing

# .ipaファイル作成
cd build/Build/Products/Debug-iphoneos
mkdir Payload
cp -r MyApp.app Payload/
zip -r MyApp.ipa Payload/

# テストパッケージ作成
cd ../Debug-iphoneos
zip -r MyApp-Tests.zip MyApp-Runner.app

# 2. アップロード（Android同様）
APP_UPLOAD=$(aws devicefarm create-upload \
  --project-arn $PROJECT_ARN \
  --name MyApp.ipa \
  --type IOS_APP)

# ... アップロード処理

# 3. テスト実行
aws devicefarm schedule-run \
  --project-arn $PROJECT_ARN \
  --app-arn $APP_UPLOAD_ARN \
  --device-pool-arn $DEVICE_POOL_ARN \
  --name "XCUITest Run" \
  --test '{
    "type": "XCTEST_UI",
    "testPackageArn": "'$TEST_UPLOAD_ARN'"
  }'
```

### Web アプリテスト（Selenium）

```python
# test_web.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class WebAppTest(unittest.TestCase):
    def setUp(self):
        # AWS Device Farm では環境変数から設定取得
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def test_homepage(self):
        self.driver.get('https://example.com')
        title = self.driver.title
        self.assertIn('Example Domain', title)

    def test_login(self):
        self.driver.get('https://example.com/login')
        username = self.driver.find_element(By.ID, 'username')
        password = self.driver.find_element(By.ID, 'password')
        submit = self.driver.find_element(By.ID, 'submit')

        username.send_keys('testuser')
        password.send_keys('password')
        submit.click()

        # 検証
        welcome = self.driver.find_element(By.ID, 'welcome')
        self.assertEqual(welcome.text, 'Welcome, testuser!')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
```

### カスタムデバイスプール作成

```bash
# 特定デバイスのみでテスト
aws devicefarm create-device-pool \
  --project-arn $PROJECT_ARN \
  --name "HighEndDevices" \
  --description "High-end devices for performance testing" \
  --rules '[
    {
      "attribute": "MANUFACTURER",
      "operator": "IN",
      "value": "[\"Samsung\",\"Google\"]"
    },
    {
      "attribute": "OS_VERSION",
      "operator": "GREATER_THAN_OR_EQUALS",
      "value": "\"12\""
    },
    {
      "attribute": "RAM",
      "operator": "GREATER_THAN_OR_EQUALS",
      "value": "\"6000\""
    }
  ]'

# デバイス一覧確認
aws devicefarm list-devices \
  --filters '[
    {"attribute": "PLATFORM", "operator": "EQUALS", "values": ["ANDROID"]}
  ]'
```

### CI/CD 統合

#### GitHub Actions

```yaml
# .github/workflows/device-farm.yml
name: AWS Device Farm Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  android-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'adopt'

      - name: Build APK
        run: |
          cd android
          ./gradlew assembleDebug assembleDebugAndroidTest

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - name: Run Device Farm Tests
        run: |
          # プロジェクトARN
          PROJECT_ARN="${{ secrets.DEVICE_FARM_PROJECT_ARN }}"

          # アップロード
          APP_UPLOAD=$(aws devicefarm create-upload \
            --project-arn $PROJECT_ARN \
            --name app-debug.apk \
            --type ANDROID_APP)

          # ... テスト実行スクリプト
```

### テスト結果の取得

```python
# get_test_results.py
import boto3
import time

devicefarm = boto3.client('devicefarm', region_name='us-west-2')

def wait_for_run_completion(run_arn, timeout=3600):
    """テスト完了まで待機"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = devicefarm.get_run(arn=run_arn)
        status = response['run']['status']

        print(f"Status: {status}")

        if status in ['COMPLETED', 'ERRORED']:
            return response['run']

        time.sleep(30)

    raise TimeoutError("Test run timed out")

def get_test_results(run_arn):
    """テスト結果取得"""
    run = wait_for_run_completion(run_arn)

    print(f"\n=== Test Run Results ===")
    print(f"Name: {run['name']}")
    print(f"Status: {run['status']}")
    print(f"Result: {run['result']}")
    print(f"Total Jobs: {run['counters']['total']}")
    print(f"Passed: {run['counters']['passed']}")
    print(f"Failed: {run['counters']['failed']}")
    print(f"Warned: {run['counters']['warned']}")
    print(f"Errored: {run['counters']['errored']}")

    # ジョブ詳細
    jobs = devicefarm.list_jobs(arn=run_arn)
    for job in jobs['jobs']:
        print(f"\n  Device: {job['device']['name']}")
        print(f"  Result: {job['result']}")

        # アーティファクト（スクリーンショット、ログ）
        artifacts = devicefarm.list_artifacts(
            arn=job['arn'],
            type='SCREENSHOT'
        )

        for artifact in artifacts['artifacts']:
            print(f"    Screenshot: {artifact['url']}")

# 使用例
run_arn = "arn:aws:devicefarm:us-west-2:123456789012:run:..."
get_test_results(run_arn)
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | ユニットテスト | 開発中の継続的テスト |
| **テスト** | デバイス互換性テスト | 実機での包括的テスト |
| **テスト** | パフォーマンステスト | 実デバイスでのパフォーマンス測定 |
| **導入** | リリース前最終テスト | 本番リリース前の品質保証 |

## メリット

- **実機テスト**: シミュレーターではなく実デバイス
- **並列実行**: 数百台のデバイスで同時テスト
- **テストフレームワーク対応**: Espresso、XCUITest、Appium等
- **詳細レポート**: スクリーンショット、動画、ログ
- **パフォーマンスデータ**: CPU、メモリ、ネットワーク測定
- **CI/CD統合**: GitHub Actions、Jenkins等と統合容易
- **マネージドサービス**: デバイス管理不要

## デメリット

- **コスト**: 従量課金、大規模テストは高額
- **us-west-2固定**: リージョンが限定
- **テスト実行待機**: デバイス空き待ちが発生する場合あり
- **学習曲線**: テストフレームワーク・API習得が必要
- **カスタマイズ制限**: 特殊なデバイス設定は困難

## 類似ツールとの比較

| ツール | 対象 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Device Farm** | iOS/Android | 従量課金 | AWS統合、実機テスト |
| **Firebase Test Lab** | Android | 従量課金 | Googleエコシステム |
| **BrowserStack** | マルチプラットフォーム | 有料サブスク | クロスブラウザテスト |
| **Sauce Labs** | モバイル・Web | 有料サブスク | エンタープライズ向け |

## ベストプラクティス

### 1. デバイスプール戦略

```text
# 段階的デバイステスト

Phase 1: 主要デバイス（5-10台）
  - iPhone最新、Android最新
  - 高シェアデバイス

Phase 2: 互換性テスト（30-50台）
  - 過去2-3世代のデバイス
  - 様々なメーカー・画面サイズ

Phase 3: 包括テスト（100台以上）
  - リリース前の最終テスト
  - レアケース検証
```

### 2. テスト並列化

```bash
# デバイスプール単位で並列実行
# 各プールで独立してテスト
aws devicefarm schedule-run ... --device-pool-arn $POOL_1 &
aws devicefarm schedule-run ... --device-pool-arn $POOL_2 &
aws devicefarm schedule-run ... --device-pool-arn $POOL_3 &
wait
```

### 3. コスト最適化

```text
# テスト時間短縮
- 並列実行の活用
- テストの優先順位付け（重要テストを先に）
- タイムアウト設定（無限ループ防止）

# デバイス選定
- 主要デバイスに絞る
- 無料枠の活用（初回1000デバイス分）
```

## 公式リソース

- **公式サイト**: https://aws.amazon.com/device-farm/
- **ドキュメント**: https://docs.aws.amazon.com/devicefarm/
- **料金**: https://aws.amazon.com/device-farm/pricing/
- **デバイスリスト**: https://aws.amazon.com/device-farm/device-list/
- **サンプル**: https://github.com/aws-samples/aws-device-farm-sample-app-for-android

## まとめ

AWS Device Farmは、実機デバイスを使用したモバイル・Webアプリケーションテストを自動化するクラウドベーステストサービスです。数百台の実デバイスで並列テストを実行し、互換性問題を早期検出、品質向上を実現します。Espresso、XCUITest、Appium等の主要テストフレームワークに対応し、CI/CD統合も容易です。モバイルアプリ開発における包括的なデバイステストには必須のツールです。

---

**最終更新**: 2025-12-06
**対象バージョン**: AWS Device Farm 2024+
