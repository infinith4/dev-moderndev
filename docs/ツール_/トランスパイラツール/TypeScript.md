# TypeScript

## 概要

TypeScriptは、Microsoft製のJavaScript拡張言語です。静的型付け、型推論、インターフェース、ジェネリクス、ES6+機能により、大規模JavaScript開発の保守性・品質を向上します。JavaScript スーパーセット、VSCode統合、React/Angular/Vue対応、エンタープライズ採用で広く使用されています。

## 主な機能

### 1. 静的型付け
- **型アノテーション**: 明示的型宣言
- **型推論**: 自動型推論
- **型チェック**: コンパイル時エラー検出
- **厳密性**: strict モード

### 2. 高度な型
- **インターフェース**: 構造定義
- **ジェネリクス**: 型パラメータ
- **ユニオン型**: 複数型
- **型ガード**: 型絞り込み

### 3. ES6+機能
- **class**: クラス構文
- **async/await**: 非同期処理
- **アロー関数**: =>構文
- **デコレータ**: @decorator

### 4. ツール統合
- **tsc**: TypeScriptコンパイラ
- **tsconfig.json**: 設定ファイル
- **型定義**: @types/*
- **IDE統合**: VSCode、IntelliJ

## 利用方法

### インストール

```bash
# グローバルインストール
npm install -g typescript

# プロジェクトローカル
npm install --save-dev typescript

# バージョン確認
tsc --version
```

### 基本的な型

```typescript
// 基本型
let name: string = "Alice"
let age: number = 30
let isStudent: boolean = false
let nothing: null = null
let notDefined: undefined = undefined

// 配列
let numbers: number[] = [1, 2, 3, 4, 5]
let strings: Array<string> = ["a", "b", "c"]

// タプル
let tuple: [string, number] = ["Alice", 30]

// enum
enum Color {
  Red,
  Green,
  Blue
}
let color: Color = Color.Green

// any（型チェックなし）
let anything: any = "hello"
anything = 42
anything = true

// unknown（型安全なany）
let value: unknown = "hello"
if (typeof value === "string") {
  console.log(value.toUpperCase())
}
```

### 関数

```typescript
// 関数型
function add(a: number, b: number): number {
  return a + b
}

// アロー関数
const subtract = (a: number, b: number): number => a - b

// オプショナル引数
function greet(name: string, greeting?: string): string {
  return `${greeting || "Hello"}, ${name}!`
}

// デフォルト引数
function greet2(name: string, greeting: string = "Hello"): string {
  return `${greeting}, ${name}!`
}

// Rest パラメータ
function sum(...numbers: number[]): number {
  return numbers.reduce((acc, n) => acc + n, 0)
}

// 関数型
type MathOperation = (a: number, b: number) => number

const multiply: MathOperation = (a, b) => a * b
```

### インターフェース

```typescript
// インターフェース定義
interface User {
  id: number
  name: string
  email: string
  age?: number  // オプショナル
  readonly createdAt: Date  // 読み取り専用
}

const user: User = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  createdAt: new Date()
}

// インターフェース継承
interface Admin extends User {
  role: string
  permissions: string[]
}

const admin: Admin = {
  id: 1,
  name: "Bob",
  email: "bob@example.com",
  createdAt: new Date(),
  role: "admin",
  permissions: ["read", "write", "delete"]
}

// 関数インターフェース
interface SearchFunc {
  (source: string, subString: string): boolean
}

const mySearch: SearchFunc = (src, sub) => {
  return src.includes(sub)
}
```

### クラス

```typescript
class User {
  // プロパティ
  private id: number
  public name: string
  protected email: string

  // コンストラクタ
  constructor(id: number, name: string, email: string) {
    this.id = id
    this.name = name
    this.email = email
  }

  // メソッド
  greet(): string {
    return `Hello, I'm ${this.name}`
  }

  // Getter/Setter
  get userId(): number {
    return this.id
  }

  // 静的メソッド
  static create(name: string, email: string): User {
    return new User(Date.now(), name, email)
  }
}

// 継承
class Admin extends User {
  role: string

  constructor(id: number, name: string, email: string, role: string) {
    super(id, name, email)
    this.role = role
  }

  greet(): string {
    return `Hello, I'm ${this.name}, role: ${this.role}`
  }
}

// 抽象クラス
abstract class Animal {
  abstract makeSound(): void

  move(): void {
    console.log("Moving...")
  }
}

class Dog extends Animal {
  makeSound(): void {
    console.log("Woof!")
  }
}
```

### ジェネリクス

```typescript
// ジェネリック関数
function identity<T>(arg: T): T {
  return arg
}

const num = identity<number>(42)
const str = identity<string>("hello")

// ジェネリック配列
function getFirst<T>(arr: T[]): T | undefined {
  return arr[0]
}

// ジェネリッククラス
class Box<T> {
  private value: T

  constructor(value: T) {
    this.value = value
  }

  getValue(): T {
    return this.value
  }
}

const numberBox = new Box<number>(42)
const stringBox = new Box<string>("hello")

// ジェネリック制約
interface HasLength {
  length: number
}

function logLength<T extends HasLength>(arg: T): void {
  console.log(arg.length)
}

logLength("hello")  // OK
logLength([1, 2, 3])  // OK
// logLength(42)  // Error
```

### 型エイリアス

```typescript
// 型エイリアス
type ID = number | string

type User = {
  id: ID
  name: string
  email: string
}

// ユニオン型
type Status = "pending" | "approved" | "rejected"

function setStatus(status: Status): void {
  console.log(`Status: ${status}`)
}

setStatus("approved")  // OK
// setStatus("unknown")  // Error

// インターセクション型
type Person = {
  name: string
  age: number
}

type Employee = {
  employeeId: number
  department: string
}

type EmployeePerson = Person & Employee

const employee: EmployeePerson = {
  name: "Alice",
  age: 30,
  employeeId: 12345,
  department: "Engineering"
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.spec.ts"]
}
```

### コンパイル

```bash
# 単一ファイル
tsc index.ts

# プロジェクト全体（tsconfig.json使用）
tsc

# Watch モード
tsc --watch

# 特定設定
tsc --target ES2020 --module commonjs index.ts
```

### React + TypeScript

```typescript
// React コンポーネント
import React, { useState } from 'react'

interface UserProps {
  name: string
  age: number
}

const User: React.FC<UserProps> = ({ name, age }) => {
  return (
    <div>
      <h2>{name}</h2>
      <p>Age: {age}</p>
    </div>
  )
}

// Hooks
function Counter() {
  const [count, setCount] = useState<number>(0)

  const increment = (): void => {
    setCount(count + 1)
  }

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  )
}

// イベントハンドラ
function Form() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault()
    console.log('Submitted')
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    console.log(e.target.value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

### Express + TypeScript

```typescript
import express, { Request, Response, NextFunction } from 'express'

const app = express()

app.use(express.json())

interface User {
  id: number
  name: string
  email: string
}

app.get('/api/users', (req: Request, res: Response) => {
  const users: User[] = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' }
  ]
  res.json(users)
})

app.post('/api/users', (req: Request, res: Response) => {
  const user: User = req.body
  res.status(201).json(user)
})

// エラーハンドリング
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack)
  res.status(500).json({ error: err.message })
})

app.listen(3000, () => {
  console.log('Server running on port 3000')
})
```

### 型定義ファイル

```bash
# @typesインストール
npm install --save-dev @types/node
npm install --save-dev @types/express
npm install --save-dev @types/react
npm install --save-dev @types/jest
```

```typescript
// カスタム型定義（.d.ts）
// types/custom.d.ts
declare module 'my-module' {
  export function myFunction(arg: string): number
}

// グローバル型
declare global {
  interface Window {
    myCustomProperty: string
  }
}
```

## エディション・料金

| エディション | 価格 | 特徴 |
|-------------|------|------|
| **TypeScript** | 🟢 無料 | オープンソース、Apache License |

## メリット

1. **無料**: オープンソース
2. **型安全**: コンパイル時エラー検出
3. **IDE支援**: 強力な補完
4. **JavaScript互換**: 段階的導入可能
5. **大規模開発**: 保守性向上

## デメリット

1. **学習曲線**: 型システム学習必要
2. **ビルドステップ**: コンパイル必要
3. **型定義**: ライブラリ型定義必要
4. **複雑性**: 型システム複雑

## 公式リンク

- **公式サイト**: [https://www.typescriptlang.org/](https://www.typescriptlang.org/)
- **ドキュメント**: [https://www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)

## 関連ドキュメント

- [トランスパイラツール一覧](../トランスパイラツール/)
- [Babel](./Babel.md)
- [Node.js](../ランタイムツール/Node.js.md)

---

**カテゴリ**: トランスパイラツール
**対象工程**: TypeScript開発
**最終更新**: 2025年12月
**ドキュメントバージョン**: 1.0
