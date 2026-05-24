from colorama import Fore, Style
from config import BOT
def handle(args):
    query   = " ".join(args).strip()
    name    = BOT.get("name", "VERA")
    persona = BOT.get("persona", "Versatile CLI assistant.")
    if not query:
        print(Fore.CYAN + f"\n  🤖  Active Persona : {name}")
        print(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
        for line in persona.split("\n"):
            if line.strip():
                print(Fore.WHITE + "  " + line.strip() + Style.RESET_ALL)
        print(Fore.CYAN + "  ──────────────────────────────────────────")
        print(Fore.DIM  + "  Example: setpersona Who are you?\n" + Style.RESET_ALL)
        return
    first_line = persona.split("\n")[0]
    return Fore.CYAN + f"""
  🤖  {name} — Persona Mode
  ──────────────────────────────────────────
  Question   : {query}
  ──────────────────────────────────────────
  Answer     : I'm {name}. {first_line}
               If there's anything I can help with, just ask.
  ──────────────────────────────────────────
""" + Style.RESET_ALL
