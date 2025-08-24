import os
import subprocess
import re
from colorama import Fore, Style

def get_download_path():
    return "/storage/emulated/0/Download"

def get_next_filename(extension, prefix="VERA_", folder=None):
    folder = folder or get_download_path()
    os.makedirs(folder, exist_ok=True)

    i = 1
    while True:
        filename = os.path.join(folder, f"{prefix}{str(i).zfill(3)}.{extension}")
        if not os.path.exists(filename):
            return filename
        i += 1

def trigger_media_scan(filepath):
    try:
        subprocess.run([
            "am", "broadcast",
            "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
            "-d", f"file://{filepath}"
        ], check=True)
    except Exception as e:
        print(Fore.RED + f"VERA : ❌ Gagal scan media: {e}" + Style.RESET_ALL)

def move_to_public_and_scan(local_path):
    target_path = os.path.join(get_download_path(), os.path.basename(local_path))
    try:
        if os.path.exists(target_path):
            os.remove(target_path)
        os.rename(local_path, target_path)
        trigger_media_scan(target_path)
        print(Fore.GREEN + f"VERA : ✅ File moved to: {target_path}")
        print("VERA : 📂 The file is now accessible." + Style.RESET_ALL)
        return target_path
    except Exception as e:
        print(Fore.RED + f"VERA : ❌ Failed to move/scan: {e}" + Style.RESET_ALL)
        return local_path

def extract_path_from_result(result):
    match = re.search(r'Disimpan di: (.*)', result)
    return match.group(1).strip() if match else None