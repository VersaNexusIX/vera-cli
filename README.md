<!-- Logo -->
<p align="center">
  <img src="Img/vera_versa.png" alt="vera-cli logo" width="200"/>
</p>

<h2 align="center">VERA CLI I</h2>

A modular command-line interface for automation, media parsing, and multi-platform bot integration.  
Developed by Versa NexusIX (David) — solo developer and systems architect.

---

## 📌 Overview

VERA CLI is a Python-based system designed for:

- Media downloading (YouTube, TikTok, Pinterest)
- Flexible prompt parsing
- ASCII generation
- Weather, quiz, anime, and persona handlers

Each module is built for stable input parsing and final output without ambiguity.


---


<p align="center">
  <img src="Img/Screenshot_20250824-054902.jpg" alt="Img/Screenshot_20250824-054902.jpg" width="600"/>
</p>


---


## ⚙️ Features

- Modular handler system (`handlers/`)
- ASCII banner generator (`utils/ascii.py`)
- Prompt parser with auto-flatten logic (`utils/parse_prompt.py`)
- Multi-format downloader (mp4, mp3, jpg)
- Quiz engine and weather handler
- Persona tuning for bot identity

---

## 📁 Folder Structure

```bash
vera-cli/
├── cli.py
├── handlers/
│   ├── yt.py
│   ├── tt.py
│   ├── weather.py
│   ├── quiz.py
│   └── ~~
├── utils/
│   ├── ascii.py
│   ├── anim.py
│   └── ~~
├── assets/
│   └── help.txt
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

### Termux

```
pkg install git -y
pkg install python -y
pkg install python3 -y
git clone https://github.com/VersaNexusIX/vera-cli.git
cd vera-cli
bash install.sh
python3 cli.py
```

### Run after Exit

```
cd vera-cli
python3 cli.py
```

---


## Example command

```
yt https://youtu.be/...      # Download YouTube video
tt https://vm.tiktok.com/... # Download TikTok video
ascii Hello World            # Generate ASCII art
cuaca Jakarta                # Get weather info
quiz                         # Start quiz engine
help                         # Show command list
exit                         # Exit CLI
```