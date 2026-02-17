"""
コード生成デモ

GitHub Copilot SDKを使用した自然言語からのコード生成を示すデモ。

主な特徴:
- 自然言語プロンプトからのコード生成
- 複数のプログラミング言語対応
- コンテキストに基づいた生成
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from ghcp_sdk_demo.utils.logger import Logger
from ghcp_sdk_demo.utils.prompts import select_prompt, text_prompt


@dataclass
class CodeGenerationRequest:
    """コード生成リクエスト"""

    description: str
    language: str
    context: str | None = None


class CodeGenerationDemo:
    """自然言語からコードを生成するデモ"""

    EXAMPLES = [
        {"desc": "フィボナッチ数列を計算する関数", "lang": "python"},
        {"desc": "JSONファイルを読み込んでパースする関数", "lang": "python"},
        {"desc": "REST APIのGETリクエストを送信する関数", "lang": "python"},
    ]

    async def run(self) -> None:
        Logger.header("GitHub Copilot SDK - コード生成デモ")

        Logger.info("自然言語の説明から、コードを生成するデモです。\n")

        Logger.section("サンプル例")
        for i, ex in enumerate(self.EXAMPLES, 1):
            print(f"{i}. {ex['desc']} ({ex['lang']})")
        print()

        choices = [
            {"name": f"サンプル{i}: {ex['desc']} ({ex['lang']})", "value": i - 1}
            for i, ex in enumerate(self.EXAMPLES, 1)
        ]
        choices.append({"name": "カスタム: 自分で入力する", "value": -1})

        choice: int = await select_prompt(
            message="デモを選択してください:",
            choices=choices,
        )

        if choice == -1:
            description = await text_prompt(message="コードの説明を入力してください:")
            language: str = await select_prompt(
                message="プログラミング言語を選択してください:",
                choices=["python", "typescript", "javascript", "java", "go", "rust"],
            )
            request = CodeGenerationRequest(description=description, language=language)
        else:
            example = self.EXAMPLES[choice]
            request = CodeGenerationRequest(
                description=example["desc"], language=example["lang"]
            )

        Logger.section("コード生成中...")
        generated_code = await self._generate_code(request)

        Logger.success("コード生成が完了しました！\n")
        Logger.result("説明", request.description)
        Logger.result("言語", request.language)
        Logger.code(generated_code, request.language)

        self._explain_features()

    async def _generate_code(self, request: CodeGenerationRequest) -> str:
        """コードを生成する（将来的にはSDK APIを呼び出す）"""
        # シミュレーション用の遅延
        await asyncio.sleep(1.0)

        # TODO: ここでGitHub Copilot SDK APIを呼び出す
        return self._get_mock_code(request.description, request.language)

    def _get_mock_code(self, description: str, language: str) -> str:
        """モックのコードを返す"""
        if "フィボナッチ" in description and language == "python":
            return '''def fibonacci(n: int) -> int:
    """フィボナッチ数列のn番目の値を返す"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """メモ化版フィボナッチ（最適化）"""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]

    result = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    memo[n] = result
    return result


# 使用例
print(fibonacci(10))        # 55
print(fibonacci_memo(50))   # 12586269025'''

        if "JSON" in description and language == "python":
            return '''import json
from pathlib import Path
from typing import Any


def read_json_file(file_path: str | Path) -> dict[str, Any]:
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
    path = Path(file_path)
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONのパースに失敗しました: {e.msg}") from e


# 使用例
if __name__ == "__main__":
    data = read_json_file("config.json")
    print(data)'''

        if "REST API" in description and language == "python":
            return '''import httpx
from typing import Any


async def fetch_data(
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
) -> Any:
    """
    REST APIのGETリクエストを送信する

    Args:
        url: リクエスト先のURL
        headers: リクエストヘッダー
        params: クエリパラメータ

    Returns:
        レスポンスのJSONデータ

    Raises:
        httpx.HTTPStatusError: HTTPエラーが発生した場合
    """
    default_headers = {"Content-Type": "application/json"}
    if headers:
        default_headers.update(headers)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, headers=default_headers, params=params
        )
        response.raise_for_status()
        return response.json()


# 使用例
if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        data = await fetch_data("https://api.example.com/data")
        print(data)

    asyncio.run(main())'''

        # デフォルトのモックコード
        return f'''# {description}
# Language: {language}
# TODO: GitHub Copilot SDK APIを使用してコードを生成


def example() -> None:
    """Generated code would appear here"""
    print("Code generation demo")
'''

    def _explain_features(self) -> None:
        """GitHub Copilot SDKの特徴を表示する"""
        Logger.section("GitHub Copilot SDKの特徴")
        print("• 自然言語からの正確なコード生成")
        print("• 複数のプログラミング言語に対応")
        print("• プロジェクトのコンテキストを理解した生成")
        print("• ベストプラクティスに準拠したコード")
        print("• エラーハンドリングやドキュメントも含む\n")


def main() -> None:
    """コード生成デモをスタンドアロンで実行する"""
    demo = CodeGenerationDemo()
    try:
        asyncio.run(demo.run())
    except (KeyboardInterrupt, EOFError):
        Logger.info("\nデモを終了しました。")


if __name__ == "__main__":
    main()
