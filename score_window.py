from tui import Screen
from theme import Theme
import sys

class ScoreWindow():
    def __init__(self, x = 40, y = 0):
        self.score = 0
        self.x = x
        self.y = y
        self.initial_print()

    def initial_print(self):
        sys.stdout.write(Screen.move_cursor(self.x, self.y))
        sys.stdout.write(f"Score: {self.score}")
        sys.stdout.flush()

    def update_print(self):
        self.initial_print()

    def update(self, score):
        self.score = score
        self.update_print()
