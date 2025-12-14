# CoffeeScript

## 概要

**CoffeeScript**は、JavaScriptにコンパイルされるプログラミング言語です。Rubyライクな簡潔な構文、クラス構文、リスト内包表記により、JavaScriptをより読みやすく、表現力豊かに記述できます。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Jeremy Ashkenas |
| **種別** | AltJS（JavaScriptトランスパイラ） |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://coffeescript.org/ |
| **ドキュメント** | https://coffeescript.org/#language |

**注意**: CoffeeScriptは2010年代に人気を博しましたが、ES6+の登場により、新規プロジェクトではTypeScriptやES6+の使用が推奨されています。

## 主な特徴

### 1. 簡潔な構文
- **インデントベース**: 波括弧不要
- **セミコロン不要**: 自動挿入
- **functionキーワード**: `->` で代替
- **変数宣言**: var自動挿入

### 2. Rubyライクな文法
- **リスト内包表記**: `[x * 2 for x in [1..10]]`
- **条件式後置**: `alert 'hello' if condition`
- **範囲演算子**: `[1..10]`、`[1...10]`
- **存在チェック**: `?` 演算子

### 3. クラス構文
- **classキーワード**: ES6以前からサポート
- **継承**: `extends`
- **スーパークラス**: `super`
- **プロトタイプ**: 自動生成

### 4. 関数機能
- **デフォルト引数**: `(a = 1) ->`
- **可変長引数**: `(args...) ->`
- **分割代入**: `{name, age} = user`
- **アロー関数**: `->` と `=>`

## 使い方

### インストール

```bash
# npm インストール
npm install -g coffeescript

# バージョン確認
coffee --version

# コンパイル
coffee -c script.coffee

# ウォッチモード
coffee -cw script.coffee

# 直接実行
coffee script.coffee
```

### 基本構文

```coffeescript
# 変数・定数
name = 'Alice'
age = 30
isActive = true

# 関数定義
square = (x) -> x * x

# 複数行関数
add = (a, b) ->
  result = a + b
  result

# アロー関数（thisバインド）
class Counter
  constructor: ->
    @count = 0

  increment: =>
    @count++

# デフォルト引数
greet = (name = 'Guest') ->
  "Hello, #{name}!"

# 可変長引数
sum = (nums...) ->
  total = 0
  total += num for num in nums
  total

# 分割代入
{name, age} = user: {name: 'Alice', age: 30}
[first, second, rest...] = [1, 2, 3, 4, 5]
```

### 条件分岐

```coffeescript
# if文
if age >= 18
  console.log 'Adult'
else
  console.log 'Minor'

# 後置if
console.log 'Adult' if age >= 18

# unless（ifの否定）
unless age < 18
  console.log 'Adult'

# 三項演算子
status = if age >= 18 then 'Adult' else 'Minor'

# switch文
switch day
  when 'Monday' then 'Start of week'
  when 'Friday' then 'End of week'
  else 'Middle of week'
```

### ループ

```coffeescript
# for..in（配列）
numbers = [1, 2, 3, 4, 5]
for num in numbers
  console.log num

# for..of（オブジェクト）
user = {name: 'Alice', age: 30}
for key, value of user
  console.log "#{key}: #{value}"

# リスト内包表記
squares = (x * x for x in [1..10])
evens = (x for x in [1..10] when x % 2 == 0)

# while
i = 0
while i < 5
  console.log i
  i++

# until
i = 0
until i == 5
  console.log i
  i++

# 範囲
for i in [1..5]   # 1, 2, 3, 4, 5
  console.log i

for i in [1...5]  # 1, 2, 3, 4
  console.log i
```

### クラス

```coffeescript
# クラス定義
class Animal
  constructor: (@name) ->
    @sound = 'generic sound'

  makeSound: ->
    console.log "#{@name} makes #{@sound}"

  @staticMethod: ->
    console.log 'This is a static method'

# 継承
class Dog extends Animal
  constructor: (name) ->
    super name
    @sound = 'bark'

  fetch: ->
    console.log "#{@name} is fetching"

# インスタンス化
dog = new Dog('Rex')
dog.makeSound()  # Rex makes bark
dog.fetch()      # Rex is fetching

# 静的メソッド
Animal.staticMethod()
```

### 配列・オブジェクト操作

```coffeescript
# 配列
numbers = [1, 2, 3, 4, 5]

# map
doubled = numbers.map (x) -> x * 2

# filter
evens = numbers.filter (x) -> x % 2 == 0

# reduce
sum = numbers.reduce (acc, x) -> acc + x, 0

# オブジェクト
user =
  name: 'Alice'
  age: 30
  email: 'alice@example.com'

# オブジェクト拡張
adminUser = {user..., role: 'admin'}

# 存在チェック
console.log user.name?  # true
console.log user.phone? # false

# 安全なメソッド呼び出し
user.greet?()  # undefined（エラーにならない）
```

### 文字列操作

```coffeescript
# 文字列補間
name = 'Alice'
age = 30
message = "Hello, #{name}. You are #{age} years old."

# 複数行文字列
longText = """
  This is a
  multi-line
  string.
  """

# ヒアドキュメント
html = """
  <div>
    <h1>#{title}</h1>
    <p>#{content}</p>
  </div>
  """
```

### 存在演算子

```coffeescript
# 存在チェック（?）
name = user?.name
email = user?.email ? 'default@example.com'

# null合体
value = nullValue ? defaultValue

# 安全なメソッド呼び出し
result = obj?.method?()

# 条件付き代入
name ?= 'Guest'  # nameがnull/undefinedの場合のみ代入
```

