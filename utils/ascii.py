from colorama import Fore, Style, init as colorama_init
from config import BOT
VERA_LOGO = r"""
 ██╗   ██╗███████╗██████╗  █████╗
 ██║   ██║██╔════╝██╔══██╗██╔══██╗
 ██║   ██║█████╗  ██████╔╝███████║
 ╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██║
  ╚████╔╝ ███████╗██║  ██║██║  ██║
   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
"""
def show_ascii_banner():
    colorama_init(autoreset=True)
    colors = [Fore.BLUE, Fore.BLUE, Fore.CYAN, Fore.CYAN, Fore.MAGENTA, Fore.MAGENTA, ""]
    for i, line in enumerate(VERA_LOGO.split("\n")):
        print(colors[min(i, len(colors)-1)] + line + Style.RESET_ALL)
    print(Fore.CYAN + "  ⚡ CLI ASSISTANT  ·  by " + BOT["developer"] + Style.RESET_ALL)
    print(Fore.WHITE + Style.DIM + f"  v{BOT['version']}  ·  {BOT['name']}" + Style.RESET_ALL)
    print()
