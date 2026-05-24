import os
import subprocess
from colorama import Fore, Style
from utils.vera_utils import get_next_filename, move_to_public_and_scan, get_download_path, trigger_media_scan
COOKIES_PATH = os.path.join(os.path.expanduser("~"), "cookies.txt")
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: fb <url> [--visible]" + Style.RESET_ALL
    url     = args[0]
    visible = "--visible" in args
    print(Fore.CYAN + "\n  📥  VERA Facebook Downloader")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(Fore.WHITE + "  [1] 🎧 MP3   [2] 🎥 MP4   [3] 🖼️  JPG   [4] ❌ Cancel" + Style.RESET_ALL)
    choice = input(Fore.MAGENTA + "  Format : " + Style.RESET_ALL).strip()
    if choice == "4":
        return Fore.CYAN + "  ❎  Cancelled." + Style.RESET_ALL
    ext    = {"1": "mp3", "2": "mp4", "3": "jpg"}.get(choice, "mp4")
    folder = get_download_path("VERA_Facebook")
    fname  = get_next_filename(ext, prefix="FB_", folder=folder)
    ytargs = ["yt-dlp", "-o", fname]
    if os.path.exists(COOKIES_PATH):
        ytargs += ["--cookies", COOKIES_PATH]
        print(Fore.DIM + "  🍪  Using cookies.txt" + Style.RESET_ALL)
    ytargs += ["--extractor-retries", "3", "--no-abort-on-error"]
    if ext == "mp3":
        ytargs += ["-x", "--audio-format", "mp3"]
    elif ext == "mp4":
        ytargs += ["-f", "best[ext=mp4]/best"]
    elif ext == "jpg":
        ytargs += ["--skip-download", "--write-thumbnail"]
    ytargs.append(url)
    print(Fore.CYAN + "  🔄  Downloading " + ext.upper() + "..." + Style.RESET_ALL)
    try:
        subprocess.run(ytargs, check=True)
        trigger_media_scan(fname)
        final = move_to_public_and_scan(fname, "Facebook") if visible else fname
        return Fore.GREEN + """
  ──────────────────────────────────────────
  ✅  Done
  Path     : """ + final + """
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except subprocess.CalledProcessError as e:
        return Fore.RED + "  ❌  Download failed: " + str(e) + Style.RESET_ALL
    except FileNotFoundError:
        return Fore.RED + "  ❌  yt-dlp not found." + Style.RESET_ALL
