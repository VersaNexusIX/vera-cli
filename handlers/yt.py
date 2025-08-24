import subprocess
from colorama import Fore, Style
from utils.vera_utils import get_next_filename, trigger_media_scan

def banner():
    print(Fore.CYAN + r"""
█░█ █▀ █▀▀▄ ▄▀▄
█░█ █▀ █▐█▀ █▀█
░▀░ ▀▀ ▀░▀▀ ▀░▀

 𝗬𝗧 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗥 𝗕𝗬 𝗩𝗘𝗥𝗔
""" + Style.RESET_ALL)

def yt_downloader(url):
    banner()
    if "youtube.com" not in url and "youtu.be" not in url:
        return Fore.RED + "VERA : URL bukan YouTube." + Style.RESET_ALL

    print(Fore.YELLOW + "VERA : Pilih format unduhan:")
    print("  1. 🎧 Audio (.mp3)")
    print("  2. 🎥 Video (.mp4)")
    print("  3. ❌ Batal")
    choice = input(Fore.MAGENTA + "Format [1/2/3] : ").strip()
    if choice == "3":
        return Fore.BLUE + "VERA : process cancelled"

    format_map = {"1": "mp3", "2": "mp4"}
    format_choice = format_map.get(choice)
    if not format_choice:
        return Fore.RED + "VERA : not a valid number"

    filename = get_next_filename(format_choice)
    ytdlp_args = ["yt-dlp", "-o", filename]
    if format_choice == "mp4":
        ytdlp_args += ["-f", "mp4"]
    elif format_choice == "mp3":
        ytdlp_args += ["-x", "--audio-format", "mp3"]
    ytdlp_args.append(url)

    print(Fore.CYAN + "VERA : 🔄 installing..." + Style.RESET_ALL)

    try:
        subprocess.run(ytdlp_args, check=True)
        trigger_media_scan(filename)
        return Fore.GREEN + f"VERA : ✅ saved to: {filename}"
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"VERA : Failed to install : {str(e)}"

def handle(args):
    if not args:
        return Fore.YELLOW + "VERA : try: yt <link>"
    return yt_downloader(args[0])