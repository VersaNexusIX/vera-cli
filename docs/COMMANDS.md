# VERA CLI — Command Reference

This document provides a complete reference for all commands available in VERA CLI v1.0.0.

---

## Table of Contents

- [Downloaders](#downloaders)
- [Developer Tools](#developer-tools)
- [Information and OSINT](#information-and-osint)
- [Encoding and Cryptography](#encoding-and-cryptography)
- [Games and Utilities](#games-and-utilities)
- [System Commands](#system-commands)
- [Global Options](#global-options)
- [Command Aliases](#command-aliases)

---

## Downloaders

### `tt` — TikTok Downloader

Downloads video, audio, or slide images from TikTok.

**Syntax**

```
tt <url> [--visible]
```

**Format Selection**

Upon execution, VERA presents a format menu:

```
[1]  Video (MP4)
[2]  Audio (MP3)
[3]  Thumbnail (JPG)
[4]  Slide (multi-image)
[5]  Cancel
```

For music posts (`/music/` URL), only MP3 and Cancel are presented.

**Output path:** `Downloads/VERA_TikTok/`

**Examples**

```
tt https://vm.tiktok.com/ZMxxxxxxxx/
tt https://www.tiktok.com/@user/video/123456789 --visible
```

---

### `yt` — YouTube Downloader

Downloads video or audio from YouTube.

**Syntax**

```
yt <url> [--visible]
```

**Format Selection**

```
[1]  Audio (MP3)
[2]  Video (MP4)
[3]  Cancel
```

**Output path:** `Downloads/VERA_YouTube/`

**Cookie Support**

If `~/cookies.txt` is present, it is used automatically to bypass bot-check. Without it, YouTube may block the request.

**Examples**

```
yt https://youtu.be/dQw4w9WgXcQ
yt https://www.youtube.com/watch?v=dQw4w9WgXcQ --visible
```

---

### `sp` — Spotify Downloader

Downloads a Spotify track as MP3 or retrieves cover art.

**Syntax**

```
sp <spotify_url>
```

**Examples**

```
sp https://open.spotify.com/track/xxxxxxxxxxxxxxxxxxxxxxxx
```

---

### `ig` — Instagram Downloader

Downloads media from Instagram via yt-dlp.

**Syntax**

```
ig <url> [--visible]
```

**Examples**

```
ig https://www.instagram.com/p/xxxxxxxx/
```

---

### `fb` — Facebook Downloader

Downloads video from Facebook via yt-dlp.

**Syntax**

```
fb <url> [--visible]
```

**Examples**

```
fb https://www.facebook.com/watch?v=123456789
```

---

### `x` — X (Twitter) Downloader

Downloads video from X (formerly Twitter) via yt-dlp.

**Syntax**

```
x <url> [--visible]
```

**Aliases:** `twit`, `twitter`

**Examples**

```
x https://twitter.com/user/status/123456789012345678
```

---

### `pin` — Pinterest Downloader

Downloads video from Pinterest.

**Syntax**

```
pin <url>
```

**Examples**

```
pin https://www.pinterest.com/pin/123456789/
```

---

### `am` — AllMedia Downloader

Downloads from Instagram or Facebook using the AllMedia API via RapidAPI. Requires `RAPIDAPI_KEY` to be configured.

**Syntax**

```
am <url>
```

**Examples**

```
am https://www.instagram.com/p/xxxxxxxx/
am https://www.facebook.com/watch?v=123456789
```

---

## Developer Tools

### `git` — Repository Clone

Clones a Git repository to the local machine.

**Syntax**

```
git <repository_url>
```

**Examples**

```
git https://github.com/username/repository.git
```

---

### `git_search` — GitHub Repository Search

Searches GitHub for public repositories matching a keyword.

**Syntax**

```
git_search <keyword>
```

**Aliases:** `github`

**Examples**

```
git_search vera-cli
git_search python automation
```

---

### `webfile` — Web File Scraper

Scrapes a web page and downloads linked files (PDF, images, archives, etc.).

**Syntax**

```
webfile <url>
```

**Examples**

```
webfile https://example.com/resources
```

---

### `webgrab` — Web Scanner and File Grabber

Performs a comprehensive web scan: crawls the target URL, identifies linked assets (SQL, XLSX, JSON, PHP), probes admin paths, scans common ports, and downloads discovered files.

**Syntax**

```
webgrab <url>
```

**Output path:** `Downloads/<domain_name>/`

**Discovered file types:** `.sql`, `.xlsx`, `.json`, `.php`

**Examples**

```
webgrab https://example.com
```

---

## Information and OSINT

### `weather` — Current Weather

Retrieves current weather data for a given city using the OpenWeatherMap API.

**Syntax**

```
weather <city>
```

**Aliases:** `cuaca`, `w`

**Examples**

```
weather Jakarta
weather New York
```

---

### `anime` — Anime Information

Searches for anime information via the MyAnimeList API.

**Syntax**

```
anime <title>
```

**Examples**

```
anime Attack on Titan
anime Naruto
```

---

### `osint-mail` — Email OSINT

Performs an OSINT scan on an email address. Checks Gravatar profile, Hunter.io verification, and MX record validity.

**Syntax**

```
osint-mail <email>
```

**Output includes:**

- Gravatar profile existence
- Hunter.io verification status and score (requires `HUNTER_API_KEY`)
- Domain MX record validation
- MD5 hash of the email address

**Examples**

```
osint-mail user@example.com
```

---

### `sysinfo` — System Information

Displays current system information including OS, CPU, memory, and disk usage.

**Syntax**

```
sysinfo
```

---

### `ipinfo` — IP Geolocation

Retrieves geolocation data for an IP address. If no IP is provided, returns data for the current machine's public IP.

**Syntax**

```
ipinfo [ip_address]
```

**Output includes:** IP, city, region, country, ISP, timezone, coordinates, and a Google Maps link.

**Examples**

```
ipinfo
ipinfo 8.8.8.8
```

---

## Encoding and Cryptography

### `encode` — Text Encoding

Encodes text using the specified method.

**Syntax**

```
encode <method> <text>
```

**Supported methods:**

| Method | Description |
|---|---|
| `base64` | Base64 encoding |
| `url` | URL percent-encoding |
| `hex` | Hexadecimal encoding |
| `rot13` | ROT13 substitution cipher |

**Examples**

```
encode base64 Hello World
encode hex secret text
encode url https://example.com/path?q=hello world
```

---

### `decode` — Text Decoding

Decodes text using the specified method.

**Syntax**

```
decode <method> <text>
```

**Supported methods:** `base64`, `url`, `hex`, `rot13`

**Examples**

```
decode base64 SGVsbG8gV29ybGQ=
decode hex 48656c6c6f
```

---

### `hash` — Hash Generation

Generates a cryptographic hash of the provided text.

**Syntax**

```
hash <text> [--algo <algorithm>]
```

**Supported algorithms:**

| Algorithm | Flag |
|---|---|
| SHA-256 | `--algo sha256` (default) |
| MD5 | `--algo md5` |
| SHA-1 | `--algo sha1` |
| SHA-512 | `--algo sha512` |
| All algorithms | `--algo all` |

**Examples**

```
hash password123
hash password123 --algo md5
hash password123 --algo all
```

---

## Games and Utilities

### `quiz` — Trivia Quiz

Starts an interactive trivia quiz session.

**Syntax**

```
quiz [local|online]
```

| Mode | Description |
|---|---|
| `local` | Uses bundled question set |
| `online` | Fetches questions from the Open Trivia Database |

**Examples**

```
quiz
quiz online
quiz local
```

---

### `guest_number` — Number Guessing Game

Interactive number guessing game. The player guesses a number between 1 and 50.

**Syntax**

```
guest_number [easy|hard]
```

**Examples**

```
guest_number
guest_number hard
```

---

### `ascii` — ASCII Art Generator

Generates ASCII art from the provided text using the pyfiglet library.

**Syntax**

```
ascii <text>
```

**Examples**

```
ascii Hello World
ascii VERA
```

---

## System Commands

### `setpersona` — Bot Persona

Displays or tests the current VERA bot persona configuration.

**Syntax**

```
setpersona [query]
```

**Examples**

```
setpersona
setpersona What can you do?
```

---

### `help` — Help Menu

Displays the in-terminal command reference.

**Syntax**

```
help
?
```

---

### `exit` — Exit

Terminates the VERA CLI session.

**Syntax**

```
exit
quit
q
```

---

## Global Options

### `--visible`

Applicable to all downloader commands (`tt`, `yt`, `ig`, `fb`, `x`). Moves the downloaded file to the public Downloads folder and triggers a media scan (on Termux/Android).

**Example**

```
yt https://youtu.be/dQw4w9WgXcQ --visible
tt https://vm.tiktok.com/ZMxxxxxxxx/ --visible
```

---

## Command Aliases

The following aliases are accepted in place of their primary command:

| Alias | Maps to |
|---|---|
| `tiktok` | `tt` |
| `youtube` | `yt` |
| `insta` | `ig` |
| `instagram` | `ig` |
| `twit` | `x` |
| `twitter` | `x` |
| `github` | `git_search` |
| `cuaca` | `weather` |
| `w` | `weather` |
