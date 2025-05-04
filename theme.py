import json
from tui import Screen

class Theme():
    def __init__(self, filename = "clean"):
        self.filename = filename
        self.filepath = f"themes/{filename}.json"
        with open(self.filepath, encoding="UTF_8") as data:
            self.obj = json.load(data)

    def _access(self, path):
        """Returns the value at a path in the theme object.

        Args:
            path (list[string]): The path to the value in the theme object.

        Raises:
            RuntimeError: If the path could not be found in the theme object.

        Returns:
            Any: The value at the path in the theme object.
        """

        current = self.obj
        for next in path:
            if next not in current:
                raise RuntimeError(f"Path {'/'.join(path)} could not be found in theme at {self.filepath}")
            current = current[next]
        return current
    
    def _colorize(self, char_path, color_path):
        """Returns a colorized character string using ANSI escape codes, following the provided paths.

        Args:
            char_path (list[string]): The path to the string in the theme object.
            color_path (list[string]): The path to the color in the theme object.

        Returns:
            string: The colorized string.
        """

        r, g, b = self._access(color_path)
        return Screen.fg_color(r, g, b) + self._access(char_path) + Screen.reset_fg_color()
    
    def frame_char(self, char_name):
        """Returns a colorized character string for the frame using ANSI escape codes.

        Args:
            char_name (string): The name of the character in the theme object.

        Returns:
            string: The colorized string.
        """

        return self._colorize(["chars", char_name], ["fg", "frame"])
    
    def tet_char(self, tetromino):
        """Returns a colorized character string for a tetromino using ANSI escape codes.

        Args:
            tetromino (string): The name of the tetromino in the theme object.

        Returns:
            string: The colorized string.
        """

        return self._colorize(["chars", "block"], ["fg", "tets", tetromino])
    
    def board_space_char(self):
        """Returns a colorized character string for the board space using ANSI escape codes.

        Returns:
            string: The colorized string.
        """

        return self._colorize(["chars", "space"], ["fg", "frame"])
    
    def empty_board_char(self):
        """Returns a colorized character string for the empty board space using ANSI escape codes.

        Returns:
            string: The colorized string.
        """

        return self._colorize(["chars", "empty"], ["fg", "frame"])
    
    def filled_row_char(self):
        """Returns a colorized character string for the filled row using ANSI escape codes.

        Returns:
            string: The colorized string.
        """

        return self._colorize(["chars", "filled"], ["fg", "filled"])
    