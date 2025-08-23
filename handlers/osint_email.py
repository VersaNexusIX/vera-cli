import requests, hashlib
from colorama import Fore, Style

def handle(args):
    if not args:
        return Fore.YELLOW + "⚠️ Format: osint-email <email>" + Style.RESET_ALL
    email = args[0].strip()
    return osint_email_trace(email)

def osint_email_trace(email):
    results = []

    # Breach Check
    try:
        r = requests.get(f"https://haveibeenpwned.com/unifiedsearch/{email}", headers={
            "User-Agent": "VERA-OSINT"
        }, timeout=5)
        if r.status_code == 200:
            results.append(Fore.RED + "⚠️ Breach ditemukan di HaveIBeenPwned" + Style.RESET_ALL)
        elif r.status_code == 404:
            results.append(Fore.GREEN + "✅ Tidak ditemukan di breach publik" + Style.RESET_ALL)
    except:
        results.append(Fore.YELLOW + "⚠️ Gagal akses HaveIBeenPwned" + Style.RESET_ALL)

    # Hunter.io
    try:
        r = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=YOUR_API_KEY")
        data = r.json()
        if "data" in data:
            sources = data["data"].get("sources", [])
            if sources:
                results.append(Fore.CYAN + f"📌 Terdaftar di {len(sources)} situs:" + Style.RESET_ALL)
                for src in sources[:5]:
                    results.append("🔗 " + src.get("uri", "unknown"))
            else:
                results.append(Fore.YELLOW + "⚠️ Tidak ditemukan sumber publik via Hunter" + Style.RESET_ALL)
    except:
        results.append(Fore.YELLOW + "⚠️ Gagal akses Hunter API" + Style.RESET_ALL)

    # Gravatar
    hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{hash}?d=404"
    try:
        r = requests.get(gravatar_url, timeout=5)
        if r.status_code == 200:
            results.append(Fore.MAGENTA + "🧠 Email terhubung ke Gravatar profile" + Style.RESET_ALL)
    except:
        pass

    return "\n".join(results)