from board import Board
from theme import Theme
from blocks import Square
from tui import Screen
import sys

class ConsoleBoard(Board):
    def __init__(self, l = 20, w = 10):
        Board.__init__(self, l, w)
        self.theme = Theme()

    def print(self):
        """Prints the current state of the board in a frame."""

        console_width = self.w * 2 + 1
        board_str = Screen.clear() + self.theme.frame_char("tl") + self.theme.frame_char("hor") * console_width + self.theme.frame_char("tr") + '\n'

        for y in range(self.l):
            board_str += self.theme.frame_char("vert") + self.theme.frame_char("space")
            for x in range(self.w):
                char_pos = self.theme.empty_board_char()

                square_pos = self.appearance_at_pos([x, y])
                if square_pos != 0:
                    char_pos = self.theme.tet_char(Square.name(square_pos))

                # TODO: board.board_color???
                board_str += char_pos + self.theme.board_space_char()
            board_str += self.theme.frame_char("vert") + "\n"

        board_str += self.theme.frame_char("bl") + self.theme.frame_char("hor") * console_width + self.theme.frame_char("br") + '\n'

        sys.stdout.write(board_str)
        sys.stdout.flush()
