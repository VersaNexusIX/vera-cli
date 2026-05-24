import os
import re
import time
import requests
from urllib.parse import urlparse
from colorama import Fore, Style
from config import ALLMEDIA, REQUEST_TIMEOUT
from utils.vera_utils import get_download_path, human_size
def _log(msg, level="info"):
    colors = {"info": Fore.BLUE, "success": Fore.GREEN, "error": Fore.RED, "warn": Fore.YELLOW}
    print(colors.get(level, Fore.WHITE) + f"  [AM] {msg}" + Style.RESET_ALL)
def _get_ext(url: str) -> str:
    url = url.lower()
    if ".mp4" in url:   return "mp4"
    if ".jpg" in url or ".jpeg" in url: return "jpg"
    if ".png" in url:   return "png"
    return "bin"
def _clean_url(raw: str) -> str:
    try:
        parsed = urlparse(raw)
        return parsed._replace(query="").geturl()
    except Exception:
        return raw
def _expand_url(url: str) -> str:
    try:
        r = requests.get(url, allow_redirects=False, timeout=5)
        if 300 <= r.status_code < 400:
            return r.headers.get("Location", url)
    except Exception:
        pass
    return url
def handle(args):
    if not args or not isinstance(args, list):
        _log("Usage: am <url>", "warn")
        return
    url = args[0]
    if not re.match(r"^https?://.+", url):
        _log("Invalid URL format.", "error")
        return
    if not all([ALLMEDIA.get("base"), ALLMEDIA.get("key"), ALLMEDIA.get("host")]):
        _log("AllMedia API not configured. Set RAPIDAPI_KEY in config.py or env.", "error")
        return
    expanded = _expand_url(url)
    cleaned  = _clean_url(expanded)
    if expanded != url:
        _log(f"Redirected → {expanded[:60]}", "info")
    try:
        res = requests.get(
            ALLMEDIA["base"],
            headers={
                "X-RapidAPI-Key":  ALLMEDIA["key"],
                "X-RapidAPI-Host": ALLMEDIA["host"],
            },
            params={"url": cleaned},
            timeout=REQUEST_TIMEOUT,
        )
        if res.status_code == 401:
            _log("Invalid RapidAPI key.", "error")
            return
        if res.status_code == 429:
            _log("Rate limit exceeded. Try again later.", "warn")
            return
        data       = res.json()
        media_list = data.get("media", [])
        if not isinstance(media_list, list) or not media_list:
            _log(f"No media found. API response: {str(data)[:100]}", "error")
            return
        ts     = int(time.time())
        folder = get_download_path("VERA_AllMedia")
        for i, media_url in enumerate(media_list):
            if not isinstance(media_url, str):
                continue
            ext       = _get_ext(media_url)
            fname     = f"AM_{ts}_{i:03}.{ext}"
            dest_path = os.path.join(folder, fname)
            _log(f"[{i+1}/{len(media_list)}] Downloading {fname}...", "info")
            try:
                with requests.get(media_url, stream=True, timeout=REQUEST_TIMEOUT) as r:
                    r.raise_for_status()
                    total = 0
                    with open(dest_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            total += len(chunk)
                _log(f"Saved → {dest_path}  ({human_size(total)})", "success")
            except Exception as e:
                _log(f"Failed [{i}]: {e}", "error")
    except Exception as e:
        _log(f"Request failed: {e}", "error")
