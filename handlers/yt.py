import os
import subprocess
from colorama import Fore, Style
from utils.vera_utils import get_next_filename, trigger_media_scan, get_download_path, move_to_public_and_scan
COOKIES_PATH = os.path.join(os.path.expanduser("~"), "cookies.txt")
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: yt <url> [--visible]" + Style.RESET_ALL
    return _download(args[0], visible="--visible" in args)
def _download(url, visible=False):
    print(Fore.CYAN + "\n  📺  VERA YouTube Downloader")
    print(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
    if "youtube.com" not in url and "youtu.be" not in url:
        return Fore.RED + "  ❌  Not a valid YouTube URL." + Style.RESET_ALL
    print(Fore.WHITE + "  [1] 🎧 Audio (MP3)")
    print(           "  [2] 🎥 Video (MP4)")
    print(           "  [3] ❌ Cancel" + Style.RESET_ALL)
    choice = input(Fore.MAGENTA + "  Format : " + Style.RESET_ALL).strip()
    if choice == "3":
        return Fore.CYAN + "  ❎  Cancelled." + Style.RESET_ALL
    if choice not in ("1", "2"):
        return Fore.RED + "  ❌  Invalid choice." + Style.RESET_ALL
    fmt      = "mp3" if choice == "1" else "mp4"
    folder   = get_download_path("VERA_YouTube")
    filename = get_next_filename(fmt, prefix="YT_", folder=folder)
    args_dl = ["yt-dlp", "-o", filename]
    if os.path.exists(COOKIES_PATH):
        args_dl += ["--cookies", COOKIES_PATH]
        print(Fore.DIM + "  🍪  Using cookies.txt" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "  ⚠️  cookies.txt not found — may fail if YouTube blocks the request" + Style.RESET_ALL)
        print(Fore.DIM    + "  💡  Place cookies.txt at ~/cookies.txt to bypass bot-check" + Style.RESET_ALL)
    args_dl += ["--extractor-retries", "3", "--no-abort-on-error"]
    if fmt == "mp4":
        args_dl += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"]
    else:
        args_dl += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
    args_dl.append(url)
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(           f"  🔄  Downloading {fmt.upper()}..." + Style.RESET_ALL)
    try:
        subprocess.run(args_dl, check=True)
        trigger_media_scan(filename)
        final = move_to_public_and_scan(filename, "YouTube") if visible else filename
        return Fore.GREEN + f"""
  ──────────────────────────────────────────
  ✅  Done
  Path     : {final}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except subprocess.CalledProcessError:
        return Fore.RED + """
  ──────────────────────────────────────────
  ❌  Download failed
  ──────────────────────────────────────────
  Possible causes:
  • YouTube blocked the request (rate limit / bot check)
  • Solution: place cookies.txt at ~/cookies.txt
  • Export cookies from your browser using the
    "Get cookies.txt LOCALLY" extension
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except FileNotFoundError:
        return Fore.RED + "  ❌  yt-dlp not found. Install: pip install yt-dlp" + Style.RESET_ALL
