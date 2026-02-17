"""
InquirerPy ラッパー

型安全なプロンプトユーティリティ。
InquirerPyの型スタブ不備を吸収する。
"""

import importlib
from typing import Any, Sequence

# InquirerPy は型スタブが不完全なため動的にインポート
_inquirer = importlib.import_module("InquirerPy.inquirer")


async def select_prompt(message: str, choices: Sequence[dict[str, Any] | str]) -> Any:
    """選択プロンプトを表示し、選択された値を返す"""
    prompt = _inquirer.select(message=message, choices=choices)
    result: Any = await prompt.execute_async()
    return result


async def text_prompt(message: str) -> str:
    """テキスト入力プロンプトを表示し、入力された文字列を返す"""
    prompt = _inquirer.text(message=message)
    result: Any = await prompt.execute_async()
    return str(result)


async def confirm_prompt(message: str, default: bool = True) -> bool:
    """確認プロンプトを表示し、真偽値を返す"""
    prompt = _inquirer.confirm(message=message, default=default)
    result: Any = await prompt.execute_async()
    return bool(result)
