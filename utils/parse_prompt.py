known_commands = [
    "tt",
    "am",
    "sp", 
    "vera",
    "yt", 
    "cuaca",
    "help", 
    "exit", 
    "pers", 
    "setpersona", 
    "pin", 
    "quiz",
    "ig", 
    "fb", 
    "x", 
    "git", 
    "ascii", 
    "osint-mail", 
    "anime", 
    "tebak angka", 
    "webfile", 
    "webgrab", 
    "wa", 
    "git_search", 
    "tebak_angka", 
]

def parse_prompt(input_str):
    input_str = input_str.strip()

    # Tokenize input by whitespace
    tokens = input_str.split()
    if not tokens:
        return {"command": None, "args": []}

    first_token = tokens[0].lower()
    if first_token in known_commands:
        return {
            "command": first_token,
            "args": tokens[1:]
        }

    # Unknown command fallback
    return {
        "command": None,
        "args": tokens
    }