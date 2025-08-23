# handlers/web_grab.py

from handlers.web_scanner import web_scan, auto_random_scan

def handle(args):
    """
    Usage:
      webgrab <url>
      webgrab --autorand [--attempts N]
    args: list of strings from CLI

    - Jika args[0] adalah '-a' atau '--autorand', maka jalankan auto_random_scan
      dengan jumlah percobaan (--attempts N) jika diberikan.
    - Selain itu, anggap args[0] adalah URL dan panggil web_scan(url).
    """
    if not args:
        print("❌ Usage: webgrab <url>  or  webgrab --autorand [--attempts N]")
        return

    # opsi autorand
    if args[0] in ("-a", "--autorand"):
        max_attempts = 100
        # cari opsi --attempts atau -n
        if len(args) >= 3 and args[1] in ("-n", "--attempts"):
            try:
                max_attempts = int(args[2])
            except ValueError:
                print(f"⚠️ Invalid attempt count '{args[2]}', menggunakan default {max_attempts}")
        auto_random_scan(max_attempts)
        return

    # scan satu URL
    url = args[0]
    web_scan(url)