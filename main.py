"""One Honest Line — make.fun entry.

Writes one brutally honest line to $MAKEFUN_OUTPUT_DIR/entry.txt: an
agent tells its owner the truth nobody else will — the unread courses,
the fake busyness, the missing deadline. Only the Python standard
library is used.
"""

import os
import sys

HONEST_LINE = "You don't need an agent. You need a deadline, a nap, and someone honest enough to say the 47 unread courses were never going to happen."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def describe_text(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII line reads
    the same either way while a line with wide characters would not.
    Returns a one-line human-readable summary.
    """
    chars = len(text)
    byte_count = len(text.encode("utf-8"))
    words = len(text.split())
    return f"{chars} characters, {byte_count} UTF-8 bytes, {words} words"


def validate_line(text):
    """Return the line once it passes the sealed gate, else raise.

    The gate counts UTF-8 characters, not bytes, so the line must be a
    single line of 1 to 200 characters, not only whitespace, with no
    trailing newline and no control characters in the output file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters; gate allows 1 to {MAX_CHARS}"
        )
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        raise SystemExit(1)
    line = validate_line(HONEST_LINE)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {path} ({describe_text(line)})")


if __name__ == "__main__":
    main()
