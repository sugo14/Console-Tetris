import random
from theme import Theme

def color(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"

""" class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"\x1b[38;2;{self.r};{self.g};{self.b}m" """
    
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

class Block():
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def copy(block):
        return Block(block.shape, block.color)
    
    def size(self):
        return len(self.shape)

    def rotated(self):
        new_shape = []
        for i in range(len(self.shape) - 1, -1, -1):
            row = []
            for j in range(len(self.shape[0])):
                row.append(self.shape[j][i])
            new_shape.append(row)
        return Block(new_shape, self.color)
    
    def coords(self):
        coords = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    coords.append([len(self.shape) - i - 1, j])
        return coords
    
    def char(self):
        return self.color + Theme.char("block") + Colors.RESET

class Blocks:
    block_list = [
        Block([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], Colors.CYAN),

        Block([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ], Colors.BLUE),

        Block([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ], Colors.ORANGE),

        Block([
            [1, 1],
            [1, 1]
        ], Colors.YELLOW),

        Block([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ], Colors.GREEN),

        Block([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ], Colors.PURPLE),

        Block([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ], Colors.RED),
    ]

    def next():
        return Block.copy(Blocks.block_list[random.randint(0, len(Blocks.block_list) - 1)])
