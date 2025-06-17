
# 🐉 Tunnels & Trolls Combat Simulator

This Python-based simulator implements a team-vs-team combat system inspired by the Tunnels & Trolls 7th Edition rules. It's modular, extensible, and easy to expand into a full RPG engine.

---

## 📦 File Structure

```
combat.py                   # Core classes and combat logic
tnt_simulator_xp_commented.py  # Main program with XP and detailed comments
test_combat.py              # Unit tests for all major functions
alice.json, goblin.json... # Sample characters and monsters
```

---

## ▶️ How to Run the Simulator

1. Ensure Python 3.9+ is installed.
2. Place all `.py` and `.json` files in the same folder.
3. Run the simulator:

```bash
python tnt_simulator_xp_commented.py
```

4. Follow prompts to:
   - Create or load characters
   - Assign characters to teams
   - Run combat rounds
   - Disengage, continue, or quit
   - View end-of-battle summaries
   - Grant XP to the winning team

---

## ⚔️ Combat Mechanics

- Teams roll total attack strength each round.
- Damage is dealt to the losing team, reduced by armor.
- "Spite" damage from rolling 6s is applied directly, ignoring armor.
- Battles loop until one team is defeated or players disengage.

---

## 🧪 How to Run Tests

Run unit tests using the built-in `unittest` module:

```bash
python -m unittest test_combat.py
```

Tests include:
- Weapon and armor stats
- Combat adds logic
- Spite and standard damage
- Dictionary serialization
- Full battle resolution

---

## 📚 Sample Characters

Each `.json` file defines a character and includes a `_description` for context. Use them to build teams quickly.

Examples:
- `alice.json`: A balanced fighter with armor and sword
- `goblin.json`: Weak but fast opponent
- `troll.json`: Strong and well-armored brute

---

## 🧱 Customization Ideas

- Add inventory and loot drops
- Implement XP leveling and skills
- Create a persistent campaign mode
- Add magic, ranged attacks, or terrain effects

---

## 🤝 Contributing

This is a great starting point for learning Python through game design. Fork, extend, and share your own additions!

---
