import random
import string
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from rich.layout import Layout
from rich.align import Align

class MainMenu:
    def __init__(self, search_engine, api_client):
        self.console = Console()
        self.search_engine = search_engine
        self.api_client = api_client

    def show_banner(self):
        banner = """
[bold red]
    ▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀     ██████  █    ██  ███▄    █ 
    ▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒    ▒██    ▒  ██  ▓██▒ ██ ▀█   █ 
    ░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░    ░ ▓██▄   ▓██  ▒██░▓██  ▀█ ██▒
    ░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄      ▒   ██▒▓▓█  ░██░▓██▒  ▐▌██▒
    ░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄   ▒██████▒▒▒▒█████▓ ▒██░   ▓██░
     ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒   ▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ 
     ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░   ░ ░▒  ░ ░░░▒░ ░ ░ ░ ░░   ░ ▒░
     ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░    ░  ░  ░   ░░░ ░ ░    ░   ░ ░ 
       ░          ░  ░   ░     ░  ░              ░     ░              ░ 
[/bold red]
[bold yellow][ Database Search & OSINT Tool code:@AL3XEY_PAN1CHKA base:@Revichs][/bold yellow]
"""
        layout = Layout()
        layout.split_column(
            Layout(Align.center(Panel(banner, border_style="red")))
        )
        self.console.print(layout)

    def get_user_input(self, prompt_text, choices=None):
        """Упрощённая и более надёжная версия получения пользовательского ввода"""
        while True:
            try:
                # Отображаем prompt с доступными вариантами
                if choices:
                    self.console.print(Panel(
                        f"[cyan]{prompt_text}[/cyan]\n[dim]Доступные варианты: {', '.join(choices)}[/dim]",
                        border_style="cyan"
                    ))
                else:
                    self.console.print(Panel(f"[cyan]{prompt_text}[/cyan]", border_style="cyan"))

                # Простое использование input() без сложной логики
                user_input = input().strip()

                # Проверка на пустой ввод
                if not user_input:
                    self.console.print("[yellow]Пустой ввод. Попробуйте еще раз.[/yellow]")
                    continue

                # Если есть список допустимых вариантов, проверяем ввод
                if choices and user_input not in choices:
                    self.console.print(f"[yellow]Пожалуйста, выберите один из вариантов: {', '.join(choices)}[/yellow]")
                    continue

                return user_input

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Прервано пользователем[/yellow]")
                return None
            except Exception as e:
                self.console.print(f"[red]Ошибка при чтении ввода: {str(e)}[/red]")
                return None

    def show_hall_of_fame(self):
        heart_ascii = """
           <3   <3
         <3    <3    <3
        <3      <3      <3
        <3             <3
         <3           <3
           <3       <3
             <3   <3
               <3
        """

        developers = [
            "[bold red]Алексей[/bold red] [cyan]паничка-кодер[/cyan]",
            "[bold blue]@Revichs[/bold blue] [cyan]датабаза и помощь[/cyan]"
        ]

        developers_panel = Panel(
            "\n".join([
                Align.center(heart_ascii),
                "\n[bold yellow]Разработчики:[/bold yellow]\n",
                "\n".join(f"• {dev}" for dev in developers)
            ]),
            title="[bold red]♥ Зал Славы ♥[/bold red]",
            border_style="red"
        )

        self.console.print("\n")
        self.console.print(developers_panel)
        self.console.print("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
        input()

    def show(self):
        while True:
            self.show_banner()
            menu_items = [
                "[1] 📱 [bold cyan]Search by Phone Number[/bold cyan] (формат: 79991234567)",
                "[2] 💬 [bold cyan]Search by Telegram Username[/bold cyan] (формат: @username)",
                "[3] 📄 [bold cyan]Search by Passport[/bold cyan] (формат: 1234 567890)",
                "[4] 🔢 [bold cyan]Search by SNILS[/bold cyan] (формат: 12345678901)",
                "[5] 🔑 [bold cyan]Password Generator[/bold cyan]",
                "[6] 🌐 [bold cyan]Search via LeakOSINT API[/bold cyan]",
                "[7] ⭐ [bold cyan]Hall of Fame[/bold cyan]",
                "[8] 🚪 [bold red]Exit[/bold red]"
            ]

            menu_table = Table(show_header=False, border_style="red", width=80)
            menu_table.add_column("Option", style="bold white", justify="left")

            for item in menu_items:
                menu_table.add_row(item)

            self.console.print(Panel(
                Align.center(menu_table),
                title="[bold red]Menu Options[/bold red]",
                border_style="red"
            ))

            choice = self.get_user_input("\n[bold]Выберите опцию[/bold]", ["1", "2", "3", "4", "5", "6", "7", "8"])
            if not choice:
                self.console.print(Panel("[yellow]Выход из программы[/yellow]", border_style="yellow"))
                break

            if choice == "1":
                self.search_by_phone()
            elif choice == "2":
                self.search_by_telegram()
            elif choice == "3":
                self.search_by_passport()
            elif choice == "4":
                self.search_by_snils()
            elif choice == "5":
                self.generate_password()
            elif choice == "6":
                self.search_via_api()
            elif choice == "7":
                self.show_hall_of_fame()
            elif choice == "8":
                self.console.print(Panel("[yellow]Программа завершена[/yellow]", border_style="yellow"))
                break

    def perform_search(self, search_function, query, search_type):
        with Progress(
            "[progress.description]{task.description}",
            SpinnerColumn(),
            BarColumn(complete_style="red", finished_style="green"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task(
                f"[bold red]🔍 Поиск {search_type}...[/bold red]",
                total=100
            )

            # Имитация прогресса поиска с более плавной анимацией
            for i in range(100):
                time.sleep(0.02)  # Увеличенная задержка для более заметной анимации
                progress.update(task, advance=1)

            results = search_function(query)
            return results

    def display_results(self, results):
        if not results:
            self.console.print(Panel(
                "[yellow]🔍 Результаты не найдены[/yellow]",
                title="[bold red]Поиск[/bold red]",
                border_style="red"
            ))
            return

        table = Table(
            show_header=True,
            header_style="bold red",
            border_style="red",
            title="[bold red]Результаты поиска[/bold red]"
        )
        table.add_column("📁 Источник", style="cyan", justify="left")
        table.add_column("📝 Данные", style="green", justify="left")

        for result in results:
            table.add_row(result["source"], result["data"])

        self.console.print(Panel(table, border_style="red"))

    def search_by_phone(self):
        self.console.print("\n[bold cyan]Поиск по номеру телефона[/bold cyan]")
        self.console.print("[dim]Формат: 79991234567 (11 цифр, без пробелов и символов)[/dim]")
        query = self.get_user_input("Введите номер телефона")
        if query:
            results = self.perform_search(
                lambda q: self.search_engine.search_files(q, "phone"),
                query,
                "телефона"
            )
            self.display_results(results)

    def search_by_telegram(self):
        self.console.print("\n[bold cyan]Поиск по Telegram[/bold cyan]")
        self.console.print("[dim]Формат: @username или username (без @)[/dim]")
        query = self.get_user_input("Введите username")
        if query:
            if not query.startswith("@"):
                query = "@" + query
            results = self.perform_search(
                lambda q: self.search_engine.search_files(q, "telegram"),
                query,
                "Telegram username"
            )
            self.display_results(results)

    def search_by_passport(self):
        self.console.print("\n[bold cyan]Поиск по паспорту[/bold cyan]")
        self.console.print("[dim]Формат: 1234 567890 (серия и номер, можно с пробелом или без)[/dim]")
        query = self.get_user_input("Введите номер паспорта")
        if query:
            results = self.perform_search(
                lambda q: self.search_engine.search_files(q, "passport"),
                query,
                "паспорта"
            )
            self.display_results(results)

    def search_by_snils(self):
        self.console.print("\n[bold cyan]Поиск по СНИЛС[/bold cyan]")
        self.console.print("[dim]Формат: 12345678901 (11 цифр без пробелов и тире)[/dim]")
        query = self.get_user_input("Введите номер СНИЛС")
        if query:
            results = self.perform_search(
                lambda q: self.search_engine.search_files(q, "snils"),
                query,
                "СНИЛС"
            )
            self.display_results(results)

    def generate_password(self):
        self.console.print("\n[bold cyan]Генератор паролей[/bold cyan]")
        length_input = self.get_user_input("[dim]Введите длину пароля (по умолчанию 12)[/dim]")
        length = 12
        try:
            if length_input:
                length = int(length_input)
        except ValueError:
            self.console.print("[yellow]Используется длина по умолчанию: 12[/yellow]")

        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        self.console.print(Panel(f"[green]{password}[/green]", title="[bold cyan]Сгенерированный пароль[/bold cyan]", border_style="cyan"))

    def search_via_api(self):
        if not self.api_client.api_key:
            self.console.print(Panel("[red]API ключ не настроен![/red]", title="[bold red]Ошибка[/bold red]", border_style="red"))
            return

        self.console.print("\n[bold cyan]Поиск через LeakOSINT API[/bold cyan]")
        query_type = self.get_user_input(
            "Выберите тип поиска",
            choices=["email", "phone", "username"]
        )
        if not query_type:
            return

        examples = {
            "email": "example@mail.com",
            "phone": "79991234567",
            "username": "@username"
        }

        self.console.print(f"[dim]Пример формата: {examples[query_type]}[/dim]")
        query = self.get_user_input("Введите запрос")
        if not query:
            return

        try:
            results = self.perform_search(
                lambda q: self.api_client.search(query_type, q),
                query,
                f"через API ({query_type})"
            )
            self.display_results([{"source": "LeakOSINT API", "data": str(result)} for result in results])
        except Exception as e:
            self.console.print(Panel(f"[red]Ошибка API: {str(e)}[/red]", title="[bold red]Ошибка[/bold red]", border_style="red"))