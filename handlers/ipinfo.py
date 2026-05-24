import requests
from colorama import Fore, Style
from config import REQUEST_TIMEOUT
def handle(args):
    ip       = args[0] if args else ""
    endpoint = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"
    try:
        data     = requests.get(endpoint, timeout=REQUEST_TIMEOUT).json()
        ip_addr  = data.get("ip", "?")
        city     = data.get("city", "?")
        region   = data.get("region", "?")
        country  = data.get("country", "?")
        org      = data.get("org", "?")
        timezone = data.get("timezone", "?")
        loc      = data.get("loc", "?")
        label    = "Your IP" if not args else f"IP : {ip_addr}"
        return Fore.CYAN + f"""
  🌐  {label}
  ──────────────────────────────────────────
  IP         : {ip_addr}
  City       : {city}
  Region     : {region}
  Country    : {country}
  ISP / Org  : {org}
  Timezone   : {timezone}
  Coordinates: {loc}
  Maps       : https://maps.google.com/?q={loc}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except requests.Timeout:
        return Fore.RED + "  ❌ Timeout." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ Error: {e}" + Style.RESET_ALL
