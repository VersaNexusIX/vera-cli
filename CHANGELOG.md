# Changelog

All notable changes to VERA CLI are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Version numbering follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2025-08-24

### Added

**Core System**
- Interactive CLI session with username prompt and welcome screen
- Modular command dispatcher with alias resolution and partial-match suggestions
- ASCII banner renderer using `pyfiglet`
- Loading animation and graceful exit animation
- Global `--visible` flag for all downloader commands (moves file to public folder and triggers media scan on Android)

**Downloaders**
- `tt` — TikTok downloader supporting video (MP4), audio (MP3), thumbnail (JPG), and slide (multi-image) formats
- `yt` — YouTube downloader supporting MP4 and MP3 via `yt-dlp`
- `sp` — Spotify track downloader (MP3 and cover art)
- `ig` — Instagram downloader via `yt-dlp`
- `fb` — Facebook video downloader via `yt-dlp`
- `x` — X (Twitter) video downloader via `yt-dlp`
- `pin` — Pinterest video downloader
- `am` — AllMedia downloader for Instagram and Facebook via RapidAPI

**Developer Tools**
- `git` — Git repository clone
- `git_search` — GitHub repository search
- `webfile` — Web file scraper and downloader
- `webgrab` — Comprehensive web scanner with port scanning, admin path detection, and file extraction

**Information and OSINT**
- `weather` — Current weather via OpenWeatherMap API
- `anime` — Anime information via MyAnimeList (Jikan API)
- `osint-mail` — Email OSINT combining Gravatar, Hunter.io, and DNS MX validation
- `sysinfo` — System information display (OS, CPU, memory, disk)
- `ipinfo` — IP geolocation via ipinfo.io

**Encoding and Cryptography**
- `encode` / `decode` — Text encoding and decoding (Base64, URL, Hex, ROT13)
- `hash` — Hash generation (MD5, SHA-1, SHA-256, SHA-512, or all)

**Games and Utilities**
- `quiz` — Trivia quiz engine with local and online (Open Trivia Database) modes
- `guest_number` — Number guessing game with easy and hard difficulty
- `ascii` — ASCII art generator

**System**
- `setpersona` — Bot persona viewer and Gemini AI tester
- `help` — In-terminal command reference

**Installation**
- `install.sh` — Automated installer with Termux and Linux/macOS support
- Optional installation prompts for Deno, Selenium, and Google Gemini AI
- `cookies.txt` detection and setup guidance during installation

**Documentation**
- `README.md` — Project overview, installation guide, and feature summary
- `docs/COMMANDS.md` — Full command reference with syntax and examples
- `docs/CONFIGURATION.md` — API key setup and environment configuration guide
- `docs/ARCHITECTURE.md` — Module structure and system design documentation
- `docs/CONTRIBUTING.md` — Contribution guidelines
- `CHANGELOG.md` — This file

---

## Planned for [1.1.0]

- WhatsApp scraper (`wa`) — stable Selenium integration
- Gemini AI chat mode — persistent conversation context
- Download progress bar for large files
- Command history with up-arrow recall
- Unit test suite for handler modules
