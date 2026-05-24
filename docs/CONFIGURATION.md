# VERA CLI — Configuration Guide

This document covers all configuration options available in VERA CLI, including API key setup, environment variables, and optional feature installation.

---

## Table of Contents

- [Configuration File](#configuration-file)
- [Environment Variables](#environment-variables)
- [API Keys](#api-keys)
- [Cookie Setup for YouTube](#cookie-setup-for-youtube)
- [Optional Features](#optional-features)
- [Download Directory](#download-directory)

---

## Configuration File

All core settings reside in `config.py` at the project root. This file is loaded at startup and controls API credentials, timeouts, and behavioral constants.

```python
# config.py (excerpt)

BOT = {
    "name":      "VERA AI",
    "version":   "1.0.0",
    "developer": "Versa NexusIX",
}

WEATHER_API_KEY = os.environ.get("OWM_API_KEY", "your_key_here")
HUNTER_API_KEY  = os.environ.get("HUNTER_API_KEY", "YOUR_HUNTER_KEY_HERE")
GEMINI_API_KEY  = os.environ.get("GEMINI_API_KEY", "")

REQUEST_TIMEOUT = 15   # seconds
MAX_RETRIES     = 3
```

It is strongly recommended to supply API keys via environment variables rather than editing `config.py` directly, to avoid committing credentials to version control.

---

## Environment Variables

Set the following variables in your shell profile (`.bashrc`, `.zshrc`, or Termux equivalent) to configure VERA CLI without modifying source files.

```bash
export OWM_API_KEY="your_openweathermap_api_key"
export HUNTER_API_KEY="your_hunter_io_api_key"
export RAPIDAPI_KEY="your_rapidapi_key"
export GEMINI_API_KEY="your_google_gemini_api_key"
```

Reload your shell after editing:

```bash
source ~/.bashrc
```

---

## API Keys

### OpenWeatherMap (Weather Command)

Used by the `weather` command to retrieve current weather data.

**Obtain a key:** https://openweathermap.org/api

**Variable:** `OWM_API_KEY`

The project includes a bundled default key for testing. Replace it with your own key for production or sustained use.

---

### Hunter.io (Email OSINT Command)

Used by `osint-mail` to verify email deliverability, scoring, and source attribution.

**Obtain a key:** https://hunter.io/

**Variable:** `HUNTER_API_KEY`

If this key is absent or left as the placeholder value `YOUR_HUNTER_KEY_HERE`, the Hunter.io section of the OSINT output is skipped. The command will still function with Gravatar and MX checks.

---

### RapidAPI — AllMedia (AllMedia Command)

Used by the `am` command to download from Instagram and Facebook via the AllMedia Downloader API.

**Obtain a key:** https://rapidapi.com/hub

**Subscribe to:** `allmedia-downloader` on RapidAPI

**Variable:** `RAPIDAPI_KEY`

This key is required for the `am` command to function. Without it, the command will fail with an authentication error.

---

### Google Gemini AI (Persona Feature)

Used to power AI-generated responses within the `setpersona` command and bot persona testing.

**Obtain a key:** https://aistudio.google.com/

**Variable:** `GEMINI_API_KEY`

This integration is optional and installed separately during setup. Without it, the persona feature operates in static mode.

---

## Cookie Setup for YouTube

YouTube applies bot-detection restrictions that can prevent downloads without authentication cookies. VERA CLI supports loading a `cookies.txt` file to authenticate requests automatically.

### How to Export Cookies

1. Open `youtube.com` in Chrome or Firefox while logged in.
2. Install the browser extension **"Get cookies.txt LOCALLY"**.
3. Click the extension icon and export cookies for `youtube.com`.
4. Save the exported file to `~/cookies.txt`.

### Verification

VERA CLI checks for `~/cookies.txt` at download time. If the file is found, it is passed to `yt-dlp` automatically:

```
Using cookies.txt
```

If the file is absent, a warning is displayed and the download proceeds without authentication.

The same `cookies.txt` applies to the `yt`, `ig`, `fb`, and `x` commands.

---

## Optional Features

The installer (`install.sh`) prompts for the following optional components:

### Deno (YouTube Bot-Check Bypass)

Deno is a JavaScript runtime used by `yt-dlp` to bypass YouTube's bot-check via the `--extractor-args "youtube:player_client=web"` method.

**Install during setup:** Select `[1] Yes` when prompted.

**Manual install (Termux):**

```bash
pkg install deno -y
```

---

### Selenium (WhatsApp Scraper)

Required for the `wa` command, which uses a headless browser to interact with WhatsApp Web.

**Install during setup:** Select `[1] Yes` when prompted.

**Manual install:**

```bash
pip install selenium
```

On Termux, Chromium must also be installed:

```bash
pkg install chromium -y
```

---

### Google Generative AI (Gemini Integration)

Required for AI-powered responses in the persona feature.

**Install during setup:** Select `[1] Yes` when prompted.

**Manual install:**

```bash
pip install google-generativeai
```

On Termux, native dependencies may need to be installed via `pkg`:

```bash
pkg install python-cryptography python-grpcio -y
```

---

## Download Directory

VERA CLI automatically detects the appropriate download directory for each platform:

| Platform | Default Path |
|---|---|
| Android (Termux) | `/storage/emulated/0/Download` |
| Linux | `~/Downloads` |
| macOS | `~/Downloads` |

Each downloader creates a subfolder within the download directory:

| Command | Subfolder |
|---|---|
| `tt` | `VERA_TikTok/` |
| `yt` | `VERA_YouTube/` |
| `ig`, `fb`, `x` | `VERA_<platform>/` |
| `webgrab` | `<domain_name>/` |

The download root can be verified at session start — VERA displays the resolved path in the welcome screen.

---

## Timeout and Retry Settings

| Parameter | Default | Description |
|---|---|---|
| `REQUEST_TIMEOUT` | 15 seconds | Maximum wait time per HTTP request |
| `MAX_RETRIES` | 3 | Number of retry attempts for yt-dlp |
| `LOADING_DOTS` | 3 | Number of dots in the loading animation |
| `LOADING_DELAY` | 0.35 seconds | Delay between animation frames |

These values can be modified in `config.py`.
