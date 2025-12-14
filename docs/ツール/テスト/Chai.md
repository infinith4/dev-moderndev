# Chai

## 概要

**Chai**は、Node.js・ブラウザ向けのBDD（振る舞い駆動開発）/TDD（テスト駆動開発）アサーションライブラリです。should、expect、assertの3スタイルをサポートし、Mocha、Jest等のテストフレームワークと統合して、自然言語に近い読みやすいテストコードを実現します。

## 基本情報

| 項目 | 内容 |
|------|------|
| **開発元** | Jake Luer / オープンソースコミュニティ |
| **種別** | JavaScriptアサーションライブラリ |
| **ライセンス** | MIT License（オープンソース） |
| **料金** | 🟢 無料 |
| **公式サイト** | https://www.chaijs.com/ |
| **ドキュメント** | https://www.chaijs.com/api/ |

## 主な特徴

### 1. 3つのアサーションスタイル
- **Should**: BDDスタイル、自然言語表現
- **Expect**: BDDスタイル、チェーン可能
- **Assert**: TDDスタイル、Node.js標準互換
- **スタイル混在可**: プロジェクトで統一推奨

### 2. プラグインエコシステム
- **chai-http**: HTTPリクエストテスト
- **chai-as-promised**: Promiseアサーション
- **sinon-chai**: Sinon.jsスパイ・スタブ
- **chai-dom**: DOM要素アサーション

### 3. テストフレームワーク統合
- **Mocha**: 最も人気の組み合わせ
- **Jest**: Jestビルトインexpect拡張
- **Karma**: ブラウザテスト
- **WebdriverIO**: E2Eテスト

### 4. TypeScript対応
- **型定義**: @types/chai
- **型安全**: アサーションの型推論
- **ジェネリック**: カスタムアサーション

## 使い方

### セットアップ

```bash
# npm インストール
npm install --save-dev chai

# yarn インストール
yarn add --dev chai

# Mocha と一緒にインストール
npm install --save-dev mocha chai

# TypeScript型定義
npm install --save-dev @types/chai
```

### Should スタイル

```javascript
// test/should.test.js
const chai = require('chai');
chai.should();

describe('Shouldスタイル', function() {
  it('数値の比較', function() {
    const num = 42;
    num.should.equal(42);
    num.should.be.a('number');
    num.should.be.above(40);
    num.should.be.below(50);
  });

  it('文字列の検証', function() {
    const str = 'Hello World';
    str.should.be.a('string');
    str.should.have.lengthOf(11);
    str.should.include('World');
    str.should.match(/^Hello/);
  });

  it('配列の検証', function() {
    const arr = [1, 2, 3, 4, 5];
    arr.should.be.an('array');
    arr.should.have.lengthOf(5);
    arr.should.include(3);
    arr.should.deep.equal([1, 2, 3, 4, 5]);
  });

  it('オブジェクトの検証', function() {
    const obj = { name: 'Alice', age: 30 };
    obj.should.be.an('object');
    obj.should.have.property('name');
    obj.should.have.property('age', 30);
    obj.should.deep.equal({ name: 'Alice', age: 30 });
  });

  it('真偽値の検証', function() {
    const bool = true;
    bool.should.be.true;
    bool.should.not.be.false;
    bool.should.equal(true);
  });
});
```

### Expect スタイル

```javascript
// test/expect.test.js
const { expect } = require('chai');

describe('Expectスタイル', function() {
  it('数値の比較', function() {
    const num = 42;
    expect(num).to.equal(42);
    expect(num).to.be.a('number');
    expect(num).to.be.above(40);
    expect(num).to.be.below(50);
    expect(num).to.be.within(40, 50);
  });

  it('文字列の検証', function() {
    const str = 'Hello World';
    expect(str).to.be.a('string');
    expect(str).to.have.lengthOf(11);
    expect(str).to.include('World');
    expect(str).to.match(/^Hello/);
    expect(str).to.not.be.empty;
  });

  it('配列の検証', function() {
    const arr = [1, 2, 3, 4, 5];
    expect(arr).to.be.an('array');
    expect(arr).to.have.lengthOf(5);
    expect(arr).to.include(3);
    expect(arr).to.include.members([2, 3, 4]);
    expect(arr).to.deep.equal([1, 2, 3, 4, 5]);
  });

  it('オブジェクトの検証', function() {
    const obj = { name: 'Alice', age: 30 };
    expect(obj).to.be.an('object');
    expect(obj).to.have.property('name');
    expect(obj).to.have.property('age').that.equals(30);
    expect(obj).to.have.all.keys('name', 'age');
    expect(obj).to.deep.equal({ name: 'Alice', age: 30 });
  });

  it('真偽値の検証', function() {
    expect(true).to.be.true;
    expect(false).to.be.false;
    expect(1).to.be.ok;
    expect(0).to.not.be.ok;
    expect(null).to.be.null;
    expect(undefined).to.be.undefined;
  });
});
```

