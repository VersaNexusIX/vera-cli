import requests
from colorama import Fore, Style
import os
import subprocess
import re
import json

# === Photo Post Detector ===
def is_photo_post(url):
    return "/photo/" in url or "aweme_type=150" in url

# === Utility ===
def resolve_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.exceptions.RequestException:
        return url

def get_download_path():
    termux_path = "/storage/emulated/0/Download"
    if os.path.exists(termux_path):
        return termux_path
    return os.path.join(os.path.expanduser("~"), "Downloads")

def get_next_filename(extension, index=None):
    download_dir = get_download_path()
    prefix = "vera_"
    if index is not None:
        return os.path.join(download_dir, f"{prefix}{str(index).zfill(3)}.{extension}")

    existing = [
        f for f in os.listdir(download_dir)
        if f.startswith(prefix) and f.endswith(f".{extension}")
    ]
    numbers = []
    for name in existing:
        try:
            num = int(name[len(prefix):-len(f".{extension}")])
            numbers.append(num)
        except:
            continue
    next_num = max(numbers, default=0) + 1
    return os.path.join(download_dir, f"{prefix}{str(next_num).zfill(3)}.{extension}")

def trigger_media_scan(filepath):
    try:
        subprocess.run([
            "am", "broadcast",
            "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
            "-d", f"file://{filepath}"
        ], check=True)
    except:
        pass

def move_to_public_and_scan(local_path, branded_name):
    public_dir = f"/sdcard/Download/VERA_{branded_name}"
    os.makedirs(public_dir, exist_ok=True)
    public_path = os.path.join(public_dir, os.path.basename(local_path))

    try:
        os.rename(local_path, public_path)
        trigger_media_scan(public_path)
        print(Fore.GREEN + f"VERA : ✅ File moved to: {public_path}")
        print("VERA : 📂 The file is now accessible." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"VERA : ❌ Gagal pindah/scan: {str(e)}" + Style.RESET_ALL)

# === Format Prompt ===
def prompt_format(url):
    print(Fore.YELLOW + "VERA : choose the format" + Style.RESET_ALL)
    if "/music/" in url:
        print("  1. 🎧 Audio (.mp3) [Indihome Style]")
        return "mp3"
    print("  1. 🎥 Video (.mp4)")
    print("  2. 🎧 Audio (.mp3)")
    print("  3. 🖼️  Thumbnail (.jpg)")
    print("  4. 🖼️  Slide (multi-image)")
    choice = input(Fore.MAGENTA + "Format [1/2/3/4] : " + Style.RESET_ALL).strip()
    format_map = {
        "1": "mp4",
        "2": "mp3",
        "3": "jpg",
        "4": "slide"
    }
    return format_map.get(choice, "mp4")

# === Slide Downloader ===
def download_slide_images(url):
    print(Fore.CYAN + "VERA :  detect Photo Post..." + Style.RESET_ALL)
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        html = res.text

        match = re.search(r'window\.__UNIVERSAL_DATA__\s*=\s*(\{.*?\});', html)
        image_urls = []

        if match:
            try:
                data = json.loads(match.group(1))
                for k in data:
                    try:
                        imgs = data[k]["props"]["pageProps"]["itemInfo"]["itemStruct"]["images"]
                        image_urls.extend(imgs)
                    except:
                        continue
            except:
                pass

        if not image_urls:
            for line in html.split('"'):
                if "https://" in line and (".jpg" in line or ".jpeg" in line or ".png" in line):
                    image_urls.append(line)

        image_urls = list(set(image_urls))[:10]

        if not image_urls:
            return Fore.RED + "VERA : cannot found" + Style.RESET_ALL

        for i, img_url in enumerate(image_urls, start=1):
            ext = img_url.split('.')[-1].split('?')[0]
            filepath = get_next_filename(ext, i)
            print(Fore.CYAN + f"VERA : installing slide {i}: {filepath}" + Style.RESET_ALL)
            with open(filepath, 'wb') as f:
                f.write(requests.get(img_url).content)
            trigger_media_scan(filepath)

        return Fore.GREEN + f"VERA : {len(image_urls)} Image saved to downloads folder." + Style.RESET_ALL

    except Exception as e:
        return Fore.RED + f"VERA : Download failed: {str(e)}" + Style.RESET_ALL

def yt_dlp_download(url, format_choice):
    if format_choice in ["jpg", "slide"] and is_photo_post(url):
        return download_slide_images(url)

    filename = get_next_filename(format_choice)
    ytdlp_args = ["yt-dlp", "-o", filename]

    if format_choice == "mp4":
        ytdlp_args += ["-f", "mp4"]
    elif format_choice == "mp3":
        ytdlp_args += ["-x", "--audio-format", "mp3"]
    elif format_choice == "jpg":
        ytdlp_args += ["--skip-download", "--write-thumbnail"]
    else:
        return Fore.RED + "VERA : Unrecognized format" + Style.RESET_ALL

    ytdlp_args.append(url)

    print(Fore.CYAN + f"VERA : intalling {format_choice.upper()} ke: {filename}" + Style.RESET_ALL)

    try:
        subprocess.run(ytdlp_args, check=True)
        trigger_media_scan(filename)
        return Fore.GREEN + f"VERA : saved to: {filename}" + Style.RESET_ALL, filename
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"VERA : failed: {str(e)}" + Style.RESET_ALL, None

# === Main Handler ===
def handle(args):
    if not args:
        return Fore.YELLOW + "VERA : URL not yet provided." + Style.RESET_ALL

    original_url = args[0]
    visible = "--visible" in args

    print(Fore.CYAN + "VERA : Resolving redirect link..." + Style.RESET_ALL)
    final_url = resolve_redirect(original_url)

    format_choice = prompt_format(final_url)
    result, filepath = yt_dlp_download(final_url, format_choice)

    if visible and filepath:
        move_to_public_and_scan(filepath, "TikTok")

    return result