import os
import re
import json
import subprocess
import requests
from colorama import Fore, Style
from utils.vera_utils import (
    get_next_filename, trigger_media_scan,
    move_to_public_and_scan, get_download_path,
)
COOKIES_PATH = os.path.join(os.path.expanduser("~"), "cookies.txt")
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: tt <url> [--visible]" + Style.RESET_ALL
    url     = args[0]
    visible = "--visible" in args
    print(Fore.CYAN + "  🔄  Resolving redirect..." + Style.RESET_ALL)
    final_url = _resolve_redirect(url)
    fmt = _prompt_format(final_url)
    if fmt == "cancel":
        return Fore.CYAN + "  ❎  Cancelled." + Style.RESET_ALL
    result, filepath = _download(final_url, fmt)
    if visible and filepath and os.path.exists(filepath):
        move_to_public_and_scan(filepath, "TikTok")
    return result
def _resolve_redirect(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        return r.url
    except Exception:
        return url
def _prompt_format(url):
    print(Fore.CYAN + "\n  📥  VERA TikTok Downloader")
    print(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
    if "/music/" in url:
        print(Fore.WHITE + "  [1] 🎧 Audio (MP3)   [2] ❌ Cancel" + Style.RESET_ALL)
        c = input(Fore.MAGENTA + "  Format : " + Style.RESET_ALL).strip()
        return "mp3" if c == "1" else "cancel"
    print(Fore.WHITE + "  [1] 🎥 Video (MP4)")
    print(             "  [2] 🎧 Audio (MP3)")
    print(             "  [3] 🖼️  Thumbnail (JPG)")
    print(             "  [4] 🖼️  Slide (multi-image)")
    print(             "  [5] ❌ Cancel" + Style.RESET_ALL)
    c = input(Fore.MAGENTA + "  Format : " + Style.RESET_ALL).strip()
    return {"1": "mp4", "2": "mp3", "3": "jpg", "4": "slide"}.get(c, "cancel")
def _build_ytargs(filename, fmt, url):
    args = ["yt-dlp", "-o", filename]
    if os.path.exists(COOKIES_PATH):
        args += ["--cookies", COOKIES_PATH]
        print(Fore.DIM + "  🍪  Using cookies.txt" + Style.RESET_ALL)
    args += ["--extractor-retries", "3", "--no-abort-on-error"]
    if fmt == "mp4":
        args += ["-f", "best[ext=mp4]/best"]
    elif fmt == "mp3":
        args += ["-x", "--audio-format", "mp3"]
    elif fmt == "jpg":
        args += ["--skip-download", "--write-thumbnail"]
    args.append(url)
    return args
def _download(url, fmt):
    folder = get_download_path("VERA_TikTok")
    if fmt == "slide":
        result = _download_slides(url, folder)
        return result, None
    filename = get_next_filename(fmt, prefix="TT_", folder=folder)
    ytargs   = _build_ytargs(filename, fmt, url)
    print(Fore.CYAN + f"  📥  Downloading {fmt.upper()}..." + Style.RESET_ALL)
    try:
        subprocess.run(ytargs, check=True)
        trigger_media_scan(filename)
        return Fore.GREEN + f"""
  ──────────────────────────────────────────
  ✅  Done
  Path     : {filename}
  ──────────────────────────────────────────
""" + Style.RESET_ALL, filename
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"  ❌  Failed: {e}" + Style.RESET_ALL, None
    except FileNotFoundError:
        return Fore.RED + "  ❌  yt-dlp not found." + Style.RESET_ALL, None
def _download_slides(url, folder):
    print(Fore.CYAN + "  🖼️   Detecting photo post..." + Style.RESET_ALL)
    try:
        r    = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        html = r.text
        image_urls = []
        m = re.search(r"window\.__UNIVERSAL_DATA__\s*=\s*(\{.*?\});", html)
        if m:
            try:
                data = json.loads(m.group(1))
                for k in data:
                    try:
                        imgs = data[k]["props"]["pageProps"]["itemInfo"]["itemStruct"]["images"]
                        image_urls.extend([
                            img.get("imageURL", {}).get("urlList", [None])[0]
                            for img in imgs if isinstance(img, dict)
                        ])
                    except Exception:
                        pass
            except Exception:
                pass
        if not image_urls:
            for line in html.split('"'):
                if line.startswith("https://") and any(e in line for e in (".jpg", ".jpeg", ".png", ".webp")):
                    image_urls.append(line)
        image_urls = list(dict.fromkeys([u for u in image_urls if u]))[:15]
        if not image_urls:
            return Fore.RED + "  ❌  No images found in this post." + Style.RESET_ALL
        saved = 0
        for i, img_url in enumerate(image_urls, 1):
            ext  = img_url.split(".")[-1].split("?")[0] or "jpg"
            path = os.path.join(folder, f"TT_slide_{str(i).zfill(3)}.{ext}")
            print(Fore.CYAN + f"  [{i}/{len(image_urls)}] Downloading slide..." + Style.RESET_ALL, end="\r")
            try:
                data = requests.get(img_url, timeout=10).content
                with open(path, "wb") as f:
                    f.write(data)
                trigger_media_scan(path)
                saved += 1
            except Exception:
                pass
        print()
        return Fore.GREEN + f"""
  ──────────────────────────────────────────
  ✅  Done
  Slides   : {saved} images
  Output   : {folder}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌  Slide download failed: {e}" + Style.RESET_ALL
