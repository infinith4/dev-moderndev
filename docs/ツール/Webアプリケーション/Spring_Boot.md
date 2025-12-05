# Spring Boot

## 概要

Spring Bootは、Spring Frameworkベースの高速開発フレームワークです。自動設定、組み込みサーバー（Tomcat）、スターター依存関係、Spring Data・Spring Security統合により、エンタープライズJavaアプリケーション・マイクロサービスを迅速に構築します。Pivotal開発、エンタープライズグレード、Java/Kotlinエコシステムで広く採用されています。

## 主な機能

### 1. 自動設定
- **Auto-configuration**: 自動設定
- **スターター**: 依存関係セット
- **組み込みサーバー**: Tomcat、Jetty、Undertow
- **ゼロコンフィグ**: XML不要

### 2. Spring Data
- **JPA**: Hibernate統合
- **リポジトリ**: CRUD自動生成
- **クエリメソッド**: メソッド名クエリ
- **トランザクション**: @Transactional

### 3. REST API
- **@RestController**: REST コントローラー
- **@RequestMapping**: ルーティング
- **JSON変換**: 自動シリアライズ
- **バリデーション**: Bean Validation

### 4. Spring Security
- **認証**: 認証機構
- **認可**: ロールベース
- **OAuth2**: OAuth2サポート
- **JWT**: JWTトークン

## 利用方法

### プロジェクト作成

```bash
# Spring Initializr
# https://start.spring.io/

# または curl
curl https://start.spring.io/starter.zip \
  -d dependencies=web,data-jpa,mysql \
  -d type=maven-project \
  -d language=java \
  -d javaVersion=17 \
  -d groupId=com.example \
  -d artifactId=myapp \
  -o myapp.zip

unzip myapp.zip
cd myapp
./mvnw spring-boot:run
```

### 基本アプリケーション

```java
// src/main/java/com/example/myapp/MyappApplication.java
package com.example.myapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyappApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyappApplication.class, args);
    }
}
```

### REST Controller

```java
// src/main/java/com/example/myapp/controller/UserController.java
package com.example.myapp.controller;

import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public List<User> getAllUsers() {
        return List.of(
            new User(1L, "Alice", "alice@example.com"),
            new User(2L, "Bob", "bob@example.com")
        );
    }

    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        return new User(id, "Alice", "alice@example.com");
    }

    @PostMapping
    public User createUser(@RequestBody User user) {
        return user;
    }

    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) {
        user.setId(id);
        return user;
    }

    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        // Delete logic
    }
}
```

### Entity（JPA）

```java
// src/main/java/com/example/myapp/entity/User.java
package com.example.myapp.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    // Constructors, Getters, Setters
    public User() {}

    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

### Repository

```java
// src/main/java/com/example/myapp/repository/UserRepository.java
package com.example.myapp.repository;

import com.example.myapp.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);
}
```

### Service

```java
// src/main/java/com/example/myapp/service/UserService.java
package com.example.myapp.service;

import com.example.myapp.entity.User;
import com.example.myapp.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public User createUser(User user) {
        return userRepository.save(user);
    }

    public User updateUser(Long id, User userDetails) {
        User user = getUserById(id);
        user.setName(userDetails.getName());
        user.setEmail(userDetails.getEmail());
        return userRepository.save(user);
    }

    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}
```

### application.properties

```properties
# src/main/resources/application.properties

# Server
server.port=8080

# Database (MySQL)
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=user
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA/Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

# Logging
logging.level.root=INFO
logging.level.com.example.myapp=DEBUG
```

### バリデーション

```java
// pom.xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>

// User.java
import jakarta.validation.constraints.*;

@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    private String name;

    @NotBlank(message = "Email is required")
    @Email(message = "Email should be valid")
    private String email;

    // Getters, Setters
}

// Controller
@PostMapping
public User createUser(@Valid @RequestBody User user) {
    return userService.createUser(user);
}
```

### 例外ハンドリング

```java
// src/main/java/com/example/myapp/exception/GlobalExceptionHandler.java
package com.example.myapp.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<ErrorResponse> handleRuntimeException(RuntimeException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage()
        );
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "Internal server error"
        );
        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

### Docker

```dockerfile
# Dockerfile
FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src
RUN ./mvnw clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Spring Boot** | 🟢 完全無料 | オープンソース、Apache License |

## メリット

1. **完全無料**: オープンソース
2. **生産性**: 高速開発
3. **エンタープライズ**: エンタープライズグレード
4. **自動設定**: 設定簡素化
5. **エコシステム**: 豊富なSpringエコシステム

## デメリット

1. **学習曲線**: Spring Framework学習必要
2. **重い**: メモリ消費大
3. **起動遅い**: 起動時間長い
4. **設定複雑**: 高度設定複雑

## 公式リンク

- **公式サイト**: [https://spring.io/projects/spring-boot](https://spring.io/projects/spring-boot)
- **ドキュメント**: [https://docs.spring.io/spring-boot/docs/current/reference/html/](https://docs.spring.io/spring-boot/docs/current/reference/html/)

## 関連ドキュメント

- [Webフレームワークツール一覧](../Webフレームワークツール/)
- [Spring Framework](./Spring_Framework.md)
- [Apache Tomcat](../アプリケーションサーバーツール/Apache_Tomcat.md)

---

**カテゴリ**: Webフレームワークツール
**対象工程**: バックエンド開発・Java
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
