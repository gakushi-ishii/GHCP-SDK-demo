import { Logger } from './utils/logger.js';
import inquirer from 'inquirer';
import { ChatDemo } from './demos/chat-demo.js';
import { CodeGenerationDemo } from './demos/code-generation-demo.js';
import { ContextAwareDemo } from './demos/context-aware-demo.js';

/**
 * GitHub Copilot SDK デモアプリケーション
 * 
 * このアプリケーションは、GitHub Copilot SDKの主要機能を実演します：
 * 1. 対話型チャット
 * 2. コード生成
 * 3. コンテキスト認識
 */

class DemoApp {
  async run(): Promise<void> {
    this.displayWelcome();

    while (true) {
      const { demo } = await inquirer.prompt([
        {
          type: 'list',
          name: 'demo',
          message: 'デモを選択してください:',
          choices: [
            { name: '💬 チャットデモ - 対話型の会話体験', value: 'chat' },
            { name: '🔨 コード生成デモ - 自然言語からコードを生成', value: 'codegen' },
            { name: '🧠 コンテキスト認識デモ - プロジェクトのコンテキストを理解', value: 'context' },
            { name: '❌ 終了', value: 'exit' },
          ],
        },
      ]);

      if (demo === 'exit') {
        Logger.success('デモアプリケーションを終了します。ご利用ありがとうございました！');
        break;
      }

      await this.runDemo(demo);
      
      console.log('\n');
      const { continueDemo } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'continueDemo',
          message: '他のデモを試しますか？',
          default: true,
        },
      ]);

      if (!continueDemo) {
        Logger.success('デモアプリケーションを終了します。ご利用ありがとうございました！');
        break;
      }
    }
  }

  private displayWelcome(): void {
    console.clear();
    Logger.header('GitHub Copilot SDK デモアプリケーション');
    
    console.log('このデモでは、GitHub Copilot SDKの以下の機能を体験できます:\n');
    console.log('  💬 対話型チャット');
    console.log('     └ 自然な会話を通じた開発支援\n');
    console.log('  🔨 コード生成');
    console.log('     └ 自然言語からの高品質なコード生成\n');
    console.log('  🧠 コンテキスト認識');
    console.log('     └ プロジェクト構造を理解した提案\n');
    
    Logger.info('各デモは独立して実行できます。自由に試してみてください！\n');
  }

  private async runDemo(demoType: string): Promise<void> {
    try {
      switch (demoType) {
        case 'chat':
          const chatDemo = new ChatDemo();
          await chatDemo.run();
          break;

        case 'codegen':
          const codeGenDemo = new CodeGenerationDemo();
          await codeGenDemo.run();
          break;

        case 'context':
          const contextDemo = new ContextAwareDemo();
          await contextDemo.run();
          break;

        default:
          Logger.error('不明なデモタイプです');
      }
    } catch (error) {
      Logger.error('デモの実行中にエラーが発生しました: ' + (error as Error).message);
    }
  }
}

// アプリケーションを起動
const app = new DemoApp();
app.run().catch((error) => {
  Logger.error('アプリケーションエラー: ' + error.message);
  process.exit(1);
});
