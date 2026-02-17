"""
コンテキスト認識デモ

GitHub Copilot SDKがコードベースのコンテキストを理解し、
それに基づいた提案を行う機能を示すデモ。

主な特徴:
- ファイルコンテキストの理解
- プロジェクト構造の認識
- 関連コードの提案
- リファクタリング提案
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from ghcp_sdk_demo.utils.logger import Logger
from ghcp_sdk_demo.utils.prompts import select_prompt


@dataclass
class ContextAnalysis:
    """コンテキスト分析結果"""

    file_type: str
    code_style: str
    dependencies: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


class ContextAwareDemo:
    """プロジェクトのコンテキストを理解するデモ"""

    SCENARIOS = [
        {
            "name": "シナリオ1: Pythonプロジェクトの分析",
            "value": "python-project",
        },
        {
            "name": "シナリオ2: RESTful API実装の提案",
            "value": "api-implementation",
        },
        {
            "name": "シナリオ3: テストコードの生成",
            "value": "test-generation",
        },
    ]

    async def run(self) -> None:
        Logger.header("GitHub Copilot SDK - コンテキスト認識デモ")

        Logger.info(
            "このデモでは、Copilot SDKがプロジェクトのコンテキストを理解する機能を示します。\n"
        )

        scenario: str = await select_prompt(
            message="デモシナリオを選択してください:",
            choices=self.SCENARIOS,
        )

        Logger.section("コンテキストを分析中...")
        analysis = await self._analyze_context(scenario)

        self._display_analysis(analysis)
        self._show_recommendations(scenario)

    async def _analyze_context(self, scenario: str) -> ContextAnalysis:
        """コンテキストを分析する（将来的にはSDK APIを呼び出す）"""
        # シミュレーション用の遅延
        await asyncio.sleep(1.2)

        # TODO: ここでGitHub Copilot SDK APIを使用してコンテキストを分析
        return self._get_mock_analysis(scenario)

    def _get_mock_analysis(self, scenario: str) -> ContextAnalysis:
        """モックの分析結果を返す"""
        analyses: dict[str, ContextAnalysis] = {
            "python-project": ContextAnalysis(
                file_type="Python Project",
                code_style="Type Hints, PEP 8, Black formatter",
                dependencies=["rich", "InquirerPy", "python-dotenv"],
                suggestions=[
                    "pyproject.tomlの設定は適切です",
                    "型ヒントが一貫して使用されています",
                    "PEP 8に準拠したコーディングスタイルです",
                    "mypyによる静的型チェックが有効です",
                ],
            ),
            "api-implementation": ContextAnalysis(
                file_type="REST API Implementation",
                code_style="FastAPI + Python",
                dependencies=["fastapi", "uvicorn", "pydantic"],
                suggestions=[
                    "ミドルウェアでエラーハンドリングを追加することを推奨",
                    "APIバージョニングの実装を検討してください",
                    "レート制限の追加をお勧めします",
                    "OpenAPI/Swaggerドキュメントの生成を検討",
                ],
            ),
            "test-generation": ContextAnalysis(
                file_type="Unit Test",
                code_style="pytest + Python",
                dependencies=["pytest", "pytest-cov", "pytest-asyncio"],
                suggestions=[
                    "カバレッジ80%以上を目標に追加テストを推奨",
                    "エッジケースのテストを追加してください",
                    "fixtureの使用が適切です",
                    "テストの命名規則が一貫しています",
                ],
            ),
        }

        return analyses.get(
            scenario,
            ContextAnalysis(
                file_type="Unknown",
                code_style="Standard",
                suggestions=["コンテキストを分析中..."],
            ),
        )

    def _display_analysis(self, analysis: ContextAnalysis) -> None:
        """分析結果を表示する"""
        Logger.success("コンテキスト分析が完了しました！\n")

        Logger.result("ファイルタイプ", analysis.file_type)
        Logger.result("コードスタイル", analysis.code_style)

        if analysis.dependencies:
            Logger.section("検出された依存関係")
            for dep in analysis.dependencies:
                print(f"  • {dep}")

        Logger.section("提案")
        for i, suggestion in enumerate(analysis.suggestions, 1):
            print(f"  {i}. {suggestion}")
        print()

    def _show_recommendations(self, scenario: str) -> None:
        """GitHub Copilot SDKのコンテキスト認識機能について表示する"""
        Logger.section("GitHub Copilot SDKのコンテキスト認識機能")

        print("Copilot SDKは以下の情報を活用します：\n")
        print("📁 プロジェクト構造")
        print("   • ディレクトリレイアウト")
        print("   • ファイル命名規則")
        print("   • モジュール構成\n")

        print("📦 依存関係")
        print("   • pyproject.toml / requirements.txt")
        print("   • import文")
        print("   • 使用ライブラリ\n")

        print("💻 コードスタイル")
        print("   • 既存のコーディング規約")
        print("   • フォーマット設定")
        print("   • 命名パターン\n")

        print("🔗 関連ファイル")
        print("   • 同じディレクトリ内のファイル")
        print("   • インポートされているモジュール")
        print("   • テストファイルと実装ファイルの対応\n")

        Logger.info("これにより、プロジェクトに最適化された提案が可能になります！")


def main() -> None:
    """コンテキスト認識デモをスタンドアロンで実行する"""
    demo = ContextAwareDemo()
    try:
        asyncio.run(demo.run())
    except (KeyboardInterrupt, EOFError):
        Logger.info("\nデモを終了しました。")


if __name__ == "__main__":
    main()
