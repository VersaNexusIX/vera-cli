#!/usr/bin/env python3
# coding: utf-8
import os
import sys
from colorama import Fore, Style, init as colorama_init
from config import BOT, DOWNLOAD_ROOT
from utils.ascii        import show_ascii_banner
from utils.parse_prompt import parse_prompt
from utils.anim         import clear_screen, exit_anim, loading_anim
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
from handlers.git_search    import handle as git_search
from handlers.sysinfo       import handle as sysinfo
from handlers.ipinfo        import handle as ipinfo
from handlers.encode_decode import handle_encode, handle_decode
from handlers.hash_gen      import handle as hash_gen
COMMANDS = {
    "tt":           tiktok,
    "yt":           yt,
    "sp":           spotify,
    "am":           allmedia,
    "ig":           ig,
    "fb":           fb,
    "x":            x,
    "pin":          pinterest,
    "git":          gitclone,
    "git_search":   git_search,
    "webfile":      webfile,
    "webgrab":      web_grab,
    "weather":      cuaca,
    "anime":        anime,
    "osint-mail":   osint_email,
    "sysinfo":      sysinfo,
    "ipinfo":       ipinfo,
    "encode":       handle_encode,
    "decode":       handle_decode,
    "hash":         hash_gen,
    "quiz":         quiz,
    "guest_number": tebak_angka,
    "ascii":        ascii_gen,
    "setpersona":   botPersona,
}
ALIASES = {
    "tiktok":    "tt",
    "youtube":   "yt",
    "insta":     "ig",
    "instagram": "ig",
    "twit":      "x",
    "twitter":   "x",
    "github":    "git_search",
    "cuaca":     "weather",
    "w":         "weather",
}
HELP_TEXT = Fore.CYAN + """
  ──────────────────────────────────────────
  📥  DOWNLOADER
  ──────────────────────────────────────────
  tt  <url>           : TikTok (video / audio / slide)
  yt  <url>           : YouTube (MP4 / MP3)
  sp  <url>           : Spotify track (MP3 / cover)
  am  <url>           : AllMedia (Instagram / Facebook)
  ig  <url>           : Instagram via yt-dlp
  fb  <url>           : Facebook via yt-dlp
  x   <url>           : X / Twitter via yt-dlp
  pin <url>           : Pinterest video

  ──────────────────────────────────────────
  🔧  DEVELOPER
  ──────────────────────────────────────────
  git <url>           : Clone repository
  git_search <q>      : Search GitHub
  webfile <url>       : Download files from web page
  webgrab <url>       : Web scanner + file grabber

  ──────────────────────────────────────────
  🌐  INFO & OSINT
  ──────────────────────────────────────────
  weather <city>      : Current weather
  anime <title>       : Anime info (MyAnimeList)
  osint-mail <email>  : Email OSINT scan
  sysinfo             : System info
  ipinfo [ip]         : IP geolocation

  ──────────────────────────────────────────
  🔐  ENCODE / HASH
  ──────────────────────────────────────────
  encode <method> <text>   : base64 | url | hex | rot13
  decode <method> <text>   : base64 | url | hex | rot13
  hash   <text>            : SHA-256 (--algo md5|sha1|sha256|all)

  ──────────────────────────────────────────
  🎮  GAME & FUN
  ──────────────────────────────────────────
  quiz [local|online]      : Trivia / quiz
  guest_number [easy|hard] : Number guessing game
  ascii <text>             : ASCII art

  ──────────────────────────────────────────
  ⚙️   SYSTEM
  ──────────────────────────────────────────
  setpersona [query]  : View / test bot persona
  help / ?            : Show this menu
  exit / quit         : Exit

  ──────────────────────────────────────────
  💡  --visible  : move file to public folder
  💡  Aliases: cuaca=weather, insta=ig, tiktok=tt
  ──────────────────────────────────────────
""" + Style.RESET_ALL
def process_command(text):
    parsed = parse_prompt(text)
    cmd    = parsed["command"]
    args   = parsed["args"]
    if not cmd:
        return Fore.YELLOW + "  ⚠️  Type 'help' for command list." + Style.RESET_ALL
    if cmd in ("help", "?"):
        return HELP_TEXT
    if cmd in ("exit", "quit", "q"):
        return None
    cmd = ALIASES.get(cmd, cmd)
    handler = COMMANDS.get(cmd)
    if not handler:
        suggestions = [c for c in COMMANDS if c.startswith(cmd[:2])]
        hint = f"\n  Did you mean: {', '.join(suggestions[:3])}?" if suggestions else ""
        return Fore.RED + f"  ❌ Unknown command '{cmd}'.{hint}" + Style.RESET_ALL
    loading_anim()
    try:
        result = handler(args if cmd != "webfile" else (args if args else []))
        return "" if result is None else str(result)
    except KeyboardInterrupt:
        return Fore.YELLOW + "\n  ⚠️  Cancelled." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"\n  ❌ Error '{cmd}': {e}" + Style.RESET_ALL
def cli_loop():
    colorama_init(autoreset=True)
    clear_screen()
    show_ascii_banner()
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(            "  Enter your name to start")
    print(            "  ──────────────────────────────────────────" + Style.RESET_ALL)
    username = input(Fore.MAGENTA + "  Name : " + Style.RESET_ALL).strip() or "Anon"
    print(Fore.CYAN + f"""
  ──────────────────────────────────────────
  Name       : {BOT["name"]}
  Version    : v{BOT["version"]}
  Developer  : {BOT["developer"]}
  User       : {username}
  Download   : {DOWNLOAD_ROOT}
  ──────────────────────────────────────────
  Type 'help' for menu  ·  'exit' to quit
  ──────────────────────────────────────────
""" + Style.RESET_ALL)
    while True:
        try:
            prompt_str = (
                Fore.MAGENTA + f"  {username}" +
                Fore.WHITE   + " : " +
                Style.RESET_ALL
            )
            inp = input(prompt_str).strip()
            if not inp:
                continue
            out = process_command(inp)
            if out is None:
                exit_anim(username)
                break
            if out:
                print(out + "\n")
        except (KeyboardInterrupt, EOFError):
            exit_anim(username)
            break
if __name__ == "__main__":
    cli_loop()
