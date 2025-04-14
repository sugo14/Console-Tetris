from blocks import Blocks, Colors
from theme import Theme
import sys

class Board():
    EMPTY_SQUARE = " "
    BOARD_COLOR = Colors.WHITE

    def __init__(self, l = 20, w = 10):
        Theme.load_theme()
        self.l = l
        self.w = w
        self.board = [[(Theme.char("empty")) for i in range(w)] for j in range(l)]
        self.blocks = Blocks()
        self.next_block()

    def block_coords(self):
        return [[x + self.x, y + self.y] for x, y in self.block.coords()]
    
    def at_pos(self, coords):
        x, y = coords
        if not self.coords_in_bounds(coords):
            return '0'
        board_char = self.board[y][x]
        if board_char != Theme.char("empty"):
            return board_char
        return Theme.char("empty")

    def print_at_pos(self, coords):
        return self.block.char() if coords in self.block_coords() else self.at_pos(coords)
    
    def coords_in_bounds(self, coords):
        x, y = coords
        return x >= 0 and x < self.w and y >= 0 and y < self.l
    
    def block_coords_valid(self, coords):
        x, y = coords
        return x >= 0 and x < self.w and y < self.l and (y < 0 or (y >= 0 and self.board[y][x] == Theme.char("empty")))
    
    def block_valid(self):
        for coords in self.block_coords():
            if not self.block_coords_valid(coords):
                return False
        return True

    def next_block(self):
        self.block = self.blocks.next()
        self.x = int(self.w / 2 - self.block.size() / 2)
        self.y = -self.block.size() + 1

    def block_grounded(self):
        coords_list = self.block_coords()
        for coords in coords_list:
            coords[1] += 1
            if not self.block_coords_valid(coords):
                return True
        return False

    def place_square(self, coords, char):
        if not self.coords_in_bounds(coords):
            raise RuntimeError(f"Coords {coords} out of bounds, {char} could not be placed.")
        x, y = coords
        self.board[y][x] = char
    
    def place_block(self):
        for coords in self.block_coords():
            self.place_square(coords, self.block.char())
    
    def drop_block(self):
        while not self.block_grounded():
            self.move_down()
        self.place_block()
        self.next_block()

    def print(self):
        """Prints the current state of the board in a frame."""

        console_width = self.w * 2 + 1
        board_str = "\x1b[2J\x1b[H" + Board.BOARD_COLOR + Theme.char("tl") + Theme.char("hor") * console_width + Theme.char("tr") + '\n'

        for y in range(self.l):
            board_str += Theme.char("vert") + Theme.char("space")
            for x in range(self.w):
                board_str += self.print_at_pos([x, y]) + Board.BOARD_COLOR + Theme.char("space")
            board_str += Theme.char("vert") + "\n"

        board_str += Theme.char("bl") + Theme.char("hor") * console_width + Theme.char("br") + '\n'

        sys.stdout.write(board_str)
        sys.stdout.flush()

    def find_filled_rows(self):
        """Finds all rows that are completely filled and ready for clearing.

        Returns:
            list: The rows that are ready to be cleared.
        """

        rows = []
        for i in range(self.l):
            count = 0
            for j in range(self.w):
                if self.board[i][j] == Theme.char("empty"):
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
        self.board.insert(index, [(Theme.char("empty")) for i in range(self.w)])

    def move_down(self):
        self.y += 1
        if not self.block_valid():
            self.y -= 1

    def move_left(self):
        self.x -= 1
        if not self.block_valid():
            self.x += 1
    
    def move_right(self):
        self.x += 1
        if not self.block_valid():
            self.x -= 1

    def rotate(self):
        self.block = self.block.rotated()
