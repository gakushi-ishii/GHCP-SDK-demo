# アーキテクチャ

## 概要

このアプリは **FastAPI** + **GitHub Copilot SDK** のシンプルな Web デモです。

```
ブラウザ (HTML/CSS/JS)
    ↕ SSE / HTTP POST
FastAPI サーバー (app.py)
    ↕ JSON-RPC
Copilot CLI (バックグラウンドプロセス)
    ↕ HTTPS
GitHub Copilot API
```

## コンポーネント

### CopilotClient ライフサイクル

`app.py` の `lifespan` コンテキストマネージャが `CopilotClient` の起動・停止を管理します。
アプリ起動時に `await client.start()` で Copilot CLI プロセスを起動し、終了時に `await client.stop()` で停止します。

### デモ API ルーター

各デモは FastAPI の `APIRouter` として独立しています:

- `demos/chat.py` — ストリーミングチャット（`/api/chat`）
- `demos/codegen.py` — コード生成（`/api/codegen`）
- `demos/tools.py` — カスタムツール（`/api/tools`）

### SSE ストリーミング

SDK の `session.on(callback)` でイベントを受信し、`StreamingResponse` で SSE 形式でクライアントに配信します。

イベントの流れ:
1. `session.send({"prompt": "..."})` でプロンプトを送信
2. `assistant.message_delta` イベントでトークンを順次受信
3. `session.idle` イベントで完了を検知
4. `session.destroy()` でセッションを破棄

### カスタムツール

`@define_tool` デコレータで Python 関数をツールとして定義し、`create_session(tools=[...])` で登録します。
LLM が必要に応じてツールを自動的に呼び出し、結果をコンテキストに組み込みます。