### Promise・非同期

```coffeescript
# Promise
fetchData = ->
  new Promise (resolve, reject) ->
    setTimeout ->
      resolve {data: 'Hello'}
    , 1000

# async/await（CoffeeScript 2+）
fetchUser = (id) ->
  response = await fetch("/api/users/#{id}")
  user = await response.json()
  user

# then/catch
fetchData()
  .then (result) ->
    console.log result
  .catch (error) ->
    console.error error
```

### Node.js統合

```coffeescript
# モジュール読み込み
fs = require 'fs'
http = require 'http'

# Expressサーバー
express = require 'express'
app = express()

app.get '/', (req, res) ->
  res.send 'Hello from CoffeeScript!'

app.listen 3000, ->
  console.log 'Server running on port 3000'

# ファイル読み込み
fs.readFile 'file.txt', 'utf8', (err, data) ->
  if err
    console.error err
  else
    console.log data
```

### ビルドツール統合

#### Webpack

```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.coffee',
  output: {
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.coffee$/,
        use: 'coffee-loader'
      }
    ]
  },
  resolve: {
    extensions: ['.coffee', '.js']
  }
};
```

```bash
npm install --save-dev coffee-loader coffeescript
```

#### Gulp

```javascript
// gulpfile.js
const gulp = require('gulp');
const coffee = require('gulp-coffee');

gulp.task('coffee', () => {
  return gulp.src('./src/**/*.coffee')
    .pipe(coffee({bare: true}))
    .pipe(gulp.dest('./dist/'));
});

gulp.task('watch', () => {
  gulp.watch('./src/**/*.coffee', gulp.series('coffee'));
});
```

```bash
npm install --save-dev gulp gulp-coffee
```

### テスト（Mocha）

```coffeescript
# test/sample.spec.coffee
{expect} = require 'chai'
Calculator = require '../src/calculator'

describe 'Calculator', ->
  calc = null

  beforeEach ->
    calc = new Calculator()

  describe 'add', ->
    it 'should add two numbers', ->
      result = calc.add 2, 3
      expect(result).to.equal 5

  describe 'subtract', ->
    it 'should subtract two numbers', ->
      result = calc.subtract 5, 3
      expect(result).to.equal 2
```

```json
// package.json
{
  "scripts": {
    "test": "mocha --require coffeescript/register test/**/*.spec.coffee"
  }
}
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | アプリケーション開発 | Webアプリ、Node.jsバックエンド |
| **実装** | スクリプト記述 | ビルドスクリプト、自動化 |
| **テスト** | テストコード | Mocha、Jasmine統合 |
| **レガシー保守** | 既存コード維持 | CoffeeScriptで書かれた既存プロジェクト |

## メリット

- **簡潔な構文**: JavaScript比で30%短い
- **Rubyライク**: Ruby開発者に親しみやすい
- **リスト内包表記**: 配列操作が簡潔
- **クラス構文**: ES6以前からサポート
- **可読性**: インデントベース
- **JavaScriptと互換**: 既存ライブラリ使用可能
- **無料**: オープンソース

## デメリット

- **メンテナンス停滞**: 2010年代以降開発鈍化
- **TypeScript優勢**: 型安全性でTypeScript推奨
- **ES6+登場**: 多くの機能が標準化
- **学習コスト**: JavaScript習得後さらに学習
- **デバッグ困難**: 生成されたJavaScriptのデバッグ
- **エコシステム縮小**: ツール・ライブラリ減少
- **新規非推奨**: 新規プロジェクトでは使用推奨されず

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **CoffeeScript** | Rubyライク、簡潔 | 無料 | レガシー保守 |
| **TypeScript** | 型安全、IDE統合 | 無料 | モダン開発推奨 |
| **Babel（ES6+）** | JavaScript標準、最新仕様 | 無料 | 標準JavaScript |
| **Dart** | Flutter、Google開発 | 無料 | モバイル開発 |

## ベストプラクティス

### 1. ES6+への移行検討

```bash
# decaffeinate で CoffeeScript → JavaScript 変換
npm install -g decaffeinate
decaffeinate script.coffee
```

### 2. リスト内包表記活用

```coffeescript
# 簡潔な配列操作
squares = (x * x for x in [1..10] when x % 2 == 0)
```

### 3. 存在演算子で安全なコード

```coffeescript
# null/undefined チェック
name = user?.name ? 'Guest'
```

### 4. クラス構文で構造化

```coffeescript
# オブジェクト指向設計
class Model extends BaseModel
  constructor: (@data) ->

  save: ->
    # 保存処理
```

## 公式リソース

- **公式サイト**: https://coffeescript.org/
- **ドキュメント**: https://coffeescript.org/#language
- **GitHub**: https://github.com/jashkenas/coffeescript
- **Cookbook**: https://coffeescript-cookbook.github.io/
- **移行ツール（decaffeinate）**: https://github.com/decaffeinate/decaffeinate

## まとめ

CoffeeScriptは、JavaScriptにコンパイルされるRubyライクなプログラミング言語です。簡潔な構文、リスト内包表記、クラス構文により、JavaScriptをより読みやすく記述できます。ただし、ES6+の登場により多くの機能が標準化され、新規プロジェクトではTypeScriptやES6+の使用が推奨されています。既存のCoffeeScriptプロジェクトの保守には有用です。

---

**最終更新**: 2025-12-10
**対象バージョン**: CoffeeScript 2.7+
**推奨**: 新規プロジェクトではTypeScript/ES6+を推奨