### Assert スタイル

```javascript
// test/assert.test.js
const { assert } = require('chai');

describe('Assertスタイル', function() {
  it('数値の比較', function() {
    const num = 42;
    assert.equal(num, 42);
    assert.typeOf(num, 'number');
    assert.isAbove(num, 40);
    assert.isBelow(num, 50);
  });

  it('文字列の検証', function() {
    const str = 'Hello World';
    assert.typeOf(str, 'string');
    assert.lengthOf(str, 11);
    assert.include(str, 'World');
    assert.match(str, /^Hello/);
  });

  it('配列の検証', function() {
    const arr = [1, 2, 3, 4, 5];
    assert.isArray(arr);
    assert.lengthOf(arr, 5);
    assert.include(arr, 3);
    assert.deepEqual(arr, [1, 2, 3, 4, 5]);
  });

  it('オブジェクトの検証', function() {
    const obj = { name: 'Alice', age: 30 };
    assert.isObject(obj);
    assert.property(obj, 'name');
    assert.propertyVal(obj, 'age', 30);
    assert.deepEqual(obj, { name: 'Alice', age: 30 });
  });

  it('真偽値の検証', function() {
    assert.isTrue(true);
    assert.isFalse(false);
    assert.isOk(1);
    assert.isNotOk(0);
    assert.isNull(null);
    assert.isUndefined(undefined);
  });
});
```

### 非同期テスト

```javascript
// test/async.test.js
const { expect } = require('chai');

describe('非同期テスト', function() {
  it('Promise（then/catch）', function(done) {
    const promise = Promise.resolve(42);
    promise.then(result => {
      expect(result).to.equal(42);
      done();
    }).catch(done);
  });

  it('async/await', async function() {
    const result = await Promise.resolve(42);
    expect(result).to.equal(42);
  });

  it('非同期関数のエラー', async function() {
    const asyncFunc = async () => {
      throw new Error('Test error');
    };

    try {
      await asyncFunc();
      expect.fail('Should have thrown an error');
    } catch (err) {
      expect(err.message).to.equal('Test error');
    }
  });
});
```

### chai-as-promised プラグイン

```bash
# インストール
npm install --save-dev chai-as-promised
```

```javascript
// test/promise.test.js
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);

const { expect } = chai;

describe('Promise アサーション', function() {
  it('Promiseが解決される', function() {
    const promise = Promise.resolve(42);
    return expect(promise).to.eventually.equal(42);
  });

  it('Promiseが拒否される', function() {
    const promise = Promise.reject(new Error('Failed'));
    return expect(promise).to.be.rejectedWith('Failed');
  });

  it('オブジェクトを返すPromise', function() {
    const promise = Promise.resolve({ name: 'Alice' });
    return expect(promise).to.eventually.have.property('name', 'Alice');
  });
});
```

### chai-http プラグイン

```bash
# インストール
npm install --save-dev chai-http
```

```javascript
// test/http.test.js
const chai = require('chai');
const chaiHttp = require('chai-http');
chai.use(chaiHttp);

const { expect } = chai;
const app = require('../app'); // Expressアプリ

describe('HTTP API テスト', function() {
  it('GET /api/users', function(done) {
    chai.request(app)
      .get('/api/users')
      .end((err, res) => {
        expect(res).to.have.status(200);
        expect(res.body).to.be.an('array');
        expect(res.body).to.have.lengthOf.above(0);
        done();
      });
  });

  it('POST /api/users', function(done) {
    const newUser = { name: 'Alice', email: 'alice@example.com' };

    chai.request(app)
      .post('/api/users')
      .send(newUser)
      .end((err, res) => {
        expect(res).to.have.status(201);
        expect(res.body).to.have.property('id');
        expect(res.body).to.have.property('name', 'Alice');
        done();
      });
  });

  it('GET /api/users/:id', async function() {
    const res = await chai.request(app).get('/api/users/1');
    expect(res).to.have.status(200);
    expect(res.body).to.have.property('id', 1);
  });
});
```

### sinon-chai プラグイン

```bash
# インストール
npm install --save-dev sinon sinon-chai
```

```javascript
// test/spy.test.js
const chai = require('chai');
const sinon = require('sinon');
const sinonChai = require('sinon-chai');
chai.use(sinonChai);

const { expect } = chai;

describe('Sinon スパイ・スタブ', function() {
  it('スパイで関数呼び出しを検証', function() {
    const callback = sinon.spy();
    const fn = (cb) => cb('Hello');

    fn(callback);

    expect(callback).to.have.been.calledOnce;
    expect(callback).to.have.been.calledWith('Hello');
  });

  it('スタブで戻り値を制御', function() {
    const obj = { getData: () => 'original' };
    const stub = sinon.stub(obj, 'getData').returns('mocked');

    expect(obj.getData()).to.equal('mocked');
    expect(stub).to.have.been.calledOnce;

    stub.restore();
  });

  it('モックで複雑な検証', function() {
    const obj = { save: () => {} };
    const mock = sinon.mock(obj);

    mock.expects('save').once().withArgs({ name: 'Alice' });

    obj.save({ name: 'Alice' });

    mock.verify();
    mock.restore();
  });
});
```

