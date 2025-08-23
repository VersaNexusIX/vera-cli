import requests
from colorama import Fore, Style

API_KEY = "dd9d95480dea801e258ba226c7fdbc0d"  # Ganti dengan API dari https://openweathermap.org/api

def handle(args):
    if not args:
        return Fore.RED + "VERA : ⚠️ Format salah. Gunakan: cuaca <nama kota>" + Style.RESET_ALL

    kota = " ".join(args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={API_KEY}&units=metric&lang=id"

    try:
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            return Fore.RED + f"VERA : ❌ Kota '{kota}' tidak ditemukan." + Style.RESET_ALL

        nama_kota = data["name"]
        suhu = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        kondisi = data["weather"][0]["description"].capitalize()
        kelembapan = data["main"]["humidity"]
        angin = data["wind"]["speed"]
        awan = data["clouds"]["all"]

        return Fore.CYAN + f"""
VERA : 🌤️ Cuaca Saat Ini di {nama_kota}

  Suhu            : {suhu}°C (Terasa seperti {feels_like}°C)
  Kondisi         : {kondisi}
  Kelembapan      : {kelembapan}%
  Angin           : {angin} km/j
  Tutupan Awan    : {awan}%

Sumber: OpenWeatherMap
""" + Style.RESET_ALL

    except Exception as e:
        return Fore.RED + f"VERA : ⚠️ Gagal mengambil data cuaca. {str(e)}" + Style.RESET_ALL