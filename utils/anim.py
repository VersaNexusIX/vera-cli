import sys
import time
import os
from colorama import Fore, Style
def loading_anim(text: str = "Processing") -> None:
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    print()
    for i in range(12):
        frame = frames[i % len(frames)]
        print(
            Fore.CYAN + f"\r  {frame}  {text}..." + Style.RESET_ALL,
            end="", flush=True
        )
        time.sleep(0.1)
    print("\r" + " " * 40 + "\r", end="", flush=True)
def progress_bar(current: int, total: int, prefix: str = "", width: int = 30) -> None:
    filled = int(width * current / max(total, 1))
    bar = "█" * filled + "░" * (width - filled)
    pct = int(100 * current / max(total, 1))
    print(
        Fore.CYAN + f"\r  {prefix} [{bar}] {pct}%" + Style.RESET_ALL,
        end="", flush=True
    )
    if current >= total:
        print()
def exit_anim(username: str) -> None:
    print(Fore.CYAN + f"\n  👋  See you later, {username}!\n")
    print(Fore.MAGENTA + Style.DIM + "  VERA CLI — shutting down..." + Style.RESET_ALL)
    time.sleep(0.8)
    clear_screen()
    sys.exit(0)
def clear_screen() -> None:
    os.system("clear" if os.name != "nt" else "cls")
