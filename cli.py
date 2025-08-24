#!/usr/bin/env python3
# coding: utf-8

import os
from colorama import Fore, Style, init as colorama_init

# VERA Core
from config import BOT
from utils.ascii import show_ascii_banner
from utils.parse_prompt import parse_prompt
from utils.anim import clear_screen, exit_anim, loading_anim

# Handlers registry
from handlers.allmedia      import handle as allmedia
from handlers.botPersona    import handle as botPersona
from handlers.tiktok        import handle as tiktok
from handlers.yt            import handle as yt
from handlers.spotify       import handle as spotify
from handlers.cuaca         import handle as cuaca
from handlers.pinterest     import handle as pinterest
from handlers.quiz          import handle as quiz
from handlers.ig            import handle as ig
from handlers.fb            import handle as fb
from handlers.x             import handle as x
from handlers.gitclone      import handle as gitclone
from handlers.ascii_gen     import handle as ascii_gen
from handlers.osint_email   import handle as osint_email
from handlers.anime         import handle as anime
from handlers.tebak_angka   import handle as tebak_angka
from handlers.webfile       import handle as webfile
from handlers.web_grab      import handle as web_grab
from handlers.wa            import handle as wa
from handlers.git_search    import handle as git_search

# Command registry
commands = {
    "tt":           tiktok,
    "sp":           spotify,
    "yt":           yt,
    "am":           allmedia,
    "cuaca":        cuaca, 
    "git":          gitclone,
    "quiz":         quiz,
    "ig":           ig,
    "fb":           fb,
    "x":            x,
    "pin":          pinterest,
    "setpersona":   set_persona,
    "ascii":        ascii_gen,
    "osint-mail":   osint_email,
    "anime":        anime,
    "guest_number":  tebak_angka,
    "webfile":      webfile,
    "webgrab":      web_grab,
    "wa":           wa,
    "git_search":   git_search,
}

def print_cyan(text: str):
    print(Fore.CYAN + text + Style.RESET_ALL)

def init_assets():
    folder, help_file = "assets", os.path.join("assets", "help.txt")
    os.makedirs(folder, exist_ok=True)
    if not os.path.isfile(help_file):
        default = """
        █░█ █▀ █▀▀▄ ▄▀▄
        █░█ █▀ █▐█▀ █▀█
        ░▀░ ▀▀ ▀░▀▀ ▀░▀

            MENU LIST

tt <link>       TikTok
yt <link>       YouTube
am <link>       AllMedia
sp <link>       Spotify
pin <link>      Pinterest
git <url>       Git clone URL
ascii <text>    ASCII generator
quiz <type>     Quiz (tebak/teka/online)
vera <prompt>   Chat VERA
cuaca <kota>    Weather
webfile <url>   Download file
webgrab [opts]  Scan & grab
help            Show this help
exit            Quit (CLI)
        """
        with open(help_file, "w", encoding="utf-8") as f:
            f.write(default)

def show_help():
    try:
        return open("assets/help.txt", "r", encoding="utf-8").read()
    except Exception:
        return "⚠️ Could not load help.txt\n"

def process_command(text: str) -> str:
    parsed = parse_prompt(text)
    cmd, args = parsed["command"], parsed["args"]

    if cmd == "help":
        return show_help()
    if cmd == "exit":
        return None

    handler = commands.get(cmd)
    if not handler:
        return f"🤔 Unknown command '{cmd}'. Try 'help'."

    loading_anim()
    try:
        if cmd == "webfile":
            payload = {"url": args[0] if args else None, "folder": "AUTO"}
            res = handler(payload)
        else:
            res = handler(args)
        return "" if res is None else str(res)
    except Exception as e:
        return f"❌ Error in '{cmd}': {e}"

def cli_loop():
    colorama_init(autoreset=True)
    clear_screen()
    show_ascii_banner()  # ← ini harus dipanggil, bukan cuma disebut
    init_assets()

    username = input(Fore.CYAN + "Enter name : " + Style.RESET_ALL).strip() or "Anon"

    print_cyan(f"""
╭────────────────────
│ ɴᴀᴍᴇ   : {BOT["name"]}
│ ᴠᴇʀsɪᴏɴ : 0.0.0 (ʙᴇᴛᴀ) 
│ ᴅᴇᴠᴇʟᴏᴘᴇʀ : Versa NexusIX
│ ᴜsᴇʀ    : {username}
╰────────────────────

ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴠᴇʀᴀ ᴄʟɪ {username}
ᴛʏᴘᴇ "ʜᴇʟᴘ" ᴛᴏ ʙʀɪɴɢ ᴜᴘ ᴛʜᴇ ᴍᴇɴᴜ
""")

    while True:
        try:
            inp = input(Fore.MAGENTA + f"{username} : " + Style.RESET_ALL).strip()
            if not inp:
                print("ᴄᴀɴɴᴏᴛ ғᴏᴜɴᴅ ɪɴᴘᴜᴛs.\n")
                continue

            out = process_command(inp)
            if out is None:
                exit_anim(username)
                break

            print_cyan(out + "\n")
        except (KeyboardInterrupt, EOFError):
            exit_anim(username)
            break

if __name__ == "__main__":
    cli_loop()