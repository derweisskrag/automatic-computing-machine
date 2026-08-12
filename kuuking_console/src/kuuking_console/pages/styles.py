from __future__ import annotations

# ---------------------------------------------------------------------------
# ANSI helpers (disabled on non-TTY)
# ---------------------------------------------------------------------------

from sys import stdout

_TTY = stdout.isatty()

def _c(code: str, text: str) -> str:
    if not _TTY:
        return text
    return f"\033[{code}m{text}\033[0m"

def bold(t: str) -> str:   return _c("1", t)
def dim(t: str) -> str:    return _c("2", t)
def green(t: str) -> str:  return _c("32", t)
def yellow(t: str) -> str: return _c("33", t)
def cyan(t: str) -> str:   return _c("36", t)
def red(t: str) -> str:    return _c("31", t)
def magenta(t: str) -> str: return _c("35", t)

# RULES: 
# Our message follows the same logic:
# [BURMESE <VERB> 🐍]: QUESTION OR INSTRUCTION
def apply_burmese_style(verb: str, message: str, emoji: str = "🐍") -> str:
    """
    Formats standard Burmese logs into: [BURMESE VERB 🐍]: message
    """
    header = green(f"[BURMESE {verb.upper()} {emoji}]")
    body = bold(red(message))
    return f"{header}: {body}"


def burmese_print(verb: str, message: str, emoji: str = "🐍", **kwargs):
    """Custom print wrapper for Burmese CLI outputs."""
    print(apply_burmese_style(verb, message, emoji), **kwargs)


def burmese_input(verb: str, prompt: str, emoji: str = "🐍") -> str:
    """Custom input wrapper so input prompts get the exact same style!"""
    return input(apply_burmese_style(verb, prompt, emoji) + " ")