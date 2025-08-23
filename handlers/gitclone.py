import os
import subprocess
from utils.vera_utils import get_download_path, trigger_media_scan
from colorama import Fore, Style

def handle(args):
    if not args:
        return Fore.YELLOW + "⚠️ Link repository kosong." + Style.RESET_ALL

    url = args[0]
    repo_name = extract_repo_name(url)
    target_dir = os.path.join(get_download_path(), "VERA_GIT", repo_name)

    try:
        os.makedirs(target_dir, exist_ok=True)

        print(Fore.CYAN + f"VERA : 🔄 Cloning ke {target_dir}..." + Style.RESET_ALL)
        subprocess.run(["git", "clone", url, target_dir], check=True)

        trigger_media_scan(target_dir)
        return Fore.GREEN + f"✅ Repo berhasil di-clone ke: {target_dir}" + Style.RESET_ALL

    except subprocess.CalledProcessError as e:
        return Fore.RED + f"❌ Gagal clone repo: {e}" + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"❌ Error sistem: {e}" + Style.RESET_ALL

def extract_repo_name(url):
    return url.rstrip("/").split("/")[-1].replace(".git", "")