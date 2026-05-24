#!/bin/bash
set -e
echo ""
echo "  ██╗   ██╗███████╗██████╗  █████╗"
echo "  ██║   ██║██╔════╝██╔══██╗██╔══██╗"
echo "  ██║   ██║█████╗  ██████╔╝███████║"
echo "  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██║"
echo "   ╚████╔╝ ███████╗██║  ██║██║  ██║"
echo "    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝"
echo ""
echo "  ──────────────────────────────────"
echo "  VERA CLI Installer v1.0.0"
echo "  ──────────────────────────────────"
echo ""
IS_TERMUX=false
if [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
    echo "  [*] Termux detected"
else
    echo "  [*] Linux/macOS detected"
fi
echo ""
if $IS_TERMUX; then
    echo "  ──────────────────────────────────"
    echo "  [*] Update package list..."
    echo "  ──────────────────────────────────"
    pkg update -y -q
    echo "  [*] Install: python git ffmpeg..."
    pkg install -y -q python git ffmpeg 2>/dev/null || true
    echo "  [*] Install native Python libs via pkg..."
    echo "      (cryptography, lxml, grpcio — require compiler if via pip)"
    pkg install -y -q python-cryptography 2>/dev/null || true
    pkg install -y -q python-lxml         2>/dev/null || true
    echo ""
    echo "  ──────────────────────────────────"
    echo "  [?] Install deno? (JS runtime to bypass YouTube bot-check)"
    echo "  [1] Yes   [2] No"
    echo "  ──────────────────────────────────"
    read -r deno_choice
    if [ "$deno_choice" = "1" ]; then
        pkg install -y -q deno 2>/dev/null \
            || echo "  [!] deno not available in this repo — skipping"
    fi
else
    echo "  [*] Checking dependencies..."
    for dep in python3 git ffmpeg; do
        which "$dep" >/dev/null 2>&1 \
            && echo "  [+] $dep found" \
            || echo "  [!] $dep not found — install manually"
    done
fi
echo ""
echo "  ──────────────────────────────────"
echo "  [*] Install Python packages..."
echo "  ──────────────────────────────────"
pip install --upgrade pip -q 2>/dev/null || true
pip install -r requirements.txt -q
echo ""
echo "  ──────────────────────────────────"
echo "  [?] Install selenium? (for 'wa' feature — WhatsApp scraper)"
echo "  [1] Yes   [2] No (skip)"
echo "  ──────────────────────────────────"
read -r sel_choice
if [ "$sel_choice" = "1" ]; then
    if $IS_TERMUX; then
        pkg install -y -q chromium 2>/dev/null || echo "  [!] chromium skipped"
    fi
    pip install selenium -q 2>/dev/null || echo "  [!] selenium failed — skipping"
fi
echo ""
echo "  ──────────────────────────────────"
echo "  [?] Install Google Gemini AI? (for AI chat feature)"
echo "  [1] Yes   [2] No (skip)"
echo "  ──────────────────────────────────"
read -r ai_choice
if [ "$ai_choice" = "1" ]; then
    if $IS_TERMUX; then
        pkg install -y -q python-cryptography python-grpcio 2>/dev/null || true
    fi
    pip install google-generativeai -q 2>/dev/null \
        || echo "  [!] google-generativeai failed — skipping"
fi
echo ""
echo "  ──────────────────────────────────"
echo "  [*] Setting up cookies.txt for YouTube bot-check bypass"
echo "  ──────────────────────────────────"
COOKIES_PATH="$HOME/cookies.txt"
if [ -f "$COOKIES_PATH" ]; then
    echo "  [+] cookies.txt already exists at $COOKIES_PATH"
else
    echo "  [!] cookies.txt not found"
    echo ""
    echo "  How to get cookies.txt:"
    echo "  1. Open YouTube in Chrome/Firefox"
    echo "  2. Install extension: 'Get cookies.txt LOCALLY'"
    echo "  3. Export cookies from youtube.com"
    echo "  4. Place the file at: $COOKIES_PATH"
    echo ""
    echo "  Without cookies.txt, YouTube downloads may be blocked."
fi
mkdir -p assets
echo ""
echo "  ──────────────────────────────────"
echo "  ✅  Installation complete!"
echo "  ──────────────────────────────────"
echo ""
echo "  ▶  Run : python3 cli.py"
echo ""
echo "  📌  cookies.txt tip:"
echo "      Place it at ~/cookies.txt"
echo "      All downloaders will use it automatically"
echo ""
