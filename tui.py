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
        Keys._last_down = Keys._now_down
        Keys._now_down = [chr(i) for i in range(ord('a'), ord('z') + 1) if Keys._down(chr(i))]
        Keys._now_down += [name for name in Keys.vk_codes if Keys._down(name)]
        Keys._first_down = [key for key in Keys._now_down if key not in Keys._last_down]
        return Keys._down
    
    def down(key):
        return key in Keys._now_down
    
    def all_down():
        return Keys._now_down

    def first_down(key):
        return key in Keys._first_down
    
    def all_first_down():
        return Keys._first_down

    def _get_code(key):
        if len(key) == 1 and ord('a') <= ord(key) <= ord('z'):
            return ord(key) - ord('a') + 0x41
        return Keys.vk_codes[key] if key in Keys.vk_codes else None
    
    def _down(key):
        vk_code = Keys._get_code(key)
        return None if vk_code == None else Keys._code_down(vk_code)

    def _code_down(vk_code):
        return ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000 != 0
    
class Screen():
    def ANSI(args):
        return f"\x1b[{args}" if args is str else "".join([f"\x1b[{arg}" for arg in args])
    
    def clear():
        return Screen.ANSI(["2J", "H"])

    def show_cursor(show):
        return Screen.ANSI("?25" + ("h" if show == True else "l"))

    def move_cursor(line, column):
        return Screen.ANSI(f"{line};{column}H")
