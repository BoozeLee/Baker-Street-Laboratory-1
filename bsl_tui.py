#!/usr/bin/env python3
"""bsl_tui.py – Textual based TUI for Baker Street Laboratory
Provides a simple menu driven interface (arrow keys / Enter) to invoke the existing bsl
commands without relying on the parllama backend.
"""
import subprocess, sys
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, ListView, ListItem, Label
from textual.containers import Vertical

class MenuItem(ListItem):
    def __init__(self, label: str, command: list[str]):
        super().__init__(Label(label))
        self.command = command

class BSLTUI(App):
    CSS_PATH = "bsl_tui.css"
    BINDINGS = [("q", "quit", "Quit"), ("r", "refresh", "Refresh UI")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        menu = ListView(
            MenuItem("🚀 Start all services", ["bsl", "start"]),
            MenuItem("📊 Show status", ["bsl", "status"]),
            MenuItem("🌐 Open UI in browser", ["bsl", "open"]),
            MenuItem("🔍 Research query", ["bsl", "research"]),
            MenuItem("🛑 Stop all services", ["bsl", "stop"]),
        )
        yield Vertical(menu, id="menu")
        yield Input(placeholder="Enter research query and press Enter", id="search_input", classes="hidden")
        yield Static("", id="output", classes="hidden")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # When a menu item is selected (Enter), run its command
        item: MenuItem = event.item
        if item.command[1] == "research":
            # Show input box for query
            self.query_one("#search_input").remove_class("hidden")
            self.query_one("#search_input").focus()
        else:
            self.run_command(item.command)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if query:
            self.run_command(["bsl", "research", query])
        self.query_one("#search_input").add_class("hidden")
        self.query_one("#search_input").value = ""

    def run_command(self, cmd: list[str]):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/home/kilisan/Projects/baker-street-webapp",
                check=False,
            )
            output = result.stdout or result.stderr
        except Exception as e:
            output = f"Error running {' '.join(cmd)}: {e}"
        out_widget = self.query_one("#output")
        out_widget.update(output)
        out_widget.remove_class("hidden")
        # Auto‑hide after a few seconds – use a timer
        self.set_timer(5, lambda: out_widget.add_class("hidden"))

    def action_quit(self) -> None:
        self.exit()

    def action_refresh(self) -> None:
        self.refresh()

if __name__ == "__main__":
    BSLTUI().run()
