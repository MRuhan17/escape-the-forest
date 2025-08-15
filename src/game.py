import sys
import time
import random
from dataclasses import dataclass, field
from typing import List

# ---------- Utilities ----------

def slow_print(text: str, delay: float = 0.02) -> None:
    """Print text with a gentle typewriter effect."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def ask(prompt: str, options: List[str]) -> str:
    """Ask the user until they give one of the allowed responses."""
    opts = "/".join(options)
    while True:
        resp = input(f"{prompt} ({opts}): ").strip().lower()
        if resp in options:
            return resp
        print(f"Please type one of: {', '.join(options)}")
