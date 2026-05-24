import hashlib
import re
import requests
from colorama import Fore, Style
from config import HUNTER_API_KEY, REQUEST_TIMEOUT
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: osint-mail <email>" + Style.RESET_ALL
    email = args[0].strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Fore.RED + "  ❌ Invalid email format." + Style.RESET_ALL
    return _scan(email)
def _scan(email):
    md5    = hashlib.md5(email.encode()).hexdigest()
    domain = email.split("@")[1]
    lines  = [Fore.CYAN + f"\n  🔍  OSINT Email : {email}",
              Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL]
    try:
        r = requests.get(f"https://www.gravatar.com/avatar/{md5}?d=404", timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            lines.append(Fore.GREEN + f"  Gravatar   : ✅ Found")
            lines.append(Fore.WHITE  + f"               https://www.gravatar.com/avatar/{md5}" + Style.RESET_ALL)
        else:
            lines.append(Fore.WHITE  + "  Gravatar   : Not found" + Style.RESET_ALL)
    except Exception:
        lines.append(Fore.YELLOW + "  Gravatar   : Timeout" + Style.RESET_ALL)
    if HUNTER_API_KEY and HUNTER_API_KEY != "YOUR_HUNTER_KEY_HERE":
        try:
            r    = requests.get(
                f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}",
                timeout=REQUEST_TIMEOUT)
            data = r.json().get("data", {})
            status  = data.get("status", "unknown")
            score   = data.get("score", "?")
            sources = data.get("sources", [])
            lines.append(Fore.CYAN + f"  Hunter.io  : {status}  (score: {score})" + Style.RESET_ALL)
            for src in sources[:3]:
                lines.append(Fore.WHITE + f"               • {src.get('uri','')}" + Style.RESET_ALL)
        except Exception as e:
            lines.append(Fore.YELLOW + f"  Hunter.io  : Error ({e})" + Style.RESET_ALL)
    else:
        lines.append(Fore.DIM + "  Hunter.io  : API key not configured" + Style.RESET_ALL)
    try:
        r    = requests.get(f"https://dns.google/resolve?name={domain}&type=MX", timeout=REQUEST_TIMEOUT)
        mx_ok = bool(r.json().get("Answer"))
        color = Fore.GREEN if mx_ok else Fore.YELLOW
        lines.append(color + f"  Domain     : {domain}  →  {'MX valid ✅' if mx_ok else 'No MX record ⚠️'}" + Style.RESET_ALL)
    except Exception:
        lines.append(Fore.WHITE + f"  Domain     : {domain}" + Style.RESET_ALL)
    lines.append(Fore.WHITE  + f"  MD5 Hash   : {md5}" + Style.RESET_ALL)
    lines.append(Fore.CYAN   + "  ──────────────────────────────────────────\n" + Style.RESET_ALL)
    return "\n".join(lines)
