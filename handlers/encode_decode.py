import base64
import urllib.parse
from colorama import Fore, Style
def handle_encode(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: encode <method> <text>\n  Method : base64 | url | hex | rot13" + Style.RESET_ALL
    return _process(args, "encode")
def handle_decode(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: decode <method> <text>\n  Method : base64 | url | hex | rot13" + Style.RESET_ALL
    return _process(args, "decode")
def _process(args, direction):
    method = args[0].lower()
    text   = " ".join(args[1:])
    if not text:
        return Fore.YELLOW + f"  ⚠️  Format: {direction} {method} <text>" + Style.RESET_ALL
    try:
        if method == "base64":
            result = base64.b64encode(text.encode()).decode() if direction == "encode" else base64.b64decode(text).decode()
        elif method == "url":
            result = urllib.parse.quote(text) if direction == "encode" else urllib.parse.unquote(text)
        elif method == "hex":
            result = text.encode().hex() if direction == "encode" else bytes.fromhex(text).decode()
        elif method == "rot13":
            result = text.translate(str.maketrans(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"))
        else:
            return Fore.RED + f"  ❌ Unknown method '{method}'. Use: base64 | url | hex | rot13" + Style.RESET_ALL
        return Fore.CYAN + f"""
  🔤  {direction.capitalize()} — {method}
  ──────────────────────────────────────────
  Input    : {text[:70]}{'...' if len(text) > 70 else ''}
  Output   : {result}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ {direction.capitalize()} error: {e}" + Style.RESET_ALL
