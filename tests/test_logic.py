import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic import validate_game_entry

class TestGameLibraryLogic(unittest.TestCase):
    def test_valid_data(self):
        self.assertTrue(validate_game_entry("Uncharted 4", 5))

    def test_empty_title(self):
        self.assertFalse(validate_game_entry("", 3))

    def test_invalid_rating(self):
        self.assertFalse(validate_game_entry("Elden Ring", 10))

if __name__ == '__main__':
    unittest.main()