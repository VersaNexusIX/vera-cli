import os, requests, subprocess
from bs4 import BeautifulSoup
from colorama import Fore, Style
from utils.vera_utils import get_next_filename, trigger_media_scan, move_to_public_and_scan

def handle(args):
    if not args:
        return Fore.YELLOW + "VERA : ⚠️ empty link."

    url = args[0]
    visible = "--visible" in args
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        video_tag = soup.find("video")

        if not video_tag or not video_tag.get("src"):
            return Fore.RED + "VERA : ❌ cannot found video MP4."

        m3u8_url = video_tag["src"]
        print(Fore.CYAN + "\nVERA : 🎥 Video found.")
        print("VERA : 🔗 URL:", m3u8_url)
        print("VERA : ❓ continue ?")
        print("   [1] Lanjut")
        print("   [2] Batal\n")

        choice = input(Fore.YELLOW + "VERA : Choose (1/2) ➤ ").strip()
        if choice != "1":
            return Fore.MAGENTA + "VERA : Cancelled by user."

        res = requests.get(m3u8_url, headers=headers)
        lines = res.text.splitlines()
        segment_urls = [line for line in lines if line and not line.startswith("#")]

        if not segment_urls:
            return Fore.RED + "VERA : ❌ cannot found video segment."

        base_url = m3u8_url.rsplit("/", 1)[0]
        download_dir = os.path.expanduser("~/Download/VERA_Pinterest")
        os.makedirs(download_dir, exist_ok=True)

        segment_paths = []
        for i, seg in enumerate(segment_urls):
            seg_url = f"{base_url}/{seg}" if not seg.startswith("http") else seg
            raw_path = os.path.join(download_dir, f"raw_{i:03}.bin")
            ts_path = os.path.join(download_dir, f"seg_{i:03}.ts")

            r = requests.get(seg_url, headers=headers)
            with open(raw_path, "wb") as f:
                f.write(r.content)

            subprocess.run([
                "ffmpeg", "-y", "-i", raw_path, "-c", "copy", ts_path
            ], check=True)

            segment_paths.append(ts_path)

        concat_list_path = os.path.join(download_dir, "concat.txt")
        with open(concat_list_path, "w") as f:
            for path in segment_paths:
                f.write(f"file '{path}'\n")

        final_path = get_next_filename("mp4", prefix="pinterest_", folder=download_dir)
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", concat_list_path, "-c", "copy", final_path
        ], check=True)

        trigger_media_scan(final_path)
        if visible:
            move_to_public_and_scan(final_path, "Pinterest")

        # Bersihkan segmen dan raw
        for path in segment_paths + [concat_list_path] + [p for p in os.listdir(download_dir) if p.startswith("raw_")]:
            try: os.remove(os.path.join(download_dir, path))
            except: pass

        return Fore.GREEN + f"VERA : ✅ File successfully merged to: {final_path}"
    except Exception as e:
        return Fore.RED + f"VERA : ❌ Failed to process fallback: {str(e)}"