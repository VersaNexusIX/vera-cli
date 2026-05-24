# VERA CLI — Contribution Guidelines

Thank you for your interest in contributing to VERA CLI. This document outlines the process for reporting issues, submitting improvements, and maintaining code quality across the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Reporting Issues](#reporting-issues)
- [Development Setup](#development-setup)
- [Branching and Workflow](#branching-and-workflow)
- [Code Standards](#code-standards)
- [Adding a New Command](#adding-a-new-command)
- [Submitting a Pull Request](#submitting-a-pull-request)

---

## Code of Conduct

All contributors are expected to engage respectfully and constructively. Criticism of code is welcome; personal criticism is not. Contributions of any size are valued equally.

---

## Reporting Issues

Before opening an issue, please search existing issues to avoid duplicates.

When reporting a bug, include the following:

- Operating system and version (e.g., Termux on Android 13, Ubuntu 22.04)
- Python version (`python3 --version`)
- The exact command that caused the issue
- The full error message or traceback
- Any relevant configuration (e.g., whether `cookies.txt` is present)

For feature requests, describe the problem you are trying to solve and why the proposed feature would address it.

---

## Development Setup

**Clone the repository:**

```bash
git clone https://github.com/VersaNexusIX/vera-cli.git
cd vera-cli
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the application:**

```bash
python3 cli.py
```

No build step or compilation is required. All changes take effect on the next run.

---

## Branching and Workflow

| Branch | Purpose |
|---|---|
| `main` | Stable release branch |
| `dev` | Active development and integration |
| `feature/<name>` | Individual feature branches |
| `fix/<issue>` | Bug fix branches |

All contributions should branch from `dev` and be submitted as pull requests targeting `dev`. The `main` branch is updated only for releases.

---

## Code Standards

### Language and Style

- Python 3.8 or later
- Follow PEP 8 for formatting and naming conventions
- Use 4-space indentation (no tabs)
- Maximum line length: 100 characters

### Handler Conventions

Every handler must:

- Reside in `handlers/<module>.py`
- Expose a `handle(args: list) -> str` function
- Return a formatted string (or `None` if there is no output)
- Validate input at the start and return a usage hint if arguments are missing
- Handle all exceptions internally and return a formatted error string rather than raising

```python
# Correct
def handle(args):
    if not args:
        return Fore.YELLOW + "  Format: mycommand <input>" + Style.RESET_ALL
    try:
        # ... logic ...
        return Fore.GREEN + "  Result: ..." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"  Error: {e}" + Style.RESET_ALL
```

### Output Formatting

Use `colorama` for all colored output. Maintain consistency with the existing style:

- Use `Fore.CYAN` for headers and section separators
- Use `Fore.GREEN` for success messages
- Use `Fore.YELLOW` for warnings and usage hints
- Use `Fore.RED` for errors
- Use `Style.RESET_ALL` at the end of every colored string
- Indent all output with two spaces for alignment within the terminal frame

### Imports

Order imports as follows:

1. Standard library
2. Third-party packages
3. Local modules (`config`, `utils`, `handlers`)

Separate each group with a blank line.

---

## Adding a New Command

Refer to the [Extending VERA CLI](ARCHITECTURE.md#extending-vera-cli) section in the Architecture document for the step-by-step process.

In summary:

1. Create `handlers/<module>.py` with a compliant `handle()` function.
2. Register the command in `COMMANDS` inside `cli.py`.
3. Add an alias to `ALIASES` if applicable.
4. Add an entry to `HELP_TEXT` in `cli.py`.
5. Add the same entry to `assets/help.txt`.
6. Document the command in `docs/COMMANDS.md`.
7. Add an entry to `CHANGELOG.md` under the appropriate version.

---

## Submitting a Pull Request

1. Fork the repository and create a branch from `dev`.
2. Make your changes, following the code standards above.
3. Test your changes on at least one supported platform.
4. Ensure no existing commands are broken by your changes.
5. Open a pull request targeting the `dev` branch.
6. Provide a clear description of what the change does and why it is needed.
7. Reference any related issue numbers in the pull request description.

Pull requests that introduce breaking changes must include a migration note in the description.

---

All contributions, including documentation improvements, issue reports, and code reviews, are appreciated and credited.
