# Angular

## 概要

Angularは、Google製のフルスタックフロントエンドフレームワークです。TypeScript、コンポーネントベース、依存性注入、RxJS（リアクティブプログラミング）、Angular CLI、双方向データバインディングにより、エンタープライズグレードのSPA・Webアプリケーションを実現します。大規模アプリケーション、エンタープライズ採用で広く使用されています。

## 主な機能

### 1. TypeScript
- **TypeScript**: 型安全
- **デコレータ**: @Component、@Injectable
- **インターフェース**: 型定義

### 2. コンポーネント
- **Component**: UIコンポーネント
- **Template**: HTMLテンプレート
- **Style**: スタイル
- **Data Binding**: データバインディング

### 3. 依存性注入
- **Service**: ビジネスロジック
- **Injectable**: DI
- **Provider**: プロバイダー

### 4. RxJS
- **Observable**: 非同期データ
- **Operators**: map、filter等
- **Subject**: イベント

## 利用方法

### インストール

```bash
npm install -g @angular/cli

# プロジェクト作成
ng new my-app
cd my-app
ng serve

# http://localhost:4200/
```

### 基本コンポーネント

```typescript
// app.component.ts
import { Component } from '@angular/core'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Hello, Angular!'
  count = 0

  increment() {
    this.count++
  }
}
```

```html
<!-- app.component.html -->
<div>
  <h1>{{ title }}</h1>
  <p>Count: {{ count }}</p>
  <button (click)="increment()">Increment</button>
</div>
```

### データバインディング

```typescript
// user.component.ts
import { Component } from '@angular/core'

@Component({
  selector: 'app-user',
  template: `
    <div>
      <!-- 補間 -->
      <h2>{{ user.name }}</h2>

      <!-- プロパティバインディング -->
      <input [value]="user.email" />

      <!-- イベントバインディング -->
      <button (click)="handleClick()">Click</button>

      <!-- 双方向バインディング -->
      <input [(ngModel)]="user.name" />
    </div>
  `
})
export class UserComponent {
  user = {
    name: 'Alice',
    email: 'alice@example.com'
  }

  handleClick() {
    console.log('Clicked!')
  }
}
```

### ディレクティブ

```typescript
// app.component.ts
import { Component } from '@angular/core'

@Component({
  selector: 'app-root',
  template: `
    <div>
      <!-- *ngIf -->
      <p *ngIf="isLoggedIn">Welcome, {{ username }}!</p>
      <p *ngIf="!isLoggedIn">Please log in.</p>

      <!-- *ngFor -->
      <ul>
        <li *ngFor="let user of users">
          {{ user.name }} - {{ user.email }}
        </li>
      </ul>

      <!-- *ngSwitch -->
      <div [ngSwitch]="status">
        <p *ngSwitchCase="'loading'">Loading...</p>
        <p *ngSwitchCase="'success'">Success!</p>
        <p *ngSwitchDefault>Error</p>
      </div>
    </div>
  `
})
export class AppComponent {
  isLoggedIn = true
  username = 'Alice'
  status = 'success'

  users = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' }
  ]
}
```

### コンポーネント生成

```bash
# コンポーネント生成
ng generate component user-list
# または
ng g c user-list
```

```typescript
// user-list.component.ts
import { Component, OnInit } from '@angular/core'

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {
  users: any[] = []

  ngOnInit() {
    this.users = [
      { id: 1, name: 'Alice', email: 'alice@example.com' },
      { id: 2, name: 'Bob', email: 'bob@example.com' }
    ]
  }
}
```

### Service（依存性注入）

```bash
ng generate service user
```

```typescript
// user.service.ts
import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = '/api/users'

  constructor(private http: HttpClient) {}

  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl)
  }

  getUserById(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`)
  }

  createUser(user: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, user)
  }
}

// user-list.component.ts
import { Component, OnInit } from '@angular/core'
import { UserService } from '../user.service'

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html'
})
export class UserListComponent implements OnInit {
  users: any[] = []

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.getUsers().subscribe(users => {
      this.users = users
    })
  }
}
```

### HttpClient

```typescript
// app.module.ts
import { HttpClientModule } from '@angular/common/http'

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule
  ]
})
export class AppModule {}
```

### フォーム（Reactive Forms）

```typescript
// app.module.ts
import { ReactiveFormsModule } from '@angular/forms'

@NgModule({
  imports: [
    BrowserModule,
    ReactiveFormsModule
  ]
})
export class AppModule {}

// user-form.component.ts
import { Component } from '@angular/core'
import { FormBuilder, FormGroup, Validators } from '@angular/forms'

@Component({
  selector: 'app-user-form',
  template: `
    <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Name" />
      <div *ngIf="userForm.get('name')?.invalid && userForm.get('name')?.touched">
        Name is required
      </div>

      <input formControlName="email" placeholder="Email" />
      <div *ngIf="userForm.get('email')?.invalid && userForm.get('email')?.touched">
        Email is required and must be valid
      </div>

      <button type="submit" [disabled]="userForm.invalid">Submit</button>
    </form>
  `
})
export class UserFormComponent {
  userForm: FormGroup

  constructor(private fb: FormBuilder) {
    this.userForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    })
  }

  onSubmit() {
    if (this.userForm.valid) {
      console.log('Submitted:', this.userForm.value)
    }
  }
}
```

### ルーティング

```typescript
// app-routing.module.ts
import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { HomeComponent } from './home/home.component'
import { AboutComponent } from './about/about.component'
import { UserDetailComponent } from './user-detail/user-detail.component'

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: 'users/:id', component: UserDetailComponent }
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

```html
<!-- app.component.html -->
<nav>
  <a routerLink="/" routerLinkActive="active">Home</a>
  <a routerLink="/about" routerLinkActive="active">About</a>
</nav>
<router-outlet></router-outlet>
```

### RxJS

```typescript
import { Component, OnInit } from '@angular/core'
import { Observable, interval } from 'rxjs'
import { map, filter } from 'rxjs/operators'

@Component({
  selector: 'app-rxjs-example',
  template: `<p>Count: {{ count$ | async }}</p>`
})
export class RxjsExampleComponent implements OnInit {
  count$!: Observable<number>

  ngOnInit() {
    this.count$ = interval(1000).pipe(
      map(n => n * 2),
      filter(n => n % 4 === 0)
    )
  }
}
```

### Pipe

```typescript
// uppercase.pipe.ts
import { Pipe, PipeTransform } from '@angular/core'

@Pipe({
  name: 'uppercase'
})
export class UppercasePipe implements PipeTransform {
  transform(value: string): string {
    return value.toUpperCase()
  }
}

// 使用例
<p>{{ 'hello' | uppercase }}</p>  <!-- HELLO -->
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **Angular** | 🟢 無料 | オープンソース、MIT License |

## メリット

1. **無料**: オープンソース
2. **TypeScript**: 型安全
3. **フルスタック**: 機能豊富
4. **エンタープライズ**: 大規模アプリ対応
5. **Google**: Google支援

## デメリット

1. **学習曲線**: 学習曲線steep
2. **重い**: バンドルサイズ大
3. **複雑**: 複雑な構造
4. **RxJS**: RxJS学習必要

## 公式リンク

- **公式サイト**: [https://angular.io/](https://angular.io/)
- **ドキュメント**: [https://angular.io/docs](https://angular.io/docs)

## 関連ドキュメント

- [フロントエンドフレームワークツール一覧](../フロントエンドフレームワークツール/)
- [React](./React.md)
- [Vue.js](./Vue.js.md)

---

**カテゴリ**: フロントエンドフレームワークツール
**対象工程**: フロントエンド開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
