from colorama import Fore, Style
from config import BOT

def bot_persona(args):
    try:
        query = " ".join(args).strip()

        if not query:
            return Fore.YELLOW + f"👋 Halo, gue {BOT['name']}. Ketik sesuatu biar gue jawab sesuai gaya persona gw!\nContoh: vera siapa kamu" + Style.RESET_ALL

        persona_lines = "\n".join(f"  {line}" for line in BOT["persona"].split("\n"))

        reply = f"""
====================================
🤖 {BOT['name']} - Persona Mode
====================================
{Style.DIM}{persona_lines}{Style.RESET_ALL}

📩 Pertanyaan lo:
{Fore.CYAN}"{query}"{Style.RESET_ALL}

💬 Jawaban gw:
Wok, gue {BOT['name']}. Gaya gue? Liat di atas. Tapi intinya, gue siap nemenin lo ngobrol, bantu, atau ngasih jawaban yang sesuai vibe lo. Gaskeun.
====================================
""".strip()

        return reply

    except Exception as err:
        return Fore.RED + f"❌ Error di bot_persona: {str(err)}" + Style.RESET_ALL

# === CLI Wrapper ===
def handle(args):
    output = bot_persona(args)
    print(output)