from pyfiglet import Figlet
from colorama import Fore, Style

def handle(args):
    if not args:
        return Fore.YELLOW + "⚠️ Format: ascii <teks>" + Style.RESET_ALL

    text = " ".join(args)
    font = ask_font()

    try:
        fig = Figlet(font=font)
        ascii_art = fig.renderText(text)
        return Fore.CYAN + ascii_art + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"❌ Gagal generate ASCII: {e}" + Style.RESET_ALL

def ask_font():
    print(Fore.CYAN + "\nPilih font:")
    print("1. standard\n2. slant\n3. block\n4. cancel" + Style.RESET_ALL)
    choice = input("Font (1/2/3/4): ").strip()

    return {
        "1": "standard",
        "2": "slant",
        "3": "block"
    }.get(choice, "standard")