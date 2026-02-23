# Quartz Scheduler

## 概要

Quartz Schedulerは、Java向けのオープンソースジョブスケジューリングライブラリです。シンプルなタイマーから複雑なCronスケジュールまで柔軟なスケジュール制御が可能で、ジョブの永続化（JDBCJobStore）、クラスタリング、障害復旧をサポートします。Spring Bootとの統合が充実しており、エンタープライズJavaアプリケーションのバッチ処理・定期実行の標準的な選択肢として広く採用されています。

## 主な機能

### 1. トリガー

- **SimpleTrigger**: 一定間隔での繰り返し実行（例：5分ごと）
- **CronTrigger**: Cron式による柔軟なスケジュール（例：毎週月曜9時）
- **CalendarIntervalTrigger**: カレンダーベースの間隔実行
- **DailyTimeIntervalTrigger**: 日次の時間範囲指定

### 2. ジョブ管理

- **Job**: 実行するタスクの定義（`Job`インターフェース実装）
- **JobDetail**: ジョブのメタデータ（名前、グループ、パラメータ）
- **JobDataMap**: ジョブへのパラメータ受け渡し
- **リスナー**: ジョブ実行前後のイベントハンドリング

### 3. 永続化・クラスタリング

- **RAMJobStore**: メモリ内保存（開発・テスト向け）
- **JDBCJobStore**: RDB永続化（本番環境向け）
- **クラスタリング**: 複数ノードでのジョブ分散実行
- **ミスファイア処理**: 実行漏れジョブの自動リカバリ

### 4. Spring Boot統合

- **Auto-Configuration**: `spring-boot-starter-quartz`で自動設定
- **Bean注入**: Spring管理のBeanをジョブ内で使用可能
- **プロパティ設定**: `application.yml`でQuartz設定を管理
- **スキーマ自動生成**: DBテーブルの自動作成

## 利用方法

### Maven依存関係

```xml
<!-- pom.xml -->
<dependencies>
  <!-- Quartz単体 -->
  <dependency>
    <groupId>org.quartz-scheduler</groupId>
    <artifactId>quartz</artifactId>
    <version>2.5.0</version>
  </dependency>

  <!-- Spring Boot統合 -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-quartz</artifactId>
  </dependency>
</dependencies>
```

### Gradle依存関係

```groovy
// build.gradle
dependencies {
    // Quartz単体
    implementation 'org.quartz-scheduler:quartz:2.5.0'

    // Spring Boot統合
    implementation 'org.springframework.boot:spring-boot-starter-quartz'
}
```

### ジョブの定義

```java
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

public class ReportJob implements Job {

    @Override
    public void execute(JobExecutionContext context)
            throws JobExecutionException {
        String reportType = context.getJobDetail()
            .getJobDataMap()
            .getString("reportType");

        System.out.println("Generating " + reportType + " report...");
        // レポート生成ロジック
    }
}
```

### スケジュール設定（Java API）

```java
import org.quartz.*;
import org.quartz.impl.StdSchedulerFactory;

public class SchedulerExample {
    public static void main(String[] args) throws Exception {
        // スケジューラの作成
        Scheduler scheduler = StdSchedulerFactory
            .getDefaultScheduler();

        // ジョブの定義
        JobDetail job = JobBuilder.newJob(ReportJob.class)
            .withIdentity("reportJob", "reporting")
            .usingJobData("reportType", "daily")
            .build();

        // Cronトリガー（毎日午前9時に実行）
        Trigger trigger = TriggerBuilder.newTrigger()
            .withIdentity("dailyTrigger", "reporting")
            .withSchedule(CronScheduleBuilder
                .cronSchedule("0 0 9 * * ?"))
            .build();

        // スケジュール登録・開始
        scheduler.scheduleJob(job, trigger);
        scheduler.start();
    }
}
```

### Spring Boot統合

```java
// Spring Boot ジョブ定義
import org.quartz.JobExecutionContext;
import org.springframework.scheduling.quartz.QuartzJobBean;
import org.springframework.stereotype.Component;

@Component
public class ReportJob extends QuartzJobBean {

    private final ReportService reportService;

    public ReportJob(ReportService reportService) {
        this.reportService = reportService;
    }

    @Override
    protected void executeInternal(JobExecutionContext context) {
        reportService.generateDailyReport();
    }
}
```

