# アーキテクチャガイド

このドキュメントでは、GitHub Copilot SDKデモアプリケーションのアーキテクチャと拡張方法について説明します。

## 全体構成

```
GHCP-SDK-demo/
├── ghcp_sdk_demo/                     # メインパッケージ
│   ├── __init__.py                    # パッケージ初期化
│   ├── __main__.py                    # python -m エントリーポイント
│   ├── app.py                         # メインアプリケーション
│   ├── demos/                         # 各デモの実装
│   │   ├── __init__.py
│   │   ├── chat_demo.py
│   │   ├── code_generation_demo.py
│   │   └── context_aware_demo.py
│   └── utils/                         # ユーティリティ
│       ├── __init__.py
│       └── logger.py                  # ロギング機能
├── docs/                              # ドキュメント
├── requirements.txt                   # pip 依存関係
└── pyproject.toml                     # プロジェクト設定
```

## コアコンポーネント

### 1. DemoApp (app.py)

メインアプリケーションクラス。対話型メニューを提供し、各デモを起動します。

**主な機能:**
- 起動時のウェルカムメッセージ表示
- デモ選択メニューの提供
- 各デモの実行管理
- ループ処理による連続実行サポート

**拡張方法:**
```python
from ghcp_sdk_demo.demos.your_new_demo import YourNewDemo

# メニューに追加
choices = [
    {"name": "🆕 新しいデモ", "value": "new-demo"},
    # ...
]

# match文に追加
match demo_type:
    case "new-demo":
        demo = YourNewDemo()
        await demo.run()
```

### 2. Logger (utils/logger.py)

`rich` ライブラリを使用して、コンソール出力を視覚的に分かりやすくするユーティリティクラス。

**提供するメソッド:**
- `info()` - 情報メッセージ（青）
- `success()` - 成功メッセージ（緑）
- `error()` - エラーメッセージ（赤）
- `warning()` - 警告メッセージ（黄）
- `header()` - セクションヘッダー
- `section()` - サブセクション
- `code()` - コードブロック表示（シンタックスハイライト付き）
- `result()` - キーバリューの表示

### 3. デモクラス

各デモは以下の構造に従います：

```python
from ghcp_sdk_demo.utils.logger import Logger
from InquirerPy import inquirer


class YourDemo:
    async def run(self) -> None:
        # 1. ヘッダー表示
        Logger.header("デモタイトル")

        # 2. 説明
        Logger.info("このデモの説明...")

        # 3. ユーザー入力
        answer = inquirer.select(
            message="選択してください:",
            choices=[...],
        ).execute()

        # 4. 処理実行
        result = await self._process_demo(answer)

        # 5. 結果表示
        self._display_results(result)
```

## デザインパターン

### Single Responsibility Principle (単一責任の原則)

各クラスは明確に定義された単一の責任を持ちます：
- `DemoApp`: アプリケーションの起動とナビゲーション
- 各デモクラス: 特定のデモ機能の実装
- `Logger`: コンソール出力の整形

### asyncio による非同期処理

すべてのデモクラスは `async/await` パターンを使用し、
将来の非同期API呼び出しに対応できる設計になっています。

```python
import asyncio


class ChatDemo:
    async def run(self) -> None:
        response = await self._get_response(message)
        # ...
```

### Dependency Injection

依存関係は明示的に注入され、テスト可能性を向上させます。

```python
# 将来的な拡張例
class ChatDemo:
    def __init__(self, api_client: CopilotApiClient | None = None) -> None:
        self._api_client = api_client or MockApiClient()
```

### dataclass による型安全なデータモデル

```python
from dataclasses import dataclass, field


@dataclass
class ContextAnalysis:
    file_type: str
    code_style: str
    dependencies: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
```

## 新しいデモの追加方法

### ステップ1: デモクラスを作成

`ghcp_sdk_demo/demos/your_new_demo.py` を作成：

