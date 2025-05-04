from blocks import Blocks, Square, WallKicks

class Board():
    def __init__(self, l = 20, w = 10):
        self._l = l
        self._w = w
        self._board = [[Square.id("empty")] * w for _ in range(l)]
        self._blocks = Blocks()
        self._points = 0
        self._next_block()

    def move_down(self):
        """Attempts to move the current block down by one row."""

        if self._block_grounded():
            self.drop_block()
            return

        self._update_rows() # TODO: i don't know if this update should be here
        self._y += 1
        if not self._block_valid():
            self._y -= 1

    def move_left(self):
        """Attempts to move current block left by one column."""

        self._x -= 1
        if not self._block_valid():
            self._x += 1
    
    def move_right(self):
        """Attempts to move current block right by one column."""
        
        self._x += 1
        if not self._block_valid():
            self._x -= 1

    def rotate(self):
        """Attempts to rotate the current block clockwise."""

        last_rotation = self._block.rotation
        self._block = self._block.cw_rotated()
        curr_rotation = self._block.rotation

        index = 0
        wall_kicks = WallKicks.kicks(self._block.id, last_rotation, curr_rotation)

        # try wall kicks
        while index < len(wall_kicks):
            x_offset, y_offset = wall_kicks[index]
            y_offset = -y_offset # my board is inverted lmao

            self._x += x_offset
            self._y += y_offset

            if self._block_valid():
                return
            index += 1

            # revert
            self._x -= x_offset
            self._y -= y_offset

        # revert rotation
        self._block = self._block.ccw_rotated()

    def drop_block(self):
        """Drops the current block to the bottom of the board."""

        while not self._block_grounded():
            self.move_down()
        self._place_block()
        self._next_block()

    def game_over(self):
        return not self._block_valid()

    def _block_square_list(self):
        """Returns a list of tuples containing the coordinates and id of each square in the block on the board.

        Returns:
            list[tuple(list[int], int)]: A list of tuples where each tuple contains the coordinates of a square and its id.
        """

        return [([coords[0] + self._x, coords[1] + self._y], id) for coords, id in self._block.to_list()]
    
    def _at_pos(self, coords):
        """Returns the square at the given coordinates on the board.

        Args:
            coords (list[int]): The coordinates to check.

        Returns:
            int or None: The id of the square at the given coordinates, or None if the coordinates are out of bounds.
        """

        x, y = coords
        if not self._coords_in_bounds(coords):
            return None
        board_square = self._board[y][x]
        if board_square != Square.id("empty"):
            return board_square
        return Square.id("empty")
    
    def _points_formula(row_cnt):
        """Calculates the points to be earned based on the number of rows cleared at once.

        Args:
            row_cnt (int): The number of rows cleared at once.

        Returns:
            int: The points earned for clearing the rows.
        """

        return row_cnt * row_cnt * 500
    
    def _update_rows(self):
        """Checks for filled rows and clears them.
        """

        rows = self._find_filled_rows()
        self._points += Board._points_formula(len(rows))
        for row in rows:
            self._clear_row(row)

    # TODO: how do i name this function?
    def _appearance_at_pos(self, coords):
        """Returns the id of the square at the given coordinates, taking into account the current block.

        Args:
            coords (list[int]): The coordinates to check.

        Returns:
            int or None: The id of the square at the given coordinates, or None if the coordinates are out of bounds.
        """

        for pos, id in self._block_square_list():
            if pos == coords:
                return id
        return self._at_pos(coords)
    
    def _coords_in_bounds(self, coords):
        """Checks if the given coordinates are within the bounds of the board.

        Args:
            coords (list[int]): The coordinates to check.

        Returns:
            bool: True if the coordinates are within bounds, False otherwise.
        """

        x, y = coords
        return x >= 0 and x < self._w and y >= 0 and y < self._l
    
    def _block_coords_valid(self, coords):
        """Checks if the given coordinates are valid positions for squares for a current block on the board.

        Args:
            coords (int): The coordinates to check.

        Returns:
            bool: True if the coordinates are valid, False otherwise.
        """

        x, y = coords
        return x >= 0 and x < self._w and y < self._l and (y < 0 or (y >= 0 and self._board[y][x] == Square.id("empty")))
    
    def _block_valid(self):
        """Checks if the current block is in a valid position on the board.

        Returns:
            bool: True if the block is valid, False otherwise.
        """

        for coords, square in self._block_square_list():
            if not self._block_coords_valid(coords):
                return False
        return True

    def _next_block(self):
        """Generates a new block and sets its initial position on the board.
        """

        # TODO: fix spawn elevation and rotation
        self._block = self._blocks.next()
        self._x = int(self._w / 2 - self._block.size() / 2)
        self._y = 0

    def _block_grounded(self):
        """Checks if the current block is grounded, meaning if it has reached the bottom of the board or is resting on another block.

        Returns:
            bool: True if the block is grounded, False otherwise.
        """

        coords_list = self._block_square_list()
        # Check if one square below any square in block is occupied
        for coords, square in coords_list:
            coords[1] += 1
            if not self._block_coords_valid(coords):
                return True
        return False

    def _place_square(self, coords, square):
        """Places a square on the board at the given coordinates.

        Args:
            coords (list[int]): The coordinates to place the square at.
            square (int): The id of the square to place.

        Raises:
            RuntimeError: If the coordinates are out of bounds.
        """

        if not self._coords_in_bounds(coords):
            raise RuntimeError(f"Coords {coords} out of bounds, \"{Square.name(square)}\" ({square}) could not be placed.")
        x, y = coords
        self._board[y][x] = square
    
    def _place_block(self):
        """Places the current block on the board at its current position."""

        for coords, square in self._block_square_list():
            self._place_square(coords, square)

    def _find_filled_rows(self):
        """Finds all rows that are completely filled and ready for clearing.

        Returns:
            list: The rows that are ready to be cleared.
        """

        return [i for i in range(self._l) if Square.id("empty") not in self._board[i]]
    
    def _clear_row(self, index):
        """Deletes a row at an index and adds an empty row in its place.

        Args:
            index (int): The index of the row to empty.
        """

        self._board.pop(index)
        self._board.insert(0, [(Square.id("empty"))] * self._w)
