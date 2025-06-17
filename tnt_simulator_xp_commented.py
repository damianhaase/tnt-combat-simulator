
import json
from combat import Character, Weapon, Armor, battle, distribute_damage, apply_spite

# Load a character from a JSON file and return it as a Character object
def load_character(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return Character.from_dict(data)

# Save a Character object to a JSON file
def save_character(character, filename):
    with open(filename, 'w') as f:
        json.dump(character.to_dict(), f, indent=2)

# Create a new character by taking input from the user
def create_character_from_input():
    name = input("Character name: ")
    str_ = int(input("Strength: "))
    dex = int(input("Dexterity: "))
    spd = int(input("Speed: "))
    luck = int(input("Luck: "))
    con = int(input("Constitution: "))

    # Get weapon details
    print("Create weapon:")
    w_name = input("  Weapon name: ")
    w_dice = int(input("  Weapon dice: "))
    w_adds = int(input("  Weapon adds: "))
    weapon = Weapon(w_name, w_dice, w_adds)

    # Get armor details
    print("Create armor:")
    a_name = input("  Armor name: ")
    a_protection = int(input("  Armor protection: "))
    armor = Armor(a_name, a_protection)

    return Character(name, str_, dex, spd, luck, con, weapon, armor)

# Build a team by either loading or creating characters
def team_builder():
    team = []
    while True:
        choice = input("Add character (N to stop, L to load from file, C to create new): ").strip().upper()
        if choice == "N":
            break
        elif choice == "L":
            filename = input("Enter filename to load character from (e.g., hero.json): ")
            try:
                char = load_character(filename)
                char.xp = 0  # Ensure XP exists
                team.append(char)
                print(f"Loaded {char.name}.")
            except Exception as e:
                print(f"Error loading file: {e}")
        elif choice == "C":
            char = create_character_from_input()
            char.xp = 0  # Initialize XP
            team.append(char)
            save = input("Save this character? (Y/N): ").strip().upper()
            if save == "Y":
                filename = input("Enter filename to save to (e.g., hero.json): ")
                save_character(char, filename)
    return team

# Grant XP to all characters on the given team
def award_xp(team, amount):
    for char in team:
        if hasattr(char, 'xp'):
            char.xp += amount
            print(f"{char.name} gains {amount} XP! Total XP: {char.xp}")

# The main loop for running multiple combat encounters
def encounter_loop():
    while True:
        print("\n=== TEAM 1 SETUP ===")
        team1 = team_builder()  # Player builds team 1
        print("\n=== TEAM 2 SETUP ===")
        team2 = team_builder()  # Player builds team 2

        if not team1 or not team2:
            print("Both teams must have at least one character. Restarting...")
            continue

        print("\n=== STARTING ENCOUNTER ===")
        round_num = 1
        while any(c.is_alive() for c in team1) and any(c.is_alive() for c in team2):
            print(f"\n--- Round {round_num} ---")
            from combat import combat_round  # Import here to ensure it's available
            combat_round(team1, team2)
            round_num += 1

            # Between rounds, offer choices
            action = input("Continue (C), Disengage (D), or Quit (Q)? ").strip().upper()
            if action == "D":
                print("Teams disengage. Encounter ends.")
                break
            elif action == "Q":
                print("Quitting game.")
                return

        # Show end-of-encounter results
        print("\n=== ENCOUNTER OVER ===")
        print("Team 1 Survivors:")
        for c in team1:
            print(f"{c.name}: {'Alive' if c.is_alive() else 'Defeated'} (CON: {c.con})")
        print("Team 2 Survivors:")
        for c in team2:
            print(f"{c.name}: {'Alive' if c.is_alive() else 'Defeated'} (CON: {c.con})")

        # Determine winner and award XP
        if any(c.is_alive() for c in team1) and not any(c.is_alive() for c in team2):
            award_xp(team1, 100)
        elif any(c.is_alive() for c in team2) and not any(c.is_alive() for c in team1):
            award_xp(team2, 100)
        else:
            print("No XP awarded due to disengagement or mutual defeat.")

        # Ask user if they want to start another encounter
        again = input("\nStart another encounter? (Y/N): ").strip().upper()
        if again != "Y":
            break

# Entry point of the simulator
if __name__ == "__main__":
    print("Welcome to the Tunnels & Trolls Combat Simulator (XP Edition)")
    encounter_loop()
