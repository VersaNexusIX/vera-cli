import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style
from utils.vera_utils import get_download_path, sanitize_filename, human_size
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
EXTS    = [".html",".js",".css",".jpg",".jpeg",".png",".pdf",
           ".mp4",".zip",".woff",".ttf",".sql",".xlsx"]
def handle(args):
    if isinstance(args, dict):
        url = args.get("url")
    elif isinstance(args, list) and args:
        url = args[0]
    else:
        return Fore.YELLOW + "  ⚠️  Format: webfile <url>" + Style.RESET_ALL
    if not url:
        return Fore.RED + "  ❌  No URL provided." + Style.RESET_ALL
    print(Fore.CYAN + "\n  🌐  VERA Webfile Downloader")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(Fore.WHITE + f"  URL    : {url}" + Style.RESET_ALL)
    try:
        r    = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        return Fore.RED + f"  ❌  Failed to fetch page: {e}" + Style.RESET_ALL
    domain  = urlparse(url).netloc.replace("www.", "")
    out_dir = get_download_path(f"VERA_Webfile_{sanitize_filename(domain)}")
    links   = []
    for tag in soup.find_all(["a", "link", "script", "img"]):
        src = tag.get("href") or tag.get("src")
        if src:
            full = urljoin(url, src)
            if any(full.lower().endswith(ext) for ext in EXTS):
                links.append(full)
    if not links:
        return Fore.YELLOW + "  ⚠️  No downloadable files found on this page." + Style.RESET_ALL
    print(Fore.CYAN + f"  Files    : {len(links)} found")
    print(           f"  Output   : {out_dir}")
    print(           "  ──────────────────────────────────────────" + Style.RESET_ALL)
    log = []
    for i, link in enumerate(links, 1):
        fname = sanitize_filename(link.split("/")[-1].split("?")[0]) or f"file_{i}"
        path  = os.path.join(out_dir, fname)
        print(Fore.CYAN + f"  [{i}/{len(links)}] {fname}" + Style.RESET_ALL, end="\r")
        try:
            res = requests.get(link, headers=HEADERS, timeout=15)
            with open(path, "wb") as f:
                f.write(res.content)
            log.append({"file": fname, "url": link, "size": len(res.content), "ok": True})
        except Exception as e:
            log.append({"file": fname, "url": link, "size": 0, "ok": False, "error": str(e)})
    with open(os.path.join(out_dir, "harvest_log.json"), "w") as f:
        json.dump({"source": url, "files": log}, f, indent=2)
    ok          = sum(1 for e in log if e["ok"])
    total_bytes = sum(e["size"] for e in log)
    print()
    return Fore.GREEN + f"""
  ──────────────────────────────────────────
  ✅  Done
  Success    : {ok}/{len(links)} files
  Total size : {human_size(total_bytes)}
  Output     : {out_dir}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
