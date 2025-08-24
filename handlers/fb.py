import requests
from utils.vera_utils import get_next_filename, move_to_public_and_scan
from colorama import Fore, Style

def handle(args):
    if not args:
        return Fore.YELLOW + "⚠️ Empty format." + Style.RESET_ALL

    url = args[0]
    choice = ask_format()
    if choice == "4":
        return Fore.CYAN + "❎ Cancelled by user." + Style.RESET_ALL

    ext = get_ext(choice)
    filename = get_next_filename(ext, prefix="FB_")  # untuk fb.py

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

        final_path = movetopublicandscan(filename)
        return Fore.GREEN + f"✅ FB: saved to: {final_path}" + Style.RESET_ALL

    except Exception as e:
        return Fore.RED + f"❌ Failed download FB: {e}" + Style.RESET_ALL

def ask_format():
    print(Fore.CYAN + "\nPilih format unduhan:")
    print("1. Mp3\n2. Mp4\n3. Jpg\n4. Cancel" + Style.RESET_ALL)
    return input("Pilihan (1/2/3/4): ").strip()

def get_ext(choice):
    return {"1": "mp3", "2": "mp4", "3": "jpg"}.get(choice, "bin")