
import random
from typing import List

# Weapon class defines a weapon's damage dice and adds
class Weapon:
    def __init__(self, name: str, dice: int, adds: int):
        self.name = name
        self.dice = dice
        self.adds = adds

    # Simulate rolling the weapon's damage
    def roll_damage(self):
        return sum(random.randint(1, 6) for _ in range(self.dice)) + self.adds

    # Count how many '6's were rolled for spite damage
    def count_spite(self):
        return sum(1 for _ in range(self.dice) if random.randint(1, 6) == 6)

    # Convert to a dictionary for JSON serialization
    def to_dict(self):
        return {"name": self.name, "dice": self.dice, "adds": self.adds}

    # Create a Weapon object from a dictionary
    @staticmethod
    def from_dict(data):
        return Weapon(data["name"], data["dice"], data["adds"])


# Armor class defines protection level
class Armor:
    def __init__(self, name: str, protection: int):
        self.name = name
        self.protection = protection

    # Convert to dictionary for saving
    def to_dict(self):
        return {"name": self.name, "protection": self.protection}

    # Load from dictionary
    @staticmethod
    def from_dict(data):
        return Armor(data["name"], data["protection"])


# Character class represents each fighter in the game
class Character:
    def __init__(self, name, strength, dexterity, speed, luck, constitution, weapon: Weapon, armor: Armor):
        self.name = name
        self.str = strength
        self.dex = dexterity
        self.spd = speed
        self.luck = luck
        self.con = constitution
        self.max_con = constitution
        self.weapon = weapon
        self.armor = armor
        self.adds = self.calculate_adds()
        self.xp = 0  # XP is tracked externally too

    # Calculate total combat adds based on stats
    def calculate_adds(self):
        adds = 0
        for attr in [self.str, self.dex, self.spd, self.luck]:
            if attr > 12:
                adds += attr - 12
            elif attr < 9:
                adds -= 9 - attr
        return adds

    # Check if the character is still alive
    def is_alive(self):
        return self.con > 0

    # Roll weapon damage and add combat adds
    def roll_attack(self):
        base_damage = self.weapon.roll_damage()
        total = base_damage + self.adds
        return total, base_damage

    # Count number of 6s for spite damage
    def roll_spite(self):
        return self.weapon.count_spite()

    # Convert to dictionary for saving
    def to_dict(self):
        return {
            "name": self.name,
            "strength": self.str,
            "dexterity": self.dex,
            "speed": self.spd,
            "luck": self.luck,
            "constitution": self.con,
            "weapon": self.weapon.to_dict(),
            "armor": self.armor.to_dict()
        }

    # Rebuild from dictionary
    @staticmethod
    def from_dict(data):
        weapon = Weapon.from_dict(data["weapon"])
        armor = Armor.from_dict(data["armor"])
        return Character(
            data["name"],
            data["strength"],
            data["dexterity"],
            data["speed"],
            data["luck"],
            data["constitution"],
            weapon,
            armor
        )


# Simulate one round of combat between two teams
def combat_round(team1: List[Character], team2: List[Character]):
    team1_attack = 0
    team2_attack = 0
    team1_spite = 0
    team2_spite = 0

    print("\n--- Combat Round ---")

    for member in team1:
        if member.is_alive():
            attack, _ = member.roll_attack()
            team1_attack += attack
            team1_spite += member.roll_spite()

    for member in team2:
        if member.is_alive():
            attack, _ = member.roll_attack()
            team2_attack += attack
            team2_spite += member.roll_spite()

    print(f"Team 1 Attack Total: {team1_attack} | Spite: {team1_spite}")
    print(f"Team 2 Attack Total: {team2_attack} | Spite: {team2_spite}")

    # Higher total wins and deals damage
    if team1_attack > team2_attack:
        distribute_damage(team2, team1_attack - team2_attack)
    elif team2_attack > team1_attack:
        distribute_damage(team1, team2_attack - team1_attack)
    else:
        print("It's a draw! No damage dealt.")

    # Apply spite damage to both teams
    apply_spite(team2, team1_spite)
    apply_spite(team1, team2_spite)


# Split incoming damage evenly among all living characters on a team
def distribute_damage(team: List[Character], damage: int):
    alive = [c for c in team if c.is_alive()]
    if not alive:
        return
    per_character = damage // len(alive)
    print(f"Distributing {damage} damage among {len(alive)} enemies ({per_character} each before armor)")
    for char in alive:
        reduced = max(0, per_character - char.armor.protection)
        char.con -= reduced
        print(f"{char.name} takes {reduced} damage after armor (CON now {char.con})")

# Apply spite damage directly to health (ignores armor)
def apply_spite(team: List[Character], spite: int):
    if spite == 0:
        return
    print(f"Applying {spite} spite damage to each member of the team")
    for char in team:
        if char.is_alive():
            char.con -= spite
            print(f"{char.name} suffers {spite} spite damage (CON now {char.con})")

# Main battle loop between two teams
def battle(team1: List[Character], team2: List[Character]):
    round_num = 1
    while any(c.is_alive() for c in team1) and any(c.is_alive() for c in team2):
        print(f"\n=== Round {round_num} ===")
        combat_round(team1, team2)
        round_num += 1

    # Check who is still standing after the loop
    team1_alive = any(c.is_alive() for c in team1)
    team2_alive = any(c.is_alive() for c in team2)

    if not team1_alive and not team2_alive:
        winner = "No one"
    else:
        winner = "Team 1" if team1_alive else "Team 2"

    print(f"\n{winner} wins the battle!")
