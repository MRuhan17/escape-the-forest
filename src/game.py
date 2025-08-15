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

# ---------- Scenes ----------

def intro(p: Player) -> None:
    slow_print("You wake to the hush of a **dark forest**.")
    slow_print("A narrow **path** leads north, and a silver **river** whispers to the east.")
    choice = ask("Where do you go", ["north", "east"])
    if choice == "north":
        hut(p)
    else:
        river(p)

def hut(p: Player) -> None:
    slow_print("You follow the path and reach a mossy **hut** with a wooden door.")
    if not p.has("rusty key"):
        slow_print("A wind chime glints… something is lodged beneath the mat.")
        if ask("Check under the mat", ["yes", "no"]) == "yes":
            p.add("rusty key", 8)
    enter = ask("Do you enter the hut", ["yes", "no"])
    if enter == "no":
        slow_print("You circle the hut and spot a faint **trail** west.")
        return clearing(p)

    slow_print("Inside: dust, a table, and a locked **chest**.")
    if p.has("rusty key") and ask("Use the rusty key on the chest", ["yes", "no"]) == "yes":
        slow_print("The lock clicks open.")
        p.add("forest map", 10)
        p.add("dried rations", 5)
        if ask("Eat some rations", ["yes", "no"]) == "yes":
            p.heal(1, 2)
    else:
        slow_print("The chest won’t budge. Maybe there’s a key somewhere…")

    if ask("Leave the hut and head back outside", ["yes", "no"]) == "yes":
        clearing(p)
    else:
        slow_print("You nap on the dusty floor and wake sneezing. Time to go.")
        clearing(p)

def river(p: Player) -> None:
    slow_print("You reach the **river**. The current looks strong.")
    if not p.has("branch pole"):
        slow_print("A fallen **branch** could make a pole.")
        if ask("Pick up the branch", ["yes", "no"]) == "yes":
            p.add("branch pole", 5)

    choice = ask("Do you try to cross", ["ford", "wait", "follow"])
    if choice == "ford":
        success = random.random() < (0.65 if p.has("branch pole") else 0.35)
        if success:
            slow_print("You balance across slick stones, the pole steadying you.")
            p.score += 10
            canyon(p)
        else:
            slow_print("You slip! The current drags you downstream.")
            p.damage(1)
            beach(p)
    elif choice == "wait":
        slow_print("You wait. The moon rises; the current eases a little.")
        p.score += 3
        canyon(p)
    else:
        slow_print("You follow the riverbank and discover a sandy **beach**.")
        beach(p)

def clearing(p: Player) -> None:
    slow_print("A sunlit **clearing** opens ahead. Stones form a circle with etched symbols.")
    slow_print("A riddle is carved on one: ‘I speak without a mouth and hear without ears. What am I?’")
    answer = input("Your answer: ").strip().lower()
    if "echo" in answer:
        slow_print("The stones hum. A hidden compartment opens.")
        p.add("silver whistle", 12)
    else:
        slow_print("The stones stay silent. Maybe another time.")
        p.damage(1)

    next_step = ask("Paths lead north to **hills** or east to the **river**", ["hills", "river"])
    if next_step == "hills":
        canyon(p)
    else:
        river(p)

def beach(p: Player) -> None:
    slow_print("You crawl onto a **beach**. Driftwood litters the shore.")
    if not p.has("glass shard"):
        slow_print("Among the driftwood, a **glass shard** glitters.")
        if ask("Take the glass shard", ["yes", "no"]) == "yes":
            p.add("glass shard", 4)

    if ask("Light a signal fire with driftwood", ["yes", "no"]) == "yes":
        slow_print("Smoke curls skyward. You hear a distant answering whistle.")
        p.score += 8

    slow_print("Footprints lead inland toward rocky **canyons**.")
    canyon(p)

def canyon(p: Player) -> None:
    slow_print("You enter a narrow **canyon**. A rope bridge spans a chasm.")
    if not p.has("forest map"):
        slow_print("Without a map, you feel uncertain where this leads…")
    act = ask("Cross the bridge or search around", ["cross", "search"])
    if act == "search":
        slow_print("Behind a boulder, a pack! Inside: **rope** and a **flint**.")
        p.add("rope", 6)
        p.add("flint", 6)

    if ask("Proceed to cross the bridge", ["yes", "no"]) == "yes":
        if p.has("rope") and random.random() < 0.9:
            slow_print("You reinforce the frayed planks with rope. Safe crossing!")
            p.score += 10
            gate(p)
        else:
            if random.random() < 0.6:
                slow_print("The bridge sways but holds. You make it across.")
                p.score += 6
                gate(p)
            else:
                slow_print("A plank snaps! You slam into the side and scramble up.")
                p.damage(1)
                gate(p)
    else:
        slow_print("You backtrack and find a longer, safer route—time lost, but safe.")
        p.score += 2
        gate(p)

def gate(p: Player) -> None:
    slow_print("Beyond the canyon stands an ancient **stone gate** with three sockets.")
    needed = {"silver whistle", "forest map", "flint"}
    have = needed.intersection(set(p.inventory))
    slow_print(f"You hold: {', '.join(sorted(have)) or 'nothing useful'}")

    # Simple ending logic based on items
    if needed.issubset(set(p.inventory)):
        slow_print("You study the map, spark the signal with flint, and blow the whistle.")
        slow_print("Mechanisms grind; the gate opens to a sunlit road. You’re free!")
        p.score += 25
        ending(p, "True Escape")
    elif {"forest map", "silver whistle"}.issubset(set(p.inventory)):
        slow_print("You coordinate with distant watchers using the whistle and map routes.")
        slow_print("A rescue party arrives by dusk and guides you out. You survive!")
        p.score += 15
        ending(p, "Rescued")
    else:
        slow_print("You can’t open the gate. As night falls, you set a camp and wait.")
        if p.health >= 3:
            slow_print("You endure the cold and find a patrol at dawn.")
            p.score += 8
            ending(p, "Survived the Night")
        else:
            slow_print("Exhausted and injured, you drift into uneasy sleep…")
            ending(p, "Lost to the Forest")

def ending(p: Player, title: str) -> None:
    slow_print("\n=== THE END ===")
    slow_print(f"Outcome: {title}")
    slow_print(f"Final Score: {p.score}")
    slow_print(f"Health: {p.health}")
    slow_print(f"Inventory: {', '.join(p.inventory) or 'Empty'}\n")
    if ask("Play again", ["yes", "no"]) == "yes":
        game()
    else:
        slow_print("Thanks for playing! 🌲")
        sys.exit(0)

# ---------- Entry Point ----------

def game() -> None:
    random.seed()  # fresh randomness each run
    player = Player()
    intro(player)

if __name__ == "__main__":
    try:
        game()
    except KeyboardInterrupt:
        print("\nGoodbye!")
