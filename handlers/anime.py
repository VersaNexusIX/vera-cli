import requests
from textwrap import shorten

def handle(args):
    if not args:
        return "⚠️ Enter the anime title. example: anime Naruto"

    query = " ".join(args)
    url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        if "data" not in data or len(data["data"]) == 0:
            return f"❌ Anime '{query}' cannot found "

        anime = data["data"][0]

        # Ambil data
        title = anime.get("title", "??")
        episodes = anime.get("episodes", "??")
        score = anime.get("score", "??")
        status = anime.get("status", "??")
        synopsis = anime.get("synopsis", "Tidak ada sinopsis.")
        url = anime.get("url", "")

        synopsis_short = shorten(synopsis, width=100, placeholder="...")

        # Format tabel
        table = f"""
╭───────────────────────────────
│ 📺 title     : {title}
│ 🎬 Episodes  : {episodes}
│ ⭐ Rating    : {score}
│ 📡 Status    : {status}
│ 📝 Sinopsis  : {synopsis_short}
│ 🔗 MAL       : {url}
╰───────────────────────────────
"""
        return table
    except Exception as e:
        return f"❌ Gagal ambil info anime: {str(e)}"