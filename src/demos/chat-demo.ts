import { Logger } from '../utils/logger.js';
import inquirer from 'inquirer';

/**
 * チャットデモ
 * 
 * このデモでは、GitHub Copilot SDKを使用した対話型チャットの基本を示します。
 * 
 * 主な特徴:
 * - インタラクティブな会話
 * - コンテキストの維持
 * - ストリーミングレスポンス
 */

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

class ChatDemo {
  private conversationHistory: Message[] = [];

  async run(): Promise<void> {
    Logger.header('GitHub Copilot SDK - チャットデモ');
    
    Logger.info('このデモでは、Copilot SDKを使った対話型チャットを体験できます。');
    Logger.info('「exit」と入力すると終了します。\n');

    while (true) {
      const { userMessage } = await inquirer.prompt([
        {
          type: 'input',
          name: 'userMessage',
          message: 'あなた:',
        },
      ]);

      if (userMessage.toLowerCase() === 'exit') {
        Logger.success('チャットを終了します。');
        break;
      }

      // ユーザーメッセージを履歴に追加
      this.conversationHistory.push({
        role: 'user',
        content: userMessage,
      });

      // TODO: ここでGitHub Copilot SDK APIを呼び出す
      // 現在はモック応答を返す
      const response = await this.getMockResponse(userMessage);

      this.conversationHistory.push({
        role: 'assistant',
        content: response,
      });

      Logger.section('Copilot:');
      console.log(response + '\n');
    }

    this.showConversationSummary();
  }

  private async getMockResponse(userMessage: string): Promise<string> {
    // シミュレーション用の遅延
    await new Promise(resolve => setTimeout(resolve, 500));

    // モック応答
    const responses = [
      `「${userMessage}」について理解しました。GitHub Copilot SDKを使えば、このような対話を簡単に実装できます。`,
      `なるほど、「${userMessage}」ですね。SDKのチャット機能を使うと、コンテキストを保持しながら会話を続けられます。`,
      `「${userMessage}」に関して、Copilot SDKは強力なAI機能を提供します。開発者はこれを活用して、インテリジェントなアプリケーションを構築できます。`,
    ];

    return responses[Math.floor(Math.random() * responses.length)];
  }

  private showConversationSummary(): void {
    Logger.section('会話のサマリー');
    Logger.result('総メッセージ数', this.conversationHistory.length.toString());
    Logger.result('ユーザーメッセージ数', 
      this.conversationHistory.filter(m => m.role === 'user').length.toString());
    Logger.result('アシスタント応答数', 
      this.conversationHistory.filter(m => m.role === 'assistant').length.toString());
  }
}

// デモを実行
if (import.meta.url === `file://${process.argv[1]}`) {
  const demo = new ChatDemo();
  demo.run().catch((error) => {
    Logger.error('エラーが発生しました: ' + error.message);
    process.exit(1);
  });
}

export { ChatDemo };
