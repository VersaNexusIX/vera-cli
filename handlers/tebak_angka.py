import random
from colorama import Fore, Style
def handle(args):
    difficulty = args[0].lower() if args else "normal"
    cfg = {
        "easy":   (1, 20,  7),
        "normal": (1, 50,  5),
        "hard":   (1, 100, 4),
    }.get(difficulty, (1, 50, 5))
    low, high, attempts = cfg
    target = random.randint(low, high)
    print(Fore.CYAN + f"""
  🎮  Number Guessing Game
  ──────────────────────────────────────────
  Range      : {low} – {high}
  Attempts   : {attempts}x
  Difficulty : {difficulty.capitalize()}
  ──────────────────────────────────────────""" + Style.RESET_ALL)
    for i in range(1, attempts + 1):
        try:
            guess = int(input(Fore.MAGENTA + f"  Guess [{i}/{attempts}] : " + Style.RESET_ALL))
        except ValueError:
            print(Fore.YELLOW + "  ⚠️  Enter a number." + Style.RESET_ALL)
            continue
        if guess == target:
            return Fore.GREEN + f"\n  🎉  Correct! The number was {target}.\n" + Style.RESET_ALL
        remaining = attempts - i
        diff      = abs(guess - target)
        hint      = "🔥 Almost!" if diff <= 3 else ("👍 Getting closer..." if diff <= 10 else "❄️  Way off.")
        direction = "⬆️  Too low" if guess < target else "⬇️  Too high"
        if remaining > 0:
            print(Fore.YELLOW + f"  {direction}  —  {hint}  ({remaining} attempts left)" + Style.RESET_ALL)
    return Fore.RED + f"\n  😢  Game over! The answer was : {target}.\n" + Style.RESET_ALL
