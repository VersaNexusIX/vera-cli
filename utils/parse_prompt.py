KNOWN_COMMANDS = {
    "tt", "am", "sp", "yt", "weather", "help", "exit",
    "setpersona", "pin", "quiz", "ig", "fb", "x", "git",
    "ascii", "osint-mail", "anime", "guest_number",
    "webfile", "webgrab", "git_search", "wa", "sysinfo",
    "ipinfo", "hash", "encode", "decode",
}
def parse_prompt(input_str: str) -> dict:
    input_str = input_str.strip()
    if not input_str:
        return {"command": None, "args": []}
    tokens = _tokenize(input_str)
    if not tokens:
        return {"command": None, "args": []}
    first = tokens[0].lower()
    if first in KNOWN_COMMANDS:
        return {"command": first, "args": tokens[1:]}
    return {"command": first, "args": tokens[1:]}
def _tokenize(text: str) -> list[str]:
    import shlex
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()
