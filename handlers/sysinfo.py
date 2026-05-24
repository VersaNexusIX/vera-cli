import os
import platform
from colorama import Fore, Style
def handle(args):
    sys_name = platform.system()
    release  = platform.release()
    machine  = platform.machine()
    node     = platform.node()
    python   = platform.python_version()
    cpu      = _get_cpu()
    mem      = _get_mem()
    disk     = _get_disk()
    return Fore.CYAN + f"""
  💻  System Information
  ──────────────────────────────────────────
  OS         : {sys_name} {release}
  Machine    : {machine}
  Hostname   : {node}
  Python     : {python}
  CPU        : {cpu}
  Memory     : {mem}
  Disk       : {disk}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
def _get_cpu():
    try:
        if platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        return platform.processor() or "Unknown"
    except Exception:
        return "Unknown"
def _get_mem():
    try:
        if platform.system() == "Linux":
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            total = int(lines[0].split()[1]) // 1024
            avail = int(lines[2].split()[1]) // 1024
            return f"{avail} MB free / {total} MB total"
        return "N/A"
    except Exception:
        return "N/A"
def _get_disk():
    try:
        stat  = os.statvfs(os.path.expanduser("~"))
        free  = stat.f_bavail * stat.f_frsize // (1024 ** 3)
        total = stat.f_blocks * stat.f_frsize // (1024 ** 3)
        return f"{free} GB free / {total} GB total"
    except Exception:
        return "N/A"
