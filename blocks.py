import random

def color(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"
    
class Colors():
    RED = color(255, 0, 0)
    GREEN = color(0, 255, 0)
    BLUE = color(0, 0, 255)

    YELLOW = color(255, 255, 0)
    CYAN = color(0, 255, 255)
    PURPLE = color(128, 0, 128)
    ORANGE = color(255, 127, 0)

    WHITE = color(255, 255, 255)
    GREY = color(127, 127, 127)

    RESET = "\x1b[0m"

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
        raise RuntimeError(f"ID could not be found for name {name_of_id}")
    
    def name(id_of_name):
        for name, id in Square._pairs:
            if id == id_of_name:
                return name
        raise RuntimeError(f"Name could not be found for ID {id_of_name}")

class Block():
    def __init__(self, shape, id = -1):
        self.shape = shape
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if id != -1 and self.shape[i][j] == 1:
                    self.shape[i][j] = id

    def copy(block):
        return Block(block.shape)
    
    def size(self):
        return len(self.shape)

    def cw_rotated(self):
        new_shape = []
        for i in range(len(self.shape) - 1, -1, -1):
            row = []
            for j in range(len(self.shape[0])):
                row.append(self.shape[j][i])
            new_shape.append(row)
        return Block(new_shape)
    
    def ccw_rotated(self):
        block = Block.copy(self)
        for i in range(3): # haha
            block = block.cw_rotated()
        return block
    
    def to_list(self):
        coords = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] != 0:
                    coords.append(([len(self.shape) - i - 1, j], self.shape[i][j]))
        return coords
    
    """ def char(self):
        return self.color + Theme.char("block") + Colors.RESET """

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

    def next(self):
        block = self._block_perm[self._index]
        self._index += 1
        if self._index >= len(Blocks._block_list):
            self._new_permutation()
        return Block.copy(block)