```python
from __future__ import annotations

import asyncio

from InquirerPy import inquirer

from ghcp_sdk_demo.utils.logger import Logger


class YourNewDemo:
    async def run(self) -> None:
        Logger.header("新しいデモ")
        # デモのロジックを実装


def main() -> None:
    demo = YourNewDemo()
    try:
        asyncio.run(demo.run())
    except (KeyboardInterrupt, EOFError):
        Logger.info("\nデモを終了しました。")


if __name__ == "__main__":
    main()
```

### ステップ2: メインアプリに統合

`ghcp_sdk_demo/app.py` を編集：

```python
from ghcp_sdk_demo.demos.your_new_demo import YourNewDemo

# メニューに選択肢を追加
{"name": "🆕 Your New Demo", "value": "your-new"},

# match文に追加
case "your-new":
    demo = YourNewDemo()
    await demo.run()
```

## API統合の準備

現在はモック応答を使用していますが、実際のGitHub Copilot SDK APIと統合する準備が整っています。

### 統合手順

1. **環境変数の設定**
```bash
cp .env.example .env
# .envファイルを編集してGITHUB_TOKENを設定
```

2. **APIクライアントの実装**
```python
from mcp import ClientSession


class CopilotApiClient:
    def __init__(self) -> None:
        self._session: ClientSession | None = None

    async def chat(self, message: str) -> str:
        """実際のAPI呼び出し"""
        ...

    async def generate_code(self, prompt: str) -> str:
        """コード生成API呼び出し"""
        ...
```

3. **デモクラスの更新**
```python
class ChatDemo:
    def __init__(self, api_client: CopilotApiClient | None = None) -> None:
        self._api_client = api_client or CopilotApiClient()

    async def _get_response(self, msg: str) -> str:
        # モックの代わりに実際のAPIを呼び出す
        return await self._api_client.chat(msg)
```

## テスト戦略

### 単体テスト（今後実装予定）

```python
# tests/test_logger.py
from ghcp_sdk_demo.utils.logger import Logger


def test_info_message(capsys):
    Logger.info("テストメッセージ")
    captured = capsys.readouterr()
    assert "テストメッセージ" in captured.out
```

### 統合テスト

```python
# tests/test_chat_demo.py
import pytest
from ghcp_sdk_demo.demos.chat_demo import ChatDemo


@pytest.mark.asyncio
async def test_mock_response():
    demo = ChatDemo()
    response = await demo._get_mock_response("テスト")
    assert len(response) > 0
```

## パフォーマンス最適化

### ストリーミングレスポンス

将来的にストリーミングAPIを使用する場合：

```python
from collections.abc import AsyncGenerator


async def stream_response(prompt: str) -> AsyncGenerator[str, None]:
    async for chunk in api_client.stream_chat(prompt):
        yield chunk


# 使用例
async for chunk in stream_response(user_message):
    print(chunk, end="", flush=True)
```

### キャッシング

頻繁に使用されるリクエストをキャッシュ：

```python
from functools import lru_cache
from typing import Any


class CacheManager:
    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    async def get(self, key: str, fetcher) -> Any:
        if key in self._cache:
            return self._cache[key]
        value = await fetcher()
        self._cache[key] = value
        return value
```

## ベストプラクティス

1. **エラーハンドリング**: すべての非同期処理で適切にエラーをキャッチ
2. **型安全性**: Python の型ヒントと mypy を最大限活用
3. **ログ**: 重要な操作は Logger を使用して記録
4. **モジュラリティ**: 機能を小さく再利用可能なモジュールに分割
5. **ドキュメント**: コードに docstring を追加

## 今後の拡張アイデア

- [ ] Webインターフェース（FastAPI + React）
- [ ] データベース連携（会話履歴の保存）
- [ ] マルチユーザーサポート
- [ ] プラグインシステム
- [ ] リアルタイムコラボレーション
- [ ] カスタムエージェントの作成
- [ ] メトリクス・分析ダッシュボード

## リファレンス

- [Python 公式ドキュメント](https://docs.python.org/3/)
- [InquirerPy ドキュメント](https://inquirerpy.readthedocs.io/)
- [Rich ドキュメント](https://rich.readthedocs.io/)
- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/sdk)
