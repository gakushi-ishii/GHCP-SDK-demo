"""
チャットデモ

GitHub Copilot SDKを使用した対話型チャットの基本を示すデモ。

主な特徴:
- インタラクティブな会話
- コンテキストの維持
- ストリーミングレスポンス（実装予定）
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from typing import Literal

from ghcp_sdk_demo.utils.logger import Logger
from ghcp_sdk_demo.utils.prompts import text_prompt


@dataclass
class Message:
    """チャットメッセージ"""

    role: Literal["user", "assistant"]
    content: str


class ChatDemo:
    """対話型チャットデモ"""

    def __init__(self) -> None:
        self._history: list[Message] = []

    async def run(self) -> None:
        Logger.header("GitHub Copilot SDK - チャットデモ")

        Logger.info("このデモでは、Copilot SDKを使った対話型チャットを体験できます。")
        Logger.info("「exit」と入力すると終了します。\n")

        while True:
            user_message = await text_prompt(message="あなた:")

            if user_message.lower() == "exit":
                Logger.success("チャットを終了します。")
                break

            # ユーザーメッセージを履歴に追加
            self._history.append(Message(role="user", content=user_message))

            # TODO: ここでGitHub Copilot SDK APIを呼び出す
            # 現在はモック応答を返す
            response = await self._get_mock_response(user_message)

            self._history.append(Message(role="assistant", content=response))

            Logger.section("Copilot:")
            print(response + "\n")

        self._show_conversation_summary()

    async def _get_mock_response(self, user_message: str) -> str:
        """モック応答を生成する（将来的にはSDK APIを呼び出す）"""
        # シミュレーション用の遅延
        await asyncio.sleep(0.5)

        responses = [
            f"「{user_message}」について理解しました。GitHub Copilot SDKを使えば、このような対話を簡単に実装できます。",
            f"なるほど、「{user_message}」ですね。SDKのチャット機能を使うと、コンテキストを保持しながら会話を続けられます。",
            f"「{user_message}」に関して、Copilot SDKは強力なAI機能を提供します。開発者はこれを活用して、インテリジェントなアプリケーションを構築できます。",
        ]

        return random.choice(responses)

    def _show_conversation_summary(self) -> None:
        """会話のサマリーを表示する"""
        Logger.section("会話のサマリー")
        Logger.result("総メッセージ数", str(len(self._history)))
        Logger.result(
            "ユーザーメッセージ数",
            str(sum(1 for m in self._history if m.role == "user")),
        )
        Logger.result(
            "アシスタント応答数",
            str(sum(1 for m in self._history if m.role == "assistant")),
        )


def main() -> None:
    """チャットデモをスタンドアロンで実行する"""
    demo = ChatDemo()
    try:
        asyncio.run(demo.run())
    except (KeyboardInterrupt, EOFError):
        Logger.info("\nチャットを終了しました。")


if __name__ == "__main__":
    main()
