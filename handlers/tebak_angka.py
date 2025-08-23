import random
from colorama import Fore, Style

def handle(args):
    target = random.randint(1, 50)
    attempts = 5

    print(Fore.CYAN + "\n Guess a number from 1 to 50")
    print(f" You have {attempts} Chance\n" + Style.RESET_ALL)

    for i in range(1, attempts + 1):
        try:
            guess = int(input(f" Guess-{i}: "))
        except ValueError:
            print(Fore.YELLOW + "⚠ Enter a valid number" + Style.RESET_ALL)
            continue

        if guess == target:
            return Fore.GREEN + f" The numbers are {target}" + Style.RESET_ALL
        elif abs(guess - target) <= 3:
            print(Fore.MAGENTA + " Just a little bit more" + Style.RESET_ALL)
        elif guess < target:
            print(Fore.BLUE + " Too small" + Style.RESET_ALL)
        else:
            print(Fore.RED + " Too big" + Style.RESET_ALL)

    return Fore.RED + f"\n Failed, the correct number is: {target}" + Style.RESET_ALL