```yaml
# application.yml
spring:
  quartz:
    job-store-type: jdbc
    jdbc:
      initialize-schema: always
    properties:
      org.quartz.scheduler.instanceName: MyScheduler
      org.quartz.scheduler.instanceId: AUTO
      org.quartz.jobStore.isClustered: true
      org.quartz.jobStore.clusterCheckinInterval: 20000
      org.quartz.threadPool.threadCount: 10
```

### Cron式リファレンス

| フィールド | 指定可能値 | 例 |
|-----------|-----------|-----|
| 秒 | 0-59 | `0` |
| 分 | 0-59 | `30` |
| 時 | 0-23 | `9` |
| 日 | 1-31 | `15` |
| 月 | 1-12 | `*` |
| 曜日 | 1-7（SUN=1） | `MON-FRI` |
| 年（任意） | 空 or 1970-2199 | `2025` |

```
# Cron式の例
0 0 9 * * ?        # 毎日 9:00
0 0/30 * * * ?     # 30分ごと
0 0 9 ? * MON-FRI  # 平日 9:00
0 0 0 1 * ?        # 毎月1日 0:00
0 0 12 ? * 2#1     # 毎月第1月曜 12:00
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Quartz Scheduler** | 無料 | オープンソース、Apache License 2.0 |

## メリット

1. **柔軟なスケジュール**: Cron式、固定間隔、カレンダーベース等を選択可能
2. **ジョブ永続化**: JDBCJobStoreでアプリケーション再起動後もジョブを保持
3. **クラスタリング**: 複数ノードでのジョブ分散・フェイルオーバー
4. **Spring Boot統合**: Auto-Configurationで容易に導入
5. **ミスファイア処理**: 実行漏れジョブの自動リカバリ
6. **動的スケジュール**: 実行時にスケジュールの追加・変更・削除が可能
7. **成熟度**: Java開発で長年の実績がある安定したライブラリ

## デメリット

1. **DB設計必要**: JDBCJobStoreは専用テーブルが必要
2. **設定複雑**: クラスタリングやミスファイア処理の設定が複雑
3. **分散実行制限**: 単一ジョブの並列分散実行は非対応
4. **モニタリング不足**: 標準ではGUIダッシュボードがない
5. **依存関係**: Spring Boot以外では設定が煩雑になりやすい

## 代替ツール

| ツール | 特徴 | 比較 |
|--------|------|------|
| **Spring @Scheduled** | Spring標準アノテーション | Quartzよりシンプルだが永続化・クラスタリング非対応 |
| **JobRunr** | モダンなJavaジョブスケジューラ | Quartzよりシンプル、ダッシュボード内蔵 |
| **Airflow** | ワークフローオーケストレーション | Quartzよりリッチだが別サービスが必要 |
| **Kubernetes CronJob** | K8sネイティブ定期実行 | コンテナ環境向け、アプリ非依存 |

## 公式リンク

- **公式サイト**: [https://www.quartz-scheduler.org/](https://www.quartz-scheduler.org/)
- **ドキュメント**: [https://www.quartz-scheduler.org/documentation/](https://www.quartz-scheduler.org/documentation/)
- **GitHub**: [https://github.com/quartz-scheduler/quartz](https://github.com/quartz-scheduler/quartz)
- **Maven Central**: [https://mvnrepository.com/artifact/org.quartz-scheduler/quartz](https://mvnrepository.com/artifact/org.quartz-scheduler/quartz)
- **Spring Boot統合**: [https://docs.spring.io/spring-boot/reference/io/quartz.html](https://docs.spring.io/spring-boot/reference/io/quartz.html)

## 関連ドキュメント

- [Checkstyle](./Checkstyle.md)
- [SpotBugs](./SpotBugs.md)
- [Maven](./Maven.md)

---

**カテゴリ**: 開発ツール
**対象工程**: 実装・運用
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
