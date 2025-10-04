"""
This is the main logic for a Tic-tac-toe game.
Converted to an OOP design with a Game class.
"""

import os, random
import oxo_data

class Game:
    def __init__(self, game=None):
        """Initialize game state. If no game passed, start a new one."""
        if game is None:
            self.game = [" "] * 9
        else:
            self.game = game

    def newGame(self):
        """Reset the board."""
        self.game = [" "] * 9
        return self.game

    def saveGame(self):
        """Save the current game to disk."""
        oxo_data.saveGame(self.game)

    @classmethod
    def restoreGame(cls):
        """Restore a previously saved game, or return a new one if unavailable."""
        try:
            game = oxo_data.restoreGame()
            if len(game) == 9:
                return cls(game)
            else:
                return cls()
        except IOError:
            return cls()

    def _generateMove(self):
        """Generate a random cell from those available, or return -1 if full."""
        options = [i for i in range(len(self.game)) if self.game[i] == " "]
        return random.choice(options) if options else -1

    def _isWinningMove(self):
        """Check if the current board has a winning line."""
        wins = ((0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6))

        for a,b,c in wins:
            chars = self.game[a] + self.game[b] + self.game[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False

    def userMove(self, cell):
        """Apply the user move. Raise error if cell is invalid."""
        if self.game[cell] != ' ':
            raise ValueError("Invalid cell")
        else:
            self.game[cell] = 'X'
        if self._isWinningMove():
            return 'X'
        else:
            return ""

    def computerMove(self):
        """Generate and apply a computer move."""
        cell = self._generateMove()
        if cell == -1:
            return 'D'
        self.game[cell] = 'O'
        if self._isWinningMove():
            return 'O'
        else:
            return ""

    def __str__(self):
        """Pretty print the board as a 3x3 grid."""
        rows = [
            " | ".join(self.game[i:i+3])
            for i in range(0, 9, 3)
        ]
        return "\n---------\n".join(rows)

# Test loop
if _name_ == "_main_":
    result = ""
    game = Game()
    while not result:
        print(game)
        try:
            result = game.userMove(game._generateMove())
        except ValueError:
            print("Oops, that shouldn't happen")
        if not result:
            result = game.computerMove()

        if not result:
            continue
        elif result == 'D':
            print("It's a draw")
        else:
            print("Winner is:", result)
        print(game)