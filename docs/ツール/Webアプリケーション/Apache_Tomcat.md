# Apache Tomcat

## 概要

Apache Tomcatは、オープンソースのJavaサーブレットコンテナ・アプリケーションサーバーです。Servlet API、JSP（JavaServer Pages）、WebSocket、JNDI、セッション管理により、Javaウェブアプリケーション（WAR、EARファイル）のデプロイ・実行を実現します。Apache Software Foundation開発、軽量、Java EE準拠で広く採用されています。

## 主な機能

### 1. サーブレットコンテナ
- **Servlet API**: Java Servlet実行
- **JSP**: JavaServer Pages
- **WebSocket**: WebSocket対応
- **HTTP/2**: HTTP/2対応

### 2. デプロイ
- **WAR**: Webアーカイブデプロイ
- **ホットデプロイ**: 再起動不要
- **Manager**: Web管理UI
- **コンテキスト**: 複数アプリ

### 3. セッション管理
- **メモリセッション**: インメモリ
- **永続化**: ファイル、JDBC
- **クラスタリング**: セッション複製

### 4. セキュリティ
- **Realm**: 認証・認可
- **SSL/TLS**: HTTPS
- **JAAS**: Java認証

## 利用方法

### インストール（Docker）

```bash
docker run -d --name tomcat \
  -p 8080:8080 \
  -v $(pwd)/webapps:/usr/local/tomcat/webapps \
  tomcat:10-jdk17
```

### サーブレット（基本）

```java
// HelloServlet.java
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h1>Hello from Tomcat!</h1>");
        out.println("</body></html>");
    }
}
```

### JSP

```jsp
<!-- index.jsp -->
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="java.util.Date" %>
<html>
<head>
    <title>JSP Example</title>
</head>
<body>
    <h1>JSP Example</h1>
    <p>Current time: <%= new Date() %></p>

    <%
        String name = request.getParameter("name");
        if (name != null) {
            out.println("<p>Hello, " + name + "!</p>");
        }
    %>
</body>
</html>
```

### web.xml（デプロイメント記述子）

```xml
<!-- WEB-INF/web.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         version="4.0">

    <servlet>
        <servlet-name>HelloServlet</servlet-name>
        <servlet-class>com.example.HelloServlet</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>HelloServlet</servlet-name>
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>

    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
        <welcome-file>index.html</welcome-file>
    </welcome-file-list>

    <session-config>
        <session-timeout>30</session-timeout>
    </session-config>
</web-app>
```

### server.xml設定

```xml
<!-- conf/server.xml -->
<Server port="8005" shutdown="SHUTDOWN">
  <Service name="Catalina">
    <!-- HTTPコネクタ -->
    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />

    <!-- HTTPSコネクタ -->
    <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true">
        <SSLHostConfig>
            <Certificate certificateKeystoreFile="conf/keystore.jks"
                         type="RSA" />
        </SSLHostConfig>
    </Connector>

    <!-- エンジン -->
    <Engine name="Catalina" defaultHost="localhost">
      <Host name="localhost" appBase="webapps"
            unpackWARs="true" autoDeploy="true">

        <!-- コンテキスト -->
        <Context path="/myapp" docBase="myapp" reloadable="true" />

      </Host>
    </Engine>
  </Service>
</Server>
```

### WARデプロイ

```bash
# WARビルド（Maven）
mvn clean package

# WARファイル生成
# target/myapp.war

# デプロイ（webappsフォルダにコピー）
cp target/myapp.war $CATALINA_HOME/webapps/

# 自動展開・起動
# http://localhost:8080/myapp/
```

### Manager App（管理UI）

```xml
<!-- conf/tomcat-users.xml -->
<tomcat-users>
  <role rolename="manager-gui"/>
  <user username="admin" password="secret" roles="manager-gui"/>
</tomcat-users>
```

```
Manager App: http://localhost:8080/manager/html
```

### データソース（JNDI）

```xml
<!-- conf/context.xml -->
<Context>
  <Resource name="jdbc/MyDB"
            auth="Container"
            type="javax.sql.DataSource"
            maxTotal="100"
            maxIdle="30"
            maxWaitMillis="10000"
            username="dbuser"
            password="dbpass"
            driverClassName="com.mysql.cj.jdbc.Driver"
            url="jdbc:mysql://localhost:3306/mydb"/>
</Context>
```

```java
// Javaコード
Context initContext = new InitialContext();
Context envContext = (Context) initContext.lookup("java:/comp/env");
DataSource ds = (DataSource) envContext.lookup("jdbc/MyDB");
Connection conn = ds.getConnection();
```

### Docker Compose（Tomcat + MySQL）

```yaml
version: '3.8'
services:
  tomcat:
    image: tomcat:10-jdk17
    ports:
      - "8080:8080"
    volumes:
      - ./webapps:/usr/local/tomcat/webapps
    environment:
      JAVA_OPTS: "-Xms512m -Xmx1024m"
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: mydb
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Apache Tomcat** | 🟢 完全無料 | オープンソース、Apache License |

## メリット

1. **完全無料**: オープンソース
2. **軽量**: 軽量アプリケーションサーバー
3. **Java EE**: Servlet、JSP対応
4. **成熟**: 長年の実績
5. **エコシステム**: 豊富なツール

## デメリット

1. **機能限定**: フルJava EE非対応
2. **設定複雑**: XML設定複雑
3. **メモリ**: メモリ消費
4. **クラスローダー**: クラスローダー問題

## 公式リンク

- **公式サイト**: [https://tomcat.apache.org/](https://tomcat.apache.org/)
- **ドキュメント**: [https://tomcat.apache.org/tomcat-10.0-doc/](https://tomcat.apache.org/tomcat-10.0-doc/)

## 関連ドキュメント

- [アプリケーションサーバーツール一覧](../アプリケーションサーバーツール/)
- [Apache HTTP Server](../Webサーバーツール/Apache_HTTP_Server.md)
- [WildFly](./WildFly.md)

---

**カテゴリ**: アプリケーションサーバーツール
**対象工程**: Javaアプリケーション実行
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
