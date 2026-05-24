import os
import re
import subprocess
from colorama import Fore, Style
from config import DOWNLOAD_ROOT
def get_download_path(subfolder: str = "") -> str:
    path = os.path.join(DOWNLOAD_ROOT, subfolder) if subfolder else DOWNLOAD_ROOT
    os.makedirs(path, exist_ok=True)
    return path
def get_next_filename(extension: str, prefix: str = "VERA_", folder: str = None) -> str:
    folder = folder or get_download_path()
    os.makedirs(folder, exist_ok=True)
    i = 1
    while True:
        filename = os.path.join(folder, f"{prefix}{str(i).zfill(3)}.{extension}")
        if not os.path.exists(filename):
            return filename
        i += 1
def human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"
def is_termux() -> bool:
    return os.path.exists("/data/data/com.termux")
def trigger_media_scan(filepath: str) -> None:
    if not is_termux():
        return
    try:
        subprocess.run(
            ["am", "broadcast",
             "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
             "-d", f"file://{filepath}"],
            check=True, capture_output=True,
        )
    except Exception as e:
        print(Fore.RED + f"[VERA] ⚠️  Media scan failed: {e}" + Style.RESET_ALL)
def move_to_public_and_scan(local_path: str, subfolder: str = "") -> str:
    target_dir = get_download_path(f"VERA_{subfolder}" if subfolder else "")
    target_path = os.path.join(target_dir, os.path.basename(local_path))
    try:
        if os.path.abspath(local_path) == os.path.abspath(target_path):
            trigger_media_scan(target_path)
            return target_path
        if os.path.exists(target_path):
            os.remove(target_path)
        os.rename(local_path, target_path)
        trigger_media_scan(target_path)
        print(Fore.GREEN + f"[VERA] ✅ Saved → {target_path}" + Style.RESET_ALL)
        return target_path
    except Exception as e:
        print(Fore.RED + f"[VERA] ❌ Move/scan failed: {e}" + Style.RESET_ALL)
        return local_path
def extract_path_from_result(result: str) -> str | None:
    match = re.search(r"Saved at:\s*(.+)", result)
    return match.group(1).strip() if match else None
def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)
