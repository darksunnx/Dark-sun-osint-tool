#!/usr/bin/env python3
import os
import sys
import traceback
from rich.console import Console
from rich.traceback import install
from menu import MainMenu
from config import Config
from search_engine import SearchEngine
from api_client import LeakOSINTClient

# Установка rich для красивого отображения ошибок
install(show_locals=True)

def is_interactive_terminal():
    """Проверка доступности интерактивного терминала"""
    # В Windows всегда используем интерактивный режим
    if sys.platform.startswith('win'):
        return True

    # Проверяем, что stdin подключен к терминалу
    try:
        return sys.stdin.isatty()
    except:
        return False

def main():
    console = Console()
    try:
        # Проверяем возможность интерактивного режима
        if not is_interactive_terminal():
            console.print("[yellow]Внимание: Программа требует интерактивного терминала[/yellow]")
            console.print("[yellow]Пожалуйста, запустите программу в обычном терминале[/yellow]")
            return

        # Create database directory if it doesn't exist
        if not os.path.exists("database"):
            os.makedirs("database")
            console.print("[yellow]Created database directory[/yellow]")

        # Initialize configuration
        config = Config()
        if not config.check_config():
            console.print("[yellow]Configuration file not found. Creating new one...[/yellow]")
            if not config.create_config():
                console.print("[red]Failed to create configuration[/red]")
                return

        # Initialize search engine
        search_engine = SearchEngine()

        # Initialize API client
        api_client = LeakOSINTClient(config.get_api_key())

        # Start main menu
        menu = MainMenu(search_engine, api_client)
        menu.show()

    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print("[red]Error occurred during startup:[/red]")
        console.print(f"[red]{str(e)}[/red]")
        console.print("[red]Detailed error information:[/red]")
        console.print_exception()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]Program terminated by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print("\n[red]Unexpected error occurred:[/red]")
        console.print_exception()
        console.print("\n[yellow]Press Enter to exit...[/yellow]")
        input()
        sys.exit(1)