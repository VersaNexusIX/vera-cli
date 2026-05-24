import os
import subprocess
from colorama import Fore, Style
from utils.vera_utils import get_next_filename, move_to_public_and_scan, trigger_media_scan, get_download_path
COOKIES_PATH = os.path.join(os.path.expanduser("~"), "cookies.txt")
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: sp <spotify_url> [--visible]" + Style.RESET_ALL
    spotify_url = args[0]
    visible     = "--visible" in args
    print(Fore.CYAN + "\n  🎵  VERA Spotify Downloader")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(Fore.WHITE + "  [1] 🎵 Audio (MP3)")
    print(            "  [2] 🖼️  Cover Art")
    print(            "  [3] ❌ Cancel" + Style.RESET_ALL)
    choice = input(Fore.MAGENTA + "  Choice : " + Style.RESET_ALL).strip()
    if choice == "3":
        return Fore.CYAN + "  ❎  Cancelled." + Style.RESET_ALL
    if choice not in ("1", "2"):
        return Fore.RED + "  ❌  Invalid choice." + Style.RESET_ALL
    try:
        if "/track/" in spotify_url:
            track_id = spotify_url.split("/track/")[1].split("?")[0]
        elif "/playlist/" in spotify_url:
            return Fore.YELLOW + "  ⚠️  Playlist not supported. Use a track URL." + Style.RESET_ALL
        else:
            return Fore.RED + "  ❌  Invalid Spotify URL." + Style.RESET_ALL
        search_query = f"ytsearch1:{track_id} official audio"
    except Exception:
        return Fore.RED + "  ❌  Failed to process Spotify URL." + Style.RESET_ALL
    folder  = get_download_path("VERA_Spotify")
    ytargs  = ["yt-dlp"]
    if os.path.exists(COOKIES_PATH):
        ytargs += ["--cookies", COOKIES_PATH]
        print(Fore.DIM + "  🍪  Using cookies.txt" + Style.RESET_ALL)
    ytargs += ["--extractor-retries", "3", "--no-abort-on-error"]
    if choice == "1":
        filename = get_next_filename("mp3", prefix="SP_", folder=folder)
        ytargs  += ["--extract-audio", "--audio-format", "mp3", "--audio-quality", "0",
                    "-o", filename, search_query]
    else:
        filename = get_next_filename("jpg", prefix="SP_", folder=folder)
        ytargs  += ["--skip-download", "--write-thumbnail",
                    "--convert-thumbnails", "jpg", "-o", filename, search_query]
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(           "  🔄  Downloading..." + Style.RESET_ALL)
    try:
        subprocess.run(ytargs, check=True)
        trigger_media_scan(filename)
        final = move_to_public_and_scan(filename, "Spotify") if visible else filename
        return Fore.GREEN + f"""
  ──────────────────────────────────────────
  ✅  Done
  Path     : {final}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"  ❌  Download failed: {e}" + Style.RESET_ALL
    except FileNotFoundError:
        return Fore.RED + "  ❌  yt-dlp not found." + Style.RESET_ALL
