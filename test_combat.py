
import unittest
from combat import Character, Weapon, Armor, battle, distribute_damage, apply_spite

# This test suite verifies functionality of the combat system
class TestCombatSystem(unittest.TestCase):

    def setUp(self):
        # Prepare reusable weapons, armor, and characters
        self.sword = Weapon("Sword", 3, 2)
        self.dagger = Weapon("Dagger", 1, 3)
        self.chainmail = Armor("Chainmail", 4)
        self.none = Armor("None", 0)

        # Create one strong hero and one weaker goblin
        self.hero = Character("Hero", 14, 13, 12, 10, 30, self.sword, self.chainmail)
        self.goblin = Character("Goblin", 10, 10, 10, 10, 20, self.dagger, self.none)

    def test_character_combat_adds(self):
        # Test that the combat adds are calculated correctly from attributes
        self.assertEqual(self.hero.adds, 3)

    def test_is_alive_logic(self):
        # Test that a character is alive or not depending on constitution
        self.assertTrue(self.hero.is_alive())
        self.hero.con = 0
        self.assertFalse(self.hero.is_alive())

    def test_weapon_damage_range(self):
        # Test that the weapon rolls damage within the expected range
        for _ in range(100):
            dmg = self.sword.roll_damage()
            self.assertGreaterEqual(dmg, 5)  # min roll = 3*1 + 2
            self.assertLessEqual(dmg, 20)    # max roll = 3*6 + 2

    def test_spite_damage_application(self):
        # Apply spite damage and confirm HP reduction
        team = [self.hero]
        apply_spite(team, 2)
        self.assertEqual(self.hero.con, 28)

    def test_damage_distribution(self):
        # Damage should be reduced by armor
        team = [self.hero]
        distribute_damage(team, 10)  # Hero has 4 armor, so 6 gets through
        self.assertEqual(self.hero.con, 24)

    def test_character_serialization(self):
        # Confirm character can be saved and loaded accurately via dict
        data = self.hero.to_dict()
        restored = Character.from_dict(data)
        self.assertEqual(restored.name, self.hero.name)
        self.assertEqual(restored.weapon.name, self.hero.weapon.name)
        self.assertEqual(restored.armor.protection, self.hero.armor.protection)

    def test_mock_battle(self):
        # Run a short mock battle and ensure one team wins
        team1 = [self.hero]
        team2 = [self.goblin]
        battle(team1, team2)
        self.assertTrue(any(c.is_alive() for c in team1))
        self.assertFalse(any(c.is_alive() for c in team2))


if __name__ == '__main__':
    unittest.main()
