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

# ---------- Game State ----------

@dataclass
class Player:
    health: int = 3
    score: int = 0
    inventory: List[str] = field(default_factory=list)

    def has(self, item: str) -> bool:
        return item in self.inventory

    def add(self, item: str, pts: int = 5) -> None:
        if item not in self.inventory:
            self.inventory.append(item)
            self.score += pts
            slow_print(f"[+] You obtained **{item}** (+{pts} pts)")

    def damage(self, amount: int = 1) -> None:
        self.health -= amount
        slow_print(f"[!] You took {amount} damage. Health: {self.health}")

    def heal(self, amount: int = 1, pts: int = 2) -> None:
        self.health += amount
        self.score += pts
        slow_print(f"[+] You feel better (+{amount} health, +{pts} pts). Health: {self.health}"
