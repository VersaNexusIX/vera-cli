import os
BOT = {
    "name": "VERA AI",
    "version": "1.0.0",
    "developer": "Versa NexusIX",
    "persona": (
        "VERA is a smart, fast, and versatile CLI assistant.\n"
        "Style: straight to the point, light humor, no fluff.\n"
        "Specialties: media download, light OSINT, developer tools."
    ),
}
def get_download_dir():
    candidates = [
        "/storage/emulated/0/Download",
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Download"),
    ]
    for path in candidates:
        if os.path.exists(os.path.dirname(path)):
            return path
    return os.path.join(os.path.expanduser("~"), "Downloads")
DOWNLOAD_ROOT = get_download_dir()
ALLMEDIA = {
    "base": "https://allmedia-downloader.p.rapidapi.com/insta-fb",
    "host": "allmedia-downloader.p.rapidapi.com",
    "key":  os.environ.get("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE"),
}
WEATHER_API_KEY = os.environ.get("OWM_API_KEY", "dd9d95480dea801e258ba226c7fdbc0d")
HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY", "YOUR_HUNTER_KEY_HERE")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
REQUEST_TIMEOUT = 15
MAX_RETRIES     = 3
LOADING_DOTS    = 3
LOADING_DELAY   = 0.35
