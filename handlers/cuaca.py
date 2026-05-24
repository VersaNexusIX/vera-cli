import requests
from colorama import Fore, Style
from config import WEATHER_API_KEY, REQUEST_TIMEOUT
WEATHER_EMOJI = {
    "clear": "☀️", "clouds": "☁️", "rain": "🌧️",
    "drizzle": "🌦️", "thunderstorm": "⛈️", "snow": "❄️",
    "mist": "🌫️", "fog": "🌫️", "haze": "🌫️",
}
def handle(args):
    if not args:
        return Fore.RED + "  ⚠️  Format: weather <city>" + Style.RESET_ALL
    city = " ".join(args)
    url  = (f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=en")
    try:
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        if data.get("cod") != 200:
            return Fore.RED + f"  ❌ City '{city}' not found." + Style.RESET_ALL
        name       = data["name"]
        country    = data["sys"]["country"]
        temp       = data["main"]["temp"]
        feels      = data["main"]["feels_like"]
        tmin       = data["main"]["temp_min"]
        tmax       = data["main"]["temp_max"]
        condition  = data["weather"][0]["description"].capitalize()
        main_w     = data["weather"][0]["main"].lower()
        humidity   = data["main"]["humidity"]
        wind       = data["wind"]["speed"]
        wind_deg   = data["wind"].get("deg", 0)
        clouds     = data["clouds"]["all"]
        visibility = data.get("visibility", 0) // 1000
        emoji      = WEATHER_EMOJI.get(main_w, "🌡️")
        return Fore.CYAN + f"""
  {emoji}  Weather — {name}, {country}
  ──────────────────────────────────────────
  Temperature : {temp}°C  (feels like {feels}°C)
  Range       : {tmin}°C – {tmax}°C
  Condition   : {condition}
  Humidity    : {humidity}%
  Wind        : {wind} m/s  ({_wind_dir(wind_deg)})
  Cloud cover : {clouds}%
  Visibility  : {visibility} km
  ──────────────────────────────────────────
""" + Style.RESET_ALL
    except requests.Timeout:
        return Fore.RED + "  ❌ Request timeout." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  ❌ Error: {e}" + Style.RESET_ALL
def _wind_dir(deg):
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[int((deg + 22.5) / 45) % 8]
