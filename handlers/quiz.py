import random
import requests
from colorama import Fore, Style
from config import REQUEST_TIMEOUT
LOCAL_TRIVIA = [
    ("Capital of Indonesia?", "jakarta"),
    ("Largest planet in the solar system?", "jupiter"),
    ("What is 7 × 8?", "56"),
    ("Who invented the telephone?", "alexander graham bell"),
    ("How many sides does a triangle have?", "3"),
    ("Colors of the Indonesian flag?", "red white"),
    ("Programming language created by Guido van Rossum?", "python"),
    ("Year Indonesia gained independence?", "1945"),
    ("Process by which plants make their own food?", "photosynthesis"),
    ("Largest island in Indonesia?", "kalimantan"),
]
RIDDLES = [
    ("I have hands but cannot shake yours. What am I?", "clock"),
    ("The more you fill me, the lighter I get. What am I?", "balloon"),
    ("I have an eye but cannot see. What am I?", "needle"),
    ("The older I get, the higher I go. What am I?", "age"),
]
def handle(args):
    mode = args[0].lower() if args else "local"
    if mode == "online":
        return _online()
    elif mode in ("local", "trivia"):
        return _local_trivia()
    elif mode == "riddle":
        return _local_riddle()
    return Fore.YELLOW + "  ⚠️  Mode: quiz local | quiz trivia | quiz online | quiz riddle" + Style.RESET_ALL
def _local_trivia():
    q, a = random.choice(LOCAL_TRIVIA)
    print(Fore.CYAN + f"\n  ❓  Question")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(Fore.WHITE + f"  {q}" + Style.RESET_ALL)
    user = input(Fore.MAGENTA + "  Answer : " + Style.RESET_ALL).strip().lower()
    print(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
    if user == a.lower():
        return Fore.GREEN + "  ✅  Correct!\n" + Style.RESET_ALL
    return Fore.RED + f"  ❌  Wrong. Answer : {a.title()}\n" + Style.RESET_ALL
def _local_riddle():
    q, a = random.choice(RIDDLES)
    print(Fore.CYAN + f"\n  🧩  Riddle")
    print(Fore.CYAN + "  ──────────────────────────────────────────")
    print(Fore.WHITE + f"  {q}" + Style.RESET_ALL)
    user = input(Fore.MAGENTA + "  Answer : " + Style.RESET_ALL).strip().lower()
    print(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
    if user == a:
        return Fore.GREEN + "  ✅  Correct!\n" + Style.RESET_ALL
    return Fore.RED + f"  ❌  Wrong. Answer : {a.title()}\n" + Style.RESET_ALL
def _online():
    try:
        r    = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=REQUEST_TIMEOUT)
        item = r.json().get("results", [])[0]
        question = item["question"]
        correct  = item["correct_answer"]
        options  = item["incorrect_answers"] + [correct]
        random.shuffle(options)
        print(Fore.CYAN + "\n  ❓  Online Trivia")
        print(Fore.CYAN + "  ──────────────────────────────────────────")
        print(Fore.WHITE + f"  {question}" + Style.RESET_ALL)
        for i, opt in enumerate(options, 1):
            print(Fore.WHITE + f"  [{i}] {opt}" + Style.RESET_ALL)
        print(Fore.CYAN + "  ──────────────────────────────────────────" + Style.RESET_ALL)
        try:
            choice = int(input(Fore.MAGENTA + "  Choice : " + Style.RESET_ALL).strip())
            chosen = options[choice - 1]
        except (ValueError, IndexError):
            return Fore.RED + "  ❌  Invalid choice." + Style.RESET_ALL
        if chosen == correct:
            return Fore.GREEN + "  ✅  Correct!\n" + Style.RESET_ALL
        return Fore.RED + f"  ❌  Wrong. Answer : {correct}\n" + Style.RESET_ALL
    except Exception:
        return _local_trivia()
