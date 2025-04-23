from blocks import Blocks, Square, WallKicks

class Board():
    def __init__(self, l = 20, w = 10):
        self.l = l
        self.w = w
        self.board = [[Square.id("empty")] * w for _ in range(l)]
        self.blocks = Blocks()
        self.points = 0
        self.next_block()

    def block_square_list(self):
        return [([coords[0] + self.x, coords[1] + self.y], id) for coords, id in self.block.to_list()]
    
    def at_pos(self, coords):
        x, y = coords
        if not self.coords_in_bounds(coords):
            return None
        board_square = self.board[y][x]
        if board_square != Square.id("empty"):
            return board_square
        return Square.id("empty")
    
    def points_formula(row_cnt):
        return row_cnt * row_cnt * 500
    
    def update_rows(self):
        rows = self.find_filled_rows()
        self.points += Board.points_formula(len(rows))
        for row in rows:
            self.clear_row(row)

    # TODO: how do i name this function?
    def appearance_at_pos(self, coords):
        for pos, id in self.block_square_list():
            if pos == coords:
                return id
        return self.at_pos(coords)
    
    def coords_in_bounds(self, coords):
        x, y = coords
        return x >= 0 and x < self.w and y >= 0 and y < self.l
    
    def block_coords_valid(self, coords):
        x, y = coords
        return x >= 0 and x < self.w and y < self.l and (y < 0 or (y >= 0 and self.board[y][x] == Square.id("empty")))
    
    def block_valid(self):
        for coords, square in self.block_square_list():
            if not self.block_coords_valid(coords):
                return False
        return True

    def next_block(self):
        # TODO: fix spawn elevation and rotation
        self.block = self.blocks.next()
        self.x = int(self.w / 2 - self.block.size() / 2)
        self.y = 0

    def block_grounded(self):
        coords_list = self.block_square_list()
        # Check if one square below any square in block is occupied
        for coords, square in coords_list:
            coords[1] += 1
            if not self.block_coords_valid(coords):
                return True
        return False

    def place_square(self, coords, square):
        if not self.coords_in_bounds(coords):
            raise RuntimeError(f"Coords {coords} out of bounds, \"{Square.name(square)}\" ({square}) could not be placed.")
        x, y = coords
        self.board[y][x] = square
    
    def place_block(self):
        for coords, square in self.block_square_list():
            self.place_square(coords, square)
    
    def drop_block(self):
        while not self.block_grounded():
            self.move_down()
        self.place_block()
        self.next_block()

    def find_filled_rows(self):
        """Finds all rows that are completely filled and ready for clearing.

        Returns:
            list: The rows that are ready to be cleared.
        """

        return [i for i in range(self.l) if Square.id("empty") not in self.board[i]]
    
    def clear_row(self, index):
        """Deletes a row at an index and adds an empty row in its place.

        Args:
            index (int): The index of the row to empty.
        """

        self.board.pop(index)
        self.board.insert(0, [(Square.id("empty"))] * self.w)

    def move_down(self):
        self.update_rows() # TODO: i don't know if this update should be here
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
        last_rotation = self.block.rotation
        self.block = self.block.cw_rotated()
        curr_rotation = self.block.rotation

        index = 0
        wall_kicks = WallKicks.kicks(self.block.id, last_rotation, curr_rotation)

        # try wall kicks
        while index < len(wall_kicks):
            x_offset, y_offset = wall_kicks[index]
            y_offset = -y_offset # my board is inverted lmao

            self.x += x_offset
            self.y += y_offset

            if self.block_valid():
                return
            index += 1

            # revert
            self.x -= x_offset
            self.y -= y_offset

        # revert rotation
        self.block = self.block.ccw_rotated()

