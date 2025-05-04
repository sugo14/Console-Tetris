from tui import Screen
from theme import Theme
import sys

class ScoreWindow():
    def __init__(self, x = 30, y = 5):
        self.score = 0
        self.x = x
        self.y = y
        self.initial_print()

    def initial_print(self):
        """Prints the initial score window."""

        sys.stdout.write(Screen.move_cursor(self.x, self.y))
        sys.stdout.write(f"Score: {self.score}")

    def update_print(self):
        """Updates the score window."""

        self.initial_print()

    def update(self, score):
        """Updates the score window with the new score."""
        
        self.score = score
        self.update_print()
