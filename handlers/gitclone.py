import os
import subprocess
from colorama import Fore, Style
from utils.vera_utils import get_download_path, trigger_media_scan
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: git <url>" + Style.RESET_ALL
    url       = args[0]
    repo_name = url.rstrip("/").split("/")[-1].removesuffix(".git")
    target    = os.path.join(get_download_path("VERA_Git"), repo_name)
    if os.path.exists(target):
        return Fore.YELLOW + f"  ⚠️  Directory already exists: {target}" + Style.RESET_ALL
    print(Fore.CYAN + "\n  🔧  VERA Git Clone")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(Fore.WHITE + f"  URL    : {url}")
    print(            f"  Target : {target}")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(            "  🔄  Cloning..." + Style.RESET_ALL)
    try:
        subprocess.run(["git", "clone", "--progress", url, target], check=True)
        trigger_media_scan(target)
        return Fore.GREEN + f"""
  ──────────────────────────────────────────
  ✅  Done
  Path     : {target}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"  ❌  git clone failed: {e}" + Style.RESET_ALL
    except FileNotFoundError:
        return Fore.RED + "  ❌  git not found. Please install git first." + Style.RESET_ALL
