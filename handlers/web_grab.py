from handlers.web_scanner import web_scan, auto_random_scan
def handle(args):
    if not args:
        print("❌ Usage: webgrab <url>  or  webgrab --autorand [--attempts N]")
        return
    if args[0] in ("-a", "--autorand"):
        max_attempts = 100
        if len(args) >= 3 and args[1] in ("-n", "--attempts"):
            try:
                max_attempts = int(args[2])
            except ValueError:
                print(f"⚠️ Invalid attempt count '{args[2]}', using default {max_attempts}")
        auto_random_scan(max_attempts)
        return
    url = args[0]
    web_scan(url)
