# Non-default libraries (e.g curses) were disallowed for this project

import ctypes

class Keys():
    # From https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    vk_codes = {
        " ": 0x20,
        "up": 0x26,
        "down": 0x28,
        "left": 0x25,
        "right": 0x27
    }

    _now_down = []
    _last_down = []
    _first_down = []

    def update():
        """Updates the current state of the keys. To be called every frame.

        Returns:
            list[str]: The names of the keys that were pressed this frame.
        """

        Keys._last_down = Keys._now_down
        Keys._now_down = [chr(i) for i in range(ord('a'), ord('z') + 1) if Keys._down(chr(i))]
        Keys._now_down += [name for name in Keys.vk_codes if Keys._down(name)]
        Keys._first_down = [key for key in Keys._now_down if key not in Keys._last_down]
        return Keys._first_down
    
    def down(key):
        """Checks if a key is currently pressed.

        Args:
            key (str): The name of the key.

        Returns:
            bool: True if the key is pressed, False otherwise.s
        """
        return key in Keys._now_down
    
    def all_down():
        """Returns a list of all currently pressed keys.

        Returns:
            list[str]: The names of the keys that are currently pressed.
        """

        return Keys._now_down

    def first_down(key):
        """Checks if a key was first pressed this frame.

        Args:
            key (str): The name of the key.

        Returns:
            bool: True if the key was first pressed this frame, False otherwise.
        """

        return key in Keys._first_down
    
    def all_first_down():
        """Returns a list of all keys that were first pressed this frame.

        Returns:
            list[str]: The names of the keys that were first pressed this frame.
        """

        return Keys._first_down

    def _get_code(key):
        """Returns the virtual key code of a key.

        Returns:
            int or None: The virtual key code of the key, or None if the key is not supported.
        """

        if len(key) == 1 and ord('a') <= ord(key) <= ord('z'):
            return ord(key) - ord('a') + 0x41
        return Keys.vk_codes[key] if key in Keys.vk_codes else None
    
    def _down(key):
        """Checks if a key is currently pressed using its virtual key code.

        Args:
            key (str): The name of the key.

        Returns:
            bool or None: True if the key is pressed, False otherwise, or None if the key is not supported.
        """

        vk_code = Keys._get_code(key)
        return None if vk_code == None else Keys._code_down(vk_code)

    def _code_down(vk_code):
        """Checks if a key is currently pressed using its virtual key code.

        Args:
            vk_code (int): The virtual key code of the key.

        Returns:
            bool: True if the key is pressed, False otherwise.
        """

        return ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000 != 0

class Screen():
    def ANSI(args):
        """Returns a formatted ANSI escape code string.

        Args:
            args (list[str] or str): A list of ANSI escape codes or a single ANSI escape code to be formatted.

        Returns:
            str: The formatted ANSI escape code string.
        """
        return f"\x1b[{args}" if isinstance(args, str) else "".join([f"\x1b[{arg}" for arg in args])
    
    def clear():
        """Returns an ANSI escape code to clear the screen."""

        return Screen.ANSI(["2J", "H"])

    def show_cursor(show):
        """Returns an ANSI escape code to show or hide the cursor."""

        return Screen.ANSI("?25" + ("h" if show else "l"))

    def move_cursor(x, y):
        """Returns an ANSI escape code to move the cursor to a specific position."""

        return Screen.ANSI(f"{y};{x}H")
    
    def fg_color(r, g, b):
        """Returns an ANSI escape code to set the foreground color."""

        return Screen.ANSI(f"38;2;{r};{g};{b}m")
    
    def bg_color(r, g, b):
        """Returns an ANSI escape code to set the background color."""

        return Screen.ANSI(f"48;2;{r};{g};{b}m")
    
    def reset_fg_color():
        """Returns an ANSI escape code to reset the foreground color."""

        return Screen.ANSI(f"0m")
