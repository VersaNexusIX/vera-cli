import os
import re
import time
import requests
from urllib.parse import urlparse
from colorama import Fore, Style
from config import ALLMEDIA  # Pastikan config.py sudah ada

# === Branding Banner ===
def banner(msg, type='info'):
    prefix = {
        'info': Fore.BLUE + '[AM]',
        'success': Fore.GREEN + '[AM]',
        'error': Fore.RED + '[AM]'
    }.get(type, Fore.WHITE + '[AM]')
    print(f"{prefix} {msg}{Style.RESET_ALL}")

# === Ekstensi Detektor ===
def get_extension(url):
    url = url.lower()
    if '.mp4' in url:
        return '.mp4'
    if '.jpg' in url or '.jpeg' in url:
        return '.jpg'
    if '.png' in url:
        return '.png'
    return '.bin'

# === Expand Redirect URL ===
def expand_url(short_url):
    try:
        res = requests.get(short_url, allow_redirects=False)
        if 300 <= res.status_code < 400:
            return res.headers.get('Location', short_url)
    except Exception:
        pass
    return short_url

# === Bersihin URL ===
def clean_url(raw):
    try:
        parsed = urlparse(raw)
        cleaned = parsed._replace(query='').geturl()
        return cleaned
    except Exception:
        return raw

# === Main Handler ===
def download_allmedia(url):
    if not re.match(r'^https?://.+', url):
        banner("URL tidak valid.", "error")
        return

    if not ALLMEDIA.get("base") or not ALLMEDIA.get("key") or not ALLMEDIA.get("host"):
        banner("Konfigurasi AllMedia tidak lengkap. Cek config.py.", "error")
        return

    expanded = expand_url(url)
    cleaned = clean_url(expanded)

    if expanded != url:
        banner(f"🔁 URL diperluas: {expanded}", "info")
    if cleaned != expanded:
        banner(f"🧼 URL dibersihkan: {cleaned}", "info")

    try:
        res = requests.get(ALLMEDIA["base"], headers={
            "X-RapidAPI-Key": ALLMEDIA["key"],
            "X-RapidAPI-Host": ALLMEDIA["host"]
        }, params={"url": cleaned})

        data = res.json()
        media_list = data.get("media", [])

        if not isinstance(media_list, list) or not media_list:
            banner("Tidak ada media ditemukan dari API.", "error")
            return

        timestamp = int(time.time())

        for i, media_url in enumerate(media_list):
            if not isinstance(media_url, str):
                banner(f"⚠️ Media ke-{i} tidak valid. Lewat.", "error")
                continue

            ext = get_extension(media_url)
            file_name = f"am_{timestamp}_{i}{ext}"
            download_path = os.path.join("/storage/emulated/0/Download", file_name)

            banner(f"📥 Mengunduh: {file_name}", "info")

            try:
                with requests.get(media_url, stream=True) as r:
                    r.raise_for_status()
                    with open(download_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                banner(f"✅ Disimpan di: {download_path}", "success")
            except Exception as e:
                banner(f"❌ Gagal unduh media ke-{i}: {str(e)}", "error")

    except Exception as err:
        msg = getattr(err, 'response', None)
        if msg and hasattr(msg, 'text'):
            banner(f"Gagal download: {msg.text}", "error")
        else:
            banner(f"Gagal download: {str(err)}", "error")
            
            # === CLI Handler Wrapper ===
def handle(args):
    if not args or not isinstance(args, list):
        banner("Argumen kosong atau tidak valid.", "error")
        return

    url = args[0]
    download_allmedia(url)