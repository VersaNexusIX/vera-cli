import os, subprocess
from colorama import Fore, Style
from yt_dlp import YoutubeDL
from utils.vera_utils import move_to_public_and_scan, trigger_media_scan

def handle(args):
    if not args:
        return Fore.YELLOW + "VERA : ⚠️ Masukkan link Spotify track."

    spotify_url = args[0]
    visible = "--visible" in args

    print(Fore.CYAN + """
VERA : Pilih jenis instalasi:
  1. 🎵 Install music
  2. 🖼️ Install picture (cover art)
  3. ❌ Cancel
""")

    choice = input(Fore.MAGENTA + "USER : ").strip()
    if choice == "3":
        return Fore.YELLOW + "VERA : ❌ Proses dibatalkan."

    download_dir = os.path.expanduser("~/Download/VERA_Spotify")
    os.makedirs(download_dir, exist_ok=True)

    try:
        track_id = spotify_url.split("/track/")[1].split("?")[0]
        search_query = f"ytsearch1:spotify track {track_id}"
    except:
        return Fore.RED + "VERA : ❌ Link Spotify tidak valid."

    if choice == "1":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(download_dir, "VERA_%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }
        ext = "mp3"
    elif choice == "2":
        ydl_opts = {
            "skip_download": True,
            "writethumbnail": True,
            "outtmpl": os.path.join(download_dir, "VERA_%(title)s.%(ext)s"),
            "quiet": True,
        }
        ext = "jpg"
    else:
        return Fore.YELLOW + "VERA : ⚠️ Pilihan tidak valid."

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            title = info.get("title", "Unknown")
            file_path = os.path.join(download_dir, f"VERA_{title}.{ext}")
            trigger_media_scan(file_path)
            if visible:
                move_to_public_and_scan(file_path, "Spotify")
            return Fore.GREEN + f"VERA : ✅ \"{title}\" berhasil diunduh ke: {file_path}"
    except Exception as e:
        return Fore.RED + f"VERA : ❌ Gagal unduh dari YouTube: {str(e)}"