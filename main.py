#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

Writes one line, the excuse an AI agent gives its human after
breaking production, to /output/entry.txt.

The line is validated before it is written: it must be a single
non-blank line of 1 to 180 characters, and the file is read back
afterwards to confirm the exact bytes landed.
"""

import hashlib
import os
import sys

LINE = "The tests all passed, which I now realise was the tests giving up, not the code working."

MIN_CHARS = 1
MAX_CHARS = 180


def validate(line: str) -> None:
    if not line.strip():
        raise ValueError("entry line must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS} to {MAX_CHARS} chars, got {len(line)}"
        )


def main() -> None:
    validate(LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(LINE)
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise ValueError("read-back mismatch: entry bytes differ from LINE")
    print(
        f"wrote {len(written)} bytes, "
        f"sha256 {hashlib.sha256(written).hexdigest()}"
    )


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
