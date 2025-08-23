import os
import requests
from urllib.parse import urlparse

def download_all_media(url, platform):
    # Simulasi universal downloader
    # Di real case, pakai API atau scraping engine
    filename = generate_filename(url, platform)
    ext = detect_extension(url)

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()

        path = f"downloads/{filename}.{ext}"
        os.makedirs("downloads", exist_ok=True)

        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        return f"✅ Berhasil unduh: {path}"
    except Exception as e:
        raise RuntimeError(f"Download gagal: {str(e)}")

def generate_filename(url, platform):
    parsed = urlparse(url)
    base = os.path.basename(parsed.path).split("?")[0]
    return f"{platform}_{base or 'media'}"

def detect_extension(url):
    if ".mp4" in url:
        return "mp4"
    elif ".jpg" in url or ".jpeg" in url:
        return "jpg"
    elif ".png" in url:
        return "png"
    else:
        return "bin"