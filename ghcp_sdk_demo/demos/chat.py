"""チャットデモ API

GitHub Copilot SDK のストリーミングチャット機能をデモします。
SSE (Server-Sent Events) でリアルタイムにレスポンスを配信します。
"""

import asyncio
import json
import os

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(tags=["chat"])

DEFAULT_MODEL = os.getenv("COPILOT_MODEL", "gpt-4.1")


class ChatRequest(BaseModel):
    """チャットリクエスト"""

    prompt: str
    model: str = DEFAULT_MODEL


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """ストリーミングチャット。SSE でトークンごとに配信。"""
    from ghcp_sdk_demo.app import get_client

    client = get_client()

    async def event_stream():
        session = await client.create_session(
            {"model": request.model, "streaming": True}
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
        await session.send({"prompt": request.prompt})

        # キューからチャンクを読み出してクライアントへ送信
        while not done.is_set() or not chunks.empty():
            try:
                chunk = await asyncio.wait_for(chunks.get(), timeout=0.1)
                yield chunk
            except asyncio.TimeoutError:
                continue

        # 残りのチャンクをフラッシュ
        while not chunks.empty():
            yield chunks.get_nowait()

        await session.destroy()

    return StreamingResponse(event_stream(), media_type="text/event-stream")
