from board import Board
from theme import Theme
from blocks import Square
from tui import Screen
from score_window import ScoreWindow
import sys

class ConsoleBoard(Board):
    def __init__(self, l = 20, w = 10):
        Board.__init__(self, l, w)
        self._theme = Theme()
        self._score_window = ScoreWindow()

    def print_first(self):
        """Prints the current state of the board in a frame."""

        console_width = self._w * 2 + 1
        board_str = Screen.clear() + self._theme.frame_char("tl") + self._theme.frame_char("hor") * console_width + self._theme.frame_char("tr") + '\n'

        for y in range(self._l):
            board_str += self._theme.frame_char("vert") + self._theme.frame_char("space")
            for x in range(self._w):
                char_pos = self._theme.empty_board_char()

                square_pos = self._appearance_at_pos([x, y])
                if square_pos != Square.id("empty"):
                    char_pos = self._theme.tet_char(Square.name(square_pos))

                board_str += char_pos + self._theme.board_space_char()
            board_str += self._theme.frame_char("vert") + "\n"

        board_str += self._theme.frame_char("bl") + self._theme.frame_char("hor") * console_width + self._theme.frame_char("br") + '\n'

        sys.stdout.write(board_str)
        sys.stdout.flush()

        self._score_window.update(self._points)
        self._last_board = self._board.copy()
        self._last_block_coords = [e[0] for e in self._block_square_list()]

    def print(self):
        """Updates the printed board using ANSI escape codes."""
        
        filled_rows = self._find_filled_rows()
        curr_block_coords = [e[0] for e in self._block_square_list()]

        update_str = ""

        for y in range(self._l):
            for x in range(self._w):
                coords = [x, y]

                if (coords in self._last_block_coords == coords in curr_block_coords) and (self._last_board[y][x] == self._board[y][x]):
                    continue

                if y in filled_rows:
                    update_str += Screen.move_cursor(x * 2 + 3, y + 2) + self._theme.filled_row_char()

                char_pos = self._theme.empty_board_char()

                square_pos = self._appearance_at_pos([x, y])
                if square_pos != Square.id("empty"):
                    char_pos = self._theme.tet_char(Square.name(square_pos))

                update_str += Screen.move_cursor(x * 2 + 3, y + 2) + char_pos
        
        self._last_block_coords = curr_block_coords

        self._score_window.update(self._points)
        sys.stdout.write(update_str)
        sys.stdout.flush()

        self._last_board = self._board.copy()
