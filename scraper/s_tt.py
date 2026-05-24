import sys
import requests
import re
import os
def banner(msg, type="info"):
    prefix = {
        "info": "[TT]",
        "success": "[TT]",
        "error": "[TT]"
    }.get(type, "[TT]")
    print(f"{prefix} {msg}")
def extract_video_url(page):
    match = re.search(r'"downloadAddr":"(.*?)"', page)
    if match:
        return match.group(1).replace("\\u0026", "&").replace("\\", "")
    return None
def download_video(video_url, filename):
    try:
        r = requests.get(video_url, stream=True)
        path = f"/storage/emulated/0/Download/{filename}"
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        banner(f"✅ Saved at: {path}", "success")
    except Exception as e:
        banner(f"❌ Download failed: {str(e)}", "error")
def main():
    if len(sys.argv) < 2:
        banner("Usage: python tiktok_scraper.py <link>", "error")
        return
    url = sys.argv[1]
    banner(f"🔗 Fetching TikTok: {url}", "info")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers)
        video_url = extract_video_url(res.text)
        if not video_url:
            banner("❌ Failed to find video.", "error")
            return
        filename = f"tt_{int(os.path.getmtime(__file__))}.mp4"
        banner(f"📥 Downloading: {filename}", "info")
        download_video(video_url, filename)
    except Exception as e:
        banner(f"❌ Error: {str(e)}", "error")
if __name__ == "__main__":
    main()
