import random

RARITIES = [
    ("Common", 60, 10),
    ("Uncommon", 25, 18),
    ("Rare", 10, 30),
    ("Epic", 4, 50),
    ("Legendary", 1, 90),
]

SPECIES = ["Mochi", "Pofu", "Chiki", "Bomu", "Hopu", "Zoomu"]

COMMANDS = {
    "pouf": "A soft POUF echoes through the group!",
    "chik": "CHIK! Something moved nearby.",
    "boom": "BOOM! A tiny event just happened.",
    "hop": "HOP! A Mochi jumps into the scene.",
    "zoom": "ZOOM! Something rushed past.",
    "ping": "PING! A mysterious signal appeared.",
    "pakh": "PAKH! A hidden clue was found.",
    "treasure": "A treasure event has appeared!",
    "night": "Night mode: a rare Mochi may appear.",
}

def roll_mochi():
    roll = random.randint(1, 100)
    total = 0
    for rarity, chance, power in RARITIES:
        total += chance
        if roll <= total:
            species = random.choice(SPECIES)
            return species, rarity, power + random.randint(0, 5)
    return "Mochi", "Common", 10

def random_event():
    return random.choice([
        ("coin", random.randint(10, 40)),
        ("gem", random.randint(1, 3)),
        ("ticket", 1),
        ("xp", random.randint(10, 30)),
    ])
