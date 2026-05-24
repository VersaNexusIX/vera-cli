import hashlib
from colorama import Fore, Style
def handle(args):
    if not args:
        return Fore.YELLOW + "  ⚠️  Format: hash <text> [--algo md5|sha1|sha256|sha512|all]" + Style.RESET_ALL
    algo = "sha256"
    text_parts = []
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False
            continue
        if a == "--algo" and i + 1 < len(args):
            algo = args[i + 1].lower()
            skip = True
        else:
            text_parts.append(a)
    text = " ".join(text_parts)
    if not text:
        return Fore.YELLOW + "  ⚠️  Text cannot be empty." + Style.RESET_ALL
    algorithms = {
        "md5":    hashlib.md5,
        "sha1":   hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    if algo == "all":
        lines = [Fore.CYAN + f"\n  🔑  Hash — all algorithms",
                 Fore.CYAN + "  ──────────────────────────────────────────",
                 Fore.WHITE + f"  Input    : {text[:60]}{'...' if len(text)>60 else ''}" + Style.RESET_ALL]
        for name, fn in algorithms.items():
            h = fn(text.encode()).hexdigest()
            lines.append(Fore.CYAN + f"  {name.upper():<8} : " + Fore.WHITE + h + Style.RESET_ALL)
        lines.append(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
        return "\n".join(lines)
    fn = algorithms.get(algo)
    if not fn:
        return Fore.RED + f"  ❌ Unknown algo '{algo}'. Use: md5 | sha1 | sha256 | sha512 | all" + Style.RESET_ALL
    h = fn(text.encode()).hexdigest()
    return Fore.CYAN + f"""
  🔑  Hash — {algo.upper()}
  ──────────────────────────────────────────
  Input     : {text[:60]}{'...' if len(text)>60 else ''}
  Hash      : {h}
  Algorithm : {algo.upper()}
  ──────────────────────────────────────────
""" + Style.RESET_ALL
