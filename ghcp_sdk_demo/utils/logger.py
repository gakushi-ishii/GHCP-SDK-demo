"""
ロガーユーティリティ

デモアプリでの出力を見やすくするためのヘルパー。
rich ライブラリを使用してカラフルなコンソール出力を提供する。
"""

from rich.console import Console
from rich.text import Text
from rich.syntax import Syntax

console = Console()


class Logger:
    """コンソール出力をリッチにフォーマットするユーティリティクラス"""

    @staticmethod
    def info(message: str) -> None:
        """情報メッセージ（青）"""
        console.print(f"[blue]ℹ[/blue] {message}")

    @staticmethod
    def success(message: str) -> None:
        """成功メッセージ（緑）"""
        console.print(f"[green]✓[/green] {message}")

    @staticmethod
    def error(message: str) -> None:
        """エラーメッセージ（赤）"""
        console.print(f"[red]✗[/red] {message}")

    @staticmethod
    def warning(message: str) -> None:
        """警告メッセージ（黄）"""
        console.print(f"[yellow]⚠[/yellow] {message}")

    @staticmethod
    def header(message: str) -> None:
        """セクションヘッダー"""
        separator = "═" * 60
        console.print()
        console.print(f"[bold cyan]{separator}[/bold cyan]")
        console.print(f"[bold cyan]{message}[/bold cyan]")
        console.print(f"[bold cyan]{separator}[/bold cyan]")
        console.print()

    @staticmethod
    def section(message: str) -> None:
        """サブセクション"""
        separator = "─" * 60
        console.print()
        console.print(f"[bold white]{message}[/bold white]")
        console.print(f"[dim]{separator}[/dim]")

    @staticmethod
    def code(code: str, language: str = "") -> None:
        """コードブロック表示（シンタックスハイライト付き）"""
        console.print()
        if language:
            syntax = Syntax(code, language, theme="monokai", line_numbers=False)
            console.print(syntax)
        else:
            console.print(f"[dim]```{language}[/dim]")
            console.print(code)
            console.print("[dim]```[/dim]")
        console.print()

    @staticmethod
    def result(label: str, value: str) -> None:
        """キーバリューの表示"""
        console.print(f"[cyan]{label}:[/cyan] [white]{value}[/white]")
