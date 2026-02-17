# GitHub Copilot SDK デモアプリケーション

GitHub Copilot SDKの主要機能を実演するインタラクティブなデモアプリケーションです。

## 🎯 このデモについて

このデモアプリケーションは、GitHub Copilot SDKの**新規性と独自性**を分かりやすく示すために作成されました。以下の3つの主要機能を体験できます：

### 1. 💬 対話型チャット
- 自然な会話を通じた開発支援
- コンテキストを保持した連続的な対話
- ストリーミングレスポンス（実装予定）

### 2. 🔨 コード生成
- 自然言語の説明から高品質なコードを生成
- 複数のプログラミング言語に対応（TypeScript, Python, JavaScript等）
- ベストプラクティスに準拠したコード出力

### 3. 🧠 コンテキスト認識
- プロジェクト構造を理解した提案
- 既存のコーディングスタイルへの適応
- 依存関係や関連ファイルを考慮した最適な提案

## 🚀 セットアップ

### 前提条件
- Node.js 18以上
- npm または yarn

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/gakushi-ishii/GHCP-SDK-demo.git
cd GHCP-SDK-demo

# 依存関係をインストール
npm install

# 環境変数を設定（必要に応じて）
cp .env.example .env
# .envファイルを編集してGitHub APIトークンを設定
```

## 📖 使い方

### メインデモアプリを起動

```bash
npm run dev
```

対話型メニューから各デモを選択できます。

### 個別のデモを実行

各デモは個別に実行することもできます：

```bash
# チャットデモ
npm run demo:chat

# コード生成デモ
npm run demo:code-gen

# コンテキスト認識デモ
npm run demo:context
```

## 🏗️ プロジェクト構造

```
GHCP-SDK-demo/
├── src/
│   ├── index.ts                    # メインエントリーポイント
│   ├── demos/
│   │   ├── chat-demo.ts           # チャットデモ
│   │   ├── code-generation-demo.ts # コード生成デモ
│   │   └── context-aware-demo.ts   # コンテキスト認識デモ
│   └── utils/
│       └── logger.ts               # ロギングユーティリティ
├── package.json
├── tsconfig.json
└── README.md
```

## ✨ GitHub Copilot SDKの特徴

このデモでは、以下のGitHub Copilot SDKの独自機能を体験できます：

### 🎨 高度なコンテキスト理解
- プロジェクトの構造、依存関係、コーディングスタイルを自動認識
- 既存のコードベースに調和した提案を生成

### 🔄 リアルタイムインタラクション
- ストリーミングレスポンスによる即時フィードバック
- 対話を通じた段階的な改善

### 🛠️ 開発者ファーストな設計
- シンプルで直感的なAPI
- TypeScriptファーストの型安全性
- 拡張可能なアーキテクチャ

## 🔜 今後の拡張予定

現在のデモは基本的な土台です。以下の機能を追加することで、さらに充実したデモになります：

- [ ] 実際のGitHub Copilot SDK APIとの統合
- [ ] ストリーミングレスポンスの実装
- [ ] より複雑なコード生成シナリオ
- [ ] カスタムエージェントの実装例
- [ ] Webベースのデモインターフェース
- [ ] リアルタイムコードレビュー機能
- [ ] マルチファイル編集のデモ

## 🤝 貢献

フィードバックや改善提案は大歓迎です！Issueやプルリクエストをお気軽にお送りください。

## 📝 ライセンス

ISC

## 🔗 関連リンク

- [GitHub Copilot](https://github.com/features/copilot)
- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/sdk)
