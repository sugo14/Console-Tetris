import random

class Square():
    _pairs = (
        ("empty", 0),
        ("I", 1),
        ("J", 2),
        ("L", 3),
        ("O", 4),
        ("S", 5),
        ("T", 6),
        ("Z", 7)
    )

    def id(name_of_id):
        """Returns the ID of a square given its name.

        Args:
            name_of_id (str): The name of the square.

        Raises:
            RuntimeError: If the name is not found in the predefined pairs.

        Returns:
            int: The ID of the square.
        """

        for name, id in Square._pairs:
            if name == name_of_id:
                return id
        raise RuntimeError(f"Square ID could not be found for name {name_of_id}")
    
    def name(id_of_name):
        """Returns the name of a square given its ID.

        Args:
            id_of_name (int): The id of the square.

        Raises:
            RuntimeError: If the ID is not found in the predefined pairs.

        Returns:
            str: The name of the square.
        """

        for name, id in Square._pairs:
            if id == id_of_name:
                return name
        raise RuntimeError(f"Square name could not be found for ID {id_of_name}")

class WallKicks():
    _REGULAR_KICKS = {
        (0, 1): [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],
        (1, 0): [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],
        (1, 2): [(0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)],
        (2, 1): [(0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)],
        (2, 3): [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)],
        (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
        (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)],
        (0, 3): [(0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)]
    }

    _I_KICKS = {
        (0, 1): [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
        (1, 0): [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
        (1, 2): [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)],
        (2, 1): [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
        (2, 3): [(0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)],
        (3, 2): [(0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)],
        (3, 0): [(0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)],
        (0, 3): [(0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)]
    }

    _O_KICKS = { }

    _TETROMINO_KICKS = {
        Square.id("I"): _I_KICKS,
        Square.id("J"): _REGULAR_KICKS,
        Square.id("L"): _REGULAR_KICKS,
        Square.id("O"): _O_KICKS,
        Square.id("S"): _REGULAR_KICKS,
        Square.id("T"): _REGULAR_KICKS,
        Square.id("Z"): _REGULAR_KICKS
    }

    def kicks(tetromino_id, from_rot, to_rot):
        """Returns the wall kicks for a given tetromino and rotation.

        Args:
            tetromino_id (int): The ID of the tetromino.
            from_rot (int): The rotation to kick from.
            to_rot (int): The rotation to kick to.

        Raises:
            RuntimeError: If the tetromino ID is not found in the predefined kicks.

        Returns:
            list[tuple[int, int]]: A list of tuples representing the wall kicks.
        """

        if tetromino_id not in WallKicks._TETROMINO_KICKS:
            raise RuntimeError(f"Wall kicks not found for tetromino {Square.name(tetromino_id)} ({tetromino_id})")
        
        kicks = WallKicks._TETROMINO_KICKS[tetromino_id]
        rot_tuple = (from_rot, to_rot)
        if rot_tuple not in kicks:
            return [(0, 0)]
        
        return kicks[rot_tuple]

class Block():
    def __init__(self, shape, id, rotation = 0):
        self.shape = shape
        self.rotation = rotation
        self.id = id
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if id != -1 and self.shape[i][j] == 1:
                    self.shape[i][j] = id

    def copy(self):
        """Creates a shallow copy of the block.

        Returns:
            Block: A new Block object with the same shape, ID, and rotation as the original block.
        """
        return Block(self.shape, self.id, self.rotation)
    
    def size(self):
        """Returns the size of the block.

        Returns:
            int: The size of the block. Blocks have the same size in both dimensions.
        """

        return len(self.shape)

    def cw_rotated(self):
        """Rotates the block 90 degrees clockwise.

        Returns:
            Block: A new Block object that is rotated 90 degrees clockwise from the original block.
        """

        block = self.copy()
        for _ in range(3):
            block = block.ccw_rotated()
        return block
    
    # this is awful
    def ccw_rotated(self):
        """Rotates the block 90 degrees counter-clockwise.

        Returns:
            Block: A new Block object that is rotated 90 degrees counter-clockwise from the original block.
        """

        new_shape = []
        for i in range(len(self.shape) - 1, -1, -1):
            row = []
            for j in range(len(self.shape[0])):
                row.append(self.shape[j][i])
            new_shape.append(row)
        return Block(new_shape, rotation = (self.rotation - 1) % 4, id = self.id)
    
    def to_list(self):
        """Converts the block to a list of coordinates and their corresponding IDs.

        Returns:
            list[tuple(list[int], int)]: A list of tuples where each tuple contains the coordinates of a square and its ID.
        """

        coords = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] != 0:
                    coords.append(([j, i], self.shape[i][j]))
        return coords

class Blocks:
    _block_list = [
        Block([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], Square.id("I")),

        Block([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ], Square.id("J")),

        Block([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ], Square.id("L")),

        Block([
            [1, 1],
            [1, 1]
        ], Square.id("O")),

        Block([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ], Square.id("S")),

        Block([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ], Square.id("T")),

        Block([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]                                                                        
        ], Square.id("Z"))
    ]

    def __init__(self):
        self._new_permutation()

    def _new_permutation(self):
        """Generates a new random permutation of the blocks."""

        self._block_perm = Blocks._block_list
        random.shuffle(self._block_perm)
        self._index = 0

    def peek(self):
        """Returns the current block in the permutation.

        Returns:
            Block: The current block in the permutation.
        """

        block = self._block_perm[self._index]
        return Block.copy(block)

    def next(self):
        """Returns the current block in the permutation and advances the index.

        Returns:
            Block: The current block in the permutation.
        """

        block = self.peek()
        self._index += 1
        if self._index >= len(Blocks._block_list):
            self._new_permutation()
        return block
