import unittest
import os
from OXO_updated import Game
from oxo_logic import oxo_data

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        """Run before each test"""
        self.game = Game()

    def tearDown(self):
        """Run after each test"""
        if os.path.exists(oxo_data.SAVE_FILE):
            os.remove(oxo_data.SAVE_FILE)

    def test_new_game_is_empty(self):
        self.assertEqual(self.game.game, [" "] * 9)

    def test_user_move_valid(self):
        result = self.game.userMove(0)
        self.assertEqual(self.game.game[0], "X")
        self.assertEqual(result, "")

    def test_user_move_invalid(self):
        self.game.userMove(0)
        with self.assertRaises(ValueError):
            self.game.userMove(0)

    def test_computer_move_places_O(self):
        result = self.game.computerMove()
        self.assertIn("O", self.game.game)
        self.assertIn(result, ["", "O", "D"])

    def test_winning_move_user(self):
        self.game.game = ["X", "X", " ", " ", " ", " ", " ", " ", " "]
        result = self.game.userMove(2)
        self.assertEqual(result, "X")

    def test_winning_move_computer(self):
        self.game.game = ["O", " ", " ", "O", " ", " ", " ", " ", " "]
        result = self.game.computerMove()
        self.assertEqual(result, "O")

    def test_draw_game(self):
        self.game.game = ["X","O","X",
                          "X","O","O",
                          "O","X"," "]
        result = self.game.computerMove()
        self.assertEqual(result, "D")

    def test_save_and_restore(self):
        self.game.userMove(0)
        self.game.saveGame()
        restored = Game.restoreGame()
        self.assertEqual(restored.game, self.game.game)

if _name_ == "_main_":
    unittest.main()