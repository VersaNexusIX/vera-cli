# VERA CLI — Troubleshooting Guide

This document addresses common issues encountered when installing or running VERA CLI, along with their recommended solutions.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [YouTube Download Issues](#youtube-download-issues)
- [TikTok Download Issues](#tiktok-download-issues)
- [AllMedia Download Issues](#allmedia-download-issues)
- [Weather and OSINT Issues](#weather-and-osint-issues)
- [Encoding and Hash Issues](#encoding-and-hash-issues)
- [General CLI Issues](#general-cli-issues)

---

## Installation Issues

### Python not found

**Symptom:** `python3: command not found`

**Solution:**

On Termux:
```bash
pkg install python -y
```

On Linux:
```bash
sudo apt install python3 python3-pip -y
```

On macOS:
```bash
brew install python3
```

---

### pip install fails with permission error

**Symptom:** `Permission denied` or `ERROR: Could not install packages`

**Solution:** Do not use `sudo pip` on Termux. Use the standard user install:

```bash
pip install -r requirements.txt
```

If the issue persists, upgrade pip first:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### `colorama` or `pyfiglet` not found after install

**Symptom:** `ModuleNotFoundError: No module named 'colorama'`

**Solution:** Confirm you are running `python3` (not `python2`) and that you installed requirements with the same interpreter:

```bash
python3 -m pip install -r requirements.txt
python3 cli.py
```

---

### `ffmpeg` not found

**Symptom:** `yt-dlp` completes but produces no audio in MP4, or MP3 extraction fails.

**Solution:**

On Termux:
```bash
pkg install ffmpeg -y
```

On Linux:
```bash
sudo apt install ffmpeg -y
```

On macOS:
```bash
brew install ffmpeg
```

---

## YouTube Download Issues

### Download fails with "Sign in to confirm you are not a bot"

**Cause:** YouTube has flagged the request as automated.

**Solution:** Set up `cookies.txt`:

1. Open `youtube.com` in Chrome or Firefox while logged in.
2. Install the **"Get cookies.txt LOCALLY"** browser extension.
3. Export cookies for `youtube.com`.
4. Save the file to `~/cookies.txt`.

VERA CLI detects this file automatically and passes it to `yt-dlp`.

---

### Download fails with HTTP 403

**Cause:** The YouTube video is region-restricted, age-restricted, or member-only.

**Solution:** Ensure `cookies.txt` is from an account that has access to the video. Age-restricted content requires a logged-in session.

---

### `yt-dlp not found`

**Symptom:** `Error 'yt': yt-dlp not found. Install: pip install yt-dlp`

**Solution:**

```bash
pip install yt-dlp
```

Or update if already installed:

```bash
pip install --upgrade yt-dlp
```

---

### Downloaded MP4 has no audio

**Cause:** `ffmpeg` is not installed. `yt-dlp` requires `ffmpeg` to merge separate video and audio streams.

**Solution:** Install `ffmpeg` (see Installation Issues above).

---

## TikTok Download Issues

### Slide download finds no images

**Symptom:** `No images found in this post.`

**Cause:** TikTok's HTML structure for carousel posts changes periodically.

**Solution:** This is a known limitation. Update `yt-dlp` to the latest version:

```bash
pip install --upgrade yt-dlp
```

If the issue persists, use a direct video URL rather than a short link.

---

### Redirect resolution fails

**Symptom:** The resolved URL is the same as the input short link.

**Cause:** TikTok's redirect service is temporarily unavailable.

**Solution:** Paste the full TikTok URL directly instead of a `vm.tiktok.com` short link.

---

## AllMedia Download Issues

### Authentication error

**Symptom:** `401 Unauthorized` or no output from the `am` command.

**Cause:** `RAPIDAPI_KEY` is not set or is set to the placeholder value.

**Solution:** Obtain a valid RapidAPI key and set it as an environment variable:

```bash
export RAPIDAPI_KEY="your_actual_api_key"
```

Or update `config.py` directly:

```python
ALLMEDKEY = {
    "key": "your_actual_api_key",
    ...
}
```

---

## Weather and OSINT Issues

### Weather returns no data or an error

**Symptom:** `Error: 401` or empty response from the `weather` command.

**Cause:** The default bundled API key may have been revoked or rate-limited.

**Solution:** Register at https://openweathermap.org/api and set your own key:

```bash
export OWM_API_KEY="your_openweathermap_api_key"
```

---

### `osint-mail` shows "API key not configured" for Hunter.io

**Symptom:** The Hunter.io section of the OSINT output is skipped.

**Cause:** `HUNTER_API_KEY` is absent or set to the placeholder value.

**Solution:** Register at https://hunter.io/ and set the key:

```bash
export HUNTER_API_KEY="your_hunter_io_api_key"
```

The command will still function for Gravatar and MX record checks without this key.

---

### `ipinfo` returns a timeout

**Symptom:** `Timeout.`

**Cause:** The `ipinfo.io` service is temporarily unavailable or the request exceeded `REQUEST_TIMEOUT`.

**Solution:** Increase the timeout in `config.py`:

```python
REQUEST_TIMEOUT = 30
```

---

## Encoding and Hash Issues

### `decode base64` raises an error

**Symptom:** `Decode error: Incorrect padding`

**Cause:** The input Base64 string is malformed or has been truncated.

**Solution:** Ensure the input is a complete, properly padded Base64 string. Base64 strings must have a length divisible by 4. Missing padding characters (`=`) may need to be appended manually.

---

### `decode hex` raises an error

**Symptom:** `Decode error: non-hexadecimal number found in fromhex()`

**Cause:** The input contains characters outside the hexadecimal range (0-9, a-f, A-F), such as spaces or line breaks.

**Solution:** Remove all non-hex characters from the input before decoding.

---

## General CLI Issues

### Terminal output appears garbled or lacks color

**Cause:** The terminal does not support ANSI escape codes, or `colorama` initialization failed.

**Solution:** On Windows, ensure you are using Windows Terminal or a compatible emulator. On Termux, color support is enabled by default.

If the issue persists, set the `NO_COLOR` environment variable to disable color output:

```bash
export NO_COLOR=1
python3 cli.py
```

---

### Command not found despite being listed in `help`

**Symptom:** `Unknown command '<name>'.`

**Cause:** The alias may differ from what was typed.

**Solution:** Run `help` to view the exact command names and aliases. Note that `cuaca` is an alias for `weather`, and `guest_number` (not `guess_number`) is the correct command name.

---

### `webgrab` scan takes very long

**Cause:** `webgrab` crawls up to 100 pages and scans the top 100 ports of the target host. On slow connections or responsive targets, this can take several minutes.

**Solution:** This is expected behavior. Press `Ctrl+C` to interrupt the scan at any time. A partial summary will not be displayed — restart the command if a full scan is needed.

---

If an issue is not covered here, open a GitHub issue with the details described in the [Reporting Issues](CONTRIBUTING.md#reporting-issues) section.
