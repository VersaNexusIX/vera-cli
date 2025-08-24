from colorama import Fore, Style, init as colorama_init

def show_ascii_banner():
    colorama_init(autoreset=True

    print(Fore.BLUE + r"""
╔╗──╔╦═══╦═══╦═══╗
║╚╗╔╝║╔══╣╔═╗║╔═╗║
╚╗║║╔╣╚══╣╚═╝║║─║║
─║╚╝║║╔══╣╔╗╔╣╚═╝║
─╚╗╔╝║╚══╣║║╚╣╔═╗║
──╚╝─╚═══╩╝╚═╩╝─╚╝
""")

    text = "𝐕𝐄𝐑𝐀 - 𝐂𝐋𝐈 𝐀𝐒𝐒𝐈𝐒𝐓𝐀𝐍𝐓"
    gradient = [Fore.BLUE]
    steps = len(gradient)
    seg_len = max(1, len(text) // steps)

    colored_text = ""
    for i, char in enumerate(text):
        color_index = min(i // seg_len, steps - 1)
        colored_text += gradient[color_index] + char

    print(colored_text + Style.RESET_ALL)