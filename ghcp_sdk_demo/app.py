"""
GitHub Copilot SDK デモアプリケーション

メインエントリーポイント。
対話型メニューから各デモを選択して実行できる。
"""

from __future__ import annotations

import asyncio
import os
import sys

from ghcp_sdk_demo.demos.chat_demo import ChatDemo
from ghcp_sdk_demo.demos.code_generation_demo import CodeGenerationDemo
from ghcp_sdk_demo.demos.context_aware_demo import ContextAwareDemo
from ghcp_sdk_demo.utils.logger import Logger
from ghcp_sdk_demo.utils.prompts import confirm_prompt, select_prompt


class DemoApp:
    """デモアプリケーションのメインクラス"""

    async def run(self) -> None:
        """アプリケーションのメインループ"""
        self._display_welcome()

        while True:
            demo: str = await select_prompt(
                message="デモを選択してください:",
                choices=[
                    {
                        "name": "💬 チャットデモ - 対話型の会話体験",
                        "value": "chat",
                    },
                    {
                        "name": "🔨 コード生成デモ - 自然言語からコードを生成",
                        "value": "codegen",
                    },
                    {
                        "name": "🧠 コンテキスト認識デモ - プロジェクトのコンテキストを理解",
                        "value": "context",
                    },
                    {"name": "❌ 終了", "value": "exit"},
                ],
            )

            if demo == "exit":
                Logger.success(
                    "デモアプリケーションを終了します。ご利用ありがとうございました！"
                )
                break

            await self._run_demo(demo)

            print("\n")
            continue_demo = await confirm_prompt(
                message="他のデモを試しますか？",
                default=True,
            )

            if not continue_demo:
                Logger.success(
                    "デモアプリケーションを終了します。ご利用ありがとうございました！"
                )
                break

    def _display_welcome(self) -> None:
        """ウェルカムメッセージを表示する"""
        os.system("clear" if os.name != "nt" else "cls")
        Logger.header("GitHub Copilot SDK デモアプリケーション")

        print("このデモでは、GitHub Copilot SDKの以下の機能を体験できます:\n")
        print("  💬 対話型チャット")
        print("     └ 自然な会話を通じた開発支援\n")
        print("  🔨 コード生成")
        print("     └ 自然言語からの高品質なコード生成\n")
        print("  🧠 コンテキスト認識")
        print("     └ プロジェクト構造を理解した提案\n")

        Logger.info("各デモは独立して実行できます。自由に試してみてください！\n")

    async def _run_demo(self, demo_type: str) -> None:
        """指定されたデモを実行する"""
        try:
            match demo_type:
                case "chat":
                    chat = ChatDemo()
                    await chat.run()
                case "codegen":
                    codegen = CodeGenerationDemo()
                    await codegen.run()
                case "context":
                    context = ContextAwareDemo()
                    await context.run()
                case _:
                    Logger.error("不明なデモタイプです")
        except Exception as e:
            Logger.error(f"デモの実行中にエラーが発生しました: {e}")


def main() -> None:
    """アプリケーションを起動する"""
    app = DemoApp()
    try:
        asyncio.run(app.run())
    except (KeyboardInterrupt, EOFError):
        print()
        Logger.success(
            "デモアプリケーションを終了します。ご利用ありがとうございました！"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
