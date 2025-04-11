from blocks import Blocks, Colors
import theme
from theme import Theme

class Board():
    EMPTY_SQUARE = " "
    BOARD_COLOR = Colors.GREY

    def __init__(self, l = 20, w = 10):
        theme.load_theme()
        self.l = l
        self.w = w
        self.board = [[(Board.EMPTY_SQUARE) for i in range(w)] for j in range(l)]
        self.next_block()

    def block_coords(self):
        return [[x + self.x, y + self.y] for x, y in self.block.coords()]

    def at_pos(self, coords):
        board_char = self.board[coords[1]][coords[0]]
        if board_char != Board.EMPTY_SQUARE:
            return board_char
        if coords in self.block_coords():
            return self.block.char()
        return Board.EMPTY_SQUARE

    def next_block(self):
        self.block = Blocks.next()
        self.x = int(self.w / 2 - self.block.size() / 2)
        self.y = 0

    def print(self):
        """Prints the current state of the board in a frame."""

        console_width = self.w * 2 + 1
        board_str = Board.BOARD_COLOR + Theme["chars"]["tl"] + Theme["chars"]["hor"] * console_width + Theme["chars"]["tr"] + '\n'

        for y in range(self.l):
            board_str += Theme["chars"]["vert"] + " "
            for x in range(self.w):
                board_str += self.at_pos([x, y]) + Board.BOARD_COLOR + " "
            board_str += Theme["chars"]["vert"] + "\n"

        board_str += Theme["chars"]["bl"] + Theme["chars"]["hor"] * console_width + Theme["chars"]["br"] + '\n'

        print("\x1b[2J\x1b[H")
        print(board_str)

    def find_filled_rows(self):
        """Finds all rows that are completely filled and ready for clearing.

        Returns:
            list: The rows that are ready to be cleared.
        """

        rows = []
        for i in range(self.l):
            count = 0
            for j in range(self.w):
                if self.board[i][j] == Board.EMPTY_SQUARE:
                    break
                count += 1
            if count == self.w:
                rows.append(i)
        return rows
    
    def clear_row(self, index):
        """Deletes a row at an index and adds an empty row in its place.

        Args:
            index (int): The index of the row to empty.
        """

        self.board.pop(index)
        self.board.insert(index, [(Board.EMPTY_SQUARE) for i in range(self.w)])

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1
    
    def move_right(self):
        self.x += 1

    def rotate(self):
        self.block = self.block.rotated()
