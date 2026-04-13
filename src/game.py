import sys
import time
import random
from dataclasses import dataclass, field

# ---------- Utils ----------

def slow(text, delay=0.015):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def ask(q, opts):
    while True:
        ans = input(f"{q} ({'/'.join(opts)}): ").lower()
        if ans in opts:
            return ans

# ---------- Player ----------

@dataclass
class Player:
    hp: int = 5
    score: int = 0
    inv: list = field(default_factory=list)

    def add(self, item, pts=5):
        if item not in self.inv:
            self.inv.append(item)
            self.score += pts
            slow(f"[+] Got {item}")

    def dmg(self, n=1):
        self.hp -= n
        slow(f"[!] Took {n} damage | HP: {self.hp}")

    def heal(self, n=1):
        self.hp += n
        slow(f"[+] Healed {n} | HP: {self.hp}")

# ---------- Combat ----------

def fight(p, name="Rival", hp=4):
    slow(f"\n⚔️ {name} appears!")

    while hp > 0 and p.hp > 0:
        slow(f"Your HP: {p.hp} | {name} HP: {hp}")
        move = ask("Choose", ["attack", "defend", "item"])

        enemy = random.choice(["attack", "attack", "defend"])

        if move == "attack":
            if enemy == "defend":
                slow(f"{name} blocked it.")
            else:
                dmg = random.randint(1,2)
                hp -= dmg
                slow(f"You deal {dmg}")

        elif move == "defend":
            slow("You brace.")

        elif move == "item":
            if "rations" in p.inv:
                p.heal(2)
                p.inv.remove("rations")
            else:
                slow("No usable item.")

        if hp > 0 and enemy == "attack":
            if move != "defend":
                p.dmg(1)
            else:
                slow("You blocked.")

    if p.hp <= 0:
        ending(p, "You were defeated")
    else:
        slow(f"{name} defeated.")
        p.score += 20

# ---------- Puzzle ----------

def puzzle_echo(p):
    slow("\n'I speak without a mouth and hear without ears. What am I?'")
    ans = input("Answer: ").lower()
    if "echo" in ans:
        p.add("whistle", 10)
    else:
        p.dmg(1)

def puzzle_math(p):
    slow("\nSequence: 2, 4, 8, 16, ?")
    ans = input("Answer: ")
    if ans == "32":
        p.add("core", 20)
    else:
        p.dmg(1)

# ---------- Scenes ----------

def intro(p):
    slow("\nYou wake in a dark forest.")
    c = ask("Go", ["north", "east"])

    if c == "north":
        hut(p)
    else:
        river(p)

# ---------- Hut ----------

def hut(p):
    slow("\nYou find a hut.")

    if ask("Search outside", ["yes","no"]) == "yes":
        p.add("key", 8)

    if ask("Enter hut", ["yes","no"]) == "yes":
        if "key" in p.inv:
            slow("Chest opened.")
            p.add("map", 10)
            p.add("rations", 5)
        else:
            slow("Locked chest.")

    clearing(p)

# ---------- River ----------

def river(p):
    slow("\nYou reach a river.")

    if ask("Cross", ["yes","no"]) == "yes":
        if random.random() < 0.6:
            slow("You cross safely.")
        else:
            slow("You slip.")
            p.dmg(1)

    beach(p)

# ---------- Clearing ----------

def clearing(p):
    slow("\nA stone circle.")

    puzzle_echo(p)

    c = ask("Go", ["hills","river"])
    if c == "hills":
        canyon(p)
    else:
        river(p)

# ---------- Beach ----------

def beach(p):
    slow("\nYou reach a beach.")

    if ask("Search", ["yes","no"]) == "yes":
        p.add("shard", 5)

    canyon(p)

# ---------- Canyon ----------

def canyon(p):
    slow("\nA canyon with a rope bridge.")

    if ask("Search area", ["yes","no"]) == "yes":
        p.add("rope", 6)

    if ask("Cross bridge", ["yes","no"]) == "yes":
        if "rope" in p.inv or random.random() < 0.6:
            slow("You cross safely.")
        else:
            slow("You fall slightly.")
            p.dmg(1)

    gate(p)

# ---------- Gate ----------

def gate(p):
    slow("\nA massive stone gate.")

    if "map" in p.inv:
        slow("You understand the mechanism.")

    slow("The gate opens...")
    ruins(p)

# ---------- PART 2 ----------

def ruins(p):
    slow("\nYou enter ancient ruins.")
    slow("This wasn't escape. It was level one.")

    c = ask("Go", ["tower","arena","vault"])

    if c == "tower":
        tower(p)
    elif c == "arena":
        arena(p)
    else:
        vault(p)

# ---------- Tower ----------

def tower(p):
    slow("\nYou climb a broken tower.")

    if random.random() < 0.7:
        p.add("ancient map", 10)
    else:
        p.dmg(1)

    ruins(p)

# ---------- Arena ----------

def arena(p):
    slow("\nArena. A rival appears.")

    c = ask("Action", ["fight","talk","run"])

    if c == "fight":
        fight(p)

    elif c == "talk":
        if random.random() < 0.5:
            p.add("medkit", 10)
        else:
            fight(p)

    ruins(p)

# ---------- Vault ----------

def vault(p):
    slow("\nA sealed vault.")

    puzzle_math(p)

    if "core" in p.inv:
        p.add("artifact", 25)

    final(p)

# ---------- Final ----------

def final(p):
    slow("\nA glowing portal stands before you.")

    if "artifact" in p.inv and "core" in p.inv:
        ending(p, "TRUE ENDING: You broke the system")
    elif p.hp >= 3:
        ending(p, "NEUTRAL: You survived")
    else:
        ending(p, "BAD: Lost forever")

# ---------- Ending ----------

def ending(p, title):
    slow("\n=== END ===")
    slow(title)
    slow(f"Score: {p.score}")
    slow(f"HP: {p.hp}")
    slow(f"Inventory: {p.inv}")

    if ask("Play again", ["yes","no"]) == "yes":
        game()
    else:
        sys.exit()

# ---------- Start ----------

def game():
    slow("\n=== ESCAPE THE FOREST ===\n")
    p = Player()
    intro(p)

if __name__ == "__main__":
    game()
