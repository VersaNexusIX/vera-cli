# VERA CLI — Architecture and Module Design

This document describes the internal structure of VERA CLI, the design decisions behind its modular architecture, and the responsibilities of each component.

---

## Table of Contents

- [System Overview](#system-overview)
- [Entry Point](#entry-point)
- [Command Dispatch](#command-dispatch)
- [Handler Modules](#handler-modules)
- [Utility Modules](#utility-modules)
- [Configuration Layer](#configuration-layer)
- [Data Flow](#data-flow)
- [Extending VERA CLI](#extending-vera-cli)

---

## System Overview

VERA CLI follows a flat, handler-based architecture. The entry point receives raw input, delegates parsing to a utility module, resolves the command name, and dispatches to the corresponding handler. Each handler is a self-contained module responsible for one domain of functionality.

```
User Input
    |
    v
cli.py  (parse, dispatch, print)
    |
    +-- parse_prompt()         utils/parse_prompt.py
    |
    +-- handler(args)          handlers/<module>.py
    |
    +-- vera_utils             utils/vera_utils.py
    |
    +-- config                 config.py
```

This design ensures that adding a new command requires only two steps: creating a handler module and registering it in the `COMMANDS` dictionary inside `cli.py`.

---

## Entry Point

**File:** `cli.py`

`cli.py` is responsible for:

- Initializing the terminal environment (colorama, screen clear, ASCII banner)
- Collecting the username at session start
- Running the main input loop (`cli_loop`)
- Parsing input via `parse_prompt`
- Resolving aliases
- Dispatching to the correct handler
- Displaying results
- Managing graceful exit

### Key Structures

```python
COMMANDS = {
    "tt":         tiktok,
    "yt":         yt,
    "weather":    cuaca,
    # ...
}

ALIASES = {
    "tiktok":    "tt",
    "youtube":   "yt",
    "cuaca":     "weather",
    # ...
}
```

### Command Resolution Order

1. Raw input is parsed into `{ "command": str, "args": list }`.
2. If the command matches `help` or `exit`, it is handled inline.
3. The command string is checked against `ALIASES` and replaced if matched.
4. The resolved command is looked up in `COMMANDS`.
5. If not found, a suggestion is generated from partial matches.
6. The loading animation runs, then the handler is called with `args`.

---

## Command Dispatch

**Function:** `process_command(text: str) -> str | None`

Returns a string to be printed to the terminal, or `None` to signal exit. All output formatting (color, spacing, borders) is handled within the handler itself using `colorama`.

Errors within handlers are caught at the dispatch layer and formatted consistently:

```
Error '<command>': <exception message>
```

Keyboard interrupts within a handler return a cancellation message rather than crashing the session.

---

## Handler Modules

All handler files reside in `handlers/`. Each module exposes a `handle(args: list) -> str` function (with the exception of `encode_decode.py`, which exposes `handle_encode` and `handle_decode` separately).

### Handler Contract

| Attribute | Requirement |
|---|---|
| Input | `args: list[str]` — tokenized arguments after the command name |
| Output | A formatted string, or `None` if no output is needed |
| Side effects | File writes, network calls, subprocess invocations |
| Error handling | Internal; returns a formatted error string rather than raising |

### Handler Inventory

| File | Command | External Dependency |
|---|---|---|
| `tiktok.py` | `tt` | yt-dlp, requests |
| `yt.py` | `yt` | yt-dlp |
| `spotify.py` | `sp` | yt-dlp, requests |
| `ig.py` | `ig` | yt-dlp |
| `fb.py` | `fb` | yt-dlp |
| `x.py` | `x` | yt-dlp |
| `pinterest.py` | `pin` | requests |
| `allmedia.py` | `am` | requests, RapidAPI |
| `gitclone.py` | `git` | subprocess (git) |
| `git_search.py` | `git_search` | requests (GitHub API) |
| `webfile.py` | `webfile` | requests, BeautifulSoup |
| `web_grab.py` | `webgrab` (grab) | requests |
| `web_scanner.py` | `webgrab` (scan) | requests, BeautifulSoup, socket |
| `cuaca.py` | `weather` | requests (OpenWeatherMap) |
| `anime.py` | `anime` | requests (Jikan API) |
| `osint_email.py` | `osint-mail` | requests (Gravatar, Hunter.io, DNS) |
| `sysinfo.py` | `sysinfo` | platform, os |
| `ipinfo.py` | `ipinfo` | requests (ipinfo.io) |
| `encode_decode.py` | `encode`, `decode` | base64, urllib |
| `hash_gen.py` | `hash` | hashlib |
| `quiz.py` | `quiz` | requests (Open Trivia DB, optional) |
| `tebak_angka.py` | `guest_number` | random |
| `ascii_gen.py` | `ascii` | pyfiglet |
| `botPersona.py` | `setpersona` | google-generativeai (optional) |
| `wa.py` | `wa` | selenium (optional) |

---

## Utility Modules

### `utils/parse_prompt.py`

Tokenizes raw user input into a structured prompt object:

```python
parse_prompt("yt https://youtu.be/xxx --visible")
# Returns: { "command": "yt", "args": ["https://youtu.be/xxx", "--visible"] }
```

Handles edge cases such as quoted strings and empty input.

---

### `utils/vera_utils.py`

Provides shared file management functions used by all downloader handlers:

| Function | Description |
|---|---|
| `get_download_path(subfolder)` | Resolves and creates the output directory |
| `get_next_filename(ext, prefix, folder)` | Returns a non-colliding filename (e.g., `YT_001.mp4`) |
| `trigger_media_scan(filepath)` | Broadcasts a media scan intent on Android via `am` |
| `move_to_public_and_scan(path, subfolder)` | Moves a file and triggers media scan |
| `human_size(nbytes)` | Converts bytes to a human-readable string |
| `is_termux()` | Returns `True` if running inside Termux |
| `sanitize_filename(name)` | Removes characters invalid in file names |

---

### `utils/anim.py`

Terminal animation utilities:

| Function | Description |
|---|---|
| `clear_screen()` | Clears the terminal |
| `loading_anim()` | Displays a brief loading animation |
| `exit_anim(username)` | Plays the exit animation and farewell message |

---

### `utils/ascii.py`

Renders the VERA ASCII banner to the terminal at session start using `pyfiglet`.

---

### `utils/banner.py`

Generates the welcome banner shown after the ASCII header.

---

### `utils/media_downloader.py`

Generic media download helper shared across handlers that perform direct HTTP file downloads.

---

## Configuration Layer

**File:** `config.py`

Centralizes all runtime configuration:

- Bot identity (`BOT` dict)
- API credentials (read from environment variables with fallback defaults)
- Download directory resolution (`get_download_dir()`)
- HTTP client parameters (`REQUEST_TIMEOUT`, `MAX_RETRIES`)

Handlers import directly from `config`:

```python
from config import DOWNLOAD_ROOT, REQUEST_TIMEOUT, HUNTER_API_KEY
```

---

## Data Flow

The following example traces the `yt https://youtu.be/xxx` command through the system:

```
1. User types:  yt https://youtu.be/xxx

2. cli_loop()   reads input, calls process_command()

3. parse_prompt()
       returns { "command": "yt", "args": ["https://youtu.be/xxx"] }

4. ALIASES check: "yt" not in ALIASES — no substitution

5. COMMANDS["yt"] resolves to handlers/yt.handle

6. loading_anim() plays

7. yt.handle(["https://youtu.be/xxx"]) is called
   |
   +-- validates URL
   +-- prompts user for format (MP3 / MP4)
   +-- calls get_download_path("VERA_YouTube")
   +-- calls get_next_filename("mp4", prefix="YT_", folder=...)
   +-- builds yt-dlp argument list
   +-- subprocess.run(yt-dlp args)
   +-- calls trigger_media_scan(filename)
   +-- returns formatted result string

8. cli_loop() prints the result string
```

---

## Extending VERA CLI

To add a new command:

**Step 1.** Create `handlers/myfeature.py`:

```python
from colorama import Fore, Style

def handle(args):
    if not args:
        return Fore.YELLOW + "  Format: myfeature <input>" + Style.RESET_ALL
    user_input = " ".join(args)
    # ... perform operation ...
    return Fore.GREEN + f"  Result: {user_input}" + Style.RESET_ALL
```

**Step 2.** Register in `cli.py`:

```python
from handlers.myfeature import handle as myfeature

COMMANDS = {
    # existing entries ...
    "myfeature": myfeature,
}
```

**Step 3.** Add an entry to `HELP_TEXT` in `cli.py` and to `assets/help.txt`.

**Step 4.** Document the command in `docs/COMMANDS.md`.

The handler will be fully integrated and accessible immediately on the next run.
