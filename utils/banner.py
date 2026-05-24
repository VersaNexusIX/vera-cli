from colorama import Fore, Style
from utils.vera_utils import human_size
def show_success_banner(file_path, size_bytes=0):
    size_str = f"\n  Size    : {human_size(size_bytes)}" if size_bytes else ""
    print(Fore.GREEN + f"""
  ✅  Download Complete
  ──────────────────────────────────────
  Path    : {file_path}{size_str}
  ──────────────────────────────────────
""" + Style.RESET_ALL)
def show_error_banner(message):
    print(Fore.RED + f"""
  ❌  Operation Failed
  ──────────────────────────────────────
  {message}
  ──────────────────────────────────────
""" + Style.RESET_ALL)
