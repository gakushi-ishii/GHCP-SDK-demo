"""GitHub Copilot SDK デモ Web アプリケーション

FastAPI ベースの Web アプリケーション。
GitHub Copilot SDK の主要機能をブラウザ上でデモします。
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from copilot import CopilotClient

from ghcp_sdk_demo.demos.chat import router as chat_router
from ghcp_sdk_demo.demos.codegen import router as codegen_router
from ghcp_sdk_demo.demos.tools import router as tools_router

load_dotenv()

# グローバル CopilotClient（アプリ起動時に初期化）
copilot_client: CopilotClient | None = None


def get_client() -> CopilotClient:
    """CopilotClient のシングルトンを取得"""
    if copilot_client is None:
        raise RuntimeError("CopilotClient が初期化されていません")
    return copilot_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """アプリのライフサイクル管理: CopilotClient の起動・停止"""
    global copilot_client

    # GITHUB_TOKEN は環境変数から SDK が自動検出する
    copilot_client = CopilotClient()
    await copilot_client.start()
    print("✅ Copilot SDK クライアント起動完了")

    yield

    await copilot_client.stop()
    print("🛑 Copilot SDK クライアント停止")


app = FastAPI(
    title="GitHub Copilot SDK Demo",
    description="GitHub Copilot SDK の機能をデモする Web アプリケーション",
    version="2.0.0",
    lifespan=lifespan,
)

# API routers
app.include_router(chat_router, prefix="/api")
app.include_router(codegen_router, prefix="/api")
app.include_router(tools_router, prefix="/api")

# 静的ファイル配信
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def index() -> FileResponse:
    """メインページを配信"""
    return FileResponse(str(static_dir / "index.html"))
