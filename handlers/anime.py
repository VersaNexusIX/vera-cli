import requests
from textwrap import shorten
from colorama import Fore, Style
from config import REQUEST_TIMEOUT
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: anime <title>" + Style.RESET_ALL
    query = " ".join(args)
    try:
        res   = requests.get(f"https://api.jikan.moe/v4/anime?q={query}&limit=3&sfw=true", timeout=REQUEST_TIMEOUT)
        items = res.json().get("data", [])
        if not items:
            return Fore.RED + f"  ❌ Anime '{query}' not found." + Style.RESET_ALL
        out = [Fore.CYAN + f"\n  🔍 Results: {query}"]
        for a in items[:3]:
            title    = a.get("title", "?")
            title_en = a.get("title_english") or ""
            eps      = a.get("episodes", "?")
            score    = a.get("score", "?")
            status   = a.get("status", "?")
            year     = a.get("year", "?")
            genres   = ", ".join(g["name"] for g in a.get("genres", [])[:4]) or "—"
            synopsis = shorten(a.get("synopsis") or "No synopsis available.", width=110, placeholder="...")
            url      = a.get("url", "")
            out.append(Fore.CYAN + f"""
  ──────────────────────────────────────────
  📺 Title    : {title}{f" ({title_en})" if title_en and title_en != title else ""}
  🎬 Episodes : {eps}   ⭐ Score : {score}   📅 Year : {year}
  📡 Status   : {status}
  🏷️  Genres   : {genres}
  📝 Synopsis : {synopsis}
  🔗 MAL      : {url}""" + Style.RESET_ALL)
        out.append(Fore.CYAN + "\n  ──────────────────────────────────────────" + Style.RESET_ALL)
        return "\n".join(out)
    except requests.Timeout:
        return Fore.RED + "  ❌ Timeout." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ Error: {e}" + Style.RESET_ALL
