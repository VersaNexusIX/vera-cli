import os
import subprocess
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from utils.vera_utils import get_next_filename, trigger_media_scan, move_to_public_and_scan, get_download_path
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: pin <url> [--visible]" + Style.RESET_ALL
    url     = args[0]
    visible = "--visible" in args
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res  = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        vid  = soup.find("video")
        if not vid or not vid.get("src"):
            print(Fore.CYAN + "  🔄 Trying yt-dlp fallback..." + Style.RESET_ALL)
            return _ytdlp_fallback(url, visible)
        m3u8_url = vid["src"]
        print(Fore.CYAN + f"  🎥 Video stream found.")
        print(f"  🔗 URL: {m3u8_url[:60]}...")
        print("  Continue? [1] Yes  [2] Cancel" + Style.RESET_ALL)
        if input(Fore.MAGENTA + "  → " + Style.RESET_ALL).strip() != "1":
            return Fore.MAGENTA + "  ❎ Cancelled." + Style.RESET_ALL
        res       = requests.get(m3u8_url, headers=headers, timeout=15)
        lines     = res.text.splitlines()
        segments  = [l for l in lines if l and not l.startswith("#")]
        if not segments:
            return Fore.RED + "  ❌ No video segments found." + Style.RESET_ALL
        base_url    = m3u8_url.rsplit("/", 1)[0]
        work_dir    = get_download_path("VERA_Pinterest_tmp")
        seg_paths   = []
        for i, seg in enumerate(segments):
            seg_url = seg if seg.startswith("http") else f"{base_url}/{seg}"
            ts_path = os.path.join(work_dir, f"seg_{i:04}.ts")
            raw     = requests.get(seg_url, headers=headers, timeout=15).content
            with open(ts_path, "wb") as f:
                f.write(raw)
            seg_paths.append(ts_path)
            print(Fore.CYAN + f"  [{i+1}/{len(segments)}] Segment downloaded" + Style.RESET_ALL, end="\r")
        print()
        concat_file = os.path.join(work_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for p in seg_paths:
                f.write(f"file '{p}'\n")
        folder     = get_download_path("VERA_Pinterest")
        final_path = get_next_filename("mp4", prefix="PIN_", folder=folder)
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", concat_file, "-c", "copy", final_path],
            check=True, capture_output=True,
        )
        for p in seg_paths + [concat_file]:
            try: os.remove(p)
            except Exception: pass
        trigger_media_scan(final_path)
        if visible:
            move_to_public_and_scan(final_path, "Pinterest")
        return Fore.GREEN + f"  ✅ Saved → {final_path}" + Style.RESET_ALL
    except subprocess.CalledProcessError:
        return Fore.RED + "  ❌ ffmpeg merge failed. Is ffmpeg installed?" + Style.RESET_ALL
    except FileNotFoundError:
        return Fore.RED + "  ❌ ffmpeg not found. Install ffmpeg." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ Error: {e}" + Style.RESET_ALL
def _ytdlp_fallback(url: str, visible: bool) -> str:
    folder   = get_download_path("VERA_Pinterest")
    filename = get_next_filename("mp4", prefix="PIN_", folder=folder)
    try:
        subprocess.run(["yt-dlp", "-f", "mp4", "-o", filename, url], check=True)
        trigger_media_scan(filename)
        if visible:
            move_to_public_and_scan(filename, "Pinterest")
        return Fore.GREEN + f"  ✅ Saved → {filename}" + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ yt-dlp fallback failed: {e}" + Style.RESET_ALL
