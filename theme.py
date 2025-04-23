import json
from tui import Screen

class Theme():
    def __init__(self, filename = "clean"):
        self.filename = filename
        self.filepath = f"themes/{filename}.json"
        with open(self.filepath, encoding="UTF_8") as data:
            self.obj = json.load(data)

    def _access(self, path):
        current = self.obj
        for next in path:
            if next not in current:
                raise RuntimeError(f"Path {'/'.join(path)} could not be found in theme at {self.filepath}")
            current = current[next]
        return current
    
    def _colorize(self, char_path, color_path):
        r, g, b = self._access(color_path)
        return Screen.fg_color(r, g, b) + self._access(char_path) + Screen.reset_fg_color()
    
    def frame_char(self, char_name):
        return self._colorize(["chars", char_name], ["fg", "frame"])
    
    def tet_char(self, tetromino):
        return self._colorize(["chars", "block"], ["fg", "tets", tetromino])
    
    def board_space_char(self):
        return self._colorize(["chars", "space"], ["fg", "frame"])
    
    def empty_board_char(self):
        return self._colorize(["chars", "empty"], ["fg", "frame"])
    
    def filled_row_char(self):
        return self._colorize(["chars", "filled"], ["fg", "filled"])
