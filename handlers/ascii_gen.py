from colorama import Fore, Style

def handle(args):
    if not args:
        return Fore.YELLOW + "⚠️ Format: ascii <teks>" + Style.RESET_ALL

    text = " ".join(args)
    font = ask_font()

    try:
        ascii_art = generate_ascii(text, font)
        return Fore.CYAN + ascii_art + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"❌ Failed to generate ASCII: {e}" + Style.RESET_ALL

def ask_font():
    print(Fore.CYAN + "\nPilih font:")
    print("1. standard\n2. wide\n3. box\n4. cancel" + Style.RESET_ALL)
    choice = input("Font (1/2/3/4): ").strip()

    return {
        "1": "standard",
        "2": "wide",
        "3": "box"
    }.get(choice, "standard")

def generate_ascii(text, font):
    if font == "wide":
        return " ".join(list(text.upper()))
    elif font == "box":
        border = "█" * (len(text) + 4)
        return f"{border}\n█ {text.upper()} █\n{border}"
    else:  # standard
        return text.upper()