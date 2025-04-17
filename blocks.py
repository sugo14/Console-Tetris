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
        for name, id in Square._pairs:
            if name == name_of_id:
                return id
        raise RuntimeError(f"Square ID could not be found for name {name_of_id}")
    
    def name(id_of_name):
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
        return Block(self.shape, self.id, self.rotation)
    
    def size(self):
        return len(self.shape)

    def cw_rotated(self):
        block = self.copy()
        for _ in range(3):
            block = block.ccw_rotated()
        return block
    
    # this is awful
    def ccw_rotated(self):
        new_shape = []
        for i in range(len(self.shape) - 1, -1, -1):
            row = []
            for j in range(len(self.shape[0])):
                row.append(self.shape[j][i])
            new_shape.append(row)
        return Block(new_shape, rotation = (self.rotation - 1) % 4, id = self.id)
    
    def to_list(self):
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
        self._block_perm = Blocks._block_list
        random.shuffle(self._block_perm)
        self._index = 0

    def peek(self):
        block = self._block_perm[self._index]
        return Block.copy(block)

    def next(self):
        block = self.peek()
        self._index += 1
        if self._index >= len(Blocks._block_list):
            self._new_permutation()
        return block
