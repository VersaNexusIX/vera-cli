import requests
from bs4 import BeautifulSoup
import random

def fetch_brilio_riddle():
    url = "https://www.brilio.net/ragam/140-pertanyaan-teka-teki-lucu-menjebak-2025-bikin-ketawa-guling-guling-250728q.html"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        raw = soup.get_text(separator="\n")

        # Ambil baris yang mengandung pola soal
        lines = [line.strip() for line in raw.split("\n") if line.strip()]
        riddles = []
        for i in range(len(lines)):
            if lines[i].startswith(tuple(str(n) + "." for n in range(1, 200))):
                q = lines[i].split(".", 1)[1].strip()
                if i + 1 < len(lines) and "Jawaban:" in lines[i + 1]:
                    a = lines[i + 1].split("Jawaban:", 1)[1].strip()
                    riddles.append((q, a))

        if not riddles:
            return "⚠️ Gagal parsing soal dari Brilio. Gunakan soal lokal."

        question, answer = random.choice(riddles)
        print(f"[Teka-Teki Online] {question}")
        user = input("Jawaban: ")
        return "✅ Benar." if user.strip().lower() == answer.lower() else f"❌ Salah. Jawaban: {answer}"
    except Exception as e:
        return f"❌ Error ambil soal online: {str(e)}"

# === CLI Handler ===
def handle(args):
    if not args:
        return "⚠️ Format: quiz <online>"
    mode = args[0].lower()
    if mode == "online":
        return fetch_brilio_riddle()
    else:
        return "⚠️ Mode quiz tidak dikenali. Gunakan 'online'."