### カスタムアサーション

```javascript
// test/custom.test.js
const chai = require('chai');

// カスタムアサーション定義
chai.use(function(chai, utils) {
  chai.Assertion.addMethod('even', function() {
    const obj = this._obj;

    this.assert(
      obj % 2 === 0,
      'expected #{this} to be even',
      'expected #{this} to not be even'
    );
  });
});

const { expect } = chai;

describe('カスタムアサーション', function() {
  it('偶数の検証', function() {
    expect(2).to.be.even();
    expect(4).to.be.even();
    expect(5).to.not.be.even();
  });
});
```

### TypeScript統合

```typescript
// test/typescript.test.ts
import { expect } from 'chai';

describe('TypeScript テスト', () => {
  interface User {
    id: number;
    name: string;
    email: string;
  }

  it('型安全なアサーション', () => {
    const user: User = {
      id: 1,
      name: 'Alice',
      email: 'alice@example.com'
    };

    expect(user).to.have.property('id').that.is.a('number');
    expect(user.name).to.equal('Alice');
    expect(user.email).to.match(/@/);
  });

  it('ジェネリック型の検証', () => {
    const users: User[] = [
      { id: 1, name: 'Alice', email: 'alice@example.com' },
      { id: 2, name: 'Bob', email: 'bob@example.com' }
    ];

    expect(users).to.have.lengthOf(2);
    expect(users[0]).to.have.property('name', 'Alice');
  });
});
```

## 開発工程での利用

| 工程 | 用途 | 詳細 |
|------|------|------|
| **実装** | ユニットテスト | 関数・モジュール単体テスト |
| **実装** | TDD/BDD | テスト駆動開発・振る舞い駆動開発 |
| **テスト** | 統合テスト | API・データベーステスト |
| **テスト** | E2Eテスト | ブラウザ自動化テスト |

## メリット

- **読みやすい**: 自然言語に近いアサーション
- **3スタイル**: Should、Expect、Assert
- **プラグイン豊富**: HTTP、Promise、Sinon等
- **フレームワーク統合**: Mocha、Jest、Karma
- **TypeScript対応**: 型定義、型安全
- **無料**: オープンソース
- **軽量**: 小さなライブラリサイズ

## デメリット

- **学習曲線**: 3スタイルの違い
- **プラグイン必須**: Promise、HTTPテスト
- **単体では不完全**: テストランナー別途必要
- **Jestビルトイン**: Jestには独自expectあり
- **メンテナンス**: 一部プラグイン更新停滞

## 類似ツールとの比較

| ツール | 特徴 | 料金 | 適用場面 |
|--------|------|------|----------|
| **Chai** | BDD/TDD、3スタイル | 無料 | Mocha、汎用 |
| **Jest（expect）** | ビルトイン、スナップショット | 無料 | React、統合環境 |
| **Assert（Node.js）** | 標準、シンプル | 無料 | Node.js標準 |
| **Should.js** | BDD専用、Chai派生 | 無料 | BDDスタイル |

## ベストプラクティス

### 1. スタイルの統一

```javascript
// プロジェクト全体でExpectスタイルに統一
const { expect } = require('chai');

// 全テストで使用
expect(value).to.equal(42);
```

### 2. 詳細なエラーメッセージ

```javascript
// カスタムメッセージ
expect(user.age, '年齢は18以上である必要があります').to.be.at.least(18);
```

### 3. deep.equal の使用

```javascript
// オブジェクト・配列の比較はdeep.equal
expect(obj).to.deep.equal({ name: 'Alice' });
expect(arr).to.deep.equal([1, 2, 3]);
```

### 4. プラグインの活用

```javascript
// chai-as-promisedでPromiseテストを簡潔に
return expect(promise).to.eventually.equal(42);

// chai-httpでAPIテストを簡潔に
return chai.request(app).get('/api/users').then(res => {
  expect(res).to.have.status(200);
});
```

## 公式リソース

- **公式サイト**: https://www.chaijs.com/
- **APIドキュメント**: https://www.chaijs.com/api/
- **プラグイン**: https://www.chaijs.com/plugins/
- **GitHub**: https://github.com/chaijs/chai
- **チュートリアル**: https://www.chaijs.com/guide/

## まとめ

Chaiは、Node.js・ブラウザ向けのBDD/TDDアサーションライブラリです。should、expect、assertの3スタイルをサポートし、Mocha、Jest等のテストフレームワークと統合して、自然言語に近い読みやすいテストコードを実現します。豊富なプラグインエコシステムにより、HTTP、Promise、スパイ・スタブ等の高度なテストシナリオにも対応します。

---

**最終更新**: 2025-12-10
**対象バージョン**: Chai 4.x / 5.x
