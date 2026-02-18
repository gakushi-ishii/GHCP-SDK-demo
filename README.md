# GitHub Copilot SDK デモアプリケーション

[github-copilot-sdk](https://github.com/github/copilot-sdk) の主要機能を Web ブラウザ上でデモする FastAPI アプリケーションです。

## 🎯 デモ内容

| デモ | 説明 | SDK 機能 |
|------|------|----------|
| 💬 チャット | ストリーミングチャット | `create_session(streaming=True)` + SSE |
| 🔨 コード生成 | 自然言語からコード生成 | `system_message` によるタスク特化 |
| 🛠️ カスタムツール | LLM がツールを自動呼び出し | `@define_tool` + Function Calling |

## 🚀 セットアップ

### 前提条件

- GitHub Copilot のアクセス権を持つ GitHub アカウント
- Dev Container 対応の VS Code（推奨）

### 1. Dev Container で開く

このリポジトリを VS Code の **Dev Containers** で開きます。自動的に以下がインストールされます:

- Python 3.12
- Node.js
- GitHub CLI
- Copilot CLI (`@github/copilot`)
- Python 依存パッケージ

### 2. 認証

```bash
# Copilot CLI にログイン
copilot auth login

# または環境変数で設定
cp .env.example .env
# .env を編集して GITHUB_TOKEN を設定
```

### 3. サーバー起動

```bash
python -m ghcp_sdk_demo
```

ブラウザで http://localhost:8000 を開きます。

## 📁 プロジェクト構造

```
ghcp_sdk_demo/
├── __init__.py          # パッケージ
├── __main__.py          # uvicorn 起動
├── app.py               # FastAPI アプリ + CopilotClient ライフサイクル
├── demos/
│   ├── chat.py          # チャットデモ（SSE ストリーミング）
│   ├── codegen.py       # コード生成デモ
│   └── tools.py         # カスタムツールデモ（@define_tool）
└── static/
    ├── index.html       # メインページ
    ├── style.css        # スタイル
    └── app.js           # フロントエンド（SSE 受信）
```

## 🔧 技術スタック

- **バックエンド**: FastAPI + uvicorn
- **AI**: GitHub Copilot SDK (`github-copilot-sdk`)
- **フロントエンド**: バニラ HTML/CSS/JS（外部フレームワーク不使用）
- **通信**: Server-Sent Events (SSE) によるストリーミング

## 📝 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `GITHUB_TOKEN` | GitHub 認証トークン | Copilot CLI のログインユーザー |
| `COPILOT_MODEL` | デフォルトモデル | `gpt-4.1` |

## ライセンス

ISC
