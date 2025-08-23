# VERA CLI v0.0.3

A modular command-line interface for automation, media parsing, and multi-platform bot integration.  
Developed by Versa NexusIX (David) — solo developer and systems architect.

---

## 📌 Overview

VERA CLI is a Python-based system designed for:

- Media downloading (YouTube, TikTok, Pinterest)
- Telegram bot integration
- Flexible prompt parsing
- WhatsApp profile scanning
- ASCII generation
- Weather, quiz, anime, and persona handlers

Each module is built for stable input parsing and final output without ambiguity.

---

## ⚙️ Features

- Modular handler system (`handlers/`)
- ASCII banner generator (`utils/ascii.py`)
- Prompt parser with auto-flatten logic (`utils/parse_prompt.py`)
- Multi-format downloader (mp4, mp3, jpg)
- WhatsApp profile scanner (`wa <number>`)
- Telegram bot support (v20+)
- Quiz engine and weather handler
- Persona tuning for bot identity

---

## 📁 Folder Structure
cli.py
handlers/
  ├── yt.py
  ├── tt.py
  ├── wa.py
  ├── vera.py
  ├── weather.py
  ├── quiz.py
  └── ...
utils/
  ├── ascii.py
  ├── anim.py
  ├── parse_prompt.py
assets/
  └── help.txt

---

## 🛠️ Installation

### Termux / Linux

```bash
pkg install python git
git clone https://github.com/yourusername/vera-cli
cd vera-cli
pip install -r requirements.txt
python cli.py


---
## Example command

vera Hello, who are you?     # Chat with VERA
yt https://youtu.be/...      # Download YouTube video
tt https://vm.tiktok.com/... # Download TikTok video
wa 6281234567890             # Scan WhatsApp profile image
ascii Hello World            # Generate ASCII art
weather Jakarta              # Get weather info
quiz                         # Start quiz engine
persona VERA                 # Set bot persona
help                         # Show command list
exit                         # Exit CLI

