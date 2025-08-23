import requests, os, json, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9"
}

EXTS = [".html", ".js", ".css", ".jpg", ".jpeg", ".png", ".pdf", ".mp4", ".zip", ".woff", ".ttf", "sql", "xlsx"]

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def download_webfiles(url, folder=None):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"❌ Gagal ambil HTML: {e}")
        return

    domain = urlparse(url).netloc.replace("www.", "")
    folder = folder or f"WEBHARVEST_{sanitize_filename(domain)}"
    save_dir = f"/storage/emulated/0/Download/{folder}"
    os.makedirs(save_dir, exist_ok=True)

    links = []
    for tag in soup.find_all(["a", "link", "script", "img"]):
        src = tag.get("href") or tag.get("src")
        if src:
            full_url = urljoin(url, src)
            if any(full_url.lower().endswith(ext) for ext in EXTS):
                links.append(full_url)

    log = []
    for link in links:
        try:
            res = requests.get(link, headers=HEADERS, timeout=15)
            fname = sanitize_filename(link.split("/")[-1].split("?")[0])
            path = os.path.join(save_dir, fname)
            with open(path, "wb") as f:
                f.write(res.content)
            log.append({
                "filename": fname,
                "url": link,
                "type": res.headers.get("Content-Type", "unknown"),
                "size_bytes": len(res.content),
                "status": "downloaded"
            })
        except Exception as e:
            log.append({
                "filename": link.split("/")[-1],
                "url": link,
                "type": "unknown",
                "size_bytes": 0,
                "status": f"failed: {str(e)}"
            })

    with open(os.path.join(save_dir, "harvest_log.json"), "w") as f:
        json.dump({"source_url": url, "files": log}, f, indent=2)

def handle(args):
    url = args.get("url")
    folder = args.get("folder")
    if url:
        download_webfiles(url, folder)
    else:
        print("❌ URL not provided.")