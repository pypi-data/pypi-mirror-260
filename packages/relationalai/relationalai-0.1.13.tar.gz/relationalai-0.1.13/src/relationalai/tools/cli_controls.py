#pyright: reportPrivateImportUsage=false

import io
from typing import Any, List, cast
import rich
from rich.console import Console
import sys
from InquirerPy import inquirer, utils as inquirer_utils
from InquirerPy.base.control import Choice
import time
import threading
import itertools
from ..debugging import jupyter

#--------------------------------------------------
# Style
#--------------------------------------------------

STYLE = inquirer_utils.get_style({
    "fuzzy_prompt": "#e5c07b"
}, False)

#--------------------------------------------------
# Helpers
#--------------------------------------------------

def rich_str(string:str) -> str:
    output = io.StringIO()
    console = Console(file=output, force_terminal=True)
    console.print(string)
    return output.getvalue()

#--------------------------------------------------
# Dividers
#--------------------------------------------------

def divider(console=None, flush=False):
    div = "\n[dim]---------------------------------------------------\n "
    if console is None:
        rich.print(div)
    else:
        console.print(div)
    if flush:
        sys.stdout.flush()

def abort():
    rich.print()
    rich.print("[yellow]Aborted")
    divider()
    sys.exit(1)

#--------------------------------------------------
# Prompts
#--------------------------------------------------

default_bindings = cast(Any, {
    "interrupt": [
        {"key": "escape"},
        {"key": "c-c"},
        {"key": "c-d"}
    ],
    "skip": [
        {"key": "c-s"}
    ]
})

def prompt(message:str, value:str|None, newline=False) -> str:
    if value:
        return value
    try:
        result:str = inquirer.text(message, keybindings=default_bindings).execute()
    except KeyboardInterrupt:
        abort()
        raise Exception("Unreachable")
    if newline:
        rich.print("")
    return result

def select(message:str, choices:List[str|Choice], value:str|None, newline=False, **kwargs) -> str|Any:
    if value:
        return value
    try:
        result:str = inquirer.select(message, choices, keybindings=default_bindings, **kwargs).execute()
    except KeyboardInterrupt:
        abort()
        raise Exception("Unreachable")
    if newline:
        rich.print("")
    return result

def fuzzy(message:str, choices:List[str], default:str|None = None, multiselect=False, **kwargs) -> str:
    try:
        kwargs["keybindings"] = default_bindings
        if multiselect:
            kwargs["keybindings"] = {
                "toggle": [
                    {"key": "tab"},   # toggle choices
                ],
                "toggle-down": [
                    {"key": "tab", "filter":False},
                ],
            }.update(default_bindings)
            kwargs["multiselect"] = True
        return inquirer.fuzzy(message, choices=choices, default=default or "", max_height=8, border=True, style=STYLE, **kwargs).execute()
    except KeyboardInterrupt:
        return abort()

def confirm(message:str, default:bool = False) -> bool:
    try:
        return inquirer.confirm(message, default=default, keybindings=default_bindings).execute()
    except KeyboardInterrupt:
        return abort()

def text(message:str, default:str|None = None) -> str:
    try:
        return inquirer.text(message, default=default or "", keybindings=default_bindings).execute()
    except KeyboardInterrupt:
        return abort()

def password(message:str, default:str|None = None) -> str:
    try:
        return inquirer.secret(message, default=default or "", keybindings=default_bindings).execute()
    except KeyboardInterrupt:
        return abort()

#--------------------------------------------------
# Spinner
#--------------------------------------------------

class Spinner:
    busy = False
    delay = 0.1

    def __init__(self, message="", finished="", delay=None):
        self.message = message
        self.finished = finished
        self.spinner_generator = itertools.cycle([ "▰▱▱▱", "▰▰▱▱", "▰▰▰▱", "▰▰▰▰", "▱▰▰▰", "▱▱▰▰", "▱▱▱▰", "▱▱▱▱" ])
        if delay and float(delay):
            self.delay = delay

    def get_message(self):
        return rich_str(f"[magenta]{next(self.spinner_generator)} {self.message}").strip()

    def get_clear(self, message:str):
        return '\b'* len(message.encode('utf-8'))

    def spinner_task(self):
        while self.busy:
            message = self.get_message()
            sys.stdout.write(message)
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write(self.get_clear(message))
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        if jupyter.ipython:
            message = self.get_message()
            sys.stdout.write(message)
            sys.stdout.flush()
        else:
            threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        if exception is not None:
            return False
        time.sleep(self.delay)
        message = self.get_message()
        sys.stdout.write(self.get_clear(message))
        if self.finished != "":
            final_message = f"[green]▰▰▰▰ {self.finished}"
            final_message += " " * (len(message) - len(final_message))
            rich.print(final_message)
        elif self.finished == "":
            sys.stdout.write(self.get_clear(message))
            sys.stdout.write(" "*len(message.encode('utf-8')))
            sys.stdout.write(self.get_clear(message))
            sys.stdout.flush()
