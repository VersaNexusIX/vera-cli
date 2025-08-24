import sys
import time
import os
from colorama import Fore, Style

def loading_anim(text="Loading..."):
    print(Fore.CYAN + f"\n{text}", end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print(Style.RESET_ALL)

def exit_anim(username):
    print(Fore.CYAN + f"\n👋 Bye {username}!")
    print(Fore.MAGENTA + """
█░█ █▀ █▀▀▄ ▄▀▄
█░█ █▀ █▐█▀ █▀█
░▀░ ▀▀ ▀░▀▀ ▀░▀
""")
    time.sleep(1)
    clear_screen()
    sys.exit(0)

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")