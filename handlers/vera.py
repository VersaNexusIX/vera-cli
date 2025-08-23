import requests
from colorama import Fore, Style

API_KEY = "AIzaSyBTOkrK0VnW8o_kGvo3L8B7J0Y6eXKuHOg"  # Dapatkan dari Google AI Studio
MODEL = "gemini-2.5-flash"

# Persona default
persona = {
    "name": "VERA",
    "style": "cerdas di bidang sains computer",
    "tone": "legacy spiritual",
    "origin": "berada di CLI termux buatan Versa NexusIX",  # ✅ key → value
}

def set_persona(args):
    global persona
    if len(args) < 2:
        return Fore.YELLOW + "VERA : ⚠️ Format salah. Gunakan: setpersona <key> <value>" + Style.RESET_ALL

    key = args[0]
    value = " ".join(args[1:])
    persona[key] = value
    return Fore.GREEN + f"VERA : ✅ Persona '{key}' di-set ke '{value}'" + Style.RESET_ALL

def handle(args):
    if not args:
        return Fore.RED + "VERA : ⚠️ Prompt kosong. Gunakan: vera <prompt>" + Style.RESET_ALL

    prompt = " ".join(args)
    full_prompt = f"""
Kamu adalah {persona['name']}, AI dengan gaya {persona['style']}.
Nada bicaramu {persona['tone']}, {persona['origin']}.
Jawab prompt berikut dengan gaya tersebut:

Prompt: {prompt}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}]
    }

    try:
        res = requests.post(url, json=payload)
        data = res.json()
        output = data["candidates"][0]["content"]["parts"][0]["text"]
        return Fore.CYAN + f"\nVERA : {output}" + Style.RESET_ALL

    except Exception as e:
        return Fore.RED + f"VERA : ⚠️ Gagal memanggil Gemini. {str(e)}" + Style.RESET_ALL