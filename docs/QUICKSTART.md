# クイックスタートガイド

このガイドでは、GitHub Copilot SDKデモアプリケーションの使い方を説明します。

## インストール

```bash
# 1. リポジトリをクローン
git clone https://github.com/gakushi-ishii/GHCP-SDK-demo.git
cd GHCP-SDK-demo

# 2. 仮想環境を作成（推奨）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. 依存関係をインストール
pip install -r requirements.txt
```

## 実行方法

### メインデモアプリ（推奨）

対話型メニューから各デモを選択できます：

```bash
python -m ghcp_sdk_demo
```

### 個別のデモを実行

各デモは単独でも実行できます：

```bash
# チャットデモ
python -m ghcp_sdk_demo.demos.chat_demo

# コード生成デモ
python -m ghcp_sdk_demo.demos.code_generation_demo

# コンテキスト認識デモ
python -m ghcp_sdk_demo.demos.context_aware_demo
```

## デモの使い方

### 1. 💬 チャットデモ

対話型のチャットインターフェースで、GitHub Copilot SDKとの会話を体験できます。

**操作方法:**
- プロンプトに質問やリクエストを入力
- `exit` と入力すると終了
- 会話履歴が保持され、コンテキストを理解した応答が得られます

**例:**
```
あなた: TypeScriptでAPI呼び出しを実装する方法を教えて
Copilot: [TypeScriptでのAPI実装についての説明...]

あなた: エラーハンドリングも含めて
Copilot: [エラーハンドリングを含めた詳細な説明...]
```

### 2. 🔨 コード生成デモ

自然言語の説明から、実際に動作するコードを生成します。

**操作方法:**
1. サンプル例から選択、または自分で説明を入力
2. プログラミング言語を選択
3. 生成されたコードを確認

**サンプル例:**
- フィボナッチ数列を計算する関数 (Python)
- JSONファイルを読み込んでパースする関数 (Python)
- REST APIのGETリクエストを送信する関数 (Python)

### 3. 🧠 コンテキスト認識デモ

プロジェクトの構造やコーディングスタイルを理解し、最適な提案を行います。

**操作方法:**
1. シナリオを選択
2. コンテキスト分析結果を確認
3. 提案された改善点をレビュー

**シナリオ:**
- Pythonプロジェクトの分析
- RESTful API実装の提案
- テストコードの生成

## よくある質問

### Q: 実際のGitHub Copilot APIと連携できますか？

A: 現在のバージョンはモックデモですが、`.env`ファイルにGitHubトークンを設定することで、実際のAPIとの統合が可能です（今後実装予定）。

### Q: 他のプログラミング言語にも対応していますか？

A: コード生成デモでは、Python、TypeScript、JavaScript、Java、Go、Rustなど、主要な言語をサポートしています。

### Q: カスタムデモを追加できますか？

A: はい！`ghcp_sdk_demo/demos/`ディレクトリに新しいデモファイルを追加し、`ghcp_sdk_demo/app.py`のメニューに登録することで、カスタムデモを作成できます。

## トラブルシューティング

### エラー: "ModuleNotFoundError"

依存関係が正しくインストールされていない可能性があります：

```bash
pip install -r requirements.txt
```

### エラー: 仮想環境が有効化されていない

```bash
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### Pythonのバージョンが古い

Python 3.12以上が必要です：

```bash
python --version
```

## 次のステップ

- 各デモのソースコードを確認してカスタマイズ
- 実際のGitHub Copilot SDK APIとの統合
- Webインターフェースの追加
- カスタムエージェントの実装

## 参考資料

- [GitHub Copilot 公式ドキュメント](https://github.com/features/copilot)
- [Model Context Protocol](https://github.com/modelcontextprotocol/sdk)
- [Python 公式サイト](https://www.python.org/)
- [InquirerPy ドキュメント](https://inquirerpy.readthedocs.io/)
- [Rich ドキュメント](https://rich.readthedocs.io/)
