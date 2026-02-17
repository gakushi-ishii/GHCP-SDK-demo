import { Logger } from '../utils/logger.js';
import inquirer from 'inquirer';

/**
 * コード生成デモ
 * 
 * このデモでは、GitHub Copilot SDKを使用した自然言語からのコード生成を示します。
 * 
 * 主な特徴:
 * - 自然言語プロンプトからのコード生成
 * - 複数のプログラミング言語対応
 * - コンテキストに基づいた生成
 */

interface CodeGenerationRequest {
  description: string;
  language: string;
  context?: string;
}

class CodeGenerationDemo {
  async run(): Promise<void> {
    Logger.header('GitHub Copilot SDK - コード生成デモ');
    
    Logger.info('自然言語の説明から、コードを生成するデモです。\n');

    const examples = [
      { desc: 'フィボナッチ数列を計算する関数', lang: 'typescript' },
      { desc: 'JSONファイルを読み込んでパースする関数', lang: 'python' },
      { desc: 'REST APIのGETリクエストを送信する関数', lang: 'javascript' },
    ];

    Logger.section('サンプル例');
    examples.forEach((ex, i) => {
      console.log(`${i + 1}. ${ex.desc} (${ex.lang})`);
    });
    console.log();

    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'choice',
        message: 'デモを選択してください:',
        choices: [
          { name: 'サンプル1: フィボナッチ数列 (TypeScript)', value: 0 },
          { name: 'サンプル2: JSONファイル読み込み (Python)', value: 1 },
          { name: 'サンプル3: REST APIリクエスト (JavaScript)', value: 2 },
          { name: 'カスタム: 自分で入力する', value: -1 },
        ],
      },
    ]);

    let request: CodeGenerationRequest;

    if (answers.choice === -1) {
      const customAnswers = await inquirer.prompt([
        {
          type: 'input',
          name: 'description',
          message: 'コードの説明を入力してください:',
        },
        {
          type: 'list',
          name: 'language',
          message: 'プログラミング言語を選択してください:',
          choices: ['typescript', 'javascript', 'python', 'java', 'go', 'rust'],
        },
      ]);
      request = customAnswers;
    } else {
      const example = examples[answers.choice];
      request = {
        description: example.desc,
        language: example.lang,
      };
    }

    Logger.section('コード生成中...');
    const generatedCode = await this.generateCode(request);

    Logger.success('コード生成が完了しました！\n');
    Logger.result('説明', request.description);
    Logger.result('言語', request.language);
    Logger.code(generatedCode, request.language);

    this.explainFeatures();
  }

  private async generateCode(request: CodeGenerationRequest): Promise<string> {
    // シミュレーション用の遅延
    await new Promise(resolve => setTimeout(resolve, 1000));

    // TODO: ここでGitHub Copilot SDK APIを呼び出す
    // 現在はモックコードを返す
    const mockCode = this.getMockCode(request.description, request.language);
    return mockCode;
  }

  private getMockCode(description: string, language: string): string {
    if (description.includes('フィボナッチ') && language === 'typescript') {
      return `function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// メモ化版（最適化）
function fibonacciMemo(n: number, memo: Map<number, number> = new Map()): number {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n)!;
  
  const result = fibonacciMemo(n - 1, memo) + fibonacciMemo(n - 2, memo);
  memo.set(n, result);
  return result;
}

// 使用例
console.log(fibonacci(10)); // 55
console.log(fibonacciMemo(50)); // 12586269025`;
    }

    if (description.includes('JSON') && language === 'python') {
      return `import json
from typing import Any, Dict

def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    JSONファイルを読み込んでパースする
    
    Args:
        file_path: JSONファイルのパス
        
    Returns:
        パースされたJSONデータ
        
    Raises:
        FileNotFoundError: ファイルが見つからない場合
        json.JSONDecodeError: JSONのパースに失敗した場合
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONのパースに失敗しました: {e.msg}") from e

# 使用例
if __name__ == "__main__":
    data = read_json_file("config.json")
    print(data)`;
    }

    if (description.includes('REST API') && language === 'javascript') {
      return `async function fetchData(url, options = {}) {
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(\`HTTP error! status: \${response.status}\`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// 使用例
fetchData('https://api.example.com/data')
  .then(data => console.log(data))
  .catch(error => console.error(error));`;
    }

    // デフォルトのモックコード
    return `// ${description}
// Language: ${language}
// TODO: GitHub Copilot SDK APIを使用してコードを生成

function example() {
  // Generated code would appear here
  console.log("Code generation demo");
}`;
  }

  private explainFeatures(): void {
    Logger.section('GitHub Copilot SDKの特徴');
    console.log('• 自然言語からの正確なコード生成');
    console.log('• 複数のプログラミング言語に対応');
    console.log('• プロジェクトのコンテキストを理解した生成');
    console.log('• ベストプラクティスに準拠したコード');
    console.log('• エラーハンドリングやドキュメントも含む\n');
  }
}

// デモを実行
if (import.meta.url === `file://${process.argv[1]}`) {
  const demo = new CodeGenerationDemo();
  demo.run().catch((error) => {
    Logger.error('エラーが発生しました: ' + error.message);
    process.exit(1);
  });
}

export { CodeGenerationDemo };
