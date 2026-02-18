"""コード生成デモ API

GitHub Copilot SDK を使って自然言語の説明からコードを生成します。
system_message オプションでコード生成に特化した指示を設定します。
"""

import asyncio
import json
import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(tags=["codegen"])

DEFAULT_MODEL = os.getenv("COPILOT_MODEL", "gpt-4.1")

CODEGEN_SYSTEM_MESSAGE = {
    "content": (
        "あなたは優秀なプログラマーです。"
        "ユーザーの説明に基づいて、クリーンで動作するコードを生成してください。"
        "コードのみを出力し、必要に応じてコメントを付けてください。"
        "言語はユーザーが指定した言語を使用してください。"
    )
}


class CodegenRequest(BaseModel):
    """コード生成リクエスト"""

    description: str
    language: str = "python"
    model: str = DEFAULT_MODEL


@router.post("/codegen")
async def codegen(request: CodegenRequest) -> StreamingResponse:
    """コード生成。自然言語の説明からコードを生成して SSE で配信。"""
    from ghcp_sdk_demo.app import get_client

    client = get_client()
    prompt = f"言語: {request.language}\n\n{request.description}"

    async def event_stream():
        session = await client.create_session(
            {
                "model": request.model,
                "streaming": True,
                "system_message": CODEGEN_SYSTEM_MESSAGE,
            }
        )
        done = asyncio.Event()
        chunks: asyncio.Queue[str | None] = asyncio.Queue()

        def on_event(event):
            etype = event.type.value
            if etype == "assistant.message_delta":
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
        await session.send({"prompt": prompt})

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
