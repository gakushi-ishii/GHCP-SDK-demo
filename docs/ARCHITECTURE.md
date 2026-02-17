# アーキテクチャガイド

このドキュメントでは、GitHub Copilot SDKデモアプリケーションのアーキテクチャと拡張方法について説明します。

## 全体構成

```
GHCP-SDK-demo/
├── src/                        # ソースコード
│   ├── index.ts               # アプリケーションのエントリーポイント
│   ├── demos/                 # 各デモの実装
│   │   ├── chat-demo.ts      
│   │   ├── code-generation-demo.ts
│   │   └── context-aware-demo.ts
│   └── utils/                 # ユーティリティ
│       └── logger.ts          # ロギング機能
├── dist/                      # ビルド出力（自動生成）
├── docs/                      # ドキュメント
├── package.json
└── tsconfig.json
```

## コアコンポーネント

### 1. DemoApp (index.ts)

メインアプリケーションクラス。対話型メニューを提供し、各デモを起動します。

**主な機能:**
- 起動時のウェルカムメッセージ表示
- デモ選択メニューの提供
- 各デモの実行管理
- ループ処理による連続実行サポート

**拡張方法:**
```typescript
// 新しいデモを追加する場合
import { YourNewDemo } from './demos/your-new-demo.js';

// メニューに追加
choices: [
  { name: '🆕 新しいデモ', value: 'new-demo' },
  // ...
]

// switch文に追加
case 'new-demo':
  const newDemo = new YourNewDemo();
  await newDemo.run();
  break;
```

### 2. Logger (utils/logger.ts)

コンソール出力を視覚的に分かりやすくするユーティリティクラス。

**提供するメソッド:**
- `info()` - 情報メッセージ（青）
- `success()` - 成功メッセージ（緑）
- `error()` - エラーメッセージ（赤）
- `warning()` - 警告メッセージ（黄）
- `header()` - セクションヘッダー
- `section()` - サブセクション
- `code()` - コードブロック表示
- `result()` - キーバリューの表示

### 3. デモクラス

各デモは以下の構造に従います：

```typescript
class YourDemo {
  async run(): Promise<void> {
    // 1. ヘッダー表示
    Logger.header('デモタイトル');
    
    // 2. 説明
    Logger.info('このデモの説明...');
    
    // 3. ユーザー入力
    const answers = await inquirer.prompt([...]);
    
    // 4. 処理実行
    const result = await this.processDemo(answers);
    
    // 5. 結果表示
    this.displayResults(result);
  }
}
```

## デザインパターン

### Single Responsibility Principle (単一責任の原則)

各クラスは明確に定義された単一の責任を持ちます：
- `DemoApp`: アプリケーションの起動とナビゲーション
- 各デモクラス: 特定のデモ機能の実装
- `Logger`: コンソール出力の整形

### Dependency Injection

依存関係は明示的に注入され、テスト可能性を向上させます。

```typescript
// 将来的な拡張例
class ChatDemo {
  constructor(private apiClient?: CopilotApiClient) {
    this.apiClient = apiClient ?? new MockApiClient();
  }
}
```

## 新しいデモの追加方法

### ステップ1: デモクラスを作成

`src/demos/your-new-demo.ts` を作成：

```typescript
import { Logger } from '../utils/logger.js';
import inquirer from 'inquirer';

class YourNewDemo {
  async run(): Promise<void> {
    Logger.header('新しいデモ');
    
    // デモのロジックを実装
  }
}

// スタンドアロン実行をサポート
if (import.meta.url === `file://${process.argv[1]}`) {
  const demo = new YourNewDemo();
  demo.run().catch((error) => {
    Logger.error('エラー: ' + error.message);
    process.exit(1);
  });
}

export { YourNewDemo };
```

### ステップ2: package.jsonにスクリプトを追加

```json
{
  "scripts": {
    "demo:your-new": "tsx src/demos/your-new-demo.ts"
  }
}
```

### ステップ3: メインアプリに統合

`src/index.ts` を編集：

```typescript
import { YourNewDemo } from './demos/your-new-demo.js';

// メニューに追加
choices: [
  { name: '🆕 Your New Demo', value: 'your-new' },
  // ...
]

// 実行ロジックに追加
case 'your-new':
  const yourNewDemo = new YourNewDemo();
  await yourNewDemo.run();
  break;
```

## API統合の準備

現在はモック応答を使用していますが、実際のGitHub Copilot SDK APIと統合する準備が整っています。

### 統合手順

1. **環境変数の設定**
```bash
cp .env.example .env
# .envファイルを編集してGITHUB_TOKENを設定
```

2. **APIクライアントの実装**
```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

class CopilotApiClient {
  private client: Client;
  
  async chat(message: string): Promise<string> {
    // 実際のAPI呼び出し
  }
  
  async generateCode(prompt: string): Promise<string> {
    // コード生成API呼び出し
  }
}
```

3. **デモクラスの更新**
```typescript
class ChatDemo {
  constructor(private apiClient = new CopilotApiClient()) {}
  
  private async getMockResponse(msg: string): Promise<string> {
    // モックの代わりに実際のAPIを呼び出す
    return this.apiClient.chat(msg);
  }
}
```

## テスト戦略

### 単体テスト（今後実装予定）

```typescript
// __tests__/logger.test.ts
import { Logger } from '../src/utils/logger';

describe('Logger', () => {
  it('should format info messages correctly', () => {
    // テストロジック
  });
});
```

### 統合テスト

```typescript
// __tests__/demos/chat-demo.test.ts
import { ChatDemo } from '../src/demos/chat-demo';

describe('ChatDemo', () => {
  it('should handle user input correctly', async () => {
    // テストロジック
  });
});
```

## パフォーマンス最適化

### ストリーミングレスポンス

将来的にストリーミングAPIを使用する場合：

```typescript
async function* streamResponse(prompt: string) {
  const stream = await apiClient.streamChat(prompt);
  
  for await (const chunk of stream) {
    yield chunk;
  }
}

// 使用例
for await (const chunk of streamResponse(userMessage)) {
  process.stdout.write(chunk);
}
```

### キャッシング

頻繁に使用されるリクエストをキャッシュ：

```typescript
class CacheManager {
  private cache = new Map<string, any>();
  
  async get(key: string, fetcher: () => Promise<any>) {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    const value = await fetcher();
    this.cache.set(key, value);
    return value;
  }
}
```

## ベストプラクティス

1. **エラーハンドリング**: すべての非同期処理で適切にエラーをキャッチ
2. **型安全性**: TypeScriptの型システムを最大限活用
3. **ログ**: 重要な操作はLoggerを使用して記録
4. **モジュラリティ**: 機能を小さく再利用可能なモジュールに分割
5. **ドキュメント**: コードにJSDocコメントを追加

## 今後の拡張アイデア

- [ ] Webインターフェース（React/Vue）
- [ ] データベース連携（会話履歴の保存）
- [ ] マルチユーザーサポート
- [ ] プラグインシステム
- [ ] リアルタイムコラボレーション
- [ ] カスタムエージェントの作成
- [ ] メトリクス・分析ダッシュボード

## リファレンス

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Inquirer.js Documentation](https://github.com/SBoudrias/Inquirer.js)
- [Chalk Documentation](https://github.com/chalk/chalk)
- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/sdk)
