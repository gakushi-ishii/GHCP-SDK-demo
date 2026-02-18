"""エントリーポイント: python -m ghcp_sdk_demo で Web サーバーを起動"""

import uvicorn


def main() -> None:
    """uvicorn で FastAPI アプリを起動"""
    uvicorn.run(
        "ghcp_sdk_demo.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
