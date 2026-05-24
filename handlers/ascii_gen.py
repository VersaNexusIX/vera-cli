from colorama import Fore, Style
try:
    import pyfiglet
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False
FONTS = {"1": "standard", "2": "banner3", "3": "block", "4": "slant", "5": "big"}
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: ascii <text>" + Style.RESET_ALL
    text = " ".join(args)
    print(Fore.CYAN + "\n  🎨  ASCII Art Generator")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print("  [1] Standard  [2] Banner3  [3] Block")
    print("  [4] Slant     [5] Big      [6] Simple" + Style.RESET_ALL)
    choice = input(Fore.MAGENTA + "  Font : " + Style.RESET_ALL).strip()
    if choice == "6" or not HAS_PYFIGLET:
        return _simple(text)
    font = FONTS.get(choice, "standard")
    try:
        result = pyfiglet.figlet_format(text, font=font)
        return Fore.CYAN + "\n" + result + Style.RESET_ALL
    except Exception:
        result = pyfiglet.figlet_format(text, font="standard")
        return Fore.CYAN + "\n" + result + Style.RESET_ALL
def _simple(text):
    upper  = text.upper()
    border = "─" * (len(upper) + 6)
    return Fore.CYAN + f"\n  {border}\n  ─  {upper}  ─\n  {border}\n" + Style.RESET_ALL
