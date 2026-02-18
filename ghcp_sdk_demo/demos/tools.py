"""カスタムツールデモ API

GitHub Copilot SDK の @define_tool 機能をデモします。
LLM がカスタムツール（Function Calling）を呼び出す様子をリアルタイムに可視化します。
"""

import asyncio
import json
import os
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from copilot import define_tool

router = APIRouter(tags=["tools"])

DEFAULT_MODEL = os.getenv("COPILOT_MODEL", "gpt-4.1")


# ─── カスタムツール定義 ───


class GetCurrentTimeParams(BaseModel):
    """現在時刻を取得するツールのパラメータ"""

    timezone_name: str = Field(
        default="UTC", description="タイムゾーン名（例: UTC, Asia/Tokyo）"
    )


@define_tool(description="現在の日時を取得します")
async def get_current_time(params: GetCurrentTimeParams) -> str:
    """現在の日時を返す"""
    now = datetime.now(timezone.utc)
    return f"現在の UTC 日時: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"


class CalculateParams(BaseModel):
    """計算ツールのパラメータ"""

    expression: str = Field(description="計算式（例: 2 + 3 * 4）")


@define_tool(description="数式を計算します。四則演算をサポートします。")
async def calculate(params: CalculateParams) -> str:
    """安全に数式を評価する"""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in params.expression):
        return "エラー: 無効な文字が含まれています。数値と演算子のみ使用できます。"
    try:
        result = eval(params.expression)  # noqa: S307
        return f"{params.expression} = {result}"
    except Exception as e:
        return f"計算エラー: {e}"


class FetchWeatherParams(BaseModel):
    """天気取得ツールのパラメータ"""

    city: str = Field(description="都市名（例: 東京, New York）")


@define_tool(description="指定された都市の現在の天気情報を取得します")
async def fetch_weather(params: FetchWeatherParams) -> str:
    """モック天気データを返す（デモ用）"""
    import random

    conditions = ["晴れ ☀️", "曇り ☁️", "雨 🌧️", "雪 ❄️"]
    temp = random.randint(-5, 35)
    condition = random.choice(conditions)
    return f"{params.city}の天気: {condition}, 気温 {temp}°C, 湿度 {random.randint(30, 90)}%"


TOOLS_LIST = [get_current_time, calculate, fetch_weather]


# ─── API エンドポイント ───


class ToolsRequest(BaseModel):
    """ツールデモリクエスト"""

    prompt: str
    model: str = DEFAULT_MODEL


@router.post("/tools")
async def tools_demo(request: ToolsRequest) -> StreamingResponse:
    """カスタムツール付きチャット。ツール呼び出しの過程も SSE で可視化。"""
    from ghcp_sdk_demo.app import get_client

    client = get_client()

    async def event_stream():
        session = await client.create_session(
            {
                "model": request.model,
                "streaming": True,
                "tools": TOOLS_LIST,
                "system_message": {
                    "content": (
                        "あなたはアシスタントです。"
                        "必要に応じてツールを使って正確な情報を提供してください。"
                        "ツールの結果を自然な日本語で説明してください。"
                    )
                },
            }
        )
        done = asyncio.Event()
        chunks: asyncio.Queue[str | None] = asyncio.Queue()

        def on_event(event):
            etype = event.type.value
            if etype == "tool.execution_start":
                tool_name = getattr(event.data, "tool_name", "unknown")
                chunks.put_nowait(
                    f"data: {json.dumps({'type': 'tool_start', 'tool': tool_name})}\n\n"
                )
            elif etype == "assistant.message_delta":
                delta = event.data.delta_content or ""
                if delta:
                    chunks.put_nowait(
                        f"data: {json.dumps({'type': 'delta', 'content': delta})}\n\n"
                    )
            elif etype == "assistant.message":
                content = event.data.content or ""
                chunks.put_nowait(
                    f"data: {json.dumps({'type': 'done', 'content': content})}\n\n"
                )
            elif etype == "session.idle":
                done.set()

        session.on(on_event)
        await session.send({"prompt": request.prompt})

        while not done.is_set() or not chunks.empty():
            try:
                chunk = await asyncio.wait_for(chunks.get(), timeout=0.1)
                yield chunk
            except asyncio.TimeoutError:
                continue

        while not chunks.empty():
            yield chunks.get_nowait()

        await session.destroy()

    return StreamingResponse(event_stream(), media_type="text/event-stream")
