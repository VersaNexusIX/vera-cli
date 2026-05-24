import requests
from colorama import Fore, Style
from config import REQUEST_TIMEOUT
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: git_search <keyword>" + Style.RESET_ALL
    keyword = " ".join(args)
    url     = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page=5"
    try:
        r = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=REQUEST_TIMEOUT)
        if r.status_code == 403:
            return Fore.YELLOW + "  ⚠️  GitHub rate limit. Try again in 60 seconds." + Style.RESET_ALL
        if r.status_code != 200:
            return Fore.RED + f"  ❌ GitHub API error ({r.status_code})" + Style.RESET_ALL
        repos = r.json().get("items", [])
        if not repos:
            return Fore.YELLOW + f"  No repositories found for '{keyword}'" + Style.RESET_ALL
        lines = [Fore.CYAN + f"\n  🔍  GitHub : {keyword}"]
        for repo in repos:
            name  = repo["full_name"]
            stars = repo["stargazers_count"]
            forks = repo["forks_count"]
            lang  = repo.get("language") or "—"
            desc  = (repo.get("description") or "—")[:80]
            link  = repo["html_url"]
            upd   = repo.get("updated_at", "")[:10]
            lines.append(Fore.CYAN + f"""
  ──────────────────────────────────────────
  Repo       : {name}
  ⭐ Stars   : {stars:,}   🍴 Forks : {forks:,}   💬 {lang}
  Updated    : {upd}
  Description: {desc}
  URL        : {link}""" + Style.RESET_ALL)
        lines.append(Fore.CYAN + "\n  ──────────────────────────────────────────" + Style.RESET_ALL)
        return "\n".join(lines)
    except requests.Timeout:
        return Fore.RED + "  ❌ Timeout." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ Error: {e}" + Style.RESET_ALL
